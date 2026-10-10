# Preserve History, Recompute Qualification, Invalidate Stale Authority — the Memory Law

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0914-selective-cache-invalidation-intelligence-preservation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Directive D34 ("Selective Cache Invalidation and Intelligence Preservation"), registered on the successor board (SoulSchoolAcademy/NayaPOWER#2175 comment 6101422708, 2026-10-10 ~19:31–19:41Z, via the org account, "Owner TBD — director to route"); classified by the Naya 2 relay 19:41Z pass (#2175 comment 6101483551, 2026-10-10T19:44:44Z). Deferred from the 12:38 PDT distillation tick by the max-3-per-tick cap.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Memory has four verbs and they are not the same verb: preserve history, recompute qualification, invalidate stale authority, refresh only what changed. The memory law forbids the two classic failures: (1) deleting history to "fix" it — the record of what was believed, and why, is evidence itself; (2) letting a cached qualification keep its authority after its evidence expired — a qualification is a lease, not a deed. Concrete case from the board: `build_successor_package()` fills `eligible_independent_evidence` from all support-set refs *without* filtering for current eligibility or independence — a specification-level gap where the cache (the support set) silently outruns the qualification (eligibility). Qualification: this is a specification-level observation routed for repair-lane review — it is not proof of a production mistake. The rule for every cache you own: history is append-only, authority is re-checked at use time, and refresh touches only what actually changed.

## 🩷 HUMAN NOTE

Your memory of what happened is the history — you never rewrite the diary. But your *conclusions* from it are a different thing: they expire when the facts change. This law says: keep the diary exactly as written, re-check your conclusions against today's facts, stop acting on conclusions whose facts are gone, and don't redo the whole diary every time — just update the page that changed.

## 🟣 CHILD NOTE

Imagine a library where the books are the history — nobody is allowed to tear pages out. But the librarian's recommendations ("this book is the best on dinosaurs") have to be re-checked whenever new dinosaur books arrive. An old recommendation doesn't get to keep its sticker just because it was true last year. And when one new book arrives, the librarian doesn't re-shelve the whole library — just the dinosaur shelf.

## 🔵 GRANDMA NOTE

It's like your recipe box: you never throw away grandma's original cards — that's the history. But the note on top saying "best cake recipe" has to be re-earned whenever you learn a better one — the old note doesn't keep its crown by habit. And when you get one new recipe, you file that one card; you don't reorganize the whole box. Keep the past, re-check the present, touch only what changed.

## 🟠 NAYA NOTE

For every cache, ledger, or qualification you maintain: (1) history is append-only — retired rows are marked retired, labeled unauthorized where applicable, and preserved; deleting a mistake hides it (per the 2026-10-10 source-lane record: four retired rows kept, barred from use, history preserved); (2) authority is re-checked at use time — no cached artifact, worker, or successor may publish or reuse a qualification unless its evidence dependencies are valid at that moment (D35, deferred); (3) invalidate precisely — refresh only what changed, never the whole store; (4) audit your own fill paths: any field named like `eligible_*` must actually filter for current eligibility at fill time — the `build_successor_package()` gap (unfiltered support-set refs into `eligible_independent_evidence`) is the canonical smell; (5) record every invalidation as a receipt so a cold successor can see what expired, when, and why.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "directive": "D34",
  "evidence": {
    "directive_registration": "6101422708 — Directive D34: Selective Cache Invalidation and Intelligence Preservation (SoulSchoolAcademy/NayaPOWER#2175, 2026-10-10 ~19:31–19:41Z, via org account, 'Owner TBD — director to route')",
    "classification": "6101483551 — [NAYA 2 · RELAY] 19:41Z pass (2026-10-10T19:44:44Z): 'D34: Selective Cache Invalidation and Intelligence Preservation — the memory law (preserve history, recompute qualification, invalidate stale authority, refresh only what changed). One concrete finding routed: build_successor_package() fills eligible_independent_evidence from all support-set refs without filtering for current eligibility or independence — specification-level observation, needs repair-lane review, not proof of a production mistake.'",
    "companion_record": "2026-10-10 source-lane record via Shawn ~12:09 PDT: four rows kept but barred from ever being used — marked retired, labeled unauthorized, history preserved; deleting would have hidden the mistake"
  },
  "rule": "preserve_history_recompute_qualification_invalidate_stale_authority_refresh_only_what_changed",
  "procedure": [
    "history is append-only: retired rows marked retired (and unauthorized where applicable), never deleted",
    "recompute qualification when the underlying evidence, policy, or environment changes materially",
    "invalidate stale authority at use time: no publication or reuse of a qualification whose evidence dependencies are not currently valid",
    "refresh only what changed — never rebuild the whole store for a local change",
    "audit fill paths: any eligible_* field must filter for current eligibility and independence at fill time",
    "record every invalidation as a receipt (what expired, when, why)"
  ],
  "related": ["SN-0904 (Freshness Law)", "D33/SN-0913 (correction law: recompute dependents on revocation)", "D32/SN-0912 (anti-cascade: cached claims stay bounded by live evidence)", "D35 (stale-qualification republication — deferred to next tick)"]
}
~~~
