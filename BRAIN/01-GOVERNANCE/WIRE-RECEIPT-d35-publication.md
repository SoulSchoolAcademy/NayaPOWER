# WIRE RECEIPT — D35 publication-boundary gate

**Directive:** D35 — Preventing Stale Qualifications From Being Republished
**Mechanism PR:** #2215 (`naya4/d35-stale-publication`), register status BUILT_AS_CODE
**Wire PR:** stacks on `naya4/d35-stale-publication` — additive only, zero mechanism changes
**Wired by:** Naya 2 night-shift WIRE lane, 2026-10-11. **No merge — the merge lane owns the queue.**

---

## Operating path now protected

The drift-canary governance-verification CI path — specifically the atomic
publication boundary. Any change touching `drift_canary/d35_publication.py`,
the gate, its manifest, its tests, or the workflow itself triggers the
publication-boundary check on `pull_request` / `push-to-main`; a red check
blocks the merge path.

**Defect class this blocks:** stale qualifications republished as current
authority — the D35 fraud: a worker reads a claim holding a *valid fencing
token*, the evidence is revoked, the worker's delayed write lands anyway
because "the token was valid." The token proves WHEN a worker read; it never
replaces the evidence-version check. Also blocked: write conflicts on a
moved projection head, scope-widened publications, forged tokens, sealed
successor packages that no longer reconcile, replayed smart-note events,
torn index pointers.

**What triggers it:** the publication-boundary check (CI workflow
`.github/workflows/d35-publication-gate.yml`) — gate tests, then the gate
itself on `tools/d35_publication_manifest.json`.

**What it blocks:** any merge whose publication scenarios diverge from the
D35 law (exit 1 VIOLATION), or any manifest/mechanism the gate cannot trust
(exit 2 BROKEN, fail-closed).

## Proof (both directions, real violation)

- **GREEN:** 22/22 gate tests pass; 25/25 mechanism tests pass on the stack;
  workflow YAML parses with `pull_request` + `push` triggers; the exact CI
  sequence (`pytest` then `gate --json`) exits 0 — DORMANT on the shipped
  manifest (zero active claims, explicit), PASS on an honestly-asserted
  stale-refusal scenario (the claimant says what the law will do and the
  engine agrees).
- **RED:** the manifest's worked example
  (`D35-WORKED-STALE-WRITE-AS-PUBLISHED` — worker W reads claim C at R5
  holding a valid fencing token; E1 revoked; W attempts publication)
  registered as a claim → exit 1 VIOLATION:
  `asserted=PUBLISHED actual=STALE_DEPENDENCY — qualification or evidence
  revision moved under the writer`. The naive checker's exact fraud is
  blocked, named in the mechanism's own words. A real violation gets
  blocked.

## Failure modes (if the wiring breaks)

1. **Workflow file deleted/renamed** — the path is unwired: the check stops
   running and stale publications face no gate. Detect: the file must exist
   at `.github/workflows/d35-publication-gate.yml` and the check must be
   required on the drift-canary path.
2. **Manifest gains claims the engine cannot construct** (e.g. qualifying
   on unknown evidence) — exit 2 BROKEN. This is fail-closed by design: a
   manifest asking for the impossible is untrustworthy, not a pass.
3. **Mechanism deleted while claims exist** — exit 2 BROKEN ("refusing to
   pass on defaults"). The gate never invents the engine.
4. **Engine invariant breaks** (`assert_invariant` fails after a scenario)
   — exit 2 BROKEN. PublishedCurrent(P) ⇒ ValidDependencies(P, now) is
   re-checked by the gate on every judged scenario.
5. **Manifest corruption / duplicate claim ids / unknown assertions or
   ops** — exit 2 BROKEN. Unknown is never defaulted.

## Verify it is still connected

```bash
python tools/d35_publication_gate.py --json        # expect exit 0 DORMANT
python -m pytest tests/test_d35_publication_gate.py -q -p no:cacheprovider  # 22 passed
ls .github/workflows/d35-publication-gate.yml      # must exist
```

Registering `tools/d35_publication_manifest.json`'s `_example` under
`claims` must exit 1 naming `STALE_DEPENDENCY`.

## Files

| File | Role |
|---|---|
| `tools/d35_publication_gate.py` | The gate: cold-executes each registered publication scenario (setup steps + one attempt) on a fresh `PublicationAuthority` and requires asserted == engine outcome. Exit 0 PASS / 0 DORMANT / 1 VIOLATION / 2 BROKEN. |
| `tools/d35_publication_manifest.json` | The scenario register. Zero active claims (DORMANT by design) + worked fraud `_example` + worked honest `_example_honest`. |
| `tests/test_d35_publication_gate.py` | 22 tests against the real engine: DORMANT/PASS/VIOLATION/BROKEN across every surface (summary CAS, smart-note replay, index pointer, successor package, forged token, scope, write conflict). |
| `.github/workflows/d35-publication-gate.yml` | CI: gate tests + gate on `pull_request` / `push-to-main` for the five paths. |
| This receipt | Operating path, proof, failure modes, verify-still-connected. |
