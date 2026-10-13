"""RED-first mechanical test suite for the t0537 refusal-point contract.

Spec: BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md (Lane 8, t912).
Gate module: tools/retrieval_authorization_gate.py (Lane 5, t942; candidate
    ACCEPTED t952 Lane 1 — sha256 pins verified before this suite was written).
Contract: tools/refusal_point_t0537.py (Lane 9, t0537). Packet:
    docs/retrieval-auth-wire-packet-t0537.md — AWAITING-SHAWN.

RED protocol: test_red_unguarded_write_lets_unauthorized_through proves the
hole the packet closes — an unauthorized entry committed through an UNGUARDED
write path is admitted. That test PASSES today (the seam is open) and is the
RED record. Every other test exercises the GUARDED path and must refuse.

Run: python3 -m pytest tools/test_refusal_predicate_t0537.py -v
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from refusal_point_t0537 import (
    RefusalError,
    refusal_predicate,
    guard_write,
    guard_disclose,
    EXIT_PERMITTED,
    EXIT_REFUSED,
    PRIVATE_CALLER,
)

# ---------------------------------------------------------------- fixtures

UNAUTHORIZED_PUBLIC = {
    "id": "SN-TEST-UNAUTH-PUB",
    "lifecycle_state": "ACTIVE",
    "retrieval_authorized": False,
    "publication_scope": "PUBLIC",
    "title": "unguarded entry must never surface",
}

AUTHORIZED_PUBLIC = {
    "id": "SN-TEST-AUTH-PUB",
    "lifecycle_state": "ACTIVE",
    "retrieval_authorized": True,
    "publication_scope": "PUBLIC",
    "title": "authorized public entry",
}

AUTHORIZED_PRIVATE = {
    "id": "SN-TEST-AUTH-PRIV",
    "lifecycle_state": "ACTIVE",
    "retrieval_authorized": True,
    "publication_scope": "PRIVATE",
    "title": "authorized private entry",
}


def committed_store():
    """A fake write sink: records every commit it receives."""
    store = []

    def commit():
        store.append(True)
        return "committed"

    return store, commit


# ------------------------------------------------------- RED record (open seam)

def test_red_unguarded_write_lets_unauthorized_through():
    """RED RECORD: the live seam has no refusal point.

    An unauthorized entry committed through an UNGUARDED write path is
    admitted — this is the hole the t0537 packet's guard closes. The test
    passes today BECAUSE the seam is open; guard_write exists precisely so
    this shape of write cannot happen once the wiring installs it.
    """
    store, commit = committed_store()
    # No guard consulted: the raw commit path.
    commit()
    assert store == [True], "RED: unguarded commit admitted the write"


# ------------------------------------------------- refusal predicate: GREEN

def test_unauthorized_write_is_refused():
    store, commit = committed_store()
    with pytest.raises(RefusalError) as excinfo:
        guard_write(commit, UNAUTHORIZED_PUBLIC)
    assert store == [], "refused write must never invoke the commit"
    assert excinfo.value.code == "EXCLUDED:retrieval-authorized-false"


@pytest.mark.parametrize("tampered", ["yes", 1, "true", None])
def test_tampered_flag_write_is_refused(tampered):
    """B7: only exact boolean True authorizes. Tampered/missing flags are
    UNKNOWN -> fail closed, never treated as authorization."""
    store, commit = committed_store()
    entry = dict(AUTHORIZED_PUBLIC)
    entry["retrieval_authorized"] = tampered
    with pytest.raises(RefusalError) as excinfo:
        guard_write(commit, entry)
    assert store == []
    assert excinfo.value.code == "FAIL_CLOSED:unknown-authorization-state"


def test_missing_authorization_field_write_is_refused():
    """Today's corpus has no retrieval_authorized writer: wiring fail-closed
    means EVERYTHING is excluded until the stamping migration runs. This test
    is the mechanical proof that the migration (packet M3) is REQUIRED before
    wiring, not optional."""
    store, commit = committed_store()
    entry = {k: v for k, v in AUTHORIZED_PUBLIC.items()
             if k != "retrieval_authorized"}
    with pytest.raises(RefusalError) as excinfo:
        guard_write(commit, entry)
    assert store == []
    assert excinfo.value.code == "FAIL_CLOSED:unknown-authorization-state"


def test_self_declared_private_surface_without_identity_is_refused():
    """B2: a self-declared private-surface claim without identity is a claim,
    not proof — the refusal point must not honor it."""
    store, commit = committed_store()
    with pytest.raises(RefusalError):
        guard_write(commit, AUTHORIZED_PRIVATE,
                    caller={"surface": "private_authenticated"})
    assert store == []


def test_stale_superseded_copy_is_refused():
    """Registry is the source of truth: a stale cached copy claiming ACTIVE
    cannot resurrect a superseded note."""
    registry = {
        "SN-HEAD": {"id": "SN-HEAD", "lifecycle_state": "ACTIVE",
                    "retrieval_authorized": True, "publication_scope": "PUBLIC"},
    }
    stale = {"id": "SN-STALE", "lifecycle_state": "ACTIVE",
             "retrieval_authorized": True, "publication_scope": "PUBLIC",
             "superseded_by": "SN-HEAD"}
    store, commit = committed_store()
    with pytest.raises(RefusalError) as excinfo:
        guard_write(commit, stale, registry_index=registry)
    assert store == []
    assert excinfo.value.code == "EXCLUDED:superseded-chain"


def test_revoked_lifecycle_write_is_refused():
    store, commit = committed_store()
    entry = dict(AUTHORIZED_PUBLIC)
    entry["lifecycle_state"] = "REVOKED"
    with pytest.raises(RefusalError) as excinfo:
        guard_write(commit, entry)
    assert store == []
    assert "lifecycle-revoked" in excinfo.value.code


def test_malformed_entry_fails_closed_never_raises_other():
    store, commit = committed_store()
    for bad in (None, "not-a-dict", 42, ["x"]):
        with pytest.raises(RefusalError) as excinfo:
            guard_write(commit, bad)
        assert excinfo.value.code.startswith("FAIL_CLOSED:")
    assert store == []


def test_refusal_codes_leak_no_content():
    """Spec 4.3: refusal codes are silent-exclusion codes — they name a code,
    never note content, titles, keywords, or ids."""
    secret = "the-secret-lesson-about-orchid-wasps"
    entry = dict(UNAUTHORIZED_PUBLIC)
    entry["title"] = secret
    entry["keywords"] = [secret]
    entry["id"] = secret
    with pytest.raises(RefusalError) as excinfo:
        guard_write(committed_store()[1], entry)
    assert secret not in excinfo.value.code
    assert secret not in str(excinfo.value)


# ------------------------------------------------- positive controls

def test_authorized_public_write_is_permitted():
    store, commit = committed_store()
    result = guard_write(commit, AUTHORIZED_PUBLIC)
    assert store == [True], "permitted write must invoke the commit once"
    assert result == "committed"


def test_authorized_private_write_with_authenticated_surface_is_permitted():
    store, commit = committed_store()
    result = guard_write(commit, AUTHORIZED_PRIVATE, caller=PRIVATE_CALLER)
    assert store == [True]
    assert result == "committed"


def test_disclose_guard_refuses_unauthorized_read():
    """H1: the read-side guard (retrieve() hook shape). The content fetch is
    never invoked on refusal — no bytes are touched."""
    reads = []

    def read():
        reads.append(True)
        return "FULL NOTE CONTENT"

    with pytest.raises(RefusalError):
        guard_disclose(read, UNAUTHORIZED_PUBLIC)
    assert reads == [], "refused read must never invoke the content fetch"


def test_disclose_guard_permits_authorized_read():
    reads = []

    def read():
        reads.append(True)
        return "content"

    assert guard_disclose(read, AUTHORIZED_PUBLIC) == "content"
    assert reads == [True]


# ------------------------------------------------- exit protocol

def _run_harness(packet):
    pkt_path = TOOLS / "_t0537_harness_packet.json"
    pkt_path.write_text(json.dumps(packet), encoding="utf-8")
    try:
        proc = subprocess.run(
            [sys.executable, str(TOOLS / "refusal_point_t0537.py"),
             str(pkt_path)],
            capture_output=True, text=True, timeout=30)
    finally:
        pkt_path.unlink(missing_ok=True)
    return proc


def test_exit_protocol_refusal_blocks_the_close():
    """The exit protocol: refusal exits 2 (non-zero) — the disposition
    cannot close over a refused write. Permit exits 0."""
    refused = _run_harness({"entry": UNAUTHORIZED_PUBLIC, "action": "write"})
    assert refused.returncode == EXIT_REFUSED == 2
    assert "REFUSED" in refused.stdout

    permitted = _run_harness({"entry": AUTHORIZED_PUBLIC, "action": "write"})
    assert permitted.returncode == EXIT_PERMITTED == 0
    assert "PERMITTED" in permitted.stdout


def test_exit_protocol_malformed_packet_exits_3():
    proc = _run_harness({"no_entry_here": True})
    assert proc.returncode == 3
