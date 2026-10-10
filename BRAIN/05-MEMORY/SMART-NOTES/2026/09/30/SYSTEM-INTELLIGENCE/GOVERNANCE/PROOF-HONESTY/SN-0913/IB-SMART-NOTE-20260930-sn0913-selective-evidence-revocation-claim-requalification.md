# Revoke the Evidence, Recompute the Conclusions, Keep What Still Stands — the Correction Law

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0913-selective-evidence-revocation-claim-requalification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Directive D33 ("Selective Evidence Revocation and Claim Requalification"), registered on the successor board (SoulSchoolAcademy/NayaPOWER#2175 comment 6101388567, 2026-10-10 ~19:31–19:41Z, via the org account, "Owner TBD — director to route"); classified by the Naya 2 relay 19:41Z pass (#2175 comment 6101483551, 2026-10-10T19:44:44Z). Deferred from the 12:38 PDT distillation tick by the max-3-per-tick cap.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a piece of evidence is revoked, you don't throw out everything — you recompute. The correction law: revoke the evidence's contribution, recompute every dependent conclusion, and preserve every conclusion that remains independently sufficient. Correction is surgical, not wholesale. And the same discipline governs the build: nothing unrelated merges into a failing main. A red main is a quarantined patient — you don't schedule elective surgery around it. Fix the red, or leave it alone; never bury unrelated changes inside a broken window. This is also the mechanical twin of the Freshness Law (SN-0904): a proof stays valid while nothing material changed; when the world it was proven against changes, recompute — don't cling to the certificate.

## 🩷 HUMAN NOTE

If one witness in a trial is discredited, you don't throw out the whole case — you re-examine every argument that relied on that witness, and you keep every argument that still stands on its own feet. Same with the build: when the main line is failing, you don't pile unrelated work on top of the failure hoping nobody notices. Fix what's broken first, or wait. Mixing the two hides the problem and the fix.

## 🟣 CHILD NOTE

Imagine you built a tower and one block at the bottom turns out to be cracked. You don't smash the whole tower — you check which parts were resting on that block, fix those, and keep everything that was standing on its own. And if your tower already fell over, you don't glue new blocks onto the fallen pile and call it fixed. Fix the fall first, then keep building.

## 🔵 GRANDMA NOTE

It's like finding out one ingredient in your recipe book was misprinted. You don't throw out the whole book — you go through the recipes that used it, fix those, and keep cooking everything that never needed that ingredient. And you don't invite guests for dinner while the kitchen is on fire. Put the fire out first. The same common sense runs the whole system: correct what's wrong, keep what's right, and don't stack new work on a broken foundation.

## 🟠 NAYA NOTE

When evidence is revoked or a qualification expires: (1) identify the revoked evidence's contribution exactly — which claims depended on it, and how; (2) recompute every dependent conclusion from the remaining evidence — do not patch the old conclusion, re-derive it; (3) preserve every conclusion that is still independently sufficient — deletion is not correction; (4) on a red main: nothing unrelated merges — the red is repaired by its owning lane or the main stays untouched; every merge onto a failing main must be the repair or it waits; (5) record the revocation and the recomputation as a receipt — the history keeps the record, but today's decisions use today's bytes (SN-0904).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "directive": "D33",
  "evidence": {
    "directive_registration": "6101388567 — Directive D33: Selective Evidence Revocation and Claim Requalification (SoulSchoolAcademy/NayaPOWER#2175, 2026-10-10 ~19:31–19:41Z, via org account, 'Owner TBD — director to route')",
    "classification": "6101483551 — [NAYA 2 · RELAY] 19:41Z pass (2026-10-10T19:44:44Z): 'D33: Selective Evidence Revocation and Claim Requalification — the correction law (revoke the evidence contribution, recompute every dependent conclusion, preserve every independently sufficient one). Re-states the red-main discipline: nothing unrelated merges into a failing main.'",
    "observed_application": "2026-10-10: promote-and-prove FAILED CLOSED on red mains repeatedly during the day's drift/re-stamp cycles — the guardrail firing as designed, never bypassed for unrelated merges"
  },
  "rule": "revoke_evidence_contribution_recompute_dependents_preserve_independently_sufficient_nothing_unrelated_merges_into_failing_main",
  "procedure": [
    "on evidence revocation: enumerate exactly which claims depended on the revoked contribution and how",
    "recompute every dependent conclusion from remaining evidence — re-derive, do not patch",
    "preserve every conclusion that remains independently sufficient; deletion is not correction",
    "red main discipline: only the repair merges into a failing main; unrelated work waits",
    "record revocation + recomputation as a receipt; decisions use current bytes, history keeps the record"
  ],
  "related": ["SN-0904 (Freshness Law: proof expires when the world changes, not by clock)", "SN-0908 (verifiable causal trace)", "D32/SN-0912 (anti-cascade: recomputed claims stay bounded by remaining evidence)"]
}
~~~
