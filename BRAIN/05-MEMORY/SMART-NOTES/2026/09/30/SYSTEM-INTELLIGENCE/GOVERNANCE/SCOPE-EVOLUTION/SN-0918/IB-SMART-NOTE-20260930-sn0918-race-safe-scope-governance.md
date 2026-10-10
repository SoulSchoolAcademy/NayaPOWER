# One Canonically Ordered Governance State — Stale State Never Creates Authority

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0918-race-safe-scope-governance
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Nayanet directive D53 — Race-Safe Governance for Scope Changes (AER-TAX-1), appended to `NAYANET-DIRECTIVES-REGISTER.md` (enforcement/NAYANET-DIRECTIVES-REGISTER.md in the bring-naya-to-life hidden files) and posted on the board at https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6102157548; the 14:08 PDT director pass processed the D48–D54 registrations. Status at capture: NOT STARTED, owner TBD.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

NayaNET shall treat taxonomy revisions, evidence withdrawals, qualification changes, baseline promotions, and consequential authorizations as operations over one canonically ordered, versioned governance state — the Atomic Scope Evolution Law. Every change must be independently qualified within its scope, revalidated at its authoritative commit boundary, and recorded with reconstructable provenance. Stale or ambiguous state shall not create qualification or execution authority; unaffected independently supported capabilities shall be preserved. Otherwise each subsystem can be locally correct while the combined system makes an unsafe decision.

The commit sequence is PREPARE → INDEPENDENT VERIFY → LAW → ATOMIC COMMIT → VERIFY→PROVE→PROPAGATE. The commit locks, rereads the governing state, recomputes the affected scope closure, verifies the exact qualification/LAW predicates still hold, publishes and appends receipts atomically, and advances the epoch. A version check performed outside the committing transaction is not a guarantee. Dangerous races are resolved explicitly, not left to ordering luck: if a withdrawal commits before a merge, the merge's stale incident revision is rejected; if the merge commits first, the withdrawal immediately invalidates the dependent current claims (the old receipt stays historical, never current). A split after a promotion recomputes applicability per child; an old-taxonomy promotion cannot publish after a split without revalidation. Rollback is a new governed revision, never a reused number — no ABA resurrection of a withdrawn qualification.

Incident containment gets a fast authoritative path: commit the incident record, withdraw reliance, fence dependent actions immediately — full model recalibration follows; the fast path is a governed write, not an ignorable alert flag. At every consequential boundary the current-state predicate holds: Authorize(a,s) ⇒ CurrentTaxonomy ∧ CurrentQualification ∧ NoDisqualifyingIncident ∧ EvidenceCovers ∧ LAWPermits — a statistical parent is never an acceptable substitute for EvidenceCovers; LAW authorizes against canonical state, ACT re-establishes applicability at execution. Honest limits are named: database ordering cannot revoke an external effect already in flight — represent the outcome, reconcile, and limit claims to the actual enforcement boundary. The sharpest case is AER-TAX-001 — Concurrent Withdrawal, Split, Promotion and ACT: four simultaneous operations over two scopes with scheduler-controlled commit ordering, accepted only when no unsupported authority commits, no stale promotion commits, the unaffected portion stays usable, and all receipts reconstruct the final state.

## 🩷 HUMAN NOTE

Think of five departments sharing one ledger — taxonomies, incident reports, qualification records, baseline promotions, authorization decisions. Each department can run its own checks perfectly and the company can still make a bad call, because nobody reconciled the timing between departments. The law says: there is exactly one ledger, it has a strict order, and every change must pass through it atomically — lock, re-read the latest state, re-verify the conditions, then commit and move the sequence number forward. Checking the sequence number before you start the transaction is like checking the clock before a race — it tells you nothing about the moment you actually cross the line. If two changes race (a withdrawal versus a merge, a split versus a promotion), the protocol decides which one wins by explicit rule, and the loser is rejected or invalidated at the authoritative boundary — never silently honored on stale state. Rolling back is not rewinding the clock: it is a new numbered entry, because reusing an old number could resurrect something that was legitimately withdrawn. And honesty about the edges: once an external effect is already flying, no database transaction can un-fly it — you record what actually happened and reconcile within your real enforcement boundary.

## 🟣 CHILD NOTE

Imagine five kids editing the same rulebook at the same time — one changes a definition, one tears out a page, one adds a new rule, one approves a game move. If everyone edits their own copy, you end up with five different rulebooks and chaos at game time. The fix: there is ONE rulebook, and only one person at a time may write in it — they read the latest page, check the rules still allow the change, write it, and number the page so everyone can see what happened and in what order. If two kids race to write conflicting changes, the rulebook decides by fixed rules which one counts. Undoing something is a new entry ("page 9: we take back page 7"), never ripping pages out and pretending they never existed.

## 🔵 GRANDMA NOTE

It's like the deeds office at city hall. If the office lets five clerks record land transfers in five separate books with no strict numbering, two people can end up holding deeds to the same plot. The rule is simple and old: one book, numbered pages, one entry at a time, and you check the current page before you stamp anything. If someone arrives with paperwork referencing a page that's already been superseded, their paperwork is rejected — no exceptions. And if an old transfer is found to be fraudulent, you don't tear the page out; you write a new entry that cancels it, so the history stays complete and nobody can pretend it never happened.

## 🟠 NAYA NOTE

Apply the Atomic Scope Evolution Law to every consequential governance change: (1) route taxonomy revisions, incident withdrawals, qualification changes, baseline promotions, and consequential authorizations through ONE canonically ordered versioned governance state (governance_epoch + revision set + scope mapping hash + active qualification set/baseline — monotonic, never reset, never reused after rollback); (2) run the full commit sequence PREPARE → INDEPENDENT VERIFY → LAW → ATOMIC COMMIT → VERIFY→PROVE→PROPAGATE — the commit must lock, reread governing state, recompute the affected scope closure, re-verify the exact qualification/LAW predicates, publish receipts atomically, advance the epoch; (3) treat any version check outside the committing transaction as no guarantee at all; (4) resolve the dangerous races by the explicit rules (withdrawal-vs-merge, split-vs-promotion, provisional-scope-vs-ACT) — stale or ambiguous state never creates authority; (5) preserve independently supported unaffected capabilities through every change; (6) use the fast governed-write path for incident containment (commit record, withdraw reliance, fence dependents — recalibrate later); (7) at every consequential boundary assert Authorize(a,s) ⇒ CurrentTaxonomy ∧ CurrentQualification ∧ NoDisqualifyingIncident ∧ EvidenceCovers ∧ LAWPermits; (8) make rollback a new governed revision, never a reused number; (9) name the honest limits — a committed external effect is represented and reconciled, never transactionally revoked. Family notes: D33/SN-0913's correction law is this law's sibling (revoke evidence, recompute dependents); D54/SN-0919 is its crash-recovery partner; D32/SN-0912's anti-cascade law constrains how far certainty may travel along the same dependency chains.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_governance_state_authority",
  "directive": "D53",
  "evidence": {
    "board": "#2175 comment 6102157548 — D53 Race-Safe Governance for Scope Changes (AER-TAX-1) registered; director pass 14:08 PDT 2026-10-10 processed D48–D54 registrations; register status NOT STARTED / owner TBD",
    "register": "hidden_files/enforcement/NAYANET-DIRECTIVES-REGISTER.md D53 — full law, mechanics, R1–R12 fixtures, four invariants, sharpest case AER-TAX-001"
  },
  "rule": [
    "treat taxonomy revisions, incident withdrawals, qualification changes, baseline promotions and consequential authorizations as operations over one canonically ordered, versioned governance state",
    "commit via PREPARE → INDEPENDENT VERIFY → LAW → ATOMIC COMMIT → VERIFY→PROVE→PROPAGATE: lock, reread state, recompute scope closure, re-verify predicates, publish atomically, advance epoch",
    "a version check outside the committing transaction is not a guarantee",
    "stale or ambiguous state shall not create qualification or execution authority; independently supported unaffected capabilities preserved",
    "resolve races explicitly: withdrawal-vs-merge, split-vs-promotion, provisional-scope-vs-ACT",
    "incident containment via governed write: commit record, withdraw reliance, fence dependents, recalibrate after",
    "Authorize(a,s) ⇒ CurrentTaxonomy ∧ CurrentQualification ∧ NoDisqualifyingIncident ∧ EvidenceCovers ∧ LAWPermits",
    "rollback is a new governed revision, never a reused number; history preserved through merges/splits",
    "name honest limits: database ordering cannot revoke an in-flight external effect — represent, reconcile, limit claims to the enforcement boundary"
  ],
  "lesson_line": "One canonically ordered governance state: lock, reread, re-verify, commit, advance the epoch — stale state never creates authority."
}
~~~
