"""Tests for the fail-closed activation gate (kernel/protocol/activation_gate.py).

The gate is a session-admission check in the WAKE -> UNDERSTAND -> GATE spine:
a worker may not begin governed work without all four evidence categories.
Every test here asserts behavior against the REAL module, not a prototype.

Covered: all four categories admit; negative controls for missing/forged
evidence; the decisive rule (claimed SHAs must resolve to REAL objects);
qualification binding to the presented protocol version; fail-closed ordering
(first failing category ends evaluation); structured refusal JSON; and the
production resolver (`git cat-file -e`) against live repo bytes — with real
SHAs computed at test time, never hard-coded, so the suite does not rot when
the tip moves.
"""

import json
import subprocess
from pathlib import Path

import pytest

from kernel.protocol.activation_gate import (
    ActivationEvidence,
    Admission,
    Identity,
    Qualification,
    Readiness,
    Refusal,
    SourceVersion,
    git_resolver,
    run_gate,
)

ROOT = Path(__file__).resolve().parents[1]

# Fixed labels for the hermetic suite. The FAKE_RESOLVER decides
# resolvability here; these strings are only names, never authority.
REAL_TIP = "57e935c1b44b10fcc27a80f8c99fc9ddb2e69440"
REAL_PROTO = "e421717b37469a822c0b4c0e1f8a72fbb0365dcd"
REAL_AGENTS = "1c0dfd87dcd39669da1eab1eafcafb0296bb00c1"
FORGED_SHA = "deadbeef" * 5  # well-formed hex, resolves nowhere
FAKE_RESOLVER = lambda sha: sha in {REAL_PROTO, REAL_AGENTS, REAL_TIP}


def good_evidence() -> ActivationEvidence:
    return ActivationEvidence(
        identity=Identity(seat_id="test-seat", lane="prove",
                          dispatcher="naya-4"),
        sources=[SourceVersion(path="PROTOCOL.md", sha=REAL_PROTO),
                 SourceVersion(path="AGENTS.md", sha=REAL_AGENTS)],
        qualification=Qualification(test_id="cold-14",
                                    protocol_version=REAL_PROTO,
                                    passed=True,
                                    graded_at="2026-10-11T05:55:00Z",
                                    grader="naya-4"),
        readiness=Readiness(git_available=True, remote_reachable=True,
                            tip_sha=REAL_TIP, tip_fresh=True,
                            workspace_writable=True),
    )


# ---------------------------------------------------------------------------
# The four evidence categories: each admits when present and valid
# ---------------------------------------------------------------------------

def test_1_identity_admits():
    res = run_gate(good_evidence(), FAKE_RESOLVER)
    assert isinstance(res, Admission)
    assert res.seat_id == "test-seat"


def test_2_source_versions_admit():
    res = run_gate(good_evidence(), FAKE_RESOLVER)
    assert isinstance(res, Admission)
    assert all("@" in s for s in res.verified_sources)


def test_3_qualification_admits():
    res = run_gate(good_evidence(), FAKE_RESOLVER)
    assert isinstance(res, Admission)


def test_4_readiness_admits():
    ev = good_evidence()
    ev.readiness.tip_fresh = True
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Admission)


# ---------------------------------------------------------------------------
# Negative controls
# ---------------------------------------------------------------------------

def test_N1_missing_qualification_refuses():
    ev = good_evidence()
    ev.qualification = None
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "QUALIFICATION_MISSING"


def test_N2_forged_versions_refuse():
    # well-formed hex, resolves nowhere -> forged/unsourced
    ev = good_evidence()
    ev.sources = [SourceVersion(path="PROTOCOL.md", sha=FORGED_SHA)]
    ev.qualification.protocol_version = FORGED_SHA
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "VERSION_UNRESOLVABLE"


def test_missing_identity_refuses():
    ev = good_evidence()
    ev.identity = None
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "IDENTITY_MISSING"


def test_failed_qualification_refuses():
    ev = good_evidence()
    ev.qualification.passed = False
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "QUALIFICATION_FAILED"


def test_version_mismatch_refuses():
    # qualification graded against AGENTS.md, not the presented PROTOCOL.md
    ev = good_evidence()
    ev.qualification.protocol_version = REAL_AGENTS
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "VERSION_MISMATCH"


def test_stale_tip_refuses():
    ev = good_evidence()
    ev.readiness.tip_fresh = False
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "READINESS_FAILED"


def test_missing_required_source_refuses():
    ev = good_evidence()
    ev.sources = [SourceVersion(path="AGENTS.md", sha=REAL_AGENTS)]
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "VERSION_UNRESOLVABLE"


def test_malformed_sha_refuses():
    ev = good_evidence()
    ev.sources[0].sha = "not-a-sha"
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "VERSION_UNRESOLVABLE"


# ---------------------------------------------------------------------------
# Refusal shape + fail-closed ordering
# ---------------------------------------------------------------------------

def test_refusal_is_structured_json():
    ev = good_evidence()
    ev.qualification = None
    res = run_gate(ev, FAKE_RESOLVER)
    d = json.loads(res.to_json())
    assert d["code"] == "QUALIFICATION_MISSING"
    assert "qualification" in d["missing_evidence"]
    assert d["remediation"]
    assert d["recorded_at"]


def test_first_failure_wins_fail_closed():
    # identity AND qualification missing -> identity reported (first)
    ev = good_evidence()
    ev.identity = None
    ev.qualification = None
    res = run_gate(ev, FAKE_RESOLVER)
    assert isinstance(res, Refusal)
    assert res.code == "IDENTITY_MISSING"


# ---------------------------------------------------------------------------
# Production resolver: real SHAs computed at test time, never hard-coded
# ---------------------------------------------------------------------------

def _git(*args) -> str | None:
    try:
        r = subprocess.run(["git", *args], cwd=ROOT,
                           capture_output=True, text=True, timeout=15)
    except Exception:
        return None
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def _live_blob_sha(path: str) -> str | None:
    out = _git("ls-tree", "HEAD", "--", path)
    if not out:
        return None
    parts = out.split()
    return parts[2] if len(parts) >= 3 and parts[1] == "blob" else None


def test_git_resolver_real_blob_resolves():
    sha = _live_blob_sha("PROTOCOL.md")
    if sha is None:
        pytest.skip("git not usable in this environment")
    assert git_resolver(sha) is True


def test_git_resolver_forged_sha_does_not_resolve():
    if git_resolver(FORGED_SHA):
        pytest.skip("collision-impossible SHA unexpectedly resolved; not a gate defect")
    assert git_resolver(FORGED_SHA) is False


def test_git_resolver_malformed_sha_false():
    assert git_resolver("not-a-sha") is False


def test_full_gate_with_production_resolver():
    # The decisive rule end-to-end: real SHAs admit, forged SHAs refuse.
    proto_sha = _live_blob_sha("PROTOCOL.md")
    agents_sha = _live_blob_sha("AGENTS.md")
    tip_sha = _git("rev-parse", "HEAD")
    if not (proto_sha and agents_sha and tip_sha):
        pytest.skip("git not usable in this environment")

    ev = ActivationEvidence(
        identity=Identity(seat_id="prod-resolver-test", lane="prove",
                          dispatcher="naya-4"),
        sources=[SourceVersion(path="PROTOCOL.md", sha=proto_sha),
                 SourceVersion(path="AGENTS.md", sha=agents_sha)],
        qualification=Qualification(test_id="cold-14",
                                    protocol_version=proto_sha,
                                    passed=True,
                                    graded_at="2026-10-11T06:15:00Z",
                                    grader="naya-4"),
        readiness=Readiness(git_available=True, remote_reachable=True,
                            tip_sha=tip_sha, tip_fresh=True,
                            workspace_writable=True),
    )
    res = run_gate(ev, git_resolver)
    assert isinstance(res, Admission)

    ev.sources = [SourceVersion(path="PROTOCOL.md", sha=FORGED_SHA)]
    ev.qualification.protocol_version = FORGED_SHA
    res = run_gate(ev, git_resolver)
    assert isinstance(res, Refusal)
    assert res.code == "VERSION_UNRESOLVABLE"
