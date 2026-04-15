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
- Agents do not orchestrate workflows. They do not hydrate Notion. They
  do not spawn peers. They do not write files. They respond as a chat
  persona — worldview, principles, pushback.
- If you find yourself writing "the agent will..." in a skill, stop.
  Rewrite the step so the skill does it itself.

## Skill Design Pattern

Every skill follows a four-phase execution pattern:

1. **Hydration** — Identify the current product from the host repo's
   CLAUDE.md. Fetch Notion context (decisions, personas, backlog, recent
   Signals) as needed. Summarize context to the user before proceeding.
   For internal skills not tied to a product (e.g., pm-digest), hydration
   means loading memory and scanning existing capabilities instead.
2. **Framework** — Apply a domain-specific, opinionated structure (scoring
   rubric, template, decomposition rules, etc.). The framework is the core
   intellectual property of the skill. It must be concrete and produce a
   specific output every time — if it reads like generic advice, it is not
   a skill.
3. **Output** — Produce structured markdown with a consistent heading
   format. Specify the destination: conversation (default), a file (only
   when the skill explicitly says so, e.g., write-prd), or Notion (e.g.,
   log-decision).
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
- Memory Protocol (Notion writes, quality signals)
- Boundaries with redirect tables

**Why:** Skills own methodology, hydration, output, and memory. Agents
respond in-chat conversationally. If an agent needs Notion context, the
user invokes a skill first.

## Notion Integration Rules (Skills Only)

- Notion is the source of truth for all product data. Never fabricate or
  assume product context.
- Implement session-level caching: fetch once per product per conversation,
  reuse unless (a) user requests fresh data or (b) a write operation just
  completed.
- If Notion MCP is unavailable for a product-context skill, halt and say
  so explicitly. Do not proceed with invented context.
- If a Notion MCP write fails, fall back to local
  `.claude/memory/shared.md` with structured format.
- Tavily unavailability degrades gracefully: skip web-sourced sections and
  note the limitation.
- **Agents do NOT call Notion MCP.** If you need Notion context during a
  conversation, invoke the relevant skill first (e.g., `/fetch-context`).

## Multi-Mode Skill Design

When a skill manages a Notion resource, it may have multiple modes:

- Example: `/knowledge` has Fetch/Store/Review; `/tasks` has
  View/Update/Add.
- Document trigger phrases for each mode in the SKILL.md.
- Default mode should be the most common read operation.
- Modes share the same Notion database schema section.
- Each mode has its own step-by-step procedure.

## Product-Agnostic Principle

- This repo contains zero product data.
- Skills are frameworks that pull context at runtime via Notion MCP.
- Product identity comes from the host repo's CLAUDE.md.
- Never hardcode product names, personas, features, or terminology into
  skill or agent definitions.
- Litmus test: "Would this skill work identically for a different product
  with different Notion data?" If not, it is not product-agnostic.

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

Memory is a two-layer system:

1. **Notion (primary)** — The three context databases are the source of
   truth, each with a distinct role per the **DB Routing Rubric** in
   `.claude/context/notion-schemas.md`:
   - **Decisions** holds commitments the PM has made.
   - **Signals** holds time-stamped observations (user feedback, competitive
     moves, market signals, technical constraints, internal learnings).
   - **Knowledge Base** holds durable, synthesized understanding (people,
     reference, research, market landscapes).
   All three are filtered by Product.
2. **Local files (secondary)** — `.claude/memory/shared.md` stores
   cross-agent learnings and user preferences. It also serves as a
   fallback when Notion MCP is unavailable — Signals or Decisions writes
   that fail should be mirrored here in structured format for later sync.

**Key properties:**

- Memory files are created at runtime in consumer repos (product repos
  that install this plugin), NOT in this plugin source repo.
- Each consumer repo gets its own memory file, providing implicit
  product isolation.
- `.claude/memory/` is gitignored to prevent accidental commits.
- **Plugin updates never touch memory files** — they live outside the
  plugin's scope. Updating the plugin is safe.
- If Notion fallback entries accumulate in `shared.md`, the `/tasks`
  session-start check will prompt syncing them back to Notion.
- The `memory-review` skill curates these files in consumer repos.

## Pre-Commit Review

Before committing changes to `skills/`, `.claude/skills/`, `agents/`,
`.claude/context/dev-standards.md`, or `.claude-plugin/plugin.json`, run
`/design-review` for an advisory check. It's advisory, not blocking —
Jesper makes the call.
