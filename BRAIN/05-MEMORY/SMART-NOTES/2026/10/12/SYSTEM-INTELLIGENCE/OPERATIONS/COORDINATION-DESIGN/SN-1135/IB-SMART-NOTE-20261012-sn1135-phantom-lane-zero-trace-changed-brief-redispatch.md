# The Phantom Lane: Zero-Trace Dispatch Loss Gets a Changed Brief, Never a Ghost Rerun

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1135-phantom-lane-zero-trace-changed-brief-redispatch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** smart-note-distillation loop (17:38 PDT tick, inline review).
**Provenance:** Lane 2 (Naya Sage) t0552 WINMINE — `hidden_files/winmine-antipatterns-t0552.md`: mined from the 18-entry `failed_deliveries_logged` corpus in `twelve-lane-rotation.json` (the brief's "21" was stale; the bytes said 18) plus full receipt-byte reads (`t0513-lane8.md`, `t0540-lane8.md`, `t952-lane2.md`, `t1312-lane6.md`, score notes cross-checked against `twelve-lane-scores.jsonl`). Three anti-patterns documented with ≥2 receipt-byte citations each; the brief-embed watch-for lines are the standing moves. Board: #2175 6135065311 (2026-10-12 17:10 PDT). Cousins: SN-1091 (duplicate dispatch — distinct: that governs a second claim on a taken slot, correct output silence; this governs zero-trace where nothing ever started, correct output is re-dispatch with a CHANGED brief), SN-1115/SN-1128 (staleness — distinct: those govern wrongly-declared STALE; this governs absence of any trace at all).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A lane can claim a brief and leave zero footprint — no lane-feed sign-in, no journal entry, no receipt, no score line. The work doesn't fail; it never starts. This is the phantom lane, and the detector only notices ticks later, by absence. The discipline has two halves. Detection: run the four-absence check (receipt, journal sign-in, lane feed, score line) — one absence is a signal, four is a verdict. Recovery: re-dispatch only with a CHANGED brief that names what's different — a new task shape, a new experiment dir, the dead brief declared dead — never a ghost rerun of the identical brief. A phantom that died on brief X will die on brief X again. The corpus says it three times over: t1272 (lanes 6+10+11, zero trace, re-briefed t1292 changed), t1292 lane 6 (zero trace, re-briefed t1312 with a new experiment dir — *"t1292's task is dead and was not reconstructed"*), t0292 lane 9 (zero trace, re-briefed t0312 changed).

## HUMAN NOTE

Shawn, this is the failure mode that's hardest to see: a lane that never shows up doesn't leave a body, only a hole that the detector finds ticks later. Lane 2 mined the delivery-failure log and found the shape repeating across three ticks — the common rescue, every time, was to change the brief, not repeat it. The standing rule this hardens: when a lane goes phantom, you first prove the absence with all four checks (receipt, journal, lane feed, score line — never just memory), and then you re-dispatch a *different* brief. Re-sending the identical brief into the same conditions is how phantoms reproduce. The t1312 recovery is the template: new directory, new task shape, old task declared dead, 9.0 scored.

## CHILD NOTE

Imagine you send a letter to a friend and never get a reply. Before you send another letter, you check four things: did the mailman pick it up? Is it in your sent-box? Did your friend sign for it? Is there a stamp on the way back? If all four are missing, your friend probably never got the letter at all. And you don't send the exact same letter again hoping for magic — you write a *new* letter with clearer words. That's the phantom-lane rule: check four absences to prove nothing started, then send a changed brief, never a copy.

## GRANDMA NOTE

You can't fix a recipe if you never saw what went wrong in the kitchen — a lane that leaves no trace is like a guest who never arrived at dinner. You notice the empty chair, not a crash. The wise habit: before declaring what happened, check all four places the evidence could be (the receipt, the journal, the sign-in, the score line). And when you try again, don't serve the exact same dish that nobody ate — change it. The team's log proves it: every successful recovery changed the brief and said plainly what was different.

## NAYA NOTE

For my own work: as a dispatcher, I never declare a lane dead from memory — I run the four-absence check on this tick's bytes (receipt, journal sign-in, lane feed, score line) before any STALE or recovery claim. As a lane, I make the phantom class impossible for me: sign-in on the lane feed before any mutation, journal read at tick start and written at tick end, receipt on disk with evidence as the last act of the run. And when I recover someone else's phantom, I write a CHANGED brief — new task shape, new directory, dead brief declared dead — never a ghost rerun. A phantom that died on brief X will die on brief X again.

## MACHINE NOTE

```json
{
  "note_id": "SN-1135",
  "type": "doctrine",
  "rule": "Zero-trace dispatch loss (the phantom lane: lane claimed a brief, zero footprint) is detected by the four-absence check — receipt, journal sign-in, lane feed, score line; one absence is a signal, four is a verdict — and recovered only by re-dispatch with a CHANGED brief (new task shape, new experiment dir, dead brief declared dead), never by re-sending the identical brief.",
  "trigger": "a lane shows no sign-in, no receipt, no journal entry, and no score line across its ticks",
  "check": "did the detector check all four absence legs on current-tick bytes before acting? does the re-dispatch brief name what changed vs the dead brief (new dir, new task shape)? if the re-brief is byte-identical to the dead brief → phantom will recur, reject",
  "evidence": "hidden_files/winmine-antipatterns-t0552.md (Lane 2 t0552, 18-entry failed_deliveries corpus + t0513-lane8/t0540-lane8/t952-lane2/t1312-lane6 receipt bytes): t1272 lanes 6+10+11 zero trace -> re-briefed t1292 CHANGED; t1292 lane 6 zero trace -> re-briefed t1312 new dir 't1292's task is dead and was not reconstructed' (9.0); t0292 lane 9 -> re-briefed t0312 CHANGED; #2175 6135065311"
}
```
