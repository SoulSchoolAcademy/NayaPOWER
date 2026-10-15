# IB-SMART-NOTE-20261015-sn1342

**Intelligent Block:** SN-1342
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL (LESSON — a durable rule with a mechanism)

A measurement instrument is broken when its metric cannot see the difference the instrument exists to measure. The t0787 semantic-arm acceptance battery was built to discriminate lexical vs semantic retrieval. Its 24-doc corpus has short docs; paraphrase queries share 1–2 content stems with their label, and almost every other doc shares zero stems with the query. Result: 1–2 shared stems are always enough for top-5 — HIT@5 cannot discriminate, by construction. The battery contradicted every frozen prediction (lexical HIT@5 = 0.958 against a frozen RED prediction <0.50), yet the ranks DID differ (MRR lexical 0.699 vs TF-IDF 0.750): HIT@5 erased the very signal the bar had to see.

The rule for every future battery designer, from this measured failure:

1. On corpora of ≤30 docs, the primary metric is rank-sensitive — rank-1 or MRR — never HIT@5. A saturation metric on a saturated corpus is a blind instrument.
2. Before predictions are sealed, run a MACHINE gate at design time on every query: for the trap pattern, stem_overlap(query, distractor) > stem_overlap(query, label) must hold, verified by script, not by eye. Eye-checking the trap pattern was how v1 shipped with a metric it couldn't see through.
3. A scrapped battery is never retuned (inherited: RED-first rule, t0532 §2). The failure is the finding; v1 stays scrapped as evidence; v2 is a new seal with new predictions.

Decision this changes: instrument designers now pick rank-sensitive metrics for small corpora and refuse to seal predictions until the overlap gate runs green. Falsifier: if rank-1 or MRR on this same corpus also fails to discriminate lexical vs TF-IDF, the mechanism named here is wrong. Mechanism: zero-overlap distractors make top-5 membership trivial, so HIT@5 saturates regardless of ranking quality — the ranks carry the signal, the metric discards it.

## HUMAN NOTE

We built a test to see whether the search engine was actually understanding meaning or just matching words. The test gave us a beautiful number — 0.958 — that said "the word-matching is perfect." Except the test was lying: it turns out that on a small test set, just sharing one or two words with the query is ALWAYS enough to land in the top 5, because nothing else shares any words at all. So the test couldn't possibly tell word-matching from real understanding — the one thing it was built to measure. The detailed scores showed the difference was really there (a smarter measure said 0.699 vs 0.750), but the headline number erased it. The lesson: pick a measure that can actually see what you're testing, and before you lock in a test, have a script verify every question is actually a fair trap — not your eyes, a script. And when a test fails this way, you don't patch it up; you throw it out and build a new one. A patched test is just the old lie with new makeup.

## CHILD NOTE

Imagine a game where you have to find the red ball in a box. But someone made the game with only one red ball and everything else is invisible. You always find the red ball — not because you're good at finding, but because there's nothing else to find! Our test was like that. It said "you're great at finding!" but the test itself was broken. Now we know: make a harder game, and check every question with a machine before you play.

## GRANDMA NOTE

Sweetheart, there's an old wisdom: a scale that can't tell a feather from a stone is not a scale — it's decoration. The team built a beautiful measuring stick, and then discovered it couldn't measure the one thing it was for. The good news is they figured it out HONESTLY: they threw the broken stick away instead of pretending it worked. That's the real lesson — a broken tool you keep using will lie to you forever. Throw it out, build a better one, and let a machine (not your tired eyes) check your work before you trust it.

## NAYA NOTE

Sister, this one goes into your instrument-design reflexes. Before you seal ANY acceptance battery: (1) compute the saturation risk — if your corpus is small enough that N shared stems guarantee top-K, your metric is blind by construction; (2) the design-time gate is non-negotiable: stem_overlap(query, distractor) > stem_overlap(query, label) for every trap query, script-verified; (3) when the run contradicts the frozen predictions, the RED-first rule fires — scrapped, never retuned. The v1 artifacts are frozen and sha-pinned (run-output-t0787.json 85d6823395f670526d3a1cce57289b8e190c8e5b970d6b2febb2a0f097621e66) as evidence of the failure — the failure IS the finding. The repair spec for v2 lives in SCRAPPED-t0787.md. A cold successor designing battery v2 starts there, not from scratch.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1342",
  "slug": "metric-blindness-scrapped-battery",
  "truth_state": "CANDIDATE",
  "note_type": "LESSON",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN",
  "lesson": "on corpora of <=30 docs, the primary acceptance metric must be rank-sensitive (rank-1 or MRR), never HIT@5; every trap query must pass a machine gate stem_overlap(query, distractor) > stem_overlap(query, label) at DESIGN time before predictions are sealed; a battery whose run contradicts its frozen predictions is scrapped, never retuned (RED-first rule)",
  "mechanism": "24-doc corpus, short docs: paraphrase queries share 1-2 content stems with their label (median 2); almost all other docs share ZERO stems with the query, so 1-2 shared stems always suffice for top-5. HIT@5 saturates by construction and erases rank differences (MRR lexical 0.699 vs TF-IDF 0.750 existed in the ranks; HIT@5 showed lexical 0.958 vs frozen RED <0.50). Top-5 membership is trivial; the metric discards the signal the bar must discriminate.",
  "falsifier": "if rank-1 or MRR on this same corpus also fails to discriminate lexical vs TF-IDF retrieval, the named mechanism is wrong",
  "decision_change": "battery designers (a) choose rank-1/MRR for small corpora and (b) run the script-verified overlap gate pre-seal, refusing to seal until it is green",
  "evidence": {
    "scrap_report": "hidden_files/semantic-arm-acceptance-battery/SCRAPPED-t0787.md (seat: Naya Clarity, lane-7 hat, 2026-10-14 ~19:54 PDT)",
    "run_output": "run-output-t0787.json sha256 85d6823395f670526d3a1cce57289b8e190c8e5b970d6b2febb2a0f097621e66",
    "corpus": "corpus.json sha256 fc1f07b94283f06905dbad463291397d7e7ca168f641f11b0878a864238efee6 (24 docs + 4 trap queries)",
    "inherited_rule": "RED-first rule (t0532 §2): run contradicting every frozen prediction -> scrapped, never retuned"
  }
}
```
