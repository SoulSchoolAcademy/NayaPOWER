# Full Screen, Not a Column

SN-2422 · DESIGN

**Created:** 2026-11-09 01:48Z

**Source:** Shawn's eye on a laptop screenshot of nayanet.app/pricing, 01:48Z (daily log 2026-11-09.md). Measured and confirmed 01:50Z.

## Hook

"Why is the pricing page not full screen?" — and the honest answer: it isn't a mobile problem, it's a column. The page was built in a centered ~1140px max-width column, so a laptop shows dead black space on both sides.

## Nutshell

His eye caught what no check had measured: on his laptop the pricing page occupies about two-thirds of the screen, with dead black space on both sides. The captain's honest answer the same pass: it is NOT mobile optimization — the page was built in a centered ~1140px max-width column; the phone layout is the same page stacked. His instinct is right (viewport is the stage — the Real Object Law's stage, SN-0858). **Measured 01:50Z by live browser at 1919px: content column 1,248px wide, gutters ~328px each side — the page occupies ~65% of the viewport, ~35% dead black space.** A full-screen seat was dispatched the same pass (brief `PRICING-FULLSCREEN-BRIEF-20261109.md`): widen to fill the viewport on desktop/laptop (24–40px gutters), phone unchanged, width only, verified at 1920/1440/1280/390. Re-freeze (GitHub + live + PI) follows once it lands. The same measurement pass confirmed the live letter carries the NEW wording (fixed line + "Welcome. It's ready for you." + signature exact; zero "smart pages" in the letter).

## Human

His question, 01:48Z: "why is the pricing page not full screen?" The captain's answer the same pass: "it is NOT mobile optimization — the page was built in a centered ~1140px max-width column, so a laptop shows dead black space on both sides; the phone layout is the same page stacked. His instinct is right (viewport is the stage)." The 01:50Z measurement: "content column 1,248px wide, gutters ~328px each side — the page occupies ~65% of the viewport, ~35% dead black space."

## Child

Imagine you paint a beautiful picture, then hang it on a huge empty wall with nothing around it — the picture is lovely, but most of the wall is just dark and empty, and your eye keeps wandering off the picture. The picture should fill the wall. That's the page: it should fill the screen it's on.

## Grandma

Dear, he looked at the page on his laptop and asked why it didn't fill the screen — and he was right. The page was sitting in a narrow strip in the middle with big black empty spaces on both sides. We measured it: only about two-thirds of the screen is the page. The fix is to let it breathe out and fill the whole screen on a computer, while the phone stays just as it is.

## Naya

Two lessons in one catch. First, the defect class: a max-width column is a design decision nobody re-examined after the page grew from a chart into a letter, a chooser, a calculator and a finale — the container stayed at the size the first chart needed. Second, the check class: every verification measured the page at its own width and never asked what fraction of the viewport it fills. The fix is width-only by design (24–40px gutters, phone unchanged) — and it is judged by the mobile-first law (SN-2421): widen the desktop without touching the phone. The re-freeze waits for the full-screen fix plus the wiring, so the frozen version is the wide one, not this column.

## What it means

- **His eye, 01:48Z: the pricing page is not full screen on laptop** — ~35% dead black space on both sides.
- **Cause: a centered ~1140px max-width column**, not a mobile problem. The phone layout is the same page stacked.
- **Measured 01:50Z at 1919px: content 1,248px, gutters ~328px each side, page ~65% of viewport.**
- **Fix dispatched (full-screen seat):** widen to fill the viewport on desktop/laptop (24–40px gutters), phone unchanged, width only, verified at 1920/1440/1280/390.
- **Re-freeze follows** once it lands (GitHub + live + PI) — the frozen version must be the wide one.
- **Same pass confirmed:** the live letter carries the new wording (fixed beat-12 line, "Welcome. It's ready for you.", signature exact).

## Why it matters

The viewport is the stage — a page that uses two-thirds of its stage looks unfinished no matter how good the two-thirds are, and on the biggest screen Shawn owns it reads as a defect at first glance. It also shows the verification gap: width, overflow and console errors were checked; share-of-viewport was never measured. From here, every page check asks what fraction of the viewport the page fills.

## What changes now

- The full-screen seat widens pricing to the viewport (desktop/laptop), phone unchanged.
- The final re-freeze waits for the full-screen fix + the wiring — the current live/GitHub v55 copy is NOT the final freeze.
- Viewport-share joins the verification checklist: measure the content column against the viewport at every width.
- The mobile-first law (SN-2421) governs how the widening is judged.
