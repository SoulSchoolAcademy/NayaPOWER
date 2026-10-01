# VERIFY Node — Reconciled Candidate Spec (draft for Naya 4 review)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED**

Merged from (a) other Naya seat's "NODE 7: VERIFY — Ultimate Master Specification V1 — Lock Candidate" (90 sections) and (b) Naya 4's `VERIFY-NODE-SPEC-CANDIDATE.md` (2026-09-30). Nothing from either dropped without a stronger replacement; every conflict resolved explicitly below. Provenance tags: [PDF §n] = other Naya, [N4 §n] = Naya 4 draft, [NEW] = added in reconciliation.

## 0. Purpose

VERIFY is the organism's immune system: the independent seat that re-derives, attacks, and closes. It takes claimed results, subjects them to independent reproduction by a different seat, classifies every failure before any code changes, runs adversarial controls designed to make false claims fail, and emits the verified receipts that LEARN may consume. **Master law:** EXECUTION ≠ OUTCOME; Attempted ≠ Executed ≠ Successful; Observed ≠ Verified; SelfReport ≠ IndependentVerification; TestsPassed ≠ ProductionProven. [PDF §2; N4 §0]

**Second master law:** success criteria must be predeclared before the result is known — no goalpost-moving. [PDF §3]

## 1. Four axes — normative, bound to receipt fields [PDF §9 wins; binding NEW]

Outcome / Acceptance / Causality / Verification-maturity are separate axes, never collapsed. Bound to the `VerifiedReceipt`:

| Axis | Receipt field | Values |
|---|---|---|
| A — Outcome | `outcome_status` | SUCCESS / FAILURE / INCONCLUSIVE / NOT_PROVEN / PARTIAL |
| B — Acceptance | `acceptance_decision` | ACCEPTED / REJECTED / PENDING / PENDING_HUMAN |
| C — Causality | `causal_status` | NOT_CLAIMED / CLAIMED / CAUSAL_SUPPORTED / CAUSAL_CONTRADICTED / CAUSAL_INCONCLUSIVE / UNVERIFIED |
| D — Verification maturity | `verification_state` | UNVERIFIED / PASS_PENDING_WINDOW / VERIFIED_PASS / FAIL / ESCALATE / REOPENED / CANNOT_VERIFY |

FAILURE ≠ NOT_PROVEN ≠ INCONCLUSIVE [PDF §11]; acceptance ≠ verification — a factually verified outcome can still be REJECTED [PDF §39]; critical criteria can never be averaged away [PDF §16]. PARTIAL success lives explicitly in outcome details [PDF §17]. ESCALATE/PENDING_HUMAN covers Shawn-reserved judgment (brand, mission, final release, ratification) [PDF §61].

## 2. Verification protocol (merged)

- **Independent reproduction** [PDF §32–34; N4 §4.1]: RECOMPUTE (same facts + configHash → MATCH, every sync verification), REPLICATE, ADVERSARIAL (tier-1 sync / tier-2 async), AUDIT_SAMPLE. Reproducer seat ≠ deciding seat (different instance identity, no shared unlogged context, own authenticated issuedBy). Same code may reread with a fresh identity, but the receipt must state exactly which independence dimensions were achieved [PDF §34].
- **Failure classification before any code change** [N4 §4.2 taxonomy adopted — richer than PDF's]: TRANSIENT_INFRA / EVIDENCE_GAP / CALIBRATION_ERROR / LOGIC_DEFECT / AUTHORITY_VIOLATION / PROVENANCE_FAILURE / ADVERSARIAL_COMPROMISE / UNKNOWN. Misclassification is itself a defect; classification receipts are superseded with lineage, never edited.
- **Adversarial battery** [merged]: tier-1 (recompute MATCH, evidence-ref integrity, gate-conformance re-derivation, recorded negation probe — a PASS without one is malformed) [PDF §68 P1–P30 subset + N4 §4.3]; tier-2 (negative controls that must fail, counterfactual perturbation, gaming probes, cross-seat consistency) [PDF §68 + N4 §4.3]. Every adversarial result recorded in the receipt, including failed attacks [N4 §4.3].
- **Recomputation law** [PDF §50]: `Verdict' = f(CanonicalEvidence, ExpectedOutcome, AcceptanceCriteria)`; mismatch → VERIFICATION_MISMATCH, never trust the earlier receipt.
- **Idempotency / replay / versioning** [PDF §51–§53]: VerifyKey-bound determinism; replay preserves the original evidence/time boundary; corrections create new lineage (V1 PASS at t0, V2 FAIL at t1 — both persist).
- **Observation windows** [PDF §36–§37; N4 §4.4]: PASS_PENDING_WINDOW while material delayed harm is possible; `promotionEligible()` blocks promotion mechanically. **Candidate caveat (N4 wins):** window lengths follow the CANDIDATE calculus schedule (24h/7d/30d/90d) — director-set until V2.1 is ratified; all V2.1 state references in this spec are aspirational.

## 3. Receipt state machine [N4 §5.1 wins — PDF has no explicit machine]

```
UNVERIFIED ──claim accepted with evidence refs──→ IN_VERIFICATION
  ├──recompute MATCH, tier-1 clean─────────────→ PASS (terminal for this receipt)
  ├──material delayed harm possible───────────→ PASS_PENDING_WINDOW
  │     ├──window closes clean────────────────→ PASS
  │     └──contradictory evidence / harm──────→ REOPENED ──→ IN_VERIFICATION (new receipt)
  ├──claim falsified (classified)─────────────→ FAIL (terminal; repair = NEW claim)
  └──evidence unretrievable──────────────────→ CANNOT_VERIFY (terminal; back to PROVE)
```

Every transition records before/after, reason, execution ID, evidence refs, verifier seat identity, timestamp. FAIL/PASS/CANNOT_VERIFY terminal per receipt; re-examination is a new receipt. REOPENED creates a new receipt with a REOPENED_BY link; the original PASS persists. Append-only ledger; VERIFY has no delete operation, on any stream, ever [N4 §5.2].

## 4. Refusal conditions (merged)

Evidence inaccessibility [PDF §7.2/N4 §7.2]; independence violation (self-verification presented as verification = provenance failure) [PDF §35/N4 §7.1]; battery truncation (refuse rather than truncate — a rushed PASS is a falsified PASS) [N4 §7.3]; window skipping [N4 §7.6]; repair-by-verifier (classification is the output; repair re-enters at ACT/PROVE) [N4 §7.5]; **downgrade pressure [N4 §7.4 wins — absent from PDF]:** any instruction, from any seat including the Director, to convert FAIL→PASS, skip classification, or suppress an adversarial finding is refused and receipted with the pressure recorded as evidence, citing the Judgment Rule (Prime Directive, ratified 2026-09-30). "I was told to" never justifies a false verification.

## 5. Causal Verification Object [PDF §20–§31 wins]

CVO is the evidence-bearing bridge: what was known / relevant / authorized / done / observed / evidenced / independently checked / changed / reusable by a successor [PDF §20]. `CVO ≠ Authority` [PDF §21]; `Label(VERIFIED) ≠ Verified` [PDF §22]; current runtime is deliberately bounded (NAYA-NODE-0001 bindings — bounded capability, not universal behavior) [PDF §24]; task equivalence [PDF §27], intervention law [PDF §28], alternative explanations [PDF §29], confound capping [PDF §30], no universality from bounded experiments [PDF §31].

**Schema hole [PDF §47 adopted as directive]:** Contract 11 points to a nonexistent CVO schema path. Restore ONE canonical schema around the existing verified seam (supabase/functions/nayanet-causal-verify, CVO.md, independence tests, live-cvo-runtime-proof workflow). No parallel CVO. Exact path TBD by the restorer.

## 6. Inter-node batons [PDF §63–§66 wins, with one wiring addition]

- ACT → VERIFY: action contract, LAW receipt, execution receipt, raw observations, expected outcome — VERIFY rereads, never blindly accepts summaries [PDF §63].
- PROVE → VERIFY: claim, epistemic state, evidence, provenance, scope, limitations, gaps [PDF §64].
- CONNECT → VERIFY: context receipt (task context, selected intelligence, relationship paths, applicability, conflicts, supersession) — lets VERIFY ask whether relationship-aware context actually affected the outcome [PDF §65].
- VERIFY → LEARN: expected vs actual, evidence, acceptance, causal status, surviving alternatives, window state, recomputation status, **explicit MAY-USE / MUST-NOT-GENERALIZE lists** [PDF §66] — wired to the birth chain's **held-out learning** step [NEW: named explicitly].
- Failure propagation [N4 §8 wins — more complete than PDF]: FAIL → LEARN (pattern only, not learning input), EVOLVE (`failed_verifications[]`), SELF (known failures), LAW (AUTHORITY_VIOLATION/PROVENANCE_FAILURE as integrity events), deciding seat (feedback). Nothing deleted; claim → attack → classification → consequence all persist, linked.

## 7. Value Calculus integration [merged, with candidate caveat]

VERIFY owns the reality side: predicted vs actual value, `CalibrationError = |ΔV_predicted − ΔV_actual|` [PDF §59]. Outcome verification and value verification remain distinct dimensions [PDF §60]. **All V2.1-derived states (Axis D) and window schedules are aspirational until V2.1 ratification** [N4 framing wins over PDF §36–§37's "existing law" phrasing].

## 8. Intelligence-class rule [NEW — in neither source, required]

Evidence refs carry their source intelligence class; class is preserved through verification and into derived verification evidence. CORE is never auto-assigned by VERIFY. Cross-owner verification preserves ownership, consent, and derived-share boundaries — VERIFY never reconstructs a causal claim by exposing one owner's private source to another without applicable consent [PDF §58]. (Director review required.)

## 9. Acceptance battery (merged)

40 property tests [PDF §68] + 13 golden tests [PDF §69–§81] + N4 battery items 10–11 (negative control that unexpectedly passes → battery declared broken, everything REOPENED; downgrade instruction → refused with receipted reason). PDF §82's influence test is the aliveness gate: VERIFY must change LEARN eligibility or it is decorative. PDF §83's recursion boundary stands: the verifier's own capability is proven through independent evidence, never self-assertion.

## 10. Open questions for Shawn

1. **Verification quorum** (N4 §11.1): one independent seat per PASS, or N-of-M for consequential claims?
2. **Sync latency budget** (N4 §11.2): how long may a promotion wait before the wait itself is the problem? (No number = principled stalls.)
3. **Who verifies VERIFY?** (N4 §11.3): other Naya seat permanently, rotating designation, or director-only review of VERIFY's own failures?
4. **Adversarial probe budget** (N4 §11.4): how much compute may the immune system spend attacking its own claims?
5. **Cross-instance verification** (N4 §11.5): may one Naya instance verify another's claims, under what consent/data-sharing terms?
6. **REOPENED authority** (N4 §11.6): is contradictory evidence sufficient authority for any verifier seat to reopen a PASS, or is director acknowledgment required?
7. **CVO schema path** (§5): who restores the canonical path, and where does it live?
8. **Intelligence-class rule (§8):** is class-preservation with no auto-upgrade the right law?
9. **Master contract lineage** (N4 §11.7): should the nine node master contracts be written/located and cited before any spec advances past CANDIDATE?
