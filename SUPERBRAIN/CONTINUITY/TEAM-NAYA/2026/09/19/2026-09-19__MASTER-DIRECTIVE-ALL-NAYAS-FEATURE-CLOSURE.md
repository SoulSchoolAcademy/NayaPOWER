# 🔱 MASTER DIRECTIVE — ALL NAYAS — 2026-09-19

## PURPOSE

This is the operating instruction set for every Naya working on the NayaNET Engineering System today.

This is not a status post and not a request for a vague review.

Every Naya receiving this directive must:

1. read the current Engineering System architecture and the feature contract;
2. read the current day's activity index;
3. read the feature's current activity record;
4. inspect the actual repository/runtime evidence before deciding what is true;
5. perform the smallest correct engineering action that closes a real gap;
6. test the complete affected path, not merely the file or function changed;
7. record exactly what changed and what was actually observed;
8. update the affected feature's checklist/current state/TODO;
9. append an immutable session record to today's activity history;
10. leave exactly ONE concrete successor action before signing out.

**No Naya may mark something VERIFIED because a document exists.**
**No Naya may replace history with a rewritten status.**
**No Naya may create a second truth store to make a feature appear complete.**

---

# 1. THE SYSTEM WE ARE BUILDING

NayaNET is one living intelligence system exposed through multiple human-facing projections.

The governing architecture is:

**one identity → one canonical event/intelligence substrate → one PIS → one CIS/learning system → one authority system → one evidence model → multiple projections**

The Hub is a projection/interface layer.

Smart Notes produce intelligence/events.

Cognition/PIS carries operational intelligence.

Learning changes the system only through governed, evidenced paths.

Smart Ledger is evidence/integrity, not a competing event database.

Intelligence Index supports retrieval/projection.

Activity is a human-readable projection of canonical work/events.

Reports synthesize existing intelligence with provenance.

Smart Mail executes governed communication.

Smart Spaces organize authorized intelligence.

Smart Tabs provide navigation/retrieval intent.

Smart List preserves intentional collections.

Smart Share exposes authorized sharing/publication.

**Do not build isolated feature engines when an existing canonical primitive already exists. REUSE → EXTEND → CONNECT → VERIFY.**

---

# 2. THE MOST IMPORTANT CORRECTION: ACTIVITY IS A STREAM, NOT A SINGLE POST

The existing dated feature files are **daily rollups/snapshots**.

They are NOT supposed to be overwritten every time a Naya works.

The durable activity model is:

**YEAR → MONTH → DAY → FEATURE → SESSION**

For example:

```
NayaNETEngineeringSystem/
  ACTIVITY/
    2026/
      09/
        19/
          INDEX.md
          SMART-TABS.md
          SMART-FEED.md
          SMART-LEDGER.md
          ...
          SMART-TABS/
            INDEX.md
            SESSION-001.md
            SESSION-002.md
            SESSION-003.md
```

The exact filenames may use timestamps rather than SESSION-001 numbering.

### Immutable history law

A completed session record is appended.

It is never deleted merely because the work continues.

It is never replaced by the next update.

It is never rewritten to make an old result look newer.

The feature daily file is the **rollup/current state**.

The timestamped session files are the **continuous history**.

Therefore if Smart Tabs has 20 Naya sessions on September 19, there must be 20 recoverable session records, plus the Smart Tabs daily rollup.

The same applies to Smart Feed, Smart Mail, Ledger, Spaces, Reports, and every other feature.

---

# 3. WHAT A NAYA MUST READ BEFORE WORK

Before touching code, the Naya must inspect, in this order:

### A. System authority

- `NayaNETEngineeringSystem/README.md`
- `00-SYSTEM-ARCHITECTURE.md`
- `01-ENGINE-AND-DATA-FLOW.md`
- `02-IDENTITY-AUTHORIZATION-PRIVACY.md`
- `03-INTELLIGENCE-EVENT-DATA-CONTRACTS.md`
- `04-VERIFICATION-GOVERNANCE-AND-DELIVERY.md`
- `06-FEATURE-COMPLETION-AND-ACTIVITY.md`

### B. Feature authority

Read the feature's `.naya` source/authority file if one exists.

Then read the feature specification under:

`NayaNETEngineeringSystem/features/`

### C. Current activity

Read:

`NayaNETEngineeringSystem/ACTIVITY/2026/09/19/INDEX.md`

Then read that feature's current daily activity record.

Then read the most recent session record for that feature.

### D. Actual implementation

Inspect the real GitHub source.

Then inspect the relevant live Supabase objects/runtime/deployed surface where accessible.

The order is:

**SOURCE CONTRACT → GITHUB IMPLEMENTATION → SUPABASE OBJECTS → EDGE FUNCTIONS → DATABASE FUNCTIONS → LIVE DATA → DEPLOYED FRONTEND → AUTHENTICATED TEST → OBSERVED EVIDENCE → VERIFIED**

Anything not observed remains **NOT-PROVEN**.

---

# 4. SESSION PROTOCOL — EVERY NAYA, EVERY TIME

## SIGN IN

Record:

- Naya/actor
- date
- exact timestamp
- feature
- mission
- starting state
- current blocker
- source records inspected

## WORK

Do the engineering.

Do not silently make unrelated changes.

Do not duplicate existing primitives.

Do not change canonical architecture merely to make a test easier.

Do not use fabricated identities, fabricated credentials, service-role impersonation as a browser user, fake evidence, or synthetic PASS results.

## VERIFY

Test the complete path affected by the change.

A unit/file-level success is not production verification.

For runtime features, prove:

**source → build → deployed runtime → authenticated behavior → observed result**

For security/privacy, prove actual owner behavior with legitimate identities.

For persistence, prove write → reload/fresh retrieval.

For idempotency, prove replay.

For authorization, prove allowed and denied paths.

For navigation, prove destination and retrieval semantics.

## REPORT

Record:

- what was already true;
- what was missing;
- what was changed;
- exact files/runtime objects changed;
- tests executed;
- observed results;
- evidence links/IDs;
- current state;
- remaining gaps;
- risks/questions;
- exactly one successor action.

## SIGN OUT

Update:

1. feature checklist;
2. feature current state;
3. feature TODOs;
4. feature daily rollup;
5. immutable timestamped session record;
6. Engineering Activity day index if status changed;
7. Team Naya feed/day index if the work is substantive.

Then leave **ONE** next action.

---

# 5. FEATURE-BY-FEATURE MASTER WORK ORDERS

## 5.1 SMART TABS

### Mission

Turn Smart Tabs from a defined contract into a real authenticated Hub navigation/retrieval surface.

### Must prove

**Smart Tab → target → existing retrieval/navigation primitive → authority/visibility filter → destination/result**

### Required work

1. Find the real deployed Hub source and insertion point.
2. Identify existing routing/navigation primitives.
3. Identify existing search/retrieval/topic/category/project primitives.
4. Identify whether a canonical Smart Tab persistence store already exists.
5. If it exists, reuse it.
6. If it does not exist, design the smallest owner-scoped persistence layer.
7. Implement authenticated CRUD.
8. Persist across reload/session.
9. Implement reorder/favorite/edit/remove.
10. Prove owner isolation.
11. Ensure deleting a tab does not delete the underlying intelligence.
12. Connect tab selection to the existing retrieval path.
13. Prove source/build/deployed parity.
14. Add Activity navigation only as a projection; never create a second intelligence/event store.

### Required acceptance path

**create → persist → reload → select → retrieve → permission filter → present → edit → reorder → favorite → remove → verify intelligence remains**

### Do not

- create a separate intelligence index;
- make the tab label itself the query;
- bypass permissions;
- hard-code demo data;
- declare completion from static UI alone.

---

## 5.2 SMART FEED

### Mission

Make the Feed a real projection of canonical activity/intelligence.

### Required work

1. Find the actual Hub Feed surface.
2. Map its current data source.
3. Map canonical Activity/intelligence events.
4. Define the exact projection query.
5. Apply identity, visibility, privacy, and authorization before presentation.
6. Support chronological pagination.
7. Preserve event/source identity.
8. Allow drill-down to the underlying evidence.
9. Ensure actions originate from authorized source objects.
10. Prove fresh retrieval after a new event.
11. Prove no duplicate event store exists.
12. Prove deployed runtime matches source.

### Acceptance

**canonical event → Feed projection → permission filter → human presentation → source drill-down → action → new canonical event**

---

## 5.3 SMART LEDGER

### Mission

Close the gap between the already-live Ledger infrastructure and the human-facing product.

### Known evidence

The live system already contains Smart Ledger infrastructure and production closure evidence.

The Ledger is an **evidence/integrity projection**, not the canonical event database.

### Required work

1. Map the live `nayanet_smart_ledger` data to the current Hub.
2. Map source event → ledger event lineage.
3. Map execution receipt → ledger.
4. Map cognition/learning/report/space consequences.
5. Verify owner-scoped retrieval.
6. Prove fresh authenticated retrieval.
7. Prove replay/idempotency behavior.
8. Show evidence/value/outcome provenance.
9. Reconcile repository documentation with live runtime.
10. Do not introduce another ledger/event store.

### Acceptance

A human can retrieve a Ledger entry and trace it backward to its source and forward to its verified consequence.

---

## 5.4 SMART LIST

### Mission

Determine and close the real implementation path for intentional saved collections.

### Required work

1. Search the repository/runtime for existing list/save/favorite/collection primitives.
2. Identify canonical ownership and membership.
3. Reuse existing storage if present.
4. Define the smallest missing persistence if absent.
5. Implement authenticated create/edit/delete.
6. Implement add/remove/reorder as applicable.
7. Prove owner isolation.
8. Prove share does not leak unauthorized intelligence.
9. Prove deleting a list does not delete its underlying intelligence.
10. Prove source/build/runtime parity.

### Acceptance

**discover → save → persist → reload → retrieve → modify → permission check → share only when authorized**

---

## 5.5 SMART MAIL

### Mission

Close the gap between the already-proven governed backend and the complete human-facing product.

### Known evidence

The live Smart Mail Edge Function is authenticated and governed.

Production closure has already proven a real authenticated Smart Mail action and receiver verification.

### Required work

1. Map the current Hub Mail surface to the live backend.
2. Preserve authority-at-use.
3. Preserve recipient membership checks.
4. Preserve receiver verification.
5. Map execution receipt and cognition lineage.
6. Test idempotency/replay.
7. Test owner isolation with legitimate users.
8. Test unauthorized recipient access.
9. Test attachment/media authorization if supported.
10. Prove deployed UI → backend → receipt → receiver verification.
11. Update documentation to match live v12 behavior.

### Acceptance

**compose → authorize → send → persist → receive → receiver-verify → receipt → cognition/ledger lineage → retrieve**

---

## 5.6 SMART SHARE

### Mission

Make authorized sharing/publication a real, observable product path.

### Required work

1. Find existing sharing/publication primitives.
2. Identify authority source.
3. Identify visibility and privacy classes.
4. Map recipient authorization.
5. Implement/reuse authorized share.
6. Prove recipient can see only authorized material.
7. Prove non-recipient cannot retrieve it.
8. Prove revocation removes access where contract requires.
9. Prove no public leakage.
10. Record canonical share event and downstream projections.
11. Prove source/build/runtime parity.

### Acceptance

**select → authorize → share → recipient retrieve → nonrecipient denied → revoke → verify**

---

## 5.7 SMART SPACES

### Mission

Turn the live Space primitives into a complete governed product.

### Known evidence

Live `nayanet_spaces` and `nayanet_space_intelligence` primitives exist, including Space → Ledger integration.

### Required work

1. Map current Hub Space UI.
2. Map creation/edit/delete lifecycle.
3. Map membership.
4. Map visibility.
5. Map intelligence attachment.
6. Map canonical Activity events.
7. Map Ledger consequences.
8. Prove owner/member authorization.
9. Prove cross-user denial.
10. Prove deletion/removal semantics.
11. Prove fresh retrieval.
12. Prove deployed parity.

### Acceptance

**create → authorize members → attach intelligence → retrieve → activity/ledger projection → mutate → revoke/remove → verify**

---

## 5.8 YOUR INTELLIGENCE TODAY

### Mission

Turn existing daily intelligence primitives into the actual human-facing synthesis surface.

### Required work

1. Find the deployed Today surface.
2. Identify the canonical daily query.
3. Determine how current intelligence is selected.
4. Synthesize without inventing facts.
5. Preserve source traceability.
6. Apply private/owner visibility.
7. Handle an empty day.
8. Handle carry-forward intelligence explicitly.
9. Handle refresh/recompute.
10. Show what is new, what changed, what matters, and where it came from.
11. Prove fresh retrieval.
12. Record synthesis provenance.

### Acceptance

A human can open Today and trace every substantive claim to underlying intelligence/evidence.

---

## 5.9 INTELLIGENT REPORTS

### Mission

Turn report infrastructure/hooks into a complete provenance-preserving report product.

### Required work

1. Find existing report generation/runtime.
2. Reuse existing report infrastructure.
3. Map report source events.
4. Preserve provenance.
5. Implement period selection.
6. Implement generation/retrieval.
7. Implement regeneration deterministically where required.
8. Apply privacy/ownership.
9. Map Report → Ledger.
10. Prove fresh retrieval.
11. Prove no invented source material.
12. Prove source/build/runtime parity.

### Acceptance

**select period → generate → trace sources → persist/retrieve → ledger/evidence → regenerate/retrieve → verify**

---

# 6. THE ACTIVITY SYSTEM ITSELF MUST BE ENGINEERED

The activity system is now a product requirement, not documentation decoration.

### Canonical model

**canonical events are truth**

Activity is a projection.

The Engineering Activity tree is a human-readable engineering projection.

Team Naya is a human-readable Naya-to-Naya communication projection.

The Hub Activity surface is the human-facing product projection.

All three must point back to the same underlying truth.

### Therefore

Do NOT create:

- a second activity database;
- a separate fake event stream;
- duplicate intelligence records;
- manually maintained “truth” that contradicts canonical events.

### Continuous updates

If Smart Tabs has:

- Naya A at 09:00 — mapped Hub source;
- Naya B at 10:15 — found retrieval primitive;
- Naya C at 11:30 — implemented persistence;
- Naya D at 13:00 — discovered RLS defect;
- Naya E at 14:20 — repaired RLS;
- Naya F at 15:00 — authenticated test passed;

then all six sessions remain visible.

The Smart Tabs daily rollup should summarize the current state and link to all six sessions.

It must NOT become six overwritten versions of one file.

---

# 7. FEATURE STATUS LAW

Use only these meanings:

**DEFINED** — contract exists; implementation not established.

**IMPLEMENTED** — implementation evidence exists; complete runtime proof may remain.

**TESTED** — explicit tests ran and passed, but full production proof may remain.

**LIVE VERIFIED** — deployed authenticated behavior observed end-to-end.

**INDEPENDENTLY VERIFIED** — verification performed through an independent evidence path appropriate to the risk.

**FOUNDATION** — meaningful primitives exist but the product lifecycle is incomplete.

**NOT-PROVEN** — required evidence has not been observed.

**BLOCKED** — work cannot legitimately continue without an external dependency.

Never upgrade status merely because code was written.

---

# 8. WHAT COUNTS AS EVIDENCE

Strong evidence includes:

- exact commit;
- exact file/path;
- exact runtime object;
- exact Edge Function/version;
- exact database function;
- exact table/query result;
- exact authenticated test identity;
- exact object IDs;
- exact execution receipt;
- exact observed UI behavior;
- exact deployment/version;
- exact before/after result.

Weak evidence:

- “the code looks right”;
- “the page exists”;
- “the function deployed”;
- “the test should work”;
- “I understand the architecture”;
- screenshots without causal verification;
- fabricated or synthetic credentials.

---

# 9. FAILURE LAW

When a test fails:

1. preserve the failure;
2. record exact observed error;
3. identify the smallest boundary where it failed;
4. compare against a known-good control;
5. change only the smallest justified boundary;
6. rerun with new information;
7. update the activity record;
8. do not erase the failed session;
9. do not call a failure a pass because another path works.

**No retry without new information.**

---

# 10. HANDOFF LAW

Every Naya must finish with exactly one continuation action.

Not:

- “continue improving”;
- “keep testing”;
- “look into it.”

Instead:

**WHO → WHAT → WHERE → ACCEPTANCE CONDITION**

Example:

> Next Naya: inspect the deployed Hub Activity route, identify the canonical Activity retrieval query, implement YEAR → MONTH → DAY navigation without creating a second event store, then prove 2026-09-19 Smart Tabs session retrieval and one previous-day session retrieval through the authenticated runtime.

That is actionable.

---

# 11. TODAY'S ORDER OF OPERATIONS

Do not have nine Nayas randomly build nine disconnected things.

Coordinate the work.

### Phase 1 — Activity substrate

First prove the continuous activity model itself:

**YEAR → MONTH → DAY → FEATURE → SESSION**

with append-only session history and daily rollups.

### Phase 2 — Hub Activity

Then wire the actual deployed Intelligent Hub to that activity projection.

Prove:

**2026 → September → 19 → Smart Tabs → session**

then navigate to a previous day and retrieve its real records.

### Phase 3 — Smart Tabs

Use the now-proven navigation/activity surface to close Smart Tabs runtime mapping.

### Phase 4 — Retrieval/projection spine

Close Smart Feed and Intelligence Today against canonical retrieval.

### Phase 5 — Evidence/action surfaces

Close Smart Ledger, Smart Mail, Smart Share, and Smart Spaces against their live governed primitives.

### Phase 6 — Collections and synthesis

Close Smart List and Intelligent Reports.

### Phase 7 — Cross-feature verification

Run authenticated owner-isolation, replay/idempotency, permission, source-build-runtime parity, and fresh-retrieval proofs across the completed surfaces.

---

# 12. THE NON-NEGOTIABLE ARCHITECTURAL RULE

**The Hub is not the brain.**

The Hub presents the brain.

**The activity feed is not the event database.**

It presents the work.

**The Smart Ledger is not the intelligence database.**

It proves evidence/integrity.

**A feature document is not proof.**

Runtime evidence is proof.

**A Naya's claim is not evidence.**

An observed result is evidence.

**A new database table is not automatically progress.**

If an existing canonical primitive can do the job, connect to it.

---

# 13. FINAL INSTRUCTION TO EVERY NAYA

You are not being asked merely to “work on a feature.”

You are being asked to leave the system in a more truthful, more connected, more observable, more recoverable state than you found it.

When you finish:

**the code must tell the truth,**
**the runtime must tell the truth,**
**the activity history must tell the truth,**
**the status must tell the truth,**
**and the next Naya must be able to continue without asking Shawn to reconstruct your work.**

**SIGN IN → UNDERSTAND → WORK → TEST → VERIFY → RECORD → UPDATE → HAND OFF.**

**One system. One truth. Continuous history. No silent work. No invented proof.**
