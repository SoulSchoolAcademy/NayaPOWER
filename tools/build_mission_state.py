#!/usr/bin/env python3
"""Mission state as data — the MISSION-STATE.json twin of the director snapshot.

WHY: BRAIN/CURRENT-MISSION-STATE.md is the canonical mission snapshot, and
it is prose — hand-refreshed by the director pass in "Snapshot refresh"
commits (~30 min cadence). There is NO code builder behind it (verified at
f7bd39ca: the snapshot's git history is director commits, and no repo tool
writes it). A machine reader gets nothing structured from it: it parses
markdown like a human, at human speed, and two seats can read the same
paragraph and derive different numbers. This tool is the missing builder
for the twin: it derives BRAIN/MISSION-STATE.json from the SAME sources
the snapshot itself rests on, in one run —

  snapshot facts  parsed structurally out of BRAIN/CURRENT-MISSION-STATE.md
                  (the director's published synthesis: last-verified time,
                  the tip the snapshot anchors to, the TOP-10 standing
                  section, the per-area team-status table, the KEY NUMBERS
                  line, the WHERE-TO-GO pointers);
  live facts      re-derived from GitHub at emit time (tip via
                  GET /git/refs/heads/main — the ref is the anchor, never
                  the commits list endpoint; open PRs fully paginated;
                  the live board's comment count).

The twin keeps the two fact classes in separate blocks (`snapshot` vs
`live`) with per-section provenance (`sources`), because a snapshot is a
claim about its verification instant while the live block is a claim
about now — collapsing them is how state arguments start.

FIELD LIST (schema: tools/mission_state.schema.json, $id naya.mission-state/1)
  schema    the literal "naya.mission-state/1"
  $schema   path of the shipped schema file
  artifact  {kind, generator, twin_of, generated_utc}
  snapshot  {last_verified_utc, main_tip, tip_moved{from,to},
             identity{repo, live_board, master_directive},
             standing_top10[{rank, headline, carried, detail}],
             team_status[{area, accomplished, working_on, plan}],
             key_numbers{board{issue, comments, delta_since_watermark,
                               watermark_comment},
                          open_prs_register[int],
                          smart_notes_rows{total, super, smart} (when stated)},
             pointers[{label, target}]}
  live      {derived_utc, main_tip, open_pr_count, open_prs[int],
             board{issue, comments}} — null when emitted with --no-live
  sources   [{section, source, anchor}] — where every block came from

VENUE SCRUB: the twin names the LIVE board only. The retired venue 2765
must never appear in the twin (it survives in the .md only as a
distilled-and-released history note in hand-owned prose). emit REFUSES to
write a twin whose serialized bytes contain "2765" and names the cure.

ONE PUBLISHER RULE: this tool writes the twin beside the .md on main. It
does not publish to live/mission-state — that branch's writers (the
state-core tick for STATE-CORE.json, the hourly hub refresh for
MISSION-STATE.md / HUB-STATE.md) are single-writer surfaces owned by
other lanes (L16: no duplicate publishers). Wiring the twin into those
publishes is the owning lanes' step; see tools/MISSION-STATE.md.

Modes:
  emit       build the twin from the .md + live API, validate it against
             the shipped schema, refuse on scrub violation, write it.
             --no-live skips the API (live block = null) for offline use.
  (drift)    tools/check_mission_state_drift.py — the separate check:
             re-derives the snapshot facts from the .md and FAILS if the
             committed twin disagrees on any shared fact.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"
TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
SCHEMA_PATH = TOOLS_DIR / "mission_state.schema.json"
DEFAULT_MD = REPO_ROOT / "BRAIN" / "CURRENT-MISSION-STATE.md"
DEFAULT_OUT = REPO_ROOT / "BRAIN" / "MISSION-STATE.json"
RETIRED_VENUE = "2765"

sys.path.insert(0, str(TOOLS_DIR))
from operating_state import validate  # noqa: E402  (house validator — imported, never re-implemented)


class SnapshotError(ValueError):
    """The .md does not carry a fact the twin is required to state."""


def _fail(what: str, cure: str) -> SnapshotError:
    return SnapshotError(f"MISSING: {what} — CURE: {cure} (owner: director pass)")


def _norm(text: str) -> str:
    """Strip markdown emphasis/backticks and collapse whitespace."""
    text = text.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


# --------------------------------------------------------------------------
# The snapshot parser — the derivation. Every pattern is required unless
# marked optional: when the director changes the snapshot's format, this
# fails loudly instead of emitting a silently partial twin.
# --------------------------------------------------------------------------

def parse_snapshot(md_text: str) -> dict:
    # --- header: last verified + tip state -----------------------------------
    # Live grammar (director pass): the timestamp carries seconds only when the
    # pass emits them (YYYY-MM-DDTHH:MMZ and YYYY-MM-DDTHH:MM:SSZ both parse),
    # and the header alternates between **TIP MOVED** `<from>` → `<to>` and
    # **TIP STATIC** `<tip>` (no move). For STATIC the move is from == to.
    m = re.search(r"\*\*Last verified:\*\*.*?\((\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)\)", md_text)
    if not m:
        raise _fail("snapshot.last_verified_utc",
                    "the snapshot header must carry '**Last verified:** ... (YYYY-MM-DDTHH:MM[:SS]Z)'")
    last_verified = m.group(1)

    m = re.search(r"\*\*TIP MOVED\*\* `([0-9a-f]{40})` → `([0-9a-f]{40})`", md_text)
    if m:
        tip_from, tip_to = m.group(1), m.group(2)
        tip_form = "moved"
    else:
        m = re.search(r"\*\*TIP STATIC\*\* `([0-9a-f]{40})`", md_text)
        if not m:
            raise _fail("snapshot.tip_moved",
                        "the snapshot header must carry '**TIP MOVED** `<from>` → `<to>`' "
                        "or '**TIP STATIC** `<tip>`'")
        tip_from = tip_to = m.group(1)
        tip_form = "static"

    # --- KEY NUMBERS line ---------------------------------------------------
    kn = next((ln for ln in md_text.splitlines() if "**KEY NUMBERS" in ln), None)
    if kn is None:
        raise _fail("snapshot.key_numbers", "the snapshot must carry a '**KEY NUMBERS' line")
    m = re.search(r"`([0-9a-f]{40})`", kn)
    if not m:
        raise _fail("snapshot.main_tip", "the KEY NUMBERS line must name the main tip in backticks")
    main_tip = m.group(1)
    if main_tip != tip_to:
        raise SnapshotError(
            f"SNAPSHOT SELF-DISAGREEMENT: header tip ({tip_form}) lands on {tip_to} but KEY NUMBERS "
            f"names main tip {main_tip} — CURE: the director reconciles the snapshot before "
            f"the twin can be emitted (owner: director pass)")

    # The director's live wording carries an optional unit word: "+7 ids since
    # watermark" (2026-10-22) vs the earlier "+4 since watermark". Accept both;
    # the four numbers stay required.
    m = re.search(r"live board \*\*#(\d+)\*\* \((\d+) count, \+(\d+)(?:\s+[a-zA-Z]+)? since watermark (\d+)", kn)
    if not m:
        raise _fail("snapshot.key_numbers.board",
                    "the KEY NUMBERS line must state 'live board **#N** (C count, +D [unit] since watermark W)'")
    board = {"issue": int(m.group(1)), "comments": int(m.group(2)),
             "delta_since_watermark": int(m.group(3)), "watermark_comment": int(m.group(4))}

    m = re.search(r"open PRs: \d+-register \(([^)]+)\)", kn)
    if not m:
        raise _fail("snapshot.key_numbers.open_prs_register",
                    "the KEY NUMBERS line must state 'open PRs: N-register (#a/#b/#c)'")
    open_prs_register = [int(x) for x in re.findall(r"#(\d+)", m.group(1))]
    if not open_prs_register:
        raise _fail("snapshot.key_numbers.open_prs_register", "the register named no PR numbers")

    key_numbers: dict = {"board": board, "open_prs_register": open_prs_register}
    m = re.search(r"(\d+) rows = (\d+) SUPER \+ (\d+) Smart Notes", md_text)
    if m:  # stated in TOP-10 item 1; carried when stated, never invented
        key_numbers["smart_notes_rows"] = {"total": int(m.group(1)),
                                           "super": int(m.group(2)),
                                           "smart": int(m.group(3))}

    # --- TOP-10 standing section -------------------------------------------
    top_line = next((ln for ln in md_text.splitlines() if ln.startswith("**TOP-10 re-ranked:**")), None)
    if top_line is None:
        raise _fail("snapshot.standing_top10", "the snapshot must carry a '**TOP-10 re-ranked:**' line")
    body = top_line.split("**TOP-10 re-ranked:**", 1)[1].strip()
    parts = re.split(r"\((\d{1,2})\)\s+", body)
    # parts = [prefix, '1', seg1, '2', seg2, ...]
    items = []
    if len(parts) >= 3 and parts[0].strip() == "":
        for i in range(1, len(parts) - 1, 2):
            rank, seg = int(parts[i]), parts[i + 1]
            bold = re.match(r"\*\*(.+?)\*\*", seg)
            headline_raw = bold.group(1).strip() if bold else ""
            carried = False
            if headline_raw.startswith("[carried]"):
                carried = True
                headline = headline_raw[len("[carried]"):].strip()
            elif headline_raw.startswith("[") and headline_raw.endswith("]"):
                headline = headline_raw[1:-1].strip()
            else:
                headline = headline_raw
            items.append({"rank": rank, "headline": headline, "carried": carried,
                          "detail": _norm(seg)})
    if [it["rank"] for it in items] != list(range(1, 11)):
        raise _fail("snapshot.standing_top10",
                    "the TOP-10 line must carry exactly items (1)..(10) in order")

    # --- TEAM STATUS table ---------------------------------------------------
    lines = md_text.splitlines()
    hdr = next((i for i, ln in enumerate(lines)
                if ln.startswith("| Area |") and "Accomplished" in ln), None)
    if hdr is None:
        raise _fail("snapshot.team_status", "the snapshot must carry the '| Area | Accomplished |' table")
    team = []
    for ln in lines[hdr + 1:]:
        if not ln.startswith("|"):
            break
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != 4:
            raise _fail("snapshot.team_status",
                        f"team-status row must have exactly 4 cells, got {len(cells)}: {ln[:60]}")
        team.append({"area": cells[0],
                     "accomplished": None if cells[1] == "—" else cells[1],
                     "working_on": None if cells[2] == "—" else cells[2],
                     "plan": None if cells[3] == "—" else cells[3]})
    if len(team) < 5:
        raise _fail("snapshot.team_status", "the team-status table must carry at least 5 area rows")

    # --- WHERE TO GO pointers -------------------------------------------------
    pointers = []
    in_where = False
    for ln in lines:
        if ln.startswith("## WHERE TO GO"):
            in_where = True
            continue
        if in_where:
            if ln.startswith("## "):
                break
            m = re.match(r"- \*\*(.+?):\*\*\s*(.*)", ln)
            if m:
                rest = m.group(2)
                url = re.search(r"https?://\S+", rest)
                tick = re.search(r"`([^`]+)`", rest)
                target = url.group(0) if url else (tick.group(1) if tick else _norm(rest))
                pointers.append({"label": m.group(1).strip(), "target": target})
    if not pointers:
        raise _fail("snapshot.pointers", "the WHERE TO GO section must carry at least one '- **Label:**' pointer")

    master = next((p for p in pointers if p["label"].startswith("Master directive")), None)
    m = re.search(r"/issues/(\d+)", master["target"]) if master else None
    if not m:
        raise _fail("snapshot.identity.master_directive",
                    "WHERE TO GO must carry a 'Master directive' pointer to its issue")
    identity = {"repo": REPO, "live_board": board["issue"],
                "master_directive": int(m.group(1))}

    return {
        "last_verified_utc": last_verified,
        "main_tip": main_tip,
        "tip_moved": {"from": tip_from, "to": tip_to},
        "identity": identity,
        "standing_top10": items,
        "team_status": team,
        "key_numbers": key_numbers,
        "pointers": pointers,
    }


# --------------------------------------------------------------------------
# Live derivation (pluggable API access — the operating_state pattern, with
# this workspace's gh-app-api wrapper as a candidate; task law: GitHub only
# via the GitHub App token path or gh).
# --------------------------------------------------------------------------

def gh_api(method: str, path: str):
    override = os.environ.get("NAYA_GH_API")
    candidates = []
    if override:
        candidates.append(override.split())
    app_wrapper = Path.home() / "workspace" / "custom-connectors" / "custom.legacy-github" / "bin" / "gh-app-api"
    if app_wrapper.exists():
        candidates.append([str(app_wrapper)])
    naya_wrapper = Path.home() / "workspace" / "naya" / "bin" / "gh-api"
    if naya_wrapper.exists():
        candidates.append([str(naya_wrapper)])
    candidates.append(["gh", "api"])
    last_err = None
    for cmd in candidates:
        try:
            if cmd[0] == "gh":
                full = cmd + ["-X", method, f"repos/{REPO}{path}"]
            else:
                full = cmd + [method, f"/repos/{REPO}{path}"]
            out = subprocess.run(full, capture_output=True, text=True, timeout=120)
            if out.returncode == 0 and out.stdout.strip():
                return json.loads(out.stdout)
            last_err = out.stderr.strip() or out.stdout.strip()
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
    raise RuntimeError(f"gh-api {method} {path} failed: {last_err}")


def _paginated(path: str, per_page: int = 100) -> list:
    items, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = gh_api("GET", f"{path}{sep}per_page={per_page}&page={page}")
        if not batch:
            break
        items.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return items


def derive_live(board_issue: int) -> dict:
    tip = gh_api("GET", "/git/refs/heads/main")["object"]["sha"]
    pulls = _paginated("/pulls?state=open")
    board_obj = gh_api("GET", f"/issues/{board_issue}")
    return {
        "derived_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "main_tip": tip,
        "open_pr_count": len(pulls),
        "open_prs": sorted(p["number"] for p in pulls),
        "board": {"issue": board_issue, "comments": board_obj["comments"]},
    }


# --------------------------------------------------------------------------
# Twin assembly + emit
# --------------------------------------------------------------------------

def build_twin(md_text: str, live: dict | None, generated_utc: str | None = None) -> dict:
    snapshot = parse_snapshot(md_text)
    generated = generated_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sources = [
        {"section": "snapshot", "source": "BRAIN/CURRENT-MISSION-STATE.md",
         "anchor": "director-pass snapshot as committed at emit time (header, TOP-10 line, TEAM STATUS table, KEY NUMBERS line, WHERE TO GO)"},
        {"section": "snapshot.identity.repo", "source": "the repository this file lives in",
         "anchor": "SoulSchoolAcademy/NayaPOWER"},
    ]
    if live is not None:
        sources.append(
            {"section": "live", "source": "GitHub API at emit time",
             "anchor": "GET /git/refs/heads/main; GET /pulls?state=open (paginated); GET /issues/<live_board>"})
    return {
        "schema": "naya.mission-state/1",
        "$schema": "tools/mission_state.schema.json",
        "artifact": {"kind": "mission-state-twin",
                     "generator": "tools/build_mission_state.py",
                     "twin_of": "BRAIN/CURRENT-MISSION-STATE.md",
                     "generated_utc": generated},
        "snapshot": snapshot,
        "live": live,
        "sources": sources,
    }


def emit(md_path: Path, out_path: Path, with_live: bool) -> dict:
    md_text = md_path.read_text(encoding="utf-8")
    board_issue = parse_snapshot(md_text)["identity"]["live_board"]
    live = derive_live(board_issue) if with_live else None
    twin = build_twin(md_text, live)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = validate(twin, schema)
    if errors:
        for e in errors:
            print(e)
        raise SystemExit("REFUSED: the twin does not validate against tools/mission_state.schema.json")
    blob = json.dumps(twin, indent=1, ensure_ascii=False) + "\n"
    if RETIRED_VENUE in blob:
        raise SystemExit(
            f"REFUSED: the twin names retired venue {RETIRED_VENUE} — CURE: the twin names the "
            f"live board only; retired-venue history stays in the .md's hand-owned prose "
            f"(owner: emitter)")
    out_path.write_text(blob, encoding="utf-8")
    return twin


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit the MISSION-STATE.json twin")
    parser.add_argument("mode", nargs="?", default="emit", choices=["emit"])
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--no-live", action="store_true",
                        help="skip the GitHub API; the live block is emitted as null")
    args = parser.parse_args()
    twin = emit(args.md, args.out, with_live=not args.no_live)
    snap = twin["snapshot"]
    print(f"WROTE {args.out}")
    print(f"  snapshot: last_verified {snap['last_verified_utc']} · main_tip {snap['main_tip'][:12]} "
          f"· top10 {len(snap['standing_top10'])} · team rows {len(snap['team_status'])} "
          f"· board #{snap['key_numbers']['board']['issue']} at {snap['key_numbers']['board']['comments']} comments")
    if twin["live"]:
        lv = twin["live"]
        print(f"  live:     tip {lv['main_tip'][:12]} · open PRs {lv['open_pr_count']} "
              f"· board comments {lv['board']['comments']} · derived {lv['derived_utc']}")
    else:
        print("  live:     skipped (--no-live)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
