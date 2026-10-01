# CONNECT Node — Reconciled Candidate Spec (draft for Naya 4 review)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED**

Merged from (a) other Naya seat's "NODE 6: CONNECT — Ultimate Master Specification V1 — Lock Candidate" (90 sections) and (b) Naya 4's `CONNECT-NODE-SPEC-CANDIDATE.md` (2026-09-30). Nothing from either dropped without a stronger replacement; every conflict resolved explicitly below. Provenance tags: [PDF §n] = other Naya, [N4 §n] = Naya 4 draft, [NEW] = added in reconciliation.

## 0. Purpose

CONNECT decides what may be connected to what, under whose consent, and what context becomes relevant because of it — for knowledge inside one mind. It owns the connection boundary for the intelligent graph: the rules of what crosses and what never does. [N4 §0, narrowed per scope decision below]

**Master invariant:** RELATED ≠ RELEVANT ≠ APPLICABLE ≠ TRUE ≠ AUTHORIZED. [PDF §2]

## 1. Scope decision (reconciliation ruling)

**Winner: PDF's scope.** The master contract (`00-CONNECT-MASTER-CONTRACT-V1.md`) states CONNECT's responsibility as "relationships, graph context" (§1), with required functions `create_edge … reconcile_graph` (§3) and inter-node contract "KNOW owns objects. PROVE supports trust. VERIFY can establish CAUSED relationships. ACT consumes context" (§8). The PDF stays inside this. N4's draft extended CONNECT to own the NayaNET connection boundary (MIND_LINK handshakes, connection spaces, governed receiver, consent ladder, door rule) — **that extension exceeds the master contract's stated responsibility** and is not adopted as normative.

N4's NayaNET material is preserved verbatim as **Appendix A: Proposed extended surface** — CANDIDATE extension, not in the master contract, requiring an explicit director decision on who owns the NayaNET governed-receiver / mind-link boundary (options: CONNECT, LAW, or a separate surface contract). Nothing dropped; nothing smuggled into the normative core.

Cross-surface context (interfaces as projections, "door ≠ brain") is normative via [PDF §56], consistent with 0015.

## 2. Normative core (all [PDF], adopted)

- **Master law:** §2 invariant; §5 MUST NEVER OWN (incl. no second Value Calculus, no second graph, no second authorization engine); §10 `AUTHORIZED_BY(A,B) ⇏ LAW_AUTHORIZED(B)`; §6 one graph, not Graph-RAG #2.
- **Relationship object:** §7 canonical schema (relationship_id, source/target, type, owner_scope, epistemic_state, status, provenance, evidence_refs, created/observed_at, valid_from/until, supersedes_relationship_id, consent_ref, applicability, reason_codes).
- **Vocabulary:** §8 — the single ratified 22-type Graph V2 vocabulary is the source of truth; §9 family grouping is an interpretation layer, not a second vocabulary. **N4's invented types (CONNECTED_TO / MEMBER_OF / SHARED_WITH, N4 §10) are dropped** — connection-ness is expressed via existing types plus applicability/purpose metadata. [PDF wins: "do not maintain two vocabularies."]
- **Claim law:** §11 every material edge = Relationship + Provenance + Evidence + Scope + Time.
- **Epistemic/lifecycle separation:** §12–§13 (epistemic_state ≠ status; historical ≠ current).
- **Temporal law:** §14 formula; malformed time → fail closed; §60 TOCTOU (inspection recomputes with recorded selection time `ts`).
- **Owner-scope law:** §15 (traversal never outruns ownership; DERIVED_SHARED requires consent_ref ≠ null and must not leak the private source); §16 private-source ≠ private-derived-context.
- **Applicability:** §17–§21 — RELATED≠APPLICABLE, UNKNOWN≠APPLICABLE; **§19 two-stage model (EXCLUDED / VISIBLE_NON_STEERING / STEERING_ELIGIBLE) adopted as CANDIDATE interpretation requiring ratification** (explicit reinterpretation of ratified V2 semantics, not normative until ratified). Task-class law §21: no heuristic widening.
- **Hard graph gate:** §23 `Gr(e,q) = O∧S∧E∧P∧T∧C∧A∧R`, fail-closed; §24 state precedence BLOCKED > UNKNOWN > FAIL > PASS, no implicit UNKNOWN→PASS.
- **Traversal:** §26 bounded, every hop independently gated; §27 no implicit transitive truth; §28 composition must be explicit; §29 cycle-safe; §30 bounds are implementation values, not constitutional values.
- **Supersession:** §31–§33 — preserved history, never deletion; **§33's direction-semantics fix is a pre-lock requirement** (canonical sentence per directional type).
- **Contradiction:** §35–§37 — surface both, route proof/verification; unresolved material conflict = UNRESOLVED_CONFLICT, scoped (§37).
- **Dependencies:** §38 — unsatisfied dependency returns DEPENDENCY_UNSATISFIED, not thinner context.
- **Minimum sufficient context:** §39–§42 — minimize cost subject to coverage, no-unsafe-conflict, privacy, budget; completeness ≠ truth (PROVE owns truth).
- **Ranking:** §43 deterministic lexicographic ordering adopted **minus the undefined `Canon` component** (dropped until defined): (GateState, TaskMatch, EpistemicFitness, RelationshipSpecificity, Freshness, PathDepth). §44 no magic relationship score.
- **Receipts:** §57 context receipt schema (incl. `retrieval_creates_authority: false`, `graph_creates_authority: false`, `handoff_to: NAYA-KERNEL-VERIFY`); §58 exclusion reason codes (what was NOT selected and why).
- **Idempotency:** §59's `ContextKey` renamed **replay key** (it includes selection time — deterministic reconstruction, not time-independent idempotency). [NEW naming fix]
- **Snapshot/concurrency:** §61–§62 — one coherent snapshot; corrections create new lineage, never mutate issued receipts; §63 graph/selector/source versions bound.
- **Security:** §68 threat model adopted (graph poisoning, AUTHORIZED_BY laundering, supersession hijack, etc.).
- **CAUSED:** §69 — CONNECT may propose causal candidates; only VERIFY establishes CAUSED. §70 CONNECT cannot self-certify.
- **Sentence semantics:** §34's six templates adopted; **remaining 16 types are pre-lock work** (open).
- **Smart Link:** §54–§55 — CONNECT owns relationship/routing semantics; canonical Receiver owns the intelligence path; link health checks. [N4 draft had no Smart Link material — PDF wins.]

## 3. Value Calculus integration [PDF §45 + N4 §9, merged]

CONNECT uses the **shared** Decision Value Calculus — never a second optimization engine. CONNECT contributes applicability, dependencies, affected parties, context, relationship evidence, freshness, conflicts, scope, baseline context. **Candidate caveat (N4 wins):** V2.1 is CANDIDATE (#1185), not ratified law — all calculus references in this spec are aspirational until ratification. Cross-owner connections: ADMISSIBLE ∧ Q ≥ 9.0 ∧ V_safe > 0 ∧ reversibility ≥ 7 (N4 §9.2 posture, kept as candidate).

## 4. Inter-node topology [PDF §86 adopted]

SELF → CONNECT (current objective/task context) · KNOW → CONNECT (objects/graph) · PROVE → CONNECT (proof-bounded claims) · CONNECT → VERIFY (situated context) · direct PROVE → VERIFY preserved. N4's pipeline line updated to match.

**Baton CONNECT → VERIFY** (merged [PDF §51 + N4 §1.2]): the §57 context receipt — selected/excluded objects and relationships with reasons, relationship paths, applicability, dependencies, conflicts, supersessions, proof refs, task identity. N4's `ConnectionPackage` maps onto this shape; the §57 schema is normative.

## 5. Intelligence-class rule [NEW — in neither source, required]

Derived/shared context carries the source intelligence class; class is preserved across traversal and derivation. CORE is never auto-assigned by CONNECT. A context package never upgrades the class of its contents. (Director review required — this closes a gap both drafts left open.)

## 6. Acceptance battery (merged)

Master contract battery (13 items) + PDF golden tests §72–§80 (positive, unrelated-control, unknown, contradiction, supersession, consent, authority, temporal-replay, graph-influence) + N4 battery items 14–16 (cross-owner leakage refused as critical finding; revocation halts sharing; door-rule violation refused). §80's graph-influence test is the aliveness gate: no behavioral delta → decorative.

## 7. Open questions for Shawn

1. **NayaNET boundary ownership (from scope decision):** who owns mind-link handshakes, connection spaces, and the governed receiver — CONNECT (Appendix A), LAW, or a separate surface contract? The master contract doesn't say.
2. **§19 ratification:** do you ratify the two-stage applicability interpretation (UNKNOWN → visible-non-steering) as the operational reading of Graph V2, or amend the V2 contract itself?
3. **Ranking:** is the lexicographic tuple (minus `Canon`) the permanent ordering, or should `Canon` be defined and included? What does "Canon" mean to you?
4. **Consent UX** (N4 §15.1), **retention default** (N4 §15.2), **PUBLIC level** (N4 §15.3), **cross-mind reputation** (N4 §15.4), **counterpart legitimacy evidence** (N4 §15.5), **break-glass** (N4 §15.6), **your own connections** (N4 §15.7) — carried forward if Appendix A advances.
5. **Sentence templates:** accept the six in §34 as canonical now and the remaining 16 as pre-lock work, or hold lock until all 22 are tabled?
6. **Intelligence-class rule (§5):** is class-preservation with no auto-upgrade the right law, or should governed promotion paths exist?

## Appendix A: Proposed extended surface (N4, preserved verbatim in substance)

N4 §§2–6 (ConnectionRequest with GRAPH_EDGE/MIND_LINK/SPACE_JOIN/INTERFACE_OPEN kinds; consent ladder PRIVATE→SHARED→COLLECTIVE→PUBLIC; purpose binding; NayaNET governed path SENDER → GOVERNED RECEIVER → CANONICAL INTELLIGENCE → HUB PROJECTION; peering handshake; door rule; connection spaces with charter/entry/exit/retention/dissolution rules) — **status: candidate extension, NOT normative, NOT in the master contract.** Advances only on your explicit decision in Q1.
