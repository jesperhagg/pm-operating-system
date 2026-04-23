#!/bin/bash
# Regenerates REPO-MAP.md from current repo state.
# Called by the PostToolUse hook (via repo-map-hook.sh) and
# directly by /generate-repo-map skill invocations.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT="$REPO_ROOT/REPO-MAP.md"
DATE=$(date +%Y-%m-%d)

# Counts
SKILL_COUNT=$(find "$REPO_ROOT/skills" -name "SKILL.md" -maxdepth 2 2>/dev/null | wc -l | tr -d ' ')
AGENT_COUNT=$(find "$REPO_ROOT/agents" -name "AGENT.md" -maxdepth 2 2>/dev/null | wc -l | tr -d ' ')
COMMAND_COUNT=$(find "$REPO_ROOT/commands" -name "*.md" -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
CONTEXT_COUNT=$(find "$REPO_ROOT/context" -name "*.md" -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')

# Extract description from YAML frontmatter (first "description:" line, unquoted, truncated)
get_desc() {
  grep -m1 "^description:" "$1" 2>/dev/null \
    | sed 's/^description:[[:space:]]*//' \
    | tr -d '"' \
    | cut -c1-70
}

{
  printf '# PM OS — Repo Map\n'
  printf '_Last generated: %s | %s skills / %s agents / %s commands_\n\n' \
    "$DATE" "$SKILL_COUNT" "$AGENT_COUNT" "$COMMAND_COUNT"

  printf '## Structure\n\n'
  printf '| Path | Contains | Count |\n'
  printf '|------|----------|-------|\n'
  printf '| `skills/` | Skills (available in consumer repos via submodule) | %s |\n' "$SKILL_COUNT"
  printf '| `agents/` | Chat-persona agents (available in consumer repos) | %s |\n' "$AGENT_COUNT"
  printf '| `commands/` | Slash commands (available in consumer repos) | %s |\n' "$COMMAND_COUNT"
  printf '| `context/` | Lazy-loaded reference docs | %s |\n' "$CONTEXT_COUNT"

  printf '\n## Skills — `skills/*/SKILL.md`\n\n'
  printf '| Skill | Path | Lines | Purpose |\n'
  printf '|-------|------|-------|----------|\n'
  while IFS= read -r skill_md; do
    name=$(basename "$(dirname "$skill_md")")
    lines=$(wc -l < "$skill_md" | tr -d ' ')
    desc=$(get_desc "$skill_md")
    printf '| /%s | `skills/%s/SKILL.md` | %s | %s |\n' "$name" "$name" "$lines" "$desc"
  done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -maxdepth 2 | sort)

  printf '\n## Agents — `agents/*/AGENT.md`\n\n'
  printf '| Agent | Path | Lines | Domain |\n'
  printf '|-------|------|-------|--------|\n'
  while IFS= read -r agent_md; do
    name=$(basename "$(dirname "$agent_md")")
    lines=$(wc -l < "$agent_md" | tr -d ' ')
    desc=$(get_desc "$agent_md")
    printf '| %s | `agents/%s/AGENT.md` | %s | %s |\n' "$name" "$name" "$lines" "$desc"
  done < <(find "$REPO_ROOT/agents" -name "AGENT.md" -maxdepth 2 | sort)

  printf '\n## Commands — `commands/*.md`\n\n'
  printf '| Command | Path | Purpose |\n'
  printf '|---------|------|----------|\n'
  while IFS= read -r cmd_md; do
    name=$(basename "$cmd_md" .md)
    desc=$(get_desc "$cmd_md")
    printf '| /%s | `commands/%s.md` | %s |\n' "$name" "$name" "$desc"
  done < <(find "$REPO_ROOT/commands" -name "*.md" -maxdepth 1 | sort)

  printf '\n## Reference Docs — `context/`\n\n'
  printf '| File | Lines | Load when |\n'
  printf '|------|-------|----------|\n'
  while IFS= read -r ctx_file; do
    filename=$(basename "$ctx_file")
    lines=$(wc -l < "$ctx_file" | tr -d ' ')
    case "$filename" in
      data-schemas.md)   when="Writing to data/ (Decisions, Signals, Knowledge, Personas, Tasks)" ;;
      dev-standards.md)  when="Authoring or reviewing skills, agents, submodule infrastructure" ;;
      *)                 when="On demand" ;;
    esac
    printf '| `%s` | %s | %s |\n' "$filename" "$lines" "$when"
  done < <(find "$REPO_ROOT/context" -name "*.md" -maxdepth 1 | sort)

  printf '\n## When You Need To...\n\n'
  printf '| Task | File to read/edit |\n'
  printf '|------|-------------------|\n'
  printf '| Modify a skill | `skills/<name>/SKILL.md` |\n'
  printf '| Modify an agent | `agents/<name>/AGENT.md` |\n'
  printf '| Modify a command | `commands/<name>.md` |\n'
  printf '| Check data layer schemas (frontmatter, file shapes, routing rubric) | `context/data-schemas.md` |\n'
  printf '| Check skill design patterns + conventions | `context/dev-standards.md` |\n'
  printf '| Add a new skill | New `skills/<name>/SKILL.md` (auto-discovered) |\n'
  printf '| Add a new agent | New `agents/<name>/AGENT.md` (auto-discovered) |\n'
  printf '| Add a new command | New `commands/<name>.md` (auto-discovered) |\n'
} > "$OUTPUT"

echo "REPO-MAP.md updated — $SKILL_COUNT skills, $AGENT_COUNT agents, $COMMAND_COUNT commands."
