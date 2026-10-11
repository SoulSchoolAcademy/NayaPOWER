# WIRE RECEIPT — D55 claims gate (recovery-claims path)

**Mechanism:** D55 safety-vs-liveness classifier (`tools/safety_liveness_classifier.py`,
PR #2302) — built + tested, CODE-ONLY at build time.
**Wired by:** Naya 2 WIRE lane, night shift 2026-10-11. **Branch:** `naya2/wire-d55-claims-gate`
(base: live tip `57e935c1b44b10fcc27a80f8c99fc9ddb2e69440`).

## Operating path protected

The recovery-claims path. **Trigger:** any PR touching the recovery path
(`tools/safety_liveness_classifier.py`, `tools/bounded_recovery_liveness.py`,
the gate, the manifest, the gate tests, or the workflow itself) or any push
to `main` touching those paths → workflow `safety-liveness-claims` runs the
gate's suite, then fires the gate. **Block:** gate exit ≠ 0 reds the run.
**Defect class:** a recovery claim resting on fraud — heartbeat fraud
(service mistaken for progress) or liveness fraud (a legitimately prohibited
action misclassified as a liveness failure).

## What was added (5 files, +0/−0 elsewhere)

- `tools/safety_liveness_gate.py` — the gate. Rebuilds each claim's obligation
  from the manifest's declared evidence and judges it with the REAL D55
  classifier. Exit 0 = PASS / explicit DORMANT; exit 1 = VIOLATION blocked;
  exit 2 = BROKEN (fail-closed).
- `tools/recovery_claims_manifest.json` — the handoff artifact. Empty `claims`
  today → explicit DORMANT. Carries the claim schema plus a worked
  heartbeat-fraud example. First claim merged activates enforcement.
- `.github/workflows/safety-liveness-claims.yml` — fires the gate on the
  recovery path (PR + main push).
- `tests/test_safety_liveness_gate.py` — 17 tests, fake-mechanism injection
  (deterministic on main, following the D28 gate precedent).
- This receipt.

## Proof (real bytes, not theater)

- Gate suite: **17/17 green** (battery venv).
- Fire battery on the combined tip + #2302-head tree (real classifier bytes):
  **9/9** — empty manifest → DORMANT exit 0; 100-heartbeat/0-progress claim of
  "healthy" → BLOCKED exit 1, fraud named `heartbeat fraud`; withdrawn-auth
  claim of "recovery_defect" → BLOCKED exit 1, actual `valid_hold`, fraud named
  `liveness fraud`; true healthy / true valid_hold → certified exit 0; corrupt
  manifest → exit 2; claims present with mechanism deleted → exit 2
  ("refusing to pass on defaults"); ungoverned disposition → exit 1;
  scheduler_defect surfaced as attention on a true claim, exit 0.
- The battery caught a REAL integration defect the unit tests could not: the
  classifier's `@dataclass` decorators require the module registered in
  `sys.modules` before `exec_module` — the gate now does this (and cleans up
  on load failure). Documented in the gate for future loaders (D56's
  `from_d55()` seam included).

## Honest state

**WIRED-AT-SEAM, AWAITING CLAIM CONTENT.** The gate is on the operating path
and proven to block real violations, but the manifest registers zero claims —
no recovery claim exists on the path yet, and this lane does not invent any.
Dormant is explicit; no false green. The gate activates the moment #2302
merges (mechanism present) and the first claim is registered.

## Failure mode if the wiring breaks

- Gate file deleted / workflow disabled → claims go unjudged silently.
  Detection: the manifest's `_note` names the workflow; the merge-protocol
  watch flags workflow deletions on the recovery path.
- Mechanism file deleted in a PR → gate exits 2 BROKEN (claims exist) — loud,
  and the mechanism's own suite gate (`safety-liveness-gate.yml`) reds
  independently. Defense in depth, no single point of silence.
- Classifier API changed → gate's `_load_mechanism` API-surface check raises
  `MechanismMissing` → exit 2, never a silent pass on a neutered module.

## How to verify it's still connected

1. `python tools/safety_liveness_gate.py --json` → `DORMANT` (exit 0) while
   the manifest is empty; register the `_example` claim → `VIOLATION` (exit 1).
2. Check the `safety-liveness-claims` workflow ran on the last recovery-path
   PR and on the last main push touching the path.
3. Re-run the fire battery: `python fire_battery.py` in the wire scratch
   (needs #2302's classifier bytes beside the gate) → 9/9.

## What this does NOT do

Invent recovery claims; touch the D55 module or its suite (owner lane stays
clean); duplicate the mechanism's own CI gate; merge anything.
**NO MERGE — Shawn pulls triggers.**
