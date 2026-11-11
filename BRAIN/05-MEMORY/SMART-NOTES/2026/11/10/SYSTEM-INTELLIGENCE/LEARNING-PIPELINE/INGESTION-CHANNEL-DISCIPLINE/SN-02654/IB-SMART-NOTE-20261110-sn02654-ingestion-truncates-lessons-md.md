**Intelligent Block:** IB-SMART-NOTE-20261110-sn02654-ingestion-truncates-lessons-md
**Smart Note:** SN-2654
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Daily-learning-review 2026-11-10 16:20 PST (learning-events-2026-11-10-16.md, window 15:20–16:20 PST), which recorded the defect as a standing ingestion-append defect observed in two consecutive notes; verified first-hand this tick by direct read of learn/lessons.md lines 16123–16132 and the ingestion log (run 20261111T000818Z, SN-2653 ingested 2026-11-11T00:08:52Z); branch census this tick: naya4/smart-notes-2026-09-30, max SN-2653, SN-2654 free.

## ✦ IN A NUTSHELL

The ingestion append truncates long fields when it writes a note's section into lessons.md — and the receipt check cannot see it, because it only verifies that the anchor exists. Two consecutive notes prove it: SN-2652's quote ends mid-word at "t3417" and its Evidence ends at "t"; SN-2653's quote ends at "SN-" and its Evidence ends at "captain's MEMORY". The full notes are intact in the repo mirror — only the lessons.md copy is cut short. The lesson: lessons.md is a summary view, never the record. Verify an ingested note's content from the full note in the repo mirror, and never accept an anchor-only receipt check as proof that the content landed whole.

## 🩷 HUMAN NOTE

Shawn — this one is about the summary book cutting sentences short. When a new lesson gets filed, a short version is written into a file called lessons.md. For the last two lessons in a row, that short version stops in the middle of a sentence — one ends with "SN-", the other with a single letter "t". The full lessons are fine where they actually live; only the summary copy is chopped. The danger is quiet: the receipt check that says "yes, it landed" only checks that the lesson's heading is there, not that its words survived. So a chopped lesson can pass as complete. The rule from here: if you want to know what a lesson really says, read the full lesson itself, never the summary — and a receipt that only found the heading is not proof the lesson is whole.

## 🟣 CHILD NOTE

Imagine you copy your homework into a notebook, but your pen runs out halfway through every long sentence — so the notebook says "the answer is SN-" and stops. The real homework on your desk is complete, but the notebook copy is not. Now imagine your teacher checks your work by only looking for the title at the top of the page. The title is there, so she says "good, it's done" — even though half the sentences are missing. That is what happened here: the summary book cuts long sentences short, and the checker only looks for the title. The fix is simple: always read the real homework, not the notebook copy — and when you check, read the whole sentence, not just the title.

## 🔵 GRANDMA NOTE

Dear, this is the rule about the summary book that cuts sentences short. When a new lesson is written down, a short copy goes into the lessons book — but the last two lessons both stop in the middle of a sentence, one ending on "SN-" and the other on a single letter. The real lessons are whole where they live; only the summary is chopped. And the check that is supposed to catch mistakes only looks for the lesson's heading — the heading is there, so it says "all good" while half the words are missing. The standing rule now is plain: never trust the summary book for what a lesson says. Go read the lesson itself, every time. And a check that only finds the heading is not a check at all — it has to read the words through to the end.

## 🟠 NAYA NOTE

This is the ingestion-append truncation instance, and it is distinct from its cousins in the artifact, the evidence, and the remedy — keep it distinct. SN-02206 is about the GitHub contents API silently truncating over 1MB — a silent-truncation cousin in a different channel, with the same remedy shape (verify by blob SHA, not by the returned copy). SN-0356 is about a CSV truncated by a row limit — the lesson there is to audit your own evidence's completeness before declaring the gate wrong; this note is the ingestion-side mirror of that rule (audit the derived copy's completeness before trusting it). SN-1995 is the proof family this note applies: delivery proven only by read-back — and an anchor-only file_contains check is not a read-back. The evidence is two consecutive truncated sections, verified by direct read this tick: learn/lessons.md lines 16123–16131 (SN-2652 — quote ends "t3417", Evidence ends "t") and lines 16132+ (SN-2653 — quote ends "SN-", Evidence ends "captain's MEMORY"). The full notes are intact in the repo mirror (learn/.git-mirror BRAIN/05-MEMORY/SMART-NOTES/...), and the daily-learning-review assessed SN-2653 from the full note, not from lessons.md. The mechanism has two legs. First, the ingestion append path truncates long fields when writing lessons.md sections — a length cap somewhere in the append, which cuts quote and evidence mid-sentence. Second, the receipt's file_contains check verifies only that the anchor string exists in the file, so a truncated section passes: the check's invariant is "anchor present", and truncation preserves the anchor. The enforcement follows directly: when citing or verifying an ingested note, read the full note from the repo mirror, never the lessons.md section alone — a lessons.md section that ends mid-sentence or mid-word is a truncated record, not a complete one, and must be treated as unverified until re-read from the mirror; and the ingestion receipt check must verify field completeness (quote and evidence fully present, ending in complete sentences), not anchor-only file_contains — an anchor-only pass on a truncated section is a false PASS. Honest hole, stated not hidden: the exact truncation point (which step caps the field, and at what length) is not yet traced — the defect is confirmed at the output, the mechanism's first leg is inferred from the output shape, not byte-traced to a line of code.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2654",
  "slug": "ingestion-truncates-lessons-md",
  "title": "Ingestion truncates lessons.md fields and the receipt check cannot see it — verify ingested notes from the repo mirror, never lessons.md alone",
  "observation": false,
  "applies_when": ["ingestion", "lessons-md", "verification", "receipt"],
  "enforcement": "When citing or verifying an ingested note, read the full note from the repo mirror (BRAIN/05-MEMORY/SMART-NOTES/...), never the lessons.md section alone; a lessons.md section ending mid-sentence or mid-word is a truncated record, not a complete one — treat it as unverified and re-read from the mirror. The ingestion receipt check must verify field completeness (quote and evidence fully present, ending in complete sentences), not anchor-only file_contains; an anchor-only pass on a truncated section is a false PASS.",
  "evidence": "Daily-learning-review 2026-11-10 16:20 PST (learning-events-2026-11-10-16.md, window 15:20-16:20 PST): lessons.md sections for SN-2652 and SN-2653 both truncated mid-sentence; full notes intact in the repo mirror; review assessed SN-2653 from the full note. Verified first-hand this tick by direct read: learn/lessons.md lines 16123-16131 (SN-2652 — quote ends 't3417', Evidence ends 't') and lines 16132+ (SN-2653 — quote ends 'SN-', Evidence ends \"captain's MEMORY\"). Ingestion log run 20261111T000818Z: SN-2653 ingested 2026-11-11T00:08:52Z; run 20261111T003819Z added nothing new. Receipt's file_contains check verifies only that the anchor exists, so it cannot catch truncation (stated in the same review). Branch census this tick: naya4/smart-notes-2026-09-30, max SN-2653, SN-2654 free.",
  "decision_change": "A seat deciding whether an ingested note's content is proven must read the full note from the repo mirror; a lessons.md section alone no longer counts as the record. A seat accepting an ingestion receipt must require field-completeness verification; an anchor-only file_contains pass no longer counts as proof the content landed whole.",
  "falsifier": "Refuted if the lessons.md sections for SN-2652 and SN-2653 are complete on re-read (the truncation was a stale read), or if the receipt check is shown to verify field completeness rather than anchor-only presence. Weakens if the truncation traces to a one-off write failure rather than the append path — then the rule narrows to re-verifying sections after write failures.",
  "cousins": ["SN-02206 (contents-API silent truncation over 1MB — verify by blob SHA; same silent-truncation family, different channel)", "SN-0356 (CSV truncated by row limit — audit your evidence's completeness before declaring the gate wrong; this note is the ingestion-side mirror)", "SN-1995 (delivery proven only by read-back — the proof family this note applies; anchor-only file_contains is not a read-back)", "SN-2652 (shared-state concurrent-writer clobber — one of the two notes whose truncation is the evidence)", "SN-2653 (memory-box split — the other note whose truncation is the evidence)"],
  "captured": "2026-11-10",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```