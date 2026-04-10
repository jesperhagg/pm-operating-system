---
description: Surface active tasks from the Notion backlog with sprint-style formatting. Runs at session start by default. Supports viewing, updating, and adding tasks.
---

# Task Management

This skill surfaces active tasks from the user's Notion backlog database
and presents them in a structured sprint-style view. It is designed to run
at the start of every session (per the CLAUDE.md session start rule) so
the user always begins with visibility into their current work.

## Expected Notion Database: Task Management

This skill queries the shared Task Management database (see **Notion
Database Schema** in CLAUDE.md for full property definitions). This is a
single database shared across all products — always filter by the
**Product** property matching the current product identity.

When no product identity exists or the user asks for a portfolio view,
show all products grouped by product.

## How to Identify the Current Product

1. Read the repo's CLAUDE.md file
2. Look for the "Repo Identity" section or product name
3. If working across a portfolio, show tasks for all products grouped
   by product
4. If no product identity exists, show all tasks

## Modes

### 1. View (default)

**Triggers:** `/tasks`, session start (automatic per CLAUDE.md rule),
"what am I working on", "what's active"

**Steps:**

1. Use Notion MCP to query the backlog database.
2. Filter to tasks with Status != `Done` (or equivalent).
3. Sort by: Status (In Progress first), then Priority (High first),
   then Due Date (soonest first).
4. Present in this format:

```
# Active Tasks — {today's date}

## In Progress
- [ ] **{Task title}** — {Product}, Priority: {priority}
  {Blocker if any: "Blocker: {description}"}
  {Due: {date} if set}

## Waiting On
| Task | Waiting For | Since | Next Action |
|------|-------------|-------|-------------|
| {title} | {person/dep} | {date status changed} | {suggested follow-up} |

## Up Next (top 3 from backlog by priority)
- [ ] **{Task title}** — {Product}, Priority: {priority}

---
{total count} tasks across {n} products. {overdue count} overdue.
```

5. If there are overdue tasks (past due date), flag them prominently
   at the top.
6. If there are no active tasks, say so and suggest reviewing the backlog.

### 2. Update

**Triggers:** `/tasks done "task name"`, `/tasks update "task name"`

**Steps:**

1. Search the Notion backlog for a task matching the given name.
2. If multiple matches, show them and ask the user to pick one.
3. For "done": Update the task's Status to `Done` in Notion.
4. For "update": Ask what to change (status, priority, blocker, notes)
   and update accordingly in Notion.
5. Confirm the change and show the updated task view.

### 3. Add

**Triggers:** `/tasks add "description"`, `/tasks new`

**Steps:**

1. Parse the description from the command, or ask if not provided.
2. Prompt for required metadata:
   - **Product:** Which product (suggest based on current context)
   - **Priority:** High / Medium / Low
   - **Status:** Default to `To Do`
   - **Due Date:** Optional
3. Create the task in the Notion backlog database via MCP.
4. Confirm creation and show where it landed in the task view.

## Session Start Behavior

Per the CLAUDE.md rule "At the start of every conversation, run `/tasks`":

1. Automatically run the View mode at session start.
2. Keep the output concise — no more than 15-20 lines for a typical
   task load.
3. If the user says "skip tasks", do not show the task view.
4. Check if `.claude/memory/shared.md` contains Notion fallback entries
   (decisions or signals logged locally because Notion was unavailable).
   If so, prompt the user: "There are {n} entries in local memory that
   should be synced to Notion. Want me to sync them now?"
5. After showing tasks, ask: "What would you like to work on?" or
   proceed with whatever the user has already asked.

## Relationship to /fetch-context

- `/tasks` provides a **focused, actionable task view** — "what am I
  working on right now?"
- `/fetch-context` provides **broad product context** — decisions,
  personas, backlog, recent Signals, Market Landscape — for skills that
  need to understand the product landscape.

They query the same Notion backlog but serve different purposes. `/tasks`
is user-facing daily workflow. `/fetch-context` is skill-facing context
hydration.

## Caching

Cache the task list within a session. Re-fetch after any update or add
operation. If the user asks to see tasks again without changes, use the
cached version.

## Suggested Follow-ups

After viewing tasks:
- If blockers exist: "Want me to help unblock {task}?"
- If a task is overdue: "{task} is past due. Want to reprioritize?"
- If the backlog is large: "You have {n} backlog items. Want to run
  `/break-down` to organize them?"

After completing a task:
- "Want to pull the next item from the backlog?"
- If it was a significant milestone: "Worth logging this as a decision?
  Run `/log-decision`."
