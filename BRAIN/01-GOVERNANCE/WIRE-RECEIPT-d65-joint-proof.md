# WIRE RECEIPT — D65 joint-proof qualification gate

**Seat:** Naya 2 · wire lane · night shift 2026-10-11
**Stacks on:** PR #2327 (D65 mechanism: strongly connected invariant groups, AER-LIVE-10).
**Plain words:** the D65 law knew how to judge a cyclic invariant group, but nothing ever asked it to.
Now the drift-canary CI path does — every joint-proof claim is cold-judged by the real engine.

## The gap (why this exists)

PR #2327 shipped the D65 mechanism as executable law — `drift_canary/strongly_connected_groups.py`
(694 lines), 38 tests, the doctrine doc — and declared itself CODE-ONLY in its own docstring:
"Wiring to D64's DEFERRED seam and to CI is the wire lane's call." A verifier that never runs on a
live path is a document, not a protection. Tonight's wire lane closed the call: D65 was the last
unwired directive of the D55–D65 AER-LIVE series; every other member already has its wire PR.

## What was built (one PR, additive only — zero changes to the mechanism)

- **`tools/d65_joint_proof_gate.py`** — the gate. Every claim in the manifest is rebuilt from its own
  model bytes into a `JointDeclaration` and cold-judged by the REAL engine (`verify_joint`). The
  claimant's asserted verdict (one of REPEATABLE_PROVEN / DEADLOCK_IN_SCOPE / LIVELOCK_COUNTEREXAMPLE /
  EXIT_POSSIBLE_NOT_GUARANTEED / JOINT_UNDETERMINED) must match the engine's recomputed judgment
  exactly. Dogfood on every judged verdict: the verdict's model digest must equal the digest of the
  model actually judged, the verdict's group must name the declared joint, and the canonical encoding
  must be byte-stable. Exit contract: 0 PASS / 0 DORMANT (explicit, never a false green) /
  1 VIOLATION (the law refuses the claim — self-certified authority, digest mismatch, spurious joint,
  member-authorized replenishment, invented repeatability, exit conflation) / 2 BROKEN (fail-closed:
  corrupt manifest, unknown assertion, missing mechanism, broken engine). The gate never pre-checks
  the digest — the engine's verdict is the authority.
- **`tools/d65_joint_proof_manifest.json`** — the claim register. Ships with zero active claims
  (DORMANT by design) plus a worked `_example`: a zero-progress closed cycle with an honest digest,
  asserted REPEATABLE_PROVEN — the naive checker's exact fraud. Registered as a claim, the gate
  BLOCKS it: the engine computes LIVELOCK_COUNTEREXAMPLE.
- **`tests/test_d65_joint_proof_gate.py`** — 18 tests against the real engine: dormant states, honest
  positive claims (exit-possible, closed-cycle repeatable), honest refusal records, and the violation
  battery (worked-example fraud, livelock-as-repeatable, self-certified authority, digest tamper,
  deadlock misjudged as repeatable, member-authorized replenishment) plus the fail-closed battery
  (corrupt manifest, duplicate ids, unknown assertion, malformed model, missing mechanism) and a
  dogfood test proving a verdict for another model is rejected.
- **`.github/workflows/d65-joint-proof-verification.yml`** — runs the gate tests + the gate itself
  on pull_request and push-to-main for paths touching the mechanism, the gate, the manifest, the
  gate tests, or the workflow file.

## Proof (wire-lane standard — both directions, real violation)

- GREEN: 18/18 gate tests pass; 38/38 mechanism tests pass on the stack; workflow YAML parses with
  pull_request + push triggers; the exact CI sequence (`pytest` then `gate --json`) exits 0 —
  DORMANT on the shipped manifest, PASS on an honestly-asserted EXIT_POSSIBLE_NOT_GUARANTEED claim.
- RED: the manifest's worked example registered as a claim → exit 1 VIOLATION —
  `asserted=REPEATABLE_PROVEN actual=LIVELOCK_COUNTEREXAMPLE`, naming the exhibited zero-progress
  cycle and the mechanism's own notes. A real violation gets blocked; the wiring is not bypassable
  from the manifest side (any divergent assertion dies the same way).

## Failure modes (honest)

- **Workflow file deleted** → the path is unwired; the receipt's verify-still-connected line says
  re-add it. No silent coverage: the check simply stops running.
- **Mechanism deleted while claims exist** → exit 2 BROKEN, fail-closed. The gate never invents
  the engine and never defaults an unknown.
- **Manifest hand-edited with a bad digest** → the engine refuses (JOINT_UNDETERMINED, digest
  mismatch) and any positive assertion BLOCKS. The worked example's digest was computed by the
  real `make_declaration` — hand-editing a digest is exactly the tamper the law refuses.
- **CI-side only:** the gate judges the manifest register, not live D64 DEFERRED seams — wiring the
  D64 deferred-joint seam itself (declaring real joint groups from real D64 runs) is follow-up work
  for the owning lane, not this wire.

## Operating path now protected

The drift-canary governance-verification CI path — trigger: any PR touching
`drift_canary/strongly_connected_groups.py`, the gate, its manifest, or its tests; block:
`joint-proof-verification` red. Defect class: joint-proof qualification claims the D65 law refuses
(self-certified authorities, digest mismatches, spurious joints, member-authorized replenishments,
invented repeatability over livelocks, exit conflation, ungrounded groups).

Verify-still-connected: `python tools/d65_joint_proof_gate.py --json` exits 0 DORMANT on a claim-free
tree; registering the manifest's worked `_example` as a claim exits 1 naming the livelock fraud;
claims present with the mechanism deleted exits 2.

## What this does NOT claim

- Not merged (merge lane owns the queue; this stacks on #2327).
- Not a verdict that any real joint group qualifies — the manifest ships claim-free; the mechanism
  records judgments, seats make the claims.
- Not the D64 DEFERRED-seam wiring — that follow-up belongs to the owning lane.
