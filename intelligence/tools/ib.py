#!/usr/bin/env python3
"""ib — Intelligent Blocks CLI.

Create, read, query, update, and validate the canonical Intelligent Blocks
in intelligence/blocks/. Stdlib only.

Usage:
  ib create --title T --principle P --who W --when D --context C
            [--topics a,b] [--situations S] [--decisions D2] [--evidence-note N]
  ib get IB-0001
  ib list [--topic T] [--status S] [--sort newest|oldest|id]
  ib update IB-0001 --status APPLIED --note "why"
  ib evidence IB-0001 --kind receipt --ref "PR #1234" --note "merged with receipt"
  ib graduate IB-0001 --stage code-gate [--enforced-by path] --next "what moves it up"
  ib validate
  ib reindex
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKS_DIR = os.path.join(ROOT, "blocks")
REGISTRY_PATH = os.path.join(BLOCKS_DIR, "REGISTRY.json")
SCHEMA_VERSION = "1.0"

ID_RE = re.compile(r"^IB-(\d{4})$")
STATUSES = ["UNVERIFIED", "APPLIED", "BEHAVIOR-CHANGE-PROVEN", "COMPOUNDED"]
STAGES = ["text", "briefing", "code-gate"]
EVIDENCE_KINDS = ["receipt", "observation", "code", "test", "direct-word"]

REQUIRED_TOP = ["id", "schema_version", "title", "principle", "source",
                "evidence", "applicability", "verification_status",
                "status_history", "graduation", "supersedes",
                "superseded_by", "created_at", "updated_at"]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def blocks_dir():
    os.makedirs(BLOCKS_DIR, exist_ok=True)
    return BLOCKS_DIR


def load_block(bid):
    path = os.path.join(blocks_dir(), f"{bid}.json")
    if not os.path.exists(path):
        return None, path
    with open(path, encoding="utf-8") as f:
        return json.load(f), path


def save_block(data):
    path = os.path.join(blocks_dir(), f"{data['id']}.json")
    data["updated_at"] = now_iso()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def all_blocks():
    out = []
    for name in sorted(os.listdir(blocks_dir())):
        if name.endswith(".json") and name != "REGISTRY.json" and ID_RE.match(name[:-5]):
            with open(os.path.join(blocks_dir(), name), encoding="utf-8") as f:
                out.append(json.load(f))
    return out


def next_id():
    top = 0
    for b in all_blocks():
        m = ID_RE.match(b["id"])
        if m:
            top = max(top, int(m.group(1)))
    return f"IB-{top + 1:04d}"


def validate_block(data):
    """Return a list of error strings; empty means valid."""
    errors = []
    for field in REQUIRED_TOP:
        if field not in data:
            errors.append(f"missing required field: {field}")
    if errors:
        return errors
    if not ID_RE.match(str(data.get("id", ""))):
        errors.append(f"bad id format (want IB-NNNN): {data.get('id')}")
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"bad schema_version: {data.get('schema_version')}")
    principle = data.get("principle", "")
    if not principle or "\n" in principle.strip():
        errors.append("principle must be a single sentence (one line)")
    if len(principle) > 400:
        errors.append(f"principle too long ({len(principle)} chars) — distill it")
    src = data.get("source", {})
    for k in ["who", "when", "context"]:
        if k not in src or not src[k]:
            errors.append(f"source.{k} missing or empty")
    for i, e in enumerate(data.get("evidence", [])):
        if e.get("kind") not in EVIDENCE_KINDS:
            errors.append(f"evidence[{i}].kind invalid: {e.get('kind')}")
        if not e.get("ref"):
            errors.append(f"evidence[{i}].ref missing")
    app = data.get("applicability", {})
    if not app.get("topics"):
        errors.append("applicability.topics must be a non-empty list")
    for k in ["situations", "decisions"]:
        if k not in app or not app[k]:
            errors.append(f"applicability.{k} missing or empty")
    status = data.get("verification_status")
    if status not in STATUSES:
        errors.append(f"bad verification_status: {status}")
    if status != "UNVERIFIED" and not data.get("evidence"):
        errors.append(f"status {status} requires non-empty evidence")
    hist = data.get("status_history", [])
    if not hist or hist[-1].get("status") != status:
        errors.append("status_history must end with the current verification_status")
    grad = data.get("graduation", {})
    if grad.get("stage") not in STAGES:
        errors.append(f"bad graduation.stage: {grad.get('stage')}")
    if not grad.get("next_step"):
        errors.append("graduation.next_step missing")
    if "enforced_by" not in grad:
        errors.append("graduation.enforced_by missing (use null)")
    return errors


def cmd_create(args):
    bid = next_id()
    evidence = []
    if args.evidence_note:
        evidence.append({"kind": "direct-word", "ref": args.evidence_note,
                         "note": "Captured at creation."})
    data = {
        "id": bid,
        "schema_version": SCHEMA_VERSION,
        "title": args.title,
        "principle": args.principle,
        "source": {"who": args.who, "when": args.when, "context": args.context},
        "evidence": evidence,
        "applicability": {
            "topics": [t.strip().lower() for t in (args.topics or "").split(",") if t.strip()],
            "situations": args.situations or "",
            "decisions": args.decisions or "",
        },
        "verification_status": "UNVERIFIED",
        "status_history": [{"status": "UNVERIFIED", "at": now_iso(),
                            "note": "Created via ib CLI."}],
        "graduation": {"stage": "text", "next_step": "Inject into briefing if load-bearing.",
                       "enforced_by": None},
        "supersedes": None,
        "superseded_by": None,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    errs = validate_block(data)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    path = save_block(data)
    print(f"created {bid} -> {path}")
    return 0


def cmd_get(args):
    data, path = load_block(args.id.upper())
    if data is None:
        print(f"not found: {args.id} ({path})")
        return 1
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def cmd_list(args):
    blocks = all_blocks()
    if args.topic:
        blocks = [b for b in blocks if args.topic.lower() in b["applicability"]["topics"]]
    if args.status:
        blocks = [b for b in blocks if b["verification_status"] == args.status.upper()]
    key = {"newest": lambda b: b["created_at"], "oldest": lambda b: b["created_at"],
           "id": lambda b: b["id"]}[args.sort]
    blocks.sort(key=key, reverse=(args.sort == "newest"))
    if args.format == "json":
        print(json.dumps([
            {"id": b["id"], "title": b["title"], "principle": b["principle"],
             "topics": b["applicability"]["topics"],
             "verification_status": b["verification_status"],
             "graduation_stage": b["graduation"]["stage"]}
            for b in blocks], indent=2, ensure_ascii=False))
        return 0
    print(f"{'ID':<10}{'STATUS':<24}{'STAGE':<10}TITLE")
    for b in blocks:
        print(f"{b['id']:<10}{b['verification_status']:<24}"
              f"{b['graduation']['stage']:<10}{b['title']}")
    print(f"\n{len(blocks)} block(s)")
    return 0


def cmd_evidence(args):
    bid = args.id.upper()
    data, _ = load_block(bid)
    if data is None:
        print(f"not found: {bid}")
        return 1
    if args.kind not in EVIDENCE_KINDS:
        print(f"bad kind (want one of {EVIDENCE_KINDS})")
        return 1
    data["evidence"].append({"kind": args.kind, "ref": args.ref,
                             "note": args.note or ""})
    errs = validate_block(data)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(f"  - {e}")
        return 1
    save_block(data)
    print(f"added evidence to {bid} ({len(data['evidence'])} total)")
    return 0


def cmd_update(args):
    bid = args.id.upper()
    data, _ = load_block(bid)
    if data is None:
        print(f"not found: {bid}")
        return 1
    status = args.status.upper()
    if status not in STATUSES:
        print(f"bad status (want one of {STATUSES})")
        return 1
    cur_idx = STATUSES.index(data["verification_status"])
    new_idx = STATUSES.index(status)
    if new_idx < cur_idx:
        print(f"refusing downgrade {data['verification_status']} -> {status} "
              f"(supersede instead)")
        return 1
    data["verification_status"] = status
    data["status_history"].append({"status": status, "at": now_iso(),
                                   "note": args.note or ""})
    errs = validate_block(data)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(f"  - {e}")
        return 1
    save_block(data)
    print(f"updated {bid} -> {status}")
    return 0


def cmd_graduate(args):
    bid = args.id.upper()
    data, _ = load_block(bid)
    if data is None:
        print(f"not found: {bid}")
        return 1
    if args.stage not in STAGES:
        print(f"bad stage (want one of {STAGES})")
        return 1
    cur_idx = STAGES.index(data["graduation"]["stage"])
    new_idx = STAGES.index(args.stage)
    if new_idx < cur_idx:
        print(f"refusing graduation downgrade "
              f"{data['graduation']['stage']} -> {args.stage}")
        return 1
    data["graduation"]["stage"] = args.stage
    data["graduation"]["enforced_by"] = args.enforced_by
    data["graduation"]["next_step"] = args.next
    errs = validate_block(data)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(f"  - {e}")
        return 1
    save_block(data)
    print(f"graduated {bid} -> {args.stage}")
    return 0


def cmd_validate(_args):
    blocks = all_blocks()
    seen = set()
    failed = 0
    for b in blocks:
        errs = validate_block(b)
        if b["id"] in seen:
            errs.append(f"duplicate id: {b['id']}")
        seen.add(b["id"])
        if errs:
            failed += 1
            print(f"{b['id']}: FAIL")
            for e in errs:
                print(f"    - {e}")
    print(f"\n{len(blocks) - failed}/{len(blocks)} blocks valid")
    return 1 if failed else 0


def cmd_reindex(_args):
    blocks = all_blocks()
    entries = [
        {
            "id": b["id"],
            "title": b["title"],
            "principle": b["principle"],
            "topics": b["applicability"]["topics"],
            "verification_status": b["verification_status"],
            "graduation_stage": b["graduation"]["stage"],
            "created_at": b["created_at"],
            "updated_at": b["updated_at"],
            "path": f"intelligence/blocks/{b['id']}.json",
        }
        for b in sorted(blocks, key=lambda x: x["id"])
    ]
    # Idempotent: if the entries are unchanged, keep the old file untouched
    # (including its generated_at) so a no-op reindex is git-clean.
    generated_at = now_iso()
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, encoding="utf-8") as f:
            old = json.load(f)
        if old.get("blocks") == entries and old.get("count") == len(blocks):
            print(f"registry unchanged ({len(blocks)} blocks) - {REGISTRY_PATH}")
            return 0
        generated_at = old.get("generated_at", generated_at)
    reg = {
        "generated_at": generated_at,
        "schema_version": SCHEMA_VERSION,
        "count": len(blocks),
        "blocks": entries,
    }
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"reindexed {len(blocks)} blocks -> {REGISTRY_PATH}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="ib", description="Intelligent Blocks CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="create the next block")
    c.add_argument("--title", required=True)
    c.add_argument("--principle", required=True, help="one sentence, plain words")
    c.add_argument("--who", required=True)
    c.add_argument("--when", required=True)
    c.add_argument("--context", required=True)
    c.add_argument("--topics", default="", help="comma-separated, e.g. process,merging")
    c.add_argument("--situations", default="")
    c.add_argument("--decisions", default="")
    c.add_argument("--evidence-note", default="")

    g = sub.add_parser("get", help="print one block")
    g.add_argument("id")

    l = sub.add_parser("list", help="list/search blocks")
    l.add_argument("--topic", default="")
    l.add_argument("--status", default="")
    l.add_argument("--sort", default="id", choices=["id", "newest", "oldest"])
    l.add_argument("--format", default="table", choices=["table", "json"],
                   help="table for humans, json for agents")

    u = sub.add_parser("update", help="advance verification status")
    u.add_argument("id")
    u.add_argument("--status", required=True)
    u.add_argument("--note", default="")

    e = sub.add_parser("evidence", help="attach evidence to a block")
    e.add_argument("id")
    e.add_argument("--kind", required=True, choices=EVIDENCE_KINDS)
    e.add_argument("--ref", required=True)
    e.add_argument("--note", default="")

    gr = sub.add_parser("graduate", help="move up the graduation path")
    gr.add_argument("id")
    gr.add_argument("--stage", required=True, choices=STAGES)
    gr.add_argument("--enforced-by", default=None)
    gr.add_argument("--next", required=True)

    sub.add_parser("validate", help="validate all blocks")
    sub.add_parser("reindex", help="rebuild REGISTRY.json")

    args = p.parse_args(argv)
    return {
        "create": cmd_create, "get": cmd_get, "list": cmd_list,
        "update": cmd_update, "graduate": cmd_graduate,
        "evidence": cmd_evidence,
        "validate": cmd_validate, "reindex": cmd_reindex,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
