#!/bin/bash
# PostToolUse activity-log hook — appends one JSONL event per meaningful tool call.
# Facts only: no LLM, no network. Complements (does not duplicate) content metadata.
# Logs only mutating/meaningful tools (Skill, Task, Write, Edit, NotebookEdit).
# Never blocks or fails a tool call — always exits 0.
set -uo pipefail

# Read the hook payload from stdin (session_id, tool_name, tool_input).
PAYLOAD=$(cat 2>/dev/null || true)
[ -z "$PAYLOAD" ] && exit 0

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
MONTH=$(date -u +%Y-%m)

# Build the JSONL line in a single pass (jq preferred, python3 fallback).
# Emits nothing for read-only / non-matching tools, so the hook is a no-op there.
build_line() {
  if command -v jq &>/dev/null; then
    printf '%s' "$PAYLOAD" | jq -c --arg ts "$TS" '
      (.tool_name // "")     as $t
      | (.tool_input // {})  as $ti
      | (.session_id // "unknown") as $sess
      | ({
          "Skill":        {actor: ("skill:" + ($ti.skill // "unknown")),               action: "invoke"},
          "Task":         {actor: ("agent:" + ($ti.subagent_type // "general-purpose")), action: "invoke"},
          "Write":        {actor: "tool:Write",        action: "write"},
          "Edit":         {actor: "tool:Edit",         action: "edit"},
          "NotebookEdit": {actor: "tool:NotebookEdit", action: "edit"}
        }[$t]) as $m
      | if $m == null then empty
        else {
          ts: $ts, session: $sess, actor: $m.actor, action: $m.action,
          targets: ([$ti.file_path, $ti.notebook_path] | map(select(. != null))),
          tool: $t, status: "ok"
        } end
    ' 2>/dev/null
  else
    printf '%s' "$PAYLOAD" | TS="$TS" python3 -c '
import os, sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
t = d.get("tool_name") or ""
ti = d.get("tool_input") or {}
m = {
    "Skill":        ("skill:" + (ti.get("skill") or "unknown"), "invoke"),
    "Task":         ("agent:" + (ti.get("subagent_type") or "general-purpose"), "invoke"),
    "Write":        ("tool:Write", "write"),
    "Edit":         ("tool:Edit", "edit"),
    "NotebookEdit": ("tool:NotebookEdit", "edit"),
}
if t not in m:
    sys.exit(0)
actor, action = m[t]
targets = [p for p in (ti.get("file_path"), ti.get("notebook_path")) if p]
print(json.dumps({
    "ts": os.environ["TS"], "session": d.get("session_id") or "unknown",
    "actor": actor, "action": action, "targets": targets, "tool": t, "status": "ok",
}))
' 2>/dev/null
  fi
}

LINE=$(build_line)
[ -z "$LINE" ] && exit 0

# Durable trail in context/audit/ when context/ exists; else a local dogfood log.
if [ -d "${PROJECT_DIR}/context" ]; then
  LOG_DIR="${PROJECT_DIR}/context/audit"
else
  LOG_DIR="${PROJECT_DIR}/.claude/logs"
fi

# Append best-effort; never fail the tool call.
mkdir -p "$LOG_DIR" 2>/dev/null && printf '%s\n' "$LINE" >>"${LOG_DIR}/activity-${MONTH}.jsonl" 2>/dev/null
exit 0
