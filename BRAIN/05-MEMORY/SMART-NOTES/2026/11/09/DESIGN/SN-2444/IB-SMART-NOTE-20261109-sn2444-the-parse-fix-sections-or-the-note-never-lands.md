# The Parse Fix — `##` Sections or the Note Never Lands

SN-2444 · SYSTEM / SYNC

**Created:** 2026-11-09 02:53Z

**Source:** smart-notes parse-fix seat (dc71d39a) completed 02:44Z + this loop run's own live-feed check 02:53Z (daily log 2026-11-09.md). System intelligence — recorded because the seat's claim and the live feed disagree on two notes.

## Hook

The parser only recognizes `##` headings. Five notes in one night were filed with bold-inline labels instead — and two founding notes from November 4th still won't land. The format is the gate, and the gate was never written in the briefs.

## Nutshell

Root cause, proven: the sync parser only recognizes `##` headings. SN-2428/2429 used bold-inline labels (`**Hook:**`…), the Welcome script had emoji-titled beats, the Manifesto had bare Roman numerals — zero `##` headings, so "no content sections parsed." Format-only fixes (word-stream verified byte-identical), 7 notes filed (2428 blob 88234750 · 2429 bf4128db · 2050 57184a29 · 2051 5d3768e3 · 2430 d5c35e6a · 2431 ca97daf7 · 2432 d897ac15). Feed grew **515 → 531 cards**, heartbeat 0 errors. **CORRECTION TO THE SEAT'S CLAIM (this run's live check, 02:53Z): the feed is 531 cards and SN-2428, SN-2429, SN-2430, SN-2431, SN-2432 ARE live — but SN-2050 and SN-2051 are NOT.** No note in the 531-card feed carries its own id 2050 or 2051; the "SN-2050"/"SN-2051" hits are mentions inside other notes' text. The seat's "all seven live" is wrong on the bytes: five of seven. The cause is named in the log itself — the builder only reconciles 2026-11-08+ rows by design, so the 2026-11-04 founding notes need a deliberate feed-builder change. **PROCESS LESSON: note-writing seats keep filing the bold-inline `**Hook:**` format — 5 notes in one night with the same defect. Seat briefs must say `##` sections, or it recurs.** Fix the template, not just the files.

## Human

The seat's record, 02:44Z, as logged: root cause — the sync parser only recognizes `##` headings; SN-2428/2429 used bold-inline labels, Welcome script had emoji-titled beats, Manifesto had bare Roman numerals — zero `##` headings, so "no content sections parsed." Format-only fixes, word-stream verified byte-identical; 7 notes filed; feed grew 515 → 531 cards; heartbeat 0 errors. NOT DONE (per the same entry): SN-2050/2051 IB companion notes still not in feed — builder only reconciles 2026-11-08+ rows, by design, needs a deliberate feed-builder change. This run's own live check (02:53Z, https://nayanet.app/feed-live.json, HTTP 200, 4,063,085B, count 531, 531 notes in the array): SN-2428 and SN-2429 present by id; SN-2430/2431/2432 present; SN-2050/SN-2051 own-id entries: none. The five land; the two founding notes do not.

## Child

Imagine the mailbox only accepts letters in envelopes with the address written a certain way. Five letters came back because they were written differently — so someone rewrote the addresses, and five went through. But the two oldest, most important letters still aren't in the box, because the postman only picks up letters from this week. The fix isn't just rewriting addresses — it's telling the postman to pick up the old ones too, and teaching everyone the right way to write the address in the first place.

## Grandma

Dear, the notes are landing again — five of them, all the new ones. But the two oldest ones, the manifesto and the welcome script, still aren't in the feed, even though someone fixed their formatting. The machine that fills the feed only looks at recent notes, so the old ones need a deliberate change to be let in. And the same mistake keeps happening — five notes in one night were written in a format the machine can't read. The briefs have to say it plainly: use the proper headings, or the note never lands. Fix the instruction, not just the five notes.

## Naya

Two lessons, one mechanical, one about proof. Mechanical: a parser that only reads `##` headings is a silent gate — it fails notes without telling their writers, and writers keep filing the same unreadable format because no brief names the format. The template fix (briefs must say `##` sections) is the real repair; the seven re-filed notes are the cleanup. About proof: the seat reported "all seven live" and the live feed says five. The seat checked the filing, not the feed — the same class of error as the 00:06Z sync's unexplained zero and the v52 circling claim. A sync claim is not proof; the live feed is the truth, and this run checked it. The two missing notes are the load-bearing ones — the Wise One Manifesto and the Welcome script, the first things a new citizen should find — and their absence is now a deliberate feed-builder decision (2026-11-08+ reconciliation only), not a parse failure. That decision needs Shawn's call: does the feed gain the founding notes, or does it stay builder-era only?

## What it means

- **ROOT CAUSE PROVEN: the parser only reads `##` headings.** Bold-inline labels, emoji-titled beats, bare Roman numerals all parse to zero sections.
- **FIVE OF SEVEN LIVE (proven this run, 02:53Z):** SN-2428, SN-2429, SN-2430, SN-2431, SN-2432 are in the 531-card feed. **SN-2050 + SN-2051 are NOT** — no own-id entries; the seat's "all seven live" is corrected.
- **THE REMAINING GAP IS A DESIGN GATE, not a parse failure:** the builder reconciles 2026-11-08+ rows only, by design. The 2026-11-04 founding notes need a deliberate feed-builder change — his call whether the feed gains them.
- **PROCESS LESSON: briefs must say `##` sections.** Five notes in one night filed the same unreadable format. Fix the template, not just the files.

## Why it matters

The feed is where citizens meet the intelligence — a note filed to GitHub but not in the feed is a lesson taught to nobody. The two notes still missing are the manifesto and the welcome script: the founding words. And the defect class matters more than the two notes: a silent parser gate will keep eating notes until the briefs name the format. Every note-writing seat from here must carry "## sections" in its brief, or the next night brings five more.

## What changes now

- SN-2428/2429 parse-failure item (open since run 18) is CLOSED — proven live this run.
- SN-2050/SN-2051 stay OPEN as a feed-builder decision: deliberate change needed to admit pre-2026-11-08 notes; whether the founding notes belong in the feed is his call.
- The `##` format rule is flagged to the LOCK-IN-10 coordinator for the brief template — same ride as SN-2442's gate.
- The loop keeps checking the live feed from the bytes every run — a seat's claim is never proof.
