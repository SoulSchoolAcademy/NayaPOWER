# Proof Environments Must Be Reset, Not Reused — Prior-Run Pollution Masquerades as Proof Failure

**Intelligent Block:** IB-SMART-NOTE-20260930-sn087-proof-environments-reset-not-reused
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5937882252 ([NAYA 2][P6-FROZEN], 2026-10-01T18:28:10Z): producer proof of the frozen P6 specimen — "Database `naya_isolated_rt` was truncated before the run (prior runs had polluted it with 5 rows, causing 4 false failures on the first attempt — 10/14. After truncate: 14/14.)" The first attempt's 4 failures were environment pollution, not proof failures; the reset made the distinction visible and the proof green.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A qualification runner was executed twice against the same proof database. The first run failed 4 of 14 checks — not because the subject was broken, but because five leftover rows from prior runs polluted the database. After truncating the database and re-running, the identical proof passed 14/14. The false failures were real-looking, specific, and entirely environmental — exactly the kind of failure that invites "fixing" the subject for a defect it doesn't have. The discipline: a proof environment is part of the proof. Reset it (truncate, recreate, or provision fresh) before the qualification run; never reuse a dirty one. If a run fails, the first question is "was the environment clean?" — and the answer must be checkable, not assumed. Recording the reset ("truncated before the run") is part of the proof report, not garnish: it tells the independent verifier that the green result belongs to the subject, not to a favorable accumulation of prior state.

## 🩷 HUMAN NOTE

Imagine grading a science experiment where the test tubes weren't washed from the last experiment — the results look like your chemicals are bad, but really it's yesterday's chemicals still in the tube. The honest fix isn't better chemicals; it's clean tubes. Same here: the proof failed because the database still held yesterday's rows, not because today's proof was wrong. Clean the environment first, then judge the subject — and write down that you cleaned it, so the verifier trusts the result.

## 🟣 CHILD NOTE

Imagine you weigh yourself on a scale that still has yesterday's backpack sitting on it — it says you're 10 pounds heavier, but that's the backpack's weight, not yours. Take the backpack off (reset!), then step on. The computer learned this the hard way: its proof database still had old rows in it, and the proof "failed" — until someone cleaned the database and the same proof passed. Always clean the scale before you weigh.

## 🔵 GRANDMA NOTE

It's like judging this year's pie contest with last year's crumbs still on the table — the crumbs aren't this year's pie, but they'll make it look like the table is dirty. The discipline: clear the table completely before you start judging, and say out loud that you cleared it. A proof is only about the thing being proven if the room it's proven in is clean — otherwise you can't tell which result belongs to the proof and which belongs to the leftovers.

## 🟠 NAYA NOTE

Apply this to every qualification/proof run: (1) the environment is part of the proof — provision it fresh (new DB, new checkout, truncate) or state explicitly that it was reset; (2) record the reset in the proof report ("truncated before the run") so the verifier can distinguish subject failures from pollution; (3) when a run fails, ask "was the environment clean?" before touching the subject — 10/14 that becomes 14/14 after a truncate is pollution, not a defect; (4) never "fix" the subject to accommodate dirty state — the fix belongs to the environment; (5) prefer fresh provisioning over reset where the cost is acceptable — a `--keep`/disposable DB is cleaner than remembering to truncate. Family note: SN-059's sibling — there, blame was assigned to the change before a clean-main control run exonerated it; here, blame was assigned to the proof before a clean-environment run exonerated it. Same doctrine: attribute the failure before you blame the artifact.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "proof_environment_pollution",
  "evidence": {
    "board": "#554 comment 5937882252 (2026-10-01T18:28:10Z) — P6 producer proof: database naya_isolated_rt polluted by prior runs (5 leftover rows) caused 4 false failures on first attempt (10/14); after truncate, 14/14 on the identical frozen specimen c5402f3f"
  },
  "rule": [
    "the environment is part of the proof — reset (truncate/recreate/provision fresh) before qualification, never reuse dirty",
    "record the reset in the proof report so the verifier can distinguish subject failure from pollution",
    "on a failing run, check environment cleanliness before touching the subject",
    "never fix the subject to accommodate dirty state",
    "prefer fresh provisioning (disposable DB/checkout) over remembering to reset"
  ],
  "lesson_line": "Proof environments must be reset, not reused. Prior-run pollution produces failures that look like proof failures — truncate first, then judge."
}
~~~
