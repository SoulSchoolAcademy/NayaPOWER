#!/usr/bin/env python3
"""Read-only, source-bound Intelligence Board over the canonical World Model.

Does not create a brain, store, scheduler, verifier, permission grant or
decision engine. Acts as human/machine projection; LAW + Compass remain separate.

    python3 tools/intelligence_board.py --format markdown
    python3 tools/intelligence_board.py --format json
    python3 tools/intelligence_board.py --world-model /path/to/snapshot.json
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from world_model import FRESHNESS_LIMITS, MODEL_PATH, section_usable

REPO_URL = "https://github.com/SoulSchoolAcademy/NayaPOWER"
MISSION_URL = f"{REPO_URL}/issues/2154"
TEAM_URL = f"{REPO_URL}/issues/2175"
LEDGER_URL = f"{REPO_URL}/issues/2396"
PROTOCOL_URL = f"{REPO_URL}/blob/main/PROTOCOL.md"
SCHEMA = "naya-intelligence-board/v1"
MANDATORY = ("tip", "mission")


def _section(sections: dict[str, Any], name: str) -> dict[str, Any]:
    raw = sections.get(name)
    return raw if isinstance(raw, dict) else {}


def _briefing_rows(preview: Any, maximum: int = 5) -> list[str]:
    """Quote mission priorities as source-reported, never commands or verified proof."""
    if not isinstance(preview, str):
        return []
    in_priorities = False
    rows = []
    for line in preview.splitlines():
        if line.strip().lower().startswith("## right now"):
            in_priorities = True
            continue
        if in_priorities and line.startswith("## "):
            break
        if in_priorities:
            item = line.strip()
            if len(item) > 2 and item[0] in "123456789" and item[1:3] == ". ":
                rows.append(item[:440])
                if len(rows) >= maximum:
                    break
    return rows


def build_board(model: Any) -> dict[str, Any]:
    """No side effects. Factual assertions require World Model's freshness gate."""
    sections = model.get("sections", {}) if isinstance(model, dict) else {}
    sections = sections if isinstance(sections, dict) else {}
    freshness = {}
    for name in FRESHNESS_LIMITS:
        item = _section(sections, name)
        usable, state = section_usable(name, sections)
        freshness[name] = {
            "usable": bool(usable), "state": state,
            "as_of_utc": item.get("as_of_utc"),
            "source_status": item.get("status", "UNKNOWN"),
        }

    ready = all(freshness[name]["usable"] for name in MANDATORY)
    tip, mission, prs, lanes, ledger, laws = (
        _section(sections, name)
        for name in ("tip", "mission", "prs", "lanes", "ledger", "laws")
    )
    verified_tip = tip.get("sha") if freshness["tip"]["usable"] else None
    if not isinstance(verified_tip, str) or len(verified_tip) != 40:
        verified_tip, ready = None, False

    # World Model captures only body[:2000]. A fresh section timestamp does
    # NOT imply its source-reported priority list is complete. A 2000-char
    # preview may have omitted critical later mission priorities: fail closed
    # rather than issue a misleading "current orientation" verdict.
    preview = mission.get("body_preview")
    preview_partial = bool(
        freshness["mission"]["usable"]
        and isinstance(preview, str)
        and len(preview) >= 2000
    )
    if preview_partial:
        ready = False
    priorities = (_briefing_rows(preview)
                  if freshness["mission"]["usable"] and not preview_partial else [])

    lane_view = {}
    if freshness["lanes"]["usable"] and isinstance(lanes.get("lanes"), dict):
        for name, lane in lanes["lanes"].items():
            if not isinstance(lane, dict):
                continue
            lane_view[str(name)] = {
                "state": lane.get("state") if lane.get("status") == "OK" else "UNKNOWN",
                "issue": lane.get("issue"),
                "interpretation": "observation only, not exclusive work lease",
            }

    return {
        "schema": SCHEMA,
        "kind": "READ_ONLY_ORIENTATION_PROJECTION",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "readiness": "ORIENTATION_CURRENT" if ready else "READ_MORE",
        "freshness": freshness,
        "in_a_nutshell": (
            "One evidence-linked picture of mission, work, proof, law orientation "
            "and next review. Not an authorization."
        ),
        "how_it_works": (
            "World Model -> freshness gate -> Intelligence Board -> human/AI/machine "
            "view -> Compass + current LAW for actual decisions."
        ),
        "current_reality": {
            "main_sha": verified_tip,
            "mission": {
                "status": ("PARTIAL_PREVIEW" if preview_partial else
                           "SOURCE_REPORTED" if freshness["mission"]["usable"] else
                           "UNKNOWN"),
                "title": mission.get("title") if freshness["mission"]["usable"] else None,
                "priorities": priorities,
                "preview_may_be_truncated": preview_partial,
                "source": MISSION_URL,
            },
            "open_pr_count": (prs.get("count") if freshness["prs"]["usable"]
                              and isinstance(prs.get("count"), int) else None),
            "open_pr_count_status": (
                "OBSERVED" if freshness["prs"]["usable"]
                and isinstance(prs.get("count"), int) else freshness["prs"]["state"]
            ),
            "lanes": lane_view,
            "proof": {
                "status": "LEDGER_METADATA_ONLY" if freshness["ledger"]["usable"] else "UNKNOWN",
                "updated_at": ledger.get("updated_at")
                if freshness["ledger"]["usable"] else None,
                "source": LEDGER_URL,
                "causal_outcome_verified": None,
            },
        },
        "what_changed": {
            "status": "NOT_MEASURED",
            "reason": "One snapshot cannot establish a delta or independently verified outcome.",
            "source": f"{REPO_URL}/blob/main/ACTIVITY-FEED.md",
        },
        "what_matters": priorities if ready else [],
        "what_is_blocked": {
            "status": "REQUIRES_SOURCE_REVIEW",
            "reason": "Mission prose is not independent merge/production verification.",
            "source": MISSION_URL,
        },
        "what_next": {
            "verdict": "READ_MORE",
            "action": (
                "Read the COMPLETE live mission issue #2154 before choosing work; "
                "its cached 2000-character preview cannot prove priority completeness."
                if preview_partial else
                "Refresh missing or stale World Model sections first."
                if not ready else
                "Review the highest current mission priority with Compass; "
                "re-check LAW, ownership and exact proof before ACT."
            ),
            "authorized": False,
            "decision_engine": "kernel/value_calculus.py",
            "compass": "tools/nayas_guide.py",
        },
        "laws": {
            "status": "ORIENTATION_ONLY" if freshness["laws"]["usable"] else "UNKNOWN",
            "briefing_headers": (
                list(laws.get("headers", []))[:8] if freshness["laws"]["usable"]
                and isinstance(laws.get("headers"), list) else []
            ),
            "authority_proven": False,
            "source": PROTOCOL_URL,
            "warning": "Cached headings and scores are not grants or ratification receipts.",
        },
        "connections": {
            "mission": MISSION_URL,
            "team_feed": TEAM_URL,
            "ledger": LEDGER_URL,
            "protocol": PROTOCOL_URL,
            "world_model": f"{REPO_URL}/blob/main/tools/world_model.py",
            "compass": f"{REPO_URL}/blob/main/tools/nayas_guide.py",
        },
    }


def render_markdown(board: dict[str, Any]) -> str:
    reality = board["current_reality"]
    tip = reality["main_sha"] or "UNKNOWN — refresh live tip"
    count = reality["open_pr_count"]
    lines = [
        "# Naya Intelligence Board",
        f"**Read-only orientation:** {board['readiness']}",
        f"**Generated:** {board['generated_utc']}", "",
        "## In a nutshell", board["in_a_nutshell"], "",
        "## How it works", board["how_it_works"], "",
        "## What is true right now?",
        f"- Main: {tip}",
        f"- Mission: {reality['mission']['title'] or 'UNKNOWN'} — {MISSION_URL}",
        f"- Open PR count: {count if count is not None else 'UNKNOWN'} "
        f"({reality['open_pr_count_status']})",
        "- Independent outcome proof: UNKNOWN (ledger metadata is not a causal receipt)",
        "", "## What matters (source-reported; not independently verified)",
    ]
    lines.extend(f"- {item}" for item in board["what_matters"])
    if not board["what_matters"]:
        lines.append("- UNKNOWN / READ_MORE — refresh mission state.")
    if reality["mission"]["preview_may_be_truncated"]:
        lines.append("- PARTIAL PREVIEW: read the complete mission issue before choosing work.")
        lines.append("- Missing priorities are not filled by simply refreshing this truncated cache.")
    lines.extend([
        "", "## What changed?",
        "- NOT MEASURED by a single snapshot. See " + board["what_changed"]["source"],
        "", "## What is blocked?",
        f"- {board['what_is_blocked']['status']} — {MISSION_URL}",
        "", "## What happens next?",
        "- " + board["what_next"]["action"],
        "- No authorization is inferred. Compass, current LAW and receipts govern action.",
        "", "## Laws, links and successor continuity",
        f"- Laws: {board['laws']['status']}; cached headings are not authority.",
        f"- Team: {TEAM_URL}",
        f"- Ledger: {LEDGER_URL}",
        f"- Protocol: {PROTOCOL_URL}",
        "", "## Data freshness",
    ])
    for name, fact in board["freshness"].items():
        lines.append(f"- {name}: {fact['state']} / {fact['source_status']}, "
                     f"as of {fact['as_of_utc'] or 'UNKNOWN'}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world-model", type=Path, default=MODEL_PATH)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    try:
        model = json.loads(args.world_model.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        import sys
        print(f"READ_MORE: World Model unavailable ({exc})", file=sys.stderr)
        model = {"sections": {}}
    board = build_board(model)
    print(json.dumps(board, indent=2) if args.format == "json"
          else render_markdown(board))
    return 0 if board["readiness"] == "ORIENTATION_CURRENT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
