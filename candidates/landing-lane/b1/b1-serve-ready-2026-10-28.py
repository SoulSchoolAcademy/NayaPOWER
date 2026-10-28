#!/usr/bin/env python3
"""B1 SERVE-READY worker (TEAM BUILD, 2026-10-28) — workspace only, NOT live.

What it is: the serve logic for the PI face's {counts, items} shape, built
from the proven core (workspace/system/b1-live-rows-core-2026-10-27.py,
run 5 ALL_PASS) and extended into a servable unit:

  serve() -> (200, envelope)  on a successful live read
  serve() -> (503, unavailable) on ANY live-read failure — never a snapshot

RULES (locked, same as the core):
  - Query LIVE at serve time (read-only work_items, project NayaPOWER).
    No cache, no file fallback, no snapshot. The .sample.json the core
    wrote is NEVER read as a fallback — a failed read is a 503, full stop.
  - Filter: project_id = a554e536-66a6-4808-8c36-988f13d9f394, in SQL.
  - Dedup: one row per item_key, most recently updated wins
    (updated_at DESC, nulls last, ties -> first seen). NOTE: updated_at is
    known-uninformative for some writes (they do not move it); the rule is
    kept for continuity with the proven core, and duplicates in this
    project are currently ~none, so the rule rarely decides anything.
  - Map: owner_seat -> owner (null stays null; the face shows "Ownerless").
  - Area: null on EVERY row, honestly (area schema not applied; no
    area_key column; no areas derived, invented, or CASE-guessed).
  - Face fields on every item: item_key, title, state, owner, priority,
    evidence_url, next_action, blocker, updated_at, area (+ maker_seat,
    prover_seat carried through; the face ignores extras).

FAILURE MODE (the point of this file): serve() catches every fetch
exception and returns (503, {"error": "live_rows_unavailable", ...})
with NO items and NO counts. A caller that renders counts/items from a
503 body is misusing it; the body carries no such keys by construction.

This file is importable (shape_items / build_response / unavailable /
serve) and runnable (CLI prints status + counts, exit 0 on 200, 1 on 503).
It performs NO production writes, NO deploy, NO landing. The live
endpoint (/pi/api/items on the merged worker) still does not exist —
Nitro wires this logic into the merged worker build behind the landing
gate; until then this is workspace-proven only, never presented as live.
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

PROJECT = "a554e536-66a6-4808-8c36-988f13d9f394"
RETRY = ["python3", "workspace/system/retry-sb.py"]

FACE_FIELDS = ("item_key", "title", "state", "owner", "priority",
               "evidence_url", "next_action", "blocker", "updated_at", "area")

COLUMNS = ("item_key, title, state, owner_seat, next_action, blocker, "
           "priority, evidence_url, maker_seat, prover_seat, updated_at")


def shape_items(rows):
    """Pure shaping: dedup + map + area-null. Input rows are raw record
    rows (dicts with record column names). Rows must already be ordered
    updated_at DESC NULLS LAST for the dedup rule to pick most-recent."""
    seen = {}
    order = []
    for row in rows:
        k = row.get("item_key")
        if k not in seen:
            seen[k] = row
            order.append(k)
    items = []
    for k in order:
        j = seen[k]
        items.append({
            "item_key": j.get("item_key"),
            "title": j.get("title"),
            "state": j.get("state"),
            "owner": j.get("owner_seat"),
            "priority": j.get("priority"),
            "evidence_url": j.get("evidence_url"),
            "next_action": j.get("next_action"),
            "blocker": j.get("blocker"),
            "updated_at": j.get("updated_at"),
            "area": None,
            "maker_seat": j.get("maker_seat"),
            "prover_seat": j.get("prover_seat"),
        })
    return items


def build_counts(items, rows_read):
    unique = len(items)
    done_proven = sum(1 for it in items if it.get("state") == "done_proven")
    return {"rows_read": rows_read, "unique": unique, "done_proven": done_proven}


def build_response(rows, mapping=None):
    """Full 200 envelope from raw live rows. Gains a "per_app" key
    (App Brief standard); counts/items are unchanged."""
    items = shape_items(rows)
    return {
        "counts": build_counts(items, len(rows)),
        "items": items,
        "per_app": compute_per_app(items, mapping),
        "project": "NayaPOWER",
        "project_id": PROJECT,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "area_note": ("area is null on every row (area schema not applied; "
                      "face shows 'unplaced' honestly; no areas derived or invented)"),
        "dedup_rule": "one row per item_key, most recently updated wins",
        "source": "live work_items (read-only), NOT a snapshot, NOT live-served yet",
    }


def unavailable_response(reason):
    """503 body. Deliberately carries NO items and NO counts."""
    return {
        "error": "live_rows_unavailable",
        "status": 503,
        "message": "Live rows unavailable — the face must show unavailable, never a stale snapshot.",
        "reason": str(reason)[:300],
        "project_id": PROJECT,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# ---------------------------------------------------------------- per-app
# Per-app done/total (App Brief standard, Resolve filing 6471995975):
# "% done computed from THIS app's own proven-done jobs, big, with the
# count beside it — never typed, never an estimate, never its area's
# number." The record carries NO app field (proven: work_items has no
# area_key/app column; parent_item_id covers only 60 of 394 rows and
# its 5 parents are work-packages, not apps). So per-app counts come
# from a mapping {item_key -> app} supplied at serve time — NEVER from
# a prefix guess or title inference invented in this code. The mapping
# is FILL-pipeline data (Resolve's packs through Nitro / STRUCTURE L1
# map); until a canonical mapping file lands, every row is honestly
# "unmapped" and the reconciliation invariant still holds.
#
# Invariant (asserted by tests): sum(per_app totals) + unmapped total
# == project unique; sum(per_app done) + unmapped done == done_proven.

def load_mapping(path):
    """Load a {item_key: app} JSON mapping. Missing file -> {} (unmapped
    mode, honest). Malformed JSON -> raises (fail loudly, never silently
    unmapped on a corrupt file)."""
    import os
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"mapping file {path} is not a JSON object")
    return {str(k): str(v) for k, v in data.items()}


def compute_per_app(items, mapping=None):
    """Group deduped items by app via mapping. Mapping keys absent from
    items create NO phantom apps (only items present count). Returns
    per-app done/total, the unmapped bucket, and mapping metadata."""
    mapping = mapping or {}
    per_app = {}
    unmapped_done = 0
    unmapped_total = 0
    mapped_keys = 0
    for it in items:
        app = mapping.get(it.get("item_key"))
        if app:
            mapped_keys += 1
            slot = per_app.setdefault(app, {"done": 0, "total": 0})
            slot["total"] += 1
            if it.get("state") == "done_proven":
                slot["done"] += 1
        else:
            unmapped_total += 1
            if it.get("state") == "done_proven":
                unmapped_done += 1
    return {
        "per_app": per_app,
        "unmapped": {"done": unmapped_done, "total": unmapped_total},
        "mapping": {
            "mapped_keys": mapped_keys,
            "unmapped_keys": unmapped_total,
            "note": ("apps come from the supplied mapping only; no app is "
                     "inferred from key prefixes or titles; unmapped rows "
                     "are counted honestly, never hidden"),
        },
    }


def _read_page(limit, offset):
    """Returns (page, effective_limit). On a no-JSON result the page
    size cascades down (50 -> 25 -> 10) deliberately, and the caller
    MUST adopt the effective limit — otherwise a cascade-shrunk page
    looks like end-of-table and the read stops early (defect found by
    the live test 2026-10-28: first live run served only 25 rows)."""
    sql = ("SELECT " + COLUMNS + " FROM work_items "
           f"WHERE project_id = '{PROJECT}' "
           "ORDER BY updated_at DESC NULLS LAST, item_key "
           f"LIMIT {limit} OFFSET {offset};")
    r = subprocess.run(RETRY + [sql], capture_output=True, text=True, timeout=180)
    m = re.search(r"\[.*\]", r.stdout, re.DOTALL)
    if not m:
        if limit > 10:
            nxt = 25 if limit > 25 else 10
            return _read_page(nxt, offset)
        r2 = subprocess.run(RETRY + [sql], capture_output=True, text=True, timeout=180)
        m2 = re.search(r"\[.*\]", r2.stdout, re.DOTALL)
        if m2:
            return json.loads(m2.group(0)), 10
        raise RuntimeError(
            f"no JSON block in page offset={offset} after second attempt: "
            f"stdout={r2.stdout[:300]!r} stderr={r2.stderr[-300:]!r}")
    return json.loads(m.group(0)), limit


def fetch_live_rows():
    """Read-only live fetch, paged. Raises on failure (caller maps to 503)."""
    probe_sql = ("SELECT item_key, title, state, owner_seat, updated_at FROM work_items "
                 f"WHERE project_id = '{PROJECT}' LIMIT 1;")
    rp = subprocess.run(RETRY + [probe_sql], capture_output=True, text=True, timeout=180)
    if not re.search(r"\[.*\]", rp.stdout, re.DOTALL):
        raise RuntimeError(f"probe failed: stdout={rp.stdout[:300]!r} stderr={rp.stderr[-300:]!r}")
    rows = []
    offset = 0
    limit = 50
    while True:
        page, eff = _read_page(limit, offset)
        if not page:
            break
        rows.extend(page)
        offset += len(page)
        limit = eff  # adopt the page size that actually works
        if len(page) < eff:
            break
        time.sleep(1)
    return rows


def serve(fetch=fetch_live_rows, mapping=None):
    """Serve one response. Returns (status, body). Never raises for a
    fetch failure — that is the 503 path, by design."""
    try:
        rows = fetch()
    except Exception as exc:  # noqa: BLE001 — any fetch failure is a 503
        return 503, unavailable_response(exc)
    return 200, build_response(rows, mapping=mapping)


# ---------------------------------------------------------------- front/back split
# Front/back split (scorecard gap 2, 2026-10-28) — Power's record-structure lane.
#
# FIELD DISCOVERY (live reads, 2026-10-28, NOT a guess): NO column in live
# work_items carries the front/back tag. information_schema shows 22
# columns (no tag column, no area_key), and sample acceptance_criteria
# objects are {id, done, text} with no surface field. The tag delivery
# vehicle is Resolve's mail mapping (thread defd9b23, message 1383eee3,
# 2026-10-28 ~17:20Z): "THE MAPPING (item_key: tag)", 392 entries,
# counts front 165 / back 119 / both 92 / process 16 / unspecified 0 —
# extracted verbatim to workspace/system/g1-front-back-tags-2026-10-28.json
# and verified against the mail's own COUNTS line (exact match, 0
# unparsed lines, 6/6 spot checks). Resolve's machine file (goal
# hidden_files/g1-front-back/g1-front-back-tags.machine.json) lives on
# HER box and was NOT read from here; the mail mapping is the
# shared-record delivery any seat can re-read. The 2 live rows outside
# the mapping are the 2 newest rows, which carry no acceptance_criteria
# (Resolve's caveat 1, confirmed by live read).
#
# The function below therefore takes the tag mapping as an INPUT (same
# pattern as compute_per_app's app mapping) and joins it to LIVE rows at
# call time. It never reads tags from a DB column that does not exist,
# and never invents tags for unmapped rows: unmapped rows are counted
# as untagged, separately, always.
#
# AREA HONESTY: work_items has no area_key, so per-area grouping takes
# an area mapping {item_key: area} as input; with none supplied (or a
# key absent from it) the row lands in "unplaced" — never a guessed
# area. When the FILL pipeline lands a canonical area mapping, the same
# function distributes the split across areas with no code change.
#
# DONE, DEFINED PRECISELY (from criteria done flags, NOT from state):
#   criteria_done(row) = acceptance_criteria is a non-empty list AND
#   every element is an object with done === True.
# Rows with no criteria, empty criteria, non-list criteria, or any
# element missing done=True are NOT done. State done_proven is reported
# separately per bucket (done_proven) so the 24 baseline reconciles
# without conflating the two definitions: the 9 adjudication rows are
# done_proven by state yet NOT criteria-done, and they stay visible as
# exactly that difference.
#
# BUCKETS (disjoint; no double count, no dropped rows):
#   front / back / both / process / untagged, per area.
#   "both" = one row belonging to BOTH lists (face Front list AND Back
#   list); "process" = governance/verification/media work that is
#   honestly neither surface nor machinery (Resolve's definition).
#   Tag values outside {front, back, both, process} — including
#   "unspecified" and any unknown string — land in untagged.
# DERIVED LIST VIEWS (what the face displays):
#   front_list = front + both; back_list = back + both (counts AND
#   item_key lists). The buckets reconcile; the list views overlap by
#   design (both rows appear in both lists) and are labelled as views,
#   never summed back into the total.
# INVARIANT (asserted by tests): for every area, front+back+both+
# process+untagged totals == area total; sum over areas == unique;
# sum of done_proven over all buckets == project done_proven.
#
# Serve-time wiring note: serve()/build_response() are NOT changed by
# this section (their fetch does not select acceptance_criteria, and
# their envelope shape is frozen for the existing tests). The CLI
# --tag-mapping path below demonstrates the serve-time computation end
# to end (criteria-inclusive live fetch + compute + print); wiring the
# split into the merged worker's /pi/api/items response is Nitro's
# landing-lane step, reusing compute_front_back_split + a
# criteria-inclusive fetch, behind the landing gate.

TAG_VALUES = ("front", "back", "both", "process")


def load_tag_mapping(path):
    """Load a {item_key: tag} JSON mapping. Same contract as
    load_mapping: missing file -> {} (all rows untagged, honest);
    malformed JSON or non-object -> raises (fail loudly). Values are
    NOT validated here: unknown values fall into untagged at compute
    time, so a corrupt tag can never silently become front or back."""
    import os
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"tag mapping file {path} is not a JSON object")
    return {str(k): str(v) for k, v in data.items()}


def is_criteria_done(row):
    """True only when acceptance_criteria is a non-empty list and every
    element is an object with done === True. Anything else is not done."""
    crit = row.get("acceptance_criteria")
    if not isinstance(crit, list) or not crit:
        return False
    return all(isinstance(c, dict) and c.get("done") is True for c in crit)


def _empty_bucket():
    return {"done": 0, "total": 0, "done_proven": 0, "items": []}


def compute_front_back_split(rows, tag_mapping=None, area_mapping=None):
    """Split live rows into front/back/both/process/untagged buckets per
    area. Rows must already be ordered updated_at DESC NULLS LAST (same
    precondition as shape_items): the first row seen per item_key wins.
    Pure function; no I/O. Input rows are RAW record rows (item_key,
    state, acceptance_criteria, updated_at).
    Returns {"per_area": {...}, "totals": {...}, "reconciliation": {...}}."""
    tag_mapping = tag_mapping or {}
    area_mapping = area_mapping or {}
    seen = {}
    order = []
    for row in rows:
        k = row.get("item_key")
        if k not in seen:
            seen[k] = row
            order.append(k)
    per_area = {}
    for k in order:
        row = seen[k]
        area = area_mapping.get(k) or "unplaced"
        tag = tag_mapping.get(k)
        bucket = tag if tag in TAG_VALUES else "untagged"
        slot = per_area.setdefault(area, {
            "front": _empty_bucket(), "back": _empty_bucket(),
            "both": _empty_bucket(), "process": _empty_bucket(),
            "untagged": _empty_bucket(), "total": 0, "done": 0,
            "done_proven": 0,
        })
        b = slot[bucket]
        b["total"] += 1
        b["items"].append(k)
        if is_criteria_done(row):
            b["done"] += 1
            slot["done"] += 1
        if row.get("state") == "done_proven":
            b["done_proven"] += 1
            slot["done_proven"] += 1
        slot["total"] += 1
    for area, slot in per_area.items():
        for view, parts in (("front_list", ("front", "both")),
                            ("back_list", ("back", "both"))):
            slot[view] = {
                "done": sum(slot[p]["done"] for p in parts),
                "total": sum(slot[p]["total"] for p in parts),
                "done_proven": sum(slot[p]["done_proven"] for p in parts),
                "items": slot[parts[0]]["items"] + slot[parts[1]]["items"],
            }
    totals = {"front": _empty_bucket(), "back": _empty_bucket(),
              "both": _empty_bucket(), "process": _empty_bucket(),
              "untagged": _empty_bucket(), "total": 0, "done": 0,
              "done_proven": 0}
    for slot in per_area.values():
        for name in ("front", "back", "both", "process", "untagged"):
            totals[name]["total"] += slot[name]["total"]
            totals[name]["done"] += slot[name]["done"]
            totals[name]["done_proven"] += slot[name]["done_proven"]
            totals[name]["items"].extend(slot[name]["items"])
        totals["total"] += slot["total"]
        totals["done"] += slot["done"]
        totals["done_proven"] += slot["done_proven"]
    totals["front_list"] = {
        "done": totals["front"]["done"] + totals["both"]["done"],
        "total": totals["front"]["total"] + totals["both"]["total"],
        "done_proven": totals["front"]["done_proven"] + totals["both"]["done_proven"],
        "items": totals["front"]["items"] + totals["both"]["items"],
    }
    totals["back_list"] = {
        "done": totals["back"]["done"] + totals["both"]["done"],
        "total": totals["back"]["total"] + totals["both"]["total"],
        "done_proven": totals["back"]["done_proven"] + totals["both"]["done_proven"],
        "items": totals["back"]["items"] + totals["both"]["items"],
    }
    buckets_sum = sum(totals[n]["total"]
                      for n in ("front", "back", "both", "process", "untagged"))
    dp_sum = sum(totals[n]["done_proven"]
                 for n in ("front", "back", "both", "process", "untagged"))
    recon = {
        "unique": len(order),
        "buckets_sum_equals_unique": buckets_sum == len(order),
        "done_proven_sum_equals_unique_done_proven": dp_sum == totals["done_proven"],
        "per_area_totals_sum": sum(s["total"] for s in per_area.values()),
        "per_area_sums_match": all(
            s["front"]["total"] + s["back"]["total"] + s["both"]["total"]
            + s["process"]["total"] + s["untagged"]["total"] == s["total"]
            for s in per_area.values()),
    }
    return {"per_area": per_area, "totals": totals, "reconciliation": recon}


CRITERIA_COLUMNS = "item_key, state, acceptance_criteria, updated_at"


def _read_criteria_page(limit, offset):
    """Criteria-inclusive page reader for the --tag-mapping CLI path
    only (serve() does not use it). Same cascade discipline as
    _read_page: 50 -> 25 -> 10 on a no-JSON result, caller MUST adopt
    the effective limit."""
    sql = ("SELECT " + CRITERIA_COLUMNS + " FROM work_items "
           f"WHERE project_id = '{PROJECT}' "
           "ORDER BY updated_at DESC NULLS LAST, item_key "
           f"LIMIT {limit} OFFSET {offset};")
    r = subprocess.run(RETRY + [sql], capture_output=True, text=True, timeout=180)
    m = re.search(r"\[.*\]", r.stdout, re.DOTALL)
    if not m:
        if limit > 10:
            nxt = 25 if limit > 25 else 10
            return _read_criteria_page(nxt, offset)
        # Smallest page: up to 3 deliberate fresh-run attempts (the test's
        # proven discipline) with pacing — a persistently flaky window
        # outlasts 2 calls (observed 2026-10-28: offset 180 failed twice,
        # then the window cleared). Never a snapshot, never a skip:
        # exhaustion still raises, loudly.
        last = r
        for _ in range(2):
            time.sleep(2)
            r2 = subprocess.run(RETRY + [sql], capture_output=True, text=True, timeout=180)
            m2 = re.search(r"\[.*\]", r2.stdout, re.DOTALL)
            if m2:
                return json.loads(m2.group(0)), 10
            last = r2
        raise RuntimeError(
            f"no JSON block in criteria page offset={offset} after 3 attempts: "
            f"stdout={last.stdout[:300]!r} stderr={last.stderr[-300:]!r}")
    return json.loads(m.group(0)), limit


def fetch_live_rows_with_criteria():
    """Read-only live fetch with acceptance_criteria, paged. Raises on
    failure (CLI maps it to FRONT_BACK_ERROR, never a snapshot)."""
    rows = []
    offset = 0
    limit = 50
    while True:
        page, eff = _read_criteria_page(limit, offset)
        if not page:
            break
        rows.extend(page)
        offset += len(page)
        limit = eff  # adopt the page size that actually works
        if len(page) < eff:
            break
        time.sleep(1)
    return rows


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mapping", default=None,
                    help="optional {item_key: app} JSON mapping file")
    ap.add_argument("--tag-mapping", default=None,
                    help="optional {item_key: tag} JSON mapping file for the front/back split print")
    ap.add_argument("--area-mapping", default=None,
                    help="optional {item_key: area} JSON mapping file for the front/back split print")
    args = ap.parse_args()
    mapping = None
    if args.mapping:
        try:
            mapping = load_mapping(args.mapping)
            print(f"MAPPING: {len(mapping)} keys from {args.mapping}")
        except Exception as exc:  # noqa: BLE001 — enrichment never breaks serve
            print(f"MAPPING WARNING: {exc}; proceeding unmapped.")
            mapping = None
    if args.tag_mapping:
        try:
            tags = load_tag_mapping(args.tag_mapping)
            areas = load_mapping(args.area_mapping) if args.area_mapping else {}
            crows = fetch_live_rows_with_criteria()
            split = compute_front_back_split(crows, tags, areas)
            print(f"TAG_MAPPING: {len(tags)} keys from {args.tag_mapping}")
            print("FRONT_BACK:", json.dumps(split))
        except Exception as exc:  # noqa: BLE001 — split print failure is fatal to this CLI path only
            print(f"FRONT_BACK_ERROR: {exc}")
            return 1
    status, body = serve(mapping=mapping)
    if status == 200:
        print("STATUS: 200")
        print("COUNTS:", json.dumps(body["counts"]))
        print("PER_APP:", json.dumps(body["per_app"]))
        print("FIRST_ITEM:", json.dumps(body["items"][0])[:400] if body["items"] else None)
        print("AREA_NULL_ON_ALL:", all(it.get("area") is None for it in body["items"]))
        print("FACE_FIELDS_ON_ALL:", all(all(k in it for k in FACE_FIELDS) for it in body["items"]))
        return 0
    print("STATUS: 503")
    print("BODY:", json.dumps(body))
    return 1


if __name__ == "__main__":
    sys.exit(main())
