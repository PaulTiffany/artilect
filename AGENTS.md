# Artilect production instructions

You are in a creator-owned repository that will produce a real creative artifact (usually a video) and record how it was made. This is not the Artilect website or event-management repository.

Given a request like "Make a music video about robot jazz using X, Y, and Z for Artilect":

1. Identify **the original upstream Git repositories** for the requested technologies. Confirm what each does, licensing, realistic installation requirements, and whether their versions interoperate. Don't swap requested technologies without explaining why and obtaining the creator's consent.
2. Add each upstream repository **directly** with `git submodule add https://github.com/owner/project.git technologies/project`. Use distinct safe folder names. No copied vendor trees, fake gitlinks, third-party wrapper stack repositories, or nested stack manifests standing in for the originals. Commit the resulting `.gitmodules` and gitlinks. At least two independently developed upstream technologies.
3. Actually use these technologies to create the requested work, testing a real output if execution is possible. Put production scripts, configuration, prompts, and settings in `production/`. Save small outputs to `output/`; host big media externally and link it. Never commit secrets, paid assets, model weights, or large generated video by default.
4. Fill in `artilect.json` with the title, concise summary, media URL or committed media path, and reproduction instruction. Make the top of `README.md` show the creative result, then explain how to reproduce/remix and credit every original upstream creator, license, and dependency. Name blockers honestly.
5. Run `python scripts/validate.py`. Fix failed checks. Prepare a GitHub repository URL for the creator to submit at https://github.com/PaulTiffany/artilect/issues/new?template=stack.yml. Do not submit/publish or deploy without the creator's approval.

**Boundaries:** Source availability does not guarantee working installation. Do not execute unknown upstream code without appropriate review/sandboxing and permission. Never invent a working render, verified source, license, execution receipt, or attribution. Keep README short: show the finished work first, instructions second. A human controls creative choices and publication.

The four hip-hop foundations inform the culture (DJing, MCing, breaking, graffiti); they are not paperwork or mandatory classifications.
