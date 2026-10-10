"""Stage definitions for the nine-node pipeline.

Each stage declares: its position in the execution order, what it consumes,
what it produces, and — for the three nodes with no implementation — the
explicit NOT_IMPLEMENTED marker with the named reason. Naya 1's law: a stage
that doesn't exist must say so loudly, never pretend.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class StageId(str, Enum):
    SELF = "SELF"
    ACT = "ACT"
    LAW = "LAW"
    KNOW = "KNOW"
    PROVE = "PROVE"
    CONNECT = "CONNECT"
    VERIFY = "VERIFY"
    LEARN = "LEARN"
    EVOLVE = "EVOLVE"


# Canonical execution order: SELF → LAW → ACT → KNOW → PROVE → CONNECT →
# VERIFY → LEARN → EVOLVE
STAGE_ORDER: tuple[StageId, ...] = (
    StageId.SELF,
    StageId.LAW,
    StageId.ACT,
    StageId.KNOW,
    StageId.PROVE,
    StageId.CONNECT,
    StageId.VERIFY,
    StageId.LEARN,
    StageId.EVOLVE,
)


@dataclass(frozen=True)
class StageContract:
    """The binding contract for one pipeline stage."""

    stage: StageId
    consumes: str
    produces: str
    implemented: bool
    implementation: str
    not_implemented_reason: str = ""


STAGE_CONTRACTS: dict[StageId, StageContract] = {
    StageId.SELF: StageContract(
        stage=StageId.SELF,
        consumes="capture {lesson_id, actor_id, system_id, mission, objective}",
        produces="identity context {actor_id, system_id, role, checkpoint_id}",
        implemented=True,
        implementation="kernel/self_node.py::SelfNode.cold_boot (in-process)",
    ),
    StageId.LAW: StageContract(
        stage=StageId.LAW,
        consumes="identity + action {owner_id, naya_id, action}",
        produces="authority decision {AUTHORIZED | BLOCKED | NEEDS_HUMAN_AUTHORIZATION}",
        implemented=True,
        implementation="supabase/functions/nayanet-law-runtime/law.ts::evaluateLaw (node bridge)",
    ),
    StageId.ACT: StageContract(
        stage=StageId.ACT,
        consumes="authority decision + capture",
        produces="execution plan {plan_id, steps, baseline_behavior}",
        implemented=True,
        implementation="supabase/functions/nayanet-act-runtime/act.ts::buildActPlan (node bridge)",
    ),
    StageId.KNOW: StageContract(
        stage=StageId.KNOW,
        consumes="capture {task, required_capability} + candidate blocks",
        produces="interpretation {essence, applicability, selected_block_id | MISS}",
        implemented=True,
        implementation="supabase/functions/nayanet-know-runtime/know.ts::selectKnowContext (node bridge)",
    ),
    StageId.PROVE: StageContract(
        stage=StageId.PROVE,
        consumes="interpretation + capture",
        produces="evidence binding {assessment, evidence_refs, provenance}",
        implemented=True,
        implementation="supabase/functions/nayanet-prove-runtime/prove.ts::assessKnowProof (node bridge)",
    ),
    StageId.CONNECT: StageContract(
        stage=StageId.CONNECT,
        consumes="evidence binding + knowledge graph",
        produces="connections {related_blocks, conflicts, downstream_consumers}",
        implemented=False,
        implementation="NONE",
        not_implemented_reason=(
            "CONNECT_NOT_IMPLEMENTED: no ConnectNode, no connect-runtime, and no "
            "connection-writing code exists anywhere in the repository (wiring "
            "manifest 2026-10-09: 0/3 bindings). The stage cannot execute."
        ),
    ),
    StageId.VERIFY: StageContract(
        stage=StageId.VERIFY,
        consumes="capture + evidence binding",
        produces="admission verdict {admitted | rejected + reason_codes}",
        implemented=True,
        implementation=(
            "tools/learning_admission_gate.py::admit_candidate — the pinned "
            "behavioral twin of the WO3 TypeScript gate (38/38 fixtures "
            "verdict-identical). Production binding targets the WO3 TS gate at "
            "nayanet-learning-verify once merged and deployed. Do NOT reimplement."
        ),
    ),
    StageId.LEARN: StageContract(
        stage=StageId.LEARN,
        consumes="admitted lesson",
        produces="retained usable knowledge {admitted_to_active_set, retrievable}",
        implemented=True,
        implementation="orchestrator/learn_node.py::LearnNode.admit (in-process)",
    ),
    StageId.EVOLVE: StageContract(
        stage=StageId.EVOLVE,
        consumes="applied outcomes over time",
        produces="improvement measurement {delta_vs_baseline, corrections}",
        implemented=False,
        implementation="NONE",
        not_implemented_reason=(
            "EVOLVE_NOT_IMPLEMENTED: no EvolveNode and no evolve-runtime exist in "
            "the repository (wiring manifest 2026-10-09: 0/3 bindings). The stage "
            "cannot execute."
        ),
    ),
}


def implemented_stages() -> list[StageId]:
    return [s for s in STAGE_ORDER if STAGE_CONTRACTS[s].implemented]


def missing_stages() -> list[StageId]:
    return [s for s in STAGE_ORDER if not STAGE_CONTRACTS[s].implemented]
