---
description: Surface active tasks from tasks/active.md with sprint-style formatting. Runs at session start by default. Supports viewing, updating, and adding tasks.
---

# Task Management

This skill manages the consumer repo's task backlog at `tasks/active.md`
and presents it in a structured sprint-style view. It is designed to run
at the start of every session (per the CLAUDE.md session start rule) so
the user always begins with visibility into their current work.

## File Layout

- `tasks/active.md` — Now / Next / Later H2 sections with markdown
  checkboxes and inline HTML-comment metadata.
- `tasks/done.md` — flat chronological list of completed tasks.
- `tasks/governance.md` — conflict and staleness tasks written by
  `/ctx-context-sync`. Review-only from this skill.

See `.claude/context/context-schemas.md` for the full format. Example:

```markdown
- [ ] Ship pricing page update <!-- priority:now due:2026-05-01 blocker:"" -->
```

One product per repo — no `Product` filter field.

## Modes

### 1. View (default)

**Triggers:** `/ops-tasks`, session start, "what am I working on", "what's active"

**Steps:**

1. Read `tasks/active.md`. If the file does not exist, say so and
   suggest creating one via `/ops-tasks add`.
2. Parse each H2 section (Now / Next / Later) and the checkbox lines.
   Extract `priority`, `due`, and `blocker` from the metadata comment.
3. Check `tasks/governance.md` if it exists — note count of open items
   (`^- \[ \]`).
4. Present in this format:

```
# Active Tasks — {today's date}

## In Progress / Now
- [ ] **{Task title}** — Priority: now
  {Blocker: {description} if any}
  {Due: {date} if set}

## Waiting On
| Task | Waiting For | Since | Next Action |
|------|-------------|-------|-------------|
| {title} | {blocker text} | {if known} | {suggested follow-up} |

## Up Next (top 3 from Next section)
- [ ] **{Task title}** — Priority: next

---
{total count} tasks. {overdue count} overdue.
{governance count if > 0: "⚠ {N} governance tasks await review in tasks/governance.md"}
```

4. If any task has a `due` date earlier than today, flag it as overdue.
5. If the file is empty, say so and suggest `/ops-tasks add`.

### 2. Update

**Triggers:** `/ops-tasks done "task name"`, `/ops-tasks update "task name"`

**Steps:**

1. Grep `tasks/active.md` for a checkbox line matching the given name.
2. If multiple matches, show them and ask to pick.
3. For "done":
   - Append `done:YYYY-MM-DD` to the metadata.
   - Change `[ ]` to `[x]`.
   - Move the line from `tasks/active.md` to the bottom of `tasks/done.md`
     (create `done.md` if missing).
4. For "update": ask what to change (priority, due, blocker) and edit
   the line in place. Move to the matching H2 section if priority changed.
5. Confirm the change and show the updated task view.

### 3. Add

**Triggers:** `/ops-tasks add "description"`, `/ops-tasks new`

**Steps:**

1. Parse the description from the command, or ask if not provided.
2. Prompt for required metadata:
   - **Priority:** Now / Next / Later (default Next)
   - **Due Date:** Optional (YYYY-MM-DD)
   - **Blocker:** Optional
3. Append the line to the matching H2 section in `tasks/active.md`.
   Format:
   `- [ ] {title} <!-- priority:{now|next|later} due:{date or ""} blocker:"{text or ""}" -->`
   Create `active.md` (with H1 + Now/Next/Later H2 scaffolding) if missing.
4. Confirm creation and show where it landed in the task view.

## Session Start Behavior

Per the CLAUDE.md rule "At the start of every conversation, run `/ops-tasks`":

1. Automatically run the View mode at session start.
2. Keep the output concise — no more than 15-20 lines for a typical load.
3. If the user says "skip tasks", do not show the task view.
4. After showing tasks, ask: "What would you like to work on?" or proceed.

## Relationship to /ctx-fetch-context

- `/ops-tasks` provides a **focused, actionable task view** — "what am I
  working on right now?"
- `/ctx-fetch-context` provides **broad product context** — decisions,
  personas, backlog, recent signals, market landscape.

Both read `tasks/active.md` but serve different purposes.

## Suggested Follow-ups

After viewing tasks:
- If blockers exist: "Want me to help unblock {task}?"
- If a task is overdue: "{task} is past due. Want to reprioritize?"
- If governance tasks exist: "Review tasks/governance.md for context
  conflicts to resolve."
- If backlog is large (>15 active): "Want to run `/disc-break-down` to
  tighten scope?"

After completing a task:
- "Want to pull the next item from the Next section?"
- If it was a significant milestone: "Worth logging this as a decision?
  Run `/strat-log-decision`."
