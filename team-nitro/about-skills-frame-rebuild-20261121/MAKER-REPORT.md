# MAKER REPORT — About + Skills FRAME REBUILD (One-Build Law)

Maker seat, coordinator 7f3f2b73-4510-45c7-b703-44e8467ff48f. Built 2026-11-21. Report to the coordinator, not to Shawn.

## What was built

One file, one build, from the frame that already works: the Collective Agreement unfold
(`team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html`, blob `1f0b0474`,
142,532 B — re-verified by git blob sha + size this round; local copy
`src-agreement-unfold-fixed.html` matches byte for byte). **No new layout, no new structure,
no additions.** No extra `<style>` block, no extra scripts, no pricing code anywhere
(the word "pricing" occurs once in the file, in the header comment stating there is none).

- **Deck: 28 frames, one deck** — About 1–9, Skills 1–14, About 10–14. A second deck is
  impossible without new scripts (wireDeck/wireFrame hardcode `#deckBody`), and a 14-beat
  deck cannot also hold 14 skill slides, so this is the only design with zero new CSS/JS
  where every control works.
- **Skills are the agreement's own deck** — the pricing-harvested `#skillsSlideshow` is
  gone; the 14 skill slides are agreement beats (kind `SKILL N`, same topbar face, same
  pinned foot, same progress pill).
- **All 28 beats are the agreement's own text beats** (`fp-noslide`, no showcase figure).
  The frame's picture is the topbar face at top; text is the middle.
- **Tones cycle by deck position** through the agreement's 10-deep spectrum, never twice
  in a row (the agreement's own rule). **Beat photos cycle the agreement's 8 FACES** by
  deck position, so blocktop photo and topbar agree per frame.

## Filed

- Branch: `about-skills-frame-rebuild-20261121`
- Commit (page + build script): `e8cdf13a350955051985aab2e1bf219164ec1930`
  (parent: main `3746bc9d20a00ba5071a24a8b6c3ba40075a950c`, fetched live)
- Page: `team-nitro/about-skills-frame-rebuild-20261121/about-skills.html`
  - Blob `461802986c46e7715cc91b1814e69fdbd0735a9e`, **137,228 B**,
    sha256 `f1ee4facfd1508f77764fa7a19ac378abaf262eb31108bdc97fbfc083bd7fc8f`
  - Blob read back by the blob API: size + sha256 match exactly.
- Build script blob `8d965558587ba8d1f0d962f59bf87d668ef051ae`
  (`build-about-skills-frame.cjs`, 16,220 B — deterministic: two consecutive runs,
  same sha).
- **Staged link (verified first-hand, HTTP 200, 137,228 B, sha256 match):**
  https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/about-skills-frame-rebuild-20261121/about-skills.html&ref=about-skills-frame-rebuild-20261121&cb=461802986c46e7715cc91b1814e69fdbd0735a9e

## Proof 1 — the frame diff (read in full, all 231 lines)

`frame.diff` in this lane dir: `diff -u` of the agreement source vs the built file,
**+67/−91**. Every hunk is one of the ordered substitutions, nothing else:

- Header comment + `<title>` rewrite; one comment word removed ("nothing gray" → the
  source file FAILs its own machine checker on that word; the one-word fix is the
  previous build's precedent).
- Header labels: steplabel, deal-title, deck-sub, playTip, foot-links
  ("The Collective Agreement" → "About Shawn Vibert").
- Deck replacement: 37 agreement articles → 28 frames (see above).
- PLAY script: 15 agreement paragraphs → 6 About paragraphs, verified identical to
  the previous build's PLAY array.
- Playing-state tip string (`setState`): 'Naya will talk you through this page' →
  'Shawn will talk you through his story' — the same visible label as the static tip,
  otherwise the label flips to agreement wording while playing.
- wireFrame7 fallback labels: 'The Collective Agreement' → 'About Shawn Vibert'.
- Media-frame labels: 'Listen to the agreement' → 'Listen to my story';
  '▶ Watch the anthem ◆' → '▶ Watch — my story ◆'; anthem note shortened to
  'The video is on its way.'
- No CSS rule changed, no script changed except the strings above, no markup outside
  the deck changed. `aboutSkillsAdditions`: 0. `skillsSlideshow`: 0. `gray`: 0.

## Proof 2 — content fidelity (programmatic, not eyeballed)

- About 14 beats: text-verbatim vs the previous build (blob `33e0f288`), allowing only
  the ordered date change (About 11: "20 November 2026" → "21 November 2026") and the
  beat-9 button relabel. Confirmed by normalized-text comparison of all 14 beats.
- Skills 14 slides: every content field verified present in its frame — head, sub,
  means, diff, ex, why, foryou, status, proof label + proof URL (11 links) or the
  verbatim "Proof owed…" note (Meet, Match, Access). Harvest order verified by name
  in the build script (`HARV[i].title === sk.name`, throws otherwise). The harvest
  `nutshell` field is metadata, not slide content — it appears verbatim in neither
  the previous build's slides nor these; head + sub carry its words.
- PLAY: 6 paragraphs, byte-identical to the previous build.
- Statuses as harvested: 3 PRODUCTION-PROVEN, 9 DEMONSTRATED, 1 DEMONSTRATED —
  STAGING-PROVEN (Match), 1 DECLARED (Meet). Nothing upgraded, nothing invented.

## Proof 3 — render (Chromium, real Marcellus + Outfit, via the localhost proxy)

Fonts proven real before trusting any fit number: `document.fonts.check('25px Marcellus')`
true, and "About Shawn Vibert" at 25px measures 226.4px in Marcellus vs 205.4px in
fallback serif. (The Google Fonts CSS itself fails in this VM with
ERR_CERT_AUTHORITY_INVALID — a probe artifact; the installed TTFs render instead.
Images all load: face portraits naturalWidth 1408.)

**Navigation:** all 28 frames advance with the page's own buttons, pill counts
1 / 28 → 28 / 28. Frame sits whole in the viewport at both widths (phone frame
bottom 669/844, desktop 918/1080 — identical to the agreement source's own numbers).
**Zero horizontal overflow on any frame at either width.**

**Desktop 1920×1080:** 26 of 28 frames fit whole with zero inner scroll. Only Skill 8
(Match) and Skill 11 (Access) overflow by 30px each — one line. The two longest
skill texts.

**Phone 390×844:** the text board scrolls inside `.frame-scroll` on every frame —
About beats 66–336px, skill slides 802–1030px. This needs the control, run the same
way on the agreement source: **the source itself scrolls inside on all 37 beats,
28–464px** (beat 1: 266px; worst beat 37: 464px). The inner scroller is the frame's
own designed behaviour (`overflow-y:auto` by design), not a defect I introduced —
but the skill slides scroll roughly 2–3 screens inside a 360px window, about twice
the source's worst beat. That follows directly from the brief's combined orders
(verbatim 6-row skill text + agreement frame + no additions); no maker-level change
can fit ~1,200px of text into a 360px window without cutting words or adding CSS,
both forbidden. **This is the captain's decision, not a hidden defect: accept the
scroll, split each skill across two frames, or shorten the skill text.** I did not
decide it, and I did not hide it.

**Design-laws checker:** `check-design-laws.py` → PASS, no machine-checkable
violation (2 warnings, both §2.2 text-colour eye-checks on agreement-harvested code:
the `--tone` inheritance and `color:transparent`). Eye-checks done by reading the
screenshots as a reader: frames 1, 2, 9, 10, 14, 23, 24, 28 at phone; 1, 9, 10, 24,
28 at desktop. Screenshots in this lane dir (`shot-phone-*.png`, `shot-desktop-*.png`).

## Two bugs found by the render check, both fixed in the build (not patched after)

1. **Double diamonds.** First build wrote "Keep reading ◆ ◆" — my label replacement
   kept the template's trailing entity while adding one. Fixed in the build script
   (labels carry no entity; the template's supplies the single ◆). Final: 26×
   "Keep reading ◆", 1× "See all my skills ◆", 0 doubles.
2. **The last frame's climax was below the fold (the real find).** First build put
   the "Enter NayaNET" anchor at the end of beat 28's article, so wireFrame7 sorted
   it into `.frame-scroll` — at phone width it sat below the fold behind a DEAD
   "Keep reading" button (wireFrame8 clamps the last frame's advance, so the button
   did nothing). Fixed with the agreement's own mechanism, exactly as its F7 comment
   states it: the final frame's climax button moves into the pinned foot, beside
   Back, "so the climax action is never below the fold". Beat 28 now carries
   `<a class="p3-enter deal-agree-btn" id="dealAgreeBtn" href="https://nayanet.app/">Enter NayaNET ◆</a>`
   and NO Keep-reading button — mirroring agreement beat 37, which also has no
   Keep-reading button. Live proof: frame 28's foot reads `‹ Back ◆` + `Enter NayaNET ◆`,
   Enter rect top 592 / bottom 653 (pinned, in view); **clicking Enter navigated to
   https://nayanet.app/** (page loaded, assets requested) — the anchor's href wins;
   wireAgree's delayed bridge hop never fires once the page unloads. The Enter text
   renders underlined, as the agreement's own links do (it is an anchor, where the
   agreement's was a button).

## Deviations from the brief, named plainly

1. **Pill reads "N / 28", not "N / 14".** The brief's parenthetical assumed a 14-beat
   deck, which cannot hold the Skills run. The pill code stays byte-identical
   (auto-counts via MutationObserver); 28 is what it counts.
2. **Beat 9's Keep-reading button is relabelled "See all my skills ◆"** — it advances
   into the Skills run using only agreement mechanics. (A second `.deck-next` on one
   beat would be dropped by wireFrame7, which keeps only the last; a non-deck-next
   jump button would be dead with no JS to wire it.)
3. **Beat 28 has no Keep-reading button and its climax is `#dealAgreeBtn`** (see bug 2
   above). The agreement's own last beat is built the same way.
4. **`.ib-rows` / `.ib-row-k` labels are unstyled** — they have no CSS in the agreement
   source (they were styled only by the forbidden additions block), so rows render as
   plain white paragraphs with unstyled labels. That is the frame as harvested.
5. **wirePlay aria-labels left unchanged** ("Play — read the agreement with Naya") as
   harvested player chrome — changing them would invent wording. Flagged for the
   captain, not decided here.
6. **Dead `article[data-beat="37"]` phone rule kept byte-identical** (inert; no beat
   37 exists). Not mine to clean.

## Still owed (not mine to decide)

- **Portrait decision** (Naya's face / Shawn's photo / monogram) awaits Shawn. The
  agreement's face-*.jpg are used verbatim, exactly as the frame does.
- **Phone skill-slide scroll** (802–1030px) — captain's call: accept, split, or shorten.
- **wirePlay aria-labels** (item 5 above).

## Files in this lane dir

- `BRIEF.md` · `build-about-skills-frame.cjs` · `about-skills.html` · `frame.diff`
- `file-about-skills-frame.cjs` (filing script) · `render-probe.py` (+ `.cjs` first attempt)
- `shot-phone-*.png` / `shot-desktop-*.png` (render evidence)
- `MAKER-REPORT.md` (this file) · `proxy.log`
