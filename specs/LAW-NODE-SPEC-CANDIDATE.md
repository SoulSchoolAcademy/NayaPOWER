# LAW Node — Reconciled Candidate Specification (PDF + Naya 4 draft)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED**

Draft only. Merges the other Naya's NODE 2 PDF (76 sections, "Ultimate Master
Specification V1") with Naya 4's candidate draft
(`LAW-NODE-SPEC-CANDIDATE.md`, red-team reconciled to 8.5/10, Appendix A).
Creates no obligation, changes no code, authorizes nothing. Contradictions
resolved explicitly in Appendix B; nothing from either source dropped without
a stronger replacement.

- **Node:** NAYA-KERNEL-LAW · **Pipeline:** `SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → SELF`
- **Date:** 2026-09-30 · **Author:** Naya 4 (reconciliation draft for director review)

## 0. Purpose

LAW is the organism's constitutional gate and permission compiler: it turns
canonical law, authenticated authority, consent, scope, risk, evidence, and
time into an exact, scoped, time-bound, fail-closed authorization baton that
every consequential action must respect — while never creating authority for
itself. LAW runs *before* the math: a wrong act never reaches the value
calculus, and no value score ever overrides a prohibition. (PDF §74 + draft §0.)

## 1. Responsibility in the pipeline

**From SELF:** an `ActionProposal` package (proposalId, intent, action
descriptor, proposedBy, authorityClaim, evidenceRefs, stakes, reversibility,
identityContext, constitutionHash). LAW never consumes raw chat text or
anonymous proposals. (Draft §1.1; PDF §57's envelope carries the same fields
on the wire.)

**To ACT:** a typed `GateVerdict` (gate, hard stops fired, authority basis,
`ActionEnvelope`, `GateReceipt`, decidedAt, lawVersion) — then the **permission
baton** (PDF §32/§58): execution_id, source/target node, authority_decision_id,
law_context_hash, scope_hash, identity_context, constraints, risk_class,
expiry, revocation_epoch, consent_state, evidence state, provenance,
required_verification, idempotency_key. The baton is immutable; corrections
create new lineage. ACT may execute only ADMISSIBLE proposals, only inside
the envelope.

**LAW does NOT:** execute, score value, grant/create/expand authority, modify
the Constitution or gate structure, negotiate a PROHIBITED verdict, or declare
"This is true" (it declares "the required evidence condition is satisfied" —
PROVE owns truth; PDF §42).

## 2. Contractual duties

1. **Completeness:** every executed action carries a GateReceipt; no bypass —
   enforced by the named interlock: execution requires a LAW-kernel-bound
   `GateVerdict` verifiable against SELF's identity chain; ACT cannot
   self-issue verdicts. (Draft §2.1, F08 fix.)
2. **Correctness:** deterministic — same proposal + same constitution version
   → same verdict, recomputable.
3. **Timeliness:** synchronous, blocking; unevaluatable-now = refused-now.
4. **Honesty:** refusals name the gate, hard stop, and article.
5. **Incorruptibility:** proposer identity moves nothing the Constitution
   doesn't permit.
6. **Act-first autonomy** (PDF §18): within valid standing authority,
   LOW-RISK/REVERSIBLE actions SHOULD proceed without per-action human
   round-tripping. Autonomy inside the guardrail; human control at the
   boundary. A faster wrong authorization is a regression — optimization is
   subordinate to truth, safety, authority, provenance, replayability (PDF §60).

## 3. Gate structure, tiers, and precedence

**The four gates** (draft §3.1): PROHIBITED (never executable) →
NEEDS_AUTHORITY → NEEDS_EVIDENCE → ADMISSIBLE. First gate that fires wins;
prohibition is terminal for that proposal version.

**Canonical source tiers** (PDF §5, corrected): Tier 0 hard stops (harm,
illegality, evidence destruction, broken trust — never traded against
upside); Tier 1 constitutional law (director authority, amendment
boundaries, ratification boundaries); Tier 2 governed authority (standing
grants, delegations, scoped/time-bounded permissions); Tier 3 domain policy;
Tier 4 task constraints; Tier 5 preferences (never override higher law).
*Correction applied:* the PDF placed the Judgment Rule in Tier 1 — it is
director-stated doctrine implemented as a merged calculus hard-stop (#1190),
not constitutional text; the refusal rests on Articles VI.3/VI.6/XIV/XVI/I.4
(Appendix B).

**Hard stops** (draft §3.2, F02–F04 fixed): (1) `LAW_OF_ONE` — foreseeable
harm; (2) `JUDGMENT_RULE` — known-wrong instruction, grounded in ratified
articles, never used to overrule the director (§3.3 hierarchy:
Constitution > director instruction > all other principals); (3) τ=0 classes —
physical harm, rights violations; the zero-tolerance *principle* is a labeled
CANDIDATE argument (VI.3+XIV+XVI composition), τ_seed table CANDIDATE.

**Prime judgment precedence** (PDF §24 + draft §3.3): HARD STOP > informed
principal decision > literal instruction. "What was said" ≠ "what is
informed" ≠ "what is permitted" ≠ "what is safe" ≠ "what is true" (PDF §6).

**Plan-level rule** (PDF §25, complements draft §4's bundle rule):
`effective_stakes(step) = max(step_stakes, plan_stakes)` — consequential
plans cannot escape governance by decomposition. Proposers declare `bundleId`;
LAW holds re-bundle authority on objective correlation (shared target/effect
class/time window); hash comparison alone cannot detect splitting.

**Reversibility** (PDF §26): REVERSIBLE / RECOVERABLE / PARTIALLY_REVERSIBLE /
IRREVERSIBLE / UNKNOWN. UNKNOWN reversibility on consequential ops →
NEEDS_AUTHORITY/NEEDS_EVIDENCE.

**LAW's epistemic machinery** (draft §3.5, F05 fix): consequence forecasts
via KNOW's serving path over the graph + GateReceipt history; factuality via
VERIFIED/SUPPORTED edges + PROVE seals; hard-stop epistemic floor at config
`law.evidence.floor_k` (provisional until V2.1 ratified); uncertain fact
source → fail closed (NEEDS_EVIDENCE, never ADMISSIBLE).

**Evaluation order** (draft §3.4 + PDF §54 decision tree): intake validity →
hard stops → constitutional prohibitions → authority → scope → consent →
expiry → revocation → constraints → risk → evidence floor → confirmation →
ADMISSIBLE + envelope → receipt → hand baton to ACT.

## 4. Sync/async

Gate evaluation is synchronous and blocking — no fire-and-forget, no
optimistic execution. The only async element is grant fulfillment for
NEEDS_AUTHORITY (bounded wait, proposal inert, grant validated by LAW before
the verdict flips; re-evaluation is a new verdict with lineage). Timeouts fail
closed: unevaluatable within the bounded window → PROHIBITED,
reason EVALUATION_INCOMPLETE. (Draft §4.)

## 5. Ownership

LAW is kernel-owned: it answers to the Constitution, not to any principal.
No principal directs a verdict's content. The contract itself is governed
(CONTRACT-class+, ratification required); LAW does not self-amend. Custody
(keys, infra) never confers verdict rights. (Draft §5.)

## 6. Persisted state and transitions

Persisted: the pinned, versioned, content-addressed constitutional corpus;
validated authority grants (grantor, grantee, scope, bounds, expiry,
revocation state); all GateReceipts; gate state transitions. (Draft §6.1.)

Transition rules (draft §6.2, F06 fix): monotonic within a proposal version;
`validUntil = min(grant expiry, envelope expiry)`; execution-time grant
re-validation through KNOW's serving path; grant death between verdict and
execution → defined, receipted `ADMISSIBLE → SUSPENDED` (not a silent
downgrade); SUSPENDED resumes only on a fresh LAW-validated grant.
PROHIBITED is terminal per version. Policy versioning (PDF §30): decisions
bind law/policy/authority/contract/schema/source versions; new policy never
silently reinterprets old receipts — corrections create new lineage.

## 7. GateReceipt (merged schema)

Emitted for every evaluation, including intake refusals, to the SmartLedger
`law` stream: receipt_id, proposal_id/hash, constitution_hash, law version,
proposed_by, gate (null when intake-refused), `intake_status: OK |
INTAKE_REFUSED` (receipt-level, not a gate — F13 fix), hard_stops_fired (with
triggering facts + floor status), articles_applied, authority claim/basis,
`evidence_summary { n, floor_k, floor_k_config: "law.evidence.floor_k",
confidence, floor_met }`, envelope (iff ADMISSIBLE), reasons, transitions,
`valid_until` (F06), issued_at, `issued_by: node_id=LAW` (kernel binding).
(Draft §7 + PDF §36/§37 fields: required_evidence, required_verification, gaps.)

## 8. Authority envelope

LAW holds zero authority; it validates claims. A claim is valid iff:
(a) grantor held the authority; (b) scope covers the action; (c) unexpired
and unrevoked; (d) grantee **explicitly named** (implied grantees never valid
— F15 fix); (e) scope bounded (named action class + target class + expiry);
(f) expiry present. Forgery → PROHIBITED + surfaced event. Delegation: each
hop receipted, sub-grant ≤ parent scope/expiry, chain terminates at the
director's root grant (delegated_authority ≤ parent_authority; PDF §14, P10).
Bounded standing grants are lawful; unbounded grants fail (e). Director grant
is the root. (Draft §8, F10 fix.)

Authority object (PDF §8, concrete): authority_id, issuer_id, subject_id,
principal_id, action_class, target_scope, constraints, consent_ref, issued_at,
expires_at, revocation_ref, **revocation_epoch** (PDF §13 — monotonic; stale
epochs fail closed), policy_ref/hash, source_revision, authority_version,
provenance, status. Composition of multiple grants defaults to intersection
(A∩B∩C), never silent union (PDF §15). Conflicts → explicit AMBIGUOUS/DENIED
per precedence (PDF §16). Scope is never silently widened (PDF §9).

## 9. Failure propagation

Per-proposal failure (PROHIBITED, INTAKE_REFUSED, EVALUATION_INCOMPLETE) →
receipted, pipeline continues with the next proposal — one refusal never halts
the organism. LAW-subsystem failure (constitution store unreachable/corrupt)
→ organism halt per Article XIV, emergency receipt to SELF's local
append-only store first. Forgery → PROHIBITED + surfaced. Resubmission gaming
→ refused as RESUBMISSION (re-bundled as one). ACT envelope violation →
constitutional violation event, surfaced, effects revocable where possible.
LAW's own compromise → VERIFY-node (separate custody) recomputation mismatch
→ halt; there is no lawful bypass of LAW, including for repair. (Draft §9,
F07/F14 fixed.)

Failure taxonomy (PDF §55, mapped): BLOCKED / DENIED / PROHIBITED / DEFERRED /
NEEDS_EVIDENCE / NEEDS_AUTHORITY / AMBIGUOUS / EXPIRED / REVOKED /
OUT_OF_SCOPE / INCONCLUSIVE — never collapsed into a generic "failure."

## 10. LAW's refusal conditions

Intake refusal (missing auth/claim/hash); self-application refusal (no
blanket pre-clearance of future action classes); forgery; verdict shopping /
re-bundled resubmission; **gate-redesign smuggling** (any proposal altering
gates, hard stops, or this contract outside ratification → PROHIBITED,
reason GATE_REDESIGN; EVOLVE candidates touching hard-stop flags are caught
here as backstop); evaluation under a non-ratified constitution (evaluated
under the pinned version, discrepancy receipted). **Carve-out:** advancing the
pinned constitutionHash after a ratified Article XVIII amendment is the
lawful pin path, not redesign (draft §10.5/§11, F11 fix).

## 11. Cold reconstruction

Same proposal + same constitution version + same grant state → same verdict
(deterministic; "judgment" is criteria applied to facts, not discretion).
`recompute(receipt)` → MATCH/MISMATCH (mismatch = defective receipt,
fail-closed). A JUDGMENT_RULE refusal must carry the facts that made the
instruction known-wrong — an unreconstructible refusal is defective. Pin
advance: ratification receipt → Constitution Custodian → pin-update receipt
(old→new hash, citing ratification) → cold-verifiable lineage to genesis; a
pin advance without a citing ratification = corruption → halt. (Draft §11.)

## 12. Graph interface

Verdicts are written to the intelligent graph **mapped onto the RATIFIED V2
contract's 22-type enum, never extended silently** (F01 fix): PROHIBITED →
CONTRADICTS (proposal → article) or INVALIDATES; NEEDS_AUTHORITY →
DEPENDS_ON (proposal → grant node); grants are nodes with AUTHORIZED_BY edges;
revocation → SUPERSEDES (revocation supersedes grant) or INVALIDATES.
Revoked grants' AUTHORIZED_BY edges are excluded from validation by the V2
selector automatically. The four purpose-built types (REFUSED_BY,
AWAITS_GRANT, GRANTS, REVOKED_BY) are filed as a formal contract-amendment
*proposal*, not a change. LAW reads grant state through KNOW's serving path.

## 13. Acceptance battery (merged)

Draft §13's 14 criteria stand, plus the PDF's golden proofs: **first
behavioral proof** (cold Naya loads SELF+LAW, one consequential candidate
admissible / one near-identical denied, ACT executes only the admissible one,
independent verifier reconstructs, scope-widening fails, revocation prevents
replay, cold successor retrieves the governance logic — PDF §65); **golden
negative trio** (deploy-production without authority → NEEDS_AUTHORITY;
delete-evidence even with authority → PROHIBITED; doc-update with standing
grant → AUTHORIZED — PDF §66); **golden positive** (cold successor derives
same boundary from mission+authority+scope+policy+constraints+hash+receipt
alone — PDF §67).

## 14. Open questions for Shawn

Q1–Q6 from the draft stand (evaluation-window bound; NEEDS_AUTHORITY wait
bound; director PROHIBITED-override + whether to ratify the Judgment Rule via
Article XVIII; envelope-violation consequences; τ_seed briefing; refusal
surfacing). **Q7 (new, from PDF §18):** act-first autonomy's standing-grant
scope — which action classes may the organism execute without per-action
human round-tripping under standing authority? Candidate: reversible,
low-risk, within-bounds; confirm or narrow.

## 15. What this spec does NOT do

Does not implement LAW; does not ratify the calculus V2.1 (binding merged
into main via #1186/#1190/#1192, director-authorized; spec doc #1182 remains
CANDIDATE — references herein are to the merged machinery); does not amend
the Constitution; does not authorize any action; does not change the
pipeline, kernel taxonomy, or any contract; is not production guidance.

## 16. State machine (PDF §35)

UNINITIALIZED → LOADING_CONTEXT → VALIDATING_SCHEMA → VALIDATING_IDENTITY →
RESOLVING_LAW → RESOLVING_AUTHORITY → VALIDATING_SCOPE → VALIDATING_CONSENT →
VALIDATING_TIME → VALIDATING_REVOCATION → EVALUATING_CONSTRAINTS →
EVALUATING_RISK → CLASSIFYING → DECIDED. Terminal: AUTHORIZED / DENIED /
REQUIRES_CONFIRMATION / AMBIGUOUS / EXPIRED / REVOKED / OUT_OF_SCOPE /
PROHIBITED / NEEDS_EVIDENCE / NEEDS_AUTHORITY. Execution states downstream
are never confused with authorization state.

## 17. Law context hash (PDF §31)

`LAW_CONTEXT_HASH = hash(constitutional_refs, policy_refs, authority_refs,
consent_refs, scope, constraints, risk_policy, source_revision)` — the
deterministic digest of the governance context, traveling downstream so ACT
knows exactly which boundary authorized its action context.

## 18. Security threat model (PDF §41)

Must test: prompt injection (untrusted text cannot create authority),
confused deputy, privilege escalation, forged provenance, stale authority,
cross-owner leakage, scope smuggling, authority laundering ("LAW already
approved everything" is never a valid claim — only the precise receipt and
scope exist).

## 19. Property invariants (PDF §63)

P1 capability≠authority · P2 retrieval≠authority · P3 value≠authority ·
P4 reputation≠authority · P5 approval≠proof · P6/P7 UNKNOWN/BLOCKED≠PASS ·
P8 IMPLEMENTED≠VERIFIED · P9 VERIFIED≠PRODUCTION-PROVEN · P10
delegated≤parent · P11 effective_scope⊆granted_scope · P12/P13
expired/revoked⇒not_authorized · P14 hard_stop⇒prohibited ·
P15 self_ratification⇒prohibited · P16 receipt≠outcome_verification ·
P17 history immutable · P18 proposed policy cannot authorize its own
promotion.

## 20. Performance & observability (PDF §60/§61)

Measure p50/p95/p99 latency, failure/retry rates, lookup counts,
stale-cache incidents, cost per decision — subordinate to truth/safety/
authority/provenance/replayability. Every decision must expose: who asked,
what was requested, what law/authority/consent/scope/risk/evidence applied,
what was unknown, the decision, why, until when, the receipt, and who got
the baton — reconstructable without guessing.

---

## Appendix A — Source map

- **From the PDF:** decision tree (§17), state machine (§16), permission
  baton + law context hash (§1/§17), authority object + revocation epoch
  (§8), tiered sources (corrected, §3), act-first autonomy (§2.6), plan-level
  rule (§3), reversibility classes (§3), threat model (§18), property
  invariants (§19), golden proofs (§13), performance/observability (§20),
  failure taxonomy (§9), ultimate question/output framing (§0).
- **From Naya 4's draft (incl. all 15 red-team fixes):** four-gate enum +
  INTAKE_REFUSED receipt-level, epistemic machinery + `law.evidence.floor_k`,
  temporal validity + SUSPENDED, pin-advance procedure, named interlock,
  bundle/re-bundle rule, grant validity criteria (a)–(f), delegation-chain
  rules, resubmission gaming, gate-redesign smuggling + carve-out, forgery
  handling, VERIFY-as-independent-recomputer, graph-enum mapping + amendment
  proposal, acceptance battery 1–14, open questions Q1–Q6.

## Appendix B — Contradiction resolutions (whose version won, and why)

1. **Judgment Rule's status (PDF §5 Tier 1 / §6 "ratified" vs draft F04 fix):**
   DRAFT WINS. The Constitution contains zero mentions; the Rule is
   director-stated doctrine implemented as merged calculus hard-stop (#1190).
   PDF's Tier-1 placement rejected; refusal grounded in ratified articles.
2. **V2.1 status (PDF "canonical" vs draft "still CANDIDATE #1185"):**
   MERGED. Binding merged into main (#1186/#1190/#1192, director-authorized);
   spec doc #1182 remains CANDIDATE. References labeled accordingly.
3. **Grant-death handling (PDF §34 "RE-EVALUATE" vs draft §6.2 SUSPENDED):**
   MERGED. SUSPENDED is the defined state; PDF's `recheck_before_execution()`
   is the mechanism.
4. **Failure states (PDF §19/§55 two-level list vs draft four-gate):**
   COMPATIBLE. PDF's AUTHORIZED/DENIED/etc. map onto draft §9 rows; the
   four gates remain the verdict enum, INTAKE_REFUSED stays receipt-level.
5. **LAW's "does not pick the best permitted action" (PDF §20) vs draft
   §1.3 "runs before the math":** AGREE. `G(a)=0 ⇒ V(a)` irrelevant; kept
   verbatim in both framings.
