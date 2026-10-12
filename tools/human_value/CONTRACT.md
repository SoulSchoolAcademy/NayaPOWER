# Human Value Measurement Contract v1

**Status:** canonical instrument (repo bytes). Replaces the lost 2026-10-06 local
instrument, whose producing bytes lived in a deleted workspace — the exact
failure this contract prevents.

## The question

**Did a human's life get measurably better?** "Task done" ≠ "mission complete."
Only observed, evidenced human outcomes count.

## What counts as human value (the four outcomes)

| value_type | Meaning |
|---|---|
| `cognitive_load_reduced` | human attention/effort the system absorbed instead of demanding |
| `rework_avoided` | work that did not have to be redone |
| `error_prevented` | mistakes caught before they cost a human |
| `useful_outcome` | a human got something they actually wanted |

Plus the service-quality counter-metric:

| value_type | Meaning | Trend target |
|---|---|---|
| `attention_demanded` | times the human had to intervene/correct the system (DAI input) | **DOWN** |

## The five laws of a valid measurement

1. **Evidence or it didn't happen.** Every event carries ≥1 durable evidence
   pointer. No evidence → no credit, fail closed. Evidence kinds: `feed_comment`
   (GitHub issue comment URL), `smart_note` (IB-… id), `receipt` (repo path),
   `content_hash` (`sha256:<hex>`), `url`.
2. **Private stays private.** Raw human data never enters a ledger. Ledgers hold
   derived measures + pointers; private bytes are pinned by `content_hash` and
   kept outside the repo.
3. **Units are human-comprehensible.** `value_units` must be explainable in one
   sentence (`unit_description`); minutes returned, cycles avoided, outcomes
   delivered. No abstract points.
4. **Deterministic recomputation.** Same ledger bytes → same report, for any
   successor, with no access to the originating workspace. `as_of` defaults to
   the latest event date (never wall-clock); the report pins `ledger_sha256`;
   `--expect-ledger-sha256` fails closed on byte drift.
5. **Prediction meets observation.** Events may carry `decision_id` +
   `delta_v_actual` (calculus scale [-10,10]). Joined to the decision receipt's
   `delta_v_predicted`, the kernel's `calibration_summary` closes the
   real-outcome loop: PREDICT → ACT → OBSERVE → CALIBRATE → RECALIBRATE-CANDIDATE.
   Recalibration candidates propose; they never promote.

## Metrics

- **HV/day** = Σ value_units per type over trailing 7 days ÷ 7. Total and per-type.
- **DAI/day** = `attention_demanded` units per day. Healthy system: trending down.
- **Calibration**: n joined observations, MAE, signed bias, overprediction flag,
  confidence multiplier (kernel math).

## What this is not

- Not a second decision engine. The Decision Value Calculus remains the one
  scoring seam; this instrument supplies the observed-outcome evidence it learns from.
- Not a survey. Sentiment is not measured; outcomes are.
- Not retroactive credit. Events are recorded when observed, with evidence that
  already exists — never manufactured to lift a number.

## Construction-independence acceptance (the 10/10 path)

Seat-independence of the *verdicts* is NOT claimed by one seat running this
code twice. The claim this instrument makes is narrower and testable: any
seat that re-implements THIS CONTRACT — without reading `collector2.py` —
must produce byte-identical decisions on the frozen control corpus and the
same agreement verdicts on the pinned sweeps. Concretely, a re-implementation
is accepted iff all hold:

1. **Channel law.** C2 (private chat logs / direct messages) is REFUSED, not
   unused: any attempt to include it fails closed (exit ≠ 0) before any API
   call. C1 (team feeds 2154/1713/1714/1715) + C3 (API repo actions) only.
2. **Marker law.** A comment is attributed to the human ONLY on a
   versioned-marker match from `authorship-markers.json` as a first-person
   speech act. Any reported-speech framing (quotation, attribution,
   "he said"/"per Shawn"/"quoting") grades `inferred` → excluded, fail closed.
   No marker → `uncertain` → excluded. C3 requires the login in
   `human-accounts.json`; v1 allowlist is empty → always "unresolvable".
3. **Control corpus.** `tools/human_value/tests/test_collector2.py` is the
   frozen acceptance suite: it contains the exact false positive caught live
   (comment 6115195148 — `Shawn: "Do you see it? Make it so."` → inferred),
   the direct-first-person controls, the case-sensitivity controls, and the
   C2-refusal controls. A re-implementation must reproduce every
   expected outcome in that suite.
4. **Agreement semantics.** Mechanical Jaccard is reported raw; pass/fail on
   it applies ONLY when the evidence universes overlap. When all baseline
   verdicts are `not_observable` (C2-sourced vs C1/C3 by construction), the
   verdict is `non_overlap_by_construction` and pass/fail does NOT apply.
5. **Determinism.** Same scan bytes → same report bytes. The agreement report
   is generated entirely from code (`collector2.py agreement --scan
   --baseline --candidates`); hand-assembled artifacts are not evidence.
6. **Pending stays pending.** A candidate promotes (proposed, never automatic)
   only on a DIRECT human trace about its artifact; a grader's prior is not
   evidence. Every re-probe stamps `window_checked`; a candidate's pending
   history is the chain of verdict artifacts across windows — a per-run
   counter is deliberately NOT emitted, because a counter recomputed from a
   stateless registry would reset every run and misrepresent history.

Until a different seat runs this acceptance, construction-independence is
OPEN — stated, specified, and unproven, never wished away.

## Cold-successor checklist (8.0 gate)

1. `git clone` at the pinned SHA; read `tools/human_value/README.md`.
2. `python3 tools/human_value/compute_hv.py --ledger <ledger> --receipts <receipts>`.
3. Compare `ledger_sha256` and every number against the posted report.
4. Any mismatch fails closed and is visible. A recomputation that matches is
   proof; a claim without one is documentation.
