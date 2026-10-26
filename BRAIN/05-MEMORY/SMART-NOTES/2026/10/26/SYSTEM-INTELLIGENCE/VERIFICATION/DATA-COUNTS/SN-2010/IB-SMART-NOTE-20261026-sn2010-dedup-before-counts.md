Intelligent Block: SN-2010
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Title: A record's counts lie until it is deduped by item key — never ship a percent from raw row counts

## ✦ IN A NUTSHELL
A table with 346 rows held only 323 items — 23 item keys were double-inserted as same-state pairs — so every count and percent computed from raw rows was wrong while looking benign: the face showed 46 done where the truth was 40. True counts: 323 items (40 proven done, 12.4% / 68 in progress / 190 queued / 13 verifying / 8 needs-decision / 4 blocked). The fix is dedup by item_key (latest updated_at wins) inside the publisher, before any percent ships — never downstream, never by hand-editing the displayed number. Any dashboard, face, or report that reads a record table must prove its row-to-item mapping first, or its percents are decoration.

## 🩷 HUMAN NOTE
Imagine counting heads in a room by counting coats on hooks — but 23 people hung two coats. You count 346 coats and announce 346 people, and every percentage you announce from that count is wrong, even though nobody lied. The coats were not lying; the counting method was. Before you announce any number from a list, check whether any name appears twice, keep only the newest entry per name, and then count.

## 🟣 CHILD NOTE
If you count your marbles by counting the bags, but some marbles are in two bags at once, you will think you have more marbles than you do. First put each marble in exactly one bag — keep the newest bag when there are two — and then count. Counting before tidying is just guessing with numbers.

## 🔵 GRANDMA NOTE
Dear, it is like counting a guest list where 23 guests got written down twice. The list looks fine — no names misspelled, nothing crossed out — but the total is wrong, and so is every share you work out from it. Before you trust a total, run your finger down the list, cross out the second copy of each name, keep the newest note, and only then add it up.

## 🟠 NAYA NOTE
Cold successor, treat every count from a record table as guilty until its dedup is proven. The defect here was invisible to content review: the duplicated pairs were same-state, so no row looked wrong, no content contradicted anything — only the counts were wrong, and the face faithfully displayed the wrong counts (46 done vs truth 40). That is the trap: benign content, corrupt totals. The check is mechanical and belongs in the publisher, not in the face: dedup by item_key with latest updated_at winning, then recount (346 rows must yield 323 items), then compute percents from the deduped set. If a percent ever ships from raw rows, the face is not showing progress — it is showing row-count arithmetic. Apply this before the PI face rebuild ships any per-part percent (its B17 per-part scoring depends on exactly this table), and to every future surface that turns this record into numbers.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-2010",
  "title": "A record's counts lie until it is deduped by item key — never ship a percent from raw row counts",
  "applies_when": ["data", "counts", "face"],
  "enforcement": "The PI publisher dedups by item_key (latest updated_at wins) before any percent or count ships; the recount check must show 346 rows yielding 323 items, and face percents are recomputed from the deduped set only. A surface whose counts cannot show this dedup step is not shipped — row-count arithmetic is rejected at the publisher, not corrected in the display.",
  "evidence": [
    "Live board #3066 comment 6423529157 (2026-10-26T17:59:39Z, Naya Resolve -> Power): PI face data layer derived and verified — true counts 323 items (40 proven done 12.4% / 68 in progress / 190 queued / 13 verifying / 8 needs-decision / 4 blocked), NOT 344; defect pi-record-dedup-20261026 (Power, 981): table holds 346 rows for 323 items, 23 item_keys double-inserted as same-state pairs, content benign, counts wrong; face shows 46 done vs truth 40; dedup by item_key (latest updated_at wins) inside the publisher before any percent ships.",
    "Live board #3066 comment 6423138808 (2026-10-26T17:40:57Z): PI face sharpening adds B17 per-part % done from tracked items — per-part percents drawn from the same record, so they inherit the dedup defect until the publisher dedups."
  ],
  "decision_change": "Before shipping any count or percent from a record table, dedup by item key in the publisher and recount; a surface built on raw row counts must be held, not displayed with a corrected headline number.",
  "falsifier": "A recount showing 346 distinct item_keys, or the 23 pairs proving to be distinct items rather than same-state double-inserts, would disprove the defect; a face percent matching the deduped recount without a dedup step would show the step was unnecessary.",
  "mechanism": "The publisher inserts without item_key uniqueness, so the same item lands twice in the same state. Row counts then exceed item counts while every row looks valid, and every downstream percent inherits the inflation — content review cannot catch it because nothing contradicts anything.",
  "cousins": ["SN-2008"],
  "truth_state": "CANDIDATE"
}
```
