# MASTER EXECUTION DIRECTIVE — NAYANET FEATURE CLOSURE
Date: 2026-09-19
Authority: NayaNET Engineering System / NayaPOWER governance
Execution model: one connected system, parallel work only where dependencies permit

## Mission
Turn the nine product areas below from documented designs plus partial production primitives into one authenticated, observable, verifiable NayaNET product.

The objective is not to build nine separate applications. The objective is to connect the existing intelligence, cognition, event, authorization, ledger, mail, space, retrieval, reporting, and Hub primitives into one coherent human experience.

## Vision
NayaNET should feel like one living super-engine:
Human → Hub → Retrieve → Understand → Authority → Act → Observe → Verify → Record → Present → Continue.

The interface must preserve the canonical visual baseline. Do not redesign the product. Separate clean components from the existing Hub baseline and connect them to canonical production primitives.

## Source of truth
Canonical visual baseline:
`2026 09 17 NAYANET HUB.html`

Canonical engineering system:
`NayaNETEngineeringSystem/`

Canonical feature contracts:
`NayaNETEngineeringSystem/features/`

Feature readiness and current-state evidence:
`NayaNETEngineeringSystem/ACTIVITY/2026/09/19/`

Team Naya activity:
`NAYA-TEAM/2026/09/19/`

Deployment target: Cloudflare. GitHub is source/change/review evidence. Do not substitute Vercel.

## Required reading for every Naya
1. This directive.
2. The applicable feature .naya authority and all cross-cutting .naya authorities identified by the feature.
3. The applicable feature specification.
4. The current feature readiness report.
5. The current day index and feature activity index.
6. The canonical Hub baseline.
7. The actual implementation and runtime primitives.
8. Supabase live objects relevant to the feature.
9. Existing activity/session records before changing anything.

Do not declare a feature implemented because its specification exists. Inspect source and runtime.

## Non-negotiable engineering laws
- Preserve working primitives.
- Make the smallest correct change.
- No duplicate intelligence/event stores.
- No demo state masquerading as production state.
- Capability does not create authority.
- Every read is filtered by identity, scope, visibility, and revocation rules.
- Activity is a projection/history surface, not a competing event database.
- Ledger is a durable consequence/evidence surface, not the intelligence store.
- Derived reports are not independent evidence.
- No retry without new information.
- No silent failure.
- No fake proof.
- Source → build → deployed runtime must agree.
- UI state must tell the truth about backend state.
- Every substantive session signs in, works, verifies, reports, signs out, and leaves exactly one concrete successor action.

## Shared definition of done
A feature is not SHIPPED until its applicable path reaches:

SPEC → SOURCE → RUNTIME → AUTHENTICATED ACTION → OBSERVATION → VERIFICATION → EVIDENCE → CLOUDFLARE DEPLOYED PARITY.

Where applicable, prove:
- authenticated user ownership;
- second-user denial/isolation;
- persistence and reload;
- idempotency/replay safety;
- loading/empty/error/unauthorized states;
- provenance and evidence links;
- source/build/runtime parity;
- real production data, not mock data;
- activity record and feature checklist update.

## Execution order

### WAVE A — FOUNDATION / RETRIEVAL SPINE
1. Smart Feed — primary retrieval/presentation spine.
2. Smart Tabs — persistent navigation into the retrieval spine.
3. Smart Ledger — durable consequence/evidence view connected to actions and intelligence.

These three may work in a synchronized sequence. Smart Tabs depends on real retrieval/navigation primitives exposed by Smart Feed. Smart Ledger depends on canonical event/execution/cognition consequences and must remain connected to Feed and downstream intelligence.

### WAVE B — ACTION / ORGANIZATION
4. Smart Mail — authenticated communication/action surface.
5. Smart Share — controlled publication/sharing boundary.
6. Smart List — intentional user collections.

These may synchronize where contracts intersect, but no team may invent a parallel storage model.

### WAVE C — COLLABORATION
7. Smart Spaces — authorized collaborative container and intelligence surface.

### WAVE D — SYNTHESIS / HUMAN DAILY EXPERIENCE
8. Your Intelligence Today — deterministic daily intelligence projection.
9. Intelligent Reports — period/scope synthesis with evidence lineage.

Today and Reports depend on the retrieval/evidence spine being truthful.

## Cross-feature connection map
Smart Tabs ↔ Smart Feed
Smart Feed ↔ Smart Ledger
Smart Feed ↔ Smart List
Smart Feed ↔ Smart Share
Smart Mail ↔ Smart Share
Smart Spaces ↔ Smart Feed / Share / Mail / Ledger
Today ↔ Feed / Cognition / Ledger
Reports ↔ Today / Feed / Ledger
Ledger ↔ all durable consequences

## Working protocol
For each job:
SIGN IN → READ → INSPECT → MAP → IMPLEMENT → TEST → AUTHENTICATE → VERIFY → RECORD → UPDATE FEATURE → SIGN OUT → HAND OFF.

The Naya must post:
1. what was inspected;
2. what changed;
3. exact files/objects/routes/functions affected;
4. tests performed;
5. evidence obtained;
6. current state;
7. blockers or unknowns;
8. one next action.

## Product quality bar
The result must be:
- useful immediately;
- visually faithful to the canonical Hub;
- fast and understandable;
- truthful about state;
- permission-correct;
- recoverable;
- observable;
- reconstructable;
- connected to the intelligence system;
- production-grade on Cloudflare.

A button is not complete because it renders. It is complete when it performs the promised action, survives reload, respects authority, produces observable consequences, and can be verified.

## Current master mission
Close the boundaries between the already-proven backend primitives and the human-facing product. Do not spend the cycle polishing isolated UI while the underlying connection is missing.

Each Naya owns the job described in its job file, but all Nayas share the same system contract. If a dependency is required, coordinate through the Team Naya activity feed and the affected feature records rather than creating a competing implementation.

## Completion gate
The master mission is complete only when the nine feature areas can be exercised as one connected authenticated system and the Cloudflare runtime is proven to match the current source.

The final proof must demonstrate:
Human authentication → navigation → retrieval → intentional organization/share/action → observed consequence → Ledger/evidence → intelligence projection → daily/report synthesis → continuation.

No feature may be marked LIVE VERIFIED on documentation alone.
