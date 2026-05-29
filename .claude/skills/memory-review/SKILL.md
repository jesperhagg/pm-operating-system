---
description: Deprecated. Use /ctx-context-sync instead.
---

# Memory Review — Deprecated

This skill has been replaced by `/ctx-context-sync`, which handles:

- **Staleness detection** — compares `context/.sync-state.json` timestamps
  against per-file thresholds and writes governance tasks when files are stale.
- **Conflict resolution** — detects semantic contradictions between sources
  and writes them to `tasks/governance.md` for PM review.
- **Session memory reconciliation** — resolves `session:pending` annotations
  written by write skills during sessions.

Run `/ctx-context-sync` to refresh the context layer and surface stale entries.
Run `/ops-weekly-review` to see open governance tasks alongside the weekly summary.
