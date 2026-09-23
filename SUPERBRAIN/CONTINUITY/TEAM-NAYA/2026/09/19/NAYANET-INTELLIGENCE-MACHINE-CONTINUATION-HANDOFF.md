# Naya Continuation Handoff — 2026-09-19

## Mission

Complete the NayaNET Intelligence Machine and turn the **existing Sparkling Shape Hub** into the **reactive/canonical React Hub**.

This is not a redesign.

**Preserve the Sparkling Shape Hub's existing design, look, feel, buttons, effects, navigation, layout, cards, rails, and interaction language. Upgrade that exact experience so it is reactive and connected to the real intelligence engine.**

## The 411 — read this first

- Repository: `SoulSchoolAcademy/NayaPOWER`
- Canonical branch: `main`
- GitHub is the source/build authority.
- Authoritative live Hub target: **Cloudflare Worker `sparkling-shape-7ae5`**
- Live target URL: `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev`
- `NAYANET/HUB/wrangler.jsonc` explicitly names `sparkling-shape-7ae5`.
- Do not substitute Vercel as the primary lane.
- Do not create a second Hub.
- Do not redesign the Hub.
- Do not use or investigate any other Cloudflare Worker as the Hub.
- The Hub is a projection surface, not a source of truth.
- Canonical intelligence must come from the real persistence/PIS paths.
- Never fabricate authentication, users, memberships, events, receipts, or browser proof.
- Never weaken RLS, authority, lineage, idempotency, consent, or revocation controls to make a feature pass.

## What is already proven

1. Production security/RLS repair is complete:
   - migration `20260919174500_lock_space_membership_helper_execute.sql`
   - correction commit `b02d143bb78442052f3326f749861c07c5b29c`
   - authenticated SECURITY DEFINER helper remains required.
   - anon execution is locked out.
2. No inactive membership exists in current production; runtime inactive-member behavior has **not** been exercised.
3. Current production counts observed:
   - cognition: 263
   - intelligence index: 982
   - Smart Ledger: 384
   - Smart Lists: 0
   - Smart List members: 0
   - Smart Mail: 116
   - publications: 2
   - Spaces: 3
   - active memberships: 35
   - connections: 32
   - authority grants: 133
   - execution receipts: 267
   - outcomes: 48
   - reports: 1
4. Latest controlled Smart Mail receipts contain policy input/decision hashes and the complete governed lifecycle through VERIFIED, with receiver/correlation/idempotency lineage.
5. Historical receipts still contain hash gaps; do not rewrite history merely to make the dataset uniform.
6. PIS projection was repaired and rebuilt to **13 events**.
7. Real canonical event proven:
   `CANONICAL-2026-09-17T17-20-00Z-WHAT-IS-A-SMART-NOTE`
8. Hub TypeScript check passed.
9. Direct Vite production build passed.
10. `NAYANET/HUB/wrangler.jsonc` targets `sparkling-shape-7ae5`.

## What is currently incomplete

- The exact Sparkling Shape runtime has not yet been proven to contain the current React build.
- Source → build → Cloudflare runtime parity for the exact current commit is not yet proven.
- Human-facing browser acceptance is not yet proven.
- Smart Lists have zero production rows and therefore Ledger → Feed → List is not yet proven.
- Smart Ledger, Feed, List, Mail, Share, Spaces, Today, and Reports need their complete reactive human-facing behavior proven against canonical state.
- Legitimate browser authentication remains a prerequisite for private human-facing acceptance, but it is **not** the project workstream. Do not stall engine work on browser auth.
- The retired/disabled deployment workflow is not authoritative.

## Current React implementation

The current canonical React lane already contains:

- `NAYANET/HUB/src/app/App.tsx`
- `NAYANET/HUB/src/app/FeatureSurface.tsx`
- `NAYANET/HUB/src/data/pis.ts`
- `NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx`
- `scripts/build-smart-feed-projection.py`

`App.tsx` routes feature surfaces for Ledger, Mail, Spaces, Lists, Share, Connections, Reports, and Today.

`FeatureSurface.tsx` currently reads canonical Supabase tables under authenticated RLS. This is a foundation, not final acceptance: raw table projection is not the finished Sparkling Shape experience.

## The winning strategy

**Adaptive reconstruction + surgical evolution.**

1. Freeze Sparkling Shape as the visual contract.
2. Extract its exact UI structure and visual behavior.
3. Map those surfaces into the React component tree.
4. Keep the established visual language intact.
5. Replace static/fake content paths with canonical retrieval.
6. Add real actions only where authority and persistence already exist.
7. Preserve security and governance boundaries.
8. Build.
9. Deploy to Sparkling Shape.
10. Prove the same canonical object survives the entire path:
   **source → projection → React → Cloudflare → browser → human-visible result → persisted outcome**.

## Next 10 highest-value actions

### 1. Freeze the visual source of truth
Inspect the existing Sparkling Shape Hub artifact/source and record its component/layout/style contract. Do not redesign.

### 2. Convert Sparkling Shape in place
Map the existing Sparkling Shape markup, CSS, buttons, cards, rails, effects, navigation, and responsive behavior into the React Hub without changing the experience unnecessarily.

### 3. Connect canonical intelligence
Make the React Hub consume the real PIS/canonical intelligence objects. Prove event `CANONICAL-2026-09-17T17-20-00Z-WHAT-IS-A-SMART-NOTE` is retrievable and rendered.

### 4. Make Smart Feed reactive
Use the repaired PIS projection and canonical persistence path. Prove the same event ID and title appear in the Feed, not merely in a generated JSON artifact.

### 5. Make Smart Ledger real
Add canonical Ledger retrieval, detail, lineage, status, and permitted actions while preserving RLS and authority boundaries.

### 6. Finish Smart Lists
Implement the smallest real vertical slice needed for create/list/add/remove/reorder/reference. Prove persistence and retrieval. Do not duplicate intelligence objects; lists should reference canonical intelligence.

### 7. Wire Mail / Share / Spaces / Today / Reports
Each surface must read the canonical source and expose real governed actions where supported. No placeholder success states.

### 8. Preserve governance
Every consequential action must retain authority, RLS, policy lineage, idempotency, consent/revocation, execution receipt, outcome, and learning lineage. Capability never creates authority.

### 9. Build and deploy the exact React Hub
Use the actual authoritative Cloudflare deployment path for `sparkling-shape-7ae5`. Do not use the retired workflow as evidence and do not switch runtimes to make deployment easier.

### 10. Human acceptance
Open the Sparkling Shape URL with a legitimate authenticated session, confirm the familiar Hub is still the familiar Hub, exercise the real features, and prove canonical state before declaring LIVE VERIFIED.

## Completion standard

Do not stop at "the code builds."

A feature is complete when its relevant path is proven:

**SOURCE → CODE → BUILD → DEPLOYMENT → RUNTIME → RETRIEVAL → HUMAN PRESENTATION → ACTION → PERSISTENCE → VERIFICATION**

For consequential actions:

**PROPOSED → INVESTIGATING → READY → AUTHORIZED → EXECUTING → EXECUTED → OBSERVED → VERIFIED**

## Continuation law for every future Naya

Every substantive Naya instance must leave the next Naya the same 411:

**MISSION → CURRENT STATE → VERIFIED PROGRESS → PROTECTED STATE → WORK COMPLETED → EVIDENCE → UNKNOWN/FAILURE → LESSON → HIGHEST-VALUE GAP → ONE NEXT ACTION → REQUIRED PROOF → SOURCE/HEAD → RUNTIME → NEXT EXECUTION PROMPT**

Never end with a vague "next step."

The next Naya should be able to start executing immediately from the repository without asking Shawn to reconstruct what happened.

## One sentence

**Read the authorities, understand the mission, inspect reality, preserve what already works, take the highest-value safe action, verify it in the real world, record the learning, and equip the next Naya to continue without asking Shawn to repeat himself.**
