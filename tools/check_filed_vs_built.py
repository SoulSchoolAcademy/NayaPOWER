#!/usr/bin/env python3
"""Filed-vs-built enforcement check.

Shawn's law (2026-10-10, "implement-don't-file"): filing a directive as a
note without implementing it as code is hoarding, not progress. This check
makes filing-without-implementing VISIBLE and ACTIONABLE.

It scans .naya/capture/ for directive notes (SMART-NOTE files) and verifies
each implementable one has corresponding code in drift_canary/ (or an open
PR building it).

Statuses:
  BUILT      - test/spec file exists  -> the directive is code, not just a note
  BUILDING   - no code yet, but an open PR matches the directive
  FILED_ONLY - no code, no PR, note older than the grace period -> FAIL
  FRESH      - no code, no PR, note within the grace period    -> ok, for now
  LAW        - behavioral law/doctrine (CAPTURE_DURABLE_LAW)   -> exempt, reported

Exit code: 0 = no FILED_ONLY; 1 = FILED_ONLY exists (unless --no-fail).
With --baseline, also reports which FILED_ONLY items are NEW vs the baseline.

Usage:
  python3 tools/check_filed_vs_built.py [--capture-dir DIR] [--tests-dir DIR]
      [--prs-json PATH] [--grace-days N] [--as-of YYYYMMDD]
      [--baseline PATH] [--json-out PATH] [--no-fail]
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime

# Intents that are behavioral law, not code-implementable -> exempt.
LAW_INTENTS = {"CAPTURE_DURABLE_LAW"}

# Slug -> test files that cover it, for notes whose coverage doesn't follow
# the test_<slug>*.py naming convention.
COVERAGE_OVERRIDES = {
    # SN-0798: the Alert Calibration Lab's five sealed histories are fixtures
    # inside the AER-CAL-1 threshold engine tests (per the note itself).
    "calibration-lab": ["test_aer_cal1.py"],
}

FILENAME_RE = re.compile(
    r"^(?:SMART-NOTE-)?(\d{8})-sn-?(\d+)-(.+?)\.json$", re.IGNORECASE
)


def parse_note(path):
    """Return (sn, slug, note_date, intent, title) or None if not a directive note."""
    base = os.path.basename(path)
    m = FILENAME_RE.match(base)
    if not m:
        return None
    datestr, sn, slug = m.group(1), m.group(2), m.group(3)
    try:
        note_date = datetime.strptime(datestr, "%Y%m%d").date()
    except ValueError:
        note_date = None
    intent, title = "UNKNOWN", ""
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        intent = d.get("canonical_intent", "UNKNOWN") or "UNKNOWN"
        title = d.get("title", "") or ""
        # Prefer the canonical smart-note id when present.
        sid = d.get("smart_note_id", "") or ""
        sm = re.search(r"(\d+)", sid)
        if sm:
            sn = sm.group(1).zfill(4)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        pass
    if note_date is None:
        try:
            note_date = date.fromtimestamp(os.path.getmtime(path))
        except OSError:
            note_date = date.today()
    return sn, slug, note_date, intent, title


def normalize(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def code_exists(slug, tests_dir):
    """True if a test file covers this directive's slug."""
    norm = normalize(slug)
    candidates = COVERAGE_OVERRIDES.get(slug.lower(), [])
    for c in candidates:
        if os.path.isfile(os.path.join(tests_dir, c)):
            return True, c
    pattern = os.path.join(tests_dir, "test_" + slug.lower().replace("-", "_") + "*.py")
    hits = [h for h in glob.glob(pattern)
            if os.path.isfile(h) and os.path.getsize(h) > 0]
    if hits:
        return True, os.path.basename(sorted(hits)[0])
    return False, ""


def load_prs(prs_json):
    """Load open PRs from a JSON file, `gh`, or the local gh-api script."""
    if prs_json:
        with open(prs_json, encoding="utf-8") as f:
            return json.load(f)
    # Try `gh` (CI) then the local connector script (dev machine).
    for cmd in (
        ["gh", "pr", "list", "--state", "open",
         "--json", "number,headRefName,body", "--limit", "200"],
    ):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if out.returncode == 0:
                prs = json.loads(out.stdout)
                return [{"number": p["number"],
                         "head_branch": p.get("headRefName", ""),
                         "body": p.get("body", "") or ""} for p in prs]
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
            continue
    gh_api = os.path.expanduser("~/workspace/naya/bin/gh-api")
    if os.path.isfile(gh_api):
        try:
            out = subprocess.run(
                [gh_api, "GET",
                 "/repos/SoulSchoolAcademy/NayaPOWER/pulls?state=open&per_page=100"],
                capture_output=True, text=True, timeout=90)
            if out.returncode == 0:
                prs = json.loads(out.stdout)
                return [{"number": p["number"],
                         "head_branch": p.get("head", {}).get("ref", ""),
                         "body": p.get("body", "") or ""} for p in prs]
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
            pass
    return None


# Slug -> list of PR head-branch substrings known to build the directive,
# for cases where the PR branch doesn't contain the note's slug.
# Human-curated; add entries when triage confirms a link the matcher misses.
# (Body-text SN mentions are NOT used: PR #2000 mentions "sn-0781" only in an
# unrelated registry discussion, which produced a false BUILDING.)
KNOWN_LINKS = {
    # SN-0781 (Causal Uncertainty Without False Blame) is D31, built by
    # Naya 4 in naya4/d31-incident.
    "0781": ["naya4/d31-incident"],
}


def pr_matches(sn, slug, pr):
    """Does this open PR look like it builds this directive?

    Only strong signals count: the normalized slug appears in the PR's head
    branch, or a human-curated KNOWN_LINKS entry matches. A false BUILDING
    is worse than a missed one -- a miss surfaces in triage, a false hit
    hides an unbuilt directive.
    """
    sn4 = sn.zfill(4)
    branch = normalize(pr.get("head_branch", ""))
    if normalize(slug) and normalize(slug) in branch:
        return True
    for known in KNOWN_LINKS.get(sn4, []):
        if normalize(known) in branch:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="Filed-vs-built enforcement check.")
    ap.add_argument("--capture-dir", default=".naya/capture")
    ap.add_argument("--tests-dir", default="drift_canary/tests")
    ap.add_argument("--prs-json", default=None)
    ap.add_argument("--grace-days", type=int, default=7)
    ap.add_argument("--as-of", default=None,
                    help="Reference date YYYYMMDD (for testing date logic).")
    ap.add_argument("--baseline", default=None,
                    help="JSON file with previous filed_only SN list.")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--no-fail", action="store_true",
                    help="Report only; exit 0 even with FILED_ONLY.")
    args = ap.parse_args()

    today = (datetime.strptime(args.as_of, "%Y%m%d").date()
             if args.as_of else date.today())

    prs = load_prs(args.prs_json)
    prs_unavailable = prs is None
    if prs_unavailable:
        print("WARNING: could not list open PRs; BUILDING detection disabled.",
              file=sys.stderr)
        prs = []

    baseline_filed = set()
    if args.baseline and os.path.isfile(args.baseline):
        try:
            with open(args.baseline, encoding="utf-8") as f:
                baseline_filed = set(json.load(f).get("filed_only", []))
        except (json.JSONDecodeError, OSError):
            pass

    rows = []
    seen_sn = {}
    duplicates = []
    for path in sorted(glob.glob(os.path.join(args.capture_dir, "SMART-NOTE-*.json"))):
        parsed = parse_note(path)
        if not parsed:
            continue
        sn, slug, note_date, intent, title = parsed
        sn_key = "SN-%s" % sn.zfill(4)
        if sn_key in seen_sn:
            # Duplicate human SN ids exist in the registry (known issue).
            # Keep the first (deterministic); record the collision.
            duplicates.append({"sn": sn_key, "path": path,
                               "kept": seen_sn[sn_key]})
            continue
        seen_sn[sn_key] = path
        days = (today - note_date).days if note_date else -1

        if intent in LAW_INTENTS:
            rows.append(dict(sn="SN-%s" % sn.zfill(4), title=title[:60],
                             intent=intent, note_date=str(note_date),
                             code="", pr="", days=days, status="LAW"))
            continue

        found, evidence = code_exists(slug, args.tests_dir)
        if found:
            status, pr_ref = "BUILT", ""
        else:
            match = next((p for p in prs if pr_matches(sn, slug, p)), None)
            if match:
                status, pr_ref = "BUILDING", "#%s" % match["number"]
            elif days < 0 or days < args.grace_days:
                status, pr_ref = "FRESH", ""
            else:
                status, pr_ref = "FILED_ONLY", ""
        rows.append(dict(sn="SN-%s" % sn.zfill(4), title=title[:60],
                         intent=intent, note_date=str(note_date),
                         code=evidence, pr=pr_ref, days=days, status=status))

    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    filed = [r for r in rows if r["status"] == "FILED_ONLY"]
    new_filed = [r for r in filed if r["sn"] not in baseline_filed]

    # Markdown report to stdout.
    print("# Filed vs Built — %s" % today.isoformat())
    print()
    print("| SN | Title | Intent | Note date | Code/PR | Days | Status |")
    print("|----|-------|--------|-----------|---------|------|--------|")
    for r in rows:
        proof = r["code"] or r["pr"]
        print("| %s | %s | %s | %s | %s | %s | **%s** |"
              % (r["sn"], r["title"].replace("|", "\\|"), r["intent"],
                 r["note_date"], proof, r["days"], r["status"]))
    print()
    print("Summary: " + ", ".join(
        "%s=%d" % (k, counts.get(k, 0))
        for k in ("BUILT", "BUILDING", "FILED_ONLY", "FRESH", "LAW")))
    if prs_unavailable:
        print("Note: open-PR data unavailable; BUILDING may be undercounted.")
    if args.baseline:
        if new_filed:
            print("NEW vs baseline (%d): %s"
                  % (len(new_filed), ", ".join(r["sn"] for r in new_filed)))
        else:
            print("No new FILED_ONLY vs baseline.")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"as_of": today.isoformat(), "counts": counts,
                       "rows": rows,
                       "filed_only": [r["sn"] for r in filed],
                       "new_vs_baseline": [r["sn"] for r in new_filed],
                       "prs_unavailable": prs_unavailable,
                       "duplicate_sns": duplicates},
                      f, indent=2)
    if duplicates:
        print("Note: %d duplicate SN id(s) collapsed (first kept): %s"
              % (len(duplicates),
                 ", ".join(sorted(set(d["sn"] for d in duplicates)))))

    if filed and not args.no_fail:
        print("\nFAIL: %d directive(s) filed as notes with no code past the "
              "%d-day grace period: %s"
              % (len(filed), args.grace_days,
                 ", ".join(r["sn"] for r in filed)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
