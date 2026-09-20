# NayaPOWER — Constitutional Governance / Authority Audit

DATE: 2026-09-11
STATUS: SOURCE-LEVEL AUDIT / UNVERIFIED RUNTIME
BASELINE: main @ 18f8451596afd37267c272fb5fb9ff1a8b273acc
MISSION: Build NayaPOWER as the model-agnostic constitutional governance layer governing human authority, machine intelligence, and consequential action.

## PURPOSE

Audit the next constitutional layer without treating documentation as runtime proof. Determine whether the governing model explicitly represents the required controls as:

1. constitutional law;
2. machine-checkable contract;
3. runtime enforcement;
4. observable evidence;
5. review / OSCAR;
6. successor continuity.

## CURRENT FINDING

The Governance Act is materially aligned with the governance-layer ontology and establishes a strong written authority hierarchy. The runtime kernel also separates authority from tool execution and records verification evidence. However, the implementation is not yet a complete machine-enforced governance layer.

The principal implementation gap is the absence of a first-class machine-readable Authority Registry and a corresponding enforcement boundary that evaluates consequence, reversibility, stopping conditions, authority scope, and responsible value as governed decision inputs rather than merely candidate metadata.

## COVERAGE MATRIX

| Control | Constitutional law | Machine-checkable contract | Runtime enforcement | Observable evidence | Review / OSCAR | Successor continuity | Finding |
|---|---|---|---|---|---|---|---|
| Human authority | YES | PARTIAL | PARTIAL | YES | YES | YES | Authority exists conceptually, but domain-scoped authority is not yet registry-backed/enforced. |
| Machine intelligence | YES | YES/PARTIAL | PARTIAL | YES | YES | YES | Intelligence is separated from governance, but runtime does not independently enforce all governance boundaries. |
| Capability | YES | YES | PARTIAL | YES | YES | YES | ActionCandidate exposes executability/tool capability, but capability is not fully separated from authority through a registry. |
| Authority | YES | PARTIAL | PARTIAL | YES | YES | YES | Authority enum exists; domain authority ownership and scoped authorization are still future Registry work. |
| Consequence | YES | PARTIAL | NO/PARTIAL | PARTIAL | YES | YES | consequence exists as candidate metadata and prose, but no hard consequence gate is enforced by the kernel. |
| Reversibility | YES | YES | NO/PARTIAL | PARTIAL | YES | YES | reversible is represented and ranked, but irreversible actions are not independently blocked/escalated by runtime. |
| Risk | YES | YES/PARTIAL | PARTIAL | YES | YES | YES | MissionState stores risks and quality gates review them, but risk classification does not yet form a hard execution gate. |
| Evidence | YES | YES | YES | YES | YES | YES | EvidenceState, receipts, commit/deployment fields, and verification gates provide a real foundation. |
| Verification | YES | YES | YES | YES | YES | YES | VERIFIED/LIVE_VERIFIED are explicit; host execution requires observed evidence before promotion. |
| Continuity | YES | YES | YES | YES | YES | YES | Mission State + receipts + continuation contract provide durable continuity; runtime proof remains pending until Torch-Pass executes. |
| Stopping conditions | YES | PARTIAL | PARTIAL | PARTIAL | YES | YES | Governance Act defines stop gates; runtime mainly returns human/external handoff when no eligible action exists. Explicit stop-state enforcement is incomplete. |
| Responsible value optimization | YES | PARTIAL | PARTIAL | YES | YES | YES | Value/scorecard/OSCAR exist, but runtime candidate selection lacks a dedicated responsible-value function combining authority, consequence, reversibility, evidence, and risk. |

## IMPORTANT SOURCE FINDINGS

### 1. Governance Act

`.naya/2026-09-11-18-05-NAYAPOWER-30-GOVERNANCE-ACT.md` correctly distinguishes Constitution, Governance, Architecture, Activation, and Execution. It establishes a tiered authority hierarchy, domain ownership, conflict resolution, verification governance, value governance, privacy, failure, continuity, and the requirement for an Authority Registry.

The Act explicitly says Lead Mode is an execution mode rather than a transfer of sovereignty and defines stop gates. This is strong constitutional/operational design.

### 2. Runtime kernel

`SUPERBRAIN/runtime/naya_power_runtime.py` already contains:

- explicit EvidenceState values including UNKNOWN, CONFLICTED, VERIFIED, and LIVE_VERIFIED;
- Authority values distinct from execution output;
- ActionCandidate authorization/constitutional/dependency/protected-scope gates;
- reversible and consequence fields;
- evidence receipts carrying source, commit, deployment, and verification state;
- MissionState known/observed/verified/unknown/blocker/risk state;
- deterministic rejection of ineligible actions;
- no false VERIFIED state when receipt evidence is not VERIFIED/LIVE_VERIFIED.

But `ActionCandidate.eligible()` does not hard-gate `consequence`, `reversible`, or `evidence_ready`; those values currently influence ranking or remain metadata. The kernel therefore does not yet implement the full Governance Act stop/risk/reversibility model as a constitutional execution gate.

### 3. Host execution bridge

`SUPERBRAIN/runtime/host_executor.py` correctly states that it never grants authority, requires an explicit executor, requires independently observed evidence, and surfaces human-required actions as handoffs. This is a correct capability/authority separation.

The bridge does not itself perform a domain-scoped authority decision; it relies on the candidate provider and kernel. That is acceptable for the current boundary but leaves the Authority Registry/enforcement layer unfinished.

### 4. Quality / OSCAR

`SUPERBRAIN/runtime/quality_gate.py` correctly prevents a score from overriding constitutional hard gates, requires valid scorecard evidence, requires a minimum responsible score of 9.5, and blocks promotion when OSCAR finds blocking defects.

Quality is therefore a promotion gate, not a substitute for authority or safety. The remaining gap is that responsible value selection occurs before this post-execution quality gate and is not yet a first-class constitutional decision function.

## ARCHITECTURAL CONCLUSION

DO NOT rewrite the architecture.

DO NOT make NayaPOWER autonomous.

DO NOT merge Naya, intelligence, agent, runtime, and governance into one object.

The correct next surgical architecture is:

**HUMAN AUTHORITY → AUTHORITY REGISTRY → GOVERNED DECISION CONTRACT → RUNTIME GATE → AUTHORIZED EXECUTOR → OBSERVATION → VERIFICATION → SCORECARD / OSCAR → CONTINUITY**

with:

**CAPABILITY != AUTHORITY**

and:

**INVALID != ZERO VALUE**

and:

**SOURCE INTENT != RUNTIME TRUTH**

## NEXT IMPLEMENTATION TARGET

Build the minimum Authority Registry + governed decision contract needed to make the following machine-checkable without creating a second authority system:

- authority owner and scope;
- action capability;
- consequence class;
- reversibility;
- risk;
- evidence requirement;
- verification requirement;
- stopping condition;
- responsible-value eligibility;
- escalation / human-decision requirement;
- canonical evidence and successor receipt.

The registry must be subordinate to the Constitution and Governance Act, domain-scoped, versioned, and auditable.

## VERIFICATION BOUNDARY

This audit is SOURCE-LEVEL ONLY.

It does not prove:

- GitHub Actions execution;
- canonical Torch-Pass execution;
- runtime deployment behavior;
- production behavior;
- public/user-facing behavior;
- exact-host enforcement in a live environment.

Foundation remains UNVERIFIED until the canonical Naya Continuous Torch-Pass Gate executes against the exact current HEAD and its complete runtime evidence is inspected.

## PROTECTED BASELINE

Preserve the existing constitutional ontology, Runtime Constitution, Intelligence Operating Model, activation semantics, Mission State persistence, quality gate, host executor boundary, Smart Note contracts, continuity gate, and canonical Torch-Pass workflow.

Make only the minimum surgical changes required by verified findings.
