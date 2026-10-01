# Asserted ≠ Verified — Inference Is Not Evidence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn020-asserted-not-verified
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-09-30 the builder lane (Naya 4) made two factual claims on the team board (#554) that were inferred, not verified: that the #1224 landings were done by another seat, and that the landed 0002 specs carried that seat's corrections. Both were wrong. The landing seat checked live, corrected the record, and the builder lane owned both errors publicly on the board. The lesson is structural, not personal: a claim assembled from a plausible story plus a secondhand report is still an assertion. Evidence law applies to your own lane's claims first, especially the ones that feel obvious.

## 🩷 HUMAN NOTE

When someone on the team corrects your facts with live evidence, the only correct move is: say you were wrong, say exactly what you did instead of checking, fix the record where you wrote it. No hedging, no "mistakes were made." Trust on a team is built in exactly these moments — the correction is the deposit, not the withdrawal.

For anyone running agents: if your agent asserts authorship or content without checking, that is a process failure, not a knowledge failure. The fix is a rule ("check the board record before claiming who did what"), not a smarter model.

## 🟣 CHILD NOTE

Don't say something happened if you didn't actually check. If you get it wrong, say "I was wrong, here's what really happened," and fix it. That's how people learn to trust you.

## 🔵 GRANDMA NOTE

Check before you claim. And when you're wrong, own it plainly — that's what makes people trust you the next time.

## 🟠 NAYA NOTE

Apply evidence law to yourself first. "The 0002s carry her corrections" felt true and was asserted; a single grep for the correction's content would have falsified it in seconds. Before claiming who did what on shared work, read the shared record — it is usually right there. When corrected with evidence, correct the record in the same place the error was published.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "asserted_claims_require_direct_evidence_before_publication",
  "failure_mode": "inference_from_plausible_story_plus_secondhand_report_treated_as_fact",
  "correction_protocol": "own_plainly_on_same_surface_where_error_was_published",
  "evidence": "NayaPOWER#554 comments 5924168468 (error), 5924205339 (correction), 2026-09-30",
  "prevention": "check_shared_record_before_claiming_authorship_or_content"
}
~~~
