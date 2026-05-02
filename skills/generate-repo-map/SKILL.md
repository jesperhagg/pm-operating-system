---
description: Regenerate REPO-MAP.md as a routing map of the codebase. In the pm-os dev repo, indexes skills/agents/commands/context. In a consumer repo, indexes the application source tree so dev tasks can route without spawning Explore agents.
---

# Generate Repo Map

Produce a `REPO-MAP.md` that lets future sessions answer "where does X live?"
without spawning Explore agents.

**Trigger phrases:** "update repo map", "regenerate map", "refresh repo map",
or explicit `/generate-repo-map`

## Step 0: Detect Mode

Decide which mode to run in before scanning anything:

- **Dev mode** — cwd contains `skills/`, `agents/`, `commands/`, **and**
  `context/` at the root, **and** the root `CLAUDE.md` contains the phrase
  `pm-os submodule`. Run **Dev Mode** below.
- **Consumer mode** — cwd contains `.claude/skills/` (the submodule mount)
  and a root `CLAUDE.md`. Run **Consumer Mode** below.
- **Neither** — stop and ask the user which repo they meant to map. Do not
  guess.

---

## Dev Mode

### Step 1: Scan the Repo

Run these four scans in parallel:

1. **Skills** — list all `skills/*/SKILL.md` files. For each, record:
   - Skill name (directory name prefixed with `/`)
   - Relative path
   - Line count
   - `description` value from frontmatter (first sentence only)

2. **Agents** — list all `agents/*/AGENT.md` files. For each, record:
   - Agent name (from frontmatter `name` field, or directory name)
   - Relative path
   - Line count
   - `description` value from frontmatter

3. **Commands** — list all `commands/*.md` files. For each, record:
   - Command name (filename without `.md`, prefixed with `/`)
   - Relative path
   - `description` value from frontmatter

4. **Context files** — list all `context/*.md` files. For each, record:
   - Filename
   - Line count
   - When to load (infer from filename: data-schemas → "Writing to data/ (Decisions, Signals, Knowledge, Personas, Tasks)",
     dev-standards → "Authoring or reviewing skills/agents")

### Step 2: Build the Map

Write `REPO-MAP.md` at the repo root with this exact structure:

```markdown
# PM OS — Repo Map
_Last generated: {today's date} | {N} skills / {K} agents / {C} commands_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `skills/` | Skills (available in consumer repos via submodule) | {N} |
| `agents/` | Chat-persona agents (available in consumer repos) | {K} |
| `commands/` | Slash commands (available in consumer repos) | {C} |
| `context/` | Lazy-loaded reference docs | {J} |

## Skills — `skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|---------|
{one row per skill, sorted alphabetically by skill name}

## Agents — `agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
{one row per agent, sorted alphabetically}

## Commands — `commands/*.md`

| Command | Path | Purpose |
|---------|------|---------|
{one row per command, sorted alphabetically}

## Reference Docs — `context/`

| File | Lines | Load when |
|------|-------|-----------|
{one row per context file}

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify a skill | `skills/<name>/SKILL.md` |
| Modify an agent | `agents/<name>/AGENT.md` |
| Modify a command | `commands/<name>.md` |
| Check data layer schemas (frontmatter, file shapes, routing rubric) | `context/data-schemas.md` |
| Check skill design patterns + conventions | `context/dev-standards.md` |
| Add a new skill | New `skills/<name>/SKILL.md` (auto-discovered) |
| Add a new agent | New `agents/<name>/AGENT.md` (auto-discovered) |
| Add a new command | New `commands/<name>.md` (auto-discovered) |
```

### Step 3: Write and Confirm

Overwrite `REPO-MAP.md`. Output to conversation:

```
REPO-MAP.md updated — {N} skills, {K} agents, {C} commands.
```

If any file was added or removed since the last map, note it explicitly:
```
Changes since last map: added {skill/agent name}, removed {name}
```

---

## Consumer Mode

### Step C1: Hydrate Stack Signals

Read in parallel (skip any that don't exist):

- Manifests: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`,
  `Gemfile`, `pom.xml`, `composer.json`
- Configs: `tsconfig.json`, `next.config.*`, `vite.config.*`,
  `nuxt.config.*`, `astro.config.*`
- Container: `Dockerfile`, `docker-compose.yml`
- `README.md` (first 100 lines for stack hints)

Extract:
- Languages and frameworks
- Package managers (presence of `pnpm-lock.yaml`, `yarn.lock`,
  `package-lock.json`, `poetry.lock`, `uv.lock`, etc.)
- Declared entry points (`main`, `bin`, `scripts.start`, `scripts.dev`,
  `[project.scripts]`)
- Repo display name (from manifest `name`, else dir basename)

### Step C2: Enumerate the Source Tree

Use `git ls-files` to enumerate tracked files (cheap, already respects
`.gitignore`). Apply skip filters:

- **Skip directories**: `.claude/`, `data/`, `node_modules/`, `dist/`,
  `build/`, `.next/`, `.nuxt/`, `target/`, `venv/`, `.venv/`,
  `__pycache__/`, `.git/`, `coverage/`, `.turbo/`, `.cache/`
- **Skip files**: lockfiles (`*-lock.json`, `*.lock`, `pnpm-lock.yaml`,
  `poetry.lock`, `Cargo.lock`, `uv.lock`), `*.min.*`, `*.map`,
  binary assets (`*.png|jpg|jpeg|gif|svg|webp|ico|woff*|ttf|otf|pdf|mp4|mov|wasm`),
  snapshot files under `__snapshots__/`
- **List but don't summarize**: `*.d.ts`, migration files
  (count + first/last only), pure config dotfiles
  (`.eslintrc*`, `.prettierrc*`, `.editorconfig`)

If the resulting kept set has more than ~600 files, **pause and ask** the
user to scope to one or more top-level directories before continuing. Do
not silently truncate.

### Step C3: Summarize Per File

For each file in the kept set, batched in parallel reads:

- Read the first 20 lines.
- Derive a 1-line purpose (≤ 80 chars) from, in order of preference:
  1. Top-of-file docstring or comment block
  2. Exported symbols (`export …`, `def …`, `class …`, `func …`,
     `pub fn …`)
  3. Filename + parent directory
- Record: relative path, total line count, purpose.

For each directory containing kept files, derive a 1-line directory
purpose by summarizing the purposes of its files (use what was already
read — do not re-open files).

### Step C4: Build the Routing Table

Generate the "When You Need To…" section using the directory map + stack
signals. Heuristics — **apply only when the matched path actually exists
in the kept set**:

| Detected | Routing entry |
|---|---|
| `src/app/` (Next.js app router) | "Add a page" → `src/app/<route>/page.tsx` |
| `pages/` (Next.js pages router) | "Add a page" → `pages/<route>.tsx` |
| `src/components/` or `components/` | "Add a UI component" → matched dir |
| `src/lib/` or `src/utils/` | "Add a shared util" → matched dir |
| `src/hooks/` | "Add a React hook" → `src/hooks/` |
| `api/`, `server/`, `backend/` | "Add an API route/handler" → matched dir |
| `tests/` or `__tests__/` | "Add a test" → matched dir |
| Collocated `*.test.*` files exist | "Add a test" → "next to the file under test" |
| `migrations/` | "Add a DB migration" → `migrations/` |
| `scripts/` | "Add a one-off script" → `scripts/` |
| `cli/` or `bin/` | "Add a CLI command" → matched dir |

If a heuristic doesn't match, omit it. Do not fabricate routes.

### Step C5: Write `REPO-MAP.md` at the Consumer Repo Root

Write to `<repo-root>/REPO-MAP.md` (NOT inside `.claude/`) with this
schema:

```markdown
# {repo display name} — Repo Map
_Last generated: {today} | {N} source files | Stack: {comma-separated}_

## Stack
- Languages: …
- Frameworks: …
- Package managers: …

## Entry Points

| Purpose | Path |
|---------|------|
{rows from manifest entry points; omit section if none found}

## Top-Level Layout

| Path | What lives here |
|------|-----------------|
{one row per top-level directory in the kept set, alphabetical}

## File Index

### `<dir-path>/`
_{directory purpose}_

| File | Lines | Purpose |
|------|-------|---------|
{files alphabetical}

{repeat per directory, top-level dirs alphabetical}

## When You Need To…

| Task | Where |
|------|-------|
{routing rows from Step C4}
```

### Step C6: Confirm

Output to conversation:

```
REPO-MAP.md updated — {N} files indexed across {D} directories. Stack: {…}.
```

If a previous `REPO-MAP.md` existed at the same path, also report:

```
Changes since last map: +{added} new, -{removed} removed, ~{modified} changed.
```

Compute by diffing the previous file table against the new one. When path
and line count both match, treat the row as unchanged — no need to
re-summarize.

---

## Follow-ups

- **Consumer mode**: "Reference `REPO-MAP.md` from your repo's root
  `CLAUDE.md` so future sessions load it before exploring."
- **Consumer mode**: "Re-run `/generate-repo-map` after large refactors or
  when the file count drifts noticeably."
- **Dev mode**: "Verify against the pre-commit checklist in
  `dev-standards.md` before committing."
