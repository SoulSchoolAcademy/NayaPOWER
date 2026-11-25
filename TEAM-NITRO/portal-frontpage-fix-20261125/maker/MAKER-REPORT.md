# MAKER REPORT — Portal Front-Page Fix 2026-11-25

**Lane:** `~/workspace/team-nitro/portal-frontpage-fix-20261125/` · **Role:** maker.
**Nothing live, nothing to Shawn.** Staged only; live is Shawn's tap.
**Brief:** Shawn's eye, voice call 2026-11-25 ~15:51–15:52 MST — two defects, nothing else.

## Staged build (current)

- **Portal:** https://portal-frontpage-fix-20261125-staging.nayapower.workers.dev/
  — HTTP 200, **1,904,285 B, sha256 `737fca6be2832855c8f6b523fc4920b8ea3d35f363f95278f141671b0c6cc82a`**
  — verified by `curl` read-back + `cmp` byte-identical to the lane file.
- **Certificate:** same worker `/identity.html` — HTTP 200, **313,224 B, sha256
  `57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b`**
  — UNCHANGED from R2 (byte-identical, same sha). It should not have changed, and it did not.
- **Worker:** `portal-frontpage-fix-20261125-staging`, deployment **`3e2a3c64b3d74b3cb1bc9b994002f865`**,
  modified 2026-11-25T23:03:10Z. KV binding `WELCOME_ASSETS` live (verified via API).
  `/agreement` 302 → live `https://nayanet.app/agreement` (unchanged route).
- **Branch:** `portal-frontpage-fix-20261125` (new, from main), repo SoulSchoolAcademy/NayaPOWER.
  Code commit: `2bc3b1b0d4581ebf2fef85431e0958989ccad801` · head (with this report): `HEAD_COMMIT_SHA`.
  Blobs (verified via git blob API): `portal.html` (1,904,285 B) ·
  `identity.html` + `identity-consolidated.html` (313,224 B, sha `57bdd387…`) ·
  `worker-consolidated.js` (2,239,196 B, sha `ba354daf…`).
  Paths `TEAM-NITRO/portal-frontpage-fix-20261125/maker/`.
- **Build scripts (re-runnable):** `maker/build-fix.mjs`, `maker/build-worker.mjs`,
  `maker/verify-fix.mjs`, `maker/evidence/probe.py`.

## DEFECT 1 — FIXED: the wall of text is off the front page

His words: *"if you go in as a new user you have all this text underneath. You
shouldn't have this... There shouldn't be a bunch of text when you sign in.
That should just be middle of the button."*

- The visible front page now carries **only**: "NAYA WELCOMES YOU" (the greeting,
  kept — it is the greeting, not the wall) + the name input + the **Enter NayaNET →**
  button + the small ⓘ trigger, centred in the middle of the frame.
- The sentence *"By entering your name, you make it official — you are signing the
  Collective Agreement, and you get the deed to your own world: high-level digital
  real estate — your personal page, your business, your space — free forever."*
  is **gone from the visible front page** (the `<p id="fpDeedSentence">` now holds
  only the ⓘ button) and lives **verbatim as PARAS[0] of the inner agreement reader**
  behind the ⓘ — the reader opens on ⓘ tap, shows it as **"1 of 13"**, Next walks
  the other 12 paragraphs. The "Read the agreement ◆" link in the bottom bar stays.
- Side benefit, as the brief predicted: the eye's R2 observation 2 is fixed — the
  orbit jewel-dot ring no longer passes behind any front-page paragraph on phone,
  because there is no paragraph there any more.

## DEFECT 2 — FIXED: the wrong red N is gone; the official N is in

His words: *"the red N in the corner that's not our official N. That's not the
one that lights up right?"*

- The old corner N was a **small static PNG red disc, 13,790 B, sha
  `035b1417f1ae5760…`** — it was NOT the agreement's ball. It is gone.
- The new corner N is the **official red N harvested BYTE-FOR-BYTE from the live
  agreement v25** (`EMBED.ball`): **WEBP, 182,452 B, 1600×1600,
  sha256 `2a4b10fdf01360120166090c25d91407541cb0c5d1b3931bae847840ad207069`**,
  data URI copied verbatim from the agreement file (22,953,906 B, sha
  `2c88513f9011b176c0af910ec0d81e314578cfe904dd62ded9010a9a54052e11` = v25,
  re-fetched fresh this round, byte-exact). Alt text harvested verbatim too:
  *"The red N — a raised glass ball with a gold N"*.
- It **lights up and spins**: the corner's existing harvested orbit ring
  (`.ncorner::before`, `eco-spin` 90s linear infinite) spins around it, the red
  hover glow lights it up, and the agreement's **jewel-gloss highlight**
  (`.orb-wrap.jewel .jewel-gloss`, agreement v25 verbatim, selector renamed only
  to `.ncorner-right .ncorner-gloss`) sits on the ball so it reads as raised
  glass, not a flat disc. I did NOT redraw anything — asset, alt text and gloss
  CSS are all harvested verbatim; the only new bytes are the `<span>` that carries
  the harvested gloss and the harvest comment recording the source.
- **Black N bottom-left untouched** — still `EMBED.logo`, JPEG 387,675 B, sha
  `08b753d3e79ff334…` (verified unchanged), still linking to `https://nayanet.app/`.
  The red N's destination stays `https://nayanet.app/agreement`.

## Verified (fresh this round)

- `verify-fix.mjs`: **ALL CHECKS PASS** — right N src == `EMBED.ball` verbatim
  (string-equal + webp sha), left N sha unchanged, visible `<p>` holds only the ⓘ,
  PARAS parses to **13 entries** with [0] the moved sentence verbatim and [1..12]
  identical to R2, final-nine hrefs identical to R2 (9/9), QUESTIONS block
  identical to R2, worker endpoint URLs identical to R2 (staged `complete()` /
  verify / world still point at the staging walk worker — live repoint is his
  hand, later), certificate sha unchanged, all **7 inline scripts `node --check`**.
- `diff` vs R2 staged portal: **exactly 5 hunks, nothing else** — harvest comment,
  gloss CSS line, sentence removal, PARAS[0], right-corner img swap
  (`maker/evidence/portal-diff.txt`).
- Design laws: **portal 81 violations + 4 warnings, identity 3 violations —
  identical counts to the R2 baseline, zero new** (all pre-existing §2.3 sub-17 px
  deck text + §2.2 flags).
- **Render probe** (`maker/evidence/probe.py`, Playwright Chromium via the
  localhost forwarder, fresh new-user view): **phone 390×844 AND desktop 1440×900** —
  sentence not visible on the front page at either width; greeting, input, Enter
  and ⓘ all visible; ⓘ centred (phone x182 y637; desk x707 y538); right N renders
  as WEBP 1600×1600 natural; both corner hrefs correct; **ⓘ tap opens the reader
  with the moved sentence as "1 of 13", Next → "2 of 13"**; no overflow
  (scrollW 390 / 1440, scrollH 844 / 900 — one viewport each). Screenshots:
  `probe-phone-front.png`, `probe-desk-front.png`, `probe-phone-reader.png`,
  `probe-desk-reader.png`. I read the front + reader screenshots with my own eyes:
  clean, centred, the red glass ball with gold N glowing bottom-right.
  - Load noise, stated honestly: **0 HTTP ≥400 responses** on either width. Phone
    had 1 request failure (Google Fonts TLS through the VM proxy — known
    environmental, same as R2). Desktop's background deck fetches hit proxy
    failures (`ERR_PROXY_CONNECTION_FAILED` / `ERR_CONNECTION_CLOSED`, 35 entries)
    while the forwarder degraded mid-run — the portal document and every measured
    element still rendered, and the desktop screenshots prove it; the checker
    should re-confirm the deck census on its own run.
- **No new test certificate was minted.** No test account was created or walked by
  me; the walk spine was not touched (diff proves it). `r2check25` / Nº 884,
  `eyetestnov24` Nº 000876, `spinetest1` Nº 877, `checknov25b` Nº 881,
  `fixnov25a` Nº 883 — all untouched.

## Preserved (R2 pass items — verified, not just claimed)

Returning view premium greeting (white Marcellus, deep-gold name, no green flat
text, no "This is me", Jump back in → Hub) · final nine destinations (hrefs
byte-identical to R2) · certificate (5 jewels, crystal-N seal, framed board —
sha unchanged) · 15-question walk spine (QUESTIONS block identical) · staged
endpoints (unchanged). Diff is 5 hunks; everything else is byte-identical by
construction and by the checks above.

## Still open (named, not hidden — other rounds own them)

1. **Reader-card / orbit-ring overlap on phone:** with the reader open, the orbit
   jewel-dot ring passes behind the reader card's edges (visible in
   `probe-phone-reader.png`). Pre-existing reader behaviour — the ring used to
   cross the paragraph; now it crosses the card instead. The card is bordered
   and the text reads cleanly, so this is an observation, not a defect in this
   round. A polish pass can move the reader clear of the ring.
2. **GAP B + C, hover law, install veil, live-deploy substitutions** — unchanged
   from R2, untouched here (see R2 FIX-REPORT open items).
3. **The ⓘ trigger is a lone dot under the button** on the front page — that is
   what the brief asked for (ⓘ stays as the trigger, no paragraph). If Shawn
   wants it labelled, that is a one-word change for a later round, not this one.

## Design-law §11 check (in writing, changed surfaces only)

- **Five gates:** no money, no credential read/used/stored, no destructive action,
  staging only, everything proven by read-back bytes + real renders. ✅
- **Harvest, never invent:** the N (asset, alt, gloss CSS) is agreement v25
  verbatim; the sentence is Shawn's own words moved, not rewritten; the spin and
  the glow are the corner's own harvested code, already in place. Nothing
  redesigned, nothing rebuilt. ✅
- **Don't touch unasked:** live portal, live agreement, the R2 branch/lane, the
  walkthrough-15 staging worker, the certificate, the nine, the returning view,
  the walk/end screens — all untouched (diff: 5 hunks). ✅
- **Sense check on the page:** a cold stranger now sees name → Enter, nothing
  else, in the middle of the frame — two seconds, one idea. The agreement is one
  tap away behind the ⓘ and the bottom-bar link, never in the way. The corner N
  is the real jewel N, lit and spinning, not a red disc. ✅
- **§2 text:** the removed sentence was 17 px white — no gray, no sub-17 text
  added or removed that changes the law counts (81+4 / 3, identical). The reader
  text is unchanged white 17 px. ✅
- **§1 / §4 objects:** the ball is a real object now — glass, gloss highlight,
  chrome-white ring, red glow, slow orbit — where a flat red disc stood. The
  front page lost a paragraph and gained air; the ring, the arch and the deed
  are untouched. ✅

## Self-scorecard — why it is not a 10

**Score: 8/10.** Both defects are fixed and proven, nothing else moved, and the
page reads clean at both widths. It is not a 10 because: the reader card still
shares space with the orbit ring on phone (observation 1); the walk/end screens
are still plain black outside the frame (R2 observation, another round's job);
the desktop deck fetches flaked through the VM proxy on my run, so my desktop
proof leans on screenshots + DOM rather than a clean network log; and the ⓘ as
a lone dot is correct per the brief but less discoverable than a labelled
trigger — his eye may still want a word next to it.

**Ten things to make it ten times better:**
1. Move the phone reader clear of the orbit ring (or fade the ring while the reader is open).
2. Bring the walk/end screens into the Innovations frame (her picture asking, 15 jewel dots filling).
3. Give the ⓘ a whisper of a label ("About this name ◆") without restoring the wall.
4. Whiten the "Your name" placeholder and the certificate's gray secondary line (eye R2 obs. 3).
5. Re-prove the desktop deck census on a clean proxy run (checker job).
6. Add the 15 jewel dots to the walk progress (text "N of 15" → dots that fill).
7. Make the corner Ns' orbit rings pause on `prefers-reduced-motion` (already) and
   brighten on hover together with the ball (already) — then leave them alone.
8. Put the agreement reader in the same bordered-card language as the certificate
   frame, not a plain dark box.
9. Let "Read the agreement ◆" open the same reader (one inner page, two doors).
10. When this ships live, repoint complete/verify/world at the live worker and
    re-walk r2check25 end to end on the live URL — staged proof is not live proof.
