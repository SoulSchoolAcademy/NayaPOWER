# Retrieval First, Authority Second — Test the Experiment's Actual Queries Against the Live Index Before Designing Around It

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0449-retrieval-relevance-first-authority-second
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Retrieval+Action track, Learning 10/10 program. Live tests on main tip `0a1353bcade21f0c712d8ac793648facc09fbf6e` via `tools/smart_note_v2.py retrieve`. Board #1354 sign-in 6019953810. PR #1590.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Two live retrieval queries on the current tip named the exact defects in under a minute — defects an abstract audit had only described as "retrieval is broken":

1. Query "Nonstop Loop" returned a CANDIDATE restatement (SN-0355) while ratified law lost purely on `captured_at` recency tie-break. The ranker scored keyword overlap only; authority had no voice.
2. Query "skipped producer artifact chain" — the compounding experiment's own note (SN-0418) — returned `NO_RELEVANT_INTELLIGENCE`. The note lives only on the draft branch; the 40-entry registry never heard of it.

The durable rule, in two parts:

- **Test the retrieval path with the experiment's actual queries before designing the experiment around it.** Abstract "retrieval is broken" sends you theorizing; two real queries hand you the defect list.
- **When fixing ranking, order the tie-breaks: relevance first, authority second, recency last.** Score stays primary — a highly relevant CANDIDATE still beats a barely relevant RATIFIED note — and truth-state (RATIFIED=2, VERIFIED=1) breaks relevance ties. The rejected alternative (authority primary) would silently change many existing retrieval outcomes without measurement; the scorecard receipt for that decision rides PR #1590.

And the harder half of the lesson: the ranking fix is necessary but not sufficient. The read-only audit (`tools/retrieval_audit.py`) found the corpus defects are *data* defects — 1 tombstone-pointing SUPERSEDED registry entry (SN-346), 1 unindexed note file (SN-018), 38 of 40 entries CANDIDATE, and the experiment's note absent from the corpus entirely. No ranker retrieves what was never indexed. Machinery repair and corpus feeding are two different jobs; do not declare retrieval fixed after only one.

## HUMAN NOTE

Shawn — when I actually ran the experiment's own questions through the retrieval tool instead of theorizing about "retrieval is broken," the problems named themselves in under a minute: the wrong note wins ties because newer beats more-authoritative, and the note the experiment needs isn't even in the index. The fix I shipped (PR #1590, open for review) makes authority break ties but never overrule relevance — the safe, small change. The bigger half is feeding the index: the notes have to be in the corpus before any ranking can find them. That's the learning lead's next coordination item.

## CHILD NOTE

Imagine a library where the librarian finds books by counting how many words on the cover match what you asked for. Two books match equally — she hands you the newer one, even though the older one is the official rulebook. And the book you actually need was never put on the shelves at all — it's still in a box in the back room. The lesson: first check whether the book is on the shelf (run the real question!), then teach the librarian that when two books match, the official rulebook wins ties.

## GRANDMA NOTE

The team's memory works like a librarian who finds notes by matching words. I tested her with the exact questions the big learning experiment will ask. She gave me the wrong note once — she picked the newer copy over the official one — and once she just shrugged because the note I asked for was never filed on her shelves. I taught her a new rule: when two notes match equally, prefer the official one. But the deeper fix is filing: a librarian can't find what was never shelved.

## NAYA NOTE

Note to future me: whenever a downstream experiment depends on retrieval, run its exact queries against the live index FIRST, on the pinned tip, before designing anything. Two queries beat a week of theory. When you touch ranking, keep relevance primary and add authority only as a tie-break — changing the primary sort key is a behavioral change that needs measurement, not a hunch. And always run the corpus audit too: `python3 tools/retrieval_audit.py` — if the defect is "not indexed," no ranker fixes it. File the note, then fix the ranker. Evidence: PR #1590, tip 0a1353bc, audit run 2026-10-06.

## MACHINE NOTE

{"sn": "SN-0449", "title": "Retrieval First, Authority Second — Test the Experiment's Actual Queries Against the Live Index Before Designing Around It", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "RETRIEVAL-RANKING"], "cousins": ["SN-0418", "SN-0341", "SN-0421"], "evidence": {"tip": "0a1353bcade21f0c712d8ac793648facc09fbf6e", "queries": [{"q": "Nonstop Loop", "got": "SN-0355 CANDIDATE (recency tie-break over ratified law)"}, {"q": "skipped producer artifact chain", "got": "NO_RELEVANT_INTELLIGENCE (SN-0418 absent from 40-entry registry)"}], "audit": {"entry_count": 40, "tombstone_projection": 1, "unindexed_note_files": 1, "candidate_share": "38/40"}, "pr": "#1590 (open, unmerged)", "tests": "55/55 pass (test_smart_note_v2.py 43 + registry drift 12)", "board": "#1354 sign-in 6019953810"}, "rule": "Run an experiment's actual queries against the live retrieval index before designing around it. Rank retrieval by (relevance score, truth-state rank, recency): relevance primary, authority breaks ties, recency last. Corpus feeding (index the note) and ranker repair are separate jobs; neither alone fixes retrieval."}
