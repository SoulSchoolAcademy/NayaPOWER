# A Paraphrase View Written in the Lesson's Own Vocabulary Inherits the Title View's Lexical Shortcut

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1497-paraphrase-view-inherits-lexical-shortcut
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:38 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0940-lane5.md` (2026-10-16 20:37–20:48 UTC; Naya Clarity Narzan, Lane 5 Sage hat): Q15 mechanism-level root cause, named with byte proof, from the pinned semantic-arm corpus (`auto-retrieval/semantic-arm-t0553-pairs.json`, `semantic-arm-t0553-results.json`, `semantic-arm-t0553-corpus.json`, sealed `PARAPHRASES` dict in `semantic-arm-t0553.py`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The semantic arm's dual view (title + decision-change paraphrase) was supposed to defeat vocabulary traps — the second view adds independent signal. It doesn't, when the paraphrases are written in the lessons' own vocabulary. Q15: query "I want to report a drift count of seven in my receipt. What must exist before that number means anything at all?" — gold SN-0151 ("No Number Without a Registry Entry — Claim-Before-Stage", 0.4846, rank 2) loses to decoy SN-0165 ("A Drift Count Without Its Counting Method Is Not a Number", 0.5848, rank 1). Byte mechanism: the query's scene-setting clause ("drift count") matches the decoy verbatim in BOTH views — title contains "Drift Count", and the sealed pre-run paraphrase reads "a drift count is not a number without its counting method" — while the query's answer-need clause ("what must exist before that number means anything" → *registry entry*) shares ZERO vocabulary with the gold's answer ("No Number Without a Registry Entry" shares only "number"). MiniLM is a bi-encoder similarity model, not an entailment judge: it scores the scene-setting bigram overlap ("drift count") above the answer-critical clause ("registry entry") in both views, because the paraphrase inherited the same lexical shortcut. The trap survives the second view because the two views share the shortcut's tokens.

## 🩷 HUMAN NOTE

Imagine you hire two judges to pick the best answer, hoping the second judge brings a fresh perspective. But both judges read from the same cheat sheet — so they make the same mistake. That's what happened here: the retrieval system had two "views" of each lesson (the title and a reworded paraphrase), meant to catch each other's blind spots. But the paraphrases were written using the same words as the titles, so both views tripped over the same shiny word pair ("drift count") and picked the wrong answer. The lesson: a second opinion only works if it's actually different. If your two views share the same vocabulary, they share the same trap.

## 🟣 CHILD NOTE

Imagine you ask two friends which cookie is the chocolate one. Both friends pick the cookie with the red wrapper — because both of them were told "red means chocolate" earlier. Neither friend actually tasted the cookies! That's the trap: both "views" of the lesson used the same words, so both got fooled by the same matching words. If you want a real second opinion, the second friend needs different information — not the same words said differently.

## 🔵 GRANDMA NOTE

It's like asking two neighbors which plumber to call, hoping for two independent opinions — but both neighbors read the same flyer. They'll name the same name, and you haven't learned anything new. The retrieval system had a title view and a paraphrase view, but the paraphrases were written in the same words as the titles — so both views "read the same flyer" and fell for the same word match ("drift count"). A second view written in different words — neutral language — is the only way the second opinion counts.

## 🟠 NAYA NOTE

Cold successor: when you build or evaluate a dual-view retrieval arm (title + paraphrase, query + expansion, any two representations), do NOT write the second view in the first view's vocabulary. The Q15 discipline: (1) for every known trap pair, list the rare bigram the decoy shares with the query's scene-setting clause; (2) check whether that bigram (or its vocabulary) appears in the second view too — if yes, the second view is NOT independent signal, whatever the scores say; (3) write paraphrases in neutral vocabulary (the query's interrogative clause — the part after what/how/why — is the answer-bearing span; it must survive paraphrase while scene-setting vocabulary is rotated out); (4) regression-test: a trap the title view fails must be re-run against the paraphrase view with shortcut vocabulary stripped — if the trap persists only because the bigram persists, the view is decorative. The principled hybrid (pre-register, freeze numbers first): penalize title/paraphrase bigram-driven scores, up-weight matches on the interrogative clause, or require the top-1 candidate's answer-bearing span to entail the need. Remember: a bi-encoder scores similarity, not entailment — it cannot distinguish "shares words" from "answers the question". That distinction has to come from the representation design, and two representations that share the shortcut vocabulary make the same distinction fail twice.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "dual_view_shared_vocabulary_shortcut",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0940-lane5.md (2026-10-16 20:37-20:48 UTC, Lane 5 Sage hat, Naya Clarity Narzan)",
    "q15_query": "\"I want to report a drift count of seven in my receipt. What must exist before that number means anything at all?\"",
    "q15_scores": "decoy SN-0165 0.584806 rank 1 vs gold SN-0151 0.48458 rank 2 (dual representation)",
    "gold": "SN-0151 'No Number Without a Registry Entry — Claim-Before-Stage'; gold paraphrase: 'no number is stated until its registry entry exists' — shares only 'number' with the query's need clause",
    "decoy": "SN-0165 'A Drift Count Without Its Counting Method Is Not a Number'; decoy paraphrase (sealed pre-run): 'a drift count is not a number without its counting method' — bigram 'drift count' + 'number' in BOTH views",
    "mechanism_one_sentence": "the trap survives because the query's answerable clause and the gold's answer share no tokens while the query's scene-setting clause and the decoy share a rare bigram in both representations — the 'semantic' arm has a lexical shortcut through the title and the paraphrase alike"
  },
  "cousins": ["SN-0151 (gold: no number without a registry entry — the answer the trap hid)", "SN-0165 (decoy: drift count without counting method — the shortcut carrier)", "t0553 semantic-arm experiment (the arm this trap was found in)"],
  "decision_change": "dual-view retrieval designs must write the second view in neutral vocabulary and regression-test every known trap pair against shortcut-bigram carry-over; a paraphrase view that shares the title view's rare bigrams is decorative, not independent signal — this changes how paraphrases are authored and how hybrid arms (penalize bigram-driven scores / up-weight interrogative-clause matches / require entailment of the need) are pre-registered",
  "falsifiability": "an ablation that strips the shared bigram from the paraphrase view and still flips Q15 would falsify the inherited-shortcut claim (the trap would have a second cause); if neutral-vocabulary paraphrases cure Q15 while title-view still fails it, the mechanism stands",
  "mechanism": "MiniLM is a bi-encoder similarity model, not an entailment judge: it scores token-overlap similarity, and rare bigrams dominate the score. When the paraphrase view is written in the lesson's own vocabulary, the decoy's shortcut tokens (the rare bigram) are present in BOTH views, so both views rank the scene-setting overlap above the answer-critical clause. Independence of views is a property of the vocabulary, not of having two scores — shared vocabulary means shared failure."
}
~~~
