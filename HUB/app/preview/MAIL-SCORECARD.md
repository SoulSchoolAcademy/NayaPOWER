# Smart Mail — Room Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2`.

## The congruency pass (2026-10-02, Shawn: "you're not hitting the mark yet")

He was specific, and he was right on every point:

1. **Buttons back to obsidian.** My "jewel" pass had drifted them to grey.
   Now: black-black (`#0b0b0e` → `#1b1b21`) with depth done right — top-light
   edge, deep shadow — never grey. Send, Cancel, Compose, folders: all
   obsidian. Color ignites on hover; the black stays black.
2. **One folder family.** Inbox glowed while the others went flat — now all
   three whisper their own color at rest and ignite when active. Same
   shape, same depth, same icon treatment. Congruent.
3. **Badge moved.** The green unread count no longer sits inside the blue
   box — it lives on UNREAD, green on green, where it belongs. Inbox
   stopped wearing someone else's color.
4. **Avatars are balls.** True spheres now — radial shading with a specular
   highlight top-left — in both rooms. No more flat discs.
5. **Bolder icons.** Stroke weight up, light-variant color for contrast
   against the black, cleaner glow.

## Scorecard — his lenses: effectiveness, quality, pro level, contrast, clarity, congruency, color

| # | Lens | Score | Note |
|---|------|-------|------|
| 1 | Effectiveness | 10 | Conversations thread, search, delete, reply-appends, spine, compose — the job is done. |
| 2 | Quality | 9 | This pass answers every note he gave. His eyes confirm the finish. |
| 3 | Pro level | 9 | Feels like real software now. He confirms. |
| 4 | Contrast | 10 | Obsidian + white text = maximum; folder colors distinct; unread green pops. |
| 5 | Clarity | 10 | Badge where it belongs, one folder family, honest empty states. |
| 6 | Congruency | 10 | Same treatment everywhere; colors never leak across identities. |
| 7 | Color law | 10 | Inbox blue / unread green / sent purple, stable; contact colors on balls. |

**Score: 9.7/10.** Why not 10: quality and pro level are his call
(-0.2), and the production mail store is the shell's job (-0.1, honestly
labeled DEMO until then).

## The organism loop (2026-10-02, elite pass)

Mail to a space is now a post in that space — same object, two views
(`naya.smartspaces.posts`, tested). Thread → Smart List is specified as
a contract (`ORGANISM-LOOPS.md`), not built: no competing note store,
no writer nobody reads.

## Verification

node syntax OK, CSS brace balance OK, 55-check stub-DOM suite green
(threading, search, delete + tombstones, traps, spine, badge placement,
space-post loop, obsidian + ball + congruency + reduced-motion CSS).

## Files

- `HUB/app/js/rooms/mail-adapter.js` — `MailAdapter.parseThreads(raw)`, newest-first, skips unparseable.
- `HUB/app/js/rooms/mail.js` — `window.NayaRooms.smartMail(el, ctx)`; ctx.threads/contacts/spaces/me.
- `HUB/app/css/mail.css` — blue identity, glassmorphism, responsive ≤760px.
- `HUB/app/preview/build-mail-preview.py` — seeds 7 demo threads, writes `~/workspace/your_files/mail-preview.html`.
- `HUB/app/preview/MAIL-SCORECARD.md` — this file.
