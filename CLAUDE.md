# PM Operating System

A personal "PM Operating System" — a collection of Claude Code skills,
templates, and workflows for AI-augmented product management.

## Multi-Product Setup

This repo manages PM work across three independent products. Each product has
its own folder tree with a dedicated `CLAUDE.md` containing product-specific
context, terminology, constraints, and conventions.

| Product | Domain | Folder |
|---|---|---|
| **Sagokraft** | AI-adaptive children's reading companion (Swedish, ages 4-8) | `/Sagokraft` |
| **Selftaped** | Mobile self-tape audition app for independent actors | `/Selftaped` |
| **FellingPal** | Forestry compliance assistant for Swedish small-scale forest owners | `/FellingPal` |

**Important:** The three products have completely different users, domains,
design philosophies, and terminology. Never cross-pollinate context between
them — each product's framing, personas, and conventions apply only within
its own folder.

When working on a product-specific task, read the relevant product `CLAUDE.md`
first to load the correct context.

### Dynamic Build Context

Each product's external repo contains a `context.md` describing the current
build state. Run `scripts/fetch-context.sh` to fetch and cache these locally
at `/<Product>/context.md`. Requires `GITHUB_TOKEN` env var with repo read
access. These files are gitignored. The fetch runs automatically on session
start via a SessionStart hook.

## Skills

- `/pm-digest` — generates a daily digest of PM + AI news, trends,
  and actionable insights by searching the web and synthesizing findings.
- `/market-scan <product>` — scans the competitive landscape for a specific
  product (sagokraft, selftaped, or fellingpal), discovering competitors,
  recent launches, funding signals, and customer sentiment.

## Agents

- `startup-advisor` — an analytical startup advisor (YC partner + McKinsey
  consultant) that pressure-tests GTM strategy, moat, unit economics, and
  prioritization. Allergic to feature creep. Works across all products.
- `product-sculptor` — minimalist PM who sculpts MVPs to their atomic core.
  Defines backlogs, user flows, and 48-hour feature scopes. Obsessed with
  Time to Value. Writes per-product backlog files.
- `growth-engineer` — distribution-first growth specialist. Advisory by
  default, produces copy when asked. Designs pre-launch funnels, cold
  outreach, and landing page positioning. Any customer-facing copy skills
  should consult this agent.
- `ai-systems-lead` — pragmatic technical architect for AI-native products.
  Architecture only (no code). Cost-models AI features, selects models,
  and prevents runaway API bills.

## Agent Collaboration

Agents can automatically collaborate by spawning each other when they need
expertise outside their domain. Each agent has a Collaboration Protocol that
defines who it can consult and how.

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

## Memory

The system maintains lightweight persistent memory across sessions:

- `/<Product>/memory.md` — product-specific decisions, insights, and open
  questions (one per product)
- `.claude/memory/shared.md` — cross-cutting: user preferences, cross-agent
  learnings, portfolio patterns

Agents read relevant memory before analysis and propose writing to memory
after significant decisions. Memory is append-only with size caps (30
decisions, 20 insights, 10 open questions per product). Use `/memory-review`
to prune stale entries.

## Skills

- `/pm-digest` — generates a daily digest of PM + AI news, trends,
  and actionable insights by searching the web and synthesizing findings.
- `/market-scan <product>` — scans the competitive landscape for a specific
  product (sagokraft, selftaped, or fellingpal), discovering competitors,
  recent launches, funding signals, and customer sentiment.
- `/memory-review` — reviews memory files, identifies stale entries, and
  proposes archival to keep memory lean and relevant.

## Conventions

- Agents live in `.claude/agents/<agent-name>/AGENT.md`
- Skills live in `.claude/skills/<skill-name>/SKILL.md`
- Product context lives in `/<ProductName>/CLAUDE.md`
- Build context lives in `/<ProductName>/context.md` (fetched, gitignored)
- Product memory lives in `/<ProductName>/memory.md`
- Scripts live in `scripts/`
- Shared memory lives in `.claude/memory/shared.md`
- Digests and artifacts are output directly in the conversation, not
  written to files, unless the user asks to save them.
