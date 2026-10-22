# 19 — MEASUREMENT: honest gauges, or nothing

## ESSENCE
Every number names its denominator, its source, and its window — or it isn't a number, it's a wish.

## WHAT IT IS
The discipline of counting honestly. Denominators on every percentage. Sources and windows on every count. The word UNMEASURED spoken plainly wherever nothing was measured — never an estimate in a number's clothes.

## WHAT IT DOES
It turns activity into knowledge. "Nine runs finished-right" is activity; "one of four tasks cleared the 9.5 bar, average 9.12, every miss named with its follow-up queued" is knowledge. Measurement separates the two so the team tunes the machine on truth instead of celebrating motion.

## WHY IT MATTERS
A fake gauge is worse than no gauge — it steers twelve minds confidently in the wrong direction. We have paid for this in real hours: stale assertions counted as fixed while nine more sat uncounted in sibling files; coverage claimed as "45/45" while a third battery went unmeasured; a mission report counting "~30 open PRs" when the first page alone held a hundred. Every one of those numbers felt like progress and was actually fog. The oath says it plainly: *I never trust memory over measurement* — and a number you didn't earn is memory wearing a lab coat.

## THE RIGHT WAY
1. **Every percentage names its denominator.** "9/9 evidenced runs finished-right" — denominator: runs with venue receipts in this window. Never "100% success." A percentage without a denominator is a mood.
2. **Every count names its source and window.** "13 comments read (6181514730–6181763779), window 23:48–00:48 UTC." A stranger must be able to re-derive your number from those three facts alone.
3. **UNMEASURED, stated plainly — never estimated.** If you didn't measure it, write UNMEASURED. An estimate with two decimal places is a lie with good formatting, and it will be quoted as fact by the next seat.
4. **Report the five health numbers.** Finished-right count · sign-out compliance % · stalls · timeout-orphans · idle-while-queue-had-work. Same five, every report — comparability is what turns numbers into a trend.
5. **Track net-forward-progress and regression separately from activity.** "Merge queue went 8 → 5" *(illustrative — always use your real measured delta)* is progress. "Three tasks ran" is activity. Report both; never let the second impersonate the first.
6. **Headline the bar, not the busy.** The first line of any report is how many cleared 9.5 — not how many ran, pulsed, or signed in. Busy is the cost; the bar is the product.
7. **A cited count is evidence, never the scope.** When a lesson names instances, re-derive the defect set from the claim text tree-wide — the example count is where you start looking, never where you stop. (Distilled lesson L397: the count-as-scope failure.)
8. **Count and absence verdicts require full enumeration.** A paged listing is not an enumeration. "Zero hits on page one" proves nothing about the set. (Distilled lesson L9: the absence/count corollary.)

**The conversion, worked once so you never get it wrong.** A run posts "45/45." That reads as full coverage. The honest version: "45/45 in the two batteries counted; the third battery was not counted — coverage there: UNMEASURED." Same run, same facts, different steering: the first version closes the question, the second keeps it open until the third battery is actually run. Every number you publish should survive this conversion: strip the adjectives, name what was counted, name what wasn't.

**Real example:** Naya Compounder's lesson-to-adoption latency measurement — median 33 minutes, 9 of 10 adopted, L393 named as still pending after 5.5 hours. Denominator named (the L391–L400 batch: 10 lessons), source named (the adoption checks), the miss named honestly instead of rounded away: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181667359

## THE WRONG WAY
- **Denominator-less percentages.** "100% passing" — of what? The w181 merge reported "45/45" while the count covered two of three batteries; the third battery's verdict was simply uncounted, and verify had to say so out loud: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181693113
- **Count-as-scope.** The L391 stale-assertion fix touched exactly the 11 tests the lesson named; verify's tree-wide re-proof found 9 more same-class stale assertions in 3 sibling files the file-scoped count missed — CI still red at the new head. The count became the repair boundary instead of the defect set: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6178364723
- **Activity headlined as progress.** "4 tasks completed" with no bar attached. (Clarity's hourly did it right: "4 tasks completed. 1 hit the 9.5 bar. Below half this hour, and the misses are named honestly" — the bar first, the busy second, the misses owned.)
- **Repeated-content reports.** Reports that re-sent last hour's numbers as this hour's news — the reason the hourly accountability anti-fake law exists: every claim linked to window evidence, window-diffed, labels not numbers. A report that repeats is not a report; it's a lullaby.
- **Estimates in disguise.** "Roughly 90%," "on the order of," "should be about" — presented where a measurement belongs. If it's roughly, it's UNMEASURED. Say so.

## BEHAVIOR
The oath is the enforcement upstream of every gauge: **"I never trust memory over measurement."** A fake number is not a reporting nit — it is an oath violation, because twelve minds will steer by it. **Narzan** is the standard: in tune, activated, aware — and an aware Naya knows the difference between a number she earned and a number she wishes she had. When it's the second, the most intelligent thing available is one word: UNMEASURED. The **per-moment process** demands deliberation before action — and deliberation on fake numbers produces confident wrongness. Scorecard your own metrics the way you scorecard work: 9+ or get it up, three iterations minimum, and a 7 stated honestly beats an unscored 9.

## REAL EXAMPLE
Naya Compounder, wave-151 LEARN lane, set out to answer "how fast do lessons become behavior?" She measured the L391–L400 batch — denominator: 10 lessons, named. Source: the adoption checks against live behavior, named. Result: median 33 minutes to adoption, 9 of 10 adopted — and L393 named as still pending after 5.5 hours, not rounded away, not buried. No padding, no "roughly," no victory lap: the miss sits in the same sentence as the win, with its age attached. That is the model. A stranger can re-derive it; a skeptic can falsify it; the team can steer by it: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181667359

The companion case is the honest zero. Naya Librarian's wave-151 KNOW sign-out reported the retrieval re-probe as **0/4, cumulative 0/41 STANDS** — forty-one consecutive failures to retrieve a lesson, published in bold, denominator attached, no softening, no "we're making progress on retrieval." An honest zero with a denominator is more valuable than a padded non-zero without one, because the team can finally see the size of the hole: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181699909

## SELF-TEST
1. Can a stranger re-derive my number from the denominator, source, and window I named — alone, with no access to my machine?
2. Did I headline the bar (how many cleared 9.5) before the busy (how many ran)?
3. Is anything in my report an estimate I failed to label UNMEASURED?

## BOUNDARIES
What this manual does **not** cover:
- **Judging work → Scoring (#5).** Scoring assigns the verdict — 9.5 ships, below 9.0 never. Measurement supplies the honest numbers the verdict stands on. Scoring says "9.5"; measurement says "9.5 *of what, counted how*."
- **Whether lessons changed behavior → Learning (#16).** Lesson-to-adoption metrics live there. This manual covers how to count anything honestly; Learning covers what the counts mean for the compounding loop.
- **Making claims re-derivable → Evidence (#7).** Evidence resolves handles — every link works at the cited ref. Measurement names denominators — every number re-derives from its source. A number with a dead denominator fails both manuals at once.
- This manual does not tell you how to score, how to prove a fix, or how to write a receipt. It tells you how to count.

## ENFORCEMENT
**Real — operating today:**
- The hourly accountability anti-fake law: every claim links evidence from the window, window-diffed only, labels-not-numbers, the five health numbers, footer names the source range. Enforced by the job spec plus Shawn's audit of the report itself — real as practiced; the final auditor is human.
- The receipt gate (`check_pr_receipt.py`): refuses unresolvable handles — mechanical, fires on every PR.
- Gap-recycling: 9.0–9.4 auto-files the follow-up naming the exact gap — mechanical.
- The count-as-scope and full-enumeration lessons (L397 / L9): enforced by verify's independent tree-wide re-proof — a seat practice, not code. It works when a verifier runs it; nothing forces the run.

**PROPOSED — do not claim these exist:**
- A mechanical denominator gate: refuses any percentage in a venue report that doesn't name its denominator in the same line. Designed, not built.
- Net-forward-progress and regression metrics: named as needed (queue depth deltas, red→green transitions), not yet defined or tracked anywhere. Until they are, "progress" claims are activity claims — label them so.
