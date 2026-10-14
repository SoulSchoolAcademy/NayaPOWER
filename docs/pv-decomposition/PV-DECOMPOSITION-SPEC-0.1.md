# PV Decomposition Spec v0.1 (CANDIDATE — unwired)

**Status:** CANDIDATE. Spec-only. Does NOT modify `kernel/value_calculus.py`.
Wiring into the kernel needs Shawn's word + ratification.
**Author:** Naya Clarity Narzan (drive loop), 2026-10-14.
**Unblocks:** B-46 proof gate — "Normalize() + term rubric + baseline-pricing rule".

## 1. Problem

`kernel/value_calculus.py` V2.1 computes `pv = B − H − C − effective_residual_risk`
from `PVEstimate(B, H, C, R)`, but nothing in the codebase specifies **how B/H/C/R
are derived from evidence**. They arrive as author-supplied floats. NAYANODE/0025
names "B/H/C/R component gaming" as a threat with no stated defense.

B-46 counts **cold-recomputable B/H/C/R decompositions**: a decomposition counts
only if a cold reader can recompute the same values from stated inputs. This spec
is the missing recipe: the term rubric, Normalize(), and the baseline-pricing rule.

## 2. Definitions

**Term** — the atomic input. Each term carries:
`{id, quote_span | evidence_ref, raw_magnitude, unit, unit_rate | rate_table_ref,
bucket, confidence, severity_0_10 (R-bucket only), probability (R-bucket only), note}`

**Bucket** — exactly one of `B` (benefit), `H` (harm), `C` (cost), `R` (risk).

## 3. Term rubric (bucket assignment — deterministic)

Precedence order for ambiguous terms (first match wins):

1. **C (Cost):** certain expenditure of a resource to execute the action
   (time, money, attention, compute, quota). Counted even when the action succeeds.
   Rationale: costs are the price of action; folding them into H would make
   "do nothing" artificially attractive.
2. **H (Harm):** certain or already-realized negative delta vs the baseline for a
   stakeholder. A certain negative MUST go here, never to R (anti uncertainty-laundering).
3. **R (Risk):** probabilistic adverse outcome not yet realized.
   Contribution = `severity_0_10 × probability`, both stated in the term.
   The decomposition surfaces (not decides) RiskPolicy trips: if
   `severity ≥ 9.0 and probability ≥ 0.01`, the receipt flags `RISK_POLICY_TRIP: true`
   (governance decides; the math only reports).
4. **B (Benefit):** positive delta vs the baseline (realized or committed).

**Anti-gaming rules (defense for the NAYANODE/0025 threat):**
- A term lands in exactly one bucket. No double-counting.
- **Distinct-evidence rule:** each term needs a distinct `evidence_ref` or `quote_span`.
  Splitting one fact into N terms to inflate `evidence_count` is a violation; the
  reference implementation rejects duplicate evidence refs.
- **No relabeling to dodge thresholds:** moving a certain negative from H to R, or a
  cost from C to H, to change a gate outcome is a violation. The precedence order above
  is the check.
- Confidence is per-term, stated, in [0,1]. No silent inheritance.

## 4. Normalize()

Per term: `n = clamp(raw_magnitude × unit_rate, 0, 10)` where `unit_rate > 0` is
stated in the receipt or cited from the versioned `DEFAULT_RATE_TABLE` below.

**Closed unit set (v0.1):**
| unit | meaning | unit_rate source |
|---|---|---|
| `value_points` | raw already on the 0–10 value scale | 1.0 (fixed) |
| `hours` | wall-clock lane time | stated in receipt (points/hour), no silent default |
| `usd` | money | stated in receipt (points/usd), no silent default |
| `count` | discrete occurrences | stated in receipt (points/count), no silent default |
| `probability` | R-bucket only | n/a — contribution = `severity_0_10 × probability` |

New units require a spec amendment (fail-closed: the implementation rejects unknown units).

**Component value:** `B = round6(Σ n over B-terms)`, likewise H, C, R.
Per-term clamp to [0,10] forces large effects to be decomposed into evidenced
sub-terms instead of arriving as one asserted number. No upper clamp on the
component sum (matches `PVEstimate`'s `≥ 0` constraint). Rounding: round-half-even
to 6 decimals, applied once at component level — deterministic across machines.

**Confidence aggregation:** component confidence = `min(term confidences)`
(matches `PVEstimate.min_component_confidence`). `evidence_count` = number of terms.

**Empty buckets (Zero Value Law):** an empty bucket is UNMEASURED, not zero —
its confidence defaults to 0.0 (matching the calculus's `confidence.get(k, 0.0)`
default; fail-closed). An author may claim a *measured* zero via an explicit
`zero_attestation` for that bucket: `{scope, confidence}` stating what was
searched and how confident the author is that nothing was found. Without it,
the 0.0 default flows into `min_component_confidence` and raises residual risk —
unexamined harms must cost, not hide.

## 5. Baseline-pricing rule

- The baseline (`baseline_id` from the decision receipt) is priced at **exactly 0**.
- Every term's `raw_magnitude` is a **delta from the baseline state**, never an absolute.
- The receipt MUST cite the baseline source (commit / PR / issue URL + quote span)
  so a cold reader can verify the counterfactual. "Do nothing" baselines state the
  observable status-quo facts they are measured against.
- The baseline's own ongoing costs (price of doing nothing) belong in the baseline
  description; they are informational only and priced at 0 in the candidate's
  decomposition (common to all candidates — they cancel).

## 6. Cold-recompute acceptance

A decomposition is cold-recomputable iff its receipt carries:
`spec_version`, `decision_id`, `baseline_id` + baseline source ref, the full term
list (every field above), the computed `(B, H, C, R)` to 6dp, and a pointer to this
spec version. A cold reader re-running the reference implementation on the term
list gets bit-identical rounded values. Deterministic: no randomness, no
floats-from-prose, no hidden defaults.

## 7. DEFAULT_RATE_TABLE v0.1

`{value_points: 1.0}` — the only fixed rate. All other units require a stated rate
in the receipt. (Deliberately sparse: silent conversion rates are how gaming hides.)

## 8. Worked examples (real decisions)

Example 1 — 04:38-cycle #2576 receipt repair (my lane's own decision), receipt:
`worked-example-2576-repair.json` (B=6.0, H=0.0 attested, C=1.4, R=0.4 → pv 4.2).

Example 2 — Lane 1 t0755 blind level-drill run (Naya Clarity Verity's decision,
another lane), receipt: `worked-example-lane1-drill.json`
(B=9.0, H=0.0 attested, C=2.0, R=0.9 → pv 6.1). This example exercises two spec
behaviors Example 1 did not: (a) the drill's lane-time cost was NOT stated in its
receipt, so the C-term arrives at confidence 0.5 — `min_component_confidence`
drops to 0.5 and the residual becomes max(R, 1−0.5)=0.9; (b) two distinct B-terms
from two distinct evidence refs (divergence data vs fail-closed confirmation),
showing the distinct-evidence rule permits — and requires — separate facts.

## 9. Pass-2 addendum (2026-10-14 07:08 PDT — drive loop, non-normative)

The recipe (sections 1–7) is unchanged; spec stays PV-DECOMP-0.1. Two
clarifications, both NON-normative (they do not alter acceptance):

- **Rate guidance:** receipts MUST state every non-fixed rate (normative §4).
  For convenience, receipts MAY cite a shared convention instead of re-deriving:
  this lane's receipts use 2.0 points/hour for lane time. A cited convention is
  still a stated rate — silence remains a rejection. (Addresses pass-1
  "rate-friction" hole without re-introducing silent defaults.)
- **Worked-example coverage:** with two real, cross-lane examples + 7 adversarial
  fail-closed tests green, the pass-1 "single example" hole is closed.
  Still owed before a PR: a second-seat review (a different seat re-derives one
  example from the receipt alone — the cold-recompute acceptance test §6, run by
  someone other than the author).

Decision detail for Example 1 (kept for continuity): 04:38-cycle #2576 receipt repair (pin + body PATCH + empty push) vs do nothing.
Baseline: #2576 stays red on receipt gates; merge stays blocked; Captain's routed
STILL-BLOCKED stays open. Baseline source: drive-loop log 2026-10-14 + board #2537.

| id | bucket | term | raw | unit | rate | n | conf |
|---|---|---|---|---|---|---|---|
| t1 | B | two receipt gates green; Captain's routed STILL-BLOCKED closed (verified live 04:38) | 6.0 | value_points | 1.0 | 6.0 | 0.9 |
| t2 | C | ~0.7h lane time + ~14 REST calls (quota spend) | 0.7 | hours | 2.0 | 1.4 | 0.8 |
| t3 | R | empty push races builder's own push / invalidates IV | sev 4.0 × p 0.1 | probability | — | 0.4 | 0.6 |

`B=6.0, H=0.0, C=1.4, R=0.4` → `pv = 6.0 − 0 − 1.4 − max(0.4, 1×(1−0.6)) = 4.2`
(RISK_POLICY_TRIP: false.) Full machine receipt: `worked-example-2576-repair.json`.
