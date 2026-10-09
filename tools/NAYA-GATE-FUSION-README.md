# Naya Unified Delivery Gate — fusion record

One gate at the delivery boundary. Fused 2026-10-09 by Naya 4 (Gate Fusion pair,
doer). Not a competing gate — the three existing efforts integrated, each owner
keeps their deep lane.

## What was fused

| Stage | Source | Owner | Commit / PR | What it contributes |
|---|---|---|---|---|
| 1 — Design (structural) | `tools/design_gate.py` | Naya 5 (Smart Blocks lane) | @ 728cab40 | 7 machine-provable structural laws: self-contained, black root, no light surfaces, dark color-scheme, no freestyle components (manifest), light text, mobile viewport |
| 2 — Activation (drink-first) | `NAYA-ACTIVATION/tools/drink_first_gate.py` | Naya 4 (LEARN lane) | PR #1979 (draft) | Fail-closed verdicts: FAIL-UNACTIVATED, FAIL-TIP-MOVED, FAIL-STALE, FAIL-CITATION, FAIL-SCHEMA |
| 2 — Activation (consistency) | `tools/qa/activation_receipt_consistency.mjs` | Naya 3 (Innovation lane) | PR #1974 (draft) | Receipt consistency falsifier: schema, identity completeness, repository binding, main_sha match, freshness, citation binding |
| 2 — Citation binding | `tools/design_gate.py --require-activation` | Naya 5 | @ 728cab40 | `<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->` must equal sha256 of the exact receipt bytes |

Deep lanes stay with their owners: Naya 5 owns structural design rules,
Naya 3 owns the CI-side deep receipt checker (`tools/qa/`), Naya 4 owns the
activation protocol (PR #1970). This gate is the single delivery-boundary
entry point that runs all three stages.

## The trusted-runner design (SN-0787)

A builder can forge both the receipt and the expected hashes, so expected
values must come from a source the builder cannot write.

- `--enforce` (default with `--require-activation`): the gate resolves the
  live tip ITSELF via `git ls-remote https://github.com/SoulSchoolAcademy/NayaPOWER.git HEAD`
  and compares the receipt against that. The builder never supplies the
  expected value.
- `--live-tip <sha>` is honored ONLY with `--trust-caller`, and the verdict
  is then labeled ADVISORY — never enforcement-grade.
- `--live-tip` without `--trust-caller` is rejected outright, citing SN-0787.
- If the trusted fetch fails, the gate fails closed (FAIL-TRUSTED-FETCH):
  unverifiable is not shippable.

## Receipt schemas

Accepts `naya.activation.receipt.v1` (drink-first) and
`naya.activation.receipt.v2` (activation protocol). Requires the union of
critical fields: status ACTIVATED, repository == SoulSchoolAcademy/NayaPOWER
(wrong-repo receipts rejected), 40-hex main_sha, fresh activation timestamp
(<4h, not future), and schema-appropriate identity/loaded fields.

## Verification

- `python3 tools/naya_gate.py --self-test` — 12 red-green adversarial controls.
- `python3 -m pytest tools/test_naya_gate.py -v` — 13 tests, including 2
  end-to-end enforce-mode runs against the REAL live tip (marked e2e).
- `.github/workflows/naya-gate.yml` — CI wiring (candidate): runs the suite.

## Status

CANDIDATE. Draft branch only. Never merged, never deployed, nothing RATIFIED.
Independent scorer attack pending (pair protocol: the doer never verifies).
