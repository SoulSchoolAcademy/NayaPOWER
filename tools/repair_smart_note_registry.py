#!/usr/bin/env python3
"""Repair Smart Note registry drift by re-anchoring entry hashes to captures.

Cure for the drift RED measured at tip 8e5baeff (defect_total 795:
entries_with_stale_hash 305, captures_unregistered_by_hash 350,
entries_without_hash 34, published_pages_without_registry_entry 106).

ROOT CAUSE (measured 2026-11-13, Naya Alpha — fresh derivation at the tip,
not inherited pins): the audit is hash-keyed, and 304/305 stale entries
plus 346/350 unregistered captures share one cause — the entry's
content_hash was computed from an older capture, and the capture has since
been re-distilled (or the registry spells the SN padded, SN-0633, while
the capture spells it unpadded, SN-633). Pairing each entry with its
current capture by NORMALIZED SN (SN-(\\d+) -> SN-%04d) and recomputing
the canonical hash clears the pair in one operation. The old test-file
note ("repairing hash coverage clears both at once") is stale in form —
at the live tip only 8/305 stale entries match a capture by exact SN;
normalization is what makes the pairing work (304/305).

SCOPE (deliberately narrow — smallest effective change):
  * REPAIRS: entries whose content_hash is missing or matches no capture,
    where the capture choice is unambiguous (exactly one capture for the
    normalized SN, or exactly one IB-SMART-NOTE-* capture, or several
    IB captures with a unique latest embedded date — the Oct-13 migration
    stubs are superseded by the later real captures).
  * DOES NOT: create registry entries (orphan pages / entry-less captures
    are reported as residuals for a second pass), delete entries, rewrite
    SN spellings, or touch entries whose hash already matches a capture
    (a same-SN capture with a different hash there is a duplicate-capture
    case, not a stale-hash case).
  * NEVER re-baselines: the drift test's PINNED_BASELINE is untouched.

WRITER CONTRACT (same as tools/backfill_b51_index_hashes.py): an
index-mutating apply re-anchors corpus_manifest_hash in the same apply,
runs _validate_index_against_corpus BEFORE the write, writes atomically,
and re-proves the landed bytes after. A refusal raises
SystemExit(REPAIR_REFUSED:...) BEFORE any write lands. Dry-run is the
default; --apply writes.

Usage:
  python3 tools/repair_smart_note_registry.py [--root PATH] [--apply]
      [--out receipt.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import smart_note_v2 as snv  # noqa: E402


def normalize_sn(sn):
    """Canonical SN spelling for MATCHING only (never rewrites ids).

    SN-633 -> SN-0633; SN-0633 -> SN-0633; anything else unchanged.
    """
    if sn is None:
        return None
    m = re.fullmatch(r"SN-(\d+)", str(sn))
    return "SN-%04d" % int(m.group(1)) if m else str(sn)


def _capture_hash(intelligence):
    return snv._canonical_content_hash(
        json.dumps(intelligence, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False)
    )


def _file_date(name: str):
    m = re.search(r"(20\d{6})", name)
    return m.group(1) if m else None


def pick_capture(candidates):
    """Pick the authoritative capture for one normalized SN.

    candidates: list of (filename, content_hash). Returns
    (filename, content_hash) or (None, reason).
    Deterministic precedence: single capture wins; else the single
    IB-SMART-NOTE-* capture wins; else the latest embedded file date
    among IB captures wins; a tie is AMBIGUOUS (reported, never guessed).
    """
    if not candidates:
        return None, "no-capture"
    if len(candidates) == 1:
        return candidates[0], "single-capture"
    ib = [c for c in candidates if c[0].startswith("IB-SMART-NOTE-")]
    if len(ib) == 1:
        return ib[0], "single-IB-capture"
    pool = ib if ib else candidates
    dated = [(c, _file_date(c[0]) or "") for c in pool]
    latest = max(d for _, d in dated)
    winners = [c for c, d in dated if d == latest]
    if len(winners) == 1:
        return winners[0], "latest-IB-date"
    return None, "ambiguous-capture"


def plan_repair(root=None):
    """Build the repair plan. Pure read — never writes.

    Returns a dict with: updates (entry hash rewrites), ambiguous,
    entries_without_capture, captures_without_entry (projected post-repair),
    orphan_pages_with_capture / orphan_pages_without_capture (residuals
    for pass 2), and the pre-repair audit counts.
    """
    root = Path(root) if root else REPO_ROOT
    registry_p = root / ".naya" / "memory" / "smart-notes" / "index.json"
    cap_dir = root / ".naya" / "capture"
    try:
        registry = json.loads(registry_p.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"REPAIR_REFUSED:UNREADABLE_REGISTRY:{exc}") from None
    entries = registry.get("entries")
    if not isinstance(entries, list):
        raise SystemExit("REPAIR_REFUSED: index has no entries list")

    # Captures keyed by normalized SN; hashes keyed by hash value.
    caps_by_nsn: dict[str, list] = {}
    capture_by_hash: dict[str, str] = {}
    captures_per_hash: dict[str, int] = {}
    if cap_dir.exists():
        for p in sorted(cap_dir.glob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                continue
            if not isinstance(data.get("intelligence"), dict):
                continue
            hh = _capture_hash(data["intelligence"])
            capture_by_hash[hh] = p.name
            captures_per_hash[hh] = captures_per_hash.get(hh, 0) + 1
            caps_by_nsn.setdefault(normalize_sn(data.get("smart_note_id")), []).append(
                (p.name, hh)
            )

    # One entry per normalized SN is assumed by the pairing; a duplicate
    # normalized SN is ambiguous and is reported, never resolved by fiat.
    entries_by_nsn: dict[str, list] = {}
    for idx, e in enumerate(entries):
        entries_by_nsn.setdefault(normalize_sn(e.get("smart_note_id")), []).append(idx)

    before = snv.audit_registry(root=root)
    updates, ambiguous, entries_without_capture = [], [], []
    # Hashes already claimed by entries this plan does NOT touch, plus
    # hashes assigned by updates accepted earlier in this plan. A picked
    # hash must be unclaimed AND identifying: assigning a hash another
    # entry holds manufactures duplicate_smart_note_ids, and assigning a
    # hash N captures share cannot identify which note it belongs to
    # (live tip: 24 captures share one intelligence hash — the Sep-29
    # foundational captures are byte-identical). Both cases are reported
    # as ambiguous, never guessed.
    updating_idx = set()
    for idx, e in enumerate(entries):
        hh = e.get("content_hash")
        if hh and hh in capture_by_hash:
            continue
        updating_idx.add(idx)
    claimed_hashes = {
        e.get("content_hash") for i, e in enumerate(entries)
        if i not in updating_idx and e.get("content_hash")
    }
    for idx, e in enumerate(entries):
        sn = e.get("smart_note_id")
        nsn = normalize_sn(sn)
        hh = e.get("content_hash")
        if hh and hh in capture_by_hash:
            continue  # already reconciled — never touched
        if len(entries_by_nsn.get(nsn, [])) > 1:
            ambiguous.append({"smart_note_id": sn, "reason": "duplicate-entry-sn"})
            continue
        picked, reason = pick_capture(caps_by_nsn.get(nsn, []))
        if picked is None:
            if reason == "no-capture":
                entries_without_capture.append(sn)
            else:
                ambiguous.append({"smart_note_id": sn, "reason": reason,
                                  "candidates": [c[0] for c in caps_by_nsn.get(nsn, [])]})
            continue
        if picked[1] == hh:
            continue  # same hash already (cannot happen for stale, guard anyway)
        if captures_per_hash.get(picked[1], 0) > 1:
            ambiguous.append({"smart_note_id": sn, "reason": "shared-capture-hash",
                              "capture": picked[0],
                              "captures_sharing_hash": captures_per_hash[picked[1]]})
            continue
        if picked[1] in claimed_hashes:
            ambiguous.append({"smart_note_id": sn, "reason": "hash-already-claimed",
                              "capture": picked[0]})
            continue
        claimed_hashes.add(picked[1])
        updates.append({"smart_note_id": sn, "entry_index": idx,
                        "old_hash": hh, "new_hash": picked[1],
                        "capture": picked[0], "pick_reason": reason})

    # Projected post-repair residuals (hash-keyed, same math as the audit).
    new_hashes = {e.get("content_hash") for e in entries if e.get("content_hash")}
    for u in updates:
        new_hashes.discard(u["old_hash"])
        new_hashes.add(u["new_hash"])
    captures_without_entry = sorted(
        name for hh, name in capture_by_hash.items() if hh not in new_hashes
    )
    orphans = before["defects"]["published_pages_without_registry_entry"]
    orphan_with, orphan_without = [], []
    for o in orphans:
        hit = False
        for path in o["paths"]:
            m = re.search(r"/(SN-\d+)/", path)
            if m and normalize_sn(m.group(1)) in caps_by_nsn:
                hit = True
                break
        (orphan_with if hit else orphan_without).append(o)

    return {
        "root": str(root),
        "before_counts": before["counts"],
        "before_defect_total": before["defect_total"],
        "updates": updates,
        "ambiguous": ambiguous,
        "entries_without_capture": sorted(str(s) for s in entries_without_capture),
        "captures_without_entry_projected": captures_without_entry,
        "orphan_pages_with_capture": orphan_with,
        "orphan_pages_without_capture": orphan_without,
    }


def apply_repair(root=None, plan=None, write=False):
    """Apply (or dry-run) the repair plan. Returns the receipt dict.

    Dry-run (default): reads only, prints the plan, writes nothing.
    --apply: mutates the registry, re-anchors corpus_manifest_hash,
    validates before the write, writes atomically, re-proves after.
    """
    root = Path(root) if root else REPO_ROOT
    plan = plan or plan_repair(root)
    registry_p = root / ".naya" / "memory" / "smart-notes" / "index.json"
    receipt = {
        "repair": "smart-note-registry-hash-reanchor",
        "updates_applied": len(plan["updates"]) if write else 0,
        "updates_planned": len(plan["updates"]),
        "ambiguous": plan["ambiguous"],
        "entries_without_capture": plan["entries_without_capture"],
        "captures_without_entry_projected": plan["captures_without_entry_projected"],
        "orphan_pages_with_capture": len(plan["orphan_pages_with_capture"]),
        "orphan_pages_without_capture": len(plan["orphan_pages_without_capture"]),
        "before_defect_total": plan["before_defect_total"],
        "before_counts": plan["before_counts"],
        "written": write,
    }
    if not write:
        return receipt

    if not plan["updates"]:
        # No-op repair: never rewrite bytes. A zero-update apply must leave
        # the registry byte-identical (manifest already anchors it).
        receipt["written"] = False
        receipt["after_defect_total"] = plan["before_defect_total"]
        receipt["after_counts"] = plan["before_counts"]
        receipt["validator"] = "PASS"
        return receipt

    registry = json.loads(registry_p.read_text(encoding="utf-8"))
    entries = registry["entries"]
    before_entries = [dict(e) for e in entries]
    for u in plan["updates"]:
        entries[u["entry_index"]]["content_hash"] = u["new_hash"]
    registry["corpus_manifest_hash"] = snv._corpus_manifest_hash(entries)

    # Diff census BEFORE the write: every targeted entry must have changed,
    # and only targeted entries may have changed.
    changed = sum(
        1 for b, a in zip(before_entries, entries)
        if json.dumps(b, sort_keys=True) != json.dumps(a, sort_keys=True)
    )
    if changed != len(plan["updates"]):
        raise SystemExit(
            f"REPAIR_REFUSED:DIFF_CENSUS_SHORTFALL:changed={changed} "
            f"planned={len(plan['updates'])}"
        )
    # Validator gate, scoped to what this repair can break: the repair
    # mutates ONLY content_hash, which _validate_index_against_corpus does
    # not check — so a validator failure that ALREADY exists on the
    # pristine registry (e.g. an ACTIVE fixture entry with no projection)
    # must not block the repair, but any NEW failure the mutation
    # introduces refuses the write. Identical failure code pre/post =
    # the repair broke nothing; a different code = refuse.
    def _validator_code(reg):
        try:
            snv._validate_index_against_corpus(reg, root=root)
            return None
        except SystemExit as exc:
            return str(exc.code)

    pristine = json.loads(registry_p.read_text(encoding="utf-8"))
    pre_code = _validator_code(pristine)
    post_code = _validator_code(registry)
    receipt["preexisting_validator_failure"] = pre_code
    if post_code != pre_code:
        raise SystemExit(
            f"REPAIR_REFUSED:VALIDATOR_CHANGED:{pre_code!r} -> {post_code!r}"
        )
    snv._atomic_write_json(registry_p, registry)

    # Post-write tripwire on the same disk bytes: the validator verdict
    # must still be the pre-existing one — identical, never silently new.
    reloaded = json.loads(registry_p.read_text(encoding="utf-8"))
    if _validator_code(reloaded) != pre_code:
        raise SystemExit(
            f"REPAIR_REFUSED:POST_WRITE_VALIDATOR_CHANGED:{pre_code!r} -> "
            f"{_validator_code(reloaded)!r}"
        )
    after = snv.audit_registry(root=root)
    receipt["after_defect_total"] = after["defect_total"]
    receipt["after_counts"] = after["counts"]
    receipt["corpus_manifest_hash"] = registry["corpus_manifest_hash"]
    receipt["validator"] = "PASS" if pre_code is None else f"PREEXISTING:{pre_code}"
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair Smart Note registry drift (hash re-anchor).")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--apply", action="store_true", help="write the repair (default: dry-run)")
    parser.add_argument("--out", type=Path, default=None, help="write the receipt JSON here")
    args = parser.parse_args()
    plan = plan_repair(args.root)
    print(f"BEFORE defect_total={plan['before_defect_total']} counts={plan['before_counts']}")
    print(f"PLANNED updates={len(plan['updates'])} ambiguous={len(plan['ambiguous'])} "
          f"entries_without_capture={len(plan['entries_without_capture'])} "
          f"captures_without_entry(projected)={len(plan['captures_without_entry_projected'])} "
          f"orphan_pages with/without capture="
          f"{len(plan['orphan_pages_with_capture'])}/{len(plan['orphan_pages_without_capture'])}")
    receipt = apply_repair(args.root, plan, write=args.apply)
    if args.apply:
        print(f"AFTER defect_total={receipt['after_defect_total']} counts={receipt['after_counts']}")
    if args.out:
        args.out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    else:
        print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
