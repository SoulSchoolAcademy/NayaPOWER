#!/usr/bin/env python3
"""Blast-radius tier classifier for governed PR flow.

The classifier recommends a tier; it never grants merge authority. Highest
risk wins. Unknown or mixed-risk path sets are escalated, not downgraded.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import PurePosixPath

TIER_A_PATHS = (
    ".github/workflows/",
    "BRAIN/01-GOVERNANCE/",
    "BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/",
    "kernel/security/",
    "supabase/migrations/",
    "supabase/functions/",
    "migrations/",
)
TIER_A_PATH_NAMES = {
    "PROTOCOL.md",
    "AGENTS.md",
    "NAYA-ACTIVATION/CONSTITUTION/CONSTITUTION.md",
}
TIER_A_PATH_PATTERNS = (
    re.compile(r"(^|/)(check_.*(gate|paperwork)|.*_gate|auto_merge_gate|check_merge_consensus)\.py$", re.I),
    re.compile(r"(^|/)(security|auth|authorization|permissions?)(/|\.|$)", re.I),
    re.compile(r"(^|/)(deploy|production|migration)(/|\.|$)", re.I),
)
TIER_A_TITLE = re.compile(
    r"\b(governance|ratif(?:y|ication)|design laws?|constitution|security|"
    r"authorization|permission boundary|fail-closed|production deploy|"
    r"deploy pipeline|webhook|protocol enforcement|merge consensus|"
    r"gate workflow|branch protection|ruleset|mass deletion|delete at scale|"
    r"human director law|oath of honor|reservoir laws|house standard)\b",
    re.I,
)
CONTENT_PATHS = (
    ".naya/capture/",
    "BRAIN/05-MEMORY/SMART-NOTES/",
    "BRAIN/05-MEMORY/SUPER-NOTES/",
    "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/",
)
CONTENT_FILES = {
    "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
    "BRAIN/REAL-TREE.json",
    "BRAIN/REAL-TREE.md",
    ".naya/memory/smart-notes/index.json",
    ".naya/memory/smart-notes/coverage-map.json",
}
CONTENT_TITLE = re.compile(
    r"^(?:SN-\d{3,}|smart note filing:|note filing:|regenerate (?:the )?(?:brain )?index)",
    re.I,
)


def _is_tier_a_path(path: str) -> bool:
    p = path.strip().replace("\\", "/")
    if p in TIER_A_PATH_NAMES:
        return True
    if any(p.startswith(prefix) for prefix in TIER_A_PATHS):
        return True
    return any(pattern.search(p) for pattern in TIER_A_PATH_PATTERNS)


def _is_content_path(path: str) -> bool:
    p = path.strip().replace("\\", "/")
    return p in CONTENT_FILES or any(p.startswith(prefix) for prefix in CONTENT_PATHS)


def classify_tier(title: str, changed_paths: list[str] | None = None, *, changed_files: list[dict] | None = None, expected_changed_files: int | None = None) -> dict[str, str]:
    """Return {tier, reason}. Use changed paths when available; title is fallback."""
    paths = [p for p in (changed_paths or []) if p and p.strip()]
    title = title or ""

    # Full live PR-file metadata is required by the real gate. File deletion,
    # rename, missing status, or a truncated/mismatched file list escalates to
    # Tier A. A title/path-only call remains useful for provisional audits and
    # unit tests, but must never be mistaken for a verified live classification.
    if changed_files is not None:
        if not isinstance(expected_changed_files, int) or expected_changed_files != len(changed_files):
            return {"tier": "A", "reason": "changed-file metadata incomplete or truncated; fail safe"}
        if not changed_files:
            return {"tier": "A", "reason": "no changed-file metadata; fail safe"}
        for item in changed_files:
            if not isinstance(item, dict) or not item.get("filename") or not item.get("status"):
                return {"tier": "A", "reason": "changed-file descriptor missing path/status; fail safe"}
            if item.get("status") in {"removed", "renamed", "copied"} or item.get("previous_filename"):
                return {"tier": "A", "reason": "file deletion/rename/copy requires Tier A review"}
            if item.get("status") not in {"added", "modified"}:
                return {"tier": "A", "reason": "unknown changed-file status; fail safe"}

    if changed_paths is not None and not paths:
        return {"tier": "A", "reason": "changed paths unavailable or empty; fail safe to high-consequence review"}

    if TIER_A_TITLE.search(title) or any(_is_tier_a_path(p) for p in paths):
        return {"tier": "A", "reason": "high-consequence law/security/gate/deploy path"}

    if paths:
        if all(_is_content_path(p) for p in paths):
            return {"tier": "C", "reason": "all changed paths are recognized mechanical content"}
        return {"tier": "B", "reason": "ordinary work or mixed non-high-risk paths"}

    # Without changed paths, only obvious content-filing titles may be a
    # provisional C candidate. It remains provisional until path inspection.
    if CONTENT_TITLE.search(title):
        return {"tier": "C", "reason": "provisional content candidate; changed paths must confirm"}
    return {"tier": "B", "reason": "provisional ordinary-work candidate; changed paths required"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run built-in classifier fixtures")
    parser.add_argument("--title", help="PR title")
    parser.add_argument("--paths", nargs="*", default=None, help="changed paths")
    args = parser.parse_args()

    if args.self_test:
        fixtures = [
            ("SN-1771 — Already Built", ["BRAIN/05-MEMORY/SMART-NOTES/SN-1771.md"], "C"),
            ("Regenerate brain index", ["BRAIN/NAYAPOWER-BRAIN-INDEX.json"], "C"),
            ("ordinary UI bug fix", ["HUB/src/button.tsx"], "B"),
            ("ordinary title but workflow changed", ["HUB/src/button.tsx", ".github/workflows/deploy.yml"], "A"),
            ("fix security boundary", ["tools/auth/check_token.py"], "A"),
            ("Smart Note bridge long-path fix", ["tools/note_bridge_live.py"], "B"),
            ("mixed note and code", ["BRAIN/05-MEMORY/SMART-NOTES/SN-1.md", "tools/note_bridge_live.py"], "B"),
            ("Governance contract V1", ["docs/governance.md"], "A"),
        ]
        failures = []
        for title, paths, expected in fixtures:
            actual = classify_tier(title, paths)["tier"]
            if actual != expected:
                failures.append({"title": title, "expected": expected, "actual": actual})
        print(json.dumps({"passed": len(fixtures) - len(failures), "total": len(fixtures), "failures": failures}, indent=2))
        return 1 if failures else 0

    raw = {"title": args.title or "", "changed_paths": args.paths}
    if not args.title and not args.paths:
        raw = json.load(sys.stdin)
    print(json.dumps(classify_tier(raw.get("title", ""), raw.get("changed_paths")), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
