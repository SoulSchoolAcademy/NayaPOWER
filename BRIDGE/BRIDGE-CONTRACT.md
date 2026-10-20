# BRIDGE-CONTRACT.md — NayaPOWER bridge backend contracts (v0.2)

The machine-readable source of truth for this directory's implementation is
`bridge_server.py` + `bridge_sync.py`. This document states the same contracts
in prose so a reader (or a later agent) can see what the code enforces without
re-deriving it. Where prose and code disagree, **the code wins** — and the
prose gets corrected.

## Lanes

| Lane | Route | Status |
|---|---|---|
| Webhook intake → append-only ledger | `POST /webhook` | working (hardened) |
| Tool endpoints | `POST /tools/<name>`, `GET /tools/get_daily_report` | working (stubbed backends) |
| Feed sync sketch | `POST /sync` | dry-run sketch (fixtures) |
| Ledger sync | `POST /sync/ledger` | working on real ledger data (local-only apply) |
| Health | `GET /health` | working |

## Webhook verifier

The verifier's contract is the code in `BridgeHandler._webhook` — never assume
the shape from another doc:

1. Body must parse as a JSON object, else `E_INVALID_INPUT` (nothing staged).
2. No app key configured → `E_UNVERIFIED` 401: intake disabled, fail closed.
3. Canonical payload = `json.dumps(body, sort_keys=True, separators=(",", ":"))`.
4. Expected signature = `"sha256=" + HMAC-SHA256(key, canonical).hexdigest()`,
   taken from the `X-Naya-Signature` header.
5. Compared with `hmac.compare_digest` (constant time). Mismatch →
   `E_BAD_SIGNATURE` 401, **no ledger directory is created, no record staged**.
6. Verified payloads are idempotent: the payload digest indexes the ledger, so
   replays return the original `ledger_seq` with `state="received-duplicate"`
   and no duplicate line is appended.

Ledger records are `webhook-ledger/v1`, `ledger_version: 1`, and carry
`owner_scope` **unchanged** — the ledger never re-labels scope (D4).

## Ledger content choice (F1 — stated explicitly, 2026-10-20)

**What the ledger carries:** every record carries event name, `owner_scope`,
`payload_sha256`, `seq`, and `received_at`. Additionally, for
**public-scope events** (`owner_scope` in PUBLIC / COLLECTIVE / SHARED) the
record carries a `content` envelope: an allowlist of string fields
(`title`, `note`, `summary`), each truncated at 500 chars.

**Why:** privacy-by-design. A PRIVATE record is name+scope+digest **only** —
payload content never lands in the ledger for private rows, so a private
note cannot leak through a ledger read. Public-scope events are intended for
the public lane, so their display content travels with the record and a
public feed row shows real content (a title or note), not the bare event
name like `note.captured`. D4 is preserved either way: PRIVATE rows are
filtered before any diff and never reach the public lane, so the envelope
can only ever exist on rows that may legally be public.

**What a public feed row shows:** `title` prefers the carried `title`,
then `note`, then `summary`, falling back to the event name; `content`
mirrors the envelope (per the emitter's `room-feed/v1` `.content` shape).
A feed row built from a private record would show only the event name —
but private rows never reach the feed at all.

## seq and replay index (F2/F3 — 2026-10-20)

**seq:** monotonic per server process, seeded from the ledger's max `seq`
at boot (`max_ledger_seq`). Two distinct events landing inside the same
millisecond get distinct seqs — `seq = max(now_ms, last_seq + 1)`. The
payload digest remains the identity for idempotence: replays return the
original seq.

**Replay detection:** an in-memory digest index
`{payload_sha256 -> (seq, event)}`, built once at boot and updated on every
append — the per-request replay check is an O(1) lookup, not an O(n)
full-ledger parse. Skeleton assumption: single writer (the server process
owns the ledger directory), so the index cannot drift. Production note:
replace with a persistent unique digest index (e.g. a DB unique constraint
on `payload_sha256`) when the skeleton grows a real store.

## Tool registry

`TOOL_REGISTRY` in `bridge_server.py` is the entire tool surface. An incoming
`/tools/<name>` that is not a registry key gets `E_UNKNOWN_TOOL` 404 — unknown
tools are rejected, never guessed at, aliased, or partially executed. Every
tool route is bearer-auth-gated; missing required fields fail closed with
`E_INVALID_INPUT` (no idempotency key → no capture).

## Sync

* `POST /sync` — dry-run plan from `sync_supabase_to_github` over labelled
  fixtures. Apply is refused (`E_NO_CREDENTIALS`): the sketch has no backend.
* `POST /sync/ledger` — **working** sync over the real append-only ledger:
  reads `events.jsonl`, applies the D4 private filter, computes the conflict
  rule, and plans against the local `feed-state.json`. Dry-run is the default.
  Apply requires `BRIDGE_CAN_WRITE=1` and writes **only the local feed-state
  file**; no remote writes exist in the skeleton.

Conflict rule (stated once, in `CONFLICT_RULE`): newest `updated_at` wins;
ties → Supabase wins and the GitHub copy is flagged `diverged` (never silently
overwritten); PRIVATE rows are filtered **before** any diff is computed and
cannot appear in the public lane at all (D4).

## Error taxonomy

Stable codes. Every error response is
`{ok:false, state:'error', error:{code, message, doc}}`.

| Code | HTTP | Meaning |
|---|---|---|
| `E_NOT_FOUND` | 404 | unknown route |
| `E_UNKNOWN_TOOL` | 404 | tool name not in `TOOL_REGISTRY` |
| `E_INVALID_INPUT` | 400/422 | malformed body, missing required field, bad mode |
| `E_UNAUTHENTICATED` | 401 | missing/invalid bearer token |
| `E_UNVERIFIED` | 401 | no app key configured (local-dev mode) |
| `E_BAD_SIGNATURE` | 401 | webhook HMAC mismatch — nothing staged |
| `E_NO_CREDENTIALS` | 503 | apply refused — skeleton has no backend credentials |

## App-key handling (design-only notes)

* The key arrives only via the `NAYA_BRIDGE_APP_KEY` environment variable.
* It is **never** logged, printed, echoed back in responses, committed to
  files, or pasted into board posts. The access log redacts it.
* Real key issuance and injection are engine-team / Shawn territory — this
  skeleton describes the envelope, never the material.
* Local testing uses throwaway keys generated at runtime (see
  `test_bridge_harness.py`); they are never committed and never leave the
  test process.
