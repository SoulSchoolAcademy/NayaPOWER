"""Demo-1 P3 RED: close the missing-envelope bypass; bind invocation to the live grant.

Priority 1 — the coordinator reproduced this: remove law_envelope, recompute
the decision receipt's hash, provide no grants, and the registered staging
tool still reaches the executor. The real demo path constructs ActNode with
require_law_envelope=True; a stripped or absent envelope must refuse with
zero executor invocations. The fixture path (no envelope) remains available
only to explicitly constructed test harnesses — never to the demo.

Priority 2 — the invocation binds to the resolved grant, principal, allowed
action, target, and bounds: the intersection of canonical capability limits,
the current grant, the LAW envelope, and the execution request. The envelope
may narrow a grant; it cannot widen one. Revocation and expiry resolve at
the invocation boundary against the node's own clock with typed,
timezone-aware comparisons — caller-supplied timestamps and cached grant
snapshots never substitute.

Every refusal test uses an executor spy and asserts ZERO invocations.
"""

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "demo1"))

from naya_kernel import smart_door
from naya_kernel.nodes import act_node
from naya_kernel.nodes.act_node import ActNode, GateVerdict

import law_authorize

REPO_ROOT = Path(__file__).resolve().parents[2]

NOW = "2026-10-01T12:00:00+00:00"
FILENAME = "sn-candidate-invocation-binding.md"
CONTENT = "# invocation binding probe\n\n" + ("bounded effect line\n" * 40)

TOOL_ID = "staging.write_file"


@pytest.fixture(scope="module")
def authz():
    """One genuine LAW authorization; every test mutates only its own copies."""
    return law_authorize.authorize(FILENAME, CONTENT.encode("utf-8"))


@pytest.fixture()
def registry():
    return smart_door.staging_tool_registry()


def _spy():
    calls = []

    def executor(tool_id, params):
        calls.append((tool_id, params))
        return {"status": "ok", "effects": "spy-effect"}

    return calls, executor


def _demo_node(executor):
    """The demo's construction: envelope required, fixed clock for determinism."""
    return ActNode(executor=executor, require_law_envelope=True,
                   clock=lambda: NOW)


def _receipt(authz, **overrides):
    body = {
        "receipt_id": "dec-binding-test-001",
        "issued_at": NOW,
        "valid_until": authz["grant"]["expiry"],
        "winner": {"tool_id": TOOL_ID, "version": "1.0",
                   "params": {"filename": FILENAME, "content": CONTENT}},
        "authority_basis": dict(authz["authority_basis"]),
        "law_envelope": copy.deepcopy(authz["envelope"]),
    }
    body.update(overrides)
    receipt = act_node.make_decision_receipt(**body)
    return receipt


def _reseal(receipt):
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    receipt["receipt_hash"] = act_node._sha256(body)
    return receipt


def _execute(node, receipt, registry, grants):
    return node.execute({
        "decision_receipt": receipt,
        "tool_registry": registry,
        "grants": grants,
        "execution_ledger": {},
        "now": NOW,
    })


# ---------------------------------------------------------------------------
# Priority 1: the missing-envelope bypass
# ---------------------------------------------------------------------------

class TestMissingEnvelopeBypass:
    def test_stripped_envelope_recomputed_hash_no_grants_refused(self, authz, registry):
        """The coordinator's exact repro: strip envelope, reseal, no grants."""
        calls, executor = _spy()
        node = _demo_node(executor)
        receipt = _receipt(authz)
        del receipt["law_envelope"]
        _reseal(receipt)  # hash proves bytes; it does not prove authorization
        handoff = _execute(node, receipt, registry, grants=[])
        assert handoff["path"] != "EXECUTED", handoff
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_absent_envelope_with_grants_still_refused(self, authz, registry):
        """Grants present but no envelope: still refused on the demo path."""
        calls, executor = _spy()
        node = _demo_node(executor)
        receipt = _receipt(authz)
        del receipt["law_envelope"]
        _reseal(receipt)
        handoff = _execute(node, receipt, registry, grants=[authz["grant"]])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_honest_envelope_path_still_executes(self, authz, registry):
        """Positive control: genuine envelope + live grant executes exactly once."""
        calls, executor = _spy()
        node = _demo_node(executor)
        handoff = _execute(node, _receipt(authz), registry, [authz["grant"]])
        assert handoff["path"] == "EXECUTED", handoff
        assert len(calls) == 1, calls

    def test_fixture_path_needs_explicit_construction(self, authz, registry):
        """The fixture path (no envelope) survives only for explicitly
        constructed test harnesses — the demo never uses this construction."""
        calls, executor = _spy()
        node = ActNode(executor=executor)  # no require_law_envelope: test mode
        receipt = _receipt(authz)
        del receipt["law_envelope"]
        _reseal(receipt)
        handoff = _execute(node, receipt, registry, grants=[])
        assert handoff["path"] == "EXECUTED", handoff
        assert len(calls) == 1


# ---------------------------------------------------------------------------
# Priority 2: grant-bound enforcement at the invocation boundary
# ---------------------------------------------------------------------------

class TestGrantBoundEnforcement:
    def test_narrowed_grant_max_bytes_refuses(self, authz, registry):
        """Grant narrowed to 1 byte after LAW admission: the 1 KiB request
        exceeds the intersection — refuse, zero invocations."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        grant["bounds"]["max_bytes"] = 1
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_changed_grantee_refuses(self, authz, registry):
        """Grant's grantee swapped after LAW admission: the principal LAW
        authorized (in the envelope's authority_basis) no longer matches."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        grant["grantee"] = "mallory"
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_revoked_between_law_and_act_refuses(self, authz, registry):
        """Revocation resolves at the invocation boundary, not from LAW's memory."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        grant["revoked"] = True
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_expired_grant_refuses(self, authz, registry):
        """Expiry resolves against the node's own clock — typed, tz-aware."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        grant["expiry"] = "2026-09-01T00:00:00+00:00"
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_malformed_expiry_fails_closed(self, authz, registry):
        """An unparseable expiry is not 'no expiry' — fail closed."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        grant["expiry"] = "not-a-time"
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_missing_mandatory_bound_fails_closed(self, authz, registry):
        """A missing max_bytes on the grant is not unlimited — fail closed."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        del grant["bounds"]["max_bytes"]
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_narrowed_filename_pattern_refuses(self, authz, registry):
        """Grant pattern tightened after LAW: the request matches the
        envelope's pattern but not the grant's — the intersection refuses."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        grant["bounds"]["filename"] = "sn-candidate-tight-*.md"
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "REFUSED", handoff
        assert calls == [], "executor must see zero invocations"

    def test_widened_grant_cannot_widen_envelope(self, authz, registry):
        """Widening the grant after LAW does not widen the envelope:
        the honest 1 KiB request still executes under the envelope's bound."""
        calls, executor = _spy()
        node = _demo_node(executor)
        grant = copy.deepcopy(authz["grant"])
        grant["bounds"]["max_bytes"] = 999999999
        handoff = _execute(node, _receipt(authz), registry, [grant])
        assert handoff["path"] == "EXECUTED", handoff
        assert len(calls) == 1
