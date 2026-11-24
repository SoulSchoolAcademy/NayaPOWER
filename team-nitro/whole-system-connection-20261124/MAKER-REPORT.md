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

**Filed 2026-11-24 ~18:35 MST — commit `b2900a93e9c5edbc38af125581c710401524c17f`
(parent `bcf747ca`, branch `whole-system-connection-20261124`, ref verified MATCH).**
Read-back verified from GitHub (blob API, raw): agreement 22,950,575 B,
sha256 `1a72623524ea…`, blob `ec558632…`; portal 1,186,194 B, sha256
`55eb1b1e522c…`, blob `011a4cdf…`. Tree `3dd28449…` confirmed with all 6 entries.

- Portal: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/welcome-staged.html (blob `011a4cdf…`, 1,186,194 B)
- Agreement: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/agreement.html (blob `ec558632…`, 22,950,575 B)
- Identity: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/identity.html (blob `1b86d392…`, 309,681 B)
- /welcome redirect: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/welcome-redirect.html (blob `6f41470b…`, 1,047 B)
- This report: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/MAKER-REPORT.md (blob `04160e3d…`)

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

---

# MAKER REPORT — v2 (fix round, staged, NOT live)

**Maker:** fix maker v2 · **Date:** 2026-11-24 · **Parent:** `fafd172c` (branch tip at
filing; verify at file time) · **Checker verdict addressed:** `checker/CHECKER-VERDICT.md`
(overall FAIL — 3 FAIL, 15 PARTIAL, design-laws §G FAIL on 9 numbered breaks).

**Status: STAGED, not live. Nothing here has been deployed. A fresh checker
re-verifies; the coordinator decides the deploy. This report goes to the parent
orchestrator, NOT to Shawn.**

**Filed 2026-11-24 — commit `e654730159b5ca9cc768e48fd68a10b7a9c20c09`
(parent `fafd172c`, branch `whole-system-connection-20261124`, ref verified MATCH).**
Read-back verified from GitHub (blob API): portal 1,189,401 B, blob
`d28503f0…`; agreement 22,953,906 B, blob `d083f2b7…`; identity 310,386 B, blob
`d57f3de1…`; report 37,514 B, blob `e7cf89b0…`.

- Portal: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/welcome-staged.html (blob `d28503f0…`, 1,189,401 B) · staged: https://naya-proof-host.nayapower.workers.dev/?file=team-nitro%2Fwhole-system-connection-20261124%2Fwelcome-staged.html&ref=whole-system-connection-20261124
- Agreement: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/agreement.html (blob `d083f2b7…`, 22,953,906 B) · staged: https://naya-proof-host.nayapower.workers.dev/?file=team-nitro%2Fwhole-system-connection-20261124%2Fagreement.html&ref=whole-system-connection-20261124
- Identity: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/identity.html (blob `d57f3de1…`, 310,386 B) · staged: https://naya-proof-host.nayapower.workers.dev/?file=team-nitro%2Fwhole-system-connection-20261124%2Fidentity.html&ref=whole-system-connection-20261124
- This report: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/whole-system-connection-20261124/team-nitro/whole-system-connection-20261124/MAKER-REPORT.md (blob `e7cf89b0…` — the follow-up report-only commit below records the final blob)

## v2 staged files

| File | Size | SHA-256 | v1 size/sha |
|---|---|---|---|
| `welcome-staged.html` (portal) | 1,189,401 B | `e620725722f7…` | 1,186,194 B, `55eb1b1e522c…` |
| `agreement.html` | 22,953,906 B | `2c88513f9011…` | 22,950,575 B, `1a72623524ea…` |
| `identity.html` | 310,386 B | `1b721d5ccb84…` | 309,681 B, `edb926dd3ea7…` |
| `welcome-redirect.html` | 1,047 B | `49cfeb004d90…` (unchanged) | 1,047 B, `49cfeb004d90…` |

Build scripts (one source of truth each, re-runnable from the v1 files in
`maker/`): `edit-portal-v2.py` + `edit-portal-v2b.py` (portal), `edit-agreement-v2.py` +
`edit-agreement-v2b.py` (agreement), `edit-identity-v2.py` (identity). Probes:
`probe-v2-portal.py`, `probe-v2-agreement.py`, `probe-v2-identity.py`,
`probe-v2-disc.py`, `probe-v2-decknav.py`, `probe-v2-cover.py`, `probe-v2-audio.py`
(local mirror `http://127.0.0.1:8898/`, Playwright Firefox; identity via Chromium
through the localhost forwarder `http://127.0.0.1:18080`, because Firefox in
this VM fires no Supabase reads).

## What v2 fixed (each proven by render with real clicks, not by bytes)

1. **Phone portal front door — check A / §G.1 (was FAIL).** The v1 deed
   sentence sat inside `.content`, which at 390px grew to 403px tall inside a
   288px circle and spilled the input above the ring. v2 moves the deed
   sentence + reader out of `.content` into `.stage` (below the 248px circle)
   at ≤480px only, by a runtime move script (desktop untouched). Render at
   390×844: `#userName` rect 104,311 182×43, hit=SELF, real click focuses it,
   typed "Shawn"; `#presence` "NAYA WELCOMES YOU" visible (two centred lines),
   hit=SELF; `#fpDeedSentence` whole, 15,466 360×163, hit=SELF, bottom 629 ≤
   844 (the 4px scrollHeight excess is line-height rounding — every glyph
   visible in the screenshot); `#fpDeedInfo` ⓘ 26×26 hit=SELF, opens the
   reader ("1 of 12", rect 535–732, in view); Enter button hit=SELF. Desktop:
   input SELF, deed inside the core (440–602 vs core 235–670). Screenshot
   `/tmp/wsc-v2/phone-portal-v2.png`.
2. **Walk comes into view — item 65 (was PARTIAL).** Root cause: the author
   `display:flex` on `.fp-login` beat the UA `[hidden]` rule, so the login
   stayed laid out and the walk sat below the fold. v2 adds
   `.fp-login[hidden]{display:none}` and `scrollIntoView` on walk load and on
   finish. Render: desktop 1280×900 `?walk=1` → scrollY 0, login display
   none, Q1 [84,117], walk top 0; phone 390×844 → Q1 [84,117]; end-slide
   buttons in view both widths (world y371 / pricing y370 desktop; world y410
   / pricing y397 phone); "Welcome home." ×1 on the end slide (duplicated
   heading removed — the completion line already says it).
3. **Agreement load error + dead Close — item 53 / §G.4 (was FAIL).** The
   appended init block attached `fpFinalClose` before the reader div existed.
   v2 wires it guarded (`wireFinalClose()`, `__fpWired` flag) on
   DOMContentLoaded and inside `openFinal()`. Render: zero page errors on
   plain, `?view=deck` and `?view=letter` loads; all 8 final-board links open
   their verbatim answers (Our Vow 2,628 chars; The Deal 517; Our Promise 483;
   The Governance 344; Our Constitution 13,255; Our Laws 3,281; Our Rules 290;
   Our Oath 1,090) and Close hides the reader for every one — **8/8 open+close**.
4. **"I agree" exists and sinks — item 11 (was FAIL).** New `.fp-agree-btn`
   (obsidian pill, green rim, min-height 64px) at the deck end (after the Oath
   link) and at the letter end (appears in `.letter-controls` when the last
   beat lands, hidden again on reset). Held-press by real mouse:
   `matrix(0.94, 0, 0, 0.94, 0, 1)` + `brightness(0.72)` for BOTH. Click-through:
   N ball holds, then in-place navigation to
   `https://nayanet.app/?from=agreement#userName` with `#userName` focused
   (deck and letter both proven). Play disc: held-press `matrix(0.94, 0, 0,
   0.94, 0, 0)` + `brightness(0.72)` — v2b also pauses the idle `enterPulse`
   animation while pressed, because the running animation composites with the
   press transform and made the held value non-deterministic (0.94 one run,
   0.993 mid-pulse the next). This also proves item 28's letter-end bridge,
   which the checker left UNPROVEN (28: PARTIAL → DONE).
5. **Portal button label — item 37 (was FAIL).** Visible `#fpEnterDeal` now
   reads "Read the agreement ◆" (long label ×0, case-sensitive count; short
   label ×6). Render phone + desktop.
6. **Taken message — items 61, 70 (were PARTIAL).** `#aliasStatus` "already
   claimed" is now green `rgb(47,232,158)`, 19px, weight 800; the green
   `#hubNote` + "This is me" button scroll into view when they appear
   (`scrollIntoView({block:'center'})`). Render (Chromium, live registry read
   of the existing `shawn` row): desktop 1280×900 — status green 19px 800
   hit=SELF in view; hubNote y728 h121 (bottom 849 ≤ 900); This-is-me y797
   h52 (bottom 849 ≤ 900); phone 390×844 — hubNote y606 h151 (bottom 757 ≤
   844), This-is-me y704 h52 (bottom 756 ≤ 844). Click "This is me" →
   `/?walk=1&name=Shawn&alias=shawn` (local mirror). No new test identities
   created; the checker's two registry rows (cert_no 860, 861) untouched —
   deletion is Shawn's hand. This also fixes item 62's phone ⓘ (PARTIAL →
   DONE — see fix 1).
7. **Choice footer fit — item 22: DONE by coordinator restatement, no build.**
   The choice block fits one screen without scroll at 390/635 (checker-proven);
   the 12-link legal footer below the fold at 1280×900 is normal footer
   behaviour. Footer unchanged.
8. **Items 48/50 — PROVE, not rebuild: render evidence in hand, items stay
   PARTIAL.** The choice screen stays the merge-law shape (settled by #3453 +
   N4). The video-left / audio-right arrangement EXISTS on the agreement
   cover screen (`#screen-cover`, reached by Back from deck slide 1):
   `.pm-art` (video) 671×630 @103,270 vs `.pm-side` (audio) 377×613 @800,270 —
   video left, audio right, both opacity 1, visible; `#videoFacade` 671×377
   with the welcome poster + play button; `#welcomeAudio` 335×40 @821,648;
   voice orb `#voice` 207×207; YouTube link `a06pPpxRil4`. Screenshot
   `/tmp/wsc-v2/agree-cover-desk-2.png` (8s settle — the first shot at 1.2s
   caught the poster before paint). Items stay PARTIAL: the frame order is
   proven present on the cover screen, not on the choice screen, and the
   coordinator settles whether the merge-law shape supersedes the frame order.
9. **Item 7 (amplitude) — FLAGGED: no real-audio path is demonstrable in this
   round.** v2 added `play`/`pause`/`ended` listeners that set `audioPlaying`
   from the real `#welcomeAudio` element — the wiring is correct, but the path
   cannot fire, by the page's own design: the one-play-path rule attaches
   `audio.addEventListener('play', function(){ audio.pause(); ytCommand('play'); })`
   — pressing play on the audio bar immediately pauses the audio and plays
   the YouTube video instead. Demonstrated live: direct `audio.play()` resolves
   yet `paused` stays true, `currentTime` 0.00, `audioPlaying` false, analyser
   present but `freqSum48` 0; real mouse clicks on the native play button do
   the same. The analyser is wired only to the audio element, and the only
   media that actually plays is the cross-origin YouTube iframe, which cannot
   feed a Web Audio analyser. Making it live would require either letting the
   audio element actually play (breaking the one-play-path law — a design
   decision, not a maker fix) or rewiring the analyser to the video
   (impossible cross-origin). The synthetic branch stays, flagged. No
   DONE-in-bytes claimed.
10. **Tidies (same pass):** "Welcome home." duplication removed (end slide
    ×1); "New user? Create a new account — click here" no longer clips on the
    circle edge on desktop (deed hidden while the returning view shows,
    reshown on "New user?" click; returning line rect 477,523 325×31 inside
    core 235–670, hit=SELF); daybar title whole at 390px ("The Collective
    Agreement", white-space normal, scrollW = clientW = 312, h24, no
    ellipsis); choice pills equal on desktop (280×64 both, was 253 vs 241 at
    48px) — item 38 PARTIAL → DONE, and item 15's phone truncation
    (DONE-in-bytes → DONE).

## Design-laws §G re-check (v2, in writing)

§G.1 phone front door — FIXED by render (fix 1). §G.2 walk whole — FIXED by
render (fix 2). §G.3 taken message — FIXED by render (fix 6: green 19px 800,
in view both widths). §G.4 Close dead — FIXED by render (fix 3: 8/8, zero
errors). §G.5 play disc sink — FIXED by render (fix 4: .94 + dim, deterministic
after v2b). §G.6 no reachable agree — FIXED by render (fix 4: deck + letter
agree .94 + click-through to the live portal name box). §G.7 clipped/duplicated
text — FIXED by render (fix 10). §G.8 v31 text boards on phone (item 78) —
UNCHANGED, still HELD pending parent authorization (artifact file untouched).
§G.9 pills width/min-height — FIXED by render (280×64 both). Honest note: the
phone presence "NAYA WELCOMES YOU" wraps to two centred lines at 15px inside
the 248px circle (visible, hittable, reads cleanly — screenshot) rather than
one line; and several pre-existing small sizes (presence 15px, deed 17px)
remain below the §2.3 17px floor for body text — the fix required visibility,
not a redesign of the base sizes.

## Regressions re-verified on the final files

- Slide 11 byte-identical: `SLIDES[10]` x-field sha256
  `33b0590cfb9f811a…` (same method as v1/v2 asserts). `.intel-board`
  occurrences 6, unchanged. `welcome-staged` ×0 in the agreement; `of 27` ×0.
- All 9 script blocks pass `node --check` on the final files (portal 6,
  agreement 2 including the 21,600,745 B EMBED block, identity 1).
- Redirect `welcome-redirect.html` unchanged (sha `49cfeb004d90…`).

## Per-item status, v2 (all 78 — checker's statuses carried forward, v2 changes noted)

V2 moves 11 items to DONE (3 FAIL + 7 PARTIAL + 1 DONE-in-bytes) and 1 WAITING
to FLAGGED. Counts: DONE 43 · DONE-in-bytes 9 · DONE-by-construction 1 ·
DONE/JUDGED 1 · PARTIAL 8 · FAIL 0 · WAITING 8 · FLAGGED 1 · BLOCKED 3 · NOTED 3 ·
N/A 1 = 78. (Checker headline was DONE 30 · DONE-in-bytes 13 · PARTIAL 15 ·
FAIL 3 · WAITING 9 · BLOCKED 3 · NOTED 3 · N/A 1 · DONE/JUDGED 1; the v2 deltas
above are computed from the verdict table rows.)

| # | v2 | Note |
|---|---|---|
| 1 | WAITING | Shawn's word owed. Untouched. |
| 2 | WAITING | Shawn's word owed (U4). Untouched. |
| 3 | WAITING | Dictation U1 unfinished. Slide 11 byte-identical (`33b0590cfb9f811a`). |
| 4 | DONE-in-bytes | As checker. |
| 5 | BLOCKED | Needs the real Smart Calendar image; none in this round. |
| 6 | WAITING | Captain's decision (player placement). Untouched. |
| 7 | FLAGGED | No real-audio path demonstrable (see fix 9). Synthetic branch stays. |
| 8 | NOTED | As checker. |
| 9 | NOTED | As checker. |
| 10 | DONE | As checker. |
| 11 | DONE | Deck + letter agree .94 + dim + click-through; play disc .94 + dim (fix 4). |
| 12 | DONE | As checker. |
| 13 | DONE | As checker. |
| 14 | DONE | As checker. |
| 15 | DONE | Daybar title whole at 390px (fix 10). |
| 16 | DONE | As checker. |
| 17 | DONE | As checker. |
| 18 | DONE | As checker. |
| 19 | DONE | As checker. |
| 20 | DONE | As checker. |
| 21 | DONE-in-bytes | As checker. |
| 22 | DONE | By coordinator restatement, no build (fix 7). |
| 23 | DONE-in-bytes | As checker. |
| 24 | PARTIAL | As checker (distillation not done; hard line on official text). |
| 25 | PARTIAL | As checker (read-back voice BLOCKED on item 34). |
| 26 | DONE-in-bytes | As checker. |
| 27 | DONE | As checker. |
| 28 | DONE | Letter-end bridge proven: agree visible, .94 press, N hold, live portal `#userName` focused (fix 4). |
| 29 | DONE | As checker. |
| 30 | DONE-in-bytes | As checker. |
| 31 | N/A | As checker. |
| 32 | DONE | As checker. |
| 33 | WAITING | OFFICIAL vs v3 — Shawn's hand; never harmonize (N7). |
| 34 | BLOCKED | Voice at the END; no recording exists. |
| 35 | WAITING | Shawn's hand — §4.11/C9 wording. |
| 36 | WAITING | Trigger not met. |
| 37 | DONE | Visible button "Read the agreement ◆"; long label ×0 (fix 5). |
| 38 | DONE | Pills 280×64 both on desktop (fix 10). |
| 39 | DONE | As checker. |
| 40 | DONE | As checker. |
| 41 | DONE-by-construction | As checker. |
| 42 | DONE | As checker. |
| 43 | DONE | As checker. |
| 44 | DONE | As checker. |
| 45 | PARTIAL | As checker (read-back BLOCKED on item 34). |
| 46 | DONE-in-bytes | As checker. |
| 47 | DONE/JUDGED | As checker. |
| 48 | PARTIAL | Render evidence: video-left/audio-right on the cover screen (fix 8). Choice screen stays merge-law shape; coordinator settles. |
| 49 | DONE | As checker. |
| 50 | PARTIAL | Same as 48 (fix 8). |
| 51 | PARTIAL | As checker (Hub/Academy source comparison not re-proven). |
| 52 | DONE | As checker. |
| 53 | DONE | Zero errors on 3 loads; final reader Close 8/8 (fix 3). |
| 54 | DONE-in-bytes | As checker. |
| 55 | DONE-in-bytes | As checker. |
| 56 | DONE | As checker. |
| 57 | DONE | As checker. |
| 58 | DONE | As checker. |
| 59 | DONE | As checker. |
| 60 | DONE | As checker. |
| 61 | DONE | Taken message green 19px 800, in view both widths (fix 6). |
| 62 | DONE | Phone ⓘ SELF-hittable, reader opens "1 of 12" in view (fix 1). |
| 63 | DONE-in-bytes | As checker. |
| 64 | PARTIAL | As checker (walk-certificate issuance live still unproven from staging). |
| 65 | DONE | Q1 + end buttons in view on load, both widths (fix 2). |
| 66 | DONE | As checker. |
| 67 | DONE | As checker. |
| 68 | DONE | As checker. |
| 69 | DONE | As checker. |
| 70 | DONE | Green note + "This is me" in view both widths; click → `/?walk=1&name=Shawn&alias=shawn` (fix 6). |
| 71 | DONE | As checker. |
| 72 | DONE | As checker. |
| 73 | WAITING | Ambassador Terms text — Shawn's hand. |
| 74 | DONE | Boards/frame untouched — `.intel-board` 6, slide 11 hash verified. |
| 75 | NOTED | As checker. |
| 76 | BLOCKED | Read-back audio — same as item 34. |
| 77 | DONE | As checker. |
| 78 | PARTIAL | HELD pending parent authorization — artifact file untouched; phone fit still FAILs per the checker's §F re-run (slides 10/15/28 empty, 32 overflow); retitle still unlanded. |

## Still HELD / WAITING / BLOCKED (v2)

- **HELD:** item 78 (retitle repair needs `artifact.inspect` with
  `repair_authorized:true` — parent authorization, not the maker's).
- **WAITING:** items 1, 2, 3/U1, 6, 33, 35, 36, 73 — decisions/dictations owed;
  nothing invented.
- **BLOCKED:** items 5, 34, 76 — sources that don't exist in this round.
- **FLAGGED:** item 7 — real-audio path not demonstrable (see fix 9); the
  coordinator decides whether the one-play-path law changes.
- **PARTIAL remaining:** 24, 25, 45, 48, 50, 51, 64, 78 (see table).
- **UNFOUND U1–U6** stay unfound. N7: payout timing not harmonized. Official
  sentence + ⓘ text not reworded (captain's draft awaiting his tap). D1 walk
  file untouched. Live workers/URLs untouched. School/howitworks untouched.

## Verification done by the maker (v2)

- Portal probe (`probe-v2-portal.py`, Firefox, local mirror): phone 390×844 +
  desktop 1280×900 + returning + walk both widths — all controls SELF,
  real clicks + typing, screenshots `/tmp/wsc-v2/phone-portal-v2.png`,
  `desk-portal-v2.png`, `desk-portal-returning-v2.png`,
  `walk-end-desk-v2.png`, `walk-end-phone-v2.png`.
- Agreement probe (`probe-v2-agreement.py` + `probe-v2-disc.py`,
  `probe-v2-decknav.py`, `probe-v2-cover.py`, `probe-v2-audio.py`): 3 loads
  zero errors; pills 280×64; disc + both agree buttons .94 + dim by held
  press; final reader 8/8; deck + letter click-throughs to the live portal
  with `#userName` focused; daybar title whole at 390px; cover frame
  video-left/audio-right with screenshot `agree-cover-desk-2.png`; item 7
  proven undemonstrable (direct `play()` resolves yet stays paused).
- Identity probe (`probe-v2-identity.py`, Chromium via forwarder, live
  registry): taken state green 19px 800 + note/button in view at both widths;
  "This is me" click-through; zero page errors.
- All script blocks pass `node --check` on the final files (9 blocks).
- **Not proven by render:** the walkthrough-15 certificate issuance from
  staging (live worker + device identity — provable only live, after deploy,
  as the checker recorded under item 64); anything on Shawn's own screen.
  His eye is the final gate.
