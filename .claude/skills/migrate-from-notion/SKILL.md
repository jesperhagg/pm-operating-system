---
description: Deprecated. Use /ctx-context-init + /ctx-context-sync instead.
---

# Migrate From Notion — Deprecated

This skill has been replaced by `/ctx-context-init` + `/ctx-context-sync`.

- `/ctx-context-init` — scaffolds the `context/` + `tasks/` layout and
  creates the Notion routing config (`context/.notion-routing.md`).
- `/ctx-context-sync` — performs the incremental pull from Notion (and Gmail)
  into `context/` files, including first-run full sync.

For initial migration from a Notion workspace: run `/ctx-context-init` to
configure routing, then `/ctx-context-sync` to pull all content.
