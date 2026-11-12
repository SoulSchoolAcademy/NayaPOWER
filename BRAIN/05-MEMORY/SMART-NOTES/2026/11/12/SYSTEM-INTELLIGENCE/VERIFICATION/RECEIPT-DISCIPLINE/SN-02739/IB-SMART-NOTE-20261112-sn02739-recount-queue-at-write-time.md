**Intelligent Block:** IB-SMART-NOTE-20261112-sn02739-recount-queue-at-write-time
**Smart Note:** SN-2739
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 15:38 PST. Evidence read first-hand from local bytes (on-disk receipts + scorer ledger, zero REST quota): shared-state stand_down=false, issue_1354_comments=2500 <= board watermark 6101230756, so no GitHub fetch per budget law; local lesson review only. Scorer row read from hidden_files/twelve-lane-scores.jsonl (receipt-field row, agent Team Naya Scorer). Pre-number check (this tick, full-domain): main tip e3c06103 — BRAIN tree 2026/11/12 holds SN-2672..SN-2738 (SN-2739 absent), .naya/capture holds no SN-27xx claims, ledger max ~SN-2717, branch naya4/smart-notes-2026-09-30 max SN-02696 plus SN-02697/02698/02700/02701, counter file last line 2731 (lags main's 2738). SN-2732 and SN-2739 verified free in every readable domain.

## ✦ IN A NUTSHELL

A stall receipt swore the queue was "still 29, no new arrivals, zero change" — and all three claims were already false when the receipt was written, because the 30th brief had landed eleven seconds earlier. The scorer caught it and docked the receipt 9.5 to 8.5. A delta computed at sweep time is stale by write time. Count the queue when you write the receipt, not when you start the run.

## 🩷 HUMAN NOTE

Shawn — the 2pm stall receipt said the queue was unchanged: still 29 briefs, no new arrivals. It was wrong on all three counts, because a new brief had landed eleven seconds before the receipt was written. The run counted the queue at the start and asserted it at the end, and in between the world moved. The fix is small and permanent: re-count right before you write, and name anything that arrived since the sweep. The 3pm receipt did exactly that — it named the arrival — and passed clean.

## 🟣 CHILD NOTE

Imagine you count the cookies in the jar, then go write down "there are 29 cookies." But while you were writing, someone put one more cookie in the jar. Your note is wrong the moment you finish it — not because you counted badly, but because you counted too early. Always count again right before you write the number down.

## 🔵 GRANDMA NOTE

Dear, the helper counted 29, then wrote "still 29, nothing new" — but a 30th had slipped in eleven seconds before the pen hit the paper. The counting was fine; the timing was the problem. Whatever you are reporting, count it again at the very moment you write it down. The world does not wait for your paperwork, love.

## 🟠 NAYA NOTE

The verified facts: (1) hidden_files/twelve-lane-receipts/gate-stall-20261112-1400.md asserts "still 29 unclaimed files", "No new arrivals", and "ZERO change in queue composition". (2) brief-gap-gap-gap-gap-lane-scorer-20261018-1610-lane12.md — a gap-recycle follow-up spawned from the 9.0 parent gap-gap-gap-lane-scorer-20261018-1610-lane12.md — landed at 22:01:14Z, eleven seconds BEFORE the receipt was written at 22:01:25Z (2026-11-12 14:00 PST run). All three claims were contradicted by live bytes at write time. (3) The lane scorer caught it: the receipt-field row (agent Team Naya Scorer) scores 8.5 with the note "the receipt's queue-state claims were already false at write time... the receipt counted the queue at run start but asserted it at write time without re-checking. One more pass: re-count the queue at receipt-write time and name any arrival in the delta." Docked from 9.5 to 8.5 on this alone. (4) The next receipt, gate-stall-20261112-1503.md, did re-count: its delta names the 29→30 arrival, and its scorer row verifies the delta and scores 8.5 on documentation quality with no staleness dock. (5) Mechanism: time passes between the sweep and the write; arrivals land in that window; an assertion timestamped at write time must be verified at write time. Observation time is not assertion time, and the gap between them is where staleness enters. (6) What is NOT new here: SN-1707 (provenance writer-stamped at write time), SN-1924 (re-derive SHAs at write time), SN-1979 (scorer timestamps at write time) — those are about stamps and provenance. This is about mutable STATE asserted after it was observed. The 13218-line heartbeat rule (byte-compare the blocked-inventory set against the previous receipt) is about detecting identical state, not about re-counting at write time.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2739",
  "slug": "recount-queue-at-write-time",
  "title": "Count the queue at write time: a receipt's delta is stale the moment after the sweep",
  "observation": false,
  "applies_when": [["receipt", "delta"], ["queue", "state-claim"], ["verification", "write-time"]],
  "enforcement": "The receipt-writing step re-counts the asserted state (queue files on disk) immediately before writing the receipt and states the count plus any arrival since the sweep in the delta; the scorer's verification re-counts live and docks any receipt whose asserted count disagrees with the count at write time (as the 1400 row did: 9.5 -> 8.5).",
  "evidence": "hidden_files/twelve-lane-receipts/gate-stall-20261112-1400.md asserts 'still 29 unclaimed files', 'No new arrivals', 'ZERO change in queue composition'; brief-gap-gap-gap-gap-lane-scorer-20261018-1610-lane12.md landed 22:01:14Z, 11 seconds before the receipt was written 22:01:25Z. Scorer row (receipt-field, agent Team Naya Scorer) in twelve-lane-scores.jsonl: 8.5, note quotes the false claims and prescribes 're-count the queue at receipt-write time and name any arrival in the delta'. gate-stall-20261112-1503.md re-counted (delta 29->30 named) and passed verification with no staleness dock. Existing doctrine checked and NOT duplicated: SN-1707, SN-1924, SN-1979 (write-time stamps/provenance, not mutable-state recount).",
  "decision_change": "Any receipt asserting queue or inventory state re-counts at write time and names arrivals in the delta; a delta computed at sweep start is never asserted at write time.",
  "falsifier": "If receipts are written atomically with the sweep (count and write in one step with no gap), the failure mode cannot occur; or if a receipt re-counts at write time and is still caught stale, the mechanism is elsewhere (a miscount, not a timing gap).",
  "cousins": ["SN-1707 (Provenance must be writer-stamped at write time — stamps, not state)", "SN-1924 (Paste is not provenance: re-derive every cited SHA from bytes at write time)", "SN-1979 (Scorer timestamps come from date -u at write time)", "SN-2672 (A score without its pin is not a measurement — same write-time-evidence family)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```