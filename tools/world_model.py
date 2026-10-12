#!/usr/bin/env python3
"""
World Model — Layer 1 of the Ultimate Decision Machine.

The always-on, always-warm picture of the team's reality. Everything the
decision machine needs to know, already loaded, already fresh.

Tracks:
  1. Open PRs — number, title, CI status, mergeability, age
  2. Lane states — #1713/#1714/#1715: free/occupied, who's in flight
  3. Ledger — #2396: what's proven, what's pending
  4. Mission state — #2154: current priorities, parked items, blockers
  5. Standing laws — from the briefing file (local, no API needed)
  6. Live tip — current main SHA (API-confirmed, cached)

Commands:
  snapshot          Write full JSON snapshot to the model file
  refresh           Incremental update — only fetch what changed
  query <question>  Ask about reality: "which lanes are free?", "merge check #2410"
  status            Show freshness of each section

Query answer contract: factual answers only from FRESH sections (see
FRESHNESS_LIMITS); stale/partial/missing data → UNKNOWN + READ_MORE,
never a positive answer with a warning. Mergeability is never claimed
from the PR list (the list API cannot supply it); "merge check #N"
fetches the per-PR detail endpoint for an evidence-backed verdict.
Briefing headings are cached orientation (BRIEFING_ORIENTATION), never
proof of permission. Exit 0 = answered from fresh data; exit 2 = UNKNOWN.

Design principles:
  - Freshness is the feature. Stale data = wrong decisions.
  - Never guess. Unavailable data → UNKNOWN with timestamp.
  - API economy: check "did it change?" before fetching. LOCAL FIRST.

Usage:
  python3 tools/world_model.py snapshot
  python3 tools/world_model.py refresh
  python3 tools/world_model.py query "what PRs are mergeable?"
  python3 tools/world_model.py status
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = os.path.expanduser("~/workspace/naya/bin/gh-api")

MODEL_PATH = Path(os.path.expanduser("~/.naya/world-model.json"))
BRIEFING_PATH = Path(os.path.expanduser("~/workspace/agent-briefing-master.md"))

LANE_ISSUES = {"alpha": 1713, "beta": 1714, "gamma": 1715}
LEDGER_ISSUE = 2396
MISSION_ISSUE = 2154

# Freshness thresholds (seconds). Data older than this is STALE.
FRESHNESS_LIMITS = {
    "tip": 300,        # 5 min — tip moves fast
    "prs": 600,        # 10 min
    "lanes": 300,      # 5 min — lanes change fast
    "ledger": 1800,    # 30 min
    "mission": 1800,   # 30 min
    "laws": 86400,     # 24 h — laws change rarely
}

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def utc_now_ts():
    return time.time()


def gh_api(method, path, body_file=None):
    """Call gh-api. Returns (ok, data_or_error)."""
    cmd = [GH_API, method, path]
    if body_file:
        cmd += ["--body-file", body_file]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False, f"gh-api exit {result.returncode}: {result.stderr[:200]}"
        try:
            return True, json.loads(result.stdout)
        except json.JSONDecodeError:
            return False, f"non-JSON response: {result.stdout[:200]}"
    except subprocess.TimeoutExpired:
        return False, "gh-api timed out"
    except Exception as e:
        return False, f"gh-api error: {e}"


def load_model():
    """Load the cached model, or return empty structure."""
    if MODEL_PATH.exists():
        try:
            return json.loads(MODEL_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return empty_model()


def empty_model():
    return {
        "version": 1,
        "created_utc": now_utc(),
        "sections": {},
    }


def save_model(model):
    # Atomic write: temp file + os.replace, so concurrent scheduled
    # writers can never leave a half-written model behind.
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = MODEL_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(model, indent=2))
    os.replace(tmp, MODEL_PATH)
    return str(MODEL_PATH)


def section_status(data_ts, limit):
    """Return freshness: FRESH, STALE, or UNKNOWN."""
    if data_ts is None:
        return "UNKNOWN"
    age = utc_now_ts() - data_ts
    if age <= limit:
        return "FRESH"
    return "STALE"


def mark_unknown(section_name, reason):
    """Build an UNKNOWN section — never guess."""
    return {
        "status": "UNKNOWN",
        "reason": reason,
        "as_of_utc": now_utc(),
        "as_of_ts": utc_now_ts(),
    }


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------


def build_tip_section(cached=None):
    """Live tip — API-confirmed main SHA."""
    ok, data = gh_api("GET", f"/repos/{REPO}/git/refs/heads/main")
    if not ok:
        s = mark_unknown("tip", f"API failed: {data}")
        # Keep last-known SHA if we have it, marked stale
        if cached and cached.get("sha"):
            s["last_known_sha"] = cached["sha"]
            s["last_known_utc"] = cached.get("as_of_utc")
        return s
    sha = data.get("object", {}).get("sha", "")
    return {
        "status": "OK",
        "sha": sha,
        "short": sha[:8] if sha else "",
        "as_of_utc": now_utc(),
        "as_of_ts": utc_now_ts(),
    }


def build_prs_section(cached=None):
    """Open PRs — number, title, age. Handles pagination.

    GitHub's PR LIST endpoint never returns `mergeable` — it is only computed
    on the per-PR detail endpoint. This builder therefore records
    mergeable=None for every PR from list data (P0-F2: never assert readiness
    from list data). Mergeability verdicts come from the on-demand
    `query "merge check #N"` path, which fetches /pulls/{n}.
    """
    prs = []
    page = 1
    partial_reason = None
    failed_page = None
    truncated = False
    while True:
        ok, data = gh_api(
            "GET",
            f"/repos/{REPO}/pulls?state=open&per_page=100&page={page}",
        )
        if not ok:
            if page == 1:
                return mark_unknown("prs", f"API failed: {data}")
            # P0-F3: pagination failed mid-way — PARTIAL, never OK.
            partial_reason = f"API failed on page {page}: {data}"
            failed_page = page
            break
        if not data:
            break
        for pr in data:
            prs.append({
                "number": pr.get("number"),
                "title": pr.get("title", "")[:120],
                "head_sha": (pr.get("head") or {}).get("sha", "")[:8],
                "head_branch": (pr.get("head") or {}).get("ref", ""),
                # P0-F2: the list response has no mergeable field. Record None
                # and never let it read as a readiness claim.
                "mergeable": None,
                "mergeable_source": "list-data-never-knows",
                "draft": pr.get("draft", False),
                "created_at": pr.get("created_at", ""),
                "user": (pr.get("user") or {}).get("login", ""),
            })
        if len(data) < 100:
            break
        page += 1
        if page > 10:  # safety cap: 1000 PRs max
            truncated = True
            break

    if partial_reason or truncated:
        # P0-F3: partial data is PARTIAL. Counts are LOWER BOUNDS, never
        # totals. No closed-world conclusions ("only X PRs") may be drawn.
        return {
            "status": "PARTIAL",
            "reason": partial_reason or "capped at 1000 PRs",
            "fetch_failed_page": failed_page,
            "truncated": truncated,
            "pr_count_lower_bound": len(prs),
            "prs": prs,
            "as_of_utc": now_utc(),
            "as_of_ts": utc_now_ts(),
        }

    return {
        "status": "OK",
        "count": len(prs),
        "prs": prs,
        "as_of_utc": now_utc(),
        "as_of_ts": utc_now_ts(),
    }


def build_lanes_section(cached=None):
    """Lane states — free/occupied from sign-in/out comments."""
    lanes = {}
    for name, issue_num in LANE_ISSUES.items():
        # Get issue to find comment count (cheap change detection)
        ok, issue = gh_api("GET", f"/repos/{REPO}/issues/{issue_num}")
        if not ok:
            lanes[name] = {"status": "UNKNOWN", "reason": f"API failed: {issue}"}
            continue

        comment_count = issue.get("comments", 0)

        # Check cache: if comment count unchanged, lane state is unchanged
        cached_lane = (cached or {}).get(name, {})
        if cached_lane.get("comment_count") == comment_count and cached_lane.get("state"):
            lanes[name] = cached_lane
            continue

        # Comment count changed — fetch last page to determine state
        per_page = 30
        last_page = max(1, (comment_count + per_page - 1) // per_page)
        ok, comments = gh_api(
            "GET",
            f"/repos/{REPO}/issues/{issue_num}/comments?per_page={per_page}&page={last_page}",
        )
        if not ok or not comments:
            lanes[name] = {
                "status": "UNKNOWN",
                "reason": "could not read comments",
                "comment_count": comment_count,
            }
            continue

        # Determine state from most recent sign-in/sign-out.
        # Sign-in takes precedence over sign-out when both words appear in one
        # body: a worker's sign-in comment routinely cites the prior sign-out
        # ("lane free — last sign-out 01:31Z"), so the body's intent is a
        # sign-in. Checking "sign-out" first misreported a lane as FREE while
        # a worker was in flight (IV, 2026-10-12).
        state = "UNKNOWN"
        occupant = ""
        last_activity = ""
        for c in reversed(comments):
            body = (c.get("body") or "").lower()
            created = c.get("created_at", "")
            if "sign-in" in body or "signin" in body:
                state = "OCCUPIED"
                # Extract who's in flight from the body
                first_line = (c.get("body") or "").split("\n")[0][:120]
                occupant = first_line
                last_activity = created
                break
            elif "sign-out" in body or "signout" in body:
                state = "FREE"
                last_activity = created
                break

        lanes[name] = {
            "status": "OK",
            "issue": issue_num,
            "state": state,
            "occupant": occupant,
            "last_activity": last_activity,
            "comment_count": comment_count,
            "as_of_utc": now_utc(),
            "as_of_ts": utc_now_ts(),
        }

    return {
        "status": "OK",
        "lanes": lanes,
        "lease_note": "OBSERVED coordination only — not a mutex. Two workers can "
                      "claim a lane simultaneously; FREE is a reading of the last "
                      "comment, not dispatch authorization. Re-read the live "
                      "feed before acting.",
        "as_of_utc": now_utc(),
        "as_of_ts": utc_now_ts(),
    }


def build_ledger_section(cached=None):
    """Ledger #2396 — what's proven, what's pending."""
    ok, issue = gh_api("GET", f"/repos/{REPO}/issues/{LEDGER_ISSUE}")
    if not ok:
        return mark_unknown("ledger", f"API failed: {issue}")

    return {
        "status": "OK",
        "issue": LEDGER_ISSUE,
        "title": issue.get("title", ""),
        "state": issue.get("state", ""),
        "comment_count": issue.get("comments", 0),
        "updated_at": issue.get("updated_at", ""),
        "url": issue.get("html_url", ""),
        "as_of_utc": now_utc(),
        "as_of_ts": utc_now_ts(),
    }


def build_mission_section(cached=None):
    """Mission state #2154 — current priorities, parked items, blockers."""
    ok, issue = gh_api("GET", f"/repos/{REPO}/issues/{MISSION_ISSUE}")
    if not ok:
        return mark_unknown("mission", f"API failed: {issue}")

    body = issue.get("body") or ""
    return {
        "status": "OK",
        "issue": MISSION_ISSUE,
        "title": issue.get("title", ""),
        "state": issue.get("state", ""),
        "comment_count": issue.get("comments", 0),
        "updated_at": issue.get("updated_at", ""),
        "body_preview": body[:2000],
        "url": issue.get("html_url", ""),
        "as_of_utc": now_utc(),
        "as_of_ts": utc_now_ts(),
    }


def build_laws_section(cached=None):
    """Standing laws — from the briefing file (local, no API).

    P0-F4: briefing headings are ORIENTATION, not law. They do not prove
    permission, ratification, or grant freshness. The section is marked
    BRIEFING_ORIENTATION, and any query touching permission/authority/consent
    must live re-read the authoritative source or carry an explicit
    "cached — verify before acting" marker.
    """
    if not BRIEFING_PATH.exists():
        return mark_unknown("laws", "briefing file not found")

    try:
        content = BRIEFING_PATH.read_text()
    except OSError as e:
        return mark_unknown("laws", f"could not read briefing: {e}")

    # Extract law markers — lines that look like laws
    laws = []
    for i, line in enumerate(content.split("\n"), 1):
        stripped = line.strip()
        # Law markers: numbered laws, L-codes, or ALL-CAPS headers
        if stripped.startswith("## "):
            laws.append({"line": i, "header": stripped[3:][:80]})
        elif "(L" in stripped and "—" in stripped and len(stripped) < 200:
            laws.append({"line": i, "law": stripped[:120]})

    import hashlib
    sha = hashlib.sha256(content.encode()).hexdigest()[:12]

    return {
        "status": "OK",
        "source_kind": "BRIEFING_ORIENTATION",
        "source": str(BRIEFING_PATH),
        "sha12": sha,
        "line_count": len(content.split("\n")),
        "headers": [l["header"] for l in laws if "header" in l][:30],
        "cached_note": "CACHED — verify before acting. Headings are orientation, "
                       "not proof of permission, ratification, or grant.",
        "permission_evidence": False,
        "as_of_utc": now_utc(),
        "as_of_ts": utc_now_ts(),
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

SECTION_BUILDERS = {
    "tip": build_tip_section,
    "prs": build_prs_section,
    "lanes": build_lanes_section,
    "ledger": build_ledger_section,
    "mission": build_mission_section,
    "laws": build_laws_section,
}


def cmd_snapshot(args):
    """Full snapshot — fetch everything."""
    model = empty_model()
    model["snapshot_utc"] = now_utc()

    for name, builder in SECTION_BUILDERS.items():
        print(f"  fetching {name}...", file=sys.stderr)
        try:
            model["sections"][name] = builder()
        except Exception as e:
            model["sections"][name] = mark_unknown(name, f"builder error: {e}")

    path = save_model(model)
    print(f"Snapshot written to {path}")

    # Summary
    for name, section in model["sections"].items():
        status = section.get("status", "?")
        detail = ""
        if name == "tip" and status == "OK":
            detail = section.get("short", "")
        elif name == "prs" and status == "OK":
            detail = f"{section.get('count', 0)} open"
        elif name == "lanes" and status == "OK":
            states = {k: v.get("state", "?") for k, v in section.get("lanes", {}).items()}
            detail = str(states)
        print(f"  {name}: {status} {detail}")
    return 0


def cmd_refresh(args):
    """Incremental refresh — only fetch what changed or is stale."""
    model = load_model()
    cached_sections = model.get("sections", {})
    now = utc_now_ts()
    refreshed = []
    skipped = []
    failed = []

    for name, builder in SECTION_BUILDERS.items():
        cached = cached_sections.get(name, {})
        cached_ts = cached.get("as_of_ts")
        limit = FRESHNESS_LIMITS.get(name, 600)

        # Skip if fresh (but always re-check tip — it's cheap and critical)
        if name != "tip" and cached_ts and (now - cached_ts) < limit:
            skipped.append(name)
            continue

        # For lanes: cheap change detection via comment count is inside builder
        # For laws: local file, always cheap — but check mtime first
        if name == "laws" and cached.get("sha12"):
            try:
                import hashlib
                current = hashlib.sha256(BRIEFING_PATH.read_bytes()).hexdigest()[:12]
                if current == cached["sha12"]:
                    skipped.append(name)
                    continue
            except OSError:
                pass

        print(f"  refreshing {name}...", file=sys.stderr)
        try:
            new_section = builder(cached if name == "lanes" else None)
            if new_section.get("status") == "UNKNOWN" and cached.get("status") == "OK":
                # API failed but we have cached data — keep cached, mark stale
                cached["freshness"] = "STALE"
                cached["stale_reason"] = new_section.get("reason", "refresh failed")
                # Don't overwrite good data with UNKNOWN
            else:
                cached_sections[name] = new_section
                refreshed.append(name)
        except Exception as e:
            failed.append(f"{name}: {e}")

    # Annotate freshness
    for name, section in cached_sections.items():
        ts = section.get("as_of_ts")
        limit = FRESHNESS_LIMITS.get(name, 600)
        section["freshness"] = section_status(ts, limit)

    model["sections"] = cached_sections
    model["last_refresh_utc"] = now_utc()
    path = save_model(model)

    print(f"Model saved to {path}")
    print(f"  refreshed: {refreshed or 'none'}")
    print(f"  skipped (fresh): {skipped or 'none'}")
    if failed:
        print(f"  failed: {failed}")
    return 0


def cmd_status(args):
    """Show freshness of each section."""
    model = load_model()
    sections = model.get("sections", {})
    if not sections:
        print("No snapshot. Run `snapshot` first.")
        return 1

    now = utc_now_ts()
    print(f"World model — last refresh: {model.get('last_refresh_utc', 'never')}")
    print()
    for name in SECTION_BUILDERS:
        section = sections.get(name, {})
        ts = section.get("as_of_ts")
        limit = FRESHNESS_LIMITS.get(name, 600)
        freshness = section_status(ts, limit)
        age = f"{int(now - ts)}s ago" if ts else "never"
        status = section.get("status", "?")
        print(f"  {name:8s} {freshness:7s} ({status}) — updated {age}")
    return 0


def section_usable(name, sections):
    """Can this section support positive factual answers?

    P0-F1: a section is usable only when status == "OK" AND it is FRESH
    (younger than FRESHNESS_LIMITS[name]). PARTIAL sections carry a lower
    bound, never a total. STALE/UNKNOWN sections can never satisfy a
    scoring predicate — the answer must be UNKNOWN with a READ_MORE
    directive (e.g. run `refresh`), never a positive answer with a
    warning footnote.

    Returns (usable: bool, state: str) where state is one of
    FRESH / STALE / UNKNOWN / PARTIAL.
    """
    section = sections.get(name, {})
    if section.get("status") == "PARTIAL":
        return False, "PARTIAL"
    if section.get("status") != "OK":
        return False, section.get("status", "UNKNOWN") or "UNKNOWN"
    ts = section.get("as_of_ts")
    limit = FRESHNESS_LIMITS.get(name, 600)
    freshness = section_status(ts, limit)
    if freshness != "FRESH":
        return False, freshness  # STALE or UNKNOWN
    return True, "FRESH"


def unknown_with_directive(section_name, state, sections):
    """Standard UNKNOWN answer with a READ_MORE directive."""
    section = sections.get(section_name, {})
    ts = section.get("as_of_ts")
    age = f"{int(utc_now_ts() - ts)}s" if ts else "never fetched"
    reason = section.get("reason", "")
    extra = f" Reason: {reason}" if reason else ""
    return (
        f"UNKNOWN — {section_name} data is {state} (age: {age}).{extra}\n"
        f"READ_MORE: run `refresh` (or `snapshot`), then re-query. "
        f"No positive answer can be given from {state} data."
    )


def cmd_query(args):
    """Answer questions about reality.

    QUERY ANSWER CONTRACT (P0-F1..F4):
    - A section answers factual questions only while FRESH (see
      FRESHNESS_LIMITS, documented below). STALE/UNKNOWN/PARTIAL data
      yields UNKNOWN + a READ_MORE directive — never a positive answer
      with a warning footnote.
    - Mergeability is NEVER claimed from PR list data (P0-F2). Use
      `query "merge check #N"` for a per-PR detail verdict with evidence.
    - Totals are never stated from PARTIAL data (P0-F3) — only lower bounds.
    - Permission/authority/consent questions are never answered from cached
      briefing headings (P0-F4) — they need live authority state.
    - Verdicts in answers: OBSERVED (fresh data), HISTORICAL (last-known,
      explicitly not current), UNKNOWN, READ_MORE.
    - Exit codes: 0 = answered from fresh data; 2 = UNKNOWN or READ_MORE.

    FRESHNESS THRESHOLDS (FRESHNESS_LIMITS, seconds) — honest by design:
      tip 300 (tip moves fast) · prs 600 · lanes 300 (lanes change fast) ·
      ledger 1800 · mission 1800 · laws 86400 (rarely changes).
    """
    question = " ".join(args.question).lower()
    model = load_model()
    sections = model.get("sections", {})
    if not sections:
        print("No snapshot. Run `snapshot` first.")
        return 2

    answer = None
    unknown = False

    def mark_unknown_answer(text):
        nonlocal answer, unknown
        answer = text
        unknown = True

    # P0-F2: mergeability from the LIST is a lie the API cannot tell.
    # Only a per-PR detail fetch qualifies as evidence.
    if "merge check" in question:
        import re
        m = re.search(r"#?(\d+)", question)
        if not m:
            mark_unknown_answer('READ_MORE: specify a PR — query "merge check #2410"')
        else:
            pr_num = m.group(1)
            usable, state = section_usable("prs", sections)
            if not usable:
                mark_unknown_answer(
                    f"UNKNOWN — cannot verify PR #{pr_num} is even open: "
                    f"prs data is {state}.\n"
                    f"READ_MORE: run `refresh`, then re-query."
                )
            else:
                ok, pr_data = gh_api("GET", f"/repos/{REPO}/pulls/{pr_num}")
                if not ok:
                    mark_unknown_answer(
                        f"UNKNOWN — per-PR detail fetch failed for #{pr_num}: "
                        f"{pr_data}\nREAD_MORE: retry the fetch; no verdict "
                        f"without evidence."
                    )
                else:
                    mergeable = pr_data.get("mergeable")
                    mstate = pr_data.get("mergeable_state", "?")
                    full_sha = (pr_data.get("head") or {}).get("sha", "")
                    fetched = now_utc()
                    title = pr_data.get("title", "")[:80]
                    if mergeable is True:
                        answer = (
                            f"OBSERVED — PR #{pr_num} ({title}):\n"
                            f"  GitHub mergeability: TRUE (mergeable_state: {mstate})\n"
                            f"  head: {full_sha[:8]} — evidence fetched {fetched}\n"
                            f"  NOTE: this is GitHub's mechanical computation, NOT a "
                            f"merge authorization. CI status + team gates still decide."
                        )
                    elif mergeable is False:
                        answer = (
                            f"OBSERVED — PR #{pr_num} ({title}):\n"
                            f"  GitHub mergeability: FALSE (mergeable_state: {mstate})\n"
                            f"  head: {full_sha[:8]} — evidence fetched {fetched}\n"
                            f"  NOTE: this is GitHub's mechanical computation, NOT a "
                            f"merge authorization."
                        )
                    else:
                        mark_unknown_answer(
                            f"UNKNOWN — GitHub has not computed mergeability for "
                            f"PR #{pr_num} yet (mergeable: null).\n"
                            f"READ_MORE: retry later; do not treat as mergeable."
                        )

    elif any(w in question for w in ["mergeable", "can merge", "ready to merge"]):
        # P0-F2: the list can never answer this. Say so, point at the
        # evidence path. Even fresh list data → READ_MORE.
        usable, state = section_usable("prs", sections)
        if not usable:
            mark_unknown_answer(unknown_with_directive("prs", state, sections))
        else:
            mark_unknown_answer(
                'READ_MORE — mergeability is not knowable from the PR list '
                "(GitHub's list API never returns `mergeable`).\n"
                'Ask: query "merge check #N" for a per-PR verdict with evidence.'
            )

    elif any(w in question for w in ["free lane", "lanes free", "which lanes", "lane state", "lanes are"]):
        usable, state = section_usable("lanes", sections)
        if not usable:
            mark_unknown_answer(unknown_with_directive("lanes", state, sections))
        else:
            lanes = sections.get("lanes", {})
            lines = ["OBSERVED — lane states:"]
            for name, lane in lanes.get("lanes", {}).items():
                if lane.get("status") != "OK":
                    lines.append(f"  #{name}: UNKNOWN ({lane.get('reason', 'no data')})")
                    continue
                lstate = lane.get("state", "?")
                extra = f" ({lane.get('occupant', '')[:60]})" if lstate == "OCCUPIED" else ""
                lines.append(f"  #{name} ({lane.get('issue', '?')}): {lstate}{extra}")
            if lanes.get("lease_note"):
                lines.append(f"  NOTE: {lanes['lease_note']}")
            answer = "\n".join(lines)

    elif any(w in question for w in ["open pr", "how many pr", "pr count", "prs open"]):
        prs = sections.get("prs", {})
        usable, state = section_usable("prs", sections)
        if state == "PARTIAL":
            # P0-F3: lower bound only, never a total.
            lb = prs.get("pr_count_lower_bound", len(prs.get("prs", [])))
            mark_unknown_answer(
                f"UNKNOWN — PR data is PARTIAL ({prs.get('reason', 'pagination failed')}).\n"
                f"At least {lb} PRs seen (lower bound, not a total).\n"
                f"READ_MORE: run `snapshot` again for a complete count."
            )
        elif not usable:
            mark_unknown_answer(unknown_with_directive("prs", state, sections))
        else:
            lines = [f"OBSERVED — {prs.get('count', 0)} open PRs:"]
            for p in prs.get("prs", [])[:20]:
                lines.append(f"  #{p['number']} — {p['title'][:60]} ({p.get('head_branch', '')})")
            answer = "\n".join(lines)

    elif any(w in question for w in ["tip", "main sha", "current main", "latest"]):
        usable, state = section_usable("tip", sections)
        tip = sections.get("tip", {})
        if not usable:
            # P0-F1: stale tip → UNKNOWN. Last-known data goes in a clearly
            # HISTORICAL field, never as the answer.
            ts = tip.get("as_of_ts")
            age = f"{int(utc_now_ts() - ts)}s" if ts else "never fetched"
            msg = (f"UNKNOWN — live tip is {state} (age: {age}). "
                   f"Run `refresh` for the current tip.")
            if tip.get("last_known_sha") or tip.get("sha"):
                known = (tip.get("last_known_sha") or tip.get("sha", ""))[:8]
                known_utc = tip.get("last_known_utc") or tip.get("as_of_utc", "?")
                msg += (f"\nHISTORICAL (not current): {known} seen at {known_utc}.")
            mark_unknown_answer(msg)
        else:
            answer = (f"OBSERVED — live tip: {tip.get('sha', '')} "
                      f"(as of {tip.get('as_of_utc', '?')})")

    elif any(w in question for w in ["allowed", "permission", "authorized", "consent",
                                     "do i have", "can i ", "may i "]):
        # P0-F4: permission/authority/consent questions are never answered
        # from cached briefing headings. Live authority state or nothing.
        mark_unknown_answer(
            "UNKNOWN — the world model does not hold live authority state.\n"
            "Briefing headings are cached orientation (BRIEFING_ORIENTATION), "
            "not grants, ratifications, or permissions.\n"
            "READ_MORE: check the live authority source before acting. "
            "Never treat a cached heading as permission."
        )

    elif any(w in question for w in ["mission", "priorit", "blocker", "parked"]):
        usable, state = section_usable("mission", sections)
        if not usable:
            mark_unknown_answer(unknown_with_directive("mission", state, sections))
        else:
            mission = sections.get("mission", {})
            answer = (
                f"OBSERVED — mission state (#{mission.get('issue')}):\n"
                f"  Title: {mission.get('title', '')}\n"
                f"  Updated: {mission.get('updated_at', '')}\n"
                f"  Preview:\n{mission.get('body_preview', '')[:1000]}"
            )

    elif any(w in question for w in ["ledger", "proven"]):
        usable, state = section_usable("ledger", sections)
        if not usable:
            mark_unknown_answer(unknown_with_directive("ledger", state, sections))
        else:
            ledger = sections.get("ledger", {})
            answer = (
                f"OBSERVED — ledger (#{ledger.get('issue')}):\n"
                f"  Title: {ledger.get('title', '')}\n"
                f"  Comments: {ledger.get('comment_count', 0)}\n"
                f"  Updated: {ledger.get('updated_at', '')}\n"
                f"  URL: {ledger.get('url', '')}"
            )

    elif any(w in question for w in ["law", "protected", "gate"]):
        usable, state = section_usable("laws", sections)
        if not usable:
            mark_unknown_answer(unknown_with_directive("laws", state, sections))
        else:
            laws = sections.get("laws", {})
            headers = laws.get("headers", [])[:15]
            # P0-F4: every law answer carries the cached marker.
            answer = (
                "CACHED ORIENTATION — verify before acting. These headings are "
                "not proof of permission, ratification, or grant.\n"
                "Standing laws (from briefing):\n"
                + "\n".join(f"  - {h}" for h in headers)
            )

    elif "ci status" in question or "check status" in question:
        # On-demand CI status for a specific PR — avoids bulk API cost
        import re
        m = re.search(r"#?(\d+)", question)
        if not m:
            mark_unknown_answer('READ_MORE: Specify a PR — query "ci status #2410"')
        else:
            pr_num = m.group(1)
            usable, state = section_usable("prs", sections)
            if not usable:
                mark_unknown_answer(unknown_with_directive("prs", state, sections))
            else:
                prs = sections.get("prs", {})
                target = None
                for p in prs.get("prs", []):
                    if str(p.get("number")) == pr_num:
                        target = p
                        break
                if not target:
                    mark_unknown_answer(f"UNKNOWN — PR #{pr_num} not in model.")
                else:
                    ok, pr_data = gh_api("GET", f"/repos/{REPO}/pulls/{pr_num}")
                    if not ok:
                        mark_unknown_answer(f"UNKNOWN — could not fetch PR #{pr_num}: {pr_data}")
                    else:
                        full_sha = (pr_data.get("head") or {}).get("sha", "")
                        ok, checks = gh_api(
                            "GET",
                            f"/repos/{REPO}/commits/{full_sha}/check-runs?per_page=100",
                        )
                        if not ok:
                            mark_unknown_answer(f"UNKNOWN — could not fetch checks: {checks}")
                        else:
                            runs = checks.get("check_runs", [])
                            if not runs:
                                answer = f"PR #{pr_num}: no check runs found."
                            else:
                                lines = [f"OBSERVED — PR #{pr_num} CI status ({len(runs)} checks):"]
                                for r in runs[:20]:
                                    name = r.get("name", "?")[:50]
                                    status = r.get("status", "?")
                                    conclusion = r.get("conclusion", "")
                                    icon = "✅" if conclusion == "success" else "❌" if conclusion in ("failure", "timed_out") else "⏳"
                                    lines.append(f"  {icon} {name}: {status}/{conclusion}")
                                answer = "\n".join(lines)

    else:
        mark_unknown_answer(
            "UNKNOWN — I don't know how to answer that yet. Try:\n"
            '  query "what PRs are mergeable?"\n'
            '  query "merge check #2410"\n'
            '  query "which lanes are free?"\n'
            '  query "how many PRs are open?"\n'
            '  query "what is the live tip?"\n'
            '  query "what is the mission state?"\n'
            '  query "what does the ledger say?"\n'
            '  query "what are the standing laws?"'
        )

    print(answer)
    return 2 if unknown else 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    cmd = sys.argv[1]
    args = type("Args", (), {"question": sys.argv[2:]})()

    handlers = {
        "snapshot": cmd_snapshot,
        "refresh": cmd_refresh,
        "query": cmd_query,
        "status": cmd_status,
    }

    handler = handlers.get(cmd)
    if not handler:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print("Commands: snapshot, refresh, query, status", file=sys.stderr)
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
