#!/usr/bin/env python3
"""Tests for tools/post_merge_guardian.py — the house-fire loop.

Negative controls are the point: a synthetic bad landing (blob drift,
a resurrected deletion, an orphaned merge, a new red, a dead Hub
surface) MUST trip detection and produce a prepared revert; a healthy
landing MUST pass silently. If the guardian were mutated to always
return OK, every ESCAPE test below would fail — the suite is the
sabotage battery, not a rehearsal of the happy path.

Git fixtures are real repositories built with plumbing + porcelain;
GitHub is a fake client with the same surface as GHClient. No network.
"""

import base64
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import post_merge_guardian as g
from post_merge_guardian import ApiError

REPO = "SoulSchoolAcademy/NayaPOWER"


# ------------------------------------------------------------- git fixture

def git(repo, *args, env=None, check=True):
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    proc = subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, env=full_env)
    if check and proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc


def write(repo, path, content):
    full = os.path.join(str(repo), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def build_base(path):
    """Repo with main@B: a.txt=v1, gone.txt, HUB/app/index.html (feed)."""
    os.makedirs(path, exist_ok=True)
    git(path, "init", "-b", "main", ".")
    git(path, "config", "user.email", "guardian-test@example.invalid")
    git(path, "config", "user.name", "Guardian Test")
    git(path, "config", "commit.gpgsign", "false")
    write(path, "a.txt", "v1\n")
    write(path, "gone.txt", "here\n")
    write(path, "HUB/app/index.html", "<html>feed OFFICIAL_NOTES v1</html>\n")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "base")
    return git(path, "rev-parse", "HEAD").stdout.strip()


def add_feature(path, base, changes, branch="feature"):
    """Branch from base, apply {path: content|None(delete)}, commit -> head."""
    git(path, "checkout", "-q", "-b", branch, base)
    for p, content in changes.items():
        if content is None:
            git(path, "rm", "-q", p)
        else:
            write(path, p, content)
            git(path, "add", p)
    git(path, "commit", "-q", "-m", f"feature {branch}")
    head = git(path, "rev-parse", "HEAD").stdout.strip()
    git(path, "checkout", "-q", "main")
    return head


def merge(path, head, msg="Merge PR #42"):
    git(path, "checkout", "-q", "main")
    git(path, "merge", "-q", "--no-ff", head, "-m", msg)
    return git(path, "rev-parse", "HEAD").stdout.strip()


def craft_merge(path, base, head, tree_ref, overrides, msg="Merge PR #42 (#42)"):
    """A merge commit with parents [base, head] but an arbitrary tree —
    the phantom-merge shape verify_gitdata_merge_tree.py exists to refuse."""
    idx = os.path.join(str(path), "craft-index")
    env = {"GIT_INDEX_FILE": idx}
    git(path, "read-tree", tree_ref, env=env)
    for p, content in overrides.items():
        blob = subprocess.run(["git", "-C", str(path), "hash-object", "-w", "--stdin"],
                              input=content, capture_output=True, text=True,
                              check=True).stdout.strip()
        git(path, "update-index", "--cacheinfo", f"100644,{blob},{p}", env=env)
    tree = git(path, "write-tree", env=env).stdout.strip()
    merge_sha = git(path, "commit-tree", tree, "-p", base, "-p", head,
                    "-m", msg).stdout.strip()
    git(path, "update-ref", "refs/heads/main", merge_sha)
    if os.path.exists(idx):
        os.remove(idx)
    return merge_sha


# ------------------------------------------------------------ fake client

def make_pr(number, head_sha, head_ref="feature", labels=None, title="Change A"):
    return {
        "number": number, "title": title, "state": "closed",
        "merged_at": "2026-10-21T22:00:00Z",
        "html_url": f"https://github.com/{REPO}/pull/{number}",
        "head": {"sha": head_sha, "ref": head_ref},
        "labels": [{"name": n} for n in (labels or [])],
    }


def run(name, conclusion, status="completed", started="2026-10-21T22:00:00Z", rid=1):
    return {"name": name, "status": status, "conclusion": conclusion,
            "started_at": started, "id": rid}


class FakeClient:
    def __init__(self, main_ref):
        self.main_ref = main_ref
        self.compare = {}
        self.pulls_by_commit = {}
        self.pr_files = {}
        self.check_runs = {}
        self.comments = []       # (issue, body)
        self.created_pulls = []  # bodies
        self.patches = []
        self.log_ref = None
        self.log_content = None
        self._last_blob = None

    def set_push(self, before, after, commits, files):
        self.compare[(before, after)] = {
            "commits": [{"sha": s} for s in commits],
            "files": [{"filename": f} for f in files],
        }

    # -- reads
    def get(self, path):
        if path.startswith("/compare/"):
            b, a = path[len("/compare/"):].split("...")
            return self.compare[(b, a)]
        if path.startswith("/commits/") and path.endswith("/pulls"):
            return self.pulls_by_commit.get(path.split("/")[2], [])
        if path.startswith("/pulls/") and "/files?" in path:
            return self.pr_files.get(int(path.split("/")[2]), [])
        if path == "/git/refs/heads/main":
            return {"object": {"sha": self.main_ref}}
        if path == "/git/refs/heads/live/guardian-log":
            if self.log_ref is None:
                raise ApiError(404, path)
            return {"object": {"sha": self.log_ref}}
        if path.startswith("/git/commits/"):
            return {"tree": {"sha": "tree-of-" + path.split("/")[3][:8]}}
        if path.startswith("/contents/guardian-log.jsonl"):
            if self.log_content is None:
                raise ApiError(404, path)
            return {"content": base64.b64encode(self.log_content.encode()).decode()}
        raise AssertionError(f"FakeClient: unrouted GET {path}")

    def get_all(self, path, key):
        if "check-runs" in path:
            return list(self.check_runs.get(path.split("/")[2], []))
        raise AssertionError(f"FakeClient: unrouted get_all {path}")

    # -- writes
    def post(self, path, body):
        if path == "/pulls":
            self.created_pulls.append(body)
            return {"number": 9001,
                    "html_url": f"https://github.com/{REPO}/pull/9001"}
        if path.startswith("/issues/") and path.endswith("/comments"):
            self.comments.append((int(path.split("/")[2]), body["body"]))
            return {"id": 1}
        if path.startswith("/issues/") and path.endswith("/labels"):
            return {}
        if path == "/labels":
            return {}
        if path == "/git/blobs":
            self._last_blob = base64.b64decode(body["content"]).decode()
            return {"sha": "blob-new"}
        if path == "/git/trees":
            return {"sha": "tree-new"}
        if path == "/git/commits":
            return {"sha": "commit-new"}
        if path == "/git/refs":
            self.log_ref = body["sha"]
            return {}
        raise AssertionError(f"FakeClient: unrouted POST {path}")

    def patch(self, path, body):
        self.patches.append((path, body))
        if path == "/git/refs/heads/live/guardian-log":
            self.log_content = self._last_blob
            self.log_ref = body["sha"]
        return {}


class Effects:
    """Injectable pusher / pr_opener recording what the guardian did."""
    def __init__(self):
        self.pushes = []
        self.opened = []

    def pusher(self, wt, branch):
        self.pushes.append(branch)

    def opener(self, branch, landing, body):
        self.opened.append({"branch": branch, "body": body})
        return {"revert_pr": 9001,
                "revert_pr_url": f"https://github.com/{REPO}/pull/9001"}


def ok_checks(*shas):
    return {s: [run("test", "success")] for s in shas}


def run_guardian(fake, repo, before, after, fx=None, **kw):
    fx = fx or Effects()
    sink = g.ListSink()
    kw.setdefault("sinks", [sink])
    kw.setdefault("pusher", fx.pusher)
    kw.setdefault("pr_opener", fx.opener)
    kw.setdefault("fetcher", lambda url: (200, "OFFICIAL_NOTES"))
    records, code = g.run_guardian(fake, str(repo), before, after, **kw)
    return records, code, sink, fx


def healthy_repo(tmp_path):
    repo = tmp_path / "repo"
    base = build_base(repo)
    head = add_feature(repo, base, {"a.txt": "v2\n"})
    m = merge(repo, head)
    return repo, base, head, m


def wire_pr(fake, m, head, files, number=42, **prkw):
    fake.pulls_by_commit[m] = [make_pr(number, head, **prkw)]
    fake.pr_files[number] = [{"filename": f, "status": "modified"} for f in files]


# ------------------------------------------------------------------ tests

def test_healthy_merge_ok_and_silent(tmp_path):
    repo, base, head, m = healthy_repo(tmp_path)
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, head, ["a.txt"])
    fake.check_runs = ok_checks(base, m)

    def no_fetch(url):
        raise AssertionError("surface must not be probed for non-Hub landings")
    records, code, sink, fx = run_guardian(fake, repo, base, m, fetcher=no_fetch)
    assert code == 0
    assert len(records) == 1 and records[0]["verdict"] == "OK"
    assert records[0]["defect_classes"] == []
    assert records[0]["cure"] is None
    assert records[0]["detection_latency_s"] is not None
    assert fake.comments == [] and fx.pushes == [] and fx.opened == []
    assert sink.records == records


def test_blob_drift_escape_and_revert_prepared(tmp_path):
    repo = tmp_path / "repo"
    base = build_base(repo)
    head = add_feature(repo, base, {"a.txt": "v2\n"})
    # Phantom merge: parents are right, but a.txt landed as neither v1 nor v2.
    m = craft_merge(repo, base, head, base, {"a.txt": "vX-drifted\n"})
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, head, ["a.txt"])
    fake.check_runs = ok_checks(base, m)

    records, code, sink, fx = run_guardian(fake, repo, base, m)
    assert code == 1
    rec = records[0]
    assert rec["verdict"] == "ESCAPE"
    assert rec["defect_classes"] == ["FAITHFULNESS_BLOB_DRIFT"]
    # the revert was really built: its tree restores a.txt to the base bytes
    cure = rec["cure"]
    assert cure["prepared"] is True and cure["revert_pr"] == 9001
    assert fx.pushes == [f"guardian/revert-{m[:10]}"]
    assert g.git_blob_at(str(repo), cure["revert_sha"], "a.txt") == \
        g.git_blob_at(str(repo), base, "a.txt")
    # alarm + evidence in one motion, naming the defect and the revert
    assert len(fake.comments) == 1
    issue, body = fake.comments[0]
    assert issue == 2793 and "FAITHFULNESS_BLOB_DRIFT" in body
    assert "/pull/9001" in body
    assert "FAITHFULNESS_BLOB_DRIFT" in fx.opened[0]["body"]


def test_not_ancestor_escape(tmp_path):
    repo, base, head, m = healthy_repo(tmp_path)
    # History rewritten: the tip no longer contains the merge commit.
    tree = git(repo, "rev-parse", f"{base}^{{tree}}").stdout.strip()
    orphan = git(repo, "commit-tree", tree, "-m", "rewritten tip").stdout.strip()
    fake = FakeClient(main_ref=orphan)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, head, ["a.txt"])
    fake.check_runs = ok_checks(base, m)
    records, code, sink, fx = run_guardian(fake, repo, base, m)
    assert code == 1
    assert records[0]["verdict"] == "ESCAPE"
    assert records[0]["defect_classes"] == ["FAITHFULNESS_NOT_ANCESTOR"]


def test_inherited_red_not_charged(tmp_path):
    repo, base, head, m = healthy_repo(tmp_path)
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, head, ["a.txt"])
    # The same red on both sides of the push is the tip's own, inherited.
    fake.check_runs = {base: [run("test", "failure")], m: [run("test", "failure")]}
    records, code, sink, fx = run_guardian(fake, repo, base, m)
    assert code == 0 and records[0]["verdict"] == "OK"
    assert records[0]["checks"]["new_reds"] == []


def test_new_red_escape(tmp_path):
    repo, base, head, m = healthy_repo(tmp_path)
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, head, ["a.txt"])
    fake.check_runs = {base: [run("test", "success")], m: [run("test", "failure")]}
    records, code, sink, fx = run_guardian(fake, repo, base, m)
    assert code == 1
    rec = records[0]
    assert rec["verdict"] == "ESCAPE" and rec["defect_classes"] == ["NEW_RED"]
    assert rec["checks"]["new_reds"] == ["test"]
    assert rec["cure"]["prepared"] is True
    assert "NEW_RED" in fake.comments[0][1]


def test_hub_surface_down_escape(tmp_path):
    repo = tmp_path / "repo"
    base = build_base(repo)
    head = add_feature(repo, base, {
        "a.txt": "v2\n",
        "HUB/app/index.html": "<html>feed OFFICIAL_NOTES v2</html>\n",
    })
    m = merge(repo, head)
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt", "HUB/app/index.html"])
    wire_pr(fake, m, head, ["a.txt", "HUB/app/index.html"])
    fake.check_runs = ok_checks(base, m)
    records, code, sink, fx = run_guardian(
        fake, repo, base, m, fetcher=lambda url: (500, ""))
    assert code == 1
    assert records[0]["defect_classes"] == ["SURFACE_DOWN"]


def test_hub_surface_ok(tmp_path):
    repo = tmp_path / "repo"
    base = build_base(repo)
    head = add_feature(repo, base, {
        "HUB/app/index.html": "<html>feed OFFICIAL_NOTES v2</html>\n"})
    m = merge(repo, head)
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["HUB/app/index.html"])
    wire_pr(fake, m, head, ["HUB/app/index.html"])
    fake.check_runs = ok_checks(base, m)
    records, code, sink, fx = run_guardian(
        fake, repo, base, m, fetcher=lambda url: (200, "x OFFICIAL_NOTES y"))
    assert code == 0 and records[0]["verdict"] == "OK"


def test_revert_landing_alarms_only_never_reverted(tmp_path):
    repo = tmp_path / "repo"
    base = build_base(repo)
    head = add_feature(repo, base, {"a.txt": "v2\n"}, branch="guardian/revert-deadbeef")
    m = craft_merge(repo, base, head, base, {"a.txt": "vX-drifted\n"})
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, head, ["a.txt"], number=43,
            labels=["GUARDIAN-REVERT"], head_ref="guardian/revert-deadbeef")
    fake.check_runs = ok_checks(base, m)
    records, code, sink, fx = run_guardian(fake, repo, base, m)
    rec = records[0]
    assert code == 1 and rec["verdict"] == "ESCAPE_ON_REVERT"
    assert rec["cure"] is None
    assert fx.pushes == [] and fx.opened == []          # no loop, ever
    assert len(fake.comments) == 1                       # but never silent
    assert "GUARDIAN-REVERT" in fake.comments[0][1]


def test_pending_checks_recorded_not_charged(tmp_path):
    repo, base, head, m = healthy_repo(tmp_path)
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, head, ["a.txt"])
    fake.check_runs = {
        base: [run("test", "success")],
        m: [run("test", "success"),
            run("promote-and-prove", None, status="in_progress", rid=2)],
    }
    records, code, sink, fx = run_guardian(fake, repo, base, m, wait_secs=0)
    rec = records[0]
    assert code == 0 and rec["verdict"] == "PENDING"
    assert rec["checks"]["pending_after"] == ["promote-and-prove"]
    assert fake.comments == []


def test_direct_push_healthy_ok(tmp_path):
    repo = tmp_path / "repo"
    base = build_base(repo)
    write(repo, "a.txt", "v3-door\n")
    git(repo, "add", "a.txt")
    git(repo, "commit", "-q", "-m", "door landing")
    d = git(repo, "rev-parse", "HEAD").stdout.strip()
    fake = FakeClient(main_ref=d)
    fake.set_push(base, d, [d], ["a.txt"])
    fake.check_runs = ok_checks(base, d)
    records, code, sink, fx = run_guardian(fake, repo, base, d)
    assert code == 0
    assert records[0]["kind"] == "DIRECT_PUSH" and records[0]["verdict"] == "OK"


def test_deleted_file_resurrected_is_drift(tmp_path):
    repo = tmp_path / "repo"
    base = build_base(repo)
    head = add_feature(repo, base, {"gone.txt": None})
    # The merge tree still carries gone.txt — the deletion never landed.
    m = craft_merge(repo, base, head, base, {})
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["gone.txt"])
    fake.pulls_by_commit[m] = [make_pr(42, head)]
    fake.pr_files[42] = [{"filename": "gone.txt", "status": "removed"}]
    fake.check_runs = ok_checks(base, m)
    records, code, sink, fx = run_guardian(fake, repo, base, m)
    assert code == 1
    rec = records[0]
    assert rec["defect_classes"] == ["FAITHFULNESS_BLOB_DRIFT"]
    assert rec["defects"][0]["path"] == "gone.txt"


def test_unfetchable_head_is_pending_never_ok(tmp_path):
    """A PR head missing from the object store must not wear an OK:
    the blob check was skipped, so the verdict is PENDING with the
    unverifiable reason on the record — no alarm, no silent pass."""
    repo, base, head, m = healthy_repo(tmp_path)
    fake = FakeClient(main_ref=m)
    fake.set_push(base, m, [m], ["a.txt"])
    wire_pr(fake, m, "f" * 40, ["a.txt"])  # head object does not exist
    fake.check_runs = ok_checks(base, m)
    records, code, sink, fx = run_guardian(fake, repo, base, m)
    rec = records[0]
    assert code == 0 and rec["verdict"] == "PENDING"
    assert rec["defect_classes"] == ["FAITHFULNESS_UNVERIFIABLE"]
    assert fake.comments == [] and fx.opened == []


def test_check_sets_latest_per_name_wins():
    fake = FakeClient(main_ref="x")
    fake.check_runs = {"sha1": [
        run("test", "failure", started="2026-10-21T22:00:00Z", rid=1),
        run("test", "success", started="2026-10-21T22:05:00Z", rid=2),
    ]}
    failing, pending, completed = g.check_sets(fake, "sha1")
    assert failing == set() and completed == {"test"}
    fake.check_runs = {"sha1": [
        run("test", "success", started="2026-10-21T22:00:00Z", rid=1),
        run("test", "failure", started="2026-10-21T22:05:00Z", rid=2),
    ]}
    failing, pending, completed = g.check_sets(fake, "sha1")
    assert failing == {"test"}


def test_gitdata_log_sink_roundtrip():
    fake = FakeClient(main_ref="maintip")
    sink = g.GitDataLogSink(fake)
    sink.append([{"v": 1, "verdict": "OK"}])
    lines = [json.loads(l) for l in fake.log_content.splitlines()]
    assert lines == [{"v": 1, "verdict": "OK"}]
    sink.append([{"v": 1, "verdict": "ESCAPE"}])
    lines = [json.loads(l) for l in fake.log_content.splitlines()]
    assert lines == [{"v": 1, "verdict": "OK"}, {"v": 1, "verdict": "ESCAPE"}]
    assert any(p == "/git/refs/heads/live/guardian-log" for p, _ in fake.patches)
