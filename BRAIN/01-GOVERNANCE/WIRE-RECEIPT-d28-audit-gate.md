# WIRE RECEIPT — D28 assumption-audit gate

**Date:** 2026-10-11 ~08:00Z · **Lane:** Naya 2 wire (night shift)
**PR:** (wire PR number — branch `naya2/wire-d28-audit-gate`, off main @ `57e935c1`)
**Mechanism:** D28 independent fairness-assumption audit protocol (PR #2306,
`drift_canary/fairness_audit.py` + 19 tests) — built and tested 2026-10-11
07:25Z, CODE-ONLY at build time (author: "not wired into any live path").

## What was wired

The D28 audit is now the fail-closed authority behind a CI gate on the
fairness path:

- `tools/fairness_assumption_audit_gate.py` (new) — the gate. Exit codes:
  0 = PASS or explicit DORMANT (never claims "audited" when dormant);
  1 = VIOLATION blocked (rigged / unjustified / redundant / unestablished
  assumption, phantom registry id, bind refusal — the gate never invents
  justification fields); 2 = BROKEN (corrupt manifest — fail-closed).
- `tools/fairness_audit_manifest.json` (new) — the handoff artifact. Empty
  `audits` today; each entry fully specifies one audit (assumption ids,
  owner, status, justification, justification evidence, model footprint,
  claim context). The fairness lane fills entries as evidence lands; the
  day the first entry lands, enforcement activates with zero new wiring.
- `.github/workflows/fairness-assumption-audit.yml` (new) — runs the gate's
  test suite, then fires the gate, on PRs touching the fairness path /
  the D27 registry / the D28 module / the manifest, and on pushes to main.
- `tests/test_fairness_assumption_audit_gate.py` (new) — 14 tests, real
  asserts, incl. negative controls (sabotage must fail the suite).

## Operating path now protected

The fairness CI path: **trigger** = PR touching
`tools/fairness_assumption_audit_gate.py`, `tools/fairness_audit_manifest.json`,
`tests/test_fairness_assumption_audit_gate.py`, `tools/fairness_assumptions.py`
(D27 registry), `drift_canary/fairness_audit.py` (D28), or the workflow itself;
**block** = `fairness-assumption-audit` red. **Defect class:** a fairness
qualification resting on a dishonest assumption (the D28 directive's rig:
"the test was rigged, not the scheduler fixed").

## Proof (wire-lane standard — real violations, real bytes)

Independent mechanism verification (exact #2306 head `56f931fc`):
19/19 module tests green; 121/121 across the fairness lane; no duplicate
mechanism (the prover's `audit_assumption()` self-questionnaire is a
different mechanism by design, documented in the module). Independent killer
probe `fire-d28-killer.py`: 6/6 — rig rejected at G1 (evidence not ledgered),
rig rejected at G4 (exclusion unnamed), legit scoping passes, scheduler
self-justification rejected at G1, starvation trace vanishes under the rig
and returns without it, verdict names its model depth.

Integration fire battery `fire-d28-gate.py` on the combined #2306+#2295 tree
(real D28 module + real D27 registry FA-A1..FA-A4): 7/7 —
empty manifest → DORMANT exit 0 ("0 audits registered (4 assumptions in
registry); no audit performed"); rigged STABILIZED_ELIGIBILITY assumption →
exit 1 naming G4_NON_CIRCULARITY; empty evidence → exit 1 "refuses to invent";
legit scoping → exit 0 AUDIT_PASSED; corrupt manifest → exit 2 BROKEN;
phantom id FA-NOPE → exit 1; scheduler-owned → exit 1 at
G1_INDEPENDENT_JUSTIFICATION.

Gate's own suite on the main tree: 14/14 green; gate run on main → DORMANT
"mechanism not present on this tree", exit 0.

## Honest state

**WIRED-AT-SEAM, AWAITING AUDIT CONTENT.** The gate is on the operating path
and proven to block real violations, but the manifest registers zero audits
tonight — the D27 registry's assumptions (FA-A1..FA-A4) do not yet carry the
justification fields D28 requires, and the wire lane does not invent them
(the D28 author's explicit refusal, honored). No false green is possible:
dormant is explicit and the fairness path's verdicts do not cite the audit.

## Handoff (fairness lane)

Author the justification fields for FA-A1..FA-A4 (owner, status,
justification, independently-ledgered evidence names, model footprint,
claim context) as entries in `tools/fairness_audit_manifest.json`
(schema + worked example embedded). First entry merged → the gate's full
D28 audit activates on the next CI run. No new wiring needed.

## What this does NOT do

Invent justification content; modify the D27 registry or the D28 module
(both untouched — owner's lanes keep their reviews clean); merge anything
(merge freeze: scorecard + cross-seat review required; Shawn pulls triggers);
claim ENFORCED (the gate enforces nothing until the manifest carries audits).
