#!/usr/bin/env python3
"""Tests for the C5 notes endpoint prototype (2026-10-28). NOT live.

Proves, against fixture stores (never the live record):
  1. append-once under retry (same client_id 3x -> exactly 1 entry)
  2. feed read returns appended notes in stored order
  3. no device-local state (stores independent; service holds nothing)
  4. record unavailable -> 503 with NO notes key (never a snapshot)
  5. validation -> 400 with the offending field
  6. unknown item -> 404 (distinct from 503)
  7. lost-response recovery (write lands, response lost -> found, not resent)
  8. race guard: injected racing entry -> both entries, each exactly once
  9. legacy tolerance (entries missing 'note' pass through, nothing invented)
 10. feed separation (item feed vs project feed never mix)

Exit 0 on all pass, 1 on any failure. Prints exact pass/fail counts.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util  # noqa: E402
# The module file uses hyphens, so it cannot be imported by name;
# load it from its path instead.
_spec = importlib.util.spec_from_file_location(
    "c5mod",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "c5-notes-endpoint-2026-10-28.py"))
c5mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c5mod)
serve_list = c5mod.serve_list
serve_append = c5mod.serve_append
append_note = c5mod.append_note
MemoryNoteStore = c5mod.MemoryNoteStore
FaultyStore = c5mod.FaultyStore
new_client_id = c5mod.new_client_id


def test_append_once_under_retry():
    store = MemoryNoteStore()
    cid = new_client_id()
    n1, d1, p1 = append_note(store, None, "naya-power", "first", cid)
    n2, d2, p2 = append_note(store, None, "naya-power", "first", cid)
    n3, d3, p3 = append_note(store, None, "naya-power", "first", cid)
    assert (d1, p1) == (False, 1), (d1, p1)
    assert (d2, p2) == (True, 1), (d2, p2)
    assert (d3, p3) == (True, 1), (d3, p3)
    assert n1 == n2 == n3, (n1, n2, n3)
    status, body = serve_list(store, None)
    assert status == 200 and body["count"] == 1, body


def test_feed_order():
    store = MemoryNoteStore()
    for text in ("alpha", "beta", "gamma"):
        append_note(store, None, "naya-power", text, new_client_id())
    status, body = serve_list(store, None)
    assert status == 200, body
    assert [n["note"] for n in body["notes"]] == ["alpha", "beta", "gamma"]
    assert body["count"] == 3


def test_no_device_local_state():
    store_a = MemoryNoteStore()
    append_note(store_a, None, "naya-power", "only in A", new_client_id())
    store_b = MemoryNoteStore()
    status, body = serve_list(store_b, None)
    assert status == 200 and body["notes"] == [] and body["count"] == 0, body
    # A fresh store over the same service functions sees nothing of A.
    store_c = MemoryNoteStore()
    append_note(store_c, None, "naya-power", "only in C", new_client_id())
    _, body_a = serve_list(store_a, None)
    _, body_c = serve_list(store_c, None)
    assert [n["note"] for n in body_a["notes"]] == ["only in A"]
    assert [n["note"] for n in body_c["notes"]] == ["only in C"]


def test_record_unavailable_503():
    inner = MemoryNoteStore()
    store = FaultyStore(inner, fail_reads=True)
    status, body = serve_list(store, None)
    assert status == 503, (status, body)
    assert "notes" not in body, body
    assert body == {"error": "notes_unavailable"}, body
    status, body = serve_append(store, {"from": "naya-power",
                                        "note": "x",
                                        "client_id": new_client_id()})
    assert status == 503 and "note" not in body, (status, body)


def test_validation_400():
    store = MemoryNoteStore()
    cases = [
        ({"from": "", "note": "x", "client_id": new_client_id()}, "from"),
        ({"from": "naya-power", "note": "   ",
          "client_id": new_client_id()}, "note"),
        ({"from": "naya-power", "note": "x"}, "client_id"),
        ({"note": "x", "client_id": new_client_id()}, "from"),
    ]
    for payload, field in cases:
        status, body = serve_append(store, payload)
        assert status == 400, (status, body, payload)
        assert body["error"] == "invalid_note"
        assert body["detail"] == field, body
    _, body = serve_list(store, None)
    assert body["count"] == 0  # nothing invalid was stored


def test_unknown_item_404():
    store = MemoryNoteStore()
    status, body = serve_list(store, "no-such-item")
    assert status == 404 and body == {"error": "unknown_item"}, (status, body)
    status, body = serve_append(store, {"item": "no-such-item",
                                        "from": "naya-power", "note": "x",
                                        "client_id": new_client_id()})
    assert status == 404, (status, body)


def test_lost_response_recovery():
    inner = MemoryNoteStore()
    store = FaultyStore(inner, fail_append_after_land=True)
    cid = new_client_id()
    # The write lands but its response is lost: the caller must still
    # see success with exactly one entry, never a duplicate.
    status, body = serve_append(store, {"from": "naya-power",
                                        "note": "landed",
                                        "client_id": cid})
    assert status == 200, (status, body)
    assert body["duplicate"] is False and body["position"] == 1, body
    status, body = serve_append(store, {"from": "naya-power",
                                        "note": "landed",
                                        "client_id": cid})
    assert status == 200 and body["duplicate"] is True, (status, body)
    _, body = serve_list(store, None)
    assert body["count"] == 1, body


def test_race_guard_reruns_decision():
    inner = MemoryNoteStore()
    racer = {"at": "2026-10-28T00:00:00Z", "from": "naya-resolve",
             "note": "racer", "client_id": new_client_id()}

    def hook():
        inner.append_guarded(None, racer, len(inner.read(None)))

    store = FaultyStore(inner, race_hook=hook)
    cid = new_client_id()
    status, body = serve_append(store, {"from": "naya-power",
                                        "note": "mine", "client_id": cid})
    assert status == 200 and body["duplicate"] is False, (status, body)
    _, body = serve_list(store, None)
    notes = [(n["note"], n["client_id"]) for n in body["notes"]]
    assert notes == [("racer", racer["client_id"]), ("mine", cid)], notes


def test_legacy_tolerance():
    store = MemoryNoteStore()
    # Legacy entry: at + from only, no note text, no client_id.
    store._feeds[None] = [{"at": "2026-10-25", "from": "old-report"}]
    status, body = serve_list(store, None)
    assert status == 200, (status, body)
    assert body["count"] == 1
    assert body["notes"][0] == {"at": "2026-10-25", "from": "old-report"}
    assert "note" not in body["notes"][0]  # nothing invented


def test_feed_separation():
    store = MemoryNoteStore()
    store.create_item("some-item")
    append_note(store, "some-item", "naya-power", "item note",
                new_client_id())
    append_note(store, None, "naya-power", "project note",
                new_client_id())
    _, item_body = serve_list(store, "some-item")
    _, proj_body = serve_list(store, None)
    assert [n["note"] for n in item_body["notes"]] == ["item note"]
    assert [n["note"] for n in proj_body["notes"]] == ["project note"]
    assert item_body["item"] == "some-item"
    assert proj_body["item"] is None


TESTS = [
    ("append-once under retry", test_append_once_under_retry),
    ("feed order", test_feed_order),
    ("no device-local state", test_no_device_local_state),
    ("record unavailable -> 503", test_record_unavailable_503),
    ("validation -> 400", test_validation_400),
    ("unknown item -> 404", test_unknown_item_404),
    ("lost-response recovery", test_lost_response_recovery),
    ("race guard reruns decision", test_race_guard_reruns_decision),
    ("legacy tolerance", test_legacy_tolerance),
    ("feed separation", test_feed_separation),
]


def main():
    passed, failed = 0, 0
    for name, fn in TESTS:
        try:
            fn()
            passed += 1
            print(f"PASS {name}")
        except Exception as exc:  # noqa: BLE001 - report, don't hide
            failed += 1
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    print(f"{passed} passed, {failed} failed, {len(TESTS)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
