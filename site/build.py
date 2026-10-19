#!/usr/bin/env python3
"""Artilect Pages: weekly creator productions and their direct upstream gitlinks.

Read ONLY Git metadata, tracked JSON, and approved issue text. Never checkout,
install, import, or execute contributor repositories or upstream submodules.
"""
from __future__ import annotations

import base64
import configparser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(os.environ.get("ARTILECT_ROOT", ".")).resolve()
OUT = Path(os.environ.get("ARTILECT_OUT", "_pages")).resolve()
HERE = Path(__file__).resolve().parent
STARTER = Path(os.environ.get("ARTILECT_TEMPLATE", "_starter_src")).resolve()
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "PaulTiffany/artilect")
BASE = "https://github.com/" + REPOSITORY
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def api(path: str):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "artilect-stage",
            **({"Authorization": "Bearer " + TOKEN} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)

def file_at(owner: str, repo: str, path: str, sha: str) -> str:
    q = urllib.parse.quote(sha, safe="")
    doc = api(f"/repos/{owner}/{repo}/contents/{path}?ref={q}")
    if doc.get("type") != "file" or not doc.get("content"):
        raise ValueError("Missing GitHub file " + path)
    return base64.b64decode(doc["content"]).decode("utf8")

def field(body: str, name: str) -> str:
    marker = "### " + name
    pos = body.find(marker)
    if pos < 0:
        return ""
    value = body[pos + len(marker):].split("\n### ", 1)[0].strip()
    return "" if value == "_No response_" else value

def get_issues() -> list[dict]:
    issues = []
    for page in range(1, 11):
        batch = api(f"/repos/{REPOSITORY}/issues?state=all&per_page=100&page={page}")
        issues.extend(x for x in batch if "pull_request" not in x)
        if len(batch) < 100:
            break
    return issues

def pinned_source(path: str) -> str | None:
    line = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-tree", "HEAD", "--", path], text=True
    ).strip()
    match = re.match(r"160000 commit ([a-f0-9]{40})\t", line)
    return match.group(1) if match else None

def source_metadata(url: str, revision: str) -> dict:
    """Read production recipe and nested *direct* upstream pointers via REST only."""
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)(?:\.git)?", url)
    if not match:
        raise ValueError("Unrecognized creator repository URL")
    owner, repo = match.groups()
    meta = json.loads(file_at(owner, repo, "artilect.json", revision))
    modules = file_at(owner, repo, ".gitmodules", revision)
    commit = api(f"/repos/{owner}/{repo}/git/commits/{revision}")
    tree = api(f"/repos/{owner}/{repo}/git/trees/{commit['tree']['sha']}?recursive=1")
    if tree.get("truncated"):
        raise ValueError("Production tree was truncated")
    gitlinks = {t["path"]: t["sha"] for t in tree.get("tree", [])
                if t.get("mode") == "160000"}
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read_string(modules)
    technologies = []
    for section in cfg.sections():
        path = cfg.get(section, "path", fallback="")
        source = cfg.get(section, "url", fallback="")
        if (not re.fullmatch(r"technologies/[A-Za-z0-9_.-]+", path)
            or path not in gitlinks
            or not re.fullmatch(r"https://github\.com/[A-Za-z0-9-]+/[A-Za-z0-9_.-]+(?:\.git)?", source)):
            continue
        technologies.append({
            "name": path.split("/", 1)[1],
            "url": source.removesuffix(".git"),
            "revision": gitlinks[path],
        })
    return {
        "title": meta.get("title", ""),
        "summary": meta.get("summary", ""),
        "demo": meta.get("media_url", ""),
        "media_path": meta.get("media_path", ""),
        "reproduce": meta.get("reproduce", ""),
        "technologies": technologies,
    }

def stacks() -> list[dict]:
    registry = ROOT / ".gitmodules"
    if not registry.is_file() or not registry.stat().st_size:
        return []
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(registry, encoding="utf8")
    productions = []
    for section in cfg.sections():
        if not section.startswith('submodule "'):
            continue
        path = cfg.get(section, "path", fallback="")
        url = cfg.get(section, "url", fallback="").removesuffix(".git")
        found = re.fullmatch(r"stacks/(\d{4}-\d{2}-\d{2})/([a-z0-9][a-z0-9_-]{0,38})", path)
        if not found:
            continue
        rev = pinned_source(path)
        if rev is None:
            continue
        week, contributor = found.groups()
        record = {
            "week": week,
            "contributor": contributor,
            "github": url + "/tree/" + rev,
            "artilect_url": BASE + "/tree/main/" + path,
            "repo_url": url,
            "revision": rev,
            "title": contributor + "'s production",
            "notes": "",
            "demo": "",
            "technologies": [],
            "issue_url": "",
            "selected": False,
        }
        try:
            meta = source_metadata(url, rev)
            record["title"] = meta["title"] or record["title"]
            record["notes"] = meta["summary"]
            record["demo"] = meta["demo"]
            if not record["demo"] and meta["media_path"]:
                record["demo"] = url + "/blob/" + rev + "/" + meta["media_path"]
            record["technologies"] = meta["technologies"]
        except Exception as exc:
            print(f"Warning: cannot read production {path} at {rev}: {exc}", file=sys.stderr)
            record["notes"] = "Production metadata temporarily unavailable; inspect the pinned repository."
        productions.append(record)
    return sorted(productions, key=lambda r: (r["week"], r["contributor"]), reverse=True)

def export_starter():
    if not (STARTER / "AGENTS.md").is_file() or not (STARTER / "SKILL.md").is_file():
        raise RuntimeError("submission-template checkout missing")
    output = OUT / "artilect-starter.zip"
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(STARTER.rglob("*")):
            if (not f.is_file() or ".git" in f.relative_to(STARTER).parts):
                # Keep .github workflow; skip only the Git checkout metadata.
                continue
            relative = f.relative_to(STARTER).as_posix()
            z.write(f, "artilect-production/" + relative)
    # Zip contains exactly the starter branch's template files. No submodules or binaries.
    print("Exported", output.name)

def build():
    accepted = stacks()
    by_key = {(s["week"], s["contributor"]): s for s in accepted}
    accepted_paths = {"stacks/" + s["week"] + "/" + s["contributor"] for s in accepted}
    battles = []
    for issue in get_issues():
        title, body = issue.get("title") or "", issue.get("body") or ""
        labels = {x.get("name", "").lower() for x in issue.get("labels", [])}
        if title.startswith("[STACK]"):
            week = field(body, "Week (YYYY-MM-DD)")
            handle = (issue.get("user", {}).get("login") or "").lower()
            entry = by_key.get((week, handle))
            if entry:
                entry["issue_url"] = issue.get("html_url", "")
                entry["selected"] = "selected-stack" in labels
        elif title.startswith("[BATTLE]") and ({"showcase", "winner"} & labels):
            week = field(body, "Battle week (YYYY-MM-DD)")
            producer = field(body, "Producer or battler")
            path = field(body, "Selected stack path").rstrip("/")
            media = field(body, "Video/audio URL")
            if (path not in accepted_paths or not path.startswith("stacks/" + week + "/")
                or not media.startswith("https://")):
                continue
            battles.append({
                "week": week, "producer": producer[:100], "stack": path,
                "stack_url": BASE + "/tree/main/" + path, "media": media,
                "notes": field(body, "What did you flip? Upstream credits and production notes")[:3000],
                "winner": "winner" in labels, "issue_url": issue.get("html_url", ""),
            })
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "index.html", OUT / "index.html")
    (OUT / ".nojekyll").write_text("", encoding="utf8")
    (OUT / "site-data.json").write_text(
        json.dumps({"stacks": accepted, "battles": battles}, indent=2, ensure_ascii=False),
        encoding="utf8",
    )
    export_starter()
    print(f"Built: {len(accepted)} accepted production repos, {len(battles)} approved battle entries")

if __name__ == "__main__":
    build()
