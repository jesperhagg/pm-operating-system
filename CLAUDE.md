## Who I Am

- **Name:** Jesper
- **Role:** <!-- Fill in: e.g., Solo founder / PM -->
- **Background:** <!-- Fill in: skills, experience, domain expertise -->
- **Working style:** <!-- Fill in: e.g., "bias toward action", "systems thinker" -->
- **What energizes me:** <!-- Fill in -->
- **What drains me:** <!-- Fill in -->

## Purpose & Strategy

### Why This Exists
<!-- Fill in: 1-2 sentences on the vision for this PM operating system -->

### Current Goals
<!-- Fill in: quarterly goals with metrics, baselines, targets -->

### Ownership Areas
<!-- Fill in: products/areas this PM system supports -->

### Personal Development
<!-- Fill in: skills being developed, growth areas -->

## How to Work With Me

### Skill Routing

When I mention these keywords, run the corresponding skill:

| When I say... | Run... |
|---|---|
| "evaluate", "opportunity", "score" | `/evaluate-opportunity` |
| "PRD", "spec", "requirements" | `/write-prd` |
| "break down", "decompose", "tasks from this" | `/break-down` |
| "competitors", "market", "landscape" | `/market-scan` |
| "decision", "log", "decided" | `/log-decision` |
| "review", "weekly", "what shipped" | `/weekly-review` |
| "memory", "clean up", "stale" | `/memory-review` |
| "digest", "news", "what's happening" | `/pm-digest` |
| person name, "stakeholder", "who is" | `/knowledge people` |
| "research", "insights", "what do we know about" | `/knowledge research` |
| "my tasks", "what am I working on", "what's active" | `/tasks` |

### MCP Usage

- **Notion** is the source of truth for all product data. Never fabricate
  product context — always fetch from Notion first.
- **Tavily** is for web search only. Use it for market scans and digests,
  not for product context.
- If Notion MCP is unavailable, say so explicitly. Do not proceed with
  stale or invented context.
- If Tavily MCP is unavailable, degrade gracefully and note the limitation.

### Session Start

At the start of every conversation, run `/tasks` to show my active work
before asking what I need. Skip if I say "skip tasks".

### Working Style

- Be direct. No preamble, no filler, no encouragement padding.
- Challenge my assumptions when you see weak reasoning — with specifics,
  not generic pushback.
- Default to action: suggest the next concrete step, not a menu of options.
- Ask before writing files, creating PRs, or taking irreversible actions.
- When making a recommendation, state the tradeoff explicitly.
- When stuck, ask one focused clarifying question — not a list.

### Context Rules

- When asking about a **product** → fetch context from Notion via
  `/fetch-context`
- When preparing for a **meeting** → check Knowledge Base (People category)
  for stakeholder profiles via `/knowledge people`
- When making a **strategic decision** → reference the Purpose & Strategy
  section above and prior decisions from Notion
- When **context window is getting full** → proactively summarize and
  suggest what to offload to Notion

### Agent Escalation

If my question is strategic and cross-cutting, suggest the appropriate
agent rather than answering generically:

- GTM, moat, unit economics → `startup-advisor`
- MVP scoping, feature cuts, backlogs → `product-sculptor`
- Distribution, funnels, positioning → `growth-engineer`
- AI architecture, cost modeling → `ai-systems-lead`

### Memory Hygiene

After any session where a significant decision was made, prompt me to run
`/log-decision`. Do not log without asking.

### What NOT to Do

- Do not write files unless I ask.
- Do not assume product details — always ground in Notion data.
- Do not recommend capabilities I already have (check the skills list).
- Do not ask 5 clarifying questions when the answer is inferrable from
  context.

## MCP Servers

| Server | Purpose | Required By | Degradation |
|--------|---------|-------------|-------------|
| Notion | Product context, knowledge, tasks, decisions | All skills except `/pm-digest` | Fatal — say so explicitly, do not proceed |
| Tavily | Web search + content extraction | `/market-scan`, `/pm-digest` | Graceful — skip web-sourced sections, note limitation |

---

# PM Operating System — Claude Code Plugin

A product-agnostic Claude Code plugin that encodes PM frameworks as reusable
skills. Skills work in any product repo — they query Notion via MCP for live
product context, so every analysis is grounded in your actual roadmap.

## What This Repo Is

A Claude Code plugin and marketplace listing. It contains:

- **Skills** — slash commands that encode repeatable PM workflows (PRDs,
  opportunity scoring, market scans, work decomposition, decision logging,
  weekly reviews)
- **Agents** — specialized reasoning roles (startup advisor, product sculptor,
  growth engineer, AI systems lead) that collaborate via a one-hop protocol
- **Internal skills** — non-exported skills for personal PM workflows

This repo contains **zero product data**. Product identity, personas,
terminology, and context live in each product repo's own `CLAUDE.md` and
in Notion databases. Skills here are frameworks — they pull context at
runtime via Notion MCP.

## Prerequisites

Two MCP servers are required:

1. **Tavily** — web search and content extraction (`/pm-digest`,
   `/market-scan`)
2. **Notion** — live product context (`/fetch-context`, `/write-prd`,
   `/evaluate-opportunity`, `/log-decision`, `/weekly-review`,
   `/knowledge`, `/tasks`)

Additionally, two Notion databases are expected:

3. **Knowledge Base** — a Notion database with properties: Title (text),
   Category (select: `People`, `Reference`, `Research`), Product
   (multi-select), Tags (multi-select). Used by `/knowledge`.
4. **Backlog / Tasks** — a Notion database with task status, priority,
   product, and blocker fields. Used by `/tasks` and `/fetch-context`.

Setup:

1. Copy `.mcp.json.example` to `.mcp.json`
2. Replace `YOUR_TAVILY_API_KEY` with your Tavily API key
3. Replace `YOUR_NOTION_TOKEN` with your Notion integration token
4. Restart your Claude Code session

The `.mcp.json` file is gitignored (it contains your API keys).

## Skills

### Plugin-exported skills (in `skills/`)

- `/fetch-context` — fetches live product context from Notion (decisions,
  personas, backlog, signals). Foundation skill used by other PM skills.
- `/write-prd` — writes a PRD using a 6-section framework, auto-hydrated
  with live Notion context.
- `/evaluate-opportunity` — scores an opportunity on 5 dimensions (Market,
  Competitive, Founder Fit, Feasibility, Strategic Fit) with Explore/Park/Kill.
- `/market-scan <product>` — scans the competitive landscape for a product,
  discovering competitors, recent launches, funding signals, and customer
  sentiment.
- `/memory-review` — reviews memory files, identifies stale entries, and
  proposes archival to keep memory lean and relevant.
- `/break-down` — decomposes a PRD into kanban-ready work items using JTBD
  framing, WIP limits, and pull-based flow.
- `/weekly-review` — portfolio-level weekly operating rhythm: what shipped,
  what's blocked, what's next.
- `/log-decision` — logs a product decision to Notion with structured
  metadata (product, type, status, impact).
- `/knowledge` — fetches, stores, and reviews structured knowledge in
  Notion (People, Reference, Research). Inspired by local knowledge
  directories but backed by Notion as the data layer.
- `/tasks` — surfaces active tasks from the Notion backlog with sprint-
  style formatting (in progress, waiting on, up next). Runs at session
  start by default.

### Internal skills (in `.claude/skills/`)

- `/pm-digest` — generates a daily digest of PM + AI news, trends,
  and actionable insights by searching the web and synthesizing findings.

## Agents

- `startup-advisor` — analytical startup advisor (YC + McKinsey lens) that
  pressure-tests GTM strategy, moat, unit economics, and prioritization.
- `product-sculptor` — minimalist PM who sculpts MVPs to their atomic core.
  Defines backlogs, user flows, and tight feature scopes.
- `growth-engineer` — distribution-first growth specialist. Advisory by
  default, produces copy when asked. Pre-launch funnels, cold outreach,
  landing page positioning.
- `ai-systems-lead` — pragmatic technical architect for AI-native products.
  Architecture only — no code. Cost-models AI features, selects models.

### Agent Collaboration

Agents can spawn each other when they need expertise outside their domain.

- **One-hop rule:** An agent may spawn exactly one other agent as a
  consultant. The consulted agent cannot spawn a third.
- **Scratchpad:** Collaboration uses `.claude/scratchpad/handoff.md` as a
  shared working file (transient, not committed).
- **Attribution:** Agent output clearly labels which parts came from a
  consulted agent.

| Agent | Can consult |
|---|---|
| startup-advisor | growth-engineer, ai-systems-lead |
| product-sculptor | ai-systems-lead, growth-engineer |
| growth-engineer | startup-advisor, product-sculptor |
| ai-systems-lead | product-sculptor, startup-advisor |

## Conventions

- Plugin-exported skills live in `skills/<skill-name>/SKILL.md`
- Internal skills live in `.claude/skills/<skill-name>/SKILL.md`
- Agents live in `.claude/agents/<agent-name>/AGENT.md`
- Plugin manifest lives in `.claude-plugin/plugin.json`
- Marketplace listing lives in `.claude-plugin/marketplace.json`
- MCP config template lives in `.mcp.json.example`
- Digests and artifacts are output directly in the conversation, not
  written to files, unless the user asks to save them.
- When developing skills or agents for this repo, use the
  `pm-os-creator` agent for architectural guidance and consistency audits.

## Development Standards

These standards govern how skills, agents, and plugin infrastructure are
built and maintained in this repo. They codify patterns extracted from the
existing codebase — follow them when creating or modifying any skill or
agent.

### Skill Design Pattern

Every skill follows a four-phase execution pattern:

1. **Hydration** — Identify the current product from the host repo's
   CLAUDE.md. Fetch Notion context (decisions, personas, backlog, signals)
   as needed. Summarize context to the user before proceeding. For internal
   skills not tied to a product (e.g., pm-digest), hydration means loading
   memory and scanning existing capabilities instead.
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

### Notion Integration Rules

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

### Multi-Mode Skill Design

When a skill manages a Notion resource, it may have multiple modes:

- Example: `/knowledge` has Fetch/Store/Review; `/tasks` has
  View/Update/Add.
- Document trigger phrases for each mode in the SKILL.md.
- Default mode should be the most common read operation.
- Modes share the same Notion database schema section.
- Each mode has its own step-by-step procedure.

### Agent Design Conventions

Standard section order for AGENT.md files:

1. Frontmatter (name, description)
2. Identity paragraph
3. Tone and Behavior
4. Product Context (or Repo Context for internal agents)
5. Focus Areas
6. Anti-Patterns to Call Out
7. Output Format
8. Collaboration Protocol
9. Memory Protocol
10. Boundaries

Rules:
- Every product-facing agent must include the Product Context block (read
  host CLAUDE.md, fetch from Notion, ask if ambiguous).
- Collaboration Protocol is always one-hop, uses
  `.claude/scratchpad/handoff.md`, requires scoped questions and
  attribution.
- Memory Protocol always reads before analysis and writes (with user
  permission) after significant interactions.
- Boundaries explicitly redirect to the correct agent/skill for
  out-of-scope requests.

### Product-Agnostic Principle

- This repo contains zero product data.
- Skills are frameworks that pull context at runtime via Notion MCP.
- Product identity comes from the host repo's CLAUDE.md.
- Never hardcode product names, personas, features, or terminology into
  skill or agent definitions.
- Litmus test: "Would this skill work identically for a different product
  with different Notion data?" If not, it is not product-agnostic.

### Plugin Export Conventions

- `skills/<name>/SKILL.md` — exported via plugin, available in consumer
  repos.
- `.claude/skills/<name>/SKILL.md` — internal, only available in this repo.
- `.claude/agents/<name>/AGENT.md` — internal, agents are not
  plugin-exported.
- When adding a new exported skill, also update `.claude-plugin/plugin.json`.
- When adding a new internal skill or agent, do NOT update plugin.json.
- Marketplace listing (`.claude-plugin/marketplace.json`) is updated only
  for significant releases.

### Frontmatter Conventions

- Skills use `description` in frontmatter (required). May optionally
  include `name`.
- Agents use both `name` and `description` in frontmatter (required).
- Descriptions should be one sentence, action-oriented, and mention the
  key framework or approach.

### Memory Convention

- Skills and agents reference `.claude/memory/shared.md` and
  `.claude/memory/shared-archive.md` in their Memory Protocol sections.
- These files are created at runtime in consumer repos (product repos that
  install this plugin), NOT in this plugin source repo.
- This repo should never contain memory files — they would hold personal
  or product-specific data.
- `.claude/memory/` is gitignored to prevent accidental commits.
- The `memory-review` skill operates on these files in consumer repos.
  When running it in this repo, it will correctly report no entries to
  review.
