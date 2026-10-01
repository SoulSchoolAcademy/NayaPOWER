# Privacy Qualification — input-state retention (Move 7)

**Question:** preserving the full evaluated `inputs_state` enables cold
recomputation of `inputs_hash`, but the state can contain more sensitive
material than a decision receipt. Is retention within legitimate scope?

## What the evaluated state contains

From the `demo-001` proof pair: the kernel's full gate-evaluation context —
nested decision receipts, authority basis (`kind`, `ref`, `revoked`),
config hashes, execution budgets, flags, stakes. This is decision-making
working material. It CAN contain sensitive content: authority references,
configuration details, and whatever the gates evaluated at decision time.
The adapter cannot enumerate what a future kernel version will put there.

## Governing boundary

- **Constitution Art XI:** PRIVATE BY DEFAULT. SHARED BY CHOICE. COLLECTIVE
  BY CONSENT. PUBLIC BY DECISION. "Technical accessibility MUST NOT be
  treated as permission to disclose."
- **Constitution Art XIV:** fail closed on scope uncertainty.
- **Migration `20260919015207`:** `privacy_classification` ∈
  (PRIVATE, SHARED, COLLECTIVE, PUBLIC), default PRIVATE.

## Qualification

1. **Default is PRIVATE (fail-closed).** `project_kernel_receipt` defaults
   `owner_scope="PRIVATE"`. The adapter never widens scope on its own.
2. **Scope is the caller's claim, not the adapter's verification.** The
   adapter shape-checks the scope string and records it verbatim in
   `p_privacy_classification`. It cannot classify content and cannot verify
   the underlying choice/consent/decision — that authorization belongs to
   the data owner and the calling application, per Art XI.
3. **"Privacy unchanged" holds only for PRIVATE.** The earlier claim that
   retention doesn't change privacy posture is true when the row is PRIVATE
   (row already private to the owner; receipt already verbatim). It is NOT
   universally true: a caller projecting with SHARED/COLLECTIVE/PUBLIC
   broadens exposure of the full input state, and the adapter records that
   broadening as the caller's explicit claim.
4. **No redaction.** The adapter never redacts inputs_state: redacted
   material would not reproduce `inputs_hash`. If a sharing context
   requires a derived (less-sensitive) projection, that projection is a
   separate artifact with its own lineage — not a silent modification of
   the recomputation evidence.
5. **Credentials.** Whether credentials can enter the evaluated state is a
   producer-side property (what the kernel's gates evaluate). The adapter
   treats all input state as opaque; it does not scan, and scanning would
   not be a boundary it can enforce.

## Test

`tests/test_persistence_seam.py` (privacy_*): default is PRIVATE;
explicit scope recorded as caller claim; adapter never widens; invalid
scopes rejected (not coerced).

## Residual

Write-time caller binding is absent in V1 (see #554 `5936492442`): a
non-owner caller could in principle project with a broad scope. Scope
authorization is an application-layer responsibility under the current
writer. If write-time scope authorization is required, that's a governed
writer change, not an adapter change.
