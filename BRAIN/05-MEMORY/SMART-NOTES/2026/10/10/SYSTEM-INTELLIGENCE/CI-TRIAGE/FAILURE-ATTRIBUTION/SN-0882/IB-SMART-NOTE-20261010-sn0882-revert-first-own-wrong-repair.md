# Revert First, Own the Wrong Repair — The Standard Response to a Ratchet-Breaking Direct Push

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0882-revert-first-own-wrong-repair
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** NayaPOWER #1354 comment 6096459172 ([NAYA 2][SCORECARD] PR #2113, 2026-10-10T10:13:54Z); #1354 comment 6096470494 ([NAYA 2][MERGE-RECEIPT] PR #2113, 2026-10-10T10:15:25Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two direct pushes to main (`de2dce6d`, `21d17e8e`) projected smart-note pages with the colliding basename `smart-note.md` and no registry entries, tripping the drift ratchet (`duplicate_published_page_paths` 1→2, `published_pages_without_registry_entry` growing; tip RED at `af118c7b`). Naya 2's first repair attempt — a rename of the two files — was **proven insufficient on exact bytes**: it fixed the dup-name class but grew the registry-entry class 1→2. She abandoned the rename branch openly (no PR, recorded in her correction post), enumerated four repair options under the five-step scorecard, and merged PR #2113 — a clean revert of the two offending commits — scoring it 9.0: clean, reversible, re-projectable, and the only option that healed every pinned class. Post-merge verification on exact tip bytes: drift test 12/12 green, tip `86449a3634` healed.

Two rules for a cold successor: (1) **when a law-violating direct push breaks a pinned ratchet, revert the offending commits first** — a revert is clean (byte-verifiable), reversible (re-applyable), and re-projectable (the notes' source data lives in the projection pipeline, so nothing is lost); forward-patching around a ratchet violation (rename, hand-registration) either moves the violation to another pinned class or corrupts provenance. (2) **a repair proven insufficient on exact bytes is dead** — close it, supersede it, and own the miss in the same record as the working repair. The abandoned rename was recorded in the correction post, not hidden.

## 🩷 HUMAN NOTE

Shawn — this morning's 10:00Z merge burst gave us a textbook repair sequence. Two direct pushes landed smart-note files with the same filename, which tripped the drift alarm and turned the tip red. Naya 2's first instinct was to rename the files — but she tested the rename on the exact bytes and it didn't work: it fixed one alarm class and set off another. So she did the honest thing: killed the rename branch, wrote up all four repair options with scores, and went with a clean revert of the two bad pushes — undo them entirely, then the projection pipeline can re-publish the notes properly later. Tip went green, verified on the exact bytes.

The two takeaways: when a bad direct push breaks a pinned guardrail, **revert it** — don't try to patch around it, because the guardrail is pinned in multiple dimensions and a partial fix just moves the violation. And when your first repair fails verification, **say so in the open and move on** — she recorded the dead rename in the same post as the working revert. That's the honesty covenant doing its job.

## 🟣 CHILD NOTE

Imagine someone spills paint on two pages of a coloring book. Your first idea is to put stickers over the spills — but the stickers make the pages too thick to close the book. So you throw the stickers away, admit "that didn't work," and just tear out the two ruined pages — you can always reprint them from the original drawings later. The rule: undo the damage cleanly instead of covering it up, and if your first fix doesn't work, say so and try the clean one.

## 🔵 GRANDMA NOTE

When something breaks a safety rule, the safest repair is to undo the breaking change completely — not to tinker around it. And if your first attempt at a fix doesn't actually work when you test it, don't hide it: write down that it failed and what you're doing instead. An honest record of a failed fix is worth more than a quiet one, because the next person won't repeat it.

## 🟠 NAYA NOTE

This note captures repair-strategy selection under the five-step scorecard, worked on real bytes. The option enumeration is the mechanism: A. revert (9.0 — heals all pinned classes, reversible, re-applyable), B. leave red (2.0 — violates fix-first), C. rename (3.0 — *proven* insufficient on exact bytes `cbd328a1`: dup-name class fixed, registry-entry class grew 1→2), D. hand-register (1.0 — would corrupt pinned hash classes; no captures exist). The rename's insufficiency was established empirically, not argued — that is the evidence law applied to one's own repair. The supersession was recorded where the failure was recorded (the correction post 6096437769), keeping the provenance chain intact. Distinct from SN-0875 (which establishes *why* rename is wrong — provenance is a chain, not a filename — and never-manufacture-provenance): this note establishes *what to do instead* at the tip-healing layer — revert first, re-project cleanly after. It also pairs with SN-0493: the decision was re-anchored on the live tip (`af118c7b`) at decision time, and mergeability re-confirmed at merge time.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "lesson_class": "failure_classification_and_process_fix",
  "mechanism": {
    "violation": "direct_pushes_de2dce6d_21d17e8e_with_colliding_smart-note.md_basename_no_registry_entry",
    "ratchet_trip": "duplicate_published_page_paths_1_to_2_and_published_pages_without_registry_entry_growth",
    "first_repair": "rename_branch_brain-build/fix-duplicate-smart-note-pages",
    "first_repair_verdict": "PROVEN_INSUFFICIENT_on_exact_bytes_cbd328a1",
    "chosen_repair": "PR_2113_clean_revert_of_offending_commits",
    "post_merge": "drift_test_12/12_green_on_exact_tip_bytes_86449a3634"
  },
  "rules": [
    "ratchet_breaking_direct_push_heals_by_revert_not_forward_patch",
    "revert_is_clean_reversible_reprojectable",
    "repair_proven_insufficient_on_exact_bytes_is_dead_close_supersede_own_openly"
  ],
  "scorecard_options": {
    "A_revert": 9.0,
    "B_leave_red": 2.0,
    "C_rename": 3.0,
    "D_hand_register": 1.0
  },
  "never": [
    "forward_patch_around_pinned_ratchet_violation",
    "hide_an_insufficient_repair_attempt"
  ],
  "pairs_with": ["SN-0493", "SN-0875"],
  "distinguishes_from": {
    "SN-0875": "why_rename_is_wrong_there_vs_what_to_do_instead_here"
  }
}
~~~

## 🟢 LEARNING LESSON

The repair is itself a decision, and decisions run through the calculus — including repairs of your own failed repairs. The rename wasn't abandoned because it "felt wrong"; it was abandoned because exact-bytes verification proved it moved the violation between pinned classes. That is the difference between a preference and a proof. And the open abandonment matters as much as the revert: a hidden dead branch is a trap the next seat can walk into; a recorded one is a lesson. The remaining rail (not this PR): the v7 projection pipeline still emits colliding page names and pushes directly to main — reverting heals the tip, but the pipeline owner must fix emission.

## 🧭 KEY DECISIONS / PRINCIPLES

- Revert the ratchet-breaking commits: clean, reversible, re-projectable — the standard response.
- Never forward-patch around a pinned ratchet (rename/hand-register move or corrupt the violation).
- A repair proven insufficient on exact bytes is dead: close it, supersede it, own it in the same record.
- Score the repair options explicitly; the receipt is the decision record.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0875 — basename discipline and never-manufacture-provenance; this adds the tip-healing repair strategy
- **PAIRS** → SN-0493 — decision re-anchored on the live tip at decision and merge time
- **ENABLES** → Cold Naya continuity — the revert-first reflex for ratchet reds, executable without inventing strategy

## 🧾 PROOF / PROVENANCE

~~~json
{
  "smart_note_id": "SN-0882",
  "lineage": "#1354 merge-burst window 2026-10-10 ~10:10-10:16Z -> proactive capture",
  "evidence": {
    "scorecard": "#1354 comment 6096459172 ([NAYA 2][SCORECARD] PR #2113, 2026-10-10T10:13:54Z)",
    "merge_receipt": "#1354 comment 6096470494 ([NAYA 2][MERGE-RECEIPT] PR #2113, 2026-10-10T10:15:25Z)",
    "rename_verdict_bytes": "cbd328a1 (rename proven insufficient)",
    "healed_tip": "86449a3634 (drift test 12/12 on exact tip bytes)",
    "abandoned_branch": "brain-build/fix-duplicate-smart-note-pages (no PR opened)"
  }
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: seat-observed and evidence-backed, awaiting director ratification. The rename-insufficiency verdict and the scorecard scores are taken from Naya 2's own posts; no independent re-run of the byte verification was performed in this capture. Attribution of the direct pushes (Shawn vs automation under his identity) remains UNKNOWN per the correction post — the repair strategy does not depend on it.
