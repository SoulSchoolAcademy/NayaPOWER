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

    def test_pr_head_mirror_copy_does_not_refuse(self):
        # B-56 polarity pole 1: a registry index.json mirror at a PR head
        # that is byte-identical to base (fixture declares "mirror_copy")
        # is the registry's voice, not a claim -> CLEAR, advisory only.
        repo = make_repo()
        fx = {"comments": [], "prs": [{
            "number": 99, "user": {"login": "SomeSeat"},
            "title": "smart notes batch", "body": "", "head": {"ref": "x"},
            "files": [{
                "filename": ".naya/memory/smart-notes/index.json",
                "patch": "+\"smart_note_id\": \"SN-0798\"",
                "mirror_copy": True}]}]}
        rc, v = run_check(SN, repo, fx)
        self.assertEqual(rc, 0, v)
        self.assertEqual(v["verdict"], "CLEAR")
        self.assertEqual(v["foreign_claims"], [])
        mirrors = [h for h in v["mirror_hits"]
                   if h["surface"] == "pr_heads"]
        self.assertTrue(mirrors, "mirror hit not reported as advisory")

    def test_pr_head_divergent_mirror_still_refuses(self):
        # B-56 polarity pole 2 (fail-closed): the same mirror path WITHOUT
        # the byte-identical declaration is a divergent/tampered mirror ->
        # stays claim-class -> COLLISION.
        repo = make_repo()
        fx = {"comments": [], "prs": [{
            "number": 99, "user": {"login": "SomeSeat"},
            "title": "smart notes batch", "body": "", "head": {"ref": "x"},
            "files": [{
                "filename": ".naya/memory/smart-notes/index.json",
                "patch": "+\"smart_note_id\": \"SN-0798\""}]}]}
        rc, v = run_check(SN, repo, fx)
        self.assertEqual(rc, 1, v)
        self.assertEqual(v["verdict"], "COLLISION")
        self.assertEqual(v["foreign_claims"][0]["surface"], "pr_heads")

    def test_pr_head_mirror_registry_voice_does_not_refuse(self):
        # B-56 core rule: a mirror token whose id is in the registry's id
        # set is the registry's voice -- no declaration needed -- so a
        # stale-based PR's mirror (divergent bytes, faithful ids) clears.
        repo = make_repo()
        fx = {"comments": [], "registry_nums": [798], "prs": [{
            "number": 99, "user": {"login": "SomeSeat"},
            "title": "smart notes batch", "body": "", "head": {"ref": "x"},
            "files": [{
                "filename": ".naya/memory/smart-notes/index.json",
                "patch": "+\"smart_note_id\": \"SN-0798\""}]}]}
        rc, v = run_check(SN, repo, fx)
        self.assertEqual(rc, 0, v)
        self.assertEqual(v["verdict"], "CLEAR")
        self.assertEqual(v["foreign_claims"], [])
        mirrors = [h for h in v["mirror_hits"]
                   if h["surface"] == "pr_heads"]
        self.assertTrue(mirrors, "mirror hit not reported as advisory")

    def test_pr_head_mirror_novel_id_still_refuses(self):
        # B-56 fail-closed pole: a mirror token the registry does not know
        # is a planted claim, not the registry's voice -> COLLISION.
        repo = make_repo()
        fx = {"comments": [], "registry_nums": [16], "prs": [{
            "number": 99, "user": {"login": "SomeSeat"},
            "title": "smart notes batch", "body": "", "head": {"ref": "x"},
            "files": [{
                "filename": ".naya/memory/smart-notes/index.json",
                "patch": "+\"smart_note_id\": \"SN-0798\""}]}]}
        rc, v = run_check(SN, repo, fx)
        self.assertEqual(rc, 1, v)
        self.assertEqual(v["verdict"], "COLLISION")
        self.assertEqual(v["foreign_claims"][0]["surface"], "pr_heads")

    def test_mirror_class_rule(self):
        # Unit test for the B-56 classifier: registry's voice vs planted
        # claim vs no-signal fail-closed.
        import check_sn_claim_coverage as c
        self.assertTrue(c._mirror_class(798, {16, 798}))
        self.assertFalse(c._mirror_class(798, {16}))
        self.assertFalse(c._mirror_class(798, set()))
        self.assertTrue(c._mirror_class(798, None, declared_copy=True))
        self.assertFalse(c._mirror_class(798, None, declared_copy=False))
        self.assertFalse(c._mirror_class(798, None))

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

    def test_graph_surface_never_walks_full_history_diff(self):
        # B-55 liveness pin: the wave-13 collector found graph commits via
        # `git log --all -G` -- a walk over every diff in history that never
        # finishes on the live repo (>460s measured, 600s budget blown ->
        # SURFACE_ERROR on all 1,109 registry ids; the allocation gate
        # would refuse every claim). The repaired collector is path-scoped
        # (message metadata + path-limited log + path-limited tree grep).
        # This test FAILS on the old implementation (it records -G in the
        # git argv) and PASSES on the repaired one -- a genuine
        # fail-without / pass-with guard against reintroducing the dead
        # gate.
        import check_sn_claim_coverage as c
        from unittest import mock
        repo = make_repo()
        seen = []
        real_git = c._git

        def recording_git(r, *args, **kw):
            seen.append(list(args))
            return real_git(r, *args, **kw)

        with mock.patch.object(c, "_git", recording_git):
            c.collect_graph(str(repo))
        walks = [a for a in seen if "-G" in a]
        self.assertEqual(walks, [],
                         f"full-history -G diff walk reintroduced: {walks}")

    def test_graph_surface_polarity_on_fixture_repo(self):
        # Polarity probe for the repaired collector on a controlled repo:
        # a note file added on a SN-bearing path, claiming the id with a
        # FOREIGN intelligent_block_id, is a claim-class graph hit; the
        # same shape with the requester's own ib is self-class (non-
        # refusing). Proves the path-scoped collector refuses and clears
        # on the right inputs, not just quickly.
        import check_sn_claim_coverage as c
        repo = make_repo()
        p = repo / "BRAIN" / "05-MEMORY" / "SMART-NOTES" / "2026" / "10" \
            / "13" / "PROBE" / "SN-0798"
        p.mkdir(parents=True)
        (p / "ib-foreign.md").write_text(
            "---\nintelligent_block_id: IB-FOREIGN\n"
            "smart_note_id: SN-0798\n---\n")
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm",
                        "probe"], check=True)
        by_num = c.collect_graph(str(repo))
        hits = by_num.get(798, [])
        claims = [h for h in hits if h.get("pre_class") == "claim"]
        self.assertTrue(claims,
                        f"no claim-class graph hit for the planted note: {hits}")
        # Requester's own ib on the same placement is self-attributed,
        # not a foreign claim: classify() puts it in self_hits.
        own = [dict(h, _num=798) for h in hits]
        _, self_hits, _, _ = c.classify(own, ["IB-FOREIGN", "Naya Librarian"],
                                        "IB-FOREIGN")
        self.assertTrue(self_hits, "owner-attributed hit misclassified")
        _, self_hits2, _, _ = c.classify(own, ["Naya Librarian"], "IB-OTHER")
        self.assertFalse(self_hits2,
                         "foreign-attributed hit self-classified")


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


class TestHeadDiffCollector(unittest.TestCase):
    """L-282 regression: the pr_heads collector keys on claim-authorship
    (open-PR-only refspec + diff-vs-base), never tree presence."""

    def _repo_with_note(self):
        repo = make_repo()
        n = (repo / "BRAIN" / "05-MEMORY" / "SMART-NOTES" / "2026" / "10"
             / "13" / "CAT" / "SN-0013")
        n.mkdir(parents=True)
        (n / "ib.md").write_text(
            "---\nintelligent_block_id: IB-OWN\n"
            "smart_note_id: SN-0013\n---\nbody\n")
        subprocess.run(["git", "-C", str(repo), "add", "."],
                       check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm",
                        "register SN-0013"], check=True)
        base = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        return repo, base

    def _head(self, repo, files):
        for rel, text in files.items():
            p = repo / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        subprocess.run(["git", "-C", str(repo), "add", "."],
                       check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm",
                        "head change"], check=True)
        return subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()

    def _entry(self, n, base, head):
        return {"number": n, "author": "SomeSeat", "head_ref": "r",
                "base_sha": base, "head_sha": head}

    def test_inherited_note_not_flagged(self):
        # The L-282 defect: a head inheriting a registered note flagged
        # COLLISION under the whole-tree grep. Diff-vs-base: zero hits.
        import check_sn_claim_coverage as c
        repo, base = self._repo_with_note()
        head = self._head(repo, {"docs/todo.txt": "unrelated\n"})
        by_num = c._collect_head_diff_hits(
            str(repo), [self._entry(1, base, head)], {1: head},
            registry_nums={13})
        self.assertEqual(by_num, {})

    def test_added_note_file_claims_with_attribution(self):
        # A head ADDING a note file is a genuine claim: fires, with the
        # front-matter owner_ib so classify() can attribute it.
        import check_sn_claim_coverage as c
        repo, base = self._repo_with_note()
        head = self._head(repo, {
            "BRAIN/05-MEMORY/SMART-NOTES/2026/10/13/CAT/SN-0799/ib.md":
            "---\nintelligent_block_id: IB-OTHER\n"
            "smart_note_id: SN-0799\n---\nbody\n"})
        by_num = c._collect_head_diff_hits(
            str(repo), [self._entry(2, base, head)], {2: head},
            registry_nums={13})
        self.assertNotIn(13, by_num)
        hits = by_num.get(799, [])
        self.assertTrue(hits, "added note file did not fire")
        self.assertTrue(
            hits[0]["where"].startswith("head diff added path"))
        self.assertEqual(hits[0].get("owner_ib"), "IB-OTHER")

    def test_cross_reference_in_added_content_is_mention(self):
        # A token inside ANOTHER note's added content references the id;
        # it does not claim it (same rule as the commit-graph seam).
        import check_sn_claim_coverage as c
        repo, base = self._repo_with_note()
        head = self._head(repo, {
            "BRAIN/05-MEMORY/SMART-NOTES/2026/10/13/CAT/SN-0013/ib.md":
            "---\nintelligent_block_id: IB-OWN\n"
            "smart_note_id: SN-0013\n---\nbody\nsee also SN-0799\n"})
        by_num = c._collect_head_diff_hits(
            str(repo), [self._entry(3, base, head)], {3: head},
            registry_nums={13})
        hits = by_num.get(799, [])
        self.assertTrue(hits, "cross-reference produced no hit")
        self.assertTrue(
            all(h.get("pre_class") == "mention" for h in hits))

    def test_bold_format_note_cross_reference_is_mention(self):
        # Real note files carry no smart_note_id field (file_sn is None;
        # the id lives in the path and the IB id). A token in another
        # note's added content is still a cross-reference: the path half
        # of the seam rule demotes it.
        import check_sn_claim_coverage as c
        repo = make_repo()
        n = (repo / "BRAIN" / "05-MEMORY" / "SMART-NOTES" / "2026"
             / "10" / "13" / "CAT" / "SN-0032")
        n.mkdir(parents=True)
        (n / "ib.md").write_text(
            "# note\n\n**Intelligent Block:** IB-X-sn0032-x\n\nbody\n")
        subprocess.run(["git", "-C", str(repo), "add", "."],
                       check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm",
                        "register SN-0032"], check=True)
        base = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        (n / "ib.md").write_text(
            "# note\n\n**Intelligent Block:** IB-X-sn0032-x\n\n"
            "body\nsee also SN-0001\n")
        n33 = (repo / "BRAIN" / "05-MEMORY" / "SMART-NOTES" / "2026"
               / "10" / "13" / "CAT" / "SN-0033")
        n33.mkdir(parents=True)
        (n33 / "ib.md").write_text(
            "# new\n\n**Intelligent Block:** IB-X-sn0033-y\n\nbody\n")
        subprocess.run(["git", "-C", str(repo), "add", "."],
                       check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm",
                        "add xref + new note"], check=True)
        head = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        by_num = c._collect_head_diff_hits(
            str(repo), [self._entry(5, base, head)], {5: head},
            registry_nums={32})
        hits = by_num.get(1, [])
        self.assertTrue(hits, "cross-reference produced no hit")
        self.assertTrue(
            all(h.get("pre_class") == "mention" for h in hits),
            f"bold-format xref not demoted: {hits}")
        # ...but a newly ADDED note file's own id stays structural.
        own = by_num.get(33, [])
        own_claims = [h for h in own
                      if h.get("pre_class", "claim") == "claim"]
        self.assertTrue(own_claims, "added-path own-id claim lost")

    def test_note_deletion_not_flagged(self):
        # Deleting a note is not claiming its id.
        import check_sn_claim_coverage as c
        repo, base = self._repo_with_note()
        subprocess.run(
            ["git", "-C", str(repo), "rm", "-q",
             "BRAIN/05-MEMORY/SMART-NOTES/2026/10/13/CAT/SN-0013/ib.md"],
            check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm",
                        "delete note"], check=True)
        head = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        by_num = c._collect_head_diff_hits(
            str(repo), [self._entry(4, base, head)], {4: head},
            registry_nums={13})
        self.assertEqual(by_num, {})

    def test_missing_base_sha_fails_closed(self):
        # An open PR without a diffable base cannot be scanned: the
        # surface errors, never silently skips the PR.
        import check_sn_claim_coverage as c
        with self.assertRaises(RuntimeError):
            c._open_pr_entries([{
                "number": 5, "user": {"login": "S"},
                "head": {"ref": "r", "sha": "a" * 40}, "base": {}}])

    def test_sn_id_field_ignores_mid_prose_quotes(self):
        # B-59 precision: SN_ID_FIELD_RE must resolve the note's OWN id
        # field (front matter at a line start), never a mid-prose QUOTE
        # of another file's id -- the quote defeated the cross-reference
        # demotion on live bytes (SN-0643's Provenance quoting
        # "smart_note_id: SN-0359" set file_sn=359).
        import check_sn_claim_coverage as c
        quote = ("**Provenance:** x declares the same "
                 "`smart_note_id: SN-0359` with a hollow body")
        self.assertIsNone(c.SN_ID_FIELD_RE.search(quote))
        for fm, want in [
                ("---\nsmart_note_id: SN-0013\n---", "13"),
                ("**Smart Note:** SN-0042", "42"),
                ("| Smart Note ID | SN-0077 |", "77"),
                ("  smart_note_id: SN-0099", "99")]:
            m = c.SN_ID_FIELD_RE.search(fm)
            self.assertIsNotNone(m, fm)
            self.assertEqual(m.group(1), want)

    def test_ib_re_ignores_mid_prose_quotes(self):
        # IB_RE precision (wave-35, wave-31's pre-ship routing): the IB id
        # must come from the note's OWN front matter (line start, optional
        # Markdown list marker), never a mid-prose QUOTE of another seat's
        # IB -- a quote misattributes owner_ib, which is fail-OPEN via
        # false self-attribution. 18 real notes at the tip declare via
        # list-item format ("- **Intelligent Block:** IB-..."), so the
        # anchor admits a list marker; a mid-prose quote is never at a
        # line start.
        import check_sn_claim_coverage as c
        quote = ("**Provenance:** this note quotes another file's "
                 "front matter: **Intelligent Block:** IB-FOREIGN-9")
        self.assertIsNone(c.IB_RE.search(quote),
                          "mid-prose IB quote must not attribute")
        inline = ("some intro text intelligent_block_id: IB-INLINE-1 "
                  "trailing text")
        self.assertIsNone(c.IB_RE.search(inline),
                          "mid-line YAML-style field must not attribute")
        for fm, want in [
                ("---\nintelligent_block_id: IB-YAML-1\n---",
                 "IB-YAML-1"),
                ("**Intelligent Block:** IB-BOLD-2", "IB-BOLD-2"),
                ("| Intelligent Block | `IB-TABLE-3` |", "IB-TABLE-3"),
                ("  intelligent_block_id: IB-INDENT-4", "IB-INDENT-4"),
                ("- **Intelligent Block:** IB-LIST-5", "IB-LIST-5"),
                ("* **Intelligent Block:** IB-LIST-6", "IB-LIST-6"),
                ("  - **Intelligent Block:** IB-LIST-7", "IB-LIST-7")]:
            m = c.IB_RE.search(fm)
            self.assertIsNotNone(m, fm)
            self.assertEqual(m.group(1), want)


if __name__ == "__main__":
    unittest.main()
