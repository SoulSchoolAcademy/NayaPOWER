#!/usr/bin/env python3
"""Fail-closed protected-progress checkpoint validator.

The checkpoint is deliberately separate from ordinary state. It protects the
ability to continue without silently rewinding critical architecture. A
protected change must be verified, then checkpointed, before another protected
change is accepted.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT = ROOT / ".naya/control-plane/PROGRESS-CHECKPOINT.json"


def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"GIT_FAILURE: {' '.join(args)}\n{p.stderr.strip()}")
    return p.stdout.strip()


def fail(message: str) -> None:
    raise SystemExit(f"PROGRESS_CHECKPOINT_FAIL: {message}")


def load() -> dict:
    if not CHECKPOINT.is_file():
        fail("canonical checkpoint file is missing")
    try:
        return json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"checkpoint JSON is unreadable: {exc}")


def changed_protected(baseline: str, protected: list[str], exceptions: list[str]) -> list[str]:
    raw = git("diff", "--name-only", f"{baseline}..HEAD")
    changed = [x for x in raw.splitlines() if x]
    result = []
    for path in changed:
        if path in exceptions:
            continue
        if any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in protected):
            result.append(path)
    return result


def main() -> int:
    cp = load()
    if cp.get("status") != "CANONICAL":
        fail("checkpoint is not CANONICAL")
    baseline = cp.get("baseline", {}).get("commit")
    branch = cp.get("baseline", {}).get("branch")
    if not baseline or len(baseline) != 40:
        fail("baseline commit is missing or malformed")
    if branch != "main":
        fail("checkpoint baseline branch must be main")

    head = git("rev-parse", "HEAD")
    current_branch = git("branch", "--show-current")
    if current_branch != "main":
        fail(f"expected main, found {current_branch or 'detached'}")

    # The baseline object must exist before ancestry can be trusted.
    git("cat-file", "-e", f"{baseline}^{{commit}}")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", baseline, head],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if ancestry.returncode != 0:
        fail(f"ANTI_REWIND: HEAD {head} is not a descendant of checkpoint {baseline}")

    protected = cp.get("protected_scope", {}).get("paths", [])
    exceptions = cp.get("protected_scope", {}).get("exceptions", [])
    if not isinstance(protected, list) or not protected:
        fail("protected scope is empty")
    if not isinstance(exceptions, list):
        fail("checkpoint exceptions must be a list")

    missing = []
    for prefix in protected:
        candidate = ROOT / prefix
        if prefix.endswith("/"):
            if not candidate.is_dir():
                missing.append(prefix)
        elif not candidate.exists():
            missing.append(prefix)
    if missing:
        fail("protected scope points to missing repository paths: " + ", ".join(missing))

    drift = changed_protected(baseline, protected, exceptions)
    if drift:
        print("PROGRESS_CHECKPOINT_STATUS=CHECKPOINT_REQUIRED")
        print(f"baseline={baseline}")
        print(f"head={head}")
        print("protected_changes=")
        for path in drift:
            print(f"- {path}")
        print("RULE=verify the protected change, then advance PROGRESS-CHECKPOINT.json before another protected change")
        return 2

    print("PROGRESS_CHECKPOINT_STATUS=GREEN")
    print(f"baseline={baseline}")
    print(f"head={head}")
    print("anti_rewind=PASS")
    print("protected_scope=PASS")
    print("checkpoint_required=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
