"""Checklist sync — the living checklist engine.

WHY THIS EXISTS
---------------
Shawn's order (2026-10-09): "Without that [checklist] she has no chance."
A static markdown checklist goes stale the moment someone forgets to update
it. This script makes the checklist self-maintaining:

1. AUTO-STATUS FROM PRs — for every item with pr_refs, checks the live PR
   state via GitHub API. Merged → DONE (with SHA). Open + CI green →
   IN PROGRESS. Open + CI red → BLOCKED (with failure detail). Closed
   unmerged → TODO (with note). No human needed for PR-driven updates.

2. STALE DETECTION — IN PROGRESS items with no update in 48h and no PR
   movement get flagged STALE and posted to #1354. No silent stalls.

3. MD REGENERATION — BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md is
   GENERATED from ACTIVATION-CHECKLIST.json. The JSON is the single source
   of truth. Never hand-edit the .md.

USAGE
-----
    python3 tools/checklist_sync.py [--dry-run] [--check-stale-only]

    --dry-run: show what would change, don't write
    --check-stale-only: skip PR checks, only run staleness detection

Exit codes: 0 = ok (changes or no changes), 2 = GitHub API failure,
3 = JSON invalid (do not proceed on corrupt data).

Stdlib only. Uses ~/workspace/skills/github/bin/gh-api when available.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = "/home/hatch/workspace/skills/github/bin/gh-api"
BOARD_ISSUE = 1354

# Paths relative to repo root. When run from repo root, these resolve directly.
JSON_PATH = "BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.json"
MD_PATH = "BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md"

STALE_HOURS = 48


def now_utc():
    return datetime.now(timezone.utc)


def parse_time(s):
    """Parse ISO timestamp, return aware datetime or None."""
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def gh_get(path):
    """GET via gh-api CLI. Returns parsed JSON or raises."""
    result = subprocess.run(
        [GH_API, "GET", path],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh-api GET {path} failed: {result.stderr[:500]}")
    return json.loads(result.stdout)


def get_pr_state(pr_number):
    """Return (state, merged, merge_sha, merged_at, ci_verdict, ci_detail)."""
    pr = gh_get(f"/repos/{REPO}/pulls/{pr_number}")
    state = pr.get("state", "unknown")  # open / closed
    merged = bool(pr.get("merged_at"))
    merge_sha = (pr.get("merge_commit_sha") or "")[:8] if merged else ""
    merged_at = pr.get("merged_at", "")

    # CI verdict from check runs on head SHA
    ci_verdict = "unknown"
    ci_detail = ""
    try:
        head_sha = pr["head"]["sha"]
        checks = gh_get(
            f"/repos/{REPO}/commits/{head_sha}/check-runs?per_page=100"
        )
        runs = checks.get("check_runs", [])
        if not runs:
            ci_verdict = "no_checks"
        else:
            conclusions = [r.get("conclusion") for r in runs]
            failures = [r.get("name") for r in runs
                        if r.get("conclusion") == "failure"]
            if failures:
                ci_verdict = "red"
                ci_detail = f"failed: {', '.join(failures[:5])}"
            elif all(c in ("success", "skipped", "neutral") for c in conclusions):
                ci_verdict = "green"
            elif any(c in ("in_progress", "queued", "waiting") for c in conclusions):
                ci_verdict = "pending"
            else:
                ci_verdict = "mixed"
                ci_detail = f"conclusions: {set(conclusions)}"
    except Exception as e:
        ci_detail = f"check-run fetch failed: {e}"[:200]

    return {
        "state": state,
        "merged": merged,
        "merge_sha": merge_sha,
        "merged_at": merged_at,
        "ci_verdict": ci_verdict,
        "ci_detail": ci_detail,
    }


def derive_status(item, pr_states):
    """Compute (status, status_detail) from live PR states.

    Rules:
    - Any pr_ref merged → DONE (all must merge for multi-PR items;
      if some merged and some open, IN PROGRESS with note)
    - All open + all CI green → IN PROGRESS
    - Any open + CI red → BLOCKED (failure detail)
    - Any closed-unmerged → TODO (note which)
    - No pr_refs → leave manual (return None)
    """
    pr_refs = item.get("pr_refs", [])
    if not pr_refs:
        return None  # manual item, sync doesn't touch

    merged = []
    open_green = []
    open_red = []
    open_pending = []
    closed_unmerged = []
    unknown = []

    for num in pr_refs:
        ps = pr_states.get(num)
        if not ps:
            unknown.append(num)
            continue
        if ps["merged"]:
            merged.append((num, ps["merge_sha"]))
        elif ps["state"] == "closed":
            closed_unmerged.append(num)
        elif ps["state"] == "open":
            if ps["ci_verdict"] == "green":
                open_green.append(num)
            elif ps["ci_verdict"] == "red":
                open_red.append((num, ps["ci_detail"]))
            else:
                open_pending.append((num, ps["ci_verdict"]))

    ts = now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")

    if unknown:
        return None  # API failure for these; don't touch

    if closed_unmerged and not merged and not open_green and not open_red:
        detail = (f"PR(s) {closed_unmerged} closed unmerged — needs new plan "
                  f"(checked {ts})")
        return ("TODO", detail)

    if open_red:
        parts = [f"#{n} CI red ({d})" for n, d in open_red]
        detail = f"BLOCKED: {'; '.join(parts)} (checked {ts})"
        return ("BLOCKED", detail)

    if merged and not open_green and not open_red and not open_pending:
        shas = ", ".join(f"#{n}@{s}" for n, s in merged)
        detail = f"Merged {shas} (checked {ts})"
        return ("DONE", detail)

    if merged and (open_green or open_pending):
        detail = (f"Partially merged ({', '.join('#'+str(n) for n, _ in merged)}); "
                  f"still open: {open_green + [n for n, _ in open_pending]} "
                  f"(checked {ts})")
        return ("IN PROGRESS", detail)

    if open_green or open_pending:
        detail = f"Open, CI green/pending (checked {ts})"
        return ("IN PROGRESS", detail)

    return None


def check_stale(item, section_title):
    """Return stale alert string if item qualifies, else None."""
    if item.get("status") != "IN PROGRESS":
        return None
    if item.get("shawn_gated"):
        return None  # Shawn gates wait on him, not stalls
    updated = parse_time(item.get("updated_at"))
    if not updated:
        return None
    age = now_utc() - updated
    if age > timedelta(hours=STALE_HOURS):
        hours = int(age.total_seconds() // 3600)
        return (f"[CHECKLIST] Item {item['id']} ({section_title}) stuck "
                f"IN PROGRESS for {hours}h — needs attention. "
                f"Owner: {item.get('owner', '?')}. "
                f"Last update: {item.get('updated_at')}. "
                f"Detail: {item.get('status_detail', '')[:200]}")
    return None


def post_to_board(body):
    """Post a comment to the main board (#1354)."""
    import tempfile
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False) as f:
        json.dump({"body": body}, f)
        tmp = f.name
    try:
        result = subprocess.run(
            [GH_API, "POST",
             f"/repos/{REPO}/issues/{BOARD_ISSUE}/comments",
             f"@{tmp}"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"WARN: board post failed: {result.stderr[:300]}",
                  file=sys.stderr)
            return None
        return json.loads(result.stdout).get("html_url")
    finally:
        os.unlink(tmp)


def generate_md(data):
    """Generate the human-readable markdown from the JSON data."""
    meta = data["meta"]
    lines = []
    lines.append("# Master Checklist — Activation to Production")
    lines.append("")
    lines.append(f"**Owner:** {meta['owner']}")
    lines.append(f"**Created:** {meta['created']} (Shawn's direct order)")
    lines.append(f"**Canonical location:** `{meta['canonical_md']}`")
    lines.append(f"**Source of truth:** `{meta['canonical_json']}` "
                 f"(this file is GENERATED — do not hand-edit)")
    lines.append(f"**Status as of:** {meta['updated_at']}")
    if meta.get("main_tip_at_update"):
        lines.append(f"**Main tip at update:** `{meta['main_tip_at_update']}`")
    lines.append("")
    lines.append("## How to read this")
    lines.append("")
    lines.append("- Each item: **WHAT**, **WHY**, **DONE WHEN** (exact verifiable "
                 "criteria), **STATUS**, **OWNER**.")
    lines.append("- DONE WHEN must be checkable by a cold reader against GitHub "
                 "bytes. No \"looks good.\"")
    lines.append("- Living document: STATUS auto-updates from PR state every 30min "
                 "via `tools/checklist_sync.py`. Manual updates via "
                 "`tools/checklist_update.py`. Never delete items — check them off.")
    lines.append("")

    for section in data["sections"]:
        lines.append("---")
        lines.append("")
        header = f"## {section['title']}"
        extras = []
        if section.get("current_score"):
            extras.append(f"current {section['current_score']}")
        if section.get("target_score"):
            extras.append(f"target {section['target_score']}")
        if section.get("feed"):
            extras.append(f"feed {section['feed']}")
        if extras:
            header += f" — {' → '.join(extras[:2])}"
            if len(extras) > 2:
                header += f" — {extras[2]}"
        lines.append(header)
        lines.append("")
        if section.get("done_when"):
            lines.append(f"**Section DONE WHEN:** {section['done_when']}")
            lines.append("")
        if section.get("owner"):
            lines.append(f"**Owner:** {section['owner']}")
            lines.append("")

        for item in section.get("items", []):
            status_icon = {"DONE": "✅", "IN PROGRESS": "🔄",
                           "BLOCKED": "🚫", "TODO": "⬜",
                           "STALE": "⚠️"}.get(item["status"], "❓")
            lines.append(f"### {status_icon} {item['id']}. "
                         f"{item['what'][:100]}")
            lines.append(f"- **WHAT:** {item['what']}")
            if item.get("why"):
                lines.append(f"- **WHY:** {item['why']}")
            lines.append(f"- **DONE WHEN:** {item['done_when']}")
            lines.append(f"- **STATUS:** {item['status']}")
            if item.get("status_detail"):
                lines.append(f"  - {item['status_detail']}")
            lines.append(f"- **OWNER:** {item.get('owner', 'Unassigned')}")
            if item.get("pr_refs"):
                lines.append(f"- **PRs:** {', '.join('#'+str(n) for n in item['pr_refs'])}")
            if item.get("blocked_by"):
                lines.append(f"- **Blocked by:** {', '.join(item['blocked_by'])}")
            if item.get("shawn_gated"):
                lines.append(f"- **🔒 SHAWN-GATED** — his word only")
            if item.get("blocker_detail"):
                lines.append(f"- **Blocker:** {item['blocker_detail']}")
            lines.append(f"- **Updated:** {item.get('updated_at', '?')}")
            lines.append("")

    # Shawn gates section
    gates = data.get("shawn_gates", [])
    if gates:
        lines.append("---")
        lines.append("")
        lines.append("## 🔒 Blocked on Shawn (protected gates — his word only)")
        lines.append("")
        lines.append("These are NOT team-actionable. They wait on Shawn explicitly:")
        lines.append("")
        for g in gates:
            prs = f" (PRs: {', '.join('#'+str(n) for n in g['pr_refs'])})" if g.get("pr_refs") else ""
            lines.append(f"{g['id']}. **{g['what']}**{prs}")
        lines.append("")

    # Production gate
    pg = data.get("production_gate", {})
    if pg:
        lines.append("---")
        lines.append("")
        lines.append("## Production Readiness Gate")
        lines.append("")
        lines.append("```")
        lines.append(pg.get("formula", ""))
        lines.append("```")
        lines.append("")
        if pg.get("shawn_rule"):
            lines.append(f"**Shawn's rule:** \"{pg['shawn_rule']}\"")
            lines.append("")

    # Summary counts
    counts = {}
    for section in data["sections"]:
        for item in section.get("items", []):
            counts[item["status"]] = counts.get(item["status"], 0) + 1
    total = sum(counts.values())
    done = counts.get("DONE", 0)
    lines.append("---")
    lines.append("")
    lines.append(f"*Summary: {done}/{total} DONE "
                 f"({counts.get('IN PROGRESS', 0)} in progress, "
                 f"{counts.get('BLOCKED', 0)} blocked, "
                 f"{counts.get('TODO', 0)} todo, "
                 f"{counts.get('STALE', 0)} stale). "
                 f"Last sync: {meta['updated_at']}.*")
    lines.append("")
    lines.append("*Generated from ACTIVATION-CHECKLIST.json — do not hand-edit.*")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Sync checklist from PR state")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show changes without writing")
    parser.add_argument("--check-stale-only", action="store_true",
                        help="Skip PR checks, only staleness")
    parser.add_argument("--repo-root", default=".",
                        help="Repo root directory")
    args = parser.parse_args()

    json_path = os.path.join(args.repo_root, JSON_PATH)
    md_path = os.path.join(args.repo_root, MD_PATH)

    try:
        with open(json_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"FATAL: cannot read checklist JSON: {e}", file=sys.stderr)
        return 3

    changes = []
    stale_alerts = []
    pr_cache = {}

    for section in data["sections"]:
        for item in section.get("items", []):
            item_id = item["id"]

            # 1. PR-driven status
            # Shawn-gated BLOCKED items wait on a human decision, not PR state.
            # The sync must never auto-clear a Shawn gate.
            if item.get("shawn_gated") and item.get("status") == "BLOCKED":
                pass  # leave for Shawn's word; still run stale check below
            elif not args.check_stale_only and item.get("pr_refs"):
                for num in item["pr_refs"]:
                    if num not in pr_cache:
                        try:
                            pr_cache[num] = get_pr_state(num)
                        except Exception as e:
                            print(f"WARN: PR #{num} check failed: {e}",
                                  file=sys.stderr)
                            pr_cache[num] = None
                # Only derive if all PRs fetched OK
                if all(pr_cache.get(n) for n in item["pr_refs"]):
                    derived = derive_status(
                        item, {n: pr_cache[n] for n in item["pr_refs"]})
                    if derived:
                        new_status, new_detail = derived
                        old_status = item["status"]
                        # Don't regress DONE → non-DONE on a transient check
                        # (merged stays merged)
                        if old_status == "DONE" and new_status != "DONE":
                            # Verify: if it was DONE via merge, keep DONE
                            # unless PR was somehow unmerged (impossible)
                            pass
                        elif (new_status != old_status or
                                new_detail != item.get("status_detail")):
                            changes.append(
                                f"{item_id}: {old_status} → {new_status}")
                            if not args.dry_run:
                                if old_status != new_status:
                                    item.setdefault("history", []).append({
                                        "at": now_utc().strftime(
                                            "%Y-%m-%dT%H:%M:%SZ"),
                                        "by": "checklist_sync",
                                        "from": old_status,
                                        "to": new_status,
                                        "reason": new_detail[:200],
                                    })
                                item["status"] = new_status
                                item["status_detail"] = new_detail
                                item["updated_at"] = now_utc().strftime(
                                    "%Y-%m-%dT%H:%M:%SZ")

            # 2. Stale detection
            alert = check_stale(item, section["title"])
            if alert:
                stale_alerts.append((item, alert))
                changes.append(f"{item_id}: flagged STALE")
                if not args.dry_run:
                    item["status"] = "STALE"
                    item.setdefault("history", []).append({
                        "at": now_utc().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "by": "checklist_sync",
                        "from": "IN PROGRESS",
                        "to": "STALE",
                        "reason": f"No update in {STALE_HOURS}h",
                    })

    # 3. Update meta
    if not args.dry_run and changes:
        data["meta"]["updated_at"] = now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")

    # 4. Write JSON + regenerate MD
    if args.dry_run:
        print("DRY RUN — would change:")
        for c in changes:
            print(f"  {c}")
        for _, alert in stale_alerts:
            print(f"  ALERT: {alert[:120]}...")
        return 0

    if changes:
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        md_content = generate_md(data)
        with open(md_path, "w") as f:
            f.write(md_content)
        print(f"Updated {len(changes)} items. JSON + MD written.")
    else:
        print("No changes.")

    # 5. Post stale alerts to board
    for item, alert in stale_alerts:
        # Only alert once per stale episode: check if already alerted
        history = item.get("history", [])
        already = any(h.get("to") == "STALE_ALERTED" for h in history[-3:])
        if not already:
            url = post_to_board(
                f"[NAYA 4] {alert}\n\nChecklist: "
                f"BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md")
            if not args.dry_run:
                item["history"].append({
                    "at": now_utc().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "by": "checklist_sync",
                    "from": "STALE",
                    "to": "STALE_ALERTED",
                    "reason": f"Posted to board: {url}",
                })
            print(f"Stale alert posted for {item['id']}")
        # Re-write JSON with alert history
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
