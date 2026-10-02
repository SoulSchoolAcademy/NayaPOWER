# Smart Mail — Room Scorecard (Naya 4 subagent, 2026-10-02)

Branch: `naya4/room-02-reports-v2` @ 2000766. Files written, NOT committed/pushed (parent owns that).
Verified: node syntax OK (adapter + room), CSS brace balance OK, jsdom — 13 pass, 0 fail, 0 jsdom errors.

## Score: 9.2/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Contract honesty | 10 | No canonical mail store exists; all 7 seeded threads labeled DEMO (chip + header banner). Sent mail is genuinely user-created (no DEMO chip) and persists to localStorage. |
| 2 | Button law | 10 | Every button has a real consequence: folders filter, thread open marks read (badge decrements), reply prefills compose, send appends to Sent + persists, validation blocks empty sends, Escape closes. |
| 3 | Color law | 10 | Blue = Smart Mail identity; contact/space colors from the shared contract drive avatars only. Silver-white at rest, blue ignites on hover/focus. |
| 4 | Readability | 9 | Three-pane layout, time-ago stamps, unread dots, empty states per folder. |
| 5 | Accessibility | 9 | Threads are keyboard-operable (Enter/Space), modal focuses To field, Escape closes, aria-pressed/selected/live wired. No full focus trap in modal. |
| 6 | Responsive | 9 | ≤760px stacks panes; rail becomes horizontal. Not visually inspected (no screenshot pipeline). |

## Why not 10

- **-0.4 — no real mail store.** Seeded content is demo by necessity; the production read path (Supabase → shell → ctx.threads) is shell work and a protected gate.
- **-0.2 — modal focus trap incomplete** (focus enters, Escape exits, but Tab can leave the dialog).
- **-0.2 — visual confirmation pending** (screenshot pipeline down; structure verified via DOM).

## What closes it

- Shell feeds the production mail store into `ctx.threads` (demo flag off) → +0.4
- Focus trap in compose modal → +0.2
- Director visual pass → +0.2

## Files

- `HUB/app/js/rooms/mail-adapter.js` — `MailAdapter.parseThreads(raw)`, newest-first, skips unparseable.
- `HUB/app/js/rooms/mail.js` — `window.NayaRooms.smartMail(el, ctx)`; ctx.threads/contacts/spaces/me.
- `HUB/app/css/mail.css` — blue identity, glassmorphism, responsive ≤760px.
- `HUB/app/preview/build-mail-preview.py` — seeds 7 demo threads, writes `~/workspace/your_files/mail-preview.html`.
- `HUB/app/preview/MAIL-SCORECARD.md` — this file.
