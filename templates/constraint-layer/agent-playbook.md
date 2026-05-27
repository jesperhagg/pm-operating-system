# Agent Playbook

_The first doc the coding agent should read in this repo. Everything here is non-obvious knowledge the agent would otherwise have to discover the hard way._

_Grown by `/agent-playbook-update` whenever a session uncovers something undocumented. Don't let the same question get answered twice — encode it here._

## How to Run This Project

_(Fill in: how to start the dev server, how to run tests, how to run lints, how to build, how to deploy. One command per line. Include any prerequisites.)_

```
# Example placeholders — replace per stack
make dev          # start local dev environment
make test         # run the test suite
make lint         # run linters
make ship         # deploy to staging
```

## Where Things Live

_(Fill in: directory map. Don't duplicate `architecture.md` — list only paths the agent needs to find files quickly.)_

- Source code: `src/`
- Tests: `tests/`
- Generated code (do not hand-edit): _(list paths)_
- Config: _(list paths)_

## Credentials and Secrets

_(How the agent obtains credentials it needs for local dev or staging. Never paste secret values here — point at the mechanism: 1Password vault, `.env.example`, the team member to ask, etc.)_

- Local `.env` template: `.env.example` (copy to `.env` and fill in)
- Staging secrets: _(source)_
- Production secrets: _(source, or "agent must not access")_

## Quirks and Gotchas

_(Things that would make a fresh agent waste a session. Add a bullet every time you catch one.)_

- _(example) The migration script must be run twice — first pass creates the schema, second pass seeds defaults._
- _(example) `npm run build` fails on the first run after dependency changes; run `npm ci` first._

## What the Agent Must Not Do

_(Hard rules. Things the review-agent and CI should also enforce, but listed here as the first line of defense.)_

- Do not hand-edit files in `_generated/`.
- Do not commit `.env` or anything matching `*secret*`, `*credential*`, `*.pem`.
- Do not bypass the test suite with `--no-verify`, `skip`, or commented-out tests.
- Do not introduce a new top-level dependency without updating `architecture.md`.

## Glossary

_(Project-specific terms that have a precise meaning. The agent will misuse them otherwise.)_

- _(example) **Tenant** — a customer organization. Always scoped at the request layer; never query across tenants._
