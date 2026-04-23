---
description: Surface active tasks from data/tasks/active.md with sprint-style formatting. Runs at session start by default. Supports viewing, updating, and adding tasks.
---

# Task Management

This skill manages the consumer repo's task backlog at
`data/tasks/active.md` and presents it in a structured sprint-style
view. It is designed to run at the start of every session (per the
CLAUDE.md session start rule) so the user always begins with visibility
into their current work.

## File Layout

- `data/tasks/active.md` — Now / Next / Later H2 sections with markdown
  checkboxes and inline HTML-comment metadata.
- `data/tasks/done.md` — flat chronological list of completed tasks.

See `.claude/context/data-schemas.md` for the full format. Example active
entry:

```markdown
- [ ] Ship pricing page update <!-- priority:now due:2026-05-01 blocker:"" -->
```

One product per repo — no `Product` filter field.

## Modes

### 1. View (default)

**Triggers:** `/tasks`, session start (automatic per CLAUDE.md rule),
"what am I working on", "what's active"

**Steps:**

1. Read `data/tasks/active.md`. If the file does not exist, say so and
   suggest creating one via `/tasks add`.
2. Parse each H2 section (Now / Next / Later) and the checkbox lines
   under each. Extract `priority`, `due`, and `blocker` from the
   metadata comment.
3. Present in this format:

```
# Active Tasks — {today's date}

## In Progress / Now
- [ ] **{Task title}** — Priority: now
  {Blocker if any: "Blocker: {description}"}
  {Due: {date} if set}

## Waiting On
| Task | Waiting For | Since | Next Action |
|------|-------------|-------|-------------|
| {title} | {blocker text} | {if known} | {suggested follow-up} |

## Up Next (top 3 from Next section)
- [ ] **{Task title}** — Priority: next

---
{total count} tasks. {overdue count} overdue.
```

4. If any task has a `due` date earlier than today, flag it as overdue
   at the top.
5. If the file is empty, say so and suggest `/tasks add`.

### 2. Update

**Triggers:** `/tasks done "task name"`, `/tasks update "task name"`

**Steps:**

1. Grep `data/tasks/active.md` for a checkbox line containing the given
   name (case-insensitive substring match).
2. If multiple matches, show them and ask the user to pick one.
3. For "done":
   - Append today's date to the metadata as `done:YYYY-MM-DD`.
   - Change `[ ]` to `[x]`.
   - Move the entire line from `data/tasks/active.md` to the bottom of
     `data/tasks/done.md` (create `done.md` if missing).
4. For "update": ask what to change (priority section, due, blocker)
   and edit the line in place. Move the line to the matching H2 section
   if priority changed.
5. Confirm the change and show the updated task view.

### 3. Add

**Triggers:** `/tasks add "description"`, `/tasks new`

**Steps:**

1. Parse the description from the command, or ask if not provided.
2. Prompt for required metadata:
   - **Priority:** Now / Next / Later (default Next)
   - **Due Date:** Optional (YYYY-MM-DD)
   - **Blocker:** Optional
3. Append the line to the matching H2 section in
   `data/tasks/active.md`. Format:
   `- [ ] {title} <!-- priority:{now|next|later} due:{date or ""} blocker:"{text or ""}" -->`
   Create `active.md` (with H1 + Now/Next/Later H2 scaffolding) if it
   does not exist.
4. Confirm creation and show where it landed in the task view.

## Session Start Behavior

Per the CLAUDE.md rule "At the start of every conversation, run `/tasks`":

1. Automatically run the View mode at session start.
2. Keep the output concise — no more than 15-20 lines for a typical
   task load.
3. If the user says "skip tasks", do not show the task view.
4. After showing tasks, ask: "What would you like to work on?" or
   proceed with whatever the user has already asked.

## Relationship to /fetch-context

- `/tasks` provides a **focused, actionable task view** — "what am I
  working on right now?"
- `/fetch-context` provides **broad product context** — decisions,
  personas, backlog, recent Signals, Market Landscape — for skills that
  need to understand the product landscape.

They both read `data/tasks/active.md` but serve different purposes.
`/tasks` is user-facing daily workflow. `/fetch-context` is skill-facing
context hydration.

## Suggested Follow-ups

After viewing tasks:
- If blockers exist: "Want me to help unblock {task}?"
- If a task is overdue: "{task} is past due. Want to reprioritize?"
- If the backlog is large (>15 active): "You have {n} active items.
  Want to run `/break-down` to tighten scope?"

After completing a task:
- "Want to pull the next item from the Next section?"
- If it was a significant milestone: "Worth logging this as a decision?
  Run `/log-decision`."
