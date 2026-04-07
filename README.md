# PM Operating System

A Claude Code plugin that encodes PM frameworks as reusable slash commands.
Skills query Notion via MCP for live product context — so every analysis is
grounded in your actual roadmap, not hypotheticals.

## What it is

A product-agnostic PM skills marketplace for solo founders. Skills wrap
repeatable PM work (PRDs, opportunity evaluation, market scans, work
decomposition, decision logging, weekly reviews) in Claude Code slash
commands. Agents handle deeper reasoning across startup advisor, product
sculptor, growth engineer, and AI systems lead roles.

No product data lives here — skills are frameworks that pull context at
runtime from Notion.

## Prerequisites

Two MCP servers are required:

1. **Tavily** — web search and content extraction
2. **Notion** — live product context (decisions, personas, backlog, signals)

Setup:

1. Copy `.mcp.json.example` to `.mcp.json`
2. Replace `YOUR_TAVILY_API_KEY` with your Tavily API key
3. Replace `YOUR_NOTION_TOKEN` with your Notion integration token
4. Restart your Claude Code session

The `.mcp.json` file is gitignored.

## Install

```bash
claude plugin marketplace add <path-or-github-url>
```

## Structure

```
.claude-plugin/
  plugin.json              # Plugin manifest (skills + agents)
  marketplace.json         # Marketplace listing
skills/                    # Plugin-exported skills
  fetch-context/           # Foundation: fetch live Notion context
  write-prd/               # Write PRDs with 6-section framework
  evaluate-opportunity/    # 5-dimension opportunity scoring
  market-scan/             # Competitive landscape scanning
  memory-review/           # Memory curation and archival
  break-down/              # PRD → kanban-ready work items
  weekly-review/           # Portfolio-level weekly operating rhythm
  log-decision/            # Log decisions to Notion
.claude/
  agents/                  # Agent definitions
    startup-advisor/       # GTM, moat, unit economics
    product-sculptor/      # MVP scoping, JTBD backlogs
    growth-engineer/       # Distribution, funnels, copy
    ai-systems-lead/       # AI architecture, cost modeling
  skills/                  # Internal skills (not plugin-exported)
    pm-digest/             # Daily PM + AI news digest
  settings.json            # Permissions + status line
```

## Skills

| Skill | Purpose |
|-------|---------|
| `/fetch-context` | Fetch live product context from Notion |
| `/write-prd` | Write a PRD using proven PM frameworks |
| `/evaluate-opportunity` | Score an opportunity (Explore/Park/Kill) |
| `/market-scan <product>` | Scan competitive landscape |
| `/memory-review` | Review and prune memory files |
| `/break-down` | Decompose PRD into kanban-ready work items |
| `/weekly-review` | Weekly portfolio review |
| `/log-decision` | Log a decision to Notion |
| `/pm-digest` | Daily PM + AI news digest (internal, requires Tavily) |

## Agents

| Agent | Role |
|-------|------|
| `startup-advisor` | Pressure-tests GTM, moat, unit economics |
| `product-sculptor` | Sculpts MVPs to atomic core, defines backlogs |
| `growth-engineer` | Distribution-first, pre-launch funnels and copy |
| `ai-systems-lead` | AI architecture, cost modeling, model selection |
