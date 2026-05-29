#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  cd "$CLAUDE_PROJECT_DIR"
  npm install
fi

# Context-layer staleness check — bash only, no LLM, no network
CONTEXT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/context"
SYNC_STATE="${CONTEXT_DIR}/.sync-state.json"

if [ ! -d "$CONTEXT_DIR" ]; then
  exit 0
fi

if [ ! -f "$SYNC_STATE" ]; then
  echo "CONTEXT_STALE=true"
  echo "CONTEXT_STALE_REASON=no_sync_state"
  exit 0
fi

# Parse last_sync timestamp (jq preferred; python3 fallback)
if command -v jq &>/dev/null; then
  LAST_SYNC=$(jq -r '.last_sync // empty' "$SYNC_STATE" 2>/dev/null || true)
else
  LAST_SYNC=$(python3 -c "import json; d=json.load(open('$SYNC_STATE')); print(d.get('last_sync') or '')" 2>/dev/null || true)
fi

if [ -z "${LAST_SYNC:-}" ]; then
  echo "CONTEXT_STALE=true"
  echo "CONTEXT_STALE_REASON=no_last_sync"
  exit 0
fi

# Days since last sync — Linux date with ISO8601 fallback for macOS
LAST_SYNC_EPOCH=$(date -d "$LAST_SYNC" +%s 2>/dev/null \
  || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$LAST_SYNC" +%s 2>/dev/null \
  || echo 0)
NOW_EPOCH=$(date +%s)
DAYS_SINCE=$(( (NOW_EPOCH - LAST_SYNC_EPOCH) / 86400 ))

if [ "$DAYS_SINCE" -ge 7 ]; then
  echo "CONTEXT_STALE=true"
  echo "CONTEXT_STALE_DAYS=$DAYS_SINCE"
fi

# Count unresolved governance tasks
GOVERNANCE="${CLAUDE_PROJECT_DIR:-$(pwd)}/tasks/governance.md"
if [ -f "$GOVERNANCE" ]; then
  OPEN=$(grep -c "^- \[ \]" "$GOVERNANCE" 2>/dev/null || echo 0)
  if [ "$OPEN" -gt 0 ]; then
    echo "CONTEXT_GOVERNANCE_OPEN=$OPEN"
  fi
fi
