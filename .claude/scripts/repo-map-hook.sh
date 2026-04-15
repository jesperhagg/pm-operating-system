#!/bin/bash
# PostToolUse hook: regenerates REPO-MAP.md when skill or agent files change.
# Triggered by Write and Edit tool calls; no-ops on unrelated files.

INPUT=$(cat)

# Extract file_path from the hook JSON payload
FILE_PATH=$(printf '%s' "$INPUT" \
  | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' \
  | head -1 \
  | sed 's/"file_path"[[:space:]]*:[[:space:]]*"//' \
  | sed 's/"$//')

# Only proceed if the modified file is a SKILL.md or AGENT.md in the
# relevant directories (skills/, .claude/skills/, .claude/agents/)
if printf '%s' "$FILE_PATH" \
  | grep -qE '(^|/)skills/[^/]+/SKILL\.md$|(^|/)\.claude/(skills|agents)/[^/]+/(SKILL|AGENT)\.md$'; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  bash "$SCRIPT_DIR/generate-repo-map.sh"
fi
