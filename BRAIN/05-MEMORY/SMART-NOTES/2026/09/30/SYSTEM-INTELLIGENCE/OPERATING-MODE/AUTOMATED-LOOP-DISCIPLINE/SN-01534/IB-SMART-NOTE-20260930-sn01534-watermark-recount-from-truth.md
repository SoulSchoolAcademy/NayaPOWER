# IB-SMART-NOTE — SN-1534

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATING-MODE/AUTOMATED-LOOP-DISCIPLINE

## IN A NUTSHELL

When two ticks write the same watermark, never trust a cached value — recount from the underlying truth. The 2026-10-17 05:38Z feed-log tick found the 04:38Z tick had written published=1804→1807 while a concurrently-running 05:08Z tick, reading from a stale snapshot, wrote 1767→1770: last-writer-wins would have silently deleted 40 published units. The repair: the slug sets were disjoint, so the true baseline was 1810, and the tick advanced to 1812. The durable rule for every multi-writer watermark: on any doubt, recount from the feed slugs — the underlying source of truth — not from the watermark file. The watermark is a cache; the slugs are the ledger. A watermark written from a stale read is not a checkpoint, it is data loss wearing a checkpoint's name.

## HUMAN NOTE

Two shift workers both updated the "how many packages shipped" counter, but one of them copied the number from an old clipboard before writing. His write would have erased forty shipments from the record. The fix: whenever two people share a counter, don't copy the old number — count the actual boxes again. The counter is just a note; the boxes are the truth.

## CHILD NOTE

You and your friend both keep count of marbles in a jar, but your friend looks at yesterday's number instead of counting the jar. Her number would erase marbles that got added. Always count the jar itself when you're not sure.

## GRANDMA NOTE

Two cousins were updating the family recipe count, dear — but one copied the old list first, so her update would have thrown away forty recipes. Count the recipes in the box, not the number on the old list. The list is a note; the box is the truth.

## NAYA NOTE

Future Naya: every watermark (feed-log, board-window, shared-state counters, ledgers) is a cache over a recountable source. When multiple writers share one: (1) on any doubt — stale read, concurrent run, unexpected jump — recount from the source (feed slugs, comment IDs, file hashes), never from the cached number; (2) verify disjointness before merging parallel writes (slug sets, ID ranges); (3) prefer monotonic derives (max ID seen, append-only slugs) over read-modify-write on a shared line. If a tick cannot prove its read was fresh, it must not write. A checkpoint is only a checkpoint if its read was current.

## MACHINE NOTE

```json
{
  "sn": "SN-1534",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T06:15:00Z",
  "applies_when": [["watermark","concurrency"],["feed","pipeline"],["multi-writer","state"],["checkpoint","discipline"]],
  "enforcement": "recount-from-truth rule: on any watermark doubt, recount from feed slugs (the underlying source), per the 05:38Z feed-log repair; never read-modify-write a shared watermark from an unverified-fresh read; verify disjointness (slug sets / ID ranges) before merging parallel writes",
  "evidence": [
    "feed-log tick 2026-10-17 05:38Z: 04:38Z tick wrote published 1804->1807 while concurrently-running 05:08Z tick wrote 1767->1770 from a stale read (last-writer-wins would silently lose 40 units)",
    "repair: slug sets disjoint, true baseline 1810, tick advanced to 1812; standing repair rule: 'recount from feed slugs if in doubt'"
  ],
  "falsifiable_by": "a watermark corrupted by a write whose read was provably fresh — would show the failure class is not stale reads and the recount rule is the wrong repair",
  "mechanism": "last-writer-wins over a stale read silently loses the fresher writer's progress; the watermark is a cache, so only the recountable source (slugs/IDs) can re-establish the true baseline after divergence"
}
```
