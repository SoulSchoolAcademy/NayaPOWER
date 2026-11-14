#!/usr/bin/env python3
"""distillation_machine.py — the distillation machine's plumbing (census + queue).

Repo-ready standalone script (stdlib only). Intended home: tools/distillation_machine.py
in SoulSchoolAcademy/NayaPOWER. It COUNTS and QUEUES; it never judges essence,
never retires, never deletes. The attended essence pass (a Naya, by hand) does
the judging; this machine keeps the numbers honest so the pass always knows
where the backlog stands.

WHAT IT DOES
------------
census (read-only):
  * fetches the Smart Note registry (.naya/memory/smart-notes/index.json) at a
    given main-tip SHA via the raw.githubusercontent.com URL for that SHA
    (fallback: Contents API through gh-app-api), and
  * fetches the recursive git tree at the same SHA via gh-app-api
    (METHOD and PATH as separate argv, PATH quoted whole), and
  * scans candidate distilled pages (every SN number >= 2000 that is ACTIVE in
    the registry or filed in the tree) for a "Distills ..." coverage line in
    the page's MACHINE section, building the coverage map
    distilled SN -> [raw SNs it covers], and
  * computes the opening numbers: active_pool, filed_pages, distilled_standing,
    covered_raw, undistilled_backlog, compression, raw_in_today, and the
    trigger (FIRES when undistilled_backlog >= 100).

check: prints trigger status only (reuses a state file when its tip matches,
otherwise computes the census in memory).

SN NUMBERS
----------
Registry ids are mixed-format ("SN-019" vs "SN-0019"); everything is matched
by NUMBER. Ids that do not parse to a plain number (e.g. "SN-782-b",
"SN-NET-POWER-MAGIC-001") are counted and reported, never silently dropped.
SN-2690 and SN-2691 are POISONED numbers: they are never treated as
assignable, never queued, and are excluded from every work list this machine
emits (guard is explicit even though neither is currently filed or ACTIVE).

VALUE MODEL (Shawn's refinement, 2026-11-14 — DESIGN LAW for the attended
essence pass; recorded here and in machine-state.json under "value_model")
--------------------------------------------------------------------------
Value is tagged by KIND:
  * honor/behavior      — intelligence that runs at nine: highest
                          honor/respect, behavior at the highest level;
  * system-multiplying  — protocols, automations, apps, functions that give
    build                 more ten-star service;
  * craft/beauty        — the made thing done beautifully;
  * knowledge/fact      — true, usable knowledge.
Rank WITHIN each kind (behavior-change > identity/honor > outcome-proven >
unique; frequency is NOT value). A distillation batch must carry the best of
EVERY kind present in its raw set — never only philosophy (losing the
protocol), never only mechanics (losing the soul). Within a kind, only
duplication / noise / already-said is rock. This machine counts and queues;
it does not judge essence.

STAGED RETIREMENT (design notes — the machine never performs any of it)
-----------------------------------------------------------------------
  active -> distilled -> archived -> gone.
Deletion ("gone") is allowed ONLY after the essence is LIVE in NayaNET
(Hub-visible) AND cold-retrieval proof exists. Retirement/archival/deletion
are attended, gated acts. This machine never deletes anything.

USAGE
-----
  python3 distillation_machine.py census --tip <sha> --out machine-state.json
  python3 distillation_machine.py census --tip <sha> --out machine-state.json --check
  python3 distillation_machine.py check  --tip <sha> [--state machine-state.json]
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

REPO = "SoulSchoolAcademy/NayaPOWER"
REGISTRY_PATH = ".naya/memory/smart-notes/index.json"
SMART_NOTES_ROOT = "BRAIN/05-MEMORY/SMART-NOTES/"
DEFAULT_GH_API = "~/workspace/naya/bin/gh-app-api"
TRIGGER_THRESHOLD = 100
CANDIDATE_FLOOR = 2000  # distilled pages live in the modern range; see method notes
POISONED_NUMBERS = {2690, 2691}

VALUE_MODEL = {
    "source": "Shawn's refinement, 2026-11-14",
    "kinds": [
        "honor/behavior (intelligence that runs at nine: highest honor/respect, behavior at the highest level)",
        "system-multiplying build (protocols, automations, apps, functions that give more ten-star service)",
        "craft/beauty",
        "knowledge/fact",
    ],
    "ranking_within_kind": "behavior-change > identity/honor > outcome-proven > unique; frequency is NOT value",
    "batch_law": (
        "A distillation batch must carry the best of EVERY kind present in its raw set — "
        "never only philosophy (losing the protocol), never only mechanics (losing the soul). "
        "Within a kind, only duplication/noise/already-said is rock."
    ),
    "machine_role": "This is design law for the attended essence pass; the machine counts and queues, it does not judge essence.",
}

DESIGN_NOTES = {
    "staged_retirement": "active -> distilled -> archived -> gone",
    "deletion_gate": (
        "Deletion ONLY after the essence is LIVE in NayaNET (Hub-visible) + cold-retrieval proof. "
        "The machine never deletes."
    ),
    "poisoned_numbers": sorted(POISONED_NUMBERS),
    "poisoned_rule": "SN-2690/SN-2691 are never treated as assignable and never enter any queue this machine emits.",
}

SN_ID_RE = re.compile(r"^SN-0*(\d+)$")
SN_TOKEN_RE = re.compile(r"SN-0*(\d+)")
SN_RANGE_RE = re.compile(r"SN-0*(\d+)\s*[-–—]\s*(?:SN-)?0*(\d+)\b")
SN_DIR_RE = re.compile(r"/SN-0*(\d+)(/|$)")
DISTILLS_LINE_RE = re.compile(r"^\s{0,3}(?:>\s*)?\**\s*Distills\b", re.IGNORECASE)
DISTILLATION_MARKER_RE = re.compile(r"\bDISTILLATION\b")


def sn_number(smart_note_id):
    """Parse a registry smart_note_id to its number, or None if unparseable."""
    if not smart_note_id:
        return None
    m = SN_ID_RE.match(str(smart_note_id).strip())
    return int(m.group(1)) if m else None


def fmt_sn(n):
    return "SN-%04d" % n


def fetch_url(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "distillation-machine/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def raw_url(tip, path):
    return "https://raw.githubusercontent.com/%s/%s/%s" % (
        REPO, tip, urllib.parse.quote(path, safe="/"))


def gh_api(gh_bin, method, path):
    """Call gh-app-api with METHOD and PATH as separate argv (PATH one whole argv)."""
    out = subprocess.run([gh_bin, method, path], capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        raise RuntimeError("gh-app-api %s %s failed (rc=%d): %s" % (method, path, out.returncode, out.stderr[:400]))
    return json.loads(out.stdout)


def fetch_registry(tip, gh_bin):
    """Registry JSON at tip. Primary: raw URL. Fallback: Contents API via gh-app-api."""
    try:
        return json.loads(fetch_url(raw_url(tip, REGISTRY_PATH)).decode("utf-8")), "raw_url"
    except Exception as exc:  # size / transient failure -> Contents API fallback
        print("registry raw fetch failed (%s); falling back to Contents API" % exc, file=sys.stderr)
    data = gh_api(gh_bin, "GET", "/repos/%s/contents/%s?ref=%s" % (REPO, REGISTRY_PATH, tip))
    import base64
    return json.loads(base64.b64decode(data["content"]).decode("utf-8")), "contents_api"


def fetch_tree(tip, gh_bin):
    data = gh_api(gh_bin, "GET", "/repos/%s/git/trees/%s?recursive=1" % (REPO, tip))
    if data.get("truncated"):
        raise RuntimeError("git tree response was truncated; census would be incomplete — refusing to estimate")
    return data["tree"]


def parse_distills(text):
    """Extract covered raw SN numbers from a page's 'Distills ...' coverage line(s).

    A coverage block starts at a line beginning with 'Distills' and continues
    until a blank line (max 6 lines). Explicit SN tokens are collected, and
    SN-a–SN-b / SN-a–b ranges are expanded. Returns a set of ints (may be empty).
    """
    covered = set()
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if DISTILLS_LINE_RE.match(lines[i]):
            block = [lines[i]]
            j = i + 1
            while j < len(lines) and lines[j].strip() and len(block) < 6:
                block.append(lines[j])
                j += 1
            blob = "\n".join(block)
            for m in SN_RANGE_RE.finditer(blob):
                a, b = int(m.group(1)), int(m.group(2))
                if a < b and (b - a) <= 500:
                    covered.update(range(a, b + 1))
            for m in SN_TOKEN_RE.finditer(blob):
                covered.add(int(m.group(1)))
            i = j
        else:
            i += 1
    return covered


def has_distillation_marker(text):
    """True when the page declares itself a distillation (e.g. 'LESSON / DISTILLATION'
    subtitle) even if no parseable 'Distills' list is present."""
    head = "\n".join(text.splitlines()[:8])
    return bool(DISTILLATION_MARKER_RE.search(head))


def run_census(tip, run_date, gh_bin, workers=16):
    registry, registry_source = fetch_registry(tip, gh_bin)
    entries = registry.get("entries", [])
    tree = fetch_tree(tip, gh_bin)
    tree_paths = set(t["path"] for t in tree)

    # ---- registry side -----------------------------------------------------
    active_numbers = set()
    active_entries = 0
    unparseable_active_ids = []
    projection_by_number = {}
    for e in entries:
        n = sn_number(e.get("smart_note_id"))
        if n is not None and e.get("projection_path"):
            projection_by_number.setdefault(n, e["projection_path"])
        if e.get("lifecycle_state") == "ACTIVE":
            active_entries += 1
            if n is None:
                unparseable_active_ids.append(e.get("smart_note_id"))
            else:
                active_numbers.add(n)
    active_pool = len(active_numbers)

    # ---- tree side ---------------------------------------------------------
    filed_numbers = set()
    page_files_by_number = {}
    today_numbers = set()
    today_files = 0
    date_partition = "/%04d/%02d/%02d/" % (run_date.year, run_date.month, run_date.day)
    for t in tree:
        p = t["path"]
        if date_partition in p:
            m = SN_DIR_RE.search(p)
            if m:
                today_numbers.add(int(m.group(1)))
                if p.endswith(".md"):
                    today_files += 1
        if not p.startswith(SMART_NOTES_ROOT):
            continue
        m = SN_DIR_RE.search(p)
        if not m:
            continue
        n = int(m.group(1))
        filed_numbers.add(n)
        if p.endswith(".md"):
            page_files_by_number.setdefault(n, []).append(p)
    filed_pages = len(filed_numbers)

    # A number counts as filed if it has an SN page dir in the tree OR its
    # registry projection_path exists in the tree (essence pages live outside
    # SMART_NOTES_ROOT, e.g. BRAIN/05-MEMORY/ESSENCE-*.md).
    def has_page(n):
        if n in filed_numbers:
            return True
        proj = projection_by_number.get(n)
        return bool(proj and proj in tree_paths)

    # ---- coverage scan -----------------------------------------------------
    candidates = sorted(
        n for n in (active_numbers | filed_numbers)
        if n >= CANDIDATE_FLOOR and n not in POISONED_NUMBERS
    )
    path_to_numbers = {}
    for n in candidates:
        paths = []
        proj = projection_by_number.get(n)
        if proj and proj in tree_paths:
            paths.append(proj)
        for p in page_files_by_number.get(n, []):
            if p not in paths:
                paths.append(p)
        for p in paths:
            path_to_numbers.setdefault(p, []).append(n)

    fetch_failures = []

    def fetch_one(path):
        for attempt in range(2):
            try:
                return path, fetch_url(raw_url(tip, path), timeout=45).decode("utf-8", "replace")
            except Exception as exc:
                last = exc
        fetch_failures.append({"path": path, "error": str(last)[:200]})
        return path, None

    coverage_by_number = {}
    marker_no_coverage = set()
    if path_to_numbers:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for path, text in pool.map(fetch_one, sorted(path_to_numbers)):
                if text is None:
                    continue
                covered = parse_distills(text)
                marker = has_distillation_marker(text)
                for n in path_to_numbers[path]:
                    cov = set(covered)
                    cov.discard(n)  # a note never covers itself
                    if cov:
                        coverage_by_number.setdefault(n, set()).update(cov)
                    elif marker:
                        marker_no_coverage.add(n)
    marker_no_coverage -= set(coverage_by_number)

    distilled_all = set(coverage_by_number)
    distilled_standing_set = distilled_all & active_numbers
    covered_raw_set = set()
    for cov in coverage_by_number.values():
        covered_raw_set |= cov
    covered_raw = len(covered_raw_set)

    backlog_set = sorted(
        n for n in active_numbers
        if has_page(n) and n not in covered_raw_set and n not in distilled_all
        and n not in POISONED_NUMBERS
    )
    undistilled_backlog = len(backlog_set)

    distilled_standing = len(distilled_standing_set)
    compression = (covered_raw / distilled_standing) if distilled_standing else None
    pool_ratio = (distilled_standing / active_pool) if active_pool else None
    trigger_fires = undistilled_backlog >= TRIGGER_THRESHOLD

    state = {
        "machine": "distillation_machine.py census",
        "tip": tip,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "run_date": run_date.isoformat(),
        "registry_source": registry_source,
        "value_model": VALUE_MODEL,
        "design_notes": DESIGN_NOTES,
        "numbers": {
            "registry_entries_total": len(entries),
            "active_entries": active_entries,
            "active_pool": active_pool,
            "active_unparseable_ids": unparseable_active_ids,
            "active_registered_max_sn": max(active_numbers) if active_numbers else None,
            "filed_pages": filed_pages,
            "filed_max_sn": max(filed_numbers) if filed_numbers else None,
            "distilled_standing": distilled_standing,
            "distilled_found_all_lifecycles": len(distilled_all),
            "distilled_marker_no_parseable_coverage": sorted(marker_no_coverage),
            "covered_raw": covered_raw,
            "undistilled_backlog": undistilled_backlog,
            "compression_raw_per_distilled": compression,
            "pool_ratio_distilled_over_active": pool_ratio,
            "raw_in_today": len(today_numbers),
            "raw_in_today_files_md": today_files,
            "trigger_threshold": TRIGGER_THRESHOLD,
            "trigger_fires": trigger_fires,
        },
        "coverage_map": {
            fmt_sn(n): sorted(coverage_by_number[n]) for n in sorted(coverage_by_number)
        },
        "distilled_standing_list": [fmt_sn(n) for n in sorted(distilled_standing_set)],
        "undistilled_backlog_list": [fmt_sn(n) for n in backlog_set],
        "raw_in_today_list": [fmt_sn(n) for n in sorted(today_numbers)],
        "fetch_failures": fetch_failures,
        "coverage_complete": not fetch_failures,
        "method_notes": [
            "active_pool = distinct SN numbers (mixed-format ids matched by number) with >=1 registry entry at lifecycle_state ACTIVE; active_entries is the raw entry count (duplicated numbers exist).",
            "filed_pages = distinct SN numbers with a page dir under BRAIN/05-MEMORY/SMART-NOTES/** in the recursive tree at the tip; a number also counts as filed for backlog purposes when its registry projection_path exists in the tree (Seven Essences pages live outside SMART-NOTES/**).",
            "Distilled detection is PAGE-BYTES ONLY: a note is distilled iff its page carries a 'Distills ...' coverage line, parsed for SN tokens and SN-a-b ranges. No known-range shortcut is used.",
            "Candidate scan set = every SN number >= %d that is ACTIVE in the registry or filed in the tree (the modern range where all distillation batches, essences and day-distillations live). Distilled pages below that floor, if any exist, are NOT scanned — coverage from them is UNKNOWN, not zero." % CANDIDATE_FLOOR,
            "distilled_standing = distilled notes (per above) that are also ACTIVE in the registry. Filed-but-unregistered distillations still contribute coverage to the backlog computation.",
            "Pages that declare DISTILLATION in their subtitle but carry coverage only in prose (no parseable 'Distills' list, e.g. hand-distilled day sets) are listed under distilled_marker_no_parseable_coverage; their covered raws are UNKNOWN and remain in the backlog (conservative).",
            "Seven Essences pages whose retirement coverage is recorded in the registry lifecycle (raws already RETIRED) rather than in a page 'Distills' line contribute no ACTIVE-backlog coverage; RETIRED raws are outside the ACTIVE pool by definition.",
            "raw_in_today = distinct SN numbers with any tree path under the /YYYY/MM/DD/ partition for the run date (local date of the run).",
            "compression = covered_raw / distilled_standing (raw notes covered per standing distilled note); pool ratio = distilled_standing / active_pool.",
            "SN-2690/SN-2691 are poisoned: excluded from candidates, backlog and every queue (neither is currently filed or ACTIVE).",
        ],
    }
    return state


def summary_line(state):
    n = state["numbers"]
    comp = ("%.2f" % n["compression_raw_per_distilled"]) if n["compression_raw_per_distilled"] is not None else "UNKNOWN"
    return (
        "tip=%s active_pool=%d filed=%d distilled_standing=%d covered_raw=%d "
        "backlog=%d compression=%s raw_in_today=%d trigger=%s"
        % (state["tip"][:12], n["active_pool"], n["filed_pages"], n["distilled_standing"],
           n["covered_raw"], n["undistilled_backlog"], comp, n["raw_in_today"],
           "FIRES" if n["trigger_fires"] else "clear")
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description="Distillation machine census (read-only).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("census")
    pc.add_argument("--tip", required=True)
    pc.add_argument("--out", required=True)
    pc.add_argument("--run-date", default=None, help="YYYY-MM-DD (default: today, local)")
    pc.add_argument("--gh-api", default=DEFAULT_GH_API)
    pc.add_argument("--workers", type=int, default=16)
    pc.add_argument("--check", action="store_true", help="also print trigger status line")

    pk = sub.add_parser("check")
    pk.add_argument("--tip", required=True)
    pk.add_argument("--state", default=None, help="reuse this state file if its tip matches")
    pk.add_argument("--run-date", default=None)
    pk.add_argument("--gh-api", default=DEFAULT_GH_API)
    pk.add_argument("--workers", type=int, default=16)

    args = ap.parse_args(argv)
    import os
    gh_bin = os.path.expanduser(args.gh_api)
    run_date = (datetime.strptime(args.run_date, "%Y-%m-%d").date()
                if args.run_date else datetime.now().date())

    if args.cmd == "check" and args.state:
        try:
            with open(args.state) as fh:
                state = json.load(fh)
            if state.get("tip") == args.tip:
                n = state["numbers"]
                print("TRIGGER %s — undistilled_backlog=%d (threshold %d) at tip %s [from %s]"
                      % ("FIRES" if n["trigger_fires"] else "CLEAR",
                         n["undistilled_backlog"], n["trigger_threshold"], args.tip[:12], args.state))
                return 0
            print("state file tip mismatch; computing fresh census", file=sys.stderr)
        except Exception as exc:
            print("state file unusable (%s); computing fresh census" % exc, file=sys.stderr)

    state = run_census(args.tip, run_date, gh_bin, workers=args.workers)

    if args.cmd == "census":
        with open(args.out, "w") as fh:
            json.dump(state, fh, indent=1)
        print(summary_line(state))
        if args.check:
            n = state["numbers"]
            print("TRIGGER %s — undistilled_backlog=%d (threshold %d)"
                  % ("FIRES" if n["trigger_fires"] else "CLEAR",
                     n["undistilled_backlog"], n["trigger_threshold"]))
    else:  # check
        n = state["numbers"]
        print("TRIGGER %s — undistilled_backlog=%d (threshold %d) at tip %s"
              % ("FIRES" if n["trigger_fires"] else "CLEAR",
                 n["undistilled_backlog"], n["trigger_threshold"], args.tip[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
