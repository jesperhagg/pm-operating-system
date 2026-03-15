# PM Operating System

A personal toolkit for AI-maximalistic Product Management — skills, workflows, and agentic orchestration examples.

## Goal

Practice and train PM craft using Claude-powered skills that automate, augment, and accelerate real PM work.

## Structure

```
pm-operating-system/
├── data/                    # Mockup data for skills to consume
│   ├── products/            # Product definitions, roadmaps
│   ├── users/               # User personas, segments
│   └── metrics/             # KPIs, analytics snapshots
├── integrations/            # Stub connectors to PM tools
│   ├── jira.py              # Jira (issues, sprints, backlogs)
│   ├── slack.py             # Slack (announcements, digests)
│   ├── analytics.py         # Analytics (Mixpanel/Amplitude-style)
│   └── linear.py            # Linear (issues, cycles)
├── skills/                  # Claude-powered PM skills (slash commands)
│   ├── prd_writer.py        # Draft a PRD from a prompt
│   ├── sprint_planner.py    # Generate sprint plan from backlog
│   ├── metrics_analyzer.py  # Analyze metrics and surface insights
│   ├── user_story_gen.py    # Generate user stories from feature idea
│   └── stakeholder_update.py# Write stakeholder update from sprint data
├── workflows/               # Multi-step agentic workflows
│   └── weekly_pm_digest.py  # End-to-end weekly PM digest
└── CLAUDE.md                # Claude Code skill definitions
```

## Quick Start

```bash
# Run a skill directly
python skills/prd_writer.py --feature "AI-powered search"

# Run a workflow
python workflows/weekly_pm_digest.py

# Use with Claude Code
# /prd-writer, /sprint-planner, /metrics-analyzer
```

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| PRD Writer | `/prd-writer` | Draft a PRD from a one-liner feature idea |
| Sprint Planner | `/sprint-planner` | Generate sprint plan from backlog |
| Metrics Analyzer | `/metrics-analyzer` | Surface insights from metric snapshots |
| User Story Gen | `/user-story-gen` | Generate user stories from feature idea |
| Stakeholder Update | `/stakeholder-update` | Write stakeholder update from sprint data |

## Workflows

| Workflow | Description |
|----------|-------------|
| Weekly PM Digest | Pulls sprint data + metrics, writes digest, posts to Slack |
