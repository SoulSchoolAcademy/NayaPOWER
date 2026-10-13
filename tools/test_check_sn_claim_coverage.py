"""Tests for tools/check_sn_claim_coverage.py (B-31).

Each test plants a synthetic duplicate on exactly one surface and asserts
the check refuses (exit 1, COLLISION); the clean case asserts exit 0.
Surfaces 1+2 are driven by injected fixtures (no live venue writes);
surfaces 3+4 by a scratch git repo. No test touches the real #554 board,
real PRs, or the live registry.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECK = Path(__file__).resolve().parent / "check_sn_claim_coverage.py"
SN = "SN-0798"


def make_repo():
    d = Path(tempfile.mkdtemp(prefix="sncover-"))
    subprocess.run(["git", "init", "-q", str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "config", "user.email", "t@t"],
                   check=True)
    subprocess.run(["git", "-C", str(d), "config", "user.name", "t"],
                   check=True)
    (d / "README.md").write_text("x")
    subprocess.run(["git", "-C", str(d), "add", "."], check=True)
    subprocess.run(["git", "-C", str(d), "commit", "-qm", "init"], check=True)
    return d


def run_check(sn, repo, fixtures=None, requester_ib=None,
              requester_names=()):
    fx = None
    if fixtures is not None:
        fx = Path(tempfile.mkdtemp(prefix="snfx-")) / "fx.json"
        fx.write_text(json.dumps(fixtures))
    cmd = [sys.executable, str(CHECK), "--sn", sn, "--repo", str(repo)]
    if fx:
        cmd += ["--fixtures", str(fx)]
    if requester_ib:
        cmd += ["--requester-ib", requester_ib]
    for n in requester_names:
        cmd += ["--requester-name", n]
    env = dict(os.environ)
    env["SN_COVERAGE_API_BIN"] = "/bin/false"  # no live API in tests
    p = subprocess.run(cmd, capture_output=True, text=True, env=env,
                       timeout=120)
    try:
        verdict = json.loads(p.stdout)
    except json.JSONDecodeError:
        verdict = {"_raw": p.stdout, "_stderr": p.stderr}
    return p.returncode, verdict


CLEAN_FX = {"comments": [], "prs": []}


class TestFourSurfaces(unittest.TestCase):
    def test_clean_repo_passes(self):
        repo = make_repo()
        rc, v = run_check(SN, repo, CLEAN_FX)
        self.assertEqual(rc, 0, v)
        self.assertEqual(v["verdict"], "CLEAR")
        self.assertEqual(v["unreadable_surfaces"], [])

    def test_board_only_claim_refuses(self):
        repo = make_repo()
        fx = {"comments": [{
            "id": 1, "author": None,
            "user": {"login": "SomeSeat"},
            "created_at": "2026-10-12T00:00:00Z",
            "body": "claiming SN-0798 for my note"}],
              "prs": []}
        rc, v = run_check(SN, repo, fx)
        self.assertEqual(rc, 1, v)
        self.assertEqual(v["verdict"], "COLLISION")
        self.assertEqual(v["foreign_claims"][0]["surface"], "board_comments")

    def test_pr_head_only_claim_refuses(self):
        repo = make_repo()
        fx = {"comments": [], "prs": [{
            "number": 99, "user": {"login": "SomeSeat"},
            "title": "smart notes batch", "body": "", "head": {"ref": "x"},
            "files": [{
                "filename": "BRAIN/05-MEMORY/SMART-NOTES/2026/10/12/CAT/TOP/SUB/SN-0798/ib.md",
                "patch": "+smart_note_id: SN-0798"}]}]}
        rc, v = run_check(SN, repo, fx)
        self.assertEqual(rc, 1, v)
        self.assertEqual(v["foreign_claims"][0]["surface"], "pr_heads")

    def test_commit_graph_only_claim_refuses(self):
        repo = make_repo()
        p = repo / "BRAIN" / "05-MEMORY" / "SMART-NOTES" / "2026" / "10" / "12" \
            / "CAT" / "SN-0798"
        p.mkdir(parents=True)
        (p / "ib-other.md").write_text(
            "---\nintelligent_block_id: IB-OTHER\nsmart_note_id: SN-0798\n---\n")
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm",
                        "stage SN-0798"], check=True)
        rc, v = run_check(SN, repo, CLEAN_FX)
        self.assertEqual(rc, 1, v)
        self.assertEqual(v["verdict"], "COLLISION")
        surfs = {h["surface"] for h in v["foreign_claims"]}
        self.assertIn("commit_graph", surfs)

    def test_cross_date_partition_claim_refuses(self):
        repo = make_repo()
        for day, ib in (("11", "IB-A"), ("12", "IB-B")):
            p = repo / "BRAIN" / "05-MEMORY" / "SMART-NOTES" / "2026" / "10" / day \
                / "CAT" / "SN-0798"
            p.mkdir(parents=True)
            (p / f"{ib}.md").write_text(
                f"---\nintelligent_block_id: {ib}\nsmart_note_id: SN-0798\n---\n")
        rc, v = run_check(SN, repo, CLEAN_FX)
        self.assertEqual(rc, 1, v)
        parts = [h for h in v["foreign_claims"]
                 if h["surface"] == "date_partitions"]
        # 2 date dirs (fail-closed: no ib) + 2 note files, different owners
        self.assertEqual(len(parts), 4, v)
        owners = {h.get("owner_ib") for h in parts}
        self.assertIn("IB-A", owners)
        self.assertIn("IB-B", owners)

    def test_self_claim_does_not_refuse(self):
        repo = make_repo()
        fx = {"comments": [{
            "id": 2, "user": {"login": "SoulSchoolAcademy"},
            "created_at": "2026-10-12T00:00:00Z",
            "body": "## [WAVE 5] [Naya Librarian] sign-in: claiming SN-0798"}],
              "prs": []}
        rc, v = run_check(SN, repo, fx,
                          requester_names=["Naya Librarian"])
        self.assertEqual(rc, 0, v)
        self.assertEqual(v["self_hits"][0]["surface"], "board_comments")

    def test_registry_owned_id_returns_clear_with_warnings(self):
        repo = make_repo()
        idx = repo / ".naya" / "memory" / "smart-notes"
        idx.mkdir(parents=True)
        (idx / "index.json").write_text(json.dumps({
            "entries": [{
                "intelligent_block_id": "IB-MINE",
                "smart_note_id": "SN-0798"}]}))
        fx = {"comments": [{
            "id": 3, "user": {"login": "Rival"},
            "created_at": "2026-10-12T00:00:00Z",
            "body": "claiming SN-0798"}],
              "prs": []}
        rc, v = run_check(SN, repo, fx, requester_ib="IB-MINE")
        self.assertEqual(rc, 0, v)
        self.assertTrue(v["already_owned_by_requester"])
        self.assertEqual(len(v["warnings"]), 1)

    def test_unreadable_surface_fails_closed(self):
        d = Path(tempfile.mkdtemp(prefix="sncover-nogit-"))
        rc, v = run_check(SN, d, CLEAN_FX)
        self.assertEqual(rc, 2, v)
        self.assertEqual(v["verdict"], "SURFACE_ERROR")
        self.assertIn("commit_graph", v["unreadable_surfaces"])

    def test_prose_mention_is_advisory_not_refusal(self):
        repo = make_repo()
        subprocess.run(["git", "-C", str(repo), "commit", "-q",
                        "--allow-empty", "-m",
                        "see SN-0798 for background"], check=True)
        rc, v = run_check(SN, repo, CLEAN_FX)
        self.assertEqual(rc, 0, v)
        self.assertEqual(v["mentions"][0]["surface"], "commit_graph")


def _load_smart_note_v2():
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    import smart_note_v2 as m
    return m


def _wire_capture():
    return {"smart_note_id": None, "title": "wire test",
            "source": {"captured_at": "2026-10-12T00:00:00Z"},
            "category": "x", "topic": "y", "subtopic": "z"}


def _wire_verify(ib):
    return {"persisted": {
        "block": {"intelligent_block_id": ib,
                  "content": {"lesson": "wire lesson"},
                  "understanding_state": "TEST",
                  "owner_scope": "PRIVATE"},
        "event": {"id": "e1"}, "lineage": {"id": "l1"},
        "relationship": {"relationship_id": "r1"},
        "index": {"id": "i1"}, "checkpoint": {"id": "c1"},
        "receipt": {"id": "rc1"}}}


def _tmp_registry():
    d = Path(tempfile.mkdtemp(prefix="sncover-reg-"))
    reg = d / "index.json"
    reg.write_text(json.dumps(
        {"entries": [], "sequence_policy": {"next_sequence": 1}}))
    return reg


class TestClaimPathWiring(unittest.TestCase):
    """The claim path refuses on foreign claims (B-31 wiring).

    These tests opt back into enforcement explicitly: the module skips the
    live scan under PYTEST_CURRENT_TEST, so each test removes that marker
    for its duration. Fixtures keep the board/PR surfaces offline; surfaces
    3+4 run against scratch repos. Nothing touches the live venue, the
    live registry, or the network.
    """

    def _enforced(self):
        import contextlib

        @contextlib.contextmanager
        def ctx():
            saved = dict(os.environ)
            os.environ.pop("PYTEST_CURRENT_TEST", None)
            try:
                yield
            finally:
                os.environ.clear()
                os.environ.update(saved)
        return ctx()

    def test_enforce_refuses_foreign_claim(self):
        m = _load_smart_note_v2()
        repo = make_repo()
        fx = {"comments": [{
            "id": 9, "user": {"login": "Rival"},
            "created_at": "2026-10-12T00:00:00Z",
            "body": "claiming SN-0798 for the rival note"}],
              "prs": []}
        with self._enforced(), self.assertRaises(SystemExit) as cm:
            m._enforce_four_surface_coverage("SN-0798", "IB-MINE",
                                            fixtures=fx, repo=str(repo))
        self.assertIn("SMART_NOTE_ID_COLLISION", str(cm.exception))
        self.assertIn("board_comments", str(cm.exception))

    def test_enforce_passes_clean(self):
        m = _load_smart_note_v2()
        # SN-99991: no real claim anywhere; fixtures keep board/PR offline.
        with self._enforced():
            m._enforce_four_surface_coverage(
                "SN-99991", "IB-MINE",
                fixtures={"comments": [], "prs": []},
                repo=str(make_repo()))  # no raise = pass

    def test_enforce_fails_closed_on_unreadable(self):
        # The supported mock seam is _get_check_sn (the single use-site
        # binding). Patching the checker's module attribute is UNSOUND:
        # without a tools/__init__.py the two import forms create two
        # module identities, the mock silently misses, and the LIVE check
        # runs instead (observed: OOM on the live PR-head fetch).
        m = _load_smart_note_v2()
        from unittest import mock
        bad = {"sn": "SN-99991", "verdict": "SURFACE_ERROR",
               "unreadable_surfaces": ["board_comments"],
               "foreign_claims": []}
        with self._enforced(), \
                mock.patch.object(m, "_get_check_sn",
                                  return_value=lambda *a, **k: bad):
            with self.assertRaises(SystemExit) as cm:
                m._enforce_four_surface_coverage("SN-99991", "IB-MINE")
            self.assertIn("SN_CLAIM_SURFACE_UNREADABLE", str(cm.exception))

    def test_mock_seam_actually_intercepts(self):
        # Polarity probe for the seam: with the API client pointed at
        # /bin/false and NO fixtures, the live path MUST fail closed
        # (SURFACE_ERROR -> SystemExit). A CLEAR mock returning normally
        # proves the mock intercepted instead of the live check running;
        # if the seam ever regresses, this test fails instead of silently
        # exercising the venue.
        m = _load_smart_note_v2()
        from unittest import mock
        clear = {"sn": "SN-99991", "verdict": "CLEAR",
                 "unreadable_surfaces": [], "foreign_claims": []}
        with self._enforced(), \
                mock.patch.object(m, "_get_check_sn",
                                  return_value=lambda *a, **k: clear), \
                mock.patch.dict(os.environ,
                                {"SN_COVERAGE_API_BIN": "/bin/false"}):
            m._enforce_four_surface_coverage("SN-99991", "IB-MINE",
                                             repo=str(make_repo()))
        # No SystemExit == the mock intercepted. The live path would have
        # raised SN_CLAIM_SURFACE_UNREADABLE.

    def test_reserve_refuses_foreign_claim_full_wire(self):
        # Full wire: reserve_smart_note_id -> _enforce -> check_sn.
        # next_sequence=1 -> candidate SN-001; the fixture claims SN-0001.
        m = _load_smart_note_v2()
        reg = _tmp_registry()
        fx = {"comments": [{
            "id": 9, "user": {"login": "Rival"},
            "created_at": "2026-10-12T00:00:00Z",
            "body": "claiming SN-0001 for the rival note"}],
              "prs": []}
        with self._enforced(), \
                self.assertRaises(SystemExit) as cm:
            m.reserve_smart_note_id(
                _wire_capture(), "IB-WIRE-TEST",
                registry_path=str(reg),
                coverage_fixtures=fx,
                coverage_repo=str(make_repo()))
        self.assertIn("SMART_NOTE_ID_COLLISION", str(cm.exception))
        # Refusal wrote nothing: sequence unadvanced, no entries.
        r = json.loads(reg.read_text())
        self.assertEqual(r["sequence_policy"]["next_sequence"], 1)
        self.assertEqual(r["entries"], [])

    def test_reserve_commits_clean_full_wire(self):
        m = _load_smart_note_v2()
        reg = _tmp_registry()
        with self._enforced():
            sn = m.reserve_smart_note_id(
                _wire_capture(), "IB-WIRE-TEST",
                registry_path=str(reg),
                coverage_fixtures={"comments": [], "prs": []},
                coverage_repo=str(make_repo()))
        self.assertEqual(sn, "SN-001")
        r = json.loads(reg.read_text())
        self.assertEqual(r["sequence_policy"]["next_sequence"], 2)

    def test_update_registry_unreserved_path_enforces(self):
        # B-31 regression test: update_registry(sn_id=None) used to allocate
        # via raw _allocate_from_registry with no surface scan -- a second,
        # unscanned claim path around the gate. Now it reserves through the
        # enforced path: foreign claim -> SystemExit BEFORE any write.
        m = _load_smart_note_v2()
        from unittest import mock
        reg = _tmp_registry()
        fx = {"comments": [{
            "id": 9, "user": {"login": "Rival"},
            "created_at": "2026-10-12T00:00:00Z",
            "body": "claiming SN-0001 for the rival note"}],
              "prs": []}
        proj = Path(tempfile.mkdtemp(prefix="sncover-proj-")) / "n.md"
        with self._enforced(), \
                mock.patch.object(m, "REGISTRY", reg), \
                self.assertRaises(SystemExit) as cm:
            m.update_registry(
                _wire_capture(), _wire_verify("IB-WIRE-TEST"), proj,
                coverage_fixtures=fx,
                coverage_repo=str(make_repo()))
        self.assertIn("SMART_NOTE_ID_COLLISION", str(cm.exception))
        r = json.loads(reg.read_text())
        self.assertEqual(r["entries"], [])

    def test_update_registry_unreserved_path_commits_clean(self):
        # Positive control: clean surfaces -> the unreserved path allocates
        # AND records the entry (the outcome the project flow gets via an
        # explicit reservation).
        m = _load_smart_note_v2()
        from unittest import mock
        reg = _tmp_registry()
        proj = Path(tempfile.mkdtemp(prefix="sncover-proj-")) / "n.md"
        with self._enforced(), mock.patch.object(m, "REGISTRY", reg):
            entry = m.update_registry(
                _wire_capture(), _wire_verify("IB-WIRE-TEST"), proj,
                coverage_fixtures={"comments": [], "prs": []},
                coverage_repo=str(make_repo()))
        self.assertEqual(entry["smart_note_id"], "SN-001")
        self.assertEqual(entry["intelligent_block_id"], "IB-WIRE-TEST")
        r = json.loads(reg.read_text())
        self.assertEqual(len(r["entries"]), 1)


    def test_git_timeout_fails_closed_not_crash(self):
        # B-31 wave-13: an unhandled TimeoutExpired in _git killed the whole
        # live --audit with a traceback. Now it converts to RuntimeError so
        # the caller fails the surface closed (SURFACE_ERROR), never crashes.
        import check_sn_claim_coverage as c
        from unittest import mock
        with mock.patch.object(
                c.subprocess, "run",
                side_effect=c.subprocess.TimeoutExpired("git", 180)):
            with self.assertRaises(RuntimeError) as cm:
                c._git(".", "log", "--all", timeout=180)
        self.assertIn("timed out", str(cm.exception))

    def test_update_registry_explicit_sn_id_refuses_foreign_claim(self):
        # B-31 wave-13 (probe P2): update_registry(sn_id=<explicit>) used to
        # trust caller provenance with no four-surface scan -- a hand-rolled
        # sn_id bypassed the gate entirely. Now the explicit path scans
        # before the transaction: foreign claim -> SystemExit, nothing
        # written.
        m = _load_smart_note_v2()
        from unittest import mock
        reg = _tmp_registry()
        fx = {"comments": [{
            "id": 9, "user": {"login": "Rival"},
            "created_at": "2026-10-12T00:00:00Z",
            "body": "claiming SN-0001 for the rival note"}],
              "prs": []}
        proj = Path(tempfile.mkdtemp(prefix="sncover-proj-")) / "n.md"
        with self._enforced(), \
                mock.patch.object(m, "REGISTRY", reg), \
                self.assertRaises(SystemExit) as cm:
            m.update_registry(
                _wire_capture(), _wire_verify("IB-WIRE-TEST"), proj,
                sn_id="SN-0001",
                coverage_fixtures=fx,
                coverage_repo=str(make_repo()))
        self.assertIn("SMART_NOTE_ID_COLLISION", str(cm.exception))
        r = json.loads(reg.read_text())
        self.assertEqual(r["entries"], [])

    def test_update_registry_explicit_sn_id_commits_clean(self):
        # Positive control: the explicit path scans and then records --
        # this is what the project CLI flow (reserve -> update_registry)
        # relies on; the second scan is redundant-but-harmless by design.
        m = _load_smart_note_v2()
        from unittest import mock
        reg = _tmp_registry()
        proj = Path(tempfile.mkdtemp(prefix="sncover-proj-")) / "n.md"
        with self._enforced(), mock.patch.object(m, "REGISTRY", reg):
            entry = m.update_registry(
                _wire_capture(), _wire_verify("IB-WIRE-TEST"), proj,
                sn_id="SN-0042",
                coverage_fixtures={"comments": [], "prs": []},
                coverage_repo=str(make_repo()))
        self.assertEqual(entry["smart_note_id"], "SN-0042")
        r = json.loads(reg.read_text())
        self.assertEqual(len(r["entries"]), 1)
        self.assertEqual(r["sequence_policy"]["next_sequence"], 43)


if __name__ == "__main__":
    unittest.main()
