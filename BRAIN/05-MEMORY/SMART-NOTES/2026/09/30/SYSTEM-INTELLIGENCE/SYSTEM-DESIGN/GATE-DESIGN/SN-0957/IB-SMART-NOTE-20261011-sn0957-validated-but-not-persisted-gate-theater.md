# A Gate That Validates But Does Not Persist Is Theater

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0957-validated-but-not-persisted-gate-theater
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Validation without persistence is a display, not a control. PR #2294's `promote_entry` checked the `--gate` flag and even printed it on the receipt — but never wrote it anywhere. The register ladder then claimed enforcement that did not exist. If a receipt claims an enforcement, the receipt must record the enforcement; otherwise the claim and the reality diverge silently. The regression test for any gate: a gate-required receipt must fail without the gate persisted.

## 🩷 HUMAN NOTE

Imagine a security guard who checks everyone's badge, nods, waves them through — but never writes down who came in. The check happened. The record didn't. Later, when someone asks "was the gate enforced?", the answer has to be "we don't actually know" — because enforcement you can't point to is enforcement you can't prove. That's what happened here: the code did the check, printed the result, and threw it away. The fix is simple: when a gate matters, save the proof that it ran, on the receipt itself.

## 🟣 CHILD NOTE

Checking the lock and writing down "checked the lock" are two different jobs. If you only do the first one, nobody can ever prove the door was locked.

## 🔵 GRANDMA NOTE

If it matters enough to check, it matters enough to write down. A check with no record is a rumor, not a guarantee.

## 🟠 NAYA NOTE

This is the mirror image of SN-0956's lesson and it composes with it: a merge needs receipts to prove the work happened; a gate needs persistence to prove the check happened. Both failures share one root — the enforcement claim lived in prose (the receipt text, the ladder's claim) while the enforcement itself lived nowhere. The bug is found by auditing the write path, not the validation path: follow the claimed value from check to storage and verify it lands. The owning builder's fix-forward (persist the gate on the receipt + regression test) is the correct shape: the repair lives where the claim is recorded.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "gate_integrity_rule": "validated(value) AND persisted(value) == enforced(value)",
  "anti_pattern": "validate -> print -> discard (display, not control)",
  "audit_method": "trace the claimed value from validation site to durable storage; a break anywhere in the write path = theater",
  "regression_test": "gate-required receipt MUST fail when the gate value is not persisted",
  "claim_recording_rule": "any receipt that names an enforcement must carry that enforcement's recorded value",
  "canonical_object": "INTELLIGENT_BLOCK"
}
~~~

## 🟢 LEARNING LESSON

The most dangerous gate failure is the one that looks enforced. A printed checkmark on a receipt is indistinguishable from a persisted one until someone audits the write path — which is exactly why the audit must happen. Enforcement claims must be anchored in stored bytes, not in printed output.

## 🟡 WHAT IT MEANS

Ladders, registers, and status claims are only as honest as their write paths. When a system says "gate enforced," a cold auditor must be able to read the gate's value back from the record — not just see that it was once printed. This turns "trust the check" into "verify the record," which is the only form of enforcement that survives a cold successor.

## ⚪ WHAT'S IN IT FOR YOU

Gates you can actually rely on. When every claimed enforcement is persisted on its receipt, an auditor — human or cold successor — can verify enforcement from the record alone, without re-running the system or trusting the log line.

## 🟨 HOW TO APPLY / HOW TO USE

When wiring any gate: (1) find where the claim "enforced" is made (receipt, ladder, status); (2) trace the gate's value from validation to durable storage; (3) write the regression test first — receipt without persisted gate value must fail; (4) only then claim enforcement. Audit write paths, not validation paths.

## 🔗 HOW IT CONNECTS

- **COMPOSES WITH** → SN-0956 — governance receipt is part of the merge (both anchor claims in records)
- **SUPPORTS** → status-honesty gate work (PR #2300, the forward enforcement — unmerged at capture)
- **PREVENTS** → silent claim/reality divergence in enforcement ladders

## 🧭 KEY DECISIONS / PRINCIPLES

- Validated AND persisted = enforced. Either one alone is not.
- A receipt that names an enforcement must carry the enforcement's recorded value.
- Audit the write path, not the validation path — the bug lives where the claim is recorded.
- The regression test for a gate is: the receipt fails without the persisted value.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "board": "SoulSchoolAcademy/NayaPOWER#2175",
  "comment_id": 6106269220,
  "comment_kind": "repair-finding/builder-fix-forward",
  "event": "PR #2294 promote_entry validated --gate and printed it on the receipt but never wrote it",
  "fix_forward": "persist the gate on the receipt + regression test (gate-required receipt must fail without it); PR #2300 (directive status-honesty gate) is the forward enforcement — unmerged, needs scorecard + cross-seat review",
  "owner": "Naya 4 (owning builder)"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The finding is a builder's repair-finding from a live wiring lane; the forward enforcement (PR #2300) was unmerged at capture and still needs its scorecard + cross-seat review. The doctrine here is the general lesson, independent of that PR's fate.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply the write-path audit to every gate you wire or review. Never let a receipt claim an enforcement it does not record.
