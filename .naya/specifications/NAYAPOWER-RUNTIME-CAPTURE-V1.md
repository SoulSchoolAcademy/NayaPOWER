# NayaPOWER — Runtime Capture V1
## Governed agent-invocation path for the canonical Receiver

**Status:** PROPOSED (PR — not merged, not deployed, not proven)
**Scope:** CAPTURE only. Resolves Blocker B1.
**Authority:** NayaPOWER System North Star; Scorecard Law.
**Canonical receiver:** `supabase/functions/v7-smart-note-canonical` — **UNCHANGED by this spec.**

---

## 1. Problem

The canonical Receiver requires an `Authorization` header validated via
`supabase.auth.getUser()` — a Supabase user JWT. No Naya runtime holds one,
so no Naya runtime can capture. CAPTURE scores 4/10: the mechanism exists,
but only Shawn can invoke it.

## 2. Design constraint (verified on live main, 2026-10-06)

The receiver's downstream pipeline is **structurally coupled to a real
authenticated user**:

- `nayanet_record_cognition_event` is `security invoker` and raises
  `AUTH_REQUIRED` when `auth.uid()` is null — a service-role / machine
  principal cannot run it.
- `nayanet_cognition_events.user_id` has `references auth.users(id)` —
  a non-user UUID violates the FK.
- RLS policies are owner-scoped (`user_id = auth.uid()`).

Therefore any correct resolution MUST present a **real Supabase user JWT**
to the receiver. Extending the receiver to accept GitHub-OIDC directly
would require rewiring `security invoker` RPCs and FK constraints —
invasive surgery on the most critical function. This spec does the
opposite: **the receiver is not touched at all.**

## 3. The path: Naya Runtime Identity + governed capture workflow

1. **One dedicated auth user** (`naya-runtime`) exists in Supabase Auth.
   Created once by Shawn. It is a real user, so JWTs, RLS, FKs, and RPCs
   all behave exactly as for any human caller. Captures are attributed to
   this distinct identity — never confused with Shawn's.
2. **The credential lives in GitHub repo secrets**
   (`NAYA_RUNTIME_EMAIL`, `NAYA_RUNTIME_PASSWORD`,
   `NAYA_SUPABASE_URL`, `NAYA_SUPABASE_ANON_KEY`).
   Naya runtimes NEVER hold the Supabase credential.
3. **`.github/workflows/nayanet-agent-capture.yml`** (this PR) is the
   single governed entry point. On `workflow_dispatch` it:
   - validates the payload shape (fail fast),
   - signs in as `naya-runtime` → real JWT (short-lived, per run),
   - POSTs the payload to the UNCHANGED receiver,
   - asserts `ok:true`, `pipeline:"PROJECTION_VERIFIED"`,
     `intelligent_block_id` matches `IB-\d{6}`, and `smart_link`
     matches the canonical receiver-bound pattern,
   - emits the receipt JSON between `CAPTURE_RECEIPT_JSON` markers.
4. **Naya runtimes invoke capture** by dispatching the workflow with
   their existing GitHub credential, polling the run, and reading the
   receipt from the logs (`scripts/naya-runtime-capture.sh`, this PR).

## 4. Why this is safe (not weakened auth, no second memory)

- The receiver's security boundary is **byte-identical**: real user JWT,
  `getUser()` validation, full RLS, canonical pipeline, 15-minute
  projection grants. Nothing bypassed, nothing added.
- The workflow file lives on protected `main` (PRs only, Shawn merges) —
  the code path is audited and versioned.
- The runtime credential is scoped to ONE user whose only purpose is
  capture; it is revocable by disabling the user or rotating the secret.
- The Receiver remains the single canonical path: IB identity is still
  allocated ONLY by `v7-smart-note-canonical`; repository code still MUST
  NOT allocate or guess IB ids.
- Every capture is provenance-bound: `actors.creator` = the runtime
  user id; `source` = `nayanet-agent-capture:<invoking-seat>`;
  idempotency keys are namespaced `naya-runtime-capture:<uuid>`.

## 5. What this deliberately does NOT do

- No OIDC acceptance in the receiver (see §2 — structurally unsound).
- No new auth scheme, no API keys, no shared secrets in chat or files.
- No change to the human capture path (Shawn's flow is untouched).

## 6. Behavioral proof plan (gated)

1. Shawn creates the `naya-runtime` user + sets the four secrets.
2. Shawn merges this PR (`.github/workflows/` is his gate).
3. A Naya runtime runs `scripts/naya-runtime-capture.sh` with a
   clearly-marked governed test note.
4. PASS = receiver returns `PROJECTION_VERIFIED` with a real `IB-…`
   id and a verified Smart Link, readable from the workflow logs.
   Only then does CAPTURE move above 4/10.

## 7. Follow-ups (named, not blocking)

- `learning_evidence.provenance` is hardcoded `"USER"` in the receiver;
  runtime captures should be labeled distinctly. Filed as a refinement
  against the receiver (small, review-heavy) — not required for 10/10.
- Secret rotation cadence for the runtime credential (Shawn's call).
