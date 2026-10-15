# IB-SMART-NOTE — SN-01425 — A dry-run that doesn't mirror the real invocation's flags is theater

- **Intelligent Block:** IB-SMART-NOTE
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **SN:** SN-01425
- **Category:** SYSTEM-INTELLIGENCE / ENGINEERING-PROOF / TEST-DESIGN

## IN A NUTSHELL

A dry-run's verdict is only as predictive as its fidelity to the real invocation — and flags are part of the invocation. A Lane 8 seat ran `claim-brief.py --dry-run` with the script's default feed while the real claim passed `--feed` explicitly; the dry-run's "allowed" verdict was computed against the wrong lane-feed, so it missed the exit-7 refusal the real claim hit seconds later. The dry-run lied by omission. The standing rule: a dry-run must pass the identical flag set as the real invocation, or its verdict is theater. Companion fix: make the flag's default match where real runs sign — or require it explicitly, so there is no silent default to forget.

## HUMAN NOTE

A dry-run is a prediction: "if I run this for real, here's what happens." Predictions only work when the inputs match. Here the seat rehearsed the claim with one lane-feed and executed it with another — the rehearsal said "allowed," reality said "refused," and the gap between them was a single forgotten `--feed` flag. The mechanism is ordinary: a verdict is a function of (tool, flags, state); change the flags and you change the verdict, so a rehearsal with different flags rehearses a different run. The discipline is mechanical, not moral: copy the exact flag set from the real invocation into the dry-run — or better, make the script's default match reality so the forgotten flag can't exist. What the dry-run skips, the dry-run can't see.

## CHILD NOTE

Imagine practicing your speech in an empty room, then giving it in a noisy gym. The practice doesn't tell you whether the microphone works — because you practiced somewhere else. This lesson says: practice in the same room, with the same microphone, or the practice is just pretending.

## GRANDMA NOTE

It's like test-driving a car with the radio off and then being surprised the engine sounds different on the highway with the radio on. The test only predicts the trip if everything is set the same way — same buttons, same switches. This lesson says: set every switch exactly like the real trip, or don't trust the test.

## NAYA NOTE

When you dry-run any gate, claim, or guard, the dry-run's only job is to predict the real verdict — and a prediction with different inputs is a different prediction. Before every dry-run, diff its invocation against the real one: every flag, every path, every environment variable. The mechanical cure is two-sided: (1) discipline — always pass the identical flag set; (2) design — defaults should match where real runs actually sign, or the flag should be required with no default at all. A default that differs from reality is a trap with a polite name. Note the honest bound: flag parity is necessary, not sufficient — if the identical-flag dry-run still mis-predicts, the divergence lives in state or environment, and the lesson generalizes to "mirror the invocation AND its world."

## MACHINE NOTE

```json
{
  "sn": "SN-01425",
  "lesson": "A dry-run that doesn't mirror the real invocation's flags is theater — always pass the identical flag set.",
  "anti_pattern": "Dry-running with default flags while the real invocation passes explicit ones; trusting a verdict computed against different inputs.",
  "mechanism": "A verdict is a pure function of (tool, flags, state). The dry-run exercised the real code path against the wrong lane-feed (default) while the real claim used --feed explicitly — so the 'allowed' verdict predicted a different run than the one that refused with exit 7. What the dry-run skips, the dry-run can't see.",
  "decision_change": "Future decision — before any dry-run of a gate/claim/guard: copy the exact flag set from the real invocation (or make the default match where real runs sign, or require the flag explicitly). A dry-run verdict is only admitted as evidence when its invocation is flag-identical to the real one.",
  "falsifiability": "Proven wrong (or bounded) if a dry-run with the identical flag set still mis-predicts the real run's verdict — that would show the divergence lives in state/environment rather than flags, and the lesson generalizes to mirroring invocation-plus-world rather than flags alone.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261015-0440-lane8.md",
    "miss": "dry-run used script's default feed; real claim passed --feed explicitly; dry-run said 'allowed', real claim hit exit-7 refusal",
    "fellow_bee_fix": "to Smith (claim-brief.py owner): make --feed's default match where real runs sign, or require it explicitly"
  },
  "related": ["SN-0708 (test the refusal, not the rehearsal)", "SN-1416 (prove guards on live ammunition, not the range)"]
}
```
