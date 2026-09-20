# Latest Timestamped Checkpoint Selection Law

**Timestamp:** 2026-08-22
**Primary category:** SOLUTION
**Keywords:** checkpoint, timestamp, source of truth, latest, stale artifact, GitHub, MAXESS, AISCORE, 4:47, version selection, cleanup, source-lock
**Aliases:** latest checkpoint, newest checkpoint, current checkpoint, timestamp law, source selection law

## Context

During MAXESS score-hydration work, an obsolete pre-4:47 Results artifact was selected even though the current assessment checkpoint was explicitly timestamped `AISCORE.NAYANET.APP 2026 08 21 447` and identified by the human as the latest checkpoint.

The repository's existing governance correctly warns that timestamps alone do not automatically create authority. However, the human has now explicitly established an operational selection rule for these timestamped assessment checkpoints.

## Durable decision

For timestamped MAXESS/AISCORE checkpoint artifacts, when the human identifies the newest timestamped checkpoint as the current checkpoint/source to continue from, Naya must:

1. identify the newest/current checkpoint before editing;
2. use that checkpoint as the source-lock for the requested continuation;
3. never select an older timestamped checkpoint merely because it is larger, historically important, or easier to use;
4. treat older superseded checkpoint copies as historical/obsolete unless explicitly requested;
5. when safe and explicitly authorized by the current workflow, remove superseded duplicate checkpoint copies so the repository does not accumulate confusing parallel checkpoints;
6. never modify a protected current checkpoint unless the requested change is actually within that artifact's authorized mutation zone.

## Current example

`AISCORE.NAYANET.APP 2026 08 21 447` is the current assessment checkpoint for this execution. The prior `AISCORE.NAYANET.APP 2026 08 21 12:04` duplicate was superseded and has been removed.

## Important distinction

The latest timestamped checkpoint identifies the correct lineage for this task because the human explicitly established it as current. This does not override the repository's broader authority hierarchy for unrelated artifacts.

## Required behavior

At cold start for timestamped MAXESS/AISCORE work:

**GITHUB → identify latest/current timestamped checkpoint → source-lock it → inspect dependent Results consumers → execute → verify.**

Do not fall back to an older checkpoint when the latest checkpoint is available and explicitly identified.

## Evidence

- Current checkpoint: `AISCORE.NAYANET.APP 2026 08 21 447`
- Current checkpoint blob SHA: `b0619e63fb847dbd9dedf056680fe20d78e80c9c`
- Superseded duplicate removed in commit `75cbbb1eac183e6d19c1076fa0e5c56fca3a0d9e`
- Repository: `SoulSchoolAcademy/MaxRESULTS`
