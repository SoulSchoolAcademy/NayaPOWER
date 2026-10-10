#!/usr/bin/env python3
"""lane_board.py — the live lane board updater.

The live lane board is the team's pulse: per lane, the current task, status,
blockers, and last heartbeat. #1354 stays the permanent record; this board is
the live picture, not the archive.

Write path (standing decision, WS-5):
  * Live state lives on the dedicated `lane-board` branch — never main.
  * Lanes commit DIRECTLY to that branch via the GitHub API (no PR, no review).
  * Conflict-free by design: each lane owns exactly one file,
    BRAIN/00-TEAM/lane-board/lanes/<lane>.json. The tool rewrites only its own
    lane file plus the two generated views, and retries the ref update if the
    tip moved (compare-and-retry, up to 10 attempts).
  * Nothing here can touch production: writes are confined to one directory on
    a non-main branch.

Staleness rule (applied automatically by the renderer):
  * Heartbeat every 15 minutes while active.
  * Heartbeat older than 30 minutes  =>  rendered STALE.

One-command usage (from the repo root):
  python3 tools/lane_board.py sign-in   --lane ws-5 --seat naya-4 --task "Building the board"
  python3 tools/lane_board.py heartbeat --lane ws-5 --seat naya-4
  python3 tools/lane_board.py sign-out  --lane ws-5 --seat naya-4
  python3 tools/lane_board.py show

Stdlib only. Auth goes through the repo's GitHub skill CLI
(~/workspace/skills/github/bin/gh-api); override with GH_API_BIN.
"""

from __future__ import annotations

import argparse
import base64
import datetime
import json
import os
import re
import subprocess
import sys
import time

REPO = os.environ.get("LANE_BOARD_REPO", "SoulSchoolAcademy/NayaPOWER")
BOARD_ROOT = "BRAIN/00-TEAM/lane-board"
LANES_DIR = BOARD_ROOT + "/lanes"
AGGREGATE_PATH = BOARD_ROOT + "/lane-board.json"
RENDERED_PATH = BOARD_ROOT + "/LANE-BOARD.md"
LIVE_BRANCH = os.environ.get("LANE_BOARD_BRANCH", "lane-board")

STALE_AFTER_MIN = int(os.environ.get("LANE_BOARD_STALE_MIN", "30"))

GH_API_BIN = os.path.expanduser(
    os.environ.get("GH_API_BIN", "~/workspace/skills/github/bin/gh-api")
)

STATUSES = ("SEEDED", "ACTIVE", "BLOCKED", "SIGNED_OUT")
LANE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


# --------------------------------------------------------------------------
# time + records
# --------------------------------------------------------------------------

def now_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def iso_z(dt: datetime.datetime) -> str:
    return dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_z(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc
    )


def lane_record(
    lane: str,
    seat: str,
    task: str,
    status: str = "ACTIVE",
    kind: str = "workstream",
    ref: str = "",
    title: str = "",
    blockers: list | None = None,
    note: str = "",
    heartbeat: datetime.datetime | None = None,
    updated_by: str | None = None,
) -> dict:
    if not LANE_RE.match(lane):
        raise ValueError(f"bad lane id: {lane!r}")
    if status not in STATUSES:
        raise ValueError(f"bad status: {status!r}; want one of {STATUSES}")
    hb = heartbeat or now_utc()
    return {
        "lane": lane,
        "kind": kind,
        "ref": ref,
        "title": title,
        "seat": seat,
        "task": task,
        "status": status,
        "blockers": list(blockers or []),
        "heartbeat_utc": iso_z(hb),
        "note": note,
        "updated_utc": iso_z(hb),
        "updated_by": updated_by or seat,
    }


def touch(rec: dict, seat: str) -> dict:
    """Refresh heartbeat + updated stamps on any mutation."""
    rec = dict(rec)
    rec["heartbeat_utc"] = iso_z(now_utc())
    rec["updated_utc"] = rec["heartbeat_utc"]
    rec["updated_by"] = seat
    return rec


def age_min(rec: dict, at: datetime.datetime | None = None) -> float:
    at = at or now_utc()
    return (at - parse_z(rec["heartbeat_utc"])).total_seconds() / 60.0


def display_state(rec: dict, at: datetime.datetime | None = None) -> str:
    """ACTIVE/BLOCKED with an old heartbeat render as STALE. Never stored."""
    st = rec["status"]
    if st in ("ACTIVE", "BLOCKED") and age_min(rec, at) > STALE_AFTER_MIN:
        return "STALE"
    return st


# --------------------------------------------------------------------------
# rendering (pure: state in, text out)
# --------------------------------------------------------------------------

STATE_EMOJI = {
    "BLOCKED": "🔴",
    "ACTIVE": "🟢",
    "STALE": "🟡",
    "SIGNED_OUT": "⚪",
    "SEEDED": "⏳",
}

STATE_WORDS = {
    "BLOCKED": "Blocked right now",
    "ACTIVE": "Active now",
    "STALE": "Gone quiet — no heartbeat for 30+ min",
    "SIGNED_OUT": "Signed out",
    "SEEDED": "Seeded — never signed in yet",
}


def _lane_line(rec: dict, at: datetime.datetime) -> str:
    mins = age_min(rec, at)
    ago = "just now" if mins < 1 else f"{int(mins)} min ago"
    ref = rec.get("ref") or rec["lane"]
    title = rec.get("title") or ""
    head = f"**{ref}**" + (f" · {title}" if title else "")
    line = f"- {head} — {rec['seat']} — “{rec['task']}” — last heartbeat {ago}"
    if rec.get("note"):
        line += f"\n  - note: {rec['note']}"
    for b in rec.get("blockers", []):
        line += f"\n  - 🚧 blocker: {b}"
    return line


def render(lanes: dict[str, dict], at: datetime.datetime | None = None) -> tuple[str, str]:
    """Return (aggregate_json, rendered_markdown)."""
    at = at or now_utc()
    buckets: dict[str, list[dict]] = {s: [] for s in STATE_EMOJI}
    for lane_id in sorted(lanes):
        buckets[display_state(lanes[lane_id], at)].append(lanes[lane_id])

    md: list[str] = []
    md.append("# 🛰️ LIVE LANE BOARD")
    md.append("")
    md.append(f"*The team's pulse — who's working on what, right now. Refreshed {iso_z(at)}.*")
    md.append("")
    md.append("> #1354 stays the permanent record. This board is the pulse, not the archive.")
    md.append("> Heartbeat every 15 min while active. Older than 30 min is marked STALE automatically.")
    md.append("")
    for state in ("BLOCKED", "ACTIVE", "STALE", "SIGNED_OUT", "SEEDED"):
        md.append(f"## {STATE_EMOJI[state]} {STATE_WORDS[state]}")
        md.append("")
        if buckets[state]:
            md.extend(_lane_line(r, at) for r in buckets[state])
        else:
            md.append("_none_")
        md.append("")
    md.append("---")
    md.append(f"_Board: `{REPO}` branch `{LIVE_BRANCH}` · updater: `tools/lane_board.py` · stale rule: {STALE_AFTER_MIN} min_")
    rendered = "\n".join(md).rstrip() + "\n"

    aggregate = {
        "board": "live-lane-board",
        "repo": REPO,
        "branch": LIVE_BRANCH,
        "generated_utc": iso_z(at),
        "stale_after_min": STALE_AFTER_MIN,
        "lane_count": len(lanes),
        "lanes": {k: lanes[k] for k in sorted(lanes)},
    }
    return json.dumps(aggregate, indent=2, sort_keys=False) + "\n", rendered


# --------------------------------------------------------------------------
# GitHub API plumbing (via the skill CLI; compare-and-retry on ref updates)
# --------------------------------------------------------------------------

def _gh(method: str, path: str, body: dict | None = None) -> dict:
    argv = [GH_API_BIN, method, path]
    if body is not None:
        argv.append(json.dumps(body))
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout or "{}")


def _ref_tip(branch: str) -> tuple[str, str]:
    """Return (commit_sha, tree_sha) for a branch tip."""
    ref = _gh("GET", f"/repos/{REPO}/git/ref/heads/{branch}")
    commit_sha = ref["object"]["sha"]
    commit = _gh("GET", f"/repos/{REPO}/git/commits/{commit_sha}")
    return commit_sha, commit["tree"]["sha"]


def _read_tree_lanes(branch: str) -> tuple[str, str, dict[str, dict]]:
    """Return (tip_commit, tip_tree, {lane_id: record}) from the branch tip."""
    tip_commit, tip_tree = _ref_tip(branch)
    tree = _gh("GET", f"/repos/{REPO}/git/trees/{tip_tree}?recursive=1")
    lanes: dict[str, dict] = {}
    prefix = LANES_DIR + "/"
    for entry in tree.get("tree", []):
        p = entry.get("path", "")
        if entry.get("type") == "blob" and p.startswith(prefix) and p.endswith(".json"):
            name = p[len(prefix):-5]
            if name.startswith("_"):
                continue
            blob = _gh("GET", f"/repos/{REPO}/git/blobs/{entry['sha']}")
            raw = blob.get("content", "")
            text = base64.b64decode(raw).decode("utf-8") if blob.get("encoding") == "base64" else raw
            lanes[name] = json.loads(text)
    return tip_commit, tip_tree, lanes


def _create_blob(text: str) -> str:
    blob = _gh("POST", f"/repos/{REPO}/git/blobs", {"content": text, "encoding": "utf-8"})
    return blob["sha"]


def write_update(lane_id: str, mutate, commit_note: str, branch: str = LIVE_BRANCH,
                 retries: int = 10) -> dict:
    """Read-modify-write one lane + regenerated views, with ref-update retry.

    `mutate(record_or_None) -> record` builds the new lane record.
    Returns the new lane record.
    """
    if not LANE_RE.match(lane_id):
        raise ValueError(f"bad lane id: {lane_id!r}")
    lane_path = f"{LANES_DIR}/{lane_id}.json"

    last_err: Exception | None = None
    for _ in range(retries):
        tip_commit, tip_tree, lanes = _read_tree_lanes(branch)
        new_rec = mutate(lanes.get(lane_id))
        if not isinstance(new_rec, dict) or new_rec.get("lane") != lane_id:
            raise ValueError("mutate() must return the lane record for " + lane_id)
        lanes[lane_id] = new_rec

        aggregate_text, rendered_text = render(lanes)
        entries = [
            {"path": lane_path, "mode": "100644", "type": "blob",
             "sha": _create_blob(json.dumps(new_rec, indent=2) + "\n")},
            {"path": AGGREGATE_PATH, "mode": "100644", "type": "blob",
             "sha": _create_blob(aggregate_text)},
            {"path": RENDERED_PATH, "mode": "100644", "type": "blob",
             "sha": _create_blob(rendered_text)},
        ]
        new_tree = _gh("POST", f"/repos/{REPO}/git/trees",
                       {"base_tree": tip_tree, "tree": entries})["sha"]
        new_commit = _gh("POST", f"/repos/{REPO}/git/commits",
                         {"message": f"lane-board: {commit_note}",
                          "tree": new_tree, "parents": [tip_commit]})["sha"]
        try:
            _gh("PATCH", f"/repos/{REPO}/git/refs/heads/{branch}", {"sha": new_commit})
            return new_rec
        except RuntimeError as exc:
            last_err = exc  # tip moved under us; rebuild on the new tip
            time.sleep(1)
    raise RuntimeError(f"ref update kept racing after {retries} tries: {last_err}")


def show(branch: str = LIVE_BRANCH) -> str:
    """Live read: print the rendered board straight from the branch tip."""
    _, tip_tree = _ref_tip(branch)
    tree = _gh("GET", f"/repos/{REPO}/git/trees/{tip_tree}?recursive=1")
    sha = next((e["sha"] for e in tree.get("tree", [])
                if e.get("path") == RENDERED_PATH), None)
    if not sha:
        return f"(no rendered board yet on branch {branch})"
    blob = _gh("GET", f"/repos/{REPO}/git/blobs/{sha}")
    raw = blob.get("content", "")
    return base64.b64decode(raw).decode("utf-8") if blob.get("encoding") == "base64" else raw


def render_local(state_dir: str, out_dir: str) -> None:
    """Offline render: state_dir holds lanes/*.json; writes aggregate + md."""
    lanes: dict[str, dict] = {}
    for path in sorted(os.listdir(state_dir)):
        if path.endswith(".json") and not path.startswith("_"):
            with open(os.path.join(state_dir, path), encoding="utf-8") as f:
                rec = json.load(f)
            lanes[rec["lane"]] = rec
    aggregate_text, rendered_text = render(lanes)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "lane-board.json"), "w", encoding="utf-8") as f:
        f.write(aggregate_text)
    with open(os.path.join(out_dir, "LANE-BOARD.md"), "w", encoding="utf-8") as f:
        f.write(rendered_text)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--lane", required=True, help="lane id, e.g. ws-5 or team-1865")
    p.add_argument("--seat", required=True, help="who is writing, e.g. naya-4")
    p.add_argument("--branch", default=LIVE_BRANCH, help="board branch (default: lane-board)")


def cmd_sign_in(a) -> dict:
    def mutate(_old):
        return lane_record(a.lane, a.seat, a.task, status="ACTIVE",
                           kind=a.kind, ref=a.ref, title=a.title,
                           note=a.note or "")
    return write_update(a.lane, mutate,
                        f"{a.lane} sign-in ({a.seat}): {a.task[:60]}",
                        branch=a.branch)


def cmd_heartbeat(a) -> dict:
    def mutate(old):
        if old is None:
            raise ValueError(f"lane {a.lane} has no record — sign-in first")
        rec = touch(dict(old), a.seat)
        if rec["status"] == "SIGNED_OUT":
            rec["status"] = "ACTIVE"
        if a.note:
            rec["note"] = a.note
        return rec
    return write_update(a.lane, mutate, f"{a.lane} heartbeat ({a.seat})",
                        branch=a.branch)


def cmd_sign_out(a) -> dict:
    def mutate(old):
        if old is None:
            raise ValueError(f"lane {a.lane} has no record — sign-in first")
        rec = touch(dict(old), a.seat)
        rec["status"] = "SIGNED_OUT"
        if a.note:
            rec["note"] = a.note
        return rec
    return write_update(a.lane, mutate, f"{a.lane} sign-out ({a.seat})",
                        branch=a.branch)


def cmd_set_task(a) -> dict:
    def mutate(old):
        if old is None:
            raise ValueError(f"lane {a.lane} has no record — sign-in first")
        rec = touch(dict(old), a.seat)
        rec["task"] = a.task
        if rec["status"] == "SIGNED_OUT":
            rec["status"] = "ACTIVE"
        return rec
    return write_update(a.lane, mutate, f"{a.lane} task := {a.task[:60]}",
                        branch=a.branch)


def cmd_set_blocker(a) -> dict:
    def mutate(old):
        if old is None:
            raise ValueError(f"lane {a.lane} has no record — sign-in first")
        rec = touch(dict(old), a.seat)
        blockers = list(rec.get("blockers", []))
        if a.clear_blocker:
            blockers = []
            rec["status"] = "ACTIVE" if rec["status"] == "BLOCKED" else rec["status"]
        else:
            if a.blocker not in blockers:
                blockers.append(a.blocker)
            rec["status"] = "BLOCKED"
        rec["blockers"] = blockers
        return rec
    note = "blocker cleared" if a.clear_blocker else f"blocker: {(a.blocker or '')[:60]}"
    return write_update(a.lane, mutate, f"{a.lane} {note}", branch=a.branch)


def self_test() -> None:
    """Fixture-based check of the pure logic (no network)."""
    t0 = datetime.datetime(2026, 10, 10, 15, 0, tzinfo=datetime.timezone.utc)

    def rec(lane, mins_ago, status="ACTIVE", blockers=()):
        hb = t0 - datetime.timedelta(minutes=mins_ago)
        return lane_record(lane, "naya-4", f"task-{lane}", status=status,
                           ref=lane.upper(), title=f"Title {lane}",
                           blockers=list(blockers), heartbeat=hb)

    lanes = {
        "ws-5": rec("ws-5", 5),
        "ws-1": rec("ws-1", 45),                       # stale
        "ws-2": rec("ws-2", 3, status="BLOCKED", blockers=["waiting on X"]),
        "ws-3": rec("ws-3", 120, status="SIGNED_OUT"),
        "team-1865": rec("team-1865", 0, status="SEEDED"),
    }
    agg_text, md = render(lanes, at=t0)
    agg = json.loads(agg_text)
    assert agg["lane_count"] == 5, agg["lane_count"]
    assert "## 🔴 Blocked right now" in md and "waiting on X" in md
    assert "## 🟢 Active now" in md and "ws-5" in md
    assert "## 🟡 Gone quiet" in md, "stale section missing"
    assert "## ⚪ Signed out" in md
    assert "## ⏳ Seeded" in md
    # stale lane must sit in the quiet section, not the active one
    active_sec = md.split("## 🟢 Active now")[1].split("## 🟡")[0]
    quiet_sec = md.split("## 🟡 Gone quiet")[1].split("## ⚪")[0]
    assert "ws-1" not in active_sec and "ws-1" in quiet_sec, "staleness mis-bucketed"
    # boundary: exactly at the limit is not stale
    edge = rec("ws-9", STALE_AFTER_MIN)
    assert display_state(edge, t0) == "ACTIVE"
    over = rec("ws-9", STALE_AFTER_MIN + 1)
    assert display_state(over, t0) == "STALE"
    # touch refreshes heartbeat
    old = rec("ws-5", 60)
    new = touch(old, "naya-4")
    assert age_min(new, t0) < 1 and new["updated_by"] == "naya-4"
    # validation
    try:
        lane_record("BAD ID!", "naya-4", "t")
        raise AssertionError("lane id validation missing")
    except ValueError:
        pass
    print("lane_board self-test: 9 assertions green")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lane_board.py", description=__doc__.splitlines()[0])
    p.add_argument("--self-test", action="store_true", help="run fixture tests, no network")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("sign-in", help="start work on a lane")
    _common(s)
    s.add_argument("--task", required=True)
    s.add_argument("--kind", default="workstream", choices=["workstream", "team"])
    s.add_argument("--ref", default="")
    s.add_argument("--title", default="")
    s.add_argument("--note", default="")

    h = sub.add_parser("heartbeat", help="I'm alive; refresh the heartbeat")
    _common(h)
    h.add_argument("--note", default="")

    o = sub.add_parser("sign-out", help="stop work on a lane")
    _common(o)
    o.add_argument("--note", default="")

    t = sub.add_parser("set-task", help="change the current task")
    _common(t)
    t.add_argument("--task", required=True)

    b = sub.add_parser("set-blocker", help="set or clear a blocker")
    _common(b)
    b.add_argument("--blocker", default="")
    b.add_argument("--clear-blocker", action="store_true")

    r = sub.add_parser("render", help="offline render from a local lanes/ dir")
    r.add_argument("--state-dir", required=True)
    r.add_argument("--out-dir", required=True)

    v = sub.add_parser("show", help="print the live rendered board")
    v.add_argument("--branch", default=LIVE_BRANCH)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if not args.cmd:
        build_parser().print_help()
        return 2
    try:
        if args.cmd == "sign-in":
            rec_out = cmd_sign_in(args)
        elif args.cmd == "heartbeat":
            rec_out = cmd_heartbeat(args)
        elif args.cmd == "sign-out":
            rec_out = cmd_sign_out(args)
        elif args.cmd == "set-task":
            rec_out = cmd_set_task(args)
        elif args.cmd == "set-blocker":
            rec_out = cmd_set_blocker(args)
        elif args.cmd == "render":
            render_local(args.state_dir, args.out_dir)
            print(f"rendered to {args.out_dir}")
            return 0
        elif args.cmd == "show":
            print(show(args.branch))
            return 0
        else:
            raise ValueError("unknown command")
    except (RuntimeError, ValueError) as exc:
        print(f"lane_board: error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "lane": rec_out["lane"],
                      "status": rec_out["status"],
                      "heartbeat_utc": rec_out["heartbeat_utc"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
