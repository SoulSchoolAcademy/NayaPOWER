# Post-Merge Verification at the Pin — Branch-Green Is Not Merged-True; Prove Negatives Non-Vacuous

**Intelligent Block:** IB-SMART-NOTE-20260930-sn061-post-merge-verification-at-pin
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5933288839 (Naya-4 self-build sign-in+sign-out, 2026-10-01T14:14:41Z) — post-merge independent verification of PR #1125 (V2 selector gates into KNOW retrieval, merged 2026-09-30T23:59Z) at main pin a726a837; full record in goal hidden_files v2-selector-postmerge-verify-2026-10-01.md.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The V2 selector repair was verified green on its branch pre-merge. After the merge, nobody had independently verified the merged artifact. The self-build loop closed that gap: merge commit c3272086 confirmed in main ancestry (101 commits behind tip, gh-api compare), the `selection_now` repair confirmed intact post-merge (`index.ts:119–151`: retrieve pins + records `evidence.selection_now`; inspect replays `selection_now → receipt.created_at → wall clock`), and the suite re-run against the pinned tree: **15/15 pass** (3 positives, 10 negatives, time-bomb pair N11/N12). Then the stronger claim: negatives proved non-vacuous by mutant kill — neutralizing the `V2_TERMINAL_STATUS` gate makes N1/N2 FAIL. One mis-targeted mutant (on the block-level superseded gate) did NOT fail N1 — it was traced to the real cause (N1's attack is an edge-level exclusion, not block-level), documented, and discarded as a diagnostic, not a failed check. The truth status is now SOURCE-VERIFIED AT PIN; the remaining live-behavioral hole (promotion of the repair migrations + a live run) stays parked behind Shawn's drift decision and D1 — named, not hidden. Two lessons: (1) a pre-merge green verifies the branch; the merged tree must be re-verified at its pin, because the merge itself is a state change; (2) a passing negative suite means nothing until a mutant kill proves the negatives CAN fail — and a non-failing mutant is evidence to investigate, not a result to bury.

## 🩷 HUMAN NOTE

Your lawyer drafts a contract change, the partners review the draft, and everyone signs off. Then the final document is printed and filed — and nobody checks whether the signed version matches the reviewed draft. That's the gap: the review certified the draft, not the filed paper. After every merge, re-check the filed version against the pin: is the exact change still there, do the tests still pass on those exact pages, and — critically — do your "this must never happen" tests actually catch the thing when you deliberately break it? If a deliberately broken version still passes your tests, your tests are decoration.

## 🟣 CHILD NOTE

Imagine your friend proofreads your story before you print it, and says "perfect, no mistakes!" Then you print 20 copies — but you never check the printed copies. What if the printer skipped a page, or the file you printed was the OLD version? You have to check the printed copies themselves, not just the draft. And here's the clever part: to prove your "mistake detector" works, you give it a story WITH a mistake on purpose — if it doesn't find the mistake, your detector is broken, even if it said "perfect" before. One tricky case: your friend once hid a mistake in a place the detector wasn't looking — that wasn't the detector failing, it was a wrong hiding spot. Figure that out, write it down, move on.

## 🔵 GRANDMA NOTE

It's like when the pharmacy says "we updated your prescription as the doctor ordered" — you don't just trust the conversation you had before the bottle was filled. You read the label on the bottle you actually brought home: the right medicine, the right dose. And you do one more check: you once asked the pharmacist what would happen if they'd made an error — and they showed you their system would catch it. If their system couldn't catch a deliberate mistake, their "all good" wouldn't mean much. Check the thing you received, not just the promise that came before it.

## 🟠 NAYA NOTE

After any merge you care about: (1) confirm the merge commit sits in main's ancestry and note how many commits behind the tip it is — that is your pin; (2) re-run the claim's test battery against the pinned tree, not the branch; state counts; (3) prove negatives non-vacuous with at least one mutant kill — neutralize the gate under test and confirm the negatives fail; (4) if a mutant does NOT fail, trace it to root cause before discarding — a mis-targeted mutant reveals where the real attack surface is (here: edge-level exclusion vs block-level gate), which is itself intelligence; (5) name the remaining hole explicitly (here: live behavioral proof behind Shawn's gates) — a verified pin closes "implemented ≠ verified at source", not "proven in production". Post-merge verification is a standing self-build-loop item, not a one-off.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "merged_artifact_unverified",
  "evidence": {
    "board": "#554 comment 5933288839 (2026-10-01T14:14:41Z)",
    "target": "PR #1125 V2 selector gates into KNOW retrieval; merged 2026-09-30T23:59Z; verified at main pin a726a837",
    "merge_commit": "c3272086 confirmed in main ancestry, 101 commits behind tip (gh-api compare)",
    "repair_intact": "index.ts:119-151 — retrieve pins + records evidence.selection_now; inspect replays selection_now -> receipt.created_at -> wall clock",
    "suite": "node --test tests/know-v2-selector.test.mjs against the pinned tree: 15/15 pass (3 positives, 10 negatives, time-bomb pair N11/N12)",
    "mutant_kill": "neutralizing V2_TERMINAL_STATUS gate makes N1/N2 FAIL — negatives non-vacuous",
    "mis_targeted_mutant": "block-level superseded-gate mutant did not fail N1; traced to edge-level exclusion (N1's attack is edge-level), documented and discarded as diagnostic",
    "remaining_hole": "live behavioral proof of the selector parked behind Shawn's 2-version drift decision (20260930233038/20260930233137) and D1 (V2 ratification); GRAPH-10 stays 8.5/10"
  },
  "rule": "post_merge_verification_at_pin",
  "procedure": [
    "confirm the merge commit in main ancestry; record distance from tip — that is the pin",
    "re-run the claim's test battery against the pinned tree; state exact counts",
    "mutant kill: neutralize the gate under test; the negatives must fail or they are vacuous",
    "non-failing mutant: trace to root cause, document, discard as diagnostic — never silently",
    "name the remaining hole explicitly (source-verified-at-pin != production-proven)"
  ],
  "related": ["SN-050 (verify the pushed bytes, not the pre-commit bytes)", "SN-028 (clean-room verification)", "SN-043 (compare at ONE commit)"]
}
~~~
