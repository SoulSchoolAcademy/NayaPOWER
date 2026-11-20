# SN-3963 — Measure the Whole Chrome, Not the Container

**Filed:** Intelligence Loop run 386, 2026-11-19 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3963; drafted and filed in run 386.

**Filed by:** Intelligence Loop run 386, 2026-11-19 — captain's eye on the Connection Profile fix-1 staged link, ~17:19–17:25 MST (2026-11-20 00:19–00:25Z).

**Paired Naya Note:** NN-20261119-measure-the-whole-chrome-not-the-container

## The teaching, in his words (in substance, as recorded)

The Connection Profile fix-1 eye came back MIXED. The scroll fix works for Thora, Terra and Zoe — but NOT for Sophia. Sophia's orb (twice) and "i" all landed at scrollY 1,836 in three consistent trials — ~680px too far: "← Back to Connections" completely above the viewport, the header card's top edge off-screen, the "S" orb top truncated. Thora "i" 1,160, Zoe "i" 1,101, Terra orb 1,147 — all correct landings with Back fully visible. The distinction is the person, not orb vs "i". The tension: the fix-1 checker measured Sophia at scrollY 1810 with `#pcProfileView` rect.top 0 and called it in-viewport — but the Back button sits ABOVE the view element, so the container's top is not the whole chrome. The checker's measurement was true of the container and false of the page the citizen sees. Fix-2 is dispatched (base = fix-1 tip); no merge of PR #3491 until it clears. The card spot-check passed (four action buttons in colours, seven cards counting the header, note saved and read back and persisted across profile switches).

## The understanding

A container is not the page. The citizen arrives and needs the whole chrome — the way back, the header, the orb — not just the element the fix scrolled. Measuring the container's top edge proves the container arrived; it says nothing about the chrome above it. The eye caught what the measurement missed because the eye looks at what the citizen sees, and the citizen sees the whole screen. A landing is proven only when everything the citizen needs on arrival is in view — Back included.

## The law

Measure the whole chrome, not the container. A scroll fix is proven when the Back button, the header and the orb are all in view on arrival — for every person, not just the ones whose layout happens to fit. If any person's chrome falls off the top, the landing is wrong for that person, whatever the rect says.

## Owed from this dictation

Connection-profile fix-2 carries the Sophia landing (scroll the whole chrome into view); PR #3491 stays unmerged until it clears.

**The rect can be 0 and the page still wrong — measure what the citizen sees.**
