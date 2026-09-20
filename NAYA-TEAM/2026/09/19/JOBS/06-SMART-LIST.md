# JOB 06 — SMART LIST
## Mission
Make Smart List the user's intentional collection layer without duplicating intelligence.

## Current known state
Readiness is low because the canonical existing list/save/favorite primitives have not yet been fully reconciled.

## Job
First discover existing list/save/favorite/storage primitives. Only then implement the smallest missing boundary.

## Build
- Map current Hub list UI.
- Find canonical owner/list/membership persistence and RLS if it already exists.
- Reuse Feed save/favorite primitives where appropriate.
- If storage is genuinely missing, create the smallest canonical model with owner/list/membership semantics; document why no existing primitive satisfies it.
- Support multiple lists without duplicating source intelligence.
- Add/remove membership without deleting source intelligence.
- Support authenticated persistence/reload.
- Enforce owner isolation and protected sharing behavior.
- Prove Cloudflare parity.

## Acceptance
A user can create/manage lists, add/remove real intelligence, reload and recover state, and another user cannot access or mutate private lists. Deleting membership never deletes the source object.

## Handoff
Update report/checklist/activity and coordinate with Feed, Tabs, Share, and Spaces.
