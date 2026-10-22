# Merge Receipt Gate — Wiring

**Status (t952):** CI wiring written on branch `naya/nine-receipt-gate-t902`.
**STILL OPEN:** marking the check required — Shawn's protected click
(documented ready below, never clicked by us). The gate ships when he clicks.

## What the gate does

## What the gate does

The scorecard receipt is **preventative, not archival**: it must certify the
EXACT merge head SHA being merged. The gate blocks merges whose receipt is:

- **MISSING** — no pin anywhere in the PR body / `pr_state`
- **TAMPERED** — pin block present but `merge_head_sha` malformed
  (must be 40 lowercase hex), attribution empty, timestamp unparseable, or
  receipt not posted (no board comment id)
- **STALE** — pinned SHA != the current merge head SHA (head moved since the
  scorecard ran — re-score on the current head, re-pin, re-verify)

## The two rungs

### Rung 1 — PR body: `tools/check_scorecard_receipt_pin.py`

```
python3 tools/check_scorecard_receipt_pin.py <expected-head-sha> [pr-body-file]
```

- Extracts the `## SCORECARD-RECEIPT-PIN` block from the PR body (key: value
  lines; blank line or next `##` header ends the block).
- Required keys: `merge_head_sha`, `decided_by`, `decided_at`,
  `board_comment_id`.
- Exit 0 + JSON `{"verdict": "PASS"}` on a valid pin; exit 1 + JSON
  `{"verdict": "MISSING"|"TAMPERED"|"STALE", "reason": ...}` otherwise.

Receipt-pin block format:

```
## SCORECARD-RECEIPT-PIN
merge_head_sha: <40 lowercase hex chars>
decided_by: <seat name>
decided_at: <ISO-8601 timestamp>
board_comment_id: <digits>
```

### Rung 2 — gate: P12 in `tools/auto_merge_gate.py`

`may_auto_merge(pr_state)` fails closed when `pr_state["receipt_pin"]` is
absent, when `receipt_pin.merge_head_sha` is not 40-char lowercase hex, or
when it differs from `pr_state["head_sha"]`. Numbered P12 because P11 is the
pre-existing smart-link regen receipt precondition — the receipt pin is a new,
separate precondition.

## Named holes

1. **No cryptographic signature on the pin.** Tamper detection is
   field-integrity only (shape + attribution + posted-ness). Signing needs a
   key-management decision — a protected-ops call, belongs to Shawn.
2. **Required-check click still Shawn's.** The wiring is ready; the
   enforcement only becomes a real gate once he marks the check required
   (see below). Until then it runs and reports but does not block.

## CI wiring (t952) — blocking check, ready for Shawn's click

- **Workflow file:** `.github/workflows/receipt-gate.yml`
  (on branch `naya/nine-receipt-gate-t902`; ships with the branch merge).
- **Triggers:** `pull_request` `opened` + `synchronize`, base branch `main`.
- **Check name as it appears in Actions:** `Receipt pin gate / Receipt pin — exact head SHA`.
- **What it does:** Rung 1 runs `tools/check_scorecard_receipt_pin.py
  <head-sha>` against the PR body (fail-closed: MISSING/TAMPERED/STALE → red);
  Rung 2 runs `tools/auto_merge_gate.py --p12-only` on the pin extracted from
  the body. Two rungs, same rule: the receipt must certify the exact head.
- **Scope:** lane branches (`naya/*`) only; other PRs get an explicit PASS
  decision (a decision, never a skip — the check never hangs in Pending,
  the #2385 lesson).
- **Permissions:** `contents: read`, `pull-requests: read` (least privilege).
- **Shawn's one line:** in repo Settings → Branches → main branch protection,
  mark **`Receipt pin gate / Receipt pin — exact head SHA`** as a required
  status check.

## Proven

`tests/test_receipt_pin_gate.py` — 19 tests (14 from t922 + 2 for the pin CLI's
`--pr-state-out` + 3 for the gate's `--p12-only`), all passing.

Fail-closed demos (t952, exact workflow commands, local simulation —
a real Actions run awaits the first PR off this branch; no PR opened this
tick per brief):

- (a) PR body with no receipt → `{"verdict": "MISSING", ...}`, exit 1 → FAIL
- (b) pin naming a stale head SHA → `{"verdict": "STALE", ...}`, exit 1 → FAIL
- (c) pin naming the exact head SHA → `{"verdict": "PASS"}` + P12
  `{"allowed": true, "reasons": []}`, exit 0 → green

Exact run evidence lives in the t952 lane receipt.
