# IB-SMART-NOTE-20260930-sn01193-read-the-ledger-before-you-match

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20260930-sn01193-read-the-ledger-before-you-match |
| Smart Note | SN-01193 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-13 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

The lane-scorer's 07:00 PDT tick manufactured its own crisis: its unscored-detection matched `(tick, 'lane'+N)` against a scores ledger whose agent field actually holds seat names (`'Naya Herald'`) — reporting 401 phantom "unscored" receipts and appending 27 malformed lines under the wrong schema (tick=t0634, missing lane int, wrong agent convention). Caught in the same tick: all 27 lines dropped, re-detection run correctly by (tick, lane-number) → only 2 truly unscored, both scored 9.0 in the canonical schema (tick=receipt tick, agent=seat name, lane=int, task=description), ledger rebuilt at 750 entries. The rule this banks: a shared JSONL ledger's schema lives in convention — field values, not enforcement. Before matching or appending, read 2–3 existing records and mirror their exact shape. Matching by assumption manufactures phantom work and corrupts the ledger you were hired to score.

## HUMAN NOTE

Shawn — the scorer caught its own mistake this morning before it did damage. It went looking for unscored lane receipts using the wrong pattern — searching for "lane 12" in a ledger that files by seat name ("Naya Herald") — so it "found" 401 unscored receipts that were already scored, and wrote 27 bad lines into the scores file. Same tick, it threw all 27 away, searched the right way, and found the real number: 2. Both scored cleanly at 9.0, ledger rebuilt. The lesson is now a standing rule: never touch a shared ledger without first reading a few real records to learn its actual shape. The schema isn't enforced anywhere — it lives in what the records look like. Two minutes of reading prevents a whole corruption.

## CHILD NOTE

Imagine a scorecard where every player is filed under their name — "Naya Herald" — but you go looking under "lane 12." You find nobody, so you report 401 missing scorecards that were never missing, and you write 27 new ones with the wrong labels. The smart move takes two minutes: read a few real scorecards first, see how names are actually written, then search. The scorer learned this the hard way and fixed it the same morning — threw out the 27 bad lines and did it right.

## GRANDMA NOTE

The clerk was asked to find unpaid bills. He searched the ledger for entries labeled "Lane 12" — but this ledger files bills under people's names, not lane numbers. So he reported 401 unpaid bills that were already paid, and filed 27 new bills with the wrong labels on top. To his credit he caught himself the same morning: threw out all 27, searched the right way, and found only 2 genuinely unpaid bills, which he processed properly. The standing rule from now on: before you touch someone else's ledger, read a few real pages first and learn how it's actually organized. The format lives in habit, not in a manual — and assuming the format is how ledgers get corrupted.

## NAYA NOTE

Note to future me: whenever you match against or append to a shared JSONL ledger (twelve-lane-scores.jsonl or any successor), read 2–3 existing records FIRST and mirror their exact schema — field names, value conventions (agent=seat name, never 'lane'+N), tick semantics (receipt tick, not current tick). The scorer's t0634 tick manufactured 401 phantom "unscored" and 27 malformed lines by matching an assumed schema; the recovery was dropping all 27, re-detecting by (tick, lane-number) → 2 truly unscored, scoring both in canonical schema, rebuilding the ledger (750 entries). Convention IS the schema; assumption is the corruption vector. When you catch yourself mid-corruption: drop the bad lines, say so in the receipt (the scorer did — "Process catch" section), rebuild, bank the lesson. Never silently leave malformed lines in a shared ledger.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20260930-sn01193-read-the-ledger-before-you-match",
  "smart_note": "SN-01193",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "A shared JSONL ledger's schema lives in convention (field values), not enforcement: read 2-3 existing records and mirror their exact shape before matching or appending; matching by assumption manufactures phantom work and corrupts the ledger.",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "LEDGER-DISCIPLINE"],
  "cousins": ["SN-0457"],
  "evidence": {
    "memory_log": "~/memory/2026-10-13.md — 'Scorer tick t0634 (07:00 PDT)' entry",
    "receipts_scored": ["twelve-lane-receipts/t0633-lane4.md", "twelve-lane-receipts/t0634-lane5.md"],
    "failure": "first detection matched (tick,'lane'+N) vs agent=seat-name convention → 401 phantom 'unscored'; 27 malformed lines appended (tick=t0634, wrong schema)",
    "recovery": "all 27 lines dropped; correct re-detection by (tick, lane-number) → 2 truly unscored; both scored 9.0 in canonical schema (tick=receipt tick, agent=seat name, lane=int, task=description)",
    "ledger": "rebuilt, 750 entries, backlog 0"
  },
  "rules": [
    "Before matching or appending to any shared ledger, read 2-3 existing records and mirror their exact schema.",
    "Never assume field value conventions (seat names vs lane labels, tick semantics); the convention is the schema.",
    "When you detect your own malformed writes: drop them all, state it in the receipt, rebuild, re-verify.",
    "Report the process catch as part of the receipt, not as a footnote — the next seat must see the failure mode."
  ]
}
```
