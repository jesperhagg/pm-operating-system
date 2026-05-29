# Activity Audit Trail

Automatic, append-only log of what skills and agents did in this repo. Written by
the `PostToolUse` hook `.claude/hooks/activity-log.sh` — never by hand, never by a
skill. One JSON object per line, in monthly files `activity-YYYY-MM.jsonl`.

## Event shape

```json
{"ts":"2026-05-29T14:03:22Z","session":"<id>","actor":"skill:strat-log-decision",
 "action":"invoke","targets":["context/product/decisions.md"],"tool":"Edit","status":"ok"}
```

- `actor` — `skill:<name>`, `agent:<subagent_type>`, or `tool:<Write|Edit|NotebookEdit>`.
- `action` — `invoke` | `write` | `edit`.
- `targets` — file path(s) touched, when present.
- `session` + `ts` + `targets` correlate a file change back to the skill that made it.

This records *that an action happened*. The *why* lives in content metadata
(`date:`, `source:`, `agent:[]`, `linked_signals:`) inside the files themselves.

## Reading it

```sh
# Everything a given skill did
jq -c 'select(.actor=="skill:strat-log-decision")' audit/activity-*.jsonl
# Everything that touched a file
jq -c 'select(.targets[]? == "context/product/decisions.md")' audit/activity-*.jsonl
# Run volume by actor
jq -r '.actor' audit/activity-*.jsonl | sort | uniq -c | sort -rn
```
