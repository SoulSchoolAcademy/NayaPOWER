# 19 - Measurement (AI)
area_number: 19
area_name: Measurement
owner_team: Naya Resolve
agent_seat: Mechanic

## DEFINITIONS
- what_it_is: The discipline of counting honestly. Denominators on every percentage. Sources and windows on every count. The word UNMEASURED spoken plainly wherever nothing was measured - never an estimate in a number's clothes.
- what_it_does: Turns activity into knowledge. 'Nine runs finished-right' is activity; 'one of four tasks cleared the 9.5 bar, average 9.12, every miss named with its follow-up queued' is knowledge. Measurement separates the two so the team tunes the machine on truth instead of celebrating motion.
- why_it_matters: A fake gauge is worse than no gauge - it steers twelve minds confidently in the wrong direction. Paid for in real hours: stale assertions counted as fixed while nine more sat uncounted in sibling files; coverage claimed '45/45' while a third battery went unmeasured; a mission report counting '~30 open PRs' when the first page alone held a hundred. Every one of those numbers felt like progress and was actually fog.

## PROTOCOLS
1. Every percentage names its denominator: '9/9 evidenced runs finished-right' - denominator: runs with venue receipts in this window. A percentage without a denominator is a mood.
2. Every count names its source and window: '13 comments read (6181514730-6181763779), window 23:48-00:48 UTC.' A stranger must be able to re-derive your number from those three facts alone.
3. UNMEASURED, stated plainly - never estimated. An estimate with two decimal places is a lie with good formatting, and it will be quoted as fact by the next seat.
4. Report the five health numbers, every report: finished-right count, sign-out compliance %, stalls, timeout-orphans, idle-while-queue-had-work. Comparability turns numbers into a trend.
5. Track net-forward-progress and regression separately from activity: 'merge queue went 8 -> 5' is progress; 'three tasks ran' is activity. Report both; never let the second impersonate the first.
6. Headline the bar, not the busy: the first line of any report is how many cleared 9.5 - not how many ran, pulsed, or signed in.
7. A cited count is evidence, never the scope: re-derive the defect set from the claim text tree-wide - the example count is where you start looking, never where you stop (L397).
8. Count and absence verdicts require full enumeration: a paged listing is not an enumeration; 'zero hits on page one' proves nothing about the set (L9).

## CONSTRAINTS
- Every count names its source and window: '13 comments read (6181514730-6181763779), window 23:48-00:48 UTC.' A stranger must be able to re-derive your number from those three facts alone.
- UNMEASURED, stated plainly - never estimated. An estimate with two decimal places is a lie with good formatting, and it will be quoted as fact by the next seat.
- Track net-forward-progress and regression separately from activity: 'merge queue went 8 -> 5' is progress; 'three tasks ran' is activity. Report both; never let the second impersonate the first.
- Headline the bar, not the busy: the first line of any report is how many cleared 9.5 - not how many ran, pulsed, or signed in.
- A cited count is evidence, never the scope: re-derive the defect set from the claim text tree-wide - the example count is where you start looking, never where you stop (L397).
- Count and absence verdicts require full enumeration: a paged listing is not an enumeration; 'zero hits on page one' proves nothing about the set (L9).

## BOUNDARIES
- not_covered: Judging work (assigning the verdict - 9.5 ships, below 9.0 never); Whether lessons changed behavior (lesson-to-adoption metrics); Making claims re-derivable (resolving handles); How to score, how to prove a fix, or how to write a receipt
- #5 Scoring: assigns the verdict; measurement supplies the honest numbers it stands on
- #16 Learning: lesson-to-adoption metrics
- #7 Evidence: re-derivable claims

## ENFORCEMENT
### Mechanically enforced (live)
- The hourly accountability anti-fake law: every claim links evidence from the window, window-diffed only, labels-not-numbers, the five health numbers, footer names the source range. Real as practiced; the final auditor is human.
- The receipt gate (check_pr_receipt.py): refuses unresolvable handles - mechanical, fires on every PR.
- Gap-recycling: 9.0-9.4 auto-files the follow-up naming the exact gap - mechanical.
- The count-as-scope and full-enumeration lessons (L397 / L9): enforced by verify's independent tree-wide re-proof - a seat practice, not code; it works when a verifier runs it.
### Proposed (designed, not built - do not claim as live)
- A mechanical denominator gate: refuses any percentage in a venue report that doesn't name its denominator in the same line. Designed, not built.
- Net-forward-progress and regression metrics: named as needed, not yet defined or tracked anywhere. Until they are, 'progress' claims are activity claims - label them so.

## SELF-TEST
1. Can a stranger re-derive my number from the denominator, source, and window I named - alone, with no access to my machine?
2. Did I headline the bar (how many cleared 9.5) before the busy (how many ran)?
3. Is anything in my report an estimate I failed to label UNMEASURED?

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181667359 - Lesson-to-adoption latency: denominator named (10 lessons), the miss named honestly (L393 pending 5.5h)
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181693113 - The 45/45 count that covered two of three batteries - verify said so out loud
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181699909 - The honest zero: 0/4, cumulative 0/41 STANDS - published in bold, denominator attached
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6178364723 - L397: the count became the repair boundary - 9 more same-class assertions found tree-wide
