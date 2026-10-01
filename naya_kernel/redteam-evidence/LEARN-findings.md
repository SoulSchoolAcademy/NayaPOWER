# Red-Team Review: LEARN Node Spec (CANDIDATE)

- **Node:** NAYA-KERNEL-LEARN
- **Spec file:** `~/workspace/nine-node-specs/LEARN-NODE-SPEC-CANDIDATE.md`
- **Review date:** 2026-09-30
- **Reviewer role:** read-only adversarial reviewer (no edits made to the spec)
- **Verdict summary:** The LEARN draft is the strongest of the node specs in skeleton — the seven refusal conditions are genuinely well-formed, the provenance section (§5) is the best in the set, and the author honestly surfaced four of the five known open questions (Q1, Q2, Q4, Q5). It does NOT deserve its ~9.5/10 draft score. Adversarial review finds three hard internal contradictions (auto-quarantine vs §4.7, Q5-draft vs §4.7, asserting autonomous rollback while asking whether it should be autonomous), the spec's core function (receipt→candidate extraction) is unspecified, its promotion authority is bootstrapped on an unratified calculus, and two load-bearing functions are named but never defined. It earns a 7.0/10: a good contract outline with real holes, not a near-final bar.

---

## FINDINGS

### LEARN-F01 — Extends the RATIFIED graph V2 contract without flagging it as a constitutional touch
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §6.1 amendment-proposal flag; Appendix A)
- **Evidence:** §6.1 binds LEARN to the graph contract "v2.0 (RATIFIED 2026-09-30)" and introduces three additions: `relationship_type = LEARNED_FROM`, `epistemic_state = LEARNED / CONTRADICTED / SUPERSEDED / INVALIDATED`, and `reason_codes` including `LEARN_PROMOTED`. The lineage section names the V2 contract as RATIFIED. Adding new enum values to a ratified contract is a change to ratified law — the spec never marks this as an OPEN constitutional touch or routes it through an amendment path; it presents the extension as a binding. The standing rule is that a CANDIDATE spec must not alter constitutional law; if it needs new enum values, that is an explicit proposal to amend the ratified contract and must be flagged.

### LEARN-F02 — §3.5 auto-quarantine contradicts §4.7's refusal of unsupervised self-modification
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §3.5 governed calibration loop + learned-vs-charter boundary; §4.7 scope clarification; Appendix A)
- **Evidence:** §3.5 mandates that sources with "persistently high calibration error" get their `U` "inflated automatically" so that "badly calibrated learning sources automatically drive their own future V_safe ≤ 0... without anyone having to decide to distrust them." §4.7 refuses any candidate proposing to change LEARN's own scoring machinery outside a ratified change, and §1.2 states LEARN "never self-applies a learning to its own scoring machinery without a ratified change." `U` is a direct input to `V_safe` (§3.2: `V_safe = ΔV_pred − U − Σ harmᵢ·pᵢ`) — automatically inflating `U` IS automatically modifying LEARN's scoring inputs. The spec both refuses unsupervised self-modification and mandates it. Additionally, §3.5 is mathematically underspecified: no threshold for "persistently high," no inflation formula, no rate, no owner of the per-source `U` registry, and no refusal path if the inflation itself is wrong.

### LEARN-F03 — §10 Q5's draft position contradicts §4.7
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §10 Q5 narrowed (Q dimensions excluded per §4.7); Appendix A)
- **Evidence:** §4.7 refuses candidates proposing to change LEARN's "scoring function." §10 Q5 states the current draft allows LEARN to propose changes to "the Q dimensions themselves" — the Q dimensions are the scoring function. The spec asks the director a question whose draft answer violates its own hard refusal condition. At minimum, §10 Q5's "current draft: all proposable" must be narrowed to exclude scoring-function surfaces (§4.7 scope) or §4.7 must be rewritten — they cannot both stand.

### LEARN-F04 — Promotion authority is bootstrapped on an unratified calculus
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §3.4 condition 0 (ratified calculusVersion gate); Appendix A)
- **Evidence:** §3.2–3.4 make autonomous promotion (§3.4 #6 `¬AskHuman`) depend entirely on Decision Value Calculus V2.1. The lineage section marks the V2.1 spec and the deterministic reference implementation as CANDIDATE. The spec therefore grants LEARN autonomous authority to persist behavior-changing rules on the strength of math that has not been ratified. If V2.1 changes at ratification (the red-team record notes uncalibrated defaults: dScale=1.0, tier thresholds, ★10=75,000 pts), LEARN's promotion thresholds (Q≥9.0, reversibility≥7, margin≥0.25, k=5/20, cAgg≥0.80, cCrit≥0.75) may all shift. The spec should condition autonomous promotion on a ratified calculus version and pin `calculusVersion` gating accordingly (§5 carries `calculusVersion`, but §3.4 does not require it to be ratified).

### LEARN-F05 — The core function — receipt→candidate extraction — is unspecified
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §1.4 extraction contract; Appendix A)
- **Evidence:** §0: "LEARN decides what should change because of a verified outcome." §8's state machine begins with "CANDIDATE — extracted, unscored." Nothing in the spec defines WHO or WHAT extracts a `LearningCandidate` from verified receipts: a deterministic transform? an agent judgment call? the auto-capture pipeline? Extraction is where learning actually happens — scoring only filters what extraction produces. An unspecified, possibly non-deterministic extractor undermines §5's cold-recompute guarantee (`recompute() → MATCH`) and acceptance #12, because a cold successor cannot reproduce which candidates were extracted in the first place. The spec needs an extraction contract: actor, determinism requirements, and whether extraction itself is scored/refused.

### LEARN-F06 — Load-bearing named functions have no definitions
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §11 (11.1 promotionEligible, 11.2 design_holdout, 11.3 recompute); Appendix A)
- **Evidence:** Three functions carry safety-critical semantics but appear with no signature, formula, or owner: `promotionEligible()` (§1.1, §3.4 #7, §7 — gates promotion from open-window receipts); `design_holdout()` (§7 — the stated detection mechanism for spurious correlation); `recompute()` (§4.6, §5, acceptance #7, #9 — the provenance-loss detector and the cold-successor test). §1.1 gestures at a definition ("no open window with material delayed harm (tail severity ≥ physical.severity threshold)") but never gives the `physical.severity` threshold value or the function's full predicate. A contract spec that names safety gates without defining them is not implementable and not testable against §9's acceptance battery.

### LEARN-F07 — Absolute trust in verified receipts: no defense against systematic VERIFY failure
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §1.1 cross-check hook + §7 systematic-bias row; Appendix A)
- **Evidence:** §1.1: "LEARN consumes only verified receipts... LEARN never consumes raw outcomes... If VERIFY has not spoken, LEARN has nothing to read." §4.6 covers forged/mismatched receipts, and §7 covers poisoning — but all poisoning defenses assume receipts are individually defective. There is no mechanism for the case where receipts are validly formatted, individually PASS, but systematically wrong (flawed verification design, correlated measurement bias, an entire cohort of outcomes mis-measured the same way). Since §3.3 counts `n` as "independent verified observations" but independence is asserted, not verified, a systematic VERIFY-level bias would sail through the evidence floor with n≥20. The trust boundary VERIFY→LEARN is total and one-directional; the spec needs at minimum a cross-check hook (e.g., calibration-error-driven receipt-source distrust extending to VERIFY sources, not just learning sources).

### LEARN-F08 — Self-reinforcing evidence: a promoted learning steers its own confirmation
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §3.6 attribution + §11.2 holdout control; Appendix A)
- **Evidence:** §3.5 measures `calibrationError = |ΔV_pred − ΔV_actual|` from "later verified outcomes" under the steered behavior. A promoted `BEHAVIOR_RULE` ("in context C, prefer action A over B") changes future behavior; future outcomes are then generated under the steered policy, so confirmation is partially self-caused (survivorship/Goodhart). §7 names `design_holdout` as the defense but never defines it (see F06), and §6.2 notes inertness "is itself evidence," which is the opposite direction (non-confirmation) but not a control for self-confirmation. The spec needs a defined holdout/randomization control before §3.5's calibration loop can be trusted.

### LEARN-F09 — CALIBRATION_UPDATE is a self-serving backdoor to future promotion
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §4.8 conflict-of-interest condition; Appendix A)
- **Evidence:** §2 defines `kind = CALIBRATION_UPDATE` ("adjust an estimator's uncertainty model"). §3.2: `V_safe = ΔV_pred − U − Σ harmᵢ·pᵢ`. A CALIBRATION_UPDATE that shrinks `U` for a learning source mechanically raises future `V_safe` for that source's candidates — the source buys its own future promotion. §4.7 refuses changes to LEARN's promotion rule/scoring, but shrinking `U` changes scoring *inputs*, which §4.7 does not cover and §3.5's auto-inflation only pushes the other direction. No refusal condition covers self-serving uncertainty reduction; this is a conflict-of-interest gap in the refusal taxonomy.

### LEARN-F10 — Sync/async behavior unspecified (GAP-A #3)
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §1.5 execution model; Appendix A)
- **Evidence:** §0–§1 give pipeline position (`... → VERIFY → LEARN → EVOLVE → SELF → ...`) but nothing states whether LEARN runs synchronously per verified receipt, in scheduled batches (relevant to the overnight push), on demand, or event-driven. This determines latency of learning availability, whether a burst of receipts can queue/flood the candidate pool, and what "autonomous" in §3.4 means operationally. GAP-A item (3) is unmet.

### LEARN-F11 — Node ownership unspecified (GAP-A #2)
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §1.6 ownership/accountability; Appendix A)
- **Evidence:** §5's `issuedBy` is an per-promotion agent identity "authenticated binding per master §10" — a provenance field, not an ownership statement. Nothing in the spec states which service/agent role operates LEARN, who is accountable for its runs, or who can invoke or halt a learning cycle. GAP-A item (2) is unmet. (Contrast: the spec is careful about `owner_scope` for *data*, §5/§6.1 — but node ownership is a different question and is absent.)

### LEARN-F12 — Causal attribution of ΔV_actual is asserted, not specified
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §3.6 causal attribution; Appendix A)
- **Evidence:** §3.5 and acceptance #10 require measuring "the actual behavioral delta" and "the delta is measured and attributed." No mechanism is given for attributing an observed ΔV to the retained learning versus confounders (other learnings promoted in the same window, environment drift, policy changes by other nodes). Without an attribution method, `calibrationError` is uncomputable in principle, and §3.5's auto-quarantine (F02) would fire on noise. The project's own "CAUSAL VERIFY" pipeline stage (standing memory) is exactly the missing machinery; the spec should either reference it or admit the gap.

### LEARN-F13 — NEEDS_EVIDENCE pool has no retention or capacity bound (candidate explosion)
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §3.3b pool lifecycle; Appendix A)
- **Evidence:** §3.3: a candidate below the evidence floor is "recorded with full provenance and held... visible, inspectable, inert... may accumulate further verified receipts until it clears the floor." No retention policy, no capacity bound, no pruning rule, no staleness criterion. Over long operation the pool accumulates every near-miss candidate forever — the learning-candidate-pool analog of the failure mode the spec otherwise guards against. The spec needs a pool lifecycle: max size, evidence-staleness expiry, and whether expired candidates are deleted (in tension with §6.3's "never delete" posture — which currently applies to graph edges, not pool candidates; the distinction should be explicit).

### LEARN-F14 — Failure propagation to EVOLVE and pipeline stall behavior unspecified (GAP-A #7)
- **Severity:** MAJOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec new §7.1 boundary contracts; Appendix A)
- **Evidence:** §1.2 hands EVOLVE a typed `PromotionPackage`, and §7's failure table covers LEARN-internal failures only. Unspecified: (a) what validates a `PromotionPackage` on EVOLVE's receipt (schema validation? re-scoring? trust-on-receipt?); (b) what happens downstream if LEARN emits a defective package; (c) what happens to the pipeline if LEARN halts mid-extraction or mid-scoring — does VERIFY backpressure, do receipts queue, is there a dead-letter path? GAP-A item (7) is partially met internally but unmet at the node boundaries.

### LEARN-F15 — "Promote" is used for two different transitions (terminology ambiguity)
- **Severity:** MINOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §8 terminology note + §6.2 TESTING-live statement; Appendix A)
- **Evidence:** §3.4 ("the promotion rule") governs CANDIDATE→TESTING: §6.1 says "on promotion, LEARN writes the learning into the graph as a V2 edge" with `epistemic_state = LEARNED`. §8's state machine then shows TESTING→PROMOTED as a separate transition (window closes → edge LEARNED→VERIFIED). So "promotion" means both "candidate admitted to TESTING" and the machine state "PROMOTED." The substantive question this obscures: per §6.2, KNOW serves edges through the V2 selector "once written" — so a LEARNED edge with an open verification window is served to KNOW and steers behavior before its window closes. §4.5 ("patience is a safety property") permits this when delayed harm is immaterial (§3.4 #7), but the spec never states explicitly that TESTING-phase learnings are live in the serving path. This should be stated, not left to inference.

### LEARN-F16 — Safety thresholds duplicated between spec prose and calculus config
- **Severity:** MINOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §3.3/§3.4 config-key references; Appendix A)
- **Evidence:** §3.3–3.4 hardcode Q≥9.0 (`qAutonomy`), reversibility≥7, margin≥0.25, k=5/20, cAgg≥0.80, cCrit≥0.75. These numbers belong to the calculus config (pinned by `configHash` in §5). Hardcoding them in spec prose creates two sources of truth: if the config is recalibrated, the spec text is silently wrong, and `recompute()` (§5) would follow the config while a reader follows the prose. Thresholds should be referenced by config key, not restated as literals.

### LEARN-F17 — §7 asserts autonomous rollback while §10 Q3 asks whether it should be autonomous
- **Severity:** MINOR | **Status:** FIXED (reconciled 2026-09-30 ~19:05 PDT — evidence: LEARN spec §7 poisoning row PROVISIONAL + §10 Q3 cross-ref; Appendix A)
- **Evidence:** §7's poisoning row prescribes "`rollback_learning` via supersession" as the response, and §10 Q3's framing ("currently specified as autonomous when calibration failure is detected") confirms the draft takes the autonomous position. But Q3 is an open director question — the draft silently resolves it while asking it. The spec should mark the §7 rollback response explicitly provisional pending the Q3 decision, and state whether a superseding correction goes through the full §3.4 promotion scoring (it should, since it changes future behavior — currently unspecified).

---

## DRAFT SCORE: 7.0 / 10

**Justification.** Credits (why not lower): the seven refusal conditions are the best-structured in the node spec set and are internally motivated by the master contract; §5 provenance is genuinely strong (content-addressed evidence, configHash-pinned recompute, cold-successor test); the author surfaced four of the five known open questions explicitly (§10 Q1, Q2, Q4, Q5 — the autonomous-envelope and stricter-floors questions are present, not buried); §4.3/§1.3 honor AUTO-CAPTURE ≠ AUTO-RATIFY for authority; contradictions-preserved-never-overwritten is specified structurally (§6.3), not just asserted.

Debits (why not 9.5): three hard internal contradictions (F02 auto-quarantine vs §4.7; F03 Q5-draft vs §4.7; F17 autonomous-rollback assertion vs Q3); the spec's core verb — extracting candidates from receipts — has no actor or mechanism (F05); promotion authority rests on an unratified calculus (F04); two named safety functions are undefined (F06); no defense against systematic VERIFY bias (F07) or self-confirming learnings (F08); and two GAP-A items (sync/async F10, ownership F11) plus boundary failure propagation (F14) are missing. A 9.5 spec does not contain contradictions with itself. 7.0 reflects "strong outline, real holes."

**GAP-A checklist status:** (1) responsibility ✓ §1 | (2) ownership ✗ F11 | (3) sync/async ✗ F10 | (4) persisted transitions ✓ §8/§6.3 | (5) evidence ✓ §5/§3.3 | (6) authority envelope ~partial (candidate-level §3.4/§4.3, but node-invocation authority and rollback authority open — F17) | (7) failure propagation ~partial (internal ✓ §7, boundaries ✗ F14) | (8) cold reconstruction ✓-ish (§5, acceptance #9/#12; weakened by F05/F06).

## OPEN QUESTIONS that should become spec sections

1. **Extraction contract** (F05): who/what extracts candidates from verified receipts; determinism requirements; whether extraction is itself scored.
2. **Ratified-calculus gating** (F04): autonomous promotion permitted only under a ratified `calculusVersion`; behavior when the calculus is CANDIDATE (human-in-the-loop default?).
3. **Graph contract amendment proposal** (F01): formalize the LEARNED_FROM / LEARNED / CONTRADICTED / SUPERSEDED / INVALIDATED / LEARN_PROMOTED additions as an amendment to the ratified V2 contract, not a silent extension.
4. **Attribution method for ΔV_actual** (F12): how post-promotion behavioral delta is causally attributed to the learning before calibrationError can be computed.
5. **Holdout design** (F06/F08): define `design_holdout()` as the control for spurious correlation and self-confirmation.
6. **Pool lifecycle** (F13): retention, capacity, staleness, and the explicit boundary between "never delete graph edges" (§6.3) and pool candidate expiry.
7. **Rollback authority and scoring** (F17): provisional status pending director decision; whether superseding corrections pass full §3.4 scoring.
8. **Boundary contracts** (F10/F11/F14): sync/async model, node ownership/accountability, PromotionPackage validation on EVOLVE receipt, and LEARN-halt backpressure semantics.
