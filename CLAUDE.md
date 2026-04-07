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
   `/evaluate-opportunity`, `/log-decision`, `/weekly-review`)

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
