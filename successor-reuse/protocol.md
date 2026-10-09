# SUCCESSOR REUSE — Trial Protocol v1

**Lane:** SUCCESSOR REUSE (final acceptance test of NayaPOWER)
**Status:** DRAFT v1 — 2026-10-06
**Authority:** Director's 10/10 definition; Scorecard Law; exact state language.

## 1. What 10/10 means

A COLD successor Naya — no prior conversation context, no memory of the lesson,
nothing rebuilt by Shawn — does MEASURABLY better work on a real task because a
prior lesson was captured → retrieved → applied → independently verified →
learned → inherited.

Measured, not asserted. Every trial preregisters: the task, the lesson, the
baseline, the treatment, the metric, and the success boundary — BEFORE any arm runs.

## 2. Roles

| Role | Who | Sees |
|---|---|---|
| Trial Director | SUCCESSOR REUSE seat (me) | Everything. Preregisters, runs arms, anonymizes, reports. Never scores unblinded. |
| Cold Agent B (baseline) | Fresh subagent, no inherited context | Task brief ONLY. No lesson, no retrieval, no hints. |
| Cold Agent T (treatment) | Fresh subagent, no inherited context | Task brief + lesson via the retrieval path under test. |
| Independent Verifier | Deterministic script where possible; otherwise a different agent than the arms | Anonymized outputs (Arm A / Arm B, randomized). Never knows which arm is which. |

## 3. Preregistration (required before any arm runs)

- Trial ID + date
- The lesson: source, ID, exact text
- The task: the EXACT brief given to both arms (byte-identical except the lesson handoff)
- Primary metric + secondary metrics
- Success boundary (e.g. "treatment first-attempt pass rate ≥ baseline + 1 success in N trials")
- What is STUBBED (capture? retrieval? lesson provenance?) — stubs are rehearsal-only, never proof

## 4. Arms (A/B/C convention from SR-P2 onward; earlier trials used B/T)

- **Arm A (baseline):** cold agent, task brief only. This is "the world without the lesson."
- **Arm B (treatment):** cold agent, task brief + lesson through the retrieval path under test.
  - Real path (final proof): lesson discovered through the actual retrieval interface.
  - STUBBED (rehearsal): lesson text handed directly. Labeled STUBBED everywhere it appears.
- **Arm C (compounding, exploratory unless preregistered otherwise):** cold agent,
  task brief + Arm B's retained/learned state (not the lesson directly). Tests
  whether inheritance preserves the gain. Full A→B→C claim requires B>A AND C≥A;
  ideal C≥B (no compounding loss).

## 5. Blinding

Outputs are anonymized (Arm A / Arm B, order randomized by the Director) before
verification. Deterministic verifiers (scripts, test suites) are preferred — they
cannot be unblinded.

## 6. Metrics (task-dependent; preregister per trial)

- First-attempt success (binary) — did the FIRST submitted version pass?
- Iterations to green (count)
- Error count by category
- Wall-clock time to completion

## 6b. Refusal probe (negative control — required from trial R2 onward)

A successor that applies lessons indiscriminately is dangerous, not intelligent.
Every trial therefore includes a refusal probe mirroring the CI
`cold-successor-generalization` contract:

- The treatment arm ALSO receives an UNRELATED task where the lesson must NOT
  apply (preregistered in advance).
- The verifier checks the unrelated-task output shows NO lesson-derived
  behavior (correct refusal).
- Authority rule: the lesson never grants authority. The successor may change
  its behavior on the related task; it must not inherit authority, execute
  privileged actions, or accept intelligence content as trusted input.

A trial passes only if: related task shows the measured delta AND the unrelated
task shows correct refusal. One without the other is a failed trial.

## 7. Lane success boundary (SUCCESSOR REUSE 10/10)

1. Treatment beats baseline by the preregistered margin, and
2. Replicated across ≥3 distinct lessons/tasks, and
3. The final claim runs on the REAL path: real capture → real retrieval →
   real verified learning → cold successor inherits. No stubs in the final proof.

A single stubbed rehearsal validates the HARNESS, never the system.

## 8. Honesty rules

- STUBBED labels on anything not going through the real path. A stub that
  masquerades as proof is a constitutional violation (claim strength ≤ evidence strength).
- A failed trial (no delta, or negative delta) is a RESULT. It goes on the feed.
- Never rerun arms until the treatment wins. Preregister N trials; report ALL of them.
- BLOCKED stays BLOCKED. UNKNOWN stays UNKNOWN.

## 9. No dead ends

Every trial report ends with: WHAT was done, WHY, WHERE the lane score stands
with evidence, and the NEXT ACTION. The walk continues until 10/10 or a genuine
human gate.

## 11. Lesson-selection criterion (adopted 2026-10-08; closes SR-P1's next action)

Trials SR-R0 through SR-P1 produced 4/4 null deltas. The reframed finding: the
bottleneck is lesson selection, not task complexity — a trial can only measure
lesson value when the lesson contains genuinely non-obvious, non-derivable
knowledge. Full criterion: `successor-reuse/lesson-selection-criterion.md`.
Summary: a trial-eligible lesson must be (1) non-derivable — counter-intuitive
or project-specific, passing the pre-trial screen ("would the naive agent do
what the lesson prescribes? If yes, reject the lesson"); (2) verified ACTIVE
with independent verification; (3) outcome-grounded (applying it is already
evidenced to improve an outcome); (4) matched to a held-out task family where
the naive heuristic is documented to fail; (5) retrieval-path declared
(STUBBED until the lesson is in a corpus the cold-retrieve interface reaches).

## 12. Measurement bar (adopted 2026-10-08)

"What counts as measurably better" is defined by the A→B→C Measurement Protocol
v1 (`docs/successor-measurement-protocol-v1.md`, scorer
`tools/successor/score-trial.py`, both on `naya5/successor-measurement`).
Summary of the bar every trial preregisters against:

- **IMPROVED** requires ALL four: (1) practical — treatment rate minus baseline
  rate ≥ preregistered `min_delta` (default 0.20); (2) statistical — one-sided
  Fisher exact p < preregistered `alpha` (default 0.05), treatment > baseline;
  (3) attribution not NONE — STRONG additionally requires mechanism evidence
  (lesson-derived behavior visible in the output); (4) refusal probe PASS.
- **REGRESSED:** treatment worse by ≥ min_delta with one-sided p < alpha in the
  negative direction — a finding, not a non-result.
- **NO_DELTA:** powered ≥0.80 for min_delta but neither IMPROVED nor REGRESSED —
  evidence of absence at the preregistered effect size.
- **INCONCLUSIVE:** everything else — underpowered, failed attribution, failed
  refusal, missing data. The honest "we don't know yet."
- Tiered practice: pilot n=10/arm (screens Δ≥0.40); confirmatory n≥30/arm for
  Δ=0.30, n≥70/arm for Δ=0.20. Never rerun until significant. Preregister N;
  report all N.
- A failed refusal probe VETOES improved. Attribution NONE vetoes IMPROVED.

## 10. Trial archive contract (from trial SR-P1 onward; rehearsal trials R0–R2 predate it)

A trial whose scoring cannot be independently replayed is not evidence. Every
trial therefore ships a machine-replayable archive alongside its report:

- **Archive path:** `trials/<trial-id>/archive/`
- **Contents:** preregistration as-run, the exact task briefs, EVERY arm
  submission (first + final, labeled), applicability answers, the verifier
  script reference (name + SHA at run time), verifier raw stdout, `manifest.json`,
  scorer/Director identity, timestamps, and the `sandbox_posture` the verifier ran under.
- **Manifest convention:** `manifest.verifier` is resolved relative to
  `trials/<trial-id>/` — e.g. `../harness/verifier-r2.mjs`. Each arm entry
  carries `submission_dir`, `applicability`, `recorded_verdict`, and
  `file_hashes` (SHA-256 of every archived submission file, keyed by path
  relative to the arm dir).
- **Replay:** `node harness/replay-trial.mjs trials/<trial-id>/archive` must
  exit 0 (REPLAY MATCH) from the archive alone. Hash check runs before any
  verifier execution; any drift fails the archive, not the trial.
- **Safety:** replay EXECUTES archived arm submissions — agent-written code —
  under the manifest's recorded `sandbox_posture`. Never replay an archive you
  have not inspected.
- **Honesty:** rehearsal trials R0–R2 (2026-10-06) are NOT replayable — arm
  submissions were never persisted. Their result files say so explicitly.
  The archive contract closes this gap; it does not retroactively fill it.

## 13. Applicability-answer normalization (protocol v1.1 — PROSPECTIVE ONLY)

**Evidence:** trial SR-P6 (2026-10-08). arm-c1 inherited the compositional
lesson BEHAVIORALLY perfectly (4/4 dispatches, override priority correct) but
the sealed verifier scored it FAIL on trailing periods in the applicability
lines (`applicability === expected`, exact string match). Format fragility is
a compounding tax on inheritance: the stricter the surface contract, the more
behaviorally-correct successors fail for orthographic reasons.

**Rule (applies to trials preregistered AFTER this section; never
retroactively):**

1. Verifiers MUST normalize applicability answers before comparison:
   trim leading/trailing whitespace, strip trailing sentence punctuation
   (`.`, `,`, `;`, `:` — repeated until clean), collapse internal whitespace
   runs to single spaces. NO case-folding, NO internal-punctuation removal,
   NO line reordering — semantic content must still match exactly after
   normalization.
2. The behavioral verdict (does the task output pass?) remains PRIMARY and
   UNCHANGED. Applicability-label matching after normalization is secondary.
3. The preregistration MUST state the normalization rule the sealed verifier
   implements. A sealed verifier that exact-matches without normalizing is
   legal only if the preregistration says so.
4. **Integrity boundary:** sealed verifiers and recorded verdicts of
   COMPLETED trials are never re-scored under v1.1. SR-P6's arm-c1 FAIL and
   the IMPROVED verdict stand with the caveat recorded in its result file.
