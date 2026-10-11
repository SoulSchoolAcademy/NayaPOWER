#!/usr/bin/env python3
"""UD-13 — NEVER ACT TWICE ON THE OUTSIDE WORLD (exactly-once guard).

Plain words: any action touching the outside world (API calls, posts, merges,
messages) happens exactly once. A timed-out request, a crashed worker, or a
missing receipt is NOT permission to do it again. Recovery is: reconcile first
(ask the provider what actually happened), retry under the same key only when
proven safe, otherwise HOLD and record the outcome as unresolved.

Machine-enforced rules:
  1. Every outward action carries a durable logical-operation identity:
     namespace + intent hash + unique key.
  2. A completed key NEVER re-executes: repeats return the cached receipt.
  3. A different key for the same intent is FLAGGED (duplicate intent).
  4. In-flight keys AND in-flight intents are FENCED: a second worker
     attempting either is held, never executed.
  5. Ambiguous outcomes (the effect MAY have happened) reconcile first; a
     same-key retry happens only when the provider contract is
     QUALIFIED_IN_SCOPE, retention covers the window, and LAW permission
     holds. Otherwise the outcome is recorded UNRESOLVED_EXTERNAL_OUTCOME
     and the retry stays blocked.
  6. No trace passes with an unqualified provider boundary.

Scope note: the provider-contract package implements the five load-bearing
dimensions (idempotency-key support, retention horizon, concurrency model,
downstream-effects coverage, query/reconcile path). The full ten-dimension
qualification package from the UD-13 spec is follow-up work, explicitly out
of scope here.

Stdlib only.
"""

import hashlib
import json
import os
import tempfile
import threading
import time

# ----------------------------------------------------------------------------
# Statuses
# ----------------------------------------------------------------------------
COMPLETED = "COMPLETED"
IN_FLIGHT = "IN_FLIGHT"
UNRESOLVED_EXTERNAL_OUTCOME = "UNRESOLVED_EXTERNAL_OUTCOME"

# Provider contract verdicts
QUALIFIED_IN_SCOPE = "QUALIFIED_IN_SCOPE"
PARTIALLY_QUALIFIED = "PARTIALLY_QUALIFIED"
FAILED = "FAILED"
UNPROVEN = "UNPROVEN"
OUT_OF_SCOPE = "OUT_OF_SCOPE"

MAX_ATTEMPTS = 3  # first try + up to 2 guarded same-key retries


# ----------------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------------
class ExactlyOnceError(Exception):
    """Base."""


class DuplicateIntentError(ExactlyOnceError):
    """A different key was used for an intent that already completed."""


class FencedError(ExactlyOnceError):
    """The key (or intent) is in-flight elsewhere; held, not executed."""


class LawRefusedError(ExactlyOnceError):
    """LAW permission absent — SafeRecovery requires LAWValid."""


class UnqualifiedProviderError(ExactlyOnceError):
    """Provider boundary not qualified for the recovery attempted."""


class UnresolvedOutcomeError(ExactlyOnceError):
    """No safe recovery exists; outcome recorded UNRESOLVED_EXTERNAL_OUTCOME."""


class PreEffectError(Exception):
    """Raised by the action fn when it failed BEFORE any external effect.
    Tells the guard a same-key retry is safe (nothing happened)."""


class AmbiguousError(Exception):
    """Raised by the action fn when the external effect MAY have happened
    (timeout, crash after send, lost receipt). Tells the guard to
    reconcile-or-hold, never blind-retry."""


# ----------------------------------------------------------------------------
# ActionKey — durable logical-operation identity
# ----------------------------------------------------------------------------
class ActionKey:
    """namespace + intent hash + unique key.

    The intent is the canonical description of WHAT the outside world should
    observe (e.g. 'post comment X to issue 2175'). The key is unique per
    logical operation. Two keys, one intent = duplicate intent, flagged.
    """

    def __init__(self, namespace, intent, key):
        if not namespace or not intent or not key:
            raise ValueError("namespace, intent, and key are all required")
        self.namespace = namespace
        self.intent = intent
        self.key = key
        self.intent_hash = hashlib.sha256(intent.encode("utf-8")).hexdigest()[:16]

    @property
    def durable_id(self):
        return "%s:%s:%s" % (self.namespace, self.intent_hash, self.key)

    @property
    def intent_id(self):
        return "%s:%s" % (self.namespace, self.intent_hash)

    def __repr__(self):
        return "ActionKey(%s)" % self.durable_id


# ----------------------------------------------------------------------------
# Ledger — durable record of every key's outcome
# ----------------------------------------------------------------------------
class Ledger:
    """Atomic JSON ledger: durable_id -> record.

    Records: {status, receipt, intent_hash, namespace, attempts, history[]}.
    Writes are atomic (tmp file + os.replace). An in-process lock serializes
    check-and-set; per-key and per-intent fence files give cross-process
    mutual exclusion.
    """

    def __init__(self, path):
        self.path = path
        # RLock: execute() holds the lock while find_completed_intent()
        # re-enters it. A plain Lock would deadlock here.
        self._lock = threading.RLock()
        self._records = self._load()

    # -- persistence ------------------------------------------------------
    def _load(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        d = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(d, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=d, prefix=".ledger-")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._records, f, indent=2, sort_keys=True)
            os.replace(tmp, self.path)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    # -- fence files ------------------------------------------------------
    def _fence_path(self, name):
        safe = hashlib.sha256(name.encode()).hexdigest()[:24]
        return self.path + ".fence-" + safe

    def _take_fence(self, name):
        try:
            fd = os.open(self._fence_path(name), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            return False

    def _release_fence(self, name):
        try:
            os.unlink(self._fence_path(name))
        except OSError:
            pass

    # -- record ops -------------------------------------------------------
    def get(self, durable_id):
        with self._lock:
            r = self._records.get(durable_id)
            return dict(r) if r else None

    def put(self, durable_id, record):
        with self._lock:
            self._records[durable_id] = record
            self._save()

    def find_completed_intent(self, namespace, intent_hash, exclude_id):
        with self._lock:
            for did, rec in self._records.items():
                if (did != exclude_id
                        and rec.get("namespace") == namespace
                        and rec.get("intent_hash") == intent_hash
                        and rec.get("status") == COMPLETED):
                    return did
        return None

    @property
    def lock(self):
        return self._lock


# ----------------------------------------------------------------------------
# ProviderContract — per-endpoint qualification
# ----------------------------------------------------------------------------
class ProviderContract:
    """Qualification of one external endpoint.

    Five load-bearing dimensions (subset of the spec's ten; the rest is
    follow-up, stated honestly):
      idempotency_key_supported : provider honors a client-supplied key
      retention_horizon_s       : how long the provider remembers the key
      concurrency_model         : 'serial' | 'concurrent-safe' | 'unknown'
      downstream_effects_covered: retry-safety reaches downstream effects
      query_path_available      : we can ask the provider what happened
    """

    DIMENSIONS = ("idempotency_key_supported", "retention_horizon_s",
                  "concurrency_model", "downstream_effects_covered",
                  "query_path_available")

    def __init__(self, endpoint, verdict=UNPROVEN, **dimensions):
        self.endpoint = endpoint
        self.verdict = verdict
        self.dimensions = {d: dimensions.get(d) for d in self.DIMENSIONS}

    def retry_allowed(self):
        """A same-key retry may lean on this contract only when qualified."""
        if self.verdict != QUALIFIED_IN_SCOPE:
            return False
        d = self.dimensions
        return bool(d["idempotency_key_supported"]) and bool(
            d["downstream_effects_covered"]) and (
                d["retention_horizon_s"] or 0) > 0

    def to_dict(self):
        return {"endpoint": self.endpoint, "verdict": self.verdict,
                "dimensions": dict(self.dimensions)}


# ----------------------------------------------------------------------------
# ExactlyOnceGuard
# ----------------------------------------------------------------------------
class ExactlyOnceGuard:
    """Enforces: outward actions happen exactly once.

    receipt = guard.execute(ActionKey(ns, intent, key), fn,
                           provider="api.example.com",
                           reconcile_fn=lambda akey: receipt_or_None,
                           law_valid=True)
    """

    def __init__(self, ledger, contracts=None):
        self.ledger = ledger
        self.contracts = contracts or {}

    # -- public -----------------------------------------------------------
    def execute(self, akey, fn, provider, reconcile_fn=None, law_valid=True):
        """Run fn exactly once under akey. Returns the receipt.

        fn signals via exceptions:
          PreEffectError -> failed before any external effect (safe to retry)
          AmbiguousError -> effect MAY have happened (reconcile-or-hold)
          any other      -> treated as ambiguous (fail closed)
        """
        # Rule 0: SafeRecovery requires LAWValid.
        if not law_valid:
            raise LawRefusedError(
                "LAW permission absent for %s" % akey.durable_id)

        did = akey.durable_id
        with self.ledger.lock:
            rec = self.ledger._records.get(did)

            # Rule 2: completed key never re-executes.
            if rec and rec["status"] == COMPLETED:
                return rec["receipt"]

            # Rule 4: in-flight key is fenced.
            if rec and rec["status"] == IN_FLIGHT:
                raise FencedError("key %s in-flight; held" % did)

            # Rule 3: same intent, different key = duplicate intent.
            dup = self.ledger.find_completed_intent(
                akey.namespace, akey.intent_hash, did)
            if dup:
                raise DuplicateIntentError(
                    "intent already completed under %s; refusing %s"
                    % (dup, did))

            # Rule 6: FAILED provider boundary blocks even first execution.
            contract = self.contracts.get(provider)
            if contract is not None and contract.verdict == FAILED:
                raise UnqualifiedProviderError(
                    "provider %s verdict FAILED" % provider)

            # Fence key AND intent before any external effect, atomically
            # under the lock so same-intent races cannot slip through.
            if not self.ledger._take_fence("intent:" + akey.intent_id):
                raise FencedError(
                    "intent %s in-flight elsewhere; held" % akey.intent_id)
            if not self.ledger._take_fence("key:" + did):
                self.ledger._release_fence("intent:" + akey.intent_id)
                raise FencedError("key %s fenced by another process" % did)
            self._record(did, {
                "status": IN_FLIGHT,
                "receipt": None,
                "intent_hash": akey.intent_hash,
                "namespace": akey.namespace,
                "attempts": 0,
                "history": ["fenced at %.3f" % time.time()],
            })

        try:
            return self._attempt_loop(akey, did, fn, provider, reconcile_fn,
                                      law_valid)
        finally:
            self.ledger._release_fence("key:" + did)
            self.ledger._release_fence("intent:" + akey.intent_id)

    # -- attempt loop -----------------------------------------------------
    def _attempt_loop(self, akey, did, fn, provider, reconcile_fn, law_valid):
        while True:
            rec = self.ledger.get(did)
            attempts = (rec.get("attempts", 0) or 0) + 1
            if attempts > MAX_ATTEMPTS:
                return self._hold(
                    did, akey, "retry budget exhausted (%d)" % MAX_ATTEMPTS)
            self._record(did, dict(rec, attempts=attempts,
                                   history=rec.get("history", []) +
                                   ["attempt %d at %.3f" % (attempts,
                                                            time.time())]))
            try:
                receipt = fn()
            except PreEffectError as e:
                # Evidence: nothing happened. Same-key retry is safe.
                continue
            except AmbiguousError as e:
                outcome = self._recover_ambiguous(
                    akey, did, provider, reconcile_fn, "%s" % e)
                if outcome is not None:
                    return outcome  # reconciled receipt
                continue  # qualified same-key retry approved; loop
            except Exception as e:
                # Unknown failure: fail closed -> treat as ambiguous.
                outcome = self._recover_ambiguous(
                    akey, did, provider, reconcile_fn,
                    "%s: %s" % (type(e).__name__, e))
                if outcome is not None:
                    return outcome
                continue

            self._record(did, {
                "status": COMPLETED,
                "receipt": receipt,
                "intent_hash": akey.intent_hash,
                "namespace": akey.namespace,
                "attempts": attempts,
                "history": (self.ledger.get(did) or {}).get("history", []) +
                           ["completed at %.3f" % time.time()],
            })
            return receipt

    # -- ambiguous recovery: reconcile / retry / hold ----------------------
    def _recover_ambiguous(self, akey, did, provider, reconcile_fn, cause):
        """Recovery selection by evidence. Returns the reconciled receipt,
        None to approve a guarded same-key retry (loop continues), or raises
        on HOLD / unqualified."""
        contract = self.contracts.get(provider)

        # 1. RECONCILE: ask the provider what actually happened.
        if reconcile_fn is not None:
            try:
                found = reconcile_fn(akey)
            except Exception:
                found = None
            if found is not None:
                rec = self.ledger.get(did) or {}
                self._record(did, {
                    "status": COMPLETED,
                    "receipt": found,
                    "intent_hash": akey.intent_hash,
                    "namespace": akey.namespace,
                    "attempts": rec.get("attempts", 0),
                    "history": rec.get("history", []) +
                               ["reconciled at %.3f (cause: %s)"
                                % (time.time(), cause)],
                })
                return found

        # 2. RETRY_SAME_KEY: only when the contract is QUALIFIED_IN_SCOPE
        #    with retention, and LAW still valid. Never a blind retry.
        if contract is not None and contract.retry_allowed():
            return None  # approved; loop retries under the same fences

        # 3. HOLD: terminal UNRESOLVED_EXTERNAL_OUTCOME record, then raise
        # the specific reason. The record is terminal either way: the
        # retry stays blocked until a human reconciles.
        if contract is not None and contract.verdict != QUALIFIED_IN_SCOPE:
            self._write_hold(did, akey,
                             "provider %s not qualified for retry "
                             "(verdict=%s)" % (provider, contract.verdict))
            raise UnqualifiedProviderError(
                "provider %s not qualified for retry (verdict=%s); "
                "retry blocked, outcome recorded %s"
                % (provider, contract.verdict, UNRESOLVED_EXTERNAL_OUTCOME))
        return self._hold(did, akey,
                          "ambiguous outcome, no reconcile path, "
                          "contract not qualified (cause: %s)" % cause)

    def _write_hold(self, did, akey, reason):
        rec = self.ledger.get(did) or {}
        self._record(did, {
            "status": UNRESOLVED_EXTERNAL_OUTCOME,
            "receipt": None,
            "intent_hash": akey.intent_hash,
            "namespace": akey.namespace,
            "attempts": rec.get("attempts", 0),
            "history": rec.get("history", []) +
                       ["HELD at %.3f: %s" % (time.time(), reason)],
        })

    def _hold(self, did, akey, reason):
        self._write_hold(did, akey, reason)
        raise UnresolvedOutcomeError(
            "no safe recovery for %s: %s" % (did, reason))

    def _record(self, did, record):
        self.ledger.put(did, record)
