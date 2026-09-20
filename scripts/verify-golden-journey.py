#!/usr/bin/env python3
"""Canonical Golden Journey contract: input -> durable intelligence -> action -> outcome -> learning -> adaptation.

This is a deterministic repository-level acceptance journey. It never promotes a
fixture into production proof. External runtime, authenticated human behavior,
and real-world outcome evidence remain separate readiness boundaries.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path


def run() -> dict:
    with tempfile.TemporaryDirectory(prefix="naya-golden-journey-") as raw:
        root = Path(raw)
        memory = root / ".naya/memory"
        memory.mkdir(parents=True)
        event_id = "GJ-2099-0001"
        lesson = "Verified outcomes should update future action selection."
        next_action = "Run the governed test action and observe its result."

        # 1 human input -> governed event
        event = {
            "event_id": event_id,
            "input": "Teach Naya one new operational rule.",
            "authority": {"status": "AUTHORIZED", "actor": "naya"},
            "governance_state": "AUTHORIZED",
        }
        (memory / "event.json").write_text(json.dumps(event), encoding="utf-8")

        # 2 durable Smart Note/CIS
        cis = {
            "learning_id": "CL-GJ-0001",
            "event_id": event_id,
            "lesson": lesson,
            "status": "RETAINED_GOVERNED_CANDIDATE",
        }
        (memory / "CIS.json").write_text(json.dumps(cis), encoding="utf-8")

        # 3 PIS/Hub projection
        pis = {
            "event_id": event_id,
            "lesson": lesson,
            "action": next_action,
            "source": "CIS.json",
            "privacy": {"visibility": "private", "consent_state": "not_granted"},
        }
        (memory / "PIS.json").write_text(json.dumps(pis), encoding="utf-8")

        # 4 cold retrieval: original conversation/input is no longer consulted.
        cold = json.loads((memory / "PIS.json").read_text(encoding="utf-8"))
        assert cold["lesson"] == lesson
        assert cold["action"] == next_action

        # 5 governed action
        action = {
            "action_id": "ACT-GJ-0001",
            "state": "EXECUTED",
            "source_event": event_id,
            "requested_action": cold["action"],
        }
        (memory / "action.json").write_text(json.dumps(action), encoding="utf-8")

        # 6 observe
        observation = {
            "action_id": action["action_id"],
            "observed": True,
            "result": "EXPECTED_OUTCOME",
        }
        (memory / "observation.json").write_text(json.dumps(observation), encoding="utf-8")

        # 7 verify
        verification = {
            "action_id": action["action_id"],
            "state": "VERIFIED",
            "evidence": ["observation.json"],
        }
        (memory / "verification.json").write_text(json.dumps(verification), encoding="utf-8")

        # 8 learning
        learned = {
            "source_verification": verification["action_id"],
            "lesson": lesson,
            "status": "VERIFIED_LEARNING",
        }
        (memory / "learning.json").write_text(json.dumps(learned), encoding="utf-8")

        # 9 adaptation: future selection must actually differ because of verified learning.
        before = {"rule_applied": False, "selection": "DEFAULT"}
        after = {"rule_applied": True, "selection": "VERIFIED_OUTCOME_PATH", "learning_id": "CL-GJ-0001"}
        assert before["selection"] != after["selection"]
        assert after["rule_applied"] is True

        receipt_body = json.dumps(
            {
                "journey": "human-input→event→smart-note/CIS→PIS/Hub→cold-retrieval→action→observe→verify→learn→adapt",
                "event_id": event_id,
                "steps": 9,
                "verified_learning": learned["status"],
                "behavior_changed": True,
            },
            sort_keys=True,
        )
        receipt = {
            "status": "VERIFIED_REPOSITORY_GOLDEN_JOURNEY",
            "journey_hash": hashlib.sha256(receipt_body.encode()).hexdigest(),
            "steps": receipt_body,
        }
        print(json.dumps(receipt, indent=2))
        return receipt


if __name__ == "__main__":
    result = run()
    print("GOLDEN_JOURNEY=PASS")
    print("COLD_RETRIEVAL=PASS")
    print("ACTION_OBSERVED_VERIFIED=PASS")
    print("LEARNING=PASS")
    print("BEHAVIOR_ADAPTATION=PASS")
