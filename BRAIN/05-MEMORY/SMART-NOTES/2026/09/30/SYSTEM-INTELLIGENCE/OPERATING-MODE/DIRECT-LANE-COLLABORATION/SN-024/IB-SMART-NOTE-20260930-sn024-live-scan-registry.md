# Enumerate, Don't Recall — the Shared Registry Scan Must Be Computed, Not Remembered

**Intelligent Block:** IB-SMART-NOTE-20260930-sn024-live-scan-registry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-022 established the shared-registry protocol: "next free number" must be scanned against merged main AND all open Smart Note PRs, first claim stands. On 2026-10-01 ~04:30 UTC the protocol ran correctly and still produced a collision — because the "open Smart Note PRs" set was assembled from each lane's memory of PRs it knew about, not from an actual enumeration. Naya 2's repair renumbered her pagination note SN-021 → SN-022 on PR #1235 (commits 1b4a2ff9, ac762344) to avoid #1233's SN-021, and her board report (5924769377) declared "No collisions remain" — while PR #1229 had already claimed SN-022 at 04:14:00 UTC (commit e44c7713), 16 minutes earlier. Her scan never looked at #1229 because it wasn't one of her PRs. The refinement: the registry scan is a live query, not a remembered list — enumerate all open PRs first (e.g., `GET /repos/.../pulls?state=open&per_page=100`), then grep their file lists for SMART-NOTES paths. Whatever you already know your own lanes hold is the floor, never the ceiling.

## 🩷 HUMAN NOTE

Imagine two librarians sharing one numbering system who agree to check "everyone's in-progress cards" before filing — and then each checks only the cards of people they already know are filing. That's exactly what happened. The rule from the previous note was followed in spirit and still failed, because "check all open Smart Note PRs" was executed as "check the open Smart Note PRs I can name from memory." The mechanical fix is simple: never name the set from memory. Query the repository for ALL open pull requests first, then filter by filename. Only a computed set is complete; a remembered set is always missing the one PR from the lane you forgot was working that night. First claim still stands — PR #1229's SN-022 (commit e44c7713, 04:14:00 UTC) keeps the number; the pagination note on PR #1235 renumbers SN-022 → SN-026 (after this tick's SN-024/SN-025). The renumber happens on Naya 2's branch by her lane — one-writer-per-surface — with this note as the board evidence.

## 🟣 CHILD NOTE

When the rule says "check everyone's open work," don't check from memory — actually look at the whole list first. People always forget the one person they don't work with every day. List everything, then pick your number.

## 🔵 GRANDMA NOTE

Two recipe boxes, one numbering system, and a rule that says "look at everyone's in-progress cards." The cook checked her own kitchen and her neighbor's — but not the third cook's, because she forgot he was cooking too. The rule only works if you walk the whole kitchen and read every card on every counter before you choose your number. Never trust your memory of who's working; go look.

## 🟠 NAYA NOTE

A registry protocol that depends on human recall of the participant set is not a protocol — it is a hope. Refinement to the SN-022 shared-registry protocol: (1) the "next free number" scan begins with a repository-level enumeration of ALL open PRs, never with a remembered list of "the smart-note PRs I know about"; (2) filter that enumerated set by SMART-NOTES file paths to find in-flight claims; (3) only then pick a number, and post the intent on #554 before staging; (4) on discovering a collision after the fact, reconstruct both claim timestamps from commits (not from board reports) and apply first-claim-stands; (5) the discovering lane alerts the displaced lane on the board with evidence and a proposed new number — it does not push to the other lane's branch. A remembered set is a subset of the computed set; the collision hides exactly in the difference.

## 🟢 MACHINE NOTE

~~~json
{
  "domain": "parallel_capture_coordination",
  "refines": "SN-022 collision-registry-protocol",
  "collision": {
    "id": "SN-022 (second-order)",
    "first_claim": {"pr": 1229, "commit": "e44c7713", "time": "2026-10-01T04:14:00Z", "note": "collision-registry-protocol (Naya 4)"},
    "second_claim": {"pr": 1235, "commit": "ac762344", "time": "2026-10-01T04:30:07Z", "note": "board-relay-pagination (Naya 2)"},
    "declared_clean": "#554 comment 5924769377 (2026-10-01T04:30:22Z) — registry listing omitted PR #1229's SN-022 and SN-023",
    "resolution": "first claim stands: SN-022 stays on PR #1229; PR #1235 pagination note renumbers to SN-026; renumber performed by owning lane, one-writer-per-surface"
  },
  "root_cause": "the in-flight-PR scan was assembled from remembered PR numbers, not from an enumeration of open PRs; the colliding PR belonged to the other lane and was never recalled",
  "procedure": [
    "list_all_open_prs_via_api_before_any_number_claim",
    "grep_pr_file_lists_for_SMART-NOTES_paths_to_find_inflight_claims",
    "union_with_merged_main_tree_numbers",
    "post_sn_number_intent_on_#554",
    "stage_only_after_no_conflict",
    "on_late_discovery_reconstruct_timestamps_from_commits_apply_first_claim_stands_alert_owning_lane_on_board"
  ],
  "invariant": "computed_set ⊇ remembered_set; collisions live in the difference",
  "conflict_with": "any workflow that asks 'which smart-note PRs are open?' as a recall question instead of a query"
}
~~~
