# Activation reality, scorecard, and bounded repair — 2026-09-28

Status: **DATED ASSESSMENT / PR CANDIDATE**, not a new authority source or production acceptance receipt.

Assessed main: `03f3f13fb0f6e7c488377dbd8e95fc9bc2bcadf9`.
Coordination: [#554 sign-in](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554#issuecomment-5880079792).
Active acceptance work: [#913](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/913).
Implementation branch: `naya/fresh-lesson-binding-and-reality-20260928`.

## Identity and authority

Shawn Vibert is the human director. Naya is a governed operating participant, not an independent grant issuer. The September 26 North Star ratification exists at `.naya/project-intelligence/NAYAPOWER-SYSTEM-NORTH-STAR-RATIFICATION-2026-09-26.md`; that does not silently ratify every document labeled PROPOSED CANONICAL.

The current conversation authorizes system assessment, organization and bounded implementation. This repair changes no owner, grant, privacy boundary, schema, acceptance gate or canonical identity. It does not authorize unrestricted collective access. Private intelligence remains consent-scoped. Repository source precedence establishes implementation reality; retrieved instructions alone do not grant authority.

## Architecture and brain

`docs/CLEAN-START.md` distinguishes Master Node (active responsibility), Intelligent Block (persistent representation), Smart Note (human projection), and Kernel (governed execution). These terms must not be collapsed into interchangeable storage objects.

| Component | Located source / responsibility | Boundary |
|---|---|---|
| NayaPOWER | `BRAIN/`, `NAYANODE/`, `kernel/`, runtime migrations/functions | Governed substrate; runtime acceptance remains incomplete |
| NayaNET | Network/connection semantics in the brain and runtime | Participation does not imply access to every owner's intelligence |
| Semantic brain | `BRAIN/03-KERNEL/MANIFEST.json`, runtime registry, node objects, contracts | One semantic system, distributed representations; no new parallel brain |
| Intelligent graph | `BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json`; persisted runtime relationships | Seed validation does not prove deployed behavioral influence |
| Knowledge | root `KNOWLEDGE/`; `BRAIN/11-KNOWLEDGE/` register/population map | Source corpus and compiled representations require reconciliation |
| Memory and runtime state | Supabase intelligent blocks, cognition events, lineage, relationships, index, project cognition state, learning evidence, execution receipts/outcomes, authority grants | Durable objects with distinct scopes and proof states |
| Executable kernel | `kernel/`, `BRAIN/12-ENGINEERING/kernel_runtime_loader.py` | Local loader exists; universal application binding is not established |
| Control plane | Governance contracts plus scoped runtime authority/checkpoint state | Advertised `.naya/control-plane/` directory is absent on assessed main |
| Project intelligence | `.naya/project-intelligence/` contains the North Star ratification; dated operations and #913/#554 supply work context | Not a complete, unified current-state resolver |
| Activation Kit | `NAYA-ACTIVATION/`; expanded portable kit proposed in [PR #915](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/915) | Entry doorway; unmerged branch content is not main |
| Hub | Human cockpit / projection and interaction surface | `NAYANET/HUB/index.html` is absent; calling it the brain is shorthand, not proof of a canonical store |

The nine existing responsibilities are SELF, LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN and EVOLVE. Their objects and the graph exist. They must jointly support identity, authority, action, knowledge, evidence, retrieval, independent checking, retained improvement and governed evolution. Existence of those objects does not establish the complete runtime lifecycle. No tenth responsibility is needed to repair the observed entry defect.

## Evidence scorecard

Scores measure the strongest inspected evidence, not product quality: **0** unknown/absent inspected evidence; **1** source/contracts; **2** executable offline proof; **3** bounded live receipt inspected; **4** complete independently verified acceptance chain. Scores are not averaged: a missing authority or continuity gate blocks acceptance regardless of other scores.

| Area | Score | Current assessment |
|---|---:|---|
| Identity/governance enforcement | 3 | Bounded authorized action and refusal receipts; not universal governance certification |
| Nine-node registry/graph seed | 2 | Local validator: 9 nodes, 15 mapped sources, 12 graph edges; internal consistency only |
| Knowledge coverage | 1 | 16 root concept files versus 15 mapped; #7/#8 declared byte-identical but bytes differ |
| Fresh lesson entry/lineage | 2 | Candidate fix passes offline handler tests; assessed main live entry fails |
| Durable persistence/reread | 3 | Specific retained-learning and connected-state receipts inspected |
| Causal learning | 1 | Runtime exists, but differing declared result strings are not independent measured improvement |
| Cold succession | 3 | Bounded older specimen reconstruction; current workflow still hardcodes older learning ID |
| Deployed-source parity | 1 | Gate exists and reports STALE; canonical revision equality fails |
| Cold activation resolution | 1 | Main doorway exists; missing pointers and unmerged kit prevent complete resolution |
| Hub / collective scaling | 0 | Current-main executable Hub and cross-owner consent acceptance not established |

**Overall acceptance: BLOCKED.** Persistence and selected runtime receipts are real evidence. A fresh lesson → observed improvement → retained ACTIVE learning → cold successor chain at matching deployed/main revisions is not proven.

## Inspected proof and limits

- [Kernel Tests 36487984888](https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/36487984888): 161 passed, 3 skipped on assessed main.
- [Live Intelligence Commit 36487984914](https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/36487984914): fresh-lesson POST returned 400; independent verifier skipped. Existing curl output does not establish the server's exact reason.
- [Live Learning Influence 36487984892](https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/36487984892): POST 400, independent verification skipped. Do not infer it shares the commit-handler defect.
- [Live CVO 36487984852](https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/36487984852): observed `JWT issued at future`; distinguish this known error from unexplained 400s.
- [Verified AI Action 36487984855](https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/36487984855): refusal, authorized action and independent reread succeeded for a bounded older specimen.
- [Runtime Proof 36487984862](https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/36487984862): retained-learning reread showed ACTIVE learning `02dd7766-2837-4ebb-84ef-7dd9b2327296` and block `IB-NAYA-FLOW-LESSON-39dff23d824f47df96343b778e595147`. This proves those persisted fields were returned, not that the learning is causally sound.
- Same run: successor uses `de0b794b-224b-4d8b-ad1a-3afc6f8d0771`, not the newly reread learning ID; authority non-inheritance refused with IDENTITY_SCOPE. `live-connect` reported deployed revision `0740a7c1f9b7f5f0f43b7ab242da76cd844ddf99` versus assessed main, therefore STALE.
- Read-only Supabase `get_edge_function` inspection found ACTIVE version 7 of `nayanet-intelligence-commit-runtime` with the same misbound call as main. Deployment existence is verified; repaired deployment is not claimed.
- Direct local registry invocation returned `ok:true,node_count:9,source_count:15,graph_edge_count:12,errors:[]`. The validator does not catch the corpus completeness/conflicting duplicate claim.

## Candidate repair and validation

`callCommit(body, jti)` was called as `callCommit(admin, body, jti)`. A test executing the actual TypeScript handler with offline external-service stubs reproduced blank lesson fields and an object-valued token ID. The corrected call preserves lesson values and derives token ID from authenticated claims. Server-fixed owner and Naya identity remain unchanged.

The independent verifier now downloads the producer's lineage artifact before reading it. A workflow regression test failed before that addition. The live Python request now includes the already-required `index_id`.

Validation after repair: **3 Node handler tests passed; 162 Python tests passed, 3 skipped**. Handler tests cover binding, caller identity spoof resistance, missing/wrong workflow refusal and RPC refusal. JWT cryptography, actual database grants and persisted lineage are not tested by these offline stubs. CI installs Node 24 and runs these tests.

Reproduce offline from repo root:

```bash
node --test tests/*.test.mjs
env -u NAYA_RUNTIME_OIDC_TOKEN -u NAYANET_INTELLIGENCE_COMMIT_GRANT_ID -u SUPABASE_USER_ACCESS_TOKEN PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -rs -p no:cacheprovider
```

## Prioritized gaps (bounded to ten)

This dated assessment supports the existing operations queue; it does not supersede human direction or create another control plane. The latest #913 direction places complete Node-0001 proof before replication and interface expansion.

1. **Repair fresh-lesson entry and verification handoff** — candidate in this branch; accept only after canonical deployment and independent lineage reread succeed for a newly created lesson.
2. **Restore deployment/source parity** — use the established deployment path; accept exact canonical SHA equality. Never weaken the STALE gate.
3. **Bind succession to current learning** — pass the promoted/reread learning ID as an artifact through both successor jobs, resolve its actual block, enforce owner/target/ACTIVE scope. Fixed old specimen success is insufficient.
4. **Replace declared learning effects with observed effects** — coordinate existing [PR #888](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/888); measure held-out control/treatment outcomes independently, preserve negative evidence.
5. **Resolve remaining live failures** — collect bounded diagnostic responses for learning-influence 400 and inspect the CVO clock failure; no unsupported common-cause claim or relaxed token validation.
6. **Audit the nine-node lifecycle** — trace each existing responsibility through birth, authority, retrieval, action, observation, learning and succession; tie gaps to executable cases, not more prose alone.
7. **Reconcile knowledge and relationships** — inventory all 16 source files, compare #7/#8 semantically, explicitly decide mapping; avoid silently merging distinct material or promoting candidate relationships.
8. **Reconcile activation pointers** — review #915 against clean-start main; resolve missing control-plane/team/Hub pointers without resurrecting historical architecture by default.
9. **Emit canonical resolution and activation receipts** — resolve existing sources by role/revision and record read scopes, conflicts, grants and next step durably in established state. Prove a cold successor can use them without this chat.
10. **Bind the Hub after continuity acceptance** — project canonical state and proof labels; add consent-scoped network participation tests before scaling collective access or node replication.

## Unknowns

Uninspected deployment functions/tables may exist beyond current source. The deployed original smart-note receiver is not inferred absent merely because its source is missing from main. Full cross-owner privacy, graph applicability/supersession, revocation behavior, application-wide runtime binding and held-out causal improvement remain unproven. Open PRs are proposals until merged. This is an evidence-bounded audit, not an exhaustive security review or inventory of every production resource.

## Exactly one next action

**Promote this bounded fresh-lesson repair through review and the canonical deployment path, then run one fresh-lesson proof and independently reread all seven linked IDs.** Stop on refusal or mismatch; attach exact SHA, deployment version, run URL and receipt IDs to #913. This establishes the entry prerequisite without claiming #913 is closed.

## Cold successor handoff

Start from current main, not this dated assessment alone. Read the repository activation instructions, clean-start, North Star ratification, kernel manifest and registry; reconcile them with #913's latest direction and #554 ownership. Recheck the missing-path and open-PR observations against the new SHA. This branch is a candidate until its PR and deployment are verified.

Carry forward: assessed/implemented/deployed SHAs separately; the seven fresh lineage IDs; learning and successor IDs; exact evidence URLs; failed/skipped gates; the scope and source of authority; unresolved conflicts; active ownership; and one bounded next step. Preserve provenance and consent scope, not secrets or reusable runtime credentials. Release the #554 reservation with PR/test details when this pass finishes. Do not inherit authority simply because you inherit these notes.
