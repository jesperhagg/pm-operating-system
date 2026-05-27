---
description: Capture non-obvious knowledge the coding agent uncovered during a session into docs/agent-playbook.md so the next session inherits it. Closes the "recursing six levels deep for credentials" trap. Softer cousin of /encode-constraint — used when the gap is missing knowledge, not a coding mistake.
---

# Agent Playbook Update

When the coding agent burns time discovering something non-obvious — where staging creds live, why a script must run twice, an undocumented API quirk, a generated-file path that must not be hand-edited — that knowledge belongs in `docs/agent-playbook.md`. Next session reads it before writing a line. The same question never gets answered twice.

**When to run:**
- A session just uncovered a piece of repo knowledge that wasn't documented (took >5 minutes to figure out).
- A mistake was caused by missing context rather than a coding error.
- Onboarding a new tool, secret store, or environment variable.

**When NOT to run:**
- The gap is a class of coding mistake — use `/encode-constraint` instead (stronger artifact).
- The knowledge is one-off and won't recur — don't pollute the playbook.

## Step 1 — Hydrate

1. Confirm cwd is a consumer product repo with `docs/agent-playbook.md`. If not, halt: *"Run `/scaffold-constraint-layer` first."*
2. Ask the user (or extract from conversation context):
   - **What did the agent learn?** One to three sentences.
   - **What was the failure mode before?** What did the agent waste time on, or what did it get wrong?
   - **Where is the canonical source of this knowledge?** (a file path, a vault, a person, an external doc). If there is one, the playbook entry points at it rather than restating it.
3. Read the current `docs/agent-playbook.md` end-to-end. The new entry might extend an existing bullet rather than start a new one — and the section heading determines where it lands.

## Step 2 — Pick the Section

The playbook has six standard H2 sections. Place the entry under the first one that fits.

| Knowledge type | Section |
|---|---|
| How to run, build, test, deploy | `## How to Run This Project` |
| Where source / generated / config files live | `## Where Things Live` |
| Where secrets and env vars come from | `## Credentials and Secrets` |
| Quirks, gotchas, time-wasting traps | `## Quirks and Gotchas` |
| Hard rules — things the agent must not do | `## What the Agent Must Not Do` |
| Project-specific terminology with a precise meaning | `## Glossary` |

If none fit, add a new H2 — but be sure: every new section is a small tax on every future read.

## Step 3 — Write the Entry

Rules for the entry itself:

- **One to three bullets.** If it's longer, you're explaining; the playbook is for the agent, not a tutorial.
- **Imperative or factual.** "Run X before Y." "Files in `_generated/` are written by the codegen step." Not "we usually..." or "you might want to..."
- **No secret values.** Point at the mechanism (1Password vault name, `.env.example`, the team member), never the secret.
- **Link out for depth.** If the canonical doc lives elsewhere, link it — don't copy.
- **Date-free.** The playbook is timeless. If something is true only until next quarter, it doesn't belong here.

Append the entry to the chosen H2 section. If the section already contains an example placeholder bullet (left over from the template), delete it as you add real content.

## Step 4 — Output

```
## agent-playbook-update — Result

**Section:** `## {section heading}`
**File:** docs/agent-playbook.md
**Action:** {appended | merged into existing bullet | created new section}

### Entry written

{the exact text appended}

### Verification

To confirm the next session inherits this, in a fresh Claude Code session ask: *"What do you know about {specific topic}?"* — the answer should cite the playbook line.
```

## Follow-ups

- If the same knowledge gap caused a coding mistake (not just lost time) → also run `/encode-constraint` to add a stronger artifact (test or lint).
- If the playbook has grown past ~300 lines → consider splitting into `docs/playbook/<area>.md` and updating the main playbook to be a router.
- Multiple onboarding gaps caught in one session → `/encode-constraint` for the architectural ones; rest into the playbook.

## Anti-Patterns

- **Don't restate the canonical doc.** If 1Password has the creds, the playbook says "creds are in 1Password vault `staging`," not the values. The playbook is a router, not a duplicate.
- **Don't write conversationally.** "Hey, just so you know..." is noise. Imperative or factual only.
- **Don't add a knowledge entry for a class of coding mistake.** That's `/encode-constraint`'s job — a lint or a test, not a paragraph.
- **Don't paste secrets, tokens, or API keys.** Even "example" ones. Every paste eventually leaks.
- **Don't grow the playbook into a wiki.** When in doubt, link out. The playbook is read top-to-bottom by every fresh session — keep it scannable.
