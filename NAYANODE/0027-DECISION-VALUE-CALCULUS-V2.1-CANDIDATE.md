# Decision Value Calculus V2.1 — Candidate Specification

**Status:** CANDIDATE, NOT RATIFIED — OFFICIAL DIRECTION only (Issue #1182).
Not production-proven. No 10/10 claim available until runtime integration +
independent verification + production evidence.
**Supersedes (candidate):** `NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md` and
`kernel/value_calculus.py` (V1) — lineage only; V1 remains untouched until ratified succession.
**Reference implementation:** `kernel/decision-calculus/value-calculus-v2.1.ts`
**Tests:** `tests/decision-calculus-v2.1.test.mjs` (40 tests, all passing)
**Machine schema:** `BRAIN/03-KERNEL/SCHEMA/DECISION-OBJECT-V2.1.json`
**Working sources:** Issue #1182 comment 5921148872 (V2.1 baseline candidate) +
comment 5921158459 (R1–R6 patch).

## 0. Root-core pattern

`RESOLVE → GATE → SCORE → COMPARE → SELECT → ACT/ESCALATE → OBSERVE → VERIFY → LEDGER → LEARN → RECALIBRATE`

Domain-general. Domains may change score dimensions/weights but MUST preserve:
hard boundaries before optimization; value never creates authority; unknown never
silently becomes pass; scores inspectable and decomposable; predicted ≠ actual value;
verified outcomes calibrate future math; human worth never reduced to a scalar.

## 1. Four-valued gate

`G(a) ∈ {PROHIBITED, NEEDS_AUTHORITY, NEEDS_EVIDENCE, ADMISSIBLE}` — evaluated in
this precedence: hard law (harm flag, known-wrong, unlawful, prohibited harm class)
→ τ_scope tail gates → jurisdiction conflict → authorization → law-unknown-at-stakes
→ conflicting principals → consequential-irreversible → evidence/confidence floors.

## 2. Pure decision quality

`Q(a) = Σ wᵢ dᵢ(a)`, `Σwᵢ = 1`, `dᵢ ∈ [0,10]`. **Value magnitude is NOT a Q
dimension** (the V2 coupling is rejected: "value manufacturing quality" is the
mirror of "value manufacturing authority").

| Dimension | Weight |
|---|---|
| objectiveFit | 0.20 |
| evidenceSufficiency | 0.20 |
| applicability | 0.15 |
| robustness | 0.15 |
| reversibility | 0.10 |
| blastContainment | 0.10 |
| simplicity | 0.10 |

Bands: 9.5–10 DELIGHT · 9.0–<9.5 ACCEPT · 7.0–<9.0 BELOW STANDARD · <7.0 REJECT.
A dimension below 5.0 caps Q below the autonomy bar regardless of the mean.

## 3. Baseline-relative value

`PV(a) = B(a) − H(a) − C(a) − R(a)` (evidence-bound benefit, harm, necessary cost,
residual risk). `ΔV(a|b) = PV(a) − PV(b)`; `ΔV(b|b) = 0` by definition.
Harmful inaction is visible: a negative-drift baseline makes action ΔV > 0.
Conservative value: `V_safe = ΔV_pred − U − Σ harmᵢ·pᵢ`, where U is the
evidence-bound uncertainty on ΔV (production estimators derive U = z·SE).

Ladder display: `D_verified = clamp(Normalize(ΔV_actual), −9, +9)` with the
versioned domain normalization `Normalize(ΔV) = 9·ΔV/(dScale+|ΔV|)` (reference
default `dScale = 1.0`, hypothesis). Raw ΔV is always preserved in the ledger.

## 4. Risk / tail protection (R4)

`τ_scope = {harm_class, severity_threshold, probability_threshold, escalation}`.
Seed table (hypotheses for director review; the system never loosens them):

| Scope | τ (max P) | Severity ≥ | Escalation |
|---|---|---|---|
| physical | 0 | 9 | PROHIBITED |
| rights | 0 | 9 | PROHIBITED |
| financial | 0.001 | 7 | NEEDS_AUTHORITY |
| data | 0.001 | 7 | NEEDS_AUTHORITY |
| reputational | 0.01 | 5 | NEEDS_AUTHORITY |
| informational | 0.05 | 3 | NEEDS_AUTHORITY |
| resource | 0.10 | 2 | NEEDS_AUTHORITY |

τ = 0 classes refuse on any material probability (≥ 1e-6); sub-material
probabilities are modeling noise, not license. Collective harm is expanded to an
effective tail: `perCapitaHarm × parties × probability`. Reversibility is a gate
input (`reversibility < 7/10` → non-autonomous), never a multiplicative reward.

## 5. Confidence integrity (R6)

`C_agg = Σ wᵢ cᵢ ≥ 0.80` and `C_critical = min(critical dims) ≥ 0.75`
(low-risk autonomous hypotheses; critical dims: objectiveFit, evidenceSufficiency,
robustness). Data floor: `n ≥ k` with `k = 5` (low stakes) / `k = 20`
(consequential). Below floor → NEEDS_EVIDENCE, never a confident score.

## 6. Pareto + selection (R1, R3)

Among ADMISSIBLE with `Q ≥ 9.0`, `V_safe > 0`: Pareto frontier over
(max V_safe, max Q, min tailPenalty); dominance = ≥ on all three, > on ≥1.
Rank frontier: V_safe → urgency → reversibility → lower human burden →
simplicity → confidence. Autonomous dominance margin (relative, on V_safe):
`m = (V_safe₁ − V_safe₂)/max(|V_safe₁|, ε) ≥ 0.25` (hypothesis).
`P_norm = P_raw/(1+P_raw)` is retained for priority-queue scheduling only.

EXECUTE iff: ADMISSIBLE ∧ Q≥9 ∧ V_safe>0 ∧ floors pass ∧ authorized ∧
reversibility ≥ 7 ∧ clear relative dominance ∧ ¬AskHuman.
Else BRIEF (top 3 + recommendation + exact authority needed), RESEARCH_PROBE
(evidence blocker), or REWORK.

## 7. AskHuman law

`AskHuman = AuthorityRequired ∨ IntentAmbiguity ∨ ConsequentialIrreversibility ∨
MaterialUncertainty ∨ NoClearDominantOption`.

## 8. Provisional verification (R5)

Windows (hypotheses): reversible 24h · financial 7d · irreversible 30d ·
rights-adjacent 90d. Verification states: PASS / PASS_PENDING_WINDOW / FAIL /
REOPENED / ESCALATE. PASS is provisional until the window closes; later evidence
reopens. No irreversible learning promotion on an open window with material
delayed harm. Calibration: `error_V = |ΔV_pred − ΔV_actual|`.

## 9. SmartLedger — one substrate, two typed streams

Decision receipts (§10A fields) and contribution receipts (§10B fields) share one
canonical event/evidence substrate; semantics, writers, access rules differ.
Receipts bind `calculusVersion` + `configHash` (FNV-1a of canonical config) so
weight/rubric manipulation is detectable by independent recomputation.

## 10. Contribution law (candidate)

Never score human worth. `Activity ≠ Value`: likes/comments/shares earn zero by
themselves; they earn only through downstream verified value via attribution
receipts (10% of the reuse's CVS, hypothesis, with provenance link).
`CVS_j = sign(ΔV_j) × 9 × (Quality×Relevance×Verification×Impact×Novelty)^(1/5)`
(candidate anti-spam formula). Profile stays multidimensional:
Contribution × Reliability × Conduct → Trust. **Authority ≠ Reputation**, always.

## 11. Flexible math

Every weight, threshold, τ, window, and normalization carries version + owner +
scope + evidence basis + calibration history + supersession lineage. Outcomes may
propose changes; nothing silently rewrites constitutional boundaries.

## 12. Reconciliation notes (R1–R6 patch → baseline)

- R1: baseline §6 defines the autonomy margin on V_safe (adopted); the patch's
  P_norm margin is retained for scheduling, not autonomy.
- R2: baseline §3's `clamp(Normalize(ΔV_actual), ±9)` adopted over the patch's
  clamp-only fallback; Normalize is versioned per §12.
- R4–R6, Pareto dominance, and provisional PASS are as patched.

## 13. Proof gate

Per §15 of the baseline: 9.5-ready requires R1–R6 definition-complete ✓, machine
schema ✓, deterministic reference passing ✓, adversarial tests ✓ (13 attacks +
bad baseline + weight manipulation + action splitting), receipt integration ✓,
cold-successor reconstruction ✓ (recompute MATCH), calibration-without-authority-change ✓,
multi-principal boundary ✓ (conflictingPrincipals / collective / jurisdiction gates).
10/10 remains unavailable until runtime integration + independent verification +
production evidence.
