# INSPECTOR SWEEP #1 — The Whole Project Against the Language
## 2026-11-17 · Inspector seat #1 · Standing sweep

**Verdict: SWEEP COMPLETE (byte-proven) — with stated limits.** Every page in the brief was walked from served and/or filed bytes. No live VM browser exists in this seat (Firefox/Chromium dead in this VM) and no browser tasks can be launched from here, so nothing below is claimed as a live-eye check — except the Ultimate Calendar artifact, which I judged from its own audit's desktop + mobile screenshots (real rendered captures, 03:09Z), and those findings are marked EYE (capture).

**Method.** Served bytes via `curl` pipes (never written to disk); filed bytes via the git blob API with FULL SHAs (contents API returns empty above 1 MB). Counts below are literal occurrences in the bytes. Where a count alone cannot prove a visual break (e.g. CSS source order ≠ visual order), I say so and do not claim it.

**Branches moved while I worked.** Calendar obsidian-rebuild tip moved 03:01Z → 03:13:53Z (d70c9b21 → 2702a8f9); Hub icons-fix tip moved to 959781c7 (01:56:47Z, fix-4 follow-on); Smart Mail tip moved to 9b61d806 (03:16:31Z, Fix-3 round 2). I re-read the new tips; scores below are against the CURRENT tip of each branch, and I name the blob I actually judged.

**The two law-vs-law tensions (need Shawn's ruling, not a seat's improvisation):**
- **T1 — Digit tiles vs Deep Palette.** The Deep Palette supersedes the bright digit values — but Shawn's 03:02Z word restores the Dashboard's EXACT tile values verbatim ("harvest the Dashboard digit tiles VERBATIM, do not remake them"). The calendar rebuild's own filed comment records it: "The DIGIT TILES are the exception: amendment #3(4) (03:02Z, the newest word) restores the Dashboard's EXACT tile values — rim, cap, glow — verbatim." So bright digits are correct BY ORDER. The Deep Palette's digit rows need a correction note: digits are the exception.
- **T2 — The 8-pill mapping vs spectrum flow.** The Naya Code §4 prescribes the pill colors (Message green · About gold · My World orange · Skills red · Connections magenta · Invite purple · Share blue · Join NayaNET green) — green twice, order scrambled against the spectrum. DNA §1 says never the same color twice in a row, follow the flow. Both are his law. A seat cannot resolve this; it needs his word.

---

## SCORECARDS (0–10, vs the language as it stands at 03:16Z)

| Page | Score | Why it is not 10 |
|---|---|---|
| Walk / entrance — live (`/`, `/welcome`, `/identity.html`) | **5** | Bright palette only (live root 11 bright / 0 deep; `/welcome` 71 / 0); orbit 4s on live `/welcome`; `/identity.html` 35 low-opacity-white + 17 non-135° gradients; live root (620,595 B, sha 0c8628d5) is NOT the staged build (938,546 B, sha e27c7fe1) — live is behind staged. |
| Walk / entrance — staged | **5** | 8,650 visible words (minimum-text law fails); bright 313 / deep 2; 33 radial-gradient washes; 29 non-135° gradients; 9 `box-shadow:none`; pulse 1.8s + ambient 8s. |
| Dashboard — live PASS10 | **6** | Bright 1,002 / deep 16; orb-spin 2.5s; marker-pulse 2s; 173 "pulse"; gray micro-labels (`#777` 9.5px tacho, `#8a8e98`, `rgba(255,255,255,.6)`); 34 `box-shadow:none`; 306 inset-top-light (superseded pattern); 347 non-135° gradients; 940/840px max-width cages; voice play chips (NayaMedia). Digits are canonical — not counted against it. |
| Dashboard — staged done-done Fix-2 | **6** | Same defects as live (bright 1,073 / deep 25; same gray, same fast motion, same flat spots) in a bigger file (1,943,088 B). Fix-2 did not move the language breaks. |
| Personal — formats tip 925a4340 | **5** | Worst bright:deep ratio in the network (1,725 / 29); `#0B0D12` inherited from the Hub feed root + a `160deg … #0b0d12` dialog; `--muted: #AAB2BF`; second green `--emerald: #51c78b`; `#888` "Actions loading…" fallback; `#777` tacho labels; voice-note play buttons (`mn-play ▶` + waveform); 5,293 words; 201 emoji. |
| Personal — feed-posts branch | **5** | Same as the formats tip (bright 1,691 / deep 40; `#0B0D12` ×3; same voice buttons; same gray fallbacks), 5,068 words. The feed work did not touch the language breaks. |
| Hub — live | **4** | `--bg: #0B0D12` is the canvas (DNA §2 names this exact value a defect) — and the file's own comments cite the law against it; `#888` 12px "Actions loading…" fallback; `#aaa` noscript text; orbSpin 4s, livepulse 2s, notifpulse 2.4s; read-aloud voice buttons (`.naya-voice-btn` + NayaVoice contract); `<title>` says "Intel Today", not the Hub; 60 radial washes; bright 173 / deep 18. |
| Hub — staged (fix-4 follow-on, tip 959781c7) | **7** | Palette fixed (deep 420 / bright 29) — the best palette repair in the network. But the gray/voice/`#0B0D12` defects are still IN the bytes, hidden at runtime by `!important` overrides (`.naya-voice-btn{display:none}`, `body{background:#050607}`, `[style*="0B0D12"]…`) — masked, not removed. orbSpin 4s remains; 58 washes remain. |
| Pricing — live v77 | **6** | Bright 348 / deep 52 (digits canonical, everything else bright); orb-spin 2.5s; ib-orb-flow 1.6s/2.8s; `#777` tacho labels; 63 inset-top-light; 74 non-135° gradients; 79 max-width; 5,351 words; 86 emoji. |
| Pricing — staged v78 | **6** | Identical language profile to v77 (bright 354 / deep 52; same fast motion, same gray, same cages). The v78 diff is the free-entry button only — the language breaks are untouched. |
| Pricing — /free | **5** | Same file family as `/identity.html`: 35 low-opacity-white; 19 inset-top-light; 17 non-135° gradients; bright 9 / deep 0. Served sha has DRIFTED since the brief record (now dfe70a8c, 310,212 B; brief recorded e0534a61, 307,918 B) — redeployed, unrecorded. |
| Pricing — /free/walk | **5** | Bright 100 / deep 0; orbit 4s; 1,578 words; 136 buttons. Served sha DRIFTED (now 2370eae2, 3,292,257 B; brief recorded ea1e77a6, 3,288,471 B). The build-step stall (~6 min, no progress/error/timeout; `/api/welcome/me` → `{"ok":false,"error":"unknown api"}`) is the eye's finding, carried here, not mine. |
| Smart Mail — staged (tip 9b61d806, blob 6bc58b80) | **8** | Best in the network on palette (0 bright / 78 deep), zero gray, zero `box-shadow:none`, dock orbit 60s/75s (correct slow). Why not 10: notifPulse 2.4s scale pulse on the notification dot; the cover is a purple/magenta/blue radial wash over a purple gradient background (colored background — DNA §2/§4); 27 non-135° gradients; 19 inset-top-light. |
| Calendar — Obsidian rebuild (tip 2702a8f9, blob b3e6acfb = staged 3cca6639) | **7** | Best-built page in the sweep: 0 gray, 0 voice, 0 pulse; deep palette in code (bright values survive only in comments + the canonical `$` tile `#ffbf3d`); 13 doors in 10-hue spectrum flow, no adjacent repeat; digit tiles verbatim Dashboard; no trailing days, no trailing blank row; white info eye. Why not 10: NO orbit/rotation anywhere (animation 2, keyframes 1, rotate 0 — Naya Code §8 circles-have-flow unmet); month view capped at max-width 1060px; leading blank cells flat/transparent with `box-shadow:none`; meet leg in code, never eye-proven; **plus B19 (03:19Z elegance law, landed during the sweep): weekday header renders SHORT names (Sun/Mon) in their day's color via inline style — not full Marcellus names — and the info eye is still the outline-eye SVG, not the pearl/diamond circle with "i".** |
| Calendar — vision artifact `the-ultimate-calendar` (audit 03:09Z) | **5** | Digits verbatim Dashboard (correct), numbers top-left (correct), white eye bottom-right (correct), rims lit at rest (correct). Breaks (EYE, capture): trailing 6th row of 7 EMPTY cells; empty cells carry gray `#888` rims; year "2026" in gray `#8b8b9c`; weekday letters in small COLORED text; 180° cell gradients; 13 door colors are 13 invented bright hexes (0 Deep Palette), Weather `#3ec6f8` exactly repeats Appointments; Notes door `#dfe3ee` near-white; todaypulse 3.2s; on mobile the cells become tall VERTICAL rectangles (DNA §5). **Plus B19:** single-letter weekday header (not full Marcellus names), outline eye (not pearl/diamond circle with "i"), numbers not shrunk. The rebuild already fixes most of this — the artifact is superseded as the vision. |
| Formats — unfold 34c756ff / slideshow 21d08a88 | **6** | 0 gray, 0 voice, minimal words (189/195 — the best text discipline in the network). Why not 10: bright-only palette (58 bright / 0 deep each); max-width 980/940px wrappers (DNA §6 full width); a flat subtitle board (`box-shadow:none`); speakPulse 1.6s; zero orbit flow. The canonical formats themselves predate the Deep Palette and need the deepening pass. |

---

## EVERY BREAK (page + spot + law broken + fix)

### B1 — Bright-palette drift, network-wide (the biggest break)
- **Pages:** Personal (1,725 bright / 29 deep) · Dashboard live 1,002/16, staged 1,073/25 · Walk staged 313/2 · Pricing v77 348/52, v78 354/52 · `/welcome` 71/0 · `/free/walk` 100/0 · Formats 58/0 each · Hub live 173/18.
- **Law:** The Deep Palette (01:30Z) — one hex per hue, deep not neon; bright spectrum values superseded. **EXCEPTION (T1): digit tiles stay Dashboard-exact by Shawn's 03:02Z word — do not "fix" the digits.**
- **Fix:** One palette pass per page (or one shared token pass): replace every live bright hex (`#a06bff #3fb8ff #2fe89e #ffbf3d #ff9a5a #ff5e6c #e84fff #7fd4ff #3a5bff #31cb8d #6675ff`) with its deep hex in rims, buttons, orbs, chips, glows — leaving digit-tile values and the deck's nine colors alone. Byte-proven counts.
- **Evidence:** byte counts above. Smart Mail (0/78) and the Calendar rebuild (deep in code) prove the pass is doable.

### B2 — Fast ambient motion, 8 of 9 surfaces
- **Spots:** orb-spin 2.5s (Dashboard, Pricing, Hub) · orbit 4s (live `/welcome`, `/free/walk`, Hub orbSpin 4s) · marker-pulse 2s, check-glow 2.5s, ctrl-pulse 4s (Dashboard) · ib-orb-flow 1.6s/2.8s (Pricing) · speakPulse 1.6s (Formats) · notifPulse 2.4s (Hub, Smart Mail) · livepulse 2s (Hub) · todaypulse 3.2s (artifact) · pulse 1.8s + ambient 8s (Walk) · jewel-breathe 3s, porb 5s (Dashboard).
- **Law:** Playbook — ambient 60s+, active 18–25s, never faster than 12s. (Entry animations under 1s are fine and are not counted here.)
- **Fix:** Slow every ambient rotation/pulse to 60s+ (orbit 60–180s), active to 18–25s. The Smart Mail dock orbit (60s/75s) is the model. Byte-proven.

### B3 — Hub live: `#0B0D12` is the canvas
- **Spot:** Hub live `:root { --bg: #0B0D12; --bg-raise: #12151D; … }` — the page background. The same file's comments cite "Law 2 — the background is obsidian #050607, never #0B0D12".
- **Law:** DNA §2 — background `#050607`, "NOT `#0B0D12` (old tinted — defect)".
- **Fix:** `--bg: #050607`, `--bg-raise` to a true obsidian raise. Byte-proven. (Also inherited into Personal's `.ib-feed-root` — B5.)

### B4 — Hub staged: violations masked, not removed
- **Spot:** Hub staged (tip 959781c7) injects a runtime law-style: `.naya-voice-btn{display:none !important}`, `body{background-color:#050607 !important}`, `[style*="0B0D12"]…` — while `#888`, `#aaa`, `--bg:#0B0D12`, and the voice-button code all remain in the bytes.
- **Law:** The fix is the fix; a runtime `!important` blanket is a cover-up. A future edit that drops the override resurrects every defect at once.
- **Fix:** Delete the defect lines themselves (gray fallback, noscript gray, `#0B0D12` root, voice-button code), then delete the override layer. Byte-proven.

### B5 — Gray text (byte-proven instances)
- **Spots:** Hub live + staged + Personal: `<span style="color:#888;font-size:12px">Actions loading…</span>` (JS fallback in the harvested feed) · Hub noscript `<p style="color:#aaa4b1">` · Dashboard/Personal/Pricing gauge SVG `.tn-tacho-bandlo,.tn-tacho-bandhi{fill:#777}` (9.5px) + `fill:#8a8e98` + `fill:rgba(255,255,255,.6)` labels · Personal `--muted: #AAB2BF` · Artifact year `color:var(--dim)` where `--dim:#8b8b9c` · Walk staged fallback `background:var(--nc,#888)` (fallback only, not text).
- **Law:** Design Language §6 + DNA §9 — NO gray text at any size; white or bright high-contrast.
- **Fix:** White for every instance above; delete the gray fallback strings. Byte-proven. (Identity `/free` 35 low-opacity-white hits need the same treatment — see B13.)

### B6 — Voice play buttons present (DNA §14: OFF)
- **Spots:** Dashboard — NayaMedia "custom play + seeded waveform + duration" voice chips · Personal — `mn-play` button `aria-label="Play the voice note"` + waveform · Hub — `.naya-voice-btn` read-aloud buttons + NayaVoice playback contract · Walk `/welcome` — `STEP_AUDIO` mp3s + `playFromEye` step audio.
- **Law:** DNA §14 — "Voice play buttons OFF — boards and top."
- **Fix:** Remove the play-button controls (keep audio as a capability behind an explicit ask, per the DNA). Byte-proven presence; exact on-screen placement is eye-unconfirmed.

### B7 — Artifact: trailing blank row + gray-rimmed empties (EYE, capture)
- **Spot:** The Ultimate Calendar audit screenshots (desktop + mobile): November 2026 renders a 6th row of 7 EMPTY cells; the empty cells' rims are gray (`--dc: #888` default in code).
- **Law:** Shawn 02:58Z — no trailing next-month days, no trailing blank row; no gray.
- **Fix:** Grid ends at the month's last day (the rebuild already does this — harvest its grid code). EYE (capture) + byte-proven (`--dc:#888`).

### B8 — Artifact: colored micro-text + gray year (EYE, capture)
- **Spots:** Weekday letters S M T W T F S in 10–13px COLORED text (`color:var(--dc)`); year "2026" in `#8b8b9c`.
- **Law:** DNA §9 + Design Language — white text always, never colored text, never gray.
- **Fix:** Weekday letters white; year white. EYE (capture) + byte-proven.

### B9 — Artifact: 13 invented door colors, one exact repeat (EYE + bytes)
- **Spot:** Artifact `DOORS`: Appointments `#3ec6f8`, Local `#2fe6a7`, Provincial `#ffb03a`, Global `#6a7cff`, Personal `#a678ff`, Business `#f5c81e`, Thing `#ff7a29`, Your World `#9a5cff`, Smart Notes `#ffd23c`, Notes `#dfe3ee`, Weather `#3ec6f8` (= Appointments, exact), Horoscope `#f06ae0`, Posts `#ff4d8d`. Zero Deep Palette hexes; two bright yellows, two pinks; Notes is near-white.
- **Law:** Deep Palette (one hex per hue) + spectrum flow, never the same color twice in a row (Shawn 03:01Z).
- **Fix:** Re-color the doors from the Deep Palette in spectrum-flow order — the rebuild's door array already does this; harvest it. Byte-proven.
- **Note:** The rebuild's doors (d70c9b21) were NOT in flow order; the new tip (2702a8f9) fixed them. The artifact was never re-cut after that fix.

### B10 — Light from the wrong direction (hundreds of gradients)
- **Spots:** Non-135° gradients — Dashboard 347, Personal 405, Hub staged 88, Pricing 74, Walk staged 29, `/identity.html` 17, Smart Mail 27, artifact cells `linear-gradient(180deg,…)`. Includes 90°/105°/145°/155°/160°/168°/180°.
- **Law:** Playbook + Design Language — one light, top-left, always; every gradient 135°, shadows down-right.
- **Fix:** Re-angle material gradients to 135°. (Scrim/overlay gradients that darken for legibility are the only candidates for exception — a seat must name each one, not blanket-keep them.) Byte-proven counts; per-gradient visual judgment is eye work.

### B11 — Flat elements + the superseded inset top-light
- **Spots:** `box-shadow:none` — Dashboard 34, Personal 37, Pricing 4, Hub 5, Formats 2 (flat subtitle board), Calendar 2 (blank leading cells). `inset 0 1px 0 rgba(255,255,255,…)` — Dashboard 306–312, Personal 384, Pricing 63, Hub staged 46, Walk staged 11, Smart Mail 22, `/identity.html` 17.
- **Law:** DNA §4 elevation everywhere, nothing flat; Design Language §6 — the Playbook inset top-light is OUT inside icons/buttons.
- **Fix:** Give every flat element elevation; remove the inset white wash inside icons/buttons (keep the outside rim). Byte-proven. (The Formats' flat subtitle board and the Calendar's transparent blank cells are the two named spots; the rest need an eye pass to separate intentional resets from dead elements.)

### B12 — Max-width cages (DNA §6: full width)
- **Spots:** `.previewzone{max-width:940px}`, `.laptop{max-width:840px}` (Dashboard + Personal, shared code) · Formats wrappers 980/940px · Calendar month view 1060px · Hub 117–122 `max-width` occurrences (mostly media queries — the constraining ones need naming) · Walk staged 75 occurrences.
- **Law:** DNA §6 — no max-width constraining content, fill the screen.
- **Fix:** Remove constraining wrappers; keep media-query breakpoints (those are not cages). Byte-proven counts; the exact cage list per page is eye work.

### B13 — Low-opacity white text on Identity / Free
- **Spots:** `/identity.html` and `/free` (same family): 35 `rgba(255,255,255,0.0–0.4)` hits each, plus 17 non-135° gradients and 19 inset-top-light each.
- **Law:** No gray text — low-opacity white IS gray at small sizes.
- **Fix:** White at full opacity for text; keep low opacity only for non-text decoration, named per instance. Byte-proven count; per-instance visual check is eye work.

### B14 — Text volume (minimum text, speak in icons)
- **Spots:** Walk staged 8,650 visible words · Personal 5,293 · Pricing 5,351 · `/free/walk` 1,578 · Dashboard 1,463–1,474 · Smart Mail 980 · Formats 189/195 (the model).
- **Law:** DNA §9 + Naya Code — minimal words, visuals over text, icons over labels.
- **Fix:** Distill per page to the Formats' density (nutshell boards, one idea each). Counts are byte-proven; what to cut is a reader's judgment (eye).

### B15 — No orbit flow where the law requires it
- **Spots:** Calendar rebuild — 0 rotations (animation 2, keyframes 1, rotate 0) · Formats — 0 "orbit" · Walk root — orbit present but at 4s (see B2).
- **Law:** Naya Code §8 — circles have flow around them, slow (60–180s ambient), alternating direction.
- **Fix:** Add slow concentric flow to the calendar day jewel, the format orbs, and the walk's circles — at 60s+, never 4s. Byte-proven absence (word + keyframe counts).

### B16 — Hub live title is wrong
- **Spot:** Live Hub `<title>Intel Today — the daily digest of NayaNET's smart notes</title>`; staged Hub says "Smart Feed — NayaNET".
- **Law:** The page should name itself (presentation standard; the Hub is the Hub).
- **Fix:** Title the live Hub as the Hub. Byte-proven. (Minor.)

### B17 — Free-route drift + walk stall (recorded, not re-proven)
- **Spots:** `/free` served sha dfe70a8c (310,212 B) vs brief record e0534a61 (307,918 B); `/free/walk` served 2370eae2 (3,292,257 B) vs brief record ea1e77a6 (3,288,471 B). The free walk's build step stalls ~6 min with no progress/error/timeout; `/api/welcome/me` returns `{"ok":false,"error":"unknown api"}`.
- **Law:** The record must tell the truth; a build step must fail loudly, never hang silently.
- **Fix:** Re-record the current SHAs; wire the welcome API into the free worker (or point the walk at the working backend) + visible progress + timeout + readable error. SHAs byte-proven; the stall is the eye's finding, carried here.

### B19 — The Elegance law (03:19Z, landed DURING this sweep — applies to both calendar surfaces)
- **Shawn's word (03:19Z):** "Look at the front entrance — the elegance, the beauty of the colors, how they all complement each other. The calendar must learn from it: the weekday header must say the FULL day names (Sunday, Monday...) written almost in royalty, in the most incredible font, a font of the quality that matches the numbers (Marcellus). The info eye becomes a CIRCLE — a real element coming off the page, pearl/diamond, with a little "i" inside so people know to click it for the day's info. The numbers get smaller (~25%, he floated half) so the page breathes and looks bigger and more elegant — the cells can't get bigger, so the numbers shrink. Less busy, less colorful, more elegant, high-tech beautiful; the light more on the SIDE (rim), not the middle."
- **Spots:** Artifact — weekday header is single letters S M T W T F S in small colored text (EYE + bytes: `.weekrow span{color:var(--dc)}`); eye is an outline-eye SVG; numbers are large tiles (EYE). Rebuild (tip 2702a8f9) — weekday header renders SHORT names via `$('weeknames').innerHTML=WEEKDAY.map(w=>`<div style="color:${w.color}">${w.short}</div>`)` — "Sun/Mon" in the day's color, inline style (byte-proven); eye is the harvested outline-eye SVG (`.plan-eye`, `EYE_SVG` almond outline), not a circle with "i" (byte-proven); numbers are the 34px Dashboard tiles verbatim — the ~25% shrink is not in the code (eye to judge the rendered size).
- **Also byte-proven in the rebuild:** a second `.plan-eye` rule sets `top:6px;right:6px` (vs the desktop `top:auto;bottom:10px;right:10px`) — if that rule is the small-width one, the eye moves back to top-right on narrow screens; the media context was not confirmed in this pass.
- **Law:** The Elegance law (03:19Z) + no-colored-text + rim light.
- **Fix:** Full day names in Marcellus, white/royal; replace the outline eye with a pearl/diamond circle carrying "i"; shrink the number tiles ~25%; keep the light on the rim.
- **Marcellus open check (walk):** "Marcellus" mentions — staged walk worker 11, `/free/walk` 4, live `/welcome` 0. Mentions are not proof the family loads and applies; the brief record says the F4 copy lost it. Eye to verify which walk surfaces actually render Marcellus.

### B18 — Emoji as icons (minor, eye to confirm)
- **Spots:** Emoji glyph counts — Personal 201, Dashboard 149–159, Pricing 86, Hub staged 43, Hub live 34.
- **Law:** Design Language — the white glyph is a real object, readable and purposeful; speak in icons.
- **Fix:** Replace emoji with the white object-glyphs where they stand in for icons. Count byte-proven; which ones are icons vs content is eye work.

---

## RANKED WHOLE-NETWORK LIST (worst first)

1. **B1 — Bright-palette drift everywhere except Smart Mail + Calendar rebuild** (Personal 1,725 · Dashboard ~1,000 · Walk 313 · Pricing ~350 · Formats 58×2 · Hub live 173). One shared token pass fixes most of it.
2. **B2 — Fast ambient motion on 8 of 9 surfaces** (2.5s orb-spin, 4s orbits, 1.6–3.2s pulses). The Playbook's slowest law, broken the most places.
3. **B3+B4 — Hub's `#0B0D12` canvas, live + the staged mask** (defect in bytes, hidden by `!important` on staged). The only DNA-named defect value, still live.
4. **B6 — Voice play buttons on 4 surfaces** (DNA §14) — Dashboard, Personal, Hub, Welcome.
5. **B5+B13 — Gray / low-opacity-white text** (`#888` fallback, `#aaa` noscript, `#777` 9.5px gauge labels, `#8b8b9c` year, `--muted #AAB2BF`, 35 low-opacity hits on Identity/Free).
6. **B7+B8+B9 — The artifact's month grid** (trailing blank row, gray rims, colored weekday letters, gray year, 13 invented door colors with an exact repeat) — the most visible single page to Shawn's eye, and already fixed in the rebuild; the artifact needs re-cutting, not a new design.
7. **B19 — The Elegance law (03:19Z)** — full Marcellus day names, circle-"i" eye, smaller numbers: missing on BOTH calendar surfaces (rebuild: short colored names + outline eye; artifact: single colored letters + outline eye + large numbers).
8. **B10 — Light from the wrong direction** (347 Dashboard, 405 Personal, 88 Hub, 74 Pricing gradients off 135°).
9. **B11 — Flat elements + superseded inset top-light** (34/37/4/5/2/2 `box-shadow:none`; 306–384 inset washes).
10. **B12 — Max-width cages** (940/840/980/1060px wrappers vs DNA §6 full width).
11. **B14 — Text volume** (Walk 8,650 words; Personal 5,293; Pricing 5,351).
12. **B15 — No orbit flow** (Calendar rebuild, Formats; Walk's orbit is 4s-fast).
13. **B17 — Free-route drift + walk stall** (SHAs unrecorded; silent hang).
14. **B16 — Hub live title says "Intel Today".**
15. **B18 — Emoji standing in for object-glyphs.**

## What is NOT a break (corrections to my own first pass)
- **Digit tiles are bright BY ORDER** (T1). The Dashboard's `#ff2a2a/#ff8c00/#f5d76e/#00a86b/#29b6f6/#b388ff/#ff1493` reels, Pricing's chart tiles, the Calendar rebuild's tiles, and the artifact's tiles are all the same canonical values — harvested verbatim, correct. Do not "deepen" them.
- **The Calendar rebuild's bright hexes are comments only.** In blob d70c9b21 the 7 bright values appeared only in supersession comments; the new tip b3e6acfb keeps exactly one live bright hex, the canonical `$` tile `#ffbf3d`. The rebuild is the palette model for the network.
- **Hub staged served bytes DO match the filed blob** (4,873,750 B, sha 340b1326b7d3) once the branch tip is accounted for (959781c7, fix-4 follow-on). The earlier size gap was a moved tip, not a serving error. Same for the Calendar rebuild (71,440 B, sha 3cca6639 = new tip b3e6acfb).
- **The 8-pill colors are canonical per the Naya Code §4** (T2) — the spectrum-flow tension is a ruling owed, not a seat-level break to "fix" by recoloring.

## What I could NOT inspect and why
- **No live eye on any page.** No VM browser (Firefox/Chromium dead in this VM) and no browser-task launch from this seat. Every "visual" claim above is either byte-proven or, for the artifact only, from its audit screenshots. Hover-alive, lift, elevation-feel, clipping, overflow, and the five-icon bottom bar on every page all need a live eye — I did not claim them.
- **The toolbar duplication** (Walk screenshot, first in Shawn's batch) — a screenshot judgment; cannot be verified from bytes. Eye owed.
- **Rim/door spectrum order as SEEN** — my rim-sequence counts come from CSS source order, which is not visual order; I did not use them as proof. The door orders I report come from the actual `DOORS` arrays (Calendar rebuild, artifact) — byte-proven.
- **Hub staged vs the brief's blob** — resolved (moved tip, see above).
- **Smart Mail's mail-by-world, IM toggle behavior, and clipping** — function checks, need the eye; bytes show the code present and the palette clean.
- **The free walk's build stall** — carried from the eye's record (02:35Z+), not re-proven here.

## Receipts (what was actually read)
- Standards read in full: THE-NAYA-CODE.md, THE-NAYA-DESIGN-LANGUAGE.md, THE-DEEP-PALETTE.md, THE-PLAYBOOK.md, DESIGN-INTELLIGENCE-REPORT.md, DNA (blob 092c3123164ce4cde352a11ac6960057363668c0, 4,475 B).
- Live: nayanet.app/ (620,595 B, sha 0c8628d5) · /welcome (97,807 B, sha 98cb6414) · /identity.html (307,759 B, sha bdd8af83) · /hub (4,678,679 B, sha bfbd895a) · /dashboard (1,817,928 B, sha bb41114d) · /pricing (11,355,594 B, sha b043167b = v77).
- Staged: walk worker / (938,546 B, sha e27c7fe1) · Dashboard Fix-2 proof-host (1,943,088 B, sha e4e098be) · Personal formats tip (3,209,315 B, sha 962159fd) · Personal feed-posts (3,227,948 B, sha be032b3b) · Hub staged (4,873,750 B, sha 340b1326 = tip 959781c7, blob fd802b03) · Pricing v78 worker (11,360,503 B, sha ca2eafeb) · /free (310,212 B, sha dfe70a8c) · /free/walk (3,292,257 B, sha 2370eae2) · Smart Mail staged (92,502 B, sha acab5ca1; new tip blob 6bc58b80, 92,840 B, sha 23cdcf30).
- Filed via blob API: DNA 092c3123… · Calendar rebuild d70c9b21 blob 1a422801 (65,883 B, sha 53ba8307) and new tip 2702a8f9 blob b3e6acfb (71,440 B, sha 3cca6639) · Unfold 34c756ff… (32,079 B, sha 70abc8e9) · Slideshow 21d08a88… (34,896 B, sha fcfa0c4c) · Hub new-tip blob fd802b03 (4,873,750 B, sha 340b1326) · Smart Mail new-tip blob 6bc58b80 (92,840 B, sha 23cdcf30).
- Artifact: `the-ultimate-calendar` index.html (45,340 B, sha 8b7295b0) + audit 2026-11-17T03-09-28Z screenshots (desktop + mobile, read visually).
