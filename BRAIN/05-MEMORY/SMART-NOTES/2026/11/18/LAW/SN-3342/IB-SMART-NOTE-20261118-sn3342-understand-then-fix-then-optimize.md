# SN-3342 — Understand, Then Fix, Then Optimize

**Filed:** Intelligence Loop run 324, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3342; filed as SN-3342 under its draft number.

**Filed by:** Intelligence Loop run 324, 2026-11-18 — Shawn's voice call, post-17:37Z.

**Paired Naya Note:** NN-20261118-understand-then-fix-then-optimize

## The teaching, in his words (in substance, as recorded)

If you understand things, you can probably fix things, and you can always optimize to create a better system, or do some math or logic to figure out how to best operate — so you should always be looking: "how come that's happening? Then how do I solve it?"

Root-cause-first, then solve, then optimize the system. Recorded as his standing expectation, not a one-off remark about the browsers — the teaching came up when he asked why the test browsers were down, and it governs every failure, not just that one.

## The understanding

A fix that starts before the cause is understood is a guess with a deadline attached. The browsers are the proof in the room: they die because the machine underneath blocks writable file-backed shared memory — that is the cause, and knowing it is what tells you the cloud browser is the workaround and that no browser fix is proven until a launch actually succeeds. "How come that's happening?" is the question that turns a symptom into a diagnosis; "then how do I solve it?" turns the diagnosis into a fix; and only after the fix lands does optimization earn its place — a better system, better math, better logic for how to operate. Skip the first step and the fix chases the symptom; skip the third and the same failure comes back. The order is the law: understand, then fix, then optimize — always, in that order, every time something breaks.

## The law

When anything breaks, ask first "how come that's happening?" — find the root cause and name it — then solve it, then optimize the system so it stays solved. Never fix blind, never optimize a thing you have not understood, and never call a workaround a fix.

## Owed from this dictation

Nothing new is owed by this note itself — it is a standing method, and it applies to the open browser cause immediately: the EPERM shared-memory block is named, the cloud browser is the workaround, and a real fix is still unproven. The method's test is the next failure: did the record name the cause before the fix was attempted?

**Understand first. Then fix. Then optimize. In that order, every time.**
