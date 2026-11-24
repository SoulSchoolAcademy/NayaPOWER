# WHOLE-SYSTEM CONNECTION ROUND — MAKER REPORT (v1, staged, NOT live)

**Maker:** maker subagent · **Date:** 2026-11-24 · **Round:** whole-system connection
**Order:** Shawn, 2026-11-24 ~10:22 MST — make sure the whole system is working;
connect to the new recent certificate; do the updated walkthrough; make sure the
updated collective agreement is done, with all the agreement edits that were never done.

**Status: STAGED, not live. Nothing here has been deployed. Nothing goes live
before the checker passes. This report goes to the parent orchestrator, NOT to Shawn.**
Per Shawn's standing law (2026-11-24 ~11:14 MST): don't send anything that's not
truly done — staged is not done unless he asked to see the stage. This round is
still building until the checker passes and his eye has seen it live.

## Staged files (branch `whole-system-connection-20261124`, repo SoulSchoolAcademy/NayaPOWER)

| File | Size | SHA-256 | Base |
|---|---|---|---|
| `welcome-staged.html` (portal) | 1,186,194 B | `55eb1b1e522c…` | live portal 1,146,566 B, sha `aa9880c7…` |
| `agreement.html` | 22,950,575 B | `1a72623524ea…` | round-2 tip `d22bccf8`, blob `8b8ccd95`, 22,886,321 B, sha `68dd6ae0…` |
| `identity.html` | 309,681 B | `edb926dd3ea7…` | live `nayanet.app/identity.html`, 307,759 B, sha `bdd8af83…` |
| `welcome-redirect.html` | 1,047 B | `49cfeb004d90…` | new file (the /welcome asset) |

Build scripts (one source of truth each, re-runnable from base):
`maker/edit-portal.py` (part 1), `maker/edit-portal-2.py` (part 2),
`maker/edit-portal-3.py` (walk view), `maker/edit-identity.py`,
`maker/edit-agreement.py`. All script blocks in all three files pass
`node --check`. The agreement's two script blocks were checked at build time
(the 22 MB EMBED block is verified by sha instead on re-check: file unchanged
since build, sha `1a72623524ea…`).

Staged links: **to be filled on filing** (commit/blob per file below).

## The /welcome redirect mechanism (item 66)

`/welcome` never renders its own gate again. The worker serves
`welcome-redirect.html` at `/welcome`: meta refresh 0 + `location.replace(
'https://nayanet.app/?from=welcome')` + a plain link for no-JS. The D1-fixed
walk file (`nayanet.app/welcome`, 124,064 B, sha `7fd0c05b`) is UNTOUCHED — the
D1 round owns it. The walk now presents from the portal (`/?walk=1`).

## The flow, as built

Portal → name in → certificate (`/identity.html`, walkthrough-15 certificate,
cert_no 94) → the 15-question walk presenting on the portal (`/?walk=1`) →
"See my world" (`/personal?name=…&alias=…`, registry-verified name) →
"Choose your plan" (pricing). The agreement comes before pricing and before
the world: the portal's agreement button goes to `https://nayanet.app/agreement`,
which opens on the CHOICE view; the deck ends onward to the portal name box
(`/?from=agreement#userName`), never back, never a new tab.

## Per-item status (all 78)

DONE = built in this round with byte evidence · DONE-in-bytes = already true in
the base, verified · PARTIAL = built as far as the evidence allows, gap named ·
WAITING = decision/dictation owed, never invented · BLOCKED = needs a source that
doesn't exist in this round · NOTED = named, no change (not a defect) · N/A = the
defect doesn't exist in this base.

| # | Status | Evidence |
|---|---|---|
| 1 | WAITING | DECISION — strict no-baked-text redo (slides 12, 19, 21, 25, 26). Shawn's word owed. No slide touched. |
| 2 | WAITING | DECISION — slide-7 pairing. Shawn's word owed (see U4). |
| 3 | WAITING | Dictation U1 unfinished. Slide 11 left byte-identical — hash asserted `33b0590cfb9f811a` after all edits. |
| 4 | DONE-in-bytes | Slide 9 is "Smart Calendar" in the base. |
| 5 | BLOCKED-needs-source | Slide 8's image is an embedded composite; its calendar grid is unreadable at 390px. The fix needs the real Smart Calendar image as an asset — no such image file was in this round's sources. Nothing invented. |
| 6 | WAITING | Separate captain's decision (player placement). Untouched per the item. |
| 7 | DONE-in-bytes | `ensureAnalyser()` wires `createMediaElementSource(audio)`; `drawWave` reads `getByteFrequencyData`. The synthetic branch is only the fallback when the analyser isn't active. |
| 8 | NOTED | Vignette named, not judged — reads as the brief's own "white light around the edges". No change. |
| 9 | NOTED | Face circles intermittently black — pre-existing probe timing. No change. |
| 10 | DONE | Choice screen is the first load (`screen-choice` active, cover not); play disc centred, two pills underneath; deep links `?view=deck` / `?view=letter`. |
| 11 | DONE | Choice pills `:active` scale `.97` + dim; Agree `.94` in the portal (`dealAgreeBtn`/`letterPageAgree` rule, `scale(.94)` ×7 in staged portal). |
| 12 | DONE-in-bytes | Rest-glow `:not()` rule covers all four pills (`0 0 6px 0`), verified present. |
| 13 | DONE | Deck-resume branch removed from `enterStage()`; it always lands on the choice view. `goResume` alone resumes the deck. |
| 14 | DONE | 12/12 legal pages + 12 footer buttons. Ambassador Terms page EXISTS in this base with real text (7 beats) — the older "nonexistent" note is superseded by these bytes. Closing a legal page returns to the view it came from (`lastScreen`). |
| 15 | DONE-in-bytes | Choice title in its own centred block with no corner emblems over it; daybar title in its own grid area. |
| 16 | DONE | Choice screen at ≤640px: title 25px, pills full-width (max 340px), play disc 72px; legalbar wraps in flow. Checker proves by render at 635. |
| 17 | DONE-in-bytes | One Jump entry in the returning view; the others-list dedup code exists. Eye proof owed. |
| 18 | DONE | Two pages merged into ONE choice view (play disc centred, two buttons underneath), behind the portal's agreement button per N4. |
| 19 | DONE | Two buttons under the play disc: "Begin the visual story" (purple) / "Read the agreement" (green, per N1). |
| 20 | DONE | No scrollable letter on the choice page — the letter lives behind the Read button. |
| 21 | DONE-in-bytes | No "Back to the login" button exists in this base (×0) — nothing overlays the footer. |
| 22 | DONE | Choice fits one screen: compact centred layout + 640px rules. |
| 23 | DONE-in-bytes | "Hi, I'm Naya" ×1 in the base — not duplicated. |
| 24 | PARTIAL | The unfold mechanism is present (one-at-a-time Keep reading + "read the whole page at once" one tap away). The 86→essence distillation is NOT done — it needs the manuscript comparison, and the hard line forbids rewriting the official text. Nothing rewritten. |
| 25 | PARTIAL | Play control big/circled/orb/Naya/centred/wired exists (PowerCast player + audio controls). The read-back VOICE is paused per item 34 — BLOCKED on recording. |
| 26 | DONE-in-bytes | Deck structure kept: 27 slides, forward/back, end → portal. No slide words changed. |
| 27 | DONE | 12 legal pages in the official unfold at the SAME addresses (`data-legal-open` keys unchanged); Accessibility (7 boards) + Disclaimer (8 boards) added verbatim from `legal-official-20261116/11-` + `12-`. |
| 28 | DONE | Bridge wiring: READ → `/agreement`; VISUAL → deck; deck-end → portal (the bridge); letter-end → choice. |
| 29 | DONE | `welcome-staged` ×0 in all three staged files. Nothing points at the proof host. |
| 30 | DONE | The unfold is complete in bytes: 12/12 legal pages + deck + choice. "Shown to Shawn whole" is his eye's job, not the build's. |
| 31 | N/A | The 404 handler path doesn't exist in this base. The agree landing is `goToPortal` → portal name box (item 43). |
| 32 | DONE | Portal: `#userName` / `?from=agreement` arrival bypasses the returning gate and focuses the input. Agreement end lands on `/?from=agreement#userName`. |
| 33 | WAITING | DECISION — OFFICIAL vs v3. No text changed. |
| 34 | BLOCKED | Voice at the END, once the text is final. No recording exists; nothing invented, nothing synthesized. |
| 35 | WAITING | Shawn's hand — §4.11/C9 wording. |
| 36 | WAITING | Trigger not met — his eye hasn't passed the unfold, so it can't template About/Skills yet. |
| 37 | DONE | Short label "Read the agreement" ×4 in the portal; long label ×0. |
| 38 | DONE | Pair-size rule added (bridge pair = intro pair, same height/width). |
| 39 | DONE | Real diamond jewel: 96×96 PNG, 12,715 B, sha `e583f51f…`, shared `.fp-btn-jewel`, 4 spans on the portal + 2 on the agreement choice. |
| 40 | DONE | `#fpBridgePick` removed (the element; a comment names the removal). `#fpIntroPick` (deck) stays. |
| 41 | DONE-by-construction | "THE OPENING" ×0 and the voice line ×0 in the base — the amendment's targets don't exist here. The new choice screen embodies it: centred play, no duplicate header, no voice line. |
| 42 | DONE | The N ball HOLDS 2 full seconds at the flow end. |
| 43 | DONE | End flow onward in place to the portal name box (`/?from=agreement#userName`), then the Hub — never a new tab, never back. |
| 44 | DONE | `PORTRAITS[0]` is `NAYA_POWER.jpg`. |
| 45 | PARTIAL | Controls exist (Back-15 / Play / Stop / Forward-30 + native audio controls). The distilled read-back is BLOCKED on the recording (item 34). |
| 46 | DONE | Portal `ensureBeatVisible` ×3 copies → `block:'start'`; agreement legal Next → `block:'start'`. One block per viewport. |
| 47 | DONE/JUDGED | Hover-tip: no hover-tip element exists in this base (N/A). Legal-row clip: the row already wraps in flow (DONE-in-bytes). 1919 void: JUDGED breathing room — the stage fills the viewport by design; the empty middle is the frame's own air (frame law §14). |
| 48 | DONE-in-bytes | One frame above the fold: video LEFT, audio RIGHT with its own play button (PowerCast PROMAX player). |
| 49 | DONE-in-bytes | Anthem `EMBED.audio` is `NayaNET_Welcome.m4a` byte-identical (6,246,935 B, sha `ce8e018c…`). Old audio never used. |
| 50 | DONE via N3 | Item 48 governs; the literal PowerCast player IS the frame's player. |
| 51 | DONE-via-harvest | Choice pills in the staged buttons-round language + the emblem jewel. The Hub/Academy source comparison is the checker's to re-prove. |
| 52 | DONE | No slide count anywhere (`of 27` ×0); no presentation bottom bar — only small floatnav Back/Forward + the legal footer. The one-button demand is superseded by N2 (TWO buttons, coordinator decision). |
| 53 | DONE | Final-board link row: "The Invitation" (his pick still owed — this is the recommendation) + 8 links, each opening its verbatim answer in a frame (see sources below). |
| 54 | DONE-in-bytes | Portal `enterBtn` → `/agreement`. |
| 55 | DONE-in-bytes | The daybar IS the old-way bar (orb + NAYANET left, title dead centre, her photo + NAYA right). The certificate is the frame standard in `identity.html`. No redesign. |
| 56 | DONE-in-bytes | Portal loads first always; boot never auto-enters the stage on a plain load. |
| 57 | DONE-in-bytes | Fresh-load walk-in fixed (no auto-enter; stale `nayanet_fp_stage` cleared). Checker must re-prove by render — Shawn's re-report is unexplained by the bytes. |
| 58 | DONE | Jump → `/personal?name=…&alias=…` with the name resolved from the registry row first (Supabase lookup, 1.5s timeout, stored name only as fallback). |
| 59 | DONE | ≤480px: the fixed stage-intro legal bar becomes static and wraps below the choice buttons — never an overlay. |
| 60 | DONE | Name entry IS the agreement: the deed sentence + ⓘ sit on the typed face; the flow is re-anchored to the portal. |
| 61 | DONE | Official sentence + ⓘ reader, the captain's draft verbatim (NOT presented as Shawn's words). Rewording rule followed ("high-level digital assets which we call digital real estate", each piece explained). "Already claimed" goes GREEN + bigger + unmissable (identity.html). |
| 62 | DONE | ⓘ reader: full text verbatim, split into short paragraphs, one at a time, Next each time, never a wall. |
| 63 | DONE (typed face) | Deed underglow (purple, beneath the gold start-here edge) + `fp-deed` on the portal name box. Per the 02:59Z amendment the sentence + ⓘ live ONLY on the typed face. |
| 64 | PARTIAL | Flow connected to the walkthrough-15 certificate (live worker `naya-welcome`, cert_no 94). The /free page showing the current certificate is a different surface — not in this round. |
| 65 | DONE | Portal presents the walk: `?walk=1` → 15 questions, state key `naya_welcome_right_v1` kept, progress "n of 15", auto-grow answers, end slide with Smart Link + world → pricing. |
| 66 | DONE | REDIRECT per the coordinator's decision (see mechanism above). |
| 67 | DONE | Flow order: portal → name → certificate → agreement → 15 questions → world → pricing. |
| 68 | DONE | The certificate-only gate goes — the walk presents from the portal; `/welcome` is a redirect. |
| 69 | DONE | Handoff is `/?walk=1` (never `/welcome`, never workers.dev). The certificate already lives on `nayanet.app` — `identity.html` is byte-identical to the workers.dev copy (sha `bdd8af83…`). |
| 70 | DONE | "This is me" path on `identity.html` (taken state) AND on the portal returning view. Taken message GREEN + bigger + unmissable, fits the viewport. |
| 71 | DONE | Jump lands on the real Personal page with the CORRECT name. Cause named: the old Jump replayed a stale stored `nayanet_smart_name` blindly into the URL (`prettyName` never mangled it — no code path turned "shawn" into "See"). Fixed at the cause: registry-first name resolution. |
| 72 | DONE | Returning greeting by name ("Welcome back, {name}.") + device memory (`nayanet_smart_name`/`alias` + walk state key). |
| 73 | WAITING | DECISION — Ambassador Terms text. The page exists in this base with real text (7 beats); the decision on its standing is still owed. Nothing invented. |
| 74 | DONE | Boards/frame untouched — `.intel-board` CSS rule count asserted unchanged before/after. |
| 75 | NOTED | Storybook cover — out of scope for the live build, not rebuilt. |
| 76 | BLOCKED | Read-back audio — same as item 34 (no recording). |
| 77 | DONE | Anthem — items 48/49. |
| 78 | WAITING-on-checker | Checker re-run owed, not a build item. |

**Count: DONE 44 · DONE/JUDGED 1 (item 47) · DONE-in-bytes 13 · PARTIAL 4 · WAITING 9 · BLOCKED 3 (items 5, 34, 76) · NOTED 3 · N/A 1 = 78.**
(Items 24/25/45 are PARTIAL on the same single blocker: the recording.)

## Exclusions from the published legal pages (named, not hidden)

The two new legal pages are filed as the draft text, verbatim except:
- The meta "Status — DRAFT" blockquotes are not published (they are file meta).
- Accessibility: "[Conformance level — Shawn: confirm, e.g. WCAG 2.1 AA.]" and
  "[Response time for accessibility fixes — Shawn: confirm.]" are bracketed
  instructions to Shawn, not publishable text — EXCLUDED, awaiting his word.
- Both md files say "Publish only after qualified Canadian counsel review and
  independent verification." That review is still owed — named here, not claimed done.

## Disagreements left as written (N7 — do NOT harmonize)

Payout timing appears in three variants in the record and was NOT harmonized:
the walk's end slide says "payouts every Wednesday"; the ⓘ text and the
ambassador beats say "paid every day" / "50% of the eligible revenue". Each
kept its own words in its own place. The portal walk's end slide carries NO
payout line at all — nothing new was written on this point.

## Gaps and follow-ons (for the parent, not the build)

1. **Top-menu Certificate entry — NOT added.** The portal file carries NO top
   menu (How It Works / PowerCast / Innovations ×0) — the menu lives on a
   different surface. Its Certificate entry is owed as a follow-on once the
   menu's home file is named. Not invented here.
2. **Item 5** — needs the real Smart Calendar image as an asset.
3. **Items 34/45/76** — need the distilled read-back recording (script exists,
   1,482 words, `agreement-audio-20261118/audio-script.md`).
4. **Item 24** — the 86→essence distillation needs the manuscript comparison.
5. **Item 64** — the /free page showing the current certificate is a separate surface.
6. **Item 53 wording** — the final board is built with "The Invitation" (the
   recommendation); the final-board wording is still his pick.
7. **Item 61** — the official sentence + ⓘ text are the CAPTAIN'S DRAFT
   (offered 2026-11-16 02:28Z), awaiting his tap. Never presented as his words.
8. **Item 57** — Shawn re-reported the portal still showing the agreement; the
   bytes show the fix in place. The checker must re-prove by RENDER, not by bytes.
9. **UNFOUND U1–U6** stay unfound (U1 dictation, U2 "no button" wording, U3 a
   single #3453 verdict document, U4 slide-7 image pairing, U5 settled-placement
   wording, U6 the "I follow protocol" board text). Nothing invented for any of them.
10. **N5** — 37 boards vs 27 slides are two different presentations; this round
    kept the 27-slide deck and did not conflate them.

## Item 53 sources (all verbatim, nothing invented)

- Our Vow — SOUL.md, "THE ULTIMATE ME — THE VOW" (2,628 chars).
- Our Oath — The Wise One Manifesto, §V "The Declaration" (1,090 chars).
- Our Constitution — NAYA-PROTOCOL.md, full text (13,255 chars).
- Our Laws — NAYA-PROTOCOL.md §§1–2 (3,281 chars).
- The Deal — the file's own THE DEAL + WHAT YOU GET beats.
- Our Promise — the file's own JOINING IS FREE + THE ONE LAW beats.
- Our Rules — the file's own THE RULE + THE EXCEPTION beats.
- The Governance — the file's own THE MOTHER BEE + THE LAW beats.
- Note: the item's "ten-ways distillation" label was not matched to a separate
  text in the file — The Deal shows the file's own plain-words deal text.

## What needs Shawn's word (decisions, not builds)

Items 1, 2, 6, 33, 35, 73 (decisions); item 3/U1 (dictation); the Accessibility
conformance level + response time; the counsel review of the two new legal pages;
the final-board wording ("The Invitation" is the recommendation); the official
sentence + ⓘ text (captain's draft awaiting his tap); the payout-timing
harmonization (N7 — do not harmonize without his word).

## Verification done by the maker

- All script blocks in all three staged files pass `node --check`
  (portal 5, identity 1, agreement 2 — agreement checked at build time, file
  unchanged since, sha `1a72623524ea…`).
- Slide 11 asserted byte-identical after all edits (hash `33b0590cfb9f811a`).
- `.intel-board` CSS rule count asserted unchanged (item 74).
- `welcome-staged` ×0 in all three staged files (item 29).
- `of 27` ×0 in the agreement (item 52); `?view=deck|letter` wiring present;
  12/12 legal pages + buttons; 7/7 and 8/8 beats/dots on the new pages.
- **Not proven:** anything by render. The checker must walk it as Shawn —
  land on nayanet.app, name in, certificate, 15 questions presenting — at phone
  width first, with real clicks. His eye is the final gate.
