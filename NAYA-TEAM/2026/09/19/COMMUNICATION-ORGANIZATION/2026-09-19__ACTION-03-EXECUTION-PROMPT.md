# ACTION 03 — CANONICAL RELATIONSHIP SUBSTRATE

**Date:** 2026-09-19  
**Owner:** Lead Naya  
**Repository:** SoulSchoolAcademy/NayaPOWER  
**Supabase:** dahisasgpfvziswqvmvm  
**Status:** IMMEDIATE EXECUTION

## MISSION

Reconcile `v7_connection_requests` into the canonical relationship model without creating a duplicate connection graph.

## WHY

Membership is absent. Before implementing it, NayaNET must know whether the existing connection-request primitive is request-only, already represents durable relationship state, or is legacy state that should be projected.

## EXACT INSPECTION

1. Inspect `v7_connection_requests` columns, constraints, indexes and RLS.
2. Inspect every live public function related to connection/request/relationship.
3. Inspect migration history for creation/evolution of the request primitive.
4. Inspect all available GitHub source references.
5. Determine pending/accepted/rejected semantics.
6. Determine whether accepted requests create durable relationship state anywhere.
7. Determine whether the relationship is directional or mutual.
8. Determine whether Space membership can be a relationship origin.
9. Determine duplicate-prevention semantics.
10. Determine multi-origin merge semantics.
11. Determine revocation/leave semantics.
12. Determine communication eligibility semantics.
13. Record exact evidence in Team Naya and feature records.

## HARD RULES

- Do not create a new `connections` table during this action.
- Do not create Space membership during this action.
- Do not weaken RLS.
- Do not bypass authority.
- Do not treat UI state as relationship state.
- Do not infer accepted semantics from column names alone.

## REQUIRED OUTPUT

**DONE** — exact reconciliation completed.

**PROOF** — exact schema, RLS, functions, migrations, source references, rows and observed states.

**NOT PROVEN** — every unresolved relationship behavior.

**DECISION** — canonical relationship ownership and state machine.

**BLOCKERS** — exact blockers.

**NEXT** — a complete successor execution directive for Action 04.

## SUCCESS CONDITION

The next executor can implement JOIN→MEMBERSHIP without creating a second identity or relationship graph.
