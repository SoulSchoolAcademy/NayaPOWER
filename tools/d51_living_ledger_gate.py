"""D51 living-ledger contract gate - Naya 2 WIRE LANE, 2026-10-11.

Wires the D51 first-slice mechanism (living_ledger/receipt.py +
living_ledger/chain.py, PR #2333) onto the CI governance path: every PR
that touches the living_ledger package must preserve the mechanism's own
contract - fail-closed receipt construction and hash-chain verification.

A mechanism that silently accepts an invalid receipt, or a verifier that
lets a broken chain pass, BLOCKS the PR (exit 1). A missing or
unimportable mechanism, or a corrupt harness, fails closed (exit 2) -
never a silent pass. Mechanism absent from the tree (pre-merge) is
explicit DORMANT (exit 0 with a witness line), never a false green.

Exit codes: 0 = PASS or DORMANT. 1 = contract violation (blocks the PR).
2 = harness/loader failure (fail-closed).

Boundary: CI governance path only. This gate judges the mechanism's
contract; it authorizes nothing. Database writes stay behind the
human-only gate per the mechanism's own docstring.
"""

from __future__ import annotations

import importlib.util
import os
import sys

MECHANISM_FILES = ("living_ledger/receipt.py", "living_ledger/chain.py")
REQUIRED_RECEIPT_ATTRS = ("LivingReceipt",)
REQUIRED_CHAIN_ATTRS = ("verify_chain", "canonical_event_hash")

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_FAIL_CLOSED = 2

_TS = "2026-10-11T11:00:00Z"
_EVIDENCE = ("pr:2333", "run:20261011-1112")
_PRIVACY = {"self": "PRIVATE", "team": "SHARED",
            "collective": "COLLECTIVE", "public": "PUBLIC"}


class GateError(Exception):
    """Harness or loader failure - always fail closed, never silent."""


def _repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_module(module_name, path):
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
    except (OSError, ValueError) as exc:
        raise GateError("cannot locate module %s at %s: %s"
                        % (module_name, path, exc))
    if spec is None or spec.loader is None:
        raise GateError("no import spec for %s at %s" % (module_name, path))
    module = importlib.util.module_from_spec(spec)
    # Register under the synthetic name BEFORE exec: dataclasses (and any
    # module doing sys.modules[__name__] lookups at class-creation time)
    # require the entry to exist during exec_module.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001 - any import failure is fail-closed
        sys.modules.pop(module_name, None)
        raise GateError("mechanism unimportable (%s): %s: %s"
                        % (path, type(exc).__name__, exc))
    return module


def load_mechanism(root):
    """Return (receipt_mod, chain_mod), None when absent, else raise GateError."""
    paths = [os.path.join(root, name) for name in MECHANISM_FILES]
    if not all(os.path.isfile(p) for p in paths):
        return None
    receipt = _load_module("d51_gate_receipt", paths[0])
    chain = _load_module("d51_gate_chain", paths[1])
    for attr in REQUIRED_RECEIPT_ATTRS:
        if not hasattr(receipt, attr):
            raise GateError("contract surface broken: living_ledger/receipt.py "
                            "lacks %s" % attr)
    for attr in REQUIRED_CHAIN_ATTRS:
        if not hasattr(chain, attr):
            raise GateError("contract surface broken: living_ledger/chain.py "
                            "lacks %s" % attr)
    return receipt, chain


class _Battery:
    def __init__(self):
        self.failures = []
        self.passed = 0

    def check(self, name, cond, detail=""):
        if cond:
            self.passed += 1
        else:
            self.failures.append("%s - %s" % (name, detail or "condition false"))

    def expect_raises(self, name, fn):
        try:
            fn()
        except ValueError:
            self.passed += 1
            return
        except Exception as exc:  # noqa: BLE001 - reported, then fail-closed upstream
            self.failures.append("%s - raised %s instead of ValueError: %s"
                                 % (name, type(exc).__name__, exc))
            return
        self.failures.append("%s - no ValueError raised (invalid input accepted)"
                             % name)


def _good_receipt(receipt_mod, **kw):
    args = {"actor": "naya2/wire-lane",
            "action": "wired D51 living-ledger gate",
            "evidence": _EVIDENCE,
            "timestamp": _TS,
            "scope": "team"}
    args.update(kw)
    return receipt_mod.LivingReceipt(**args)


def _check_receipt_contract(receipt_mod):
    bat = _Battery()
    r1 = _good_receipt(receipt_mod)
    r2 = _good_receipt(receipt_mod)
    bat.check("receipt constructs", True)
    bat.check("receipt_id deterministic", r1.receipt_id == r2.receipt_id,
              "same envelope gave different ids")
    r3 = _good_receipt(receipt_mod, action="a different action")
    bat.check("receipt_id discriminates", r1.receipt_id != r3.receipt_id,
              "different envelopes gave the same id")
    for scope, privacy in _PRIVACY.items():
        r = _good_receipt(receipt_mod, scope=scope)
        bat.check("scope %s -> %s" % (scope, privacy),
                  r.privacy_classification == privacy,
                  "got %r" % (r.privacy_classification,))
    params = r1.to_ledger_params("owner-1")
    bat.check("to_ledger_params source_table", params["p_source_table"] == "living_ledger",
              "got %r" % (params.get("p_source_table"),))
    bat.check("to_ledger_params source_id == receipt_id",
              params["p_source_id"] == r1.receipt_id, "mismatch")
    bat.check("to_ledger_params status RECORDED", params["p_status"] == "RECORDED",
              "got %r" % (params.get("p_status"),))
    bat.check("to_ledger_params owner passthrough", params["p_owner_id"] == "owner-1",
              "got %r" % (params.get("p_owner_id"),))
    bat.check("to_ledger_params evidence carried",
              list(params["p_evidence_refs"]) == list(_EVIDENCE), "evidence lost")

    bad = [
        ("empty actor", {"actor": ""}),
        ("blank actor", {"actor": "   "}),
        ("empty action", {"action": ""}),
        ("empty evidence tuple", {"evidence": ()}),
        ("empty evidence list", {"evidence": []}),
        ("blank evidence item", {"evidence": ("  ",)}),
        ("non-tuple evidence", {"evidence": "pr:2333"}),
        ("empty timestamp", {"timestamp": ""}),
        ("non-ISO timestamp", {"timestamp": "not-a-date"}),
        ("impossible timestamp", {"timestamp": "2026-13-99T99:99:99Z"}),
        ("empty scope", {"scope": ""}),
        ("unknown scope", {"scope": "galaxy"}),
        ("non-dict metadata", {"metadata": "x"}),
    ]
    for name, kw in bad:
        bat.expect_raises("reject " + name,
                          lambda kw=kw: _good_receipt(receipt_mod, **kw))
    return bat


def _event_from_params(chain_mod, params, previous_chain_hash, chain_seq,
                       parent=None):
    event = {
        "owner_id": params["p_owner_id"],
        "event_type": params["p_event_type"],
        "event_at": params["p_event_at"],
        "source_table": params["p_source_table"],
        "source_id": params["p_source_id"],
        "parent_ledger_event_id": parent,
        "previous_chain_hash": previous_chain_hash,
        "evidence_refs": params["p_evidence_refs"],
        "metadata": params["p_metadata"],
        "chain_seq": chain_seq,
    }
    event["event_hash"] = chain_mod.canonical_event_hash(event)
    return event


def _build_chain(receipt_mod, chain_mod, n=3):
    events = []
    prev = ""
    for i in range(n):
        r = _good_receipt(receipt_mod, action="wired D51 gate event %d" % i)
        params = r.to_ledger_params("owner-1")
        events.append(_event_from_params(chain_mod, params, prev, i + 1))
        prev = events[-1]["event_hash"]
    return events


def _check_chain_contract(receipt_mod, chain_mod):
    bat = _Battery()
    events = _build_chain(receipt_mod, chain_mod)
    verdict = chain_mod.verify_chain(events)
    bat.check("valid 3-event chain -> CHAIN_VALID",
              verdict.verdict == "CHAIN_VALID" and verdict.ok,
              "got %r (%s)" % (verdict.verdict, verdict.detail))
    bat.check("chain links carry receipt ids",
              all(e["source_id"] for e in events), "empty source_id")

    tampered = [dict(e) for e in events]
    tampered[1]["event_hash"] = "0" * 64
    v = chain_mod.verify_chain(tampered)
    bat.check("forged event_hash -> HASH_MISMATCH @1",
              v.verdict == "HASH_MISMATCH" and v.index == 1 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))

    broken = [dict(e) for e in events]
    broken[2]["previous_chain_hash"] = "deadbeef" * 8
    # Re-hash AFTER planting the wrong link: recompute must pass so the
    # LINK check itself is what fires (a post-hoc mutation is instead
    # caught earlier as HASH_MISMATCH - also loud, tested below).
    broken[2]["event_hash"] = chain_mod.canonical_event_hash(broken[2])
    v = chain_mod.verify_chain(broken)
    bat.check("wrong previous_chain_hash -> LINK_BROKEN @2",
              v.verdict == "LINK_BROKEN" and v.index == 2 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))

    mutated_link = [dict(e) for e in events]
    mutated_link[2]["previous_chain_hash"] = "deadbeef" * 8
    v = chain_mod.verify_chain(mutated_link)
    bat.check("post-hoc link mutation -> HASH_MISMATCH @2 (tamper-evident)",
              v.verdict == "HASH_MISMATCH" and v.index == 2 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))

    dropped = [dict(events[0]), dict(events[2])]
    v = chain_mod.verify_chain(dropped)
    bat.check("dropped event (0 -> 2) -> LINK_BROKEN @1",
              v.verdict == "LINK_BROKEN" and v.index == 1 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))

    regressed = [dict(e) for e in events]
    regressed[2]["chain_seq"] = regressed[1]["chain_seq"]
    v = chain_mod.verify_chain(regressed)
    bat.check("non-increasing chain_seq -> SEQ_REGRESSION @2",
              v.verdict == "SEQ_REGRESSION" and v.index == 2 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))

    v = chain_mod.verify_chain([])
    bat.check("empty event list -> EMPTY_CHAIN (not a pass)",
              v.verdict == "EMPTY_CHAIN" and not v.ok,
              "got %r" % (v.verdict,))

    missing = [dict(e) for e in events]
    del missing[1]["event_hash"]
    v = chain_mod.verify_chain(missing)
    bat.check("missing event_hash -> HASH_MISMATCH @1",
              v.verdict == "HASH_MISMATCH" and v.index == 1 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))

    bad_genesis = [dict(e) for e in events]
    bad_genesis[0]["previous_chain_hash"] = "should-not-be-here"
    bad_genesis[0]["event_hash"] = chain_mod.canonical_event_hash(bad_genesis[0])
    v = chain_mod.verify_chain(bad_genesis)
    bat.check("genesis with predecessor -> LINK_BROKEN @0",
              v.verdict == "LINK_BROKEN" and v.index == 0 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))

    reordered = [dict(events[0]), dict(events[2]), dict(events[1])]
    v = chain_mod.verify_chain(reordered)
    bat.check("reordered events -> LINK_BROKEN @1, never a silent pass",
              v.verdict == "LINK_BROKEN" and v.index == 1 and not v.ok,
              "got %r @%d" % (v.verdict, v.index))
    return bat


def run_gate(root=None):
    """Run the gate. Returns (exit_code, report_lines)."""
    root = root or os.environ.get("D51_LIVING_LEDGER_ROOT") or _repo_root()
    report = []
    try:
        loaded = load_mechanism(root)
    except GateError as exc:
        report.append("D51-GATE FAIL-CLOSED - %s" % exc)
        return EXIT_FAIL_CLOSED, report
    if loaded is None:
        report.append("D51-GATE DORMANT - living_ledger mechanism not present "
                      "on this tree; nothing to judge")
        return EXIT_PASS, report
    receipt_mod, chain_mod = loaded
    try:
        bat_r = _check_receipt_contract(receipt_mod)
        bat_c = _check_chain_contract(receipt_mod, chain_mod)
    except Exception as exc:  # noqa: BLE001 - a crashed battery proves nothing
        report.append("D51-GATE FAIL-CLOSED - contract battery crashed: %s: %s"
                      % (type(exc).__name__, exc))
        return EXIT_FAIL_CLOSED, report
    failures = bat_r.failures + bat_c.failures
    passed = bat_r.passed + bat_c.passed
    if failures:
        report.append("D51-GATE VIOLATION - %d contract break(s), %d check(s) "
                      "held:" % (len(failures), passed))
        report.extend("  - " + f for f in failures)
        return EXIT_VIOLATION, report
    report.append("D51-GATE PASS - receipt contract + chain integrity hold on "
                  "the live tree (%d checks)" % passed)
    return EXIT_PASS, report


def main(argv):
    root = argv[1] if len(argv) > 1 else None
    code, report = run_gate(root)
    for line in report:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
