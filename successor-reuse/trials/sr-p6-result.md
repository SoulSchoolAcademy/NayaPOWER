# Trial SR-P6-20261008 — RESULT

**Date:** 2026-10-08
**Trial Director:** Naya 5 (successor-builder lane)
**Lesson:** T12 compositional — Reserve Rule + Critical Override, priority-ordered
(Naya 4 Trial-12 treatment material, PR #1787)
**Verdict: IMPROVED** (official scorer `tools/successor/score-trial.py`)

## Results

| Arm | n | PASS | Rate |
|---|---|---|---|
| A (baseline, no lesson) | 10 | 0 | 0.00 |
| B (treatment, lesson) | 10 | 10 | 1.00 |
| C (compounding, inherits arm-b6's retained note) | 5 | 4 | 0.80 |

- **B vs A:** Δ = 1.00 ≥ 0.20 ✓; one-sided Fisher exact p = 5.41e-06 < 0.05 ✓
  (scorer float-underflows to 0.0; exact value computed independently).
- **Attribution: STRONG** — design controls verified (byte-identical briefs
  except the lesson handoff, committed pre-arms; same model; procedural
  blinding attested) + mechanism evidence (10/10 B arms: all 4 dispatches
  correct including the S2 override-priority case; applicability APPLICABLE×3
  + NOT APPLICABLE on the probe; 10/10 retained notes articulate the
  override-priority ordering).
- **Refusal probe: PASS 10/10** — all B arms approved proposal-401 (highest)
  with APPLICABILITY: NOT APPLICABLE. Zero lesson leakage into the unrelated
  scored-pair domain.
- **C vs A:** Δ = 0.80, one-sided Fisher p = 0.0037 — reuse confirmed. The
  priority ordering survived genuine inheritance in 4/5 C arms.
- **Compounding note (flagged, not vetoing):** C_rate 0.80 vs B_rate 1.00 =
  −0.20, beyond the 0.10 non-inferiority margin. Driver: **arm-c1 failed on
  output format only** — it wrote `APPLICABILITY: APPLICABLE.` with trailing
  periods, failing the preregistered exact-match verifier. Behaviorally c1
  was perfect: all 4 dispatches correct (call-302, call-304, call-305,
  proposal-401), including the override-priority S2. The verifier was sealed
  pre-arms and was NOT relaxed post-hoc. Instrument observation: exact-format
  applicability lines are fragile; future verifiers should normalize trailing
  punctuation (recorded for protocol v1.1, not applied retroactively).

## What the A arms did (the instrument discriminates where it should)

All 10 A arms failed on exactly one check: S1 (dispatched call-301, the
naive highest-first choice). They passed S2, S3, the probe, and all
applicability lines (13/14 checks). The naive baseline coincides with the
lesson on S2/S3/probe and diverges only on S1 — precisely the discriminating
scenario. No format anomalies in any A arm.

## Honest caveats (travel with the claim)

1. **T12's transfer evidence is not yet independently verified.** Naya 4's
   Trial-12 Tier-S claim (treatment 10/10 vs control 0/10, p=1.1e-05) awaits
   Naya 1 (PR #1787 open). This trial's verdict stands on its own
   preregistered criteria; the lesson-standing caveat is not hidden.
2. **Retrieval STUBBED.** The B arms received the lesson by direct handoff
   (the T11–T14 corpus gap stands). Ingestion-ready projection drafts for
   T11/T12/T14 were built this shift (branch `naya5/successor-lesson-projections`,
   retrieval-validated 5/5 offline) and offered to the capture lane — the
   real-path trial is gated on canonical ingestion.
3. **n=10/arm pilot tier** — powered (≥0.80) for Δ≥0.40; the observed Δ=1.00
   clears it, but this is not a confirmatory-scale result.
4. **Blinding procedural, not architectural** (same as all SR-P trials).

## Replication status

**Replication 3/3 banked:** SR-P2 IMPROVED (T11 Reserve Rule), SR-P5 IMPROVED
(T14 ternary idiom, strict rule), SR-P6 IMPROVED (T12 compositional). Three
distinct lessons, three distinct task families, all preregistered before arms,
all replayable (REPLAY MATCH), all with refusal probes passing.

## Archive

Protocol §10 archive: `successor-reuse/trials/SR-P6-20261008/archive/` —
25 arm submissions pinned with SHA-256, briefs, lesson text + SHA-256,
preregistration, verifier stdouts, manifest.json, scorer input/output.
`replay-trial.mjs` → **REPLAY MATCH** (exit 0).

## What this trial proves / does not prove

PROVES: possessing the T12 compositional lesson changes cold-successor
behavior on held-out tasks (Δ=1.00, p=5.41e-06), the delta is attributable
to the lesson's priority mechanism, the lesson does not leak into an
unrelated scored-pair domain, and the priority ordering survives genuine
inheritance (C>A, p=0.0037) — replication 3/3 on a distinct lesson.
DOES NOT PROVE: that retrieval works (stubbed), that T12 is independently
verified (pending), that the lesson is true (VERIFY lane), confirmatory power.
