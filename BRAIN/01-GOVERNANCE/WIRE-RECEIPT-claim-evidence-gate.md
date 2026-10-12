# WIRE RECEIPT — claim-evidence gate (anti-citogenesis)

**Wired:** 2026-10-11 ~10:05Z, wire lane (Naya 2's team), night shift.
**Mechanism:** PR #2325 — anti-citogenesis claim-evidence adjudicator
(`tools/check_claim_evidence.py`), built and tested by Naya 5, explicitly
parked as CODE-ONLY ("not wired into CI … enforcement is a separate
activation").
**Wire PR:** stacked on `naya5/truth-claim-evidence-gate` — activates when
the mechanism merges first, then the wire.

## What was CODE-ONLY

The adjudicator is a pure function: claim text + structured evidence in,
verdicts out. Nothing in any operating path fed it real PR prose. A PR body
could claim "independently verified" on nothing but the author's own note
and no mechanism would object — the exact citogenesis defect class the
team's standing law forbids (internal repetition is not independent
corroboration).

## What the wiring adds

- `tools/scan_pr_claim_evidence.py` — the caller the mechanism scoped out.
  Extracts the author seat (`Seat:` line), harvests evidence items from PR
  prose (test paths, CI run ids near run/CI cues, seat mentions near
  review cues, commit SHAs, smart-note ids), and feeds them to
  `check_claim_evidence.adjudicate`. Never invents evidence; extraction
  limits are documented in the module.
- `.github/workflows/claim-evidence-gate.yml` — enforcement gate on the
  PR merge path. Runs on every `pull_request` event (no paths filter —
  the trigger is the prose, not the files). Bodies with no attestations
  pass quietly.
- `tests/test_scan_pr_claim_evidence.py` — 19 tests incl. negative
  controls.

## Operating path now protected

The PR merge path for **all** pull requests. Trigger: any PR body
containing a verification attestation ("independently verified",
"independent verification", "verified by", "proven"). Block:
`claim-evidence-gate` red — the attestation lacks admissible independent
evidence (self-attestation, repetition, phantom test path, bare claim).
Defect class: citogenesis in PR prose.

## Proof (wire-lane standard)

- Live fire on synthetic PR bodies: self-attested "independently verified"
  → exit 1 BLOCKED; bare "proven" → exit 1 BLOCKED; phantom test path →
  exit 1 BLOCKED; existing test path → exit 0; CI run id → exit 0;
  other-seat review ("verified by Naya 4") → exit 0; attestation-free body
  → exit 0 quiet; code identifier (`outcome_verified`) → no trigger.
- Fail-closed: unreadable body → exit 2; adjudicator unimportable →
  exit 2 at import. The gate goes red, never silently green.
- 19/19 caller tests green; 20/20 mechanism tests green (reproduced).
- Workflow parsed as YAML on the wire head before the PR opened.

## Failure mode if the wiring breaks

- Invalid workflow YAML → the gate never runs (a gate that never ran is
  not a gate that passed). Guard: YAML parsed pre-merge; CI-visible.
- Extractor misses an evidence cue → attestation fails closed (red) until
  the author cites evidence the extractor recognizes or softens the claim.
  Noisy-red beats silent-green for this defect class.
- Adjudicator semantics change → the caller's test suite pins the
  contract (19 tests); CI runs both suites on every PR touching the gate.

## How to verify it is still connected

1. Open any PR whose body says "independently verified" with no evidence
   → `claim-evidence-gate` must go red with the verdict reasons.
2. Amend the body to cite an existing test path → the check must go green.
3. `python3 tools/scan_pr_claim_evidence.py --body-file <file> --repo .`
   reproduces the verdict locally; exit codes 0/1/2 per the contract above.

## What remains unwired

- Per-attestation evidence linkage (the adjudicator pools evidence across
  one text by design; one real test cited once covers a second bare
  attestation — documented overclaiming, future work).
- `repeats` auto-detection across note chains (caller's documented limit).
- Activation itself: the gate enforces only after the wire PR merges to
  main — until then it is WIRED-AT-SEAM, DORMANT-PENDING-MERGE.
