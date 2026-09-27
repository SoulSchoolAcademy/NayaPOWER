from __future__ import annotations

from dataclasses import dataclass
import subprocess


@dataclass(frozen=True)
class SourceInspection:
    ok: bool
    freshness: str
    head: str
    canonical_head: str
    branch: str
    dirty: bool
    reasons: tuple[str, ...]


def run_git(*args: str):
    return subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )


def inspect_source() -> SourceInspection:
    head = run_git("rev-parse", "HEAD").stdout.strip()
    canonical_head = run_git("rev-parse", "origin/main").stdout.strip()
    branch = run_git("symbolic-ref", "--short", "-q", "HEAD").stdout.strip() or "DETACHED"
    dirty_output = run_git("status", "--porcelain").stdout
    dirty = bool(dirty_output.strip())

    reasons: list[str] = []

    if not canonical_head:
        freshness = "UNKNOWN"
        reasons.append("origin/main could not be resolved")
    elif dirty:
        freshness = "DIRTY"
        reasons.append("working tree contains uncommitted changes")
    elif head != canonical_head:
        freshness = "STALE"
        reasons.append(f"HEAD {head} does not equal origin/main {canonical_head}")
    else:
        freshness = "CURRENT"

    if freshness != "CURRENT":
        reasons.append("cold evaluation must not promote claims from non-current source")

    return SourceInspection(
        ok=freshness == "CURRENT",
        freshness=freshness,
        head=head,
        canonical_head=canonical_head,
        branch=branch,
        dirty=dirty,
        reasons=tuple(reasons),
    )


def main() -> int:
    result = inspect_source()
    print(f"STATUS={'PASS' if result.ok else 'FAIL'}")
    print(f"SOURCE_FRESHNESS={result.freshness}")
    print(f"HEAD={result.head}")
    print(f"ORIGIN_MAIN={result.canonical_head}")
    print(f"BRANCH={result.branch}")
    print(f"DIRTY={str(result.dirty).lower()}")
    for reason in result.reasons:
        print(f"REASON={reason}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
