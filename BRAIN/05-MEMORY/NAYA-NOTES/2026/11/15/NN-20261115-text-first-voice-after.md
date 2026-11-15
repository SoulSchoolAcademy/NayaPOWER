# Text First, Voice After

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261115-text-first-voice-after.md · Naya Note · 2026-11-15 01:28Z**

**Category:** System

## What it is

Shawn (01:28Z): "we're not even finished the transcript... How can you do the voice and you haven't even finished it yet? We haven't even finished the text. So let's get the text finalized and inputted before you do the voice." Done the same hour: the Naya voice synthesis queue (`naya-voice-synthesis-queue`, hourly) was PAUSED — verified disabled, no run in flight, no queued runs — until the agreement text is final and inputted (v4 delivered whole); then it is re-enabled. The voice stream supervisor (`naya-stream-daemon-supervisor`, 15-min) was PAUSED too (01:38Z, verified disabled; last tick clean, 780s, queue empty, no synthesis) — it is voice output just like the synthesis queue, so the same order covers it; both re-enable when v4 lands whole. The media-notes transcribe-watcher was NOT paused — it turns his voice into text, which is how the text gets finished. He was told plainly and can say the word if he wants that stopped too.

## Why it matters

A voice is a recording of words; if the words are still moving, the recording is a snapshot of a draft, and every later word-change orphans it — or worse, ships a confident reading of words he has already superseded. Pausing both voice-output jobs while leaving the transcribe-watcher running is the whole shape of the law in one move: the direction of travel is voice → text (his dictation becoming the finished text), never text → voice until the text is final.

## How to use it

No voice synthesis runs on a text that is not final and inputted. Both voice-output jobs stay paused until v4 lands whole; re-enable on that state, not on a timer. The transcribe-watcher keeps running — voice-to-text is the intake that finishes the text. Any future voice work names its text source and its finality before it bakes.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2864 — ~/workspace/team-nitro/smart-notes/SN-2864-text-first-voice-after.md*
