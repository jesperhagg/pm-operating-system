---
description: "Advisory review of pending changes to skills, agents, or plugin infrastructure. Flags pattern drift, inconsistency, and product-agnosticism violations. No hard blocks — recommendations only."
---

# Design Review

Advisory pre-ship review for PM Operating System changes. Surfaces issues against the design standards so you can decide whether to ship, revise, or defer. **This skill is advisory — it does not block commits.** You make the call.

## When to Run

Run `/design-review` before committing changes to any of these paths:
- `skills/*/SKILL.md` — exported skills
- `.claude/skills/*/SKILL.md` — internal skills
- `agents/*/AGENT.md` — agents
- `.claude/context/dev-standards.md` — design conventions
- `.claude-plugin/plugin.json` — plugin manifest

Also useful mid-design to sanity-check a draft before you go further.

## Trigger Phrases

- "review these changes", "design review", "check this before I commit"
- "does this look right?", "is this consistent?", "sanity check this skill/agent"

## Step 1: Gather Changes

1. Run `git diff --stat HEAD` to list modified files.
2. Run `git diff HEAD` on files within review scope.
3. If nothing is in scope (only README, scripts, etc.), say "No design-scope changes detected" and exit.
4. Also list any new, untracked files in scope — `git status --short` catches these.

## Step 2: Load Rubrics

Read as reference:
- `.claude/context/dev-standards.md` — authoritative design standards
- `.claude/REPO-MAP.md` — current inventory (to cross-check follow-ups reference real skills)

## Step 3: Review Each Changed File

### Skills (SKILL.md)

Check the four-phase pattern (Hydration → Framework → Output → Follow-ups):

| Check | What to flag |
|---|---|
| **Pattern compliance** | Skill skips a phase. Hydration missing for product-context skills. No follow-ups. |
| **Frontmatter** | Missing `description`. Description not action-oriented or not one sentence. |
| **Framework depth** | Reads like generic advice. No concrete rubric, template, or decomposition rule that produces a specific output every time. |
| **Output spec** | No explicit destination (conversation / file / Notion). Output format not shown. |
| **Notion integration** | No session caching. No fallback when Notion unavailable. Writes without user confirmation. |
| **Follow-ups** | Generic menu instead of contextual. References skills that don't exist in REPO-MAP. |
| **Product-agnosticism** | Hardcoded product name, persona, or terminology. Would fail for a different product with different Notion data. |

### Agents (AGENT.md) — new lightweight format

Check against the chat-persona format (no orchestrator machinery):

| Check | What to flag |
|---|---|
| **Section order** | Required order: Persona → Decision Principles → Challenge Style → What I Push Back On → Out of Scope. |
| **Frontmatter** | Missing `name` or `description`. |
| **Length** | Target 40–70 lines. If an agent is over ~100 lines, it's probably creeping back toward orchestrator shape. |
| **Forbidden sections** | Objectives, Proactive Checks, Product Context, Capabilities (When/What/Output/Follow-up), Output Format templates, Collaboration Protocol, Memory Protocol, Boundaries redirect tables. If any appear, flag as drift back to orchestrator pattern. |
| **Persona specificity** | Generic "you are a helpful PM advisor." Not grounded in a real mental model (e.g., "YC partner + McKinsey EM"). |
| **Push-back concreteness** | Anti-patterns too vague to trigger pushback. Should be specific, quotable one-liners. |
| **No Notion hydration** | Agent tries to fetch Notion context itself. That's the user's job (via skills). |

### dev-standards.md

| Check | What to flag |
|---|---|
| **Backwards compatibility** | Existing skills/agents no longer comply with the updated standards. List which ones break. |
| **Completeness** | Related sections not updated (e.g., file conventions changed but agent design section still references old paths). |
| **Product-agnostic drift** | Change introduces product-specific assumptions. |

### plugin.json

| Check | What to flag |
|---|---|
| **Version bump** | Exported skills added/changed without version bump. |
| **Skill list drift** | Manifest doesn't match actual files in `skills/`. |
| **Agent export** | If `agents/` is now exported, manifest reflects it. |

## Step 4: Output (Advisory Format)

```
# Design Review — {date}

## Files Reviewed
- {path} — {lines changed} — {one-line status}

## Observations
*(ordered by impact, not by severity enum)*

### 1. {Observation title}
**File:** {path}
**Issue:** {what's off and why it matters}
**Suggested fix:** {specific edit}

### 2. ...

## Consistency Check
- {Cross-file drift: e.g., 3 skills follow X pattern, this new one does Y}
- {Or: "No cross-file inconsistencies detected."}

## Recommendation
{One to three sentences. Ship as-is? Revise first? Defer? Your call — here's the tradeoff.}
```

**No SHIP/REVISE/BLOCK enum.** Present observations + a recommendation; the user decides.

## Step 5: Follow-ups

Contextual to what was reviewed:

- If framework depth flagged on a skill → `/skill-eval {skill-name}` for the full 6-dimension evaluation
- If agent drift toward orchestrator shape → re-read the agent section of `dev-standards.md` and trim
- If plugin.json changes → confirm version bump intent
- If nothing flagged → "Looks consistent. Ship when ready."

## Edge Cases

- **No git history yet** (fresh clone, new file never committed): review the file contents as-is against the rubrics. Skip the `git diff` step.
- **Large diff (10+ files)**: review in batches by type — all skills first, then all agents, then standards/manifest. Summarize per batch.
- **File deleted** (e.g., removing an agent): note the deletion, check if anything references it (follow-ups in skills, routing in CLAUDE.md, REPO-MAP entries). Flag dangling references.
