# 🔱 Active Living Brain — 2026-09-23

## What happened
Shawn clarified the required end state for NayaPOWER/NayaNET:
> Meaningful experience must have the opportunity to become understood, durable, reusable intelligence. It must not remain an inert note that has to be re-taught repeatedly.

The governing concept is now **Active Living Brain / Compounding Intelligence**.

## Architectural decision
Do not create a second brain.

Use the existing canonical chain:
EXPERIENCE → INTELLIGENT EVENT → INTELLIGENCE → INTELLIGENT BLOCK → PERSISTENCE/INDEX → RETRIEVAL → APPLY → VERIFY → LEARNING → COMPOUNDING → SUPERBRAIN.

The missing integration concept is the **Cognitive Checkpoint**: a durable, provenance-bound declaration of what the system currently understands after a meaningful cognition cycle.

## Existing machinery reused
- cognition / Intelligent Events
- Intelligent Blocks
- Smart Notes
- intelligence index
- learning evidence
- learner state
- Dream/replay
- decision context
- execution receipts
- Smart Ledger
- Project Intelligence restore/retrieval
- successor handoff
- governed authority
- supersession lineage
- nayanet-compound-intelligence

## New canonical directive
.naya/TEAM-NAYA/01-ACTIVE-LIVING-BRAIN-COMPOUNDING-INTELLIGENCE-V1.md

All Nayas must use this as the operating contract for compounding intelligence.

## Immediate implementation boundary
A governed checkpoint operation has been added to the existing compound-intelligence runtime. It does not create a second store. It records a provenance-bound cognition checkpoint through the existing canonical cognition/receipt machinery.

## Important limitation
A runtime checkpoint primitive does not by itself make every ChatGPT conversation automatically persistent. Automatic capture requires the calling Naya/runtime surface to invoke the governed checkpoint boundary. The next integration step is therefore to connect the existing Smart Note/conversation capture path to the checkpoint operation and prove the behavioral no-replay chain.

## Current proof status
**DESIGN/CONTRACT: ESTABLISHED**
**RUNTIME PRIMITIVE: SOURCE IMPLEMENTED**
**FULL AUTOMATIC CONVERSATION CAPTURE: UNKNOWN**
**NO-REPLAY BEHAVIORAL PROOF: OPEN**

## Protected rule
Do not claim “Naya learned” because a row exists.
Naya has learned only when retained intelligence is later retrieved and demonstrably changes future behavior, with the relevant evidence preserved.

## Success condition
Shawn teaches an important lesson once.
A cold Naya later:
1. restores context,
2. retrieves the learned intelligence,
3. understands it,
4. applies it without re-teaching,
5. verifies the outcome,
6. updates learning,
7. checkpoints the new state,
8. leaves a successor another cold Naya can continue.

That is the acceptance target.

## Source implementation
The existing nayanet-compound-intelligence runtime now exposes action `checkpoint` with schema `NAYANET_INTELLIGENCE_CHECKPOINT_V1`. It is authenticated, cold-restore-gated, provenance-bound to existing cognition events, idempotent by checkpoint identity, and explicitly refuses to equate checkpoint persistence with proof of learning.

**Live production deployment/proof remains OPEN.** The source change must be deployed through the existing governed Supabase runtime boundary before the new operation can be called as production-proven.
