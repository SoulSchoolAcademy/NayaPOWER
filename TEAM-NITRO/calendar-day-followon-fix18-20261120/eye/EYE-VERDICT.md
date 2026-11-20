# CAPTAIN'S EYE — fix-18 (desktop leg)

- **Staged:** blob `f7b14ce7`, 413,386 B — https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix18-20261120&cb=f7b14ce75d590738a9efb87a4fa056ee98f3561d
- **Eye:** cloud browser, 1919×998 viewport, 2026-11-20 09:25–09:28 MST. Nothing edited, merged, or deployed.
- **Verdict: GOES BACK** — item 1 only. Items 2 and 3 PASS.

## Item 1 — GOES BACK (gap 16px, not 24px)
"November 2026" is centered (text spans x=837–1078, centre 957.5 vs viewport centre 959.5 — offset −2px) and on one line. But the glyph-to-glyph gap between "NOVEMBER" (ends x=993) and "2026" (starts x=1010) measures **16px, measured twice with identical results** — 8px short of the 24px target. Inter-letter gaps inside the words are 4–7px, so the word gap is visibly wider, but it does not meet the target. The checker's "exactly 24px" is a measurement difference; the eye's glyph-to-glyph number governs until the maker re-proves 24px the same way.
**Fix:** make the gap a true 24px glyph-to-glyph and re-prove it by measurement. Fold into Round 2 or a small fix-18 follow-up. Do not ship fix-18 until it measures 24px.

## Item 2 — PASS
No "396 HZ"/"396 Hz" in the top header, month view or day view (day header: "Friday 20", "November 2026", live clock only). Wisdom line keeps both mentions intact: "Friday · 396 Hz · red — The day of the ground — the root, 396 Hz."

## Item 3 — PASS
All 9 day-view slides checked for Fri Nov 20, 2026. Pill present on exactly two: 1 of 9 Wisdom and 4 of 9 Worlds (bottom-right of the cover image). Absent on: 2 of 9 Notifications (confirmed — no pill anywhere), 3 of 9 Journal, 5 of 9 News Hub, 6 of 9 Appointments, 7 of 9 Summary, 8 of 9 Naya Notes, 9 of 9 Smart Notes.

## Also confirmed
Page loads fully, no error message or failed content observed (images decoded, month grid rendered). Deck/nav work: opened today (Nov 20) from the month grid, tapped through all 9 slides via the block dots, "Back to month" returned to the month view.

## Still owed from my own eye
Phone-390 leg (cloud browser can't resize; the checker's 390 leg does not stand in for it).
