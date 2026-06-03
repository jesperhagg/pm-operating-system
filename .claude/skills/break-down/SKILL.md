---
description: Break down a PRD or feature idea into kanban-ready work items. Reads current backlog from data/tasks/ and decomposes work into small, independently deliverable tasks using JTBD framing.
---

# Break Down

## Before Starting — Self-Hydration

1. Identify the current product (read CLAUDE.md for Repo Identity, or ask the user)
2. Locate the PRD to decompose:
   - If the user specifies a PRD file path, read it
   - If a PRD was just generated in this conversation, use it
   - If neither, ask the user what feature or idea to break down
3. Read:
   - `tasks/active.md` — scan Now/Next/Later to avoid duplicating existing tasks.
   - Grep `context/product/decisions.md` for `type:Scope`, `type:Architecture`, or `type:Technical` and `status:Active` (last 90 days). Open the 2–4 most relevant H2 blocks.
   - Grep `context/users/personas.md` for H2 headings; read the primary persona block (to ground JTBD framing).
   - If `context/learnings/break-down.md` exists, read the top 3–5 H3 entries. Apply silently to this run — do not narrate prior lessons back to the user.
4. Briefly summarize context before proceeding

## Decomposition Framework

Break the PRD into work items following these principles:

### Sizing Rule
Each task should be completable in **one focused session** (roughly 2-4 hours).
If a task feels larger, split it. If it feels trivial, merge it with a related task.

### JTBD Framing
Write each task title as a Job to Be Done:
> "When [situation], I want to [action], so I can [outcome]"

This keeps every task tied to user value, not implementation detail.

### Task Structure
For each work item, provide:

1. **Title** — JTBD-formatted
2. **What to build** — concrete scope (2-3 sentences max)
3. **Done when** — observable acceptance criteria (not "code is written" but "user can X")
4. **Depends on** — list any tasks that must be completed first (by title reference)
5. **Risk flag** — note if this task carries technical uncertainty or needs discovery first

### Ordering Rules
- Order tasks by **dependency chain first**, then by **user value**
- Tasks with no dependencies that deliver visible user value come first
- Infrastructure/setup tasks come early only if they unblock multiple downstream tasks
- Flag tasks that can be worked on in parallel

### WIP Discipline
- Suggest a WIP limit (typically 1-2 for a solo founder)
- Mark the first 1-2 tasks as "Pull next" — these are what to start building
- Remaining tasks are "Backlog" — ordered but not yet active

## Output

Present the breakdown as:

```
# [Feature Name] — Work Breakdown

## Pull Next (WIP limit: N)
1. [Task title — JTBD format]
   - **Build:** [scope]
   - **Done when:** [criteria]
   - **Depends on:** none
   - **Risk:** [if any]

## Backlog (ordered)
2. [Task title]
   ...

## Parking Lot
- [Ideas that surfaced during breakdown but are out of scope]
```

## Scope Creep Check

After generating the breakdown:
- Count the tasks. If more than 8-10 for a single feature, flag it: the PRD scope may be too large
- If scope creep is detected, suggest the user either narrow the PRD or split it into multiple features
- Suggest running `/evaluate-opportunity` if the feature scope has grown beyond the original intent

## Capture Learning

After delivering the breakdown, append one H3 entry to `context/learnings/break-down.md` (create with `# Learnings — break-down` H1 if missing). Newest first. Mark `session:pending` — `/context-sync` will reconcile.

```markdown
### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:break-down session:pending -->

**Worked:** {one sentence — which decomposition / sizing / ordering move produced the cleanest tasks}.
**Missed:** {one sentence — tasks that were too big, too small, or hid risk}.
**Next time:** {one adjustment — sizing heuristic, dependency check, scope-creep trigger}.
```

Keep entries three lines, not three paragraphs.

## After Completing

Suggest the user might want to:
- Build each "Pull Next" task test-first with `/spec-feature` — turn its `Done when:` into failing tests, then code until green.
- Append the top "Pull Next" items to `tasks/active.md` under the Now section via `/tasks add` (priority:now).
- Run `/log-decision` if the breakdown committed to a scope choice worth recording.
- Consult the **product-sculptor** agent if further scope reduction is needed.
