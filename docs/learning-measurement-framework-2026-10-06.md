# Learning Measurement Framework: From Captured to Learned

**Status:** CANDIDATE (not ratified — only Shawn ratifies)
**Date:** 2026-10-06
**Author:** Naya 4 (learning measurement spec)
**Goal:** learning-10-10 (LEARNING 5.0 → 10/10)

---

## 1. The Problem Shawn Named

> "You can do 45 smart notes but if we don't learn from them it has no value."

We currently measure **capture** (notes filed). We do not measure **learning** (behavior changed because of those notes). A system that files 45 notes and changes zero behaviors has a Learning Yield of 0% — regardless of how impressive the capture pipeline looks.

**This spec defines the metric that distinguishes captured from learned, the ladder from 5.0 to 10.0 with falsifiable criteria per rung, and the instrumentation required to measure each rung.**

---

## 2. The Key Metric: Learning Yield

### 2.1 Definition

**Learning Yield** = (notes with proven behavioral delta) / (notes captured)

A note counts as "learned" (numerator) iff ALL of the following hold:

1. **Retrieved through the normal path.** A later agent pulled the note's intelligence through the standard retrieval mechanism (LEARN brief template, brain index, or other production retrieval path) — not hand-fed by the experimenter.
2. **Measured behavioral delta.** On a hard transfer task (novel scenario, not a restatement), the treatment agent (with retrieved intelligence) performed measurably better than a control agent (without it) on pre-registered metrics.
3. **Independently verified.** A second seat (not the builder) re-scored the transcripts and corroborated the delta.
4. **No negative transfer.** On an unrelated task, the treatment agent did not perform worse than control (the lesson didn't cause harm elsewhere).

### 2.2 Why this metric

- **Falsifiable.** If treatment ≤ control, the note was captured but not learned. No vibes.
- **Distinguishes the two things Shawn cares about.** Capture rate measures the pipeline. Learning Yield measures the outcome.
- **Prevents gaming.** You cannot inflate Learning Yield by filing more notes (that increases the denominator). You can only raise it by proving behavioral change.
- **Ceiling-effect resistant.** If the task is too easy (both arms score 100%), the delta is undefined — the trial is discarded, not counted as "learned." (This is what happened in Experiment 01: 5/5 vs 4/5 with ceiling effects → delta NOT proven → still 5.0.)

### 2.3 Supporting metrics

| Metric | Definition | Purpose |
|--------|-----------|---------|
| **Capture Rate** | notes filed / significant experiences | Measures pipeline health (we're good here) |
| **Retrieval Rate** | notes retrieved via normal path / notes filed | Measures whether intelligence reaches agents |
| **Transfer Delta** | treatment score − control score (per trial) | Measures whether retrieved intelligence changes behavior |
| **Compounding Slope** | cycle N+1 floor − cycle N floor | Measures whether learning accumulates |
| **Negative Transfer Rate** | trials where treatment < control on unrelated tasks / total NT trials | Safety: lessons must not cause harm |

---

## 3. The Ladder: 5.0 → 10.0

Each rung has a **criterion** (what must be true), a **falsifier** (what would prove it's NOT met), and the **evidence required**.

### 5.0 — CAPTURE MACHINERY WORKS (current)

**Criterion:** Notes flow from experience into durable storage (learn/*.md + brief template) via an operational pipeline. Authority-touching notes are flagged, not auto-integrated.

**Evidence (already have):** LEARN ingestion loop operational; 45 notes captured 2026-10-06; Experiment 01 proved the pipeline runs end-to-end (note → block → retrieval → trial).

**Falsifier:** If notes stop flowing or the pipeline breaks, we fall below 5.0.

**Why we're stuck here:** Experiment 01's behavioral delta was NOT proven (ceiling effects, 5/5 vs 4/5, n too small). The machinery runs; the learning isn't measured yet.

---

### 6.0 — RETRIEVAL PROVEN

**Criterion:** Later agents retrieve note intelligence through the **normal production path** (not hand-fed by experimenters) and the retrieval is logged with receipts.

**Falsifiable test:** Take 10 notes captured ≥7 days ago. For each, spawn a fresh agent with a task related to the note's domain, giving it ONLY the standard brief template (no hand-fed lesson). Log whether the agent's transcript shows it accessed and used the note's intelligence.

**Pass threshold:** ≥7/10 agents retrieve and reference the relevant intelligence through the normal path.

**Falsifier:** If agents need the lesson hand-fed in the prompt to use it, retrieval is NOT proven — we're still at 5.0. Hand-feeding is capture, not retrieval.

**Instrumentation needed:**
- Retrieval path logging: every brief-template injection logged with note IDs
- Transcript scanner: detects whether agent referenced retrieved intelligence
- Receipt per retrieval: {agent_id, note_id, retrieval_path, timestamp, task_domain}

**What proves 5.0 → 6.0:** 10 logged retrievals through the normal path, ≥7 showing the agent used the intelligence, all with receipts. No hand-feeding.

---

### 7.0 — SINGLE-LESSON BEHAVIORAL DELTA PROVEN

**Criterion:** For at least ONE lesson, control/treatment trials on a **hard transfer task** (no ceiling effects) show treatment > control with independent verification.

**Falsifiable test (Round 2 protocol):**
- Hard transfer tasks: novel scenarios where baseline (control) accuracy is 40–70% (not 80%+ — ceiling effects invalidate)
- Power tier chosen at pre-registration (see Power Tier Table); minimum n = 10/arm
- Pre-registered metrics: ONE primary metric (accuracy, diagnostic order, OR cost — chosen before trials run); the rest are secondary/exploratory
- Pre-registered hypotheses before trials run
- Independent verifier re-scores all transcripts from scratch
- Negative-transfer control: treatment must not degrade on unrelated task

**Power Tier Table** (all tiers: two-sided α = 0.05, power ≥ 80% at the stated minimum d):

| Tier | n per arm | Minimum Cohen's d | Use when |
|------|-----------|-------------------|----------|
| S | 10 | 1.4 (large) | Fast signal check; only large effects count |
| M | 25 | 0.85 (large-medium) | Balanced cost |
| L | 64 | 0.5 (medium) | Full proof; the original d ≥ 0.5 bar, properly powered |

Why tiers: the original bar (n ≥ 10, p < 0.05, d ≥ 0.5) has ~18% power at its minimum n — an honest trial fails 4 times out of 5 even when the effect is real. A bar that cannot detect what it demands is not a high bar; it is a broken ruler. Tiers keep full falsifiability (tier pre-registered, decision rule fixed) while making each rung actually passable.

**Pass threshold (all on the PRIMARY metric):**
- Treatment > control with two-sided p < 0.05
- Observed Cohen's d ≥ the pre-registered tier's minimum
- Bayesian corroboration: P(treatment > control | data) ≥ 0.95 (weakly informative prior, e.g. Cauchy(0, 0.707) on d — pre-registered)
- Negative transfer: no statistically significant degradation on the unrelated task (reported with 95% CI; descriptive — the control is a guardrail, not a powered test)
- Independent verifier corroborates all numbers from raw transcripts

**Multiplicity rule:** secondary metrics are reported but cannot pass the bar. If a secondary metric is promoted to a claim, Holm correction applies across all examined metrics.

**Falsifier:** If treatment ≤ control on the primary metric, or observed d < tier minimum, or the verifier disagrees, or ceiling effects make the delta undefined — delta NOT proven, still at 6.0.

**Instrumentation needed:**
- Trial harness (exists: experiment-01 protocol, needs hardening for n=10+, harder tasks)
- Pre-registration log (hypotheses locked before trials)
- Blind trial runner (agents don't know they're in an experiment)
- Independent scoring pipeline (second seat re-scores from raw transcripts)
- Receipt per trial: {brief, transcript, scores, timestamps, verifier_id}

**What proves 6.0 → 7.0:** One lesson with statistically significant treatment > control on a hard task, independently verified, no negative transfer. Published receipt.

---

### 8.0 — MULTI-LESSON TRANSFER PROVEN

**Criterion:** Behavioral deltas **replicate** across ≥3 different lessons and ≥3 different transfer task families.

**Falsifiable test:** Run the Round 2 protocol independently for 3 lessons from different domains (e.g., verification-methods, safety-gates, retrieval-patterns). Each must independently meet the 7.0 bar.

**Pass threshold:** ≥3 lessons each meet the 7.0 bar at their pre-registered tier, with independent verification and no negative transfer.

**Falsifier:** If deltas replicate for 1–2 lessons but not the third, or if any lesson shows negative transfer — we're at 7.0, not 8.0. One swallow doesn't make a summer.

**Instrumentation needed:**
- Lesson registry: tracks which lessons have been tested, with links to receipts
- Task family library: ≥3 distinct hard transfer task families with validated baselines
- Cross-lesson dashboard: Learning Yield = lessons with proven delta / lessons tested

**What proves 7.0 → 8.0:** 3 lessons × 3 task families, all meeting the 7.0 bar independently. Learning Yield > 0 with n ≥ 3.

---

### 9.0 — COMPOUNDING LOOP CLOSED

**Criterion:** Improved behavior from cycle N is **captured as new intelligence**, retrieved in cycle N+1, and produces a **higher floor**.

**Falsifiable test (the compounding experiment):**
1. Cycle N: treatment agent learns lesson L, performs at level X on task family F
2. The agent's improved approach is captured as new note L2 (with provenance: derived from L)
3. Cycle N+1: fresh treatment agent receives L + L2, fresh control receives nothing
4. Measure: does cycle N+1 treatment beat cycle N treatment on a harder variant of F?

**Pass threshold:**
- Cycle N+1 treatment accuracy > cycle N treatment accuracy (the floor rose)
- L2's provenance chain is machine-verifiable (L2 derived from L's application, not just restated)
- Independent verifier confirms both cycles

**Falsifier:** If cycle N+1 ≤ cycle N, the loop didn't compound — we're at 8.0. Capturing L2 without a measured floor increase is documentation, not compounding.

**Instrumentation needed:**
- Provenance tracker: every derived note links to its parent lesson + the trial receipt that produced it
- Cycle comparator: stores per-cycle floors per task family, computes slope
- Compounding receipt: {cycle_N_receipt, L2_note_id, cycle_N+1_receipt, floor_delta, verifier_id}

**What proves 8.0 → 9.0:** One complete compounding cycle with measured floor increase, provenance-verified, independently confirmed.

---

### 10.0 — AUTONOMOUS COMPOUNDING

**Criterion:** The system runs the **full loop without human orchestration**: captures → retrieves → applies → verifies → compounds, across **multiple consecutive cycles** with **rising floors**.

**Falsifiable test:**
- 3 consecutive compounding cycles (N, N+1, N+2), each meeting the 9.0 bar
- Zero human intervention in trial design, execution, or scoring (humans only set the initial protocol and verify the final receipts)
- Floors rise monotonically: floor(N) < floor(N+1) < floor(N+2)
- All receipts independently verified by a different seat each cycle

**Pass threshold:**
- 3 consecutive cycles, each with positive floor delta
- No human touched the trial pipeline between cycles
- Learning Yield trending upward across cycles

**Falsifier:** If any cycle needs human rescue, or if floors plateau/decline, or if verification finds a gap — we're at 9.0, not 10.0. Autonomy is the bar.

**Instrumentation needed:**
- Autonomous orchestrator: schedules cycles, spawns trials, collects receipts without human triggers
- Floor tracker: time series of per-family floors across cycles
- Human-touch detector: logs every human intervention; any intervention during the 3-cycle window disqualifies
- Final verification: independent seat audits the entire 3-cycle chain

**What proves 9.0 → 10.0:** 3 autonomous cycles, rising floors, zero human intervention, all independently verified. This is Shawn's "she learns from everything put into her" — proven, not claimed.

---

## 4. Instrumentation Summary

| Rung | New instrumentation required | Builds on |
|------|------------------------------|-----------|
| 6.0 | Retrieval path logging, transcript scanner, retrieval receipts | Existing brief template |
| 7.0 | Power-tiered trial harness (S/M/L tiers, hard tasks), pre-registration log, blind runner, independent scoring pipeline | Experiment-01 protocol |
| 8.0 | Lesson registry, task family library (≥3), cross-lesson dashboard | 7.0 harness × 3 |
| 9.0 | Provenance tracker, cycle comparator, compounding receipts | 8.0 results |
| 10.0 | Autonomous orchestrator, floor time-series tracker, human-touch detector | 9.0 pipeline |

**Estimated build order:** 6.0 instrumentation is the immediate next step (retrieval logging). 7.0 hardens what exists. 8.0–10.0 are extensions, not rebuilds.

---

## 5. What Moves Us From 5.0 to 6.0 (Immediate)

**The single next action:** Instrument the retrieval path.

Right now, we cannot answer the question: "When a fresh agent gets the standard brief, does it actually pull and use the relevant Smart Note intelligence?" We hand-fed lessons in Experiment 01. That's capture, not retrieval.

**Concrete steps:**
1. Add logging to the LEARN brief template injection: every time a note's intelligence is included in a brief, log {note_id, agent_id, timestamp, injection_context}.
2. Build a transcript scanner: after an agent completes a task, scan for references to retrieved intelligence (quotes, paraphrases, applied principles).
3. Run 10 fresh agents on note-relevant tasks with ONLY the standard brief. Count how many retrieve and use the intelligence.
4. If ≥7/10: 6.0 proven. If not: we know exactly where the retrieval chain breaks, and that's the next fix.

**No new notes needed.** No new trials needed. Just: does the existing machinery actually deliver intelligence to agents through the normal path?

---

## 6. Anti-Gaming Rules

1. **Hand-feeding disqualifies.** If the lesson is in the prompt (not retrieved), the trial doesn't count toward any rung.
2. **Ceiling effects invalidate.** If control scores ≥80%, the task is too easy — discard, don't count as "learned."
3. **Small-n doesn't prove.** n < 10 per arm is a pilot, not proof. Pilots inform design; they don't move scores. n ≥ 10 is the Tier S minimum and the tier's minimum d applies. Choosing or changing the tier after seeing data disqualifies the trial.
4. **Builder doesn't self-verify.** Every delta must be corroborated by a different seat from raw transcripts.
5. **Filing more notes can't raise Learning Yield.** The denominator grows with capture; only proven deltas grow the numerator.
6. **A rung is not met until the falsifier has been tested.** "We didn't find a problem" is not "we proved there's no problem." Each rung's falsifier must be actively attempted.

---

## 7. Relation to Existing Work

- **Experiment 01** (SN-0356): Proved the pipeline runs end-to-end. Did NOT prove behavioral delta (ceiling effects). This is the 5.0 → 7.0 pilot that showed us what Round 2 needs.
- **Experiment 02** (in progress): Second source rule — contributes to the task family library for 8.0.
- **SN-0418 trials**: Showed the scenario-too-easy failure mode. Directly motivates the "hard transfer task" requirement (control baseline 40–70%).
- **GOAL.md 6-stage chain**: This spec operationalizes stages 3–6 (retrieval → behavior change → verification → compounding) with falsifiable criteria. Stages 1–2 (capture → block) are the 5.0 we already have.

---

**Bottom line for Shawn:** We file 45 notes (capture). We prove ~0 notes changed behavior (learning). The Learning Yield is the number that matters. This spec defines exactly how we measure it, what each rung requires, and what we build next. The immediate move: instrument retrieval (6.0). No new notes, no new theories — just measure whether the intelligence we already captured actually reaches agents through the normal path.
