# UD-13 — NEVER ACT TWICE ON THE OUTSIDE WORLD

`tools/exactly_once.py` — the exactly-once guard. Stdlib only.

## What it is

Any action touching the outside world (API calls, posts, merges, messages)
happens **exactly once**. A timed-out request, a crashed worker, or a missing
receipt is not permission to do it again.

## The rules (machine-enforced)

1. Every outward action carries a durable logical-operation identity:
   `ActionKey(namespace, intent, key)`. The intent says WHAT the world should
   observe; the key is unique per logical operation.
2. A completed key never re-executes — repeats return the cached receipt.
3. A different key for the same intent raises `DuplicateIntentError`.
4. In-flight keys and intents are fenced — a second worker is held, never run.
5. Ambiguous outcomes reconcile first (`reconcile_fn` asks the provider what
   happened). A same-key retry happens only when the provider contract is
   `QUALIFIED_IN_SCOPE` with retention, and LAW permission holds. Otherwise
   the outcome is recorded `UNRESOLVED_EXTERNAL_OUTCOME` and the retry stays
   blocked.
6. No trace passes with an unqualified provider boundary.

## Usage

```python
from tools.exactly_once import (
    ActionKey, Ledger, ProviderContract, ExactlyOnceGuard,
    PreEffectError, AmbiguousError, QUALIFIED_IN_SCOPE)

ledger = Ledger("/var/lib/naya/exactly-once-ledger.json")
guard = ExactlyOnceGuard(ledger, {"api.example.com": ProviderContract(
    "api.example.com", verdict=QUALIFIED_IN_SCOPE,
    idempotency_key_supported=True, retention_horizon_s=3600,
    concurrency_model="concurrent-safe", downstream_effects_covered=True,
    query_path_available=True)})

def post_comment():
    try:
        return api.post_comment(issue, body)   # the external effect
    except TimeoutError:
        raise AmbiguousError("timeout after send")

receipt = guard.execute(
    ActionKey("lanes", "post comment X to issue 2175", "op-uuid-1"),
    post_comment, "api.example.com",
    reconcile_fn=lambda akey: api.find_comment(issue, body),
    law_valid=True)
```

The action fn signals with exceptions:
- `PreEffectError` — failed before any effect (safe same-key retry).
- `AmbiguousError` — effect may have happened (reconcile-or-hold).
- anything else — treated as ambiguous (fail closed).

## What this does NOT claim

- The five-dimension provider contract is a subset of the UD-13 spec's ten
  dimensions; the full qualification package is follow-up work.
- Cross-process fencing uses lock files next to the ledger; NFS-style
  filesystems with weak atomicity are out of scope.
- Reconcile correctness depends on the provider's query path telling the
  truth; a lying provider is a separate (UD-14) problem.
- It judges duplication, not authorization — pair with the LAW gates.
