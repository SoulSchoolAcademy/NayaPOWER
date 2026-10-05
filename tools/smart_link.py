#!/usr/bin/env python3
"""Smart-Link generator + gate for NayaPOWER Smart Notes.

A Smart Link is the human-viewable proof of an intelligent event:
    https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/<projection_path>

main ONLY. Branch URLs are rejected by the generator and fail CI.

Subcommands:
    generate <projection_path> [--verify] [--json]   emit link + entry fragment
    gate --index <path> [--tree-list <path>] [--check name,...]
    backfill --index <path> --rev <sha> [--dry-run]

Design spec: ~/workspace/smart-link-generator-spec-2026-10-04.md
Decisions (Naya 4, 2026-10-04):
    D1 auto-PR wins over manual post-merge (humans forgetting is the failure mode;
       PRs are still human-merged, so the human decides).
    D2 PRIVATE-scope notes get status ACTIVE_AUTH_GATED, never bare ACTIVE
       (a 404-for-strangers link must not be presented as universally resolvable).
    D3 one-pass backfill with per-link verification, not lazy re-verification
       (acceptance criterion: zero PENDING links older than one merge cycle).
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"
LINK_RE = re.compile(r"^https://github\.com/SoulSchoolAcademy/NayaPOWER/blob/main/")
BRANCH_URL_RE = re.compile(r"github\.com/SoulSchoolAcademy/NayaPOWER/blob/(?!main/)")
STATUSES = {"ACTIVE", "ACTIVE_AUTH_GATED", "PENDING", "SUPERSEDED", "BROKEN", "COLLISION"}
SMART_NOTES_PREFIX = "BRAIN/05-MEMORY/SMART-NOTES/"


# ---------------------------------------------------------------- link building

def smart_link_for(projection_path: str) -> str:
    """Build the canonical Smart Link for a projection path.

    Raises ValueError on anything that is not a main-branch markdown projection.
    """
    p = (projection_path or "").strip().lstrip("/")
    if not p:
        raise ValueError("EMPTY_PROJECTION_PATH")
    if ".." in p.split("/"):
        raise ValueError("PATH_TRAVERSAL_REJECTED:" + p)
    if "/blob/" in p or re.search(r"/(heads|tree)/", p):
        raise ValueError("REF_IN_PATH_REJECTED:" + p)
    if not p.startswith(SMART_NOTES_PREFIX):
        raise ValueError("NOT_A_SMART_NOTE_PROJECTION:" + p)
    if not p.endswith(".md"):
        raise ValueError("NOT_MARKDOWN:" + p)
    return f"https://github.com/{REPO}/blob/main/{p}"


def validate_shape(url: str) -> bool:
    return bool(LINK_RE.match(url or ""))


# ---------------------------------------------------------------- verification

class GitHubVerifier:
    """Checks a projection path exists on main via the GitHub contents API.

    Injectable: tests pass a fake; CI passes the real one.
    """

    def __init__(self, repo: str = REPO, token: str | None = None):
        self.repo = repo
        self.token = token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    def exists_on_main(self, projection_path: str) -> bool:
        url = f"https://api.github.com/repos/{self.repo}/contents/{projection_path}?ref=main"
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "nayapower-smart-link-gate",
        })
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status == 200
        except Exception:
            return False


class FakeVerifier:
    """Test double: existence is driven by an explicit set of paths."""

    def __init__(self, existing: set[str] | None = None):
        self.existing = set(existing or set())

    def exists_on_main(self, projection_path: str) -> bool:
        return projection_path in self.existing


# ---------------------------------------------------------------- index helpers

def load_index(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def covered_projection_paths(index: dict) -> set[str]:
    """All projection paths the index accounts for (live + superseded)."""
    out = set()
    for e in index.get("entries", []):
        pp = e.get("projection_path")
        if pp:
            out.add(pp)
        for s in e.get("superseded_projections") or []:
            sp = s.get("projection_path") if isinstance(s, dict) else None
            if sp:
                out.add(sp)
    return out


def entry_for_path(index: dict, projection_path: str) -> dict | None:
    for e in index.get("entries", []):
        if e.get("projection_path") == projection_path:
            return e
    return None


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- gate checks
# Each returns a list of violation strings (empty == pass).

def check_shape(index: dict) -> list[str]:
    bad = []
    for e in index.get("entries", []):
        url = e.get("smart_link") or ""
        sid = e.get("smart_note_id", "?")
        if not validate_shape(url):
            bad.append(f"SHAPE {sid}: {url!r} is not a main-only Smart Link")
    return bad


def check_resolves(index: dict, verifier) -> list[str]:
    bad = []
    for e in index.get("entries", []):
        status = e.get("smart_link_status")
        if status not in ("ACTIVE", "ACTIVE_AUTH_GATED"):
            continue
        pp = e.get("projection_path") or ""
        sid = e.get("smart_note_id", "?")
        if not pp or not verifier.exists_on_main(pp):
            bad.append(f"RESOLVES {sid}: {pp or '<no path>'} not found on main")
    return bad


def check_unique(index: dict) -> list[str]:
    seen: dict[str, str] = {}
    bad = []
    for e in index.get("entries", []):
        url = e.get("smart_link") or ""
        sid = e.get("smart_note_id", "?")
        if not url:
            continue
        if url in seen:
            bad.append(f"UNIQUE {sid}: shares smart_link with {seen[url]}: {url}")
        else:
            seen[url] = sid
    return bad


def check_complete(index: dict, tree_paths: list[str]) -> list[str]:
    covered = covered_projection_paths(index)
    bad = []
    for p in tree_paths:
        if p.startswith(SMART_NOTES_PREFIX) and p.endswith(".md") and p not in covered:
            bad.append(f"COMPLETE: {p} has no index entry")
    return bad


def check_no_branch_links(diff_text: str) -> list[str]:
    bad = []
    for i, line in enumerate((diff_text or "").splitlines(), 1):
        if line.startswith("+") and not line.startswith("+++"):
            for m in BRANCH_URL_RE.finditer(line):
                bad.append(f"BRANCH_LINK line {i}: {m.group(0)}... (main-only required)")
    return bad


CHECKS = {
    "link-shape": check_shape,
    "link-resolves": check_resolves,
    "link-unique": check_unique,
    "link-complete": check_complete,
    "no-branch-links": check_no_branch_links,
}


# ---------------------------------------------------------------- generate

def generate(projection_path: str, index: dict, verifier=None,
             rev: str = "", capture: dict | None = None) -> dict:
    """Build the Smart Link + entry fragment for one projection.

    Raises ValueError with a machine-readable reason on any refusal.
    """
    url = smart_link_for(projection_path)  # raises on bad input
    if verifier is not None and not verifier.exists_on_main(projection_path):
        raise ValueError("NOT_ON_MAIN:" + projection_path)
    for e in index.get("entries", []):
        if (e.get("smart_link") or "") == url and \
                e.get("projection_path") != projection_path:
            raise ValueError(
                "COLLISION:" + projection_path + " vs "
                + str(e.get("smart_note_id", "?")))
    existing = entry_for_path(index, projection_path)
    scope = (existing or {}).get("scope", "PRIVATE")
    verified = verifier is not None
    status = "ACTIVE_AUTH_GATED" if scope == "PRIVATE" else "ACTIVE"
    if not verified:
        status = "PENDING"
    now = utcnow()
    fragment = {
        "projection_path": projection_path,
        "smart_link": url,
        "smart_link_status": status,
        "smart_link_verified_at": now if verified else "",
        "smart_link_verified_rev": rev if verified else "",
    }
    if capture:
        fragment["capture_event_id"] = capture.get("event_id", "")
    return fragment


def delivery_text(smart_note_id: str, title: str, url: str,
                  truth_state: str, verified_at: str) -> str:
    return (
        f"\U0001f517 Smart Link \u2014 {smart_note_id}: {title}\n"
        f"{url}\n"
        f"State: {truth_state} \u00b7 Verified resolvable on main at {verified_at}"
    )


# ---------------------------------------------------------------- backfill

def backfill(index: dict, verifier, rev: str, dry_run: bool = False) -> dict:
    """Stamp every entry with verification fields (D3: one-pass, verified).

    Returns a report dict; mutates index in place unless dry_run.
    """
    report = {"stamped": 0, "broken": [], "rev": rev}
    for e in index.get("entries", []):
        pp = e.get("projection_path") or ""
        sid = e.get("smart_note_id", "?")
        ok = bool(pp) and verifier.exists_on_main(pp)
        now = utcnow()
        if dry_run:
            if not ok:
                report["broken"].append(sid)
            else:
                report["stamped"] += 1
            continue
        if ok:
            e["smart_link_verified_at"] = now
            e["smart_link_verified_rev"] = rev
            e["smart_link_status"] = (
                "ACTIVE_AUTH_GATED" if e.get("scope") == "PRIVATE" else "ACTIVE"
            )
            report["stamped"] += 1
        else:
            e["smart_link_status"] = "BROKEN"
            report["broken"].append(sid)
    return report


# ---------------------------------------------------------------- CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="smart_link")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="emit Smart Link + entry fragment")
    g.add_argument("projection_path")
    g.add_argument("--index", default=".naya/memory/smart-notes/index.json")
    g.add_argument("--rev", default="")
    g.add_argument("--verify", action="store_true",
                   help="check the path exists on main before emitting")
    g.add_argument("--delivery", action="store_true",
                   help="also print the human delivery text")

    gt = sub.add_parser("gate", help="run CI gate checks")
    gt.add_argument("--index", required=True)
    gt.add_argument("--tree-list", default="",
                    help="file with one repo path per line (for link-complete)")
    gt.add_argument("--diff", default="", help="diff text (for no-branch-links)")
    gt.add_argument("--checks", default="link-shape,link-unique",
                    help="comma-separated check names")
    gt.add_argument("--verify-resolves", action="store_true",
                    help="actually hit the GitHub API for link-resolves")

    bf = sub.add_parser("backfill", help="stamp verification fields (D3)")
    bf.add_argument("--index", required=True)
    bf.add_argument("--rev", required=True)
    bf.add_argument("--dry-run", action="store_true")
    bf.add_argument("--no-verify", action="store_true",
                    help="stamp without API verification (NOT for production)")

    args = ap.parse_args(argv)

    if args.cmd == "generate":
        index = load_index(args.index) if Path(args.index).exists() else {"entries": []}
        verifier = GitHubVerifier() if args.verify else None
        try:
            frag = generate(args.projection_path, index, verifier, rev=args.rev)
        except ValueError as ex:
            print(f"REFUSED {ex}", file=sys.stderr)
            return 2
        print(json.dumps(frag, indent=2))
        if args.delivery:
            entry = entry_for_path(index, args.projection_path) or {}
            print()
            print(delivery_text(
                entry.get("smart_note_id", "?"),
                entry.get("title", args.projection_path),
                frag["smart_link"],
                entry.get("truth_state", "CANDIDATE"),
                frag["smart_link_verified_at"] or "unverified",
            ))
        return 0

    if args.cmd == "gate":
        index = load_index(args.index)
        violations: list[str] = []
        for name in [c.strip() for c in args.checks.split(",") if c.strip()]:
            if name == "link-resolves":
                if not args.verify_resolves:
                    print("link-resolves: SKIPPED (pass --verify-resolves for live check)")
                    continue
                violations += check_resolves(index, GitHubVerifier())
            elif name == "link-complete":
                if not args.tree_list:
                    print("link-complete: SKIPPED (no --tree-list)", file=sys.stderr)
                    return 2
                tree_paths = Path(args.tree_list).read_text().splitlines()
                violations += check_complete(index, tree_paths)
            elif name == "no-branch-links":
                violations += check_no_branch_links(
                    Path(args.diff).read_text() if args.diff and Path(args.diff).exists()
                    else (sys.stdin.read() if not sys.stdin.isatty() else ""))
            elif name in CHECKS:
                violations += CHECKS[name](index)
            else:
                print(f"unknown check: {name}", file=sys.stderr)
                return 2
        for v in violations:
            print("VIOLATION " + v)
        print(f"{'FAIL' if violations else 'PASS'}: {len(violations)} violations")
        return 1 if violations else 0

    if args.cmd == "backfill":
        index = load_index(args.index)
        verifier = FakeVerifier(set()) if args.no_verify else GitHubVerifier()
        if args.no_verify:
            # stamp blindly only when explicitly asked (tests / dry runs)
            for e in index.get("entries", []):
                e["smart_link_verified_at"] = utcnow()
                e["smart_link_verified_rev"] = args.rev
                e["smart_link_status"] = (
                    "ACTIVE_AUTH_GATED" if e.get("scope") == "PRIVATE" else "ACTIVE")
            report = {"stamped": len(index.get("entries", [])), "broken": [],
                      "rev": args.rev, "mode": "no-verify"}
        else:
            report = backfill(index, verifier, args.rev, dry_run=args.dry_run)
        if not args.dry_run:
            Path(args.index).write_text(json.dumps(index, indent=2) + "\n",
                                        encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
