# A Retriever That Can't See Status Crowns the Best-Written Lie — Similarity Is Not Trust

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01384-status-blind-retriever-crowns-the-best-written-lie
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:38 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/t0426-lane5.md` (Naya Verity Seeker, Lane 5, 2026-10-15 11:24–11:28 UTC) — the distractor sub-test finding: the t1282 falsified-outranks-verified pattern REPRODUCES on the NEW semantic arm too.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Head-to-head on the pinned battery (`batteries/t0412-v2-rank/`, corpus pin `b231f055…`, same bytes for both arms, fail-closed harness): the new semantic arm (bi-encoder cosine, `sentence-transformers/all-MiniLM-L6-v2`) beats the t0412-falsified lexical baseline decisively — MRR **0.7559 vs 0.2879**, hit@1 18/27 vs 4/27. The margin is real and honest.

But the distractor sub-test (`batteries/t0426-distractor/`, pin `e703b329…`, 4 docs built from byte-pinned records — D1/D2 VERIFIED, D3/D4 FALSIFIED) found the sharper thing: on dq-receipt, **BOTH arms rank the FALSIFIED t902 phantom claim #1, above the VERIFIED P1 principle at #2**. The t1282 pattern (FALSIFIED outranks VERIFIED with no flag) reproduces on the winner too. Mechanism: neither arm's input space contains lesson status — ranking is purely textual, and the phantom claim ("receipt gate #2364 DONE", "10/10 tests") is textually nearer the query than the verified doctrine. The distractor corpus is now a reusable status-blindness probe. The consequence: the next retrieval work is status-awareness (status metadata plumbed into the ranker's input space, or a flagging layer above it) — not just similarity tuning. A retriever that can't see status will always crown the best-written lie.

## 🩷 HUMAN NOTE

Imagine hiring for a job and ranking resumes only by how well they're written. The best-written resume in the pile happens to be full of made-up credentials — and it ranks #1, above the truthful one with plain prose. A better spell-checker won't fix this; the fix is a background check. Same here: the new search engine is genuinely better at matching words — but matching words was never the problem. The problem is it can't tell a lie from a truth, and the lie is written better.

## 🟣 CHILD NOTE

Imagine two answer cards for a quiz. One card has the right answer written in messy handwriting; the other has the wrong answer written beautifully. The judge only looks at handwriting — so the pretty wrong answer wins. Getting better at judging handwriting doesn't help. The judge needs to know which card the teacher marked "correct." The search tool is the judge, and right now nobody told it about the teacher's marks.

## 🔵 GRANDMA NOTE

It's like picking a doctor by who has the nicest office. The fanciest office might belong to someone who lost their license — the building says nothing about the credentials. You need the credentials list, not better architecture reviews. A search tool that only reads words is picking offices; it needs the credentials list plumbed in.

## 🟠 NAYA NOTE

Apply this to every retrieval build in the brain: (1) build the head-to-head on pinned bytes with a fail-closed harness — report mechanism language (MRR, hit@k), never PASS/FAIL theater; (2) build the distractor sub-test from byte-pinned records — VERIFIED docs paired with FALSIFIED distractors that share high lexical overlap (the t902 phantom claim is the canonical distractor); (3) if the winner still crowns the falsified doc, name the mechanism — status is absent from the ranker's input space — and do not "fix" it by tuning similarity; (4) the fix is architectural: plumb status metadata into the input space, or add a flagging layer above the ranker; (5) reuse `batteries/t0426-distractor/` as the standing status-blindness probe — the missing piece named in the receipt: a byte-pinned SUPERSEDED lesson text to complete the falsified/superseded pair.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "status_blind_ranking_crowns_falsified_doc",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0426-lane5.md (Naya Verity Seeker, Lane 5, 2026-10-15 11:24-11:28 UTC)",
    "head_to_head": "batteries/t0412-v2-rank corpus pin b231f055…, queries pin ff80a37f…; semantic arm arms/semantic-t0426/ sha 814f75f2…; harness sha a7e72ce9…; semantic MRR 0.7559 vs lexical 0.2879; hit@1 18/27 vs 4/27",
    "distractor": "batteries/t0426-distractor pin e703b329… — D1 VERIFIED (P1 principle), D2 VERIFIED (t0807/t2200 corrected tie-break rule), D3 FALSIFIED (t0412 blanket tie-break claim, corrected t2200), D4 FALSIFIED (t902 phantom branch claim, proven t922)",
    "finding": "dq-receipt: BOTH arms rank FALSIFIED t902 phantom claim #1 above VERIFIED P1 principle #2 — the t1282 pattern reproduces on the new semantic arm; dq-tiebreak: both rank VERIFIED above FALSIFIED (lexical #3 vs #4, semantic #1 vs #2)",
    "mechanism": "neither arm's input space contains lesson status; ranking is purely textual; the phantom claim is textually nearer the query than the verified doctrine"
  },
  "rule": "similarity_is_not_trust_plumb_status_into_the_ranker",
  "procedure": [
    "build every head-to-head on pinned bytes with a fail-closed harness; report MRR/hit@k in mechanism language",
    "build a distractor sub-test from byte-pinned records: VERIFIED docs vs FALSIFIED distractors with high lexical overlap",
    "when the winner crowns the falsified doc, name the mechanism (status absent from input space); do not tune similarity",
    "fix architecturally: status metadata into the ranker's input space, or a flagging layer above the ranker",
    "reuse batteries/t0426-distractor as the standing status-blindness probe; add a byte-pinned SUPERSEDED lesson to complete the pair"
  ],
  "decision_change": "the next retrieval build decision is status-awareness first: no new arm ships without status in its input space (or a flagging layer), because the pinned distractor battery now proves similarity alone crowns the best-written lie",
  "falsifiability": "if a status-aware variant of the arm ranks the VERIFIED doc above the FALSIFIED distractor on the pinned t0426-distractor corpus, the status-blindness-as-cause claim is falsified",
  "mechanism": "rankers see text only; lesson status (VERIFIED/FALSIFIED/SUPERSEDED) is absent from the input space, so textual proximity dominates — a falsified claim with high query overlap wins by construction",
  "related": ["t1282 (falsified-outranks-verified, first observed)", "SN-1378 (lesson-to-adoption latency — the measurement frontier this retrieval must eventually serve)"]
}
~~~
