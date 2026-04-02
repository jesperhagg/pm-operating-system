# FellingPal — Product Context

## What it is

A forestry compliance assistant for Swedish small-scale forest owners. Auto-
prepares avverkningsanmälan (felling notices), pulls parcel data, flags
protected areas, and tracks approval status with Skogsstyrelsen.

NOT a general forestry management platform, timber marketplace, or GIS tool.

## Target users

- **Primary — "The Small Forest Owner":** Private individual owning forest
  land, handling one or a few felling operations per year, unfamiliar with
  regulatory details.
- **Secondary — "The Forestry Consultant":** Advisor or contractor managing
  notices and compliance on behalf of multiple landowners.
- **Tertiary — "The Association / Contractor":** Forest owner associations
  and local harvesting contractors who batch-process notices at scale.

## Core user journey

Parcel selection → parcel data pull (GIS/cadastral) → avverkningsanmälan
auto-preparation → protected-area & environmental flagging → samråd
handling → submission to Skogsstyrelsen → approval status tracking

## What makes it hard to copy

1. **Deep Swedish regulatory knowledge** — forms, terminology, exception
   handling, and procedural nuances specific to Skogsstyrelsen.
2. **Parcel & GIS integration** — automated data pull from Swedish cadastral
   and geographic sources, pre-populated into notices.
3. **Audit trail & compliance memory** — tracks submission history, approval
   status, and regulatory changes per parcel over time.

## Key terminology

- **Avverkningsanmälan** — mandatory felling notice submitted to
  Skogsstyrelsen before harvesting can proceed
- **Samråd** — consultation process required when environmental or cultural
  values are affected
- **Skogsstyrelsen** — the Swedish Forest Agency; regulatory authority
- **Blanketter** — official forms used for notices and compliance filings
- **Skiften / parceller** — forest parcels identified by cadastral data

## Design principles

1. **Local-first** — Swedish forms, GIS context, and Skogsstyrelsen
   terminology baked in; not a localized global product
2. **Compliance-correct** — accuracy over speed; every notice must meet
   regulatory requirements before submission
3. **Reduce manual burden** — auto-fill from parcel data, flag known
   exceptions, minimize re-entry
4. **Transparent status** — clear visibility into where each notice sits
   in the approval pipeline

## Business model

Local B2B SaaS — subscription per user or per organization. Pricing TBD.
Potential tiers: individual forest owner vs. consultant/association with
batch workflows.

## Market context

Sweden's forestry sector employs ~115,000 people, 75% of forest land is in
active use, and roughly 1% of the resource is felled annually. That creates
a large, recurring compliance surface for a narrow, focused software product.

## Solution complexity

Medium. The workflows are narrow, but geography, parcel data, and legal
exception handling matter a lot. Getting the regulatory details right is
the moat.

## What NOT to do

- Do not apply Sagokraft's educational framing, personas, or content
  principles here
- Do not apply Selftaped's consumer/speed-first approach here
- Do not build a general forestry management suite — stay narrow on
  compliance
- Do not assume English-first; the product domain is inherently Swedish
