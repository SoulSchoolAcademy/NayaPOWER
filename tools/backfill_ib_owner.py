#!/usr/bin/env python3
"""Backfill `owner` across the Smart Note projection index entries.

w187 BUILD — Naya Beta. ITEM 5 (IB owners = NAYA, Shawn 2026-10-14):
every projection-index entry names its accountable Naya seat.

SAFETY MODEL:
  - Default mode is DRY RUN (read-only): coverage + would-assign distribution.
  - --apply writes ONLY through registry_transaction (one writer, flocked,
    atomic temp+replace) and VERIFIES INSIDE THE TRANSACTION, before commit:
      (1) every entry carries an owner matching the named-seat pattern
      (2) corpus_manifest_hash recomputed via the single hashing authority
      (3) all non-owner entry content byte-identical (canonical sha256 of
          entries-with-owner-stripped, before == after)
      (4) smart_note_id / intelligent_block_id sets unchanged
    Any check failing raises -> the transaction aborts with NO write.
  - Verify on a COPY first: --index /path/to/copy.json

Usage:
  python3 tools/backfill_ib_owner.py                        # dry run, read-only
  python3 tools/backfill_ib_owner.py --index /tmp/copy.json --apply --receipt /tmp/receipt.json
  python3 tools/backfill_ib_owner.py --apply                 # the worktree index (the real backfill)
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tools"))

import smart_note_v2 as s2  # noqa: E402  (the single hashing + writer authority)

STRIP_KEYS = ("owner", "owner_source")


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_capture_map(root):
    """smart_note_id (upper) -> capture dict, from .naya/capture/*.json."""
    cap_dir = Path(root) / ".naya" / "capture"
    m = {}
    if not cap_dir.is_dir():
        return m
    for f in sorted(cap_dir.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        sn = str(d.get("smart_note_id") or "").strip().upper()
        if sn and sn not in m:
            m[sn] = d
    return m


def resolve_entry_owner(entry, capture):
    """Owner for one index entry. Entry's own category/topic/title stand in
    for capture fields when the capture file is missing."""
    if capture is not None:
        return s2.resolve_ib_owner(capture, None)
    pseudo = {
        "category": entry.get("category", ""),
        "topic": entry.get("topic", ""),
        "subtopic": entry.get("subtopic", ""),
        "title": entry.get("title", ""),
        "source": {"captured_by": ""},
    }
    return s2.resolve_ib_owner(pseudo, None)


def assign(registry, capture_map):
    """Return (assigned_entries, report). Pure: does not mutate."""
    report = {"assigned": 0, "already_had_owner": 0, "by_source": {}, "missing_capture": 0}
    out = []
    for e in registry.get("entries", []):
        e2 = dict(e)
        if e2.get("owner") and s2._OWNER_EXPLICIT_RE.match(str(e2["owner"])):
            report["already_had_owner"] += 1
            out.append(e2)
            continue
        sn = str(e2.get("smart_note_id") or "").strip().upper()
        capture = capture_map.get(sn)
        if capture is None:
            report["missing_capture"] += 1
        owner, src = resolve_entry_owner(e2, capture)
        e2["owner"] = owner
        e2["owner_source"] = src
        report["assigned"] += 1
        report["by_source"][src] = report["by_source"].get(src, 0) + 1
        report["by_source"]["owner:" + owner] = report["by_source"].get("owner:" + owner, 0) + 1
        out.append(e2)
    return out, report


def verify(registry, before_entries_stripped_sha, before_sn_set, before_ib_set):
    entries = registry.get("entries", [])
    bad = [str(e.get("smart_note_id")) for e in entries
           if not s2._OWNER_EXPLICIT_RE.match(str(e.get("owner") or ""))]
    if bad:
        raise SystemExit("VERIFY-FAIL: entries with invalid/missing owner: %s" % bad[:10])
    stripped = [{k: v for k, v in e.items() if k not in STRIP_KEYS} for e in entries]
    after_sha = sha(canonical(stripped))
    if after_sha != before_entries_stripped_sha:
        raise SystemExit("VERIFY-FAIL: non-owner entry content changed "
                         "(before %s after %s)" % (before_entries_stripped_sha[:12], after_sha[:12]))
    sn_set = {str(e.get("smart_note_id")) for e in entries}
    ib_set = {str(e.get("intelligent_block_id")) for e in entries}
    if sn_set != before_sn_set or ib_set != before_ib_set:
        raise SystemExit("VERIFY-FAIL: entry identity sets changed")
    manifest = registry.get("corpus_manifest_hash")
    if manifest != s2._corpus_manifest_hash(entries):
        raise SystemExit("VERIFY-FAIL: corpus_manifest_hash != hashing authority")
    return after_sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=None, help="registry path (default: worktree index)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args()

    rp = Path(a.index) if a.index else s2.REGISTRY
    capture_map = load_capture_map(REPO)
    raw = json.loads(Path(rp).read_text(encoding="utf-8"))
    before_entries = raw.get("entries", [])
    before_stripped_sha = sha(canonical([{k: v for k, v in e.items() if k not in STRIP_KEYS}
                                        for e in before_entries]))
    before_sn = {str(e.get("smart_note_id")) for e in before_entries}
    before_ib = {str(e.get("intelligent_block_id")) for e in before_entries}
    n_missing = sum(1 for e in before_entries if not e.get("owner"))
    new_entries, report = assign(raw, capture_map)

    print("index:", rp)
    print("entries:", len(before_entries), "| missing owner:", n_missing,
          "| already owned:", report["already_had_owner"])
    print("would-assign by source:")
    for k in sorted(report["by_source"]):
        print("   %4d  %s" % (report["by_source"][k], k))

    receipt = {"index": str(rp), "entries": len(before_entries),
               "missing_owner_before": n_missing,
               "report": report,
               "before_entries_stripped_sha256": before_stripped_sha,
               "before_manifest": raw.get("corpus_manifest_hash")}

    if not a.apply:
        print("DRY RUN — no write. Re-run with --apply to write via registry_transaction.")
        if a.receipt:
            Path(a.receipt).write_text(json.dumps(receipt, indent=1), encoding="utf-8")
        return 0

    # --apply: verify INSIDE the transaction, before commit. Failure aborts, no write.
    with s2.registry_transaction(str(rp)) as registry:
        reg_entries = registry.get("entries", [])
        stripped_sha = sha(canonical([{k: v for k, v in e.items() if k not in STRIP_KEYS}
                                      for e in reg_entries]))
        live_new, live_report = assign(registry, capture_map)
        registry["entries"] = live_new
        registry["corpus_manifest_hash"] = s2._corpus_manifest_hash(live_new)
        after_sha = verify(registry,
                           stripped_sha,
                           {str(e.get("smart_note_id")) for e in reg_entries},
                           {str(e.get("intelligent_block_id")) for e in reg_entries})
    final = json.loads(Path(rp).read_text(encoding="utf-8"))
    receipt.update({"applied": True,
                    "after_entries_stripped_sha256": after_sha,
                    "stripped_sha_match": after_sha == before_stripped_sha,
                    "after_manifest": final.get("corpus_manifest_hash"),
                    "all_entries_owned": all(bool(e.get("owner")) for e in final.get("entries", []))})
    print("APPLIED. stripped-content sha match:", after_sha == before_stripped_sha)
    print("manifest before:", receipt["before_manifest"][:12], "-> after:", receipt["after_manifest"][:12])
    if a.receipt:
        Path(a.receipt).write_text(json.dumps(receipt, indent=1), encoding="utf-8")
        print("receipt:", a.receipt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
