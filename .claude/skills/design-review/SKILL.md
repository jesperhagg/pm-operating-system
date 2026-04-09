---
description: "Pre-ship review gate that runs pm-os-creator analysis on pending changes to agent definitions, skill definitions, or plugin architecture. Ensures consistency and quality before commit."
---

# Design Review

A review gate for changes to the PM Operating System repo. This skill
invokes the `pm-os-creator` agent's architectural analysis on pending
changes before they are committed. It is the enforcement mechanism for
the pm-os-creator's authority over repo design.

## When to Run

Run `/design-review` before committing changes to any of these paths:
- `skills/*/SKILL.md` — exported skill definitions
- `.claude/skills/*/SKILL.md` — internal skill definitions
- `.claude/agents/*/AGENT.md` — agent definitions
- `CLAUDE.md` (Development Standards section) — design conventions
- `.claude-plugin/plugin.json` — plugin manifest

You can also run it proactively at any point during a design session to
get early feedback from pm-os-creator before finalizing changes.

## Trigger Phrases

- "review these changes", "design review", "check before committing"
- "does this look right?", "is this consistent?"
- Automatically suggested before any commit touching the paths above

## Step 1: Gather the Changes

1. Run `git diff --stat` to identify which files have been modified.
2. Run `git diff` on each modified file that falls within the review
   scope (skills, agents, CLAUDE.md, plugin.json).
3. If no changes are staged or unstaged in the review scope, report
   "No changes in scope for design review" and exit.

## Step 2: Load pm-os-creator Context

Invoke the `pm-os-creator` agent with the following brief:

1. The agent must read `CLAUDE.md` (Development Standards section) as
   its rubric source of truth.
2. The agent must scan the current skill and agent inventory to
   understand the existing patterns.
3. The agent must review the specific changes (provided as diffs).

## Step 3: pm-os-creator Review

The pm-os-creator evaluates each changed file against these checks:

### For Skills (SKILL.md changes)

- **Pattern compliance** — Does it follow hydration-framework-output-follow-ups?
- **Frontmatter** — Description present, one sentence, action-oriented?
- **Notion integration** — Proper MCP usage, caching, fallback handling?
- **Follow-ups** — Reference real, existing skills?
- **Product-agnosticism** — Would it work for any product with Notion data?
- **Consistency** — Does it match the patterns of other skills in the repo?

### For Agents (AGENT.md changes)

- **Section order** — Does it follow the standard section order from
  Development Standards?
- **Frontmatter** — Both name and description present?
- **Collaboration protocol** — Correct hop limit, scratchpad usage,
  consultation matrix references real agents?
- **Memory protocol** — Reads before analysis, writes with permission?
- **Boundaries** — Explicit, with redirects to real agents/skills?
- **Consistency** — Does it match the patterns of other agents in the repo?

### For CLAUDE.md (Development Standards changes)

- **Backwards compatibility** — Do existing skills and agents still comply
  with the updated standards?
- **Completeness** — Are all impacted sections updated consistently?
- **No drift** — Does the change maintain the product-agnostic principle?

### For Plugin Manifest (plugin.json changes)

- **Version bump** — Is the version updated appropriately?
- **Skill list** — Does it match the actual files in `skills/`?

## Step 4: Output the Verdict

```
# Design Review

## Verdict: [SHIP / REVISE / BLOCK]

## Files Reviewed
- [file path] — [status: OK / Issues found]

## Issues (if any, ordered by severity)
1. [BLOCK] [issue + specific fix]
2. [REVISE] [issue + specific fix]
3. [NOTE] [observation, non-blocking]

## Consistency Check
- [Any pattern drift detected across the library]

## Recommendation
[One sentence: what to do before committing]
```

### Verdict Definitions

- **SHIP** — Changes are consistent with design standards. No issues found.
  Proceed with commit.
- **REVISE** — Minor issues found that should be fixed before committing.
  None are architectural violations, but they reduce quality or consistency.
- **BLOCK** — Architectural violation detected (broken pattern, product-
  specific data hardcoded, inconsistent section order, missing required
  sections). Must fix before committing.

## Step 5: Follow-ups

After the review:
- If SHIP → proceed with commit
- If REVISE → fix the listed issues, then run `/design-review` again
- If BLOCK → fix the architectural violations, then run `/design-review` again
- Optionally run `/skill-eval <target>` for a deeper 6-dimension evaluation
  of a specific skill or agent
