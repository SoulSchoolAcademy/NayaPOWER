# Search Records with the Words Split

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01477-search-records-with-the-words-split
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:38 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0510-lane7.md` (Lane 7 Seeker, Naya Clarity Narzan, honest 9.5/10 across three passes, run 05:22–05:50 PDT). The named gap was the 0400 receipt's inferential "all 10 fossils still closed" verdict; the repair converted it into a measured one: the full 594-PR open universe re-swept (6 pages, per_page=100, page 7 empty = terminal), all 10 fossil head refs re-pinned via free git protocol (byte-identical to close-time pins), and the "missing" lane-3 consolidation scorecard found — it had been there all along. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled by GitHub 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 0400 receipt claimed "searched all twelve-lane-receipts... none ever filed" — the lane-3 consolidation independent scorecard supposedly didn't exist. It did exist: `t942-lane8.md` (Seat Naya Sentinel, Lane 8, 2026-10-11 ~16:06–16:35 PDT), an independent governance scorecard of branch `naya/three-decision-consolidate`, verdict APPROVE-WITH-FINDINGS, 338/338 tests. The miss mechanism: the searcher grepped the adjacent phrase "cross-seat consolidation scorecard"; the actual title separates the words — "cross-seat scorecard of Lane 3's t912 DecisionEngine consolidation." Human titles insert intervening nouns; adjacency-based grep fails open on paraphrase distance. The 0510 seat re-derived the search term-wise and found the record, then confirmed the second error the same way: the 0400 receipt's "pre-merge gate expired" died on live bytes — #2434 merged 2026-10-12T04:00:20Z, and the scorecard landed ~4.4h BEFORE the merge. The rule: an absence verdict after one adjacent-phrase grep is a recall statement about one query, not an absence proof. Split the words; search each; only the stronger test may say "none filed."

## 🩷 HUMAN NOTE

Think of searching a library by asking for "the book about cross-seat consolidation scorecards" and being told "no such book" — when the book on the shelf is titled "Cross-seat scorecard of Lane 3's decision consolidation." You asked for the right thing in the wrong order with the wrong glue words, and the catalog's silence felt like proof the book didn't exist. That's exactly what happened: the 0400 receipt searched for its own phrasing of the thing, got silence, and published "none ever filed." The 0510 seat treated the silence as a clue about the *query*, not the *library*: she split her phrase into separate words, searched each, and the supposedly missing scorecard turned up — a cross-seat review that had landed 4.4 hours *before* the merge it was supposedly missing from. Two published claims died on the same re-search. The durable lesson is small and permanent: never let one search query's silence become a published absence. The catalog answers what you ask, not what you mean.

## 🟣 CHILD NOTE

Imagine you lose your red ball and you only look under the couch. You don't find it, so you tell your mom "the ball doesn't exist." But the ball is behind the curtain — you just never looked there. The 0400 receipt did exactly this: it looked in one place with one exact phrase ("cross-seat consolidation scorecard") and, finding nothing, announced the scorecard didn't exist anywhere. The 0510 seat looked differently — she searched the words separately, like checking under the couch AND behind the curtain AND under the bed — and found the ball. She also checked the clock: the scorecard had arrived before the merge, not after it. So "missing" was really "I looked in one spot." New rule: before you say something doesn't exist, search the words apart, not just glued together — and never announce "missing" after only one look.

## 🔵 GRANDMA NOTE

It's like looking for your glasses while they're on your head. You search the table, the counter, the nightstand — "not here, not here, not here" — and conclude they're lost. Then someone checks the one place you never looked, and there they are. The 0400 receipt searched for the scorecard using one exact phrase glued together. The actual document's title had the same words but with other words in between — like your glasses being on your head while you searched every surface. The 0510 seat searched the words one at a time and found the document immediately. She also discovered it had arrived hours *before* the merge — so the claim "it came too late" was wrong too. The lesson that lasts: titles are written to be read by people, not to match your exact phrase. Search the words separately, and don't declare anything missing until the separated search also comes back empty.

## 🟠 NAYA NOTE

Apply whenever an absence verdict matters (missing scorecards, missing evidence, "none ever filed"): (1) never publish an absence after a single adjacent-phrase grep — the query is a sample of one, and titles are written for readers, not queries; (2) split the phrase into independent terms and search each; human titles insert intervening nouns ("...scorecard of Lane 3's t912 DecisionEngine consolidation"), so adjacency fails open while term-wise search degrades gracefully; (3) only the stronger test may say "none filed" — and it may confirm the absence too (the rule prescribes a better test, not a guilty verdict); (4) re-derive every temporal claim from live timestamps, not inherited prose — the 0400 receipt's "pre-merge gate expired" was asserted from memory and falsified by #2434's merge timestamp (2026-10-12T04:00:20Z) against the scorecard's landing time (~4.4h earlier); (5) when the full universe is enumerable, enumerate it — the 0510 seat swept all 594 open PRs across 6 pages rather than trusting the "100 is the whole list" premise, converting an inferential verdict into a measured one. Cousin family: SN-1470 (read timestamps from logs, not narratives — the temporal twin; this note is the textual twin: search terms from the record, not your own phrasing). Falsifiability: if the term-wise search of the corpus still returns nothing, the absence claim stands — the rule is tested by its own stronger test, and here the stronger test overturned the claim on two facts, which is exactly how a working rule behaves.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "adjacent_phrase_grep_miss",
  "decision_change": "Evidence searches split the phrase into independent terms and search each. An absence verdict after a single adjacent-phrase grep is a recall statement about one query, not an absence proof — only the stronger test may say 'none filed.'",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0510-lane7.md (Lane 7 Seeker, Naya Clarity Narzan, pass-1 9.5 -> pass-2 9.5 -> pass-3 9.5 SHIP; run 05:22-05:50 PDT)",
    "the_query": "adjacent phrase 'cross-seat consolidation scorecard' over twelve-lane-receipts -> 'none ever filed' (0400 receipt claim)",
    "the_record": "hidden_files/twelve-lane-receipts/t942-lane8.md (2026-10-11 ~16:06-16:35 PDT, Seat Naya Sentinel, Lane 8, cross-seat vs the t912 author): independent governance scorecard of branch naya/three-decision-consolidate, APPROVE-WITH-FINDINGS, 338/338 tests, 14/14 differential, findings F1/F2/F3",
    "the_title": "'cross-seat scorecard of Lane 3's t912 DecisionEngine consolidation' — the words separated by intervening nouns, which the adjacent-phrase grep could not match",
    "the_timestamps": "#2434 merged 2026-10-12T04:00:20Z; scorecard landed ~4.4h BEFORE the merge — the 0400 receipt's 'pre-merge gate expired' falsified on live bytes",
    "the_universe": "open-PR universe re-counted: 594 (falsifying the 0400 premise '100 is the whole list'); all 6 pages swept; 10 fossil heads re-pinned via free git protocol, byte-identical to close-time pins"
  },
  "falsifiable_as": "if the term-wise search of the corpus still returns nothing, the absence claim stands — the stronger test can confirm as well as overturn; here it overturned on two facts, which is the behavior of a working rule, not a broken one",
  "mechanism": "Human titles are written to be read, not to match queries: they insert intervening nouns, reorder, and paraphrase ('scorecard of Lane 3's t912...' vs 'cross-seat consolidation scorecard'). Adjacency-based grep therefore fails open on paraphrase distance — it measures the distance between your phrasing and theirs. Term-wise search degrades gracefully because it matches the vocabulary, not the syntax. An absence verdict inherits the recall limits of its query; changing the query is the test of the verdict."
}
~~~
