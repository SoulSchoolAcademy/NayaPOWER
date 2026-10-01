#!/usr/bin/env python3
"""Tests for the runtime nine-node kernel boot.

Design rule: every test runs against the REAL canonical manifest, or a mutated
copy of it. There are no synthetic nine-node fixtures, because synthetic
fixtures are how the previous version of this module managed to pass checks for
fields the canonical schema does not contain.

Two tests are architectural guards rather than behaviour tests:
  * the module must not restate the ratified node constants, and
  * the module must not hardcode a second copy of the kernel.
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / ".naya/runtime"))

import kernel_boot as kb  # noqa: E402

MANIFEST = REPO / kb.MANIFEST_REL
TODAY = date(2026, 9, 26)
ENVELOPE = {"next_action": "Ratify one constitutional law and merge the authority gate."}


def real_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def boot(manifest: dict | None = None, envelope: dict | None = None,
         today: date = TODAY):
    src = (lambda: manifest) if manifest is not None else kb.manifest_source
    return kb.boot_kernel(src, envelope=envelope, today=today)


# --- the real thing ---------------------------------------------------------

def test_real_manifest_boots_all_nine_nodes():
    report = boot(envelope=ENVELOPE)
    assert len(report.loaded) == 9, report.unresolved
    assert report.boot_permitted is True, report.unresolved
    assert report.conclusive is True


def test_real_manifest_is_the_only_specification():
    assert MANIFEST.is_file(), f"canonical manifest missing: {kb.MANIFEST_REL}"


def test_manifest_source_reads_the_canonical_file():
    m = kb.manifest_source()
    assert m["schema_id"] == "naya/master-node-kernel/v1"
    assert len(m["nodes"]) == 9


def test_authority_is_never_granted_even_on_a_healthy_boot():
    report = boot(envelope=ENVELOPE)
    assert report.boot_permitted is True
    assert report.authority == "NONE"


def test_loaded_keys_are_reported_from_the_manifest():
    report = boot(envelope=ENVELOPE)
    assert report.loaded_keys == [n["key"] for n in real_manifest()["nodes"]]


def test_safety_invariants_pass_against_real_invariants():
    report = boot(envelope=ENVELOPE)
    check = next(f for f in report.findings if f.check == "SAFETY_INVARIANTS")
    assert check.status == "PASS"


# --- architectural guards: no second copy of the spec ----------------------

def _code_string_literals() -> list[str]:
    """Every string literal in the module EXCEPT docstrings.

    Prose may legitimately mention MN-01/SELF; executable code may not, because
    that would be a second copy of the ratified specification.
    """
    import ast
    src = (REPO / ".naya/runtime/kernel_boot.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    docstring_nodes: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                docstring_nodes.add(id(body[0].value))
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in docstring_nodes]


def test_module_does_not_hardcode_the_ratified_node_constants():
    """A second copy of the spec would create a competing canonical store.

    Matched on whole tokens, not substrings: `CONTRACT_OWNERSHIP` contains
    "ACT" and `UNKNOWN` contains "KNOW", and neither is a node key.
    """
    import re
    literals = _code_string_literals()
    id_rx = re.compile(r"\bMN-\d{2}\b")
    key_rx = re.compile(
        r"\b(?:SELF|LAW|ACT|KNOW|PROVE|CONNECT|VERIFY|LEARN|EVOLVE)\b")
    offenders = [l for l in literals if id_rx.search(l) or key_rx.search(l)]
    assert not offenders, (
        "kernel_boot.py restates the ratified specification in executable code; "
        f"the manifest is the single source of truth. offenders={offenders[:5]}"
    )


def test_guard_itself_detects_a_planted_literal():
    """The guard must be able to fail, or it proves nothing."""
    import re
    key_rx = re.compile(
        r"\b(?:SELF|LAW|ACT|KNOW|PROVE|CONNECT|VERIFY|LEARN|EVOLVE)\b")
    assert key_rx.search("EVOLE" if False else "EVOLVE")
    assert key_rx.search("MN-01") is None and re.search(r"\bMN-\d{2}\b", "MN-01")
    # negative controls: these must NOT trip the guard
    for innocent in ("CONTRACT_OWNERSHIP", "UNKNOWN", "contract_id_range",
                     "MASTER-NODE-KERNEL", "IMPLEMENTED", "verified"):
        assert not key_rx.search(innocent), f"{innocent!r} must not trip the guard"


def test_module_declares_no_node_name_mapping():
    """Guards against reintroducing a semantic name table alongside the ids."""
    literals = " ".join(_code_string_literals())
    assert "Identity, Mission" not in literals
    assert "Authority, Consent" not in literals


def test_module_declares_no_master_nodes_tuple():
    source = (REPO / ".naya/runtime/kernel_boot.py").read_text(encoding="utf-8")
    assert "MASTER_NODES" not in source, "hardcoded kernel spec must not return"


def test_module_has_no_expected_kernel_version_constant():
    source = (REPO / ".naya/runtime/kernel_boot.py").read_text(encoding="utf-8")
    assert "EXPECTED_KERNEL_VERSION" not in source
    assert "EXPECTED_SEQUENCE" not in source


# --- fail-closed on an unreadable / unreachable kernel ----------------------

def test_missing_manifest_is_unknown_not_pass(tmp_path):
    report = kb.boot_kernel(lambda: kb.manifest_source(tmp_path), today=TODAY)
    assert report.conclusive is True
    assert report.boot_permitted is False
    assert report.findings[0].status == "UNKNOWN"
    assert report.loaded == []


def test_unparseable_manifest_is_unknown_not_pass():
    def bad():
        raise ValueError("Expecting ',' delimiter")

    report = kb.boot_kernel(bad, today=TODAY)
    assert report.boot_permitted is False
    assert report.findings[0].status == "UNKNOWN"


def test_non_object_manifest_fails_closed():
    report = kb.boot_kernel(lambda: [1, 2, 3], today=TODAY)
    assert report.boot_permitted is False


def test_receiver_without_credentials_is_unknown():
    report = kb.boot_kernel(kb.receiver_source, today=TODAY)
    assert report.boot_permitted is False
    assert report.findings[0].status == "UNKNOWN"
    assert "credentials absent" in report.findings[0].detail


# --- successor envelope (SS37 / SS38) --------------------------------------

def test_missing_envelope_is_unknown_and_blocks():
    report = boot(envelope=None)
    assert report.boot_permitted is False
    env = next(f for f in report.findings if f.check == "SUCCESSOR_ENVELOPE")
    assert env.status == "UNKNOWN"


def test_envelope_without_next_action_fails_closed():
    report = boot(envelope={})
    assert report.boot_permitted is False


def test_two_next_actions_fail_closed():
    report = boot(envelope={"next_action": "Merge the gate. Then deploy the Hub."})
    assert report.boot_permitted is False
    env = next(f for f in report.findings if f.check == "SUCCESSOR_ENVELOPE")
    assert "exactly ONE" in env.detail


def test_semicolon_separated_next_actions_fail_closed():
    report = boot(envelope={"next_action": "Merge the gate; deploy the Hub"})
    assert report.boot_permitted is False


def test_trailing_period_is_not_a_second_action():
    report = boot(envelope={"next_action": "Merge the gate."})
    assert report.boot_permitted is True, report.unresolved


def test_valid_envelope_next_action_is_recorded():
    report = boot(envelope=ENVELOPE)
    assert report.next_action == ENVELOPE["next_action"]


# --- mutated copies of the REAL manifest must fail closed -------------------

def test_mutated_missing_node_fails_closed():
    m = real_manifest()
    m["nodes"] = m["nodes"][:8]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any(f.check == "NODE_SET" for f in report.failed)


def test_mutated_node_count_lie_fails_closed():
    m = real_manifest()
    m["node_count"] = 11
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any("node_count" in f.detail for f in report.failed)


def test_mutated_duplicate_node_id_fails_closed():
    m = real_manifest()
    m["nodes"][1] = copy.deepcopy(m["nodes"][0])
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any("duplicate" in f.detail for f in report.failed)


def test_mutated_node_no_gap_fails_closed():
    m = real_manifest()
    m["nodes"][2]["node_no"] = 99
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_broken_runtime_flow_fails_closed():
    m = real_manifest()
    m["runtime_flow"] = m["runtime_flow"][:-1]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any(f.check == "RUNTIME_FLOW" for f in report.failed)


def test_mutated_open_loop_fails_closed():
    """A kernel whose flow does not return to its origin is not a closed kernel."""
    m = real_manifest()
    m["runtime_flow"] = [m["runtime_flow"][0]] + m["runtime_flow"][1:-1]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_contract_coverage_gap_fails_closed():
    m = real_manifest()
    m["contract_primary_ownership"].pop("26")
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any(f.check == "CONTRACT_OWNERSHIP" for f in report.failed)


def test_mutated_contract_double_ownership_fails_closed():
    """A contract claimed as primary by two nodes must fail."""
    m = real_manifest()
    stolen = m["contract_primary_ownership"]["26"]
    m["nodes"][0]["primary_contracts"] = list(m["nodes"][0]["primary_contracts"]) + ["26"]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any("both" in f.detail for f in report.failed)
    assert stolen in " ".join(f.detail for f in report.failed)


def test_mutated_node_claim_disagrees_with_ownership_map_fails_closed():
    m = real_manifest()
    m["nodes"][0]["primary_contracts"] = ["00"]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any(f.check == "CONTRACT_OWNERSHIP" for f in report.failed)


def test_mutated_triad_overlap_fails_closed():
    m = real_manifest()
    m["triads"][1]["nodes"][0] = m["triads"][0]["nodes"][0]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any(f.check == "TRIADS" for f in report.failed)


def test_mutated_triad_partition_incomplete_fails_closed():
    m = real_manifest()
    m["triads"] = m["triads"][:2]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_removed_safety_invariant_fails_closed():
    """A kernel that permits self-authorization must never boot."""
    m = real_manifest()
    m["global_invariants"]["must_not"] = [
        x for x in m["global_invariants"]["must_not"] if "self-authorize" not in x.lower()
    ]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any(f.check == "SAFETY_INVARIANTS" for f in report.failed)


def test_mutated_removed_self_ratification_prohibition_fails_closed():
    m = real_manifest()
    m["global_invariants"]["must_not"] = [
        x for x in m["global_invariants"]["must_not"] if "self-ratify" not in x.lower()
    ]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_competing_store_prohibition_removed_fails_closed():
    m = real_manifest()
    m["global_invariants"]["must_not"] = [
        x for x in m["global_invariants"]["must_not"]
        if "competing canonical intelligence store" not in x.lower()
    ]
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_empty_envelopes_fail_closed():
    m = real_manifest()
    m["required_input_fields"] = []
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False
    assert any(f.check == "ENVELOPES" for f in report.failed)


def test_mutated_removed_kernel_gates_fail_closed():
    m = real_manifest()
    m["kernel_gates"] = []
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_gate_without_requirement_fails_closed():
    m = real_manifest()
    m["kernel_gates"][0].pop("required")
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_bad_kernel_version_fails_closed():
    m = real_manifest()
    m["kernel_version"] = "one point oh"
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_missing_schema_id_fails_closed():
    m = real_manifest()
    m.pop("schema_id")
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


def test_mutated_bad_effective_date_fails_closed():
    m = real_manifest()
    m["effective_date"] = "not-a-date"
    report = boot(m, envelope=ENVELOPE)
    assert report.boot_permitted is False


# --- freshness (SS17) -------------------------------------------------------

def test_real_manifest_is_fresh_today():
    report = boot(envelope=ENVELOPE)
    fresh = next(f for f in report.findings if f.check == "KERNEL_FRESHNESS")
    assert fresh.status == "PASS"


def test_stale_kernel_fails_closed():
    # Absolute past date: a test derived from MAX_AGE_DAYS cannot detect
    # tampering with MAX_AGE_DAYS itself.
    report = boot(today=date(2027, 9, 26))
    assert report.boot_permitted is False
    assert any(f.check == "KERNEL_FRESHNESS" for f in report.failed)


def test_far_future_effective_date_is_observation_not_failure():
    m = real_manifest()
    m["effective_date"] = "2030-01-01"
    report = boot(m, envelope=ENVELOPE)
    obs = next(f for f in report.findings if f.check == "KERNEL_FRESHNESS")
    assert obs.status == "OBSERVATION"
    assert not obs.blocking


# --- status vocabulary: surfaced, not invented -----------------------------

def test_status_outside_state_machine_is_observation_not_failure():
    """The ratified baseline uses a term its own state machine does not define.

    This must be surfaced (SS46) without being turned into an invented
    integrity break.
    """
    report = boot(envelope=ENVELOPE)
    obs = [f for f in report.findings if f.check == "STATUS_VOCABULARY"]
    assert len(obs) == 1
    assert obs[0].status == "OBSERVATION"
    assert not obs[0].blocking
    assert report.boot_permitted is True, "an observation must not refuse the boot"


def test_observations_do_not_appear_in_unresolved():
    report = boot(envelope=ENVELOPE)
    assert all(not u.startswith("STATUS_VOCABULARY") for u in report.unresolved)


def test_status_inside_state_machine_passes_cleanly():
    m = real_manifest()
    m["status"] = m["state_machine"]["states"][1]
    report = boot(m, envelope=ENVELOPE)
    check = next(f for f in report.findings if f.check == "STATUS_VOCABULARY")
    assert check.status == "PASS"


# --- gating behaviour -------------------------------------------------------

def test_assert_bootable_raises_when_unproven():
    report = boot(envelope=None)
    with pytest.raises(kb.KernelBootError):
        kb.assert_bootable(report)


def test_assert_bootable_passes_on_real_manifest():
    kb.assert_bootable(boot(envelope=ENVELOPE))


def test_report_serializes_for_receipt():
    blob = json.dumps(boot(envelope=ENVELOPE).to_dict(), sort_keys=True)
    parsed = json.loads(blob)
    assert parsed["schema"] == "naya.kernel-boot-report/2"
    assert parsed["boot_permitted"] is True
    assert parsed["authority"] == "NONE"
    assert parsed["manifest"] == kb.MANIFEST_REL
    assert len(parsed["loaded"]) == 9
