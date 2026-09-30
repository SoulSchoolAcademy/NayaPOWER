# 0006 — Decision Value Calculus V2.1 (Candidate Specification)

**Truth state:** OFFICIAL DIRECTION / CANDIDATE SPEC — not production-proven, not eligible for a 10/10 claim.
**Spec authority:** SoulSchoolAcademy/NayaPOWER issue #1182 — "DIRECTOR-APPROVED DIRECTION — Decision Value Calculus V2.1 baseline candidate" plus the R1–R6 red-team patch (both CANDIDATE, NOT RATIFIED).
**Reference implementation:** `kernel/value_calculus_v2.py` (`VALUE-CALCULUS-V2.1.0`), tests in `tests/test_value_calculus_v2.py`.
**Network-value companion:** `kernel/network_value.py` (`NETWORK-VALUE-V2.1.0`), tests in `tests/test_network_value.py`.

## 0. Root-core pattern

Every decision-capable Naya, agent, and subsystem uses one reusable pattern:

`RESOLVE → GATE → SCORE → COMPARE → SELECT → ACT/ESCALATE → OBSERVE → VERIFY → LEDGER → LEARN → RECALIBRATE`

Domains may use different score dimensions and weights but MUST preserve the invariants:
- hard boundaries precede optimization;
- value never creates authority;
- unknown never silently becomes pass;
- scores remain inspectable and decomposable;
- predicted value is not actual value;
- verified outcomes calibrate future math;
- human worth is never reduced to a scalar score.

## 1. Three mathematics — connected, never confused

- **A. Decision mathematics** — what should Naya do?
  `GATES → QUALITY → VALUE → RISK → COMPARE → ACT/ESCALATE`
- **B. Evidence mathematics** — did the decision actually work?
  `PREDICTION → ACTION → OBSERVATION → VERIFICATION → ACTUAL VALUE → CALIBRATION`
- **C. Network-value mathematics** — what verified value did a contributor create?
  `contribution → provenance → novelty → quality → relevance → verification → impact → reuse → downstream verified value`

A and B share the typed **decision receipt** (SmartLedger stream A).
C uses the typed **contribution receipt** (SmartLedger stream B).
One substrate; different semantics, writers, access rules, and trust computations. Never create two competing physical truth systems.

## 2. Four-valued gate

`G(a) ∈ {PROHIBITED, NEEDS_AUTHORITY, NEEDS_EVIDENCE, ADMISSIBLE}`

Hard rights, privacy, safety, security, law/policy, and authority constraints are not scalarized. Evidence-floor failures gate `NEEDS_EVIDENCE`; they never silently become PASS.

## 3. Pure decision quality

`Q(a) = Σ w_i d_i(a)`, `Σw_i = 1`, `d_i ∈ [0,10]`.

V2.1 dimensions: objective fit 0.20, evidence sufficiency 0.20, applicability 0.15, robustness 0.15, reversibility 0.10, blast containment 0.10, simplicity 0.10.

**Value magnitude is NOT a Q dimension.** Q measures decision soundness only. Bands: 9.5–10 DELIGHT, 9.0–<9.5 ACCEPT, 7.0–<9.0 BELOW STANDARD, <7.0 REJECT. A critical proof gap caps autonomous readiness regardless of the arithmetic mean.

## 4. Baseline-relative value

`PV(a) = B(a) − H(a) − C(a) − R(a)`; `ΔV(a|b) = PV(a) − PV(b)`; `ΔV(b|b) = 0` by definition, while inaction itself may still have positive or negative absolute consequences. The `−9…+9` range is a semantic anchor/display scale, not a ceiling; `D_verified = clamp(ΔV_actual, −9, +9)` is for ladder display only — raw ΔV is preserved in the ledger.

## 5. Risk / tail protection

Expected value may never average away unacceptable tail risk. Versioned per-scope risk policy `τ_scope`; prohibited harm class triggered → PROHIBITED; `P(unacceptable harm) > τ_scope` → PROHIBITED or NEEDS_AUTHORITY. Reversibility is a control/escalation input (below 0.70 → non-autonomous regardless of score), not a multiplier that can zero out must-do irreversible work.

## 6. Confidence integrity

Aggregate `C_agg = Σ w_i c_i` and critical-dimension `C_critical = min(c_i)`. Low-risk autonomous hypotheses: `C_agg ≥ 0.80`, `C_critical ≥ 0.75`. One unknown critical fact cannot be averaged away by many certain minor facts. Sample/data floor `k_scope` (5 low-stakes / 20 consequential hypotheses): below floor → NEEDS_EVIDENCE.

## 7. Pareto + selection

Among ADMISSIBLE candidates with `Q ≥ 9` and `V_safe > 0`: Pareto frontier over (max `V_safe`, max `Q`, min residual risk); rank frontier by `V_safe` desc (ties: `Q`, then lower risk); top-3 deep-checked; top-1 selected. Autonomous dominance uses the **relative** margin `m = (V1 − V2)/max(|V1|, ε) ≥ 0.25` (hypothesis, calibratable). No unbounded absolute Priority-ratio margin.

## 8. Rule of up-to-10 → top 3 → one

Generate up to 10 plausible options where ambiguity merits breadth. Mandatory candidates where applicable: current course / do nothing, gather evidence, reversible probe, rollback/revert, human escalation — the candidate set cannot rig the winner.

EXECUTE only if: ADMISSIBLE ∧ Q≥9 ∧ V_safe>0 ∧ confidence floors pass ∧ data floor passes ∧ authority permits ∧ reversible enough for scope ∧ clear relative dominance ∧ no unauthorized parameter deviation. Else BRIEF / RESEARCH / REWORK.

AskHuman = AuthorityRequired ∨ MaterialIntentAmbiguity ∨ ConsequentialIrreversibility ∨ MaterialUncertainty ∨ NoClearDominantOption.

## 9. Provisional verification

Domain-specific observation windows (24h reversible/low-stakes; 7d financial; 30d irreversible/third-party; 90d physical/rights). PASS is PROVISIONAL until the window closes with no harm → CONFIRMED; harm reopens the record (REOPENED, delta recomputed). No irreversible learning promotion may depend solely on a still-open window where delayed harm is material.

## 10. Learning / flexible math

Every weight, threshold, normalization map, and rubric carries version + owner + scope + evidence basis + calibration history + supersession lineage. `error_V = |ΔV_pred − ΔV_actual|`; persistent bias, gaming signals, or degraded outcomes lower estimator confidence and generate LEARN candidates. Low-stakes decisions are sampled into the ledger so the estimator cannot game calibration by avoiding consequential records. The algorithm learns without rewriting its own Constitution.

## 11. Human contribution / reputation law

**Never score human worth.** `Activity ≠ Value.` Contribution credit (candidate anti-spam formula, not ratified law):

`CVS_j = sign(ΔV_verified_j) × 9 × (Quality × Relevance × Verification × Impact × Novelty)^(1/5)`, factors in [0,1].

Profile stays multidimensional: Contribution (verified value), Reliability (accuracy over time), Conduct (rule compliance), Trust (derived, contextual). No single negative contribution auto-punishes or bans. **Authority ≠ Reputation — always.** Levels/status derive only from verified contribution + reliability + conduct thresholds, with diminishing returns and novelty controls so 10,000 low-value actions cannot outrank one major verified contribution.

Hub levels (candidate): 1 New (0), 2 Emerging (100), 3 Developing (500), 4 Advancing (1,500), 5 Five-Star (4,000), 6 Advanced (9,000), 7 Expert (18,000), 8 Elite (32,000), 9 Master (52,000), 10 Ten-Star (75,000) — points from verified contribution value; micro-actions (like/comment/share) earn small capped diminishing credit as weak value signals; upper levels additionally require reliability/conduct standing.

## 12. Attack closures required of any V2.1 implementation

Prediction inflation, B/H/C/R component gaming, action-splitting / authorization laundering (plans get whole-plan assessment; steps inherit plan gates; step PVs never sum into plan PV), delayed harm, collective vs individual harm, conflicting principals, malicious-user value asymmetry, ledger/reputation reward hacking, uncertainty laundering, AI-to-AI conflict, jurisdiction conflict, bad baseline selection, weight/rubric manipulation. Threshold/parameter deviation without recorded authority → NEEDS_AUTHORITY semantics.

## 13. Nine-node placement

SELF → objective, stakeholders, baseline, current state · LAW → gates, policy, rights, authority, risk class · KNOW → evidence-bound facts/estimates · CONNECT → applicability, affected parties, relationships · ACT → selected authorized action · PROVE → decision + execution + observation receipts · VERIFY → independent outcome/value recomputation · LEARN → calibrated estimator/rubric proposals · EVOLVE → versioned promotion + cold-successor continuity.

## 14. Proof gate

A specification may be called 9.5-ready only when: R1–R6 definition-complete; schema machine-readable; deterministic reference implementation passes; all named adversarial/property tests pass or are explicitly accepted residual risk; SmartLedger receipt schema integrated without a second truth system; cold successor can reconstruct the decision; calibration can change future ranking without changing authority; multi-principal/distributional harm has an explicit policy boundary. **10/10 remains unavailable** until runtime integration + independent verification + production evidence establish the declared scope.
