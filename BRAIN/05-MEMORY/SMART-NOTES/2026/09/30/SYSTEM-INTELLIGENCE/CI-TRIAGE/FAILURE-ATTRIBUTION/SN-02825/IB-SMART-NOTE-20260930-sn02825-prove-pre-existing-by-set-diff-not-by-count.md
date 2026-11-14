# Prove Pre-Existing by Set Diff, Not by Count — A Failure Count Cannot Prove a Failure Is Pre-Existing

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02825-prove-pre-existing-by-set-diff-not-by-count
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** learning-events-2026-11-14-03.md (hourly learning review, 2026-11-14 ~03:20 PST); CORE-PRINCIPLES.md CANDIDATE 1055; gap-lane-scorer-20261114-0230-lane10.md (2026-11-14 02:55-03:18 PST, 9.5/10); PR #3371.

## ✦ IN A NUTSHELL

PR #3371's `test` run showed 37 failed / 5727 passed / 5 errors, which looked like the re-stamp's fault — until the failure LIST was diffed against main's latest run (40 failed / 5724 passed / 5 errors). Every one of the PR run's 42 FAILED/ERROR lines also fails on main (`comm` empty both ways); main adds exactly 3 — the freshness trio, which PASS on the PR head. The new-head run's failure list is BYTE-IDENTICAL to the old PR head's (sha256 5de950fd3a4f9ee3). The re-stamp caused zero failures and fixes three. Counts can look guilty while the sets prove innocence: a count comparison cannot prove a failure is pre-existing — only a diff of the failing set against main's can. Corollary from the same receipt: a red gate's job log names the fix, its summary names nothing — the Receipt-pin gate failed with an empty summary and a bare "exit code 1", but its job log printed the exact verdict and the repo's checker spelled out the block format; the pin format was fixed from the log.

## 🩷 HUMAN NOTE

Shawn — imagine two classrooms take the same test and both score "3 wrong." That doesn't mean the same three kids got them wrong — one room's three could be entirely different children. Counting wrong answers can't tell you whose fault they are; you have to compare the names. That's what happened with PR #3371: the count looked like the change broke things, but comparing the actual failing tests name-by-name showed every single one already failed on main — and the change actually fixed three. Same for a red gate: its summary says "failed" and nothing else; the job log is where the verdict lives. Never judge by the count or the headline — diff the list, read the log.

## 🟣 CHILD NOTE

Imagine two classes both get 3 answers wrong on a quiz. Does that mean the same kids got them wrong? No — different kids could have missed different questions! To know who needs help, you compare the names, not just the number 3. That's the lesson: count the names, not just the number. And when something says "FAILED," don't stop at the big red word — open the log and read what it actually says went wrong.

## 🔵 GRANDMA NOTE

Dear, it's like two baskets that both hold three bruised apples — that doesn't mean they're the same three apples. To know whether your new recipe bruised any, you have to lay the apples out side by side and compare them one by one. The count tells you nothing; the comparison tells you everything. And when the oven light flashes red, the little display on the front just says "error" — the real reason is written in the booklet underneath. Read the booklet, compare the apples, then decide.

## 🟠 NAYA NOTE

Worked proof: gap-lane-scorer-20261114-0230-lane10.md (2026-11-14 02:55-03:18 PST, 9.5/10). PR #3371 `test` run: 37 failed / 5727 passed / 5 errors. Main's latest run: 40 failed / 5724 passed / 5 errors. Every one of the PR run's 42 FAILED/ERROR lines also fails on main (`comm` empty both ways); main adds exactly 3 — the freshness trio, which PASS on the PR head. The new-head run's failure list is BYTE-IDENTICAL to the old PR head's (sha256 5de950fd3a4f9ee3). The re-stamp caused zero failures and fixes three. Corollary from the same receipt: a red gate's job log names the fix, its summary names nothing — the Receipt-pin gate failed with an empty summary and a bare "exit code 1", but its job log printed the exact verdict (`MISSING ... no '## SCORECARD-RECEIPT-PIN' block`) and the repo's checker spelled out the block format; the pin format was fixed from the log (local checker PASS). Cousins: CANDIDATE 430 (classify every failure from the failing step's own verdict line) and CANDIDATE 661 (name the class from the job log, not the workflow skin) — those cover reading the log; this note names the set-diff proof that a failure is pre-existing. The no-regressions recipe in learn/lessons.md uses the same set-diff mechanism for tip verification (diff the failure sets; the intersection is pre-existing).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "prove_pre_existing_by_set_diff_not_by_count",
  "mechanism": "counts collapse set membership: two runs can show similar failure counts with entirely different failing tests, so a count comparison cannot distinguish 'my change broke these' from 'these were already broken'. The failing set is the identity of the failure; diffing the PR run's failing set against main's (comm) shows whether it is a subset (pre-existing, intersection) or has a non-empty difference (the change's own failures). The same collapse applies to gate summaries: a summary reports the conclusion, the job log holds the verdict line that names the fix",
  "evidence": "gap-lane-scorer-20261114-0230-lane10.md (2026-11-14 02:55-03:18 PST, 9.5/10): PR #3371 test run 37 failed / 5727 passed / 5 errors vs main 40 failed / 5724 passed / 5 errors; every one of the PR run's 42 FAILED/ERROR lines also fails on main (comm empty both ways); main adds exactly 3 (freshness trio, PASS on PR head); new-head failure list byte-identical to old PR head's (sha256 5de950fd3a4f9ee3); re-stamp caused zero failures and fixes three. Corollary: Receipt-pin gate failed with empty summary + bare 'exit code 1'; job log printed exact verdict (MISSING ... no '## SCORECARD-RECEIPT-PIN' block); repo checker spelled out the block format; pin fixed from the log, local checker PASS",
  "falsifiability": "a count comparison that correctly proves a failure pre-existing where the sets differ would show counts suffice; a set diff showing the PR set is a subset of main's while the PR still caused a failure would show the subset test insufficient",
  "decision_change": "any future 'pre-existing' verdict cites the comm diff of the failing set vs main's (empty both ways) instead of a count comparison; any gate report quotes the failing step's verdict line from the job log, never the summary's conclusion",
  "applies_when": ["failure-attribution", "pre-existing", "gate"],
  "enforcement": "a 'pre-existing' verdict in any failure report must cite the comm diff of the failing set vs main's; a count-only pre-existing claim is rejected at lane-scorer review; a gate report must quote the failing step's verdict line from the job log, not the summary's conclusion",
  "related": ["CANDIDATE 430 classify every failure from the failing step's own verdict line - covers reading the log; this note names the set-diff proof", "CANDIDATE 661 name the class from the job log, not the workflow skin - covers reading the log; this note names the set-diff proof", "the no-regressions recipe (learn/lessons.md) - same set-diff mechanism applied to tip verification: diff the failure sets, the intersection is pre-existing"]
}
~~~
