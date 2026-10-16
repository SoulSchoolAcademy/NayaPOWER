# Name the Guaranteed-by-Construction Half in Writing Before the Run — So the Real Test Is the Other Half

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1502-name-the-guaranteed-half-before-the-run
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-1340-lane5.md` (2026-10-16 21:07–21:35 UTC) + `hidden_files/learning-events-2026-10-16-14.md` (LEARNING CANDIDATE 499)

## ✦ IN A NUTSHELL

The 1340-lane5 seat pre-registered which half of the outcome was guaranteed by the design's own construction — λ=0.12 frozen on the pinned Q15 baseline margin 0.100226, so the Q15 flip was guaranteed; written in PRE-REGISTRATION.md BEFORE any hybrid number. That made the verdict fall on the OTHER half: no-regression on the full 20 pairs. When the run came back 0.50/0.80, it read as a falsification of the mechanism FORM ("lexical overlap is the retrieval signal, not the trap signal") — not an invitation to tune λ. The λ sensitivity characterization (0.06 → Q15 lost, 0.65; 0.18 → Q15 flipped, 0.30) confirmed the trade-off is structural, not parametric. The second falsification stopped iteration per the pre-declared stop rule. No re-tuning permitted, none attempted. A failed experiment became a finding instead of a fishing trip — because the guaranteed half was named in writing, the falsification had nowhere to land except on the mechanism.

## 🩷 HUMAN NOTE

The honest move before an experiment isn't just writing down the pass bar — it's writing down which part of the result the design itself guarantees, so you can't take credit for it afterward. Here, the team knew in advance that the Q15 flip was guaranteed by the construction (λ frozen on the pinned margin), so when the numbers came in weak, they couldn't say "well, at least Q15 flipped." That was never the test. The test was the other half — no regression across all 20 pairs — and it failed, honestly. And because they'd also pre-registered the stop rule, the second falsification ended the experiment. Nobody tuned λ. Nobody squinted. The failure became a finding: the mechanism itself was wrong, not the parameter.

## 🟣 CHILD NOTE

Imagine you're testing whether your special "echo shoes" help you run faster. You know the shoes have springs, so of course the first step is bouncy — that's guaranteed by the shoes themselves, and you write that down before the race. The real test is the other half: do you finish the whole race faster, not just bounce the first step? You don't. The springs helped the bounce (guaranteed) but you were slower overall (the real test). You don't change the springs and race again. You write down: the spring idea doesn't make runners faster. Two races, same answer — done.

## 🔵 GRANDMA NOTE

It's like testing a new soup recipe. You know adding salt makes it saltier — that's guaranteed, not the test. The real test is whether it tastes better. It doesn't. Because you wrote down "saltier is guaranteed" before tasting, you can't fool yourself afterward into saying "but it IS saltier!" as if that were the point. The test was taste. It failed. You stop tweaking the salt and throw out the recipe. Two tastings, same verdict — the recipe is the problem, not the amount of salt.

## 🟠 NAYA NOTE

Apply this to every experiment and trial you run: (1) before the run, write down explicitly which part of the outcome is guaranteed by the design's own construction — the part you may NOT take credit for; (2) name the OTHER half as the real test, in the same writing; (3) pre-register the failure clause AND the circuit-breaker stop count (here: the second falsification stops iteration); (4) when the run fails, read the verdict by elimination — the guaranteed half is out of play, so the falsification lands on the mechanism, not the parameter; (5) characterize the parameter sensitivity ONCE to confirm the trade-off is structural (0.06 lost it, 0.18 flipped it, 0.30 broke everything — structural, not tunable); (6) no re-tuning after the stop rule fires — a re-tuned "pass" after a pre-registered stop is a fishing trip with a better story.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "post_hoc_interpretation_slip",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-1340-lane5.md (2026-10-16 21:07–21:35 UTC)",
    "preregistration_sha256": "18e09f0585dd… (PRE-REGISTRATION.md, written BEFORE any hybrid number)",
    "guaranteed_half": "λ=0.12 frozen on the pinned Q15 baseline margin 0.100226 — the Q15 flip is guaranteed by construction",
    "real_test": "no-regression on the full 20 pairs",
    "result": "0.50/0.80 — read as falsification of the mechanism FORM ('lexical overlap is the retrieval signal, not the trap signal'), not an invitation to tune λ",
    "sensitivity": "λ=0.06 → Q15 lost (0.65); λ=0.18 → Q15 flipped (0.30) — trade-off structural, not parametric",
    "stop_rule": "second falsification stopped iteration; no re-tuning permitted or attempted"
  },
  "rule": "name_the_guaranteed_half_in_writing_before_the_run",
  "mechanism": "writing fixes the interpretation before the numbers arrive, removing the degrees of freedom that enable fishing; the guaranteed half is excluded from the verdict by elimination, so a failure can only land on the mechanism — and the pre-registered stop count converts the second falsification into a finding instead of a tuning invitation",
  "falsifier": "a written guaranteed-half that still produces tuning or misattributed falsification would falsify the mechanism claim; a post-hoc specification achieving the same stop behavior would show the 'in writing before' part is unnecessary",
  "decision_changed": "every experiment brief carries a written 'guaranteed by construction' clause plus a pre-registered stop count before the run; failed runs are read as mechanism falsifications by elimination; stop rules fire instead of tuning",
  "related": ["SN-01258 (pre-register the bar — the numeric threshold; this is the interpretation complement)", "SN-01498 (pre-declared splits — the values; this is the interpretation)"]
}
~~~
