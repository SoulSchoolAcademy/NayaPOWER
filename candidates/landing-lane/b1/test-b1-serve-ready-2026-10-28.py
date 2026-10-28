#!/usr/bin/env python3
"""Tests for b1-serve-ready-2026-10-28.py (TEAM BUILD, 2026-10-28).

Run: python3 workspace/system/test-b1-serve-ready-2026-10-28.py
Exit 0 only if EVERY check passes. No hardcoded counts: the live test
re-reads the record fresh at test time and compares serve() against that
independent read. A mismatch fails honestly (it never falls back to a
stale number).

Checks:
  F1 dedup: duplicate item_keys collapse to one row, most-recent wins.
  F2 dedup tie: equal updated_at -> first seen wins.
  F3 owner mapping: owner_seat -> owner, null stays null.
  F4 area null on every shaped item; face fields present on every item.
  F5 counts math: rows_read/unique/done_proven from shaped items.
  F6 failure: failing fetcher -> 503, error == live_rows_unavailable,
      NO items key, NO counts key (never a snapshot, never partial rows).
  P1 per-app grouping; P2 unmapped bucket; P3 phantom mapping keys
      ignored; P4 reconciliation invariant; P5 loader drop-in/missing/
      malformed; P6 serve() carries per_app through the envelope.
  L1 live: serve() counts == independent fresh-read counts (raw rows,
      unique keys, done_proven), key sets equal.
  L2 live: every served item's (title, state, owner) matches the
      independent read's deduped row for that key.
  L3 live: 3 individually re-read keys match the served rows exactly.
  L4 live: per-app unmapped mode on live data (no canonical mapping
      exists yet) reconciles exactly to the served counts.
"""
import json
import re
import subprocess
import sys
import time

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "b1_serve_ready", "workspace/system/b1-serve-ready-2026-10-28.py")
B1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B1)

PROJECT = B1.PROJECT
RETRY = ["python3", "workspace/system/retry-sb.py"]
FAILURES = []


def check(name, cond, detail=""):
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")
    if not cond:
        FAILURES.append(name)


def sql_json(sql, attempts=0):
    """Independent-read helper with the proven transport discipline:
    a no-JSON result (chunked-read failure, or empty stdout) gets
    deliberate fresh-run retries (same page), never a blind reword and
    never a silent skip. After 3 attempts it fails honestly."""
    r = subprocess.run(RETRY + [sql], capture_output=True, text=True, timeout=180)
    m = re.search(r"\[.*\]", r.stdout, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    if attempts < 2:
        time.sleep(2)
        return sql_json(sql, attempts + 1)
    raise RuntimeError(f"no JSON block for sql={sql[:120]!r} after 3 attempts: "
                       f"stdout={r.stdout[:300]!r} stderr={r.stderr[-300:]!r}")


def fixture_tests():
    rows = [
        {"item_key": "k1", "title": "Old", "state": "queued", "owner_seat": None,
         "priority": 1, "evidence_url": None, "next_action": "a", "blocker": None,
         "maker_seat": "m", "prover_seat": None, "updated_at": "2026-10-20T00:00:00+00:00"},
        {"item_key": "k1", "title": "New", "state": "in_progress", "owner_seat": "naya-power",
         "priority": 2, "evidence_url": "http://x", "next_action": "b", "blocker": None,
         "maker_seat": "m", "prover_seat": "p", "updated_at": "2026-10-27T00:00:00+00:00"},
        {"item_key": "k2", "title": "TieFirst", "state": "queued", "owner_seat": "naya-resolve",
         "priority": 1, "evidence_url": None, "next_action": "c", "blocker": None,
         "maker_seat": "m", "prover_seat": None, "updated_at": "2026-10-25T00:00:00+00:00"},
        {"item_key": "k2", "title": "TieSecond", "state": "queued", "owner_seat": "nitro",
         "priority": 1, "evidence_url": None, "next_action": "d", "blocker": None,
         "maker_seat": "m", "prover_seat": None, "updated_at": "2026-10-25T00:00:00+00:00"},
        {"item_key": "k3", "title": "Done", "state": "done_proven", "owner_seat": None,
         "priority": 1, "evidence_url": "http://y", "next_action": None, "blocker": None,
         "maker_seat": "m", "prover_seat": "p", "updated_at": "2026-10-26T00:00:00+00:00"},
    ]
    # Rows are pre-ordered updated DESC (as fetch_live_rows orders them).
    rows_sorted = sorted(rows, key=lambda r: (r["updated_at"] is None, r["updated_at"] or ""), reverse=True)
    items = B1.shape_items(rows_sorted)
    by_key = {it["item_key"]: it for it in items}
    check("F1 dedup-most-recent-wins", by_key["k1"]["title"] == "New" and len(items) == 3,
          f"items={len(items)} k1={by_key['k1']['title']}")
    check("F2 dedup-tie-first-seen", by_key["k2"]["title"] == "TieFirst",
          f"k2={by_key['k2']['title']}")
    check("F3 owner-mapping", by_key["k1"]["owner"] == "naya-power" and by_key["k3"]["owner"] is None,
          f"k1.owner={by_key['k1']['owner']} k3.owner={by_key['k3']['owner']}")
    check("F4 area-null-all", all(it["area"] is None for it in items))
    check("F4b face-fields-all", all(all(k in it for k in B1.FACE_FIELDS) for it in items))
    counts = B1.build_counts(items, 5)
    check("F5 counts-math", counts == {"rows_read": 5, "unique": 3, "done_proven": 1},
          f"counts={counts}")

    def boom():
        raise RuntimeError("simulated transport failure")
    status, body = B1.serve(fetch=boom)
    check("F6 failure-503", status == 503 and body.get("error") == "live_rows_unavailable"
          and body.get("status") == 503, f"status={status} error={body.get('error')}")
    check("F6b failure-no-items-no-counts", "items" not in body and "counts" not in body,
          f"keys={sorted(body.keys())}")


def independent_fresh_read():
    """Independent read: different page size (40), own dedup loop."""
    rows = []
    offset = 0
    while True:
        sql = ("SELECT item_key, title, state, owner_seat, updated_at FROM work_items "
               f"WHERE project_id = '{PROJECT}' ORDER BY updated_at DESC NULLS LAST, item_key "
               f"LIMIT 40 OFFSET {offset};")
        page = sql_json(sql)
        if not page:
            break
        rows.extend(page)
        offset += len(page)
        if len(page) < 40:
            break
    seen = {}
    for row in rows:
        if row.get("item_key") not in seen:
            seen[row["item_key"]] = row
    return rows, seen


def live_tests():
    status, body = B1.serve()
    check("L0 serve-200", status == 200, f"status={status}")
    if status != 200:
        print("LIVE BODY:", json.dumps(body)[:500])
        return
    served_counts = body["counts"]
    raw, deduped = independent_fresh_read()
    fresh_total = len(raw)
    fresh_unique = len(deduped)
    fresh_done = sum(1 for r in deduped.values() if r.get("state") == "done_proven")
    print(f"FRESH READ: raw={fresh_total} unique={fresh_unique} done_proven={fresh_done}")
    print(f"SERVED:     {served_counts}")
    check("L1 live-counts-match", served_counts["rows_read"] == fresh_total
          and served_counts["unique"] == fresh_unique
          and served_counts["done_proven"] == fresh_done,
          f"served={served_counts} fresh=({fresh_total},{fresh_unique},{fresh_done})")
    served_keys = {it["item_key"] for it in body["items"]}
    check("L1b live-key-sets-equal", served_keys == set(deduped.keys()),
          f"served_keys={len(served_keys)} fresh_keys={len(deduped)}")
    mismatches = []
    for it in body["items"]:
        live = deduped.get(it["item_key"])
        if not live or live.get("title") != it["title"] or live.get("state") != it["state"] \
                or live.get("owner_seat") != it["owner"]:
            mismatches.append(it["item_key"])
    check("L2 live-rows-match", not mismatches, f"mismatches={mismatches[:5]}")
    # L3: three individually re-read keys.
    served_by_key = {it["item_key"]: it for it in body["items"]}
    sample_keys = list(served_by_key.keys())[:3]
    ok = True
    for k in sample_keys:
        one = sql_json("SELECT item_key, title, state, owner_seat, updated_at FROM work_items "
                       f"WHERE item_key = '{k}' AND project_id = '{PROJECT}' LIMIT 1;")
        live = one[0] if one else {}
        s = served_by_key[k]
        if not (live.get("title") == s["title"] and live.get("state") == s["state"]
                and live.get("owner_seat") == s["owner"]):
            ok = False
    check("L3 live-spot-check-3-keys", ok, f"keys={sample_keys}")
    # Per-app on live data, unmapped mode (no canonical mapping exists yet):
    # per_app empty, unmapped reconciles exactly to the served counts.
    pa = body.get("per_app", {})
    check("L4 live-per-app-unmapped-mode", pa.get("per_app") == {}
          and pa.get("unmapped") == {"done": served_counts["done_proven"],
                                     "total": served_counts["unique"]},
          f"per_app={pa}")
    tot = sum(v["total"] for v in pa.get("per_app", {}).values()) + pa["unmapped"]["total"]
    dn = sum(v["done"] for v in pa.get("per_app", {}).values()) + pa["unmapped"]["done"]
    check("L4b live-per-app-reconciliation", tot == served_counts["unique"]
          and dn == served_counts["done_proven"], f"tot={tot} done={dn}")


def per_app_fixture_tests():
    shaped = [
        {"item_key": "a1", "title": "A1", "state": "done_proven", "owner": None,
         "priority": 1, "evidence_url": None, "next_action": None, "blocker": None,
         "updated_at": "2026-10-26T00:00:00+00:00", "area": None},
        {"item_key": "a2", "title": "A2", "state": "queued", "owner": None,
         "priority": 1, "evidence_url": None, "next_action": None, "blocker": None,
         "updated_at": "2026-10-26T00:00:00+00:00", "area": None},
        {"item_key": "b1", "title": "B1", "state": "in_progress", "owner": None,
         "priority": 1, "evidence_url": None, "next_action": None, "blocker": None,
         "updated_at": "2026-10-26T00:00:00+00:00", "area": None},
        {"item_key": "u1", "title": "U1", "state": "done_proven", "owner": None,
         "priority": 1, "evidence_url": None, "next_action": None, "blocker": None,
         "updated_at": "2026-10-26T00:00:00+00:00", "area": None},
    ]
    mapping = {"a1": "App A", "a2": "App A", "b1": "App B", "ghost-key": "Ghost App"}
    pa = B1.compute_per_app(shaped, mapping)
    check("P1 per-app-grouping", pa["per_app"] == {"App A": {"done": 1, "total": 2},
                                                  "App B": {"done": 0, "total": 1}},
          f"per_app={pa['per_app']}")
    check("P2 unmapped-bucket", pa["unmapped"] == {"done": 1, "total": 1},
          f"unmapped={pa['unmapped']}")
    check("P3 phantom-ignored", "Ghost App" not in pa["per_app"], "ghost absent")
    tot = sum(v["total"] for v in pa["per_app"].values()) + pa["unmapped"]["total"]
    dn = sum(v["done"] for v in pa["per_app"].values()) + pa["unmapped"]["done"]
    check("P4 reconciliation-invariant", tot == len(shaped) and dn == 2,
          f"tot={tot} done={dn} items={len(shaped)}")
    # P5: loader drop-in via /tmp scratch (test-only, not workspace data).
    import os
    tmp = "/tmp/teambuild-mapping-dropin.json"
    with open(tmp, "w") as f:
        json.dump({"a1": "App A", "b1": "App B"}, f)
    loaded = B1.load_mapping(tmp)
    check("P5a loader-dropin", loaded == {"a1": "App A", "b1": "App B"}, f"loaded={loaded}")
    check("P5b loader-missing-empty", B1.load_mapping("/tmp/teambuild-no-such-file.json") == {})
    bad = "/tmp/teambuild-mapping-bad.json"
    with open(bad, "w") as f:
        f.write("{not json")
    try:
        B1.load_mapping(bad)
        check("P5c loader-malformed-raises", False, "no raise")
    except Exception:
        check("P5c loader-malformed-raises", True, "raised")
    os.remove(tmp)
    os.remove(bad)
    # P6: serve() carries per_app through the envelope.
    status, body = B1.serve(fetch=lambda: [
        {"item_key": "a1", "title": "A1", "state": "done_proven", "owner_seat": None,
         "priority": 1, "evidence_url": None, "next_action": None, "blocker": None,
         "maker_seat": "m", "prover_seat": "p", "updated_at": "2026-10-26T00:00:00+00:00"},
        {"item_key": "u1", "title": "U1", "state": "queued", "owner_seat": None,
         "priority": 1, "evidence_url": None, "next_action": None, "blocker": None,
         "maker_seat": "m", "prover_seat": None, "updated_at": "2026-10-26T00:00:00+00:00"},
    ], mapping={"a1": "App A"})
    check("P6 serve-carries-per-app", status == 200
          and body["per_app"]["per_app"] == {"App A": {"done": 1, "total": 1}}
          and body["per_app"]["unmapped"] == {"done": 0, "total": 1},
          f"per_app={body['per_app'] if status == 200 else body}")


def main():
    fixture_tests()
    per_app_fixture_tests()
    live_tests()
    print("FAILURES:", FAILURES if FAILURES else "none")
    print("ALL_PASS:", not FAILURES)
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
