---
description: Pull the latest pm-os submodule commits from the remote.
---

Update the pm-os submodule to the latest version:

1. Run `git submodule update --remote --merge` from the repo root.
2. Show the new HEAD commit for the submodule (run `git submodule status`).
3. If new commits were pulled, read `.claude/REPO-MAP.md` inside the submodule and briefly summarise what changed (new skills, agents, or commands).
4. If already up to date, confirm with one line.
