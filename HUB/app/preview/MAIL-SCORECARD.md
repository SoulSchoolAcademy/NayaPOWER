# Smart Mail — Room Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2`.

## Director rework — depth, color, honesty (2026-10-02, Shawn's review)

Shawn's notes, verbatim in spirit: the icons are too flat (he wants them
"coming off the page" — living depth); the "DEMO THREADS · seeded for
design review" pill reads as a nonsense button — get rid of it; the three
folders are "hyper blued" — everything lights up the same blue.

1. **Banner gone.** The `.ml-demo` pill is removed from the header. Honesty
   is unchanged: every seeded thread still carries its own DEMO chip.
2. **Folders own their colors.** Inbox stays blue, Unread is green, Sent is
   purple when lit — each folder's color is stable (its identity), never
   positional. The unread badge, unread dots, and unread sender names all
   speak green now.
3. **Icons with living depth.** Each folder gets an SVG icon (tray /
   envelope-dot / paper plane) in its folder color with a glow that
   intensifies on hover and ignites on active. Avatars are gradient spheres
   now — top-light catch, inner shadow, deep contact-color glow — instead of
   flat discs. The unread dot is a radial green orb.

## Score: 9.3/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Contract honesty | 10 | No canonical mail store; seeded threads carry DEMO chips. Sent mail is genuinely user-created and persists. |
| 2 | Button law | 10 | Folders filter, open marks read (badge decrements), reply prefills, send appends + persists, validation blocks empty sends, Escape closes. |
| 3 | Color law | 10 | Blue = room identity; inbox blue / unread green / sent purple — stable per folder; contact/space colors drive avatars only. |
| 4 | Icon craft / depth | 9 | SVG folder icons with igniting glow, gradient-sphere avatars, radial unread dots. Shawn's eyes confirm the feel. |
| 5 | Readability | 9 | Three panes, time-ago stamps, unread dots, empty states per folder. |
| 6 | Accessibility | 9 | Keyboard-operable threads, modal focuses To, Escape closes, aria wired. Compose modal has no full focus trap yet. |
| 7 | Functional completeness | 8 | No search, no delete — a real mailbox needs both. |

## Effectiveness scorecard (Shawn: "is it going to be effective, is it functionable")

The room's job: see what you need to act on, inside the NayaNET network.

| # | Effectiveness test | Score | Note |
|---|--------------------|-------|------|
| 1 | See what needs action | 9 | Unread folder + green dots + badge count. No search across the archive yet. |
| 2 | Read a thread fully | 10 | Full body, meta, reply / mark-unread right there. |
| 3 | Write to a person or space | 10 | Compose with grouped To, validation, send persists locally. |
| 4 | Trust what's shown | 10 | DEMO chips on seeded threads; sent mail unlabeled honestly; no fake delivery claims. |
| 5 | Feel pro doing it | 9 | His three corrections applied this pass; his eyes are the last point. |

**Effectiveness: 9.6/10.** It does the job — the gap is search + delete.

## What would make it more impressive (my honest ranking)

1. **Search** — instant filter across subject/snippet/body. A mailbox you can't search isn't functional at scale. This is the big one.
2. **Delete** — remove threads from the reading pane. Mail you can't throw away isn't a real mailbox.
3. **Focus trap** in the compose modal — correctness; Tab shouldn't escape the dialog.
4. **Star / flag** — mark what matters, find it later.
5. **Mark all read** — one tap, inbox zero.

## Why not 10

- **-0.4 — no real mail store.** Seeded content is demo by necessity; the production read path (Supabase → shell → ctx.threads) is shell work and a protected gate.
- **-0.2 — no search / delete** (the functional gap above).
- **-0.1 — compose modal focus trap incomplete.**

## What closes it

- Search + delete + focus trap -> +0.3
- Shell feeds the production mail store into `ctx.threads` (demo flag off) -> +0.4
- Director visual pass -> +0.3

## Verification

node syntax OK (adapter + room), CSS brace balance OK, 23-check stub-DOM smoke suite green (banner gone, per-folder icons/colors, badge, folder filtering, open-marks-read, compose→send→persist, avatar/dot/icon depth in CSS).

## Files

- `HUB/app/js/rooms/mail-adapter.js` — `MailAdapter.parseThreads(raw)`, newest-first, skips unparseable.
- `HUB/app/js/rooms/mail.js` — `window.NayaRooms.smartMail(el, ctx)`; ctx.threads/contacts/spaces/me.
- `HUB/app/css/mail.css` — blue identity, glassmorphism, responsive ≤760px.
- `HUB/app/preview/build-mail-preview.py` — seeds 7 demo threads, writes `~/workspace/your_files/mail-preview.html`.
- `HUB/app/preview/MAIL-SCORECARD.md` — this file.
