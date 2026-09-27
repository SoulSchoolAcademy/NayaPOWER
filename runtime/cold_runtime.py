"""Executable cold-runtime seam: manifest → canonical memory → kernel decision."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from kernel.nayapower_kernel import Authority, DecisionContext, Kernel
from runtime.canonical_memory import (
    CanonicalMemoryConfiguration,
    SupabaseCanonicalMemory,
)


def cold_restore_and_decide(
    root: Path,
    *,
    block_id: str,
    action: str,
    consequential: bool,
    task_target: str | None = None,
    authority_scope: str | None = None,
    configuration: CanonicalMemoryConfiguration | None = None,
) -> dict[str, object]:
    """Boot the canonical manifest, retrieve one block, then run the real kernel."""

    kernel = Kernel.from_brain(root)
    memory = SupabaseCanonicalMemory(
        configuration or CanonicalMemoryConfiguration.from_environment()
    )
    block = memory.retrieve_block(block_id)
    relationships = memory.retrieve_relationships(block.intelligent_block_id)
    authority = (
        Authority(scope=authority_scope)
        if authority_scope is not None
        else None
    )
    decision = kernel.decide(
        DecisionContext(
            action=action,
            consequential=consequential,
            authority=authority,
            task_target=task_target,
            intelligence=(block,),
            relationships=relationships,
        )
    )
    return {
        "kernel_id": kernel.kernel_id,
        "source_manifest": kernel.source_manifest,
        "retrieval": {
            "block_id": block.block_id,
            "intelligent_block_id": block.intelligent_block_id,
            "version": block.version,
            "status": block.status,
            "understanding_state": block.understanding_state,
            "owner_scope": block.owner_scope,
            "subject_id": block.subject_id,
            "source_event_ids": list(block.source_event_ids),
            "provenance": block.provenance,
            "applicable": block.is_applicable_to(task_target),
            "relationships": [
                {
                    "relationship_id": relationship.relationship_id,
                    "source_id": relationship.source_id,
                    "target_id": relationship.target_id,
                    "relationship_type": relationship.relationship_type,
                    "epistemic_state": relationship.epistemic_state,
                }
                for relationship in relationships
            ],
        },
        "decision": asdict(decision),
        "truth_contract": {
            "retrieved_is_not_authorized": not (
                consequential
                and decision.allowed
                and authority is None
            ),
            "execution_truth_state": decision.truth_state.value,
        },
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--block-id", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--task-target")
    parser.add_argument("--consequential", action="store_true")
    parser.add_argument("--authority-scope")
    args = parser.parse_args()

    result = cold_restore_and_decide(
        Path(args.root).resolve(),
        block_id=args.block_id,
        action=args.action,
        consequential=args.consequential,
        task_target=args.task_target,
        authority_scope=args.authority_scope,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
