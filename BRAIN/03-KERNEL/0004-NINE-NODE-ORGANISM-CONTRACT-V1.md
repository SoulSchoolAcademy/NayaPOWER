# NayaPOWER Nine-Node Organism Contract V1

**Status:** CANONICAL ORGANISM CONTRACT — runtime binding proven only where evidence says so.  
**Human Director:** Shawn Vibert  
**Core law:** **ONE ORGANISM / ONE INTELLIGENCE SUBSTRATE / ONE AUTHORITY MODEL.**

## Organism

`MISSION → SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → CONTINUE`

The Nodes are responsibilities, not separate brains, databases, identities, or authority systems.

| Node | Owns | Must never do |
|---|---|---|
| **SELF** | identity, mission, objective, continuity | grant authority; execute external actions; declare truth |
| **LAW** | authority, consent, scope, governance, revocation | execute action; create authority; infer consent; promote truth |
| **ACT** | authorized execution, agency, refusal, safe action | grant authority; self-verify outcomes; rewrite truth |
| **KNOW** | canonical intelligence, events, memory | authorize use; claim evidence quality; verify outcomes |
| **PROVE** | provenance, evidence, truth state, lineage | execute action; grant authority; declare outcome success |
| **CONNECT** | relationships, retrieval, reconciliation, context | authorize action; verify causal outcomes; promote learning |
| **VERIFY** | observed outcomes, acceptance, causality | grant authority; invent observations; create learning without evidence |
| **LEARN** | verified learning, future behavior | self-ratify authority; learn from unverified claims; rewrite history |
| **EVOLVE** | succession, governed evolution, self-optimization | inherit authority; self-deploy consequential change; erase provenance |

## Universal Node envelope

Every Master Node MUST define: identity, purpose, owned responsibilities, explicit non-responsibilities, inputs, outputs, canonical state read/write, consumed/produced events, relationships, required authority, privacy behavior, fail-closed conditions, observability, receipts, proof ladder, neighbor handoff, cold-successor obligation, success criteria.

## Handoff law

No Node may silently absorb another Node's job.

- SELF supplies identity/mission context.
- LAW decides permission; **LAW never executes**.
- ACT executes only after valid authority.
- KNOW retrieves/preserves intelligence; retrieval never grants permission.
- PROVE constrains claims to provenance/evidence.
- CONNECT relates/reconciles/routes context.
- VERIFY checks observed reality independently where consequential.
- LEARN changes future behavior only from verified evidence.
- EVOLVE carries proven improvements forward without manufacturing authority.

## Continuation engine

`MISSION → CURRENT VERIFIED STATE → GAP → PRIORITY → RELEVANT INTELLIGENCE → AUTHORITY → ACTION → OBSERVATION → VERIFY → LEARN → UPDATE STATE → NEXT GAP`

This loop is a planning contract, not proof of autonomous self-building.

## Smart Note example

A Smart Note may touch multiple responsibilities, but not every Node must perform heavy work on every transaction. The runtime should invoke only relevant responsibilities and leave receipts/handoffs sufficient to prove what actually ran.

## Proof boundary

As of this contract, universal nine-node production binding remains **NOT_PROVEN**. LAW has two bounded live cases with independent recomputation. The scope-negative repair below is source-tested and not yet deployed; neither statement proves universal binding.


## Source-mapped executable responsibilities

Assessment base: `744d9b5d694d158ac051682b62766afe6572ed77`.
The companion JSON is a machine-readable projection of this contract, not another authority or proof ledger.
Each Node now maps contracts, semantic schema, runtime source, tests, workflow, reads/writes, transition, graph seed IDs, and remaining gap.
The semantic schemas describe target outputs; their presence does not establish runtime conformance. LAW's three runtime statuses require an explicit adapter to the older semantic status vocabulary. This change documents that seam without silently changing either interface.

| Node | Existing executable seam | Next missing proof/implementation |
|---|---|---|
| SELF | cold-runtime owner/Naya/OIDC binding; reference SELF/manifest boot | universal runtime convergence; local continuity files cannot become canonical memory |
| LAW | law-runtime evaluate/receipt/recompute; executor and SQL grant gates | wrong-target/absent-project bypass repaired here; corrected deployed negative proof pending; broader request/mission/constraint validation remains open |
| ACT | verified-ai-action execute; intelligence-commit-runtime -> canonical SQL RPC | exact LAW decision/request -> selected Door -> observed effect binding |
| KNOW | Event/IB/Lineage/Relationship/Index/state/Receipt commit and reread | arbitrary IB -> dynamic Hub; general scoped retrieval |
| PROVE | independent commit lineage reread; causal evidence reconstruction | schema conformance; immutable checkpoint access security (#978) |
| CONNECT | owner-scoped connect/graph-behavior/graph-verify | broader applicability, conflicts/supersession and cross-owner negative proof |
| VERIFY | independent causal/outcome/generalization/successor recomputation | #975 exact outcome recovery; #810 live current-source acceptance |
| LEARN | candidate -> verified ACTIVE/LEARNED lock-in and reread | arbitrary lessons, held-out benefit and negative transfer beyond the specimen |
| EVOLVE | cold-successor retrieval/reuse/refusal and independent verification | A->B->C compounding; two-owner continuity; governed evolution |

### Scheduling and handoff

The listed order enumerates responsibilities; it is not a fixed execution itinerary.
Private access requires identity and access authority before KNOW/CONNECT.
Retrieved context informs the plan; fresh authority must constrain ACT at the effect boundary.
PROVE prepares and limits evidence; VERIFY independently judges outcomes; LEARN never changes authority.
Every applicable consequential transition retains exact IDs/revisions, provenance, expected/observed result and gaps in the existing receipt surfaces.
Non-applicable responsibilities must carry a reason; capture alone does not invoke promotion or manufacture learning.
Graph seed relationship IDs denote architectural relationships, not evidence that runtime traversal occurred.

### Actual LAW access and effect boundaries

`nayanet-law-runtime/index.ts` validates GitHub OIDC issuer/audience/repository/workflow/ref before privileged reads, binds owner/Naya server-side, loads the existing authority ledger and writes only a decision receipt.
It never executes the requested action. `ok=true` means evaluation completed, not permission; ACT must require `decision.status=AUTHORIZED`.
`nayanet-verified-ai-action/index.ts` separately resolves an exact grant before effect and persists refusal with no execution outcome on denial.
`nayanet-intelligence-commit-runtime/index.ts` calls the existing runtime SQL bridge; the commit RPC validates authority and writes the canonical intelligence chain transactionally.
No general consumer of LAW decision receipts at every effect boundary was established by this inspection.

### Evidence and limits

GitHub jobs for run `36620337089` were reread: authorize/refuse and independent verification both completed successfully.
This supports the two bounded live cases on the assessed source; it does not deploy or prove this patch.
The older receipt `BRAIN/06-PROOF/0006-LAW-LIVE-PROOF-36620001626-V1.json` retains its exact historical source and limits.
SN-001/SN-002 identify CANDIDATE canonical IBs and authorized human projections; no live IB database reread was performed by this patch session.
#810 and #975 remain open; #978/PR #980 retain the Human Director policy-acceptance boundary. No production authorization is inferred from this task.

### LAW regression and next failing rung

Failure classified: authorization scope comparison bug. With a grant for NAYA-NODE-0001 and a request for OTHER-NAYA, both omitted project IDs compared equal and returned AUTHORIZED.
Failure-first tests also reproduced missing/empty scope authorization. The correction requires non-empty strings and exact equality, preserving explicit target/project grants.
The real HTTP handler is exercised offline with mocked OIDC verification/database I/O: refusal receipt, valid authorization without action effects, wrong-workflow no privileged access, and receipt failure.
This is behavioral source verification, not production or real-token proof.

Next unclosed LAW seam: general malformed request/grant, mission/constraints and intent provenance enforcement. `LawRequest` has no mission field, invalid expiry parses to NaN, and same-note intent flags are supplied by the admitted workflow. These are not repaired by the scope correction. A separate bounded classification/test must determine the smallest correction without broadening this change.
The invalid-expiry source probe returned AUTHORIZED for `expires_at="not-a-date"`. The actual grant column is `timestamptz` with an expiry-order check in `supabase/migrations/20260919001730_create_authority_grant_runtime_v1.sql`; therefore this probe establishes a pure-evaluator malformed-input gap, not a demonstrated production database bypass.
The ACT handoff must not treat the existing two-case proof as general LAW qualification.

### Cold-successor torch

Recheck live main, this PR, #810/#975/#978/#980 and the actual deployed LAW revision before mutation.
Review and integrate the source-tested scope repair; production validation requires the applicable explicit authorization.
Next action: reproduce malformed-expiry handling in LAW with failure-first tests, reconcile it with canonical expiry semantics, then prepare the smallest fail-closed correction. Keep ACT/Hub and all existing proof gates intact until the required LAW preconditions are resolved.
Proof: invalid expiry cannot authorize; valid unexpired grants remain usable; real handler refuses and records the reason; independent deployment proof binds the exact corrected source.

### Verification receipt for this source change

Source assessed: `744d9b5d694d158ac051682b62766afe6572ed77`; rebased without conflict onto `ff29510cf242fdc830b2d9b17dd741344143c147` (capture-only workflow guard).
Scope regressions: RED before correction (wrong target and missing/empty scope accepted); GREEN afterward.
Node suite: 54 passed. Python suite after rebase: 247 passed, 3 skipped (live receipt, short-lived runtime/grant, protected live-proof credentials absent).
Collective-chain controls: 10/10; readiness: 2/11, equal to the recorded floor; this is no-regression, not full-chain PASS.
Migration controls: 7/7 detector and 7/7 baseline controls; measured static findings: 0; no new debt. No empty-database rebuild was performed.
All source-map paths and graph relationship IDs resolve; diff whitespace check passes.
The repaired LAW source was not deployed or exercised against production. #810/#975/#978 remain open; no policy acceptance or DEPLOY is inferred.
