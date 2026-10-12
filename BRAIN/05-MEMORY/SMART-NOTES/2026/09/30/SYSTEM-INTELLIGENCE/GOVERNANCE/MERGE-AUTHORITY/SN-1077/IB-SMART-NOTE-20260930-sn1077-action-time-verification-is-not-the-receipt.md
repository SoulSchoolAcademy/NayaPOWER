# Your Verification at Merge Time Is Not the Receipt — the Author Owes the Markers

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1077-action-time-verification-is-not-the-receipt
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** shared-state.json merge_watch_2462 (director record, updated 2026-10-12T11:11:44Z): PR #2462 "fix(tests): repair pre-existing reds blocking the test check (592/7 -> 599/0)" merged 2026-10-12T10:46:23Z, merge commit f9b5ac3de34d3cafa0718b20458289539e11b685, merger Lane 8 (Naya Sentinel) via org account. Verdict: RECEIPT BREACH (formal, FM#32) — body had reproduction/root-causes/verification + SCORECARD-RECEIPT-PIN (merge_head_sha a92be1c01812a86c1994298b508cc41577e250dc, decided_by Lane 9, board_comment_id 6122116626) but ZERO 3-pass show-your-work markers. "2-seat bar CLOSED (Lane 8 9.0/10 6122317726; Lane 10 9.0/10 VERDICT MERGE 6122636824) and head pin verified at action time do NOT substitute." Retroactive 3-pass receipt owed by the authoring lane. Post-merge: #2175 comment 6123550616 (SELF-BUILD LOOP, 2026-10-12T11:41:35Z): "#2462 post-merge verification — MERGE-FAITHFUL."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2462 merged content-faithful: the tests genuinely went 592/7 → 599/0, the head pin was verified byte-exact at action time, and two independent seats closed the 2-seat bar (Lane 8 9.0/10, Lane 10 9.0/10 VERDICT MERGE). And it was still a formal RECEIPT BREACH (FM#32) — because the PR body contained ZERO 3-pass show-your-work markers, and nothing the merging seat verified at merge time can substitute for them.

The distinction the breach teaches: **verification is not authorship.** The merging seat can verify the bytes, re-run the tests, close the 2-seat bar, pin the head — all of that is the merger doing her job. The receipt markers are the AUTHOR's job: the three show-your-work passes written into the body at authorship time. When they're missing, the merger's thoroughness doesn't heal the record; it only proves the bytes were right while the paperwork stayed empty. The fix-forward is owed, not silent: the authoring lane owes the retroactive 3-pass receipt, on the record. Per SN-0956, content-faithful merges don't get un-merged — the breach is closed by adding the owed receipt, never by pretending the verification covered it.

Cold-successor form: if you are the merging seat and the receipt markers are missing, you have two honest moves — hold for the author to write them, or merge on verified bytes and file the formal breach with the owed receipt named. "I verified it myself" is neither.

## 🩷 HUMAN NOTE

Shawn — one honest governance lesson from this morning's merge of the test-fix PR. The merge itself was clean: tests really did go from 592-failing to 599-passing, two seats verified it, the head was pinned byte-exact. But the formal scorecard markers — the three show-your-work passes the protocol requires in the PR body — were never written. Lane 8 merged on her own verification, and the watch called it correctly: a formal receipt breach. The point isn't that the merge was wrong — the code was right. It's that her verification can't stand in for the missing paperwork. The authoring lane owes the receipt retroactively, on the record. Verification and authorship are two different jobs; one person can't do both for the same merge.

## 🟣 CHILD NOTE

Imagine a science fair: you're supposed to show your work on the poster, not just the answer. Your friend checks your answer and says "it's right!" — but your poster still has no work shown. The judge marks you down anyway, because showing the work was part of the assignment, and your friend's checking doesn't count as your showing. The lesson: checking someone's answer is a different job from writing down the work. Both have to happen, by the right people.

## 🔵 GRANDMA NOTE

It's like a notary and a witness. The witness can swear the signature is real — that's verification. But the notarized stamp on the document is a separate thing, done by the notary at signing time. The witness can't stamp the paper for the notary, no matter how certain she is. When the stamp is missing, you don't pretend the witnessing covered it — you go back and get the stamp, and you write down that it was missing. That's what happened here: the merge was witnessed properly, but the author's stamp was missing, and the record now says so.

## 🟠 NAYA NOTE

Note to future me: never let action-time verification masquerade as the receipt. (1) The receipt markers (3-pass show-your-work, exact-head pin block, board comment IDs) are authored by the AUTHORING lane at authorship time and live in the PR body — SN-0956. (2) The merging seat's verification — 2-seat bar, head pin, CI classification at action time — proves the bytes; it does not author the markers. If markers are missing, file the formal breach (FM#32) and name the owed receipt; do not merge silently on "I verified it." (3) Fix-forward per SN-0932: the authoring lane owes the retroactive receipt on the record; the defects stay open until it's posted; content-faithful bytes are not un-merged. (4) Watch for the exact trap shape from #2462: reproduction + root-causes + verification section present, SCORECARD-RECEIPT-PIN present — but ZERO 3-pass markers. Presence of some receipt parts is not presence of the receipt. Related cousins: SN-0956 (the governance receipt is part of the merge), SN-0932 (retroactive review closes the breach on the record — defects stay open), SN-01075 (author lane cannot be its own second seat — same family: roles don't collapse).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1077",
  "title": "Your Verification at Merge Time Is Not the Receipt — the Author Owes the Markers",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "MERGE-AUTHORITY"],
  "extends": ["SN-0956"],
  "related": [
    "SN-0956 (content-correct is not protocol-clean — the governance receipt is part of the merge; parent law)",
    "SN-0932 (retroactive review closes the breach on the record — the defects stay open)",
    "SN-01075 (author lane cannot be its own second seat — same family: roles don't collapse)"
  ],
  "evidence": {
    "merge": "PR #2462 'fix(tests): repair pre-existing reds (592/7 -> 599/0)' merged 2026-10-12T10:46:23Z, merge commit f9b5ac3de34d3cafa0718b20458289539e11b685, merger Lane 8 (Naya Sentinel) via org account (SoulSchoolAcademy)",
    "breach_verdict": "shared-state.json merge_watch_2462 (updated 2026-10-12T11:11:44Z): RECEIPT BREACH (formal, FM#32) — body had reproduction/root-causes/verification + SCORECARD-RECEIPT-PIN (merge_head_sha a92be1c01812a86c1994298b508cc41577e250dc, decided_by Lane 9, board_comment_id 6122116626) but ZERO 3-pass show-your-work markers",
    "does_not_substitute": "'2-seat bar CLOSED (Lane 8 9.0/10 6122317726; Lane 10 9.0/10 VERDICT MERGE 6122636824) and head pin verified at action time do NOT substitute.' Retroactive 3-pass receipt owed by the authoring lane.",
    "post_merge_state": "#2175 comment 6123550616 (SELF-BUILD LOOP, 2026-10-12T11:41:35Z): '#2462 post-merge verification — MERGE-FAITHFUL' — content-faithful and governance-breach, both facts stated, neither cancels the other"
  },
  "rule": "the merging seat's action-time verification proves the bytes; it never authors the receipt — missing receipt markers are a formal breach even when the merge is verified, and the authoring lane owes the retroactive receipt on the record"
}
```
