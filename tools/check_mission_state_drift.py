#!/usr/bin/env python3
"""Mission-state drift check: the prose snapshot and its JSON twin must agree.

The twin (BRAIN/MISSION-STATE.json, built by tools/build_mission_state.py)
exists so a machine reader never parses prose. That only holds if the pair
cannot drift apart silently. This check RE-DERIVES the snapshot facts from
BRAIN/CURRENT-MISSION-STATE.md with the same parser the emitter uses and
compares them, field by field, against the committed twin:

  * any disagreement on a shared fact  -> DRIFT (exit 1), each line naming
    the field, the .md value, the .json value, and the cure;
  * the twin must also validate against tools/mission_state.schema.json
    (house validator, cure lines) and must not name the retired venue 2765;
  * with --live, the twin's live block is additionally compared against a
    fresh GitHub derivation (timestamps excluded): live.main_tip must equal
    GET /git/refs/heads/main NOW, open PRs and board comments must match.

Default mode is offline (no network): it checks the pair as committed.
Exit codes: 0 = no drift · 1 = drift/invalid · 2 = the pair cannot be read.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

import build_mission_state as bms  # noqa: E402
from operating_state import validate  # noqa: E402

CURE = "re-run `python3 tools/build_mission_state.py emit` and commit the regenerated twin (owner: director pass)"


def _walk(md_val, json_val, path: str, lines: list[str]) -> None:
    """Deep-compare two fact structures; append one DRIFT line per mismatch."""
    if isinstance(md_val, dict) and isinstance(json_val, dict):
        for key in sorted(set(md_val) | set(json_val)):
            if key not in md_val:
                lines.append(f"DRIFT: {path}.{key} — in twin only ({json_val[key]!r}) — CURE: {CURE}")
            elif key not in json_val:
                lines.append(f"DRIFT: {path}.{key} — in snapshot only ({md_val[key]!r}) — CURE: {CURE}")
            else:
                _walk(md_val[key], json_val[key], f"{path}.{key}", lines)
    elif isinstance(md_val, list) and isinstance(json_val, list):
        if len(md_val) != len(json_val):
            lines.append(f"DRIFT: {path} — snapshot has {len(md_val)} entries, twin has "
                         f"{len(json_val)} — CURE: {CURE}")
        for i, (a, b) in enumerate(zip(md_val, json_val)):
            _walk(a, b, f"{path}[{i}]", lines)
    elif md_val != json_val:
        lines.append(f"DRIFT: {path} — snapshot: {md_val!r} vs twin: {json_val!r} — CURE: {CURE}")


def run_check(md_path: Path, json_path: Path, live: bool = False) -> tuple[int, list[str]]:
    """Returns (exit_code, report_lines). Never raises for drift — drift is data."""
    lines: list[str] = []
    try:
        md_text = md_path.read_text(encoding="utf-8")
        twin = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return 2, [f"UNREADABLE: {exc} — CURE: restore the snapshot/twin pair (owner: director pass)"]

    schema = json.loads(bms.SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = validate(twin, schema)
    if errors:
        lines.extend(f"INVALID: {e}" for e in errors)

    blob = json.dumps(twin, ensure_ascii=False)
    if bms.RETIRED_VENUE in blob:
        lines.append(f"SCRUB: the twin names retired venue {bms.RETIRED_VENUE} — CURE: the twin "
                     f"names the live board only (owner: emitter)")

    try:
        derived = bms.parse_snapshot(md_text)
    except bms.SnapshotError as exc:
        return 2, lines + [f"UNPARSEABLE SNAPSHOT: {exc}"]

    # snapshot.key_numbers.open_prs_register is machine-derived at emit
    # time (director ruling 2026-10-22, Option C) — it is not a fact the
    # .md states, so it is not a shared fact for the offline pair walk.
    # The --live branch below compares it against a fresh derivation.
    twin_snap = json.loads(json.dumps(twin.get("snapshot", {})))
    twin_snap.get("key_numbers", {}).pop("open_prs_register", None)
    drift: list[str] = []
    _walk(derived, twin_snap, "snapshot", drift)
    lines.extend(drift)

    if live:
        if twin.get("live") is None:
            lines.append("DRIFT: live — twin was emitted --no-live, so no live block to compare "
                         f"— CURE: {CURE}")
        else:
            fresh = bms.derive_live(twin["snapshot"]["identity"]["live_board"])
            live_drift: list[str] = []
            recorded = {k: v for k, v in twin["live"].items() if k != "derived_utc"}
            fresh_cmp = {k: v for k, v in fresh.items() if k != "derived_utc"}
            _walk(fresh_cmp, recorded, "live", live_drift)
            lines.extend(live_drift)
            register = twin.get("snapshot", {}).get("key_numbers", {}).get("open_prs_register")
            if register != fresh["open_prs"]:
                lines.append(f"DRIFT: snapshot.key_numbers.open_prs_register — twin: {register!r} "
                             f"vs fresh live list: {fresh['open_prs']!r} — CURE: {CURE}")
            if not live_drift:
                lines.append(f"LIVE OK: live block matches a fresh derivation "
                             f"(tip {fresh['main_tip'][:12]}, {fresh['open_pr_count']} open PRs, "
                             f"board {fresh['board']['comments']} comments)")

    if any(ln.startswith(("DRIFT", "INVALID", "SCRUB")) for ln in lines):
        return 1, lines
    lines.append(f"NO DRIFT: twin and snapshot agree on every shared fact "
                 f"(snapshot tip {derived['main_tip'][:12]}, {len(derived['standing_top10'])} standing items, "
                 f"{len(derived['team_status'])} team rows, board #{derived['key_numbers']['board']['issue']} "
                 f"at {derived['key_numbers']['board']['comments']} comments)")
    return 0, lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Drift check: CURRENT-MISSION-STATE.md vs MISSION-STATE.json")
    parser.add_argument("--md", type=Path, default=REPO_ROOT / "BRAIN" / "CURRENT-MISSION-STATE.md")
    parser.add_argument("--json", type=Path, default=REPO_ROOT / "BRAIN" / "MISSION-STATE.json")
    parser.add_argument("--live", action="store_true",
                        help="also compare the twin's live block against a fresh GitHub derivation")
    args = parser.parse_args()
    code, lines = run_check(args.md, args.json, live=args.live)
    for ln in lines:
        print(ln)
    return code


if __name__ == "__main__":
    sys.exit(main())
