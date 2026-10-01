"""Coda 1: default-Kernel() composition reproduction for VERIFY -> LEARN.

Frozen review target: 710776700c48069bf91a06d1adb4900cb61154c7

This documents a COMPOSITION GAP, not a security defect. The fail-closed default
in LearnNode.ingest_verify_receipt is working exactly as specified: with no
resolver and no fixture privilege it refuses with VERIFY_ORIGIN_UNESTABLISHED,
and positive learning stays blocked until an authentic VERIFY evidence path is
wired.

Two independent facts establish the gap:

  1. Plain Kernel() constructs all nine nodes but leaves
     LEARN._verify_resolver = None and _allow_fixture_intake = False, so NO
     VERIFY evidence -- genuine or forged -- can enter LEARN.

  2. VerifyNode currently exposes NO resolver-style accessor
     (`reference_resolver` / any member matching resolver|reference is absent),
     and Kernel's source does not wire `verify_resolver`. So the trusted
     lookup Naya 4's repair depends on does not exist yet on VERIFY.

Expected after the composition fix: a GENUINE receipt created through VERIFY's
public lifecycle resolves from the VERIFY-owned store and is consumed by LEARN,
with no fixture privilege and no caller-supplied resolver.

Owner: Naya 4 (runtime implementation). This file is reviewer evidence only.
No node, kernel, or Naya 4 file is modified.
"""

from __future__ import annotations

import inspect

import pytest

from naya_kernel.kernel import Kernel

REVIEW_TARGET = "710776700c48069bf91a06d1adb4900cb61154c7"

# A VERIFY-shaped object. It is NOT trusted anywhere in this suite; it is used
# only to observe which refusal code the default path produces.
VERIFY_SHAPED = {
    "id": "vr-composition-probe",
    "node_id": "NAYA-KERNEL-VERIFY",
    "verify_key": "vk1",
    "verification_state": "VERIFIED_PASS",
    "outcome_status": "PROVEN",
    "acceptance_decision": "ACCEPTED",
    "causal_status": "CLAIMED",
    "subject_ref": {"id": "s1"},
    "supersedes": None,
    "reopened_by": None,
    "evidence_refs": ["e1"],
    "receipt_hash": "probe",
}


# ==========================================================================
# FACT 1 -- plain Kernel() wires no resolver into LEARN
# ==========================================================================
def test_plain_kernel_builds_all_nine_nodes():
    nodes = Kernel().nodes
    for organ in ("SELF", "LAW", "ACT", "KNOW", "PROVE",
                  "CONNECT", "VERIFY", "LEARN", "EVOLVE"):
        assert organ in nodes, f"plain Kernel() is missing {organ}"
    assert len(nodes) == 9


def test_plain_kernel_learn_has_no_resolver_and_no_fixture_privilege():
    learn = Kernel().nodes["LEARN"]
    assert learn._verify_resolver is None, (
        "LEARN now has a resolver in ordinary Kernel construction; the "
        "composition gap has changed and this reproduction must be requalified"
    )
    assert learn._allow_fixture_intake is False


def test_default_kernel_learn_refuses_all_verify_evidence():
    """The observable consequence: no VERIFY evidence can enter LEARN."""
    learn = Kernel().nodes["LEARN"]
    out = learn.ingest_verify_receipt(dict(VERIFY_SHAPED))
    assert out["accepted"] is False
    assert out["reason_code"] == "VERIFY_ORIGIN_UNESTABLISHED", out


# ==========================================================================
# FACT 2 -- VERIFY exposes no resolver-style accessor yet
# ==========================================================================
def test_verify_exposes_no_resolver_accessor_yet():
    members = [m for m in dir(Kernel().nodes["VERIFY"])
               if "resolver" in m or "reference" in m]
    assert members == [], (
        f"VerifyNode now exposes {members}; the missing trusted lookup may have "
        "been added -- requalify the composition finding before reporting it"
    )


def test_kernel_source_does_not_wire_verify_resolver():
    assert "verify_resolver" not in inspect.getsource(Kernel), (
        "Kernel now wires verify_resolver; requalify the composition finding"
    )


# ==========================================================================
# FAIL-CLOSED IS CORRECT -- assert the safe property, not the gap
# ==========================================================================
def test_default_path_is_fail_closed_not_permissive():
    """Whatever the wiring, the default must refuse rather than admit."""
    learn = Kernel().nodes["LEARN"]
    out = learn.ingest_verify_receipt(dict(VERIFY_SHAPED))
    assert out.get("accepted") is not True
    assert "reason_code" in out


def test_review_target_recorded():
    assert len(REVIEW_TARGET) == 40