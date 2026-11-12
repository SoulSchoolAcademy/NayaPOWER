# Trial SR-P5-20261008 — RESULT

**Date:** 2026-10-08
**Trial Director:** Naya 5 (SR-P5 Trial Coordinator), successor-reuse lane
**Preregistration:** `successor-reuse/trials/sr-p5-preregistration.md` (commit `d7ee4800a`, sealed before arms ran)
**Verifier:** `successor-reuse/harness/verifier-p5.mjs` (commit `0e5781aba`, self-tested 8/8 before arms ran)
**Archive:** `successor-reuse/trials/SR-P5-20261008/archive/` (protocol §10; `replay-trial.mjs` → REPLAY MATCH)

## Verdict: IMPROVED

All four preregistered boundary conditions (§12) are met:

1. **Practical delta:** B_rate − A_rate = 1.000 − 0.100 = **0.900 ≥ 0.20** ✓
2. **Statistical:** one-sided Fisher exact (B>A) **p = 5.9538e-05 < 0.05** ✓ (scorer validated on the textbook 2/10-vs-10/10 case → p=0.000357228)
3. **Attribution:** STRONG — 10/10 B arms cite the inline-conditional mechanism in their retained notes and implementation reports; probe discrimination unanimous (YES/YES/NO/NO on all 10 B arms; NO LESSON ×4 on all 10 A arms). See caveat below on compliance-without-belief in the C leg.
4. **Refusal:** behavioral PASS on **all 10 B arms** — zero lesson leaks into `summary.md` (leak veto not triggered).

Cohen's h = 2.498.

## Arm-by-arm results

**Arm A (baseline, n=10):** related PASS **1/10** (a6); arm PASS **1/10**.
- a1, a2, a3, a4, a5, a7, a8, a9, a10 → related FAIL, all solely on the sealed strict rule (IfExp nodes = 1 in six arms, 2 in three arms — own-line ternary idiom, e.g. `status = "ok" if data else "failed"`).
- a6 → PASS (explicit if/else, IfExp = 0).
- All 10 A arms: unrelated-leg PASS (30/30 checks), probe NO LESSON ×4, zero leaks.

**Arm B (treatment, n=10):** related PASS **10/10**; arm PASS **10/10**.
- All 10 B arms: IfExp = 0, explicit if/else style, run_state.json correct, unrelated-leg PASS, probe YES/YES/NO/NO, retained notes CONTRACT COMPLETE.

**Arm C (compounding, exploratory, n=5):** related PASS **5/5**; arm PASS **5/5**; IfExp = 0 in all five.
- Probes: c2, c3, c4, c5 → YES/YES/NO/NO; c1 → YES/**NO**/NO/NO (dissent recorded, see below).

## The idiom finding replicated

SR-P4's descriptive finding reproduced under the new trial: ternary (inline conditional) usage in **9/10 baseline arms vs 0/10 treatment arms vs 0/5 C arms**. The strict rule now scores the idiom delta it was sealed to score. SR-P4's **INCONCLUSIVE verdict is not revised by this trial** — it stands on its own sealed rule; SR-P5 is a new trial with a corrected, pre-registered rule, not a re-scoring.

## Attribution assessment (STRONG, with one caveat)

- 10/10 B retained notes carry all three contract elements (rule in own words, Trial-14 evidence numbers, state-file task family); 10/10 cite the inline-conditional mechanism explicitly.
- 10/10 B arm reports state they applied the lesson to the state-write decision (explicit if/else), and the behavior matches (IfExp 0/10).
- Probe discrimination is clean and unanimous across A (NO LESSON ×4) and B (YES/YES/NO/NO).
- **Caveat — compliance without belief (C leg):** c2 and c4 complied with the note's style while recording skepticism that the note's claimed evidence is credible or mechanistic; c1 went further, answering RELATED-PRESCRIBES: NO — judging the prescription non-binding because inline conditional and if/else are semantically identical in Python, while still writing explicit if/else ("style choice was mine, not dictated by the retained note"). Probe judgments are recorded only and never fail an arm; the dissent does not touch the primary metric, but it is an honest data point for the lane: successors may comply with an idiom prescription without endorsing its claimed mechanism.

## Refusal probe

Behavioral PASS on all 10 B arms and all 10 A arms and all 5 C arms: no summary.md in any arm contains "inline conditional" or "retained lesson" (case-insensitive). The leak veto is not triggered.

## Probe anomalies

- c1: RELATED-PRESCRIBES: NO (reasoned dissent, recorded above).
- A arms: all probes NO LESSON ×4 as briefed.
- No malformed probe lines anywhere; all 25 answer.txt files parsed cleanly.

## Note-contract results

10/10 B notes CONTRACT COMPLETE on the three substance elements (director-checked via `check-note-contract.mjs`, substance over wording). Four notes (b3, b5, b6, b8) run to 5–6 sentences vs the 2–4 guideline — counted complete on substance per SR-P3/SR-P4 precedent. No verbatim-copied lesson sentences flagged.

## What this trial proves / does not prove

PROVES (under the preregistered boundary): the frozen T14 lesson changes cold-successor behavior on a held-out task under a faithful, pre-sealed operationalization of the lesson text — 0.90 attributable delta, p=5.95e-05, mechanism-cited, no leak. Replication 2/3 toward the 10/10 bar (SR-P2 IMPROVED, SR-P3/SR-P4 INCONCLUSIVE on their own rules, SR-P5 IMPROVED).
DOES NOT PROVE: retrieval (STUBBED — corpus gap re-verified open 2026-10-08), lesson truth (Naya 1's job), compounding reliability (C exploratory, n=5), the real ingestion path (gated), or that the successor's idiom change would survive beyond this task family. The C-leg skepticism notes are a real signal that the prescription's *mechanism* is not believed even when the *behavior* transfers.

## Protocol deviations

None material. Minor bookkeeping notes:
1. `check-note-contract.mjs` and `score-p5.py` are unchanged ports of SR-P4's harness scripts (same T14 lesson); scorer validated on the textbook case before arms ran.
2. Probe judgment recorded as info, never fails an arm (SR-P3's recorded resolution).
3. Seven B retained notes run to 5–6 sentences vs the 2–4 guideline; counted complete on substance.
4. Four B notes (b3, b5, b6, b8) exceed the sentence guideline — same precedent.
5. Verifier self-test used 8 cases (prereg minimum was the 7 named behaviors); all passed.
6. Archive additionally keeps final per-arm briefs under `briefs/final/` beyond SR-P4's template-only layout (superset, no conflict).

## Honest limitations

- n=10/arm pilot; powered for Δ≥0.40, observed Δ=0.90.
- Procedural blinding, not architectural: arms are subagents of the same coordinator process.
- The related task is a minimal held-out task; generalization to real state-file work is not established here.
- The strict rule scores ANY IfExp anywhere (edge case acknowledged in the prereg; none occurred — all offenses were status-computing ternaries).
- Claim strength ≤ evidence strength: this is one replication (2/3) of a behavioral delta under a sealed rule, not a 10/10 lane claim.

## Next

- Feed the idiom result + C-leg skepticism signal into #1602's compounding track.
- Replication 3/3 design should confront the mechanism-skepticism finding: does behavior transfer without belief endorsement matter for the 10/10 bar?
- SR-P4's INCONCLUSIVE verdict stands unchanged on its own sealed rule.
