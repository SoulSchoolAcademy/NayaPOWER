# Adversarial Implementation-Fidelity Audit — A Decided Option Is Verified at the Field Level, Not Just by the Green Suite

**Intelligent Block:** IB-SMART-NOTE-20260930-sn058-adversarial-implementation-fidelity-audit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5929462478 (Naya-2 nine-node verify, 2026-10-01 10:24:07Z) — independent verification of branch naya4/nine-node-kernel-v1 at exact commit 42eb0e0c34bafa851d6d5bc124d5f23612240443 ("Kernel 0.3.0-candidate: FAIL dominates decision verdict; first_non_pass preserved"), adversarial spot-review of the Brief-3 decision implementation, watermark advanced bd8fda27 → 42eb0e0c.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When the Decision Protocol decides an option, the builder implementing it and the suite going green are not the verification. On 2026-10-01 the verifier lane independently re-checked the builder's exact commit in a clean ephemeral worktree (read-only, worktree removed afterward) and did two things: (1) ran the full suite per kernel-tests.yml — 1014 passed, 3 skipped, byte-exact match with the builder's commit-message claim, no CI reliance; (2) an adversarial spot-review that the *decided semantics* were faithfully implemented, field by field — `Kernel.decide()` now sets verdict=FAIL / stopped_at=failing gate when a halting FAIL follows an earlier NEED_EVIDENCE; `first_non_pass` and `first_non_pass_at` are preserved in BOTH the return dict and the hash-bound receipt; the rewritten test pins the new semantics; `verify_decision_receipt()` returns MATCH with the new fields because receipt hash recomputation accounts for them. The verdict was "no findings / discrepancies" — stated explicitly, not implied. The lesson: a decision log names semantics; the implementation-fidelity audit checks the code implements exactly those semantics at the field level. Green suite proves the machine runs; the fidelity audit proves the decision landed as decided.

## 🩷 HUMAN NOTE

Your accountant says "I applied the new tax rule" and shows you a clean report. You don't just admire the clean report — you open the spreadsheet and check that the specific rule was applied to the right cells: the right line carries the new number, the supporting fields still show the old diagnostic values, and the totals recompute with the new inputs. The clean report is reassuring; the cell-by-cell check is the proof. Do both, at the exact version they claimed.

## 🟣 CHILD NOTE

Imagine your friend builds a LEGO set and says "I followed the instructions exactly, see — the box picture matches!" You don't just look at the box picture — you flip open the instruction book to the tricky step, and check that the exact bricks are in the exact places: is the red piece really where step 5 says, are the extra pieces still kept in the tray like the book shows? The box looking right is nice; checking the tricky step brick by brick is how you know they actually followed it.

## 🔵 GRANDMA NOTE

It's like when the pharmacist says they filled the new prescription exactly as the doctor wrote it — you don't just admire the tidy bottle. You read the label against the prescription: the right medicine, the right dose, the right instructions, and the doctor's notes still attached. The tidy bottle is nice; matching the label to the prescription line by line is what tells you the change actually landed the way it was decided.

## 🟠 NAYA NOTE

Apply this every time a lane verifies a decided implementation: (1) verify at the builder-claimed exact SHA, in a clean ephemeral worktree — read-only, removed afterward; never trust the branch label or a moved tip; (2) run the full suite and state the counts against the builder's claimed counts (exact match or not); (3) conduct the adversarial fidelity audit — read the decision's declared semantics from the decision record and check each named field/behavior in the code: the verdict field, the diagnostic-preservation fields, the receipt bindings, the recomputation logic; (4) state the outcome explicitly — "no findings / discrepancies" or name the gap; silence is not a verdict; (5) advance the verification watermark (here bd8fda27 → 42eb0e0c) so the next lane knows exactly what was last verified. Suite-green is the floor; field-level decision fidelity is the bar.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "decision_implementation_drift",
  "evidence": {
    "target": "naya4/nine-node-kernel-v1 @ 42eb0e0c34bafa851d6d5bc124d5f23612240443 — 'Kernel 0.3.0-candidate: FAIL dominates decision verdict; first_non_pass preserved'",
    "suite_check": "1014 passed, 3 skipped in clean ephemeral worktree (pytest -q per kernel-tests.yml, pyyaml + pglast installed) — exact match with builder's commit-message claim, no CI reliance",
    "fidelity_audit": "adversarial spot-review vs Brief-3 decision (5929067367): Kernel.decide() sets verdict=FAIL / stopped_at=failing gate when halting FAIL follows earlier NEED_EVIDENCE; first_non_pass / first_non_pass_at preserved in return dict AND hash-bound receipt; rewritten test pins new semantics; verify_decision_receipt() MATCH accounts for new fields",
    "outcome": "no findings / discrepancies; read-only — no branch mutation, no merge, no push",
    "watermark": "bd8fda27 → 42eb0e0c"
  },
  "rule": "adversarial_implementation_fidelity_audit",
  "procedure": [
    "verify at the builder-claimed exact SHA in a clean ephemeral worktree (read-only, removed afterward); never trust the branch label",
    "run the full suite and state counts against the builder's claimed counts",
    "fidelity audit: read the decision's declared semantics from the decision record; check each named field/behavior in the implementation (verdict, diagnostic preservation, receipt bindings, recomputation)",
    "state the outcome explicitly — 'no findings / discrepancies' or name the gap",
    "advance the verification watermark to the exact verified SHA"
  ],
  "related": ["SN-028 (clean-room verification)", "SN-050 (verify the pushed bytes, not the pre-commit bytes)", "SN-043 (compare at ONE commit)"]
}
~~~
