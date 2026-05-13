---
description: Deprecated. Use /context-init + /context-sync instead.
---

# Migrate From Notion — Deprecated

This skill has been replaced by `/context-init` + `/context-sync`.

- `/context-init` — scaffolds the `context/` + `tasks/` layout and
  creates the Notion routing config (`context/.notion-routing.md`).
- `/context-sync` — performs the incremental pull from Notion (and Gmail)
  into `context/` files, including first-run full sync.

For initial migration from a Notion workspace: run `/context-init` to
configure routing, then `/context-sync` to pull all content.
