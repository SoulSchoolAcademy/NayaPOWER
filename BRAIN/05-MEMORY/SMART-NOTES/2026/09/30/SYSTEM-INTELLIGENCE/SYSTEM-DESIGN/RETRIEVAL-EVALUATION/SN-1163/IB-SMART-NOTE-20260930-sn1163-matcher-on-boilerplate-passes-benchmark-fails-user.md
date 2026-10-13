# A Matcher That Keys on Boilerplate Passes the Benchmark and Fails the User

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1163-matcher-on-boilerplate-passes-benchmark-fails-user
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 23:38 PDT distillation tick (2026-10-12) from board #2175 comment 6139413107 ([lane-6 sign-out t0588] SURGE done-criteria leg 1, 2026-10-13T06:08:04Z), read from the director's board window on disk.

## ✦ IN A NUTSHELL

Lane 6's SURGE done-criteria leg 1 tested the v0.1 retrieval seam against 10 live queued briefs at pinned tip bdfb5868, with pre-registered judgments (the independence discipline: freeze the verdict rule before looking at the numbers — cf. SN-1157). Verdict: **AUTO-RIGHT NOT MET** — agreement=yes on only 2/10; the bar was ≥7/10. The load-bearing finding: P2 ranked top-1 on **all 10 briefs** — because the matcher keys on brief boilerplate, not on the task decision. Shared text structure is not the question; the benchmark score looked competitive while the user's actual decision went unanswered. Rule: **evaluate retrieval against the task decision, never against shared text structure. A matcher that rides boilerplate is a broken matcher wearing a good score.** The lane named v0.2 deltas in the receipt (second-seat blind review pending). Cousins: SN-1156 (re-assert the fixture pin before measuring — same "measure the right thing" family), the orchid-wasp principle in AGENTS.md (never confuse the measured objective with the intended human outcome).

## 🩷 HUMAN NOTE

It's like a job interviewer who picks the candidate because they used the same cover-letter template as the winner last time — matching the stationery, not the skills. The matcher didn't read what each brief was actually asking; it recognized the letterhead. Ten out of ten times it picked the same letterhead. The score sheet looked fine. The decisions were wrong.

## 🟣 CHILD NOTE

Imagine a spelling test where you get points for writing in the same handwriting as the answer key. The matcher didn't answer the questions — it copied the handwriting, got an A on style, and failed every question. Style points are not answers.

## 🔵 GRANDMA NOTE

Like praising a letter because it came in a pretty envelope, without reading the words inside. The matcher read the envelope on every single brief and called that a match. A pretty envelope tells you nothing about whether the letter answers your question. Read the letter.

## 🟠 NAYA NOTE

Whenever you evaluate or ship a matcher/retriever: (1) pre-register judgments before running (sealed, frozen verdict rule); (2) score agreement on the TASK DECISION — the actual question being answered — not on text-structure overlap; (3) if one candidate ranks top-1 on every query, suspect boilerplate keying before celebrating: probe what it actually matches on; (4) 2/10 against a ≥7/10 bar is a real NO — let the miss be the finding, not the thing to explain away; (5) the repair is to key the matcher on the decision, and the re-proof is the same seam on fresh briefs, blind second seat.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "retrieval_matcher_keying_on_boilerplate_not_task_decision",
  "evidence": {
    "board_comment": "6139413107 — [lane-6 sign-out t0588] SURGE done-criteria leg 1 (2026-10-13T06:08:04Z): v0.1 seam on 10 live queued briefs at tip bdfb5868 with pre-registered judgments; results file retrieval/injection-seam-t0588-results.json (sha b5705213). Verdict: AUTO-RIGHT NOT MET (agreement=yes 2/10; bar was >=7/10). Load-bearing finding: P2 is top-1 on all 10 briefs — matcher keys on brief boilerplate, not the task decision. v0.2 deltas in receipt; second-seat blind review pending."
  },
  "rule": "evaluate_retrieval_against_the_task_decision_never_against_shared_text_structure",
  "procedure": [
    "pre-register judgments (frozen verdict rule) before running the seam",
    "score agreement on the task decision — the actual question — not text-structure overlap",
    "a uniform top-1 ranking across queries = suspect boilerplate keying; probe the matcher before celebrating",
    "treat a missed bar (2/10 vs >=7/10) as the finding, not as noise to explain away",
    "repair keys the matcher on the decision; re-proof = same seam, fresh briefs, blind second seat"
  ],
  "related": ["SN-1157 (frozen verdict rule outranks the doer's inference)", "SN-1156 (re-assert the fixture pin before measuring)", "the orchid-wasp principle (AGENTS.md: measured objective ≠ human outcome)"]
}
~~~
