# SN-4250 — Reachability Is Proved by Reaching, Not by Scrolling (LAW)

**Filed:** SN-4250 — Intelligence Loop run 410, 2026-11-20.

## The lesson

A test that moves the container cannot prove you can reach what's inside it. Reachability is proved by reaching.

## What happened

Agreement distill fix-4 was charged with six phone-width defects, F among them: the footer links row cut at the right edge at 390. The maker decided no change for F, on a scroll test — the strip scrolls. The independent checker (GOES BACK on F only, 11:17:59Z) proved the test could not establish what it claimed: the strip scrolls, yet 5 of its 12 links can never be reached at 390 — they sit left of the scroll origin at every scroll position, because the nowrap strip is `justify-content:center`. The defect is pre-existing (byte-identical on base and fix-4b), not a fix-4 regression — but F was one of the six defects this round was charged with, and the brief requires "all links reachable." The fix is one CSS value. Everything else in the round passes; A–E proven, F9 remedies untouched and re-proven, laws delta 0.

## The value

A no-change decision backed by the wrong test is worse than no test at all — it closes the defect in the record while the defect stays on the page. The checker caught it because it tested the criterion itself (can each link be reached?) instead of the proxy (does the strip move?). Five links a citizen can never tap is a failed page wearing a passing report.

## The rule

**Prove the acceptance criterion itself, never a proxy for it.** If the brief says "all links reachable," the test touches every link at every scroll position and reports which ones it could not reach — scrollLeft extremes plus element visibility, not "the strip scrolls." A test that cannot fail on the defect it is meant to catch is not a test; it is a ritual. Name the criterion in the test, and let the test fail loudly when the criterion fails.

## His words

None — this is a machine verdict, not Shawn's dictation. The record is the fix-4 checker report (CHECKER-REPORT.md, 11:17:59Z): "the maker's no-change decision for F rested on a scroll test that cannot establish reachability."

## Paired Naya Note

None — no new Shawn dictation this run.
