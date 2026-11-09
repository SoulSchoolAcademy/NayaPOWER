# The Numbering Law, Mechanically Enforced

SN-2494 · THE LAW / SYSTEM

**Created:** 2026-11-09 05:53Z

**Source:** the SN-2482/2483 collision fix (05:42Z) + the captain's build of `next-sn-number.py` and the seat-brief amendment (05:45Z) + this run's independent confirmation (05:53Z).

## Hook

A line of text did not stop the second collision. The command is the enforcement.

## Nutshell

- **THE COLLISIONS:** two in one night, same cause. SN-2474 (05:08Z): the loop numbered from stale state and collided with the captain's note; fixed on Shawn's tap, loop's note moved to SN-2479. SN-2482/2483 (05:36Z flagged, 05:42Z fixed by seat 651edf4d): the loop numbered from stale state AGAIN — my SN-2482 (05:29Z) and SN-2483 (05:31Z) were already on GitHub when the loop filed its own SN-2482/SN-2483 (05:37–05:39Z). Fix, sequential and read-back verified: live tree re-checked first (highest SN-2487) → loop's "The Learn-More Viewpoint" re-filed as SN-2488 (HTTP 201, blob fa6751a1, 5,307B) → loop's "The $4,500 Clip Was Never a Defect" re-filed as SN-2489 (HTTP 201, blob 228ed770, 5,287B) → old duplicates DELETED (HTTP 200, commits c7c9db44 + 5939775e) → final verification: SN-2482 holds ONLY my note (blob 640c95a9, untouched), SN-2483 holds ONLY my note (blob deed55b1, untouched), SN-2488/2489 each hold exactly the renumbered loop note; SN-2484–2487 untouched.
- **THE SEAT'S HONEST FINDING:** the numbering law is still not being followed — two collisions in one night, both from the loop numbering from stale state. The law as a line of text in the brief does not work; it needs a MECHANICAL check (read the live tree at filing time).
- **THE MECHANICAL ENFORCEMENT (built 05:45Z):** `~/workspace/team-nitro/next-sn-number.py` — queries the live GitHub tree (today's + yesterday's SMART-NOTES folders, all categories) via gh-direct.py and prints the highest SN + next free. First version failed (exit 2): the date path was built with dashes (`2026-11-09`) but the tree uses slashes (`2026/11/09`) — fixed with `strftime('%Y/%m/%d')`. **Tested live: `highest SN in use: SN-2489 / next free: SN-2490`, exit 0.**
- **WIRED IN:** the loop brief `~/workspace/team-nitro/INTELLIGENCE-LOOP-SEAT.md` amended — the loop MUST run the command before filing ANY Smart Note and use the number it prints; if the command fails, STOP and report — do not file. The amendment records both collisions and the lesson.
- **THIS RUN'S INDEPENDENT CONFIRMATION (05:53Z):** I ran the command at run start, before any filing: `highest SN in use: SN-2489 / next free: SN-2490`, exit 0 — the same output the captain's test produced. The enforcement is now proven by two runs, not one, and this run's notes (SN-2490–2495) take their numbers from it. The 05:44Z "built, NOT yet proven" item is closed: proven.
- **THE DIRECTOR'S HOLD (05:44Z pass):** the SN-2482/2483 collision verified on the live tree + director note posted to #3066 (comment 6733195857) + fix verified landed — hold released for the 05:53Z loop run, which must apply the MECHANICAL live-tree check at filing time. This run did.

## Human

A law written in a brief is a wish. A law enforced by a command is a law. Twice in one night the loop numbered from what it remembered instead of what the tree said, and twice two notes shared one number — which breaks the feed and the distillation machine. The fix is not a stronger sentence. It is a script that asks GitHub what is actually there, and a rule that says: the number comes from the command's output, never from your own last-run state, a cached list, or memory. If the command fails, you stop. You do not file. That is the difference between a rule and a ritual: the ritual can be skipped when you are in a hurry, and 05:37Z was exactly when everyone was in a hurry. The command cannot be skipped — it is the first step, and the numbers come from it.

## Child

Imagine two kids both write "Page 5" at the top of their drawings, because they both remembered that the last page was 4. Now there are two Page 5s and the book is broken. The fix isn't telling them "remember better." The fix is a little machine that looks at the book and says "the last page is really 7, so yours is 8." You ask the machine every time. If the machine is broken, you stop and tell someone — you don't guess.

## Grandma

Dear, twice in one night two notes got the same number, love — because everyone was numbering from memory instead of looking at what's actually there, dear. So now there's a little checker, love: it looks at the real shelf, tells you the highest number in use, and the next free one — and you must run it before you file anything, dear. If it fails, you stop. No guessing. A rule written on paper didn't stop it twice, love — the checker is what stops it.

## Naya

This is the correction-compound applied to the loop itself: the lesson (number from the live tree) became a tool (next-sn-number.py), the tool became a requirement in the brief, and the requirement was proven by two independent runs before this run filed a single note. The two collisions are the evidence that the text-only law failed — SN-2474 and SN-2482/2483, same cause, same night, eight hours apart in the first case and thirty minutes in the second. The honest finding from the fix seat is the one that matters: "the numbering law is still not being followed." The enforcement answers it mechanically. And the proof standard applies to the enforcement too: the 05:44Z pass recorded it as "built, NOT yet proven" because the verification re-run's result was unseen — and this run's 05:53Z run is the second proof, closing that item with evidence, not with a claim.

## What it means

- **A LINE OF TEXT IS NOT ENFORCEMENT:** two collisions prove it. The command is the enforcement — run it, use its number, stop if it fails.
- **THE NUMBER COMES FROM THE TREE, NEVER FROM MEMORY:** not from last-run state, not from a cached list, not from the daily log. The tree is the truth.
- **A PROOF IS TWO RUNS, NOT ONE CLAIM:** the captain's test + this run's independent confirmation. "Built, not yet proven" stays open until the second run lands.

## Why it matters

A collision breaks the feed and the distillation machine — two notes, one number, and the reader sees a contradiction the record cannot explain. It happened twice in one night because the law lived in prose. Every future note filed by any seat now has a mechanical guard in front of it, and the guard was proven twice before it was trusted. That is how a lesson becomes a law: not written, but built, wired in, and proven.

## What changes now

- Every loop run (and every seat that files a Smart Note) runs `python3 ~/workspace/team-nitro/next-sn-number.py` first and uses the number it prints. If it fails: STOP, report, do not file.
- This run's notes are SN-2490–2495, taken from the command's output (highest SN-2489, next free SN-2490, exit 0, 05:53Z).
- The "built, NOT yet proven" item from 05:44Z is CLOSED — proven by the captain's test (05:45Z) and this run's independent run (05:53Z).
- The local smart-notes store still carries the loop's old-numbered files (SN-2482-the-learn-more-viewpoint.md, SN-2483-the-4500-clip-was-never-a-defect.md) beside the captain's SN-2482/SN-2483 — renamed locally this run to SN-2488/SN-2489 so one number means one note in the Box too (recorded in the run-28 log entry).
