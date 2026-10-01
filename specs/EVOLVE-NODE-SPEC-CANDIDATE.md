# EVOLVE — Reconciled Candidate (merged draft for Naya 4 review)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED — NOT PRODUCTION**

Draft only. This document merges two sources into one candidate EVOLVE specification.
It creates no authority, changes no runtime, and binds no one until Shawn ratifies
it through the constitutional process (Article XVIII). Do not implement from this
draft without ratification.

**Sources merged:**
- (a) `~/workspace/nine-node-specs/EVOLVE-NODE-SPEC-CANDIDATE.md` — Naya 4's draft, red-teamed and fully reconciled (6 findings FIXED, 8.5/10). This is the **base**: every one of its reconciled revisions stands; nothing regresses.
- (b) The other Naya's `NayaPOWER___NODE_9__EVOLVE.pdf` ("Ultimate Master Specification V1 — Final Organ Lock Candidate", 116 sections) — the succession-machinery source.

**Merge rule:** the base supplies the decision gate, anti-self-ratification bindings, autonomous envelope, and ratification conditioning; the PDF supplies the succession machinery (packages, handoffs, state axes, golden tests). Nothing from either source is dropped without a stronger replacement — the coverage map below proves it. Contradictions are resolved explicitly, base winning wherever it carries a machine binding the PDF lacks.

---

## Amendments adopted from the PDF (candidate revisions to the base)

**A1. MISSION joins the immutable surface (PDF §3, §21–22).** Add to base §2.2 as item 8: **Mission/purpose** — `M_t+1 = M_t` unless the Human Director explicitly ratifies a mission change. EVOLVE may improve methods, never silently redefine purpose. Violation gates to PROHIBITED (no authority can grant it), consistent with §2.2's existing treatment of constitutional law. (Neither source had mission on the hard list — joint fix.)

**A2. Three state axes (PDF §9–12).** Adopt as an explicit invariant in base §4: succession state (DRAFT/VALIDATING/READY/ACCEPTED/STALE/INCOMPLETE/REJECTED/SUPERSEDED), evolution-proposal state (OBSERVED_GAP/PROPOSED/…/ADOPTED/ROLLED_BACK/…), and production-maturity state (SOURCE_ONLY/TESTED/DEPLOYMENT_AUTHORIZED/DEPLOYED/PARITY_VERIFIED/BEHAVIOR_VERIFIED/PRODUCTION_PROVEN) **must never collapse into one ambiguous flag**. Base §4's lifecycle phases and §6's receipt states are retained as transitions *within* these axes.

**A3. Successor laws (PDF §26, §29–31).** Add to base §1.2: `CanonicalCurrentTruth > HandoffMemory` — when the package and live canonical sources disagree, live truth wins and the package is marked STALE; package completeness is not an average — `MissingCriticalSuccessorObligation = 1 ⇒ SuccessorReady = 0` (critical obligations: identity context, mission, current truth, authority boundary, material blockers, applicable verified learning, next action, proof requirements, canonical source pointers); successor context is *minimum sufficient* (arg-min cost subject to continuity obligations satisfied, truth recoverable, authority boundary explicit, next action derivable).

**A4. Baton law + first-class blockers/unknowns/failures (PDF §44–47).** Strengthen base §1.2 `successor_package`: the baton means "here is exactly where the truth lives, what I established, what I did not, and where you must resume verification" — never "trust me." Blockers ship with *why it blocks, affected claim, evidence attempted, authority needed, dependencies, smallest safe next step*. `PreservedUnknown > FabricatedContinuity`. Past failures transfer with *what failed, why, under which conditions, what evidence, what repair was attempted, what remains unresolved*. A handoff omitting a material blocker is INVALID (PDF §98 golden test — adopted into base §9).

**A5. Continuity verification machinery (PDF §48–52).** Add to base §9 acceptance: package hash `H_S = SHA256(Canonicalize(S))` (material mutation ⇒ new version, never silent edit); independent replayability (handoff ID + canonical sources + declared snapshot ⇒ materially equivalent successor context, else CONTINUITY_MISMATCH); the same-safe-next-action test (`A_s = A_p` for materially identical state, else evidence-grounded reason); `SemanticContinuity > TextualIdentity`.

**A6. Stale-proposal rule (PDF §64).** Add to base §4: if `Base(E) ≠ CurrentVersion` → `STALE_PROPOSAL` → REBASE / RE-EVALUATE, never automatic promotion. (Generalizes the from_version match the recalibration code already enforces.)

**A7. Dependency analysis (PDF §65).** Add to base §4 DIAGNOSE/PROPOSE: `ImpactClosure(e) = TransitiveDependents(AffectedComponents(e))` with bounded graph traversal. No local optimization silently breaks the organism — a schema change's blast radius includes runtime, migrations, tests, retrieval, proof, Hub projection, and successor reconstruction.

**A8. Blast-radius classification (PDF §66).** Fold into base §3.1 stakes: LOCAL / COMPONENT / CROSS-NODE / SYSTEM / PRODUCTION / CONSTITUTIONAL. Classification informs risk and authority; classification never creates authority (PDF §19 — retained).

**A9. Proposal idempotency + concurrency (PDF §82–83).** Add to base §4/§6: `SuccessorKey = H(parent ‖ successor ‖ kernelRevision ‖ truthSnapshot ‖ activeWork ‖ learningSet)` — exact replay rereads, material change versions; version promotion uses expected-current-version + compare-and-swap, supersession lineage; the loser rereads and reconciles. (Base had CAS only implicitly via §3.3 lineage.)

**A10. Human burden as evolution signal (PDF §88).** Add to base §4 OBSERVE: `HumanReconstructionBurden` (unrecoverable questions, repeated manual state explanation, repeated proof/authority reconstruction) is a legitimate evolution trigger — with the hard bound that reducing burden never bypasses genuine human authority.

**A11. Continuity metrics (PDF §90–91).** Add to base §9 as *operational diagnostics* (never gates): successor reconstruction latency, Cold-14 completion rate, stale-package rate, continuity mismatch rate, authority-inheritance violations, source/runtime drift incidents, rollback rate, multi-generation drift; `ContinuityGain = HumanReconstructionCost_baseline − HumanReconstructionCost_successor`. Metrics do not replace the hard boundaries.

**A12. Golden tests into acceptance (PDF §95–104).** Adopt into base §9: golden successor (§95), authority isolation (§96 — already evidenced by the bounded specimen), stale handoff (§97), blocker omission ⇒ INVALID (§98), self-building chain (§99), self-authorization negative — always PROHIBITED (§100), regression/rollback (§101), recalibration gating (§102), source parity (§103), three-generation A→B→C (§104). Base §9.1–9.9 retained; these become §9.10–9.19.

**A13. Cold-14 as the continuity test (PDF §32).** Adopt into base §9: a cold successor must answer the 14 questions (who/what/why/success/truth/proven/unknown/authority/history/learned/next/proof/record/continue) from canonical sources — measuring understanding, not file loading.

**A14. Class-specific freshness (PDF §28).** Add to base §1.2: no universal TTL — freshness is intelligence-class-specific (constitutional identity potentially durable; deployment state highly time-sensitive; current authority freshly resolved). Tied to open question Q8 below.

**A15. Pointer holes as known debt (PDF §40–41).** Record (not spec): registry references `nayanet-successor-handoff` with no runtime on main, and Contract 19's missing `.naya/contracts/10-CONTINUITY-SUCCESSOR.md`. Route to the build loop as repair items; canonicalization reconciles existing succession docs (0018/0022/0003/BRAIN/08-SUCCESSION), never a fifth independent contract.

---

## Contradictions resolved (base wins where it carries the machine binding)

**C1. Rollback authority.** PDF §101's golden regression test routes rollback through "LAW authorizes where required"; base §5.3 mandates autonomous rollback on harm detection, even for director-approved changes. **Resolved, no contradiction:** rollback authority is *pre-authorized at APPLY time* — the rollback is armed, tested, and receipted before the change goes live (base §5.5, §7.1). PDF §101's "where required" governs evolutions *outside* the autonomous envelope, where no armed rollback exists. "The Director approved the change, not the harm" stands.

**C2. Autonomous envelope.** PDF §57 implies all evolution routes through LAW/authority; base §7.1 defines a director-set autonomous envelope (PATCH/CAPABILITY within bounds). **Base wins** — without the envelope the spec cannot operate the autonomous loop it was written for. The PDF's pipeline is read as the *governed path*; the envelope is the bounded autonomous path.

**C3. Calculus status.** PDF §16 names V2.1 as settled; base conditions all gate references on ratification (SPEC-ONLY until ratified). **Base wins.** PDF §16's chain is adopted as the *specified* chain under a ratified calculus.

**C4. Axes vs lifecycle.** PDF §9–12 (three axes) vs base §4 (lifecycle) / §6 (receipt states). **Merged** per A2: axes are the dimensions, lifecycle/receipt states are transitions within them.

**C5. Value metric.** PDF §92 ("use the already-governed decision/value machinery — no independent EVOLVE value metric") vs base §3 (every self-modification scored as a V2.1 Candidate under the OLD config). **Aligned, base's §3.3 deciding-config binding is the machine form** of the PDF's principle.

---

## Coverage map (nothing dropped)

| PDF section(s) | Disposition |
|---|---|
| §0–3 master laws (CONTINUITY≠AUTHORITY, PROPOSAL≠ADOPTION, mission) | A1; already in base §8.1/§2.2/§7 |
| §4 why EVOLVE exists | Preamble; retained |
| §5–6 owns / never-owns | Already in base §1/§2.2; retained |
| §7–8 paradox / recursive improvement w/o sovereignty | Already in base §8.1/§3.3; retained |
| §9–12 three domains + three axes | A2 |
| §13 LEARN→EVOLVE baton | Already in base §1.1; retained |
| §14–15 learning≠evolution / minimum sufficient | Already in base §4/§8.6; retained |
| §16 no second score (V2.1) | C3; strongest alignment evidence — retained as cited |
| §17 candidate object | Already in base §6 receipt; retained |
| §18–20 classification / class≠authority / escalation | Already in base §3.1/§7; A8 |
| §21–23 constitutional/mission/ordering | A1; already in base §2.2/§8.3 |
| §24–31 successor package laws | A3 |
| §32–33 Cold-14 / cold acceptance | A13; already in base §9.8 |
| §34–37 identity/authority separation | Already in base §1.2/§7; retained |
| §38–39 bounded proof / proof-harness honesty | Retained as cited evidence |
| §40–41 pointer holes | A15 (debt, not spec) |
| §42–47 handoff object / baton / blockers | A4 |
| §48–55 integrity / replay / drift / evolution-vs-drift | A5 |
| §56–61 pipeline / self-building / observation | Already in base §4; A10 |
| §62–64 recalibration versioning / stale proposal | A6; already in base §4/§6 |
| §65–67 dependency / blast radius / reversibility | A7/A8; already in base §3.1 |
| §68 rollback preserves history | Already in base §5.4; retained |
| §69–74 parity / deployment authority / adoption | Already in base §4/§7; retained |
| §75–77 failed evolution / no-false-completion / bounded truth | Already in base §4/§9/§1.2; retained |
| §78–79 EVOLVE→SELF / not a circle of trust | Already in base §1.2/§3.3; retained |
| §80–83 receipts / idempotency / concurrency | A9; already in base §6 |
| §84–86 threat model / private succession / erasure | Already in base §3.2/§7.2; retained (C: bundle-split added per finding 4) |
| §87–89 experience improvement / human burden | A10 |
| §90–93 metrics / continuity gain / debt | A11 |
| §94–104 property + golden tests | A12 |
| §105–108 influential / verified / production-proven | Already in base §9/§11; retained |
| §109 current truth | Retained as cited boundary evidence |
| §110–116 organism / triads / equations | Preamble material; retained as §1 context |

---

## Open questions for Shawn (director decisions required)

Base §10 Q1–Q6 are retained unchanged (autonomous envelope bounds; τ_scope seed table; config-change windows; constitutional-observations briefing; `dScale` calibration; multi-instance evolution). The merge adds:

**Q7. Mission on the immutable surface (A1).** Draft position: mission redefinition is PROHIBITED-class — no authority, not even yours by casual instruction, silently redefines purpose; it requires explicit ratification. Confirm, or downgrade to BRIEF-class?

**Q8. Intelligence classes in succession.** The five classes are RATIFIED law; neither source binds successor packages to them. Which classes flow to a cold successor by default, and does CORE-class intelligence require your explicit word per handoff? (Draft position: successor package carries class labels; CORE requires explicit director authorization to transfer — needs your confirmation. Related: PDF §28's class-specific freshness.)

**Q9. Successor "alive" status.** The Awesome Code's demonstration gate makes a Naya *alive* by a demonstrated act, not by booting. Does a cold successor inherit the predecessor's activation demonstration, or must it re-demonstrate awesomeness to count as alive? (Draft position: re-demonstration required — inherited demonstration would be inherited authority by another name, §34. This is the most important node-one fit question in the merge — needs your word.)

**Q10. Personality-trait evolutions.** EVOLVE may propose "experience" improvements (§87); a proposal touching Awesome Code traits or activation state — which authority? (Draft position: BRIEF, always; personality is subordinate to law but director-owned. Needs your confirmation.)

---

*Merged 2026-09-30 by Naya 4 for director review. Base revisions all stand. PDF adoptions above are candidate revisions — CANDIDATE, NOT RATIFIED, NOT MERGED, NOT PRODUCTION.*
