# WIRE RECEIPT — D65 strongly-connected groups gate

**Date:** 2026-10-11 ~10:10Z (night shift)
**Lane:** WIRE (Naya 2's team)
**Directive:** D65 — Strongly Connected Invariant Groups and Joint Proof Qualification (AER-LIVE-10)
**Build:** PR #2327 (`drift_canary/strongly_connected_groups.py`, 38/38 tests green) — BUILT AS CODE, unwired.
**Status after this wire:** WIRED-AT-SEAM, DORMANT-PENDING-MERGE. No merge from the wire lane — Shawn pulls triggers.

## What was wired

The D65 joint-proof verifier (`verify_joint`) onto the joint-proof CI path:

| File | Role |
|---|---|
| `tools/d65_strongly_connected_groups_gate.py` | The gate: judges each manifest claim against the REAL engine. Exit 0 pass/dormant, 1 violation, 2 fail-closed. |
| `tools/d65_strongly_connected_groups_manifest.json` | Claims register. Ships with `"claims": []` — explicit DORMANT, plus a worked `_example` (dormant, certifies if registered). |
| `tests/test_d65_strongly_connected_groups_gate.py` | 23 tests, fake-mechanism injection (mechanism not on this tree yet). |
| `.github/workflows/d65-strongly-connected-groups.yml` | The live path: runs on `pull_request` + `push: main`, path-filtered to the engine, its tests, the gate, the manifest, and itself. |

## Operating path now protected

The joint-proof CI path: any PR touching `drift_canary/strongly_connected_groups.py` (or its tests, the gate, or the manifest) must pass the gate, and every push to `main` touching those paths re-runs it. The first claim merged into the manifest activates enforcement with zero new wiring. The gate also covers D64's DEFERRED seam: a joint a D64 run defers can be registered as a claim here and is judged jointly, never member-by-member.

## Proof the wiring works (L215)

1. **Gate tests:** 23/23 green (fake mechanism).
2. **Fire battery (not committed):** the same gate judged against the REAL #2327 bytes (sha256-verified identical) — 7/7: honest claim certifies (exit 0); exit-swallowing blocked (exit 1); zero-progress spin asserted REPEATABLE_PROVEN blocked as progress-laundering (exit 1); tampered digest honestly asserted JOINT_UNDETERMINED certifies (exit 0); authority-is-a-member asserted REPEATABLE_PROVEN blocked as grounding-laundering (exit 1); dormant manifest exits 0; claims without the mechanism fail closed (exit 2).
3. **Shipped `_example`:** registers as a live claim and certifies (exit 0); flipping its asserted verdict to REPEATABLE_PROVEN blocks with exit-swallowing named (exit 1).
4. **TEMP-PROOF on the branch:** a temporary violating claim registered — the gate went RED (exit 1); reverted — explicit DORMANT (exit 0). Both directions proven; the temp claim is not in the PR.
5. **YAML parsed** as valid workflow; **fail-closed** proven (corrupt manifest → 2, unknown asserted verdict → 2, unknown transition kind → 2, bad presented_digest → 2, claims without mechanism → 2, engine raising → 2).

## What the gate blocks

- **Exit-swallowing:** asserting REPEATABLE_PROVEN where the engine finds EXIT_POSSIBLE_NOT_GUARANTEED — the exit dimension the engine keeps separate may not be collapsed (the spec's naive defect #4).
- **Progress-laundering:** asserting REPEATABLE_PROVEN where the engine exhibits a zero-progress cycle — repeatability of motion is not repeatability of progress.
- **Grounding-laundering:** asserting any grounded verdict where the engine refuses — authority is a member (the group would establish its own external facts), relation digest mismatch (the model swapped under the authorization), no authorized initial allocation. The minimal obstruction is named, never swallowed.
- **Refusal-laundering:** asserting JOINT_UNDETERMINED where the engine certifies — manufactured doubt where the model grounds.
- D65's distinctive coverage: cyclically-dependent invariant groups are proven jointly — no member may certify another, and the verifier computes every property from the presented complete transition relation instead of trusting pre-computed booleans.

## What remains unwired

- D65's build PR #2327 itself (open, unmerged) — this wire's gate goes DORMANT-fail-closed-safe until it lands; the first claim merged then activates enforcement with zero new wiring.
- D62 fix lane; #2294 (directive-register CLI, not gate-shaped); #2244 reqs; naya4/naya5 owner lanes (D29–D31, D33–D36 evidence PRs all still open).
- All wire PRs (including this one) await the merge lane. Until merged, every wire is DORMANT — CODE-ONLY at the wire layer per L215, honestly stated.
