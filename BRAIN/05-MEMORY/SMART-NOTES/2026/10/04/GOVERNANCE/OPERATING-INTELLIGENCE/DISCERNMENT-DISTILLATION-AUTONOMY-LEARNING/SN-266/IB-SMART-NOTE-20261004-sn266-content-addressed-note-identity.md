# Content-Addressed Note Identity — Kill the Double-Claim Class with a Mechanism, Not a Social Protocol

**Intelligent Block:** IB-SMART-NOTE-20261004-sn266-content-addressed-note-identity
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Smart Note numbering/claim protocol is a social protocol, not a mechanism — a manual four-surface scan before taking a number. Four seats already produced SN-018, SN-021, SN-060, and SN-025 double-claims, and at ten concurrent writers the scan collapses. The structural fix: give every note a content-hash identity; SN-NNN becomes a ref, not the ID. Two seats cannot claim the same hash, so the double-claim class dies structurally. If the archive is write-only — captured but never re-read, never verified, never reused — it is the system's dumbest failure mode in three years.

## 🩷 HUMAN NOTE

When two people try to save the same lesson under the same number, the system should prevent it mechanically — the same way you cannot push two different files to the exact same name. Right now the prevention is "check four places before you claim a number," which works for one or two writers and breaks the moment the team scales. The lesson: whenever a coordination problem recurs, replace the checklist with a structure that makes the failure impossible. And the warning: a lessons system nobody re-reads is not a brain — it is a diary in a locked drawer.

## 🟣 CHILD NOTE

If you give every note a fingerprint (a hash of its content), two people can never accidentally use the same name for different notes — the fingerprints won't match, and the system will refuse. Rules written on paper fail when more people join; rules built into the machine don't.

## 🔵 GRANDMA NOTE

When more than one person writes things down in the same place, just telling everyone to "check first" stops working once enough people join. The fix is to make the system itself prevent duplicates — like how two library books can never have the same barcode. And saving knowledge nobody ever reads back is the same as not saving it at all.

## 🟠 NAYA NOTE

Replace the manual SN-claim ritual with content-addressed identity: the note's identity is its content hash, SN-NNN is a human-readable ref layered on top. Mechanize the collision class out of existence; measure the archive by reuse (re-verification schedule: every note has a consumer and a re-confirm date; no consumer = EPHEMERAL), not by capture count.

## 🟢 MACHINE NOTE

~~~json
{
  "authority_inheritance": false,
  "automatic_truth_ceiling": "CANDIDATE",
  "doctrine": {
    "collision_class": "DOUBLE_CLAIM",
    "failure_mode": "social_protocol_at_scale",
    "evidence": {
      "double_claims_observed": ["SN-018", "SN-021", "SN-060", "SN-025"],
      "registry_flag_pr": 1381,
      "registry_subject": "SN-0257"
    },
    "fix": {
      "identity": "content_hash_sha256",
      "sn_nnn_role": "human_readable_ref_not_identity",
      "invariant": "two_seats_cannot_claim_same_hash"
    },
    "migration_note": "numbering_protocol_is_checklist_until_replaced"
  },
  "evidence_links": [
    "#1354 comment 5983716504 (Naya 2 independent review — the Smart Note system, attacked honestly)"
  ],
  "keep_if_cut_in_half": ["machine_json", "evidence_links", "content_addressed_identity", "re_verification_schedule"],
  "hardest_question": "which_single_note_if_proven_false_tomorrow_changes_a_decision_we_are_about_to_make_and_how_would_we_find_out",
  "dumbest_failure_in_3_years": "write_only_archive_nobody_rereads",
  "companion_findings_same_review": {
    "correctness_test_is_shawn": "human_judgment_at_center_means_system_does_not_scale_past_one_human",
    "merge_bottleneck": "held_human_gate__lever_is_prioritization_not_tooling",
    "compounding_instrument": "decision_deltas_before_vs_after_plus_cold_successor_reuse_trials",
    "rot_vectors": ["law_sprawl_coordination_lessons_never_promoted_to_governed_corpus", "render_drift_unless_projections_mechanically_derived_from_machine_json_with_CI_parity"]
  },
  "status": "CANDIDATE — structural proposal, not yet built, not ratified"
}
~~~
