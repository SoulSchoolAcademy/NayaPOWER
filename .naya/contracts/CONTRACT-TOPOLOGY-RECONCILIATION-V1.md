# NayaPOWER Contract Topology Reconciliation V1

**Status:** WORKING RECONCILIATION — evidence-bound, not ratified  
**Branch:** naya/canonical-contract-registry-2026-09-26  
**Purpose:** Assign one clear normative owner to each material responsibility before creating or rewriting contracts.

## Critical correction from Registry V1

The first registry pass incorrectly described the Execution Protocol as absent. Repository inspection proves that **EP-001 already exists** at:

`.naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md`

Its status is **PROPOSED**, not missing. Therefore the correct action is **EXTEND/HARDEN + reconcile surrounding execution laws**, not CREATE a second Execution Protocol.

This correction is itself evidence that topology reconciliation must precede contract creation.

## Requirement → Owner → Authority → Dependency → Acceptance

| Requirement | Proposed current owner | Authority | Key dependencies | Acceptance boundary | Current disposition |
|---|---|---|---|---|---|
| Constitutional law | .naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md | constitutional layer | human authority/platform constraints | all subordinate contracts obey it | CONFLICTED with control-plane constitutional pointer |
| Contract-library governance | .naya/contracts/00-CONTRACT-STACK-OPERATING-LAW.md | constitutional subordinate law | Constitution | contract changes follow governed lifecycle | CANONICAL |
| Execution behavior | EP-001 .naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md | Constitution | authority + mission + state | authorized objective causes proactive verified progression + continuation | PROPOSED; EXTEND/HARDEN |
| Legacy execution policy/laws | distributed .naya execution/protocol/control-plane artifacts | subordinate execution policy | EP-001 | each supporting artifact has non-overlapping role | OVERLAP TO RECONCILE |
| Mission definition | Mission Contract + control-plane mission state | constitutional + live state | Constitution | objective/success/current mission reconstructable | EXISTING; ownership reconciliation |
| Naya identity | NAYA-SUBJECT-IDENTITY-CONTRACT-V1.json | constitutional/identity authority | human authority | canonical runtime identity established and stable | CANONICAL CONTRACT |
| Subject binding | NAYA-SUBJECT-BINDING-CONTRACT-V1.json | identity layer | subject identity | runtime actor maps to governed subject without ambiguity | CANONICAL / binding proof pending |
| Authority/consent | authority registries + constitutional law | human authority | identity | actor, scope, consent, expiration, revocation are explicit | EXISTING; reconcile ownership |
| Durable intelligence intake | 03-RECEIVER.md + PRIMARY-INTELLIGENCE-SYSTEM-CONTRACT-V1.json | intelligence/governance | identity + authority | one governed creation path | CANONICAL / integration proof scope varies |
| Intent transmission | 04-SENDER.md | execution/intelligence flow | authority + receiver | intent reaches Receiver without local canonical identity | CANONICAL |
| IB identity/lifecycle | 01-SMART-NOTE-INTELLIGENT-BLOCK.md | intelligence layer | Receiver | receiver-issued immutable identity and lifecycle | CANONICAL |
| Smart Note projection | INT-001 .naya/contracts/01-INTELLIGENCE/01-SMART-NOTE-AND-SMART-LINK.md | intelligence layer | IB + Receiver | exact human-readable projection | PROPOSED |
| Smart Link semantics | INT-001 + 02-SMART-LINK.md + SMART-LINK-CONTRACT.json | intelligence layer | Smart Note | one unambiguous noun and acceptance test | CONFLICTED |
| Proof/evidence semantics | 08-PROOF-RECEIPT.md + PROOF.json + receipt schema | proof layer | execution + runtime | claim strength never exceeds evidence | OVERLAP TO RECONCILE |
| Verified AI Action | VERIFIED-AI-ACTION-V1.md | proof/action layer | authority + proof | authorized action and consequence are independently evidenced | EXISTING / proof mapping pending |
| Causal verification | .github workflow + project-intelligence evidence; no single inspected canonical feature contract | proof/action layer | verified action + outcome | causal relation between action and outcome established | MISSING OR EXTEND — decide after deeper inspection |
| Learning | 09-LEARNING.md | intelligence/learning | outcome + verification | reusable learning requires evidence and verified application | CANONICAL |
| Ledger/accountability | SMART-LEDGER-CCT-MACHINE-CONTRACT-V1.md + event schema | accountability layer | action/proof | actor→authority→action→result→receipt→verification lineage | EXISTING; runtime proof varies |
| Continuity/successor | 10-CONTINUITY-SUCCESSOR.md | continuity layer | state + proof + next action | cold successor reconstructs and continues correctly | CANONICAL contract |
| Baton / next action | BATON-CONTRACT.md + BATON.json + NAYA-NEXT-ACTION-HANDOFF schema | continuity/execution | state + active block | exactly one executable next action | CANONICAL; not a second state machine |
| Hub projection/experience | 05-HUB-CONSUMPTION.md + Hub contracts | Hub layer | canonical intelligence + retrieval | Hub projects canonical intelligence and does not become source | CANONICAL / runtime evidence separate |
| Production parity | production verification artifacts + Hub runtime contract | deployment/proof | source identity + deployment | exact claim-relevant source/deployment parity | EXISTING proof law; topology boundary to reconcile |

## Immediate ownership conclusions

### 1. Execution Protocol is not missing

EP-001 is the correct candidate owner for **execution behavior**. It already contains the required proactive ownership principle:

**LEAD THE WORK, NOT THE HUMAN.**

It also defines continuous verified progress, next-action selection, blocker handling, evidence preservation, continuation handoff, and explicit stop conditions.

Its present weakness is **status and integration**, not absence.

The topology task is therefore:

**EP-001 = normative execution behavior**  
**Master Execution / Activation / Lead Mode / Continuous Execution Policy = supporting implementation/policy layers unless evidence proves they own distinct normative boundaries.**

No second Execution Protocol should be created.

### 2. Baton is continuation, not a competing work queue

BATON-CONTRACT.md explicitly states that BATON does not become a second project state machine.

The control-plane sources retain ownership of their respective state/navigation/proof boundaries, while BATON assembles the continuation object.

Therefore the desired topology is:

**STATE = current operational state**  
**BLOCKS = active block + one next action**  
**MAP = mission/system/authority navigation**  
**PROOF = proof/evidence law and proof claims**  
**BATON = coherent successor continuation projection**

The next-action handoff schema is a machine format, not a competing authority.

### 3. Smart Link has a three-artifact semantic collision

The repository contains:

- `01-INTELLIGENCE/01-SMART-NOTE-AND-SMART-LINK.md` — INT-001, PROPOSED, narrow Smart Link semantics;
- `02-SMART-LINK.md` — narrow direct Smart Note link;
- `SMART-LINK-CONTRACT.json` — broad target_type enum.

This must be reconciled before INT-001 ratification.

### 4. Constitutional authority must be reconciled before downstream ratification

The new constitutional law is explicitly marked RATIFIED, while live control-plane material still contains a different constitutional pointer. The registry must not silently treat the pointer as irrelevant or silently rewrite it.

Required resolution:

**identify source versions → establish intended supersession → update authoritative navigation → verify no stale constitutional pointer remains.**

If the repository itself cannot establish the final precedence, the affected decision remains **UNKNOWN / HUMAN DECISION REQUIRED**.

## Contract disposition rules

Use these dispositions rather than inventing documents:

- **CREATE** — no adequate owner exists and the boundary is independently governed.
- **EXTEND** — an existing contract owns the boundary but lacks required normative detail.
- **MERGE** — two artifacts claim the same normative boundary without meaningful separation.
- **SCHEMA** — machine representation only; subordinate to the owning contract.
- **LAW** — cross-cutting constitutional/governance rule, not a feature contract.
- **NOT NEEDED** — requirement is already completely owned elsewhere.
- **UNKNOWN** — evidence insufficient to decide safely.

## Current P0 topology queue

1. Constitutional authority reconciliation.
2. EP-001 integration: define its exact relationship to existing execution laws and machine enforcement.
3. Smart Link semantic reconciliation.
4. Proof/verification ownership reconciliation.
5. Identity/authority/binding ownership reconciliation.
6. Causal Verification Object boundary decision.
7. Refusal/revocation/replay ownership decision.
8. Receiver/Sender/PIS boundary reconciliation.
9. Continuity/Baton/next-action ownership reconciliation.
10. Update registry and produce ratification-ready topology map.

## Acceptance test

The topology is ready for contract hardening only when:

- every material normative requirement has exactly one owner;
- supporting artifacts are explicitly subordinate and do not compete;
- every machine schema has a named normative owner;
- every cross-cutting law has explicit authority;
- Smart Link has one semantic definition;
- execution has one normative owner;
- next-action has one state authority;
- proof has one claim/evidence authority;
- constitutional precedence is explicit;
- unresolved items are marked UNKNOWN/CONFLICTED rather than inferred;
- each P0 boundary has an executable acceptance test;
- the registry can tell the next Naya exactly what to execute next.

## Required next action

**CONTRACT-TOPOLOGY-002: reconcile constitutional authority and execution ownership.**

Do not draft a new Execution Protocol. Harden EP-001 only after its boundary is reconciled against the existing execution stack.


## CONTRACT-TOPOLOGY-002 — CONSTITUTION + EXECUTION OWNERSHIP RECEIPT

**Date:** 2026-09-26
**Status:** VERIFIED DISCOVERY / RATIFICATION BLOCKED AT CONSTITUTIONAL PRECEDENCE

### Constitutional authority comparison

| Artifact | Version | Date/effective evidence | Authority claim | Current references | Supersession evidence | Disposition |
|---|---|---|---|---|---|---|
| `.naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md` | Proposed V1.0 | Human-director-directed 2026-09-26; explicitly marked ratified | NayaNET Constitutional Contract Law; applies to every Naya, agent, contract, capability and governed execution | New contract itself; not yet the sole control-plane pointer | **NONE FOUND in inspected repository evidence** | RATIFIED BY DOCUMENTED HUMAN DIRECTION, but repository authority chain remains conflicted |
| `.naya/codex/11-RUNTIME-CONSTITUTION.md` | V1.0 | No effective date stated in inspected header | Canonical / Constitutional; Document 11 of 20 | `.naya/control-plane/MAP.json`, `.naya/control-plane/STATE.json` still identify it as current constitutional authority | **NONE FOUND in inspected repository evidence** | CANONICAL/CONSTITUTIONAL POINTER REMAINS ACTIVE; conflict unresolved |

**Precedence finding:** the repository does **not** currently establish explicit supersession or amendment precedence between these two constitutional artifacts. The new law contains a human-directed ratification statement, but that statement does not by itself rewrite the older control-plane authority pointers. Therefore the constitutional chain remains **CONFLICTED / HUMAN DECISION REQUIRED**. No constitutional pointer was silently changed.

### Execution ownership finding

**EP-001 is the single normative execution-owner candidate and should be treated as the only normative Execution Protocol boundary.** It explicitly owns execution behavior: proactive ownership, authorized objective advancement, next-value action selection, continuous execution, dependency ordering, execution waves, verification, evidence preservation, blocker handling, safe stops, continuation, and anti-passivity.

The surrounding execution artifacts are classified as follows:

| Artifact | Classification | Relationship to EP-001 |
|---|---|---|
| `.naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md` (EP-001) | **NORMATIVE OWNER** | One bounded normative execution contract; PROPOSED; harden/integrate, do not duplicate |
| `.naya/NAYA-MASTER-EXECUTION-CONTRACT.md` | **SUPPORTING POLICY / LEGACY NORMATIVE OVERLAP** | Broad operational contract predating EP-001; its execution-behavior claims must be subordinated/reconciled rather than left as a competing owner |
| `.naya/2026-09-11-18-50-NAYAPOWER-33-MASTER-ACTIVATION-PROTOCOL.md` | **SUPPORTING POLICY** | Entry/activation procedure; restores context and mission before execution; does not own execution loop semantics |
| `.naya/2026-09-11-19-05-NAYAPOWER-34-LEAD-MODE-PROTOCOL.md` | **SUPPORTING POLICY** | Human/Naya lead-mode behavior; should defer execution mechanics to EP-001 |
| `.naya/2026-09-11-19-20-NAYAPOWER-35-MISSION-CONTRACT.md` | **SUPPORTING POLICY / MISSION BOUNDARY** | Defines mission/objective framing; not the execution engine |
| `.naya/control-plane/NAYA-CONTINUOUS-EXECUTION-POLICY.md` | **SUPPORTING POLICY + ENFORCEMENT BINDING** | Operationalizes continuous execution and lifecycle gating; it must not define a competing execution protocol |
| `.naya/NAYA-EXECUTION-CONTINUITY-AND-LEARNING-LAW.md` | **SUPPORTING CROSS-CUTTING LAW** | Governs continuity/learning relationship; EP-001 consumes its constraints |
| `.naya/NAYA-EXECUTION-EFFICIENCY-LAW.md` | **SUPPORTING POLICY** | Efficiency/optimization constraints; not normative ownership of execution behavior |
| `.naya/NAYA-EXECUTION-LOOP-ESCALATION-LAW.md` | **SUPPORTING CROSS-CUTTING LAW** | Escalation/repetition boundary; EP-001 incorporates it as an execution constraint |
| `.naya/control-plane/BATON-CONTRACT.md` | **SUPPORTING CONTINUATION CONTRACT** | Owns continuation boundary, not execution behavior |
| `.naya/contracts/NAYA-NEXT-ACTION-HANDOFF-V1.schema.json` | **MACHINE SCHEMA** | Projects one next action/handoff; subordinate to BLOCKS + EP-001 + Baton relationship |
| `.naya/control-plane/BLOCKS.json` | **CURRENT STATE / NEXT-ACTION AUTHORITY** | Owns active block and exactly one project-level next action; not a second execution protocol |
| `.naya/control-plane/BATON.json` | **CONTINUATION PROJECTION** | Assembles continuation from STATE/BLOCKS/MAP/PROOF; does not override them |
| `.naya/control-plane/STATE.json` | **CURRENT STATE AUTHORITY** | Owns current operational state; does not select execution semantics |
| `.naya/control-plane/MAP.json` | **NAVIGATION / AUTHORITY MAP** | Owns mission/system/authority navigation; its constitutional pointer is currently conflicted |

### One-next-action authority

The topology is now explicit at the execution/continuity boundary:

**BLOCKS.json owns the single project-level next action.**

**EP-001 owns the normative rule for how Naya selects and executes that authorized action.**

**BATON.json owns the continuation handoff projection.**

**NAYA-NEXT-ACTION-HANDOFF-V1.schema.json owns only machine shape.**

**STATE.json owns current operational state; MAP.json owns navigation; PROOF.json owns proof claims/evidence rules.**

This is one next-action authority, not competing state machines.

### Contract topology acceptance status

| Acceptance condition | Result |
|---|---|
| One normative execution owner | **PASS — EP-001** |
| No second Execution Protocol created | **PASS** |
| Supporting execution artifacts classified | **PASS — evidence-backed classification above** |
| One project-level next-action authority | **PASS — BLOCKS.json** |
| Baton preserved as continuation boundary | **PASS** |
| Machine handoff schema subordinate | **PASS** |
| Constitutional precedence explicit | **BLOCKED — repository cannot establish supersession** |
| Final topology ratification-ready | **BLOCKED by constitutional conflict** |

### Safe authorized P0 frontier after reconciliation

Because constitutional precedence remains unresolved, do **not** ratify or rewrite constitutional authority. The next safe P0 work is **EP-001 hardening/integration analysis** that does not alter constitutional authority: identify exact overlapping MUST rules with the Master Execution Contract, Lead Mode, Activation, and Continuous Execution Policy; define subordinate/supporting boundaries; and produce acceptance tests proving EP-001 is the sole normative execution owner.

This work may proceed without resolving the constitutional conflict because it is repository analysis/reconciliation, not constitutional amendment. Any action that would change which constitutional artifact is authoritative remains **HUMAN DECISION REQUIRED**.

### Evidence receipt

- EP-001 exists at the exact canonical path and is V1.0 / PROPOSED.
- New Constitutional Contract Law exists and is explicitly marked RATIFIED — HUMAN-DIRECTOR DIRECTED — 2026-09-26.
- Runtime Constitution exists as V1.0 / CANONICAL / CONSTITUTIONAL.
- MAP.json and STATE.json still point to Runtime Constitution as canonical current constitution.
- No inspected repository evidence established explicit supersession/amendment of Runtime Constitution by Contract 00.
- BATON-CONTRACT explicitly says Baton is not a second project state machine.
- NAYA-NEXT-ACTION-HANDOFF schema explicitly says it is not a competing mission state machine.

### Result

**CONTRACT-TOPOLOGY-002: EXECUTED.** Constitutional authority remains **CONFLICTED / HUMAN DECISION REQUIRED**. Execution ownership is reconciled to **EP-001 as the single normative execution owner**, with existing execution artifacts retained as subordinate/supporting layers until explicit hardening is completed.


## CONTRACT-TOPOLOGY-002B — SMART LINK SEMANTIC RECONCILIATION

**Status:** VERIFIED SEMANTIC FINDING / SCHEMA CHANGE NOT YET APPLIED

The P0 Smart Link boundary was inspected after execution ownership was hardened.

**Normative semantic owner:** INT-001 / `.naya/contracts/01-INTELLIGENCE/01-SMART-NOTE-AND-SMART-LINK.md`, reinforced by `.naya/contracts/02-SMART-LINK.md`.

Both normative Markdown artifacts agree: **Smart Link means only the direct GitHub link to the canonical human-readable `smart-note.md` projection of one Receiver-created IB.** Hub Deep Link and Evidence Link are explicitly different nouns.

**Conflict:** `.naya/contracts/SMART-LINK-CONTRACT.json` currently permits `target_type = smart_note | ledger_event | value_event | collective_intelligence`. That machine schema therefore exposes multiple meanings for the same noun and violates the repository's Exact-Noun Law.

**Disposition:** `SMART-LINK-CONTRACT.json` = **MACHINE SCHEMA / MERGE-NARROW CANDIDATE**, not a competing semantic contract. The schema should be narrowed to the single normative Smart Link meaning only after a reference audit establishes whether any live implementation depends on the broad enum. No schema mutation was made in this wave because the reference/dependent surface was not yet established; guessing a compatibility impact would violate the anti-guessing law.

**Next P0 action:** audit all repository references to `SMART-LINK-CONTRACT.json` and its `target_type` values; then, if no distinct canonical generic-link owner exists, narrow the schema to `smart_note` and preserve ledger/value/collective links under their own nouns/schemas rather than calling them Smart Links.

**EP-001 hardening receipt:** EP-001 now contains an explicit normative ownership boundary and acceptance tests; status remains PROPOSED because hardening does not equal ratification/verification.


## SMART-LINK-DEPENDENCY-001 — FINAL RECEIPT

**Date:** 2026-09-26
**Result:** PARTIAL / SAFE RECONCILIATION APPLIED; DEPENDENCY PROOF REMAINS INCOMPLETE

### Authoritative evidence discovered

1. `.naya/contracts/SMART-LINK-CONTRACT.json` was introduced by commit `6611a3fe52dd0b353277c5e763b9e4b6c02b214f` on 2026-09-11. The commit creates the schema from scratch and is the direct provenance of the broad `target_type` enum.
2. The older prose `.naya/2026-09-12-NAYAPOWER-48-SMART-LINK-CONTRACT.md` was introduced by commit `03a1831b633aabf06d199c6c5929b2c3c920b591`. It defines a broader identity/intelligence-link concept, including canonical intelligence object/event links.
3. The newer canonical `.naya/codex/NAYA-LINK-IDENTITY-AND-EVIDENCE-CONTRACT-V1.md` is explicitly **CANONICAL — RATIFIED 2026-09-25** and defines Smart Link narrowly as the direct GitHub canonical `smart-note.md` link. Its enforcement test is `.naya/tests/test_smart_link_identity_contract.py`, executed by `.github/workflows/verify-smart-link-identity.yml`.
4. The current INT-001 and Contract 02 prose independently agree with that narrow definition.
5. Dedicated schemas exist for `ledger_event` and `value_event`, so those nouns already have separate machine boundaries.

### Dependency classification

| Surface | Finding |
|---|---|
| Current code/schema references to `SMART-LINK-CONTRACT.json` | **UNKNOWN** — GitHub code-search index returned no matches and cannot be treated as exhaustive |
| Current `target_type` consumers | **UNKNOWN** — no authoritative indexed consumer evidence |
| Historical provenance | **CONFIRMED** — schema created in commit 6611a3f; broad prose contract created in commit 03a1831 |
| Smart Note target | **CANONICAL / LIVE SEMANTIC OWNER** via NAYA LINK IDENTITY + INT-001 + Contract 02 |
| Ledger event target | **SEPARATE CANONICAL NOUN/SCHEMA**, not Smart Link |
| Value event target | **SEPARATE CANONICAL NOUN/SCHEMA**, not Smart Link |
| Collective intelligence target | **NO verified Smart Link consumer found; separate Collective Intelligence artifacts exist** |
| Generic-link concept | **EXISTED HISTORICALLY** in Contract 48, but newer canonical law explicitly narrows the Smart Link noun; historical broader meaning requires supersession/reconciliation, not silent coexistence |

### Safety determination

**Narrowing `target_type` is NOT yet proven safe.** There is insufficient authoritative dependency evidence to claim that no implementation, fixture, generated artifact, or historical compatibility path consumes the broad enum.

Therefore **NO schema mutation was made**.

The smallest safe reconciliation is documentation/topology-level classification: the broad JSON is now treated as a **MACHINE SCHEMA / NARROW-MERGE CANDIDATE**, while the canonical Smart Link semantic owner is the newer narrow contract family. This does not break any demonstrated live consumer because no live consumer was demonstrated; it also avoids claiming that absence from search proves safety.

### Disposition of broad schema

**MERGE / NARROW CANDIDATE — NOT RETIRED YET.**

Do not create a replacement Smart Link contract. If dependency evidence later proves the broad enum unused, narrow this existing schema in place to the canonical `smart_note` target (or retire the redundant machine schema only if the canonical machine representation is explicitly established elsewhere). If a live consumer is discovered, reconcile that consumer first.

### Validation

The existing Smart Link identity test suite is structurally consistent with the narrow definition: Hub Deep Links, wrong-IB links, and generic GitHub pages are rejected; a canonical Smart Note URL is accepted. However, this audit did not execute GitHub Actions or local test runtime, so **test execution status = UNKNOWN**, not PASS.

### Hard stops preserved

- Constitutional authority untouched.
- No replacement Smart Link contract created.
- No schema narrowing performed without dependency proof.
- UNKNOWN was not converted to PASS.
- BLOCKS / EP-001 / BATON topology preserved.

### Next authorized P0

**SMART-LINK-DEPENDENCY-002 — AUTHORITATIVE REFERENCE SWEEP:** obtain complete repository bytes through a source that permits whole-tree materialization (local clone/authorized workspace or equivalent), then run exact literal-reference scans for `SMART-LINK-CONTRACT.json`, `nayanet://contracts/smart-link-v1`, `target_type`, and each enum value across source, tests, workflows, fixtures, generated artifacts, and historical compatibility surfaces. Reconcile any discovered consumer before changing the schema.
