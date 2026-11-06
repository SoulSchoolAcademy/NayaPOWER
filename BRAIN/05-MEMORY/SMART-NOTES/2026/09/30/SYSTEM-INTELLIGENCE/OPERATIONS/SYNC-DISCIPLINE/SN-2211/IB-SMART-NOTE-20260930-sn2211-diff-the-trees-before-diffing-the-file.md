# Diff the Trees Before Diffing the File — A Snapshot Branch Is Not a Merge Candidate

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2211-diff-the-trees-before-diffing-the-file
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A branch named like a snapshot stream is not a merge candidate — diff the trees before diffing the file. The file diff said "sync me" (45 lines on BRAIN/CURRENT-MISSION-STATE.md); the tree diff said "never merge me whole" (3,211 files changed, +56,295 / −1,160,261 lines; main 6,418 files vs branch 3,452; 2,972 files on main absent from the branch). The brief's "merge/sync the branch" read naively would have merged 1.16M deleted lines onto main. The seat scoped the vehicle to a single-file sync and opened PR #3258 (1 commit, exactly 1 file, 16+/21−), which merged 2026-11-06T17:12:57Z. Every future sync/merge brief tree-diffs before acting on a file diff, and a snapshot-named branch is treated as a diverged tree until the tree diff proves otherwise.

## 🩷 HUMAN NOTE

Imagine someone hands you a single page from a 6,000-page book and says "this page changed — reprint the book from my copy." You look at the one page: 45 lines differ, seems small. But their copy of the book is missing 2,972 pages and has 3,211 pages different. If you reprint from their copy, you lose whole chapters. The lesson is simple: before you trust one page, count the whole book. Compare the entire tree first, then decide what to sync — never the other way around.

## 🟣 CHILD NOTE

It is like copying homework from a friend. You check one answer and it looks almost the same, so you copy the whole page. But your friend's notebook is missing half the pages and has different answers everywhere else. If you copy the whole thing, your homework gets much worse. The smart move: look at the whole notebook first, count what is different, and then copy only the one answer you actually need.

## 🔵 GRANDMA NOTE

Dear, when someone brings you a basket and says "just this one apple is bruised," you do not take the whole basket on their word — you lift the cloth and look at every apple first. One bruised apple is a small fix; a basket with three thousand apples swapped is a different errand entirely. The file is the one apple; the tree is the whole basket. Always lift the cloth. Always count the basket before you carry it home.

## 🟠 NAYA NOTE

This note exists because the naive reading of a merge/sync brief nearly destroyed main on 2026-11-06. The branch naya/mission-state refreshes intraday ("Snapshot refresh 05:13 PDT") and is a diverged snapshot tree, not a main-tracking branch — the file diff for BRAIN/CURRENT-MISSION-STATE.md showed only 45 lines of drift, which is a true statement about one file and a lie about the branch. The tree diff is what made the call: 3,211 files changed, −1.16M lines, 2,972 files on main absent from the branch. The only sane vehicle was a single-file sync (PR #3258, commit 1d37b67a, 1 file, 16+/21−, blob byte-identical to the live snapshot blob), which merged the same day. The sibling rule is SN-1987: a sync must be re-run against its own output before it counts as proof. This note governs the step before that — how the sync is scoped in the first place. The root cause underneath (main lags a branch that refreshes intraday, with no standing sync) recurs daily and is named, not cured, in the receipt; this note keeps the daily dose safe until a standing sync exists.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["merge", "sync"],
    ["branch", "snapshot-stream"],
    ["merge", "scope-error"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note governs scoping, not whether a snapshot branch may ever be merged: a snapshot branch whose tree diff proves it tracks main is mergeable. It does not claim every file-diff reading is wrong — only that a file diff cannot establish scope, and a snapshot-named branch is presumed diverged until the tree diff says otherwise.",
  "decision_change": "When a merge/sync brief arrives, the seat runs the tree diff (git diff --stat main...<branch>) before acting on any file diff, and treats a snapshot-named branch as a diverged tree until the tree diff proves otherwise; the sync vehicle is scoped to the smallest file set the tree diff justifies, never to the whole branch on a file diff's say-so.",
  "enforcement": "A merge/sync PR is opened only with the tree diff attached (git diff --stat main...<branch> in the PR body); the verification/scorecard step rejects a PR whose body lacks tree-diff evidence, and a file-diff-only scoping is a blocking finding. The merge/sync brief template carries the tree-diff step as a required pre-flight.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/distill-daily-20261106.md (2026-11-06): branch naya/mission-state tip b087c9c4191951986a719cf9ebc6def804205fa7 ('Snapshot refresh 05:13 PDT'), main tip at check 67067ec5e234a1a85f7550ec644f0221573aa6c6; file diff BRAIN/CURRENT-MISSION-STATE.md = 45 lines; full tree diff main vs branch = 3,211 files changed, +56,295 / -1,160,261 lines; main tree 6,418 files vs branch tree 3,452 files; 2,972 files present on main absent from the branch",
    "PR #3258 (SoulSchoolAcademy/NayaPOWER): branch naya4/mission-state-sync-20261106-0513, one commit 1d37b67a8e1d8b5f88c3ef7c103c92d095d89653 ('Sync BRAIN/CURRENT-MISSION-STATE.md from naya/mission-state @ b087c9c'), exactly 1 file changed, 16 insertions / 21 deletions, pushed via GitHub App identity, pushed file blob byte-identical to the live snapshot blob 1bf11b5cb5ec768b9460b0f9f666ceee4abe2f82; merged 2026-11-06T17:12:57Z (verified via App-route API this tick)",
    "The brief's 'merge/sync the branch' read naively would have merged 1.16M deleted lines onto main; the tree-diff scoping was the run's highest-value judgment call (distill-daily-20261106.md)"
  ],
  "falsifier": "The rule is refuted if a measured run of snapshot-branch syncs shows file-diff scoping alone never mis-scopes a sync — i.e., if tree diffs add nothing over file diffs across snapshot streams. The 'never merge me whole' presumption specifically is refuted by a snapshot-named branch whose tree diff equals its file diff (a snapshot that truly tracks main).",
  "intelligence_class": "LESSON",
  "mechanism": "A file diff compares one path; a tree diff compares whole trees. A snapshot stream refreshes by replacing the tree, so it diverges across the whole tree while any single file's diff stays small — the 45-line file diff was true about one file and silent about the 3,211-file divergence. Only the tree diff sees the true scope, so scoping from the file diff alone hides destructive collateral.",
  "related_notes": ["SN-1987"],
  "truth_state": "CANDIDATE"
}
```
