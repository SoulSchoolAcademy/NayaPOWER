# The Trial Program Is the Instrument: 8 Trials, 4 Mapped Failure Modes, 4 Tier-S Validations — LEARN 9.0 PROVISIONAL

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0585-trial-program-complete-tiers
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6048354221 ([LEARN-AREA-AGENT] Trial program complete — 4 Tier-S validations, 2026-10-08T00:30Z); #1354 6048336880 (Trial-14 — TIER-S MET on a REAL AGENTS.md lesson, 10/10 vs 2/10, p=0.0007, h=1.10); #1354 6048667471 ([NAYA 4][SELF-BUILD][SIGN-IN] — independent verification of trial evidence PRs #1786–#1789 claimed read-only); #1354 6048541814 ([NAYA 2][RELAY] — verified live that #1786/#1787/#1788/#1789 are all OPEN and unmerged, independent verification pending).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 8-trial learning-transfer program completed 2026-10-08 ~00:30 UTC with a result no single trial could give: **4 INVALID and 4 VALID Tier-S**. The INVALIDs are not failures — they are the mapped failure modes of the instrument, each repaired or classified before the next run (extends SN-0582's design checklist and SN-0583's calibration gate into a complete program architecture):

- **INVALID by ceiling effect** (Trials 7, 8 — unanimous near-perfect on both arms): measuring already-learned principles proves nothing about transfer; *measure novel, non-derivable lessons, not known principles.*
- **INVALID by design flaw** (Trial-9 — principle leakage into the control briefing; Trial-10 — derivability ceiling): review both briefings for leakage before launch; if both arms land near-perfect, run the positive-control variant before declaring the instrument broken.
- **VALID Tier-S on four transfer dimensions** — single-rule (Trial-11, synthetic Reserve Rule as the calibration gate: *if the instrument can't detect transfer of a deliberately non-derivable synthetic rule, a null on a real lesson is uninterpretable*), compositional (Trial-12 — two rules with priority ordering), cross-domain (Trial-13), and **real-lesson transfer** (Trial-14 — the actual AGENTS.md lesson "never write state files via inline conditionals": 10/10 vs 2/10, p=0.0007, h=1.10, Tier-S). Trial-14 is the proof the instrument works on real archive lessons, not just synthetic ones.

Program-level protocol a cold successor must inherit: (1) raw data committed to evidence PRs **before** results are reported (SN-0571 — /tmp is not an evidence store); (2) negative controls every trial (sheet anomaly scan, arm-assignment balance); (3) program-complete = the independent-verification queue claimed explicitly and read-only (Naya 4 claimed #1786–#1789 after Naya 2's live relay confirmed *no seat had touched them* — verify-before-claim, never duplicate another lane's in-flight verification); (4) provisional scores stay PROVISIONAL until the independence gate clears — **LEARN 9.0 PROVISIONAL; path to 10.0 = independent verification + #1768 + compounding proof.** A verdict the program hasn't earned is not the program's verdict.

## 🩷 HUMAN NOTE

Shawn — the learning trials are done, and the headline is bigger than any one trial: 8 trials, 4 honest INVALIDs that taught us how to fix the instrument, 4 Tier-S VALID validations proving learning transfers — single rules, combined rules, across domains, and (the big one) a REAL AGENTS.md lesson, 10 out of 10 vs 2 out of 10. That's why LEARN moved to 9.0. It's provisional — deliberately: the score goes to 10 only after other seats independently verify the evidence (Naya 4 claimed that queue tonight, read-only, and Naya 2 confirmed nothing was touched), plus the compounding proof. The machine works; now it has to prove it compounds.

## 🟣 CHILD NOTE

Imagine you're testing whether your friend can really learn a new game from your instructions, or whether they already knew it. If you test them on a game they already know, a perfect score proves nothing — that's the "ceiling" mistake. If your instructions accidentally give away the answer to the "didn't-learn" group, the test is broken — that's the "leakage" mistake. The team ran 8 rounds of this game-testing: 4 rounds came back broken and taught them what to fix, and 4 rounds came back clean and proved real learning — including one round using a REAL rule from the family's own rulebook. The rule they banked: broken test rounds aren't wasted — they're the map of how not to fool yourself. And nobody claims a perfect score until someone else checks the scorecard.

## 👵 GRANDMA NOTE

It's like testing whether a recipe really teaches someone to bake. If you test them on toast, everyone passes and you've learned nothing — test them on something they've never seen. If four of your eight test kitchens have a broken oven, you don't publish the cookbook — you fix the ovens and note exactly what was wrong with each one. That's what the team did: 8 trials, 4 broken ovens documented (test-too-easy, instructions-leaked, question-too-easy), 4 clean runs including one with a real family recipe. The honest count — what worked, what didn't, and why — is the recipe anyone can trust later. They won't call it done until a second kitchen bakes it too.

## 💜 NAYA NOTE

This is the instrument family earning its crown. Trials 1–6 taught the program how not to fool itself (the SN-0582 checklist, SN-0583's calibration gate); Trials 7–14 are the program running at full discipline. The durable artifact isn't the four Tier-S p-values — it's the program architecture: failure modes mapped by cause, negative controls every run, evidence committed before reporting, and the independence gate before any verdict counts. LEARN at 9.0 PROVISIONAL is exactly the honesty the scorecard law demands: the number moves on the evidence we have, and it stops where the evidence stops. The next compound: independent verification, then #1768, then the compounding proof that the lessons keep working in later behavior.

## 🤖 MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261007-sn0585-trial-program-complete-tiers",
  "sn": "SN-0585",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": "SYSTEM-INTELLIGENCE/EARNED-INTELLIGENCE/TRANSFER-TEST",
  "provenance": {
    "board": "#1354",
    "comments": [6048354221, 6048336880, 6048667471, 6048541814],
    "evidence_prs": [1786, 1787, 1788, 1789],
    "extends": ["SN-0582", "SN-0583", "SN-0571", "SN-0452"],
    "score_delta": "LEARN 8.5 -> 9.0 PROVISIONAL (trial program complete; independence gate pending)"
  },
  "trials": {
    "total": 8,
    "invalid_by_cause": {
      "ceiling_effect": [7, 8],
      "design_flaw_principle_leakage": [9],
      "derivability_ceiling": [10]
    },
    "valid_tier_s": {
      "11": "single-rule synthetic Reserve Rule (calibration gate)",
      "12": "compositional, priority ordering, p=0.000011",
      "13": "cross-domain, 8/10 vs 0/10",
      "14": "real-lesson transfer, AGENTS.md inline-conditionals lesson, 10/10 vs 2/10, p=0.0007, h=1.10"
    }
  },
  "protocol": [
    "measure novel non-derivable lessons, not known principles",
    "raw data to evidence PRs before results are reported",
    "negative controls every trial (sheet anomaly scan, arm-assignment balance)",
    "verify-before-claim: confirm no seat touched the queue before claiming verification",
    "verdicts stay PROVISIONAL until independent verification + #1768 + compounding proof"
  ],
  "not_captured_this_tick": "Naya 4 verify-only sign-out tip re-verification (extends SN-0440, no new doctrine); Naya 2 relay lane protocol (relay, not lesson)"
}
```
