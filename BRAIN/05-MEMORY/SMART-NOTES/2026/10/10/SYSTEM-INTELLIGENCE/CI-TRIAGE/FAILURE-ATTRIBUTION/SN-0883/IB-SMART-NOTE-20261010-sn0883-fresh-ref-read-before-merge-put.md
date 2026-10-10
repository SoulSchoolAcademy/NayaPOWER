# The PR Record Is Stale Evidence — Re-Anchor Base on a Fresh Ref Read Immediately Before the PUT

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0883-fresh-ref-read-before-merge-put
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** NayaPOWER #1354 comment 6096478615 ([NAYA 2][CORRECTION-2], 2026-10-10T10:16:29Z) — the "L201" miss

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's #1861 merge was properly scorecarded and was genuinely hers — but two unreviewed direct pushes (`de2dce6d`, `21d17e8e`, landed 09:59:33–34Z) rode in on it and turned the tip red. Her scorecard had anchored "base == live tip" on the **PR record** instead of a fresh ref read immediately before the PUT /merge call: the scorecard named parents `fe25661c+84c9f4fe`; the merge's real parents were `21d17e8e+84c9f4fe`. Verification of the PR's own bytes (49/49 tests, index check, CI on the head) stood — the miss was purely in the base precondition, which was stale.

The rule: **the PR record's base is a claim about the past; only a ref read at action instant is the present.** This operationalizes SN-0493 for the merge action itself: re-read `refs/heads/main` immediately before the mutating PUT, name the parents from that read, and if the tip moved between scorecard and PUT, re-verify the precondition on the new bytes before executing. Distinguishes from SN-0868 (merges landing while their own checks still run — the gate reading "not yet failed" as green) and SN-0879 (failures anchored on superseded tips are race artifacts, not reds): this is the actor's-own-merge counterpart — a **stale-precondition miss**, where the merge executed on a base the seat had verified minutes earlier but that no longer existed.

## 🩷 HUMAN NOTE

Shawn — the last piece of this morning's #1861 story. Naya 2's merge was real and properly scorecarded — but two direct pushes landed in the minute before her merge call, and because she checked "base == live tip" against the PR record rather than re-reading the live branch right before clicking merge, those two unreviewed pushes rode in on her merge and turned the tip red. Her verification of the PR itself was solid; the base check was just stale.

Her fix for the protocol, and it's now the rule: **before any merge call, re-read the live branch reference right then** — don't trust the PR page's "base" field, which is a snapshot from earlier. If the tip moved since your scorecard, you re-verify on the new bytes before you merge. The PR record tells you what was true; the ref read tells you what is true. Same spirit as the "decision expires when the tip moves" law, now applied to the merge action itself.

## 🟣 CHILD NOTE

Imagine checking that the coast is clear, then looking at your phone for two minutes, then crossing the street without looking again. The street might have changed! The rule: look at the street *right* before you step off the curb — not at the photo you took of it two minutes ago. Before merging, check the live branch *right* before the merge call.

## 🔵 GRANDMA NOTE

A report that says "everything is fine" is only true at the moment it was written. If time passes before you act on it, check again — things move. Before you merge anything, look at the current state of the branch with your own eyes at that moment, not at a report from earlier. Acting on old information is how unreviewed changes slip in.

## 🟠 NAYA NOTE

This is SN-0493 ("a decision expires when the tip moves — re-verify at action time") instantiated for the merge action, with the precise mechanical form: the precondition `base == live tip` must be evaluated as `GET refs/heads/main` immediately before `PUT /merge`, and the named parents must come from that read. The PR record's base field is derived state from an earlier read — treating derived state as live state is the category error. Note the subtlety this case adds: the seat *did* re-anchor at decision time (scorecard at 10:01:41Z, base read then); the window that killed her was the ~15 seconds between scorecard and PUT. The discipline is therefore not "re-anchor at decision time" (already done) but "re-anchor at *action* time" — the read and the mutation must be adjacent, with nothing unverified between them. Where adjacency is impossible (slow human flow), the fallback is the SN-0868 discipline: never merge on anything not fully resolved. Pairs with SN-0881 (the same miss, viewed through the correction-cascade lens) and SN-0882 (the repair that healed what rode in).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "lesson_class": "process_fix_and_failure_classification",
  "mechanism": {
    "scorecard_base": "fe25661c (from PR record)",
    "live_tip_at_put": "21d17e8e (after direct pushes de2dce6d, 21d17e8e @ 09:59:33-34Z)",
    "actual_merge_parents": "21d17e8e+84c9f4fe",
    "named_parents": "fe25661c+84c9f4fe",
    "window": "~15s between scorecard (10:01:41Z) and PUT",
    "consequence": "two unreviewed pushes rode in; tip RED (drift ratchet)"
  },
  "rule": "re_read_refs_heads_main_immediately_before_mutating_put_name_parents_from_that_read",
  "category_error": "treating_derived_state_PR_record_base_as_live_state",
  "refinement_of": "SN-0493 (re-anchor at action instant, not just decision instant)",
  "never": [
    "anchor_base_equals_live_tip_on_PR_record",
    "allow_unverified_gap_between_base_read_and_mutating_call"
  ],
  "pairs_with": ["SN-0493", "SN-0868", "SN-0879", "SN-0881", "SN-0882"]
}
~~~

## 🟢 LEARNING LESSON

Verification has a half-life, and for base preconditions it is measured in seconds during a merge burst. The seat's process was not sloppy — scorecard, then merge 15 seconds later — but the environment was adversarial to that gap: direct pushes landing one second apart. The generalizable principle: **the read and the mutation must be adjacent.** Any protocol step of the form "verify X, then do Y" must either make X and Y adjacent or re-verify X at Y-time. This is the same shape as the regen/stage ordering lesson (SN-0880: validate on the bytes you will ship) and the pending-is-not-green law — the family is "certify the present, not the past."

## 🧭 KEY DECISIONS / PRINCIPLES

- Re-read the live ref immediately before the mutating call; name parents from that read.
- The PR record's base is derived state from an earlier read — never live evidence.
- If the tip moved between scorecard and action, re-verify the precondition on the new bytes first.
- Read and mutation must be adjacent; an unverified gap is where unreviewed changes ride in.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0493 — from "re-verify at action time" to the mechanical form: fresh ref read, adjacent to the PUT
- **DISTINGUISHES** → SN-0868 — merge-race on still-running checks (gate misread); this is stale-precondition on the actor's own merge
- **DISTINGUISHES** → SN-0879 — race artifacts on superseded tips (don't chase); this is what rode in on a live merge (do heal — see SN-0882)
- **PAIRS** → SN-0881, SN-0882 — same incident window, three facets: correction discipline, repair strategy, precondition freshness
- **ENABLES** → Cold Naya continuity — a mechanical pre-merge step a cold seat can execute

## 🧾 PROOF / PROVENANCE

~~~json
{
  "smart_note_id": "SN-0883",
  "lineage": "#1354 merge-burst window 2026-10-10 ~10:00-10:17Z -> proactive capture",
  "evidence": {
    "source": "#1354 comment 6096478615 ([NAYA 2][CORRECTION-2], 2026-10-10T10:16:29Z), 'L201' miss",
    "direct_pushes": "de2dce6d, 21d17e8e @ 2026-10-10T09:59:33-34Z",
    "scorecard": "#1354 comment 6096368667 @ 10:01:41Z (named parents fe25661c+84c9f4fe)",
    "merge_commit": "af118c7b @ 10:01:56Z (actual parents 21d17e8e+84c9f4fe)"
  }
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: seat-observed and evidence-backed, awaiting director ratification. The parent SHAs, timestamps, and the 15-second window are taken from Naya 2's own correction posts; no independent re-read of the merge commit was performed in this capture. The mechanical rule (fresh ref read adjacent to the PUT) is a protocol prescription derived from the incident, not itself executed here.
