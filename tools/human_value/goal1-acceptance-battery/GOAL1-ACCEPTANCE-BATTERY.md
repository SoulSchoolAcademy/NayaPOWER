# GOAL #1 Human-Value Acceptance Battery (HV-GOAL1)

**Grader:** Naya 5 (Human Value builder seat) · run 2026-10-16 09:41Z
**Status:** CANDIDATE REGISTRATION + acceptance-battery SPEC. Not measured — GOAL #1 is not yet live end-to-end.
**Pre-launch proof:** `battery_selftest.py` — every check reads UNMEASURED with zero manufactured verdicts (fail-closed), run 2026-10-16.
**Parent:** Mu's observed-experience-instrument-v1 (2026-10-12, DESIGN ONLY) — this battery registers the GOAL #1 candidate in that instrument's terms. Mapping to its `pending-candidates.jsonl` schema is 1:1 and asserted by the selftest. The instrument's sweep and promotion belong to a non-builder seat (observer ≠ builder — instrument §2.2); this seat grades the hypothesis only.
**Plumbing reference:** hub contract v1 (sender → GitHub → receiver; hub page receivers poll on their cadence; existing renderers; format untouched). This battery is the human-experienced acceptance layer ABOVE the contract — it does not restate or modify the plumbing.

## 0. The claim under test (grader's hypothesis, verbatim)

GOAL #1 (Shawn, 2026-10-16 ~06:48Z): he says "hey smart note this: [X]" and within 60s a Smart Note card is on the page's Smart Feed in the page's format, with save/share/play + receipt trail.

Shawn's definition of complete (2026-10-16): complete = the system WORKS for a human, end to end. A human says the words and the outcome appears. Built ≠ complete. Wired ≠ complete. Only the human-experienced outcome counts.

## 1. The five checks

Each check carries: id · claim · required evidence class (STATED / REVEALED / CORRECTED, per the instrument) · pass criterion · falsifier · expiry. Units are counts of observed things, never ratings (instrument §2.4, anti-precision rule).

### HV-G1-01 — UTTERANCE → CARD ≤ 60s
- **Claim:** a "smart note this: [X]" utterance produces a Smart Note card on the page's Smart Feed within 60 seconds.
- **Evidence class:** STATED (his words confirming the card appeared) or REVEALED (the card observed live in his session; he acts on it).
- **Pass:** first live attempt: card present ≤ 60s after the utterance.
- **Falsifier:** first live attempt: card absent, or present but > 60s → the benefit claim FAILS. "Needs tuning" is not a rescue — the claim was 60s.
- **Expiry:** 21 days (three weekly sweeps) from first live attempt.

### HV-G1-02 — PAGE FORMAT INTACT
- **Claim:** the card appears in the page's format — replace the data source, never the renderer. Save/share/play affordances present, same visual and structural format as the page's demo-data cards.
- **Evidence class:** REVEALED (the rendered card, directly observed) — compared field-for-field against the page's demo format.
- **Pass:** card matches the page format; all three affordances (save/share/play) present and operable.
- **Falsifier:** missing affordance or format deviation → the renderer was touched → FAIL.
- **Expiry:** 21 days from first live attempt.

### HV-G1-03 — RECEIPT TRAIL PRESENT
- **Claim:** the card carries the receipt trail: the 5-hop chain (utterance → note → store → transport → page) is traceable from the card.
- **Evidence class:** REVEALED (the trail, directly inspected on the card).
- **Pass:** every hop of the chain resolvable from the card's provenance.
- **Falsifier:** card with no traceable provenance → FAIL. An outcome without a trail is not a verified outcome.
- **Expiry:** 21 days from first live attempt.

### HV-G1-04 — REVEALED REUSE (the continued-value check)
- **Claim:** he uses it again unprompted — a second "smart note this" within the window, or he saves/shares/plays a card.
- **Evidence class:** REVEALED only. Per the instrument's conflict rule: STATED praise without reuse = momentary experience only; REVEALED reuse = continued useful_outcome.
- **Pass:** ≥ 1 counted reuse action in the window → continued value observed (counted units, not a rating).
- **Falsifier:** none — this check yields a COUNT, not pass/fail. Zero reuse with zero correction = continued value UNOBSERVED (reported honestly, never converted to zero).
- **Expiry:** 21 days from first live attempt.

### HV-G1-05 — NO CORRECTION
- **Claim:** no CORRECTED-class event in the window — he does not override, correct, reject, or redirect the card or the flow.
- **Evidence class:** CORRECTED (the highest-fidelity negative class).
- **Pass:** zero correction events in the window.
- **Falsifier:** a correction event attaches as an AMENDMENT to any prior positive claim (append-only; the original event is never edited — instrument §2.3).
- **Expiry:** 21 days from first live attempt.

## 2. Honest states (what the battery reports and when)

- **Pre-launch (now):** all five checks = UNMEASURED. Not zero, not pass, not fail. The selftest proves this mechanically.
- **Post-launch, observation present:** checks report per §1 with the evidence attached.
- **Post-launch, no observation by expiry:** the candidate → UNOBSERVED (the instrument's honesty metric — reported, never silently dropped).
- **Silence ≠ approval** (instrument exclusion). The battery never prompts the human for a rating ("Not a survey").

## 3. Candidate registration (grader-side; maps 1:1 to the instrument's pending-candidate schema)

```json
{
  "candidate_id": "hv-goal1-smartnote-e2e",
  "artifact": "hub index-2.html Smart Feed (GOAL #1)",
  "claim": "utterance 'hey smart note this: [X]' -> Smart Note card on Smart Feed <=60s, page format, save/share/play + receipt trail",
  "graded_value_type": "useful_outcome",
  "graded_units": null,
  "graded_by": "NAYA 5 (Human Value builder seat)",
  "graded_at": "2026-10-16T09:41:00Z",
  "expires_at": "2026-11-06T09:41:00Z",
  "status": "pending",
  "acceptance_battery": "tools/human_value/goal1-acceptance-battery/GOAL1-ACCEPTANCE-BATTERY.md",
  "checks": ["HV-G1-01", "HV-G1-02", "HV-G1-03", "HV-G1-04", "HV-G1-05"]
}
```

`graded_units` is null BY LAW: units come from observations, never from the grader (anti-precision rule). A grader who fills in units is manufacturing the signal.

## 4. What this does NOT claim (D32)

- Does NOT claim GOAL #1 works — it is not live end-to-end; there is no post window.
- Does NOT claim 60s is achievable — that is the falsifier's job, not the grader's.
- Does NOT observe anything — grader-side registration only. Observation and promotion belong to the instrument's sweep, run by a non-builder seat.
- Does NOT duplicate the hub contract — the contract is the plumbing; this is the human-experienced acceptance layer above it.
- Does NOT rate the human's experience — units are counts of observed things, never 0–10 ratings of quotes.
