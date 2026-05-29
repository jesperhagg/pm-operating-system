# Context Index

_Machine-facing router. Read this first; open only the file(s) you need.
Anchor lists are refreshed by `/context-sync` — do not hand-edit._

## product/
- `decisions.md` — H2 per decision, newest first. Recent: _(refreshed by `/context-sync`)_
- `strategy.md` — positioning, bets, north-star (living doc).
- `roadmap.md` — Committed / Next / Later.
- `experiments.md` — H2 per experiment.

## market/
- `landscape.md` — competitive snapshot (append-only via `/market-scan`).
- `signals.md` — H3 dated observations. Recent: _(refreshed by `/context-sync`)_
- `archive/` — quarterly rollover from `signals.md`.

## users/
- `personas.md` — H2 per persona.
- `feedback.md` — H3 dated user feedback. Recent: _(refreshed by `/context-sync`)_
- `research.md` — H2 per finding.
- `icp.md` — H2 per ICP (created on first `/ideal-customer-profile` run).

## ops/
- `people.md` — stakeholder profiles.
- `leads.md` — pipeline board.
- `leads-detail/{slug}.md` — per-lead append-only logs.

## learnings/
- `<skill>.md` — per-skill accumulated lessons (created on first capture).
