# Shared Decision Calculus V2.1 — Nine-Node Placement

**Status:** CANDIDATE, NOT RATIFIED (Issue #1182). Shared machinery — **not a tenth node**.
The calculus is the reusable pattern every node invokes; dimensions and weights
change by domain, the invariants do not.

Reference: `kernel/decision-calculus/value-calculus-v2.1.ts` ·
Spec: `NAYANODE/0027-DECISION-VALUE-CALCULUS-V2.1-CANDIDATE.md` ·
Schema: `BRAIN/03-KERNEL/SCHEMA/DECISION-OBJECT-V2.1.json`

## Placement (§14 baseline)

| Node | Calculus role |
|---|---|
| SELF | Declares objective, stakeholders, horizon, baseline/current course, current ladder state. Owns the baseline declaration (bad-baseline defense starts here). |
| LAW | Owns gates: hard-law boundaries, τ_scope table, authority envelope, risk class, jurisdiction status. Admissibility is decided here, never in scoring. |
| KNOW | Supplies evidence-bound facts: PV components (B/H/C/R), ΔV uncertainty U, tails, evidence count n, per-dimension confidences. Unknown is reported as unknown. |
| CONNECT | Applicability/context fit, affected parties (collective-harm expansion), relationships, resource-claim contention between agents. |
| ACT | Executes ONLY the selected ADMISSIBLE action within the authority basis recorded in the receipt. No score ever widens ACT's authority. |
| PROVE | Writes typed SmartLedger receipts: decision receipt (§10A) at decide-time, execution receipt at act-time, observation receipt at verify-time. Binds calculusVersion + configHash. |
| VERIFY | Independently recomputes outcomes: ΔV_actual, D_verified, calibration error, PASS/PASS_PENDING_WINDOW/FAIL/REOPENED. Recompute must MATCH for cold successors. |
| LEARN | Turns calibration errors into LEARN candidates: weight/threshold/τ/window proposals with evidence basis. Never promotes on an open window with material delayed harm. |
| EVOLVE | Versioned promotion of calculus configs (supersession lineage) + cold-successor continuity: same facts + same config version → same decision. |

## Invariants (all nodes, all domains)

1. Hard boundaries precede optimization.
2. Value never creates authority (a 10/10 score grants zero new permissions).
3. Unknown never silently becomes pass.
4. Scores remain inspectable and decomposable (receipt shows every input).
5. Predicted value is not actual value.
6. Verified outcomes calibrate future math; calibration never rewrites constitutional boundaries.
7. Human worth is never reduced to a scalar (contribution scoring is a separate
   candidate model; see `docs/hub-contribution-economy-v2.1-candidate.md`).

## Domain panels (same computer, different instrument panel)

- **Code:** correctness, simplicity, maintainability, performance, compatibility, proof.
- **Product:** usefulness, comprehension, friction, speed, delight, accessibility.
- **Retrieval:** relevance, applicability, provenance, freshness, epistemic state.
- **Network matching:** relevance, permission, availability, complementary capability, privacy.

Each panel is a versioned config (weights, thresholds, τ, windows, dScale) under
§12 flexible-math rules. Panels do not override the invariants above.
