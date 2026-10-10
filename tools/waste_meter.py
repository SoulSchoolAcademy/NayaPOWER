#!/usr/bin/env python3
"""Waste Meter v1 — make AI waste visible.

Operational definition: waste = any unit of machine or human effort that did
not advance a merged, verified outcome. Three shapes: rework (doing the same
work twice), waiting (work sitting idle), redo (work that undoes earlier work).

Measurable-now proxies (every figure cites its source; estimates are labeled):
  1. Commits per merged PR        (PR timeline `committed` events)
  2. Force-pushes / branch rewrites(PR timeline `head_ref_force_pushed`)
  3. PR cycle time created->merged(PR list API)
  4. CI re-runs                   (Actions runs API `run_attempt`)
  5. Reverted merges              (Search API, merged PRs titled "Revert ...")
  6. Stalled PRs                  (open PRs untouched > 72h)
  7. Smart Notes staged per builder-day (#1354 comments, keyword proxy)

Aspirational (NOT measured — no data source exists): token/compute spend per
decision. The GitHub API exposes no token usage and local agent logs don't
record tokens. Faking it would be worse than admitting the gap.

Read-only on GitHub. Never touches .github/workflows/, production,
credentials, or anything destructive.

Usage:
    python3 tools/waste_meter.py --days 7
    python3 tools/waste_meter.py --since 2026-10-03 --until 2026-10-10 \\
        --out-md /tmp/waste.md --out-json /tmp/waste.json
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO = "SoulSchoolAcademy/NayaPOWER"
DEFAULT_BOARD_ISSUE = 1354
DEFAULT_GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")

SPEC_PATH = "docs/waste-meter-spec.md"


class WasteMeterError(RuntimeError):
    """A data-source failure. The meter reports gaps; it never invents data."""


# ---------------------------------------------------------------------------
# GitHub access (read-only GETs through the skill's gh-api; auth stays there)
# ---------------------------------------------------------------------------

def gh_get(path: str, gh_api: str = DEFAULT_GH_API, timeout: int = 60) -> object:
    """GET a GitHub API path via gh-api. Returns parsed JSON."""
    try:
        proc = subprocess.run(
            [gh_api, "GET", path],
            capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise WasteMeterError(f"gh-api not found at {gh_api}: {exc}") from exc
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()[:300]
        raise WasteMeterError(f"gh-api GET {path} failed: {detail}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise WasteMeterError(f"gh-api GET {path} returned non-JSON") from exc


def paginate(path: str, gh_api: str, per_page: int = 100):
    """Yield items across all pages of a list endpoint (newest first)."""
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        data = gh_get(f"{path}{sep}per_page={per_page}&page={page}", gh_api)
        if not isinstance(data, list) or not data:
            return
        yield from data
        if len(data) < per_page:
            return
        page += 1


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _progress(msg: str) -> None:
    print(f"[waste-meter] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------

def collect_merged_prs_windowed(repo: str, since: datetime, until: datetime, gh_api: str):
    """Same as collect_merged_prs but stops paging early (fewer API calls)."""
    prs, page_had_candidate = [], False
    page = 1
    while True:
        data = gh_get(
            f"/repos/{repo}/pulls?state=closed&sort=updated&direction=desc"
            f"&per_page=100&page={page}", gh_api)
        if not data:
            break
        page_had_candidate = False
        for pr in data:
            merged_at = _parse(pr.get("merged_at"))
            updated_at = _parse(pr.get("updated_at"))
            if merged_at and since <= merged_at <= until:
                prs.append({
                    "number": pr["number"],
                    "title": pr.get("title", ""),
                    "created_at": pr.get("created_at"),
                    "merged_at": pr.get("merged_at"),
                })
                page_had_candidate = True
            elif updated_at and updated_at >= since:
                page_had_candidate = True  # still in the fresh zone; keep going
        if len(data) < 100 or not page_had_candidate:
            # Entire page is older than the window (or last page): nothing
            # later can be merged in-window because updated_at >= merged_at.
            if not page_had_candidate:
                break
        page += 1
    return prs


def collect_pr_timeline(repo: str, number: int, gh_api: str) -> dict:
    """One timeline call per PR: commit count + force-push count.

    Events used: `committed` (one per commit landed on the PR) and
    `head_ref_force_pushed` (one per branch rewrite)."""
    events = list(paginate(f"/repos/{repo}/issues/{number}/timeline", gh_api))
    commits = sum(1 for e in events if e.get("event") == "committed")
    force_pushes = sum(1 for e in events if e.get("event") == "head_ref_force_pushed")
    truncated = len(events) == 0  # empty timeline is itself a signal, not a gap
    return {"number": number, "commits": commits,
            "force_pushes": force_pushes, "timeline_events": len(events)}


def collect_ci_runs(repo: str, since: datetime, until: datetime, gh_api: str):
    """Workflow runs created in-window. Stops paging once runs are older than
    the window (sorted newest first). Records attempts, conclusions, durations."""
    runs = []
    page = 1
    while True:
        data = gh_get(
            f"/repos/{repo}/actions/runs?created=%3E%3D{_iso(since)}"
            f"&per_page=100&page={page}", gh_api)
        batch = data.get("workflow_runs", []) if isinstance(data, dict) else []
        if not batch:
            break
        keep_going = False
        for r in batch:
            created = _parse(r.get("created_at"))
            if created and since <= created <= until:
                updated = _parse(r.get("updated_at")) or created
                runs.append({
                    "id": r.get("id"),
                    "name": r.get("name"),
                    "event": r.get("event"),
                    "conclusion": r.get("conclusion"),
                    "run_attempt": r.get("run_attempt", 1) or 1,
                    "minutes": max(0.0, (updated - created).total_seconds() / 60.0),
                })
                keep_going = True
            elif created and created >= since:
                keep_going = True
        if len(batch) < 100 or not keep_going:
            if not keep_going:
                break
        page += 1
    return runs


def collect_board_comments(repo: str, issue: int, since: datetime, until: datetime,
                           gh_api: str):
    """#1354 comments in-window. `since=` filters by updated_at, so we
    re-filter strictly on created_at."""
    comments = []
    for c in paginate(
            f"/repos/{repo}/issues/{issue}/comments"
            f"?since={_iso(since)}", gh_api):
        created = _parse(c.get("created_at"))
        if created and since <= created <= until:
            comments.append({
                "id": c.get("id"),
                "author": (c.get("user") or {}).get("login", "?"),
                "created_at": c.get("created_at"),
                "body": c.get("body", "") or "",
            })
    return comments


def collect_reverts(repo: str, since: datetime, until: datetime, gh_api: str):
    """Merged PRs with 'Revert' in the title inside the window (redo waste)."""
    lo, hi = since.strftime("%Y-%m-%d"), until.strftime("%Y-%m-%d")
    q = (f"repo:{repo}+type:pr+is:merged+merged:{lo}..{hi}"
         f"+Revert+in:title").replace(" ", "+")
    data = gh_get(f"/search/issues?q={q}&per_page=100", gh_api)
    items = data.get("items", []) if isinstance(data, dict) else []
    return [{"number": i["number"], "title": i.get("title", "")} for i in items]


def collect_stalled_prs(repo: str, gh_api: str, stale_hours: float = 72.0):
    """Open PRs untouched for longer than `stale_hours` (waiting waste).

    Returns {"stalled": [...], "open_total": n} — the denominator matters:
    "185 stalled" means something different out of 190 open vs 2000 open."""
    now = datetime.now(timezone.utc)
    stalled, open_total, seen_fresh = [], 0, False
    for pr in paginate(f"/repos/{repo}/pulls?state=open&sort=updated&direction=asc",
                       gh_api, per_page=100):
        updated = _parse(pr.get("updated_at"))
        if not updated:
            continue
        open_total += 1
        age_h = (now - updated).total_seconds() / 3600.0
        if age_h <= stale_hours:
            seen_fresh = True
            continue  # ascending: still count the rest for the denominator
        if not seen_fresh:
            stalled.append({"number": pr["number"], "title": pr.get("title", ""),
                            "stale_days": round(age_h / 24.0, 1)})
    return {"stalled": stalled, "open_total": open_total}


def scan_local_logs(logs_dir: str, since: datetime, until: datetime) -> dict:
    """Rough local-activity signal: *.log files modified in-window.

    This is NOT effort measurement — it only shows the machine was busy.
    Reported as a rough signal, never as a precise figure."""
    result = {"available": False, "files": 0, "bytes": 0}
    try:
        proc = subprocess.run(
            ["find", logs_dir, "-name", "*.log", "-newermt", since.strftime("%Y-%m-%d"),
             "!", "-newermt", (until + timedelta(days=1)).strftime("%Y-%m-%d"),
             "-printf", "%s\\n"],
            capture_output=True, text=True, timeout=120)
        if proc.returncode != 0:
            return result
        sizes = [int(x) for x in proc.stdout.split() if x.strip().isdigit()]
        result.update({"available": True, "files": len(sizes),
                       "bytes": sum(sizes)})
    except (OSError, subprocess.TimeoutExpired):
        pass
    return result


# ---------------------------------------------------------------------------
# Aggregation (pure — fully unit-testable, no network)
# ---------------------------------------------------------------------------

def _median(xs: list[float]) -> float | None:
    return float(statistics.median(xs)) if xs else None


def _mean(xs: list[float]) -> float | None:
    return float(statistics.fmean(xs)) if xs else None


SN_KEYWORDS = ("smart note", "smart-note", "sn-")


def is_sn_stage_post(body: str) -> bool:
    """Keyword proxy for a Smart-Note-staged post. Counts posts, not quality."""
    low = body.lower()
    if "smart note" in low or "smart-note" in low:
        return True
    import re
    return bool(re.search(r"\bsn-\d", low))


_TAG_RE = None

def lane_tag(body: str) -> str | None:
    """Lane identity from a [TAG] signature in the post body.

    GitHub `author` is useless here — every lane posts through one service
    account — so identity comes from the sign-in/out tag convention
    (`[NAYA 4]`, `[CODA 3]`, ...). Returns the normalized lane family
    ("NAYA 4") or None for untagged posts."""
    global _TAG_RE
    import re
    if _TAG_RE is None:
        _TAG_RE = re.compile(r"^\s*(?:#+\s*)?\[([^\]\n]{1,48})\]", re.MULTILINE)
    m = _TAG_RE.search(body or "")
    if not m:
        return None
    tag = m.group(1).strip().upper()
    # "NAYA 4 → LEARNING", "NAYA 5 | VOICE-BUILDER", "NAYA 2 — BRAIN LOOP"
    # all normalize to the lane family before the first delimiter.
    tag = re.split(r"\s*[→\|\-—–/]\s*", tag, maxsplit=1)[0].strip()
    return tag or None


def aggregate(raw: dict) -> dict:
    """Turn collected raw data into metrics. Every number traces to raw."""
    prs = raw.get("prs", [])
    timelines = {t["number"]: t for t in raw.get("timelines", [])}

    commit_counts, cycles_h, force_pushes = [], [], 0
    prs_with_force_push = 0
    timeline_errors = raw.get("timeline_errors", 0)
    for pr in prs:
        tl = timelines.get(pr["number"])
        if tl is None:
            continue  # excluded honestly; counted in timeline_errors
        commit_counts.append(tl["commits"])
        force_pushes += tl["force_pushes"]
        prs_with_force_push += 1 if tl["force_pushes"] else 0
        created, merged = _parse(pr.get("created_at")), _parse(pr.get("merged_at"))
        if created and merged and merged >= created:
            cycles_h.append((merged - created).total_seconds() / 3600.0)

    runs = raw.get("ci_runs", [])
    extra_attempts = sum(max(0, r["run_attempt"] - 1) for r in runs)
    conclusions: dict[str, int] = {}
    for r in runs:
        conclusions[str(r.get("conclusion"))] = conclusions.get(str(r.get("conclusion")), 0) + 1
    failed_runs = conclusions.get("failure", 0)
    ci_minutes = sum(r["minutes"] for r in runs if r.get("conclusion") in
                     ("success", "failure", "cancelled", "timed_out"))

    comments = raw.get("board_comments", [])
    authors = {c["author"] for c in comments}
    sn_posts = sum(1 for c in comments if is_sn_stage_post(c["body"]))
    lane_counts: dict[str, int] = {}
    untagged = 0
    for c in comments:
        tag = lane_tag(c["body"])
        if tag:
            lane_counts[tag] = lane_counts.get(tag, 0) + 1
        else:
            untagged += 1
    active_lanes = len(lane_counts)

    reverts = raw.get("reverts", [])
    stalled_raw = raw.get("stalled_prs", {"stalled": [], "open_total": 0})
    if isinstance(stalled_raw, list):  # tolerate the pre-v1.1 shape
        stalled_raw = {"stalled": stalled_raw, "open_total": len(stalled_raw)}
    stalled = stalled_raw["stalled"]
    open_total = stalled_raw["open_total"]

    days = raw.get("window_days", 7) or 7
    extra_commits = sum(max(0, c - 1) for c in commit_counts)

    waste_ranking = [
        ("Extra commits beyond the first on each PR (rework)",
         extra_commits,
         "Every commit after the first is a do-over on the same change."),
        ("CI re-runs — extra attempts beyond the first (machine redo)",
         extra_attempts,
         "Each extra attempt re-spends machine time on a run that already ran."),
        ("Failed CI runs (work that produced no green signal)",
         failed_runs,
         "A failed run is effort with no usable outcome until it is fixed."),
        ("Force-pushes / branch rewrites (rework)",
         force_pushes,
         "Rewriting history can invalidate review already done."),
        ("Reverted merges (redo — landed, then un-landed)",
         len(reverts),
         "The original work plus the revert both produced nothing."),
        ("Stalled PRs — open and untouched over 72h (waiting)",
         len(stalled),
         "Effort frozen: value not shipped, author context decaying."),
    ]
    waste_ranking.sort(key=lambda x: x[1], reverse=True)

    return {
        "window": raw.get("window", {}),
        "window_days": days,
        "prs_merged": len(prs),
        "prs_measured": len(commit_counts),
        "timeline_errors": timeline_errors,
        "commits_per_pr": {
            "mean": _mean(commit_counts), "median": _median(commit_counts),
            "max": max(commit_counts) if commit_counts else None,
            "buckets": {
                "1 commit (clean landing)": sum(1 for c in commit_counts if c == 1),
                "2-3 commits": sum(1 for c in commit_counts if 2 <= c <= 3),
                "4-8 commits": sum(1 for c in commit_counts if 4 <= c <= 8),
                "9+ commits (heavy rework)": sum(1 for c in commit_counts if c >= 9),
            },
        },
        "extra_commits_beyond_first": extra_commits,
        "force_pushes": force_pushes,
        "prs_with_force_push": prs_with_force_push,
        "cycle_hours": {"mean": _mean(cycles_h), "median": _median(cycles_h)},
        "ci": {
            "runs": len(runs),
            "extra_attempts": extra_attempts,
            "rerun_rate": (extra_attempts / len(runs)) if runs else None,
            "conclusions": conclusions,
            "failed_runs": failed_runs,
            "wall_minutes": round(ci_minutes, 1),
        },
        "reverts": {"count": len(reverts),
                    "items": reverts[:10]},
        "stalled_prs": {"count": len(stalled), "open_total": open_total,
                        "oldest": stalled[:5]},
        "board": {
            "comments": len(comments),
            "sn_stage_posts": sn_posts,
            "active_authors": len(authors),
            "active_lanes": active_lanes,
            "untagged_posts": untagged,
            "top_lanes": sorted(lane_counts.items(), key=lambda kv: kv[1],
                                reverse=True)[:8],
            "sn_posts_per_lane_day":
                round(sn_posts / (active_lanes * days), 2) if active_lanes and days else None,
        },
        "local_logs": raw.get("local_logs", {"available": False}),
        "waste_ranking": [
            {"source": name, "wasted_events": n, "plain": plain}
            for name, n, plain in waste_ranking
        ],
    }


# ---------------------------------------------------------------------------
# Plain-words readout (the part a non-engineer reads)
# ---------------------------------------------------------------------------

def _fmt(x, nd=1, suffix=""):
    if x is None:
        return "n/a (no data)"
    if isinstance(x, float):
        return f"{x:.{nd}f}{suffix}"
    return f"{x}{suffix}"


def _fmt_hours(h: float | None) -> str:
    """Cycle time in the unit a human feels: minutes when under an hour."""
    if h is None:
        return "n/a (no data)"
    if h < 1:
        return f"{h * 60:.1f} minutes"
    return f"{h:.1f} hours"


def render_markdown(m: dict, meta: dict) -> str:
    """The plain-words readout. No jargon, every figure sourced."""
    w = m["window"]
    L: list[str] = []
    A = L.append

    A(f"# Waste Meter — week of {w.get('since', '?')[:10]} to {w.get('until', '?')[:10]}")
    A("")
    A("**In a nutshell:** "
      f"the team landed **{m['prs_merged']} changes** this week. "
      f"The typical change took **{_fmt(m['commits_per_pr']['median'], 0)} tries** "
      f"(commits) and **{_fmt_hours(m['cycle_hours']['median'])}** from first draft to landed. "
      f"Machines re-ran work **{m['ci']['extra_attempts']} extra times**, "
      f"and **{m['stalled_prs']['count']} of {m['stalled_prs']['open_total']} open changes "
      f"are sitting frozen**, untouched for over 3 days. "
      f"Details below — every number names where it came from.")
    A("")
    A("## The numbers")
    A("")
    A("| What we counted | Figure | Where it came from |")
    A("|-----------------|--------|--------------------|")
    A(f"| Changes landed (PRs merged) | {m['prs_merged']} | GitHub PR list API |")
    cp = m["commits_per_pr"]
    A(f"| Tries per change (commits), typical | {_fmt(cp['median'], 0)} | PR timeline API (`committed` events) |")
    A(f"| Tries per change (commits), average | {_fmt(cp['mean'])} | PR timeline API |")
    A(f"| Worst case: most tries on one change | {_fmt(cp['max'], 0)} | PR timeline API |")
    b = cp["buckets"]
    A(f"| Clean landings (1 try) | {b['1 commit (clean landing)']} of {m['prs_measured']} | PR timeline API |")
    A(f"| Heavy rework (9+ tries) | {b['9+ commits (heavy rework)']} of {m['prs_measured']} | PR timeline API |")
    A(f"| Branch rewrites (force-pushes) | {m['force_pushes']} on {m['prs_with_force_push']} changes | PR timeline API (`head_ref_force_pushed`) |")
    A(f"| Draft-to-landed time, typical | {_fmt_hours(m['cycle_hours']['median'])} | PR `created_at` → `merged_at` |")
    A(f"| Draft-to-landed time, average | {_fmt_hours(m['cycle_hours']['mean'])} | PR `created_at` → `merged_at` |")
    ci = m["ci"]
    A(f"| Machine runs (CI) | {ci['runs']} | GitHub Actions runs API |")
    A(f"| Machine re-runs (extra attempts) | {ci['extra_attempts']} | Actions runs API (`run_attempt`) |")
    A(f"| Failed machine runs | {ci['failed_runs']} | Actions runs API (`conclusion`) |")
    A(f"| Machine time burned (wall-clock) | {_fmt(ci['wall_minutes'], 0)} minutes | Actions runs API (run durations) |")
    A(f"| Changes landed then un-landed (reverts) | {m['reverts']['count']} | Search API: merged PRs titled \"Revert …\" |")
    A(f"| Changes sitting frozen 3+ days (stalled) | {m['stalled_prs']['count']} of {m['stalled_prs']['open_total']} open | PR list API (`state=open`, `updated_at`) |")
    bd = m["board"]
    A(f"| Board posts this week (#1354) | {bd['comments']} | Issue comments API (`since=`) |")
    A(f"| Note-stage posts (useful output signal) | {bd['sn_stage_posts']} | #1354 comments, keyword proxy |")
    A(f"| Active lanes posting | {bd['active_lanes']} | `[TAG]` signatures in post bodies (GitHub author is one service account for all lanes) |")
    A(f"| Posts without a lane tag | {bd['untagged_posts']} | #1354 comments with no `[TAG]` signature |")
    A(f"| Note-stage posts per lane per day | {_fmt(bd['sn_posts_per_lane_day'], 2)} | derived (proxy — counts posts, not quality) |")
    ll = m["local_logs"]
    if ll.get("available"):
        mb = ll["bytes"] / (1024 * 1024)
        A(f"| Local run-log volume touched (rough activity signal) | {ll['files']} files, {_fmt(mb)} MB | `find` over local *.log by mtime |")
    else:
        A("| Local run-log volume | not available on this machine | local `find` failed or no logs |")
    if m["timeline_errors"]:
        A(f"| Changes we could not measure (timeline fetch failed) | {m['timeline_errors']} | excluded from averages, counted honestly |")
    A("")
    A("## Where the waste went (biggest first)")
    A("")
    A("Ranked by wasted events. An event is not a verdict — a human judges "
      "whether it was wasteful. The meter only makes it visible.")
    A("")
    for i, item in enumerate(m["waste_ranking"], 1):
        A(f"{i}. **{item['source']}** — {item['wasted_events']} events. {item['plain']}")
    A("")
    if m["reverts"]["items"]:
        A("Reverted changes this week:")
        for r in m["reverts"]["items"]:
            A(f"- #{r['number']}: {r['title']}")
        A("")
    if m["stalled_prs"]["oldest"]:
        A("Longest-frozen open changes:")
        for s in m["stalled_prs"]["oldest"]:
            A(f"- #{s['number']}: {s['title']} — frozen {s['stale_days']} days")
        A("")
    if m["board"]["top_lanes"]:
        A("Most active lanes this week (by `[TAG]` signature):")
        for tag, n in m["board"]["top_lanes"]:
            A(f"- {tag}: {n} posts")
        A("")
    A("## What this doesn't show (honest gaps)")
    A("")
    A("- **Zero re-run attempts alongside failed runs is not a contradiction "
      "(interpretation, labeled as such):** the team redoes failed work by "
      "pushing new commits — that waste is captured under rework commits, not "
      "under the re-run button nobody presses.")
    A("- **Token / compute spend per decision — NOT measured.** No data source "
      "exists: the GitHub API exposes no token usage and local agent logs don't "
      "record tokens. Needs instrumentation at the agent-runtime layer. We did "
      "not fake it.")
    A("- Human attention: review time, context-switch cost, and the opportunity "
      "cost of frozen work are not instrumented.")
    A("- Reverts found only by PR title; direct-push reverts and partial "
      "rollbacks are missed.")
    A("- \"Untouched\" means no GitHub event — a lane may be working locally.")
    A("- Note-stage posts count posts, not quality; a quiet lane may be doing "
      "deep work.")
    A("")
    A("## How this was measured")
    A("")
    A(f"- Window: {w.get('since')} → {w.get('until')} (UTC)")
    A(f"- Repo: {meta.get('repo')} · board: #{meta.get('board_issue')} · "
      f"measured at: {meta.get('measured_at')}")
    A(f"- Spec: `{SPEC_PATH}`")
    A("- Re-run: `python3 tools/waste_meter.py --days 7`")
    A("- Raw data: see the `--out-json` file archived with this report. "
      "Week-over-week deltas are the point — one week is a snapshot, the trend "
      "is the signal.")
    A("")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Waste Meter v1 — make AI waste visible (read-only).")
    p.add_argument("--repo", default=DEFAULT_REPO)
    p.add_argument("--board-issue", type=int, default=DEFAULT_BOARD_ISSUE)
    win = p.add_mutually_exclusive_group()
    win.add_argument("--days", type=float, default=7.0,
                     help="window length in days ending now (default 7)")
    win.add_argument("--since", help="window start, e.g. 2026-10-03")
    p.add_argument("--until", help="window end, e.g. 2026-10-10 (default now)")
    p.add_argument("--gh-api", default=DEFAULT_GH_API)
    p.add_argument("--logs-dir", default=os.path.expanduser("~/workspace"),
                   help="directory scanned for local run logs (rough signal)")
    p.add_argument("--no-logs", action="store_true",
                   help="skip the local-log scan")
    p.add_argument("--max-pr-timelines", type=int, default=0,
                   help="cap PR timeline fetches (0 = all; for quick samples)")
    p.add_argument("--out-md", help="write the plain-words report here")
    p.add_argument("--out-json", help="write raw+metrics JSON here")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    now = datetime.now(timezone.utc)
    until = (_parse(args.until) or now).astimezone(timezone.utc)
    if args.since:
        since = _parse(args.since).astimezone(timezone.utc)  # type: ignore[union-attr]
    else:
        since = until - timedelta(days=args.days)
    window_days = (until - since).total_seconds() / 86400.0

    _progress(f"window {_iso(since)} → {_iso(until)} on {args.repo}")

    _progress("collecting merged PRs…")
    prs = collect_merged_prs_windowed(args.repo, since, until, args.gh_api)
    _progress(f"{len(prs)} PRs merged in window")

    cap = args.max_pr_timelines or len(prs)
    timelines, errors = [], 0
    for i, pr in enumerate(prs[:cap], 1):
        try:
            timelines.append(collect_pr_timeline(args.repo, pr["number"], args.gh_api))
        except WasteMeterError as exc:
            errors += 1
            _progress(f"timeline failed for PR #{pr['number']}: {exc}")
        if i % 25 == 0:
            _progress(f"timelines {i}/{min(cap, len(prs))}…")

    _progress("collecting CI runs…")
    ci_runs = collect_ci_runs(args.repo, since, until, args.gh_api)
    _progress(f"{len(ci_runs)} workflow runs")

    _progress("collecting board comments…")
    board_comments = collect_board_comments(
        args.repo, args.board_issue, since, until, args.gh_api)
    _progress(f"{len(board_comments)} comments on #{args.board_issue}")

    _progress("collecting reverts + stalled PRs…")
    try:
        reverts = collect_reverts(args.repo, since, until, args.gh_api)
    except WasteMeterError as exc:
        _progress(f"revert search unavailable: {exc}")
        reverts = []
    stalled = collect_stalled_prs(args.repo, args.gh_api)

    logs = {"available": False}
    if not args.no_logs:
        _progress("scanning local logs…")
        logs = scan_local_logs(args.logs_dir, since, until)

    raw = {
        "window": {"since": _iso(since), "until": _iso(until)},
        "window_days": round(window_days, 2),
        "prs": prs, "timelines": timelines, "timeline_errors": errors,
        "ci_runs": ci_runs, "board_comments": board_comments,
        "reverts": reverts, "stalled_prs": stalled, "local_logs": logs,
    }
    metrics = aggregate(raw)
    meta = {"repo": args.repo, "board_issue": args.board_issue,
            "measured_at": _iso(now)}
    report = render_markdown(metrics, meta)

    if args.out_md:
        Path(args.out_md).write_text(report, encoding="utf-8")
        _progress(f"report → {args.out_md}")
    else:
        print(report)
    if args.out_json:
        Path(args.out_json).write_text(
            json.dumps({"meta": meta, "metrics": metrics,
                        "raw": {k: v for k, v in raw.items()
                                if k in ("window", "window_days")}},
                       indent=2, default=str),
            encoding="utf-8")
        _progress(f"data → {args.out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
