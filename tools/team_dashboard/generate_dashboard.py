#!/usr/bin/env python3
"""
Team Naya Activity Dashboard generator.

Regenerates BRAIN/90-OPERATIONS/TEAM-DASHBOARD.md (human) and
BRAIN/90-OPERATIONS/team-dashboard.machine.json (machine / Hub smart-ledger ready)
from live structured sources. Same truth, two tongues.

Sources:
- area roster:      ~/workspace/goals/nayapower-10-10-completion-drive/hidden_files/area-agents/AREA-DEFINITIONS.machine.json
- bullseyes:        .../area-agents/charter-*.md  (**BULLSEYE:** lines)
- scores:           ~/workspace/agent-scorecard/agent-scorecard.machine.json
- wave counter:     .../hidden_files/team-naya-wave-counter.txt
- board activity:   GitHub #2175 comments (sign in/out)
- open PRs:         GitHub API

Usage: python3 generate_dashboard.py [--worktree PATH] [--out-md PATH] [--out-json PATH]
Defaults assume the NayaPOWER repo worktree; override for testing.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = os.path.expanduser("~/workspace/naya/bin/gh-api")
GOAL = os.path.expanduser("~/workspace/goals/nayapower-10-10-completion-drive/hidden_files")
AGENTS_DIR = os.path.join(GOAL, "area-agents")
AREA_DEFS = os.path.join(AGENTS_DIR, "AREA-DEFINITIONS.machine.json")
SCORECARD = os.path.expanduser("~/workspace/agent-scorecard/agent-scorecard.machine.json")
WAVE_COUNTER = os.path.join(GOAL, "team-naya-wave-counter.txt")

AREA_ORDER = ["learn", "know", "act", "law", "prove", "build",
              "wire", "team", "infra", "product", "memory", "govern"]
AREA_NAMES = {"learn": "LEARN", "know": "KNOW", "act": "ACT", "law": "LAW",
              "prove": "PROVE", "build": "BUILD", "wire": "WIRE", "team": "TEAM",
              "infra": "INFRA", "product": "PRODUCT", "memory": "MEMORY", "govern": "GOVERN"}


def gh_api(path):
    out = subprocess.run([GH_API, "GET", path], capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError(f"gh-api failed on {path}: {out.stderr[:200]}")
    return json.loads(out.stdout)


def load_roster():
    with open(AREA_DEFS) as f:
        defs = json.load(f)
    roster = {}
    for a in defs["areas"]:
        roster[a["id"]] = a
    # bullseyes from charters
    for i, aid in enumerate(AREA_ORDER, 1):
        charter = os.path.join(AGENTS_DIR, f"charter-{i:02d}-{aid}.md")
        bull = None
        try:
            with open(charter) as f:
                m = re.search(r"\*\*BULLSEYE:\*\*\s*\*(.+?)\*", f.read())
                if m:
                    bull = m.group(1)
        except FileNotFoundError:
            pass
        if aid in roster:
            roster[aid]["bullseye"] = bull or "(not set)"
    return roster


def load_scores():
    try:
        with open(SCORECARD) as f:
            sc = json.load(f)
    except FileNotFoundError:
        return {}, None
    scores = {}
    for a in sc.get("areas", []):
        key = (a.get("key") or "").lower()
        if key:
            scores[key] = {
                "current": a.get("current"),
                "trend": a.get("trend"),
                "next_action": (a.get("next_action") or "")[:220],
                "why_not_10": (a.get("why_not_10") or [])[:3],
            }
    return scores, {"edition": sc.get("edition"), "issued": sc.get("issued_utc"),
                    "team_average": sc.get("team_average")}


def current_wave():
    try:
        with open(WAVE_COUNTER) as f:
            n = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        n = 0
    # wave N dispatched areas ((N*3)+1..(N*3)+3) mod 12; the *active* wave is the last dispatched = n-1
    active = (n - 1) % 4 if n > 0 else 0
    areas = [AREA_ORDER[(active * 3 + i) % 12] for i in range(3)]
    return {"wave_number": active + 1, "counter": n, "active_areas": areas}


def recent_board_activity(limit_pages=2, per_page=100):
    """Most recent sign in/out style comments on #2175 (fetches the LAST pages)."""
    events = []
    # find the last page first
    try:
        first = gh_api(f"/repos/{REPO}/issues/2175/comments?per_page=1&page=1")
        # GitHub doesn't give total directly; probe pages from the tail estimate
        # #2175 is large; fetch pages 4 and 5 which hold the newest (per worker convention)
        pages = [4, 5]
    except RuntimeError:
        pages = [4]
    for page in pages:
        try:
            comments = gh_api(f"/repos/{REPO}/issues/2175/comments?per_page={per_page}&page={page}")
        except RuntimeError:
            break
        if not comments:
            break
        for c in comments:
            body = c.get("body", "")
            head = body[:500]
            lane, kind = None, None
            m = re.search(r"\[LANE ([A-Z0-9\- ]+)\][^\n]*?(sign-in|sign-out)", head, re.I)
            if m:
                lane, kind = m.group(1).strip().upper(), m.group(2).lower().replace("sign-", "")
            else:
                m2 = re.search(r"([A-Z][A-Z0-9 ]{1,20}) lane sign-(in|out)", head, re.I)
                if m2:
                    lane, kind = m2.group(1).strip().upper(), m2.group(2).lower()
                else:
                    m3 = re.search(r"##?\s*\[?([A-Z0-9 ]+)\]?[^\n]{0,80}?(signing out|sign-out|signing in|sign-in)", head, re.I)
                    if m3:
                        lane = m3.group(1).strip().upper()
                        kind = "out" if "out" in m3.group(2).lower() else "in"
            if lane and kind:
                summary = ""
                for line in body.split("\n")[1:8]:
                    clean = line.strip(" |*#>-")
                    if len(clean) > 25 and not clean.startswith("["):
                        summary = clean[:160]
                        break
                # normalize lane to 12-area names where possible
                lane_norm = lane.replace("NAYA 2", "").replace("NIGHT-SHIFT-", "").strip()
                events.append({
                    "comment_id": c["id"],
                    "url": c["html_url"],
                    "lane": lane_norm or lane,
                    "kind": kind,
                    "at": c["created_at"],
                    "summary": summary,
                })
    # dedupe by comment id, newest first
    seen = set()
    uniq = []
    for e in sorted(events, key=lambda e: e["at"], reverse=True):
        if e["comment_id"] not in seen:
            seen.add(e["comment_id"])
            uniq.append(e)
    return uniq[:16]


def open_prs():
    try:
        prs = gh_api(f"/repos/{REPO}/pulls?state=open&per_page=100")
    except RuntimeError:
        return []
    out = []
    for pr in prs:
        out.append({
            "number": pr["number"],
            "title": pr["title"][:90],
            "head": pr["head"]["ref"][:50],
            "url": pr["html_url"],
            "created": pr["created_at"][:10],
            "draft": pr.get("draft", False),
        })
    return out


def area_for_pr(title, head):
    """Best-effort area tag from PR title/head."""
    t = (title + " " + head).lower()
    hints = [
        ("learn", ["learn", "compounding", "four-arm"]),
        ("know", ["brain-index", "brain index", "re-stamp", "restamp", "drift"]),
        ("act", ["intent", "advise", "act_pipeline"]),
        ("law", ["law 11", "law11", "law-11", "decision principle", "harm", "neutrality"]),
        ("prove", ["verify", "sabotage", "scorecard", "battery"]),
        ("wire", ["wire", "wiring", "gate", "d22", "d23", "d24", "d25", "d26", "d2", "d3", "d5", "d6"]),
        ("infra", ["ci", "workflow", "github actions", ".github"]),
        ("product", ["hub", "nayanet", "ask naya", "voice"]),
        ("memory", ["memory", "intelligent block", "persistence", "continuity"]),
        ("govern", ["protocol", "twelve laws", "briefing", "governance", "no-bottleneck"]),
        ("build", ["merge", "rebase"]),
        ("team", ["team", "dispatcher", "rotation", "charter", "dashboard"]),
    ]
    for aid, keys in hints:
        if any(k in t for k in keys):
            return aid
    return "build"


def build_dashboard():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    roster = load_roster()
    scores, meta = load_scores()
    wave = current_wave()

    print("Fetching board activity...", file=sys.stderr)
    events = recent_board_activity()
    print(f"  {len(events)} sign in/out events", file=sys.stderr)
    print("Fetching open PRs...", file=sys.stderr)
    prs = open_prs()
    print(f"  {len(prs)} open PRs", file=sys.stderr)

    prs_by_area = {aid: [] for aid in AREA_ORDER}
    for pr in prs:
        aid = area_for_pr(pr["title"], pr["head"])
        pr["area"] = aid
        prs_by_area[aid].append(pr)

    # --- machine JSON (Hub smart-ledger ready) ---
    agents = []
    for aid in AREA_ORDER:
        r = roster.get(aid, {})
        s = scores.get(aid, {})
        agents.append({
            "id": aid,
            "name": AREA_NAMES[aid],
            "agent_name": r.get("agent_name"),
            "agent_title": r.get("agent_title"),
            "bullseye": r.get("bullseye"),
            "mission": r.get("mission"),
            "current_score": s.get("current", r.get("current_score")),
            "trend": s.get("trend"),
            "why_not_10": s.get("why_not_10", []),
            "next_action": s.get("next_action"),
            "active_now": aid in wave["active_areas"],
            "board_lane": r.get("board_lane"),
            "open_prs": [{"number": p["number"], "title": p["title"], "url": p["url"],
                          "draft": p["draft"]} for p in prs_by_area[aid][:8]],
            "open_pr_count": len(prs_by_area[aid]),
        })

    machine = {
        "schema": "naya.team-dashboard.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo": REPO,
        "team_average": meta["team_average"] if meta else None,
        "scorecard_edition": meta["edition"] if meta else None,
        "wave": wave,
        "agents": agents,
        "recent_activity": events,
        "open_pr_total": len(prs),
        "unassigned_prs": len(prs_by_area["build"]),
    }

    # --- human markdown ---
    L = []
    A = L.append
    A("# 🔱 Team Naya — Live Activity Dashboard")
    A("")
    A(f"*Don't tell me, show me. Generated {now} from live sources. Regenerated every wave (~10 min).*")
    A("")
    A(f"**Team average:** {meta['team_average'] if meta else 'n/a'}/10 &nbsp;|&nbsp; "
      f"**Open PRs:** {len(prs)} &nbsp;|&nbsp; "
      f"**Active wave:** #{wave['wave_number']} ({', '.join(AREA_NAMES[a] for a in wave['active_areas'])})")
    A("")
    A("## The Twelve")
    A("")
    A("| Agent | Area | Bullseye | Score | Status |")
    A("|---|---|---|---|---|")
    for ag in agents:
        status = "🟢 ACTIVE NOW" if ag["active_now"] else "⚪ standby"
        score = ag["current_score"]
        score_s = f"{score:.1f}" if isinstance(score, (int, float)) else "—"
        A(f"| **{ag['agent_name']}** | {ag['name']} | *{ag['bullseye']}* | {score_s} | {status} |")
    A("")
    A("## Recent Receipts (sign in / out on #2175)")
    A("")
    if events:
        for e in events[:12]:
            icon = "🟢" if e["kind"] == "in" else "✅"
            verb = "signed in" if e["kind"] == "in" else "signed out"
            A(f"- {icon} **{e['lane']}** {verb} — {e['at'][11:16]}Z — [receipt]({e['url']})")
            if e["summary"]:
                A(f"  - {e['summary']}")
    else:
        A("_No recent sign in/out events found._")
    A("")
    A("## Open PRs by Area")
    A("")
    for ag in agents:
        if ag["open_pr_count"]:
            A(f"### {ag['name']} ({ag['open_pr_count']})")
            for p in ag["open_prs"][:5]:
                draft = " 📝draft" if p["draft"] else ""
                A(f"- [#{p['number']}]({p['url']}) {p['title'][:70]}{draft}")
            if ag["open_pr_count"] > 5:
                A(f"- …and {ag['open_pr_count'] - 5} more")
            A("")
    A("---")
    A("*Same truth, two tongues: humans read this file; the Hub reads `team-dashboard.machine.json`. "
      "Both regenerated from the same live sources every wave.*")
    md = "\n".join(L) + "\n"
    return md, machine


def main():
    ap = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_md = os.path.join(ap[0], "BRAIN/90-OPERATIONS/TEAM-DASHBOARD.md") if ap else \
        "BRAIN/90-OPERATIONS/TEAM-DASHBOARD.md"
    out_json = out_md.replace("TEAM-DASHBOARD.md", "team-dashboard.machine.json")
    for i, a in enumerate(sys.argv):
        if a == "--out-md" and i + 1 < len(sys.argv):
            out_md = sys.argv[i + 1]
        if a == "--out-json" and i + 1 < len(sys.argv):
            out_json = sys.argv[i + 1]
        if a == "--worktree" and i + 1 < len(sys.argv):
            wt = sys.argv[i + 1]
            out_md = os.path.join(wt, "BRAIN/90-OPERATIONS/TEAM-DASHBOARD.md")
            out_json = os.path.join(wt, "BRAIN/90-OPERATIONS/team-dashboard.machine.json")

    md, machine = build_dashboard()
    os.makedirs(os.path.dirname(out_md), exist_ok=True)
    with open(out_md, "w") as f:
        f.write(md)
    with open(out_json, "w") as f:
        json.dump(machine, f, indent=1)
    print(f"Wrote {out_md} ({len(md)} chars)")
    print(f"Wrote {out_json} ({len(json.dumps(machine))} chars)")
    print(f"Agents: {len(machine['agents'])}, events: {len(machine['recent_activity'])}, "
          f"open PRs: {machine['open_pr_total']}")


if __name__ == "__main__":
    main()
