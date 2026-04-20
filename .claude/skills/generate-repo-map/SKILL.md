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

1. **Exported skills** — list all `skills/*/SKILL.md` files. For each, record:
   - Skill name (directory name prefixed with `/`)
   - Relative path
   - Line count
   - `description` value from frontmatter (first sentence only)

2. **Internal skills** — list all `.claude/skills/*/SKILL.md` files. Same fields.

3. **Agents** — list all `.claude/agents/*/AGENT.md` files. For each, record:
   - Agent name (from frontmatter `name` field, or directory name)
   - Relative path
   - Line count
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
_Last generated: {today's date} | {N} exported skills / {M} internal skills / {K} agents_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `skills/` | Exported skills (available in consumer repos via plugin) | {N} |
| `.claude/skills/` | Internal skills (this repo only) | {M} |
| `.claude/agents/` | Agents | {K} |
| `.claude/context/` | Lazy-loaded reference docs | {J} |
| `.claude-plugin/` | plugin.json (manifest), marketplace.json | 2 |

## Exported Skills — `skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|---------|
{one row per exported skill, sorted alphabetically by skill name}

## Internal Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|---------|
{one row per internal skill, sorted alphabetically}

## Agents — `.claude/agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
{one row per agent, sorted alphabetically}

## Reference Docs — `.claude/context/`

| File | Lines | Load when |
|------|-------|-----------|
{one row per context file}

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify an exported skill | `skills/<name>/SKILL.md` |
| Modify an internal skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `.claude/agents/<name>/AGENT.md` |
| Update plugin export list | `.claude-plugin/plugin.json` |
| Check data layer schemas (frontmatter, file shapes, routing rubric) | `.claude/context/data-schemas.md` |
| Check skill design patterns + conventions | `.claude/context/dev-standards.md` |
| Add a new exported skill | New `skills/<name>/SKILL.md` + add entry to `plugin.json` |
| Add a new internal skill | New `.claude/skills/<name>/SKILL.md` (no plugin.json update) |
| Add a new agent | New `.claude/agents/<name>/AGENT.md` (no plugin.json update) |
| Update marketplace listing | `.claude-plugin/marketplace.json` (major releases only) |
```

## Step 3: Write and Confirm

Overwrite `.claude/REPO-MAP.md` with the generated content.

Output to conversation:

```
REPO-MAP.md updated — {N} exported skills, {M} internal skills, {K} agents.
```

If any file was added or removed since the last map, note it explicitly:
```
Changes since last map: added {skill/agent name}, removed {name}
```

## Follow-ups

- If this was run after adding a new exported skill: "Don't forget to update
  `.claude-plugin/plugin.json` with the new skill entry."
- If structural changes were made: "Verify against the pre-commit checklist in `dev-standards.md` before committing."
