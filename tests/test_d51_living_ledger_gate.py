"""Tests for the D51 living-ledger contract gate - incl. negative controls.

The sabotage tests are the anti-theater proof: a neutered mechanism must
make the gate go red, and a corrupt mechanism must fail closed. If any of
them passes against a sabotaged tree, the gate is theater.
"""

import os
import shutil
import subprocess
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

import d51_living_ledger_gate as gate  # noqa: E402

_MECH_FILES = ("receipt.py", "chain.py", "__init__.py")
MECH_PRESENT = all(
    os.path.isfile(os.path.join(REPO_ROOT, "living_ledger", f))
    for f in ("receipt.py", "chain.py")
)
needs_mech = pytest.mark.skipif(
    not MECH_PRESENT,
    reason="living_ledger mechanism not on this tree (pre-merge DORMANT)",
)


def _copy_mech(tmp_path):
    dest = os.path.join(str(tmp_path), "living_ledger")
    os.makedirs(dest, exist_ok=True)
    for name in _MECH_FILES:
        src = os.path.join(REPO_ROOT, "living_ledger", name)
        if os.path.isfile(src):
            shutil.copy(src, dest)
    return str(tmp_path)


def _sabotage(path, old, new):
    with open(path) as f:
        text = f.read()
    count = text.count(old)
    assert count == 1, "sabotage anchor not unique/found in %s: %r (%d hits)" % (
        path, old[:60], count)
    with open(path, "w") as f:
        f.write(text.replace(old, new, 1))


# --- loader: DORMANT and fail-closed paths (no mechanism needed) ---

def test_dormant_when_mechanism_absent(tmp_path):
    code, report = gate.run_gate(str(tmp_path))
    assert code == gate.EXIT_PASS
    assert any("DORMANT" in line for line in report)


def test_dormant_when_mechanism_partial(tmp_path):
    dest = os.path.join(str(tmp_path), "living_ledger")
    os.makedirs(dest)
    with open(os.path.join(dest, "receipt.py"), "w") as f:
        f.write("# partial tree\n")
    code, report = gate.run_gate(str(tmp_path))
    assert code == gate.EXIT_PASS
    assert any("DORMANT" in line for line in report)


def test_fail_closed_on_syntax_error(tmp_path):
    root = _copy_mech(tmp_path)
    with open(os.path.join(root, "living_ledger", "chain.py"), "a") as f:
        f.write("\ndef broken(:\n")
    code, report = gate.run_gate(root)
    assert code == gate.EXIT_FAIL_CLOSED
    assert any("FAIL-CLOSED" in line for line in report)


def test_fail_closed_on_missing_contract_surface(tmp_path):
    root = _copy_mech(tmp_path)
    with open(os.path.join(root, "living_ledger", "chain.py"), "w") as f:
        f.write('"""Neutered: imports fine, contract surface gone."""\n')
    code, report = gate.run_gate(root)
    assert code == gate.EXIT_FAIL_CLOSED
    assert any("FAIL-CLOSED" in line for line in report)


# --- contract battery on the real mechanism ---

@needs_mech
def test_contract_passes_on_real_mechanism():
    code, report = gate.run_gate(REPO_ROOT)
    assert code == gate.EXIT_PASS, "\n".join(report)
    assert any("PASS" in line for line in report)


@needs_mech
def test_gate_script_exit_zero_on_real_tree():
    proc = subprocess.run(
        [sys.executable, os.path.join(REPO_ROOT, "tools",
                                     "d51_living_ledger_gate.py")],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "D51-GATE PASS" in proc.stdout


@needs_mech
def test_gate_script_dormant_on_empty_tree(tmp_path):
    proc = subprocess.run(
        [sys.executable, os.path.join(REPO_ROOT, "tools",
                                     "d51_living_ledger_gate.py"),
         str(tmp_path)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "DORMANT" in proc.stdout


# --- negative controls: sabotage the mechanism, the gate must go red ---

@needs_mech
def test_blocks_receipt_validation_removed(tmp_path):
    """Sabotage: LivingReceipt stops refusing empty evidence -> exit 1."""
    root = _copy_mech(tmp_path)
    _sabotage(
        os.path.join(root, "living_ledger", "receipt.py"),
        'if not isinstance(ev, tuple) or not ev:\n'
        '            raise ValueError("evidence must be a non-empty tuple/list")',
        'pass  # SABOTAGED: empty evidence accepted',
    )
    code, report = gate.run_gate(root)
    assert code == gate.EXIT_VIOLATION, "\n".join(report)
    assert any("evidence" in line for line in report)


@needs_mech
def test_blocks_verifier_always_passes(tmp_path):
    """Sabotage: verify_chain redefined to always say CHAIN_VALID -> exit 1."""
    root = _copy_mech(tmp_path)
    with open(os.path.join(root, "living_ledger", "chain.py"), "a") as f:
        f.write("\n\ndef verify_chain(events):  # SABOTAGED\n"
                "    return ChainVerdict('CHAIN_VALID', detail='always')\n")
    code, report = gate.run_gate(root)
    assert code == gate.EXIT_VIOLATION, "\n".join(report)
    assert any("HASH_MISMATCH" in line or "LINK_BROKEN" in line
               for line in report)


@needs_mech
def test_blocks_hash_neutered_to_constant(tmp_path):
    """Sabotage: canonical_event_hash returns a constant -> exit 1.

    A constant hash lets a forged event_hash pass recomputation, so the
    tamper battery must catch it.
    """
    root = _copy_mech(tmp_path)
    _sabotage(
        os.path.join(root, "living_ledger", "chain.py"),
        "    return hashlib.sha256(joined.encode(\"utf-8\")).hexdigest()",
        "    return \"0\" * 64  # SABOTAGED: constant hash",
    )
    code, report = gate.run_gate(root)
    # Forged "0"*64 now recomputes equal: the tamper case must still fail
    # loudly somewhere (recompute no longer discriminates -> the battery's
    # positive chain and determinism checks still pass, but the tamper
    # probe must not silently pass). Either VIOLATION or FAIL-CLOSED is
    # acceptable; a PASS is the defect.
    assert code != gate.EXIT_PASS, "\n".join(report)
