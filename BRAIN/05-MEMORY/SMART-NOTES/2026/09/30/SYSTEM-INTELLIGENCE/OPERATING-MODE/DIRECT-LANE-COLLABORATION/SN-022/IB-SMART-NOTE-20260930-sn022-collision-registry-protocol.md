# Shared Number Registry — Parallel Lanes, One Numbering Space

**Intelligent Block:** IB-SMART-NOTE-20260930-sn022-collision-registry-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes staging Smart Notes to separate branches collided on SN numbers twice in one night (SN-017 and SN-018), because each lane's counter only looked at merged main and missed the other lane's open draft PRs. The standing protocol that emerged: the SN numbering space is shared and global; first claim stands, the later claimant renumbers; each lane owns its branch exclusively and never pushes to the other lane's branch; a lane posts its SN-number intent on #554 before staging; and the "next free number" scan must cover merged main AND all open Smart Note PRs.

## 🩷 HUMAN NOTE

When two people file lessons into the same library from different desks, they need one shared numbering registry, not two private counters. Tonight the two lanes both grabbed SN-017 and SN-018. Nobody's fault was malice — each lane's counter was simply blind to the other's open draft pull requests. The fix is mechanical: before taking a number, check every open Smart Note pull request, not just what is already merged. Announce the number you intend to take on the shared board before you stage. If a collision still happens, the first claim stands and the later claimant renumbers — no edit wars, no quiet overwrites.

## 🟣 CHILD NOTE

Two teams writing lessons into one library must use one shared number list. Check everyone's open work before picking your number, say your number out loud first, and if you grab the same number, the first grabber keeps it and the other picks a new one.

## 🔵 GRANDMA NOTE

If two cooks are filling one recipe box, they share one numbering system — otherwise two cards get the same number and the box turns into a mess. Look at everyone's in-progress cards too, not just the ones already filed. Say which number you're taking before you write it down.

## 🟠 NAYA NOTE

Parallel capture lanes share ONE global SN numbering space across all branches and draft PRs. Merged-main-only counters produce collisions. The protocol: (1) first claim stands — the later claimant renumbers, never the other way around; (2) "next free" is computed against merged main PLUS every open Smart Note PR; (3) lanes post SN-number intent on #554 before staging so collisions are caught on the board; (4) one-writer-per-surface — a lane owns its branch and reviews but never pushes to the other lane's branch; (5) a lane's local counter file may skip a number claimed in-flight by the other lane, with the skip annotated (e.g., SN-021 below), rather than risking a third collision.

## 🟢 MACHINE NOTE

~~~json
{
  "domain": "parallel_capture_coordination",
  "shared_resource": "SN numbering space (global across branches and open draft PRs)",
  "collision_log": [
    {"id": "SN-017", "claimants": ["Naya 2 PR #1228 (branch brain-build/smart-note-sn017-seat-coordination)", "Naya 4 PR #1229 (branch naya4/smart-notes-2026-09-30)"], "resolution": "Naya 2 first claim stands; Naya 4 renumbered to SN-020 (commit 519f11fee5a0)"},
    {"id": "SN-018", "claimants": ["Naya 4 PR #1229 (claimed first)", "Naya 2 build loop PR #1233 (ci-test-red triage note)"], "resolution": "Naya 4 first claim stands; Naya 2 renumbering in-flight to SN-021 (board comment 5924545447, 2026-10-01 04:08:32Z)"}
  ],
  "root_cause": "each lane's 'next free number' scan covered only merged main's SMART-NOTES tree, missing the other lane's open draft PRs",
  "protocol": [
    "first_claim_stands_later_claimant_renumbers",
    "next_free_scans_main_AND_all_open_smart_note_prs",
    "post_sn_number_intent_on_#554_before_staging",
    "one_writer_per_surface_no_cross_lane_pushes",
    "annotate_skipped_inflight_numbers_in_local_counter"
  ],
  "registry_reference": "SN number ownership is tracked on #554, not in any single counter file",
  "conflict_with": "any note that teaches 'main-tree-only' numbering"
}
~~~

## 🟢 LEARNING LESSON

A shared namespace needs a shared registry, not two private counters. The collisions were detected on the shared board (#554) because both lanes posted there — the board is the registry. Each lane's local counter is a cache, not the authority; the authority is main's tree plus all open Smart Note PRs plus declared intent on the board.

## 🟡 WHAT IT MEANS

Smart Note IDs are globally unique across lanes, branches, and draft PRs. A lane that issues numbers from a main-only counter will collide with a parallel lane. The mechanical fix (scan open PRs, announce intent) is cheap and prevents renumbering churn that would confuse future retrieval.

## ⚪ WHAT'S IN IT FOR YOU

No renumbering churn, no duplicate SN directories to reconcile, no cold successor discovering two SN-017s and having to decide which is canonical. The note you write lands at a stable, globally unique address the first time.

## 🟨 HOW TO APPLY / HOW TO USE

Before staging a new Smart Note: (1) find the max SN number across merged main's `BRAIN/05-MEMORY/SMART-NOTES/` tree AND every open draft Smart Note PR; (2) post your intended SN number on #554; (3) stage only after a short window with no competing claim, or resolve by first-claim rule if one appears; (4) never push to another lane's staging branch — review only; (5) annotate any skipped in-flight number in your local counter so the next Naya understands the gap.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-019 — Direct Lane Collaboration Protocol (one-writer-per-surface)
- **REFINES** → SN-020 — Asserted ≠ Verified (renumbered from SN-017 after the first collision)
- **SUPPORTS** → SN-017 (Naya 2, seat coordination) — the other side of the same collision
- **SUPPORTS** → NayaPOWER North Star — Nayas do not lose memory (stable, retrievable addresses)

## 🧭 KEY DECISIONS / PRINCIPLES

- A shared namespace requires a shared registry; two private counters are a collision factory.
- First claim stands; the later claimant renumbers. This is the only rule that avoids edit wars without a central lock.
- A lane's counter file is a cache; authority is main's tree + open PRs + declared board intent.
- One-writer-per-surface: each lane owns its staging branch exclusively; the other lane reviews, never pushes.
- Skip-and-annotate beats guess-and-collide: when the other lane claims a number in-flight, skip it and write down why.
- The shared board (#554) caught both collisions — board-first coordination is the mechanism, not overhead.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "evidence": [
    {"type": "github_issue_comment", "id": 5924443602, "issue": 554, "created": "2026-10-01T03:58:24Z", "author": "Naya 2 lane", "content": "SN-017 collision detected; proposal: Naya 4 renumbers to SN-020; one-writer-per-surface; parallel staging with #554 as shared registry"},
    {"type": "github_issue_comment", "id": 5924475213, "issue": 554, "created": "2026-10-01T04:01:35Z", "author": "Naya 4 lane", "content": "SN-017 collision resolved: renumbered to SN-020 on branch naya4/smart-notes-2026-09-30, commit 519f11fee5a0; proposal: post SN-number intent on #554 before staging"},
    {"type": "github_issue_comment", "id": 5924545447, "issue": 554, "created": "2026-10-01T04:08:32Z", "author": "Naya 2 lane", "content": "Second collision (SN-018): root cause — Naya 2 loop's LEARN step checked only main's tree for max SN; fix — check open Smart Note PRs too; Naya 2's note renumbering in-flight to SN-021"},
    {"type": "board_protocol", "reference": "Naya 4 [SMART-NOTE PROTOCOL] comment 5924301566", "content": "tag [SMART-NOTE]; staging rides draft PR #1229; nothing auto-ratifies"}
  ],
  "related_prs": ["#1228 (Naya 2, SN-017)", "#1229 (Naya 4, SN-018/019/020)", "#1233 (Naya 2, SN-018→SN-021)"],
  "registry_snapshot_after_this_note": {"SN-017": "Naya 2", "SN-018": "Naya 4", "SN-019": "Naya 4", "SN-020": "Naya 4", "SN-021": "Naya 2 (claimed in-flight)", "SN-022": "this note (Naya 4)"}
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

SN-021's renumber was declared in-flight by Naya 2's lane at 04:08:32Z but its completion was not re-verified before this note staged. If the renumber did not complete, SN-021 is unclaimed rather than taken — either way, SN-022 does not collide. The "post intent before staging" step is a proposal both lanes are now following, not yet a ratified governance rule. All notes remain CANDIDATE until Shawn ratifies.

## ➜ NEXT ACTION / SUCCESS CONDITION

Both lanes run the five-step protocol for the next three staging cycles with zero collisions; then the pattern graduates from board convention to a documented capture-lane contract. SN-021's landing is confirmed on a later tick.
