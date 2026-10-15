# IB-SMART-NOTE — SN-01423 — A shared token is not a semantic signal: audit retrieval batteries for lexical-collision boosts before quoting agreement

- **Intelligent Block:** IB-SMART-NOTE
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **SN:** SN-01423
- **Category:** SYSTEM-INTELLIGENCE / SYSTEM-DESIGN / RIGOR-SIMPLICITY

## IN A NUTSHELL

When you measure a semantic retrieval arm on live queries, a principle can rank high for the wrong reason: it shares the query's most frequent token, not its meaning. In the first live-dispatch brief-inspection battery, principle P7 ("The brief is a hypothesis") landed top-2 in 4 of 5 queries — because the token "brief" appears 9–22 times in every query and P7's text is the only corpus document containing it. A systematic boost, not semantic agreement. Before quoting any arm's agreement numbers, audit for shared-token artifacts: mask the colliding token, re-run, compare. A headline that can't survive the mask doesn't ship as a finding.

## HUMAN NOTE

The team ran the winning semantic arm against five real dispatch briefs to see if it could recover each brief's dispatcher-embedded principles: 3 of 5 hits, MRR 0.1988. But one pattern kept showing up: P7 sat in the top-2 on nearly every query. The cause wasn't that P7 was the right principle for every brief — it was that every query says "brief" dozens of times, and P7 is the only one of the 15 corpus principles that mentions the word "brief." The embedding mixes word-overlap with meaning, so the shared word acts like a magnet. The fix isn't a better arm; it's a better battery discipline: identify the query-wide tokens, mask them, and re-run before you let anyone quote "3 of 5" as settled. The two misses told the same story from the other side — one was debatable ground truth (P10's embedding on the Heart brief), one was undercoverage (P1 ranked #1 but wasn't in the dispatcher's two-principle embedding). Measurement artifacts and ground-truth limits, not just arm limits.

## CHILD NOTE

Imagine you ask a friend to find the five most similar songs to five different songs — but every song you hand them has the word "moon" in it, and your friend keeps picking the one song whose title says "moon," even when it's nothing like the others. Your friend isn't hearing the music; they're just spotting the word. Before you grade your friend, hide the word "moon" and ask again.

## GRANDMA NOTE

Dear, it's like judging which recipe tastes most like five different cakes, when every cake happens to be vanilla — and your taster keeps picking the one recipe labeled "vanilla," even when the flavor is wrong. The label is drowning out the taste. Cover the labels before you let anyone score the taster.

## NAYA NOTE

When you score retrieval agreement on live batteries, treat shared-token artifacts as the first confound to rule out, not a footnote: (1) count token frequency per query and identify query-wide tokens; (2) check whether any corpus document is the unique carrier of a query-wide token (P7 was); (3) mask the colliding token from the queries and re-run the battery; (4) quote the headline from the masked run, or report the boost delta honestly. The brief-inspection run also hardened the two companion rules: exclude the answer key from queries (the t0761 leak class — `**Principles**` key, broadcasts, pre-mortem all excluded), and autopsy the misses into arm-failure vs ground-truth ambiguity before quoting. Note the honest ceiling the receipt named: two of the three hits sit exactly at rank 3 (boundary fragility), 3 of 5 queries came from one brief family (sample diversity), and no second seat has re-run the battery yet — the 3/3 is first evidence, not a settled "the arm works."

## MACHINE NOTE

```json
{
  "sn": "SN-01423",
  "lesson": "Audit retrieval-measurement batteries for shared-token boost artifacts (mask-and-rerun) before quoting agreement numbers.",
  "anti_pattern": "Quoting an arm's hit rate while a query-wide token silently carries the ranking; grading the friend while the word 'moon' is still visible.",
  "mechanism": "Embeddings mix lexical overlap with semantic similarity. When a query-wide high-frequency token ('brief': 9-22x per query) appears in exactly one corpus document (P7), that document receives a systematic rank boost unrelated to meaning — top-2 in 4 of 5 queries. Masking the colliding token removes the lexical channel and isolates the semantic signal; the delta between masked and unmasked runs quantifies the artifact.",
  "decision_change": "Future decision — any retrieval-measurement battery closes with a shared-token audit (mask colliding tokens, re-run, report the delta) before its agreement numbers are quoted or wired into dispatch; verdicts that die under the mask don't ship as findings.",
  "falsifiability": "Mask 'brief' from the 5 t0461 queries and re-run the pinned arm: if ranks are unchanged (no boost delta), the artifact claim is falsified for this battery and the lesson's prescription was unnecessary here. Weakened across batteries if masked re-runs never change any decision.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0461-lane5.md (9.3/10, Seeker hat, honest below 9.5)",
    "battery": "batteries/t0461-brief-inspection/queries.json (sha 3140c5e401169afb); arm arms/semantic-t0426 (sha 814f75f203cf7e73...); corpus batteries/t0412-v2-rank (sha b231f055fb959552..., 15 principles P1-P15); harness bin/semantic_arm_harness.py (sha a7e72ce93bd75df0...); results brief-inspection-t0461/scores.json (sha 65c76ce5e89fe5ae)",
    "artifact": "P7 top-2 in 4/5 queries; 'brief' occurs 9-22x per query; P7 is the only corpus doc containing the token",
    "metrics": "MRR 0.1988, hit@1 0.0, hit@5 0.300 (n=10); hits at exactly rank 3 for 2 of 3 hits (boundary fragility)",
    "companion_disciplines": "answer-key exclusion from queries (t0761 leak class); miss autopsy: t0492-lane11 = ground-truth ambiguity (P10@15), t0431-lane6 = undercoverage (P1@1 unlisted)"
  },
  "related": ["SN-1418 (name the carrier stem — same family: headline must survive the artifact audit)", "CANDIDATE 19 (anti-proxy tripwire F3: vocabulary overlap -> falsified)", "CANDIDATE 363 (similarity is not trust — plumb status into the ranker)"]
}
```
