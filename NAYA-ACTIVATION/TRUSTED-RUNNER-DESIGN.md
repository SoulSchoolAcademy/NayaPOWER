# Trusted Runner for Activation Receipts — Design Proposal (CANDIDATE)

Per SN-0787: *a builder can forge both the receipt and the expected hashes;
expected values must come from a source the builder cannot write.*

## The problem
The activation receipt is written by the builder. If the same builder also
supplies the "expected" values the gate checks against, the check is theater:
forge the receipt, forge the expectations, pass. The enforcement chain needs
its expected values from somewhere the builder cannot write.

## Where the check runs
A GitHub Actions workflow on the PR: `.github/workflows/activation-receipt-check.yml`,
triggered on `pull_request` (opened, synchronize). It runs on GitHub-hosted
runners with the standard `GITHUB_TOKEN` — the builder has no write access to
the runner, its token, or its network fetches.

## What the builder supplies (and nothing more)
1. An activation citation on the deliverable: `activation:<16-hex>`.
2. The receipt JSON at `NAYA-ACTIVATION/receipts/<session-id>.json` in the PR head tree
   (schema `naya.activation.receipt.v2`, per the protocol Step 2).

That is the builder's entire input channel. There is no field, parameter, or
file by which the builder provides expected values.

## What the runner fetches itself (the builder cannot write these)
At check time, the runner calls the GitHub API directly:
- Current main tip: `GET /repos/{o}/{r}/git/ref/heads/main`
- Blob SHA of the receipt's recorded doctrine file: `GET /repos/{o}/{r}/contents/<path>?ref=main`
- Blob SHA of the receipt's recorded block manifest: same contents API
- Current UTC time: the runner's own clock

## Checks, in order (first failure stops the run)
1. **CITATION_PRESENT** — the PR carries an `activation:<16-hex>` citation. Reject: `NO_CITATION`.
2. **RECEIPT_FOUND** — the receipt path exists in the head tree. Reject: `RECEIPT_NOT_FOUND`.
3. **SCHEMA_VALID** — `schema == "naya.activation.receipt.v2"` and `status == "ACTIVATED"`. Reject: `SCHEMA_MISMATCH`.
4. **TIMESTAMP_SANE** — parses as ISO-8601, not in the future, within 4h of runner time. Reject: `FUTURE_TIMESTAMP` / `STALE_TIMESTAMP`.
5. **TIP_CURRENT** — `receipt.main_sha ==` live main tip. Reject: `TIP_MOVED` (re-activate; SN-0493).
6. **COMPONENTS_LIVE** — each recorded component SHA equals the freshly fetched blob SHA. Reject: `COMPONENT_MISMATCH` (forged or stale doctrine/blocks).
7. **CITATION_BOUND** — runner recomputes sha256 over the canonical receipt bytes (keys sorted recursively, separators `(',', ':')`) and compares the first 16 hex chars to the citation. Reject: `CITATION_MISMATCH` (forged citation or edited receipt).

## Why forgery fails
- Forge the receipt content → its recomputed hash won't match the citation (`CITATION_MISMATCH`).
- Forge the citation → it won't match the recomputed hash (`CITATION_MISMATCH`).
- Copy a real receipt but edit the component SHAs to match stale files → runner fetches live SHAs itself (`COMPONENT_MISMATCH`).
- Reuse yesterday's valid receipt → `main_sha` no longer equals the tip (`TIP_MOVED`) or timestamp is stale (`STALE_TIMESTAMP`).
- The builder cannot supply alternative "expected" values because the workflow defines no such input.

## Honest limits (not oversold)
- The runner proves the builder resolved *current* SHAs, not that they *read* the doctrine. Reading is verified behaviorally (cold-Naya proof) and by independent review — this gate is the ENFORCE layer, not the VERIFY layer.
- `session_id` uniqueness is not checked; replay of one's own fresh receipt within the window is possible and acceptable (it is still a current activation).
- A builder can activate and then ignore everything they loaded. The gate makes skipping *detectable and pointless*, not physically impossible — exactly what the protocol's Verification section claims.

## Status
CANDIDATE design. Not implemented, not merged, not RATIFIED. Implementation owner: gate-fusion pair (Naya 5's `tools/design_gate.py --require-activation` is the existing seed; this design specifies the CI-side runner it must become).
