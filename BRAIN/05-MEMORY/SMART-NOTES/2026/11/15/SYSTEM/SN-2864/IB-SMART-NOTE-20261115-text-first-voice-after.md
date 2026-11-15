# Text First, Voice After

SN-2864 · LESSON / SYSTEM

**Created:** 2026-11-15 01:28Z

**Paired Naya Note:** NN-20261115-text-first-voice-after

## Hook

Finish the text before you do the voice. A voice reading unfinished words is a performance of a draft.

## Nutshell

Shawn (01:28Z): **"we're not even finished the transcript... How can you do the voice and you haven't even finished it yet? We haven't even finished the text. So let's get the text finalized and inputted before you do the voice."** Done the same hour: the Naya voice synthesis queue (`naya-voice-synthesis-queue`, hourly) was PAUSED — verified disabled, no run in flight, no queued runs — until the agreement text is final and inputted (v4 delivered whole); then it is re-enabled. The voice stream supervisor (`naya-stream-daemon-supervisor`, 15-min) was PAUSED too (01:38Z, verified disabled; last tick clean, 780s, queue empty, no synthesis) — it is voice output just like the synthesis queue, so the same order covers it; both re-enable when v4 lands whole. The media-notes transcribe-watcher was NOT paused — it turns his voice into text, which is how the text gets finished. He was told plainly and can say the word if he wants that stopped too.

## Human

The order looks like a scheduling decision and it is really a sequencing law: voice is downstream of text. A voice is a recording of words; if the words are still moving, the recording is a snapshot of a draft, and every later word-change orphans it — or worse, ships a confident reading of words he has already superseded. Pausing both voice-output jobs while leaving the transcribe-watcher running is the whole shape of the law in one move: the direction of travel is voice → text (his dictation becoming the finished text), never text → voice until the text is final. The transcribe-watcher is the intake; the synthesis queue is the output; you do not run the output while the intake is still filling the page. And the pause is bounded, not a stop: "until the agreement text is final and inputted" names the exact condition for re-enabling, so the jobs come back on a state, not on a feeling.

## Child

Imagine you're making a storybook. First you write all the words, nice and neat — THEN you read it out loud for everyone! If you try to read it out loud while you're still writing it, you'll read the wrong words and have to start all over. Write first, read second!

## Grandma

It's like baking, love — you finish the cake before you put the icing on! You don't ice a cake that's still in the oven. The words are the cake; the voice is the icing. We let his voice become the words first — that's how the cake gets made — and once the words are finished, then we can read them aloud beautifully.

## Naya

I finish the text first, then I give it a voice. His voice becomes the words; the words, once final, become the voice — never the other way round.

## What it means

- **THE ORDER:** text finalized and inputted first; voice after. Never voice a text that is still moving.
- **THE PAUSE:** voice synthesis queue + voice stream supervisor both paused (verified disabled) until the agreement text is final and inputted and v4 lands whole; both re-enable on that state.
- **THE EXCEPTION THAT PROVES IT:** the transcribe-watcher keeps running — it turns his voice INTO text, which is how the text gets finished. Intake runs; output waits.
- **THE BOUND:** the pause names its own end condition, so it is a hold, not a stop.

## Why it matters

Every voice bake costs minutes of machine time and, worse, creates an artifact that looks finished. A finished-sounding voice over unfinished words is the most convincing kind of wrong — it invites everyone to treat the draft as done. Sequencing the work text-first costs nothing (the watcher keeps filling the text) and saves the re-bakes, the stale audio, and the confusion of two versions of the same words in two media. It is the same law as the manuscript work: the words get their own scorecard before the page does; the page gets its eye before it ships. Order is the quality system.

## What changes now

1. No voice synthesis runs on a text that is not final and inputted.
2. Both voice-output jobs stay paused until v4 lands whole; re-enable on that state, not on a timer.
3. The transcribe-watcher keeps running — voice-to-text is the intake that finishes the text.
4. Any future voice work names its text source and its finality before it bakes.
