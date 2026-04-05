# PM Operating System

A personal PM skills marketplace for Claude Code. Skills encode PM frameworks and dynamically query Notion for live product context — so every analysis is grounded in your actual roadmap, not hypotheticals.

## What it is

This repo is a multi-product PM workspace for a solo founder setup, currently covering:

- **Sagokraft** — AI-adaptive children's reading companion (Swedish, ages 4-8)
- **Selftaped** — Mobile self-tape audition app for independent actors
- Exploratory bets as they emerge

Skills wrap repeatable PM work (strategy reviews, prioritization, market scans, digests) in Claude Code slash commands. Agents handle deeper reasoning across startup advisor, product sculptor, growth engineer, and AI systems lead roles.

## Install

```bash
claude plugin marketplace add <path-or-github-url>
```

Replace `<path-or-github-url>` with the local path or GitHub URL of this repo.

## Structure

```
.claude-plugin/
  plugin.json       # Plugin manifest
  marketplace.json  # Marketplace listing
skills/             # Skill definitions (coming soon)
commands/           # Custom commands (coming soon)
.claude/
  agents/           # Agent definitions
  skills/           # Internal skill prompts
```
