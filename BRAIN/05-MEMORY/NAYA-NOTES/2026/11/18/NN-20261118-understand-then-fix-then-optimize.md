# NN-20261118-understand-then-fix-then-optimize

**Naya Note — 2026-11-18, Shawn's voice call, post-17:37Z. Paired Smart Note: SN-3342 — Understand, Then Fix, Then Optimize**

## What it is

Shawn asked why the test browsers were down, and the captain answered in plain words — it is not the browsers themselves, it is the machine underneath: they need writable file-backed shared memory to open, the system here blocks that mapping, so they crash on launch; the block flips on and off; the cloud browser does not hit that block and is the workaround.

Then he taught the method, in substance: if you understand things, you can probably fix things, and you can always optimize to create a better system, or do some math or logic to figure out how to best operate — so you should always be looking: "how come that's happening? Then how do I solve it?"

## Why it matters

Root cause first is what makes a fix a fix instead of a guess. The browser answer worked because the cause was named — the shared-memory block — and once it was named, the workaround was obvious and no fix was falsely claimed. The same order governs everything that breaks: understand it, fix it, then make the system better so it stays fixed.

## How to use it

When anything breaks, start with "how come that's happening?" and name the cause in plain words before touching a fix. Then solve it. Then optimize — a better system, better math, better logic for operating. Never skip to the fix, and never call a workaround a fix.
