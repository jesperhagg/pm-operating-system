# PM OS — Conventions and Development Standards

## File Conventions

- Skills live in `skills/<skill-name>/SKILL.md`
- Agents live in `agents/<agent-name>/AGENT.md`
- Commands live in `commands/<command-name>.md`
- MCP config template lives in `.mcp.json.example`
- Digests and artifacts are output directly in the conversation, not
  written to files, unless the user asks to save them.

## Architecture — Skills-First

**Skills are self-sufficient. Agents are lightweight chat personas.**

- Skills own their methodology. They do not delegate reasoning to agents.
  If a skill needs a framework, the framework is embedded in SKILL.md.
- Agents do not orchestrate workflows. They do not hydrate data. They
  do not spawn peers. They do not write files. They respond as a chat
  persona — worldview, principles, pushback.
- If you find yourself writing "the agent will..." in a skill, stop.
  Rewrite the step so the skill does it itself.

## Skill Design Pattern

Every skill follows a four-phase execution pattern:

1. **Hydration** — Identify the current product from the host repo's
   CLAUDE.md (one product per repo). Read targeted files from `context/`
   (decisions, signals, personas, research, people) and `tasks/`. Use grep
   for metadata filtering before opening full H2 sections. Summarize context
   to the user before proceeding.
   For internal skills not tied to a product (e.g., pm-digest), hydration
   means loading any local context and scanning existing capabilities.
2. **Framework** — Apply a domain-specific, opinionated structure (scoring
   rubric, template, decomposition rules, etc.). The framework is the core
   intellectual property of the skill. It must be concrete and produce a
   specific output every time — if it reads like generic advice, it is not
   a skill.
3. **Output** — Produce structured markdown with a consistent heading
   format. Specify the destination: conversation (default), a `data/`
   file (writer skills), or a `docs/` artifact (e.g., `/write-prd`).
4. **Follow-ups** — Suggest 1-3 specific next skills to chain. Follow-ups
   must be contextual (not a generic menu) and reference the skill name
   with slash-command syntax. Only suggest skills that actually exist.

## Agent Design Pattern — Lightweight Chat Persona

Agents are 40–70 line chat personas. No orchestrator machinery.

**Required section order:**

1. Frontmatter (`name`, `description`)
2. **Persona** — one paragraph. Grounded in a real mental model (e.g.,
   "YC partner + McKinsey EM", "Linear/Vercel Lead PM"). Not a generic
   "helpful advisor."
3. **Decision Principles** — 3–5 bullets. What this agent optimizes for
   when faced with a tradeoff.
4. **Challenge Style** — 2–4 bullets. How the agent pushes back (tone,
   cadence, what it demands from the user).
5. **What I Push Back On** — 5–8 specific, quotable anti-patterns. Each
   is a concrete behavior the agent flags, not a category.
6. **Out of Scope** — one-line note. What the agent won't try to do
   (defers to skills, other agents, or the user).

**Forbidden sections (these are orchestrator drift):**

- Objectives (Primary / Success / Failure)
- Proactive Checks
- Product Context / Repo Context hydration blocks
- Capabilities (When / What I Do / Output / Follow-up)
- Output Format templates
- Collaboration Protocol (scratchpad, handoffs)
- Memory Protocol (data writes, quality signals)
- Boundaries with redirect tables

**Why:** Skills own methodology, hydration, output, and memory. Agents
respond in-chat conversationally. If an agent needs product context, the
user invokes a skill first.

## Data Layer Rules (Skills Only)

- Product context lives in `context/` + `tasks/`. The repo IS the product —
  one product per repo. There is no `Product` filter.
- Skills read and write `context/` and `tasks/` directly via Read, Write,
  Edit, Glob, Grep. No external database, no fallback buffer.
- Filter by inline metadata comments (grep for `status:Active`, `type:`,
  `date:`) before opening full H2 sections. Read only the sections you need.
- If `context/` does not exist, surface it to the user — suggest `/context-init`.
- Caching across skill invocations is forbidden. Files are cheap; stale
  reads are dangerous. Always read fresh.
- **Agents do NOT touch `context/`.** Agents are chat personas — they react
  to whatever the user pasted. If an agent needs context, the user invokes
  a skill first.

## Context Layer Routing Rules

When writing context, follow the routing rubric in `context-schemas.md`. Quick reference:

| Content type | Target file |
|---|---|
| Commitment we're making | `context/product/decisions.md` (H2 block) |
| Market / competitive observation | `context/market/signals.md` (H3 block) |
| User feedback signal | `context/users/feedback.md` (H3 block) |
| Internal learning / experiment | `context/product/experiments.md` (H2 block) |
| Synthesized persona | `context/users/personas.md` (H2 block) |
| Research / domain knowledge | `context/users/research.md` (H2 block) |
| Stakeholder profile | `context/ops/people.md` (H2 block) |
| Strategy / positioning / reference | `context/product/strategy.md` |
| Competitive landscape | `context/market/landscape.md` (append-only, /market-scan only) |
| Prospect / lead | `context/ops/leads-detail/{slug}.md` + `context/ops/leads.md` board |
| Active tasks | `tasks/active.md` |
| Governance / conflict tasks | `tasks/governance.md` (/context-sync only) |

**Write skills** must add `session:pending` to new blocks. `/context-sync`
resolves these by changing to `session:synced` after source reconciliation.
Never write `session:synced` manually.

## Multi-Mode Skill Design

When a skill manages a `data/` resource type, it may have multiple modes:

- Example: `/knowledge` has Fetch/Store/Review; `/tasks` has
  View/Update/Add.
- Document trigger phrases for each mode in the SKILL.md.
- Default mode should be the most common read operation.
- Modes share the same on-disk schema section.
- Each mode has its own step-by-step procedure.

## Product-Agnostic Principle

- This template repo contains zero product data.
- Skills are frameworks that read product data from `context/` at runtime
  in the product repo.
- Product identity comes from the product repo's CLAUDE.md.
- Never hardcode product names, personas, features, or terminology into
  skill or agent definitions.
- Litmus test: "Would this skill work identically for a different product
  with different `context/` content?" If not, it is not product-agnostic.

## Layout Conventions

- All skills in `skills/` and agents in `agents/` are auto-discovered by
  Claude Code when this template is copied as `.claude/` in a product repo.
- No enumeration is required — Claude Code discovers them from directories.
- Commands in `commands/` are available as slash commands in the product repo.

## Frontmatter Conventions

- Skills use `description` in frontmatter (required). May optionally
  include `name`.
- Agents use both `name` and `description` in frontmatter (required).
- Descriptions should be one sentence, action-oriented, and mention the
  key framework or approach.

## Memory Convention

The `context/` and `tasks/` directories are the durable memory of the
product repo. They hold product context: decisions, signals, personas,
research, leads, tasks. See `context/context-schemas.md` for the full layout.

`.claude/memory/shared.md` is a lightweight local buffer for **cross-agent
learnings and user preferences** that don't belong in product context
(e.g., "Jesper prefers digests as bullets, not prose"). It is NOT a
fallback for any write failures. The `/context-sync` skill and session-start
hook together keep context fresh and surfaced.

**Key properties:**

- `context/` and `tasks/` are created and committed in the product repo.
  Template updates never touch them.
- `.claude/memory/shared.md` lives in the product repo and is gitignored
  to prevent accidental commits of personal learnings.
- `context/.sync-state.json` is machine-written by `/context-sync` only.
  Never edit it manually.
- Template updates never touch product-repo `context/`, `tasks/`, or memory files.

## Pre-Commit Checklist (Skills, Agents, Plugin Infrastructure)

Before committing changes to `skills/`, `agents/`, `commands/`, or
`dev-standards.md`:

1. **Diff check** — `git diff --stat HEAD` to confirm scope of changes.
2. **Standards compliance** — verify changed files against the relevant
   section above (Skill Design Pattern, Agent Design Pattern, etc.).
3. **Cross-file consistency** — if multiple skills/agents changed, check
   they follow the same patterns. If a new skill is added, confirm
   follow-ups in other skills reference it correctly.
4. **REPO-MAP** — run `/generate-repo-map` if files were added or removed.

Advisory — Jesper makes the call.
