# Trial SR-P3-20261008 — RESULT

**Date:** 2026-10-08
**Trial Director:** Naya 5 (SR-P3 Trial Coordinator subagent), successor-reuse lane
**Preregistration:** `successor-reuse/trials/sr-p3-preregistration.md` (commit `f5dc72803`, sealed before any arm ran)
**Lesson:** T14 `66122e1e-677b-4ef0-a765-80d08ccfa85b` — "Never write state files through inline conditional expressions." Handoff SHA-256 verified before B arms ran: `b35914a04ee77f2c323882c80cfb4bbd3838013d828d0ce8a95a9fe564a93b5d` (reconstructed byte sequence matched on the first candidate family; variant recorded in archive).
**Verifier:** `successor-reuse/harness/verifier-p3.mjs` (commit `5f0b866eb`; self-tested 7/7 before arms ran)
**Archive:** `successor-reuse/trials/SR-P3-20261008/archive/` — `replay-trial.mjs` returns **REPLAY MATCH** (all 25 verdicts reproduced).

## Headline

**Verdict: INCONCLUSIVE (ceiling effect)** — not IMPROVED, not NO_DELTA, not REGRESSED.

The behavioral instrument could not discriminate: the baseline arm passed at 10/10, so no lesson-driven delta was observable. The lesson's failure mode (ternary inside the state-write path) never occurred in any arm, treated or not.

## The four numbers

| Arm | Related-task behavioral PASS | Rate |
|-----|------------------------------|------|
| A (baseline, n=10) | 10/10 | 1.00 |
| B (treatment, n=10) | 10/10 | 1.00 |
| C (compounding, n=5) | 5/5 | 1.00 (descriptive) |

- **A_rate = 1.00, B_rate = 1.00, Δ = +0.00**
- **One-sided Fisher exact p (B>A) = 1.0** (method: `successor-reuse/harness/score-p3.py`, hypergeometric tail via `math.comb`; validated on the 2/10-vs-10/10 case → p=0.000357, matching the textbook value)
- **Cohen's h = 0.000**
- Prereg boundary (1) Δ≥0.20: **NO**. Boundary (2) p<0.05: **NO**. → IMPROVED fails on (1) and (2).

## Per-arm verdicts (all 25, one run each, no reruns)

- arm-a1…arm-a10: **PASS** (all four legs green; IfExp count 0 in every checkpoint.py)
- arm-b1…arm-b10: **PASS** (all four legs green; no lesson leak into any summary.md)
- arm-c1…arm-c5: **PASS** (all four legs green)

Full verifier stdout per arm: `archive/verifier-stdout/arm-<k><i>.txt`. File hashes pinned in `archive/manifest.json`.

## Attribution

- **Mechanism evidence: STRONG-capable.** 10/10 B retained notes cite the inline-conditional/ternary mechanism in the arm's own words (not just statistics); all B arms' probe judgments were RELATED-RELEVANT: YES / RELATED-PRESCRIBES: YES.
- **Refusal probe: PASS on all 10 B arms** — zero lesson leaks into `summary.md` (case-insensitive check for "inline conditional" / "retained lesson"). No veto.
- Per the prereg boundary, attribution does not rescue a verdict that fails (1) and (2): STRONG mechanism citation is recorded, but the trial cannot attribute an improvement that was never observed.

## Probe judgments (recorded separately per prereg; do not fail arms)

- All 10 A arms: `RELATED-RELEVANT: NO LESSON / RELATED-PRESCRIBES: NO LESSON / UNRELATED-RELEVANT: NO LESSON / UNRELATED-PRESCRIBES: NO LESSON` (exactly as briefed).
- All 10 B arms: `RELATED-RELEVANT: YES / RELATED-PRESCRIBES: YES / UNRELATED-RELEVANT: NO / UNRELATED-PRESCRIBES: NO` — matches the treatment expectation perfectly; the RELEVANT-vs-PRESCRIBES split (SR-P2 instrument refinement) behaved identically across all arms.
- All 5 C arms: same YES/YES/NO/NO pattern.
- **Probe-judgment anomalies: zero.** No malformed lines, no judgment errors, no disagreements between judgment and behavior.

## Retained-note contract (SR-P2 C-leg refinement)

All 10 B notes verified against the 3-element contract by the director (`successor-reuse/harness/check-note-contract.mjs` + manual read):
- (a) rule in own words: 10/10 (zero verbatim copies of the lesson sentence)
- (b) outcome evidence numbers: 10/10 (b9 spells them "10 out of 10 / 2 out of 10 / p=0.0007" — counted complete by substance, deviation recorded in manifest)
- (c) task family (state-file writing): 10/10
- C-leg selection: `shuf -n 1` over the 10 complete notes → **arm-b10** (output recorded in `archive/shuf-selection.txt`). b10's note: "…do not route the write through inline conditional (ternary) expressions that pick the file, the payload, or whether the write happens… control 2/10 vs treatment 10/10, p=0.0007… state-file writing task family, including job-runner checkpoint scripts like checkpoint.py."

## Interpretation: why INCONCLUSIVE, not NO_DELTA

The honest reading is a **ceiling effect**, and it is an instrument failure, not evidence against the lesson:

1. The task handed arms the success value as a literal: "whether it succeeded (True)". No conditional value ever needed computing, so the natural Python idiom never tempted a ternary — 0 IfExp nodes across all 10 baseline scripts.
2. Trial-14's control was 2/10 because its task evidently required a genuinely conditional value (the condition had to be *decided* in code). SR-P3's operationalization removed the decision point, and with it the failure mode the lesson guards.
3. With both arms at ceiling, Δ is unmeasurable. Calling this NO_DELTA would assert "the lesson makes no difference," which the trial cannot establish — there was no room to observe a difference. Per the prereg ("If the true effect is smaller, the honest verdict is INCONCLUSIVE, not failure"), the ceiling case is INCONCLUSIVE a fortiori.

**Design lesson for the next replication (SR-P4):** the related task must include a genuinely conditional value — e.g., "whether it succeeded, determined by checking that the input file is non-empty" — so the baseline's natural idiom is a ternary inside the write path. Re-running THIS task with any tweak would be significance-chasing; the fix belongs in a new preregistration with a discriminating instrument.

## What this trial proves / does not prove

**PROVES:**
- The sealed-prereg → self-tested-verifier → isolated-arms → pinned-archive → REPLAY MATCH pipeline works end to end for a 25-arm trial (second consecutive clean replay after SR-P2).
- The refusal probe is robust: 10/10 treatment arms kept the lesson out of the unrelated prose domain, with perfect YES/YES/NO/NO probe calibration.
- B arms can reproduce the lesson's mechanism in their own words with outcome evidence intact (10/10 contract-complete notes; C leg received a valid evidence-bearing note).
- A negative instrument finding, honestly reported: this operationalization of the T14 lesson cannot discriminate. That is now a recorded design constraint for the lane.

**DOES NOT PROVE:**
- Anything about the lesson's behavioral value (unmeasured — ceiling).
- That retrieval works (STUBBED by design; corpus gap unchanged).
- That compounding is reliable (C is exploratory; here it measured nothing new).
- Any movement toward the 10/10 "≥3 distinct lessons" bar: this replication attempt does not count as 2/3. The count stands at 1/3 (SR-P2).

## Verifier interpretation notes (per prereg: follow the letter, record interpretation)

1. The IfExp check walks each `IfExp` up to its **enclosing statement** and fails only if that statement's subtree references `run_state` (string constant containing it, or Name id containing it). This implements the prereg's rationale literally: "computing a value on its own line and then writing it plainly is compliant."
2. Consequence of the letter: a script that computes the dict with ternaries but writes via a separate plain `json.dump(state, open("run_state.json","w"))` statement **passes** (the IfExp's enclosing statement does not reference run_state). In this trial no arm used any IfExp at all, so the distinction was not exercised.
3. Probe judgment is recorded but never fails an arm (prereg §Probe judgment overrides §Unrelated PASS on this point — followed the later, more specific section).

## Protocol deviations (also in archive/manifest.json)

1. Arm c4's first spawn carried a corrupted Task-1 sentence (coordinator transcription slip); closed pre-init, respawned with the byte-identical brief. No arm ran twice; Task 1+2 byte-identity asserted programmatically across all 25 final briefs.
2. b9's note spells evidence as "10 out of 10 / 2 out of 10" — counted complete by substance.
3. c4's first verification read was premature (agent still writing); final submission verified after completion: PASS. One run, not a rerun.
4. `tools/successor/score-trial.py` (named in prereg) does not exist in this worktree; scoring done with `successor-reuse/harness/score-p3.py` (validated).

## Limitations (honest)

- Procedural blinding, not architectural: arms inherit model context; the tested asymmetry is direction-to-lesson vs no direction.
- n=10/arm is pilot tier; powered for Δ≥0.40 — irrelevant here given the ceiling.
- STUBBED retrieval: this trial says nothing about the real retrieval path.
- The coordinator (this agent) knew all outcomes before C selection — selection was mechanical (`shuf`), but the ceiling was visible before C arms ran. C was exploratory per prereg and is reported descriptively; no inference is drawn from it.
- Verifier's IfExp rule is a proxy with the letter-of-prereg limitation noted above.

## Bottom line for the lane

SR-P3 is a **clean, replay-verified INCONCLUSIVE**: the instrument failed to discriminate (ceiling), the refusal probe and note-contract machinery worked perfectly, and the lane now has a recorded design rule for the next attempt — the related task must force a genuinely conditional value into the write path. Replication count toward the 10/10 bar stays at **1/3**.
