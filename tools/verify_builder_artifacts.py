#!/usr/bin/env python3
"""Verify builder artifacts — never trust completion summaries.

Machine form of the standing lesson (AGENTS.md, 2026-09-30): "A subagent's
'done' report is not evidence the artifact exists. ... Before accepting any
delegated completion: check the artifact handle directly (branch/PR/commit/
file) via the relevant read tool."

Given a claimed-artifact receipt (JSON), this tool resolves EVERY handle
against the LIVE remote — never the claimer's word — and verdicts each:

  file    path exists as a blob in <ref>'s tree; optional sha256 / min_bytes pin
  branch  refs/heads/<name> exists on origin (reports its SHA)
  commit  <sha> is a commit object; optional ancestor_of pin
  pr      PR number exists via the GitHub API; optional head / state pin

Receipt schema (JSON file):
  {"artifacts": [
     {"kind": "file", "path": "tools/x.py", "ref": "main",
      "sha256": "<64hex>", "min_bytes": 1},
     {"kind": "branch", "name": "naya4/my-branch"},
     {"kind": "commit", "sha": "<40hex>", "ancestor_of": "main"},
     {"kind": "pr", "number": 1759, "head": "<40hex>", "state": "closed"}
  ]}

Exit codes: 0 = every artifact verified; 1 = at least one phantom
(claimed-but-missing); 2 = usage or environment error. Fail-closed: any
unresolvable handle is a FAIL, never a pass. Stdlib only.

The fetch cache is ephemeral scratch (recreated every run); the printed
verdicts are the evidence, not the cache.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_REPO = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"

# Candidate gh-api CLIs: the skill's canonical path first, then the legacy lane path.
GH_API_CANDIDATES = (
    Path.home() / "workspace/skills/github/bin/gh-api",
    Path.home() / "workspace/naya/bin/gh-api",
)

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA64 = re.compile(r"^[0-9a-f]{64}$")


class EnvError(Exception):
    """The verification environment cannot do its job (missing git/gh-api)."""


@dataclass
class Verdict:
    kind: str
    label: str
    ok: bool
    detail: str

    def as_dict(self):
        return {
            "kind": self.kind,
            "artifact": self.label,
            "verdict": "PASS" if self.ok else "FAIL",
            "detail": self.detail,
        }


def _run(cmd, cwd=None, input_bytes=None, timeout=120):
    """Run a command; return (returncode, stdout, stderr) as text."""
    try:
        p = subprocess.run(
            cmd,
            cwd=cwd,
            input=input_bytes,
            capture_output=True,
            timeout=timeout,
        )
    except FileNotFoundError as e:
        raise EnvError(f"required executable missing: {e.filename}")
    except subprocess.TimeoutExpired:
        raise EnvError(f"command timed out: {' '.join(cmd[:3])}...")
    return (
        p.returncode,
        p.stdout.decode("utf-8", "replace"),
        p.stderr.decode("utf-8", "replace"),
    )


class GitRemote:
    """Read-only resolver against a git remote. Never trusts local state."""

    def __init__(self, repo_url):
        if shutil.which("git") is None:
            raise EnvError("git not found on PATH")
        self.repo_url = repo_url
        # Ephemeral scratch: recreated every run; verdicts are the evidence.
        self._work = Path(tempfile.mkdtemp(prefix="vba-git-"))
        rc, _, _ = _run(["git", "init", "-q"], cwd=str(self._work))
        if rc != 0:
            raise EnvError("git init failed in scratch dir")
        self._fetched = set()

    def close(self):
        shutil.rmtree(self._work, ignore_errors=True)

    def branch_sha(self, name):
        """Resolve refs/heads/<name> on the remote. Returns SHA or None."""
        rc, out, _ = _run(
            ["git", "ls-remote", self.repo_url, f"refs/heads/{name}"]
        )
        if rc != 0:
            return None
        for line in out.splitlines():
            sha, ref = line.split("\t", 1)
            if ref == f"refs/heads/{name}":
                return sha
        return None

    def _fetch_sha(self, sha):
        if sha in self._fetched:
            return True
        rc, _, _ = _run(
            ["git", "fetch", "-q", "--depth", "1", self.repo_url, sha],
            cwd=str(self._work),
        )
        if rc == 0:
            self._fetched.add(sha)
        return rc == 0

    def _resolve_ref(self, ref):
        """A ref may be a branch name or a raw 40-hex SHA."""
        if _SHA40.match(ref or ""):
            return ref
        sha = self.branch_sha(ref)
        return sha

    def object_type(self, sha):
        """Type of <sha> on the remote, fetched by SHA. None if unresolvable."""
        if not _SHA40.match(sha or ""):
            return None
        if not self._fetch_sha(sha):
            return None
        rc, out, _ = _run(["git", "cat-file", "-t", sha], cwd=str(self._work))
        if rc != 0:
            return None
        return out.strip()

    def file_blob(self, ref, path):
        """(blob_sha, size) for path in ref's tree; None if absent."""
        tip = self._resolve_ref(ref)
        if not tip:
            return None
        if not self._fetch_sha(tip):
            return None
        rc, out, _ = _run(
            ["git", "ls-tree", tip, "--", path], cwd=str(self._work)
        )
        if rc != 0:
            return None
        for line in out.splitlines():
            parts = line.split()
            # "<mode> <type> <sha>\t<path>"
            if len(parts) >= 4 and parts[1] == "blob" and line.rsplit("\t", 1)[-1] == path:
                blob = parts[2]
                rc2, size_out, _ = _run(
                    ["git", "cat-file", "-s", blob], cwd=str(self._work)
                )
                size = int(size_out.strip()) if rc2 == 0 else -1
                return (blob, size)
        return None

    def blob_sha256(self, blob_sha):
        rc, out, _ = _run(
            ["git", "cat-file", "blob", blob_sha], cwd=str(self._work)
        )
        if rc != 0:
            return None
        # Stream-safe: cat-file already returned bytes via text decode; for
        # binary blobs recompute from raw.
        p = subprocess.run(
            ["git", "cat-file", "blob", blob_sha],
            cwd=str(self._work),
            capture_output=True,
        )
        return hashlib.sha256(p.stdout).hexdigest()

    def is_ancestor(self, ancestor, descendant_ref):
        tip = self._resolve_ref(descendant_ref)
        if not tip or not _SHA40.match(ancestor):
            return False
        if not self._fetch_sha(tip):
            return False
        # Fetch the ancestor too so merge-base has both objects.
        self._fetch_sha(ancestor)
        rc, _, _ = _run(
            ["git", "merge-base", "--is-ancestor", ancestor, tip],
            cwd=str(self._work),
        )
        return rc == 0


def find_gh_api():
    for cand in GH_API_CANDIDATES:
        if cand.is_file() and os.access(cand, os.X_OK):
            return str(cand)
    return None


def gh_api_get(gh_api, api_path):
    rc, out, err = _run([gh_api, "GET", api_path])
    if rc != 0:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def verify_artifact(art, git, gh_api, default_ref):
    kind = art.get("kind")
    if kind == "file":
        path = art.get("path", "")
        ref = art.get("ref", default_ref)
        label = f"file {path} @ {ref}"
        if not path or path.startswith("/") or ".." in Path(path).parts:
            return Verdict(kind, label, False, "invalid path (absolute or escapes)")
        blob = git.file_blob(ref, path)
        if blob is None:
            return Verdict(kind, label, False, "not in remote tree — PHANTOM")
        blob_sha, size = blob
        want_hash = art.get("sha256")
        if want_hash:
            if not _SHA64.match(want_hash):
                return Verdict(kind, label, False, "malformed sha256 pin")
            got = git.blob_sha256(blob_sha)
            if got != want_hash:
                return Verdict(
                    kind, label, False,
                    f"sha256 mismatch: remote blob is {got[:12]}..., claim pins {want_hash[:12]}...",
                )
        min_bytes = art.get("min_bytes")
        if min_bytes is not None and size < int(min_bytes):
            return Verdict(
                kind, label, False,
                f"too small: {size} bytes < min_bytes {min_bytes}",
            )
        detail = f"blob {blob_sha[:12]}, {size} bytes" + (
            ", sha256 OK" if want_hash else ""
        )
        return Verdict(kind, label, True, detail)

    if kind == "branch":
        name = art.get("name", "")
        label = f"branch {name}"
        sha = git.branch_sha(name)
        if not sha:
            return Verdict(kind, label, False, "no such ref on origin — PHANTOM")
        return Verdict(kind, label, True, f"origin SHA {sha[:12]}")

    if kind == "commit":
        sha = art.get("sha", "")
        label = f"commit {sha[:12]}"
        if not _SHA40.match(sha):
            return Verdict(kind, label, False, "malformed SHA")
        otype = git.object_type(sha)
        if otype != "commit":
            return Verdict(
                kind, label, False,
                f"not a commit object on remote ({otype or 'missing'}) — PHANTOM",
            )
        ancestor_of = art.get("ancestor_of")
        if ancestor_of and not git.is_ancestor(sha, ancestor_of):
            return Verdict(
                kind, label, False,
                f"not an ancestor of {ancestor_of}",
            )
        return Verdict(kind, label, True, "commit object exists on remote")

    if kind == "pr":
        number = art.get("number")
        label = f"PR #{number}"
        if not isinstance(number, int) or number <= 0:
            return Verdict(kind, label, False, "invalid PR number")
        if gh_api is None:
            raise EnvError("a pr claim requires gh-api, none found")
        pr = gh_api_get(gh_api, f"/repos/SoulSchoolAcademy/NayaPOWER/pulls/{number}")
        if not pr or pr.get("number") != number:
            return Verdict(kind, label, False, "PR not found — PHANTOM")
        want_head = art.get("head")
        if want_head:
            if not _SHA40.match(want_head):
                return Verdict(kind, label, False, "malformed head pin")
            if (pr.get("head") or {}).get("sha") != want_head:
                return Verdict(
                    kind, label, False,
                    f"head is {(pr.get('head') or {}).get('sha', '')[:12]}, claim pins {want_head[:12]}",
                )
        want_state = art.get("state")
        if want_state and pr.get("state") != want_state:
            return Verdict(
                kind, label, False,
                f"state is {pr.get('state')}, claim pins {want_state}",
            )
        merged = bool(pr.get("merged_at"))
        return Verdict(
            kind, label, True,
            f"exists, state={pr.get('state')}, merged={merged}, head={((pr.get('head') or {}).get('sha') or '')[:12]}",
        )

    return Verdict(str(kind), str(art), False, f"unknown kind {kind!r}")


def verify_receipt(receipt, repo_url, default_ref):
    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise EnvError("receipt must contain a non-empty 'artifacts' list")
    needs_gh = any(a.get("kind") == "pr" for a in artifacts)
    gh_api = find_gh_api() if needs_gh else None
    if needs_gh and gh_api is None:
        raise EnvError(
            "receipt claims a PR but no gh-api CLI found "
            f"(looked at {', '.join(str(c) for c in GH_API_CANDIDATES)})"
        )
    git = GitRemote(repo_url)
    try:
        return [verify_artifact(a, git, gh_api, default_ref) for a in artifacts]
    finally:
        git.close()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Verify claimed builder artifacts against the live remote."
    )
    ap.add_argument("receipt", help="JSON file with {\"artifacts\": [...]}")
    ap.add_argument("--repo", default=DEFAULT_REPO,
                    help="git remote URL or local path (default: NayaPOWER)")
    ap.add_argument("--ref", default="main",
                    help="default ref for artifacts without their own")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    args = ap.parse_args(argv)

    try:
        receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read receipt: {e}", file=sys.stderr)
        return 2
    try:
        verdicts = verify_receipt(receipt, args.repo, args.ref)
    except EnvError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    failed = [v for v in verdicts if not v.ok]
    if args.format == "json":
        print(json.dumps({
            "ok": not failed,
            "summary": {"pass": len(verdicts) - len(failed),
                        "fail": len(failed)},
            "verdicts": [v.as_dict() for v in verdicts],
        }, indent=2))
    else:
        for v in verdicts:
            print(f"{'PASS' if v.ok else 'FAIL'} {v.label} — {v.detail}")
        print(f"summary: {len(verdicts) - len(failed)} pass, "
              f"{len(failed)} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
