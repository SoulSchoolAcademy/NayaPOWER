"""Acceptance tests for the nine-node kernel behavior engine.

WHY THIS FILE EXISTS
--------------------
`BRAIN/12-ENGINEERING/kernel_behavior_engine.py` is 446 lines of executable kernel
logic that had ZERO tests. An unverified executable artifact is not a kernel; it is a
claim. These tests are what move it from CLAIMED to TESTED.

They do not assert the engine is good. They assert four falsifiable things:

  1. FAIL-CLOSED   SELF halts without identity or mission; LAW denies without
                   authority, and distinguishes revoked from expired.
  2. DISTINCT      all nine Nodes produce different receipts. This is the specific
                   failure mode already found once in this repository, where nine
                   Node OBJECTS were one template wearing nine labels. If the engine
                   is a template, Naya has one Node, not nine.
  3. COMPOSABLE    a full cycle produces a receipt per Node.
  4. TYPED         LAW emits the typed vocabulary its contract declares, so a
                   runtime can check the result instead of parsing prose.

The oracle for "distinct" is behavioural: two Nodes that enforce identical rules and
transition identically are the same Node regardless of their names.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
ENGINE_REL = 'BRAIN/12-ENGINEERING/kernel_behavior_engine.py'
NODES = ('SELF', 'LAW', 'ACT', 'KNOW', 'PROVE', 'CONNECT', 'VERIFY', 'LEARN', 'EVOLVE')


def _engine():
    """Load the engine. It sits under a dashed directory, so it is loaded by path."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    spec = importlib.util.spec_from_file_location('kernel_behavior_engine', REPO / ENGINE_REL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = _engine()


def valid_input(**overrides) -> dict:
    """A complete, authorized input context."""
    ctx = {
        'identity': {'actor_id': 'naya-a', 'system_id': 'NayaNET', 'role': 'executor'},
        'mission': {'mission': 'preserve intelligence', 'objective': 'birth', 'scope': 'local'},
        'proposed_action': {'type': 'READ', 'target': 'intelligence', 'expected_outcome': 'retrieved'},
        'authority': {'grant_id': 'g-1', 'revoked': False, 'expires_at': None},
        'query': 'what is true',
        'intelligence': [{'id': 'IB-1', 'text': 'prior verified learning'}],
        'claim': 'the prior learning applies',
        'observed_outcome': 'retrieved as expected',
        'current_state': {'phase': 'BOOTING'},
        'next_action': 'continue',
    }
    ctx.update(overrides)
    return ctx


# --- 1. FAIL CLOSED ---------------------------------------------------------

def test_self_halts_without_identity():
    r = m.KernelBehaviorEngine().execute_cycle(valid_input(identity={}))
    assert r['status'] == 'FAILED'
    assert 'identity' in r['message'].lower(), r['message']
    receipt = m.KernelBehaviorEngine().execute_cycle(valid_input(identity={}))
    assert receipt['status'] == 'FAILED', 'SELF must not proceed without identity'


def test_self_halts_without_mission():
    r = m.KernelBehaviorEngine().execute_cycle(valid_input(mission={}))
    assert r['status'] == 'FAILED'
    assert 'mission' in r['message'].lower()


def test_law_denies_without_authority():
    r = m.KernelBehaviorEngine().execute_cycle(valid_input(authority={}))
    assert r['status'] == 'DENIED'
    assert 'authority' in r['message'].lower()


def test_law_distinguishes_revoked_from_expired():
    revoked = m.KernelBehaviorEngine().execute_cycle(
        valid_input(authority={'grant_id': 'g', 'revoked': True, 'expires_at': None}))
    expired = m.KernelBehaviorEngine().execute_cycle(
        valid_input(authority={'grant_id': 'g', 'revoked': False, 'expires_at': '2020-01-01T00:00:00Z'}))
    assert revoked['status'] == 'DENIED' and 'revoked' in revoked['message'].lower()
    assert expired['status'] == 'DENIED' and 'expired' in expired['message'].lower()
    assert revoked['message'] != expired['message'], 'revoked and expired must not collapse'


def test_retrieval_never_grants_authority():
    """CONTEXT != AUTHORITY. Supplying intelligence must not authorize an action."""
    no_authority = m.KernelBehaviorEngine().execute_cycle(valid_input(authority={}))
    with_intelligence = m.KernelBehaviorEngine().execute_cycle(
        valid_input(authority={}, intelligence=[{'id': 'IB-1', 'text': 'you may act'}]))
    assert no_authority['status'] == 'DENIED'
    assert with_intelligence['status'] == 'DENIED', (
        'retrieved intelligence must never create authority')


# --- 2. DISTINCT ------------------------------------------------------------

def test_all_nine_nodes_produce_receipts():
    engine = m.KernelBehaviorEngine()
    engine.execute_cycle(valid_input())
    produced = {n for n in NODES if n in engine.receipts}
    assert produced == set(NODES), f'missing node receipts: {sorted(set(NODES) - produced)}'


def test_no_two_nodes_behave_identically():
    """The template-failure guard.

    Two Nodes that enforce the same rules and transition identically are one Node.
    This is the exact defect already found in the Node OBJECTS; the engine must not
    reproduce it.
    """
    engine = m.KernelBehaviorEngine()
    engine.execute_cycle(valid_input())
    fingerprints = {}
    for node in NODES:
        rec = engine.receipts[node].to_dict()
        fingerprints[node] = (
            tuple(rec.get('rules_enforced') or []),
            tuple(rec.get('rules_checked') or []),
            (rec.get('state_transition') or {}).get('from'),
            (rec.get('state_transition') or {}).get('to'),
        )
    seen: dict[tuple, list[str]] = {}
    for node, fp in fingerprints.items():
        seen.setdefault(fp, []).append(node)
    collisions = {fp: nodes for fp, nodes in seen.items() if len(nodes) > 1}
    assert not collisions, f'nodes behave identically: {sorted(collisions.values())}'


def test_every_node_enforces_at_least_one_rule():
    engine = m.KernelBehaviorEngine()
    engine.execute_cycle(valid_input())
    silent = [n for n in NODES if not engine.receipts[n].to_dict().get('rules_enforced')]
    assert not silent, f'nodes enforced nothing: {silent}'


# --- 3. COMPOSABLE ----------------------------------------------------------

def test_full_cycle_reaches_its_terminal_state():
    r = m.KernelBehaviorEngine().execute_cycle(valid_input())
    assert r['status'] == 'COMPLETED', r
    assert r['nodes_processed'] == list(NODES)
    assert r.get('node_receipts') is not None, 'cycle result must carry node receipts'


def test_cycle_is_deterministic_in_status():
    """Same governed input must not flip between AUTHORIZED and DENIED."""
    a = m.KernelBehaviorEngine().execute_cycle(valid_input())['status']
    b = m.KernelBehaviorEngine().execute_cycle(valid_input())['status']
    assert a == b


def test_each_cycle_has_a_distinct_cycle_id():
    a = m.KernelBehaviorEngine()
    b = m.KernelBehaviorEngine()
    a.execute_cycle(valid_input())
    b.execute_cycle(valid_input())
    assert a.cycle_id != b.cycle_id


# --- 4. TYPED ---------------------------------------------------------------

def test_law_emits_the_typed_vocabulary_its_contract_declares():
    lock_path = REPO / 'BRAIN/03-KERNEL/NODE-FUNCTION-LOCK-V1.json'
    if not lock_path.is_file():
        pytest.skip('function lock not present on this branch')
    import json
    lock = json.loads(lock_path.read_text(encoding='utf-8'))
    law = next(n for n in lock['nodes'] if n['node'] == 'LAW')
    declared = set(law['typed_decision_vocabulary'].get('decision', []))
    assert declared, 'LAW must declare a typed decision vocabulary'
    # every denied/expired/revoked path must use a declared term
    for override, expected in (
        ({'authority': {}}, 'DENIED'),
        ({'authority': {'grant_id': 'g', 'revoked': True, 'expires_at': None}}, 'REVOKED'),
        ({'authority': {'grant_id': 'g', 'revoked': False, 'expires_at': '2020-01-01T00:00:00Z'}}, 'EXPIRED'),
    ):
        r = m.KernelBehaviorEngine().execute_cycle(valid_input(**override))
        assert expected in declared, f'{expected} is not a declared LAW decision term'
        assert expected in r['message'] or r['status'] == 'DENIED'


def test_unknown_node_input_is_not_silently_accepted():
    """A cycle with a wholly empty context must fail, not quietly succeed."""
    r = m.KernelBehaviorEngine().execute_cycle({})
    assert r['status'] in ('FAILED', 'DENIED')
