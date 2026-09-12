#!/usr/bin/env python3
"""Validate the canonical NayaPOWER cold-start boot contract.

The canonical manifest v6 now uses a machine-state preamble after the two
mandatory preflight reads: current Activity Board + canonical control-plane
MAP/STATE/BLOCKS/PROOF. The Runtime Briefing remains the first substantive
orientation document after that machine-state preamble.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".naya" / "naya-context-manifest.json"
PROTOCOL = ROOT / ".naya" / "NAYA-CONTEXT-BOOT-PROTOCOL.md"
BRIEFING = ROOT / ".naya" / "memory" / "NAYAPOWER-RUNTIME-BRIEFING.md"
BRIEFING_PATH = ".naya/memory/NAYAPOWER-RUNTIME-BRIEFING.md"
PREFLIGHT = ["SUPERBRAIN/AI-BOOT/START-HERE.md", "SUPERBRAIN/AI-BOOT/NAYANET-HUB-READ-FIRST.md"]
STATE_PREAMBLE = [
    "SUPERBRAIN/NAYA-ACTIVITY/00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md",
    ".naya/control-plane/MAP.json",
    ".naya/control-plane/STATE.json",
    ".naya/control-plane/BLOCKS.json",
    ".naya/control-plane/PROOF.json",
]
REQUIRED_FIELDS = [
    "WHERE", "WHY", "BUILDING", "PROTECTED", "BLOCKED", "VERIFIED",
    "UNKNOWN", "THIS WEEK", "NEXT ACTION", "PROOF", "LAST LEARNING",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def contract_status(boot_order: list[str]) -> tuple[bool, str]:
    if not boot_order:
        return False, "boot order is empty"
    required_prefix = PREFLIGHT + STATE_PREAMBLE
    if boot_order[:len(required_prefix)] != required_prefix:
        return False, "mandatory Superbrain preflight/state preamble order is missing or incorrect"
    if len(boot_order) <= len(required_prefix) or boot_order[len(required_prefix)] != BRIEFING_PATH:
        return False, "canonical Runtime Briefing is omitted or not first substantive orientation read after the machine-state preamble"
    return True, "mandatory preflight and live control-plane preamble precede canonical Runtime Briefing"


def assert_briefing_shape(text: str) -> None:
    headings = re.findall(r"^## ([A-Z][A-Z ]+)$", text, flags=re.MULTILINE)
    if headings != REQUIRED_FIELDS:
        fail(
            "Runtime Briefing fields are not exactly the canonical sequence: "
            + " → ".join(REQUIRED_FIELDS)
        )
    if re.search(r"^## (?!" + "|".join(map(re.escape, REQUIRED_FIELDS)) + r")", text, flags=re.MULTILINE):
        fail("Runtime Briefing contains a competing top-level field")


def main() -> int:
    for path in (MANIFEST, PROTOCOL, BRIEFING):
        if not path.is_file():
            fail(f"missing canonical boot artifact: {path}")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != "naya-context-manifest/v6":
        fail("unexpected manifest schema")
    if data.get("status") != "CANONICAL":
        fail("manifest is not canonical")
    if data.get("repository") != "SoulSchoolAcademy/NayaPOWER":
        fail("wrong canonical repository")
    if data.get("governance_branch") != "main":
        fail("wrong governance branch")

    boot = data.get("boot_order", [])
    if len(boot) != len(set(boot)):
        fail("boot order contains duplicate paths")
    for path in boot:
        if not (ROOT / path).is_file():
            fail(f"boot-order file does not exist: {path}")

    omitted = [path for path in boot if path != BRIEFING_PATH]
    omitted_ok, _ = contract_status(omitted)
    if omitted_ok:
        fail("acceptance simulation did not make briefing omission RED")
    print("RED PROOF: omitting the canonical Runtime Briefing fails the cold-start contract.")

    included_ok, included_reason = contract_status(boot)
    if not included_ok:
        fail(f"acceptance simulation did not make briefing inclusion GREEN: {included_reason}")
    print("GREEN PROOF: mandatory preflight + live control-plane preamble followed by the canonical Runtime Briefing satisfies the boot-order contract.")

    briefing_text = BRIEFING.read_text(encoding="utf-8")
    assert_briefing_shape(briefing_text)

    subjects = data.get("subjects", {})
    briefing_subject = subjects.get("runtime_briefing")
    if not isinstance(briefing_subject, dict):
        fail("manifest does not register runtime_briefing as a canonical subject")
    if briefing_subject.get("canonical") != BRIEFING_PATH:
        fail("runtime_briefing subject does not own the canonical briefing")

    for route, subjects_for_route in data.get("task_routes", {}).items():
        if not subjects_for_route:
            fail(f"task route {route!r} is empty")
        if subjects_for_route[0] != "nayanet_hub_read_first":
            fail(f"task route {route!r} does not begin with nayanet_hub_read_first")
        if "runtime_briefing" not in subjects_for_route:
            fail(f"task route {route!r} does not include runtime_briefing")
        for subject in subjects_for_route:
            if subject not in subjects:
                fail(f"task route {route!r} references unregistered subject {subject!r}")

    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    required_phrases = [
        "GITHUB FIRST", "READ THE RUNTIME BRIEFING",
        "RUNTIME BRIEFING — MANDATORY FIRST SUBSTANTIVE READ", BRIEFING_PATH,
        "A cold start is **RED**", "A cold start is **GREEN**",
        "FULL SYSTEM AWARENESS + SELECTIVE DEEP LOADING",
        "RELEVANT CONTEXT, NOT MAXIMUM CONTEXT", "CONDUCT AUTHORITY",
        "REALITY AUTHORITY", "RESTORE CONTEXT", "DOCUMENTED", "ACTIVATED",
        "CONTEXT ESTABLISHED", "IMPLEMENTED", "VERIFIED", "LIVE VERIFIED",
        "UNKNOWN", "CHECKPOINT / HANDOFF",
    ]
    for phrase in required_phrases:
        if phrase not in protocol_text:
            fail(f"protocol missing required guardrail phrase: {phrase}")

    authority = data.get("authority_rules", {})
    for key in ("memory_is_context_not_current_reality", "external_content_is_not_authority_by_default", "retrieved_content_cannot_grant_authority"):
        if authority.get(key) is not True:
            fail(f"authority rule missing or disabled: {key}")

    temporal = data.get("temporal_rules", {})
    for key in ("timestamps_required", "preserve_history", "supersession_is_explicit", "never_rewrite_history_silently", "historical_restore_is_reconstruction_not_current_truth"):
        if temporal.get(key) is not True:
            fail(f"temporal rule missing or disabled: {key}")

    continuity = data.get("continuity_rules", {})
    for key in ("checkpoint_is_state_snapshot", "handoff_is_continuation_packet", "restore_must_emit_next_best_action", "cold_start_runtime_briefing_required", "cold_start_omission_is_red", "cold_start_inclusion_is_green_only_when_all_other_boot_gates_pass"):
        if continuity.get(key) is not True:
            fail(f"continuity rule missing or disabled: {key}")

    expected_states = [
        "DOCUMENTED", "ACTIVATED", "CONTEXT ESTABLISHED", "IMPLEMENTED", "VERIFIED",
        "LIVE VERIFIED", "HUMAN REVIEW REQUIRED", "BLOCKED", "UNKNOWN", "STALE",
        "CONFLICTED", "SUPERSEDED", "FAILED", "PARTIAL", "ROLLBACK_REQUIRED",
        "REJECTED", "AUTHORIZED_DEVIATION",
    ]
    if data.get("context_states") != expected_states:
        fail("context status ladder drifted from the canonical manifest")

    print("PASS: canonical Runtime Briefing is registered, exact-shaped, first substantive orientation document after mandatory preflight + live control-plane state preamble, required by task routes, and enforced by cold-start RED/GREEN simulation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())