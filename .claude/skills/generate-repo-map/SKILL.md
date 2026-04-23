---
description: Regenerate .claude/REPO-MAP.md by scanning current skills, agents, and context files. Run after adding, removing, or renaming any skill or agent.
---

# Generate Repo Map

Regenerate `.claude/REPO-MAP.md` with accurate file paths and line counts by
scanning the current state of the repo.

**Trigger phrases:** "update repo map", "regenerate map", "refresh repo map",
or explicit `/generate-repo-map`

## Step 1: Scan the Repo

Run these four scans in parallel:

1. **Skills** — list all `.claude/skills/*/SKILL.md` files. For each, record:
   - Skill name (directory name prefixed with `/`)
   - Relative path
   - Line count
   - `description` value from frontmatter (first sentence only)

2. **Agents** — list all `.claude/agents/*/AGENT.md` files. For each, record:
   - Agent name (from frontmatter `name` field, or directory name)
   - Relative path
   - Line count
   - `description` value from frontmatter

3. **Commands** — list all `.claude/commands/*.md` files. For each, record:
   - Command name (filename without `.md`, prefixed with `/`)
   - Relative path
   - `description` value from frontmatter

4. **Context files** — list all `.claude/context/*.md` files. For each, record:
   - Filename
   - Line count
   - When to load (infer from filename: data-schemas → "Writing to data/ (Decisions, Signals, Knowledge, Personas, Tasks)",
     dev-standards → "Authoring or reviewing skills/agents")

## Step 2: Build the Map

Write `.claude/REPO-MAP.md` with this exact structure:

```markdown
# PM OS — Repo Map
_Last generated: {today's date} | {N} skills / {K} agents / {C} commands_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `.claude/skills/` | Skills (available in consumer repos via submodule) | {N} |
| `.claude/agents/` | Chat-persona agents (available in consumer repos) | {K} |
| `.claude/commands/` | Slash commands (available in consumer repos) | {C} |
| `.claude/context/` | Lazy-loaded reference docs | {J} |

## Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|---------|
{one row per skill, sorted alphabetically by skill name}

## Agents — `.claude/agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
{one row per agent, sorted alphabetically}

## Commands — `.claude/commands/*.md`

| Command | Path | Purpose |
|---------|------|---------|
{one row per command, sorted alphabetically}

## Reference Docs — `.claude/context/`

| File | Lines | Load when |
|------|-------|-----------|
{one row per context file}

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify a skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `.claude/agents/<name>/AGENT.md` |
| Modify a command | `.claude/commands/<name>.md` |
| Check data layer schemas (frontmatter, file shapes, routing rubric) | `.claude/context/data-schemas.md` |
| Check skill design patterns + conventions | `.claude/context/dev-standards.md` |
| Add a new skill | New `.claude/skills/<name>/SKILL.md` (auto-discovered) |
| Add a new agent | New `.claude/agents/<name>/AGENT.md` (auto-discovered) |
| Add a new command | New `.claude/commands/<name>.md` (auto-discovered) |
```

## Step 3: Write and Confirm

Overwrite `.claude/REPO-MAP.md` with the generated content.

Output to conversation:

```
REPO-MAP.md updated — {N} skills, {K} agents, {C} commands.
```

If any file was added or removed since the last map, note it explicitly:
```
Changes since last map: added {skill/agent name}, removed {name}
```

## Follow-ups

- If structural changes were made: "Verify against the pre-commit checklist in `dev-standards.md` before committing."
