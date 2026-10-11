# Evidence Ledger — UD-03: CHANGING OUR MIND TAKES EVIDENCE

Beliefs are versioned and evidence-weighted. Changing our mind requires
evidence proportional to the claim — no silent rewrites, no convenient
forgetting, no updating on vibes.

## The model

- **Belief**: an id, an append-only tuple of `BeliefVersion`s, a status
  (`SETTLED → CHALLENGED → REOPENED → REQUALIFIED`, or `UNRESOLVED`).
- **BeliefVersion**: version number, interpretation, cited evidence ids,
  confidence interval `[lo, hi]`, hash of the previous version (chain),
  and the receipt id that caused it. Frozen — never mutated in place.
- **Evidence**: id, statement, weight 0..1, source, direction
  (`SUPPORTS`/`REFUTES`). Frozen and **never deleted** — contradicting
  evidence is recorded, never retracted. There is no delete path;
  `retract_evidence` raises `EVIDENCE_IMMUTABLE`.
- **Receipt**: every transition emits an immutable receipt
  (belief, from→to, evidence cited, reason, timestamp).

## The three thresholds

Calibrated for a world where severe failures are rare and labels are noisy:

| Threshold      | Default | Meaning                                              |
|----------------|---------|------------------------------------------------------|
| LISTEN         | 0.25    | New evidence is noted; refuting weight at/above opens a challenge. Easy to listen. |
| CHANGE_TRUTH   | 0.70    | Only evidence at/above this rewrites a settled interpretation. Hard to change truth. |
| PROTECT_PEOPLE | 0.30    | Harm-suggesting evidence at/above triggers protective action quickly — even before truth changes. |

`protective_check()` is a tripwire, not a truth claim: it recommends
`PROTECT` without moving the belief's status.

## Uncertainty intervals

Confidence is `[lo, hi]`. Supporting evidence raises `lo` (noisy-OR cap);
refuting evidence lowers `hi`. No evidence at all = `[0.0, 1.0]`: total
uncertainty, honestly stated. **Absence of observed harm never counts as
proof of safety** — claiming safety from zero observations is refused
(`SAFETY_FROM_ABSENCE`), and absence moves no bound toward "safe".

Confidence can never exceed what the evidence supports (noisy-OR cap):
one 0.9 source supports 0.9; ten 0.1 sources support only 0.65. Quantity
is not proof. Claiming more raises `CONFIDENCE_EXCEEDS_EVIDENCE`.

## Drift

Every threshold set is bound to the policy/model/evaluator/environment it
was qualified under (`ContextFingerprint`). `note_context_drift()` marks
thresholds unqualified; until `requalify_thresholds()` runs, consequential
`rely()` and `update_belief()` are refused (`DRIFT_UNREQUALIFIED`).

## The versioned challenge path

1. `record_evidence(...)` — always allowed; evidence is append-only.
2. `challenge(belief, evidence)` — below LISTEN: noted, stays SETTLED.
   At/above: `SETTLED → CHALLENGED`.
3. `update_belief(belief, new_interpretation, evidence, confidence)` —
   refused on no evidence (`NO_EVIDENCE`), thin evidence (`WEAK_EVIDENCE`),
   inflated confidence, or drifted context. On success the old version is
   retained and the new version cites its cause.
4. `return_to_unresolved(...)` — the honest alternative to a forced update.

## Usage

```python
from evidence_ledger import BeliefLedger, SUPPORTS, REFUTES

L = BeliefLedger()
e1 = L.record_evidence("3 independent safety reviews passed", 0.8,
                       "safety-team", SUPPORTS)
L.register_belief("connector-safe",
                  "The connector is safe for production.", [e1])

# Someone tries to change our mind with no evidence:
L.update_belief("connector-safe", "Actually it is not.", [])
# -> Refusal NO_EVIDENCE. Belief stays SETTLED, version 1 intact.

# Real counter-evidence arrives:
e2 = L.record_evidence("reproduced data corruption", 0.85, "qa", REFUTES)
L.challenge("connector-safe", [e2])          # -> CHALLENGED
e3 = L.record_evidence("root cause confirmed", 0.9, "eng", SUPPORTS)
L.update_belief("connector-safe",
                "The connector corrupts data under load.", [e3])  # -> v2
# v1 retained, v2 cites e3, receipt records the path.
```

## Tests

`python3 test_evidence_ledger.py` — 18 adversarial cases, all green:
genuine updates requalify with history intact; evidence-free updates,
evidence deletion, weak-evidence rewrites, and confidence inflation are
refused; silent rewrite is structurally impossible (frozen versions,
tuple history, no rewrite path); absence-of-harm never certifies safety;
drifted thresholds block reliance until requalified; unaffected beliefs
continue while one is challenged.

## Honest scope notes

- The ledger judges the evidence it is given; it does not verify that a
  source told the truth (source credibility is UD-05/UD-06 territory).
- Threshold defaults (0.25 / 0.70 / 0.30) are starting calibrations, not
  proven constants — requalify under your own policy/model/evaluator/
  environment before consequential reliance.
- `protective_check` keys harm-suggesting evidence on the word "harm" in
  the statement; production use wants a real harm taxonomy, not a
  substring.

## What this does NOT claim

It does not discover truth — it governs how beliefs may change. A
REQUALIFIED belief is only as good as the evidence cited, and the ledger
says exactly what that evidence was.
