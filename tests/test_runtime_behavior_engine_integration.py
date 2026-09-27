from kernel.nayapower_kernel import Kernel


def test_runtime_kernel_drives_canonical_nine_node_behavior_engine():
    kernel = Kernel()

    result = kernel.execute_governed_cycle(
        {
            "identity": {
                "actor_id": "naya-test",
                "system_id": "NayaPOWER",
                "owner_id": "owner-1",
            },
            "mission": {
                "mission": "prove runtime convergence",
                "objective": "execute the canonical nine-node cycle",
            },
            "proposed_action": {
                "type": "runtime_convergence_test",
                "expected_outcome": "retained intelligence changes governed behavior",
                "proof_requirements": ["independent"],
            },
            "authority": {
                "grant_id": "test-grant",
                "revoked": False,
                "expires_at": None,
            },
            "intelligent_block_id": "IB-NAYA-NODE-0001-0001",
            "query": "retrieve retained intelligence",
            "intelligence": [
                {
                    "id": "IB-NAYA-NODE-0001-0001",
                    "owner_id": "owner-1",
                    "epistemic_state": "VERIFIED",
                    "provenance": {"source": "test"},
                }
            ],
            "claim": "retained intelligence changes governed behavior",
            "evidence": [{"provenance": "test://outcome"}],
            "evidence_strength": "STRONG",
            "observed_outcome": "retained intelligence changes governed behavior",
            "independent_evidence": [{"provenance": "test://independent"}],
            "holdout_result": True,
            "applicability_conditions": ["runtime_convergence"],
            "current_state": {"truth": "test"},
            "unknowns": [],
            "blockers": [],
            "relationships": [],
            "intelligent_block_ids": ["IB-NAYA-NODE-0001-0001"],
            "next_action": "cold successor continuation",
            "kernel_revision": "runtime-convergence-v1",
        }
    )

    assert result["runtime_boot"]["overall_status"] == "READY"
    assert result["status"] == "COMPLETED"
    assert result["nodes_processed"] == [
        "SELF",
        "LAW",
        "ACT",
        "KNOW",
        "PROVE",
        "CONNECT",
        "VERIFY",
        "LEARN",
        "EVOLVE",
    ]
    assert result["node_receipts"]["VERIFY"]["status"] == "VERIFIED"
    assert result["node_receipts"]["LEARN"]["status"] == "PROMOTED"
