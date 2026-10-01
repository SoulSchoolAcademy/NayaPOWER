# 🔱 NayaNET Hub Room Runtime Matrix — 2026-09-24

**Purpose:** authoritative current-truth/gap register for the human-facing Hub rooms and the core Feed surface.

**Observed main:** `ab450cf96fb785661217048bfbba1d8a9572e8ff`

**Source authority:** `NAYANET/HUB/`

**Evidence rule:** source inspection establishes implementation facts, not production proof. A room is only PROVEN when the repository's release/runtime/behavioral gates independently observe the required chain.

## Canonical target

The September 24 Master Objective defines these human-facing destinations:

1. Intelligence Today
2. Feed
3. Reports
4. Library
5. Smart Connect
6. Smart Mail
7. Smart Lists
8. Contacts
9. Smart Spaces
10. Smart Ledger
11. Settings

**Not rooms:** Dream, Naya Play, Smart Notes, Intelligent Blocks. Dream is a Superbrain process; Naya Play is an Intelligent Block capability; Smart Notes/Blocks are canonical intelligence objects/capabilities.

## Runtime chain

Every room is evaluated as:

`UI → authenticated identity → governed runtime → canonical data → privacy → action → persistence → verification → receipt/evidence`

A missing link remains **NOT VERIFIED**.

---

## Room Runtime Matrix

| Target | Exact UI/source | Runtime / entry | Canonical data | Identity boundary | Privacy / authority | Persistence / evidence | Current truth | First deterministic RED | Next bounded action |
|---|---|---|---|---|---|---|---|---|---|
| **01 Intelligence Today** | `src/app/IntelligenceTodaySurface.tsx`; routes `/`, `/today` | `loadPrimaryIntelligence()`; `IntelligenceTodaySurface` | PIS adapter over canonical intelligence; `nayanet_intelligence_index` when persistent PIS is available | `IdentityProvider`; PIS persistent path is owner-scoped | Private intelligence must remain owner-scoped; read surface has no execution authority | Canonical event identity + machine evidence/trust; room read has no separate receipt | **IMPLEMENTED; NOT PROVEN/FROZEN** | Prior-day comparison, daily activity, governed priority, and separate retention recommendation are not independently exposed/proven | Add a deterministic authenticated daily-intelligence retrieval contract; then prove source→runtime→Today states without deriving unsupported values from UI counts |
| **02 Feed** | `src/app/HubRouter.tsx` → `FeedView`; `src/intelligence/SmartFeedBoard`; route `/feed` | `loadPrimaryIntelligence()`, `searchPrimaryIntelligence()`, Smart Feed Board | PIS / canonical intelligence adapter; persistent index plus canonical Smart Feed source | Authenticated `useIdentity()` gate | Personal / Collective / Activity projections must preserve visibility; search cannot widen scope | Event IDs, provenance, machine evidence, trust; capture path can return event/receipt | **SUBSTANTIAL IMPLEMENTATION; NOT COMPLETE PROOF** | Feed is not a canonical sidebar room in current `AppShell`/room registry, and full authenticated reload/pagination/visibility/action proof is not closed | Reconcile Feed as a first-class Hub destination/projection in the room contract and prove authenticated retrieval, lens isolation, search, reload and source lineage |
| **03 Reports** | `src/app/ReportsSurface.tsx`; route `/reports` | `NayaAssistantRuntime.retrieve()`; period projection in React | Canonical runtime event stream; contract also references report projection `v7_intelligence_reports` | Runtime snapshot must be authenticated | Read-only synthesis; no invented trends/counts/conclusions | Source event IDs/metadata; report persistence is not created by this surface | **IMPLEMENTED; PARTIAL** | Period selector currently filters retrieved events locally; it does not yet prove distinct authoritative Daily/Weekly/Monthly/Yearly report datasets | Bind each period to an authoritative report retrieval contract with period provenance, then prove selector→dataset→reload |
| **04 Intelligent Library** | `src/app/HubRouter.tsx` → FeedView(`library=true`); route `/library`; contract `03-INTELLIGENT-LIBRARY.md` | `loadPrimaryIntelligence()`, `searchPrimaryIntelligence()` | Canonical intelligence/PIS; 58-domain model is contractual | Authenticated PIS retrieval | Private intelligence remains private; search must not fabricate matches | Event/source/provenance carried by IntelligentEvent; no room-local store | **IMPLEMENTED SURFACE; PARTIAL PROOF** | Current React Library is a FeedView/search projection, not yet the full 58-domain Library contract | Reconcile Library to the 58-domain workspace contract and prove search, domain selection, source opening, privacy and reload |
| **05 Smart Connect** | **No `SmartConnectSurface.tsx` exists** in current `src/app`; canonical contract `04-SMART-CONNECT.md` | No Hub route/component currently implements the seven-door room | Participation/connection runtime exists elsewhere; exact Hub receiver contract must be bound | Must use authenticated participation identity | Participation ≠ execution authority; connection/authentication must not imply authorization; identity private by default | Participation/contribution proofs exist at backend boundary; Hub room proof absent | **DOCUMENTED + BACKEND SEAM PROVEN; HUB ROOM NOT IMPLEMENTED** | There is no canonical Smart Connect Hub surface and no seven-door UI/runtime/evidence chain | Build the bounded Smart Connect room against the existing seven-door contract and existing governed participation runtime; do not create a new authority model |
| **06 Smart Mail** | `src/app/SmartMailSurface.tsx`; route `/mail` | `listMailThreads()`, `listConnections()`, `listMailMessages()`, `listAuthorityGrants()`, `sendSmartMail()`, `verifySmartMail()` | Governed Mail + canonical Connections + authority grants | Runtime requires authenticated session | Reading ≠ sending; drafting ≠ sending; explicit authority grant required; idempotency key on send | Execution receipt returned by send; receiver verification endpoint/action | **SUBSTANTIAL IMPLEMENTATION; PRODUCTION CAUSAL PROOF OPEN** | Complete real-human send chain remains unproven end-to-end: recipient eligibility → grant → send → persistence → receiver verification → independent receipt | Execute and independently reconstruct one authorized real participant Mail transaction, then prove denial/revocation/idempotency and reload |
| **07 Smart Lists** | `src/app/SmartListsSurface.tsx`; route `/lists` | `listSmartLists()`, `listConnections()`, `createSmartList()`, `addConnectionToList()`, `removeConnectionFromList()` | Canonical Smart Lists + canonical Connections | Authenticated runtime | List membership ≠ ownership; actions stay within connection/list authority | Runtime list state; creation/membership persistence expected | **SUBSTANTIAL IMPLEMENTATION; PROOF PARTIAL** | Contract requires intelligent lists (NOW/NEXT/WAITING/QUESTIONS/IDEAS/OPPORTUNITIES/COMPLETED) and durable membership proof; current UI is mainly Connection grouping | Reconcile Smart Lists to the full intelligent-list contract and prove create→membership→reload plus authority boundaries |
| **08 Contacts** | Current implementation is `src/app/ConnectionsSurface.tsx`; route `/connections`; room contract is `06-YOUR-CONNECTIONS.md` | `listConnections()`, `revokeConnection()` | `nayanet_connections` | Authenticated owner boundary | Connection ≠ permission; relationship claims need evidence/context | Canonical connection IDs, source type/Space provenance, active/revoked state | **IMPLEMENTED AS “Your Connections”; NAMING/DEPTH GAP** | Master Objective calls the room **Contacts**, while registry/source call it **Your Connections**; rich connection detail/context and Mail/List integration are not proven | Make the naming decision canonical (without duplicating the store), then add/prove selected-connection context, privacy, revoke persistence and cross-room continuity |
| **09 Smart Spaces** | `src/app/SmartSpacesSurface.tsx`; route `/spaces` | `listSpaces()`, `createSpace()`, `joinSpace()`, `leaveSpace()` | Canonical Spaces runtime | Authenticated member boundary | Membership ≠ connection; membership ≠ private-data access; visibility is explicit | Space IDs + membership operations; room reload proof pending | **SUBSTANTIAL IMPLEMENTATION; TWO-USER PROOF OPEN** | Contract requires a real contextual workspace; current surface proves list/create/join/leave calls but not complete two-user shared intelligence lifecycle | Prove two authenticated users through create/share/join/use/leave/revoke/privacy boundaries and verify resulting canonical records independently |
| **10 Smart Ledger** | `FeatureSurface(kind='ledger')` path plus Ledger action in `FeatureSurface.tsx`; route `/ledger` | Legacy feature path can read `nayanet_smart_ledger`; newer runtime path probes `listLedgerEntries()`, `listExecutionReceipts()`, `listActivity()`, `getLedger()`, `getActivity()` | Canonical cognition/events/receipts/ledger | Authenticated identity required by active surfaces | Protected records owner-scoped; RECEIVED/AUTHORIZED/EXECUTED/VERIFIED/PROJECTED must remain distinct | Execution receipts + cognition/event ledger; inspection action can create a canonical record | **SUBSTANTIAL INFRASTRUCTURE; HUB RECONSTRUCTION PARTIAL** | The repository contains more than one Ledger rendering path, and independent causal reconstruction from Actor→Authority→Decision→Execution→Commit→Persistence→Receipt is not closed for the human Hub | Collapse Ledger presentation onto one canonical runtime path and prove one independently reconstructed causal event, including protected retrieval and outcome distinction |
| **11 Settings** | `src/app/SettingsSurface.tsx`; route `/settings` | `runtime.verify()`, `runtime.signOut()`, `runtime.snapshot()` | Governed identity/session/runtime state | Authenticated identity provider | Human-facing governance controls; no raw DB authority | Runtime verification returns event/receipt/index/persistence state | **IMPLEMENTED; CONTROL SURFACE PARTIAL** | Current surface exposes identity, session, verification and sign-out, but not the full contract sections: Privacy, Authority, Connections, Notifications, Data, Security, Appearance, Your Intelligence | Expand only against existing governed settings contracts; prove one non-destructive persisted setting change and protected control behavior before adding breadth |

---

## Cross-cutting contradictions found during matrix construction

### C1 — Smart Share is still active in the canonical React shell

Observed in `src/app/AppShell.tsx`:

- navigation item: **Smart Share**
- route: `routes.share`
- `SmartShareSurface.tsx` exists
- `FeatureSurface` still has a Smart Share configuration

The September 24 Master Objective says **Smart Share is retired** and Smart Connect is canonical.

**Required treatment:** do not delete historical evidence. Remove/retire the active product path only after the Smart Connect replacement is wired and the old path is explicitly recorded as historical/retired.

### C2 — Naya Play is currently a sidebar navigation item

Observed in `AppShell.tsx`:

- `Naya Play` appears in the primary `items` array
- route `/play`
- `NayaPlaySurface.tsx` exists

The Master Objective says Naya Play is a **Block capability, not a room**.

**Required treatment:** preserve the capability; remove it from room navigation when the canonical Intelligent Block action path is ready. Do not delete the underlying capability.

### C3 — Dream is currently a route, although it is a Superbrain process

Observed:

- `routes.dream = '/dream'`
- `DreamSurface.tsx`
- `HubRouter.tsx` exposes `routes.dream`

The Master Objective says Dream is **not a Hub room**.

**Required treatment:** retain Dream as an internal/process capability and remove it from human room navigation unless a future product decision explicitly defines a human-facing Dream experience.

### C4 — Feed is a real Hub destination in React but absent from the room registry/sidebar

Observed:

- `routes.feed = '/feed'`
- `FeedView` exists
- top action **Explore Intelligence** reaches Feed
- `ROOM-REGISTRY.md` contains 10 rooms and no Feed
- primary `AppShell` room list contains no Feed item

This is a **contract reconciliation hole**, not permission to create a second Feed.

### C5 — Contacts vs Your Connections is a naming/specification mismatch

Observed:

- Master Objective: **Contacts**
- Room registry/contract: **Your Connections**
- React implementation: **Your Connections**
- canonical durable primitive: `nayanet_connections`

The data model should not be duplicated to satisfy naming.

### C6 — Direct Supabase access remains inside a Hub surface

Observed in `src/app/FeatureSurface.tsx`:

`supabase.from(c.table).select('*')...`

The Hub architecture contract states that the human-facing Hub should use:

`User → GitHub/NayaPOWER control substrate → NayaNET runtime → managed persistence → Hub`

and must not receive raw database authority.

**This is a higher-severity architecture RED than visual incompleteness.** The next reconciliation should remove direct browser-to-Supabase access from the canonical human-facing path and route the affected surfaces through the governed runtime adapter.

### C7 — Multiple generations of Hub surface rendering coexist

Observed in `NAYANET/HUB/index.html`:

- legacy/static navigation and functional scripts
- `intelligence-surfaces-runtime.js`
- React/Vite application source under `src/`

The Worker declares the Vite-built React entry as canonical, but the source file still contains legacy/static surface machinery.

**Required treatment:** prove exactly which DOM/render path reaches production, then remove only redundant active render paths. Preserve historical source where required for provenance.

---

## Highest-value deterministic RED

**RED-1: canonical Hub boundary violation — direct Supabase access in `FeatureSurface.tsx`.**

Why this comes before adding room breadth:

1. It violates the declared Hub activation boundary.
2. It can cause multiple rooms to bypass the governed runtime.
3. It weakens the very authority/privacy model the rooms are supposed to demonstrate.
4. Fixing it creates a reusable room adapter boundary rather than another one-off implementation.
5. It is more foundational than cosmetic room completion.

**RED-2: Smart Connect has no canonical Hub room implementation.**

Once the boundary is repaired, Smart Connect is the highest-value missing product surface because it is the house's canonical door system and already has a backend participation seam.

**RED-3: Feed/room registry reconciliation.**

Feed is materially implemented as a core surface but is not represented consistently in the current room contract/navigation model.

---

## Immediate execution order

1. **Repair the browser data boundary:** identify every Hub component that imports/uses Supabase directly; route only the affected human-facing retrievals through the governed runtime adapter.
2. **Implement Smart Connect as one canonical room** using the existing seven-door contract and existing participation/authority seams.
3. **Reconcile navigation:** Smart Connect replaces active Smart Share; Dream/Naya Play cease being rooms; Feed becomes an explicitly defined canonical core destination; Contacts/Your Connections receives one canonical product name.
4. **Close Feed proof:** authenticated retrieval → lens isolation → search → action → persistence/reload → independent evidence.
5. **Close Today proof:** deterministic daily retrieval boundary → comparison → learning → priority → memory → activity.
6. **Close Reports proof:** period-specific authoritative datasets → source lineage → reload.
7. **Close Contacts/Lists/Spaces two-user proof.**
8. **Close Smart Mail causal send/verify proof.**
9. **Unify Smart Ledger rendering and independently reconstruct a causal event.**
10. **Expand Settings only from governed controls and prove state persistence.**

## Definition of done for the house

The Hub is complete only when every canonical destination has:

**UI → authenticated identity → governed runtime → real canonical data → correct privacy → real action → persistence → verification → evidence/receipt**

and the whole house supports:

**SEE → UNDERSTAND → LEARN → PRIORITIZE → REMEMBER → QUESTION → INTERPRET → ACT**

without a second brain, second persistence authority, fabricated intelligence, or authority leakage.

**Status of this matrix:** repository-grounded working control record. It does not itself promote any room to PROVEN.
