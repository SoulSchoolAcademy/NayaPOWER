#!/usr/bin/env python3
"""Build the walk S2 staging worker from the S2 files' bytes.
S2 (2026-11-12): completion creates the citizen's Smart Box + the one project
record + the three pages from the walk answers; the Box table is citizen_worlds
(live schema, PK alias, answers jsonb) and the pages table is page_about — the
staging worker's anon key is RLS-blocked from inserting into both (proven
401/42501), so the worker tries the live tables, mirrors the records in KV in
the tables' exact shapes, and the live projects row IS created (anon writes
allowed there). The live-table write waits for the server-side key (his hand).
Original docstring follows. Build the walk-beginning staging worker from the fixed files' bytes.
Worker: naya-walk-beginning-staging. Serves:
  /                         -> the staged welcome entry (welcome-staged.html, v5 dial)
  /welcome                  -> the fixed walk (walk-beginning-fixed.html)
  /identity.html            -> the fixed identity page (identity-fixed.html)
  /login-obsidian.jpg, /naya-logo.png -> the welcome page's assets, from KV
  /naya-a.jpg, /naya-b.jpg, /naya-c.jpg -> the three Naya choice pictures, from KV (QUESTIONS 10/10)
  POST /api/claim         -> Supabase insert + read-back (same-origin claim)
  GET  /api/claim         -> availability / read-back {exists, own, cert_no}
  POST /api/welcome/me    -> {alias, name} from the registry row
  POST /api/welcome/complete -> stores the completion in KV, returns reveal
  GET  /api/welcome/complete?alias= -> read-back of the stored completion
  /<alias>[/business|space|dashboard] -> 302 to the live nayanet.app pages
Asserts the fixed walk + identity shas before building. The registry
credential is read programmatically from the live-extracted identity file
and embedded ONLY in this staging worker (the key is the public anon key
already shipped in the live page; the LIVE splice must hold it as a secret
binding instead — see the record). The key value is never printed.
KV binding: WELCOME_ASSETS (the live nayanet KV namespace) — completions
are stored as complete_<alias> keys, test aliases only.
"""
import hashlib
import json
import re
import sys
_OUT = sys.stdout
if "--stdout" in sys.argv:
    # Stream mode (EPERM-flake workaround): log lines go to stderr, the
    # worker bytes go to the real stdout for piping to cf-worker.py.
    sys.stdout = sys.stderr

ROUND = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114"
FIXROUND = "/home/hatch/workspace/team-nitro/walk-fix-20261111"
WALK = ROUND + "/walk-beginning-fixed.html"
IDENT = ROUND + "/identity-fixed.html"
WELCOME = ROUND + "/welcome-staged.html"
# BRIDGE PAGE (2026-11-17): the official unfold, served verbatim at
# /agreement. Source is the agree-fix round's filed file (blob 41d2c71f,
# 85,625 B, sha 842cae53...), NOT the PR #3404 base (c7b14a98, 85,676 B):
# the fix round changed exactly one line (line 437, agree destination).
# AGREEMENT MERGE (2026-11-17, BRIEF-AGREEMENT-UPDATE-20261117.md): the
# unfold sha moves 842cae53 -> faea2190 (85,679 B) — the agree
# destination changes from the proof-host welcome-staged.html to
# /?stage=bridge on this worker. The landing-fix round (dispatched
# 19:18Z) owns the unfold next.
UNFOLD = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
MIRROR = "/home/hatch/workspace/team-nitro/space-business-mirror-personal-20261112"
TEMPLATE = MIRROR + "/template-composed.html"
LIVE_IDENT = FIXROUND + "/identity-live-extracted.html"
OUT = ROUND + "/walk-beginning-staging-worker.js"

walk_raw = open(WALK, "rb").read()
walk_sha = hashlib.sha256(walk_raw).hexdigest()
ident_raw = open(IDENT, "rb").read()
ident_sha = hashlib.sha256(ident_raw).hexdigest()
welcome_raw = (sys.stdin.buffer.read() if "--welcome-stdin" in sys.argv
               else open(WELCOME, "rb").read())
welcome_sha = hashlib.sha256(welcome_raw).hexdigest()
template_raw = open(TEMPLATE, "rb").read()
template_sha = hashlib.sha256(template_raw).hexdigest()
print(f"walk {len(walk_raw)} B sha {walk_sha}")
print(f"identity {len(ident_raw)} B sha {ident_sha}")
print(f"welcome {len(welcome_raw)} B sha {welcome_sha}")
print(f"personal-template {len(template_raw)} B sha {template_sha}")
unfold_raw = open(UNFOLD, "rb").read()
unfold_sha = hashlib.sha256(unfold_raw).hexdigest()
print(f"unfold {len(unfold_raw)} B sha {unfold_sha}")
# Walk sha reconciled 2026-11-13 (sisters' Personal pages, step 1): the file in
# this dir is the GOLD-FIXED local walk (names-page base a3510446 -> 4e8500c2
# by the identical gold fix). The FILED Q10 walk is be55a494 (Q10 base
# 227a667e -> be55a494 by the same fix); the two differ by 1,344 B because
# their bases differ. v23 (2026-11-14): the assembler chose 4e8500c2 (names + gold)
# over be55a494 (a strict subset — the 69-line names diff is the only delta),
# then merged the Q2 reword (7 lines), the news steps 11-14 verbatim from the
# staged df17ac67 walk, the quote fix (650->700), and the JS renumber 10->14.
# This build asserts the merged v23 walk bytes: faedf1c3.
# v24 (2026-11-14, end rebuild): the walk is the v23 walk + the ONE unfolding
# end (step 16: agreement folds -> world -> hired -> package); sha d329e4b2.
# v24 ADDENDUM (~15:48Z): the agreement words come from the manuscript
# (COLLECTIVE-AGREEMENT-MANUSCRIPT-20261114.md) — cover + eight steps, the
# Wednesday line replaced by Step 6's plain wording, cover bands on the cards.
# v24 ADDENDUM 2 (~16:00Z): agreement words from the v2 manuscript
# (COLLECTIVE-AGREEMENT-MANUSCRIPT-V2-20261114.md) — cover + TEN steps.
# Bugatti line OUT, day-10 line OUT (30-day hold supersedes it), new Steps 7-9
# (skeptic, cap ladder $100-$500, protection). Wednesday still 0.
# v24 ADDENDUM 3 (~16:10Z): ROYAL MANUSCRIPT presentation (ROYAL-MANUSCRIPT-PRESENTATION-20261114.md) — true fold (hinged rotateX), gold frame/seal/ribbon, step rail + re-fold, Step N of 10, touch preview, split-flap ladder, green agree pill + gold seal stamp gating the world reveal. Words still the v2 manuscript (2b: $300-$700).
# v24 ADDENDUM 3b+3c (~16:16Z + ~16:24Z): the cover gains the deed line verbatim; Step 6 gains the ambassador=representative lines verbatim. Order confirmed: deed -> world -> hired -> pricing page.
# v24 ADDENDUM 3d+3e (~16:29Z + ~16:34Z): hue ON the blocks (border + top band + jewel diamond), the Eye top-right + nutshell, nine little eyes with plain-words notes (appendix parsed verbatim), skip scrolls to the agree pill. Words unchanged.
# DEPLOY LAW (learned 16:36Z — see record §3): EVERY put-script MUST carry --meta with the WELCOME_ASSETS KV binding, or the PUT wipes the bindings and /api/welcome/complete 500s (error 1101).
# v24 ADDENDUM 3f (~16:46Z): the WHAT IT IS / WHAT IT IS NOT block in the world reveal, right after the hired doors, before the package button. Shawn's verbatim words (16:44Z). Bugatti now twice on the end: the job popover (3e) + this block — never in the agreement's own words.
# OVERHAUL (~17:24Z): the v24 hinged fold is REPLACED whole — pricing letter flow (append-in-order, Keep reading, read-all-at-once) carrying Hub Intelligent Blocks (hook + cover + 10 steps), a play button per block (walk's own speechSynthesis path, English by default), the 60s generous pricing gateway, Step 2 + wars line (17:17Z), Step 6 + online-resume line. Words still the v2 manuscript, re-parsed at build time.
# WALK-END FIX ROUND (2026-11-14, BRIEF-WALK-END-FIX-20261114.md): the walk is the
# overhaul walk + the six fix items only (hook says what it is, one play kept,
# player honest/visible, display always pro, Smart Box -> Smart Vault, nothing else).
# AGREEMENT v4 (2026-11-14, BRIEF-AGREEMENT-V4-20261114.md): the walk is the
# fix-round walk + the twelve v4 items only (v3 words in her first-person voice,
# a different portrait on every board, royal manuscript, make-it-official,
# definitions, joining-is-the-agreement, no repeats, review presentation shape,
# one player, skip test, verbatim logo, payout-clock question named in record).
# Walk sha 349b6238 (3,450,550 B). Steps 1-15 untouched in behavior. v4c: addendum #4 (no play, no Ready-to-sign, logo in footers, obsidian) + addendum #5 (words scorecard pass, bigger portraits) + run-3 skip-back + overflow fixes.
# WALK-END RE-PRESENTATION ROUND (2026-11-15, BRIEF-WALK-END-REPRESENTATION-20261115.md):
# the walk is the F1-F4 fix walk + the re-presentation only (world leads, white
# only, generic photographic covers, See-a-sample views, ornaments never cover
# text, hero lands whole at 390, pill reads in full). Demo mapping corrected
# per the captain (Shawn 19:30Z): Personal golden-profile-tree, Business
# spaces, Space companion-golden; no Thing demo. Walk sha fc6bb640 (4,415,812 B).
# UNFOLDING ADD-IMAGES (2026-11-15, BRIEF-UNFOLDING-ADD-IMAGES-20261115.md):
# the walk is the re-presentation walk + 7 scene pictures inside the letter
# beats only (beats 19/22/25/27/31/34/81) + the .lb-showcase frame CSS.
# Text byte-identical; diff-proof in MAKER-RECORD-UNFOLDING-ADD-IMAGES-20261115.md.
# Walk sha fc6bb640 (4,415,812 B) -> f7b32bf9 (4,418,252 B).
# WALK-END GRAY FIX (2026-11-15, BRIEF-WALK-END-GRAY-FIX-20261115.md):
# the walk is the unfolding-images walk + ONE line only — .p3-progress color
# rgba(232,232,236,.55) -> #fff (line 82). Nothing else moves; diff-proof in
# MAKER-RECORD-WALK-END-GRAY-FIX-20261115.md. Walk sha f7b32bf9 -> 54b9b4c1
# (4,418,235 B, -17 B). Identity sha untouched (6e4fc905, PROTECT).
# WALK-END AGREEMENT OUT (2026-11-15, BRIEF-WALK-END-AGREEMENT-OUT-20261115.md):
# the agreement letter comes OUT of the end slide (Shawn 22:13Z — it lives on
# the front page now). Removed: the 83-board dealUnfold section + the ambassador
# checkbox + the skip note (letter apparatus). Added: wireLetter early-return
# guard (no letter markup -> return before any null deref, so boot survives),
# showStep(16) reveals endRest (the deeds show on arrival — no skip/agree tap
# exists any more), and the dead door gets its way through (a harvested
# .p3-enter anchor pill in #step-door -> /identity.html). Nothing else moves;
# diff-proof in MAKER-RECORD-WALK-END-AGREEMENT-OUT-20261115.md.
# Walk sha 54b9b4c1 -> c43300e7 (4,418,235 B -> 4,347,247 B, -70,988 B)
# -> 746a5142 (4,347,276 B, +29 B: the door pill is an anchor, and .p3-enter
# never resets the anchor underline — style="text-decoration:none" on the
# anchor itself, so the button reads as a button, not a link).
# IDENTITY NOTE: staged /identity.html serves fa3b2197 (round 2 fixpass,
# deployed after the front-page round landed — the 171eb90c in the dispatch
# brief was stale); the live curl is the source of truth, the local file and
# this assert already agree on fa3b2197, so identity is preserved, not moved.
# FREE WALK -> HUB HANDOFF (2026-11-16, BRIEF-FREE-WALK-HUB-HANDOFF-20261116.md):
# the end slide gains the Hub door (#hubBtn, lead line + .p3-enter anchor
# after the three cards, before "Choose your package") wired in renderEnd()
# to the staged Hub + ?name=&alias=&pricing=1 — Hub FIRST, pricing pops up
# over it once in. Nothing else moves; diff-proof in the handoff maker record.
# Walk sha 746a5142 -> cd4305c5 (4,347,276 B -> 4,348,824 B, +1,548 B).
# Walk sha cd4305c5 -> 2c459891 (4,348,824 B, +0 B: the Hub door's HUB_BASE
# cb moves f8bd1af0 -> 571a9808 — Hub FIX F1, the <head> pricing-signal
# capture. Same length, so the diff is one line and the size does not move).
# WALK END SHARE PLUS (2026-11-16, BRIEF-WALK-END-SHARE-PLUS-20261116.md +
# MAKER-BRIEF-WALK-END-SHARE-PLUS-20261116.md): the end slide gains the
# share plus (obsidian, white glowing circling orb, white plus; menu =
# Mobile via navigator.share when present, Facebook sharer, Email mailto —
# all carrying the citizen's real Smart Link); tap-to-view + See sample go
# to the updated Personal (correction round, proof-host ref=
# personal/correction-20261116, WIRED — LANDING PENDING its filing);
# back buttons on every walk view (17: steps 1-14, names, building, end);
# certificate gains its back button too (item 5) — see identity note below.
# Walk sha 2c459891 -> 33166195 (4,348,828 B -> 4,358,909 B, +10,081 B).
# Walk sha 33166195 -> 681c4866 (4,358,909 B -> 4,359,029 B, +120 B: the
# correction round FILED while this round was in flight (branch
# personal/correction-20261116, head 173fd57d, 16:42:46Z), so the cb pin
# the brief required went on the moment the branch existed — cb=
# 045af4e0005c04c6387601d491334d589b40dc23, the filed blob, verified
# byte-identical from the proof host before the line was written.
# Items 2 & 3 are LANDED, not pending.)
assert walk_sha.startswith("4b5f9264"), "walk sha is not the BRIDGE PRESENTATION walk sha (2026-11-17: Full Custom eye inline-flex, quotes off 18 headings, names-step crests hidden, end-slide VISUAL/READ)"
assert template_sha.startswith("61002d15"), "personal template sha is not the composed template sha (live Personal v9 992ab18c + hero fix + rooms-plus fix)"
# IDENTITY CERTIFICATE ROUND (2026-11-15, BRIEF-IDENTITY-CERTIFICATE-20261115.md):
# the identity sha moved 55fdffa8 -> e9398f75 (gold live name 86px, date truly
# centered + visible at phone widths, install pill + 5s auto-invite retired,
# text wall -> three short lines + unfold, seal/gem ignition on typing)
# -> cc4f5e3c (FIXPASS: compact phone clock, phone panels-shown grid lean,
# ornaments pointer-events none — the 390 verify found the header overlap
# and the unfold pill under the bottom stone)
# -> 6d3692d6 (FIXPASS 2: phone brand title hides; unfold REPLACES the short
# lines + deeper grid lean — the unfolded body clipped the frame at 390 AND
# 1440, and the compact date still overlapped the title at 390).
# -> 6e4fc905 (FIXPASS 3: unfold is a centered pop-up card; the 0.60fr lean
# collided the live name with the jewels + title, so the lean and the
# short-lines-hide are reverted; card closes on tap or Escape).
# IDENTITY CERTIFICATE ROUND 2 (2026-11-15, BRIEF-IDENTITY-CERTIFICATE-ROUND2-20261115.md):
# -> 171eb90c (v2.13 SUPER SPECIAL: green pulsing clock dot, full local clock
# at every width, local stamp, layered engraved name, pure-white text, ONE
# purple, obsidian panels + typing values, ink-centered title/clock, F8
# certified->composing switch, agreement line at the decision moment).
# -> fa3b2197 (v2.13 FIXPASS: certified name left/bottom auto — the relative
# rule had woken the composing left:50%; text-indent 0 — measured off = indent/2).
# IDENTITY CERTIFICATE ROUND 3 (2026-11-16, BRIEF-IDENTITY-CERTIFICATE-ROUND3-20261116.md):
# -> 7517caac (357,879 B): H1 words (Collective Agreement certification,
# Society of NayaNET, signing = entering the name); H2/H3 no overlap ever
# at 390/1440/1920/1851x1009 AND the short heights (the defect is height-
# driven — his 1851x1009 screen is ~790-810 CSS tall once chrome + zoom
# come off); H4 gold out, hero name obsidian + purple glow, harvested from
# the ENTER button; the compact document (<=820px) + the 0-7-0 foot trims +
# the 821-880 desktop band fund the pill and the certified switch.
# IDENTITY CERTIFICATE ROUND 4 (2026-11-16, BRIEF-IDENTITY-CERTIFICATE-ROUND4-20261116.md):
# -> 44801918 (360,793 B): H1 the name as a trophy, Shawn's clone trick
# verbatim ("clone it once... put it behind it") — TWO text layers only:
# front = solid obsidian body, top-lit, sharp 1px white/silver chrome
# stroke; back = the clone (::before, data-text) in royal purple, blurred
# 12px, 2% wider — purple underglow BEHIND, never the fill; hover lights
# the glow + lifts 2px. Beats his own NayaNET_text.png reference (black
# letters + purple outline) by adding the body + chrome. Round 3's purple
# extrusion + lavender top edge retired (they WERE the purple paint);
# the round-4 ::after sheen retired too (third layer; the trick is clone
# ONCE). Paint only — no geometry moves, so the round-3 H2/H3 gaps are
# byte-identical by construction and re-probed to the same numbers.
# IDENTITY CERTIFICATE ROUND 5 (2026-11-16, BRIEF-IDENTITY-CERTIFICATE-ROUND5-20261116.md + Shawn's 02:41Z + 02:59Z amendments):
# -> 1b8fd1d1 (373,856 B): H1 the official sentence VERBATIM, typed face only
# ("...you get the deed to your own world: high-level digital real estate — your personal page, your business, your space — free forever.");
# H2 the ⓘ (clone trick) opens the full contract as a reader — one paragraph at a time, 9 paragraphs, Next/Close/Escape/toggle, zero layout shift;
# H1 amended 02:59Z: the certified face loses the composing line ENTIRELY (agree-cert display:block retired) and the composing line hides in the
# taken state too; H6 the taken message is lit green (#2fe89e, 1.02rem/700, its own highlighted box) and fits whole in the viewport;
# H3 the name's rest glow down a tad (clone 0.55->0.45, halo 0.22->0.18), hover untouched. The pill is funded by the sentence's own measure
# (460->740px, 2 lines at desktop, threshold-tested) + the panels leans + the phone foot trims; name gaps byte-identical to round 4.
# WALK END SHARE PLUS (2026-11-16): item 5 names the certificate among the
# views needing a back button ("from the certificate back to the walk"), and
# the round's own WHAT-MUST-NOT-BE-THERE carves the certificate out for
# exactly that ("untouched except for the back control"). The certificate
# had NO back control at all (verified by grep), so the back control is
# added here and ONLY that: one in-flow row above the plaque
# ("‹ Back to the walk" -> /welcome, obsidian pill in the cert-more
# family) + its CSS. Nothing else in the file moves.
# -> 84e3d3e7 (373,856 B -> 374,938 B, +1,082 B).
# WALK END SHARE PLUS ITEM 11 (2026-11-16, MAKER-BRIEF-WALK-END-SHARE-PLUS-ITEM11-20261116.md):
# the welcome sha moved ee348e7c -> 6a10a1ed (921,988 B -> 924,184 B,
# +2,196 B): the agreement end persists across a refresh — the stage is
# saved to localStorage (nayanet_fp_stage='agree') when render() lands on
# the agree view, read back through the existing resumeTarget() mechanism,
# and restored on load (enterStage + agree view, no deck walk); any other
# view or a stage exit clears the key, so only the end view ever restores.
# The end view itself is byte-identical (agree markup hash unchanged);
# walk, template, identity shas unchanged.
# WALK END FIX — SEAL STAMP / RED ORB / STALE ALIAS NOTE (2026-11-16,
# BRIEF-WALK-END-FIX-SEAL-ORB-NOTE-20261116.md; One List walk-end-share-plus,
# fix cycle — the final checker PASSED 20:11Z, the captain's eye did NOT):
# the welcome sha moves 6a10a1ed -> 5f33d273 (925222 B, +1038 B):
# H14 — the red N seal stamps visibly on EVERY tap of "I agree" (stamp
# restarted, seal scrolled into view, dwell 2000ms, stage exits 1950ms);
# the seal itself is byte-identical to the visual-agreement-end build
# (blob f5fd6448, sha c85e91ce) — markup, seal CSS and stamp code harvested
# verbatim, only its visibility on tap changes. The identity sha moves
# 092001d6 -> 8c641f96 (376814 B, +781 B): the
# taken-alias note clears the moment a fresh alias comes back available
# (setAliasState hides #hubNote on available/own/neutral). Walk + template
# shas unchanged.
assert ident_sha.startswith("a1550164"), "identity sha is not the BRIDGE PRESENTATION identity sha (2026-11-17: certified lean 0.88fr at 600-640px)"
# ENTRANCE WELCOME (2026-11-16, BRIEF-AGREEMENT-ENTRANCE-WELCOME-20261116.md):
# the welcome sha moves 5f33d273 -> db5960eb (925,222 B -> 934,065 B,
# +9,337 B): Item 0 — the opening-view intro block only. Shawn's 10-star
# copy verbatim in order (kicker / "The Collective Agreement" / "Welcome.
# Let's begin with trust."); Naya's portrait beside the welcome
# (/agmt-b06.png — the exact Naya.png bytes, already in KV) + the BIG PLAY
# BUTTON restored beside her picture, harvested verbatim from the live
# walk (.p3-naya-play + orbiting dot + tip, glow-only wiring, voice
# PAUSED). The brief named blob f5fd6448 as the play-button source; that
# blob carries NO play button (verified by grep) — the walk is the one
# place it exists. The welcome unfolds in 9 short .intel-board boards,
# three then a "Continue" button (the legal-pages unfolding law); the
# Royal Unfolding intro is "Nine pictures. One beautiful story." + his
# four lines + sign-off; the buttons read "Begin the visual story" /
# "Read the Collective Agreement" (HTML + updateChrome — the old labels
# are gone everywhere). Items 1+: the "How it works" rail pill retargets
# 44 -> 18 (Q2 beat 18, verified); every other audit item is agreement
# WORDS, blocked while Shawn reads v3 — named in the maker record, not
# done. Deck, letter, agree, login, legal row untouched. Walk, template,
# identity shas unchanged.
# ENTRANCE WELCOME FIX (2026-11-16, maker-eye self-check 3): the welcome
# sha moves db5960eb -> fc546ee8 (934,065 B -> 936,958 B, +2,893 B):
# the pinned choice bar collided with the unfolding boards at 390 and
# 1851 (pick line across board text, buttons over boards 2-3), so the bar
# is hidden in the intro view only and the pick line + the two choice
# buttons live in the intro flow after the Royal Unfolding lines —
# stacked, centred, purple + green, same labels, same handlers
# (goResume / enterLetterPage). The bar buttons stay in the DOM (deck
# end uses nextBtn2). Walk, template, identity shas unchanged.
# ENTRANCE WELCOME FIX 2 (2026-11-16, maker-eye self-check 3): the
# welcome sha moves fc546ee8 -> 170016d7 (936,958 B -> 937,045 B, +87 B):
# the last choice button sat under the legal strip at max scroll (390,
# measured: button bottom = viewport bottom, strip intercepts the tap).
# Root cause: #deckUnfold is flex:1 1 auto + min-height:0, so with the
# long unfolding it shrinks below its content and spills past the
# scrollable area. Scoped to the intro view only, it may not shrink
# (flex:0 0 auto; min-height:auto) — max scroll then leaves the choices
# 118px above the viewport bottom, clear of the strip. Walk, template,
# identity shas unchanged.
# ENTRANCE WELCOME FIX 3 (2026-11-16, checker FAIL line 4 + DEFECT line 10):
# the welcome sha moves 170016d7 -> e27c7fe1 (937,559 B -> 938,546 B,
# +987 B): (1) the portrait sat centred ABOVE the welcome boards at
# 1851px, exactly as on phone — the brief requires it BESIDE the welcome
# on wide screens. The hero + welcome are wrapped in .fp-intro-side; at
# >=1024px (intro view only) the hero (portrait + play, stacked as a
# side column) sits beside the welcome column; below 1024px nothing
# changes — hero stays centred above the boards, as now. Portrait bytes,
# play button, boards, copy untouched. (2) "What we do" rail pill
# data-beat 18 -> 11 (Q1 "What is Naya?" is beat 11); "How it works"
# stays 18 (Q2, correct). Walk, template, identity shas unchanged.
# ENTRANCE + OFFICIAL UNFOLD FIX (2026-11-16/17, BRIEF-ENTRANCE-BRIDGE-FIX-20261116.md + Shawn's 23:04Z letter-layout amendment; second attempt — first attempt built + verified in memory 00:01Z but the EPERM flake blocked the disk write):
# the welcome sha moves e27c7fe1 -> 6dc14953 (938,546 B staged -> 1,101,772 B on disk; 1,101,040 chars):
# (1) play button dead center at the top of the welcome, says Naya, glow-only, CSS byte-identical to the live walk harvest;
# (2) the speaking face beside every speaking board (placeFaces rule), welcome portrait centred on the "Hi, I'm Naya" line;
# (3) the letter rebuilt in the official unfold, 19 -> 34 distilled boards, <=3 sentences each, deck's unfolding harvested verbatim;
# (4) the deck kept as it was, nutshells word-perfect (3 sentences each) from the approved script + 10-star copy;
# (5) the 12 merged legal pages in the official unfold (157 boards + 12 intro boards, 3-then-button groups, footer now links all 12);
# (6) the bridge verified, not moved; agree step and login untouched. Sha 2d213de8 is SUPERSEDED — it silently dropped the letter's in-flow
# end block (letterPageEnd); 6dc14953 restores it byte-identical (+272 B). Walk, template, identity shas unchanged.
# Letter-layout amendment (23:04Z): letter board centered, "Keep reading" just below the board, links at the very bottom, fitBarPadding kills the 390 clipping.
# ENTRANCE + OFFICIAL UNFOLD FIX ROUND (2026-11-17, BRIEF-ENTRANCE-FIX-20261117.md; the second attempt's probe FAILED all four defects, this round fixes them at the root):
# the welcome sha moves 6dc14953 -> aba6e440 (1,101,772 B -> 1,104,861 B on disk; 1,104,111 chars):
# (1) LEGAL PAGES OPEN: the intro-strip tap landed in the footer view, where the panel stays display:none (only the legal view shows a panel) — all 12 links were dead. The tap now lands IN the legal view with the last revealed beat of group 0, exactly as derive() does from the footer; Close returns to the footer list.
# (2) STALE FACES: placeFaces moves each photo out of its board, so the next run's board.querySelector found nothing and stale faces were never hidden (deck 9 showed all nine). Moved faces are now tagged data-fp-face and re-found; every beat change (deck/letter show(), legal open/close) re-runs placeFaces.
# (3) PLAY CENTERED AT 1851: Fix-3's >=1024px rule (margin:0) left the 860px hero in a left column, play 495px off the welcome's centre. The hero rule now uses Fix-3's own selector, later in the sheet, with margin:0 auto. The play button's own bytes are untouched.
# (4) DECK BEAT 1 FACE: the face kept its first-computed pre-font position (118px below the speaking line at 390) because it could never be re-found; with data-fp-face tracking the fonts.ready / load / render re-runs re-position it on the first <p>'s centre. Walk, template, identity shas unchanged.
# ENTRANCE FIX ROUND 2 (2026-11-17, same day — checker verdict NOT PASS on round 3: two defects):
# the welcome sha moves e3a9a3a2 -> 9f4edba0 (1,106,285 B -> 1,109,267 B on disk; 1,108,495 chars):
# Defect A — the letter-end agree path exited to login 1950ms after "I agree" even when the citizen tapped
# "The whole deal" in the agree view (the exit timer was fire-and-forget, pre-existing in base e27c7fe1);
# the timer is now stored and cancelled on any navigation out of the agree view (whole-deal / back-to-agreement /
# back-to-opening / back-to-deck-end mirrors + the Login exit). The short path (footer -> Back to the agreement)
# never arms a timer and is unchanged. Defect B — the legal face sat on board 1, 162px below the intro's line,
# covering board 1's opening words on every legal page: the intro board was crushed by the legal body's flex
# shrink (overflow:hidden -> automatic minimum size 0), and the face kept the base 104px !important size at phone
# widths because it stays under the .fp-now panel; the intro now keeps its natural height (flex:0 0 auto), the
# legal face is capped to the same 64px/104px as every other speaking face (later + one class more specific, so it
# beats both base !important rules), and the placement clamps the face into the intro board's own band as a
# backstop so it can never sit on board 1. Walk, template, identity shas unchanged.
# ENTRANCE FIX ROUND 2b (2026-11-17, same day — Defect C, found while proving Defect B):
# the welcome sha moves 8e26522a -> 617c550b (1,113,351 B -> 1,114,623 B on disk; 1,113,831 chars):
# Defect C — a re-opened legal page was stuck at beat 0 with a dead "Keep reading": the panel's group
# index (gidx) was never reset, and render() re-hides every beat of a non-current panel, so a second
# open set S.legal=0 while the internal Next was already exhausted — a no-op forever (proven live:
# privacy read to the end, terms opened, privacy re-opened -> 15 Next clicks, still "Keep reading").
# The panel is now restored to its entry state (group 0 shown, gidx=1, Next/All back, dots reset) on
# every close and every open, so every entry behaves exactly like the first. Defects A + B and the
# item-10 amendment untouched (verify checks 16-20 still pass; new check 21 covers the reset).
# ENTRANCE FIX ROUND 3 AMENDMENT (2026-11-17, same day — item 10, face settle):
# the welcome sha moves 617c550b -> f93c52c1 (1,114,623 B -> 1,116,556 B on disk; 1,115,750 chars):
# letter boards 21/45/58 sat exactly -3.0px off the speaking line at 1851, stable to 4s and
# identical across runs, while a manual re-run lands exactly on it — the 650ms settle fires while
# the speaking line is still moving (the dial-in easing tail runs past it; the line's last move
# lands ~800ms). A second settle pass now runs at 900ms, and the board's dial/slide animations
# re-place faces the moment they actually end (animationend). Defects A + B + C and the item-10
# gap/unit amendment untouched (verify checks 16-21 still pass; new check 22 covers the fix).
# BRIDGE PAGE FIX (2026-11-17, BRIEF-BRIDGE-PAGE-FIX-20261117.md; maker fix round —
# deterministic from welcome-new.html dce5e9fc via
# bridge-page-fix-20261117/build-bridge-fix.py, 41/41 checks):
# the welcome sha moves 1dd5b88e -> 395794a3 (1,127,402 B -> 1,129,270 B,
# +1,868 B): the deck-end back is the deck's own control (#fpDeckBack, the
# 4th S.view='bridge' landing) and render() saves 'bridge' while in the
# deck, so browser-back from /agreement after the deck path lands on the
# bridge, the same as the READ path; four corner geos (the agreement
# page's own .ldot jewels) at the four corners of the bridge top title
# block; the stale S.view='intro' comment fixed. Layout, the nine, the
# wiring, the legal pages, the unfold and the laws are untouched.
# Walk, template, identity, unfold shas unchanged.
# AGREEMENT MERGE (2026-11-17, BRIEF-AGREEMENT-UPDATE-20261117.md; maker
# round — deterministic from the bridge bytes 9eea1703 via
# agreement-update-20261117/work/edit-merge.py):
# the welcome sha moves 9eea1703 -> 8aad1e5c (1,132,653 B -> 1,133,238 B,
# +585 B): the two agreement pages merge into ONE at the root — the intro
# welcome boards are gone from the choice view (their byte-identical copy
# lives on in #fpBridge, so the citizen reads them once, on the bridge,
# not twice); the portrait moves into the hero above the play button;
# the Royal Unfolding header/lines hide in intro view only; stage entry
# defaults to the intro (choice) view (?stage=bridge + bridge resume
# still land on the bridge); intro READ + the intro next button go to
# /agreement (one letter destination); 'Back to the login' leaves the
# fixed bar for two in-flow buttons (bridge final + footer), so it never
# covers the twelve legal links; choice pills render 17px at phone
# widths; phone fit trims at <=640px (layer pad 118->80, deckUnfold
# margins) so the choice fits one screen at 390x844. R10 (found by
# verification, not the brief): one stray '}' in the returning-citizen
# script (block 1) closed the line-220 try with no catch and killed the
# whole block in the browser — deleted, all three script blocks parse.
# The unfold sha moves 842cae53 -> faea2190 (85,625 B -> 85,679 B, +54 B):
# the agree button's destination changes from the proof-host
# welcome-staged.html to /?stage=bridge on this worker — the proof host
# is never a destination. Walk, template, identity shas unchanged.
# AGREEMENT MERGE EYE FOLLOW-ON (2026-11-17, BRIEF-AGREEMENT-MERGE-EYE-FOLLOWON-20261117.md
# + bridge fix #2 amendment; maker round — agreement-merge-eye-followon-20261117/work/
# edit-followon.py + edit-followon2.py + edit-followon3.py):
# the welcome sha moves 8aad1e5c -> c8f0df54 (1,133,238 B -> 1,140,854 B,
# +7,616 B): F1 first load shows the clean choice (the 'bridge' localStorage
# save + auto-restore are gone — only 'agree' is ever saved/restored, ITEM 11);
# F2 every button visibly presses in while held (depress + dim + shadow collapse,
# spring back on release, incl. the NAYA play control); F3 choice rims go DEEP
# purple #8e24aa / deep green #07925f (deck-end pills + Keep reading, button-scoped);
# F4 all twelve legal buttons open their legal text in-page (ungated handler +
# bridge return); F5 title clear of the corner emblems (harvested bridge fix #2
# D3: top emblems up to -76px/-56px, measured 10-12px clear, 0 overlap). D1-D4
# carried from bridge-presentation-fix2-20261117 (blob 36b0eaa6, sha b1d4b16d):
# D1 stray '}' already present via the merge R10 (same deletion); D2 the
# _fpRestoreStage guard carried verbatim in mechanism, agree-only per F1;
# D3/D4 carried verbatim (emblem lift + legal-strip one-row, wrap override
# deleted). The 13px final-vs-bar overlap at 635/390 is pre-existing (fix2
# checker: lifts/padding/final layout byte-identical to base; bar hidden at
# max scroll) — not redesigned. Button labels UNCHANGED (named per arrival in
# the maker report). Walk, template, identity shas unchanged.
# The unfold sha moves faea2190 -> 87fa3fa4 (85,679 B -> 87,076 B, +1,397 B):
# the /agreement play control gets a base transition so its press/release
# animates instead of snapping (part 2); the rest is the merged unfold bytes.
assert welcome_sha.startswith("c8f0df54"), "welcome sha is not the AGREEMENT MERGE EYE FOLLOW-ON welcome sha (2026-11-17: F1 clean-choice first load, F2 visible press-in, F3 deep rims, F4 twelve legal unfolds, F5/D3 emblem clearance, D1-D4 carried from fix2)"
assert unfold_sha.startswith("87fa3fa4"), "unfold sha is not the AGREEMENT MERGE EYE FOLLOW-ON unfold sha (2026-11-17: /agreement play-button press transition, 87,076 B)"
# WALK END SHARE PLUS FIX (2026-11-16, MAKER-BRIEF-WALK-END-SHARE-PLUS-FIX-20261116.md; checker NOT PASS 18:50Z):
# the welcome sha moved 62f691b4 -> ee348e7c (919,910 B -> 921,988 B,
# +2,078 B): H8 — the intro legal links keep their natural one-line width
# (flex:0 0 auto + white-space:nowrap, intro view only), so the strip is
# 54px tall at every width and clears the opening buttons by 18px; H13a —
# the orb fade fires 1500ms after a beat renders (the dial-in is done by
# ~700ms), because the nutshell never scrolls and the old scrollTop
# trigger could never fire; sense-check — the last-beat in-flow end block
# hides in stage (its agree + back buttons duplicate the bar's mirror +
# stage link, identical handlers). The identity sha moved 84e3d3e7 ->
# 092001d6 (374,938 B -> 376,033 B, +1,095 B): H10 — in the taken state
# only, the certificate card scrolls (overflow-y:auto) and the taken
# note scrolls itself into view, so its last line is never cut at short
# heights. Walk + template shas unchanged.
# WALK END SHARE PLUS ITEM 10 CORRECTED (2026-11-16, MAKER-BRIEF-WALK-END-SHARE-PLUS-ITEM10-CORRECTED-20261116.md):
# the welcome sha moved 4e931985 -> 62f691b4 (905,927 B -> 919,910 B,
# +13,983 B): the letter presents like the deck — the deck's unfolding
# harvested verbatim (wireLetterUnfold = wireDeck's handler, beats list +
# dots indexing only; per-beat .deck-next buttons; mirror button clicks
# them), the 86-beat stacked scroll GONE from the letter path, the whole
# letter centered and aligned (one centered column: picture first — order:-1
# pulls it above the title on beats 11/25, which carry title-first in the
# source — text in a 640px centered column, blue diamond orb centered below
# the text fading to 0 past 24px of scroll), and distilled to its essence:
# 19 beats, each one official beat's words whole, never rewritten; the full
# 86-beat letter stays intact one tap away ("read the whole letter at
# once", plainLetterText untouched). Walk, template, identity shas unchanged.
# VISUAL COLLECTIVE AGREEMENT END (2026-11-16, BRIEF-VISUAL-COLLECTIVE-AGREEMENT-END-20261116.md + Shawn's 03:13Z + 03:17Z amendments):
# the welcome sha moved 88bcd18b -> c85e91ce (891,262 B -> 897,595 B, +6,333 B).
# Walk, template, identity shas unchanged (identity staged 1b8fd1d1; the local
# identity-fixed.html agrees, so no backup dance this round).
# WALK END SHARE PLUS (2026-11-16, BRIEF-WALK-END-SHARE-PLUS-20261116.md):
# the welcome sha moved c85e91ce -> 4e931985 (897,595 B -> 905,927 B,
# +8,332 B): mirror buttons bigger (single 16px 46px/15px -> 20px 48px/18px;
# two-button 16px 12px/14px -> 20px 14px/16px, min-height 64px; <=480px 18px
# 10px/15px, min-height 60px); opening buttons into the middle (stacked,
# purple #a06bff / green #2fe89e) above a legal strip at the very bottom
# (intro view only; #fpLegal content byte-identical); deck show-all removed
# entirely (button, stage link, handler, S.all==='deck' paths — zero refs);
# back on every front view (deck/letter -> opening, letterPage/agree ->
# deck end 9/9, enter-name -> deck end via __fpDeckEndReturn); X on every
# "Also on this device" row with warning + confirm, removal persisted in
# nayanet_smart_identities. Template sha unchanged (61002d15).
# FRONT-PAGE UNFOLDING FIX (2026-11-16, BRIEF-FRONT-PAGE-UNFOLDING-FIX-20261115.md):
# the welcome sha moved 7991dc64 -> 88bcd18b (889,972 B -> 891,262 B, +1,290 B).
# Walk, template, identity shas unchanged (identity staged 44801918; the local
# identity-fixed.html was the round-5 in-flight 56a53807 at build time, so the
# build used the STAGED 44801918 bytes and restored the local file after).
# FRONT-PAGE UNFOLDING (2026-11-16, BRIEF-FRONT-PAGE-UNFOLDING-20261115.md):
# the welcome sha moved 0909c3d0 -> 7991dc64 (889,972 B). Walk, template,
# identity shas unchanged.
# FRONT-PAGE AGREEMENT v2 (2026-11-15, 22:28Z addendum): the welcome sha moved
# 3d6fd2c9 -> 0909c3d0 (854,847 B). Walk, template shas unchanged. Identity
# still staged 171eb90c (re-curled before this build); local identity-fixed.html
# still round 2's in-flight fa3b2197, so the build again used the STAGED
# 171eb90c bytes and restored the local file after.
# FRONT-PAGE AGREEMENT (2026-11-15, BRIEF-FRONT-PAGE-AGREEMENT-20261115.md + legal footer):
# the welcome sha moved f5ed6343 -> 3d6fd2c9 (853,681 B). Walk, template shas
# unchanged. Identity: round 2 deployed 171eb90c to staging WHILE this round
# built (staged /identity.html re-curled 22:2xZ: 326,013 B, sha 171eb90c); the
# local identity-fixed.html at build time was round 2's still-moving fa3b2197
# (326,004 B), so this build used the STAGED 171eb90c bytes, pulled by curl —
# never the stale 6e4fc905, never the in-flight local file (backed up as
# identity-fixed-round2-inflight-fa3b2197.html and restored after the build).
# ENTRANCE TEXT FIX (2026-11-15, BRIEF-WALK-ENTRANCE-TEXT-FIX-20261115.md):
# the welcome sha moved 51b42b87 -> 83e79855 (white lit pill, white label,
# coloured account blocks) -> 54662010 (maker eye round 2: stack shortened
# so two rows fit the dial's circle at 390) -> f5ed6343 (maker eye round 3:
# phone list cap 68px so the presence line is never cut by the ring with
# 4+ accounts; desktop cap 132px). Walk, identity, template shas unchanged.

live = open(LIVE_IDENT, encoding="utf-8").read()
m = re.search(r"var SB_ANON_KEY = '([^']+)';", live)
assert m, "registry key not found in live-extracted identity"
sb_key = m.group(1)
assert sb_key.startswith("eyJ"), "key shape unexpected"
print("registry key read programmatically (value not printed)")

walk = walk_raw.decode("utf-8")
ident = ident_raw.decode("utf-8")
welcome = welcome_raw.decode("utf-8")
personal = template_raw.decode("utf-8")
unfold = unfold_raw.decode("utf-8")

worker = r"""const WALK = __WALK__;
const IDENTITY = __IDENTITY__;
const WELCOME = __WELCOME__;
const UNFOLD = __UNFOLD__;
const PERSONAL_TEMPLATE = __PERSONAL__;
const SB_URL = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities";
const SB_KEY = __SBKEY__;
const SB_BASE = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1";
const SB_PROJECTS = SB_BASE + "/projects";
const SB_WORLDS = SB_BASE + "/citizen_worlds";
const SB_PAGES = SB_BASE + "/page_about";
const BOX_TABLE = "citizen_worlds"; /* Box record table, live schema: PK alias, answers jsonb, topics, settings jsonb */
const PAGE_TABLE = "page_about"; /* page record table, live schema: page_kind, page_alias, owner_alias, headline, body */
const PROJECT_TABLE = "projects"; /* the one project record, live schema: owner_alias, name, motto */
/* v23 (2026-11-14): the four news keys ride the allowlist so the carried-forward
   news steps 11-14 persist to the Box + the KV completion record. Before v23
   no worker ever stored them (the ten-key allowlist dropped them server-side
   even though the walk sent them); the news answers vanished. Additive only:
   the ten keys, the page bodies and the renderer are untouched. */
const ANSWER_KEYS = ["about", "into", "vision", "mission", "motto", "goal", "biz_do", "biz_offer", "biz_building", "space", "news_local", "news_global", "news_province", "news_create_anywhere"];

const JSONH = { "content-type": "application/json" };
function j(obj, status) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: JSONH });
}
function sbHeaders() {
  return { "apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY, "Content-Type": "application/json" };
}
async function sbGetRow(alias) {
  const r = await fetch(SB_URL + "?alias=eq." + encodeURIComponent(alias)
    + "&select=alias,name,device_key,cert_no,created_at", { headers: sbHeaders() });
  if (!r.ok) return null;
  const rows = await r.json().catch(() => null);
  return (rows && rows.length) ? rows[0] : null;
}
function cleanAlias(a) {
  return String(a || "").trim().toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 32);
}
function slug(s, fb) {
  return String(s || "").trim().toLowerCase().replace(/[^a-z0-9\s-]/g, "")
    .replace(/[\s_]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "") || fb;
}
async function sbReq(method, url, body, prefer) {
  const h = sbHeaders();
  if (prefer) h["Prefer"] = prefer;
  let r;
  try {
    r = await fetch(url, { method, headers: h, body: body ? JSON.stringify(body) : undefined });
  } catch (e) { return { ok: false, status: 0, error: "fetch failed: " + String((e && e.message) || e) }; }
  const txt = await r.text().catch(() => "");
  let data = null;
  try { data = txt ? JSON.parse(txt) : null; } catch (e) { data = txt; }
  if (!r.ok) return { ok: false, status: r.status, error: (data && data.message) || String(txt).slice(0, 160) };
  return { ok: true, status: r.status, data };
}
async function sbRows(table, query) {
  const r = await sbReq("GET", SB_BASE + "/" + table + "?" + query);
  return (r.ok && Array.isArray(r.data)) ? r.data : [];
}
/* ---- JOIN ATTRIBUTION (back-end round 20261112, JOIN-ATTRIBUTION.md steps 1-5) ----
   The join moment is the claim: the alias is first known here. The worker
   reads the naya_sl cookie the Smart Link redirect set (first-party on the
   domain the citizen joined from), resolves the link, and inserts ONE row
   into smart_link_joins. Dedupe: at most one join per (link, joined_alias),
   checked before insert; the table intentionally carries no unique
   constraint, so this flow owns the identity moment. Uses the existing anon
   INSERT grant on smart_link_joins and the anon SELECT on smart_links
   (active rows only) — no new grant, no new table, no schema change. No
   query parameter is ever appended to a redirect target; the cookie is the
   carrier, by design. Ambassador case: the claim body carries no invite
   code and the invites table carries no smart_link_name column, so the
   cross-device fallback is NOT built here — that is the invite step's call,
   named honestly, never a default link assumed. A join is recorded ONLY on
   a successful claim; a failed claim, or an alias taken by another device,
   records nothing. The result rides in the claim response as `join`, so the
   claim proves its own attribution. */
const SL_NAME_RE = /^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/;
const SB_LINKS = SB_BASE + "/smart_links";
const SB_JOINS = SB_BASE + "/smart_link_joins";
function slNameFromCookie(cookieHeader) {
  const m = String(cookieHeader || "").match(/(?:^|;\s*)naya_sl=([^;]+)/);
  if (!m) return null;
  let name = "";
  try { name = decodeURIComponent(m[1]).split(".")[0]; } catch (e) { return null; }
  return SL_NAME_RE.test(name) ? name : null;
}
async function recordJoin(req, alias) {
  const name = slNameFromCookie(req.headers.get("Cookie"));
  if (!name) return { attributed: false, reason: "no naya_sl cookie" };
  const links = await sbRows("smart_links", "name=eq." + encodeURIComponent(name) + "&active=is.true&select=id&limit=1");
  if (!links.length) return { attributed: false, reason: "link not found", link_name: name };
  const linkId = links[0].id;
  const ex = await sbRows("smart_link_joins", "link_id=eq." + encodeURIComponent(linkId) + "&joined_alias=eq." + encodeURIComponent(alias) + "&select=id&limit=1");
  if (ex.length) return { attributed: false, reason: "duplicate", link_id: linkId, link_name: name, already: true };
  const ins = await sbReq("POST", SB_JOINS + "?select=id",
    { link_id: linkId, joined_alias: alias, invite_code: null, source: "cookie" }, "return=representation");
  if (!ins.ok) return { attributed: false, reason: "insert refused", link_id: linkId, link_name: name, error: ins.error || ("status " + ins.status) };
  return { attributed: true, link_id: linkId, link_name: name };
}
function esc(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
/* Pages from the Box: each page's body is the citizen's own words, in the
   smart-note ## sections in order (nutshell, why it matters, what it means,
   how to apply it, what's in it for you). A section appears only when it has
   distinct words of its own — nothing duplicated, nothing invented. */
function pageBody(kind, a) {
  const out = [];
  const seen = {};
  function sec(title, text) {
    const t = String(text || "").trim();
    if (!t || seen[t]) return;
    seen[t] = true;
    out.push("## " + title + "\n" + t + "\n");
  }
  if (kind === "personal") {
    sec("Nutshell", a.about);
    sec("Why it matters", a.into);
    sec("What it means", a.vision);
    sec("How to apply it", [a.mission, a.goal].filter(Boolean).join("\n"));
    sec("What's in it for you", a.motto);
  } else if (kind === "business") {
    sec("Nutshell", a.biz_do);
    sec("Why it matters", a.biz_offer);
    sec("What it means", a.biz_building);
    /* S2 (addendum 5) — vision runs through all three pages: the thread. */
    sec("The vision", a.vision);
    sec("How to apply it", a.mission);
  } else {
    sec("Nutshell", a.space);
    sec("Why it matters", a.into);
    sec("What it means", a.vision);
    /* S2 (addendum 5) — mission runs through all three pages: the thread. */
    sec("The mission", a.mission);
    sec("What's in it for you", a.motto);
  }
  return out.join("\n") || "## Nutshell\nYour words will appear here as you add them in the walk.\n";
}
function composePages(answers, pn) {
  return ["personal", "business", "space"].map(function(kind) {
    return { kind, headline: (pn[kind] && pn[kind].title) || "",
      page_alias: (pn[kind] && pn[kind].slug) || kind,
      body: pageBody(kind, answers) };
  });
}
/* SISTERS' PERSONAL PAGES (2026-11-13) — the narrow card renderer is DELETED.
   A citizen's page IS the Personal page. The template is live Personal v9
   (sha 992ab18c) + the hero fix + the rooms-plus fix, harvested byte for
   byte (template-composed.html, sha 61002d15). Only the citizen's labels
   are swapped in, each with a counted assertion — a failed count throws
   and the request 500s, never serves a half-swapped page. Nothing is
   invented: cover, photo, pills, buttons, feed, composer, bottom bar all
   arrive inside the template. Personal says "My Story", Business and Space
   say "Our Story" (the template's own page-kind mechanism). */
const PERSONAL_STORY = "Shawn Vibert builds NayaNET — the intelligent layer of the internet, where intelligence compounds and everybody wins. This is his personal world: his feed, his messages, his invites, his reports and intel, all working, all live. Welcome to the new world. Welcome to the new net.";
const PERSONAL_TAG = "Welcome to my world — make a post on my feed, send a message, make yourself at home";
function escJs(s) {
  return String(s == null ? "" : s).replace(/\\/g, "\\\\").replace(/'/g, "\\'").replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/</g, "\\u003c");
}
function swapCounted(t, old, nw, expect, label) {
  const parts = t.split(old);
  if (parts.length - 1 !== expect) throw new Error("personal-render swap failed: " + label + " expected " + expect + " found " + (parts.length - 1));
  return parts.join(nw);
}
function swapSplit(t, old, vals, markers, label) {
  /* Context-aware swap: the same string sits in HTML text AND in JS
     single-quoted literals (demo-persona migrations), and the citizen's
     words carry apostrophes — each occurrence gets the escaping its
     context needs. markers[i] must sit just before occurrence i, or the
     template moved and we throw instead of serving a broken page. */
  const parts = t.split(old);
  if (parts.length - 1 !== vals.length) throw new Error("personal-render swap failed: " + label + " expected " + vals.length + " found " + (parts.length - 1));
  for (let i = 0; i < markers.length; i++) {
    if (parts[i].indexOf(markers[i]) < 0) throw new Error("personal-render swap failed: " + label + " context " + i + " moved");
  }
  let out = parts[0];
  for (let i = 0; i < vals.length; i++) out += vals[i] + parts[i + 1];
  return out;
}
function secText(body, title) {
  /* Fallback when the Box is missing: read a ## section out of the composed
     pageBody the completion flow wrote. */
  const parts = String(body || "").split(/^## /m);
  for (let i = 0; i < parts.length; i++) {
    const nl = parts[i].indexOf("\n");
    const h = (nl >= 0 ? parts[i].slice(0, nl) : parts[i]).trim();
    if (h === title) return (nl >= 0 ? parts[i].slice(nl + 1) : "").trim();
  }
  return "";
}
function pageHtml(alias, pg, box) {
  /* S2 fix — the KV mirror stores the TABLE shape (page_kind), the composed
     record uses kind. Resolve both, or every page renders as YOUR SPACE. */
  const k = pg.page_kind || pg.kind || "personal";
  const a = (box && box.answers) || {};
  const headline = pg.headline || (box && box.name) || alias;
  const name = (box && box.name) || headline;
  const story = k === "personal" ? (a.about || secText(pg.body, "Nutshell"))
    : k === "business" ? [a.biz_do, a.biz_offer, a.biz_building].filter(Boolean).join(" ")
    : (a.space || secText(pg.body, "Nutshell"));
  const tagline = k === "business" ? (a.biz_offer || secText(pg.body, "Why it matters"))
    : (a.into || secText(pg.body, "Why it matters"));
  const vision = a.vision || "";
  const mission = a.mission || "";
  const goal = a.goal || "";
  const motto = a.motto || "";
  const whatido = a.biz_do || "";
  const initial = (String(name || alias).trim().charAt(0) || "N").toUpperCase();
  let t = PERSONAL_TEMPLATE;
  t = swapCounted(t, "<title>Shawn Vibert</title>", "<title>" + esc(headline) + "</title>", 1, "title-tag");
  t = swapCounted(t, ">Shawn Vibert</div>", ">" + esc(headline) + "</div>", 1, "pname");
  t = swapCounted(t, 'class="os-owner-name">Shawn Vibert</span>', 'class="os-owner-name">' + esc(headline) + "</span>", 1, "owner-name");
  t = swapCounted(t, "localStorage.setItem('naya.name','Shawn Vibert')", "localStorage.setItem('naya.name','" + escJs(name) + "')", 1, "name-migration-set");
  t = swapCounted(t, "pn.textContent='Shawn Vibert'", "pn.textContent='" + escJs(name) + "'", 1, "name-migration-text");
  t = swapCounted(t, "Memberships \\u2014 Shawn Vibert", "Memberships \\u2014 " + escJs(headline), 1, "memberships-doc");
  t = swapSplit(t, PERSONAL_STORY, [esc(story), esc(story), escJs(story), escJs(story)],
    ['id="abouttext">', 'id="os-story-text" style="margin:0;">', "localStorage.setItem('naya.about','", "at.textContent='"], "story");
  t = swapSplit(t, PERSONAL_TAG + ".", [esc(tagline), escJs(tagline), escJs(tagline)],
    ['id="ptag" title="Click to edit">', "localStorage.setItem('naya.tag','", "pt.textContent='"], "tagline");
  t = swapCounted(t, "Shawn&rsquo;s Smart Notes", esc(name) + "&rsquo;s Smart Notes", 1, "feed-smart");
  t = swapCounted(t, "Shawn&rsquo;s Naya Notes", esc(name) + "&rsquo;s Naya Notes", 1, "feed-naya");
  /* FEED SHARPENING (Shawn 2026-11-13 ~04:34Z; supersedes the brief's §6
     "Activity" wording AND the old feed-activity swap below it, which
     invented an "Our Activity" label the template never produces — the
     template has "Our Activity" x0 and no runtime feed relabel; only the
     story relabels My->Our. The third feed tab is the PUBLIC FEED (the
     world feed), never "Activity". The system is the Personal template's
     feed harvested verbatim; only the visible labels change (his words:
     "take that EXACT system ... and just change some of the labels").
     Internal wiring (ids, data-mw-tab, data-v) stays — it is invisible,
     and the course code reads the tab label from the DOM, so the swap
     flows through. The notif-bar "Activity" chip, the bottom-bar
     "Activity" menu item and the Stats "Activity mix" donut are NOT the
     feed tab; they stay as the template carries them. */
  t = swapCounted(t, ">My Activity — tap for the full dashboard ↓</button>", ">Public Feed — tap for the full feed ↓</button>", 1, "feed-name-public");
  t = swapCounted(t, "id=\"mwTabActivity\" data-mw-tab=\"activity\" role=\"tab\" aria-selected=\"false\"><b>Activity</b></button>", "id=\"mwTabActivity\" data-mw-tab=\"activity\" role=\"tab\" aria-selected=\"false\"><b>Public Feed</b></button>", 1, "feed-tab-public");
  t = swapCounted(t, "<button type=\"button\" data-v=\"activity\">Activity</button>", "<button type=\"button\" data-v=\"activity\">Public Feed</button>", 1, "feed-default-public");
  t = swapCounted(t, "middle%22%3EN%3C/text", "middle%22%3E" + initial + "%3C/text", 1, "avatar-letter");
  /* Avatar stroke stays #a06bff — the template's own color. No per-citizen
     color exists in the Box; the initial orb is the default by law. */
  t = swapCounted(t, "var baUser='Shawn'", "var baUser='" + escJs(name) + "'", 1, "smartname-bauser");
  t = swapCounted(t, "||'Shawn'", "||'" + escJs(name) + "'", 1, "smartname-fallback1");
  t = swapCounted(t, "|| 'Shawn'", "|| '" + escJs(name) + "'", 1, "smartname-fallback2");
  t = swapCounted(t, "return 'Shawn'", "return '" + escJs(name) + "'", 1, "smartname-fallback3");
  t = swapCounted(t, "flagship-personal", alias, 7, "page-alias-literals");
  t = swapCounted(t, "window.MSHIP_PAGE_KIND='personal'", "window.MSHIP_PAGE_KIND='" + k + "'", 1, "page-kind");
  t = swapCounted(t, "(typeof PAGE_ALIAS !== 'undefined' ? PAGE_ALIAS : 'flagship-community')", "(typeof PAGE_ALIAS !== 'undefined' ? PAGE_ALIAS : '" + alias + "')", 1, "injector-fallback-alias");
  if (vision) t = swapCounted(t, ">A world where intelligence compounds and everybody wins.</p>", ">" + esc(vision) + "</p>", 1, "sec-vision");
  if (mission) t = swapCounted(t, ">Build NayaNET — the intelligent highway for the AI age.</p>", ">" + esc(mission) + "</p>", 1, "sec-mission");
  if (goal) t = swapCounted(t, ">One million citizens by 2027.</p>", ">" + esc(goal) + "</p>", 1, "sec-goals");
  if (whatido) t = swapCounted(t, ">No what-I-do yet &mdash; tap Edit and say what you do, in one line.</p>", ">" + esc(whatido) + "</p>", 1, "sec-whatido");
  /* Purpose keeps the template's honest empty state: no walk question asks
     for a purpose, and live Personal shows the same prompt. */
  if (motto) {
    t = swapCounted(t, 'id="os-sec-motto-text" class="os-note" style="margin:0;"></p>', 'id="os-sec-motto-text" style="margin:0;">' + esc(motto) + "</p>", 1, "sec-motto");
    /* FIX-7 paints "No motto yet" over the static motto unless
       __osAboutSecs['motto'] is defined when the read resolves — seed it
       through the page's own variable, before the main script runs.
       ANCHOR LAW (fix, 2026-11-13 — the first version used
       lastIndexOf("<script") before loadAbout and landed INSIDE the main
       script block: the F5 comment in that block contains a literal
       "<script>" string, so the seed split the block in two and the whole
       main script died with 'unterminated comment' + "unexpected token:
       keyword 'this'" (2 pageerrors, feed never painted, motto never
       seeded). Anchor on the main block's own id tag instead, and assert
       the text before it ends with </script> — between blocks, never
       inside one. */
    const si = t.indexOf('<script id="os-script">');
    if (si < 0) throw new Error("personal-render: os-script tag not found");
    if (t.indexOf('<script id="os-script">', si + 1) >= 0) throw new Error("personal-render: os-script tag not unique");
    if (!t.slice(0, si).replace(/\s+$/, "").endsWith("</script>")) throw new Error("personal-render: os-script tag is not between blocks");
    t = t.slice(0, si) + '<script>window.__osAboutSecs=window.__osAboutSecs||{};window.__osAboutSecs["motto"]=' + JSON.stringify(motto).replace(/</g, "\\u003c") + ";</script>\n" + t.slice(si);
  }
  return t;
}
function hubHtml(alias, name, cards) {
  const defs = { personal: ["#a06bff", "YOUR PERSONAL PAGE"], business: ["#2fe89e", "YOUR BUSINESS"], space: ["#ffbf3d", "YOUR SPACE"] };
  const items = cards.map(function(pg){
    const k = pg.page_kind || pg.kind;
    const d = defs[k] || ["#a06bff", k];
    return '<a class="hcard" style="--hc:' + d[0] + '" href="/pages/' + esc(alias) + '/' + esc(pg.page_alias) + '">'
      + '<div class="label" style="color:' + d[0] + '">' + d[1] + '</div>'
      + '<div class="t">' + esc(pg.headline) + '</div>'
      + '<div class="u">nayanet.app/' + esc(alias) + '/' + esc(pg.page_alias) + '</div></a>';
  }).join("");
  const body = cards.length
    ? '<p class="sub">Your pages — built from your own words in the walk. Tap one to open it.</p>' + items
    : '<p class="sub">No pages yet — walk the walk first, and your pages will be here.</p>'
      + '<a class="hcard" style="--hc:#a06bff" href="/welcome"><div class="t">Start the walk</div></a>';
  return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    + '<title>' + esc(name || alias) + ' — Your Hub — NayaNET</title><style>'
    + 'body{margin:0;background:#050507;color:#fff;font-family:system-ui,-apple-system,sans-serif}'
    + '.wrap{max-width:680px;margin:0 auto;padding:28px 18px 40px;box-sizing:border-box}'
    + 'h1{font-size:28px;margin:0 0 6px;text-align:center}.sub{font-size:15px;line-height:1.6;color:#fff;text-align:center;margin:0 0 20px}'
    + '.hcard{display:block;text-decoration:none;color:#fff;background:linear-gradient(180deg,#1d1d28,#07070b 85%);border:2px solid var(--hc,#a06bff);border-radius:18px;padding:20px;margin-bottom:14px;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.4),0 12px 30px rgba(0,0,0,.65)}'
    + '.hcard:hover{transform:translateY(-2px);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.5),0 16px 36px rgba(0,0,0,.7),0 0 24px var(--hc,#a06bff)}'
    + '.label{font-size:11px;letter-spacing:.22em;font-weight:700}'
    + '.t{font-size:20px;font-weight:800;margin:8px 0 4px}.u{font-size:13px;font-family:ui-monospace,Menlo,monospace;word-break:break-all}'
    + '</style></head><body><div class="wrap"><h1>' + esc(name ? (name + " — your Hub") : "Your Hub") + '</h1>' + body + '</div></body></html>';
}

export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    const p = u.pathname;

    // ---- same-origin claim: write name + alias, read the row back ----
    if (p === "/api/claim" && req.method === "GET") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const row = await sbGetRow(alias);
      if (!row) return j({ exists: false, alias });
      const dk = u.searchParams.get("device_key") || "";
      return j({ exists: true, alias: row.alias, name: row.name,
        cert_no: row.cert_no, created_at: row.created_at,
        own: !!(dk && row.device_key === dk) });
    }
    if (p === "/api/claim" && req.method === "POST") {
      let b = {};
      try { b = await req.json(); } catch (e) { return j({ ok: false, error: "bad json" }, 400); }
      const alias = cleanAlias(b.alias);
      const name = String(b.name || "").trim().slice(0, 80);
      const device_key = String(b.device_key || "").slice(0, 64);
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      if (!name) return j({ ok: false, error: "name required" }, 400);
      const ins = await fetch(SB_URL + "?select=alias,name,cert_no,created_at", {
        method: "POST",
        headers: Object.assign(sbHeaders(), { "Prefer": "return=representation" }),
        body: JSON.stringify({ alias, name, device_key }),
      });
      if (ins.status === 201 || ins.status === 200) {
        const row = await sbGetRow(alias); // read-back before answering
        if (!row || row.cert_no == null) return j({ ok: false, error: "claimed but no certificate number came back" }, 502);
        const join = await recordJoin(req, row.alias); // JOIN ATTRIBUTION: the join moment is this claim
        return j({ ok: true, alias: row.alias, name: row.name, cert_no: row.cert_no, created_at: row.created_at, join });
      }
      if (ins.status === 409) {
        const row = await sbGetRow(alias);
        if (!row) return j({ ok: false, error: "alias taken" }, 409);
        if (row.device_key && row.device_key !== device_key)
          return j({ ok: false, error: "taken" }, 409);
        if (row.cert_no == null) return j({ ok: false, error: "claimed but no certificate number came back" }, 502);
        const join = await recordJoin(req, row.alias); // JOIN ATTRIBUTION: re-claim by the same device attributes too (dedupe guards the repeat)
        return j({ ok: true, alias: row.alias, name: row.name, cert_no: row.cert_no, created_at: row.created_at, join });
      }
      const txt = await ins.text().catch(() => "");
      return j({ ok: false, error: "claim failed: " + ins.status + " " + txt.slice(0, 120) }, 502);
    }

    // ---- welcome me: name for the walk's background verify ----
    if (p === "/api/welcome/me" && req.method === "POST") {
      let b = {};
      try { b = await req.json(); } catch (e) {}
      const alias = cleanAlias(b.alias);
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const row = await sbGetRow(alias);
      if (!row) return j({ ok: false, error: "unknown alias" }, 404);
      return j({ alias: row.alias, name: row.name });
    }

    // ---- welcome complete: store server-side, return the reveal ----
    if (p === "/api/welcome/complete" && req.method === "GET") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const rec = await env.WELCOME_ASSETS.get("complete_" + alias, "text");
      if (!rec) return j({ ok: false, error: "not found" }, 404);
      return new Response(rec, { headers: JSONH });
    }
    if (p === "/api/welcome/complete" && req.method === "POST") {
      let b = {};
      try { b = await req.json(); } catch (e) { return j({ ok: false, error: "bad json" }, 400); }
      const alias = cleanAlias(b.alias);
      const name = String(b.name || alias || "").trim().slice(0, 80);
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      /* Answers: only the known keys (ten questions + four news), word for word,
         trimmed. A skipped question arrives with no key at all and is stored
         as nothing — the Box never invents an answer. */
      const rawAns = (b.answers && typeof b.answers === "object") ? b.answers : {};
      const answers = {};
      ANSWER_KEYS.forEach(function(k){
        const v = String(rawAns[k] == null ? "" : rawAns[k]).trim();
        if (v) answers[k] = v.slice(0, 2000);
      });
      const topics = Array.isArray(b.topics) ? b.topics.map(function(t){ return String(t); }).slice(0, 32) : [];
      const pnIn = (b.pageNames && typeof b.pageNames === "object") ? b.pageNames : {};
      const pn = {
        personal: { title: (String((pnIn.personal && pnIn.personal.title) || name || alias).trim().slice(0, 80) || alias),
          slug: slug((pnIn.personal && pnIn.personal.slug) || alias, alias) },
        business: { title: (String((pnIn.business && pnIn.business.title) || "My Business").trim().slice(0, 80) || "My Business"),
          slug: slug((pnIn.business && pnIn.business.slug) || "business", "business") },
        space: { title: (String((pnIn.space && pnIn.space.title) || "My Space").trim().slice(0, 80) || "My Space"),
          slug: slug((pnIn.space && pnIn.space.slug) || "space", "space") }
      };
      const now = new Date().toISOString();
      /* The one project record — LIVE in Supabase (anon writes allowed on
         projects). Check first: there is no unique constraint on owner_alias,
         so a blind insert would double it. Exactly one per alias. */
      let project = null, projectErr = null;
      const exProj = await sbRows("projects", "owner_alias=eq." + encodeURIComponent(alias) + "&select=id,owner_alias,name,motto&limit=1");
      if (exProj.length) {
        const pr = await sbReq("PATCH", SB_PROJECTS + "?owner_alias=eq." + encodeURIComponent(alias),
          { name: pn.personal.title, motto: answers.motto || "" });
        project = { id: exProj[0].id, owner_alias: alias, name: pn.personal.title, motto: answers.motto || "" };
        if (!pr.ok) projectErr = pr.error;
      } else {
        const pr = await sbReq("POST", SB_PROJECTS + "?select=id,owner_alias,name,motto",
          { owner_alias: alias, name: pn.personal.title, motto: answers.motto || "" }, "return=representation");
        if (pr.ok && Array.isArray(pr.data) && pr.data[0]) project = pr.data[0];
        else projectErr = pr.error || "project insert failed";
      }
      /* The Box — try the live citizen_worlds table first; the staging
         worker's anon key is RLS-blocked there (proven 401/42501), so the Box
         is mirrored in KV in the table's exact shape until the server-side
         key lands (his hand). The store is reported, never hidden. */
      const boxRow = { alias, name, answers, topics, settings: { pageNames: pn } };
      const boxTry = await sbReq("POST", SB_WORLDS + "?select=alias",
        boxRow, "return=representation,resolution=merge-duplicates");
      const boxStore = boxTry.ok ? "citizen_worlds" : "kv-fallback";
      const boxNote = boxTry.ok ? null : ("citizen_worlds insert refused: " + (boxTry.status || "") + " " + (boxTry.error || ""));
      /* The three pages — try the live page_about table per kind, mirror in
         KV in the table's exact shape either way. Pages are composed from
         the Box's answers, never from a browser copy. */
      const pages = composePages(answers, pn);
      const pageStores = [];
      for (const pg of pages) {
        const q = "owner_alias=eq." + encodeURIComponent(alias) + "&page_kind=eq." + pg.kind + "&select=id&limit=1";
        const ex = await sbRows("page_about", q);
        let st = "kv-fallback", note = null;
        const row = { page_kind: pg.kind, page_alias: pg.page_alias, owner_alias: alias, headline: pg.headline, body: pg.body };
        if (ex.length) {
          const r2 = await sbReq("PATCH", SB_PAGES + "?owner_alias=eq." + encodeURIComponent(alias) + "&page_kind=eq." + pg.kind, row);
          if (r2.ok) st = "page_about"; else note = "page_about update refused: " + (r2.status || "") + " " + (r2.error || "");
        } else {
          const r2 = await sbReq("POST", SB_PAGES + "?select=id", row, "return=representation");
          if (r2.ok) st = "page_about"; else note = "page_about insert refused: " + (r2.status || "") + " " + (r2.error || "");
        }
        pageStores.push({ kind: pg.kind, table: "page_about", store: st, note });
        await env.WELCOME_ASSETS.put("page_" + alias + "_" + pg.kind, JSON.stringify({
          table: "page_about", page_kind: pg.kind, page_alias: pg.page_alias, owner_alias: alias,
          headline: pg.headline, body: pg.body, store: st, updated_at: now }));
      }
      await env.WELCOME_ASSETS.put("box_" + alias, JSON.stringify({
        table: "citizen_worlds", alias, name, answers, topics, settings: { pageNames: pn },
        project_id: project ? project.id : null, store: boxStore, note: boxNote,
        created_at: now, updated_at: now }));
      const rec = { alias, name, answers, topics, pageNames: pn, completed_at: now,
        box_store: boxStore, box_note: boxNote, project_id: project ? project.id : null,
        project_error: projectErr, page_stores: pageStores };
      await env.WELCOME_ASSETS.put("complete_" + alias, JSON.stringify(rec));
      const origin = u.origin;
      const reveal = { alias,
        ambassador_link: "https://nayanet.app/joinus?ref=" + alias,
        pages: { personal: origin + "/pages/" + alias + "/" + pn.personal.slug,
          business: origin + "/pages/" + alias + "/" + pn.business.slug,
          space: origin + "/pages/" + alias + "/" + pn.space.slug,
          dashboard: "https://nayanet.app/dashboard?name=" + encodeURIComponent(name)
            + "&alias=" + encodeURIComponent(alias) },
        hub: origin + "/hub?alias=" + encodeURIComponent(alias),
        box: { table: "citizen_worlds", store: boxStore, note: boxNote },
        project: project ? { id: project.id, table: "projects", live: true } : { table: "projects", live: false, error: projectErr },
        page_stores: pageStores };
      return j(reveal);
    }

    // ---- Box read-back: the Box + the one project + the three pages ----
    if (p === "/api/welcome/box" && req.method === "GET") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const boxRaw = await env.WELCOME_ASSETS.get("box_" + alias, "text");
      const box = boxRaw ? JSON.parse(boxRaw) : null;
      const projRows = await sbRows("projects", "owner_alias=eq." + encodeURIComponent(alias) + "&select=id,owner_alias,name,motto,created_at");
      const livePages = await sbRows("page_about", "owner_alias=eq." + encodeURIComponent(alias) + "&select=page_kind,page_alias,headline,body&order=page_kind");
      const pages = [];
      for (const kind of ["personal", "business", "space"]) {
        const raw = await env.WELCOME_ASSETS.get("page_" + alias + "_" + kind, "text");
        pages.push(raw ? JSON.parse(raw) : null);
      }
      return j({ ok: true, alias, box, box_count: box ? 1 : 0,
        project_rows: projRows, project_count: projRows.length,
        live_pages: livePages, pages });
    }

    // ---- created pages: /pages/<alias>/<slug> renders the page record ----
    const pm = p.match(/^\/pages\/([a-z0-9-]+)\/([a-z0-9-]+)\/?$/);
    if (pm) {
      const a = pm[1].toLowerCase(), seg = pm[2].toLowerCase();
      let found = null;
      for (const kind of ["personal", "business", "space"]) {
        const raw = await env.WELCOME_ASSETS.get("page_" + a + "_" + kind, "text");
        if (raw) { const pg = JSON.parse(raw); if (pg.page_alias === seg) { found = pg; break; } }
      }
      if (!found) {
        const live = await sbRows("page_about", "owner_alias=eq." + encodeURIComponent(a) + "&page_alias=eq." + encodeURIComponent(seg) + "&select=page_kind,page_alias,headline,body&limit=1");
        if (live.length) found = live[0];
      }
      if (!found) return new Response("page not found", { status: 404 });
      /* The page IS the Personal page: pageHtml swaps the citizen's labels
         into the harvested template, so it needs the Box (answers +
         pageNames). KV first (sisters are kv-fallback), live citizen_worlds
         second. Without a Box, pageHtml falls back to the page record's own
         headline + ## body — a page never renders with another citizen's
         words. A failed swap throws and answers 500, never half-swapped. */
      let box = null;
      const boxRaw = await env.WELCOME_ASSETS.get("box_" + a, "text");
      if (boxRaw) { try { box = JSON.parse(boxRaw); } catch (e) { box = null; } }
      if (!box) {
        const wrows = await sbRows("citizen_worlds", "alias=eq." + encodeURIComponent(a) + "&select=alias,name,answers,settings&limit=1");
        if (wrows.length) box = wrows[0];
      }
      try {
        return new Response(pageHtml(a, found, box), { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
      } catch (e) {
        return new Response("page render failed: " + String(e && e.message || e).slice(0, 200), { status: 500, headers: { "content-type": "text/plain;charset=utf-8" } });
      }
    }

    // ---- staging Hub: /hub?alias= shows the citizen's three pages ----
    if (p === "/hub") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return Response.redirect("https://nayanet.app" + p + u.search, 302);
      const boxRaw = await env.WELCOME_ASSETS.get("box_" + alias, "text");
      const box = boxRaw ? JSON.parse(boxRaw) : null;
      const cards = [];
      for (const kind of ["personal", "business", "space"]) {
        const raw = await env.WELCOME_ASSETS.get("page_" + alias + "_" + kind, "text");
        if (raw) cards.push(JSON.parse(raw));
      }
      return new Response(hubHtml(alias, box ? box.name : "", cards),
        { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }

    // ---- pages: the ENTRY is the welcome page; the walk lives at /welcome ----
    if (p === "/") {
      return new Response(WELCOME, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }
    if (p === "/identity.html") {
      return new Response(IDENTITY, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }
    if (p === "/welcome" || p === "/welcome/") {
      return new Response(WALK, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }
    // ---- BRIDGE PAGE (2026-11-17): the official unfold, filed bytes verbatim ----
    if (p === "/agreement") {
      return new Response(UNFOLD, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }
    // ---- welcome-page assets, from KV (uploaded by kv-put-welcome-assets.py) ----
    if (p === "/login-obsidian.jpg" || p === "/naya-logo.png") {
      const key = p === "/login-obsidian.jpg" ? "wbf-login-obsidian.jpg" : "wbf-naya-logo.png";
      const buf = await env.WELCOME_ASSETS.get(key, "arrayBuffer");
      if (!buf) return new Response("not found", { status: 404 });
      return new Response(buf, { headers: { "content-type": p.endsWith(".jpg") ? "image/jpeg" : "image/png", "cache-control": "public, max-age=3600" } });
    }
    // ---- QUESTIONS 10/10 — the three Naya choice pictures, from KV
    // (uploaded by kv-put-naya-choice-pictures.py; A = Profile 2, B = Profile 3, C = Profile 4) ----
    if (p === "/naya-a.jpg" || p === "/naya-b.jpg" || p === "/naya-c.jpg") {
      const key = p === "/naya-a.jpg" ? "wbf-naya-a.jpg" : (p === "/naya-b.jpg" ? "wbf-naya-b.jpg" : "wbf-naya-c.jpg");
      const buf = await env.WELCOME_ASSETS.get(key, "arrayBuffer");
      if (!buf) return new Response("not found", { status: 404 });
      return new Response(buf, { headers: { "content-type": "image/jpeg", "cache-control": "public, max-age=3600" } });
    }
    // ---- BRIDGE PRESENTATION (2026-11-17) — the official emblem, from KV
    // (uploaded by kv-put-naya-emblem.py; NAYA_ICON.png verbatim, the
    // clearer fuller render Shawn sent 21:02Z; the bridge corners show
    // it on an angle) ----
    if (p === "/naya-emblem.png") {
      const buf = await env.WELCOME_ASSETS.get("wbf-naya-emblem.png", "arrayBuffer");
      if (!buf) return new Response("not found", { status: 404 });
      return new Response(buf, { headers: { "content-type": "image/png", "cache-control": "public, max-age=3600" } });
    }
    // ---- BRIDGE PRESENTATION (2026-11-17, die-cut) — the emblem with its
    // solid-black background flood-filled to transparent, so the rotated
    // corner jewel reads as a die-cut seal, not a black diamond patch
    // (the 21:57Z emblem eye flagged the pasted-diamond on the other
    // round's corners; the artwork pixels are byte-identical to
    // NAYA_ICON.png — only the background sheet is removed) ----
    if (p === "/naya-emblem-cut.png") {
      const buf = await env.WELCOME_ASSETS.get("wbf-naya-emblem-cut.png", "arrayBuffer");
      if (!buf) return new Response("not found", { status: 404 });
      return new Response(buf, { headers: { "content-type": "image/png", "cache-control": "public, max-age=3600" } });
    }
    // ---- AGREEMENT v4 — Naya's portraits + official logo, from KV
    // (uploaded by kv-put-agreement-v4.py; keys wbf-agmt-*; byte-identical
    // harvests, Naya_Profile_black_full.jpg never uploaded: it duplicates
    // Naya_Profile_2.jpg) ----
    if (p.startsWith("/agmt-")) {
      const key = "wbf-" + p.slice(1);
      const buf = await env.WELCOME_ASSETS.get(key, "arrayBuffer");
      if (!buf) return new Response("not found", { status: 404 });
      return new Response(buf, { headers: { "content-type": p.endsWith(".png") ? "image/png" : "image/jpeg", "cache-control": "public, max-age=3600" } });
    }
    // ---- service worker: the Personal template registers sw.js; serve a
    // valid no-op worker so registration succeeds (zero console errors).
    // Without this route the fallback serves the walk HTML and registration
    // fails on every staged page load. ----
    if (p === "/sw.js") {
      return new Response("/* NayaNET staging service worker — no offline cache. */\nself.addEventListener('install', function(){ self.skipWaiting(); });\nself.addEventListener('fetch', function(){ });\n", { headers: { "content-type": "application/javascript", "cache-control": "no-store" } });
    }
    if (p.startsWith("/api/")) return j({ ok: false, error: "unknown api" }, 404);

    // ---- alias redirects to the live pages (name from the completion record when known) ----
    const am = p.match(/^\/([a-z0-9-]+)(\/([a-z0-9-]+))?\/?$/i);
    if (am) {
      const a = am[1].toLowerCase(), sub = (am[3] || "").toLowerCase();
      const reserved = ["welcome", "dashboard", "identity.html", "hub", "enter",
        "manifest.webmanifest", "manifest.json", "icon-192.png", "icon-512.png", "sw.js", "world", "api", "pages"];
      if (reserved.indexOf(a) === -1) {
        let nm = "";
        try {
          const rec = await env.WELCOME_ASSETS.get("complete_" + a, "text");
          if (rec) nm = (JSON.parse(rec).name || "");
        } catch (e) {}
        const qs = "?name=" + encodeURIComponent(nm) + "&alias=" + encodeURIComponent(a);
        let dest;
        if (sub === "dashboard") dest = "https://nayanet.app/dashboard" + qs;
        else if (sub === "business") dest = "https://nayanet.app/business" + qs;
        else if (sub === "space") dest = "https://nayanet.app/space" + qs;
        else dest = "https://nayanet.app/personal" + qs;
        return Response.redirect(dest, 302);
      }
    }
    if (p.startsWith("/hub/")) {
      return Response.redirect("https://nayanet.app" + p + u.search, 302);
    }
    return new Response(WALK, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
  },
};
"""

worker = (worker
          .replace("__WALK__", json.dumps(walk))
          .replace("__IDENTITY__", json.dumps(ident))
          .replace("__WELCOME__", json.dumps(welcome))
          .replace("__UNFOLD__", json.dumps(unfold))
          .replace("__PERSONAL__", json.dumps(personal))
          .replace("__SBKEY__", json.dumps(sb_key)))
if "--stdout" in sys.argv:
    _OUT.buffer.write(worker.encode())
else:
    open(OUT, "w", encoding="utf-8").write(worker)
print(f"OK worker built: {OUT} ({len(worker.encode())} B, "
      f"sha256={hashlib.sha256(worker.encode()).hexdigest()})")
print("NOTE: this staging worker embeds the public anon key; live must use a secret binding.")
