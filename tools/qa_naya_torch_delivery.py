#!/usr/bin/env python3
"""Machine acceptance test for Naya-owned human-facing torch delivery."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
import continuity_enforcement as ce  # noqa: E402


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def fixture() -> dict:
    policy = ce.load_policy()
    return {
        "event_id": "SE-20260829-180000-torch-delivery-positive-test",
        "effective_at": policy["structured_handoff_effective_at"],
        "event_type": "execution-milestone",
        "representations": {
            "naya": {
                "id": "SN-20260829-180000-torch-naya",
                "lessons": ["Naya owns continuation; the human does not author the next prompt."],
                "next_best_actions": ["Run the next governance verification."],
            },
            "shawn": {
                "id": "SN-20260829-180000-torch-human",
                "lessons": ["The human receives and uses the Naya-authored continuation."],
                "next_best_actions": ["Use the provided Naya continuation."],
            },
        },
        "verification": {"status": "VERIFIED", "receipt": "RCPT-torch-delivery-test"},
        "receipt": {"receipt_id": "RCPT-torch-delivery-test"},
        "delivery": {"state": "VERIFIED"},
        "next_execution": ".naya/handoffs/NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md",
        "continuity": {
            "handoff_url": "https://example.invalid/torch-handoff",
            "learning_status": "LEARNED",
            "execution_state": "COMPLETED",
            "handoff": {
                "mission": "Test Naya-owned torch delivery",
                "source_of_truth": "SoulSchoolAcademy/NayaPOWER",
                "current_state": "Testing the structured handoff boundary",
                "protected_baseline": "Continuity law and UNKNOWN semantics",
                "work_completed": "Created positive and negative torch fixtures",
                "evidence": "Runtime acceptance test",
                "decisions": "Human continuation remains Naya-authored",
                "lessons": "Torch has both successor and human delivery targets",
                "unknowns": "None for this fixture",
                "risks": "False completion if human continuation is omitted",
                "recommendation": "Require Naya-authored human continuation",
                "next_action": "Run the governance gate",
                "ready_to_run_execution": "Execute the governance verification command.",
                "human_continuation": "Run the governance verification command, then inspect the exact tested SHA and preserve UNKNOWN for any unavailable evidence.",
                "human_continuation_naya_authored": True,
            },
        },
    }


def main() -> int:
    policy = ce.load_policy()
    required = {"human_continuation", "human_continuation_naya_authored"}
    configured = set(policy.get("structured_handoff_fields", []))
    if not required.issubset(configured):
        fail("policy does not require both human continuation fields")
    if policy.get("contract", {}).get("naya_owned_human_continuation") is not True:
        fail("policy does not enable Naya-owned human continuation")
    if policy.get("contract", {}).get("human_prompt_authoring_required") is not False:
        fail("policy incorrectly requires human prompt authoring")

    good = fixture()
    good_errors = ce.check_event(good, Path("positive-torch-fixture.json"), policy)
    if good_errors:
        fail("positive Naya-owned torch fixture rejected: " + "; ".join(good_errors))
    print("GREEN PROOF: successor handoff + Naya-authored human continuation satisfies the structured continuity contract.")

    bad = json.loads(json.dumps(good))
    del bad["continuity"]["handoff"]["human_continuation"]
    del bad["continuity"]["handoff"]["human_continuation_naya_authored"]
    bad_errors = ce.check_event(bad, Path("negative-torch-fixture.json"), policy)
    if not any("structured Future-Naya handoff missing required fields" in error and "human_continuation" in error for error in bad_errors):
        fail("negative fixture did not make missing human-facing continuation RED")
    print("RED PROOF: removing the Naya-authored human continuation fails the structured continuity contract.")

    wrong_author = json.loads(json.dumps(good))
    wrong_author["continuity"]["handoff"]["human_continuation_naya_authored"] = False
    wrong_author_errors = ce.check_event(wrong_author, Path("wrong-author-torch-fixture.json"), policy)
    if not any("structured Future-Naya handoff missing required fields" in error and "human_continuation_naya_authored" in error for error in wrong_author_errors):
        fail("wrong-author fixture did not reject non-Naya-authored continuation")
    print("RED PROOF: marking the human continuation as not Naya-authored fails the contract.")

    print("PASS: Naya-owned human-facing torch delivery is policy-configured and machine-enforced at the structured handoff boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
