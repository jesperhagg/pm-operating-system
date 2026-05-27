# Architecture

_System map for the coding agent. Short. Updated when structure changes — not aspirational._

## What This Project Is

_(One paragraph. What the system does, who uses it, the single sentence a new engineer needs to understand the rest of this doc.)_

## High-Level Shape

_(Diagram or bullet list. Services, processes, deployment targets. Where each thing runs.)_

```
# Example placeholder
client (web) ──► api (FastAPI) ──► postgres
                       │
                       └─► background workers (RQ) ──► redis
```

## Components

_(One H3 per component. Path, responsibility, one-line summary of what it owns.)_

### _(example)_ `src/api/`

HTTP layer. Owns request validation, auth, response shaping. Does not contain business logic — delegates to `src/domain/`.

### _(example)_ `src/domain/`

Business logic. Pure functions over domain models. No I/O, no framework imports.

### _(example)_ `src/infra/`

Adapters: database, message broker, external APIs. Implements interfaces defined in `src/domain/`.

## Data Flow — Hot Paths

_(2-3 numbered flows for the most-touched user actions. Step-by-step. The agent reads this before changing anything in the request layer.)_

### _(example)_ Creating an order

1. `POST /orders` lands in `src/api/orders.py`
2. Validated against `OrderCreate` schema
3. Handed to `domain.orders.create_order()`
4. Persisted via `infra.db.orders.insert()`
5. Event published to `infra.events.bus`

## Constraints

_(Things that constrain design choices. Not preferences — hard limits.)_

- _(example) Database is single-region. No cross-region replicas; design for one primary._
- _(example) No long-running requests — workers handle anything >2s._
- _(example) Tenant isolation enforced at the query layer. Never select across tenants._

## What's NOT in Scope

_(Adjacent systems the agent might confuse for this one. Names + one-line "that's a different repo / service.")_
