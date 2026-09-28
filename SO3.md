[CODER-2][SIGN-OUT] DEPLOY AUTHORITY IS GENUINELY ABSENT. SO I MADE DRIFT VISIBLE. PR #880. VERDICT TODAY: UNKNOWN — AND THAT IS CORRECT.

**HEAD inspected:** `d289ff2abfd03dc65ebae3775de05b16e46848c6` ("Merge remote-tracking branch 'origin/naya/intelligent-graph-v1'")
**Branch / commit / PR:** `coder2/deployed-runtime-parity-detector-2026-09-28` @ `35ed4dab` → **PR #880 — OPEN**
Earlier this session: `4fac43e5` → **#874 MERGED**; `d7df85a3` → **#875 OPEN**; Coder 1's **#854 MERGED**.

## WHAT I WAS ASKED, AND WHAT I FOUND
Establish a deploy path for edge functions, or obtain authority for one. I probed rather than assumed:

| Probe | Result |
|---|---|
| `SUPABASE_ACCESS_TOKEN` (management token `functions deploy` requires) | **absent** |
| `supabase` CLI / `supabase/config.toml` | **absent** |
| any workflow with `functions deploy` | **NONE — all 5 only *invoke* deployed functions** |

**Deploy authority is a human decision and I do not have it.** I did not reach for `SUPABASE_SERVICE_ROLE_KEY`, did not hand-edit runtime state, and did not fabricate a deploy.

## ⚠ CREDENTIAL FINDING — REPORTED, NOT EXPLOITED
Repo secrets hold **`SUPABASE_SERVICE_ROLE_KEY`** and **`SUPABASE_USER_ACCESS_TOKEN`** — a service-role bypass and a long-lived human token. These are the exact two credentials the OIDC architecture was built to eliminate, and the contract tests assert `SUPABASE_USER_ACCESS_TOKEN` is absent from workflows. **I did not use, read, or modify either.** Flagging only: a long-lived human token in the secret store is a standing governance risk and removing it is not my call.

## WHAT I BUILT (#880) — the detector
> **A merged source fix can be cited as fixed and never reach runtime, and nothing in this repo would detect it.**

That is not hypothetical. `evidence/deployed-runtime-observation.json` records it from run **36445685851**: the deployed `connect` receipt had **no `behavior` key** (proven by `KeyError: 'behavior'`), so `live-connect` failed and `independent-connect-verification` was **SKIPPED** while every other job looked fine. That stale artifact is still what serves traffic.

**THE ONE RULE: `UNKNOWN` is never reported as `MATCH`, and never exits 0.**
`MATCH`→0 · `DRIFT`→1 · `UNKNOWN`→1. Both non-pass verdicts fail by design.

**It works with no management token.** `CANONICAL` is *imported* from `tests/verify_connect_runtime_receipt.py` — single source of truth, so the detector cannot drift from the contract it enforces. `OBSERVED` is a real recorded runtime response. No Supabase query, no service-role.

## TODAY'S VERDICT IS UNKNOWN — AND THAT IS THE POINT
```
verdict : UNKNOWN
  - observation was taken against canonical 620cabd7 but HEAD is 35ed4dab;
    the comparison would be invalid
UNKNOWN IS NOT PASS.
```
**I did not fabricate an observation to go green.** The record marks `authority_boundary` as **`NOT PROBED`** — that run died at `behavior` and never reached those assertions. Asserting absence would have been fabrication. **A fabricated conforming receipt is worse than a permanently red detector, because it would be trusted.**

## I CAUGHT TWO BUGS IN MY OWN DETECTOR — DISCLOSED
`tests/test_deployed_runtime_parity.py` (12 checks) failed my own work twice:
1. It flattened `connect.*` while the contract only required the `connect` object → **conforming receipts flagged as drift.** Fixed by adding `REQUIRED_CONNECT_FIELDS` to the verifier, since the verifier genuinely does assert them.
2. `REQUIRED_BEHAVIOR_FIELDS` are **bare** (`blocked_by`) while observed keys are **qualified** (`behavior.blocked_by`) → **every conforming receipt reported as missing everything.**

A detector that cannot be shown to detect drift is worse than none, because it is trusted.

## KNOWN LIMITATION — STATED PLAINLY
**SHAPE parity, not VALUE parity.** It proves the deployed artifact *emits* required fields. It does **not** police values: a deployed function emitting `connect_grants_authority: true` with the field present would still read `MATCH`. Value enforcement stays with `verify_connect_runtime_receipt.py`. The test asserts this limitation explicitly so nobody mistakes parity for safety.

## TESTS — exact command, actual result
```
python -m pytest tests -q   →   108 passed, 4 skipped, 0 failed   (was 96 passed)
python BRAIN/12-ENGINEERING/verify-deployed-runtime-parity.py   →   exit 1 (UNKNOWN, correct)
```
Contract **not weakened** — the verifier still rejects the real historical receipt: `exit=1 CONNECT_RECEIPT_CONTRACT_DRIFT: required field receipt.behavior is absent.`

## RUNTIME / PERSISTENCE
**NOT claimed. No deploy performed, none claimed.** No credential, no RLS change, no schema change, no production mutation.

## KNOWN FAILURES / BLOCKERS
- **BLOCKED:** deploy authority (human decision) → CONNECT runtime re-verification stays BLOCKED.
- **UNKNOWN:** whether ANY deployed function matches `main`. Now a standing, measurable, machine-checkable risk rather than an assumption.
- Receipt lineage for runs `36447664463` / `36445685851` still not in a canonical PROOF layer (queue #8) — though #880 is the first step toward it.
- `b31f37fd` clean-start-vs-restore undecided.

## SELF-SCORE (not inflated)
| Dimension | Status |
|---|---|
| Current truth reconstructed | VERIFIED |
| Coder 1 claims checked | VERIFIED |
| Source / Test evidence | VERIFIED (108 passed, 12 negative paths) |
| Runtime evidence | **UNKNOWN — not claimed** |
| Persistence evidence | **UNKNOWN — not claimed** |
| Authority evidence | PARTIAL — receipt-level, runtime not re-run |
| Independent evidence | VERIFIED (clean clone, synthetic fixtures) |
| Negative-path evidence | VERIFIED |
| Regression safety | VERIFIED (0 failed, contract intact) |
| Source/runtime parity | **PARTIAL — now DETECTABLE, verdict honestly UNKNOWN** |
| Causal evidence | PARTIAL — receipt contract green, genuine chain unproven by me |
| Cold successor evidence | MISSING (queue #6/#8) |
| North Star | **NO** |

**Still under 9.5 and I will not inflate it. A brain whose deployed code nobody can verify is not a finished brain — it is a brain that can lie to itself quietly.**

## TOP-10 STATUS
#1 BLOCKED (proven, detector built as the fallback) · #2 DONE · #3–#10 open

## EXACTLY ONE NEXT ACTION
> **Decide the deploy-authority question. If a deploy path is authorized, refresh the observation so parity becomes provable: run the read-only `connect` live workflow, record the real receipt shape against the exact commit it ran, and confirm the detector reports `MATCH`.**
> **PASS =** authorized path exists, deployed artifact is refreshed from merged `main`, and `verify-deployed-runtime-parity.py` exits **0** on a genuine runtime observation.
> **FAILURE =** authority withheld → **leave the detector red on UNKNOWN and do not hand-write an observation.** Then the honest state is: the system knows it does not know, which is the first genuinely trustworthy thing in this repo.

**#854 made the tests run. #874 made CONNECT prove its authority boundary in source. #880 makes it impossible to mistake "I don't know what's deployed" for "it's fine." Next Naya: the answer is one human decision away.**
