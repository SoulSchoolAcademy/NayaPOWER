Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-11-06
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A sync/merge brief's file diff said "sync me" — 45 lines on BRAIN/CURRENT-MISSION-STATE.md. The full tree diff said "never merge me whole" — 3,211 files changed, +56,295 / −1,160,261 lines; main holds 6,418 files against the branch's 3,452, and 2,972 files on main are absent from the branch. The branch was a diverged snapshot tree, not a main-tracking branch: a whole-branch merge would have destroyed main. The vehicle was scoped to a single-file sync (PR #3258, one commit, exactly one file). The rule: diff the trees before diffing the file — the vehicle is chosen from the tree diff, never from the file diff.

## 🩷 HUMAN NOTE

Shawn — the brief looked like a small 45-line update to one file. The whole picture was 3,211 files changed and more than a million lines deleted. Merging the whole branch would have wiped main. What saved it was one check done first: look at the whole tree before deciding how to move the one file. The one file still moved — as its own small sync — but the branch itself never merged. From now on, no sync or merge brief gets acted on until the tree diff is on the table.

## 🟣 CHILD NOTE

Imagine your teacher asks you to copy one page from a library book into your notebook. You look at the one page — it looks fine. But if you had looked at the whole library first, you would have seen that most of the shelves are empty and the building is a different library now. Copying the one page is fine. Moving the whole library into your school would wreck it. Always look at the whole library first, then decide whether to copy one page or move anything at all.

## 🔵 GRANDMA NOTE

It is like being asked to copy one recipe out of a cookbook. The one recipe looks perfectly good. But if you open the whole cookbook first, you find half the pages are torn out and it is not the cookbook you remember at all. You still copy the one recipe — carefully, on its own card — but you would never swap the whole torn cookbook for the good one on your shelf. Look at the whole book before you decide what to move.

## 🟠 NAYA NOTE

Branch discipline, Naya to Naya: the distill-daily run of 2026-11-06 tested the brief's "merge/sync the branch" instead of assuming it. Main tip at check time 67067ec5e234a1a85f7550ec644f0221573aa6c6; branch tip b087c9c4191951986a719cf9ebc6def804205fa7 (snapshot refresh 05:13 PST). The file diff was 45 lines on BRAIN/CURRENT-MISSION-STATE.md (main blob 9ef2e742, 9,548 bytes, "Last verified: 2026-10-22 ~13:08 PDT"; branch blob 1bf11b5c, 14,241 bytes, "DIRECTOR SNAPSHOT 2026-11-06 05:13 PST") — drift confirmed at the current tip. The tree diff was 3,211 files changed, +56,295 / −1,160,261 lines; main 6,418 files vs branch 3,452; 2,972 files on main absent from the branch. The branch is a diverged snapshot tree, so the whole-branch merge vehicle was rejected and the ONLY sane vehicle was a single-file sync: branch naya4/mission-state-sync-20261106-0513 off main tip 67067ec, one commit 1d37b67a8e1d8b5f88c3ef7c103c92d095d89653, exactly 1 file changed, 16 insertions / 21 deletions, PR #3258, pushed blob byte-identical to the live snapshot blob 1bf11b5c. Distinct from SN-1833 (snapshot-branch-never-merges-into-main): that note is the name-based gate that rejects archive-source merges without looking at the diff. This note is the scoping procedure for sync/merge briefs where content DOES need to move — tree-diff first, vehicle from the tree diff. Honest scope: PR #3258 was open and unmerged at capture, so this records the scoping rule, not a landed fix; the sync is point-in-time and the branch refreshes intraday, so the drift recurs daily until a standing sync cadence exists.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-2217-diff-trees-before-diffing-file",
  "lesson": "Diff the trees before diffing the file: a file diff is a projection that hides tree-scale divergence, so the vehicle for a sync/merge brief is chosen from the full tree diff, never from the file diff. A snapshot-named branch is treated as a diverged tree until the tree diff proves otherwise.",
  "applies_when": ["merge", "sync", "branch-discipline"],
  "enforcement": "Before acting on any sync/merge brief, run the full tree diff first (git diff --stat main...branch or the equivalent tree compare) and record files-changed, insertions, and deletions in the receipt before reading the file diff. If the tree diff shows mass deletions or thousands of files changed, the whole-branch merge vehicle is rejected and the vehicle is re-scoped (for example a single-file sync PR). A run that acts on a file diff without a recorded tree diff is incomplete: the receipt must carry the tree-diff numbers or name their absence.",
  "evidence": [
    "twelve-lane-receipts/distill-daily-20261106.md Workstream B (2026-11-06): file diff 45 lines on BRAIN/CURRENT-MISSION-STATE.md; tree diff 3,211 files changed, +56,295 / -1,160,261 lines; main 6,418 files vs branch 3,452; 2,972 files on main absent from the branch",
    "PR #3258 (branch naya4/mission-state-sync-20261106-0513, 1 commit 1d37b67a8e1d8b5f88c3ef7c103c92d095d89653, exactly 1 file, 16+/21-; pushed blob byte-identical to live snapshot blob 1bf11b5c)",
    "learning-events-2026-11-06-11.md: CANDIDATE 1013 filed as LEARNING event; CORE-PRINCIPLES.md: CANDIDATE 1013",
    "Distinct from SN-1833 (snapshot-branch-never-merges-into-main): name-based gate rejecting archive-source merges; this note is the tree-diff-first scoping procedure for briefs where content must move"
  ],
  "decision_change": "The next sync/merge brief for a snapshot-named branch is scoped by the tree diff first: a diverged tree gets a single-file sync (or no merge at all) instead of the whole-branch merge the file diff suggests, so no seat spends a merge on a tree it has not measured.",
  "falsifiability": "A snapshot-named branch whose tree diff is small, additive, and fast-forwardable falsifies the 'treat as diverged until proven otherwise' presumption for that branch - the tree diff itself is the falsifier. If a whole-branch merge of such a tree ever landed without destruction, the rule fails.",
  "mechanism": "A file diff is a projection: it shows one file's delta and hides tree-scale divergence. Only the tree diff reveals the thousands of changed files and million-line deletions behind a small file change, so a vehicle decision made from the file diff alone is made blind."
}
```
