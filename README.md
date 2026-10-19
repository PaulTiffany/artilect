# ARTILECT

**Bring the subs. Drop the stack. Pass the mic. All glory upstream.**

An upstream-first AI production cypher, inspired by hip-hop's four foundations: **DJing, MCing, breaking, graffiti**. We make things using other people's technologies—and credit their creators.

**Wednesday: MC battles.** Bring finished work and its production repo. The crowd chooses what to feature, and two producers can battle, remix and answer each other. We don't have to force a matchup when fewer people show up.

[**THE STAGE ↗**](https://paultiffany.github.io/artilect/) · [**EXPORT STARTER ↓**](https://paultiffany.github.io/artilect/artilect-starter.zip) · [**DROP YOUR REPO ↗**](../../issues/new?template=stack.yml)

## Make a thing

Download the starter above or [browse its source](../../tree/submission-template). Tell your favorite GPT, Claude, or other coding agent:

> Read AGENTS.md. Make a music video about [SUBJECT] using [X], [Y], and [Z] for Artilect. Produce the actual media, use direct upstream Git submodules, document how to make something similar, credit the creators, and prepare my submission. Go.

**Your finished GitHub repo is both the work and the recipe.** It contains your production process, assets you may legally share, and exact versions of the sampled technologies.

```text
my-creative-production/
├── README.md          # Watch it; reproduce it; credit its makers
├── AGENTS.md          # Agent-readable production instructions
├── SKILL.md           # Portable agent skill instructions
├── artilect.json      # Short, predictable gallery metadata
├── .gitmodules        # URLs of the original upstream repositories
├── technologies/      # Direct Git submodules: X, Y, Z
├── production/        # Scripts, prompts, settings, reproducibility
└── output/            # Small media files or links to hosted video
```

**[Submit that production repository URL](../../issues/new?template=stack.yml)** for a Wednesday. GitHub Actions validates it and proposes **one pinned submodule per contributor's completed production** under:

```text
artilect/
├── README.md
├── LICENSE
├── .gitmodules
└── stacks/
    └── YYYY-MM-DD/
        ├── paul/        # Paul's complete production repository
        └── larry/       # Larry's complete production repository
```

Each contributed repo has its own **direct** upstream technology submodules. No need to copy or repackage anyone's source. An Artilect visitor can recursively retrieve a selected production and its technologies:

```bash
git clone https://github.com/PaulTiffany/artilect.git
cd artilect
git submodule update --init --recursive -- stacks/YYYY-MM-DD/contributor
```

Fetching source does **not** install software, model weights, or external dependencies. That's why every submitted repo includes a production recipe.

## Rules, short version

- Show something **actually made** with at least two independently developed upstream technologies. The production repo must contain their direct Git submodules, pinned in Git history.
- Credit upstream authors and licenses, respect media permissions, and describe any paid components, missing dependencies, or manual steps. Never invent a successful render.
- Keep big videos out of Git when practical; link to them from `artilect.json` and your README.
- Your creative work remains yours. Artilect preserves links, provenance and approved showcases; each upstream project retains its own license.

Need to submit an additional battle performance? [Drop a battle entry](../../issues/new?template=battle.yml). Hosts mark approved entries `showcase` and optional `winner`. Select a featured production by labeling its stack issue `selected-stack`.

GitHub Actions collects and publishes the weekly gallery automatically. The MC handles the people, the battle and the mic; Actions handles the receipts. The site and export implementation live on separate branches to keep this `main` readable.

**Steal the show, not the credit.**
