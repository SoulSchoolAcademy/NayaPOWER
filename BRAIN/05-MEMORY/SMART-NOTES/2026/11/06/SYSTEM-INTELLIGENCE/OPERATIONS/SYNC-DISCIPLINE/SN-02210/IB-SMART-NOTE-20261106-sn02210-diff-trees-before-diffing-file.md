# INTELLIGENT BLOCK — SN-2210

**Intelligent Block:** IB-SMART-NOTE-20261106-sn02210-diff-trees-before-diffing-file
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Daily distill receipt hidden_files/twelve-lane-receipts/distill-daily-20261106.md (2026-11-06 05:29–05:41 PST, Naya Clarity Narzan): the daily distill brief said "sync the mission-state branch to main"; the file diff said 45 lines in BRAIN/CURRENT-MISSION-STATE.md, but the full tree diff said 3,211 files changed (+56,295 / −1,160,261 lines), 2,972 files present on main absent on the branch — whole-branch merge rejected as destructive, single-file sync PR #3258 opened instead (commit 1d37b67a8e1d8b5f88c3ef7c103c92d095d89653, branch naya4/mission-state-sync-20261106-0513, pushed blob byte-identical to live branch snapshot 1bf11b5c). Duplication check this tick: branch naya4/smart-notes-2026-09-30 tip 11e8eeb7 (SN-02209) — recursive tree grep found 0 paths for "tree-diff" / "vehicle" / "merge-candidate"; the four nearest snapshot cousins (SN-01633, SN-1072, SN-01615, SN-0624) were read in full and are distinct (see MACHINE NOTE); memory-log grep found only the distill-daily event record itself. Counter ends at 2209; branch max SN-02209.

## ✦ IN A NUTSHELL

A branch named like a snapshot stream is not a merge candidate. On 2026-11-06 the daily distill brief said "sync the mission-state branch to main": the file diff said "sync me" — 45 lines in BRAIN/CURRENT-MISSION-STATE.md, main's copy a 2026-10-22 snapshot, the branch's a live 05:13 PST refresh — but the full tree diff said "never merge me whole": 3,211 files changed, +56,295 / −1,160,261 lines, main tree 6,418 files vs branch tree 3,452 files, 2,972 files present on main but absent on the branch. The branch is a diverged snapshot tree, not a main-tracking branch; a whole-branch merge would have deleted 1.16M lines from main. The only sane vehicle was a single-file sync (PR #3258, exactly 1 file, +16/−21). The rule: **diff the trees before diffing the file** — scope the vehicle by tree divergence first, then choose single-file sync vs whole-branch merge. The brief's fix read naively would have destroyed main; the scoping check was the work.

## 🩷 HUMAN NOTE

Shawn — this morning a routine brief said "bring the mission-state branch over to main." The one file that needed syncing differed by only 45 lines, so the obvious move looked like merging the whole branch. But checking the whole shape of the branch first showed it had drifted far from main: merging it whole would have wiped out nearly 3,000 files that only exist on main — over a million lines gone. The fix was to move just the one file instead (PR #3258). The standing rule now: before any branch sync, look at the whole tree, not just the file — a branch that looks like a small update can be a wrecking ball in disguise. Filed as Smart Note candidate SN-2210.

## 🟣 CHILD NOTE

Imagine your friend asks you to copy their homework folder onto yours, because one page in it is newer. If you copy the whole folder, you might erase all the pages that are only in your folder — thousands of them — just to update one page. The smart move is to look at both folders first: if they are very different, copy only the one new page, not the whole folder. Always compare the whole folders before you copy anything.

## 🔵 GRANDMA NOTE

Dear, it is like someone asking you to swap your whole recipe box for theirs because one card is newer. If you swap the whole box, you lose every recipe that is only in yours — years of cards, gone in one move. First you lay both boxes side by side and count what is missing from each. If the boxes have drifted far apart, you copy just the one new card and leave the rest alone. Check the whole box before you move a single card.

## 🟠 NAYA NOTE

For every seat handed a "sync / merge the branch" brief: (1) never take the brief's vehicle at face value — run the full tree diff (`git diff --stat main...<branch>`) BEFORE the file diff, and read the files-absent-on-branch count first; (2) if the branch is a snapshot stream (it refreshes on its own cadence while main moves independently), treat whole-branch merge as guilty until proven innocent — a snapshot branch is a diverged tree by construction, not a main-tracking branch; (3) when the tree diff shows main-only files or deletions dominating, scope to the smallest vehicle that carries the fix (single-file sync, as PR #3258 did: 1 file, +16/−21, blob byte-identical to the live snapshot); (4) record the rejection in the receipt with the tree-diff numbers, so the next seat does not re-litigate the naive reading — the numbers are the argument; (5) remember the companion failure mode: the same branch refreshes intraday, so a point-in-time sync goes stale within hours — a standing sync cadence is the root cure, a single PR is one day's dose.

## 🟢 MACHINE NOTE

```json
{
  "slug": "diff-trees-before-diffing-file",
  "sn": "SN-2210",
  "title": "Diff the Trees Before Diffing the File — Scope the Merge Vehicle First",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-06",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": [["merge", "vehicle-scoping"], ["sync", "snapshot-branch"], ["branch", "tree-diff"]],
  "enforcement": "Before any branch sync or merge, run the full tree diff (git diff --stat main...<branch>) and record it in the receipt; if files present on main are absent on the branch, or deletions dominate the diff, whole-branch merge is rejected and the vehicle is scoped to the smallest change that carries the fix (single-file sync). The scored-route verifier re-checks the tree diff at the merge commit and fails the merge if the vehicle was not scoped. Regression test: the next snapshot-branch sync brief must show a tree diff in its receipt before any PR is opened — a PR opened without one reopens this note.",
  "falsifier": "If a branch whose tree diff shows thousands of main-only files and a million deleted lines is merged whole and main loses nothing (e.g. the deletions are proven to be files already removed from main by another route, verified blob-by-blob at the merge commit), tree divergence was not destructive here and this note is wrong. If snapshot branches are proven to track main (tree diff stays near-zero across refreshes for 30 days), the snapshot-stream premise fails and this note retires to OBSERVATION.",
  "decision_changed": "How a sync/merge brief is executed: the vehicle is scoped by the full tree diff before any file diff is acted on, so a snapshot-stream branch is synced file-by-file instead of merged whole — the next naive 'sync the branch' reading cannot delete a million lines from main.",
  "mechanism": "A snapshot branch refreshes on its own cadence while main moves independently, so the two trees diverge monotonically: files land on main that the branch never sees, and the branch's tree silently lacks them. A file-level diff hides this — it shows only the one file's 45 lines. A whole-branch merge applies the branch tree as the target state, so every main-only file is a deletion. Only the tree diff reveals the divergence (3,211 files, −1.16M lines, 2,972 main-only files on 2026-11-06), because it compares the trees as wholes. The scoping check works because it measures the blast radius before choosing the vehicle, and the smallest vehicle (single-file sync) carries zero blast radius by construction.",
  "cousins": ["SN-01633 (a stale-payload re-run artifact made a correct body fix look failed — about CI event snapshots staling a pin; this note is about branch trees diverging, not event payloads)", "SN-1072 (a CI gate reads the event snapshot, not the live body — the event-snapshot law; this note's snapshot is a branch tree, and the remedy is vehicle scoping, not a fresh event)", "SN-01615 (a re-anchor is a snapshot, not a floor — names the distance to tip; this note measures the distance between two trees and uses it to choose the vehicle)", "SN-0624 (a quarantine snapshot listed 29 collisions that live bytes had already resolved — stale snapshots mislead; this note is the constructive half: when the snapshot is a branch, diff the trees and scope the vehicle)"],
  "provenance": "Daily distill receipt hidden_files/twelve-lane-receipts/distill-daily-20261106.md (2026-11-06 05:29-05:41 PST): main tip moved faa4fb8 -> 67067ec during verification; branch tip b087c9c unchanged; file diff 45 lines (main blob 9ef2e742, 9,548 bytes, 'Last verified: 2026-10-22 ~13:08 PDT' vs branch blob 1bf11b5c, 14,241 bytes, 'DIRECTOR SNAPSHOT 2026-11-06 05:13 PST'); whole-branch merge REJECTED (3,211 files changed, +56,295 / -1,160,261 lines; main 6,418 files vs branch 3,452; 2,972 main-only files); single-file sync PR #3258 opened (https://github.com/SoulSchoolAcademy/NayaPOWER/pull/3258, commit 1d37b67a8e1d8b5f88c3ef7c103c92d095d89653, pushed blob byte-identical to 1bf11b5c), never merged (dock merges via scored route). Duplication check this tick: branch naya4/smart-notes-2026-09-30 tip 11e8eeb7 (SN-02209) — recursive tree grep: 0 paths for 'tree-diff' / 'vehicle' / 'merge-candidate'; nearest snapshot cousins SN-01633/SN-1072/SN-01615/SN-0624 read in full, distinct mechanisms above; memory-log grep found only the distill-daily event record itself. Counter ends at 2209; branch max SN-02209; open-PR census 2026-11-06 05:41 (3 open: #3258 mission-state sync, #3178 intelligence report, #3089 PI draft — none a Smart Note carrier) + staging script's mechanical branch-tree claim check as backstop."
}
```
