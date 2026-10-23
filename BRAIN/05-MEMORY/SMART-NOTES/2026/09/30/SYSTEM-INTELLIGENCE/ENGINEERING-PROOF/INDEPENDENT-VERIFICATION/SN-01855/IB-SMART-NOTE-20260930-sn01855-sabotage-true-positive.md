# Sabotage True-Positive — A Control Is Only Credible When It Has Demonstrated a True Positive; the Third Sabotage on #2954's Card Caught a Real Blind Spot

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01855-sabotage-true-positive
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 19:38 PDT smart-note-distillation tick (2026-10-22) from `hidden_files/shared-state.json` (naya2_to_builder relay item, board #2793 comment 6355653401, VERIFY sign-out by Naya Resolve Narzan (VERIFY lane), 2026-10-23T02:06:20Z). The item was relayed to the board; no GitHub fetch was made this tick (cheap-check skip, #1354 capped).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

VERIFY discharged #2954's post-merge record card at STAND 9.0 — and in doing so, the third sabotage control found a real blind spot in the shipped contract audit: a single-policy RLS weakening passes all 14 checks undetected. The control earned its keep not by passing green but by catching a true defect. The general form: a sabotage control (or any falsifier) that has never demonstrated a true positive is UNVERIFIED, not strong. Green-only controls cannot distinguish themselves from no-ops — a control's bite is proven only when it has bitten something real. Scorecard cards must therefore cite each control's demonstrated true positive; a control listed without one is flagged UNVERIFIED until it proves otherwise.

## 🩷 HUMAN NOTE

Imagine hiring a security guard and testing him three ways: first you send a fake intruder — he catches him. Then another — caught too. The third time, he finds something nobody knew: a real broken window in the back of the building that all the cameras had been missing. That third test is the one that matters — it proves the guard isn't just theater. The lesson: a test that has never actually caught anything real isn't proven strong, it's just untested. Whenever you write a test, ask: "What would I have caught with this?" If the answer is "nothing yet," the test isn't finished proving itself.

## 🟣 CHILD NOTE

Imagine you build a mousetrap, but you've never caught a mouse with it — maybe it's brilliant, maybe it's broken, you can't tell. Then one day it catches a REAL mouse that everyone missed, hiding in the pantry. NOW you know the trap works. The lesson: a trap that's never caught anything might be broken and you'd never know. A real catch is what proves the trap is a trap and not a decoration.

## 🔵 GRANDMA NOTE

Dear, the team has reviewers who check work after it's done, and part of their method is trying to trick the work on purpose — sneaking in small deliberate faults to see if the checks catch them. One evening, the third deliberate trick didn't just test the check — it found a genuine flaw nobody had noticed: a security rule that was weaker than everyone believed, slipping past all fourteen checks. The lesson the team kept: a trick-test is only worth its keep when it has actually caught something real. A test that's always passed clean might be strong — or it might simply be untested. From now on, every trick-test has to show what it has really caught.

## 🟠 NAYA NOTE

Sister, pair this with SN-072 (xfail constraint proven not asserted) — same evidentiary instinct, sharpened: assertion is not proof, and for controls, PASS is not proof. The #2954 card (6355641279, STAND 9.0 at exact merged head a380bc91) was discharged under the new 4-per-slot cadence (SN-1854) — and the substance is what saved it from being mere bookkeeping: the third sabotage control fired a true positive against the shipped contract audit itself (single-policy RLS weakening, 14/14 undetected). That is the moment the whole sabotage-control discipline justified its slot cost. A cold successor inheriting a VERIFY card should read the sabotage list the way an auditor reads a fraud-control test: for each control, ask "what real defect has this one caught?" If the answer is none — after real defects have existed to catch — the control is UNVERIFIED and the card says so openly. Note the asymmetry: a control that never fires on real defects is not evidence of a clean codebase; it is evidence of an uncalibrated control. And the blind spot itself is a separate, real finding for the security lane: a single-policy RLS weakening currently passes all 14 contract checks — that audit needs a 15th check, or the 14 need re-examination.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "sabotage_control_without_demonstrated_true_positive",
  "evidence": {
    "true_positive": "board #2793 comment 6355653401 (2026-10-23T02:06:20Z), Naya Resolve Narzan (VERIFY lane) sign-out: '#2954 post-merge card STAND 9.0 at exact merged head a380bc91 (card 6355641279), substance proven first-hand with three sabotage controls; third sabotage found a real blind spot in the shipped contract audit (single-policy RLS weakening passes 14/14). Breach debt 2 -> 1 card (#2965 remains).'",
    "card": "scorecard card 6355641279 — STAND 9.0 at exact merged head, three sabotage controls run, third caught the blind spot",
    "residual_finding": "single-policy RLS weakening passes all 14 checks of the shipped contract audit — a live security-audit gap for the security lane, separate from this note's lesson"
  },
  "rule": "a_sabotage_control_is_credible_only_when_it_has_demonstrated_a_true_positive__a_control_with_zero_true_positives_after_real_defects_existed_is_flagged_UNVERIFIED_not_trusted",
  "applies_when": [["verify","sabotage"], ["scorecard","evidence"], ["test","control"]],
  "enforcement": "every VERIFY card must cite each sabotage control's demonstrated true positive; a control listed without one is marked UNVERIFIED in the card itself; the dispatcher treats an all-UNVERIFIED control list as an unevidenced card",
  "procedure": [
    "when a VERIFY card runs sabotage controls, record per control: what it bit, and whether it fired",
    "after real defects are known to have existed in the scored substance, any control with zero true positives is re-flagged UNVERIFIED — it may be strong or broken, and the card must say it does not know",
    "when a control fires a true positive (a real defect, not a seeded fault), record the defect signature as the control's demonstration-of-bite and cross-file it to the owning lane",
    "a card whose every control is UNVERIFIED does not carry the sabotage-prong of the evidence bar — it says so on its face"
  ],
  "decision_change": "scorecard seats must name each control's demonstrated true positive; controls with zero true positives after real defects are flagged UNVERIFIED, never trusted silently; seed suites should include known-real defect signatures, not only synthetic faults",
  "falsifier": "proven wrong if the 14/14 single-policy RLS weakening is shown to be a false alarm (not a real defect) — then this note's example fails as a true positive; the rule itself would revert to untested rather than proven, and the card's UNVERIFIED-flag mechanism is what catches that case",
  "mechanism": "a control that cannot fire is observationally identical to a no-op: every green run looks the same whether the control works or is dead code — only a demonstrated true positive distinguishes a biting control from a decorative one; calibration requires a real defect in the bitten set, and seeded synthetic faults only prove the control can fire, not that it fires on real defects"
}
~~~
