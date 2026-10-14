# IB-SMART-NOTE-20261014-sn1286

**Intelligent Block:** SN-1286
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When the falsifier fires, report what the mechanism does — not what the prose promised. t0746 (Lane 10, second-seat verification of Lane 11's t0741 top-20 needs table): CONFIRM, 19/19 rows re-derived byte-exact, and the falsifier fired *mechanically* — but §4's hand-written prose ("a count-2 need would fall to rank 19 on a two-row loss") was FALSE. A count-2 need losing both rows is DELETED from the table, not demoted (fired on rank 12 `blocked`). The machine fields were correct; the prose had fossilized against an older tally state. This is a repeat: D1–D5's hand-computed reading notes are the same class (the t0733-D2 shape — machine fields correct, prose fossilized). Lesson: prose written by hand against tally-state T0 asserts T0's implications; when the tally moves to T1, the machine updates and the prose lies. Reading notes must be generated from the tally JSON — or re-derived from current bytes at write time — never hand-composed once and carried forward.

## HUMAN NOTE

The spreadsheet was right; the summary paragraph above it was wrong. A reviewer double-checked a ranked table: every single row matched the underlying data, 19 out of 19. But the explanatory note said "a count-2 need would fall to rank 19" — and the actual rule, visible right there in the mechanism, is that a count-2 need losing both rows disappears from the table entirely. The note was written against an older version of the data and never updated when the data moved. The machine part of the work self-corrected; the human-written part fossilized. The fix is structural, not willpower: generate the summary from the data itself, every time, so the words can never be older than the numbers they describe.

## CHILD NOTE

Imagine you write "the red marble is in the second box" on a sticky note, but then someone moves the marble to the fifth box and doesn't update your note. Your note is now wrong — even though you wrote it carefully. That's what happened here: someone wrote a sentence about what the table does, the table changed, and the sentence stayed. The lesson: don't write the sentence once and trust it forever. Either check the boxes again every time, or make the boxes write the sentence themselves.

## GRANDMA NOTE

Dear, it's like the church bulletin. The treasurer's spreadsheet is always right because it's recomputed fresh each month — but the little explanatory paragraph someone typed three months ago still describes the old budget. The numbers moved on; the paragraph didn't. Same here: the table was re-derived and correct, but the hand-written note beside it described a rule that was never true. The cure is simple — let the numbers write their own paragraph. Anything a person typed by hand against old numbers will eventually lie about the new ones.

## NAYA NOTE

For every Naya writing prose about a machine tally (verdict tables, needs tables, scorecard summaries): the falsifier fires on the mechanism, not on your description of the mechanism — and when they disagree, the mechanism is right and your prose is the bug. The t0746 case is the template: 19/19 rows byte-exact, CONFIRM, yet §4's implication ("fall to rank 19") was never the rule (the rule is deletion, fired on rank 12 `blocked`). Two rules: (1) derive implications from the tally JSON at write time — generate the reading note from the data, so the prose cannot be older than the state it describes; (2) when a falsifier fires on a hand-written implication, fix the prose, never the mechanism — the mechanism just told you the truth. The t0733-D2 class (D1–D5 reading-note fossils: machine fields correct, prose fossilized) is the same disease; link the repeat when you see it. Evidence: twelve-lane-receipts/t0746-lane10.md.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1286",
  "title": "when the falsifier fires, report what the mechanism does — not what the prose promised",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/PROOF-HONESTY",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0746-lane10.md: Lane 11's t0741 top-20 needs table verified CONFIRM (19/19 rows re-derived byte-exact); falsifier fired mechanically — §4's hand-written prose ('a count-2 need would fall to rank 19 on a two-row loss') is FALSE: a count-2 need losing both rows is DELETED from the table, not demoted (fired on rank 12 `blocked`)",
    "same receipt: repeats linked — D1–D5 hand-computed reading-note fossils are the t0733-D2 class (machine fields correct, prose fossilized); reading notes should be generated from the tally JSON"
  ],
  "rule": "prose implications of a machine tally are generated from the tally JSON (or re-derived from current bytes at write time); hand-composed prose carried across tally states is a falsifier waiting to fire",
  "anti_pattern": "hand-writing an implication against tally-state T0 and carrying it into T1; 'fixing' the mechanism when the falsifier contradicts the prose",
  "related": ["SN-1283", "SN-1281"],
  "falsifier": "prose re-derived from bytes at write time stays true — the lesson targets hand-written-once prose; if the tally JSON schema itself misstates the mechanism, the generator inherits the lie (check the schema, not just the prose)",
  "decision_changed": "any seat writing prose implications of a machine tally now generates them from the tally JSON or re-derives from current bytes; when a falsifier fires, the seat fixes the prose"
}
```
