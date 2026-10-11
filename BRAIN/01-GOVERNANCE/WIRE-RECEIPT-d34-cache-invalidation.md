# WIRE RECEIPT — D34 cache-invalidation claims gate

**Wire PR:** (this PR) `naya2/wire-d34-cache-invalidation`, stacked on #2217
**Mechanism:** `drift_canary/d34_cache_invalidation.py` @ #2217 head
`f6de2d3497` — built + tested (19/19 on exact head bytes; real-D33
composition proven on real #2212 bytes by the build lane), CODE-ONLY until
now: zero live consumers on main or any open branch.
**Directive:** D34 — Selective Cache Invalidation and Intelligence
Preservation (the memory law): preserve history, recompute qualification,
invalidate stale authority, refresh only what changed. A change in evidence
eligibility changes the right to *use* a conclusion — never rewrites
history. Discoverability != certifiability.

## What was wired (5 additive files, zero mechanism changes)

- `tools/d34_cache_invalidation_gate.py` — replays every registered
  scenario's ordered ops (register source/claim, add projection, commit
  eligibility change, serve, refresh, authorize_act, verdict/status
  assertions, reconcile) against the REAL `IntelligenceStore` built from
  the live tree. Asserted outcomes must match the engine exactly.
  Exit 0 PASS / 0 DORMANT / 1 VIOLATION / 2 BROKEN (fail-closed).
- Fixed sharpest-sequence canaries, run first every run:
  C1 stale-as-current refused on an authority route after revocation;
  C2 generation-bound compare-and-swap refuses a stale refresh
  (`StaleGenerationError` — a delayed refresh may never republish an
  earlier PASS over a later revocation);
  C3 ACT commit-boundary re-check refuses at a stale generation
  (TOCTOU close). A neutered engine fails a canary -> exit 2, never a
  blind pass.
- `tools/d34_cache_invalidation_manifest.json` — ships with zero live
  scenarios = explicit DORMANT (canary still runs every CI run), plus a
  worked fraud `_example` and a worked honest `_example_honest`
  (documentation + gate self-test, never judged as live claims).
- `tests/test_d34_cache_invalidation_gate.py` — gate tests: shipped
  manifest well-formed-and-DORMANT (the owning lane registers real
  scenarios without editing tests), fraud/honest worked examples,
  three sharpest frauds (stale ACT authorization, delayed-refresh
  republication, historical receipt served as current), malformed
  inputs -> exit 2, sabotage controls (missing mechanism -> exit 2;
  neutered always-serve engine fails the canary).
- `.github/workflows/d34-cache-invalidation-gate.yml` — CI job on the
  drift-canary governance path: gate tests + mechanism suite + the gate
  on PRs touching the mechanism, gate, manifest, tests, or workflow.

## Proof (wire-lane standard)

- Mechanism: 19/19 green on the exact #2217 head bytes; real-D33
  composition + hostile-engine fraud controls green per the build lane's
  12:25Z receipt (89/89 with real D33 bytes).
- Gate suite green on the combined tree (see CI).
- Fire battery on real bytes: fraud (stale served as current) -> exit 1
  VIOLATION naming `asserted=SERVE_CURRENT actual=REFUSE_STALE`; honest
  two-phase choreography -> exit 0 PASS; corrupt manifest -> exit 2;
  missing mechanism -> exit 2; neutered engine -> canary fails -> exit 2.
- Shipped manifest -> exit 0 DORMANT.
- L215 live both-directions on the wire branch (see PR checks).

## Operating path now protected

The drift-canary governance CI path — trigger: `d34-cache-invalidation-gate`
check on PRs touching the mechanism, gate, manifest, or tests; block: check
red. Defect class: stale qualifications republished as current, history
rewritten, delayed refreshes republishing earlier PASSes over later
revocations, ACT authorized on stale generations, successor/index/summary
surfaces serving revoked authority.

## Failure mode if the wiring breaks

- Gate red on a PR touching watched paths = a registered claim the D34
  law refuses (or a broken gate/manifest) — the PR is blocked until the
  claim is corrected or the gate repaired.
- Workflow deleted/disabled = the mechanism returns to CODE-ONLY silently;
  verify-still-connected: `python tools/d34_cache_invalidation_gate.py`
  exits 0 DORMANT on a claim-free tree; registering `_example` as a live
  scenario exits 1 naming the refused serve decision.

## Verify it's still connected

```
python tools/d34_cache_invalidation_gate.py            # expect: DORMANT, exit 0
python -m pytest tests/test_d34_cache_invalidation_gate.py -q -p no:cacheprovider
```

## Boundary

CI governance path only. Runtime kernel/KNOW/LAW/ACT wiring needs Shawn's
word per the mechanism's own docstring ("NOT wired into kernel/, KNOW,
LAW, ACT, or any live path. Wiring needs Shawn's word."). The
`D33EngineAdapter` real-engine composition test stays DORMANT until #2212
merges; the wire activates fully when #2217 merges and Naya 5 registers
the first real scenario. No merge from the wire lane.
