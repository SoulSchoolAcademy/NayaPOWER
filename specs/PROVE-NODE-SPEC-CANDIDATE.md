# PROVE Node — Reconciliation Draft (MERGED candidate)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED**

Merged from: (a) other Naya's `NayaPOWER___NODE_5__PROVE.pdf` (83 sections) and
(b) Naya 4's `PROVE-NODE-SPEC-CANDIDATE.md` (8.5/10; all 16 red-team findings reconciled, App. A).
Nothing from either source dropped without a stronger replacement.
Contradictions resolved explicitly below. Draft for Naya 4's review — not final.

**Heads-up:** the PDF is the strongest spec received — no F01-class contract violation,
honest boundaries (§77), formalized circular-proof and causation machinery. The merge
mostly *adds our already-reconciled findings* (floors, forecast crossing, stakes) to her machinery.

---

## Merge decisions (whose version won and why)

| Area | Winner | Why |
|---|---|---|
| Claim/evidence objects | PDF (§§7/10) | Richer schemas (limitations, unresolved_gaps, counterevidence_refs, directness/independence/reproducibility). |
| Claim classes | PDF (§8) | 19 classes (EXISTENCE…SUCCESSOR_CONTINUITY); my claim types map onto them. |
| Proof obligations | **Merged**: PDF §9 + my F02/F07 | PDF's `O(c)` ladders win; ADD my evidence floors (V2.1 DATA_FLOOR k=5/20 keyed by class/stakes) and stakes-assignment rule — the PDF's biggest gap. |
| Admissibility | **Merged**: PDF §11 + my G-gates | PDF's `A(e,c)` 6-gate formula wins; my G5 anti-theater (fresh derivation path) and G7 staleness merge in. |
| Epistemic states | **Merged** | PDF's dual-axis model (§§26–28) wins structurally; my F01 reconciliation stands: PROVE's ceiling is SUPPORTED, never VERIFIED; ladder mapped onto ratified enum (App. A). |
| Strength | **Merged**: PDF §12 + new rule | ADD the missing combination rule: `claim_strength ≤ min(strength of critical-dimension evidences)` (scorecard finding #2). |
| Refusals | Mine (§4) | Eight named refusal conditions (incl. IMPLEMENTED-as-VERIFIED, floor-never-lowered-for-urgency) are the reference bar; PDF's equivalents merge in as rows. |
| Anti-laundering | **Merged**: PDF §31 + my F15 | PDF's caller-supplied-content rejection wins; my §4.3 method-finding kept WITH F15 scoping (where it lives, who sees it, clearance). |
| Forecast crossing | Mine (F03) | PDF silent; my reconciled forecast-crossing section stands. |
| VERIFY prerequisite | Mine (F04) | Any sealed receipt (not L4) is VERIFY's prerequisite; L4 gates CONNECT crossing only. |
| Provisional windows | **Merged** | PDF §46 (PASS_PENDING_WINDOW) + my F06 (cap at L2 / bind valid_until to window close) — consistent. |
| Raise-level | Mine (F08) | PDF silent; raising must be receipted, reasoned, bounded. |
| Materiality | Mine (F09) | Admit the hybrid: binary gates with a scored materiality pre-step. |
| Fresh-path independence | Mine (F11) | PDF §29 says "fresh derivation path"; my independence criterion (different code path/agent/blinded inputs, recorded) makes it checkable. |
| Battery invalidation | Mine (F12) | PDF silent; sealed receipts vs battery changes need the rule. |
| Seal-to-cross race | Mine (F14) | Boundary re-validation (seal timestamp + challenge check) at CONNECT crossing. |
| Briefing mechanics | Mine (F16) | Which node briefs, format, record, Director response options. |
| Receipt | **Merged**: PDF §49 + mine | PDF's schema wins; add my recompute/independence fields. |
| Ledger | PDF (§47) | Typed events on the existing Smart Ledger substrate ("does not create another ledger"). |
| Causation/counterfactual | PDF (§§43–44) | Formalized; correlation⇏causation + CONTROL/TREATMENT pattern. |
| Circular proof | PDF (§54) | Evidence dependency graph, `ExternalRoot(c)=∅ ⇒ IndependentSupport=0`. |
| Triangle wiring | PDF (§78) | PROVE→CONNECT→VERIFY→LEARN + direct PROVE→VERIFY + ACT→VERIFY; consistent with my §4.2. |
| Baton | **Merged**: PDF §30 + fix | ADD `contract_version` (scorecard finding #3). |
| Golden/property tests | **Union** | PDF's 9 golden + 30 invariants; my battery's unique cases appended. |
| Production-proven | PDF (§§45/76) | `GreenCI ≠ ProductionProven`; node-5 self-proof checklist. |

## Merged spec skeleton (sections)

1. Responsibility & PROVE/VERIFY split — my §1 + PDF §§6/78.
2. Claim objects & 19 classes — PDF §§7–8 (+ my claim-type mapping).
3. Proof-obligation law — PDF §9 + floors (F02) + stakes (F07) + forecast crossing (F03).
4. Admissibility & gates — PDF §11 + my G1–G7 (materiality hybrid F09).
5. Evidence strength & combination — PDF §12 + ceiling rule.
6. Epistemic/implementation/lifecycle axes & transitions — PDF §§26–29 (F01 mapping intact).
7. Refusal conditions — my §4 (8 refusals) + PDF rows.
8. Anti-laundering & method findings — PDF §31 + F15 scoping.
9. Causation, counterfactuals, circularity — PDF §§43/44/54.
10. Independence (sources, verifiers, derivation paths) — PDF §§16–18/§20 + F11.
11. Authority boundaries — PDF §§33–35 + my §1.4 (proof grants nothing; never touches authority).
12. Temporal: windows, staleness, prematurity — PDF §46 + F06.
13. Receipts & ledger — PDF §§47–49 (+ recompute fields).
14. Idempotency & hash law — PDF §§50/52.
15. Batons & handshakes — PDF §§30/32/36–40 (+ contract_version).
16. V2.1 integration — PDF §§41–42 (Value≠Truth; Confidence≠Truth).
17. Seal, crossing & VERIFY prerequisite — F04 + F14.
18. Battery ownership & invalidation — F12.
19. Acceptance battery — union tests; cold-successor proof (PDF §72); influential bar (PDF §74).
20. Production-proven for Node 5 — PDF §76.
21. What this spec does NOT do — my §11 + PDF §77 boundary list.
22. Open questions — union (below).

## Open questions for Shawn

1. Evidence floors: V2.1 DATA_FLOOR (k=5/20) is still CANDIDATE math. If Shawn ratifies stricter floors for proofs than learnings (LEARN §10.2 question), PROVE's constants change — accept the coupling?
2. Ownership (F13): who answers for a PROVE verdict — named principal, or the Director by default? Single-instance PROVE+VERIFY staffing: separate checks or acknowledged single check?
3. Method-finding retention (F15): keep the claimant method-finding mechanism with the F15 scoping, or drop it as authority-adjacent?
4. My draft's §10 open questions carry over (§10.1/10.2/10.4/10.5: forecast reporting format, stricter proof floors, battery ownership, method-finding retention).
5. Birth-chain claim templates: add worked §8-class mappings for the eight birth-acceptance steps, or leave to the build?
