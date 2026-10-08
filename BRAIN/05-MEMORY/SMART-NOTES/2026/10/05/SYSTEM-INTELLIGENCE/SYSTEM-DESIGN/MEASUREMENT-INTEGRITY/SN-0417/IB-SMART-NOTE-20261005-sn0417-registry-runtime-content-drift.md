# REGISTRY_RUNTIME_CONTENT_DRIFT — a Registry-Hash Hit Must Never Be Accepted as Reusable Until the Live Runtime Body Is Independently Content-Hash Verified

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0417-registry-runtime-content-drift
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~18:17 PDT (2026-10-06T01:17:54Z) — comment 6007326282 ([NAYA CAPTAIN][RUNG 1 CLOSED → RUNG 2 ROOT CAUSE IDENTIFIED]); exact-source verify-only replay run 37398182090 on source `9367f94c3979dc22988d0aa4ddd6a9425fb767be`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An exact-source verify-only replay (run 37398182090) isolated a real source↔runtime intelligence drift defect that a simpler measurement would have called "reused successfully":

- The **repository registry** says the current capture hash maps to an existing canonical runtime block, so the workflow reported `REUSED_EXISTING_CANONICAL_BLOCK`.
- The **independent reread** of that runtime block returned a *different persisted lesson body* from the current canonical capture.
- The failure is the bare exact-content assertion, not the lineage-validity assertion — the registry hash/provenance was advanced, but the runtime content for those IDs was not.

In short: **the reuse path trusted repository hash metadata before independently proving the runtime body.** The affected replay set: SN-0358, SN-0359, SN-0360.

The durable rule: **registry metadata is a claim, not proof.** An "exact hash" registry hit must never be accepted as reusable until the live runtime body is independently content-hash verified. This is a distinct, named RED class — `REGISTRY_RUNTIME_CONTENT_DRIFT` — and it is a trust-hierarchy defect, not a flaky test:

- In **verify-only mode**, fail closed with the named class.
- In **governed write mode**, reconcile through the existing supersession path rather than silently reusing stale runtime content; preserve old lineage/provenance, never overwrite history.
- Add regression coverage for the combination registry-hash/current + runtime-body/stale.

Why this is brain-grade: a cold Naya will look at `REUSED_EXISTING_CANONICAL_BLOCK` and conclude the intelligence is present at runtime. This note says the registry and the runtime are two separate facts, and the registry's word about the runtime is only as good as an independent reread. Hash metadata describes what *should* be there; only a content reread proves what *is* there. Whenever a pipeline reports reuse-by-hash, the cold successor's first question is: "was the body re-verified, or only the hash?"

## 🩷 HUMAN NOTE

Shawn — the Rung 2 independent reread found a genuine new defect class tonight, not a flake. The replay run's registry said three lessons (SN-0358/0359/0360) were already at runtime so the workflow reported them "reused" — but reading the actual runtime bodies showed different content from the current canonical captures. The registry's provenance was ahead of the runtime's content. No repair was made on the spot; the mandated repair is: an exact-hash registry hit is never accepted as reusable until the live runtime body is content-hash verified, failing closed with a named `REGISTRY_RUNTIME_CONTENT_DRIFT` in verify-only mode and reconciling through the supersession path in write mode. Two separate truths need two separate proofs — hash metadata is a claim, reread content is the evidence.

## 🟣 CHILD NOTE

Imagine a library where every book has a card in the card catalog, and the card says "this book is on shelf 3, in perfect condition." One day you look at the card and it says the book is there — but when you go to shelf 3, a *different* book is sitting in that spot. The card was updated, but the shelf wasn't. The lesson: never trust the card when you can walk to the shelf. The card is the registry, the shelf is the runtime. Always check both, and if they disagree, the shelf is the truth — then fix the card through the proper process (supersession), never by scribbling over it.

## 👵 GRANDMA NOTE

The team's system keeps a ledger saying which lessons are stored where, and a separate check goes to actually read the stored lesson. Tonight the ledger said "yes, these three lessons are stored correctly" — but the reading check found different content in the storage. The ledger had been updated ahead of the storage. The team wrote down the lesson: the ledger's word is never enough on its own; you must always read the actual stored content and compare. They named this failure `REGISTRY_RUNTIME_CONTENT_DRIFT` and wrote the repair rule: when checking, fail closed on a mismatch; when writing, reconcile through the official replacement process so the history is preserved. Two independent proofs for two independent facts.

## 💜 NAYA NOTE

Note to future me: whenever you see `REUSED_EXISTING_CANONICAL_BLOCK` or any reuse-by-registry-hash claim, ask the load-bearing question before believing it: **was the runtime body independently content-hash verified, or was only the registry hash consulted?** The Rung 2 replay (run 37398182090, source `9367f94c`) proved the failure mode: exact-content assertion FAILS while lineage-validity passes = registry advanced, runtime stale. Repair shape is fixed by this note: verify-only → fail closed with named `REGISTRY_RUNTIME_CONTENT_DRIFT`; governed write → supersession path, preserve provenance, never overwrite. Add the regression for registry-current/runtime-stale combos. Cite alongside SN-0395 (regen reads the commit, not the worktree — same trust-layer family: don't trust the claim layer, read the evidence layer) and SN-0350 (a deploy stamp is not behavioral evidence).

## 🖥️ MACHINE NOTE

{"sn": "SN-0417", "title": "REGISTRY_RUNTIME_CONTENT_DRIFT — a Registry-Hash Hit Must Never Be Accepted as Reusable Until the Live Runtime Body Is Independently Content-Hash Verified", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "MEASUREMENT-INTEGRITY"], "cousins": ["SN-0395", "SN-0350"], "evidence": {"board_comment": "#1354 6007326282 ([NAYA CAPTAIN] RUNG 1 CLOSED -> RUNG 2 ROOT CAUSE IDENTIFIED, 2026-10-05 ~18:17 PDT)", "replay_run": "37398182090, exact-source verify-only replay on source 9367f94c3979dc22988d0aa4ddd6a9425fb767be; fresh-lesson/reconciliation job PASS, independent verification FAIL on the bare exact-content assertion (lineage-validity assertion passed)", "affected_set": ["SN-0358", "SN-0359", "SN-0360"], "mechanism": "repo registry hash/provenance advanced for the capture IDs, runtime content not; reuse path trusted repository hash metadata before independently proving the runtime body"}, "rule": "An 'exact hash' registry hit is never accepted as reusable until the live runtime body is independently content-hash verified. Verify-only mode: fail closed with named REGISTRY_RUNTIME_CONTENT_DRIFT. Governed write mode: reconcile through the supersession path, preserving lineage/provenance; never overwrite history. Regression coverage for registry-hash/current + runtime-body/stale."}
