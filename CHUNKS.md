# PM OS Architecture Shift — Chunked Plan

Reference doc for the skills-first architecture shift. Splits the work into 3 gated chunks so each decision is isolated.

## Context

Moving PM OS from agent-orchestration to **skills-first + lightweight chat personas**:

- Skills are self-sufficient: methodology baked in, no reliance on agent judgment.
- Agents are no longer orchestrators. They don't lead workflows, don't hydrate Notion, don't spawn peers.
- Agents become lightweight chat personas — worldview, decision principles, pushback style. Invoked in-chat for ad-hoc conversation only.

Current state: 5 heavy agents (189–338 lines) loaded with orchestrator machinery — Proactive Checks, Notion hydration, Collaboration Protocol, Memory Protocol, Output Format. Most of it becomes dead weight under the new paradigm.

---

## Chunks

### Chunk 1 — Audit existing *(in progress)*
Skills audit + agents audit through the skills-first lens. Produces a punch list of what to keep, rewrite, split, or delete. **Executed below.**

**Gate:** Approve punch list + answer 4 open questions before Chunk 2.

### Chunk 2 — Redesign agents + fill skill gaps
Propose lightweight agent format, draft rewrites of 4 surviving agents, prioritize missing skills.

**Gate:** Approve new agent format + skill gap priority order before Chunk 3.

### Chunk 3 — CLAUDE.md revision
Merge Karpathy-style principles (think-before-coding, simplicity, surgical changes, goal-driven execution) into CLAUDE.md. Cut anything that doesn't change behavior.

**Gate:** Approve revised CLAUDE.md.

---

# Chunk 1 — Audit

## 1A. Skills (15 total: 11 exported + 4 internal)

### Keep as-is — self-sufficient (11)
`/break-down`, `/fetch-context`, `/knowledge`, `/log-decision`, `/log-signal`, `/market-scan`, `/tasks`, `/weekly-review`, `/generate-repo-map`, `/pm-digest`, `/skill-eval`

### Rewrite for depth (2)

| Skill | Problem | Fix |
|---|---|---|
| `/evaluate-opportunity` (55 lines) | 5-dimension scoring with no explicit 1–5 anchors. Leans on agent taste to fill rubric gaps. | Add explicit 1–5 anchors per dimension + worked example. Target ~100 lines. |
| `/write-prd` (62 lines) | Section list without templates. No falsifiability format for Hypothesis, no North Star + threshold format for Metrics. | Add worked PRD example + per-section templates. Target ~130 lines. |

### Rewrite for schema (1)

| Skill | Problem | Fix |
|---|---|---|
| `/memory-review` (77 lines) | References retired "Insights" type (now Signals). Volume guidelines don't match current schema. | Align to Decisions/Signals/KB taxonomy. |

### Rewrite for skills-first autonomy (1)

| Skill | Problem | Fix |
|---|---|---|
| `/design-review` (123 lines) | Delegates the actual review to `pm-os-creator` agent. Violates skills-first. | Embed review rubric inline (pull from `pm-os-creator` + `dev-standards.md`). No agent call. Target ~180 lines. |

### Splits — none needed
`/knowledge` and `/tasks` are multi-mode but modes are explicit via trigger words. Keep unified.

---

## 1B. Agents (5 total)

All 5 classify as chat personas *by function* — none actually orchestrate. But all are bloated with orchestrator-shaped machinery that becomes dead weight under the new paradigm.

### Rewrite lightweight (4)

| Agent | Current | Target | What stays | What dies |
|---|---|---|---|---|
| `startup-advisor` | 313 | ~60 | Skeptical tone, unit-economics obsession, anti-patterns, "demand the math" style | Proactive Checks, Product Context, Output Format, Collaboration Protocol, Memory Protocol |
| `product-sculptor` | 297 | ~60 | Linear/Vercel minimalism, 48-hour rule, "what breaks if we remove this?" | Same as above |
| `growth-engineer` | 312 | ~70 | Distribution-first, Hook-Story-Offer, one-channel-at-a-time, copy-on-request | Same as above |
| `systems-architect` | 338 | ~70 | Boring-tech preference, cost-per-user obsession, AI/LLM cost modeling | Same as above |

**Cut machinery (applies to all 4):**
- Objectives block (measurable outcomes = skills' job)
- Proactive Checks (agent shouldn't auto-query Notion)
- Product Context (agent shouldn't hydrate)
- Capabilities (When/What/Output/Follow-up template)
- Output Format templates
- Collaboration Protocol (no spawning, no scratchpad)
- Memory Protocol (user invokes `/log-decision` — agent doesn't write)
- Boundaries redirect table (replace with one-line "out of scope" note)

**Keep machinery (applies to all 4):**
- Persona paragraph
- Tone and behavior bullets
- Decision frameworks and principles
- Anti-Patterns section (these ARE the pushback triggers)

### Delete (1)

| Agent | Rationale |
|---|---|
| `pm-os-creator` (189 lines) | Redundant. Actual work is in `/design-review` and `/skill-eval` skills. Narrow chat-persona value. Fold unique rubric content into `/design-review` (which is being rewritten anyway). Remove reference from CLAUDE.md "This Repo" section. |

---

## Open questions — gate for Chunk 2

1. **pm-os-creator deletion** — agree it's redundant? Or preserve a chat-persona use case (e.g., rubber duck for designing new skills)?
2. **Agent location** — agents currently in `.claude/agents/` (internal, not exported via plugin). Export to consumer repos (`agents/` top-level) so they're invokable anywhere? Or stay internal?
3. **`/design-review` scope** — after rewrite, keep SHIP/REVISE/BLOCK verdicts, or lean advisory (blocking commits is frictionful for a solo founder)?
4. **Unified vs. split** — keep `/knowledge` and `/tasks` unified (my recommendation), or explore splitting?

---

## Critical files (touched across all chunks)

**Chunk 2 rewrites:**
- `.claude/agents/startup-advisor/AGENT.md`
- `.claude/agents/product-sculptor/AGENT.md`
- `.claude/agents/growth-engineer/AGENT.md`
- `.claude/agents/systems-architect/AGENT.md`
- `.claude/agents/pm-os-creator/AGENT.md` *(delete)*
- `skills/evaluate-opportunity/SKILL.md`
- `skills/write-prd/SKILL.md`
- `skills/memory-review/SKILL.md`
- `.claude/skills/design-review/SKILL.md`
- `.claude/context/dev-standards.md` *(update agent section conventions)*

**Chunk 3 rewrite:**
- `CLAUDE.md`

## Verification

After each chunk lands:
- `/skill-eval` on rewritten skills (pattern compliance)
- `/generate-repo-map` (refresh inventory)
- Scratch conversation with each rewritten agent (confirm chat-persona feel, no orchestration drift)
- Fresh session smoke test after CLAUDE.md revision
