#!/usr/bin/env python3
"""Balance gauge — Balanced Machine step 6 instrumentation.

Computes the four gauge metrics of DESIGN.ai.md §6 from live GitHub data
(via the gh-api wrapper) plus the live Hub page. Every number is DERIVED
from the pull; the script prints its sources. No number is estimated.

Metrics (window = --window-days, default 7):
  (a) Paperwork-block rate — open PRs whose ONLY attributable failing
      checks are the paperwork family (Team review + scorecard receipt /
      Receipt gate / Receipt pin) ÷ all open PRs. "Attributable" =
      failing at the PR head minus checks already failing at the PR's
      merge-base with main (the audit lane subtracted the then-tip's
      reds at a frozen anchor — hidden_files/gate-redesign/
      tier-audit.md, the 44.0% (22/50) baseline of 2026-10-21; the
      merge-base is the same intent made race-proof, since the tip
      moves under a live drain while a PR's base does not). A paperwork
      check that has not run at the head counts as a blocker too (the
      audit's 'expected-pending'), while conflicted (dirty) and draft
      PRs are never charged to paperwork.
  (b) Time-to-merge median by tier — merged PRs in the window; tier by
      the audit-lane path classifier (tier-audit.md methodology),
      encoded in classify_tier() below.
  (c) Post-merge escape rate (PROXY) — merged PRs in the window that are
      referenced (#<n>) by a later fix/revert-titled PR opened within
      7 days of the merge, ÷ merges in the window. Mechanical proxy for
      the design's finder-attributed defect count; labeled a proxy in
      every output.
  (d) Feed freshness — age of the newest entry on https://nayanet.live/
      (max created_at in the served page) vs now; plus the lag vs the
      newest Smart Note landing on main (commits API on the note trees).

Usage:
  python3 tools/balance_gauge.py [--window-days 7] [--json] [--repo OWNER/NAME]

The collector shells out to the gh-api wrapper ($GH_API or
~/workspace/naya/bin/gh-api). The metric functions are pure and are
unit-tested against fixtures in tools/test_balance_gauge.py.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

REPO_DEFAULT = "SoulSchoolAcademy/NayaPOWER"
FEED_URL = "https://nayanet.live/"
NOTE_TREES = ("BRAIN/05-MEMORY/SMART-NOTES", "BRAIN/05-MEMORY/SUPER-NOTES")

PAPERWORK_CHECKS = {
    "Team review + scorecard receipt",
    "Receipt gate (evidence or it didn't happen)",
    "Receipt pin — exact head SHA",
}
FAIL_CONCLUSIONS = {"failure", "timed_out", "cancelled", "action_required", "startup_failure"}
PENDING_STATUSES = {"queued", "in_progress", "waiting", "pending", "requested"}

CONTENT_TREES = ("BRAIN/05-MEMORY/", ".naya/memory/", ".naya/capture/")
INDEX_FILES = {
    "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
    "BRAIN/REAL-TREE.json",
    "BRAIN/REAL-TREE.md",
    ".naya/memory/smart-notes/index.json",
}
DATA_EXTS = (".json", ".ndjson", ".jsonl", ".csv")
KEYWORD_TIERS = ("auth", "security", "rls", "credential", "deploy", "production")
RECEIPT_TOOLS = {
    "tools/check_merge_consensus.py",
    "tools/check_pr_receipt.py",
    "tools/check_scorecard_receipt_pin.py",
}


# --------------------------------------------------------------------------
# Pure metric functions (fixture-tested)
# --------------------------------------------------------------------------

def _in_content_tree(path):
    return any(path.startswith(t) for t in CONTENT_TREES)


def _is_tier_a_path(path):
    """Audit-lane Tier A triggers (tier-audit.md methodology)."""
    base = path.rsplit("/", 1)[-1]
    if path.startswith("BRAIN/01-GOVERNANCE/"):
        return True
    if path.startswith(".github/workflows/"):
        return True
    if base == "AGENTS.md":
        return True
    if path in RECEIPT_TOOLS:
        return True
    if path.startswith("tools/") and "gate" in base:
        return True
    if "/engine/" in path or path.startswith("engine/"):
        return True
    if "hub_sync" in base or "hub-state-builder" in base:
        return True
    if not _in_content_tree(path):
        if "PROTOCOL" in base and "/tests/" not in path and not path.startswith("tests/"):
            return True
        low = path.lower()
        if any(k in low for k in KEYWORD_TIERS):
            return True
    return False


def _is_tier_c_file(path):
    """True when a single changed file is a mechanical/content class."""
    if path.startswith("BRAIN/05-MEMORY/"):
        return True
    if path in INDEX_FILES:
        return True
    if path.endswith(".md") and not path.startswith("BRAIN/01-GOVERNANCE/"):
        return True
    if path.endswith(DATA_EXTS) and not (
        path.startswith("tools/") or path.startswith(".github/") or path.startswith("kernel/")
    ):
        return True
    return False


def classify_tier(files):
    """files: iterable of {'filename': str, 'status': str}. Highest tier wins.

    Audit-lane rules (tier-audit.md): any Tier A path => A; >10 removed
    files => A; every file mechanical/content => C; otherwise B.
    """
    files = list(files)
    removed = sum(1 for f in files if f.get("status") == "removed")
    if removed > 10:
        return "A"
    if any(_is_tier_a_path(f["filename"]) for f in files):
        return "A"
    if files and all(_is_tier_c_file(f["filename"]) for f in files):
        return "C"
    return "B"


def latest_per_name(check_runs):
    """Latest run per check name (by started_at, tie-break: run id)."""
    best = {}
    for run in check_runs:
        name = run.get("name")
        if not name:
            continue
        cur = best.get(name)
        key = (run.get("started_at") or "", run.get("id") or 0)
        if cur is None or key >= (cur.get("started_at") or "", cur.get("id") or 0):
            best[name] = run
    return best


def failing_names(check_runs):
    """Names whose latest run completed with a failing conclusion."""
    out = set()
    for name, run in latest_per_name(check_runs).items():
        if run.get("status") == "completed" and run.get("conclusion") in FAIL_CONCLUSIONS:
            out.add(name)
    return out


SATISFIED_CONCLUSIONS = {"success", "neutral", "skipped"}


def attributable_failures(head_failing, base_failing):
    """Failures the PR itself owns: red at its head, not already red at
    its merge-base with main. (The audit lane subtracted the then-tip's
    reds at a frozen anchor; the merge-base is the same intent made
    race-proof — the anchor moves under a live drain, the base does
    not. PR-only checks never run at a merge-base, so they always stay
    attributable, as they should.)"""
    return set(head_failing) - set(base_failing)


def resolve_tip_failing(per_commit_runs):
    """Failing check names for main, resolved across recent commits
    (newest first): a name pending at the tip resolves from the newest
    ancestor where it completed. Keeps the reported tip set stable
    while the tip's own checks are mid-flight."""
    resolved = {}
    for runs in per_commit_runs:
        for name, run in latest_per_name(runs).items():
            if name in resolved:
                continue
            if run.get("status") == "completed":
                resolved[name] = run.get("conclusion") in FAIL_CONCLUSIONS
    return {name for name, failed in resolved.items() if failed}


def paperwork_blocked(attributable, check_runs=None, mergeable_state=None,
                      draft=False):
    """True iff paperwork is the PR's only blocker (audit methodology).

    `attributable` is the PR-owned failure set (see
    attributable_failures). Blocked when:
      - no attributable failure is a content check, AND
      - some paperwork check is failing, OR (when check_runs are given)
        some paperwork check is not yet satisfied at the head — absent
        (never ran) or still pending both leave the gate as the blocker,
        which is how the audit lane counted 'expected-pending' PRs, AND
      - the PR is not conflicted (dirty) or a draft: those are blocked
        by the conflict / by not being in the merge flow at all.
    """
    if draft or mergeable_state == "dirty":
        return False
    attributable = set(attributable)
    if not attributable <= PAPERWORK_CHECKS:
        return False
    if attributable & PAPERWORK_CHECKS:
        return True
    if check_runs is not None:
        latest = latest_per_name(check_runs)
        for name in PAPERWORK_CHECKS:
            run = latest.get(name)
            if run is None:
                return True  # absent = the gate has not been satisfied
            if not (run.get("status") == "completed"
                    and run.get("conclusion") in SATISFIED_CONCLUSIONS):
                return True  # pending or otherwise unsatisfied
    return False


def median(values):
    vals = sorted(values)
    n = len(vals)
    if n == 0:
        return None
    mid = n // 2
    if n % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


_REF_RE = re.compile(r"#(\d+)")
_FIX_RE = re.compile(r"\b(fix|fixes|fixed|revert|reverts|hotfix)\b", re.IGNORECASE)


def escape_candidates(merged, candidates):
    """PROXY: merged PR numbers escaped by a later fix/revert PR.

    merged: [{'number': int, 'merged_at': datetime}]
    candidates: [{'number': int, 'title': str, 'body': str|None,
                  'created_at': datetime}] — a candidate escapes a merged
    PR when its title carries a fix/revert keyword, it references #<n>
    in title or body, and it was opened within 7 days after the merge.
    """
    escaped = set()
    merged_by_num = {m["number"]: m for m in merged}
    for cand in candidates:
        if cand["number"] in merged_by_num:
            continue
        if not _FIX_RE.search(cand.get("title") or ""):
            continue
        refs = set(_REF_RE.findall(cand.get("title") or ""))
        refs |= set(_REF_RE.findall(cand.get("body") or ""))
        for ref in refs:
            m = merged_by_num.get(int(ref))
            if m is None:
                continue
            delta = cand["created_at"] - m["merged_at"]
            if timedelta(0) < delta <= timedelta(days=7):
                escaped.add(m["number"])
    return escaped


_CREATED_RE = re.compile(r'"created_at"\s*:\s*"([^"]+)"')


def feed_newest(html):
    """(newest created_at datetime | None, entry count) from the Hub page."""
    stamps = []
    for raw in _CREATED_RE.findall(html or ""):
        try:
            stamps.append(parse_ts(raw))
        except ValueError:
            continue
    if not stamps:
        return None, 0
    return max(stamps), len(stamps)


def parse_ts(raw):
    """Parse an ISO-8601 timestamp ('Z' or offset) to an aware datetime."""
    if raw is None:
        return None
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def fmt_hours(hours):
    if hours is None:
        return "n/a"
    if hours < 1:
        return f"{hours * 60:.0f} min"
    if hours < 48:
        return f"{hours:.1f} h"
    return f"{hours / 24.0:.2f} d"


# --------------------------------------------------------------------------
# Live collection (gh-api wrapper)
# --------------------------------------------------------------------------

class Collector:
    def __init__(self, repo):
        self.repo = repo
        self.gh = os.environ.get("GH_API") or os.path.expanduser("~/workspace/naya/bin/gh-api")
        self.calls = []

    def get(self, path):
        self.calls.append(path)
        out = subprocess.run(
            [self.gh, "GET", path], capture_output=True, text=True, timeout=120
        )
        if out.returncode != 0:
            raise RuntimeError(f"gh-api GET {path} failed: {out.stderr.strip()[:300]}")
        return json.loads(out.stdout) if out.stdout.strip() else None

    def paged(self, path, max_pages=10):
        items = []
        sep = "&" if "?" in path else "?"
        for page in range(1, max_pages + 1):
            batch = self.get(f"{path}{sep}per_page=100&page={page}")
            if not batch:
                break
            items.extend(batch)
            if len(batch) < 100:
                break
        return items

    def pr_files(self, number):
        files = []
        for page in range(1, 4):  # cap 300 files; tier rules need no more
            batch = self.get(
                f"/repos/{self.repo}/pulls/{number}/files?per_page=100&page={page}"
            )
            if not batch:
                break
            files.extend(batch)
            if len(batch) < 100:
                break
        return files

    def check_runs(self, sha):
        # A busy commit carries >100 check runs (tip measured at 140);
        # paginate to total_count or the latest-per-name set is fiction.
        runs, page = [], 1
        while True:
            data = self.get(
                f"/repos/{self.repo}/commits/{sha}/check-runs?per_page=100&page={page}"
            )
            batch = (data or {}).get("check_runs", [])
            runs.extend(batch)
            if len(runs) >= (data or {}).get("total_count", len(runs)) or not batch:
                break
            page += 1
        return runs

    def search(self, query, max_pages=10):
        """Issue/PR search — the only enumeration that filters on the
        timestamp itself (merged:/created:) instead of updated-order."""
        from urllib.parse import quote

        items = []
        for page in range(1, max_pages + 1):
            data = self.get(
                f"/search/issues?q={quote(query)}&per_page=100&page={page}"
            )
            batch = (data or {}).get("items", [])
            items.extend(batch)
            if len(items) >= (data or {}).get("total_count", len(items)) or not batch:
                break
        return items


def collect(window_days):
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=window_days)
    c = Collector(REPO)
    sources = []

    tip = c.get(f"/repos/{REPO}/git/refs/heads/main")["object"]["sha"]
    sources.append(f"GET /repos/{REPO}/git/refs/heads/main -> tip {tip}")
    recent_main = c.get(f"/repos/{REPO}/commits?sha=main&per_page=3")
    tip_failing = resolve_tip_failing(
        [c.check_runs(cm["sha"]) for cm in recent_main]
    )
    sources.append(
        f"GET check-runs across last {len(recent_main)} main commits "
        f"(pending-at-tip names resolved from ancestors) -> failing on main: "
        f"{sorted(tip_failing)}"
    )

    # (a) paperwork-block rate over open PRs. Attributable failures are
    # measured against each PR's own merge-base (race-proof under a
    # moving tip); merge-base check-runs are cached by SHA.
    open_prs = c.paged(f"/repos/{REPO}/pulls?state=open")
    sources.append(f"GET pulls?state=open -> {len(open_prs)} open PRs (full pagination)")
    blocked = []
    base_cache = {}
    fallbacks = 0
    for pr in open_prs:
        runs = c.check_runs(pr["head"]["sha"])
        failing = failing_names(runs)
        try:
            cmp_data = c.get(
                f"/repos/{REPO}/compare/main...{pr['head']['sha']}"
            )
            base_sha = cmp_data["merge_base_commit"]["sha"]
            if base_sha not in base_cache:
                base_cache[base_sha] = failing_names(c.check_runs(base_sha))
            attributable = attributable_failures(failing, base_cache[base_sha])
        except Exception:
            fallbacks += 1
            attributable = attributable_failures(failing, tip_failing)
        if paperwork_blocked(attributable, runs,
                             mergeable_state=pr.get("mergeable_state"),
                             draft=bool(pr.get("draft"))):
            blocked.append(pr["number"])
    sources.append(
        "GET check-runs per open PR head + GET compare/main...<head> per PR "
        f"(merge-base reds subtracted; {len(base_cache)} distinct merge-bases, "
        f"{fallbacks} compare fallbacks to the main-resolved set)"
    )

    # (b)+(c) merged PRs in window, enumerated by the Search API on the
    # merged: timestamp itself (a pulls?state=closed scan sorted by
    # updated misses merges buried under later comment activity — the
    # first live run found 7 that way vs 53 by search; search governs).
    start_q = window_start.strftime("%Y-%m-%dT%H:%M:%SZ")
    merged_items = c.search(
        f"repo:{REPO} is:pr is:merged merged:>={start_q}"
    )
    merged = [
        {
            "number": it["number"],
            "created_at": it["created_at"],
            "merged_at": (it.get("pull_request") or {}).get("merged_at"),
        }
        for it in merged_items
        if (it.get("pull_request") or {}).get("merged_at")
        and parse_ts(it["pull_request"]["merged_at"]) >= window_start
    ]
    sources.append(
        f"GET search/issues is:pr is:merged merged:>={start_q} -> {len(merged)} merged "
        f"in window {window_start.isoformat()}..{now.isoformat()}"
    )
    ttm = {"A": [], "B": [], "C": []}
    merged_records = []
    for pr in merged:
        tier = classify_tier(c.pr_files(pr["number"]))
        hours = (parse_ts(pr["merged_at"]) - parse_ts(pr["created_at"])).total_seconds() / 3600.0
        ttm[tier].append(hours)
        merged_records.append(
            {"number": pr["number"], "merged_at": parse_ts(pr["merged_at"]), "tier": tier}
        )
    sources.append("GET pulls/<n>/files per merged PR (tier classification)")

    # escape candidates: any PR created in window (Search API, created:)
    cand_items = c.search(f"repo:{REPO} is:pr created:>={start_q}", max_pages=5)
    candidates = [
        {
            "number": it["number"],
            "title": it.get("title") or "",
            "body": it.get("body") or "",
            "created_at": parse_ts(it["created_at"]),
        }
        for it in cand_items
        if parse_ts(it["created_at"]) >= window_start
    ]
    sources.append(
        f"GET search/issues is:pr created:>={start_q} -> {len(candidates)} "
        f"escape candidates"
    )
    escaped = escape_candidates(merged_records, candidates)

    # (d) feed freshness
    feed_info = {"url": FEED_URL, "newest": None, "entries": 0, "error": None}
    try:
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "balance-gauge/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", "replace")
        newest, count = feed_newest(html)
        feed_info["newest"] = newest
        feed_info["entries"] = count
        sources.append(f"GET {FEED_URL} -> {count} created_at entries parsed")
    except Exception as exc:  # never fake a freshness number
        feed_info["error"] = f"{type(exc).__name__}: {exc}"
        sources.append(f"GET {FEED_URL} FAILED -> {feed_info['error']}")
    landing = None
    for tree in NOTE_TREES:
        commits = c.get(f"/repos/{REPO}/commits?path={tree}&per_page=1")
        if commits:
            ts = parse_ts(commits[0]["commit"]["committer"]["date"])
            landing = ts if landing is None or ts > landing else landing
    if landing:
        sources.append(f"GET commits?path=<note trees> -> newest landing {landing.isoformat()}")

    return {
        "now": now,
        "window_start": window_start,
        "window_days": window_days,
        "tip": tip,
        "tip_failing": sorted(tip_failing),
        "open_total": len(open_prs),
        "paperwork_blocked": sorted(blocked),
        "merges": len(merged_records),
        "ttm_hours": ttm,
        "escaped": sorted(escaped),
        "feed": feed_info,
        "newest_landing": landing,
        "sources": sources,
        "api_calls": len(c.calls),
    }


def render(result):
    lines = []
    lines.append(f"BALANCE GAUGE — read at {result['now'].isoformat()} (window: last "
                 f"{result['window_days']} days, from {result['window_start'].isoformat()})")
    lines.append(f"Main tip: {result['tip']}")
    lines.append("")
    n, total = len(result["paperwork_blocked"]), result["open_total"]
    rate = (100.0 * n / total) if total else 0.0
    lines.append(f"(a) Paperwork-block rate: {n}/{total} open PRs = {rate:.1f}% "
                 f"(target < 10%; baseline 2026-10-21: 44.0%)")
    lines.append(f"    Blocked PRs: {result['paperwork_blocked']}")
    lines.append("")
    lines.append("(b) Time-to-merge median by tier (merged PRs in window):")
    for tier in ("A", "B", "C"):
        vals = result["ttm_hours"][tier]
        lines.append(f"    Tier {tier}: n={len(vals)}, median {fmt_hours(median(vals))}")
    lines.append("")
    esc, merges = len(result["escaped"]), result["merges"]
    erate = (100.0 * esc / merges) if merges else 0.0
    lines.append(f"(c) Post-merge escape rate (PROXY — fix/revert PR referencing the "
                 f"merged PR within 7 days): {esc}/{merges} merges = {erate:.1f}% "
                 f"(target <= 2%)")
    lines.append(f"    Escaped PRs: {result['escaped']}")
    lines.append("")
    feed = result["feed"]
    if feed["newest"] is not None:
        age_h = (result["now"] - feed["newest"]).total_seconds() / 3600.0
        lines.append(f"(d) Feed freshness: newest entry on {feed['url']} is "
                     f"{feed['newest'].isoformat()} — age {fmt_hours(age_h)} "
                     f"({feed['entries']} entries on the page)")
        if result["newest_landing"] is not None:
            lag_min = (feed["newest"] - result["newest_landing"]).total_seconds() / 60.0
            lines.append(f"    Newest note landing on main: "
                         f"{result['newest_landing'].isoformat()}; feed-vs-landing "
                         f"offset {lag_min:+.0f} min (negative = feed behind newest landing)")
    else:
        lines.append(f"(d) Feed freshness: NOT DERIVABLE this run — {feed['error']}")
    lines.append("")
    lines.append(f"Sources ({result['api_calls']} gh-api calls + feed fetch):")
    for s in result["sources"]:
        lines.append(f"  - {s}")
    return "\n".join(lines)


REPO = REPO_DEFAULT


def main(argv=None):
    global REPO
    ap = argparse.ArgumentParser(description="Balanced Machine balance gauge (§6).")
    ap.add_argument("--window-days", type=int, default=7)
    ap.add_argument("--repo", default=REPO_DEFAULT)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    REPO = args.repo
    result = collect(args.window_days)
    if args.json:
        out = dict(result)
        out["now"] = result["now"].isoformat()
        out["window_start"] = result["window_start"].isoformat()
        out["feed"] = dict(result["feed"])
        out["feed"]["newest"] = (
            result["feed"]["newest"].isoformat() if result["feed"]["newest"] else None
        )
        out["newest_landing"] = (
            result["newest_landing"].isoformat() if result["newest_landing"] else None
        )
        out["ttm_median_hours"] = {t: median(v) for t, v in result["ttm_hours"].items()}
        out["paperwork_block_rate"] = (
            len(result["paperwork_blocked"]) / result["open_total"] if result["open_total"] else None
        )
        out["escape_rate_proxy"] = (
            len(result["escaped"]) / result["merges"] if result["merges"] else None
        )
        print(json.dumps(out, indent=2, default=str))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
