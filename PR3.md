## Coder 2 — deploy authority is genuinely absent, so I made drift VISIBLE instead

**Base:** `main` `d289ff2a` · **Branch:** `coder2/deployed-runtime-parity-detector-2026-09-28` @ `35ed4dab`

### I tried to establish a deploy path first. It does not exist.

| Probe | Result |
|---|---|
| `SUPABASE_ACCESS_TOKEN` (the management token `functions deploy` requires) | **absent** |
| `supabase` CLI / `supabase/config.toml` | **absent** |
| any workflow containing `functions deploy` | **NONE — all 5 only *invoke*** |

I did not reach for `SUPABASE_SERVICE_ROLE_KEY` to manufacture a deploy, and I did not hand-edit runtime state. **Deploy authority is a human decision; this PR does not pretend to have it.**

### ⚠ Credential finding, reported not exploited

Repo secrets currently include **`SUPABASE_SERVICE_ROLE_KEY`** and **`SUPABASE_USER_ACCESS_TOKEN`** — a service-role bypass key and a long-lived human token. Those are the exact two credentials the OIDC design was built to eliminate, and the contract tests assert `SUPABASE_USER_ACCESS_TOKEN` is absent from workflows. **I did not use, read, or modify either.** Flagging because a long-lived human token in the secret store is a standing governance risk, and removing it is not my call.

### The gap this closes

> A merged source fix can be cited as fixed and **never reach runtime**, and nothing in this repo would detect it.

That is not hypothetical. `evidence/deployed-runtime-observation.json` records it from run **36445685851**: the deployed function's `connect` receipt had **no `behavior` key** — proven by `KeyError: 'behavior'` — so `live-connect` failed and `independent-connect-verification` was **SKIPPED** while every other job looked fine. That artifact is still the one serving traffic.

### The one rule

> **UNKNOWN is never reported as MATCH, and never exits 0.**

An unverified system is not a verified system. Absence of evidence is not evidence of absence of drift. `MATCH` → 0. `DRIFT` → 1. `UNKNOWN` → 1. Both non-pass verdicts fail by design.

### Today's honest verdict is UNKNOWN

```
verdict : UNKNOWN
  - observation was taken against canonical 620cabd7 but HEAD is 35ed4dab;
    the comparison would be invalid
UNKNOWN IS NOT PASS.
```

**I did not fabricate an observation to turn this green.** Hand-writing a conforming receipt would be worse than having none — it launders an assumption into evidence. The record marks `authority_boundary` as **`NOT PROBED`**, because that run died at `behavior` and never reached those assertions. Asserting it was absent would have been fabrication.

### It works without any management token

`CANONICAL` is imported from `tests/verify_connect_runtime_receipt.py` — **single source of truth**, so the detector cannot drift away from the contract it enforces. `OBSERVED` is a real recorded runtime response. No Supabase query, no service-role access.

### I disclosed two bugs in my own detector

`tests/test_deployed_runtime_parity.py` (12 checks) caught **two real bugs I wrote**:

1. It flattened `connect.*` subfields while the contract only required the `connect` object → a *conforming* receipt was flagged as drift. Fixed by adding `REQUIRED_CONNECT_FIELDS` to the verifier, since the verifier genuinely does assert on those fields.
2. `REQUIRED_BEHAVIOR_FIELDS` are **bare** names (`blocked_by`) while observed keys are **qualified** (`behavior.blocked_by`) → every conforming receipt was reported as missing everything.

A drift detector that cannot be shown to detect drift is worse than no detector, because it is trusted. Disclosed rather than quietly fixed.

### Known limitation — stated plainly

**This is SHAPE parity, not VALUE parity.** It proves the deployed artifact *emits* the required fields. It does not police values: a deployed function emitting `connect_grants_authority: true` with the field present would still read `MATCH`. Value enforcement remains `verify_connect_runtime_receipt.py`'s job. The test asserts this limitation explicitly so nobody mistakes parity for safety.

### Contract not weakened

Every existing assertion in `verify_connect_runtime_receipt.py` is preserved verbatim. It still rejects the real historical receipt:

```
exit=1 — CONNECT_RECEIPT_CONTRACT_DRIFT: required field receipt.behavior is absent.
```

### Tests

```
python -m pytest tests -q   →   108 passed, 4 skipped, 0 failed   (was 96 passed)
```

No RLS change. No schema change. No credential. No production mutation. **No deploy performed, and none claimed.**

### One next action

> **Decide the deploy authority question, and if a deploy path is authorized, refresh the observation so parity becomes provable rather than UNKNOWN.**
> **PASS =** an authorized path by which merged `main` reaches runtime, plus a fresh `evidence/deployed-runtime-observation.json` recorded against that exact commit, producing `MATCH` from a real runtime response.
> **FAILURE =** authority withheld — then keep the detector red on UNKNOWN. **Do not hand-write an observation.** A fabricated conforming receipt is a worse outcome than a permanently red detector, because it would be trusted.

**The point of this PR is not to make the system look verified. It is to make "we do not know what is deployed" impossible to mistake for "everything is fine."**
