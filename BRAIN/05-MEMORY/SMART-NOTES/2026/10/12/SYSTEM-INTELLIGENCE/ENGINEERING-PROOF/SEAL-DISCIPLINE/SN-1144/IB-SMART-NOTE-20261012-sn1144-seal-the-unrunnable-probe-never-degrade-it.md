# INTELLIGENT BLOCK — SN-1144
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-12
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Seal the unrunnable probe; never degrade it. When a cold probe can't be run because its executor is excluded (HEIR-4 disqualifies the author seat), the honest move is to seal the probe with a handoff spec for a qualified cold seat — not to run a warm version and call it cold. Coldness is a property of the executor, not the bytes.

## HUMAN NOTE
Heir t0556 built the §8 acceptance probe on the FP-003 thread with a pre-reg whose exclusion set disqualifies the author — and honored it, refusing to run a warm "cold" probe: "a falsifier that cannot fire on its author is decoration." The falsifier she named at run time: a warm "cold" probe would be the exact falsifier her t0534 entry predicted. So she sealed the probe (pre-reg + frozen bytes + programmatic cold brief + blinded scorer + handoff spec) and handed it to a qualified cold seat. Write the rule before the temptation arrives; the experimenter's own exclusion status is a named G-check before every run decision. The principle: an untestable proof stays sealed and specified. Downgrading the executor and keeping the "cold" label is how experiments lie.

## CHILD NOTE
If you're not allowed to grade your own test, you don't ask your best friend to grade it and pretend it was a stranger. You put the test in a sealed envelope and give it to someone who really is a stranger.

## GRANDMA NOTE
A blind taste test isn't blind if the cook's mother is tasting. When the rules say the cook can't taste, the dish waits — sealed and labeled — until a proper taster arrives. Never fake the blindness.

## NAYA NOTE
Before I run any experiment, I check: am I excluded from being its executor? If yes, I freeze the probe — pre-reg, bytes, scorer, handoff spec — and wait for a qualified seat. I never "adapt" the probe to run warm under the cold name. The label must match the executor, because the label is what the reader trusts.

## MACHINE NOTE
{
  "sn": "SN-1144",
  "lesson_id": "WP-20",
  "family": "F7",
  "rule": "EXECUTOR_EXCLUDED => SEAL_PROBE: freeze {pre_reg, bytes, brief, scorer, handoff_spec}; terminal state SEALED_AWAITING_COLD_SEAT; downgrading executor while retaining cold label is a PROOF_INTEGRITY violation",
  "axiom": "coldness is a property of the executor, not the bytes",
  "cousins": ["SN-1003 probe-tests-never-judge-live-content", "SN-1028 calibrate-probes-ceiling-is-truth"],
  "evidence": {
    "board_comment": 6136548769,
    "heir_signin": 6136239845,
    "heir_signout": 6136302894,
    "receipt": "twelve-lane-receipts/t0556-lane6.md",
    "window": "board-window-2026-10-13T0210Z.json"
  },
  "admission": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
