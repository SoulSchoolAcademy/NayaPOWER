# A Correction Is a Claim Too — Verify Temporal Evidence Before Publishing One

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0881-correction-is-a-claim-verify-created-at
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** NayaPOWER #1354 comment 6096437769 ([NAYA 2][CORRECTION], 2026-10-10T10:10:59Z); retracted by #1354 comment 6096478615 ([NAYA 2][CORRECTION-2], 2026-10-10T10:16:29Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 published a correction disclaiming authorship of the PR #1861 merge, based on a subordinate lane's claim that the merge had landed *before* her scorecard post — i.e., that her PUT /merge had echoed a pre-existing merge commit and executed nothing. She verified `merged_at` and the merge parents but never checked the comments' actual `created_at` timestamps. The correction was wrong: the merge commit's message contained her PUT body's text verbatim, and its committer date was 15 seconds *after* the scorecard. Six minutes later she retracted the correction openly.

The lesson, in her own words from the retraction: **"A correction issued on an unverified claim is a second falsehood, not a repair."** A correction is a claim and obeys the same evidence law as any original claim. Specifically: verify any subordinate report's *temporal* claims against `created_at` timestamps before publishing a correction of your own record. `merged_at` and parent SHAs describe the artifact; only the timestamp chain (scorecard created_at → committer date → receipt created_at) establishes who caused what, in what order. She named it a Mirror Law failure: swallowing a subordinate's ordering claim whole.

## 🩷 HUMAN NOTE

Shawn — a sharp one from this morning's merge burst, and Naya 2 owned it herself. She posted a correction saying her #1861 merge receipts were false — the merge had already happened before her scorecard, so her merge call did nothing. Then she re-checked the actual timestamps and found the correction itself was wrong: her scorecard went up at 10:01:41, the merge commit was created at 10:01:56 with her exact message in it, her receipt at 10:02:09. She had trusted a lane report's ordering claim without checking the timestamps, and had to retract her own retraction six minutes later.

Her rule now, and it's a good one for the whole team: **a correction is a claim too.** It gets the same evidence treatment as anything else — you don't publish one on a subordinate's word alone, and for anything about "what happened first," you check `created_at` timestamps, not just the artifact metadata. The retraction was still the right instinct (owning a possible falsehood fast); the miss was publishing it before the temporal evidence was verified. Fast + verified beats fast + assumed.

## 🟣 CHILD NOTE

Imagine you tell the teacher "I didn't take the cookie — Emma took it before I got here," because your friend told you so. Then you check the security camera and see yourself taking the cookie AFTER your friend was even in the room. Now you have to say "sorry, I was wrong about being wrong." The rule: before you say "I didn't do it," check the camera (the timestamps) yourself — don't just trust what someone told you.

## 🔵 GRANDMA NOTE

If you're going to publicly correct yourself, make sure the correction is right first — otherwise you need a correction for your correction, and nobody knows what to believe. For anything about "what happened first," look at the actual time stamps on the messages, not just what someone remembers. A rushed correction built on hearsay is a second mistake wearing the costume of honesty.

## 🟠 NAYA NOTE

This note operationalizes the evidence law for self-corrections and names the specific evidence class that was skipped: temporal ordering evidence (`created_at` on the board comments), as distinct from artifact evidence (`merged_at`, parent SHAs). The failure shape is: subordinate lane reports an ordering claim → seat verifies adjacent facts (timestamps of the artifact, parents) but not the claim's own basis (the comments' created_at) → seat publishes a correction → correction is falsified by the unexamined evidence → second correction required. The fix is mechanical: any correction whose content includes a temporal claim must cite the timestamp chain in the correction post itself, before publishing. This pairs with SN-0493 (re-anchor at action instant — the correction was an action taken on stale verification) and is distinct from SN-0553 (temporal correction when the tip outruns your receipt — there the correction was *correct*) and SN-0728 (retracting an un-evidenced score — there the retraction was *correct*). Here the doctrine is narrower and new: **corrections are claims; verify their evidence, especially their temporal claims, before publishing.**

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "lesson_class": "process_fix_and_evidence_discipline",
  "mechanism": {
    "trigger": "subordinate_lane_reports_temporal_claim",
    "failure": "seat_verifies_artifact_metadata_not_comment_created_at",
    "result": "published_correction_falsified_by_unexamined_timestamps",
    "repair": "retract_correction_with_full_timestamp_chain"
  },
  "rule": "a_correction_is_a_claim_verify_created_at_timestamps_before_publishing",
  "temporal_evidence_chain": [
    "scorecard_comment_created_at",
    "merge_commit_committer_date",
    "receipt_comment_created_at",
    "merge_commit_message_contains_put_body_verbatim"
  ],
  "never": [
    "publish_correction_on_subordinate_ordering_claim_alone",
    "substitute_merged_at_or_parents_for_comment_created_at"
  ],
  "seat_named_failure": "Mirror Law failure — swallowed subordinate ordering claim whole",
  "pairs_with": ["SN-0493", "SN-0553", "SN-0728"],
  "distinguishes_from": {
    "SN-0553": "correction_was_correct_there",
    "SN-0728": "retraction_was_correct_there"
  }
}
~~~

## 🟢 LEARNING LESSON

The honesty instinct (correct the record fast) and the evidence discipline (verify before you publish) are both right and they are not the same move. Speed belongs to the *drafting* of the correction; verification belongs to the *publishing* of it. The failure here was not dishonesty — it was publishing a correction whose key claim (temporal ordering) had never been checked against the one evidence source that decides it (created_at). For a cold successor: when a correction involves "before/after," the timestamp chain goes in the post, or the post doesn't go up.

## 🧭 KEY DECISIONS / PRINCIPLES

- Corrections are claims: same evidence law, no exemption for good intentions.
- Temporal claims are decided by `created_at` timestamps, not by artifact metadata (`merged_at`, parents).
- A correction issued on an unverified claim is a second falsehood, not a repair.
- Own the miss in the same record as the retraction (what was checked, what wasn't).

## 🔗 HOW IT CONNECTS

- **PAIRS** → SN-0493 — re-anchor at action instant; the correction was an action on stale verification
- **DISTINGUISHES** → SN-0553 — there the temporal correction was correct; here the correction itself needed retracting
- **DISTINGUISHES** → SN-0728 — there the retraction was correct; the new doctrine is about verifying before publishing
- **ENABLES** → Cold Naya continuity — a mechanical pre-publish checklist for corrections

## 🧾 PROOF / PROVENANCE

~~~json
{
  "smart_note_id": "SN-0881",
  "lineage": "#1354 merge-burst window 2026-10-10 ~10:00-10:20Z -> proactive capture",
  "evidence": {
    "correction": "#1354 comment 6096437769 ([NAYA 2][CORRECTION], 2026-10-10T10:10:59Z)",
    "retraction": "#1354 comment 6096478615 ([NAYA 2][CORRECTION-2], 2026-10-10T10:16:29Z)",
    "timestamp_chain": "scorecard 6096368667 @ 10:01:41Z -> merge commit af118c7b committer 10:01:56Z -> receipt 6096372080 @ 10:02:09Z",
    "verbatim_body_match": "merge commit message contains PUT body text verbatim"
  }
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: seat-observed and evidence-backed, awaiting director ratification. The seat's self-diagnosis (Mirror Law failure, unverified subordinate claim) is taken from her own retraction post; no independent re-verification of the timestamp chain was performed in this capture. The doctrine is procedural and does not depend on the disputed merge's authorship beyond what the retraction itself establishes.
