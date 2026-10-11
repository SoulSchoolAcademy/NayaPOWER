"""Adversarial tests for UD-18 — the Living Ledger (tools/living_ledger.py).

Acceptance gate: every consequential action emits a chained receipt, any
seat can verify any receipt live, and nothing consequential is untracked.
One failure = FAIL.
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from living_ledger import LivingLedger, LedgerError, GENESIS_PREV


def fresh():
    return LivingLedger()


def emit_decision(ledger, actor="naya-4", action="merge fix", refs=("ev-1",)):
    return ledger.emit(actor=actor, kind="DECISION", action=action,
                       evidence_refs=refs, scope="repo")


# ---- positive: write, query, chain-verify -------------------------------

def test_emit_and_chain_verifies():
    L = fresh()
    r1 = emit_decision(L)
    r2 = L.emit(actor="naya-2", kind="ACTION", action="ran checks",
                evidence_refs=("ev-2",), links=(r1.entry_hash,))
    assert r1.seq == 1 and r1.prev_hash == GENESIS_PREV
    assert r2.seq == 2 and r2.prev_hash == r1.entry_hash
    ok, brk, _ = L.verify_chain()
    assert ok and brk is None, "healthy chain must verify"


def test_query_surface():
    L = fresh()
    emit_decision(L, actor="naya-4")
    emit_decision(L, actor="naya-2", action="other")
    L.emit(actor="naya-4", kind="EVIDENCE", action="stored proof",
           evidence_refs=("ev-x",))
    assert len(L.by_actor("naya-4")) == 2
    assert len(L.by_kind("DECISION")) == 2
    assert len(L.by_kind("EVIDENCE")) == 1
    rows = L.by_time_range("2000-01-01", "2100-01-01")
    assert len(rows) == 3
    assert L.get(2).action == "other"
    assert L.get(99) is None


def test_causal_chain_follows_links():
    L = fresh()
    d = emit_decision(L)
    a = L.emit(actor="naya-4", kind="ACTION", action="executed",
               evidence_refs=("ev-a",), links=(d.entry_hash,))
    o = L.emit(actor="naya-4", kind="OUTCOME", action="verified +3",
               evidence_refs=("ev-o",), links=(a.entry_hash,))
    chain = L.causal_chain(o.seq)
    assert [r.seq for r in chain] == [d.seq, a.seq, o.seq]
    # Unrelated receipt is not in the chain.
    emit_decision(L, actor="naya-9", action="unrelated")
    chain2 = L.causal_chain(o.seq)
    assert [r.seq for r in chain2] == [d.seq, a.seq, o.seq]


def test_single_receipt_verifies():
    L = fresh()
    emit_decision(L)
    assert L.verify_receipt(1) is True
    assert L.head_seq == 1
    assert L.head_hash == L.get(1).entry_hash


def test_anchor_summary_accepted_when_hash_matches():
    L = fresh()
    payload = LivingLedger.seal_payload({
        "ledger": "work-honesty", "head_seq": 42, "entry_count": 42,
        "head_hash": "abc123", "anchored_at": "2026-10-10T20:00:00Z"})
    r = L.anchor_summary(ledger_name="work-honesty", payload=payload)
    assert r.kind == "ANCHOR"
    assert r.evidence_refs == (payload["payload_hash"],)
    ok, _, _ = L.verify_chain()
    assert ok


def test_persistence_roundtrip():
    L = fresh()
    emit_decision(L)
    emit_decision(L, actor="naya-2", action="second")
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "ledger.jsonl")
        L.save(p)
        L2 = LivingLedger.load(p)
    ok, _, _ = L2.verify_chain()
    assert ok and L2.head_seq == 2
    assert L2.get(1).entry_hash == L.get(1).entry_hash


def test_render_surface_writes_page():
    L = fresh()
    emit_decision(L)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "surface.html")
        L.render_surface(p)
        html = open(p, encoding="utf-8").read()
    assert "CHAIN OK" in html
    assert "merge fix" in html
    assert "ev-1" in html


# ---- negative: tampering, backdating, unlinking, bad anchors -------------

def test_tampered_entry_detected_at_exact_seq():
    L = fresh()
    emit_decision(L)
    emit_decision(L, actor="naya-2", action="second")
    emit_decision(L, actor="naya-3", action="third")
    # Tamper with entry 2's content in place (simulating file edit).
    victim = L._entries[1]
    tampered = type(victim)(
        seq=victim.seq, timestamp=victim.timestamp, actor=victim.actor,
        kind=victim.kind, action="MALICIOUS EDIT", evidence_refs=victim.evidence_refs,
        scope=victim.scope, content=victim.content, links=victim.links,
        prev_hash=victim.prev_hash, entry_hash=victim.entry_hash)
    L._entries[1] = tampered
    ok, brk, detail = L.verify_chain()
    assert not ok and brk == 2, f"must break at seq 2, got {brk}: {detail}"


def test_tampered_file_refused_on_load():
    L = fresh()
    emit_decision(L)
    emit_decision(L, actor="naya-2", action="second")
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "ledger.jsonl")
        L.save(p)
        lines = open(p).read().splitlines()
        d2 = json.loads(lines[0])
        d2["action"] = "forged"
        lines[0] = json.dumps(d2)
        open(p, "w").write("\n".join(lines) + "\n")
        try:
            LivingLedger.load(p)
            raise AssertionError("tampered file must be refused")
        except LedgerError as e:
            assert e.code == "CHAIN_BREAK", e.code


def test_backdated_entry_refused():
    L = fresh()
    L.emit(actor="naya-4", kind="NOTE", action="now",
           timestamp="2026-10-10T20:00:00+00:00")
    try:
        L.emit(actor="naya-4", kind="NOTE", action="earlier",
               timestamp="2026-10-10T19:00:00+00:00")
        raise AssertionError("backdated entry must be refused")
    except LedgerError as e:
        assert e.code == "BACKDATED_ENTRY", e.code
    assert L.head_seq == 1  # refused entry never recorded


def test_unlinked_decision_refused():
    L = fresh()
    for kind in ("DECISION", "ACTION"):
        try:
            L.emit(actor="naya-4", kind=kind, action="no evidence")
            raise AssertionError(f"unlinked {kind} must be refused")
        except LedgerError as e:
            assert e.code == "UNLINKED_DECISION", e.code
    # EVIDENCE and NOTE kinds may stand without refs.
    L.emit(actor="naya-4", kind="NOTE", action="observation")
    assert L.head_seq == 1


def test_dangling_link_refused():
    L = fresh()
    try:
        L.emit(actor="naya-4", kind="NOTE", action="bad link",
               links=("deadbeef" * 8,))
        raise AssertionError("dangling link must be refused")
    except LedgerError as e:
        assert e.code == "UNKNOWN_LINK", e.code


def test_anchor_with_wrong_hash_refused():
    L = fresh()
    payload = LivingLedger.seal_payload({"ledger": "belief", "head_seq": 7})
    payload["payload_hash"] = "0" * 64  # forge the hash
    try:
        L.anchor_summary(ledger_name="belief", payload=payload)
        raise AssertionError("forged anchor must be refused")
    except LedgerError as e:
        assert e.code == "ANCHOR_HASH_MISMATCH", e.code
    assert L.head_seq == 0  # nothing recorded


def test_duplicate_sequence_in_file_refused():
    L = fresh()
    emit_decision(L)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "ledger.jsonl")
        L.save(p)
        with open(p, "a") as f:  # append a second seq-1 entry
            f.write(open(p).read().splitlines()[0] + "\n")
        try:
            LivingLedger.load(p)
            raise AssertionError("duplicated seq must be refused")
        except LedgerError as e:
            assert e.code == "DUPLICATE_SEQUENCE", e.code


def test_forked_prev_hash_detected():
    L = fresh()
    r1 = emit_decision(L)
    # Forge a fork: entry 2 pointing at a wrong prev_hash but with a
    # recomputed-looking hash is still caught because prev linkage breaks
    # the moment the real head is present. Simulate by hand-editing.
    L.emit(actor="naya-2", kind="NOTE", action="real two")
    L._entries[1] = type(L._entries[1])(
        **{**L._entries[1].to_dict(),
            "evidence_refs": tuple(L._entries[1].evidence_refs),
            "links": tuple(L._entries[1].links),
            "content": dict(L._entries[1].content),
            "prev_hash": "f" * 64})
    ok, brk, _ = L.verify_chain()
    assert not ok and brk == 2


def test_unknown_kind_and_empty_actor_refused():
    L = fresh()
    for kwargs in ({"actor": "", "kind": "NOTE", "action": "x"},
                   {"actor": "naya-4", "kind": "VIBE", "action": "x"}):
        try:
            L.emit(**kwargs)
            raise AssertionError("must be refused")
        except LedgerError as e:
            assert e.code in ("EMPTY_ACTOR", "UNKNOWN_KIND"), e.code
    assert L.head_seq == 0


def run_all():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} green")
    return failed


if __name__ == "__main__":
    sys.exit(1 if run_all() else 0)
