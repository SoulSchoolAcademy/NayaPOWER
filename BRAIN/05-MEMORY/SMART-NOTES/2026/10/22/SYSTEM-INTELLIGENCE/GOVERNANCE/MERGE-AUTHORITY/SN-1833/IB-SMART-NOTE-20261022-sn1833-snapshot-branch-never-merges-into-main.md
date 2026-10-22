Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #2928 merged the naya/mission-state snapshot branch into main — the 2nd instance of the named failure mode MISSION-STATE-BRANCH-MERGE (after #2859). The mission-state branch is an archive: point-in-time snapshots of what the mission decided then. Merging it into main folds the archive into the living lineage and corrupts the distinction between "what we recorded at T" and "what is live now" — provenance collapses into a merge commit. The archive lands on main by snapshot-write, never by merge. The pre-merge gate rejects any merge whose source is a named archive branch (naya/mission-state) before scoring begins: the branch name is the check, not the diff.

## 🩷 HUMAN NOTE

Shawn — the mission-state branch is your time capsule: snapshots of what the mission believed at each moment, frozen. Twice now a merge has tried to fold the time capsule into the live system. That breaks what the capsule is for — once it's merged into the live line, you can't tell "what we recorded then" from "what's true now." The capsule's contents reach the live system through snapshots, never through merges. The gate now checks the branch name before it ever looks at the diff: anything merging from the archive branch gets stopped at the door, not cleaned up after.

## 🟣 CHILD NOTE

Imagine a diary that records exactly what happened each day. Now imagine ripping a page out of the diary and gluing it onto today's calendar. The calendar now has two todays, and nobody knows which one is real. The diary page reaches the calendar by being copied out as a note — never by tearing the diary apart. The branch is the diary; main is the calendar.

## 🔵 GRANDMA NOTE

It's like a photograph album of the family through the years. You'd never paste the whole album into today's newspaper — the newspaper is what's happening now, the album is what happened then. Mixing them means nobody can tell the record from the news. The album is for reading; the newspaper is for now. Two different jobs, kept separate.

## 🟠 NAYA NOTE

Branch discipline, Naya to Naya: the snapshot branch is an archive, not a merge source. The director's 1508 tick named #2928 (naya/mission-state branch merged INTO main 15:00:15Z, empty template body) the ARCHITECTURAL FLAG — the 2nd MISSION-STATE-BRANCH-MERGE instance after #2859. The mechanism is provenance collapse: an archive branch exists to hold append-only, point-in-time records ("the mission believed X at T"); merging it into main's lineage rewrites the record as current action, and the empty-template merge body compounds it by recording nothing of the archive's own state. After the merge, a cold reader cannot distinguish "what we decided then" from "what is live now" — the two get one history. The archive's delivery path is snapshot-write (the tick's own snapshot PUTs, e.g. snapshot b0532eacf7a47c6f65ceed0d7ed6209226dee208 first try), never merge: snapshots move the state forward while leaving the archive's record intact and separate. The gate is name-based, not diff-based: before scoring, reject any merge whose source branch is on the archive list (naya/mission-state). No diff review can rescue a structurally wrong merge — the branch name is the verdict. Two instances is a pattern; the third should die at the gate.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1833-snapshot-branch-never-merges-into-main",
  "lesson": "Archive branches are append-only records, not merge sources: merging naya/mission-state into main collapses the archive's point-in-time record into the living lineage, destroying the distinction between 'what we recorded at T' and 'what is live now'. The archive's delivery path is snapshot-write, never merge. The pre-merge gate rejects archive-source merges by branch name before scoring.",
  "applies_when": ["merge", "branch-discipline"],
  "enforcement": "Pre-merge gate: before any merge is scored, check the source branch against the archive list (naya/mission-state); a match is REJECTED at the gate with the named failure mode MISSION-STATE-BRANCH-MERGE — no diff review, no scorecard, no dock hand. Snapshot state moves to main only through the snapshot-write path (branch PUT + snapshot commit), which advances the live line while leaving the archive's record intact and separate.",
  "evidence": [
    "hidden_files/shared-state.json director_tick_20261022_1508 (#2928 = ARCHITECTURAL FLAG (naya/mission-state branch merged into main 15:00:15Z, empty template body; 2nd instance after #2859))",
    "hidden_files/shared-state.json director_tick_20261022_1508 (snapshot 693d8e319acc first try (branch naya/mission-state intact at 6d390c3e post-#2928-merge) — the archive branch survived the merge as a record; the live line is what got folded)"
  ],
  "decision_change": "The next merge from naya/mission-state into main dies at the gate on the branch name alone — no one spends a scorecard on it, no one reviews the diff, no one cleans up afterward. The seat that wants archive state live writes a snapshot, not a PR.",
  "falsifiability": "Superseded by Shawn's word if he ever directs the snapshot branch to merge into main as the delivery vehicle — his bytes outrank the gate. Absent that, the archive/merge distinction stands.",
  "mechanism": "Provenance collapse: an archive branch and the live main serve two different consumers — the archive serves cold readers asking 'what was decided then', the live line serves lanes asking 'what is true now'. A merge fuses the two histories into one commit graph; after the merge the graph can no longer answer either question cleanly. The snapshot-write path avoids this by construction: it copies state forward (a new live commit with a snapshot record) while the archive keeps its own unmerged lineage. The check is name-based because the error is structural — no diff content can make an archive-source merge correct."
}
```
