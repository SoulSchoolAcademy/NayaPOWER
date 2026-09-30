# NayaPOWER Decision Value Calculus Specification V2.1

**Status:** HUMAN-DIRECTOR RATIFIED — CANONICAL DECISION ARCHITECTURE V1; IMPLEMENTATION VERIFICATION REQUIRED  
**Domain:** 13 VALUE & EXPERIENCE  
**Canonical seam retained:** `NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md`  
**Implementation:** `kernel/value_calculus.py`  
**Tests:** `tests/test_value_calculus.py`  
**Machine schema:** `.naya/specifications/NAYA-DECISION-VALUE-CALCULUS-V2.1.schema.json`  
**Issue:** #1182  
**Effective working version:** 2.1

> This file keeps the established canonical path to avoid a second value brain. V2.1 supersedes the internal V1 scoring semantics while preserving the V1 provenance in Git history.

## 1. Root operating law

NayaPOWER uses one reusable decision pattern:

`RESOLVE → GATE → SCORE → COMPARE → SELECT → ACT/ESCALATE → OBSERVE → VERIFY → LEDGER → LEARN → RECALIBRATE`

Hard boundaries precede optimization. Value never creates authority. UNKNOWN never silently becomes PASS.

## 2. Four-state gate

For every candidate action `a`:

`G(a) ∈ {PROHIBITED, NEEDS_AUTHORITY, NEEDS_EVIDENCE, ADMISSIBLE}`

- **PROHIBITED** → refuse.
- **NEEDS_AUTHORITY** → obtain the legitimate authority source.
- **NEEDS_EVIDENCE** → research, probe, narrow scope, wait, or escalate.
- **ADMISSIBLE** → eligible for quality/value comparison.

Truth, rights, privacy, safety, security, law/policy, consent, and authority are not scalarized into preference weights.

## 3. Decision quality Q

Quality answers: **How sound is this decision?**

`Q(a)=Σ w_i d_i(a)`, where `d_i∈[0,10]` and `Σw_i=1`.

Default V2.1 dimensions:

| Dimension | Default weight | Meaning |
|---|---:|---|
| objective_fit | 0.20 | directly advances the declared legitimate objective |
| evidence_sufficiency | 0.20 | evidence supports the decision rather than a guess |
| applicability | 0.15 | evidence/context actually applies here |
| robustness | 0.15 | plausible failure modes are controlled |
| reversibility | 0.10 | action can be stopped/recovered where appropriate |
| blast_containment | 0.10 | effects are bounded |
| simplicity | 0.10 | smallest effective path / least unnecessary burden |

**Value magnitude is not a Q dimension.**

Bands:
- **9.5–10.0 DELIGHT**
- **9.0–<9.5 ACCEPT**
- **7.0–<9.0 BELOW STANDARD**
- **<7.0 REJECT / REWORK**

A critical proof gap may cap autonomy regardless of average Q.

## 4. Positive value and baseline-relative delta

For an action:

`PV(a)=B(a)-H(a)-C(a)-R(a)`

where:
- `B` = evidence-bound expected benefit;
- `H` = expected harm;
- `C` = necessary cost/resources/opportunity cost;
- `R` = residual uncertainty/risk penalty.

Decision value is relative to a declared baseline `b`:

`ΔV(a|b)=PV(a)-PV(b)`

Therefore `ΔV(b|b)=0` by definition, while the absolute consequences of inaction may be nonzero.

The familiar `−9 … 0 … +9` is a semantic display anchor, not a ceiling on raw real-world value. Verified display direction may use:

`D_verified = clamp(Normalize(ΔV_actual), -9, +9)`

The raw delta remains preserved.

## 5. Confidence and evidence floors

Confidence cannot be averaged into false certainty.

The engine requires both:

`C_agg = Σw_i c_i`

and:

`C_critical = min(c_i for critical dimensions)`.

Initial low-risk autonomous defaults:
- `C_agg ≥ 0.80`
- `C_critical ≥ 0.75`
- PV component confidence `≥ 0.75`
- evidence count `≥ k_scope` (default implementation: 1; profiles may raise it)

If the data floor is not met, the state is **NEEDS_EVIDENCE**, not PASS.

Residual uncertainty is mechanically priced into `R`; low component confidence creates a minimum residual-risk floor.

## 6. Risk and unacceptable tails

Expected value may not average away catastrophic or otherwise unacceptable tail risk.

Each governed domain provides a versioned risk policy:

`τ_scope = {harm_class, severity_threshold, probability_threshold, stakeholder_harm_limit, response}`

If the threshold is crossed, the result is PROHIBITED or NEEDS_AUTHORITY according to the approved policy.

Risk thresholds are versioned hypotheses unless constitutional law fixes a stricter boundary.

## 7. Plan-level stakes and anti-laundering

A consequential plan cannot be split into apparently low-stakes steps to escape authority.

`effective_stakes(step)=max(step_stakes, plan_stakes)`

Consequential or irreversible action requires explicit human authority unless a separate standing-authority contract explicitly covers that exact scope.

## 8. Pareto and ranking

After gates, only candidates with `Q≥9` and positive conservative value may enter the autonomous selection set.

Pareto frontier objectives:
- maximize `V_safe`;
- maximize `Q`;
- minimize residual risk.

A candidate is dominated when another is at least as good on all three and strictly better on at least one.

Frontier survivors are ordered by:
1. conservative value;
2. dependency unlock when relevant;
3. reversibility/recoverability;
4. lower human burden;
5. simplicity/efficiency;
6. evidence confidence.

Autonomous dominance uses a relative margin:

`m=(V_safe1−V_safe2)/max(|V_safe1|, ε)`

The default implementation threshold is 0.10 and is calibratable.

## 9. Rule of up-to-10 → top 3 → one

When ambiguity merits breadth, generate up to 10 plausible candidates.

Where applicable include:
- current course / do-nothing baseline;
- gather evidence;
- reversible probe;
- rollback/revert;
- human escalation.

Deep-check the top 3.

Autonomous EXECUTE requires:

`ADMISSIBLE ∧ Q≥9 ∧ V_safe>0 ∧ confidence floors pass ∧ evidence floor passes ∧ authority permits ∧ bounded/reversible enough ∧ relative dominance passes`

Otherwise the system must BRIEF, RESEARCH, or REWORK instead of exporting unnecessary orchestration.

## 10. AskHuman law

`AskHuman = AuthorityRequired ∨ MaterialIntentAmbiguity ∨ ConsequentialIrreversibility ∨ MaterialUncertainty ∨ NoClearDominantOption`

If none apply and the action is within standing authority, the machine should absorb orchestration complexity and act.

## 11. Observation, verification, and delayed harm

Prediction is not achievement.

Verification states include:
- UNVERIFIED;
- PASS_PENDING_WINDOW;
- VERIFIED_PASS;
- FAIL;
- ESCALATE.

Where delayed harm is material, a PASS remains provisional until its domain-specific observation window closes. Later contradictory evidence may reopen a prior PASS.

## 12. SmartLedger decision receipt

The calculus emits a typed `ALIGNMENT_DECISION` receipt suitable for the existing SmartLedger/event/evidence substrate.

Required fields include:
- decision ID;
- engine/schema version;
- objective;
- baseline;
- stakeholders;
- time horizon;
- complete candidate evaluations;
- gate reasons;
- Q dimensions/weights/confidence;
- PV and ΔV;
- risk/tail policy outcome;
- authority basis;
- selected action/decision state;
- evidence refs;
- observation window;
- verification state;
- predicted and actual ΔV;
- display `D_verified`;
- calibration error.

**No second ledger is created.** The receipt maps to the existing SmartLedger's typed event/value/verification/outcome/metadata fields.

## 13. Independent recomputation and calibration

A cold verifier must be able to recompute the decision from the preserved candidates, profile, baseline, risk policy, and evidence state.

Calibration:

`error_V = |ΔV_predicted − ΔV_actual|`

Persistent bias or increasing error lowers estimator confidence and creates a LEARN candidate.

Learning may propose weight/threshold/rubric changes; it may not silently rewrite constitutional boundaries or authority.

## 14. Contribution / network-value scoring

The same mathematical discipline may score a **contribution**, never a human being.

Initial contribution score:

`CVS = sign(ΔV_verified) × 9 × (Quality × Relevance × Verification × Impact × Novelty)^(1/5)`

where each factor is normalized to `[0,1]`.

Properties:
- no verified value → no positive credit;
- low novelty discounts repetitive/spam-like activity;
- raw activity count is not value;
- negative CVS is evidence, not automatic punishment;
- positive recognition points may be derived from positive CVS using a versioned domain profile and repeat-decay factor;
- authority is never derived from reputation.

Human/profile state remains multidimensional:
- **Contribution** — verified value created;
- **Reliability** — accuracy/usefulness over time;
- **Conduct** — governance/rule compliance;
- **Trust** — contextual inference from verified history, provenance, recency, and domain.

`Activity ≠ Value`  
`Reputation ≠ Human Worth`  
`Reputation ≠ Authority`

Exact level names, point thresholds, and social-action weights remain a configurable NayaNET profile until empirical calibration establishes a fair baseline.

## 15. Anti-gaming / adversarial requirements

V2.1 must defend or explicitly record residual risk for:
- prediction inflation;
- B/H/C/R component gaming;
- action splitting / authority laundering;
- delayed harm;
- collective vs individual harm;
- conflicting principals;
- malicious-user value asymmetry;
- reward/ledger gaming;
- uncertainty laundering;
- AI-to-AI resource/value conflict;
- jurisdiction conflict;
- bad baseline selection;
- weight/rubric manipulation.

## 16. Nine-node placement

- **SELF** — objective, stakeholders, baseline, current state.
- **LAW** — gates, policy, rights, authority, risk class.
- **KNOW** — evidence-bound facts and estimates.
- **CONNECT** — applicability, affected parties, relationships.
- **ACT** — selected authorized action.
- **PROVE** — decision, execution, observation receipts in SmartLedger.
- **VERIFY** — independent outcome/value recomputation.
- **LEARN** — calibrated estimator/rubric proposals from verified outcomes.
- **EVOLVE** — versioned promotion and cold-successor continuity.

No separate Value Node, authority engine, truth model, ledger, or learning path is created.

## 17. Proof law

The required chain is:

`SPEC → SCHEMA → DETERMINISTIC CODE → PROPERTY TESTS → ADVERSARIAL TESTS → DECISION RECEIPT → INDEPENDENT RECOMPUTATION → COLD SUCCESSOR`

IMPLEMENTED ≠ VERIFIED.  
VERIFIED ≠ PRODUCTION-PROVEN.

A 10/10 claim is unavailable until runtime integration, independent verification, and production evidence prove the declared scope.


## 18. Runtime binding — V2.1 value receipts

The production seam is intentionally additive.

Every new execution receipt that enters the canonical SmartLedger path receives an explicit assessment state:

- **UNASSESSED** — no value assessment has been established.
- **ASSESSED** — V2.1 value has been calculated, but verification is not yet sufficient for verified-value recognition.
- **VERIFIED_VALUE** — the receipt carries a verified outcome and independently checkable value result.

Typed V2.1 receipts are carried in the existing SmartLedger `value` field and classified in SmartLedger metadata. The canonical event substrate remains one ledger; no second value ledger is introduced.

Supported typed receipt families at the runtime boundary are:

- `ALIGNMENT_DECISION` — validated against the V2.1 decision engine/schema identity.
- `CONTRIBUTION_VALUE` — validated as a V2.1 contribution receipt and unable to claim positive points without verified value.

The legacy `NayaNET_V1_STARTING_MODEL` is provenance, not modern verified value. Historical `base_points=5/10` records are not rewritten or reinterpreted. New runtime records using that legacy marker remain explicitly legacy/unassessed and cannot silently become V2.1 verified value.

Positive recognition must therefore follow:

`evidence → assessment → verification → value receipt → derived recognition`

not:

`activity → points`

The SmartLedger receipt stores a deterministic receipt hash alongside the typed payload so an independent reader can reconstruct the exact persisted receipt. Projection to `nayanet_intelligence_index` remains a derived view of the same canonical ledger event.

This runtime binding is an implementation proof point, not a claim that the full V2.1 behavior is production-proven. Behavioral effectiveness, contribution calibration, anti-gaming performance, and profile fairness remain subsequent verification work under Issue #1184.


## 18. Human-Director-ratified Decision Architecture

The Human Director has ratified the canonical decision discipline in:

**NAYANODE/0028-CANONICAL-DECISION-ARCHITECTURE-V1.md**

This is an evolution of the existing V2.1 calculator, not a replacement engine.

The canonical decision state is represented by four separate layers:

1. **Hard gates / admissibility** — non-tradeable constraints.
2. **Signed value V** — V ∈ [-10,+10].
3. **Quality Q** — Q ∈ [0,10].
4. **Confidence and uncertainty** — C ∈ [0,1] plus a visible deterministic uncertainty envelope.

Canonical sequence:

OBJECTIVE → CURRENT TRUTH → HARD GATES → OPTIONS → SIGNED VALUE → QUALITY → UNCERTAINTY → RANK → AUTHORITY → ACT / READ_MORE / ASK / REFUSE → VERIFY → LEARN

The Rule of 10 → 3 → 1 is a decision-compression strategy, not a requirement to expose ten internal alternatives to the human.

The machine must not use a positive score to trade away a hard stop, and it must not represent an uncertainty envelope as a statistical confidence interval.

Historical V1/base-point provenance remains historical. New recognition derives from verified value evidence, never raw activity.

This ratification closes the architecture decision. Remaining work is executable implementation proof and empirical calibration, not another conceptual scoring design.
