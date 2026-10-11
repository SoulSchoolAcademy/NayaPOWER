# Retrieval Must Rank on Applicability Triggers, Not Generic Titles

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0824-retrieval-rank-applicability-triggers
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6089544416 (2026-10-09).
**Provenance:** #1354 6089544416 (2026-10-09T21:27:31Z — independent 43-lesson retrieval diagnostic); PR #2058 `naya-integrator/43-smart-note-learning-exam-20261009`; evidence `.naya/evaluations/learning-exam-43/evidence/repository-retrieval-audit-20261009.json`, commit 3920e4f122a3c2540e42f67e39a40b896b75596d; CI head b62e0ff93295f2d4d648705303bac1ad5a711bca 7/7 actions green.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An independent 43-case held-out paraphrase diagnostic (PR #2058) ran 43 distinct scenarios through the general `smart_note_v2.retrieve` selector and got MATCH_ID 2/43 (SN-0470, SN-0496), WRONG_NOTE 40/43, BLOCKED_ID_COLLISION 1/43 (SN-0501). The supported failure hypothesis: each note's digest carries title+essence+lesson+**trigger_conditions**, but the retriever scores only registry titles, the projection nutshell, generic keywords, and topic — relevance ranking is never driven by the digest's distinct applicability triggers. Relevance is a matching problem, and the matcher is ignoring the field built for matching. The repair belongs in the single canonical path (#1886 owner to independently reproduce PR #2058's exact SHA and repair canonical retrieval/metadata relevance — NOT a second Brain or a second index).

## 🩷 HUMAN NOTE

Shawn — one of the lanes built a proper blind test for the brain's lesson-finder: 43 real-world scenarios, each phrased differently than the original note, to see if the retriever could find the right lesson. It got 2 right out of 43. The good news: the test itself is honest — CI ran it clean, and the harness reports what actually happened instead of inflating. The cause they found: the retriever ranks notes by their generic titles and keywords, while every note's digest already contains *trigger conditions* — the exact "use me when this happens" signals — that the retriever never looks at. The fix goes into the one canonical retrieval path, not a second brain. Also flagged along the way: the registry holds 42 unambiguous IDs plus a duplicate SN-0501 — no invented records, just what exists.

## 👶 CHILD NOTE

Imagine a library where every book has a sticky note saying "read me when you're sad about a test" — but the librarian ignores the sticky notes and only reads the book covers. The test showed the librarian picks the wrong book 40 times out of 43. The fix: read the sticky notes.

## 👵 GRANDMA NOTE

They tested whether the machine can find the right lesson when it's needed. Out of 43 tries it found the right one twice. The reason: the finder looks at book titles instead of the little notes that say when each lesson applies. Those notes exist — the finder just wasn't taught to read them. They're teaching it now, in the one official place, not building a second machine.

## 🧠 NAYA NOTE

This is a selector-discriminability finding, not a forgetting finding. Interpretation from the diagnostic: this does NOT prove 40 lessons are forgotten and does NOT contradict the separate 14/14 learning battery — a named battery is not general-purpose retrieval; keep claim-matched provenance and never silently equate them. Full battery conditions (control/treatment, negative transfer, second cold successor, longitudinal use) were NOT run, so FULL_LEARNING_PASSES=0 reads as unassessed, not zero. All CI green means the harness executed accurately — never convert harness success into learner success. The diagnostic remains CANDIDATE; #1886 owns the repair.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0824",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": [
    "gh:SoulSchoolAcademy/NayaPOWER#1354:6089544416",
    "gh:SoulSchoolAcademy/NayaPOWER#2058",
    ".naya/evaluations/learning-exam-43/evidence/repository-retrieval-audit-20261009.json@3920e4f"
  ],
  "results": {"MATCH_ID": "2/43 (SN-0470, SN-0496)", "WRONG_NOTE": "40/43", "BLOCKED_ID_COLLISION": "1/43 (SN-0501)"},
  "failure_hypothesis": "retriever scores registry titles + projection nutshell + generic keywords + topic; digest trigger_conditions ignored",
  "rule": "relevance ranking must be driven by distinct applicability triggers (title+essence+lesson+trigger_conditions), not generic titles/keywords",
  "repair_constraint": "fix the single canonical retrieval path; never build a second Brain/index",
  "do_not": [
    "do not equate a named battery score with general-purpose retrieval",
    "do not convert harness success into learner success",
    "do not invent registry records (42 unambiguous IDs + duplicate SN-0501)"
  ]
}
```
