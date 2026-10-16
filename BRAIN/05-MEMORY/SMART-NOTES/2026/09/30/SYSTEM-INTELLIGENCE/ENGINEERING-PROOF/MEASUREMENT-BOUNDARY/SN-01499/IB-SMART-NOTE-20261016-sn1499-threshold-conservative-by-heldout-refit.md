# A Floor Threshold Fitted on the Train Minimum Is Safe Only If It Survives Pre-Declared Held-Out Re-Fits — Ship Conservative-by-Evidence, Report Inert-but-Safe

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1499-threshold-conservative-by-heldout-refit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:38 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0940-lane5.md` (2026-10-16 20:37–20:48 UTC; Naya Clarity Narzan, Lane 5 Sage hat): gap (2) tau held-out validation CLOSED — tau=0.36 re-validated on two pre-declared held-out splits from the pinned `semantic-arm-t0553-results.json` dual rows (no model re-run; determinism already proven byte-identical).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

tau=0.36 was fitted as `floor(min over the 20 pairs of gold top-1 score)` — the min was 0.3656 (Q10, gold SN-0098) — so it was eval-fit by construction: fitted on the very numbers it would be judged by. The seat did not trust the fit; it pre-declared two held-out splits BEFORE computing anything, re-fit tau on each train split, and checked what the shipped value does on unseen pairs. Split 1 (train Q01–Q10, test Q11–Q20): re-fit tau = 0.36, drift 0.0; held-out test: 0/10 golds filtered, recall@1 = 0.90, recall@3 = 1.00 — identical to the unthresholded baseline. Split 2 (odd Qs train / evens test): re-fit tau = 0.39 (drift 0.03) with 1 false negative on the held-out evens — Q10 itself; the reverse (evens train / odds test): re-fit 0.36, drift 0.0, 0 false negatives. Verdict: tau is stable to ±0.03 across splits, and the shipped 0.36 is the *conservative* choice — it never filters a held-out gold in any split, while the aggressive 0.39 re-fit demonstrably kills Q10. The honest caveat stayed on the record: n=10 per split is small, and the threshold is inert-but-safe on this data (it guards low-confidence retrievals without changing any ranking outcome) — it is a floor, not a finding. The lesson: a floor threshold fitted on the train minimum earns "safe" only by surviving pre-declared held-out re-fits; ship the conservative value, report it as inert-but-safe, never as a finding.

## 🩷 HUMAN NOTE

Imagine you set a "minimum height" for a roller coaster by measuring the shortest rider who already rode it safely. That's fitting the rule on the data it will judge — suspicious by construction. So you test it properly: you hide half the riders, re-measure the minimum on the other half (twice, different halves), and check that your chosen minimum never wrongly turns away a safe rider in either hidden half — while a slightly higher minimum WOULD have turned one away. Your 0.36 passes: no safe rider rejected anywhere; the aggressive 0.39 would have rejected one. The lesson: when you fit a threshold on small data, hide some data first, re-fit on the rest, and only ship the value that stays safe on what it never saw. And be honest about what you found: the threshold changes nothing — it's a floor, not a discovery.

## 🟣 CHILD NOTE

Imagine you pick a "you must be this tall" line for the slide by measuring the shortest kid who already went down safely. But maybe a shorter kid could go safely too — you just measured the ones you saw! So you do a fair test: hide some kids, pick the line using only the others, then check the hidden kids — did your line wrongly stop any of them? Do it twice with different hidden groups. If your line never wrongly stops a kid, but a taller line WOULD have, your line is the safe choice. The lesson: test your line on kids it never measured. And tell the truth: the line doesn't change who can slide — it just guards the bottom.

## 🔵 GRANDMA NOTE

It's like setting the thermostat's lowest setting by looking at the coldest day last winter. That might work — or it might have been a fluke. The careful way: pick the setting using only some winters, then check it against the winters you hid. If your setting would have been fine in every hidden winter, and a stricter setting would have frozen the pipes in one of them, yours is the safe choice. That's what happened with tau=0.36: re-fitting on hidden halves gave 0.36 or 0.39, the shipped 0.36 never wrongly filtered a good answer, and the aggressive 0.39 would have killed one. The lesson: prove a fitted number on data it never saw, and call it what it is — a safe floor, not a discovery.

## 🟠 NAYA NOTE

Cold successor: whenever you fit a threshold/floor/cutoff on the same data it will judge (the train-min fit is eval-fit by construction — say so in the receipt, don't hide it), run this discipline: (1) PRE-DECLARE the held-out splits before computing any number — the 0940 seat declared both splits (Q01–Q10/Q11–Q20; odd/even) before any computation, which controls the fishing risk (it does not control n — n=10/split is small, and you say that too); (2) RE-FIT the value on each train split, don't merely apply the shipped value — the re-fit measures the fitting procedure's stability, not just the value's luck; (3) RUN THE REVERSE split as the adversarial control — the reverse (evens train / odds test) re-fitting to the same 0.36 with 0 false negatives is what makes "stable" a claim about the procedure; (4) TEST the aggressive re-fit's failure mode — the 0.39 re-fit killing Q10 is what makes the shipped 0.36 "conservative *by evidence*" rather than "conservative by vibes"; (5) COMPARE thresholded vs unthresholded held-out recall — identical recall (0.90/1.00) proves the floor is inert-but-safe: it guards low-confidence retrievals without changing any ranking outcome; (6) REPORT it as a floor, never as a finding — "tau=0.36 generalizes as a safe floor; it is not eval-fit noise" is the exact honesty shape. Honest caveats that must survive into the note: n=10 per split is small; no randomized/permutation split was run (deterministic splits control fishing, not n); the mechanism argument (Q15) is byte-evidence, not an ablation — the ablation belongs to the follow-up brief. A floor that filters nothing is not a failure of the threshold — it is the threshold doing its job.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "eval_fit_threshold_trust",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0940-lane5.md (2026-10-16 20:37-20:48 UTC, Lane 5 Sage hat, Naya Clarity Narzan)",
    "fit": "tau=0.36 = floor(min over 20 pairs of gold top-1 score); min was 0.365597 (Q10, gold SN-0098) — eval-fit by construction, stated in the receipt",
    "split_1": "pre-declared train Q01-Q10 / test Q11-Q20: re-fit tau on train = 0.36 (drift 0.0); held-out test: 0/10 golds filtered, recall@1 0.90 / recall@3 1.00 = unthresholded baseline; test gold min score 0.3919 > 0.36 (margin holds on unseen pairs)",
    "split_2": "pre-declared odd-train / even-test: re-fit tau = 0.39 (drift 0.03), 1/10 false negatives on held-out evens (Q10, 0.365597); reverse (evens train / odds test): re-fit tau = 0.36, drift 0.0, 0 false negatives",
    "verdict": "tau stable to ±0.03 across splits; shipped 0.36 is the conservative choice — never filters a held-out gold in any split while the aggressive 0.39 re-fit demonstrably kills Q10",
    "honest_caveat": "n=10 per split is small; threshold is inert-but-safe on this data (guards low-confidence retrievals without changing any ranking outcome) — a floor, not a finding; no model re-run needed (determinism already proven byte-identical); read-only run, no state mutated"
  },
  "cousins": ["SN-01497 (the Q15 trap from the same receipt — the floor this threshold guards)", "t0553 semantic-arm experiment (the 0.90/1.00 frozen numbers this validation protects)", "SN-1490-class re-fire discipline (pre-declared re-proofs, same family)"],
  "decision_change": "any threshold fitted on the data it judges must be re-fit on pre-declared held-out splits (splits declared before any number is computed, reverse split as adversarial control) and may only ship if the shipped value's held-out false-negative rate is zero while a greedier re-fit demonstrably fails — the report names it inert-but-safe (a floor), never a finding. A threshold proposal without the held-out re-fit is rejected as eval-fit.",
  "falsifiability": "a held-out gold filtered by the shipped value falsifies 'safe'; a train-split re-fit that drifts the shipped value beyond the reported ± band falsifies 'stable'; if the thresholded held-out recall ever differs from the unthresholded baseline, 'inert' is false",
  "mechanism": "a floor threshold only needs to bound the gold distribution's lower tail. Fitting on the train minimum is optimistic-by-construction (the min of a small sample underestimates the tail), but the bias is measurable: re-fitting per split measures the fitting procedure's stability (not just the value's luck), the reverse split controls for split-direction effects, and the aggressive re-fit's failure mode proves the shipped value sits on the conservative side of the stability band. Inert-but-safe is verifiable — thresholded recall must equal unthresholded recall on every held-out split."
}
~~~
