# Scorecard Receipt Authority — Learning Promotion Bridge

**Branch:** `naya5/scorecard-receipt-authority`
**Law:** SN-0340 (The Scorecard Law) — "If you did your scorecard honestly, you don't need to ask."
**Design decision:** Naya 5, 2026-10-07. Naya 2's bridge proposal, adopted with the honesty-binding refinement.

## Problem

Learning promotion requires a `learning_lock_in` grant row. Grants are issued by
rescue mission (the 2026-10-07 freeze: 10 candidates sat 5 days waiting on one).
The Human Director's directive: his authority is the rubric, not the bottleneck.
The math decides; the system flows.

## Bridge (not demolition)

The verifier accepts **EITHER**:

1. **Personal grant** — existing `nayanet_authority_grants` path, unchanged.
2. **Scorecard receipt** — NEW. A receipt meeting the Scorecard Law's five steps
   (mechanically validated, ported from `tools/auto_merge_gate.py`) **plus**
   learning-promotion bindings:
   - `scope_target` exactly matches the promotion target block id
   - `scope_action` is `"learning_lock_in"`
   - `decided_at` within 7 days (matches grant expiry pattern)
   - `decided_by` names the scorer (anonymous receipts are not authority)
   - `promotion_option_id` declares which option authorizes promotion; winner must equal it
   - Winner averages ≥ 9.0 across the four dimensions (nothing under 9.0 ships)
   - Winner holds the highest total (the math decides, not the author)

Fail-closed: no valid grant AND no valid receipt → 403 `LEARNING_LOCK_IN_LAW_DENIED`.
An offered-but-invalid receipt returns its reasons (debuggability, still denied).

## Why this is safe

- **No new authority system.** Reuses the existing Scorecard Law receipt schema
  and its mechanical validator. Extends the existing gate; does not replace it.
- **Visibility is the honesty bond.** Receipts must be posted (step 5 requires
  `receipt_posted_comment_id`). Inflated scores are public, attributable, and
  falsifiable by any seat.
- **Scope-bound.** A receipt authorizes one target, one action, for 7 days —
  same discipline as a grant's `scope.target`.
- **Hard boundaries untouched.** This changes what the *learning promotion gate*
  accepts. It does not touch production deploys, credentials, destruction, or
  constitutional ratification. Deploying this change itself needs the Director's word.

## Files

- `supabase/functions/nayanet-learning-verify/scorecard_receipt_authority.js` — NEW.
  Plain JS (harness-compatible, no TS annotations), `// SCORECARD-RECEIPT-AUTHORITY-END`.
- `supabase/functions/nayanet-learning-verify/index.ts` — MODIFIED. Import +
  fallback path at the LAW gate. Grant checked first; receipt tried only when
  grant fails and a receipt was offered.
- `tests/scorecard_receipt_authority.test.mjs` — NEW. 15 tests, all passing.
- `.naya/specifications/NAYA-SCORECARD-RECEIPT-AUTHORITY-V1.schema.json` — NEW.

## What this does NOT do

- Does not deploy. The edge function change ships only on the Director's explicit word
  (authority change — the calculus says value never creates authority).
- Does not remove the grant path. Grants remain the direct-expression authority.
- Does not auto-promote. A receipt must still be written, scored honestly, and posted.

## Next

1. Naya 4 opens PR.
2. Team review + Director's deploy decision.
3. After deploy: grant-queue becomes scorecard-queue — the rubric issues them.
