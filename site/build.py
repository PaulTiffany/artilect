#!/usr/bin/env python3
"""Build a static Artilect stage from accepted direct Git submodules and GitHub issues.

Runs from the trusted site-source branch. Never clones, installs or executes
contributed upstream software.
"""
from __future__ import annotations

import configparser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = Path(os.environ.get("ARTILECT_ROOT", ".")).resolve()
OUT = Path(os.environ.get("ARTILECT_OUT", "_pages")).resolve()
HERE = Path(__file__).resolve().parent
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "PaulTiffany/artilect")
BASE = "https://github.com/" + REPOSITORY

def field(body: str, name: str) -> str:
    marker = "### " + name
    at = body.find(marker)
    if at < 0:
        return ""
    value = body[at + len(marker):].split("\n### ", 1)[0].strip()
    return "" if value == "_No response_" else value

def get_issues() -> list[dict]:
    token = os.environ.get("GITHUB_TOKEN", "")
    issues = []
    for page in range(1, 11):
        req = urllib.request.Request(
            f"https://api.github.com/repos/{REPOSITORY}/issues?state=all&per_page=100&page={page}",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "artilect-site-builder",
                **({"Authorization": f"Bearer {token}"} if token else {}),
            },
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            batch = json.load(resp)
        issues.extend(x for x in batch if "pull_request" not in x)
        if len(batch) < 100:
            break
    return issues

def stacks() -> list[dict]:
    modules = ROOT / ".gitmodules"
    if not modules.exists():
        return []
    config = configparser.ConfigParser(interpolation=None)
    config.read(modules, encoding="utf8")
    compositions: dict[tuple[str, str], dict] = {}
    for section in config.sections():
        if not section.startswith('submodule "') or not section.endswith('"'):
            continue
        path = config.get(section, "path", fallback="")
        url = config.get(section, "url", fallback="")
        m = re.fullmatch(r"stacks/(\d{4}-\d{2}-\d{2})/([a-z0-9][a-z0-9_-]{0,38})/([a-z0-9_.-]+)", path)
        if not m or not re.fullmatch(r"https://github\.com/[A-Za-z0-9-]+/[A-Za-z0-9_.-]+(?:\.git)?", url):
            continue
        # Pull exact Gitlink SHA from the approved Artilect commit, not from upstream HEAD.
        tree_line = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-tree", "HEAD", "--", path],
            text=True,
        ).strip()
        match = re.match(r"160000 commit ([0-9a-f]{40})\t", tree_line)
        if not match:
            continue
        week, contributor, name = m.groups()
        entry = compositions.setdefault(
            (week, contributor),
            {
                "week": week,
                "contributor": contributor,
                "technologies": [],
                "github": BASE + "/tree/main/stacks/" + week + "/" + contributor,
                "demo": "",
                "notes": "",
                "issue_url": "",
            },
        )
        entry["technologies"].append({
            "name": name,
            "url": url.removesuffix(".git"),
            "revision": match.group(1),
        })
    return sorted(compositions.values(), key=lambda e: (e["week"], e["contributor"]), reverse=True)

def build():
    accepted = stacks()
    issues = get_issues()
    by_key = {(s["week"], s["contributor"]): s for s in accepted}
    accepted_paths = {"stacks/" + s["week"] + "/" + s["contributor"] for s in accepted}
    battles = []
    for issue in issues:
        title = issue.get("title") or ""
        body = issue.get("body") or ""
        labels = {x.get("name", "").lower() for x in issue.get("labels", [])}
        if title.startswith("[STACK]"):
            week = field(body, "Week (YYYY-MM-DD)")
            contributor = field(body, "Contributor GitHub handle").lower()
            s = by_key.get((week, contributor))
            if s:
                s["demo"] = field(body, "Demo video or audio URL (optional)")
                s["notes"] = field(body, "What can your composition do, and who made the upstream work?")
                s["issue_url"] = issue.get("html_url", "")
                s["selected"] = "selected-stack" in labels
        elif title.startswith("[BATTLE]") and ("showcase" in labels or "winner" in labels):
            week = field(body, "Battle week (YYYY-MM-DD)")
            producer = field(body, "Producer or battler")
            path = field(body, "Selected stack path").rstrip("/")
            media = field(body, "Video/audio URL")
            if (not re.fullmatch(r"\d{4}-\d{2}-\d{2}", week)
                or path not in accepted_paths
                or not path.startswith("stacks/" + week + "/")
                or not media.startswith(("https://", "http://"))):
                continue
            battles.append({
                "week": week, "producer": producer[:100], "stack": path,
                "stack_url": BASE + "/tree/main/" + path,
                "media": media, "notes": field(body, "What did you flip? Upstream credits and production notes")[:3000],
                "winner": "winner" in labels,
                "issue_url": issue.get("html_url", ""),
            })
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "index.html", OUT / "index.html")
    (OUT / "site-data.json").write_text(
        json.dumps({"stacks": accepted, "battles": battles},
                   indent=2, ensure_ascii=False), encoding="utf8"
    )
    (OUT / ".nojekyll").write_text("", encoding="utf8")
    print(f"Built Artilect stage: {len(accepted)} accepted stacks, {len(battles)} approved battles")

if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print("Artilect build failed:", e, file=sys.stderr)
        raise
