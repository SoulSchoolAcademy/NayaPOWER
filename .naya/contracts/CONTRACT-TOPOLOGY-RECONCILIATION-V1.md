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
