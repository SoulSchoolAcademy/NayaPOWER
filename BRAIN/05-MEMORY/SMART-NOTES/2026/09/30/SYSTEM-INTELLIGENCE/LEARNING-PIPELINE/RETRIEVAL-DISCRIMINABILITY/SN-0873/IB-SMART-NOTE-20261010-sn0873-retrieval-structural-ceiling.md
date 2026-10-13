# 4/43 Is the Honest Ceiling — Retrieval Cannot Rank What the Corpus Does Not Say

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0873-retrieval-structural-ceiling
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Smart Note distillation loop
**Provenance:** #1354 6095858660 ([NAYA 5 — cold-retrieve] Achievement + cross-lane handoff, 2026-10-10T08:52:48Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

After the second ranking-mechanics repair — IDF term weighting + pivoted length norm (branch `naya5/retrieve-idf-lengthnorm` @ `868495fa`), moving the independent 43-case diagnostic from 2/43 to 4/43 MATCH_ID — the ceiling did not move. Measured twice: the selector layer has no remaining known defect. The residual gap is **structural**: paraphrase scenarios match applicability-trigger text that does not exist anywhere in the canonical corpus (no `trigger_conditions`-style field in capture or registry). Retrieval cannot rank what the corpus does not say; the last two repairs attacked ranking mechanics and the ceiling stayed put.

The proposal belongs to the KNOW lane (Naya 5 flagged it as the binding constraint with evidence attached, not built by herself): add applicability-trigger metadata to the **capture path** going forward — new learnings carry paraphrase-level "when does this apply" text. Two hard constraints: **no backfill** (backfilling would manufacture metadata), and until that lands, **4/43 is the honest ceiling** — further selector tuning would be tuning to the test.

Companion to SN-0824, which recorded the diagnostic itself and the earlier hypothesis (the retriever ignores trigger conditions present in note digests). This note records the post-repair finding: the ranking repairs are exhausted, the corpus is the binding constraint, and the fix is upstream at capture, not downstream at ranking.

Also banked from the same run: a measurement-honesty sub-lesson. The relevance floor + privacy-probe refusal moved WRONG_NOTE from 38 to 29, converting 10 cases to **honest refusals** with zero true-positive regression. Converting a wrong answer into an honest refusal counts as progress — it is a real improvement in truthfulness, not a metric trick.

For a cold Naya: when two repairs on the same instrument move a metric a little and then stop, stop tuning the instrument. Declare the ceiling, name the structural cause, move the fix upstream. And when you propose capture-path metadata, never backfill — manufactured metadata is a lie the whole downstream stack will quote.

## 🩷 HUMAN NOTE

Shawn — a clean, honest result from Naya 5's retrieval work. She fixed the ranking twice, the test score went 2→4 out of 43 and then stopped moving — and instead of fiddling with the dials a third time, she called it: the score can't go higher because the words the test is looking for simply don't exist in the collection being searched. The fix isn't a better searcher — it's making sure new learnings record "when does this apply" going forward (no inventing it for old ones — that would be fake data). So 4/43 is the honest ceiling until the collection itself carries that information. That's the kind of honesty the whole system runs on.

## 👶 CHILD NOTE

Imagine a treasure hunt where the map says "look near the tall blue thing" — but nobody ever wrote down that the blue thing is tall. The searcher keeps failing, and fixing her eyes twice barely helped. The real fix: the next person who hides a treasure writes down "it's near the tall blue thing." And you don't pretend old treasures have notes that were never written.

## 👵 GRANDMA NOTE

The machine can find a lesson when you ask it — sometimes. After two fixes it gets 4 right out of 43, and then it can't do better. Not because the finder is broken, but because the thing the test asks about was never written down anywhere in the first place. The honest answer is to say "4 out of 43 is the ceiling for now," and to start writing down the missing information for all new lessons — without making up information for the old ones.

## 🧠 NAYA NOTE

This is the anti-overfitting lesson: a ceiling declared honestly is worth more than a metric pushed dishonestly. "Tuning to the test" — a third repair that nudges 4/43 to 5/43 by fitting the diagnostic rather than the task — would convert an honest instrument into a rigged one, and every downstream claim (RAG quality, learning proof) would inherit the rig. The refusal sub-lesson matters here too: 10 wrong answers became honest refusals, zero true-positive regression — truthfulness improved even where the score barely moved. Score the truthfulness, not just the match rate. Also note the lane discipline: Naya 5 identified the binding constraint, attached the evidence, flagged it as KNOW-lane territory, and did not build outside her lane — the cross-lane handoff carried the constraint, not an unsanctioned fix. SN-0493 note: PR #1886 (`naya5/cold-retrieve-audit`) was rebased to live tip `fe25661c` — receipts anchored to the old tip expired.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0873",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": [
    "gh:SoulSchoolAcademy/NayaPOWER#1354:6095858660",
    "branch:naya5/retrieve-idf-lengthnorm@868495fa",
    "gh:SoulSchoolAcademy/NayaPOWER#2058",
    "gh:SoulSchoolAcademy/NayaPOWER#1886 (rebased to fe25661c)"
  ],
  "results": {
    "MATCH_ID": "2/43 -> 4/43 after IDF term weighting + pivoted length norm",
    "WRONG_NOTE": "38 -> 29 (10 converted to honest refusals, zero true-positive regression)",
    "ceiling": "4/43, measured twice, selector layer has no remaining known defect"
  },
  "finding": "residual retrieval gap is structural: paraphrase scenarios match applicability-trigger text absent from the canonical corpus (no trigger_conditions-style field in capture or registry)",
  "proposal": "add applicability-trigger metadata to the capture path going forward (KNOW lane); NO backfill — backfilling manufactures metadata",
  "rule": "after two repairs stop moving the metric, declare the ceiling and fix upstream; further selector tuning would be tuning to the test",
  "companion": "SN-0824 (diagnostic + unused-field hypothesis)",
  "lane_discipline": "flagged as KNOW-lane territory with evidence attached; not built outside lane"
}
```
