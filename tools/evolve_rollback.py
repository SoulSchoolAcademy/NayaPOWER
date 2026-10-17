#!/usr/bin/env python3
"""EVOLVE rollback machinery — armed, tested, receipted self-modification.

Requirement source (CANDIDATE, not ratified): the EVOLVE node spec candidate
requires that every evolution proposal's rollback be ARMED before APPLY,
TESTED by execution, and RECEIPTED (autonomous rollback on harm detection;
rollback pre-authorized at APPLY time; regression/rollback golden test).
Before this tool, "rollback" in the repo was a label in a scorecard schema
(tools/auto_merge_gate.py); this makes it machinery.

Lifecycle
    ARM -> APPLY -> DECIDE -> ADOPT | ROLLBACK (fail-closed)

  ARM    Validate the proposal, snapshot the ENTIRE workdir tree byte-for-byte
         (the armed manifest is a claim about the whole tree, so the snapshot
         must back the whole tree — a declared-paths-only snapshot could
         detect a silent drop but never restore the dropped bytes) plus a
         full tree manifest. Refuses: empty changesets, stale proposals
         (base_commit != workdir HEAD), path escapes, non-file change
         targets, and PRODUCTION / CONSTITUTIONAL blast radii (protected
         gates — the tool cannot grant that authority).
  APPLY  Write the declared new contents. Then diff the workdir tree against
         the armed manifest: the ONLY differences allowed are the declared
         paths with exactly the declared new hashes. Anything else (a file
         silently dropped or added, e.g. the 2026-10-07 head-tree merge
         incident) is an undeclared change -> rollback path.
  DECIDE Run the proposal's verify command in the workdir. Exit 0 -> ADOPT
         (adoption receipt, snapshot released). Anything else -> ROLLBACK:
         snapshot integrity is re-checked first (tampered snapshot ->
         ROLLBACK_INCOMPLETE, fail-closed, workdir left untouched), then
         bytes are restored, apply-created files removed, and the full tree
         re-hashed — it must equal the armed manifest byte-for-byte, else
         ROLLBACK_INCOMPLETE.

Exit codes (repo convention):
  0 = ADOPTED (execute) / ARMED (arm) / APPLIED (apply)
  1 = ROLLED_BACK (verify failed or undeclared change detected; tree
      restored byte-identical to the armed snapshot — the harness working,
      not an error)
  2 = FAIL-CLOSED (arm refused, snapshot tampered, restore mismatch,
      or any unexpected error)

Subcommands: arm | apply | decide | execute (arm+apply+decide in one shot).
All state lives in --scratch (outside the workdir): state file, snapshot
bytes, receipts. The workdir itself is never polluted. Stdlib only.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RECEIPT_SCHEMA = "NAYANET_EVOLVE_ROLLBACK_RECEIPT_V1"
PROPOSAL_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_RADII = {"LOCAL", "COMPONENT", "CROSS-NODE", "SYSTEM"}
FORBIDDEN_RADII = {"PRODUCTION", "CONSTITUTIONAL"}

EXIT_ADOPTED = 0
EXIT_ROLLED_BACK = 1
EXIT_FAIL_CLOSED = 2


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_manifest(workdir: Path) -> dict[str, str]:
    """relpath -> sha256 for every file under workdir, excluding .git."""
    manifest: dict[str, str] = {}
    for root, dirs, files in os.walk(workdir):
        if ".git" in dirs:
            dirs.remove(".git")
        # never descend into nested checkouts either
        for d in list(dirs):
            if (Path(root) / d / ".git").is_dir():
                dirs.remove(d)
        for name in files:
            p = Path(root) / name
            rel = p.relative_to(workdir).as_posix()
            manifest[rel] = sha256_file(p)
    return manifest


def manifest_digest(manifest: dict[str, str]) -> str:
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(canonical.encode("utf-8"))


def git_head(workdir: Path) -> str | None:
    if not (workdir / ".git").exists():
        return None
    try:
        out = subprocess.run(
            ["git", "-C", str(workdir), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    head = out.stdout.strip()
    return head if SHA_RE.match(head) else None


def fail(state_path: Path | None, scratch: Path, msg: str) -> "Result":
    return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED" if state_path is None else "ROLLBACK_INCOMPLETE", msg)


class Result:
    def __init__(self, exit_code: int, verdict: str, reason: str, receipt: dict | None = None):
        self.exit_code = exit_code
        self.verdict = verdict
        self.reason = reason
        self.receipt = receipt


def write_receipt(scratch: Path, receipt: dict) -> Path:
    receipts = scratch / "receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    stamp = utcnow().replace(":", "").replace("+", "p")
    name = f"{receipt['proposal_id']}-{receipt['verdict']}-{stamp}.json"
    path = receipts / name
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def base_receipt(proposal: dict, verdict: str, reason: str) -> dict:
    return {
        "schema": RECEIPT_SCHEMA,
        "proposal_id": proposal["proposal_id"],
        "verdict": verdict,
        "reason": reason,
        "base_commit": proposal["base_commit"],
        "blast_radius": proposal["blast_radius"],
        "rationale": proposal.get("rationale", ""),
        "decided_at": utcnow(),
    }


def load_proposal(path: Path) -> tuple[dict | None, str]:
    try:
        proposal = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return None, f"proposal unreadable: {e}"
    if not isinstance(proposal, dict):
        return None, "proposal must be a JSON object"
    pid = proposal.get("proposal_id", "")
    if not isinstance(pid, str) or not PROPOSAL_ID_RE.match(pid):
        return None, "proposal_id must match [A-Za-z0-9._-]{1,128}"
    base = proposal.get("base_commit", "")
    if not isinstance(base, str) or (base != "UNGOVERNED" and not SHA_RE.match(base)):
        return None, "base_commit must be a 40-hex sha or the literal UNGOVERNED"
    radius = proposal.get("blast_radius", "")
    if radius in FORBIDDEN_RADII:
        return None, (
            f"blast_radius {radius} refused: PRODUCTION/CONSTITUTIONAL cross "
            "protected gates (NEEDS_AUTHORITY) — this tool cannot grant it"
        )
    if radius not in ALLOWED_RADII:
        return None, f"blast_radius must be one of {sorted(ALLOWED_RADII)} (PRODUCTION/CONSTITUTIONAL refused)"
    changes = proposal.get("changes")
    if not isinstance(changes, list) or not changes:
        return None, "changes must be a non-empty list"
    seen = set()
    for ch in changes:
        if not isinstance(ch, dict):
            return None, "each change must be an object"
        rel = ch.get("path", "")
        if not isinstance(rel, str) or not rel or rel.startswith("/") or ".." in Path(rel).parts:
            return None, f"change path escapes workdir or is invalid: {rel!r}"
        if rel in seen:
            return None, f"duplicate change path: {rel}"
        seen.add(rel)
        b64 = ch.get("content_b64", "")
        if not isinstance(b64, str):
            return None, f"content_b64 must be a string for {rel}"
        try:
            ch["_content"] = base64.b64decode(b64, validate=True)
        except (ValueError, base64.binascii.Error):
            return None, f"content_b64 is not valid base64 for {rel}"
    verify = proposal.get("verify")
    if not isinstance(verify, dict) or not isinstance(verify.get("cmd"), list) or not verify["cmd"]:
        return None, "verify.cmd must be a non-empty list"
    if not all(isinstance(a, str) for a in verify["cmd"]):
        return None, "verify.cmd entries must be strings"
    timeout = verify.get("timeout_s", 300)
    if not isinstance(timeout, (int, float)) or timeout <= 0 or timeout > 3600:
        return None, "verify.timeout_s must be in (0, 3600]"
    return proposal, ""


def cmd_arm(args) -> Result:
    workdir = Path(args.workdir).resolve()
    scratch = Path(args.scratch).resolve()
    if not workdir.is_dir():
        return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED", f"workdir not a directory: {workdir}")
    proposal, err = load_proposal(Path(args.proposal))
    if proposal is None:
        return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED", err)

    head = git_head(workdir)
    if head is None:
        if proposal["base_commit"] != "UNGOVERNED":
            return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED",
                          "workdir is not a git checkout: base_commit must be the literal UNGOVERNED")
        version_binding = "none (non-git workdir)"
    else:
        if proposal["base_commit"] != head:
            return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED",
                          f"STALE_PROPOSAL: proposal base {proposal['base_commit']} != workdir HEAD {head} — rebase, never auto-promote")
        version_binding = f"git HEAD {head}"

    for ch in proposal["changes"]:
        target = workdir / ch["path"]
        if target.exists() and not target.is_file():
            return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED",
                          f"change path exists but is not a regular file: {ch['path']}")

    scratch.mkdir(parents=True, exist_ok=True)
    snap_dir = scratch / "snapshot"
    if snap_dir.exists():
        shutil.rmtree(snap_dir)
    snap_dir.mkdir(parents=True)

    # Full-tree snapshot: the armed manifest is a claim about the WHOLE
    # workdir tree, so the snapshot must back the whole tree byte-for-byte.
    # A declared-paths-only snapshot could detect a silent drop but never
    # restore the dropped bytes — detection without recovery is half a
    # rollback. (.git is excluded from both manifest and snapshot.)
    snap_manifest: dict[str, str] = {}
    for root, dirs, files in os.walk(workdir):
        if ".git" in dirs:
            dirs.remove(".git")
        for d in list(dirs):
            if (Path(root) / d / ".git").is_dir():
                dirs.remove(d)
        for name in files:
            src = Path(root) / name
            rel = src.relative_to(workdir).as_posix()
            dest = snap_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            snap_manifest[rel] = sha256_file(dest)

    tree = tree_manifest(workdir)
    if set(snap_manifest) != set(tree) or any(snap_manifest[r] != tree[r] for r in tree):
        return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED",
                      "internal error: snapshot does not match armed tree")

    clean_proposal = {k: v for k, v in proposal.items() if k != "changes"}
    clean_changes = []
    for ch in proposal["changes"]:
        clean_changes.append({
            "path": ch["path"],
            "new_sha256": sha256_bytes(ch["_content"]),
        })
    clean_proposal["changes"] = clean_changes

    state = {
        "schema": "NAYANET_EVOLVE_ROLLBACK_STATE_V1",
        "proposal_id": proposal["proposal_id"],
        "proposal": clean_proposal,
        "workdir": str(workdir),
        "scratch": str(scratch),
        "version_binding": version_binding,
        "armed_at": utcnow(),
        "armed_tree": tree,
        "armed_tree_digest": manifest_digest(tree),
        "snapshot_manifest": snap_manifest,
        "phase": "ARMED",
    }

    state_path = scratch / "state.json"
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return Result(0, "ARMED",
                  f"armed {proposal['proposal_id']}: {len(clean_changes)} path(s), tree digest {state['armed_tree_digest'][:12]}")


def load_state(state_path: Path) -> tuple[dict | None, str]:
    try:
        return json.loads(state_path.read_text(encoding="utf-8")), ""
    except (OSError, json.JSONDecodeError) as e:
        return None, f"state unreadable: {e}"


def snapshot_integrity_ok(state: dict, scratch: Path) -> tuple[bool, str]:
    snap_dir = scratch / "snapshot"
    for rel, digest in state["snapshot_manifest"].items():
        p = snap_dir / rel
        if not p.is_file():
            return False, f"snapshot file missing: {rel}"
        if sha256_file(p) != digest:
            return False, f"snapshot file tampered: {rel}"
    return True, ""


def do_rollback(state: dict, scratch: Path, proposal: dict, reason: str,
                verify_info: dict | None) -> Result:
    workdir = Path(state["workdir"])
    ok, why = snapshot_integrity_ok(state, scratch)
    if not ok:
        receipt = base_receipt(proposal, "ROLLBACK_INCOMPLETE", f"SNAPSHOT_TAMPERED: {why}")
        receipt["verify"] = verify_info or {}
        write_receipt(scratch, receipt)
        return Result(EXIT_FAIL_CLOSED, "ROLLBACK_INCOMPLETE",
                      f"refusing rollback from tampered snapshot ({why}); workdir left untouched", receipt)

    snap_dir = scratch / "snapshot"
    armed = state["armed_tree"]
    try:
        # restore every armed path byte-for-byte (covers files the apply
        # step — or an outside actor — silently dropped)
        for rel in armed:
            target = workdir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(snap_dir / rel, target)
        # remove anything the evolution added that was never armed
        current = tree_manifest(workdir)
        for rel in current:
            if rel not in armed:
                (workdir / rel).unlink()
        # prune dirs left empty by the removal (best effort)
        for root, dirs, files in os.walk(workdir, topdown=False):
            if ".git" in Path(root).parts:
                continue
            p = Path(root)
            if p != workdir and not any(p.iterdir()):
                try:
                    p.rmdir()
                except OSError:
                    pass
    except OSError as e:
        receipt = base_receipt(proposal, "ROLLBACK_INCOMPLETE", f"RESTORE_ERROR: {e}")
        receipt["verify"] = verify_info or {}
        write_receipt(scratch, receipt)
        return Result(EXIT_FAIL_CLOSED, "ROLLBACK_INCOMPLETE", f"restore failed: {e}", receipt)

    restored = tree_manifest(workdir)
    if restored != state["armed_tree"]:
        receipt = base_receipt(proposal, "ROLLBACK_INCOMPLETE",
                               "RESTORE_MISMATCH: post-rollback tree != armed tree")
        receipt["verify"] = verify_info or {}
        receipt["armed_tree_digest"] = state["armed_tree_digest"]
        receipt["restored_tree_digest"] = manifest_digest(restored)
        write_receipt(scratch, receipt)
        return Result(EXIT_FAIL_CLOSED, "ROLLBACK_INCOMPLETE",
                      "post-rollback tree does not match armed tree", receipt)

    receipt = base_receipt(proposal, "ROLLED_BACK", reason)
    receipt["verify"] = verify_info or {}
    receipt["armed_tree_digest"] = state["armed_tree_digest"]
    receipt["restored_tree_digest"] = manifest_digest(restored)
    receipt["tree_match"] = True
    path = write_receipt(scratch, receipt)
    # release snapshot bytes on clean rollback (manifest retained in receipt/state)
    shutil.rmtree(snap_dir, ignore_errors=True)
    return Result(EXIT_ROLLED_BACK, "ROLLED_BACK",
                  f"rolled back: {reason}; tree restored byte-identical ({path.name})", receipt)


def cmd_apply(args) -> Result:
    scratch = Path(args.scratch).resolve()
    state, err = load_state(scratch / "state.json")
    if state is None:
        return Result(EXIT_FAIL_CLOSED, "APPLY_FAILED", err)
    if state.get("phase") != "ARMED":
        return Result(EXIT_FAIL_CLOSED, "APPLY_FAILED",
                      f"apply requires phase ARMED, found {state.get('phase')}")
    proposal, err = load_proposal(Path(args.proposal))
    if proposal is None:
        return Result(EXIT_FAIL_CLOSED, "APPLY_FAILED", err)
    if proposal["proposal_id"] != state["proposal_id"]:
        return Result(EXIT_FAIL_CLOSED, "APPLY_FAILED", "proposal id mismatch vs armed state")

    workdir = Path(state["workdir"])
    for ch in proposal["changes"]:
        target = workdir / ch["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(ch["_content"])

    # Undeclared-change detector: the ONLY tree differences allowed are the
    # declared paths carrying exactly the declared new hashes.
    applied = tree_manifest(workdir)
    armed = state["armed_tree"]
    declared = {ch["path"]: sha256_bytes(ch["_content"]) for ch in proposal["changes"]}
    problems = []
    for rel, digest in applied.items():
        if rel not in armed:
            if rel not in declared:
                problems.append(f"undeclared file added: {rel}")
            elif digest != declared[rel]:
                problems.append(f"declared path {rel} has wrong content hash")
        elif rel in declared:
            if digest != declared[rel]:
                problems.append(f"declared path {rel} has wrong content hash")
        elif digest != armed[rel]:
            problems.append(f"undeclared file modified: {rel}")
    for rel in armed:
        if rel not in applied and rel not in declared:
            problems.append(f"undeclared file removed: {rel}")
        elif rel not in applied and rel in declared:
            problems.append(f"declared path {rel} missing after apply")

    if problems:
        state["phase"] = "APPLY_DIRTY"
        (scratch / "state.json").write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return do_rollback(state, scratch, proposal,
                           "SILENT_CHANGE_DETECTED: " + "; ".join(problems), None)

    state["phase"] = "APPLIED"
    state["applied_at"] = utcnow()
    (scratch / "state.json").write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return Result(0, "APPLIED",
                  f"applied {len(declared)} declared change(s); tree diff clean")


def cmd_decide(args) -> Result:
    scratch = Path(args.scratch).resolve()
    state, err = load_state(scratch / "state.json")
    if state is None:
        return Result(EXIT_FAIL_CLOSED, "ROLLBACK_INCOMPLETE", err)
    if state.get("phase") not in ("APPLIED", "APPLY_DIRTY"):
        return Result(EXIT_FAIL_CLOSED, "ROLLBACK_INCOMPLETE",
                      f"decide requires phase APPLIED, found {state.get('phase')}")
    proposal, err = load_proposal(Path(args.proposal))
    if proposal is None:
        return Result(EXIT_FAIL_CLOSED, "ROLLBACK_INCOMPLETE", err)

    workdir = Path(state["workdir"])
    verify_info: dict = {"cmd": proposal["verify"]["cmd"], "timeout_s": proposal["verify"]["timeout_s"]}
    try:
        proc = subprocess.run(
            proposal["verify"]["cmd"],
            cwd=str(workdir),
            capture_output=True, text=True,
            timeout=proposal["verify"]["timeout_s"],
        )
        verify_info["exit_code"] = proc.returncode
        verify_info["stdout_tail"] = proc.stdout[-2000:]
        verify_info["stderr_tail"] = proc.stderr[-2000:]
        passed = proc.returncode == 0
        if not passed:
            verify_info["reason"] = f"verify command exited {proc.returncode}"
    except subprocess.TimeoutExpired:
        passed = False
        verify_info["exit_code"] = "TIMEOUT"
        verify_info["reason"] = f"verify command timed out after {proposal['verify']['timeout_s']}s"
    except OSError as e:
        passed = False
        verify_info["exit_code"] = "SPAWN_ERROR"
        verify_info["reason"] = f"could not run verify command: {e}"

    if passed:
        receipt = base_receipt(proposal, "ADOPTED", "verify command exited 0")
        receipt["verify"] = verify_info
        receipt["armed_tree_digest"] = state["armed_tree_digest"]
        receipt["adopted_changes"] = state["proposal"]["changes"]
        path = write_receipt(scratch, receipt)
        shutil.rmtree(scratch / "snapshot", ignore_errors=True)
        state["phase"] = "ADOPTED"
        (scratch / "state.json").write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return Result(EXIT_ADOPTED, "ADOPTED", f"adopted ({path.name})", receipt)

    state["phase"] = "VERIFY_FAILED"
    (scratch / "state.json").write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return do_rollback(state, scratch, proposal,
                       f"VERIFY_FAILED: {verify_info.get('reason', 'non-zero exit')}", verify_info)


def cmd_execute(args) -> Result:
    r = cmd_arm(args)
    if r.verdict != "ARMED":
        # arm wrote no receipt; record the refusal
        proposal, _ = load_proposal(Path(args.proposal))
        if proposal is not None:
            scratch = Path(args.scratch).resolve()
            receipt = base_receipt(proposal, "ARM_REFUSED", r.reason)
            write_receipt(scratch, receipt)
        return Result(EXIT_FAIL_CLOSED, "ARM_REFUSED", r.reason)
    r = cmd_apply(args)
    if r.verdict != "APPLIED":
        return r  # apply already rolled back (SILENT_CHANGE_DETECTED) or failed
    return cmd_decide(args)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="EVOLVE rollback machinery: arm/apply/decide/execute")
    sub = ap.add_subparsers(dest="sub", required=True)
    for name in ("arm", "apply", "decide", "execute"):
        p = sub.add_parser(name)
        p.add_argument("--proposal", required=True, help="path to evolution proposal JSON")
        p.add_argument("--workdir", required=True, help="directory the evolution applies to")
        p.add_argument("--scratch", required=True, help="scratch dir for state/snapshot/receipts (outside workdir)")
    args = ap.parse_args(argv)
    fn = {"arm": cmd_arm, "apply": cmd_apply, "decide": cmd_decide, "execute": cmd_execute}[args.sub]
    try:
        result = fn(args)
    except Exception as e:  # fail-closed on anything unexpected
        print(f"FAIL-CLOSED: unexpected error: {e}", file=sys.stderr)
        return EXIT_FAIL_CLOSED
    print(f"{result.verdict}: {result.reason}", file=sys.stderr)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
