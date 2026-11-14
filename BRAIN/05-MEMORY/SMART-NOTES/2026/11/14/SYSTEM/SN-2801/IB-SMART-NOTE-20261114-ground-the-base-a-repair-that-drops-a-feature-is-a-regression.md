# Ground the Base — A Repair That Drops a Feature Is a Regression

SN-2801 · LESSON / CHARGE

**Created:** 2026-11-14 10:55Z

**Paired Naya Note:** NN-20261114-ground-the-base-a-repair-that-drops-a-feature-is-a-regression

## Hook

A repair built on a stale base silently drops what the base never had. Ground the base first — with SHAs — or the fix is a regression wearing a repair's name.

## Nutshell

The find of 2026-11-14 ~05:39Z, in the walk v23 assembly. BIG FIND — staging had regressed: the pre-v23 staged walk `df17ac67` (deployed ~03:29Z from the stale beginning-fix base) had steps 11–14 + quote fix but NO Q10 presentation, NO names, NO Q2, NO gold — the Nov 14 repair silently dropped the Q10 presentation Shawn praised Nov 13. v23 = base `4e8500c2` + Q2's 7 lines + steps 11–14 transplanted verbatim from `df17ac67` + quote fix + JS renumber 10→14 (diff vs base 232 lines, all in intended regions). Two df defects fixed, not carried: names-Enter dead-end (`showStep(14)` re-showed names instead of building) and duplicate `#enterBtn-14`. The assembler was dispatched 05:07Z with the ground-first instruction: ground the pieces FIRST with SHAs (names-page build, two-line join fix, Q2 walk `fd38de47`, Q10 walk `be55a494`, sisters' walk `4e8500c2`, sisters' renderer fix riding unmerged); assembler chooses sisters' walk vs Q10 walk on the evidence and records the choice; ONE deploy, staged only, live = Shawn's tap. VERIFICATION: checker Vera PASS 9/10 + captain double-check CONFIRMED (own fresh-citizen walk, own aliases, own Box re-read, diffs re-run herself); captain's own 28/28 walk at 390px; v23 SHOWN to Shawn WHOLE 05:54Z with the regression find named — his eye + tap owed; pay-words delta rides after his tap. Slugify-concatenate + wildcard subdomains stay queued behind walk deploys, NOT in v23.

## Human

A repair is judged by what it fixes, but it must also be judged by what it keeps. The pre-v23 staging had been "repaired" from a stale base, and the repair worked — steps 11–14, quote fix, all present — while silently deleting the Q10 presentation Shawn had praised the day before, plus names, Q2, and gold. Nobody noticed, because the repair was verified against its own brief, not against the whole page. The brief said "fix these things," the fix fixed them, and the page quietly got worse. That is why the v23 assembler was dispatched with ground-first as the first instruction: name every piece with its SHA, choose the base on the evidence, record the choice — and only then compose. The composition itself is the discipline: base plus Q2's seven lines plus steps 11–14 transplanted verbatim plus the quote fix plus the renumber, 232 lines of diff, all in intended regions. And the verification matches the discipline: Vera used her OWN fresh aliases and her OWN Box re-read, never the assembler's; the captain walked it herself, 28/28, and showed it to Shawn whole with the regression find named out loud. A repair that drops a praised feature is not a repair. It is a regression that nobody checked for.

## Child

Imagine you fix your toy car's broken wheel — but you use an old photo of the car that doesn't have its shiny gold stripe! Now the car works, but the gold stripe is GONE! You have to look at the REAL car first, with all its pretty parts, and THEN fix it — so you keep everything beautiful AND fix what's broken!

## Grandma

It's like mending a dress, love — you must look at the whole dress first, with all its ribbons and buttons, before you start stitching. If you mend from an old pattern that's missing the prettiest part, you'll sew it right out and never notice. Look at the real thing first, keep everything lovely, and then fix what's torn.

## Naya

I ground the base first — every piece named with its SHA — before I repair anything. I choose the base on the evidence and I record the choice. I transplant verbatim, I fix only what is intended, and I verify against the whole page, not just my brief. A repair that drops a feature Shawn praised is a regression, and I name it out loud when I find one — because the next repair must not repeat it.

## What it means

- **GROUND THE BASE FIRST:** every piece named with its SHA before any composition — the base is chosen on evidence, the choice recorded.
- **VERIFY AGAINST THE WHOLE PAGE:** a repair verified only against its own brief can silently drop what the brief never mentioned.
- **THE REGRESSION WAS SILENT:** Q10 presentation, names, Q2, gold — all praised, all gone from staging, nobody noticed until the ground-first assembly.
- **TRANSPLANT VERBATIM:** steps 11–14 moved word for word; the diff is 232 lines, all in intended regions.
- **VERIFY WITH YOUR OWN EYES:** Vera's own aliases, own Box re-read, diffs re-run herself; the captain's own 28/28 walk.
- **NAME THE FIND OUT LOUD:** the regression was shown to Shawn whole, with the find named — not hidden behind the fix.

## Why it matters

Staging is the page Shawn will be asked to tap live. If staging can silently lose a praised feature while a repair is declared done, then every "done" in the system is suspect — the verification proved the fix and never proved the page. Ground-first is the cure because it makes the base explicit: when the base is a SHA, the diff is a fact, and a dropped feature shows up as a missing region instead of a feeling. The v23 round is the proof that the discipline works: the same machine that produced the silent regression, given the ground-first instruction, produced a 232-line composition with every intended region intact and two old defects fixed along the way.

## What changes now

1. Every repair grounds its base first — pieces named with SHAs, base chosen on evidence, choice recorded.
2. Verification covers the whole page, not just the brief's diff — praised features are checked as present.
3. Composition is verbatim transplant + named fix + renumber — the diff stays inside intended regions.
4. Checkers verify with their own aliases, their own reads, their own diffs — never the maker's.
5. A regression found is named out loud to Shawn, whole, with the fix — never hidden behind it.
