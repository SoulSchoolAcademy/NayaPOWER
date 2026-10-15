# 18 - Reviews (AI)
area_number: 18
area_name: Reviews
owner_team: Naya Resolve
agent_seat: Auditor

## DEFINITIONS
- what_it_is: The independent judgment on someone else's work - the gate's required second mind before anything merges or ships. A review that cannot say no is decoration, and decoration launders defects.
- what_it_does: Catches what the author's eyes cannot see, and converts 'I built it' into 'a stranger re-derived it and agrees - here is exactly what was checked, and here is what is still missing.'
- why_it_matters: Every merge, every scorecard, every 9.5+ rests on a review. A rubber-stamp review is worse than no review at all: no review leaves the gap visible, while a rubber stamp covers it with the appearance of scrutiny. We have paid for this in real merges - the review was right and the system walked past it.

## PROTOCOLS
1. Independent seat - never the author. Producer != qualifier, full stop.
2. First available wins - never wait on a specific reviewer. 'I'm waiting for her' is abdication.
3. Re-derive from live bytes, never inherit the author's claims: read the actual code at the exact head being merged - not the PR description, not a summary. A summary scored instead of the source inverts verdicts.
4. Specific findings with evidence, never vague approval. Name what you checked, what passed, what failed, with links a stranger can re-derive in one command.
5. Score honestly - a 7 is a 7. Use the right rubric for the artifact: a manual is an instruction set to achieve success and is judged as one, not as code (L380).
6. Review the exact head being merged, re-fetched at review time. Builders move the tip mid-review; score the frozen head named, then confirm it is still the head.
7. When two reviews disagree, do not debate which is right - combine both into 'why not 10?'. Every gap either review named becomes the fix list.

## CONSTRAINTS
- Independent seat - never the author. Producer != qualifier, full stop.
- First available wins - never wait on a specific reviewer. 'I'm waiting for her' is abdication.
- Re-derive from live bytes, never inherit the author's claims: read the actual code at the exact head being merged - not the PR description, not a summary. A summary scored instead of the source inverts verdicts.
- Specific findings with evidence, never vague approval. Name what you checked, what passed, what failed, with links a stranger can re-derive in one command.
- Score honestly - a 7 is a 7. Use the right rubric for the artifact: a manual is an instruction set to achieve success and is judged as one, not as code (L380).
- When two reviews disagree, do not debate which is right - combine both into 'why not 10?'. Every gap either review named becomes the fix list.

## BOUNDARIES
- not_covered: Proving your own work (producer != qualifier is the wall); Defining the bar (9.5 ships, below 9.0 never); The dock that consumes reviews (a review never merges); Owning your misses (the author owns the correction; the reviewer owns the finding)
- #6 Verification: proving your own work
- #5 Scoring: the bar
- #14 Merging: the dock that consumes reviews
- #17 Corrections: the author owns the correction

## ENFORCEMENT
### Mechanically enforced (live)
- The merge-protocol watch: every relay pass verifies each merge to main carries a cross-seat review AND a scorecard naming the exact merged head; a missing review is posted as a breach on the venue immediately.
- Ruleset 23853581 'Naya Execution Governance' live on the merge path.
- The first-available-scoring law (never wait on a specific reviewer) is standing.
### Proposed (designed, not built - do not claim as live)
- Machine-parsed review rejection: a review-shaped comment that fails the parse gets bounced automatically, so theater reviews cannot even land. Designed, not built - do not claim it exists.

## SELF-TEST
1. Was the reviewer a different seat than the author?
2. Did I touch the live bytes at the exact head - and could a stranger re-derive my verdict from my evidence alone?
3. Did I name specific findings, or just approve?

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6171210114 - L380: wrong rubric manufactured the wrong verdict - a manual re-scored 3.0 -> 7.0 on the document rubric
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181282692 - Fail-closed guard regression test independently scored 9.5/10 with sabotage battery
- https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1475 - PR #1475 merged after blocking review 5998194111 had landed - the review was right; the system walked past it
