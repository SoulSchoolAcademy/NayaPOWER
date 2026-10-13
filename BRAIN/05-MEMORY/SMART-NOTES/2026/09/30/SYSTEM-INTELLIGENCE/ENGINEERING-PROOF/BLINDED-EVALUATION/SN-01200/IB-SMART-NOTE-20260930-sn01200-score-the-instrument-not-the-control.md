# Score the Instrument, Not the Control — The Stripped Run First, or Echo Wears the PASS Badge

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01200-score-the-instrument-not-the-control
**Smart Note:** SN-01200
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-13, Lane 2 dry-fired each brief in two forms — full and stripped (picks blocks removed). P3 ("Independent eyes…") ranked top-5 in 3/3 full runs and 0/3 stripped: the picks blocks name P3's title verbatim, so the judge "scored it right" by echoing the brief's own words back. Auto-right 0/3. The seat nearly scored 3/3 auto-right on first reading — the stripped runs falsified that reading. The principle: **the stripped run is the instrument and the full run is the control — score the instrument, not the control.** Always run the no-echo baseline FIRST; judge auto-right against it, never against the full-brief run.

## HUMAN NOTE

An LLM judge grading briefs that contain their own answer key is not a judge — it's a mirror. The mechanics:

1. **Strip first, judge second.** Remove the picks blocks / titles / any text the brief carries about its own verdicts, then judge. That stripped score is the instrument's real reading.
2. **The full run is the control.** Running the full brief afterwards tells you how much the judge leans on echo, not how right it is. Echo demonstrated = contamination measured, not capability proven.
3. **The t0637 lesson carries over.** The t0637 stability baseline does NOT generalize: the production path is clean by construction precisely because the picks-exclusion is load-bearing. A baseline that works on leaky queries and fails on clean ones is measuring the leak.

"Reinforcement is the null hypothesis wearing a PASS badge." A lesson that only scores well when its own titles are echoed back is not reinforced — it is repeated.

## CHILD NOTE

If the answer is written inside the question, anyone can "get it right" just by reading aloud. To really test what someone knows, cover the answers first, then ask. The version with the answers covered is the real test — the other one just checks reading.

## GRANDMA NOTE

Don't be fooled when someone looks smart repeating words that were already on the page. Check them with the hints removed. If they still know it, they know it; if not, it was never knowledge — it was echo.

## NAYA NOTE

For the decision machine this protects every auto-scored judgment we run on ourselves: lesson-injection auto-right, brief quality scoring, any LLM judge grading artifacts that name their own verdicts. Title-echo is the silent contaminant of self-grading — the judge sees the brief's own picks and "chooses correctly" by transcription. The no-echo baseline must come FIRST in every evaluation protocol: strip, score, then run full as the contamination control. Any bar that can be cleared by echo alone is a bar that measures nothing. Cousin: SN-01198 (sealed-probe blinding must fire before first-reads) — same contamination family, executor-side vs judge-side.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "rule": "score_the_instrument_not_the_control",
  "protocol": "stripped_run_first (no_echo_baseline), then_full_run_as_control",
  "failure_mode": "title_echo_contamination -> phantom_auto_right (3/3_full, 0/3_stripped)",
  "baselines_do_not_generalize": "t0637_stability_baseline_fails_on_leaky_queries; picks_exclusion_is_load_bearing",
  "cousin": "SN-01198_sealed_probe_blinding (executor-side contamination)",
  "master_nodes": ["VERIFY", "LEARN", "PROVE"]
}
~~~

## 🟡 WHAT IT MEANS

A judge that grades its own echoes is a mirror, not a judge. The stripped run is the instrument; the full run is the control. Baseline first, always.

## 🧾 PROOF / PROVENANCE

- Lane 2 (Naya Beta) t0642 receipt: `hidden_files/twelve-lane-receipts/t0642-lane2.md` — full-vs-stripped dry-fire; P3 top-5 in 3/3 full, 0/3 stripped; picks blocks name P3's title verbatim; auto-right 0/3.
- Verdict: `hidden_files/auto-retrieval/injection-proof-dryfire-t0642.md`
- F5: echo demonstrated on leaky queries; t0637 stability baseline does NOT generalize; production path clean by construction (picks-exclusion load-bearing).
- Distilled in: `hidden_files/learning-events-2026-10-13-09.md` (review ran 09:20 PDT).

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Covers the injection-proof dry-fire experiment (t0642). The "baseline first" rule is a candidate evaluation protocol for LLM judges, not yet RATIFIED; it has not yet been tested against judge architectures other than the brief-scoring path.
