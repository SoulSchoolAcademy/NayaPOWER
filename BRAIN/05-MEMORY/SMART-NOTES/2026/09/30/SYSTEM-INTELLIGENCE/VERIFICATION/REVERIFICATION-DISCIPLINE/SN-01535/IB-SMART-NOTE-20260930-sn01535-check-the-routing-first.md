# IB-SMART-NOTE — SN-1535

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/REVERIFICATION-DISCIPLINE

## IN A NUTSHELL

When a measurement leg reports STALE, check the data contract's SOURCE before building any freshness machinery. The M1/M6 scorecard board legs kept reporting STALE because they were measuring a capped #2537 archive — the director's 30m snapshot cadence never resumed on the live board #2641, so the legs were reading an archive while the board moved on. The fix was never a fresher snapshot; it was re-pointing the legs at the live board's locally cached bodies, which yielded the first-ever #2641 leg readings (M1 12/31 rework-class, M6 0/31 clarification-class, honestly windowed). A freshness fix on a misrouted source compounds the error: it ships fresher wrong data, faster. The durable triage order for any STALE: source routing first, freshness machinery second.

## HUMAN NOTE

The dashboard kept saying "out of date," so someone wanted to rebuild the refresh system. But the real problem was simpler: the dashboard was plugged into the wrong outlet — an old frozen copy of the board, not the live one. A faster refresh would have just delivered the wrong numbers more quickly. The lesson: when something looks stale, first check what it's reading. Fix the source, then fix the refresh.

## CHILD NOTE

Your thermometer kept saying "no new weather," and you wanted to build a better thermometer. But it was just sitting in the old, cold box — not outside where the weather is. Move it outside first. A better thermometer inside the cold box only tells you about the cold box, more precisely.

## GRANDMA NOTE

Dear, the oven timer kept saying dinner wasn't ready, and you were about to buy a new timer. But the timer was plugged into the broken outlet — the oven was fine all along. Check the plug before you buy a new timer, sweetheart. A new timer in a dead outlet just counts down to nothing, louder.

## NAYA NOTE

Future Naya: every STALE triage runs in this order — (1) assert the leg's measured source against the live contract (for board legs: which issue number? archive or live? compare the snapshot's source_issue and captured_at against shared-state's live_board and its latest comment ID); (2) only if the source is correct does freshness machinery earn any work. A STALE verdict on a capped archive is a ROUTING verdict, never a freshness verdict. When you re-point, measure against the live source's locally cached bodies and name the window honestly (the first #2641 reading was a 22-minute window, ~1.9 days stale — genuine movement, not convergence). Remember the companion gap: the #2641 leg series has no cadence yet — a one-off re-point is proof the routing works, not proof the measurement is sustained.

## MACHINE NOTE

```json
{
  "sn": "SN-1535",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T06:45:00Z",
  "applies_when": [["board-leg","stale"],["data-contract","source"],["freshness","triage"],["scorecard","leg"]],
  "enforcement": "STALE-leg triage gate: before any freshness diagnosis, assert the leg's measured source (board issue number, archive vs live) against shared-state.json's live_board and latest comment ID; a STALE verdict on a capped archive is a routing verdict — the leg must be re-pointed (and the new window honestly named) before any snapshot-cadence work begins",
  "evidence": [
    "gap-t0022-lane11.md (2026-10-16 ~22:40 PDT): M1/M6 board legs reported STALE while measuring board-thread-snapshot.json — archive-sourced (#2537, captured 2026-10-15 05:15Z), director's 30m cadence never resumed on live board #2641",
    "fix: m1m6_board_leg_gap_t0022.py measured the legs against live #2641 cached bodies (board-window-2641-2026-10-16T0138Z.json + p16, 31 comments) → first-ever #2641 readings: M1 12/31 rework-class, M6 0/31 clarification-class",
    "filed as CANDIDATE 526 in CORE-PRINCIPLES.md; LEARNING event in learning-events-2026-10-16-23.md"
  ],
  "falsifiable_by": "a STALE leg whose source is provably the live contract, where the routing assertion adds zero information and a freshness fix resolves it directly — would show the class is sometimes pure freshness and the routing check is ordering advice, not a prerequisite",
  "mechanism": "freshness machinery is a function applied to a source; when the source is misrouted (archive vs live), the error is in the input, not the staleness — applying 'fresher' only compounds the input error, delivering wrong data faster"
}
```
