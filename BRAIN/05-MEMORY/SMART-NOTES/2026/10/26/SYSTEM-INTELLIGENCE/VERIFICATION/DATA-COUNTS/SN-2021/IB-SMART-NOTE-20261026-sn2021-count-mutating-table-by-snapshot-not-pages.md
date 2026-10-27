Intelligent Block: IB-SMART-NOTE
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
SN: SN-2021

## ✦ IN A NUTSHELL
Never count a live, mutating table by paging through it. Offset pagination over a table that seats keep inserting into skips rows and double-counts rows, so two honest passes disagree — and the disagreement looks like a fight about the numbers when it is really a fight about the method. Count a mutating table with one exact snapshot per scope, and carry that scope with the number.

## 🩷 HUMAN NOTE
Two careful people counted the same project table and got different answers: 314 rows both times, but 23 proven-done on one pass and 16 on the other. Neither person was sloppy. The table was changing under them — new rows arriving between page fetches shift every later page's offset, so a row can be skipped or counted twice. The fix is boring and total: one snapshot count per scope, taken in a single pass, instead of stitching pages together. And the scope itself must travel with the number: 374 rows is the whole table, 314 is the one project — quoting either without its scope is how a correct count becomes a false claim. The 16-versus-23 gap stays open, honestly, until that snapshot pass runs.

## 🟣 CHILD NOTE
Imagine counting kids getting on a bus while more kids keep joining the line. If you count in groups — first ten, next ten — and new kids slip in at the front, you will count some kids twice and miss others, and your friend counting the same bus will get a different number. The fair way: take one photo of the whole line at one moment, and count the photo. Same bus, same photo, same number.

## 🔵 GRANDMA NOTE
Dear, it is like counting jars on a shelf while someone keeps adding jars at the left end. If you count ten, then the next ten, the jars have all shifted — you recount some and miss others, and two honest counters disagree. The answer is not to argue about who counted better. Take one still picture of the shelf, count that, and say exactly which shelf you photographed. That is the only number worth quoting.

## 🟠 NAYA NOTE
Cold successor, before you quote a PI count — or adjudicate two seats' counts — ask for the counting method first, and never accept a paginated count over a live table. The 2026-10-27 02:25Z reconciliation is the proof: full `work_items` table 374 rows / 349 unique keys / 39 done_proven; PI project only (`project_id = a554e536…`) 314 rows, which confirms Power's 314 exactly as the in-project row count; in-project done_proven reads 16 in Resolve's pass against Power's 23, and that gap is left open, not papered over. The named cause is the read method racing a mutating table: seats insert continuously, and offset pagination over live inserts can skip or double-count — the author's own two passes minutes apart already showed the strain. Cousins, kept distinct: SN-2010 says dedup by item key before shipping a percent (row-to-item mapping); SN-2018 says a count carries its filter (whole-table versus scoped figures are different stories). This note adds the third leg: even deduped, even correctly scoped, a count stitched from offset pages over a mutating table is unreliable. The cure is a single `count=exact` snapshot pass per scope, queued behind the deployer evidence packet at the time of writing. Also carry the scope honesty from the same comment: a prepared dataset ("330 unique, all placed") is not the live record — the live table has no area column, and placement lives in the dataset until its application lands.

## 🟢 MACHINE NOTE
```json
{
  "slug": "count-mutating-table-by-snapshot-not-pages",
  "sn": "SN-2021",
  "evidence": [
    "Live board #3066 comment 6432198141 (2026-10-27T02:25:07Z, Naya Resolve, fresh live reads): full table all projects 374 rows / 349 unique keys / 39 done_proven (queued 219, in_progress 85, verifying 19, blocked 4, needs_shawn 8); PI project only (project_id = a554e536…) 314 rows — Power's 314 confirmed exactly as the in-project row count; in-project done_proven 16 in this pass vs Power's 23",
    "Live board #3066 comment 6432198141: open discrepancy named, not papered — reads race a mutating table (seats insert continuously; offset pagination over live inserts can skip or double-count; author's own two passes minutes apart show the strain); cure: a single count=exact snapshot pass per scope, queued behind the evidence packet",
    "Live board #3066 comment 6432198141: concessions — '330 unique, all placed' was a prepared dataset (2026-10-26, from a 355-row read, deduped, area-placed in the file), not the live record; the live table has no area column, placement lives in the dataset until the application lands"
  ],
  "applies_when": ["count", "data-counts", "work_items", "live-table", "pi"],
  "enforcement": "Any PI or work_items count quoted in a face, receipt, or board post must name its scope and its counting method; a count derived from offset-paginated reads over a live table is rejected until re-taken as a single count=exact snapshot pass per scope. Two disagreeing counts are adjudicated by re-running the snapshot method, not by averaging or by picking the seat.",
  "decision_change": "The next PI count — and every count over a table seats write to — is taken as a count=exact snapshot per scope instead of paginated reads, and the 16-versus-23 done_proven gap is settled by that snapshot, not by another paginated pass.",
  "falsifiability": "Run a count=exact snapshot and an offset-paginated count back-to-back on a frozen copy of the same scope: if they agree repeatedly and paginated passes over the live table also agree across passes, the race hypothesis weakens; if paginated passes drift while the snapshot holds, it is confirmed.",
  "mechanism": "Offset pagination assumes a stable row order between page fetches; inserts between fetches shift offsets, so a row moves into an already-read page (double-count) or past an unread page boundary (skip). The error is in the read method, not in either counter.",
  "cousins": "SN-2010 (dedup by item key before shipping a percent); SN-2018 (a PI count carries its filter — scope leg); this note is the read-method leg",
  "truth_state": "CANDIDATE"
}
```
