# PM OS — Conventions and Development Standards

## File Conventions

- Plugin-exported skills live in `skills/<skill-name>/SKILL.md`
- Internal skills (plugin-dev only) live in `.claude/skills/<skill-name>/SKILL.md`
- Agents live in `agents/<agent-name>/AGENT.md` (top-level — exported to consumer repos)
- Plugin manifest lives in `.claude-plugin/plugin.json`
- Marketplace listing lives in `.claude-plugin/marketplace.json`
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
   CLAUDE.md (one product per repo). Read targeted files from `data/`
   (decisions, signals, personas, knowledge, tasks). Read indexes
   (`data/decisions/index.md`, `data/personas/index.md`) before opening
   individual files. Summarize context to the user before proceeding.
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

- Product data lives in the consumer repo at `data/`. The repo IS the
  product — one product per repo. There is no `Product` filter field.
- Skills read and write `data/` directly via Read, Write, Edit, Glob,
  Grep. No MCP fetch, no external database, no fallback buffer.
- Hydrate from indexes first (`data/decisions/index.md`,
  `data/personas/index.md`), then open targeted files.
- Filter by frontmatter, not by reading bodies. Open a body only when
  the entry passes the filter.
- If a `data/` directory or specific file is missing for the current
  task, surface that explicitly to the user — do not invent context.
- Caching across skill invocations is forbidden. Files are cheap; stale
  reads are dangerous. Always read fresh.
- **Agents do NOT touch `data/`.** Agents are chat personas — they react
  to whatever the user pasted. If an agent needs context, the user
  invokes a skill first.

## Multi-Mode Skill Design

When a skill manages a `data/` resource type, it may have multiple modes:

- Example: `/knowledge` has Fetch/Store/Review; `/tasks` has
  View/Update/Add.
- Document trigger phrases for each mode in the SKILL.md.
- Default mode should be the most common read operation.
- Modes share the same on-disk schema section.
- Each mode has its own step-by-step procedure.

## Product-Agnostic Principle

- This plugin repo contains zero product data.
- Skills are frameworks that read product data from `data/` at runtime
  in the consumer repo.
- Product identity comes from the host repo's CLAUDE.md.
- Never hardcode product names, personas, features, or terminology into
  skill or agent definitions.
- Litmus test: "Would this skill work identically for a different product
  with different `data/` content?" If not, it is not product-agnostic.

## Plugin Export Conventions

- `skills/<name>/SKILL.md` — exported via plugin, available in consumer
  repos.
- `agents/<name>/AGENT.md` — exported via plugin, available in consumer
  repos.
- `.claude/skills/<name>/SKILL.md` — internal (plugin-dev only), only
  available in this repo.
- Plugin manifest (`.claude-plugin/plugin.json`) gets a version bump when
  exported skills or agents change materially. Skills and agents are
  auto-discovered from their directories — no enumeration required.
- Marketplace listing (`.claude-plugin/marketplace.json`) is updated only
  for significant releases or description changes.

## Frontmatter Conventions

- Skills use `description` in frontmatter (required). May optionally
  include `name`.
- Agents use both `name` and `description` in frontmatter (required).
- Descriptions should be one sentence, action-oriented, and mention the
  key framework or approach.

## Memory Convention

The `data/` directory is the durable memory of the consumer repo. It
holds product facts: decisions, signals, knowledge, personas, tasks.
See `.claude/context/data-schemas.md` for the full layout.

`.claude/memory/shared.md` is a lightweight local buffer for **cross-agent
learnings and user preferences** that don't belong in product data
(e.g., "Jesper prefers digests as bullets, not prose"). It is NOT a
fallback for failed `data/` writes — there are no failures to fall back
from. The `/memory-review` skill curates this file alongside `data/`.

**Key properties:**

- `data/` is created and committed in the consumer repo (one product
  per repo). Plugin updates never touch it.
- `.claude/memory/shared.md` lives in the consumer repo and is
  gitignored to prevent accidental commits of personal learnings.
- Plugin updates never touch consumer-repo `data/` or memory files.
- The `/memory-review` skill walks `data/**/*.md` and `shared.md` for
  staleness, redundancy, and pruning candidates.

## Pre-Commit Checklist (Skills, Agents, Plugin Infrastructure)

Before committing changes to `skills/`, `.claude/skills/`, `agents/`,
`dev-standards.md`, or `plugin.json`:

1. **Diff check** — `git diff --stat HEAD` to confirm scope of changes.
2. **Standards compliance** — verify changed files against the relevant
   section above (Skill Design Pattern, Agent Design Pattern, etc.).
3. **Cross-file consistency** — if multiple skills/agents changed, check
   they follow the same patterns. If a new skill is added, confirm
   follow-ups in other skills reference it correctly.
4. **REPO-MAP** — run `/generate-repo-map` if files were added or removed.

Advisory — Jesper makes the call.
