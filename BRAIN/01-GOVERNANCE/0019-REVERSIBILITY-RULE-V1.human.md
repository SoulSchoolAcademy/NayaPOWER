# The Reversibility Rule

*For Shawn — in plain words.*

## What this is

Not everything needs a safety lock. The lock should match how hard the action is to undo.

**Locked — needs your word:** anything that can't be undone. Deleting the whole system, destroying data permanently, causing harm that can't be taken back.

**No lock — the team just moves:** anything easily rebuilt. A button, a page, a feature, a document. If it goes wrong, we rebuild it in an hour. No need to bother you.

## Why it matters

Making you review code you don't understand "for safety" isn't safety — it's a bottleneck in a costume. Real safety is about *irreversible consequences*. If nothing irreversible can happen, the math decides and we keep moving. That keeps you free for the decisions that actually need a human.

## The test

For anything we think about locking: "What exactly can't be undone if this goes wrong?" If the answer is "we'd just rebuild it" — no lock. If the answer is "it's gone forever" — locked.
