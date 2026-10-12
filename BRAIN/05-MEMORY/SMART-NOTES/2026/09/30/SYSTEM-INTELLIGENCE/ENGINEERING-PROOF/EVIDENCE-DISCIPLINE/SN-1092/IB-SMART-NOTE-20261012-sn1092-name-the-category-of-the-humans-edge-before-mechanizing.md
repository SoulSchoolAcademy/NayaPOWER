# Name the Category of the Human's Edge Before Mechanizing It

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1092-name-the-category-of-the-humans-edge-before-mechanizing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The judge rubric for lesson retrieval (which brief changes the decision / which names the trap / which anchors the decision) does not mechanize at lexical depth: explicit features built from vocabulary overlap scored MRR 0.426 — below dumb TF-IDF cosine (0.502) — and missed the decisive case worse than keywords (rank #14 vs #6; judge #3). The judge's real edge was semantic entailment — seeing that "rank only what would change the decision" *means* a distillation principle with zero shared vocabulary. Lexicalizing meaning-shaped questions replaces understanding with counting, which can never recover a relation that has no vocabulary. It is a category error, not a weak approximation. Before building an automatic arm, name the category of the human's edge — semantic, statistical, or procedural — and build in that category, or declare the mismatch as the hypothesis under test.

## 🩷 HUMAN NOTE

We tried to turn a human judgment rubric into a mechanical formula by counting overlapping words. The formula lost to plain keyword search — because the rubric asks about *meaning* (which brief would change a decision, what trap is hiding), and word counting cannot see meaning. The lesson: if the human's advantage is understanding, don't build the machine out of counting. Name what kind of advantage it is first, then build the matching kind of machine.

## 🟣 CHILD NOTE

If the game is about what things *mean*, you can't win by counting their letters.

## 🔵 GRANDMA NOTE

Don't try to copy someone's wisdom by copying the words they used. Wisdom lives in the understanding between the words — copy that, or you're counting the wrong thing.

## 🟠 NAYA NOTE

Stage-0 automatic retrieval cannot be built as hand-coded rubric features over words. The next mechanization attempt must be semantic (embeddings, entailment), or it asymptotes to TF-IDF. Tuning lexicons on the frozen set would be tuning to the test. The frozen t0392 exam stands: P10 must rank top-5 — no claim beats keywords without it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "block_connections_role": "derived outbound projection",
  "canonical_object": "INTELLIGENT_BLOCK",
  "category_error_rule": "name the category of the human edge (semantic / statistical / procedural) before building the mechanization arm; build in that category or declare the mismatch as the hypothesis under test",
  "experiment": {
    "auto_mrr": 0.426,
    "auto_p10_rank": 14,
    "auto_top5_hit_rate": "7/10",
    "determinism": "one run, then clean-output re-run, identical sha256",
    "discipline": "pre-registered lexicons and thresholds in docstring before the run; frozen ground truth verified by sha256 before judging; ties by frozen packet order",
    "frozen_set": "ground-truth-FROZEN.md (19e08fdc), judge-packet.md (98b10462), judge-map-SEALED.json (fa4e89ce), judge-scores.json (58b10462)",
    "judge_mrr": 0.567,
    "judge_p10_rank": 3,
    "judge_top5_hit_rate": "10/10",
    "n_rows": 10,
    "script": "hidden_files/auto-retrieval-slice3.py (8e82eb70)",
    "tfidf_mrr": 0.502,
    "tfidf_p10_rank": 6,
    "tfidf_top5_hit_rate": "8/10"
  },
  "exam": "t0392 P10 must rank top-5 on brief-t0392-lane2 before any 'beats keywords' claim",
  "knowledge_creates_authority": false,
  "negative_result_is_result": true,
  "scoped_to": "lexical hypothesis only; embeddings / LLM-judge / hybrid arms untested"
}
~~~

## 🟢 LEARNING LESSON

A negative result delivered honestly is a result. The builder's own instrument lost to the dumb baseline, and the failure localized exactly: semantic relations cannot be recovered by vocabulary features. The experiment also proved the negation of its own design — features that scored vocabulary behaved like vocabulary (Principle 10: distill by principle, score decision-change, not vocabulary).

## 🟡 WHAT IT MEANS

This is the methodological boundary for the Stage-0 retrieval work: stop lexicalizing meaning. It turns an expensive dead end into a standing exam (the t0392 P10 test) and a rule that future builders can apply before spending a cycle.

## ⚪ WHAT'S IN IT FOR YOU

You don't have to re-run this experiment. Any retrieval mechanization you design inherits two things: the category-first rule and the exact frozen test it must pass.

## 🟨 HOW TO APPLY / HOW TO USE

1. Ask what the human judge is actually doing — understanding, pattern-matching, or procedure-following.
2. Name the category: semantic / statistical / procedural.
3. Build the arm in that category. If you can't, declare the category mismatch as the hypothesis under test.
4. Pre-register instruments before the run; freeze ground truth by sha256; one run; deterministic re-run.
5. Deliver honest negative results without softening.

## 🔗 HOW IT CONNECTS

- **SUPPORTS** → SN-015 — Active Intelligence Rule (retrieval quality governs applied intelligence)
- **REFINES** → Principle 10 (Distill by principle, delete the rest)
- **REFINES** → Principle 2 (The receipt is the work — pre-registration is the receipt's front half)

## 🧭 KEY DECISIONS / PRINCIPLES

- Test for the category first, tune second.
- Lexicalizing a semantic rubric is a category error, not a weak approximation.
- When the human's edge is semantic entailment, counting words is TF-IDF with extra steps.
- A scoped negative result ("doesn't mechanize at lexical depth") is exact honesty; don't over-claim to "can't be mechanized."
- Tuning on the frozen exam set would be tuning to the test.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "source_receipt": "hidden_files/twelve-lane-receipts/t0412-lane2.md",
  "seat": "Naya Sage (Lane 2), tick t0412, 2026-10-12 ~08:56–09:20 PDT",
  "frozen_artifacts": "ground-truth-FROZEN.md (19e08fdc), judge-packet.md (98b10462), judge-map-SEALED.json (fa4e89ce), judge-scores.json (58b10462), judge_packet.py (f8403eb9), unblind.py (d6463e31), slice2-comparison.md (d6463e31)",
  "instrument": "hidden_files/auto-retrieval-slice3.py (8e82eb70)",
  "comparison": "lane-experiments/t0412/auto-retrieval/slice3-comparison.md",
  "scores": "auto-scores.json (5c87df57, identical both runs)"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Scoped to the lexical hypothesis. Embeddings, LLM-judge, and hybrid arms were not tested. N=10 frozen rows; the instrument was builder-designed (non-blind) with pre-registered thresholds and no iterative tuning — declared in the receipt.

## ➜ NEXT ACTION / SUCCESS CONDITION

Next retrieval arm must be semantic (embeddings/entailment) and must pass the t0392 exam: P10 in the top-5 on brief-t0392-lane2 against the frozen ground truth. No lexicon-tuning on this set.
