# LEARN — Reconciled Candidate (merged draft for Naya 4 review)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED**

Draft only. This document merges two sources into one candidate LEARN specification.
It creates no obligation, changes no code, and authorizes nothing until Shawn
ratifies it through the governing process. Do not implement from this draft
without ratification.

**Sources merged:**
- (a) `~/workspace/nine-node-specs/LEARN-NODE-SPEC-CANDIDATE.md` — Naya 4's draft, red-teamed and fully reconciled (all 17 findings FIXED, 8.5/10). This is the **base**: every one of its reconciled revisions stands; nothing regresses.
- (b) The other Naya's `NayaPOWER___NODE_8__LEARN.pdf` ("Ultimate Master Specification V1 — Lock Candidate", 93 sections) — the normative law source.

**Merge rule:** the base supplies the machine bindings (typed contracts, gates, named functions, ratification conditioning); the PDF supplies normative laws, formalisms, and test batteries. Nothing from either source is dropped without a stronger replacement — the coverage map below proves it. Contradictions are resolved explicitly, base winning wherever it carries a machine binding the PDF lacks.

---

## Amendments adopted from the PDF (candidate revisions to the base)

**A1. Four learning axes (PDF §6).** Adopt as the terminology frame for base §8: every learning carries four independent axes — *epistemic state* (CANDIDATE/TESTING/SUPPORTED/VERIFIED/CONTRADICTED/REJECTED/SUPERSEDED), *adoption state* (INACTIVE/ACTIVE/RETIRED/ROLLED_BACK), *transfer maturity* (UNTESTED/SOURCE_TASK_ONLY/HELD_OUT_RELATED_SUPPORTED/BOUNDED_GENERALIZATION/COMPOUNDING_SUPPORTED/SUCCESSOR_RETAINED), *applicability* (APPLICABLE/NOT_APPLICABLE/UNKNOWN per Reuse Graph V2). Rationale: prevents one ambiguous word (e.g. ACTIVE) meaning five things. Base §8's lifecycle is retained as the transition machine *across* these axes.

**A2. Generalization ceiling (PDF §11).** Add to base §3.3 as an explicit rule: `Scope(L_candidate) ⊆ S_verified-source` unless additional transfer evidence justifies expansion. Scope expansion is earned, never inferred from confidence. This is the anti-evidence-laundering inequality (`L_strength ≤ Evidence_strength`, PDF §10) made structural.

**A3. Reconciliation taxonomy (PDF §12–13).** Adopt the classification for base §6.3: every candidate is classified NEW / EXACT_DUPLICATE / REFINEMENT / SCOPE_NARROWING / SCOPE_EXPANSION_CANDIDATE / CONTRADICTION / CORRECTION / SUPERSEDES / PARALLEL_DIFFERENT_SCOPE / UNKNOWN. Duplicate law: `L_n ≡ L_e` (same lesson, owner, scope, evidence lineage) → REUSE / ADD EVIDENCE, never a second canonical learning.

**A4. Validity envelope (PDF §28).** Extend base `ApplicabilityClause` with `E_L = (Owner, TaskClasses, Capabilities, Environment, Time, Dependencies, Limitations)`. A learning steers behavior only inside its envelope; outside, applicability is UNKNOWN unless separately verified. `HistoricallyVerified ⇏ CurrentlyApplicable` (PDF §29) — CONNECT and LEARN cooperate on temporal validity; stale learning is a first-class detection (REGRESSION_CANDIDATE per PDF §30, feeding base §3.5).

**A5. Failure/success/correlation learning discipline (PDF §32–35).** Adopt as extraction guidance for base §1.4: `OneFailure ⇏ UniversalRule` (scope stays evidence-bounded); success requires identifying the *causally responsible* part of the approach (anti-superstition); correlation without VERIFY support is retained only as ASSOCIATION CANDIDATE with explicit uncertainty — never promoted to causal lesson.

**A6. Lineage + checkpoint reconstruction law (PDF §36–38).** Strengthen base §5 provenance: the canonical lineage EXPERIENCE→EVENT→BLOCK→PROVENANCE→RELATIONSHIP→ACTION→OBSERVATION→OUTCOME→VERIFY→CANDIDATE→HELD-OUT→VERIFIED LEARNING is required; `CurrentStateMovement ≠ HistoricalEvidenceLoss` — when the checkpoint advances past a candidate's checkpoint, reconstruct from the immutable intelligence-commit receipt, never rewrite history; `Checkpoint ≠ Learning`.

**A7. Test-contamination fields (PDF §51).** Add to base §11.2 `HoldoutPlan`: `source_task_refs`, `holdout_task_refs`, `test_created_before_outcome?`, shared-evidence declaration. A held-out task designed from the verification example is contaminated and invalid.

**A8. Compounding attribution questionnaire (PDF §52–54).** Extend base §3.5/§3.6: a compounding claim must answer — which earlier learning was used, which later learning depended on it, what changed, what outcome improved, how much is attributable, did unrelated behavior stay stable, did a cold successor retain the chain. `LaterIsBetter ⇏ EarlierLearningCausedIt`.

**A9. Governance-change routing (PDF §61).** Adopt as base §4.3 corollary: a verified lesson *"policy X caused recurring friction"* may produce a *governance change proposal*; only the proper authority ratifies a new policy. Lessons may not silently rewrite governance.

**A10. Anti-metric-gaming posture (PDF §69–72).** Add to base §3: no magical "Learning Score" — a learning is evaluated through explicit properties (source verification, behavioral/outcome effect, applicability, negative transfer, stability, regression, value effect, successor retention); `MetricImprovement ⇏ MissionImprovement`; learning efficiency is an optimization metric only *after* truth, privacy, authority, and safety gates pass.

**A11. Production-proven definition for LEARN (PDF §89).** Adopt into base §11 (what this spec is not): a declared LEARN capability is production-proven only with exact canonical source + deployed runtime parity + real candidate + canonical VERIFY evidence + independent validation + reconciliation + promotion + block lock-in + relationship lock-in + independent reread + related held-out reuse + unrelated refusal + regression-negative + cold-successor reuse + no authority inheritance. Until then it is CANDIDATE machinery.

**A12. Pre-verification investigation candidates (PDF §3).** Adopt narrowly: an unverified experience may create an *investigation placeholder* (state CANDIDATE, `verification: PENDING`), but it may NOT enter scoring (§3), promotion (§3.4), or the TESTING serving path (§6.2) until a verified receipt arrives. This preserves base §1.1 ("never consumes unverified") for all consequential transitions while gaining the PDF's early-capture concept. `CandidateCapture ≠ VerifiedLearning`.

---

## Contradictions resolved (base wins where it carries the machine binding)

**C1. Calculus status.** PDF §§43–46 treat the Value Calculus as settled law; base §3.4-condition-0 requires a RATIFIED `calculusVersion` for autonomous promotion (F04 fix). **Base wins.** The PDF's recalibration semantics (§§44–46) are adopted as specified behavior *under a ratified calculus*; while V2.1 is CANDIDATE, all promotions route to BRIEF.

**C2. Graph-contract touch.** PDF §41 proposes relationship types in candidate language without referencing the RATIFIED V2 contract; base §6.1 flags them as a GRAPH CONTRACT AMENDMENT PROPOSAL (F01 fix). **Base wins.** PDF §41 is reframed: the five types are amendment proposals; implementation maps to ratified equivalents or holds.

**C3. Extraction.** PDF §10 assumes extraction; base §1.4 contracts it (F05 fix). **Base wins** — A12's investigation placeholder is the only PDF concept added.

**C4. Axes vs state machine.** PDF §6 (four axes) vs base §8 (lifecycle). **Merged:** axes are the dimensions, the state machine is the transition law across them (A1).

**C5. Promotion gate phrasing.** PDF §16's `V∧P∧R∧A∧B∧N∧C` vs base §3.4. **Subsumed:** V→§1.1 verified receipts; P→§5 provenance; R→§6.3 reconciliation; A→applicability (A4); B→§3.6 behavioral attribution; N→§11.2 negative transfer; C→§6.3 contradiction handling. The PDF's gate is the mnemonic; the base's §3.4 + §11 named functions are the machine.

**C6. Calculus self-mutation.** PDF §5 ("never own automatic Value Calculus mutation") vs base §2 `RECALIBRATION` kind (propose weight/threshold changes). **No contradiction:** both permit *candidates*, both refuse *automatic* mutation. Base §4.7/§4.8 govern.

---

## Coverage map (nothing dropped)

| PDF section(s) | Disposition |
|---|---|
| §0–2 master laws (STORED≠LEARNED, behavioral proof) | Already in base §0/§8; retained |
| §3 pre-verification candidates | A12 (narrowed) |
| §4–5 owns / never-owns | Already in base §1.3/§4.3–4.7; retained |
| §6 four axes | A1 |
| §7 ACTIVE≠UNIVERSAL | Already in base §6.2/§8; retained |
| §8 learning object, §62–64 receipts/reason codes | Already in base §2/§5/§7; retained |
| §9 VERIFY→LEARN baton | Already in base §1.1; retained |
| §10 extraction + strength ceiling | A2 + C3 |
| §11 generalization ceiling | A2 |
| §12–15 reconciliation/duplicate/contradiction/correction | A3; already in base §6.3 |
| §16 promotion gate | C5 |
| §17 promotion-seam hole | Corroborates base F04/F05 fixes; retained as cited evidence |
| §18 no caller-supplied verified learning | Already in base §3.4; retained |
| §19–25 held-out / negative transfer / overgeneralization | Already in base §11.2/§3.6; retained |
| §26–28 applicability structure + envelope | A4; C2 for contract touch |
| §29–31 stale/regression/rollback | A4 (stale law); already in base §3.5/§6.3/§7 |
| §32–35 failure/success/correlation | A5 |
| §36–39 lineage/checkpoint/KNOW-home | A6; already in base §5/§6 |
| §40–42 KNOW/CONNECT/EVOLVE boundaries | Already in base §1.2/§6.1/§7.1; retained (C2) |
| §43–48 calibration/recalibration/prediction | C1/C6; already in base §2/§3.5 |
| §49–51 learning rate/overfitting/contamination | A7; already in base §11.2 |
| §52–55 compounding | A8; §55's honesty retained |
| §56–57 successor learning ≠ authority | Already in base §1.2/§5; retained |
| §58–59 privacy/cross-owner | Already in base §6.1 owner_scope/consent; Q4 retained |
| §60–61 learning/authority/governance | A9; already in base §4.3/§4.4 |
| §65–67 idempotency/concurrency/hash | Already in base §5; retained |
| §68–69 threat model/reward hacking | Already in base §7; A10 |
| §70–73 quality/efficiency/compression | A10; already in base §5 |
| §74–75 state machine/maturity | A1; already in base §8 |
| §76–86 property + golden tests | Adopted into base §9 acceptance battery (P1–P40 map to existing 12; golden tests added as §9.13–9.21) |
| §87–89 influential/verified/production-proven | A11; already in base §9 |
| §90 current runtime truth | Noted as branch-specific evidence, not spec — retained as cited context |
| §91–93 organism/equation | Preamble material; retained as §0 context |

---

## Open questions for Shawn (director decisions required)

Base §10 Q1–Q5 are retained unchanged (τ_scope proposals; stricter evidence floors; rollback authority — still PROVISIONAL; cross-owner learnings; RECALIBRATION scope). The merge adds:

**Q6. Intelligence classes for learnings.** The five classes are RATIFIED law and neither source binds learnings to them. Should a learning carry a class, and is CORE-class learning ever promotable without your direct word? (Draft position: learnings default to the class of their source intelligence; CORE excluded from autonomous promotion — needs your confirmation.)

**Q7. Learnings that touch identity/personality.** A verified learning proposing a change to SELF's identity state or an Awesome Code trait — which authority? (Draft position: routes to BRIEF/governance like any constitutional-adjacent touch per §4.4; personality is subordinate to law but director-owned. Needs your confirmation.)

**Q8. Investigation-candidate visibility (A12).** Pre-verification placeholders are inert and unscored — should they be visible to other nodes (e.g., KNOW serving) or LEARN-internal only? (Draft position: LEARN-internal only until a verified receipt arrives.)

---

*Merged 2026-09-30 by Naya 4 for director review. Base revisions (Appendix A of the base draft) all stand. PDF adoptions above are candidate revisions — CANDIDATE, NOT RATIFIED, NOT MERGED.*
