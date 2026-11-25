# MAKER REPORT — FIX ROUND — Custom Jewel Icon Set (2026-11-24)

**Round:** Fix maker for the checker GOES BACK verdict on the jewel icon
set. **Verdict: DONE — all five failing items fixed, staged, filed, and
the staged link rendered (phone 390 + desktop, 0 page errors).
Self-score 8/10 (the missing 2 are the eye's alone: the emblem gap —
vector medallion vs photoreal faceted jewel — stands, and the final
verdict is Shawn's eye).**
**Nothing live.** Branch `jewel-icon-set-20261124`, no PR, no merge, no
live deploy, no message to Shawn.

## 0. Activation read first (before any work)

`checker/CHECKER-VERDICT.md` (in full, first) · `THE-NAYA-DESIGN-LAWS.md`
(full, §0.5 ten laws first) · `laws/THE-REAL-OBJECT-LAW.md` (full) · the
MESSENGER + MAIL entry in `MEMORY.md` (colour flow law + point 7) ·
`maker/MAKER-REPORT.md` (first round) · the emblem itself,
`~/workspace/user/media_library/image/NAYA_ICON.png` (seen again: faceted
purple diamond, silver winged crown frame, black ground — the bar).

**Declaration:** I am Anaya, the wise one. I think before I act. I do the
most intelligent thing, every time, for everyone it touches. I prove it
with receipts. I give ten stars by default. I never waver.

## 1. The five failing items — what changed per item

### Item 1 (BLOCKER) — staged showcase showed zero icons. FIXED.
The proof host serves one file per `?file=` URL; the showcase's 47
relative `<img>` refs + `jewel-icons.css` resolved to the host root
without the `?file=/ref=/cb=` params and 400'd. The fix: the staged
showcase is now ONE self-contained file — all 59 icons + the CSS inlined
into `showcase.html` (189,462 B, sha256
`21887143…`). The human-editable source stays as
`showcase-template.html` (same relative refs, readable); `node
build-showcase-inline.mjs` rebuilds the staged file after any edit. The
standalone SVG files remain the consumable assets — inlining is
staging-only. Note: the same icon file is inlined several times (mail in
§1 and §2, type-chat-sm five times in the ladder); its gradient ids
repeat verbatim, the definitions are byte-identical, so the render is the
same. Verified by RENDERING the staged link itself (see §6), not by
curling bytes — the failure the checker caught was bytes-only
verification, and this round does not repeat it.

### Item 2 — bottom bar colour flow wrong, 2 of 6. FIXED.
Baked real variants: `icons/presentation/bar-add.svg` — the plus in
royal purple `#8e24aa` (core `plus.svg` keeps its indigo spectrum slot)
— and `icons/presentation/bar-worlds.svg` — the globe in deep gold
`#d4a017` (core `spaces.svg` keeps its purple slot). A `--c` wrapper
cannot recolour a baked SVG, so the bar gets its own files; the core
icons are untouched. Measured on the render: bar rims read `#8e24aa`,
`#0f52ba`, `#07925f`, `#d4a017`, `#c2410c`, `#c62828` — purple, blue,
green, gold, orange, red. Exactly the flow.

### Item 3 — emoji were a second, unacknowledged construction. FIXED.
All 12 emoji rebuilt into the ONE construction (generator
`build-jewel-icons.mjs`, `emojiIcon()` now shares the full-icon anatomy):
obsidian disc — board black inside, no glow inside · silver bezel · the
icon's own colour as rim + outside halo + faceted crown jewel at 12
o'clock · slow orbit ring (65–175s, alternating direction) · the face as
the WHITE glyph, with a dark cast copy down-right and a top-left
specular. The old `gemorb` coloured fill, the facet spokes and the
polygon are gone. Construction audit on the live render, 12/12: orbit
yes, obsidian disc yes, crown yes, `gemorb` no. No exception is claimed
and none is needed — the emoji ARE the one construction now. Laws cited:
§4 (inside = board black) / §3 + §12.8 (no colour fills).

### Item 4 — think.svg stray ring on the bezel. FIXED.
The outer thought-bubble circle moved from (74,23) r=3.2 — centre
distance 36.1, outside the disc, straddling the bezel — to (68,26)
r=2.6: centre distance 29.7, outer edge 32.3, clear of the disc edge
(35.5) and the bezel. The inner bubble moved to (63,32) r=2.0. The party
hat was pulled inside the disc in the same pass (apex 12 → 22, clear of
the crown jewel at y 4–16) — it sat on the disc edge under the crown.
Verified in the live DOM: every think circle's outer edge is < 35.5
(except the halo r=47, orbit r=44 and crown specular by design), and the
render shows both bubbles inside the disc.

### Item 5 — phone bar wrapped 4+2, labels touched. FIXED.
The bar is now `flex-wrap: nowrap` with `flex: 1 1 0` cells and 44px
icons at ≤480px: one row at 390px, `scrollWidth == clientWidth` (364),
all six cells on the same top. The labels hide at phone width — and only
there. This is measured, not styled around: with real Marcellus at 17px,
ECOSYSTEM is 101.1px wide and ACTIVITY 80.3px against a 62px cell pitch
at 390px, so six 17px labels cannot sit in one row without touching;
shrinking them would break laws §2.3 (no text under 17). The names still
read in the §2 lede above the bar, in order, and the labels return on
desktop (verified: all six visible, one row, top 1260). The trade-off is
named here in plain words so the checker can judge it — it is not
silent.

## 2. Follow-ons — done in this round

- **Wow mouth:** the r=4.8 dot is now an open oval (rx 5.5, ry 7) with a
  dark cast copy — it reads as an open mouth at 64px and at 24px.
- **Emoji `-sm` variants:** all 12 exist now (`icons/emoji/*-sm.svg`,
  48px art, same construction, face scaled half into the disc, crown
  jewel, no orbit — like the presentation `-sm`). The showcase shows all
  12 at 24px in a new row under §4.
- **USAGE.md:** emoji colour table added (12 rows), `-sm` inventory
  added (presentation 7 + emoji 12), bar-variant table + note added,
  counts updated 41 → 55.
- **Count correction:** the real count in the first round was 47 img
  refs, not 48 — the 48th is the escaped `<img
  src="icons/core/mail.svg">` example inside the §5 text. The fix-round
  template carries 59 real refs (47 + the 12 emoji `-sm` row) plus that
  same escaped example; the staged showcase inlines all 59, 0 external
  refs.

## 3. What stays (untouched, per the brief)

The core construction is proven and was not rebuilt: 12 core + 10
presentation + 7 presentation `-sm` SVGs are byte-identical to round 1
(the generator's `fullIcon`/`smallIcon` paths are unchanged);
`jewel-icons.css` is byte-identical; hover lift `translateY(-4px)
scale(1.04)` + ignite, press `scale(0.97)`, mail orbit 120s period,
type-chat-sm legible at 16px — all re-measured on the local render
(§6) and unchanged.

## 4. §11 check — in writing

**Five gates:** 1 Right — the checker's own five items, staged only,
nothing live. 2 Truly needed — the captain cannot eye-check a page that
shows zero icons; the bar colour flow is Shawn's law (§3.2). 3 Mine to
do — new branch commit, staged only, no money/credentials/destructive
step, no live deploy. 4 Now — the round is the lane's next step, inside
the hour. 5 Prove it — receipts in §5–§6, including a render of the
staged link itself.

**The design check, per object:**
- Could I pick this up? Obsidian disc + silver bezel + cast shadow +
  specular: layers, lift, real shadow down-right — now on the emoji too.
  Reference objects: the emblem (crown jewel + silver frame) and the
  Personal bottom-bar tile.
- Where is the light from? Top-left, always — every gradient 135°,
  shadows down-right, specular top-left, in the new emoji as in the core.
- What is it made of? Board black inside, white glyph/face in the
  middle, silver bezel, own-colour light outside.
- Does it cast a shadow? Yes — glyph/face cast copy + tile/box shadows.
- What happens when I touch it? `.jwl` lifts + lights whole in its own
  colour on hover, depresses scale 0.97 on press; in-message jewels stay
  still. Re-measured live: hover `matrix(1.04, 0, 0, 1.04, 0, -4)`,
  press `matrix(0.97, 0, 0, 0.97, 0, -1)`.
- Any glow inside, at rest or hover? No — the halo is outside only; the
  emoji disc is the same black-on-black gradient as the core.
- Any text gray, especially small? No — design-law check PASS, 0
  warnings, on the inlined showcase.
- Any text smaller than 17? No — 25 / 19 / 17 throughout; the phone bar
  hides its labels rather than shrinking them (§1 item 5).
- Two same colours together anywhere? No — the bar now reads the fixed
  flow; the core spectrum order is unchanged.
- Anything flat or dead? No by construction — every icon has bezel,
  shadow, specular, orbit; every tile answers hover. The emoji now turn
  (orbit measured: mail 22.4° → 40.5° over 6.1s ≈ 18° expected for a
  120s period).
- Can I see what the icon IS? Mail, chat, mic, camera, the faces
  (smile, laugh, love, wow, think, cool, sad, party, peace, fire,
  thumbs-up, star) — each distinct, never the same shape in a different
  colour.
- Which reference object was each measured against? The emblem
  (`NAYA_ICON.png`) for the jewel language; the Personal bottom-bar tile
  for the construction.
- Read as a reader: yes, this time — the staged link was rendered at
  phone 390 and desktop and read top to bottom (§6 + screenshots in
  `maker/fix-local-*.png` and the staged probe's shots).

**Sense check:** the phone-bar label decision is the one place the brief
and the geometry disagreed, and the geometry won with the reason named
(§1 item 5). The inlining decision keeps the consumable assets as files
and makes staging-only the self-contained copy — a consumer never has to
take the showcase apart. The spaces globe still reads as a leaf/eye at
small sizes; redrawing a harvested glyph is a design decision, not a
colour fix, so it stays owed and named (§7) rather than silently
redrawn.

## 5. Design-laws check + byte verification

- `python3 check-design-laws.py showcase.html` (inlined): **PASS — 0
  warnings.**
- **55 SVGs**, all XML-parsed clean (55/55). Generator run: `node
  build-jewel-icons.mjs` → "icons written: 55".
- **Showcase:** 59 SVGs inlined, 0 `<img>` tags, 0 external stylesheet
  refs (Google Fonts link only, falls back to Georgia serif in this VM).
- **Filing:** branch `jewel-icon-set-20261124`, commit A
  `62b19dcb83eee5782ca920c0ea60f58cda99fa97` (64 files filed, 0 SHA
  mismatches, ref verified); commit B (this report) is the branch tip —
  see §8. Tree entries under `TEAM-NITRO/jewel-icon-set-20261124/`: 68
  (64 blobs + 4 directory trees). Filing ran through the git-data API
  via `gh-direct.py` (in-memory token), as round 1. No raw token touched
  a file, a log, or a command line.
- **Showcase blob:** `09896daf092ced1a7a45803962366a085757ff5e`, 189,462 B,
  sha256
  `218871438e47301bb9772fcb88744a3b3b23e1bbd99a0c6337a9c9cb8a43cc3f`
  — identical to the local file.
- **Environment note:** a service restart mid-round wiped the VM's
  Playwright Python package (`/usr/local` is ephemeral) and the running
  proxy forwarder + local server. Both were restored (forwarder PID
  restarted, `pip install playwright` from cache, server re-started) and
  the probe re-run clean — the numbers in §6 are from the re-run, not
  the interrupted one.

## 6. Verification — local render (before filing) + staged render (after)

Local render (Chromium via the 127.0.0.1:18080 forwarder, same bytes,
`verify-fix-local.py`, phone 390×844 dsf 3 + desktop 1280×800):
59/59 inline SVGs render (0 zero-size), 0 `<img>` tags, **0 page errors,
0 failed requests, both widths**. Bar phone: one row, nowrap, no
overflow, rims purple/blue/green/gold/orange/red. Emoji 12/12:
orbit + disc + crown, no `gemorb`. Think outer bubble edge 32.3 < 35.5.
Wow mouth ellipse present. Hover/press/orbit re-measured (§4). Desktop
bar: labels visible, one row. Screenshots: `maker/fix-local-phone-*.png`,
`maker/fix-local-desktop-*.png` (lane evidence, not filed).

Staged render (the linked page itself, `verify-fix-staged.py`, Chromium
via the forwarder, phone 390 + desktop — run after filing, before this
report was filed):
- Staged link: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/jewel-icon-set-20261124/showcase.html&ref=62b19dcb83eee5782ca920c0ea60f58cda99fa97&cb=09896daf092ced1a7a45803962366a085757ff5e&t=1795050600
- Fresh staged fetch: HTTP 200, 189,462 B, sha256 `21887143…` — identical
  to the local file and to the filed blob.
- Rendered: 59/59 inline SVGs render, 0 page errors, 0 failed requests
  (Google Fonts loads through the forwarder; the VM's cert warning is
  environmental, as the checker noted in round 1).
- Bar phone: one row, rims purple/blue/green/gold/orange/red. Bar
  desktop: labels visible, one row. Screenshots: staged probe shots in
  `maker/fix-staged-*.png` (lane evidence, not filed).

## 7. Seven questions, answered in writing

1. **Is it 9 or better?** **8/10 — honest.** All five checker items are
   fixed and re-proven by render, including the staged link itself. The
   missing 2 are the eye's alone: vector medallion vs the emblem's
   photoreal faceted jewel, and the final verdict is Shawn's eye.
2. **What could this break?** Nothing live: new commits on the same
   branch, no PR, no merge, no live deploy, no page wiring. Inside the
   set: the inlined showcase duplicates gradient ids per repeated icon
   (byte-identical defs — visually the same); the standalone files are
   unchanged as assets. The emoji rebuild changes 12 files' bytes — any
   consumer already using the round-1 emoji gets the new construction
   on the next pull (nothing is live yet, so nobody is).
3. **Are the automatic checks green?** Yes: laws checker PASS
   (0 warnings); XML parse 55/55; blobs 0 mismatches; staged sha match;
   local + staged renders 0 page errors, 0 failed requests.
4. **Five gates?** All five yes (§4).
5. **Proved with real measurements?** Yes — renders, rim hexes,
   bounding boxes, orbit angles, blob SHAs, staged sha256 (§5–§6).
6. **Anything knowingly left not-10?** (a) The spaces globe reads as a
   leaf/eye at small sizes — owed, named below. (b) No wiring into
   Messenger/Mail — the look round's job. (c) Custom font — separate
   round. (d) The phone bar hides its labels — a measured trade-off,
   named in §1 item 5 for the checker to judge.
7. **What would make it a 10?** Checker re-verification passing on the
   staged link; captain's eye; his eye; then the Messenger + Mail look
   round wearing these jewels live.

## 8. Filing and staged receipt

- Branch: `jewel-icon-set-20261124` (from main
  `879a7fdcccea3e77ea24949a99de27fe07518116`; round-1 tip
  `2d60190d20f65747e775eb006d1b54805f2038f4`)
- Commit A (the fix): `62b19dcb83eee5782ca920c0ea60f58cda99fa97` (64 files,
  parent `2d60190d`)
- Commit B (this report): the branch tip. It changes no asset — the
  staged link below (commit A ref) serves the identical showcase blob,
  and the tip sha is recorded in the fix-maker's delivery to the captain.
- Staged link (commit A ref; the showcase blob is identical at the tip):
  https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/jewel-icon-set-20261124/showcase.html&ref=62b19dcb83eee5782ca920c0ea60f58cda99fa97&cb=09896daf092ced1a7a45803962366a085757ff5e&t=1795050600
- Staged bytes: sha256 `21887143…` — identical to the filed blob
- Local copy: `jewel-icon-set-20261124/maker/` (whole lane)
- No PR, no merge, no live deploy, no message to Shawn.

## 9. DONE / NOT-DONE

DONE: staged showcase renders as linked (self-contained) · bar colour
flow purple/blue/green/gold/orange/red · emoji in the one construction ·
think bubble inside the disc · phone bar one row at 390px · wow mouth
oval · 12 emoji `-sm` variants · USAGE emoji table + `-sm` inventory ·
47-vs-48 count corrected · laws PASS 0 warnings · filed on branch
`jewel-icon-set-20261124` (commits `62b19dcb` + this report).
NOT-DONE: checker re-verification (staged render) · captain's eye · his
eye + tap · wiring into Messenger + Mail (look round) · spaces globe
redraw (harvested geometry reads as a leaf/eye at small sizes) · custom
font (separate round).
