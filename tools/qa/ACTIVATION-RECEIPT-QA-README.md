# Activation receipt falsifier — independent QA only
**Status: CANDIDATE / DRAFT / NOT WIRED TO CI / NOT THE ACTIVATION IMPLEMENTATION.**
**Owner coordination:** Naya 4 owns Protocol V2 (#1970); Naya 5 owns the canonical Smart Blocks and design gate (#1969); Naya 2 performs independent design acceptance. This QA file should be reviewed by those owners, not installed as a new Naya law by itself.

## Plain language
**Before Naya serves, she must show she checked the current project and loaded the proper rules.** This small checker rejects inconsistent activation papers: no receipt, wrong or stale main, old design contract, wrong block library, stale feed/goal fingerprint, future/expired time, or a report with no matching receipt citation.

It **cannot** determine whether Naya actually *understood* the documents; whether the page is beautiful, useful, readable or safe; or whether Naya received LAW authority. Successful source consistency is **eligibility for independent review only**, not verification, runtime activation or deployment.

## Source truth and contradictions found
At the 2026-10-09 review, live main `9f2e3db56b2b399713f2bc6833e39264e03b958c` had:
- Canonical `AGENTS.md`, Portable Activation Protocol V1, Smart Note Operating Contract V1, Design Contract v1.1.
- Candidate Protocol V2 in draft #1970 references `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md`, which was **not found on main** at that exact path. Existing ratified law is `BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md`; candidate block sets exist at `BRAIN/10-INTERFACES/DESIGN-BLOCKS/README.md`, while Naya 5's newer 58-block library is only on draft #1969.
- Draft #1969's `tools/design_gate.py` inspects HTML/CSS structure, not activation receipt identity, freshness, document version or work-product citation.
- Main can move while a session proceeds (and did move during this QA session). A receipt must be checked against the fresh **main at the action boundary**, not the session's remembered tip.

## Narrow test contract
`checkActivationReceipt(receipt, expected, workProduct, nowIso)` consumes a V2 **candidate** receipt:
```json
{
  "schema": "naya.activation.receipt.v2",
  "status": "ACTIVATED",
  "session_id": "...",
  "naya_identity": "...",
  "human_authority": "...",
  "repository": "SoulSchoolAcademy/NayaPOWER",
  "job": "human outcome",
  "gates": ["specific governing tests"],
  "proof_plan": "independent result check",
  "main_sha": "40-hex",
  "loaded": {
    "design_blob": "40-hex",
    "blocks_blob": "40-hex",
    "goals_digest": "64-hex",
    "feed_digest": "64-hex"
  },
  "activated_at": "ISO-8601"
}
```
The trusted `expected` must be supplied by **an independent, protected runner**, not by the builder. It contains the current main SHA, actual blob SHAs, actual digest of current goal and feed snapshots and the SHA256 of exact receipt bytes. The delivered artifact contains `NAYA-ACTIVATION-RECEIPT-SHA256:<digest>`. The verifier rejects missing/mismatched/expired entries. The pure function does not itself fetch GitHub or calculate cryptographic hashes.

**Security warning:** Anyone can fabricate a plausible receipt JSON **and matching expected object** if you let the builder supply both. This module is not a trusted gate until the runner obtains the expected values from GitHub itself and computes/validates the exact receipt digest; even then it verifies provenance/freshness, **not cognition**. A token named `ACTIVATED` is never authority.

## Tests and falsifiers
Run `node --test tools/qa/activation_receipt_consistency.test.mjs`.
Cases: valid (review-eligible only), missing receipt, missing expected state, changed main, changed design, changed blocks, changed goals, changed feed, expired 4h, future time, missing deliverable citation, missing proof plan, wrong status and malformed trusted receipt digest. A test of this function on sample data is **not** CI integration or production proof.

## Integration path — Naya 4 / Naya 5 / Naya 2
1. Naya 4 resolves V2's nonexistent design-doctrine path to a ratified canonical source and decides where activation metadata is created *from live GitHub*; fill user/session/clock/goal/feed identity with witnessed values.
2. An independent/verifier-controlled runner generates `expected` values and receipt SHA256, invokes this logic before any builder product becomes delivery-eligible. Do **not** trust builder-supplied `expected`.
3. Naya 5 can wire this as a **separate prerequisite** to the existing design gate, preserving the design gate's scope and ownership. Only approved components compile; code is law, no second design component library.
4. Naya 2 independently tests false evidence, wrong read-state and the actual rendered design/user outcome. Builder cannot certify own elite score.
5. Human Director ratification and protected workflow changes go through existing gates. No merge, CI, deploy, credentials or score uplift from this draft alone.

**One next action:** Independent Naya 4/Naya 5 review this sample against the latest V2 and live 58-block branch, correct missing doctrine path, and integrate the smallest witness-bound pre-delivery gate under existing ownership.
