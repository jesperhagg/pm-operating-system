#!/bin/bash
# Regenerates .claude/REPO-MAP.md from current repo state.
# Called by the PostToolUse hook (via repo-map-hook.sh) and
# directly by /generate-repo-map skill invocations.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT="$REPO_ROOT/.claude/REPO-MAP.md"
DATE=$(date +%Y-%m-%d)

# Counts
EXPORTED_COUNT=$(find "$REPO_ROOT/skills" -name "SKILL.md" -maxdepth 2 2>/dev/null | wc -l | tr -d ' ')
INTERNAL_COUNT=$(find "$REPO_ROOT/.claude/skills" -name "SKILL.md" -maxdepth 2 2>/dev/null | wc -l | tr -d ' ')
AGENT_COUNT=$(find "$REPO_ROOT/agents" -name "AGENT.md" -maxdepth 2 2>/dev/null | wc -l | tr -d ' ')
CONTEXT_COUNT=$(find "$REPO_ROOT/.claude/context" -name "*.md" -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')

# Extract description from YAML frontmatter (first "description:" line, unquoted, truncated)
get_desc() {
  grep -m1 "^description:" "$1" 2>/dev/null \
    | sed 's/^description:[[:space:]]*//' \
    | tr -d '"' \
    | cut -c1-70
}

{
  printf '# PM OS — Repo Map\n'
  printf '_Last generated: %s | %s exported skills / %s internal skills / %s agents_\n\n' \
    "$DATE" "$EXPORTED_COUNT" "$INTERNAL_COUNT" "$AGENT_COUNT"

  printf '## Structure\n\n'
  printf '| Path | Contains | Count |\n'
  printf '|------|----------|-------|\n'
  printf '| `skills/` | Exported skills (available in consumer repos via plugin) | %s |\n' "$EXPORTED_COUNT"
  printf '| `.claude/skills/` | Internal skills (this repo only) | %s |\n' "$INTERNAL_COUNT"
  printf '| `agents/` | Exported chat-persona agents (available in consumer repos) | %s |\n' "$AGENT_COUNT"
  printf '| `.claude/context/` | Lazy-loaded reference docs | %s |\n' "$CONTEXT_COUNT"
  printf '| `.claude-plugin/` | plugin.json (manifest), marketplace.json | 2 |\n'

  printf '\n## Exported Skills — `skills/*/SKILL.md`\n\n'
  printf '| Skill | Path | Lines | Purpose |\n'
  printf '|-------|------|-------|----------|\n'
  while IFS= read -r skill_md; do
    name=$(basename "$(dirname "$skill_md")")
    lines=$(wc -l < "$skill_md" | tr -d ' ')
    desc=$(get_desc "$skill_md")
    printf '| /%s | `skills/%s/SKILL.md` | %s | %s |\n' "$name" "$name" "$lines" "$desc"
  done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -maxdepth 2 | sort)

  printf '\n## Internal Skills — `.claude/skills/*/SKILL.md`\n\n'
  printf '| Skill | Path | Lines | Purpose |\n'
  printf '|-------|------|-------|----------|\n'
  while IFS= read -r skill_md; do
    name=$(basename "$(dirname "$skill_md")")
    lines=$(wc -l < "$skill_md" | tr -d ' ')
    desc=$(get_desc "$skill_md")
    printf '| /%s | `.claude/skills/%s/SKILL.md` | %s | %s |\n' "$name" "$name" "$lines" "$desc"
  done < <(find "$REPO_ROOT/.claude/skills" -name "SKILL.md" -maxdepth 2 | sort)

  printf '\n## Agents — `agents/*/AGENT.md`\n\n'
  printf '| Agent | Path | Lines | Domain |\n'
  printf '|-------|------|-------|--------|\n'
  while IFS= read -r agent_md; do
    name=$(basename "$(dirname "$agent_md")")
    lines=$(wc -l < "$agent_md" | tr -d ' ')
    desc=$(get_desc "$agent_md")
    printf '| %s | `agents/%s/AGENT.md` | %s | %s |\n' "$name" "$name" "$lines" "$desc"
  done < <(find "$REPO_ROOT/agents" -name "AGENT.md" -maxdepth 2 | sort)

  printf '\n## Reference Docs — `.claude/context/`\n\n'
  printf '| File | Lines | Load when |\n'
  printf '|------|-------|----------|\n'
  while IFS= read -r ctx_file; do
    filename=$(basename "$ctx_file")
    lines=$(wc -l < "$ctx_file" | tr -d ' ')
    case "$filename" in
      data-schemas.md)   when="Writing to data/ (Decisions, Signals, Knowledge, Personas, Tasks)" ;;
      dev-standards.md)  when="Authoring or reviewing skills, agents, plugin infrastructure" ;;
      *)                 when="On demand" ;;
    esac
    printf '| `%s` | %s | %s |\n' "$filename" "$lines" "$when"
  done < <(find "$REPO_ROOT/.claude/context" -name "*.md" -maxdepth 1 | sort)

  printf '\n## When You Need To...\n\n'
  printf '| Task | File to read/edit |\n'
  printf '|------|-------------------|\n'
  printf '| Modify an exported skill | `skills/<name>/SKILL.md` |\n'
  printf '| Modify an internal skill | `.claude/skills/<name>/SKILL.md` |\n'
  printf '| Modify an agent | `agents/<name>/AGENT.md` |\n'
  printf '| Update plugin version | `.claude-plugin/plugin.json` |\n'
  printf '| Check data layer schemas (frontmatter, file shapes, routing rubric) | `.claude/context/data-schemas.md` |\n'
  printf '| Check skill design patterns + conventions | `.claude/context/dev-standards.md` |\n'
  printf '| Add a new exported skill | New `skills/<name>/SKILL.md` (auto-discovered) |\n'
  printf '| Add a new internal skill | New `.claude/skills/<name>/SKILL.md` |\n'
  printf '| Add a new agent | New `agents/<name>/AGENT.md` (auto-discovered) |\n'
  printf '| Update marketplace listing | `.claude-plugin/marketplace.json` (major releases only) |\n'
} > "$OUTPUT"

echo "REPO-MAP.md updated — $EXPORTED_COUNT exported skills, $INTERNAL_COUNT internal skills, $AGENT_COUNT agents."
