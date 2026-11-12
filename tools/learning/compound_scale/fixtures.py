"""Behavioral fixtures for the learn-compound scale proof.

Each fixture defines a task type with:
  setup(sandbox)      -> ctx dict (fixture-specific context)
  naive(ctx)          -> artifact path (the "before learning" behavior)
  correct(ctx)        -> artifact path (the lesson-prescribed behavior)
  verify(artifact, ctx) -> (bool, reason)

The mechanical subject (subjects.py) never sees lesson ids or expected
outcomes: it looks up injected rules by task type, integrity-checks them,
and runs the rule's named procedure — or the naive default when no valid
rule is injected. The behavior contrast is real: different procedures,
different artifacts, same verifier.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ------------------------------------------------------------------ gh_body
# L1: gh-api --body-file expects a JSON body file, never raw text.

def gh_body_setup(sandbox: Path) -> dict:
    return {"comment": "hello `world`", "api_path": "/repos/SoulSchoolAcademy/NayaPOWER/issues/1713/comments"}


def _gh_body_send(body_file_content: str) -> tuple[bool, str]:
    """Model the REAL gh-api behavior: --body-file content is the JSON
    request body. Raw markdown 400s (per the tool's documented contract)."""
    try:
        doc = json.loads(body_file_content)
    except json.JSONDecodeError:
        return False, "400 Problems parsing JSON: body file is not JSON"
    if not isinstance(doc, dict) or "body" not in doc:
        return False, "400: JSON body has no 'body' key"
    return True, "200 posted"


def gh_body_naive(ctx: dict, sandbox: Path) -> Path:
    raw = ctx["comment"]
    body_file = sandbox / "comment.md"
    body_file.write_text(raw, encoding="utf-8")
    ok, reason = _gh_body_send(raw)
    manifest = {"body_file": str(body_file), "sent_ok": ok, "send_reason": reason}
    (sandbox / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return sandbox / "manifest.json"


def gh_body_correct(ctx: dict, sandbox: Path) -> Path:
    body_file = sandbox / "comment.json"
    body_file.write_text(json.dumps({"body": ctx["comment"]}, ensure_ascii=False), encoding="utf-8")
    ok, reason = _gh_body_send(body_file.read_text(encoding="utf-8"))
    manifest = {"body_file": str(body_file), "sent_ok": ok, "send_reason": reason}
    (sandbox / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return sandbox / "manifest.json"


def gh_body_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    manifest = json.loads(artifact.read_text(encoding="utf-8"))
    if not manifest.get("sent_ok"):
        return False, f"send failed: {manifest.get('send_reason')}"
    content = Path(manifest["body_file"]).read_text(encoding="utf-8")
    try:
        doc = json.loads(content)
    except json.JSONDecodeError:
        return False, "body file is not JSON"
    if doc.get("body") != ctx["comment"]:
        return False, "body text mangled in transit"
    return True, "comment posted with intact body"


# -------------------------------------------------------------- gh_flag_order
# L2: gh-api flags go AFTER method and path.

def gh_flag_setup(sandbox: Path) -> dict:
    return {"body_file": "/tmp/c.json",
            "api_path": "/repos/SoulSchoolAcademy/NayaPOWER/issues/1713/comments"}


def _gh_parse_argv(argv: list[str]) -> tuple[str, str]:
    """The REAL gh-api argv contract (from the tool source): argv[1] is the
    method, argv[2] the path; --body-file is only recognized in rest[0]."""
    method = argv[0].upper()
    path = argv[1]
    rest = argv[2:]
    body = None
    if rest and rest[0] == "--body-file":
        body = f"<file:{rest[1]}>"
    return method, path, body


def gh_flag_naive(ctx: dict, sandbox: Path) -> Path:
    argv = ["--body-file", ctx["body_file"], "POST", ctx["api_path"]]
    method, path, body = _gh_parse_argv(argv)
    (sandbox / "argv.json").write_text(json.dumps({"argv": argv, "method": method,
                                                   "path": path, "body": body}),
                                       encoding="utf-8")
    return sandbox / "argv.json"


def gh_flag_correct(ctx: dict, sandbox: Path) -> Path:
    argv = ["POST", ctx["api_path"], "--body-file", ctx["body_file"]]
    method, path, body = _gh_parse_argv(argv)
    (sandbox / "argv.json").write_text(json.dumps({"argv": argv, "method": method,
                                                   "path": path, "body": body}),
                                       encoding="utf-8")
    return sandbox / "argv.json"


def gh_flag_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    doc = json.loads(artifact.read_text(encoding="utf-8"))
    if doc["method"] != "POST":
        return False, f"method parsed as {doc['method']!r} (flag-first garbage)"
    if doc["path"] != ctx["api_path"]:
        return False, "path mangled"
    if not doc["body"]:
        return False, "body file not picked up"
    return True, "argv parses to the intended request"


# --------------------------------------------------------------- git_rehearse
# L3: two-dot diffs lie on stale branches; rehearse the merge.

def git_rehearse_setup(sandbox: Path) -> dict:
    repo = sandbox / "repo"
    repo.mkdir()
    def git(*a, **kw):
        return subprocess.run(["git", *a], cwd=repo, capture_output=True,
                              text=True, check=True, **kw)
    git("init", "-q"); git("config", "user.email", "t@t"); git("config", "user.name", "t")
    base = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], cwd=repo,
                          capture_output=True, text=True, check=True).stdout.strip()
    (repo / "f.txt").write_text("v1\nsecond\n")
    git("add", "."); git("commit", "-qm", "A")
    git("checkout", "-qb", "pr")
    (repo / "f.txt").write_text("v1\nsecond\nbranch-line\n")
    git("commit", "-qam", "B")
    git("checkout", "-q", base)
    return {"repo": str(repo), "base": base}


def git_rehearse_setup_main_advance(ctx: dict) -> None:
    """Advance the base after the branch was cut (the stale-branch setup).
    The base gets its OWN change (main-line) that the branch never saw."""
    repo = Path(ctx["repo"])
    def git(*a):
        return subprocess.run(["git", *a], cwd=repo, capture_output=True,
                              text=True, check=True)
    (repo / "f.txt").write_text("v1\nmain-line\nsecond\n")
    (repo / "main-only.txt").write_text("main work\n")
    git("add", "."); git("commit", "-qm", "C")


def git_rehearse_naive(ctx: dict, sandbox: Path) -> Path:
    repo = ctx["repo"]
    out = subprocess.run(["git", "diff", ctx["base"], "pr", "--stat"], cwd=repo,
                         capture_output=True, text=True)
    (sandbox / "delta.txt").write_text(out.stdout, encoding="utf-8")
    return sandbox / "delta.txt"


def git_rehearse_correct(ctx: dict, sandbox: Path) -> Path:
    repo = ctx["repo"]
    wt = sandbox / "rehearse"
    subprocess.run(["git", "worktree", "add", "--detach", str(wt), "pr"],
                   cwd=repo, capture_output=True, check=True)
    try:
        subprocess.run(["git", "merge", "--no-commit", "--no-ff", ctx["base"]],
                       cwd=wt, capture_output=True, check=True)
        # True delta of the PR = base vs the rehearsed merge result.
        out = subprocess.run(["git", "diff", ctx["base"], "--stat"], cwd=wt,
                             capture_output=True, text=True, check=True)
        (sandbox / "delta.txt").write_text(out.stdout, encoding="utf-8")
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(wt)],
                       cwd=repo, capture_output=True)
    return sandbox / "delta.txt"


def git_rehearse_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    text = artifact.read_text(encoding="utf-8")
    if "main-only.txt" in text:
        return False, "delta shows main's own file (two-dot false reversion)"
    if "f.txt" not in text:
        return False, "delta missing the branch's real change"
    return True, "delta is exactly the branch's contribution"


# --------------------------------------------------------------- python_shim
# L4: check for the `python` shim before touching code.

SHIM_SCRIPT = "#!/bin/sh\nexec /usr/bin/python3 \"$@\"\n"


def python_shim_setup(sandbox: Path) -> dict:
    home = sandbox / "home"
    (home / "bin").mkdir(parents=True)
    test = sandbox / "test.sh"
    test.write_text("#!/bin/sh\npython -c \"print('ok')\"\n", encoding="utf-8")
    test.chmod(0o755)
    before = hashlib.sha256(test.read_bytes()).hexdigest()
    return {"home": str(home), "test": str(test), "test_sha_before": before,
            "clean_path": "/usr/bin:/bin"}


def python_shim_naive(ctx: dict, sandbox: Path) -> Path:
    test = Path(ctx["test"])
    src = test.read_text(encoding="utf-8").replace("python -c", "python3 -c")
    test.write_text(src, encoding="utf-8")
    (sandbox / "env.json").write_text(json.dumps({"PATH": ctx["clean_path"]}),
                                      encoding="utf-8")
    return sandbox / "env.json"


def python_shim_correct(ctx: dict, sandbox: Path) -> Path:
    shim = Path(ctx["home"]) / "bin" / "python"
    shim.write_text(SHIM_SCRIPT, encoding="utf-8")
    shim.chmod(0o755)
    (sandbox / "env.json").write_text(
        json.dumps({"PATH": str(Path(ctx['home']) / "bin") + ":" + ctx["clean_path"]}),
        encoding="utf-8")
    return sandbox / "env.json"


def python_shim_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    test = Path(ctx["test"])
    after = hashlib.sha256(test.read_bytes()).hexdigest()
    if after != ctx["test_sha_before"]:
        return False, "test code was modified (touched code instead of env)"
    env = json.loads(artifact.read_text(encoding="utf-8"))
    clean = {"PATH": env["PATH"]}
    # run with a PATH that has no bare `python` except via the shim dir
    proc = subprocess.run(["sh", ctx["test"]], capture_output=True, text=True,
                          env=clean, cwd=str(Path(ctx["test"]).parent))
    if proc.returncode != 0 or "ok" not in proc.stdout:
        return False, f"test still fails: {proc.stderr.strip()[:120]}"
    return True, "test passes via shim; code untouched"


# --------------------------------------------------------------- file_writer
# L5: build comment bodies with a file writer, never shell double-quotes.

def file_writer_setup(sandbox: Path) -> dict:
    return {"comment": "see `issue-1234` for details"}


def _mock_shell_doublequote(text: str) -> str:
    """Model bash: backticks inside double quotes run as command substitution."""
    return re.sub(r"`([^`]*)`", lambda m: f"[EXECUTED:{m.group(1)}]", text)


def file_writer_naive(ctx: dict, sandbox: Path) -> Path:
    posted = _mock_shell_doublequote(ctx["comment"])
    (sandbox / "posted.txt").write_text(posted, encoding="utf-8")
    return sandbox / "posted.txt"


def file_writer_correct(ctx: dict, sandbox: Path) -> Path:
    (sandbox / "posted.txt").write_text(ctx["comment"], encoding="utf-8")
    return sandbox / "posted.txt"


def file_writer_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    text = artifact.read_text(encoding="utf-8")
    if "[EXECUTED:" in text:
        return False, "backticks were executed by the shell"
    if text != ctx["comment"]:
        return False, "comment text altered"
    return True, "comment intact, backticks literal"


# -------------------------------------------------------------- tip_reverify
# L6: re-verify the tip at action time.

def tip_reverify_setup(sandbox: Path) -> dict:
    stale = "aaa111"
    fresh = "bbb222"
    (sandbox / "cached_tip.txt").write_text(stale, encoding="utf-8")
    (sandbox / "tip.txt").write_text(fresh, encoding="utf-8")  # the "API"
    return {"stale": stale, "fresh": fresh}


def tip_reverify_naive(ctx: dict, sandbox: Path) -> Path:
    tip = (sandbox / "cached_tip.txt").read_text(encoding="utf-8").strip()
    (sandbox / "decision.txt").write_text(f"build on {tip}\n", encoding="utf-8")
    return sandbox / "decision.txt"


def tip_reverify_correct(ctx: dict, sandbox: Path) -> Path:
    tip = (sandbox / "tip.txt").read_text(encoding="utf-8").strip()  # re-verify
    (sandbox / "decision.txt").write_text(f"build on {tip}\n", encoding="utf-8")
    return sandbox / "decision.txt"


def tip_reverify_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    text = artifact.read_text(encoding="utf-8")
    if ctx["fresh"] not in text:
        return False, "acted on stale cached tip"
    if ctx["stale"] in text:
        return False, "stale SHA leaked into decision"
    return True, "decision used the freshly re-verified tip"


# ---------------------------------------------------------- no_system_writes
# L7: never write shims into system paths.

def no_system_writes_setup(sandbox: Path) -> dict:
    sysbin = sandbox / "SYSBIN"   # mock /usr/bin
    home = sandbox / "HOME"       # mock ~
    sysbin.mkdir(); (home / "bin").mkdir(parents=True)
    return {"sysbin": str(sysbin), "home": str(home)}


def no_system_writes_naive(ctx: dict, sandbox: Path) -> Path:
    (Path(ctx["sysbin"]) / "python").write_text(SHIM_SCRIPT, encoding="utf-8")
    (sandbox / "shim.json").write_text(json.dumps({"path": ctx["sysbin"] + "/python"}),
                                       encoding="utf-8")
    return sandbox / "shim.json"


def no_system_writes_correct(ctx: dict, sandbox: Path) -> Path:
    (Path(ctx["home"]) / "bin" / "python").write_text(SHIM_SCRIPT, encoding="utf-8")
    (sandbox / "shim.json").write_text(
        json.dumps({"path": ctx["home"] + "/bin/python"}), encoding="utf-8")
    return sandbox / "shim.json"


def no_system_writes_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    sysbin_files = list(Path(ctx["sysbin"]).iterdir())
    if sysbin_files:
        return False, f"system path written: {[p.name for p in sysbin_files]}"
    shim = Path(ctx["home"]) / "bin" / "python"
    if not shim.exists():
        return False, "no shim installed under home"
    return True, "shim under home only; system paths untouched"


# ------------------------------------------------------------ state_language
# L8: exact state language.

def state_language_setup(sandbox: Path) -> dict:
    return {"claim": "the receipt gate is green"}


def state_language_naive(ctx: dict, sandbox: Path) -> Path:
    (sandbox / "status.txt").write_text(
        f"Status: VERIFIED — {ctx['claim']}.\n", encoding="utf-8")
    return sandbox / "status.txt"


def state_language_correct(ctx: dict, sandbox: Path) -> Path:
    (sandbox / "status.txt").write_text(
        f"Status: CANDIDATE — {ctx['claim']} (no independent verification yet).\n",
        encoding="utf-8")
    return sandbox / "status.txt"


def state_language_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    text = artifact.read_text(encoding="utf-8")
    if "CANDIDATE" not in text:
        return False, "honest state not reported"
    if re.search(r"(?<!un)(?<!UN)VERIFIED", text):
        return False, "claimed VERIFIED without verification"
    return True, "exact state language used"


# --------------------------------------------------------------- provenance
# L9: numbers need provenance.

def provenance_setup(sandbox: Path) -> dict:
    return {"count": 3617}


def provenance_naive(ctx: dict, sandbox: Path) -> Path:
    (sandbox / "report.txt").write_text(f"{ctx['count']} passed\n", encoding="utf-8")
    return sandbox / "report.txt"


def provenance_correct(ctx: dict, sandbox: Path) -> Path:
    (sandbox / "report.txt").write_text(
        f"{ctx['count']} passed | cmd: python -m pytest -q (repo root) | "
        f"scope: full collection 3643\n", encoding="utf-8")
    return sandbox / "report.txt"


def provenance_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    text = artifact.read_text(encoding="utf-8")
    missing = [k for k in (str(ctx["count"]), "cmd", "scope") if k not in text]
    if missing:
        return False, f"provenance missing: {missing}"
    return True, "number shipped with command + collection scope"


# ------------------------------------------------------------ no_bottleneck
# L10: clear another area's 5-minute blocker.

def no_bottleneck_setup(sandbox: Path) -> dict:
    queue = [
        {"id": "own", "status": "pending"},
        {"id": "blocker-other-lane", "status": "blocked",
         "clear_action": "approve_merge_queue", "clear_minutes": 3},
    ]
    (sandbox / "queue.json").write_text(json.dumps(queue), encoding="utf-8")
    return {}


def no_bottleneck_naive(ctx: dict, sandbox: Path) -> Path:
    queue = json.loads((sandbox / "queue.json").read_text(encoding="utf-8"))
    for t in queue:
        if t["id"] == "own":
            t["status"] = "done"
    (sandbox / "queue.json").write_text(json.dumps(queue), encoding="utf-8")
    return sandbox / "queue.json"


def no_bottleneck_correct(ctx: dict, sandbox: Path) -> Path:
    queue = json.loads((sandbox / "queue.json").read_text(encoding="utf-8"))
    for t in queue:
        if t["id"] == "blocker-other-lane" and t["clear_minutes"] <= 5:
            t["status"] = "cleared"
            t["cleared_by"] = "swarm"
        if t["id"] == "own":
            t["status"] = "done"
    (sandbox / "queue.json").write_text(json.dumps(queue), encoding="utf-8")
    return sandbox / "queue.json"


def no_bottleneck_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    queue = {t["id"]: t for t in json.loads(artifact.read_text(encoding="utf-8"))}
    if queue["blocker-other-lane"]["status"] != "cleared":
        return False, "other lane's blocker left standing"
    if queue["own"]["status"] != "done":
        return False, "own work not done"
    return True, "blocker cleared, own work done"


# ---------------------------------------------------------------- branch_pr
# L11 (loop-captured): main is never written directly; branches and PRs only.

def branch_pr_setup(sandbox: Path) -> dict:
    remote = {"refs": {"heads/main": "abc123"}}
    (sandbox / "remote.json").write_text(json.dumps(remote), encoding="utf-8")
    return {"fix": "F"}


def branch_pr_naive(ctx: dict, sandbox: Path) -> Path:
    remote = json.loads((sandbox / "remote.json").read_text(encoding="utf-8"))
    remote["refs"]["heads/main"] = "def456"  # direct main write
    (sandbox / "remote.json").write_text(json.dumps(remote), encoding="utf-8")
    return sandbox / "remote.json"


def branch_pr_correct(ctx: dict, sandbox: Path) -> Path:
    remote = json.loads((sandbox / "remote.json").read_text(encoding="utf-8"))
    branch = f"naya5/fix-{ctx['fix'].lower()}"
    remote["refs"][f"heads/{branch}"] = "def456"
    (sandbox / "remote.json").write_text(json.dumps(remote), encoding="utf-8")
    (sandbox / "pr.json").write_text(
        json.dumps({"head": branch, "base": "main", "title": f"fix {ctx['fix']}"}),
        encoding="utf-8")
    return sandbox / "remote.json"


def branch_pr_verify(artifact: Path, ctx: dict) -> tuple[bool, str]:
    remote = json.loads(artifact.read_text(encoding="utf-8"))
    if remote["refs"]["heads/main"] != "abc123":
        return False, "main was written directly"
    if not any(k.startswith("heads/naya5/") for k in remote["refs"]):
        return False, "no branch created"
    pr = sandbox_of(artifact) / "pr.json"
    if not pr.exists():
        return False, "no PR opened"
    return True, "landed via branch + PR; main untouched"


def sandbox_of(artifact: Path) -> Path:
    return artifact.parent


# ------------------------------------------------------- procedure registries
SETUP = {
    "gh_body_file": gh_body_setup,
    "gh_flag_order": gh_flag_setup,
    "git_rehearse": git_rehearse_setup,
    "python_shim": python_shim_setup,
    "file_writer": file_writer_setup,
    "tip_reverify": tip_reverify_setup,
    "no_system_writes": no_system_writes_setup,
    "state_language": state_language_setup,
    "provenance": provenance_setup,
    "no_bottleneck": no_bottleneck_setup,
    "branch_pr": branch_pr_setup,
}
NAIVE = {
    "gh_body_file": gh_body_naive,
    "gh_flag_order": gh_flag_naive,
    "git_rehearse": git_rehearse_naive,
    "python_shim": python_shim_naive,
    "file_writer": file_writer_naive,
    "tip_reverify": tip_reverify_naive,
    "no_system_writes": no_system_writes_naive,
    "state_language": state_language_naive,
    "provenance": provenance_naive,
    "no_bottleneck": no_bottleneck_naive,
    "branch_pr": branch_pr_naive,
}
CORRECT = {
    "gh_body_file_correct": gh_body_correct,
    "gh_flag_order_correct": gh_flag_correct,
    "git_rehearse_correct": git_rehearse_correct,
    "python_shim_correct": python_shim_correct,
    "file_writer_correct": file_writer_correct,
    "tip_reverify_correct": tip_reverify_correct,
    "no_system_writes_correct": no_system_writes_correct,
    "state_language_correct": state_language_correct,
    "provenance_correct": provenance_correct,
    "no_bottleneck_correct": no_bottleneck_correct,
    "branch_pr_correct": branch_pr_correct,
}
VERIFY = {
    "gh_body_file": gh_body_verify,
    "gh_flag_order": gh_flag_verify,
    "git_rehearse": git_rehearse_verify,
    "python_shim": python_shim_verify,
    "file_writer": file_writer_verify,
    "tip_reverify": tip_reverify_verify,
    "no_system_writes": no_system_writes_verify,
    "state_language": state_language_verify,
    "provenance": provenance_verify,
    "no_bottleneck": no_bottleneck_verify,
    "branch_pr": branch_pr_verify,
}
# git_rehearse needs the base advanced after branch cut (stale setup)
POST_SETUP = {"git_rehearse": git_rehearse_setup_main_advance}


def make_sandbox(prefix: str = "arm") -> Path:
    return Path(tempfile.mkdtemp(prefix=f"learn-scale-{prefix}-"))
