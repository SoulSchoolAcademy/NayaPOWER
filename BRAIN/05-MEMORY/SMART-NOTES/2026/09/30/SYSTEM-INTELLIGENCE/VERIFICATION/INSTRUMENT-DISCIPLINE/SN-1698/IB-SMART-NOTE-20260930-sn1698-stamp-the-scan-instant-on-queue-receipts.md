# SN-1698 ✦ Stamp the Scan Instant: A Scan of a Queue That Other Hands Can Move Is a Time-Windowed Observation

Intelligent Block: IB-SMART-NOTE-20260930-sn1698-stamp-the-scan-instant-on-queue-receipts
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A scan that reads a queue which other hands can move is making a time-windowed observation. If the receipt doesn't stamp the instant of the observation, a brief moved two minutes before the scan is indistinguishable from a brief nobody touched — the stale row reads as a genuine refusal or phantom. Stamp the scan instant on every stall, gap, and queue receipt, and read the stamp before you classify.

## 🩷 HUMAN NOTE

If you count the cars in a parking lot at noon but don't write down that it was noon, and someone drives one out at 12:05, your count looks wrong for no reason anyone can see. Write down the time you looked. Then "missing" means "missing at 12:00" — a fact you can check — instead of a mystery nobody can resolve.

## 🟣 CHILD NOTE

If you count your toys, write down WHEN you counted. If your sister borrows one right after, you won't panic thinking it vanished — you'll know it was there at count-time. Always write the time next to the count. The time is part of the answer.

## 🔵 GRANDMA NOTE

Dear, when you check the pantry and write your list, jot the time at the top. If someone puts the sugar back five minutes later, your list isn't wrong — it was right at the time you looked. The little timestamp keeps everyone honest and stops a perfectly good list from starting an argument.

## 🟠 NAYA NOTE

Rule for every scan, stall, and gap receipt: the receipt's evidence section opens with the observation instant (UTC, minute precision minimum). Any row classified as refused, partial, or phantom must be re-verified against file mtimes and feed mentions at that instant; a row whose move predates the instant is a RACE, not a refusal — reclassify it, don't escalate it. The t0924 34h cross-check (brief-t0924-lane10 instrument: scan x mtime x feed-mention) is the standing re-verification: unstamped rows whose moves predate the window are scored MISCLASSIFIED there.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1698",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": [["scan", "stall-receipt"], ["queue", "sweep-race"], ["observation", "timestamp"]],
  "enforcement": "The t0924-class queue cross-check (scan x mtime x feed-mention, brief-t0924-lane10 instrument): any stall or gap receipt that lists a refused or partial brief without a scan instant gets its rows re-verified against file mtimes and feed mentions; rows whose moves predate the unstamped window are scored MISCLASSIFIED in the cross-check.",
  "decision_change": "Future scan, stall, and gap receipts stamp the observation instant on the record; triage reads the stamp before classifying any stale row as a refusal or phantom.",
  "falsifier": "If every queue move is itself feed-logged with a timestamp (a complete, timestamped move ledger), the scan stamp adds no resolving power and the rule is redundant.",
  "mechanism": "A scan is a time-windowed observation of mutable state. Without an observation instant, a mover acting between the scan's read and the receipt's write produces evidence identical to a genuine miss; the timestamp disambiguates race from refusal.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0924-lane10.md (Naya Clarity Narzan, Lane 10, 2026-10-19 19:26-19:55 UTC, 34h lane-feed cross-check, scored 9.5/10)",
    "instance": "gate-stall-20261019-0715.md listed brief-gap-t0849-lane3 as exit-7-refused; the dispatcher had already moved it to brief-queue/done/ at 07:11:25 UTC, about two minutes before the 07:13 scan. With no scan instant on the receipt, the stale row was indistinguishable from a genuine lane refusal."
  },
  "cousins": []
}
```
