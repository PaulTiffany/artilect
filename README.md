# ARTILECT

**Bring the subs. Drop the stack. Pass the mic. All glory upstream.**

Artilect is an upstream-first AI production cypher. We don't ask you to invent the instruments. We ask what you can make when you **sample, compose, and celebrate other people's technology**.

**Wednesday:** bring a stack, give a short demo (2–3 minutes), credit its upstream creators. The community chooses a stack and, when two producers are available, puts it in the hands of two battlers. They go bar for bar, branch for branch, making original audio, video, scenes, and remixes with the same technology. The audience inspires the next move. Next meetup, screen the results and pass the mic.

**Steal the show, not the credit.**

[See the stage (GitHub Pages)](https://paultiffany.github.io/artilect/) · [Drop a stack](../../issues/new?template=stack.yml) · [Drop a battle entry](../../issues/new?template=battle.yml) · [Browse submissions](../../issues)

## The rule: upstream first

1. **Not your featured technology.** Demonstrate a thoughtful *combination* of independently created upstream projects. Your direction, artistry, selection, configuration, and minimal integration glue are yours.
2. **Direct submodules, no wrappers.** Artilect records each upstream source as a **direct Git submodule** at `stacks/YYYY-MM-DD/<contributor>/<technology>/`. The nominated stack is that directory. No stack-repository submodule in between.
3. **Show and credit.** Name the upstream authors, link each original repository, and demonstrate what the combination makes possible. Give credit again in released media.
4. **Same samples, different flips.** Battlers start from the selected, pinned submodule set. They can direct and make original art, but do not silently replace the shared technologies during a round.
5. **Be transparent.** Disclose paid/proprietary services, compute needs, manual steps, and generative-media provenance. Source availability is **not** the same as one-click installability.
6. **Respect creators and audiences.** Respect licenses, permissions, consent, and platform policies. Do not present synthetic real-world footage as documentary evidence.

There is no mandatory polished film and no promise of a battle every week. Rough demos and honest failures are welcome; the people come first.

## Submit a stack

**Easiest:** [open the submission template](../../issues/new?template=stack.yml). Enter the Wednesday date (`YYYY-MM-DD`), your GitHub handle, **two or more** public upstream GitHub repositories (one URL per line), a demonstration link if you have one, and credit/usage notes.

A GitHub Action validates public repository URLs and proposes a pull request that pins each technology to the current default-branch commit. A maintainer reviews and merges it. The actual files under `stacks/` are Git submodule *gitlinks*, not copied upstream code, contributor wrapper repos, or installed dependencies.

```text
README.md                 ← rulebook / contributing guide
LICENSE                   ← MIT for Artilect's own code
.gitmodules               ← Git's direct upstream URLs
stacks/
  2026-10-21/
    paul/
      blender-mcp/        ← upstream Git submodule
      soundcraft/         ← upstream Git submodule
    larry/
      project-a/          ← upstream Git submodule
      project-b/          ← upstream Git submodule
```

*The names above illustrate the layout, not actual accepted stacks.*

For a battler or passerby:

```bash
git clone https://github.com/PaulTiffany/artilect.git
cd artilect
git submodule update --init --depth 1 -- stacks/YYYY-MM-DD/contributor/
```

This downloads that contributor's **pinned source revisions**, subject to repository accessibility. It does **not** install runtimes, model weights, or operating-system packages. Inspect unfamiliar code before executing it. For submodules whose pinned commit is unavailable by a shallow fetch, rerun that update without `--depth 1`.

## Bring a track

[Submit a battle entry](../../issues/new?template=battle.yml) with the week's selected stack path, an accessible video/audio link, and credits. Artilect Pages collects approved stacks from Git history and performances from public submission issues. Producers retain their own media and tools; Artilect links to or embeds permitted media rather than copying large files into Git.

The MC only needs to host the conversation, choose the stack and battlers with the community, review proposed changes, and mark featured entries in issues when appropriate. GitHub Actions handles refreshing the site on merges, issue activity, and a weekly schedule.

## How to play

*A short video walkthrough will live here when one has been produced.* Until then: **pick upstream projects → drop URLs through the issue template → merge the resulting direct submodules → demo → community selects → two battlers flip → share and credit.**

## Licenses and boundaries

- `LICENSE` (MIT) covers **Artilect's original software**, not its submodule targets.
- Artilect-authored README text and site design/content are offered under **CC BY 4.0**, unless otherwise noted. Contributors retain ownership of their submitted content and grant only the permissions they explicitly give for Artilect showcases.
- **Every upstream project keeps its own license and attribution.** A submodule pointer never relicenses upstream code. Confirm model, asset, music, and API terms before publication.
- BGI Nexus is a community gathering context, not an automatic transfer of participant IP to any organization.

**The technology is theirs. The creativity is ours. The credit travels upstream.**
