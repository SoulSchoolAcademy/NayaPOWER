"""Acceptance gates must be platform-deterministic without becoming weaker.

A gate that reports FAIL on a correct checkout is not protecting anything; it
trains the team to ignore it. A gate that reports PASS on a correct checkout is
only useful if it still reports FAIL on real drift.

Both halves are asserted here, because a fix that achieves determinism by
accepting anything would pass the first half alone.

History: on a Windows checkout these gates reported
  tools/spec_integrity_check.py          -> 11 integrity failure(s), exit 1
  tools/successor-reuse-trial-replay    -> ARCHIVE ERROR, exit 2
while the ratified content was provably intact:
  - 5 of 6 Director-ratified projections matched their manifest pins exactly
    once line endings were normalized;
  - 1 pin was legitimately recorded over a CRLF-in-blob artifact;
  - all 4 replay fixture pins were recorded over LF bytes.
Root causes were (a) hashing raw disk bytes, (b) comparing OS-native path
separators against POSIX manifest paths.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

SPEC_TOOL = ROOT / "tools" / "spec_integrity_check.py"
REPLAY_TOOL = ROOT / "tools" / "successor-reuse-trial-replay" / "replay-trial.mjs"
REPLAY_FIXTURE = (
    ROOT
    / "tools"
    / "successor-reuse-trial-replay"
    / "selftest"
    / "fixtures"
    / "sr-selftest"
    / "archive"
)

# A DIRECTOR-RATIFIED projection. Never mutate this outside a temp restore.
RATIFIED_SPEC = ROOT / "BRAIN" / "01-GOVERNANCE" / "0004-nonstop-loop-v1.machine.json"
REPLAY_FILE = REPLAY_FIXTURE / "arm-b" / "sum.mjs"


def _run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout + p.stderr


def _spec_gate() -> tuple[int, str]:
    return _run([sys.executable, str(SPEC_TOOL)])


def _replay_gate() -> tuple[int, str]:
    return _run(["node", str(REPLAY_TOOL), str(REPLAY_FIXTURE)])


def _to_crlf(data: bytes) -> bytes:
    """The opposite line-ending convention, built from normalized bytes."""
    return data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")


@pytest.fixture
def restore():
    """Guarantee both touched files come back byte-identical."""
    backups = {p: p.read_bytes() for p in (RATIFIED_SPEC, REPLAY_FILE)}
    yield
    for path, data in backups.items():
        path.write_bytes(data)
    for path, data in backups.items():
        assert path.read_bytes() == data, f"{path} was not restored byte-identically"


@pytest.mark.parametrize(
    "gate,label",
    [(_spec_gate, "spec_integrity_check"), (_replay_gate, "replay-trial")],
)
def test_gates_are_green_on_an_untouched_checkout(gate, label):
    rc, out = gate()
    assert rc == 0, f"{label} must pass on a correct checkout.\n{out}"


def test_spec_gate_still_fails_on_real_content_drift(restore):
    original = RATIFIED_SPEC.read_bytes()
    assert b'"terminal"' in original, "fixture assumption changed; pick a stable token"
    RATIFIED_SPEC.write_bytes(original.replace(b'"terminal"', b'"terminalX"', 1))

    rc, out = _spec_gate()
    assert rc != 0, "the gate accepted a real edit to a ratified projection"
    assert "drifted from ratified pin" in out, f"wrong failure reason:\n{out}"

    RATIFIED_SPEC.write_bytes(original)
    rc, out = _spec_gate()
    assert rc == 0, f"gate did not return to green after restore:\n{out}"


def test_spec_gate_does_not_treat_line_endings_as_ratified_content(restore):
    original = RATIFIED_SPEC.read_bytes()
    RATIFIED_SPEC.write_bytes(_to_crlf(original))
    rc, out = _spec_gate()
    assert rc == 0, f"line-ending representation was treated as ratified drift:\n{out}"


def test_replay_gate_still_fails_on_real_archive_drift(restore):
    original = REPLAY_FILE.read_bytes()
    REPLAY_FILE.write_bytes(original + b"\n// tampered\n")
    rc, out = _replay_gate()
    assert rc != 0, "the replay gate accepted a tampered archive fixture"
    assert "hash mismatch" in out, f"wrong failure reason:\n{out}"

    REPLAY_FILE.write_bytes(original)
    rc, out = _replay_gate()
    assert rc == 0, f"gate did not return to green after restore:\n{out}"


def test_replay_gate_does_not_treat_line_endings_as_archive_drift(restore):
    original = REPLAY_FILE.read_bytes()
    REPLAY_FILE.write_bytes(_to_crlf(original))
    rc, out = _replay_gate()
    assert rc == 0, f"line-ending representation broke archive integrity:\n{out}"


def test_ratified_specs_are_not_rewritten_by_any_check(restore):
    """The fix must not 'solve' the problem by rewriting Director-ratified bytes."""
    before = RATIFIED_SPEC.read_bytes()
    _spec_gate()
    _replay_gate()
    assert RATIFIED_SPEC.read_bytes() == before, "an acceptance check mutated a ratified artifact"
