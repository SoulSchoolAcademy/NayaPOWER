# Index the Lesson, Not Just the Metadata — Retrieval Matches Its Haystack

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0612-index-the-lesson
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team 3 retrieval track, 2026-10-06. Verified on live main corpus (51ab3c33, 40-entry registry): content-word query "declaring intent before acting" (verbatim lesson language of SN-0359 Captain Protocol) returned SN-042 (wrong); "every seat is the captain of its lane" returned SN-018 (wrong). Root cause: capture stamps every note with identical generic keywords ("smart note", "capture", "intelligent block", ...), so the metadata-only haystack (title/topic/keywords) cannot distinguish lessons. Repair: PR #1611 (merged as f1fa032b) includes each note's IN A NUTSHELL lesson text in the retrieval haystack. Post-fix: both queries return SN-0359. Ranking order unchanged (keyword score → truth-state rank → recency). 44/44 tests pass.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A retriever can only match what's in its haystack. When every captured note carries the same generic keywords, a metadata-only haystack (title/topic/keywords) goes blind to lesson language — content-word queries retrieve wrong notes, and wrong notes drive wrong actions. The repair is to index the lesson itself (the distilled NUTSHELL), not just its metadata. Ranking fixes cannot help: no ranker retrieves the right note if the haystack can't see it. Corpus and representation before algorithm — always.

## HUMAN NOTE

Imagine a library where every book's card catalog entry says "book, pages, reading" — nothing about what the book is actually about. That's what the retrieval corpus was: 40 notes, all tagged with the same generic words. Ask for "declaring intent before acting" and you'd get a book about something else entirely. The fix was simple: put each book's actual summary (the one-paragraph lesson) on its catalog card. Now the right book comes back. The deeper lesson: when retrieval fails, check what the retriever can actually see before blaming the ranking math.

## CHILD NOTE

The robot's memory had 40 notes, but it could only search their titles — not what they actually said. So when you asked about something IN a note, it guessed wrong. We fixed it by letting the robot search what the notes say, not just their titles. Now it finds the right one.

## GRANDMA NOTE

Think of it like a recipe box where every card just says "food, cooking, yummy" on top. You ask for "the chicken soup recipe" and get pancakes. We fixed it by writing what each recipe actually IS on the card. Now you get the chicken soup.

## NAYA NOTE

Future Naya: when you change the capture pipeline's keyword generation, re-verify retrieval with content-word queries (not just title-word queries). The regression test is `test_retrieve_matches_lesson_content_not_just_metadata` in tests/test_smart_note_v2.py. If you ever see "wrong note retrieved" again, check in this order: (1) is the right note in the corpus at all? (2) is the lesson text in the haystack? (3) only then look at ranking. Never tune ranking to fix a corpus or representation problem.

## MACHINE NOTE

```json
{
  "sn": "SN-0612",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "repair": {"pr": 1611, "merge_commit": "f1fa032b", "branch": "naya4/retrieval-lesson-content-haystack"},
  "evidence": {
    "corpus": "main 51ab3c33, 40 entries",
    "before": {"q1": "SN-042 (wrong)", "q2": "SN-018 (wrong)"},
    "after": {"q1": "SN-0359", "q2": "SN-0359"},
    "tests": "44/44 pass"
  },
  "lesson": "Index the lesson (NUTSHELL), not just the metadata. Corpus and representation before algorithm.",
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1611"
}
```
