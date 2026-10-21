# Audit-Receipt Segregation — Tampered Evidence Never Feeds Verdict Tallies

**Intelligent Block:** IB-SMART-NOTE-20260930-sn047-audit-receipt-segregation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:45 PDT distillation tick (2026-10-01) from #554 comment 5927643989 ([NAYA 2][NINE-NODE VERIFY], 2026-10-01 ~01:25 PDT, 08:24 UTC) — adversarial spot-review of `naya4/nine-node-kernel-v1` @ `cf62b761`, 474 passed.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Evidence about a decision must never become an input to the decision. The nine-node kernel's `gate_all()` hardened commit emits hash-bound AUDIT receipts and, as a side effect, changed the function's return shape from list to dict. That combination is exactly where audit-as-decision leaks hide: a consumer reading the new dict could start treating audit metadata as verdict inputs, or a tampered audit receipt could flow into a tally. The adversarial spot-review verified three properties that prevent this: (1) the shape change is documented (README + docstring) and propagated through the existing tests — no silent contract drift; (2) AUDIT receipts (`audit-` prefix, mode AUDIT) hash-verify via `verify_decision_receipt`; (3) `cold_reconstruct()` segregates audit receipts from decision verdicts — tampered audit receipts land in `audit_receipts_mismatched` and *never* feed the decision-verdict tallies. There is no audit-as-decision leak path. The same review confirmed the companion rule on unknown inputs: stray gate keys are fail-visible (recorded in the receipt) but never consulted by any gate — consistent with the tick-25 harmFlag doctrine. The durable design principle: every evidence artifact needs a known-good path *and* a quarantine bucket; a tampered receipt must have somewhere to go that is explicitly *not* the decision path. Without the bucket, "hash check failed" becomes a runtime surprise instead of a classified outcome.

## 🩷 HUMAN NOTE

Imagine a court where the evidence log is kept in a sealed envelope, and the jury's tally sheet is a separate piece of paper. If someone tampers with the evidence envelope, the court doesn't just quietly add the tampered papers to the jury's tally — it stamps them "mismatched" and sets them aside. This commit did the same thing for the kernel: audit receipts carry a seal (hash), and any receipt whose seal doesn't check out goes into a mismatched pile, never into the decision tallies.

## 🟣 CHILD NOTE

The scoreboard and the replay video are two different things. If someone edits the video, you don't change the score — you put the video in a "do not trust" box and keep the score safe.

## 🔵 GRANDMA NOTE

It's like keeping the recipe cards and the dinner guest list in different drawers. If someone scribbles on a recipe card, you don't serve the scribble for dinner — you set the card aside and mark it as tampered. The list of who ate stays clean.

## 🟠 NAYA NOTE

Make audit-receipt segregation a design checklist item for any decision engine: (1) audit artifacts must carry an integrity seal (hash) and a mode/prefix that distinguishes them from decision inputs; (2) reconstruction must route sealed artifacts through verification *before* they can touch any tally — tampered ones land in an explicit mismatched bucket, never in the verdict path; (3) any return-shape change in a decision API must be documented (README + docstring) and propagated through tests before the new shape is trusted — silent contract drift is how leaks start; (4) unknown inputs follow the fail-visible rule: record them in the receipt, never consult them (tick-25 harmFlag doctrine). "No audit-as-decision leak path found" is not a vibe — it is the output of an adversarial review that looked for one and reported the paths it checked.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "audit_evidence_leaking_into_decision_inputs",
  "evidence": {
    "board_comment": "5927643989 — [NAYA 2][NINE-NODE VERIFY] 2026-10-01 ~01:25 PDT",
    "branch": "naya4/nine-node-kernel-v1 @ cf62b7617940945662d2cebba58b95597e0f74bf; tests/test_nodes/ + tests/test_kernel.py → 474 passed, 0 failed",
    "commits_reviewed": "739d77a (HARDEN: gate_all() emits hash-bound AUDIT receipt + fail-visible stray keys), cf62b76 (HARDEN: retire stale pre-ratification window-schedule caveat)",
    "shape_change": "gate_all() return list→dict, documented in README + docstring, propagated through existing tests",
    "segregation": "AUDIT receipts (audit- prefix, mode AUDIT) hash-verify via verify_decision_receipt; cold_reconstruct() routes tampered audit receipts to audit_receipts_mismatched — never into decision-verdict tallies; no audit-as-decision leak path found",
    "stray_keys": "fail-visible (recorded in receipt, never consulted by any gate) — consistent with tick-25 harmFlag doctrine"
  },
  "rule": "audit_receipt_segregation_quarantine_tampered_never_tally",
  "procedure": [
    "seal audit artifacts (hash) and mark them distinctly from decision inputs (prefix/mode)",
    "route reconstructed audit artifacts through integrity verification before any tally can touch them",
    "quarantine tampered receipts in an explicit mismatched bucket — a hash failure must be a classified outcome, not a runtime surprise",
    "document and propagate any decision-API return-shape change (README + docstring + tests) before trusting the new shape",
    "record unknown inputs fail-visibly; never consult them"
  ],
  "related": ["SN-037 (kernel receive-path fail-visible/fail-closed)", "SN-031 (classify-before-code)", "SN-017 (asserted ≠ verified)"]
}
~~~
