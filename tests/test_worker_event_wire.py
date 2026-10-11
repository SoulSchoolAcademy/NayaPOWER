#!/usr/bin/env python3
"""Tests for the #2244-D worker-lifecycle -> learning-event wire.

Covers tools/worker_event_wire.py plus the two gate call-sites
(worker_entry.py STAND_DOWN, worker_exit.py blocked). Every emission test
has a matching no-emission or no-raise control; the negative-control test
runs the UNPATCHED main-branch gates to prove the emission comes from the
new call-sites, not from the wire module alone.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
TESTS = Path(__file__).resolve().parent

PY = sys.executable
TIP_40 = "57e935c1b44b10fcc27a80f8c99fc9ddb2e69440"
TIP_40_B = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def run_gate(script: Path, *args, env_extra: dict | None = None, cwd: Path | None = None):
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run(
        [PY, str(script), *args],
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        cwd=str(cwd or TOOLS.parent),
    )


def make_fake_home(tip: str = TIP_40, stand_down: bool = False) -> Path:
    """Hermetic HOME for worker_entry.py (GOAL_DIR derives from HOME)."""
    home = Path(tempfile.mkdtemp(prefix="wire-home-"))
    goal = home / "workspace/goals/nayapower-10-10-completion-drive/hidden_files"
    goal.mkdir(parents=True)
    (goal / "LIVE-PLAN.md").write_text(
        "# plan\n## TIP NOTE\n- tip: `%s` (verified)\n" % tip, encoding="utf-8"
    )
    if stand_down:
        (goal / "api-stand-down.flag").write_text("test", encoding="utf-8")
    return home


def read_ledger(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def copy_gate_tree(dest: Path, *, with_envelope: bool, broken_envelope: bool = False):
    tools = dest / "tools"
    tools.mkdir(parents=True)
    for name in ("worker_event_wire.py", "worker_entry.py", "worker_exit.py"):
        shutil.copy(TOOLS / name, tools / name)
    if broken_envelope:
        (tools / "learning_event_envelope.py").write_text(
            "raise RuntimeError('present-but-broken outbox/envelope')\n", encoding="utf-8"
        )
    elif with_envelope:
        shutil.copy(TOOLS / "learning_event_envelope.py", tools / "learning_event_envelope.py")


class WireUnitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="wire-unit-"))
        self.ledger = self.tmp / "ledger.json"
        sys.path.insert(0, str(TOOLS))
        import worker_event_wire  # noqa: E402
        import importlib  # noqa: E402
        self.wire = importlib.reload(worker_event_wire)

    def tearDown(self):
        sys.path.remove(str(TOOLS))
        shutil.rmtree(self.tmp, ignore_errors=True)

    _MISSING = object()

    def _env(self, **kw):
        env = {"NAYA_EVENT_LEDGER": str(self.ledger)}
        env.update(kw)
        old = {k: os.environ.get(k, self._MISSING) for k in env}
        os.environ.update(env)

        def restore():
            for k, v in old.items():
                if v is self._MISSING:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

        self.addCleanup(restore)
        return env

    def test_emit_and_duplicate(self):
        self._env()
        r1 = self.wire.emit_lifecycle_event(
            event_type="blocker", severity="WARNING", title="t", expected="e",
            actual="a", next_action="n", source_artifact="tools/worker_exit.py",
            source_sha=TIP_40,
        )
        self.assertEqual(r1["status"], "emitted")
        self.assertTrue(r1["event_id"].startswith("evt-"))
        r2 = self.wire.emit_lifecycle_event(
            event_type="blocker", severity="WARNING", title="t", expected="e",
            actual="a", next_action="n", source_artifact="tools/worker_exit.py",
            source_sha=TIP_40,
        )
        self.assertEqual(r2["status"], "duplicate")
        self.assertEqual(r1["event_id"], r2["event_id"])
        self.assertEqual(len(read_ledger(self.ledger)["events"]), 1)

    def test_kill_switch(self):
        self._env(NAYA_LIFECYCLE_EVENTS="0")
        r = self.wire.emit_lifecycle_event(
            event_type="blocker", severity="WARNING", title="t", expected="e",
            actual="a", next_action="n", source_artifact="tools/worker_exit.py",
            source_sha=TIP_40,
        )
        self.assertEqual(r, {"status": "skipped", "reason": "kill_switch"})
        self.assertFalse(self.ledger.exists())

    def test_no_source_sha_skips(self):
        self._env()
        r = self.wire.emit_lifecycle_event(
            event_type="blocker", severity="WARNING", title="t", expected="e",
            actual="a", next_action="n", source_artifact="tools/worker_exit.py",
            source_sha=None, goal_dir=str(self.tmp / "no-goal-here"),
        )
        self.assertEqual(r["status"], "skipped")
        self.assertEqual(r["reason"], "no_source_sha")
        self.assertFalse(self.ledger.exists())

    def test_envelope_unavailable_skips_never_raises(self):
        self._env()
        real_import = self.wire._import_envelope
        self.wire._import_envelope = lambda: None
        try:
            r = self.wire.emit_lifecycle_event(
                event_type="blocker", severity="WARNING", title="t", expected="e",
                actual="a", next_action="n", source_artifact="tools/worker_exit.py",
                source_sha=TIP_40,
            )
        finally:
            self.wire._import_envelope = real_import
        self.assertEqual(r, {"status": "skipped", "reason": "envelope_unavailable"})

    def test_broken_envelope_never_raises(self):
        self._env()
        def boom():
            raise RuntimeError("import exploded")
        real_import = self.wire._import_envelope
        self.wire._import_envelope = boom
        try:
            r = self.wire.emit_lifecycle_event(
                event_type="blocker", severity="WARNING", title="t", expected="e",
                actual="a", next_action="n", source_artifact="tools/worker_exit.py",
                source_sha=TIP_40,
            )
        finally:
            self.wire._import_envelope = real_import
        self.assertEqual(r["status"], "skipped")
        self.assertTrue(r["reason"].startswith("wire_error:"))


class ExitGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="wire-exit-"))
        self.ledger = self.tmp / "ledger.json"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, *args, tree_tools: Path = TOOLS, **env_extra):
        env = {"NAYA_EVENT_LEDGER": str(self.ledger)}
        env.update(env_extra)
        return run_gate(tree_tools / "worker_exit.py", *args, env_extra=env)

    def test_blocked_emits_detected_blocker(self):
        r = self._run("--claim", "blocked", "--evidence", "waiting on PR #2293 merge")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("EVENT_WIRE:", r.stdout)
        receipt = json.loads(r.stdout.split("EVENT_WIRE:", 1)[1].strip().splitlines()[0])
        self.assertEqual(receipt["status"], "emitted")
        events = read_ledger(self.ledger)["events"]
        self.assertEqual(len(events), 1)
        env_rec = next(iter(events.values()))
        self.assertEqual(env_rec["event_type"], "blocker")
        self.assertEqual(env_rec["severity"], "WARNING")
        self.assertEqual(env_rec["lifecycle_state"], "DETECTED")
        self.assertEqual(env_rec["source_artifact"], "tools/worker_exit.py")
        self.assertIn("waiting on PR #2293 merge", env_rec["actual"])
        self.assertEqual(len(env_rec["source_sha"]), 40)

    def test_blocked_is_idempotent(self):
        self._run("--claim", "blocked", "--evidence", "same blocker twice")
        r2 = self._run("--claim", "blocked", "--evidence", "same blocker twice")
        receipt = json.loads(r2.stdout.split("EVENT_WIRE:", 1)[1].strip().splitlines()[0])
        self.assertEqual(receipt["status"], "duplicate")
        self.assertEqual(len(read_ledger(self.ledger)["events"]), 1)

    def test_nothing_changed_emits_nothing(self):
        r = self._run("--claim", "nothing_changed")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("EVENT_WIRE:", r.stdout)
        self.assertFalse(self.ledger.exists())

    def test_work_done_emits_nothing(self):
        r = self._run("--claim", "work_done", "--evidence", "merged PR #9999, tests 10/10 verified")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("EVENT_WIRE:", r.stdout)
        self.assertFalse(self.ledger.exists())

    def test_rejected_blocked_emits_nothing(self):
        r = self._run("--claim", "blocked")
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("EVENT_WIRE:", r.stdout)
        self.assertFalse(self.ledger.exists())

    def test_kill_switch_blocks_exit_emission(self):
        r = self._run("--claim", "blocked", "--evidence", "x", NAYA_LIFECYCLE_EVENTS="0")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"status": "skipped"', r.stdout)
        self.assertFalse(self.ledger.exists())

    def test_absent_envelope_gate_unaffected(self):
        tree = self.tmp / "noenv"
        copy_gate_tree(tree, with_envelope=False)
        r = self._run("--claim", "blocked", "--evidence", "no envelope here",
                      tree_tools=tree / "tools")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"reason": "envelope_unavailable"', r.stdout)
        self.assertFalse(self.ledger.exists())

    def test_broken_envelope_gate_unaffected(self):
        tree = self.tmp / "broken"
        copy_gate_tree(tree, with_envelope=False, broken_envelope=True)
        r = self._run("--claim", "blocked", "--evidence", "broken envelope here",
                      tree_tools=tree / "tools")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"status": "skipped"', r.stdout)
        self.assertFalse(self.ledger.exists())


class EntryGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="wire-entry-"))
        self.ledger = self.tmp / "ledger.json"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_stand_down_emits_detected_blocker(self):
        home = make_fake_home(tip=TIP_40, stand_down=True)
        try:
            env = {"HOME": str(home), "NAYA_EVENT_LEDGER": str(self.ledger)}
            r = run_gate(TOOLS / "worker_entry.py", env_extra=env)
        finally:
            shutil.rmtree(home, ignore_errors=True)
        self.assertEqual(r.returncode, 20, r.stderr + r.stdout)
        self.assertIn("STAND_DOWN", r.stdout)
        self.assertIn("EVENT_WIRE:", r.stdout)
        receipt = json.loads(r.stdout.split("EVENT_WIRE:", 1)[1].strip().splitlines()[0])
        self.assertEqual(receipt["status"], "emitted")
        events = read_ledger(self.ledger)["events"]
        self.assertEqual(len(events), 1)
        env_rec = next(iter(events.values()))
        self.assertEqual(env_rec["event_type"], "blocker")
        self.assertEqual(env_rec["severity"], "NOTICE")
        self.assertEqual(env_rec["lifecycle_state"], "DETECTED")
        self.assertEqual(env_rec["source_artifact"], "tools/worker_entry.py")
        self.assertEqual(env_rec["source_sha"], TIP_40)

    def test_stand_down_absent_envelope_verdict_intact(self):
        tree = self.tmp / "noenv"
        copy_gate_tree(tree, with_envelope=False)
        home = make_fake_home(tip=TIP_40, stand_down=True)
        try:
            env = {"HOME": str(home), "NAYA_EVENT_LEDGER": str(self.ledger)}
            r = run_gate(tree / "tools" / "worker_entry.py", env_extra=env)
        finally:
            shutil.rmtree(home, ignore_errors=True)
        self.assertEqual(r.returncode, 20, r.stderr + r.stdout)
        self.assertIn("STAND_DOWN", r.stdout)
        self.assertFalse(self.ledger.exists())


class NegativeControlTests(unittest.TestCase):
    """Prove the emission comes from the new call-sites, not the wire module.

    Runs the UNPATCHED main-branch gate bytes (which lack the EVENT_WIRE
    call-sites) against the SAME wire module: the verdict must hold and no
    event may be emitted.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="wire-negctl-"))
        self.ledger = self.tmp / "ledger.json"
        tree = self.tmp / "mainbytes"
        copy_gate_tree(tree, with_envelope=True)
        # Overwrite with the exact main-branch gate bytes (no wire call-sites).
        for name in ("worker_entry.py", "worker_exit.py"):
            data = subprocess.run(
                ["git", "-C", str(TOOLS.parent), "show", f"57e935c1b44b10fcc27a80f8c99fc9ddb2e69440:{'tools/' + name}"],
                capture_output=True, timeout=30,
            ).stdout
            (tree / "tools" / name).write_bytes(data)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_unpatched_exit_blocked_emits_nothing(self):
        env = {"NAYA_EVENT_LEDGER": str(self.ledger)}
        r = run_gate(self.tmp / "mainbytes" / "tools" / "worker_exit.py",
                     "--claim", "blocked", "--evidence", "old bytes", env_extra=env)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("EVENT_WIRE:", r.stdout)
        self.assertFalse(self.ledger.exists())

    def test_unpatched_entry_stand_down_emits_nothing(self):
        home = make_fake_home(tip=TIP_40, stand_down=True)
        try:
            env = {"HOME": str(home), "NAYA_EVENT_LEDGER": str(self.ledger)}
            r = run_gate(self.tmp / "mainbytes" / "tools" / "worker_entry.py", env_extra=env)
        finally:
            shutil.rmtree(home, ignore_errors=True)
        self.assertEqual(r.returncode, 20, r.stderr + r.stdout)
        self.assertNotIn("EVENT_WIRE:", r.stdout)
        self.assertFalse(self.ledger.exists())


if __name__ == "__main__":
    unittest.main()
