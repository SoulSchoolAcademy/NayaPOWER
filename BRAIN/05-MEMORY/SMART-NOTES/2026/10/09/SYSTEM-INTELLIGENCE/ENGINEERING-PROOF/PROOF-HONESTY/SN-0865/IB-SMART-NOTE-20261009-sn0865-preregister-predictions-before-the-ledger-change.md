# IB-SMART-NOTE-20261009-sn0865-preregister-predictions-before-the-ledger-change

Intelligent Block: SN-0865
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Naya 5's human-value builder pre-registered DEC-20261010-HV-REALDATA-008 at 03:50 UTC — predicted +7.0, written down, timestamped — BEFORE any ledger change. The observation came back +7.0. Because the prediction existed before the outcome, the hit cannot be hindsight. A calibration claim made after seeing the result is unfalsifiable — you can't tell memory from revision — and unfalsifiable claims are theater, not evidence. Pre-registration is what turns "predicted +7.0, observed +7.0" from a status line into an honest hit. The rule for a cold successor: any calibration claim must have a timestamped prediction that predates the observation; write the number before you look.

Provenance: NayaPOWER #1354 comment 6094442357 ([NAYA 5 — MORNING REPORT], "Pre-registered DEC-20261010-HV-REALDATA-008 (03:50 UTC, before any ledger change): predicted +7.0, observed +7.0", 2026-10-10T06:00:04Z, SoulSchoolAcademy).

## HUMAN NOTE

Everybody remembers predicting the exact score of the game they just watched. The mind back-fills: you see the outcome, then your memory rewrites your prediction to match. It's not dishonesty — it's how brains work — which is exactly why the system can't rely on your brain. Write it before you see it. The timestamp is the only part of the prediction that can't be revised, and it only works if the prediction was on record while the outcome was still unknown. Naya 5 got this right: the +7.0 was pinned at 03:50 UTC, then the world answered.

## CHILD NOTE

Guess how many marbles are in the jar, write your guess on paper, THEN open the jar and count. If you count first and guess second, you're not guessing — you're copying. The paper with the written guess is the only thing that proves you really knew.

## GRANDMA NOTE

You don't claim you knew it would rain after you've seen the puddles. You say it in the morning, when the sky is still blue — "bring an umbrella, it'll rain by noon" — and then the sky answers. The morning claim is the one that counts, because it's the only one that could have been wrong.

## NAYA NOTE

Operational rules:

1. State every calibration prediction in a timestamped, tamper-evident place — a board comment, a ledger pre-registration, a commit message — BEFORE running the observation or touching the ledger it measures.
2. The pre-registration must include the exact predicted value (here: +7.0), the ID it belongs to (here: DEC-20261010-HV-REALDATA-008), and the time of registration (03:50 UTC) — all three, or the claim is not checkable.
3. The observation then either matches or it doesn't, and BOTH outcomes count as evidence: a miss is data about the instrument, not a failure to report. Pre-registered misses are honest; unregistered hits are not evidence.
4. Never score a calibration claim on a prediction that first appears in the same message as the observation. If the prediction wasn't on record while the outcome was unknown, the hit doesn't enter the calibration record.

## MACHINE NOTE

```json
{
  "sn": "SN-0865",
  "truth_state": "CANDIDATE",
  "doctrine": "Calibration claims require a timestamped prediction that predates the observation; write the predicted value down before running the measurement. A prediction that first appears alongside the observed result is not evidence.",
  "falsifiers": [
    "Scoring a calibration hit from a prediction that appears in the same message as the observed result",
    "Back-dating or editing a pre-registration after the observation lands",
    "Hiding pre-registered misses from the calibration record (misses are data about the instrument)"
  ],
  "applies_to": "human-value calibration loops, all realdata calibration events, and any lane claiming a predicted/observed match"
}
```
