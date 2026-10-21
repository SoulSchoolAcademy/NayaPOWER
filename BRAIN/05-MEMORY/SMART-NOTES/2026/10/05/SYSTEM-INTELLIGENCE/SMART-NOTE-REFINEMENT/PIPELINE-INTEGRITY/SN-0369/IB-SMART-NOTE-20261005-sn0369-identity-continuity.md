# Identity Continuity — a Canonical Repair Must Preserve the Requested Smart Note ID

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0369-identity-continuity
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~09:32–09:35 PDT — Naya identity-continuity correction (comment 5998719606), scorecard receipt PR #1482 (comment 5998753292), scope update closing inherited SN-002 conformance RED (comment 5998776908).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The SN-0355 canonical repair (PR #1477) fixed the capture but the capture pipeline allocated a new human ID instead of preserving the requested one: the canonical capture carried no explicit `smart_note_id`, so the projector regenerated the note as SN-346 while the director's requested identity was SN-0355 — two human views of one note. Classification: IDENTITY CONTINUITY DEFECT. The standing repair (PR #1482, one line): add explicit `smart_note_id=SN-0355` to the canonical capture, and remove the stale generated SN-346 projection so it cannot survive as a second view. The same PR also carried the missing boolean `machine_view.raw_source_separate_from_distillation=true`, which closed the inherited SN-002 conformance RED (`test_baseline_never_grows` was failing on the SN-0355 capture) — fixed at the canonical seam instead of growing the exemption baseline. And the merge acceptance is runtime evidence, not merge success: same IB → SN-0355 registry → regenerated SN-0355 projection → CANDIDATE → the exact 9 gates.

Why this is brain-grade: every future repair to the canonical capture path must carry the requested identity through, or the pipeline quietly re-numbers notes and the registry, the projection, and the human's reference diverge. The repair also demonstrates the right direction for inherited REDs: heal at the canonical seam, never widen the exemption. And the acceptance criterion is a permanent bar — a merge that doesn't regenerate the requested projection at runtime proves nothing.

## 🩷 HUMAN NOTE

Shawn — this morning's SN-0355 repair episode surfaced a pipeline defect and its clean fix: when a repair rewrites a Smart Note's canonical capture, the repair must carry the original note number through explicitly, or the system silently invents a new number and you get two views of one note. The follow-up (PR #1482) does exactly that in one line — and as a bonus it also fixed the SN-002 conformance red at the same seam. The standing rule from now on: any repair of the capture path preserves the requested identity, and acceptance is proven by a regenerated projection, not by the merge landing.

## 🟣 CHILD NOTE

Imagine a library book with a number on its spine. If the library re-binds the book and accidentally prints a *different* number on the new spine, now there are two different numbers for the same book and nobody can find it. The fix: when you re-bind, copy the *original* number carefully, and throw away the wrong spine. And a book counts as "fixed" only when you can actually find it on the shelf by its real number — not just because the binding machine finished.

## 👵 GRANDMA NOTE

Shawn's AI filing system gave one of his notes a new file number when it repaired the file — so the same note existed under two different numbers. They caught it and wrote a rule: whenever you repair a note, you must keep its original number, remove the wrongly-numbered copy, and prove the fix worked by actually finding the note under its real number afterward. A repair isn't done when the paperwork is filed; it's done when the real thing is back in place.

## 💜 NAYA NOTE

For any future seat repairing the canonical capture path: (1) Always add the explicit `smart_note_id` matching the requested identity; never let the allocator mint a fresh one on a repair. (2) Remove the stale generated projection (the wrong-numbered human view) in the same change — it cannot be allowed to survive. (3) If the same change can close an inherited conformance RED at the seam (as #1482 did for SN-002's `raw_source_separate_from_distillation`), take it — but never grow the exemption baseline to make a red go away. (4) Post-merge acceptance is runtime evidence: the same IB must project as the requested SN at CANDIDATE through the exact gate set. Cross-reference SN-0364 (twin-gate fidelity distillation), SN-002 (conformance gate).

## 🖥️ MACHINE NOTE

{"sn": "SN-0369", "title": "Identity Continuity — a Canonical Repair Must Preserve the Requested Smart Note ID", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SMART-NOTE-REFINEMENT", "PIPELINE-INTEGRITY"], "cousins": ["SN-0364", "SN-002", "SN-0355"], "evidence": {"defect": "board #1354 comment 5998719606 — canonical capture of SN-0355 lacks explicit smart_note_id; registry maps IB to generated SN-346; classified IDENTITY CONTINUITY DEFECT", "repair": "board #1354 comments 5998753292, 5998776908 — PR #1482: one-line explicit smart_note_id=SN-0355, removes stale SN-346 projection, adds machine_view.raw_source_separate_from_distillation closing inherited SN-002 test_baseline_never_grows RED at the seam"}, "rule": "Repairs to the canonical capture must carry the requested smart_note_id explicitly and delete the stale generated projection; heal inherited REDs at the canonical seam, never by widening exemptions; merge acceptance is runtime evidence (same IB → requested SN → projection → CANDIDATE → exact gates), not merge success"}
