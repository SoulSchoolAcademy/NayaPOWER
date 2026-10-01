"""RED tests for the coordinator's three reproduced trust-boundary failures.

Each test reproduces a case the coordinator demonstrated against the
published Demo-1. They MUST fail on the unrepaired head and pass after
the boundary repairs (directive moves 3/4/5):

  1. fresh_verify resolves the tool from the canonical registry by a
     hardcoded name instead of the receipt's own ``tool`` binding, and it
     never inspects ``authority_basis.revoked``. A resealed receipt with
     a revoked basis or a phantom tool currently exits 0.
  2. ``make_staging_executor`` follows a ``<base>/demo-staging`` symlink
     to a directory outside ``<base>`` and reports ok.
  3. The ``exists()`` -> ``write_bytes()`` sequence lets two concurrent
     conflicting writes both report ok; the loser silently overwrites
     the winner.

These are behavior tests, not ImportError placeholders: each exercises
the real seam and fails for its actual reason.
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from naya_kernel import smart_door
from naya_kernel.nodes import act_node

REPO_ROOT = Path(__file__).resolve().parents[2]
FRESH_VERIFY = REPO_ROOT / "scripts" / "demo1" / "fresh_verify.py"

FILENAME = "sn-candidate-red-boundary.md"
CONTENT = "# RED boundary probe\n\nReal executor, real receipt.\n"


def _run_demo(root: Path) -> dict:
    """Execute one real bounded write, mirroring scripts/demo1/act_run.py."""
    registry = smart_door.staging_tool_registry()
    receipt = act_node.make_decision_receipt(
        receipt_id="dec-red-001",
        issued_at="2026-10-01T15:55:00+00:00",
        valid_until="2026-10-02T00:00:00+00:00",
        winner={"tool_id": "staging.write_file", "version": "1.0",
                "params": {"filename": FILENAME, "content": CONTENT}},
        authority_basis={"kind": "director_order", "ref": "order-demo-1",
                         "revoked": False},
    )
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(root)))
    state = {"decision_receipt": receipt, "tool_registry": registry,
             "execution_ledger": {}, "now": "2026-10-01T15:55:00+00:00"}
    handoff = node.execute(state)
    assert handoff["path"] == "EXECUTED", handoff["receipt"]
    return handoff["receipt"]


def _write_receipt(root: Path, receipt: dict) -> Path:
    rdir = root / "demo-staging" / "receipts"
    rdir.mkdir(parents=True, exist_ok=True)
    rpath = rdir / (receipt["execution_id"] + ".json")
    rpath.write_text(json.dumps(receipt, indent=2, sort_keys=True),
                     encoding="utf-8")
    return rpath


def _reseal(receipt: dict) -> dict:
    receipt["receipt_hash"] = act_node._sha256(
        {k: v for k, v in receipt.items() if k != "receipt_hash"})
    return receipt


def _fresh_verify(rpath: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(FRESH_VERIFY), str(rpath)],
                          capture_output=True, text=True, timeout=60)


# ---------------------------------------------------------------------------
# 1. fresh_verify must bind the receipt's ACTUAL tool and authority basis
# ---------------------------------------------------------------------------

class TestFreshVerifyBindsReceipt:
    def test_rejects_revoked_authority_basis(self, tmp_path):
        receipt = _run_demo(tmp_path)
        bad = json.loads(json.dumps(receipt))
        bad["authority_basis"] = dict(bad["authority_basis"], revoked=True)
        rpath = _write_receipt(tmp_path, _reseal(bad))
        proc = _fresh_verify(rpath)
        assert proc.returncode != 0, (
            "fresh_verify exited 0 for a resealed receipt whose "
            "authority_basis.revoked=True\n" + proc.stdout)

    def test_rejects_undeclared_tool(self, tmp_path):
        receipt = _run_demo(tmp_path)
        bad = json.loads(json.dumps(receipt))
        bad["tool"] = {"tool_id": "phantom_tool", "version": "9.9",
                       "idempotent": False}
        rpath = _write_receipt(tmp_path, _reseal(bad))
        proc = _fresh_verify(rpath)
        assert proc.returncode != 0, (
            "fresh_verify exited 0 for a resealed receipt naming "
            "phantom_tool, which the canonical registry never declared\n"
            + proc.stdout)

    def test_accepts_honest_receipt(self, tmp_path):
        """Control: the unmodified receipt must still verify."""
        receipt = _run_demo(tmp_path)
        rpath = _write_receipt(tmp_path, receipt)
        proc = _fresh_verify(rpath)
        assert proc.returncode == 0, proc.stdout + proc.stderr


# ---------------------------------------------------------------------------
# 2. The staging root must not escape via symlink
# ---------------------------------------------------------------------------

class TestStagingRootContainment:
    def test_refuses_symlinked_staging_dir(self, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        (tmp_path / "demo-staging").symlink_to(outside, target_is_directory=True)
        ex = smart_door.make_staging_executor(str(tmp_path))
        res = ex("staging.write_file",
                 {"filename": FILENAME, "content": CONTENT})
        assert res["status"] == "error", (
            "executor reported ok through a symlinked staging root: %r"
            % (res,))
        assert not (outside / FILENAME).exists(), (
            "executor wrote OUTSIDE the sandbox root via symlink")

    def test_honest_write_still_works(self, tmp_path):
        """Control: a normal staging dir still accepts the write."""
        ex = smart_door.make_staging_executor(str(tmp_path))
        res = ex("staging.write_file",
                 {"filename": FILENAME, "content": CONTENT})
        assert res["status"] == "ok", res
        assert (tmp_path / "demo-staging" / FILENAME).read_text() == CONTENT


# ---------------------------------------------------------------------------
# 4. Canonical declaration binds runtime behavior (move 4)
# ---------------------------------------------------------------------------

class TestDeclarationBindsRuntime:
    def _tight_registry(self, tmp_path, **param_overrides):
        reg = json.loads((REPO_ROOT / "BRAIN/10-INTERFACES"
                          / "0002-SMART-DOOR-REGISTRY-V1.json").read_text())
        for door in reg["doors"]:
            if door["door_id"] == "DOOR-LOCAL-STAGING":
                for op in door["operations"]:
                    if op["operation"] == "staging.write_file":
                        op["params"].update(param_overrides)
        p = tmp_path / "registry-tight.json"
        p.write_text(json.dumps(reg), encoding="utf-8")
        return p

    def test_tightened_max_bytes_tightens_runtime(self, tmp_path):
        tight = self._tight_registry(tmp_path, max_bytes=16)
        ex_tight = smart_door.make_staging_executor(
            str(tmp_path), registry_path=tight)
        res = ex_tight("staging.write_file",
                       {"filename": FILENAME, "content": "x" * 17})
        assert res["status"] == "error", res
        # The default declaration still admits the same write.
        ex_default = smart_door.make_staging_executor(str(tmp_path))
        res2 = ex_default("staging.write_file",
                          {"filename": "sn-candidate-ok.md",
                           "content": "x" * 17})
        assert res2["status"] == "ok", res2

    def test_incompatible_declaration_fails_closed(self, tmp_path):
        reg = json.loads((REPO_ROOT / "BRAIN/10-INTERFACES"
                          / "0002-SMART-DOOR-REGISTRY-V1.json").read_text())
        for door in reg["doors"]:
            if door["door_id"] == "DOOR-LOCAL-STAGING":
                for op in door["operations"]:
                    if op["operation"] == "staging.write_file":
                        del op["params"]["max_bytes"]
        p = tmp_path / "registry-broken.json"
        p.write_text(json.dumps(reg), encoding="utf-8")
        with pytest.raises(ValueError, match="max_bytes"):
            smart_door.make_staging_executor(str(tmp_path), registry_path=p)

    def test_traversal_target_fails_closed(self, tmp_path):
        _, op = smart_door.find_operation(
            smart_door.load_registry(), "DOOR-LOCAL-STAGING",
            "staging.write_file")
        evil = json.loads(json.dumps(op))
        evil["target"] = "../escape/"
        with pytest.raises(ValueError, match="target"):
            smart_door.make_staging_executor(str(tmp_path), operation=evil)

class TestConcurrentWrites:
    def test_conflicting_concurrent_writes_single_winner(
            self, tmp_path, monkeypatch):
        # Force both threads to observe "not present" before either writes,
        # exactly the interleaving the coordinator produced.
        real_exists = Path.exists

        def fake_exists(self):
            if self.name == FILENAME:
                return False
            return real_exists(self)

        monkeypatch.setattr(Path, "exists", fake_exists)

        ex = smart_door.make_staging_executor(str(tmp_path))
        barrier = threading.Barrier(2)
        results = {}

        def worker(tag, content):
            barrier.wait()
            results[tag] = ex("staging.write_file",
                              {"filename": FILENAME, "content": content})

        threads = [
            threading.Thread(target=worker, args=("a", "content-from-A\n")),
            threading.Thread(target=worker, args=("b", "content-from-B\n")),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)

        statuses = sorted(r["status"] for r in results.values())
        assert statuses == ["error", "ok"], (
            "expected exactly one winner and one refusal, got %r" % (results,))
        on_disk = (tmp_path / "demo-staging" / FILENAME).read_text()
        winner = "a" if results["a"]["status"] == "ok" else "b"
        assert on_disk == ("content-from-A\n" if winner == "a"
                           else "content-from-B\n"), (
            "loser's content overwrote the winner's: %r" % on_disk)
