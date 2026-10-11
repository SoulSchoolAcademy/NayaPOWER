# WIRE RECEIPT — D29 boundary-claims gate (accountability path)

**Mechanism:** D29 Environment–Scheduler–Worker Responsibility Boundary
(`drift_canary/d29_boundary.py`, PR #2184) — built + tested, CODE-ONLY at
build time. The module's own docstring stated it was "NOT wired into
kernel/, KNOW, LAW, ACT, or any live path."
**Wired by:** Naya 2 WIRE lane, night shift 2026-10-11. **Branch:**
`naya2/wire-d29-boundary` (base: `naya4/d29-boundary-fixture` @
`1c760c7908201e36ba2f03256a73a2609b78fbb5`; live tip at wire time
`57e935c1b44b10fcc27a80f8c99fc9ddb2e69440`).

## Operating path protected

The incident-accountability path. **Trigger:** any PR touching the
accountability path (`drift_canary/d29_boundary.py`, its tests, the gate,
the manifest, the gate tests, or the workflow itself) or any push to
`main` touching those paths → workflow `d29-boundary-gate` runs the
gate's suite, then fires the gate. **Block:** gate exit != 0 reds the run.
**Defect class:** a boundary claim resting on false blame — an incident
assigned to the scheduler or worker when the independent evidence says
the environment was down, or any component converting its own failure
into another component's assumption.

## What was added (5 files, +0/−0 elsewhere)

- `tools/d29_boundary_gate.py` — the gate. Loads the REAL D29 mechanism
  (sys.modules pre-registration before exec, repo-root on sys.path, API
  surface check, cleanup on load failure). Runs the fixed canary FIRST:
  (A,6) with hostile false-blame labels must stay ENVIRONMENT_BLOCKER/
  ENVIRONMENT; (B,7) — a parameterization no claim uses — must stay
  SCHEDULER_STARVATION/SCHEDULER; (C,6) must stay WORKER_NONPROGRESS/
  WORKER; every probe also passes the mechanism's own ledger cross-check.
  Then cold-judges each manifest claim: rebuilds the scenario with the
  real `run_case`, runs `verify_against_ledger`, and requires the
  claimed verdict AND controller to match exactly. Exit 0 = PASS /
  explicit DORMANT; exit 1 = VIOLATION; exit 2 = BROKEN fail-closed.
- `tools/d29_boundary_manifest.json` — the handoff artifact. Empty
  `claims` today → explicit DORMANT. Carries the claim schema plus a
  worked fraud (`_example`: A/6 claimed SCHEDULER_STARVATION) and a worked
  honest (`_example_honest`: C/6 → WORKER_NONPROGRESS). First claim merged
  activates enforcement.
- `.github/workflows/d29-boundary-gate.yml` — fires the gate on the
  accountability path (PR + main push); runs the gate suite first.
- `tests/test_d29_boundary_gate.py` — 13 tests: 6 against the real
  mechanism (dormant, honest C, honest B, fraud blocked, false-blame
  immunity, controller-mismatch violation) + 7 sabotage negative controls
  via fake-mechanism injection (blind engine, masquerade engine keyed to
  the manifest, missing file, changed API surface, broken ledger
  cross-check, corrupt manifest, malformed claim).
- This receipt.

## Proof (real bytes, not theater)

- Gate suite: **13/13 green** (battery venv, real #2184 mechanism bytes).
- Mechanism dogfood: the mechanism's own suite **13/13 green** on the
  combined tree (run locally; the #2184 base predates main's
  `drift_canary/liveness.py`, so its test file needs main's package to
  collect — noted below, owned by the merge lane).
- Fire battery on the combined tree (real mechanism): **9/9** — empty
  manifest → DORMANT exit 0; A/6 claimed SCHEDULER_STARVATION → BLOCKED
  exit 1 naming ENVIRONMENT_BLOCKER; A/6 with false-blame labels claimed
  SCHEDULER_STARVATION → BLOCKED exit 1 (labels ignored); C/6 and B/6
  honest claims → certified exit 0; corrupt manifest → exit 2; mechanism
  deleted → exit 2; blind always-UNDETERMINED engine → canary FAILED exit
  2; masquerade engine returning manifest-claimed values → canary (B,7)
  FAILED exit 2.
- 3.11-safety: tokenizer-scanned, zero f-strings, no 3.12-only constructs
  in either new code file.

## Honest state

**WIRED-AT-SEAM, AWAITING CLAIM CONTENT.** The gate is on the operating
path and proven to block real violations, but the manifest registers zero
claims — no boundary claim exists on the path yet, and this lane does not
invent any. Dormant is explicit; no false green. The gate activates the
moment #2184 merges (mechanism present on main) and the first claim is
registered.

## Failure mode if the wiring breaks

- Gate file deleted / workflow disabled → claims go unjudged silently.
  Detection: the manifest's `_note` names the workflow; the merge-protocol
  watch flags workflow deletions on the accountability path.
- Mechanism file deleted in a PR → canary load fails → exit 2 BROKEN —
  loud, and the mechanism's own suite gate reds independently.
- Mechanism API changed → API-surface check raises MechanismMissing →
  exit 2, never a silent pass on a neutered module.
- A claim registered for a scenario the mechanism cannot reproduce →
  judgment raises → exit 2 (fail-closed), not a pass.

## How to verify it's still connected

1. `python tools/d29_boundary_gate.py --json` → `DORMANT` (exit 0) while
   the manifest is empty; register the `_example` fraud as a claim →
   `VIOLATION` (exit 1) naming ENVIRONMENT_BLOCKER/ENVIRONMENT.
2. Check the `d29-boundary-gate` workflow ran on the last
   accountability-path PR and on the last main push touching the path.
3. Re-run the gate suite: `python -m pytest tests/test_d29_boundary_gate.py -q`
   → 13/13 (needs the #2184 mechanism bytes beside the gate).

## What this does NOT do

Invent boundary claims; touch the D29 module or its suite (owner lane
stays clean); duplicate the mechanism's own CI gate; merge anything.
**NO MERGE — Shawn pulls triggers.**

## Known condition (not introduced by this wire)

The #2184 base branch predates main's `drift_canary/liveness.py`, so the
mechanism's own test file cannot be collected on the stacked tree until
the build branch rebases onto current main. The gate and its suite do not
need liveness and run clean on the stack. Rebase ownership: build/merge
lane.
