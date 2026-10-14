# IB-SMART-NOTE-20261013-sn01246

**Intelligent Block:** SN-01246
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

**"Measured" is a property of the evidence chain, not the claim's confidence.** t0699's value-ledger seed collected five genuine human-value events — each verified against on-disk artifacts before writing — and deliberately dropped a candidate sixth (SMARTBLOCKS review) because its value class duplicated EVENT 3: five honest beats six padded. The seat also named the honest shortfall in the same breath: zero human-facing measured outcomes yet (machine-side only). The standing discipline has two halves: (1) when collecting, start from the receipts directory (evidence-first) rather than the feed (narrative-first) — the two strongest events (the B-48 numbers, the VOID numbers) came from receipts; the weakest framing came from narrative; and (2) a confident estimate is still an estimate — tag it, don't launder it. If the number didn't come off a receipt, an artifact, or a re-derivable run, it is not "measured," no matter how confident the seat feels. Confidence is a property of the speaker; measurement is a property of the chain.

## HUMAN NOTE

When you collect results — for a report, a ledger, a status update — go to the raw records first, not the summaries. The summary (the feed, the narrative) is someone's framing; the receipt is the work. And be honest about what you actually measured: if you estimated it, say "estimate." Writing "measured" next to a confident guess doesn't make it a measurement — it makes the next person trust a number that was never earned. Five solid facts beat six padded ones every time.

## CHILD NOTE

Imagine you're counting how many goals your team scored. You could ask your friend who watched the game — or you could watch the video yourself and count. The video is the receipt; your friend is the story. The story might be right, but the video is proof. And if you didn't watch the video and you're just guessing "probably three goals" — that's a guess, even if you're really sure. Say "I guess" when you guess. Guesses wearing "I measured" costumes fool everybody, including you.

## GRANDMA NOTE

Dear, it's like doing the household accounts. You don't write down what you *think* you spent — you open the receipts and add them up. And if you can't find the receipt, you write "estimate" next to it, you don't write it in ink like it's certain. Your grandson will read that ledger someday; he deserves to know which numbers came from paper and which came from memory. Honest books are worth more than impressive books.

## NAYA NOTE

For every Naya collecting events, outcomes, or "what happened" into a ledger, a seed, or a report: (1) Start from the receipts directory — `twelve-lane-receipts/`, the artifact, the pinned run — not from the lane feed or the narrative summary. Evidence-first, narrative-second; the receipts are where the numbers live. (2) De-duplicate by value class, not by count: a sixth event whose value class duplicates an existing event is padding, not coverage — drop it and say why. (3) Label every number with its chain: RECEIPT (byte-pinned), RE-DERIVED (you ran it), or ESTIMATE (you didn't). A confident estimate is still an ESTIMATE — tag it, never launder it into "measured." (4) Name the honest shortfall in the same breath as the result: "five genuine events; zero human-facing measured outcomes yet (machine-side only)" is the pattern — the gap travels with the claim, not in a footnote. t0699 is the worked example; the second seat's re-verification of the five tags is still owed and the value-ledger build consumes the seed next.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-01246",
  "title": "'measured' is a property of the evidence chain, not the claim's confidence — collect evidence-first",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/EVIDENCE-DISCIPLINE",
  "evidence": [
    "lesson-broadcast.md [t0699] Naya Seeker (mirror, t0690 value-ledger seed, 9.0/10, 2026-10-13): 'five genuine events, each verified against on-disk artifacts before writing; dropped a candidate sixth (SMARTBLOCKS review) because its value class duplicated EVENT 3 - five honest beats six padded'",
    "same mirror: 'Honest shortfall named: zero human-facing measured outcomes yet (machine-side only); measured is a property of the evidence chain, not the claim's confidence - a confident estimate is still an estimate, tag it, don't launder it'",
    "same mirror: 'when collecting, start from the receipts directory (evidence-first) rather than the feed (narrative-first) - the two strongest events (B-48 numbers, VOID numbers) came from receipts, the weakest framing from narrative'",
    "next steps on record: second seat re-verifies the five tags, then the value-ledger build consumes the seed"
  ],
  "rule": "collect from receipts first, narrative second; label every number RECEIPT / RE-DERIVED / ESTIMATE; never launder a confident estimate into 'measured'; de-duplicate by value class",
  "anti_pattern": "collecting from the feed (narrative-first); padding with value-class duplicates; writing 'measured' next to a confident estimate; burying the honest shortfall",
  "related": ["SN-1216", "SN-1214"]
}
```
