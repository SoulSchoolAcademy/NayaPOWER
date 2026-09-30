# Nine-Node Kernel — Execution Model V1

**Kernel:** SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE

## 1. Purpose

The nine Nodes form a coordinated cognitive/governance loop.

They are not nine sequential prompts and not nine independent agents. They are nine responsibilities that must be available to the execution algorithm.

## 2. Responsibilities

| Node | Input focus | Output focus |
|---|---|---|
| SELF | identity, mission, state | execution identity/context |
| LAW | authority, policy, consent | permitted/refused scope |
| ACT | intent, priorities, available actions | proposed/selected action |
| KNOW | relevant intelligence | contextual knowledge |
| PROVE | evidence, provenance | trust/evidence assessment |
| CONNECT | relationships, applicability | routed intelligence graph |
| VERIFY | observed result | verified/unknown/failed outcome |
| LEARN | verified outcome | learning candidate/result |
| EVOLVE | verified learning + system evidence | bounded improvement/successor |

## 3. Critical ordering

SELF and LAW establish the boundary before consequential action.

KNOW, PROVE, and CONNECT enrich action.

VERIFY determines what actually happened.

LEARN may only promote from verified experience.

EVOLVE may only change the system through governed change.

## 4. Execution record

Every meaningful kernel run should preserve:

```
run_id
execution_identity
kernel_version
node_versions
input/context
authority_context
retrieval_set
node_trace
decision
action
observation
outcome
verification
learning
successor
```

## 5. Integrity failure

The kernel must stop or degrade explicitly when:

- identity is unresolved;
- authority is missing;
- required Node is absent;
- critical evidence conflicts;
- applicable intelligence is stale;
- verification is unavailable for a required claim;
- successor ownership cannot be established.

A partial kernel must never masquerade as a full kernel.

## 6. Ablation proof

Behavioral proof requires comparison between:

**CONTROL:** relevant kernel capability unavailable.

**TREATMENT:** relevant kernel capability available.

The test must measure an observable behavioral difference attributable to the treatment.
