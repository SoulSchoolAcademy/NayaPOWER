"""Tests for living_ledger.chain.verify_chain.

A helper builds genuinely valid chains with canonical_event_hash; every
negative control then breaks exactly one link property and asserts the
verifier names it. Nothing here touches a database.
"""
import pytest

from living_ledger.chain import (
    ChainVerdict,
    canonical_event_hash,
    normalize_postgres_event,
    verify_chain,
)


def _event(index, previous_hash, **overrides):
    event = {
        "owner_id": "owner-123",
        "event_type": "shipped slice %d" % index,
        "event_at": "2026-10-11T10:5%d:00+00:00" % index,
        "source_table": "living_ledger",
        "source_id": "receipt-%d" % index,
        "parent_ledger_event_id": None,
        "previous_chain_hash": previous_hash,
        "evidence_refs": ["proof-%d" % index],
        "metadata": {"actor": "naya2/build-lane", "scope": "team"},
        "chain_seq": index + 1,
    }
    event.update(overrides)
    event["event_hash"] = canonical_event_hash(event)
    return event


def _chain(length=3):
    events = []
    previous = None
    for index in range(length):
        event = _event(index, previous)
        events.append(event)
        previous = event["event_hash"]
    return events


# --- positive controls -----------------------------------------------------

def test_valid_chain_verifies():
    verdict = verify_chain(_chain(3))
    assert verdict.ok
    assert verdict.verdict == "CHAIN_VALID"


def test_single_genesis_event_verifies():
    assert verify_chain(_chain(1)).verdict == "CHAIN_VALID"


def test_chain_without_seq_still_verifies():
    events = _chain(3)
    for event in events:
        del event["chain_seq"]
        # hash must be recomputed after removing a non-hashed field? chain_seq
        # is NOT a hash field, so stored hashes stay valid.
    assert verify_chain(events).verdict == "CHAIN_VALID"


# --- negative controls ------------------------------------------------------

def test_empty_chain_is_not_a_pass():
    verdict = verify_chain([])
    assert verdict.verdict == "EMPTY_CHAIN"
    assert not verdict.ok


def test_tampered_evidence_fails_hash():
    events = _chain(3)
    events[1]["evidence_refs"] = ["forged proof"]
    verdict = verify_chain(events)
    assert verdict.verdict == "HASH_MISMATCH"
    assert verdict.index == 1
    assert verdict.expected != verdict.actual


def test_tampered_action_fails_hash():
    events = _chain(3)
    events[2]["event_type"] = "rewrote history"
    verdict = verify_chain(events)
    assert verdict.verdict == "HASH_MISMATCH"
    assert verdict.index == 2


def test_dropped_event_breaks_link():
    events = _chain(3)
    del events[1]
    verdict = verify_chain(events)
    assert verdict.verdict == "LINK_BROKEN"
    assert verdict.index == 1


def test_reordered_events_never_silently_pass():
    events = _chain(3)
    events[0], events[1] = events[1], events[0]
    verdict = verify_chain(events)
    assert verdict.verdict in ("HASH_MISMATCH", "LINK_BROKEN")
    assert not verdict.ok


def test_forged_event_hash_fails():
    events = _chain(3)
    events[1]["event_hash"] = "0" * 64
    verdict = verify_chain(events)
    assert verdict.verdict == "HASH_MISMATCH"
    assert verdict.index == 1
    assert verdict.actual == "0" * 64


def test_seq_regression_fails():
    events = _chain(3)
    events[2]["chain_seq"] = 1  # not a hash field; stored hash stays valid
    verdict = verify_chain(events)
    assert verdict.verdict == "SEQ_REGRESSION"
    assert verdict.index == 2


def test_genesis_pointing_at_predecessor_fails():
    events = _chain(2)
    events[0]["previous_chain_hash"] = "abc123"
    events[0]["event_hash"] = canonical_event_hash(events[0])
    # fix the follow-on link so only the genesis rule is under test
    events[1]["previous_chain_hash"] = events[0]["event_hash"]
    events[1]["event_hash"] = canonical_event_hash(events[1])
    verdict = verify_chain(events)
    assert verdict.verdict == "LINK_BROKEN"
    assert verdict.index == 0


def test_missing_event_hash_fails():
    events = _chain(2)
    del events[0]["event_hash"]
    verdict = verify_chain(events)
    assert verdict.verdict == "HASH_MISMATCH"
    assert verdict.index == 0


def test_non_mapping_event_fails():
    verdict = verify_chain(["not-an-event"])
    assert verdict.verdict == "HASH_MISMATCH"
    assert not verdict.ok


def test_broken_middle_link_names_both_hashes():
    events = _chain(3)
    events[2]["previous_chain_hash"] = "deadbeef"
    events[2]["event_hash"] = canonical_event_hash(events[2])
    verdict = verify_chain(events)
    assert verdict.verdict == "LINK_BROKEN"
    assert verdict.index == 2
    assert verdict.expected == events[1]["event_hash"]
    assert verdict.actual == "deadbeef"


# --- canonical encoding -----------------------------------------------------

def test_hash_field_order_matters():
    event = _event(0, None)
    h1 = canonical_event_hash(event)
    swapped = dict(event)
    swapped["event_type"], swapped["source_id"] = (
        swapped["source_id"], swapped["event_type"])
    assert canonical_event_hash(swapped) != h1


def test_none_and_empty_string_render_identically():
    base = _event(0, None)
    variant = dict(base)
    variant["parent_ledger_event_id"] = ""
    # None renders as ""; "" renders as "" -> same hash pre-stamp.
    # (Stored hash covers the base form; this pins the rendering rule.)
    assert canonical_event_hash(variant) == base["event_hash"]


def test_metadata_key_order_does_not_change_hash():
    base = _event(0, None)
    variant = dict(base)
    variant["metadata"] = {"scope": "team", "actor": "naya2/build-lane"}
    assert canonical_event_hash(variant) == base["event_hash"]


def test_normalize_postgres_event_converts_timestamptz():
    row = _event(0, None)
    row["event_at"] = "2026-10-11 10:50:00+00"
    row["evidence_refs"] = '["proof-0"]'
    normalized = normalize_postgres_event(row)
    assert normalized["event_at"] == "2026-10-11T10:50:00+00:00"
    assert normalized["evidence_refs"] == ["proof-0"]
    # input untouched
    assert row["event_at"] == "2026-10-11 10:50:00+00"


def test_verdict_ok_property():
    assert ChainVerdict(verdict="CHAIN_VALID").ok
    assert not ChainVerdict(verdict="HASH_MISMATCH").ok
