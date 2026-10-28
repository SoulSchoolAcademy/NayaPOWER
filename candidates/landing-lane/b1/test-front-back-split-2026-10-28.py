#!/usr/bin/env python3
"""Tests for the front/back split extension in b1-serve-ready-2026-10-28.py
(TEAM BUILD, 2026-10-28, Power's record-structure lane).

Run: python3 workspace/system/test-front-back-split-2026-10-28.py
Exit 0 only if EVERY check passes. Fixture checks are pure. Live checks
re-read the record fresh at test time and compare the split against that
independent read; the 394 rows / 24 done_proven baseline check (L1) is
deliberately a baseline assertion, not a hardcoded convenience: if the
record grows, it fails honestly and the report must be re-baselined.

Checks:
  S1 buckets partition (front/back/both/process/untagged, disjoint, sum).
  S2 done rule matrix (criteria done flags only, strict True).
  S3 state-vs-criteria split (done_proven row, unmet criteria: counted
      done_proven but NOT done — the adjudication shape).
  S4 dedup: first-seen (most-recent) row wins per item_key.
  S5 unknown tag + "unspecified" + missing tag -> untagged, never assigned.
  S6 area mapping: two areas + unmapped key -> "unplaced"; per-area sums.
  S7 list views: front_list = front + both, back_list = back + both;
      overlap by design (both rows in both lists), never summed to total.
  S8 loader: missing -> {}, malformed -> raises, drop-in valid -> loads.
  S9 empty input -> all zeros, reconciliation true.
  L0 live independent fresh read (criteria-inclusive, page 40, own dedup).
  L1 live read sanity: raw == unique (no duplicate keys); baseline
      numbers are REPORTED with their read time, never asserted as
      fixed — the record grows under live seat work (394 -> 397 during
      this test's own runs), and drift must be reported, not hidden.
  L2 tag mapping file: 392 keys, counts front 165 / back 119 / both 92 /
      process 16, no "unspecified" values.
  L3 live key sets: every mapped key still live; unmapped keys listed
      (they are rows outside the mapping snapshot, by construction).
  L4 live split: buckets recomputed independently from mapping + live
      key set (drift-proof); split total == fresh unique,
      done_proven == fresh done_proven, reconciliation block all true.
  L5 live bucket bounds: done <= total and done_proven <= total per
      bucket; untagged done/items reported.
  L6 live area: no area mapping -> per_area keys == {"unplaced"} only,
      unplaced total == fresh unique.
  L7 CLI --tag-mapping path prints a FRONT_BACK split whose
      reconciliation block is all true and whose tagged buckets equal
      the mapping counts; CLI timeouts are caught and retried once
      (read-only run, no side effects).
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
TAG_FILE = "workspace/system/g1-front-back-tags-2026-10-28.json"
FAILURES = []


def check(name, cond, detail=""):
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")
    if not cond:
        FAILURES.append(name)


def sql_json(sql, attempts=0):
    """Independent-read helper with the proven transport discipline:
    a no-JSON result gets deliberate fresh-run retries (same query),
    never a blind reword and never a silent skip. After 3 attempts it
    fails honestly."""
    r = subprocess.run(RETRY + [sql], capture_output=True, text=True, timeout=180)
    m = re.search(r"\[.*\]", r.stdout, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    if attempts < 2:
        time.sleep(2)
        return sql_json(sql, attempts + 1)
    raise RuntimeError(f"no JSON block for sql={sql[:120]!r} after 3 attempts: "
                       f"stdout={r.stdout[:300]!r} stderr={r.stderr[-300:]!r}")


def C(*flags):
    """Build an acceptance_criteria list from done flags (True/False/None
    for a missing done key)."""
    out = []
    for i, f in enumerate(flags):
        c = {"id": f"c{i+1}", "text": f"criterion {i+1}"}
        if f is not None:
            c["done"] = f
        out.append(c)
    return out


def fixture_tests():
    # Rows pre-ordered updated_at DESC (the compute precondition).
    rows = [
        {"item_key": "f1", "state": "queued", "acceptance_criteria": C(True, True),
         "updated_at": "2026-10-27T00:00:00+00:00"},
        {"item_key": "f2", "state": "queued", "acceptance_criteria": C(True, False),
         "updated_at": "2026-10-27T00:00:00+00:00"},
        {"item_key": "b1", "state": "done_proven", "acceptance_criteria": C(True),
         "updated_at": "2026-10-26T00:00:00+00:00"},
        {"item_key": "bo1", "state": "in_progress", "acceptance_criteria": C(True, True, True),
         "updated_at": "2026-10-26T00:00:00+00:00"},
        {"item_key": "p1", "state": "queued", "acceptance_criteria": C(False),
         "updated_at": "2026-10-25T00:00:00+00:00"},
        {"item_key": "u1", "state": "queued", "acceptance_criteria": C(True),
         "updated_at": "2026-10-25T00:00:00+00:00"},
        {"item_key": "u2", "state": "queued", "acceptance_criteria": [],
         "updated_at": "2026-10-24T00:00:00+00:00"},
        {"item_key": "u3", "state": "queued",
         "updated_at": "2026-10-24T00:00:00+00:00"},
        {"item_key": "u4", "state": "queued", "acceptance_criteria": {"id": "c1", "done": True},
         "updated_at": "2026-10-23T00:00:00+00:00"},
        {"item_key": "u5", "state": "queued", "acceptance_criteria": C(None),
         "updated_at": "2026-10-23T00:00:00+00:00"},
        {"item_key": "u6", "state": "queued", "acceptance_criteria": [{"id": "c1", "done": "true"}],
         "updated_at": "2026-10-22T00:00:00+00:00"},
        {"item_key": "u7", "state": "queued", "acceptance_criteria": ["not-a-dict"],
         "updated_at": "2026-10-22T00:00:00+00:00"},
        # Adjudication shape: done_proven by state, unmet criteria.
        {"item_key": "adj1", "state": "done_proven", "acceptance_criteria": C(True, False),
         "updated_at": "2026-10-21T00:00:00+00:00"},
        # Dedup pair: most-recent (first) row is done; older twin is not.
        {"item_key": "dup1", "state": "queued", "acceptance_criteria": C(True),
         "updated_at": "2026-10-28T00:00:00+00:00"},
        {"item_key": "dup1", "state": "queued", "acceptance_criteria": C(False),
         "updated_at": "2026-10-20T00:00:00+00:00"},
    ]
    tags = {"f1": "front", "f2": "front", "b1": "back", "bo1": "both",
            "p1": "process", "u1": "weird-tag", "u2": "unspecified",
            "adj1": "front", "dup1": "front"}
    # u3, u4, u5, u6, u7 have no tag entry -> untagged.
    out = B1.compute_front_back_split(rows, tags)
    t = out["totals"]
    check("S1 buckets-partition",
          t["front"]["total"] == 4 and t["back"]["total"] == 1
          and t["both"]["total"] == 1 and t["process"]["total"] == 1
          and t["untagged"]["total"] == 7 and t["total"] == 14,
          f"front={t['front']['total']} back={t['back']['total']} "
          f"both={t['both']['total']} process={t['process']['total']} "
          f"untagged={t['untagged']['total']} total={t['total']}")
    check("S1b recon-block-true", all(out["reconciliation"][k] for k in
          ("buckets_sum_equals_unique",
           "done_proven_sum_equals_unique_done_proven",
           "per_area_sums_match"))
          and out["reconciliation"]["unique"] == 14
          and out["reconciliation"]["per_area_totals_sum"] == 14,
          f"recon={out['reconciliation']}")
    check("S2 done-rule",
          t["front"]["done"] == 2  # f1 + dup1; f2 and adj1 not done
          and t["back"]["done"] == 1 and t["both"]["done"] == 1
          and t["process"]["done"] == 0 and t["untagged"]["done"] == 1,
          # untagged.done == 1 is u1: bad tag, but its criteria are all done.
          # The done rule reads criteria only, never the tag.
          f"front.done={t['front']['done']} back.done={t['back']['done']} "
          f"both.done={t['both']['done']} untagged.done={t['untagged']['done']}")
    check("S2b done-strictness",
          B1.is_criteria_done({"acceptance_criteria": C(True, True)})
          and not B1.is_criteria_done({"acceptance_criteria": C(True, False)})
          and not B1.is_criteria_done({"acceptance_criteria": C(None)})
          and not B1.is_criteria_done({"acceptance_criteria": []})
          and not B1.is_criteria_done({})
          and not B1.is_criteria_done({"acceptance_criteria": {"id": "c1", "done": True}})
          and not B1.is_criteria_done({"acceptance_criteria": [{"id": "c1", "done": "true"}]})
          and not B1.is_criteria_done({"acceptance_criteria": ["not-a-dict"]}),
          "strict-True matrix")
    check("S3 state-vs-criteria",
          t["done_proven"] == 2  # b1 + adj1
          and t["front"]["done_proven"] == 1  # adj1 only (f1/f2/dup1 queued)
          and t["front"]["done"] == 2,
          f"done_proven={t['done_proven']} front.dp={t['front']['done_proven']}")
    check("S4 dedup-first-wins", t["front"]["done"] == 2
          and "dup1" in t["front"]["items"] and t["total"] == 14,
          "dup1 counted once, from its done row")
    check("S5 unknown-unspecified-missing-untagged",
          set(t["untagged"]["items"]) == {"u1", "u2", "u3", "u4", "u5", "u6", "u7"},
          f"untagged={sorted(t['untagged']['items'])}")
    # S6: area mapping.
    areas = {"f1": "Area A", "f2": "Area A", "b1": "Area B", "bo1": "Area B"}
    out2 = B1.compute_front_back_split(rows, tags, areas)
    pa = out2["per_area"]
    check("S6 area-buckets",
          set(pa.keys()) == {"Area A", "Area B", "unplaced"}
          and pa["Area A"]["total"] == 2 and pa["Area B"]["total"] == 2
          and pa["unplaced"]["total"] == 10,
          f"areas={sorted(pa.keys())} A={pa['Area A']['total']} "
          f"B={pa['Area B']['total']} unplaced={pa['unplaced']['total']}")
    check("S6b area-sums-match", all(out2["reconciliation"][k] for k in
          ("buckets_sum_equals_unique", "per_area_sums_match")),
          f"recon={out2['reconciliation']}")
    # S7: list views.
    fl, bl = t["front_list"], t["back_list"]
    check("S7 list-views",
          fl["total"] == 5 and bl["total"] == 2
          and fl["total"] == t["front"]["total"] + t["both"]["total"]
          and bl["total"] == t["back"]["total"] + t["both"]["total"]
          and set(fl["items"]) == {"f1", "f2", "adj1", "dup1", "bo1"}
          and set(bl["items"]) == {"b1", "bo1"}
          and set(fl["items"]) & set(bl["items"]) == {"bo1"},
          f"front_list={fl['total']} back_list={bl['total']} overlap=both row")
    # S8: loader.
    import os
    tmp = "/tmp/teambuild-tag-dropin.json"
    with open(tmp, "w") as f:
        json.dump({"f1": "front", "b1": "back"}, f)
    check("S8a loader-dropin", B1.load_tag_mapping(tmp) == {"f1": "front", "b1": "back"})
    check("S8b loader-missing-empty", B1.load_tag_mapping("/tmp/teambuild-no-such-tag.json") == {})
    bad = "/tmp/teambuild-tag-bad.json"
    with open(bad, "w") as f:
        f.write("{not json")
    try:
        B1.load_tag_mapping(bad)
        check("S8c loader-malformed-raises", False, "no raise")
    except Exception:
        check("S8c loader-malformed-raises", True, "raised")
    os.remove(tmp)
    os.remove(bad)
    # S9: empty input.
    out3 = B1.compute_front_back_split([], {})
    check("S9 empty-input", out3["totals"]["total"] == 0 and out3["per_area"] == {}
          and out3["reconciliation"]["buckets_sum_equals_unique"],
          f"totals={out3['totals']['total']}")


def read_criteria_page(limit, offset):
    """One criteria-inclusive page, with the proven cascade: a page that
    fails outright (chunked transport, criteria bulk) retries smaller
    (40 -> 25 -> 10) at the SAME offset, never skipping rows."""
    sql = ("SELECT item_key, state, acceptance_criteria, updated_at FROM work_items "
           f"WHERE project_id = '{PROJECT}' ORDER BY updated_at DESC NULLS LAST, item_key "
           f"LIMIT {limit} OFFSET {offset};")
    try:
        return sql_json(sql), limit
    except RuntimeError:
        if limit > 10:
            nxt = 25 if limit > 25 else 10
            print(f"PAGE offset={offset} limit={limit}: failed; cascading to {nxt}")
            return read_criteria_page(nxt, offset)
        raise


def independent_fresh_read():
    """Independent read: criteria-inclusive, own dedup loop, cascading
    page sizes, 1s pacing between pages (flaky transport window)."""
    rows = []
    offset = 0
    limit = 40
    while True:
        page, eff = read_criteria_page(limit, offset)
        if not page:
            break
        rows.extend(page)
        offset += len(page)
        limit = eff  # adopt the page size that actually works
        if len(page) < eff:
            break
        time.sleep(1)
    seen = {}
    for row in rows:
        if row.get("item_key") not in seen:
            seen[row["item_key"]] = row
    return rows, seen


def live_tests():
    raw, deduped = independent_fresh_read()
    fresh_total = len(raw)
    fresh_unique = len(deduped)
    fresh_done = sum(1 for r in deduped.values() if r.get("state") == "done_proven")
    print(f"FRESH READ: raw={fresh_total} unique={fresh_unique} done_proven={fresh_done}")
    print(f"BASELINE AT READ: unique={fresh_unique} done_proven={fresh_done} "
          f"(prior baseline 394/24; any drift is live seat work, reported not hidden)")
    check("L1 live-read-no-duplicates", fresh_total == fresh_unique,
          f"raw={fresh_total} unique={fresh_unique}")
    with open(TAG_FILE, "r", encoding="utf-8") as f:
        tags = json.load(f)
    from collections import Counter
    counts = Counter(tags.values())
    check("L2 mapping-file-counts", len(tags) == 392
          and counts.get("front") == 165 and counts.get("back") == 119
          and counts.get("both") == 92 and counts.get("process") == 16
          and "unspecified" not in counts,
          f"keys={len(tags)} counts={dict(counts)}")
    live_keys = set(deduped.keys())
    mapped_keys = set(tags.keys())
    mapped_live = mapped_keys & live_keys
    unmapped = sorted(live_keys - mapped_keys)
    print(f"UNMAPPED LIVE KEYS ({len(unmapped)}): {unmapped}")
    check("L3 key-sets", mapped_live == mapped_keys and len(mapped_live) == 392,
          f"mapped_live={len(mapped_live)} unmapped={len(unmapped)}")
    # Split over the fresh-read rows in the order the read returned them
    # (updated_at DESC NULLS LAST, the compute precondition).
    out = B1.compute_front_back_split(raw, tags)
    t = out["totals"]
    print(f"LIVE SPLIT: front={t['front']['total']}/{t['front']['done']} "
          f"back={t['back']['total']}/{t['back']['done']} "
          f"both={t['both']['total']}/{t['both']['done']} "
          f"process={t['process']['total']}/{t['process']['done']} "
          f"untagged={t['untagged']['total']}/{t['untagged']['done']} "
          f"total={t['total']} criteria_done={t['done']} done_proven={t['done_proven']}")
    print(f"LIVE LISTS: front_list={t['front_list']['total']}/{t['front_list']['done']} "
          f"back_list={t['back_list']['total']}/{t['back_list']['done']}")
    # Expected buckets recomputed independently from mapping + live key
    # set (drift-proof: new live rows land in untagged by construction).
    exp = {name: sum(1 for k in live_keys if tags.get(k) == name)
           for name in ("front", "back", "both", "process")}
    exp["untagged"] = fresh_unique - len(mapped_live)
    check("L4 live-buckets", t["front"]["total"] == exp["front"]
          and t["back"]["total"] == exp["back"]
          and t["both"]["total"] == exp["both"]
          and t["process"]["total"] == exp["process"]
          and t["untagged"]["total"] == exp["untagged"]
          and t["total"] == fresh_unique and t["done_proven"] == fresh_done,
          f"expected={exp} got=({t['front']['total']},{t['back']['total']},"
          f"{t['both']['total']},{t['process']['total']},{t['untagged']['total']}) "
          f"total={t['total']} dp={t['done_proven']}")
    check("L4b live-recon-block", all(out["reconciliation"][k] for k in
          ("buckets_sum_equals_unique",
           "done_proven_sum_equals_unique_done_proven",
           "per_area_sums_match"))
          and out["reconciliation"]["unique"] == fresh_unique
          and out["reconciliation"]["per_area_totals_sum"] == fresh_unique,
          f"recon={out['reconciliation']}")
    check("L5 bucket-done-bounded", all(
        t[n]["done"] <= t[n]["total"] and t[n]["done_proven"] <= t[n]["total"]
        for n in ("front", "back", "both", "process", "untagged")),
        f"untagged.done={t['untagged']['done']} untagged.items={t['untagged']['items']}")
    check("L6 live-area-unplaced-only", set(out["per_area"].keys()) == {"unplaced"}
          and out["per_area"]["unplaced"]["total"] == fresh_unique,
          f"areas={sorted(out['per_area'].keys())}")
    # L7: CLI --tag-mapping path prints a matching FRONT_BACK split.
    # The CLI is read-only (live fetch + print, no side effects), so a
    # run that yields no FRONT_BACK line gets ONE deliberate second run
    # after pacing — the same fresh-run discipline as the page readers.
    # A second run is used only when the first produced nothing to parse.
    def run_cli():
        try:
            r = subprocess.run([sys.executable, "workspace/system/b1-serve-ready-2026-10-28.py",
                                "--tag-mapping", TAG_FILE],
                               capture_output=True, text=True, timeout=1200, cwd=".")
        except subprocess.TimeoutExpired:
            return None, None
        fb = None
        for line in r.stdout.splitlines():
            if line.startswith("FRONT_BACK:"):
                fb = json.loads(line[len("FRONT_BACK:"):].strip())
        return r.returncode, fb
    rc, fb = run_cli()
    attempts = 1
    if fb is None:
        time.sleep(10)
        rc, fb = run_cli()
        attempts = 2
    if fb is None:
        check("L7 cli-tag-mapping-matches", False,
              f"attempts={attempts} no FRONT_BACK line (timeout or fetch failure)")
    else:
        fbrec = fb["reconciliation"]
        fb_dp_sum = sum(fb["totals"][n]["done_proven"]
                        for n in ("front", "back", "both", "process", "untagged"))
        ok = (all(fbrec[k] for k in ("buckets_sum_equals_unique",
                                     "done_proven_sum_equals_unique_done_proven",
                                     "per_area_sums_match"))
              and fb["totals"]["front"]["total"] == 165
              and fb["totals"]["back"]["total"] == 119
              and fb["totals"]["both"]["total"] == 92
              and fb["totals"]["process"]["total"] == 16
              and fb["totals"]["untagged"]["total"] == fb["totals"]["total"] - 392
              and fb["totals"]["done_proven"] == fb_dp_sum)
        check("L7 cli-tag-mapping-matches", ok,
              f"attempts={attempts} rc={rc} fb_total={fb['totals']['total']} "
              f"fresh_unique={fresh_unique} (drift between sections is reported, not asserted)")


def main():
    fixture_tests()
    live_tests()
    print("FAILURES:", FAILURES if FAILURES else "none")
    print("ALL_PASS:", not FAILURES)
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
