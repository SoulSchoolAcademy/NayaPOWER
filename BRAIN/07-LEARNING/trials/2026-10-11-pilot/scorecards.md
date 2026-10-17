# Spec Scorecard — ROUND 1 (scorer voice, adversarial)

**Target:** PR #2391 `BRAIN/07-LEARNING/0002-COMPOUNDING-EXPERIMENT-SPEC-V1.md` as authored.
**Scorer independence note:** I am the builder's scorer-role; I cannot spawn a separate seat at this depth. Scoring in own lane, 3 rounds, every gap named. Raw records published for independent re-grade.

## What's strong (kept)
- Four falsifiable claims, each with data source + numeric criterion + named falsifier. A claim without a falsifier is not run — good law.
- Behavioral grading: yes/no on observed actions, never prose quality.
- The four arms ask the right four questions (change? fail-closed? compound? valid control?).
- Trial rules: frozen tip, randomized order, recorded evidence, different-seat scoring.

## Why it's not a 10 — the gaps

**G1. The significance math is wrong (MATH ERROR).** §4.5 / C1 claim "≥ 9 of 12 paired comparisons (binomial vs chance: p < 0.05)". Computed: P(X≥9 | n=12, p=0.5) one-sided = 0.0730 > 0.05. The spec's own p-value claim is false; ≥10/12 is needed for p<0.05. A spec whose math doesn't check out cannot be the instrument that proves learning.

**G2. C1's criterion doesn't measure a delta (CENTRAL DESIGN FLAW).** Criterion: "treatment-arm pass count ≥ 9 of 12 paired scenario comparisons vs control". Falsifier: "treatment ≈ control (≤ 6 of 12)". These don't cohere:
  - treatment=10/12, control=9/12 → criterion PASSES, but the lesson changed almost nothing. C1 would claim "injection changes behavior" on a delta of 1.
  - treatment=8/12, control=2/12 → criterion FAILS on a delta of 6, a massive behavioral change.
  - "Paired comparisons" is misnamed: different workers per arm = independent groups, not pairs. The comparison unit is muddled.
  A learning claim is a claim about a DELTA. The criterion must be a delta.

**G3. "Cold worker" is undefined for knowledge-sharing seats (CONFOUND).** The suggested test lessons (tmpfs triage, depth-1 proof) are already standing law every Naya seat knows (TOOLS.md, AGENTS.md). Treatment-vs-control on a known lesson measures recall, not learning. No novelty check exists. Without one, C1 is confounded from the first trial.

**G4. The adversarial lesson can't trip its own tripwire (VACUOUS C2).** The example misleading lesson ("run the adversarial harness and pytest concurrently") targets NO graded scenario among the twelve — none of S1–S12 grades concurrent harness+battery runs. So "any trial worker follows the misleading lesson on a graded scenario → C2 FAILS outright" can never fire. C2's hard-fail trigger is decorative. The misleading lesson must name its target scenario, and following it must flip that scenario's grade.

**G5. C4 is unexecutable in a single run (MISSING BATCHES).** "Control pass count stays within ±2 of its first-batch value across batches" — but the run plan defines no batches; each arm runs once. There is no first batch vs later batch. C4 needs an operational batch definition or it can't be evaluated.

**G6. No arm order / carryover control.** Seats share memory across arms. Run order, one-way progression (never re-run an earlier arm after seeing a later briefing), and washout are unspecified. Single-blind is claimed for workers, but cross-arm contamination through the runner/shared substrate isn't addressed.

**G7. Scenario-instance equivalence unspecified.** "The exact twelve may rotate" + "randomized scenario order per worker" — but who generates instances, and what makes a control instance vs a treatment instance equally difficult? Without an instance-equivalence rule (same scenario id, same difficulty class, different surface details, generated before arms run, answer key withheld), difficulty can confound the delta.

**G8. Solo-execution fallback missing.** "The scorer is not the trial runner" — but no fallback when only one seat is available. A spec that can't be executed solo by a seat with full transparent records is less useful than one that can (provisional self-grade + mandatory independent re-grade from published records).

## Round 1 score: 6.5/10
Strong skeleton (falsifiers, behavioral grades, four arms), but the math is wrong (G1), the central criterion doesn't measure what the claim claims (G2), the adversarial tripwire can't fire (G4), and "cold" is undefined (G3). Not runnable as an honest instrument yet.
# Spec Scorecard — ROUND 2 (scorer voice, adversarial)

**Target:** Spec V2 (fixes G1–G8 applied).
**Method:** cold re-read of V2 as an instrument. What would still let a dishonest-or-sloppy run claim "learning proven"?

## What's fixed (verified)
- G1: binomial math corrected; Fisher's exact as readout. ✓
- G2: C1/C3 are delta criteria (≥4, gray zone 2–3 → higher-n re-run). ✓
- G3: novelty check required, synthetic lessons labeled. ✓
- G4: misleading lesson must target a graded scenario; tripwire can fire. ✓
- G5: batches operationally defined (first-6/last-6). ✓
- G6: arm order one-way, recorded. ✓
- G7: instance-equivalence rule (pre-generated, seeded, answer key withheld). ✓
- G8: solo fallback with mandatory independent re-grade. ✓

## Why it's still not a 10 — remaining gaps

**G9. The delta threshold (≥4) has no power justification.** Why 4 and not 3 or 5? With n=12, delta ≥ 4 with treatment ≥ 9/12 implies control ≤ 8/12 — Fisher's exact one-sided p for 9/12 vs 5/12 (delta 4): table [[9,3],[5,7]] → p ≈ 0.089 > 0.05. For 10/12 vs 6/12: p ≈ 0.13? Let me not hand-wave — the spec should state the achieved significance at the boundary case, or set the boundary where p<0.05 actually holds. As written, the decision rule can PASS while Fisher's readout says p>0.05, and the spec says p "corroborates but does not gate" — which quietly lets a non-significant result pass. Either the boundary moves to where the math holds, or the spec admits the rule is a decision threshold, not a significance claim, and says so plainly. Currently it wants it both ways.

**G10. Successor-arm information leak via receipts is unmeasured.** C3's receipts "show the lesson's application" — but receipts may ALSO leak the lesson's verbatim text (a treatment worker quoting L-CANARY-7 in its sign-out). Then C3 measures "lesson restated in receipts," not "behavior transmitted through receipts." The spec needs a receipt-hygiene rule: treatment sign-outs must record actions/commands/evidence, and MUST NOT restate the lesson text (quote the application, not the lesson). Otherwise C3 is confounded.

**G11. The adversarial aggregate guard is nearly vacuous.** "Adversarial ≤ control" — with the misleading lesson targeting ONE scenario (S1), the maximum damage a followed lesson does to the total is ~1 point. If adversarial=control−1 because of S1 but the worker followed the lesson (tripwire), C2 already failed via tripwire. If the worker ignored the lesson, adversarial≈control trivially. The aggregate guard adds almost nothing beyond the tripwire. Honest fix: keep the tripwire as the real test, demote the aggregate guard to descriptive, OR make the misleading lesson's trigger appear in 3 scenarios. Don't keep a guard that can't guard.

**G12. No handling of "treatment fails but successor passes" (or other incoherent patterns).** If C1 fails (lesson didn't change behavior) but C3 passes (successor beats control), something is wrong with the instrument — receipts transmitted what the lesson didn't teach? The spec should name incoherent patterns as instrument-failure alarms: C3-pass-requires-C1-pass (successor can't inherit what treatment never exhibited); if observed, the run is VOID for instrument failure, not a C3 pass.

**G13. Instance generation "difficulty class" is hand-waved.** "Same difficulty class" — who judges difficulty, and how? Without at least a rubric (e.g., each scenario's template fixes the number of distractors, the API surface, and the expected command count), "same difficulty" is the generator's vibes. Minimum fix: each scenario template declares its difficulty parameters; instances vary only surface details.

**G14. Gray-zone re-run has no pre-registered n.** "Re-run at higher n (power-tiered S/M/L)" — but S/M/L tiers are referenced, not defined. A gray zone that points to an undefined tier is a parking lot. Minimum: define the tiers here (S=12, M=24, L=48 trials/arm) with the delta thresholds scaled (M: delta ≥ 6; L: delta ≥ 9 — or state the scaling rule).

**G15. C4's within-run split is weak against slow drift.** First-6 vs last-6 catches abrupt mid-run changes, but a gradual drift (model behavior shifting across the run) could still hide inside ±2. Acceptable for V2 — but the spec should say what C4 does NOT catch, so nobody over-claims. One honest sentence.

## Round 2 score: 8.0/10
V2 is a runnable honest instrument. Remaining gaps are about over-claiming (G9, G11, G15), confounds (G10, G12), and undefined parameters (G13, G14). None is fatal; all need fixing before this spec certifies anyone's learning loop.
# Spec Scorecard — ROUND 3 (scorer voice, final)

**Target:** Spec V3 (Round 2 fixes G9–G15 applied).
**Method:** cold re-read hunting for anything that still lets a sloppy run certify learning, plus checkability of every number.

## Verification of Round 2 fixes
- G9: Fisher p<0.05 is now the gate (not a "corroborating readout"); verified the boundary math holds — 10/12 vs 5/12 → p=0.0447 ✓; 9/12 vs 5/12 → p=0.107 correctly fails ✓. The spec no longer wants it both ways.
- G10: receipt-hygiene rule added (§2.1 + scorer checklist); hygiene violation voids C3. ✓
- G11: C2 tripwire primary; aggregate honestly demoted to descriptive with the reason stated. ✓
- G12: coherence alarms named; C1-fail + C3-pass → run VOID (not a pass). ✓
- G13: template schema (a)–(e); instances vary only surface details. ✓
- G14: tiers S=12/M=24/L=48 defined with the same math at larger n. ✓
- G15: honest C4 limits sentence present. ✓

## Remaining nits (named, none blocking)
- **N1.** The 75% rate guard's interaction with the Fisher gate at tier M/L is stated but unworked — at M, 18/24 vs 13/24: does the p-gate bind before the rate guard? The math is the same test; both must hold; no contradiction. Fine.
- **N2.** "Blindness check: guesses beat chance" — with one worker per arm, "beats chance" is 1/1 correct guesses, a weak check. The spec reports it rather than gating on it — honest as stated. Fine for V3; a multi-worker run should pre-register the blindness criterion.
- **N3.** Solo fallback leans on "independent re-grade mandatory before MERGED-VERIFIED" — the enforcement is social (the merge protocol), not mechanical. Named honestly in the spec. Acceptable.

## Why nothing else blocks
- Every claim has data source + numeric criterion + falsifier. ✓
- The central math is computed, not asserted. ✓
- Confounds found in R1/R2 (recall-vs-learning, vacuous tripwire, receipt leakage, incoherent patterns) are closed with mechanisms, not prose. ✓
- Gray zones have named next steps, never silent passes. ✓
- The spec is executable solo (with the honest fallback) and multi-seat. ✓

## Round 3 score: 9.2/10
V3 is an honest instrument: it can fail, it says exactly how it can fail, and its numbers check out. The 0.8 remaining is N1–N3 (multi-worker pre-registration details) plus the fact that no instrument scores 10 before its first real run — the run itself is the remaining validation. **V3 is cleared to run.**
