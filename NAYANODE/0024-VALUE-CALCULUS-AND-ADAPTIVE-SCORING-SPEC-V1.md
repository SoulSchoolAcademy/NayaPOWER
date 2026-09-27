# NayaPOWER Value Calculus & Adaptive Scoring Specification V1

**Status:** PROPOSED — implementation branch; human ratification required before constitutional adoption
**Purpose:** Define one deterministic, evidence-aware scoring capability for heterogeneous digital work.

## 1. Foundational law
**MAXIMUM VERIFIED VALUE / MINIMUM NECESSARY COMPLEXITY.**

Value is measurable evidence about usefulness, consequence, reuse, learning, and resource efficiency. Measurement never overrides truth, authority, privacy, safety, provenance, or human sovereignty.

The system may score an artifact, action, outcome, interaction, contribution, or system state. It must not score a person's intrinsic human worth.

## 2. Scores are contextual measurements
A score is valid only relative to a declared subject, objective, context, time window, dimensions, weights, evidence requirements, and aggregation rule.

Score = f(subject, objective, context, dimensions, weights, evidence, observations).

There is no universally meaningful score independent of purpose.

## 3. Value vector
Represent value first as a vector:
V = (U, R, A, E, C, Re, L, K, T, H)

U Utility; R Reliability; A Applicability; E Evidence strength; C Consequence/outcome; Re Reusability; L Learning yield; K Compounding yield; T Time/resource efficiency; H Harm/error/waste/misapplication.

Dimensions are included only when required by the declared objective.

## 4. Epistemic state is separate from value
UNKNOWN, OBSERVED, SUPPORTED, VERIFIED, FAILED, and BLOCKED are states, not value scores.

High desirability with weak evidence remains weakly evidenced. A verified result may be low-value. This prevents confidence, popularity, or preference from becoming truth.

## 5. Adaptive domain profiles
Profiles declare what matters for the evaluation, for example CODE_QUALITY, ARCHITECTURE, DESIGN, USER_EXPERIENCE, INTELLIGENCE, SYSTEM_READINESS, EXECUTION_CYCLE, LEARNING, and CONTRIBUTION.

Baseline weights are normalized so sum(w_i) = 1.

Effective weights:
w*_i = normalize(w_base_i × m_objective_i × m_context_i × m_risk_i).

Every multiplier and final weight is recorded. Critical requirements are gates, not merely weights: a required security, authority, correctness, privacy, or evidence failure can block readiness regardless of the arithmetic score.

## 6. Transparent value calculation
Each dimension is measured from observations and evidence, then normalized to [0,1].

V_raw = sum(w*_i × d_i).

Net value explicitly accounts for harm:
V_net = positive_value − harm_cost.

Resource cost may include human attention, human time, compute, storage, latency, operational effort, and risk exposure.

## 7. Estimated, observed, verified
Keep three distinct quantities:
- V_estimated: predicted or claimed value before sufficient observation.
- V_observed: value measured from observed outcomes.
- V_verified: value supported by the required verification procedure.

Only V_verified may support a claim of verified improvement.

## 8. Efficiency metrics
MVPA = Verified Value Produced / Resources Consumed.

MVPM = Verified Human Value / (Human Attention + Human Time + System Cost).

Learning Efficiency = Useful Understanding Acquired / (Attention + Time).

Compression Ratio = Source Information / Operational Intelligence.

Meaning Preservation = Required Meaning Preserved / Required Meaning.

Contribution Value = Direct Value + Reuse + Verification + Learning + Compounding − Harm Cost.

Contribution value is not human worth. Economic reward is a separate layer.

## 9. Procedural fairness
Mathematics cannot prove that every domain's value judgment is morally just. It can provide reproducible procedural fairness through declared objectives, deterministic formulas, normalized weights, consistent missing-evidence handling, immutable receipts, versioned profiles, calibration, sensitivity analysis, conflict handling, and independent review.

When multiple approved profiles are reasonable, expose material sensitivity instead of silently selecting a favorable profile.

## 10. Universal scoring algorithm
SUBJECT → IDENTIFY TYPE/SCOPE → SELECT OBJECTIVE/PROFILE → SELECT REQUIRED DIMENSIONS → COLLECT OBSERVATIONS → VALIDATE EVIDENCE → CLASSIFY EPISTEMIC STATE → DERIVE WEIGHTS → NORMALIZE → CALCULATE GROSS VALUE → SUBTRACT HARM/COST → APPLY CRITICAL GATES → CALCULATE VERIFIED-VALUE METRICS → RUN SENSITIVITY → EMIT SCORE + RECEIPT → PRESERVE IF USEFUL → LEARN ONLY IF FUTURE BEHAVIOR CAN CHANGE.

## 11. Anti-gaming
Reject score inflation, cherry-picked evidence, duplicate counting, popularity-as-truth, activity-as-value, confidence-as-proof, complexity-as-quality, feature-count-as-value, documentation-volume-as-value, and favorable-profile selection.

## 12. Complexity efficiency
Efficiency = Verified Capability Gain / Added Complexity Cost.

Complexity cost includes storage, compute, latency, maintenance, cognitive load, dependency surface, and failure surface. A feature is not valuable merely because it exists.

## 13. Score receipt
Persist: score_id, subject_id, subject_type, objective, profile_id/version, timestamp, context, dimensions, observations, effective weights, evidence references, verification states, gross value, harm/cost, net value, sensitivity result, critical gates, final score, evaluator/version, and supersession lineage.

## 14. V1 implementation boundary
Implement typed value vectors, profile-based adaptive weighting, deterministic normalization, net-value calculation, critical gates, MVPA/MVPM, score receipts, sensitivity analysis, and deterministic serialization.

Do not implement person-worth scoring, autonomous economic pricing, opaque learned weights, a second database, or a new memory subsystem.

## 15. Acceptance tests
Prove identical inputs produce identical scores; weights normalize; objective changes alter weights predictably; critical failure cannot be averaged away; missing evidence cannot silently become verified; harm reduces net value; duplicate evidence is not double-counted; receipts permit recomputation; approved-profile sensitivity is visible; value scores remain distinct from readiness scores; and human intrinsic worth is not a scoreable subject type.

## Master question
Did this subject produce more verified useful value than the resources, risk, harm, ambiguity, and complexity required to produce and maintain it — for the declared objective and context?

That is the machine-operational form of **MAXIMUM VERIFIED VALUE / MINIMUM NECESSARY COMPLEXITY**.