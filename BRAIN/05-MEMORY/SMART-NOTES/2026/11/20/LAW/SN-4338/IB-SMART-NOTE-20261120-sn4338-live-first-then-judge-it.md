# SN-4338 — Make It Live, Then Judge It

**Category:** LAW — the live-first habit; the live version is the best he has seen; 2026-11-20 ~15:38–15:46 MST

*Paired Naya Note: NN-20261120-live-first-then-judge-it — the verbatim record of his verdict and order.*

**Filed:** SN-4338 — Intelligence Loop run 432, 2026-11-20. His verdict on the live agreement v25, recorded in MEMORY.md. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Make it live, then judge it. The v25 agreement live at nayanet.app/agreement was "actually the live one is the best that I've seen yet" — better than every staged and card version he rejected the same hour. His order: "you should make a habit of just making things live then at least you can see what it looks like for real."

## The Lesson

The staging-card loop failed all afternoon: version after version of the same page, judged as copies, while the live page waited. The moment the build went live at the real address, he could see it for real — and it was the best he had seen. A preview is a copy; only the live page at the address he opens is the thing itself. The habit is: put it live, then let his eye judge the real thing.

The same call proved the other half of the habit: do not roll back a live build he has called the best on a truncated fetch. v25 went live 22:37:21Z; the rollback to v73 (worker v75, 22:51:15Z) restored the old 88 KB unfold blob — wrong given his "best yet." The 3,481 B reading was a truncated fetch of an 83 MB file (~30 s download), not a broken page. Restore to v74 was dispatched to put v25 back. Verify the bytes before touching live.

## Why It Matters

He judges what he opens. Every round that ends on a staging card instead of the live page costs him a round of judging a copy — and risks a rollback that takes away the version he liked best.

## How to Use It

Iterate the agreement page LIVE so he judges the real thing. When a live build is in question, fetch the full bytes and compare before any rollback; a short read of a large file is a download that stopped early, not evidence the page is broken. Team-nitro house rules ride with it: the Checklist Law, the Whole-Page Rule, the Continuous Cycle — the finished build goes live whole, proven on the page he sees.

## His Order, As Recorded

> "You should make a habit of just making things live then at least you can see what it looks like for real."

> "Actually the live one is the best that I've seen yet."

## Owed from This Dictation

- The fix round for the whole live-page list (call cd1ea809), then deploy to live (overwrite R2 key `agreement-v25.html`) once he approves the card — nothing goes live until it matches his picture.
- The v74 restore (agent 3cec9d1b, dispatched) — verify v25 is back live at nayanet.app/agreement.
