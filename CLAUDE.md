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

## Conventions

- Agents live in `.claude/agents/<agent-name>/AGENT.md`
- Skills live in `.claude/skills/<skill-name>/SKILL.md`
- Product context lives in `/<ProductName>/CLAUDE.md`
- Digests and artifacts are output directly in the conversation, not
  written to files, unless the user asks to save them.
