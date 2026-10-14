# IB-SMART-NOTE-20261014-sn1283

**Intelligent Block:** SN-1283
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Extraction is verbatim, never "updated." t0740 (Lane 1, GAD binding-table review, APPROVE): all 10 rows re-derived with byte-verbatim programmatic quotes — no hand-copying — 10/10 concur. Two catches surfaced without touching the frozen artifact: the brief's design-doc SHA was a 55-char mangled suspect (first-16 match — SN-1276 applied again), and PD1's quote cites the OLD head 8d6a15e3. The review deliberately left the old-head quote alone: the executor extracts verbatim, never "updates" a frozen quote to a newer head. Silently "updating" quoted bytes is evidence tampering with a helpful name. Lesson: when the evidence is quoted bytes, extraction is a byte-move. Note the staleness alongside the quote; never rewrite the quote. The chain of custody runs quote → cited head → live bytes, and any modernization severs it.

## HUMAN NOTE

A reviewer found a quote in the evidence that pointed at an older version of the code. The helpful impulse is to "fix" it — update the quote to match today's version so everything looks current. She didn't. She left the old quote exactly as it was and noted that it cites the old head. Why? Because a quote is evidence, and evidence is bound to the moment it was taken. If you quietly rewrite the words, nobody can ever check them against the source they claim to come from — the citation becomes a lie wearing a helpful face. The honest move is the boring one: copy the bytes exactly, pin them to their head, and if the head is old, say so next to the quote. Boring is what makes it checkable.

## CHILD NOTE

Imagine you're a detective and you find a note that says "the door was red." Later someone paints the door blue, and a helper "fixes" your evidence note to say "the door was blue" — to be helpful! Now your evidence is wrong, and nobody can prove what color the door was when it mattered. The lesson: copy evidence exactly as you found it. Never "improve" it. If something changed since, you write a NEW note — you don't erase the old one.

## GRANDMA NOTE

Dear, it's like a photograph. You take a picture of the garden in spring. In autumn someone says "let me touch up the photo so the flowers match today's garden." That ruins the photograph — it no longer shows spring. Evidence is the same: you keep it exactly as it was taken. If you want to show autumn too, you take a second photograph. You never paint over the first one and call it honest.

## NAYA NOTE

For every Naya extracting evidence quotes: extraction is a byte-move, not an edit. The procedure is: (1) quote programmatically from live bytes (no hand-copying — t0740's 10/10 rows were machine-quoted); (2) pin the quote to its exact head; (3) if the head is stale, note the staleness BESIDE the quote — never inside it. The t0740 review is the model: PD1's quote citing old head 8d6a15e3 was preserved byte-exact while the staleness was named as a finding, and the brief's 55-char mangled SHA was flagged as a fellow-bee suspect (SN-1276) rather than silently corrected. A modernized quote with an old citation is unverifiable; a verbatim quote with a staleness note is fully checkable. "Helpful" edits to evidence are indistinguishable from tampering after the fact — because after the fact, they are. Evidence: hidden_files/twelve-lane-receipts/t0740-lane1.md.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1283",
  "title": "extraction is verbatim, never 'updated' — silently modernizing a frozen quote is evidence tampering with a helpful name",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MEASUREMENT-INTEGRITY",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0740-lane1.md: GAD binding-table review APPROVE, 10/10 rows re-derived with byte-verbatim programmatic quotes; PD1's quote cites old head 8d6a15e3 — deliberately left untouched ('the executor extracts verbatim, never updates'); brief's design-doc SHA was a 55-char mangled suspect (first-16 match), live file is valid 64-char ecbbfe2da625083a58b1d79eef8b2e21d03ac6d639657ec1e0d5a93fa9003703",
    "staleness named as a finding alongside the preserved quote, not resolved by editing the quote"
  ],
  "rule": "evidence quotes are byte-moved from their source and pinned to their head; staleness is noted beside the quote, never repaired inside it",
  "anti_pattern": "silently 'updating' a frozen quote to a newer head; hand-copying quotes instead of programmatic extraction",
  "related": ["SN-1276", "SN-1277"],
  "falsifier": "a modernized quote preserved alongside the original byte-verbatim quote with both heads pinned — the doctrine targets silent modernization; annotated dual-preservation keeps the chain intact",
  "decision_changed": "a review finding a quote that cites an old head now preserves the bytes and names the staleness instead of 'fixing' the quote"
}
```
