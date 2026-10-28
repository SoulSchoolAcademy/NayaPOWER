"""Tests for the Conversation endpoint prototype (fixtures only).

Run: python3 test-conversation-endpoint-2026-10-28.py
Exit 0 only when every test passes; exit 1 otherwise. Prints exact
PASS/FAIL counts plus one line per failure. No network, no record access.

The module file uses hyphens (conversation-endpoint-2026-10-28.py), so it
is loaded via importlib, not a plain import.
"""

import importlib.util
import os
import sys
import uuid

_HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "conversation_endpoint_2026_10_28",
    os.path.join(_HERE, "conversation-endpoint-2026-10-28.py"),
)
_MOD = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MOD)

ConversationService = _MOD.ConversationService
ConversationUnavailable = _MOD.ConversationUnavailable
FailingStore = _MOD.FailingStore
InMemoryStore = _MOD.InMemoryStore
UnverifiableStore = _MOD.UnverifiableStore
ValidationError = _MOD.ValidationError

RESULTS = []


def check(name, fn):
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - report, don't crash the run
        RESULTS.append((name, False, repr(exc)))
    else:
        RESULTS.append((name, True, ""))


def new_id():
    return str(uuid.uuid4())


# ---- 1. append stores with seq 1, duplicate False ----
def t_append_first():
    svc = ConversationService(InMemoryStore())
    out = svc.append_message("block-a", new_id(), "naya-power", "hello")
    assert out["duplicate"] is False, out
    assert out["message"]["seq"] == 1, out
    assert out["message"]["author_alias"] == "naya-power", out
    assert out["message"]["body"] == "hello", out
    assert out["message"]["block_key"] == "block-a", out


# ---- 2. retry with same id returns same message, writes nothing ----
def t_append_retry_idempotent():
    svc = ConversationService(InMemoryStore())
    mid = new_id()
    first = svc.append_message("block-a", mid, "naya-power", "hello")
    # Simulate a lost response: the client retries the SAME send.
    second = svc.append_message("block-a", mid, "naya-power", "hello")
    assert second["duplicate"] is True, second
    assert second["message"] == first["message"], (first, second)
    opened = svc.open_conversation("block-a")
    assert opened["count"] == 1, opened
    assert opened["messages"][0]["seq"] == 1, opened


# ---- 3. multiple appends read back in seq order ----
def t_ordering():
    svc = ConversationService(InMemoryStore())
    svc.append_message("block-a", new_id(), "naya-power", "one")
    svc.append_message("block-a", new_id(), "nitro", "two")
    svc.append_message("block-a", new_id(), "resolve", "three")
    opened = svc.open_conversation("block-a")
    assert [m["seq"] for m in opened["messages"]] == [1, 2, 3], opened
    assert [m["body"] for m in opened["messages"]] == ["one", "two", "three"]
    assert opened["count"] == 3, opened


# ---- 4. per-block isolation: no leakage, independent seq ----
def t_isolation():
    svc = ConversationService(InMemoryStore())
    svc.append_message("block-a", new_id(), "naya-power", "for A")
    svc.append_message("block-a", new_id(), "naya-power", "also A")
    svc.append_message("block-b", new_id(), "nitro", "for B")
    a = svc.open_conversation("block-a")
    b = svc.open_conversation("block-b")
    assert a["count"] == 2 and b["count"] == 1, (a, b)
    assert all(m["body"] != "for B" for m in a["messages"]), a
    assert all(m["body"] != "for A" for m in b["messages"]), b
    assert [m["seq"] for m in b["messages"]] == [1], b
    assert a["participants"] == ["naya-power"], a
    assert b["participants"] == ["nitro"], b
    # Same client message_id in a DIFFERENT block is a different message.
    mid = new_id()
    svc.append_message("block-a", mid, "naya-power", "shared id A")
    out = svc.append_message("block-b", mid, "naya-power", "shared id B")
    assert out["duplicate"] is False, out
    assert svc.open_conversation("block-b")["count"] == 2


# ---- 5. open on an empty block: empty, not an error ----
def t_open_empty():
    svc = ConversationService(InMemoryStore())
    opened = svc.open_conversation("block-new")
    assert opened["messages"] == [], opened
    assert opened["participants"] == [], opened
    assert opened["count"] == 0, opened


# ---- 6. store outage: open and append raise, never fake data ----
def t_outage():
    svc = ConversationService(FailingStore())
    for fn in (
        lambda: svc.open_conversation("block-a"),
        lambda: svc.append_message("block-a", new_id(), "naya-power", "x"),
    ):
        try:
            fn()
        except ConversationUnavailable as exc:
            assert exc.error == "conversation_store_unavailable", exc
        else:
            raise AssertionError("outage did not raise ConversationUnavailable")


# ---- 7. validation rejects bad input, writes nothing ----
def t_validation():
    svc = ConversationService(InMemoryStore())
    bad = [
        ("", new_id(), "naya-power", "x"),  # empty block key
        ("block-a", "not-a-uuid", "naya-power", "x"),  # bad message id
        ("block-a", new_id(), "", "x"),  # empty alias
        ("block-a", new_id(), "naya-power", "   "),  # blank body
        ("block-a", new_id(), "naya-power", "x" * 8001),  # overlong body
    ]
    for args in bad:
        try:
            svc.append_message(*args)
        except ValidationError:
            pass
        else:
            raise AssertionError("invalid input accepted: %r" % (args,))
    assert svc.open_conversation("block-a")["count"] == 0


# ---- 8. participants in first-appearance order ----
def t_participants():
    svc = ConversationService(InMemoryStore())
    svc.append_message("block-a", new_id(), "nitro", "first")
    svc.append_message("block-a", new_id(), "naya-power", "second")
    svc.append_message("block-a", new_id(), "nitro", "third")
    opened = svc.open_conversation("block-a")
    assert opened["participants"] == ["nitro", "naya-power"], opened


# ---- 9. unverifiable write is refused, never claimed as success ----
def t_verify_after_write():
    svc = ConversationService(UnverifiableStore())
    try:
        svc.append_message("block-a", new_id(), "naya-power", "lost")
    except ConversationUnavailable as exc:
        assert "verification failed" in exc.detail, exc
    else:
        raise AssertionError("unverifiable write was reported as success")


# ---- 10. pagination: after_seq + limit slice correctly ----
def t_pagination():
    svc = ConversationService(InMemoryStore())
    for i in range(5):
        svc.append_message("block-a", new_id(), "naya-power", "m%d" % i)
    page = svc.open_conversation("block-a", after_seq=2, limit=2)
    assert [m["seq"] for m in page["messages"]] == [3, 4], page
    assert page["count"] == 5, page  # count is the block total, not page size
    tail = svc.open_conversation("block-a", after_seq=4)
    assert [m["seq"] for m in tail["messages"]] == [5], tail


# ---- 11. duplicate flag survives a third identical retry ----
def t_triple_retry():
    svc = ConversationService(InMemoryStore())
    mid = new_id()
    svc.append_message("block-a", mid, "resolve", "once")
    for _ in range(2):
        out = svc.append_message("block-a", mid, "resolve", "once")
        assert out["duplicate"] is True, out
    assert svc.open_conversation("block-a")["count"] == 1


TESTS = [
    ("append_first_seq1", t_append_first),
    ("append_retry_idempotent", t_append_retry_idempotent),
    ("ordering_seq", t_ordering),
    ("per_block_isolation", t_isolation),
    ("open_empty_block", t_open_empty),
    ("store_outage_503", t_outage),
    ("validation_rejects", t_validation),
    ("participants_order", t_participants),
    ("verify_after_write", t_verify_after_write),
    ("pagination", t_pagination),
    ("triple_retry_once", t_triple_retry),
]


def main():
    for name, fn in TESTS:
        check(name, fn)
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    failed = [(n, e) for n, ok, e in RESULTS if not ok]
    print("PASS %d / %d" % (passed, len(RESULTS)))
    for name, err in failed:
        print("FAIL %s: %s" % (name, err))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
