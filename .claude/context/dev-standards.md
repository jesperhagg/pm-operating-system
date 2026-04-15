# PM OS — Conventions and Development Standards

## File Conventions

- Plugin-exported skills live in `skills/<skill-name>/SKILL.md`
- Internal skills live in `.claude/skills/<skill-name>/SKILL.md`
- Agents live in `.claude/agents/<agent-name>/AGENT.md`
- Plugin manifest lives in `.claude-plugin/plugin.json`
- Marketplace listing lives in `.claude-plugin/marketplace.json`
- MCP config template lives in `.mcp.json.example`
- Digests and artifacts are output directly in the conversation, not
  written to files, unless the user asks to save them.

## PM OS Creator Authority

**The `pm-os-creator` agent is the lead architect for this repo. Its
architectural recommendations take precedence over ad-hoc analysis.**

When working on this repo (not a consumer repo), follow these rules:

- **Design work:** For ANY modification to agent definitions, skill
  definitions, plugin architecture, or Development Standards, consult
  `pm-os-creator` FIRST. It must lead the design — do not bypass it
  with generic exploration or independent synthesis.
- **Analysis work:** When analyzing the repo's structure, patterns, or
  gaps, route through `pm-os-creator` as the primary analyst. Use
  Explore agents to gather raw data, but `pm-os-creator` interprets
  the findings and makes the architectural call.
- **Review gate:** Before committing changes to files in `skills/`,
  `.claude/skills/`, `.claude/agents/`, or `CLAUDE.md` Development
  Standards, run `/design-review` to get pm-os-creator's sign-off.
- **Override:** Only the user (Jesper) can override a pm-os-creator
  recommendation. If you disagree with its architectural call, present
  both perspectives to the user and let them decide.

This exists because the pm-os-creator has the full context of the plugin's
design patterns, conventions, and consistency requirements. Bypassing it
leads to drift.

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

## Notion Integration Rules

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

## Multi-Mode Skill Design

When a skill manages a Notion resource, it may have multiple modes:

- Example: `/knowledge` has Fetch/Store/Review; `/tasks` has
  View/Update/Add.
- Document trigger phrases for each mode in the SKILL.md.
- Default mode should be the most common read operation.
- Modes share the same Notion database schema section.
- Each mode has its own step-by-step procedure.

## Agent Design Conventions

Standard section order for AGENT.md files:

1. Frontmatter (name, description)
2. Identity paragraph
3. Tone and Behavior
4. Objectives (Primary Objective, Success Looks Like, Failure Looks Like)
5. Proactive Checks (data-driven conditions assessed during hydration)
6. Product Context (or Repo Context for internal agents)
7. Capabilities (structured as: When, What I Do, Output, Follow-up skills)
8. Anti-Patterns to Call Out
9. Output Format
10. Collaboration Protocol
11. Memory Protocol
12. Boundaries

Rules:
- Every product-facing agent must include the Product Context block (read
  host CLAUDE.md, fetch from Notion, ask if ambiguous).
- Every product-facing agent must include Objectives that define a
  measurable outcome the agent works toward, not just a response style.
- Every product-facing agent must include Proactive Checks — data-driven
  conditions assessed against Notion context during hydration, surfaced as
  "Before we dive in, I noticed..." observations before responding.
- Collaboration Protocol is always one-hop, uses
  `.claude/scratchpad/handoff.md`, requires scoped questions and
  attribution.
- Memory Protocol always reads before analysis and writes (with user
  permission) after significant interactions. Includes quality signal
  capture (user accepts/rejects/modifies recommendations).
- Boundaries explicitly redirect to the correct agent/skill for
  out-of-scope requests.

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
- `.claude/skills/<name>/SKILL.md` — internal, only available in this repo.
- `.claude/agents/<name>/AGENT.md` — internal, agents are not
  plugin-exported.
- When adding a new exported skill, also update `.claude-plugin/plugin.json`.
- When adding a new internal skill or agent, do NOT update plugin.json.
- Marketplace listing (`.claude-plugin/marketplace.json`) is updated only
  for significant releases.

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
