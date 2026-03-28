# Selftaped — Product Context

## What it is

A mobile-first app (iOS & Android) for independent actors to record
professional-quality self-tape auditions on their own — no scene partner,
camera operator, or extra equipment needed. Combines script management,
AI dialogue mocking, guided video recording, and simple editing in one
workflow.

## Target users

- **Primary — "The Independent Actor":** Professional or aspiring actor who
  auditions regularly via self-tape, works alone, values speed and simplicity.
- **Secondary — "The Acting Student":** Drama school student, budget-conscious,
  practicing scenes and building early audition reels.

## Core user journey

Script upload -> Script parsing -> Role selection -> AI dialogue mocking setup ->
Guided recording -> Review & edit -> Export / submit

## Key features (MVP scope)

- Script upload via text paste and PDF (OCR = future)
- Script parsing: character + line detection
- TTS dialogue mocking with 2-3 voice options + adjustable pacing
- Self-recorded reader line mode with basic AI adjustments (speed, pitch)
- Karaoke-style script display during recording
- Front-camera recording with framing guide
- Take management: grid view, star favorites, quick discard
- Basic trim editing + slate card generation
- MP4 export to camera roll and share sheet

## Key terminology

- **Sides** — the audition script excerpt (industry term for the pages an
  actor receives)
- **Dialogue mocking** — TTS playback of the other characters' lines during
  recording
- **Slate** — intro card with actor name, agent, and role (industry standard
  for submissions)
- **Take** — a single recording attempt of a scene
- **Reader lines** — lines spoken by off-screen characters the actor records
  against
- **Karaoke overlay** — the script display mode during recording, scrolling
  with audio

## Design principles

1. **Speed over perfection** — script to recording in under 3 minutes
2. **Solo-friendly** — every feature assumes the user is alone with just their
   phone
3. **Audition-aware** — defaults match what casting directors expect
4. **Minimal learning curve** — if you can use a camera app, you can use
   Selftaped

## Technical stack

- Built mobile-first with Lovable
- TTS: ElevenLabs / Google Cloud TTS (decision pending)
- Audio processing: Web Audio API or lightweight library
- Video: native device camera with overlay rendering
- Background segmentation: MediaPipe / TF Lite (post-MVP)
- Storage: local-first with optional cloud backup

## Out of scope for MVP (do not spec or prioritize)

- OCR script upload
- Animated scene view
- AI background replacement
- Side-by-side take comparison
- Direct casting platform uploads (Actors Access, Eco Cast)
- Advanced editing (splice, color correction)
- Collaboration features
- Monetization/subscription flows

## Success metrics

- **Activation:** % completing first full recording session within 7 days
- **Core loop:** % of sessions going script -> export
- **Retention:** WAU returning within 14 days
- **Recording quality proxy:** avg takes per session (fewer = better UX)

## Business model

TBD — freemium with limited exports OR flat subscription (open question).

## Current status

PRD v0.2 (March 2026). Prototype phase. Collecting prototype feedback.

## What NOT to do

- Do not apply Sagokraft's educational framing, personas, or content
  principles here
- Do not assume a B2B or institutional angle — this is direct-to-consumer
- Do not over-engineer — the core product philosophy is simplicity and speed
- Do not reference children, literacy, or reading development in any context
  here
