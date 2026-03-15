# Claude Code — PM Operating System

This repository contains PM skills and workflows powered by Claude.

## Skills (Slash Commands)

### /prd-writer
Draft a Product Requirements Document from a feature idea.
Usage: `/prd-writer <feature description>`
File: `skills/prd_writer.py`

### /sprint-planner
Generate a sprint plan from the current backlog.
Usage: `/sprint-planner [--sprint-length 2w] [--team-capacity 40]`
File: `skills/sprint_planner.py`

### /metrics-analyzer
Analyze a metrics snapshot and surface key insights.
Usage: `/metrics-analyzer [--product <product-id>] [--period last_7d]`
File: `skills/metrics_analyzer.py`

### /user-story-gen
Generate user stories (with acceptance criteria) from a feature idea.
Usage: `/user-story-gen <feature description>`
File: `skills/user_story_gen.py`

### /stakeholder-update
Write a stakeholder update from sprint and metrics data.
Usage: `/stakeholder-update [--sprint <sprint-id>]`
File: `skills/stakeholder_update.py`

## Data

Mockup data lives in `data/`. All integrations default to local mockup data
when no real credentials are configured (set via env vars).

## Environment Variables (optional real integrations)

```
JIRA_URL=https://yourorg.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=...

SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL=#pm-digest

ANTHROPIC_API_KEY=...
```
