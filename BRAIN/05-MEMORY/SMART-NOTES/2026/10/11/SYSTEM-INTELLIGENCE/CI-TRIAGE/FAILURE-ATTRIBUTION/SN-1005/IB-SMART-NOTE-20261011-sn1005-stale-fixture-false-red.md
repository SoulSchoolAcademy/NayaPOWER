# Stale-Fixture False Red — After a Legit Contract Change, the Failing Test Is Guilty Until Proven Otherwise

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1005-stale-fixture-false-red
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 12:08 PDT distillation tick (2026-10-11) from #2175 comments 6112565099 ([build lane sign-out — T-20 tip `test` red → PR #2369], 2026-10-11T19:01:50Z) and 6112627502 (sign-out correction — #2369 closed as superseded by #2367, 2026-10-11T19:08:26Z), read live. Live bytes: main tip c510d743.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The tip's `test` check went RED at 18:37:24Z on `c510d743` — right after six mechanism merges (Law 11 v2, decision discipline, conflict resolution, Law 12) landed 18:13–18:36Z. The build lane decomposed it on live bytes instead of assuming a production regression: exactly 4 failures, ALL fixture defects in `tests/test_proof_expiry_integration.py` — the file was written against the PRE-Law-11-v2 gate/door contract. Production behavior was the intended, separately-tested contract; the test fixture still encoded the OLD contract. The fix was fixture-only, zero production bytes, and the proof carried a negative control: the same file at the tip commit fails exactly these 4, and the only delta is the fixture edit. Full suite on the pushed tree: 3593 passed / 11 skipped / 2 xfailed / 0 failed. (PR #2369 carried the fix, then closed as superseded when Lane Beta CI-watch's #2367 landed first with the identical fix plus the brain-index re-stamp.) The lesson: a red tip right after a legit contract change is a *stale-fixture false red* until proven otherwise. Decompose from the live job log, locate the layer — test, fixture, or production — fix only the stale layer, and prove production bytes untouched with a negative control. Fixtures fail first and loudest when the contract moves; treating a fixture failure as a production regression is the waste to avoid.

## 🩷 HUMAN NOTE

It's like a recipe book that says the cake bakes at 350°, but you just upgraded the oven and now everything bakes at 325°. The cake comes out wrong — but the new oven is fine; the *book* is stale. You don't rebuild the oven. You update the page in the book. And you prove the oven is innocent by baking the old recipe at the old temperature: same failure, exactly — so the failure belongs to the book, not the oven.

## 🟣 CHILD NOTE

Imagine your teacher changes the rules of the game — now you get points for teamwork, not just goals. The scorekeeper's old chart only counts goals, so after the game the chart says you lost. But you didn't lose — the chart is just using the old rules. You don't replay the game; you fix the chart. Then you double-check: play one round by the OLD rules with the OLD chart — same "loss" — so the chart was the problem all along.

## 🔵 GRANDMA NOTE

It's like the tailor's measuring tape stretched over the years. He measures you for a suit and it comes out wrong — not because your body changed wrong, but because his tape is off. You don't alter your body; you replace the tape. And you check: measure the old suit with the old tape — same wrong numbers — so the tape was lying, not you. When the team's checking tools are written for yesterday's design, a failure is usually the tool's, not the thing it measures.

## 🟠 NAYA NOTE

Apply this every time a check goes red right after a contract/mechanism change: (1) decompose from the LIVE job log — count the exact failures, name the files (here: exactly 4, all in `tests/test_proof_expiry_integration.py`); (2) locate the layer: is the failure in production behavior, or in a test/fixture written against the OLD contract? (here: fixture written against the pre-Law-11-v2 gate/door — stale); (3) fix ONLY the stale layer — fixture-only edits, zero production bytes; (4) prove it with a negative control: the same stale file at the tip commit fails exactly those failures; the only delta is your fixture edit; (5) run the full suite on the fixed tree to prove nothing else moved (3593/0 here); (6) never merge a "production fix" for a fixture defect — if two seats produce the same fix, the superset vehicle wins and the other closes with its verification standing as corroboration, not a competing PR.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_fixture_false_red_after_contract_change",
  "evidence": {
    "board_comments": "6112565099 — [build lane sign-out] (2026-10-11T19:01:50Z): 'The tip's test check failed 18:37:24Z on c510d743... exactly 4 failures, all fixture defects in tests/test_proof_expiry_integration.py — the file was written against the pre-Law-11-v2 gate/door. Production behavior is the intended, separately-tested contract. Fix is fixture-only, zero production bytes. Full suite on the pushed tree: 3593 passed / 11 skipped / 2 xfailed / 0 failed. Negative control: same file at the tip commit fails exactly these 4; the only delta is the fixture edit.'",
    "correction": "6112627502 (2026-10-11T19:08:26Z): #2369 CLOSED as superseded by #2367 (comment 6112619077) — Lane Beta CI-watch opened #2367 first (18:40:50Z) with the identical fixture fix PLUS the brain-index re-stamp; fixture diff verified substantively identical",
    "merge_context": "six merges landed 18:13–18:36Z before the red (#2359 Decision Discipline, #2360 Law 11 v2, #2361 Conflict Resolution, #2362 Law 12, #2363 respelling fix, #2366 Law 11 v2 wiring)"
  },
  "rule": "red_tip_after_contract_change_is_a_stale_fixture_false_red_until_proven_otherwise",
  "procedure": [
    "decompose from the live job log: exact failure count, exact files",
    "locate the layer — production behavior vs test/fixture written against the old contract",
    "fix only the stale layer (fixture-only = zero production bytes)",
    "negative control: same stale file at the tip commit fails exactly those failures; delta is fixture-only",
    "full suite on the fixed tree to prove nothing else moved; no 'production fix' for a fixture defect",
    "if a second lane ships the same fix first, close yours as superseded — the verification stands as corroboration, not a competing PR"
  ],
  "related": ["SN-0995 (gate-failure triage: GRAMMAR / DISCRIMINATION / DELIVERY — run the layers before the fix)", "SN-044 (red-run triage)"]
}
~~~

---
*DRAFTED 2026-10-11 12:08 PDT — CANDIDATE, NOT RATIFIED. Only Shawn ratifies. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/10/11/SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION/SN-1005/IB-SMART-NOTE-20261011-sn1005-stale-fixture-false-red.md. Rides draft PR #1825 (naya4/smart-notes-2026-09-30) — never merge.*
