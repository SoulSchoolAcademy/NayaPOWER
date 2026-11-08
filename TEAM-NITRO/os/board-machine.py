#!/usr/bin/env python3
"""board-machine.py — Machine 5 of the Ultimate Operating System.

The Living List, generated from pipeline state instead of hand-maintained.

Reads the lane ledger (team-pulse-waiting.json — the pipeline state source
of truth for lanes) + state.json + the live work_items mirror, and generates
the board: one entry per open lane, with its holder, its last movement, and
its status derived from the ledger's own timestamps. The board matches the
ledger exactly — a different seat proves it with --verify.

Outputs (always, even dry-run):
  proof/board.json         — the generated board (lanes + reconciliation)
  proof/board-report.json  — the run report (counts, review items, verify input)
With --publish, it ALSO upserts one work_items row per open lane
(key "lane:<ledger-id>", last_actor_seat "board-machine") and deletes
lane:* rows whose ledger item closed — so the lanes show on the PI page
in the app, which reads work_items live. No worker deploy, no face rebuild,
no artifact redesign: the page already reads this table.

Discipline (the same as the other feeds — ACTIVATION.md):
  - Observations + reconciliation only. Never rewrites state.json items,
    never transitions needs-his-hands, never claims done without proof.
  - Disagreements become review items, never silent rewrites.
  - Supabase failures are caught: the board from the ledger is still
    written, the page side is reported null, the run exits 0 so the
    refresh cycle is never failed by this machine.
  - Writes are atomic (temp + os.replace). The ANON key is read from
    publish-to-project.py and never printed.

Status thresholds (same numbers as checkpoint-watch.py):
  ACTIVE  movement < 30 min   SITTING  30-60 min   STALE  > 60 min
Work-items state mapping: ACTIVE -> in_progress, SITTING/STALE -> queued
(lanes are open work; only ACTIVE claims someone is on it right now).
Priority is the page's sort (higher first; the face renders the top 30
open jobs; seat-born rows reach 10000): ACTIVE lanes 10100 (they lead the
page — that is the board's purpose), SITTING 10050, STALE/UNKNOWN 9000
(counted in the strip, listed in board.json, visible via Show-all).

Usage:
  board-machine.py [--publish] [--verify] [--ledger PATH] [--state PATH]
  --verify: re-read ledger + board.json + work_items and diff exactly.
            Exit 0 = exact match. Exit 1 = differences listed.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import urllib.parse
from datetime import datetime, timezone

WS = os.path.expanduser("~/workspace")
PI = os.path.join(WS, "project-intelligence")
OS_DIR = os.path.join(WS, "team-nitro", "os")
LEDGER = os.path.join(PI, "team-pulse-waiting.json")
STATE = os.path.join(PI, "state", "state.json")
BOARD = os.path.join(PI, "proof", "board.json")
REPORT = os.path.join(PI, "proof", "board-report.json")
PROJECT_ID = "a554e536-66a6-4808-8c36-988f13d9f394"
ACTOR = "board-machine"

ACTIVE_MIN = 30
SITTING_MIN = 60


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def first_line(text, limit=500):
    t = (text or "").strip().splitlines()
    t = t[0].strip() if t else ""
    return t[:limit]


def last_line(text, limit=500):
    t = (text or "").strip().splitlines()
    t = t[-1].strip() if t else ""
    return t[:limit]


def status_for(age_minutes):
    if age_minutes is None:
        return "UNKNOWN"
    if age_minutes < ACTIVE_MIN:
        return "ACTIVE"
    if age_minutes < SITTING_MIN:
        return "SITTING"
    return "STALE"


def load_ledger(path):
    with open(path, "rb") as f:
        raw = f.read()
    data = json.loads(raw)
    return data, hashlib.sha256(raw).hexdigest()


def build_board(ledger, state, work_items, now):
    """Pure computation: ledger + state + mirror -> board dict + review list."""
    items = ledger.get("items") or []
    closed = ledger.get("closed") or []
    lanes = []
    holders = {}
    for it in items:
        lid = it.get("id") or ""
        holder = it.get("holder") or "unassigned"
        holders[holder] = holders.get(holder, 0) + 1
        moved = parse_ts(it.get("movement_utc")) or parse_ts(it.get("since_utc"))
        age = None
        if moved is not None:
            age = max(0, int((now - moved).total_seconds() // 60))
        status = status_for(age)
        lanes.append({
            "lane_id": lid,
            "holder": holder,
            "what": first_line(it.get("what")),
            "since_utc": it.get("since_utc"),
            "movement_utc": it.get("movement_utc"),
            "age_minutes": age,
            "status": status,
            "movement_note": last_line(it.get("movement_note")),
        })
    lanes.sort(key=lambda l: (l["status"] != "STALE", l["status"] != "SITTING",
                              l["age_minutes"] if l["age_minutes"] is not None else 10 ** 9,
                              l["lane_id"]))
    counts = {
        "open": len(lanes),
        "active": sum(1 for l in lanes if l["status"] == "ACTIVE"),
        "sitting": sum(1 for l in lanes if l["status"] == "SITTING"),
        "stale": sum(1 for l in lanes if l["status"] == "STALE"),
        "unknown": sum(1 for l in lanes if l["status"] == "UNKNOWN"),
        "closed_total": len(closed),
        "holders": holders,
    }

    # ---- reconciliation: the Living List vs its mirror vs the page ----
    review = []
    recon = {"done_verifying": [], "extra_work_items_keys": {"count": None, "sample": []},
             "headline": {"artifact": None, "page": None}}
    state_items = {i["id"]: i for i in (state.get("items") or [])}
    done_proven = sum(1 for i in state_items.values() if i.get("state") == "done-proven")
    recon["headline"]["artifact"] = f"{done_proven}/{len(state_items)}"
    if work_items is not None:
        wi_by_key = {r["item_key"]: r for r in work_items}
        wi_done = sum(1 for r in work_items if r.get("state") == "done_proven")
        recon["headline"]["page"] = f"{wi_done}/{len(work_items)}"
        # done in state.json but verifying in the mirror (no evidence/prover)
        for key, it in sorted(state_items.items()):
            if it.get("state") != "done-proven":
                continue
            mirror = wi_by_key.get(key)
            if mirror is not None and mirror.get("state") == "verifying":
                proof = it.get("proof") or []
                recon["done_verifying"].append({
                    "id": key,
                    "title": (it.get("title") or key)[:120],
                    "mirror_state": "verifying",
                    "proof_entries": len(proof),
                    "proof_ok": it.get("proof_ok"),
                    "reason": "mirror downgrades done without evidence + independent prover",
                })
        if recon["done_verifying"]:
            review.append(
                f"{len(recon['done_verifying'])} items are done-proven in state.json "
                f"but verifying in the mirror (no evidence + independent prover) — "
                f"human check: {', '.join(d['id'] for d in recon['done_verifying'][:5])}"
                + (" ..." if len(recon["done_verifying"]) > 5 else ""))
        extra = sorted(set(wi_by_key) - set(state_items) - {"lane:" + l["lane_id"] for l in lanes})
        # lane:* keys belong to this machine, not to the state/mirror gap
        extra = [k for k in extra if not k.startswith("lane:")]
        recon["extra_work_items_keys"] = {"count": len(extra), "sample": extra[:10]}
        if extra:
            review.append(
                f"{len(extra)} work_items keys are not in state.json (seat-born rows "
                f"the guarded delete preserves) — the PI page shows the work_items "
                f"universe, not the Living List alone — human check")
        if recon["headline"]["artifact"] and recon["headline"]["page"]:
            a_done, a_tot = recon["headline"]["artifact"].split("/")
            p_done, p_tot = recon["headline"]["page"].split("/")
            if (a_done, a_tot) != (p_done, p_tot):
                review.append(
                    f"headline disagreement: Living List artifact {recon['headline']['artifact']} "
                    f"done vs PI page {recon['headline']['page']} done (different "
                    f"universes: 198-item queue vs work_items mirror + seat rows) — human check")
    else:
        review.append("work_items unreadable this run — page side of reconciliation is null, not assumed")

    stale_lanes = [l for l in lanes if l["status"] == "STALE"]
    if stale_lanes:
        oldest = sorted(stale_lanes, key=lambda l: -(l["age_minutes"] or 0))[:3]
        review.append(
            f"{len(stale_lanes)} of {len(lanes)} open lanes are STALE (no movement "
            f"in over 60 min) — oldest: "
            + ", ".join(f"{l['lane_id']} ({l['age_minutes']} min)" for l in oldest)
            + " — captain's call per the Always-On Law (the board lists every one; "
              "this review carries the count, not 77 lines)")

    board = {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": {"ledger": "team-pulse-waiting.json",
                   "state": "state.json",
                   "mirror": "work_items (Supabase, project a554e536...)"},
        "counts": counts,
        "lanes": lanes,
        "reconciliation": recon,
    }
    return board, review


def lane_row(lane, now):
    """One work_items row per open lane. Never claims done. Detail carries
    the ledger's own words; updated_at is the lane's own movement stamp."""
    state = "in_progress" if lane["status"] == "ACTIVE" else "queued"
    # Priority is the page's sort (higher first; the face renders the top 30
    # open jobs). Seat-born rows reach 10000, so a lane at 9000 never renders.
    # ACTIVE lanes — work moving RIGHT NOW — outrank everything (10100):
    # that IS the board's purpose (Shawn sees what is running without asking).
    # SITTING lanes (10050) sit just under them. STALE/UNKNOWN lanes (9000)
    # stay below the top window: counted in the strip, listed in board.json,
    # visible via the panel's Show-all — they must not push live work out.
    priority = {"ACTIVE": 10100, "SITTING": 10050}.get(lane["status"], 9000)
    detail = lane["what"]
    if lane["movement_note"]:
        detail = (detail + "\nLast movement: " + lane["movement_note"])[:2000]
    next_action = None
    if lane["status"] in ("SITTING", "STALE"):
        next_action = (f"No movement in {lane['age_minutes']} min — "
                       f"captain's call per the Always-On Law")
    return {
        "project_id": PROJECT_ID,
        "item_key": "lane:" + lane["lane_id"],
        "title": ("Lane — " + lane["what"])[:500],
        "detail": detail or None,
        "state": state,
        "evidence_url": None,
        "priority": priority,
        "owner_seat": lane["holder"],
        "maker_seat": ACTOR,
        "prover_seat": None,
        "next_action": next_action,
        "blocker": None,
        "notes": [],
        "last_actor_seat": ACTOR,
        "updated_at": lane["movement_utc"] or lane["since_utc"] or now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def supabase_req():
    """Reuse publish-to-project.py's req() — one auth path, no new keys."""
    spec = importlib.util.spec_from_file_location(
        "publish_to_project", os.path.join(PI, "publish-to-project.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.req


def read_work_items(req):
    rows, off = [], 0
    while True:
        page = req("GET", f"/work_items?project_id=eq.{PROJECT_ID}"
                          f"&select=item_key,state,updated_at,last_actor_seat"
                          f"&order=updated_at.asc&limit=1000&offset={off}") or []
        if not page:
            break
        rows += page
        off += len(page)
        if len(page) < 1000:
            break
    return rows


def publish(req, board, now):
    """Upsert lane:* rows for open lanes; delete lane:* rows whose lane closed.
    Only rows this machine wrote (last_actor_seat == board-machine)."""
    existing = read_work_items(req)
    by_key = {r["item_key"]: r for r in existing}
    rows = [lane_row(l, now) for l in board["lanes"]]
    if rows:
        req("POST", "/work_items?on_conflict=project_id,item_key",
            body=rows, prefer="resolution=merge-duplicates")
    live_keys = {"lane:" + l["lane_id"] for l in board["lanes"]}
    stale = [r for r in existing
             if r["item_key"].startswith("lane:")
             and r["item_key"] not in live_keys
             and r.get("last_actor_seat") == ACTOR]
    for r in stale:
        req("DELETE", f"/work_items?project_id=eq.{PROJECT_ID}"
                      f"&item_key=eq.{urllib.parse.quote(r['item_key'], safe='')}")
    return {"upserted": len(rows), "deleted": len(stale)}


def atomic_write(path, obj):
    tmp = path + ".tmp-board"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def verify(ledger, board, req):
    """Exact match, three ways. Returns (ok, differences)."""
    diffs = []
    open_ids = {it.get("id") for it in (ledger.get("items") or [])}
    board_ids = {l["lane_id"] for l in board.get("lanes", [])}
    if open_ids != board_ids:
        diffs.append(f"board lanes != ledger open items: "
                     f"missing from board {sorted(open_ids - board_ids)[:5]}, "
                     f"extra in board {sorted(board_ids - open_ids)[:5]}")
    now = datetime.now(timezone.utc)
    for l in board.get("lanes", []):
        src = next((it for it in (ledger.get("items") or [])
                    if it.get("id") == l["lane_id"]), None)
        if src is None:
            continue
        if l.get("holder") != (src.get("holder") or "unassigned"):
            diffs.append(f"{l['lane_id']}: holder board={l.get('holder')} ledger={src.get('holder')}")
        if l.get("movement_utc") != src.get("movement_utc"):
            diffs.append(f"{l['lane_id']}: movement_utc board={l.get('movement_utc')} ledger={src.get('movement_utc')}")
        moved = parse_ts(src.get("movement_utc")) or parse_ts(src.get("since_utc"))
        age = None
        if moved is not None:
            age = max(0, int((now - moved).total_seconds() // 60))
        if l.get("status") != status_for(age):
            diffs.append(f"{l['lane_id']}: status board={l.get('status')} recomputed={status_for(age)} (age {age}m)")
    # work_items lane:* rows == board lanes
    try:
        existing = read_work_items(req)
    except Exception as e:
        return False, diffs + [f"work_items unreadable during verify: {e}"]
    wi_lanes = {r["item_key"][5:]: r for r in existing
                if r["item_key"].startswith("lane:") and r.get("last_actor_seat") == ACTOR}
    if set(wi_lanes) != board_ids:
        diffs.append(f"work_items lane rows != board lanes: "
                     f"missing {sorted(board_ids - set(wi_lanes))[:5]}, "
                     f"extra {sorted(set(wi_lanes) - board_ids)[:5]}")
    for l in board.get("lanes", []):
        row = wi_lanes.get(l["lane_id"])
        if row is None:
            continue
        want = "in_progress" if l["status"] == "ACTIVE" else "queued"
        if row.get("state") != want:
            diffs.append(f"lane:{l['lane_id']}: work_items state={row.get('state')} want={want}")
    return (len(diffs) == 0), diffs


def main():
    ap = argparse.ArgumentParser(description="Board machine — Living List from pipeline state")
    ap.add_argument("--publish", action="store_true",
                    help="also upsert lane:* rows to work_items (default: dry-run, files only)")
    ap.add_argument("--verify", action="store_true",
                    help="verify board.json + work_items against the ledger, exact match")
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--state", default=STATE)
    args = ap.parse_args()
    now = datetime.now(timezone.utc)

    ledger, ledger_sha = load_ledger(args.ledger)
    state = json.load(open(args.state))

    if args.verify:
        board = json.load(open(BOARD))
        req = supabase_req()
        ok, diffs = verify(ledger, board, req)
        print("BOARD VERIFY: " + ("EXACT MATCH" if ok else "MISMATCH"))
        for d in diffs:
            print("  -", d)
        return 0 if ok else 1

    # work_items read (always — the reconciliation needs the page side).
    # A failed read degrades honestly: page side null, board still written.
    work_items = None
    wi_error = None
    try:
        work_items = read_work_items(supabase_req())
    except Exception as e:
        wi_error = str(e)[:200]

    board, review = build_board(ledger, state, work_items, now)
    board["ledger_sha256"] = ledger_sha
    if wi_error:
        review.append(f"work_items read failed this run ({wi_error}) — page side null, not assumed")
    atomic_write(BOARD, board)

    pub = None
    if args.publish:
        try:
            pub = publish(supabase_req(), board, now)
        except Exception as e:
            pub = {"error": str(e)[:200]}
            review.append(f"work_items publish failed ({pub['error']}) — board.json still written")
    report = {"at": now_iso(), "generated_board": BOARD, "publish": pub,
              "counts": board["counts"], "review": review,
              "ledger_sha256": ledger_sha,
              "work_items_read": len(work_items) if work_items is not None else None}
    atomic_write(REPORT, report)
    print(f"board-machine: lanes={board['counts']['open']} "
          f"(active {board['counts']['active']} / sitting {board['counts']['sitting']} "
          f"/ stale {board['counts']['stale']}) "
          f"publish={pub} review={len(review)}")
    for r in review:
        print("  ?", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
