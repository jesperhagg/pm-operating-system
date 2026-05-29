# Context

Product context for this repo. One product per repo — the repo IS the
product. PM OS skills read and write these files directly; no external
database.

`INDEX.md` is the machine-facing router (refreshed by `/ctx-context-sync`).
Skills consult it first to scope which files to open.

## Layout

- `product/decisions.md` — commitments made (H2 per decision, newest first).
- `product/strategy.md` — positioning, bets, north-star.
- `product/roadmap.md` — committed / next / later.
- `product/experiments.md` — active hypotheses + outcome log.
- `market/landscape.md` — living competitive doc (append-only scans).
- `market/signals.md` — market and competitive observations.
- `users/personas.md` — customer personas (H2 per persona).
- `users/feedback.md` — user-feedback signal stream.
- `users/research.md` — domain research and literature.
- `ops/people.md` — stakeholder profiles.
- `ops/leads.md` — pipeline board.
- `ops/leads-detail/` — one file per lead (append-only interaction log).
- `learnings/<skill>.md` — per-skill accumulated lessons (created on first
  capture by a looped skill).

See the plugin's `.claude/context/context-schemas.md` for frontmatter and
file conventions.
