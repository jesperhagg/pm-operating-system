# PM Operating System

A personal "PM Operating System" — a collection of Claude Code skills,
templates, and workflows for AI-augmented product management.

## Multi-Product Setup

This repo manages PM work across two independent products. Each product has
its own folder tree with a dedicated `CLAUDE.md` containing product-specific
context, terminology, constraints, and conventions.

| Product | Domain | Folder |
|---|---|---|
| **Sagokraft** | AI-adaptive children's reading companion (Swedish, ages 4-8) | `/Sagokraft` |
| **Selftaped** | Mobile self-tape audition app for independent actors | `/Selftaped` |

**Important:** The two products have completely different users, domains,
design philosophies, and terminology. Never cross-pollinate context between
them — do not apply Sagokraft's educational framing to Selftaped, and do not
apply Selftaped's consumer/speed-first approach to Sagokraft.

When working on a product-specific task, read the relevant product `CLAUDE.md`
first to load the correct context.

## Skills

- `/pm-digest` — generates a daily digest of PM + AI news, trends,
  and actionable insights by searching the web and synthesizing findings.
- `/market-scan <product>` — scans the competitive landscape for a specific
  product (sagokraft or selftaped), discovering competitors, recent launches,
  funding signals, and customer sentiment.

## Conventions

- Skills live in `.claude/skills/<skill-name>/SKILL.md`
- Product context lives in `/<ProductName>/CLAUDE.md`
- Digests and artifacts are output directly in the conversation, not
  written to files, unless the user asks to save them.
