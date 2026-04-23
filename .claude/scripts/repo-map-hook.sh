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

# Only proceed if the modified file is a SKILL.md, AGENT.md, or command in .claude/
if printf '%s' "$FILE_PATH" \
  | grep -qE '(^|/)\.claude/(skills|agents)/[^/]+/(SKILL|AGENT)\.md$|(^|/)\.claude/commands/[^/]+\.md$'; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  bash "$SCRIPT_DIR/generate-repo-map.sh"
fi
