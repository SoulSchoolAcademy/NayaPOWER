# One Schema, One Protected Truth Provider — the Unified Activation Gate (a Builder Cannot Self-Authenticate, Ever)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0799-unified-activation-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6085006645 (Naya 1 engineering action, 2026-10-09T16:30:46Z), 6085266887 (Naya 4 builder-seat confirm, 2026-10-09T16:47:15Z), 6085304830 (Naya 2 scope-limited confirm, 2026-10-09T16:49:39Z); real CI run 37959342664 (14/14 rows HOLD).

## ✦ IN A NUTSHELL

Three activation checkers were drifting: PR #1979's `drink_first_gate.py` (v1, six fail-open defects), PR #1974's `.mjs` QA falsifier (v2), and `design_gate.py::check_activation` (structural, delegated deep verification). On 2026-10-09 Naya 1 unified them into a single enforcement point — `tools/activation_gate.py` on branch `naya5/unified-activation-gate @ cae9cee1` — built on two rules: ONE schema (`naya.activation.receipt.v2`, v1 retired for enforcement; canonical template `NAYA-ACTIVATION/ACTIVATION-RECEIPT-V2.json`) and ONE protected truth provider (`resolve_truth()` resolves the repository, the live main SHA, and canonical source blob SHAs ITSELF from `GITHUB_REPOSITORY` + `GITHUB_TOKEN` + the live API — no caller flag may supply truth). Proven in real CI, not local: workflow run 37959342664, job 113917887952, conclusion success, 14/14 rows HOLD — lawful PASS; fabricated, stale (genuine old commit `c791b7798c34`), wrong-repo, abbreviated-SHA, expired, future, v1-schema, unregistered-source, fingerprint-mismatch, unactivated, tampered-bytes, and missing-citation all REJECTed; the self-minted-truth alternate route yields `CANDIDATE-LOCAL-*`, never PASS. All three lanes confirmed the agreement. Retirement map: `drink_first_gate.py` SUPERSEDED (defects 1–6 closed); `.mjs` STAYS as #1974's QA falsifier lane; `design_gate.py` keeps the structural layer.

## HUMAN NOTE

We had three different tools checking whether a Naya was properly activated, and they disagreed — one of them had six ways to fail open. Instead of patching each one, Naya 1 replaced all three with a single checkpoint built on two non-negotiable rules: there is exactly one official form (v2 — the old v1 form is retired), and the checkpoint looks up the truth itself from the source — it never accepts a builder's own claim about what the truth is. Then the new checkpoint was tested against 14 attack scenarios in real CI (not on someone's laptop): fake receipts, stale commits, wrong repositories, tampered bytes, expired or future dates — every forgery was rejected, the real thing passed. The three lanes that owned the old tools all signed off. The lesson: when enforcement points drift, unify them — and the enforcement must fetch its own truth, because a builder can never be allowed to authenticate itself.

## CHILD NOTE

Imagine three guards at three doors, each checking IDs differently — and one guard's rulebook has six holes. The fix isn't to patch all three rulebooks; it's to build ONE door with ONE rulebook that follows two rules: only one kind of ID is valid, and the guard calls the ID office himself to check it — nobody gets to bring their own "yes, I'm allowed" note. That's what happened here: one door, one rulebook, and the guard always calls to verify.

## GRANDMA NOTE

Three people were checking the same thing three different ways, and one of them kept waving bad cases through. So they set up a single checkpoint: one official form, and the checker verifies everything himself against the real records — he doesn't take anyone's word for it. It passed 14 different cheating tests. One check, done right, beats three checks done differently.

## NAYA NOTE

Standing enforcement architecture (three-lane agreement, 2026-10-09): the activation enforcement point is `tools/activation_gate.py` with ONE schema (`naya.activation.receipt.v2`) and ONE protected truth provider (`resolve_truth()`). Core doctrine — **a builder cannot self-authenticate, ever**: no caller flag may supply truth; the provider resolves repository, live main SHA, and canonical blob SHAs itself. Supporting rules: closed-world `CANONICAL_SOURCES` registry (unregistered `loaded` keys fail CI); citation marker always required, digest-bound to exact receipt bytes; self-served truth (`--mode local`) yields `CANDIDATE-LOCAL-*`, never PASS. This closes the circular-verification hole Naya 2's adversarial testing found (gate trusting caller-provided SHA + receipt). Explicitly open items (do NOT treat as closed): PR #1969's `verify_activation_provenance.py` vs `resolve_truth()` — supersede/complement/merge is Naya 1 + builder lane's call; deliverable-side closed-world component check stays the design gate's lane; wiring this gate into the pre-delivery workflow + required status check is Shawn's authority; live goals/feed digest binding stays in #1974's QA lane (digest race makes it flaky at the delivery boundary). Related: DRINK-FIRST law (activation before service), SN-0351 (sign-in/out law).

## MACHINE NOTE

```json
{
  "rule": "ONE-SCHEMA-ONE-PROVIDER-ACTIVATION-ENFORCEMENT",
  "enforcement_point": "tools/activation_gate.py (branch naya5/unified-activation-gate @ cae9cee1, CANDIDATE)",
  "schema": "naya.activation.receipt.v2 (v1 retired for enforcement; template NAYA-ACTIVATION/ACTIVATION-RECEIPT-V2.json)",
  "truth_provider": "resolve_truth() — resolves repository, live main SHA, canonical source blob SHAs itself from GITHUB_REPOSITORY + GITHUB_TOKEN + live API; no caller-supplied truth, ever",
  "doctrine": "a builder cannot self-authenticate, ever",
  "proof": "real CI run 37959342664, job 113917887952, conclusion success; 14/14 rows HOLD (fabricated/stale/wrong-repo/abbreviated-SHA/expired/future/v1-schema/unregistered-source/fingerprint-mismatch/unactivated/tampered-bytes/missing-citation REJECTed; self-minted-truth route yields CANDIDATE-LOCAL-*, never PASS)",
  "retirement_map": {"drink_first_gate.py": "SUPERSEDED (defects 1-6 closed)", ".mjs QA falsifier": "STAYS (#1974 lane)", "design_gate.py": "keeps structural layer"},
  "open_items": ["verify_activation_provenance.py vs resolve_truth() resolution (Naya 1 + builder lane)", "CI workflow wiring + required status check (Shawn's authority)", "deliverable-side closed-world component check (design gate lane)", "goals/feed digest binding (#1974 QA lane)"],
  "closed_world_registry": "CANONICAL_SOURCES — unregistered loaded keys fail CI",
  "citation": "citation marker always required, digest-bound to exact receipt bytes",
  "related": ["SN-0351", "drink-first-law", "PR #1979", "PR #1974", "PR #1969"]
}
```
