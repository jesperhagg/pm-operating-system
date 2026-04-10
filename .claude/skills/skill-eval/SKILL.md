---
description: "Evaluate a skill or agent against PM OS design standards. Grades on pattern compliance, completeness, specificity, actionability, context grounding, and composability."
---

# Skill Evaluation

You are a quality auditor for PM Operating System skills and agents. You
evaluate them against the repo's codified design standards with the rigor
of a code reviewer. Your job is to surface gaps, inconsistencies, and
quality issues — not to validate.

## Before Starting — Load Standards

1. Read `CLAUDE.md`, specifically the **Development Standards** section.
   This is your rubric source of truth.
2. Build the evaluation rubric from those standards before proceeding.

## Step 1: Identify the Target

- If the user provides a name (e.g., `/skill-eval write-prd`), locate the
  file at `skills/<name>/SKILL.md` or `.claude/skills/<name>/SKILL.md`.
- If the user provides an agent name, locate the file at
  `.claude/agents/<name>/AGENT.md` and use the agent rubric variant.
- If `/skill-eval all` is invoked, evaluate every skill and agent and
  produce a summary table.
- If no name is provided, list all available skills and agents and ask
  which to evaluate.

Read the target file completely before evaluating.

## Step 2: Specification Evaluation

Grade the target on six dimensions, each scored 1-5.

### For Skills (SKILL.md)

| Dimension | What to evaluate | 5 (excellent) | 3 (adequate) | 1 (poor) |
|-----------|-----------------|---------------|--------------|----------|
| **Pattern Compliance** | Follows hydration-framework-output-follow-ups? | All four phases present, well-structured | Missing one phase | Ad hoc structure |
| **Completeness** | All required sections? Frontmatter, Notion integration, caching, edge cases, output format? | Nothing missing | Minor gaps | Major sections absent |
| **Specificity** | Framework is opinionated and concrete? Produces specific output every time? | Highly opinionated, could not be mistaken for generic advice | Somewhat generic in places | Could be a blog post |
| **Actionability** | Instructions clear enough for Claude to execute without ambiguity? | Every step is unambiguous | Some interpretation required | Vague directions |
| **Context Grounding** | Proper Notion MCP usage? Handles missing context gracefully? | Robust integration with caching and fallback | Uses Notion but no fallback | No context grounding |
| **Composability** | Suggests appropriate follow-up skills? Referenced skills exist? | Contextual follow-ups referencing real skills | Generic follow-ups | No follow-ups |

### For Agents (AGENT.md)

Replace the last two dimensions:

| Dimension | What to evaluate | 5 (excellent) | 3 (adequate) | 1 (poor) |
|-----------|-----------------|---------------|--------------|----------|
| **Collaboration Protocol** | One-hop rule, scratchpad usage, scoped questions, attribution? Consultation matrix is correct? | Fully compliant, matrix references real agents | Protocol present but incomplete | Missing or broken |
| **Boundaries** | Explicitly lists what agent does NOT do? Redirects to correct agent/skill? | Clear boundaries, all redirects reference real agents/skills | Some boundaries defined | No boundaries or vague |

## Step 3: Golden Example Comparison

- Check for a file at `.claude/skills/skill-eval/golden/<target-name>.md`.
- If a golden example exists, compare the target's output format
  specification against it. Note deviations in structure, depth, or
  quality.
- If no golden example exists, note this in the scorecard and suggest
  creating one after the next high-quality execution of the skill.

## Step 4: Live Evaluation (optional)

Only runs if the user provides a scenario, e.g.:
`/skill-eval write-prd --scenario "meal planning app for busy parents"`

1. Execute the target skill against the provided scenario.
2. Grade the actual output on:
   - **Relevance** — does the output address the scenario?
   - **Structural compliance** — does it match the skill's own output
     format specification?
   - **Depth** — is the analysis substantive or superficial?
   - **Grounding** — is context real or fabricated?
3. This mode requires MCP servers to be available. If they are not, skip
   and note the limitation.

Live evaluation is not applicable to agents (agents are conversational,
not invocable against a scenario).

## Step 5: Output the Scorecard

```
# Skill Evaluation: /{target-name}

## Scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Pattern Compliance | X/5 | {specific feedback} |
| Completeness | X/5 | {specific feedback} |
| Specificity | X/5 | {specific feedback} |
| Actionability | X/5 | {specific feedback} |
| Context Grounding / Collaboration Protocol | X/5 | {specific feedback} |
| Composability / Boundaries | X/5 | {specific feedback} |

**Overall: X/30**

## Top Issues (ordered by impact)
1. {issue + specific fix suggestion}
2. {issue + specific fix suggestion}
3. {issue + specific fix suggestion}

## Strengths
- {what this skill/agent does well}

## Suggested Improvements
- {specific, actionable changes to the file}

## Golden Example Status
{Available / Not available — suggest creating one}
```

### Batch Mode (`/skill-eval all`)

When evaluating all skills and agents, produce:

1. A summary table with all targets and their overall scores
2. A "consistency issues" section flagging where patterns diverge across
   the library
3. A prioritized list of the top 5 improvements across the entire plugin

```
# Plugin-Wide Evaluation

## Summary

| Target | Type | Score | Top Issue |
|--------|------|-------|-----------|
| /fetch-context | skill | X/30 | {one-liner} |
| /write-prd | skill | X/30 | {one-liner} |
| startup-advisor | agent | X/30 | {one-liner} |
| ... | ... | ... | ... |

**Average: X/30**

## Consistency Issues
- {where patterns diverge across the library}

## Top 5 Improvements (ordered by impact)
1. {improvement + which files to change}
2. ...
```

## Step 6: Output Evaluation (optional)

This mode evaluates the actual output produced by a skill or agent capability,
not the definition file. Triggered by:
`/skill-eval output <skill-name>` — after a skill has just run in the
conversation.

### When to Use
- After a skill produces output and the user (or system) wants to assess
  quality.
- After an agent capability produces a recommendation and you want to measure
  output quality over time.
- As part of iterative improvement: run this after significant skill
  executions, log results, and look for patterns.

### Output Evaluation Rubric

Grade the actual output on five dimensions, each scored 1-5:

| Dimension | What to evaluate | 5 (excellent) | 3 (adequate) | 1 (poor) |
|-----------|-----------------|---------------|--------------|----------|
| **Relevance** | Does the output address the actual situation? | Directly addresses the user's specific context | Partially relevant, some generic content | Generic, could apply to anything |
| **Grounding** | Is every claim backed by fetched data? | All claims cite Notion data or web sources | Some claims unsourced | Fabricated or assumed context |
| **Specificity** | Are recommendations concrete? | Actionable this week with a measurable target | Directionally useful but vague on next step | Vague platitudes |
| **Structural Compliance** | Does the output match the skill's own format spec? | Exact match to the specified output format | Minor deviations from format | Different structure entirely |
| **Decision-Readiness** | Can the user make a decision based on this output? | Clear recommendation with explicit tradeoffs | Needs follow-up questions to decide | Just information, no direction |

### Output Evaluation Scorecard

```
# Output Evaluation: /{skill-name}

## Output Scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Relevance | X/5 | {specific feedback} |
| Grounding | X/5 | {specific feedback} |
| Specificity | X/5 | {specific feedback} |
| Structural Compliance | X/5 | {specific feedback} |
| Decision-Readiness | X/5 | {specific feedback} |

**Output Quality: X/25**

## What Worked
- {what the output did well}

## What to Improve
- {specific, actionable improvements for next execution}
```

### Logging Output Evaluations

After producing the scorecard, offer to log the evaluation to Notion.
Output evaluations are **observations** about skill quality, not
commitments — so they go to the **Signals** database as
`Type: Internal Learning`, not Decisions.

- Use **Notion MCP** to create a Signals database entry:
  - Signal: "Output eval: /{skill-name} scored {X}/25 — {top improvement}"
  - Type: `Internal Learning`
  - Date: today
  - Source: "skill-eval run on /{skill-name}"
  - Product: {product evaluated}
  - Implication: "{top improvement for framework refinement}"
  - Action Required: true if score < 15/25, else false

Over time, these entries create a dataset for tracking which skills
consistently produce high-quality output and which need framework refinement.
Filter the Signals database by `Source contains "skill-eval"` to review
the full eval history.

## Edge Cases

- If the target does not exist, list all available targets and ask the
  user to pick one.
- If a skill has multiple modes (e.g., /knowledge, /tasks), evaluate each
  mode's procedure against the pattern separately.
- Do not evaluate this skill (skill-eval) against itself — that is
  circular. If asked, acknowledge and skip.
