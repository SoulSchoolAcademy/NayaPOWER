"""Checklist update CLI — for area drivers and seats.

WHY THIS EXISTS
---------------
The sync script (checklist_sync.py) handles PR-driven status automatically.
But some updates are human: notes, blockers, manual items, DONE_WHEN
evidence that isn't a PR. This CLI is the one command for those updates.
It writes to the JSON (source of truth) and regenerates the .md.

USAGE (run from repo root)
--------------------------
    # Update status + note
    python3 tools/checklist_update.py L1 --status "IN PROGRESS" \
        --note "Battery running on Naya 2 seat, 3/14 lessons scored"

    # Flag a blocker
    python3 tools/checklist_update.py B2 --status BLOCKED \
        --blocker "CI red on test_memory_ingest; investigating" \
        --note "Rebase needed after main moved"

    # Mark done with evidence (non-PR item)
    python3 tools/checklist_update.py K2 --status DONE \
        --note "Retrieval precision 92% measured on 2026-10-10, receipt at <link>"

    # Add a PR reference to an item
    python3 tools/checklist_update.py E1 --add-pr 2070

    # Show an item
    python3 tools/checklist_update.py L1 --show

    # List all items with status
    python3 tools/checklist_update.py --list [--status IN_PROGRESS]

Exit codes: 0 = ok, 1 = item not found / bad args, 3 = JSON invalid.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

JSON_PATH = "BRAIN/00-ACTIVATION/ACTIVATION-MASTER-CHECKLIST.json"
MD_PATH = "BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md"

VALID_STATUSES = {"TODO", "IN PROGRESS", "DONE", "BLOCKED", "STALE"}


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(repo_root):
    path = os.path.join(repo_root, JSON_PATH)
    with open(path) as f:
        return json.load(f)


def save(data, repo_root):
    path = os.path.join(repo_root, JSON_PATH)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    # Regenerate MD via the sync module's generator
    sys.path.insert(0, os.path.join(repo_root, "tools"))
    import checklist_sync
    md = checklist_sync.generate_md(data)
    with open(os.path.join(repo_root, MD_PATH), "w") as f:
        f.write(md)


def find_item(data, item_id):
    for section in data["sections"]:
        for item in section.get("items", []):
            if item["id"].upper() == item_id.upper():
                return section, item
    return None, None


def main():
    p = argparse.ArgumentParser(description="Update checklist item")
    p.add_argument("item_id", nargs="?",
                   help="Item ID (e.g. L1, B2, C4)")
    p.add_argument("--status", choices=sorted(VALID_STATUSES),
                   help="New status")
    p.add_argument("--note", help="Note to append to status_detail")
    p.add_argument("--blocker", help="Blocker detail")
    p.add_argument("--add-pr", type=int, action="append", default=[],
                   help="Add a PR reference (repeatable)")
    p.add_argument("--owner", help="Set owner")
    p.add_argument("--show", action="store_true",
                   help="Show item, don't modify")
    p.add_argument("--list", action="store_true",
                   help="List all items")
    p.add_argument("--filter-status", choices=sorted(VALID_STATUSES),
                   help="With --list: filter by status")
    p.add_argument("--repo-root", default=".",
                   help="Repo root directory")
    p.add_argument("--by", default="manual",
                   help="Who is updating (seat/lane name)")
    args = p.parse_args()

    try:
        data = load(args.repo_root)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"FATAL: cannot read checklist JSON: {e}", file=sys.stderr)
        return 3

    if args.list:
        for section in data["sections"]:
            for item in section.get("items", []):
                if (args.filter_status and
                        item["status"] != args.filter_status):
                    continue
                flag = "🔒" if item.get("shawn_gated") else " "
                print(f"{flag} {item['id']:6} [{item['status']:11}] "
                      f"{item['what'][:70]}")
        return 0

    if not args.item_id:
        p.error("item_id required (unless --list)")

    section, item = find_item(data, args.item_id)
    if not item:
        print(f"Item '{args.item_id}' not found.", file=sys.stderr)
        return 1

    if args.show:
        print(json.dumps(item, indent=2, ensure_ascii=False))
        print(f"\nSection: {section['title']}")
        return 0

    changed = []
    old_status = item["status"]

    if args.status and args.status != old_status:
        item.setdefault("history", []).append({
            "at": now_utc(),
            "by": args.by,
            "from": old_status,
            "to": args.status,
            "reason": (args.note or args.blocker or "manual update")[:200],
        })
        item["status"] = args.status
        changed.append(f"status {old_status} → {args.status}")

    if args.note:
        existing = item.get("status_detail", "")
        item["status_detail"] = (
            f"{existing} | {args.note}" if existing else args.note)
        changed.append("note added")

    if args.blocker:
        item["blocker_detail"] = args.blocker
        if item["status"] not in ("BLOCKED", "DONE"):
            item["status"] = "BLOCKED"
            changed.append("status → BLOCKED (blocker set)")
        changed.append("blocker set")

    for pr in args.add_pr:
        if pr not in item.get("pr_refs", []):
            item.setdefault("pr_refs", []).append(pr)
            changed.append(f"PR #{pr} added")

    if args.owner:
        item["owner"] = args.owner
        changed.append(f"owner → {args.owner}")

    if not changed:
        print("No changes specified.")
        return 0

    item["updated_at"] = now_utc()
    data["meta"]["updated_at"] = now_utc()
    save(data, args.repo_root)

    print(f"Updated {item['id']}: {', '.join(changed)}")
    print(f"JSON + MD regenerated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
