#!/usr/bin/env python3
"""Adversarial tests for UD-13 exactly-once guard.

Every test uses a counting fake for the external world: the fake counts
real external effects. The guard passes only if the effect count is exactly
what a correct exactly-once system would produce.
"""
import os
import shutil
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exactly_once import (
    ActionKey, Ledger, ProviderContract, ExactlyOnceGuard,
    PreEffectError, AmbiguousError,
    DuplicateIntentError, FencedError, LawRefusedError,
    UnqualifiedProviderError, UnresolvedOutcomeError,
    COMPLETED, IN_FLIGHT, UNRESOLVED_EXTERNAL_OUTCOME,
    QUALIFIED_IN_SCOPE, UNPROVEN, FAILED,
)


# ----------------------------------------------------------------------------
# Fakes for the external world
# ----------------------------------------------------------------------------
class CountingWorld:
    """Non-idempotent provider: EVERY call is a real external effect."""

    def __init__(self):
        self.effects = 0
        self.calls = []

    def fire(self, key_id):
        self.effects += 1
        self.calls.append(key_id)
        return {"receipt": "rcpt-%d" % self.effects, "key": key_id}


class IdempotentWorld:
    """Qualified provider: honors the client key, dedupes repeats."""

    def __init__(self):
        self.effects = 0
        self.seen = {}

    def fire(self, key_id):
        if key_id in self.seen:
            return self.seen[key_id]  # no new external effect
        self.effects += 1
        r = {"receipt": "rcpt-%d" % self.effects, "key": key_id}
        self.seen[key_id] = r
        return r


def qualified_contract():
    return ProviderContract(
        "api.example.com", verdict=QUALIFIED_IN_SCOPE,
        idempotency_key_supported=True, retention_horizon_s=3600,
        concurrency_model="concurrent-safe", downstream_effects_covered=True,
        query_path_available=True)


def unproven_contract():
    return ProviderContract("api.example.com", verdict=UNPROVEN)


# ----------------------------------------------------------------------------
class TestExactlyOnce(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ud13-")
        self.ledger = Ledger(os.path.join(self.tmp, "ledger.json"))
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def key(self, intent="post comment X to issue 2175", key=None):
        self.n += 1
        return ActionKey("test-ns", intent, key or ("k%d" % self.n))

    def guard(self, contracts=None):
        return ExactlyOnceGuard(
            self.ledger,
            contracts if contracts is not None
            else {"api.example.com": qualified_contract()})

    # -- positive ------------------------------------------------------
    def test_first_execution_runs_and_records(self):
        w = CountingWorld()
        g = self.guard()
        k = self.key()
        r = g.execute(k, lambda: w.fire(k.durable_id), "api.example.com")
        self.assertEqual(w.effects, 1)
        self.assertEqual(r["receipt"], "rcpt-1")
        rec = self.ledger.get(k.durable_id)
        self.assertEqual(rec["status"], COMPLETED)

    def test_retry_same_key_returns_cached_receipt(self):
        """The core guarantee: a repeat never re-executes."""
        w = CountingWorld()
        g = self.guard()
        k = self.key()
        calls = []
        def fn():
            calls.append(1)
            return w.fire(k.durable_id)
        r1 = g.execute(k, fn, "api.example.com")
        r2 = g.execute(k, fn, "api.example.com")
        self.assertEqual(r1, r2)
        self.assertEqual(len(calls), 1, "fn must run exactly once")
        self.assertEqual(w.effects, 1, "external effect must happen once")

    def test_ledger_survives_restart(self):
        w = CountingWorld()
        k = self.key()
        g1 = self.guard()
        r1 = g1.execute(k, lambda: w.fire(k.durable_id), "api.example.com")
        # brand-new guard + ledger object, same durable file (a restart)
        ledger2 = Ledger(os.path.join(self.tmp, "ledger.json"))
        g2 = ExactlyOnceGuard(ledger2, {"api.example.com": qualified_contract()})
        r2 = g2.execute(k, lambda: w.fire(k.durable_id), "api.example.com")
        self.assertEqual(r1, r2)
        self.assertEqual(w.effects, 1)

    # -- concurrency ---------------------------------------------------
    def test_concurrent_same_key_single_effect(self):
        w = CountingWorld()
        g = self.guard()
        k = self.key()
        barrier = threading.Barrier(8)
        results, errors = [], []

        def worker():
            barrier.wait()
            try:
                results.append(g.execute(
                    k, lambda: w.fire(k.durable_id), "api.example.com"))
            except Exception as e:  # FencedError is acceptable for losers
                errors.append(e)

        ts = [threading.Thread(target=worker) for _ in range(8)]
        [t.start() for t in ts]
        [t.join() for t in ts]
        self.assertEqual(w.effects, 1,
                         "8 racing threads, one external effect, got %d"
                         % w.effects)
        self.assertTrue(results, "at least one thread got the receipt")

    def test_concurrent_diff_key_same_intent(self):
        """Two keys, one intent racing: exactly one effect; the loser is
        fenced while racing, flagged duplicate once the winner completes."""
        w = CountingWorld()
        g = self.guard()
        k1 = self.key(key="kA")
        k2 = self.key(key="kB")  # same intent, different key
        barrier = threading.Barrier(2)
        outcomes = []

        def worker(k):
            barrier.wait()
            try:
                g.execute(k, lambda: w.fire(k.durable_id), "api.example.com")
                outcomes.append("ran")
            except (FencedError, DuplicateIntentError) as e:
                outcomes.append(type(e).__name__)

        ts = [threading.Thread(target=worker, args=(k,)) for k in (k1, k2)]
        [t.start() for t in ts]
        [t.join() for t in ts]
        self.assertEqual(w.effects, 1)
        self.assertIn("ran", outcomes)
        # now the loser retries after completion -> duplicate intent flagged
        for k in (k1, k2):
            try:
                g.execute(k, lambda: w.fire(k.durable_id), "api.example.com")
            except DuplicateIntentError:
                outcomes.append("DuplicateIntentError")
        self.assertIn("DuplicateIntentError", outcomes)

    # -- crash / ambiguity ----------------------------------------------
    def test_crash_mid_action_reconciles_no_double_fire(self):
        """Effect applied, then crash before receipt recorded. Reconcile
        finds it; the retry adopts instead of re-firing."""
        w = CountingWorld()
        g = self.guard()
        k = self.key()
        state = {"fired": False}

        def fn():
            if not state["fired"]:
                state["fired"] = True
                w.fire(k.durable_id)
                raise AmbiguousError("crashed after send, receipt lost")
            raise AssertionError("must not re-execute after reconcile")

        def reconcile(akey):
            return {"receipt": "rcpt-1", "key": k.durable_id}  # provider shows it

        r = g.execute(k, fn, "api.example.com", reconcile_fn=reconcile)
        self.assertEqual(r["receipt"], "rcpt-1")
        self.assertEqual(w.effects, 1, "reconcile must not double-fire")

    def test_pre_effect_failure_retries_safely(self):
        """Failure BEFORE any effect: same-key retry is provably safe."""
        w = CountingWorld()
        g = self.guard()
        k = self.key()
        calls = []

        def fn():
            calls.append(1)
            if len(calls) == 1:
                raise PreEffectError("connection refused before send")
            return w.fire(k.durable_id)

        r = g.execute(k, fn, "api.example.com")
        self.assertEqual(r["receipt"], "rcpt-1")
        self.assertEqual(w.effects, 1)

    def test_ambiguous_unqualified_provider_holds(self):
        """No reconcile path + unproven provider: HOLD, never blind retry."""
        w = CountingWorld()
        g = self.guard(contracts={"api.example.com": unproven_contract()})
        k = self.key()

        def fn():
            w.fire(k.durable_id)
            raise AmbiguousError("timeout; effect may have happened")

        with self.assertRaises((UnqualifiedProviderError,
                                UnresolvedOutcomeError)):
            g.execute(k, fn, "api.example.com")
        self.assertEqual(w.effects, 1, "must not blind-retry")
        rec = self.ledger.get(k.durable_id)
        self.assertEqual(rec["status"], UNRESOLVED_EXTERNAL_OUTCOME)

    def test_ambiguous_qualified_provider_single_effect(self):
        """Qualified idempotent provider: retry is safe, provider dedupes."""
        w = IdempotentWorld()
        g = self.guard()  # qualified contract
        k = self.key()
        calls = []

        def fn():
            calls.append(1)
            r = w.fire(k.durable_id)
            if len(calls) == 1:
                raise AmbiguousError("timeout after send")
            return r

        r = g.execute(k, fn, "api.example.com")
        self.assertEqual(w.effects, 1, "idempotent retry: one effect")
        self.assertEqual(r["receipt"], "rcpt-1")

    def test_retry_budget_exhausted_holds(self):
        w = IdempotentWorld()
        g = self.guard()
        k = self.key()

        def fn():
            w.fire(k.durable_id)
            raise AmbiguousError("always ambiguous")

        with self.assertRaises(UnresolvedOutcomeError):
            g.execute(k, fn, "api.example.com")  # no reconcile_fn
        self.assertEqual(w.effects, 1)
        rec = self.ledger.get(k.durable_id)
        self.assertEqual(rec["status"], UNRESOLVED_EXTERNAL_OUTCOME)

    def test_twin_worlds_both_hold(self):
        """Acceptance-gate fixture: the SAME incomplete evidence
        (ambiguous, no reconcile, unqualified) must produce HOLD in both
        worlds — whether the effect happened or not. Never blind retry."""
        for effect_happened in (True, False):
            with self.subTest(effect_happened=effect_happened):
                tmp = tempfile.mkdtemp(prefix="ud13-twin-")
                try:
                    ledger = Ledger(os.path.join(tmp, "ledger.json"))
                    g = ExactlyOnceGuard(
                        ledger, {"api.example.com": unproven_contract()})
                    w = CountingWorld()
                    k = ActionKey("twin", "same-intent", "same-key")

                    def fn():
                        if effect_happened:
                            w.fire(k.durable_id)
                        raise AmbiguousError("evidence incomplete")

                    with self.assertRaises((UnqualifiedProviderError,
                                            UnresolvedOutcomeError)):
                        g.execute(k, fn, "api.example.com")
                    rec = ledger.get(k.durable_id)
                    self.assertEqual(rec["status"],
                                     UNRESOLVED_EXTERNAL_OUTCOME)
                    self.assertEqual(w.effects, 1 if effect_happened else 0)
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)

    # -- guards ----------------------------------------------------------
    def test_different_key_same_intent_flagged(self):
        w = CountingWorld()
        g = self.guard()
        k1 = self.key(key="first")
        k2 = self.key(key="second")  # same intent string
        g.execute(k1, lambda: w.fire(k1.durable_id), "api.example.com")
        with self.assertRaises(DuplicateIntentError):
            g.execute(k2, lambda: w.fire(k2.durable_id), "api.example.com")
        self.assertEqual(w.effects, 1)

    def test_inflight_fence_holds_second_worker(self):
        g = self.guard()
        k = self.key()
        # simulate a crashed worker that left the key fenced+in-flight
        self.ledger.put(k.durable_id, {
            "status": IN_FLIGHT, "receipt": None,
            "intent_hash": k.intent_hash, "namespace": "test-ns",
            "attempts": 0, "history": []})
        with self.assertRaises(FencedError):
            g.execute(k, lambda: {"receipt": "x"}, "api.example.com")

    def test_law_refused(self):
        w = CountingWorld()
        g = self.guard()
        k = self.key()
        with self.assertRaises(LawRefusedError):
            g.execute(k, lambda: w.fire(k.durable_id), "api.example.com",
                      law_valid=False)
        self.assertEqual(w.effects, 0)

    def test_failed_provider_blocks_first_execution(self):
        w = CountingWorld()
        g = self.guard(contracts={"api.example.com": ProviderContract(
            "api.example.com", verdict=FAILED)})
        with self.assertRaises(UnqualifiedProviderError):
            g.execute(self.key(), lambda: w.fire("x"), "api.example.com")
        self.assertEqual(w.effects, 0)

    def test_action_key_requires_all_parts(self):
        with self.assertRaises(ValueError):
            ActionKey("", "intent", "k")
        with self.assertRaises(ValueError):
            ActionKey("ns", "", "k")

    def test_unknown_exception_treated_as_ambiguous(self):
        """An unexpected failure mode fails closed (reconcile-or-hold)."""
        w = CountingWorld()
        g = self.guard(contracts={"api.example.com": unproven_contract()})
        k = self.key()

        def fn():
            w.fire(k.durable_id)
            raise RuntimeError("weird new failure mode")

        with self.assertRaises((UnqualifiedProviderError,
                                UnresolvedOutcomeError)):
            g.execute(k, fn, "api.example.com")
        self.assertEqual(w.effects, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
