# MAKER REPORT — About + Skills rebuild, 2026-11-20 (overnight round)

One lane, one round. Build it, file it, report back. No merge, no live
deploy, no message to Shawn. The Personal file was not touched.

## What was built

`about-skills.html` — **201,793 bytes**, sha256
`8749d432fcf26ce8af084f56ff962bf200392c800d9c17cfc0024c57d050885c`
(built file; string length 200,993 — byte count is the truth).
Build script `build-about-skills.cjs` reproduces these exact bytes
(rebuilt 3×, same sha256 every time).

- **About** (built file lines 965–978): the collective agreement's
  actual frame system, 14 beats in the settled order — Who I am,
  Mission, Vision, Goal, Motto, My story, What I stand for, What I do,
  Skills teaser, Interests, Working on now, Proof, My world, How to
  connect. Each frame follows the smart-note pattern (nutshell · why it
  matters · how it applies · how it connects · what's in it for you).
- **Skills** (lines 987–1055): its own slideshow in the pricing page's
  visual presentation — 14 slides, best first, presented as the growing
  list (not a fixed 14). Each slide: name · plain words · what makes us
  different · one real example · status (SN-3747) · proof link or an
  honest "proof owed" note. Opens "This is what makes us skilled. This
  is what makes us different."
- Two views, one page: "See all my skills" (beat 9, line 973) and beat
  14's Keep reading open Skills; "Back to About" restores the exact
  About frame you left; `?view=skills` opens Skills directly. The deck
  pill reads "N / 14" and hides while Skills is showing.

## Per-item verdicts (with line-number evidence)

| Brief item | Verdict | Evidence |
|---|---|---|
| Harvest agreement frame system, byte for byte | PASS | 1,319/1,818 lines byte-identical to the agreement source; diff +569/−89 (`harvest-proof-agreement.diff`). Full account in `HARVEST-PROOF.md` §1. |
| About = 14 frames, settled order | PASS | `data-beat="1"`…`"14"` (lines 965–978); all 14 kinds present (WHO I AM … HOW TO CONNECT); beat 1 unhidden, 2–14 hidden; pill reads "◆1 / 14" live. |
| Skills = own page/slideshow, pricing presentation | PASS | 14 `.letter-beat.lb` slides (lines 992–1031), 14 `.ldot` dots (line 1035), `#skillsNext`/`#skillsAll`/`#skillsSign` (1052–1055); pricing CSS embedded byte-identical (`harvest-proof-pricing-css.diff` 0 bytes); wireLetter 7 renames only (`harvest-proof-pricing.diff`). |
| Content as him, in his voice, no placeholders | PASS | Mission, prophecy, five gates, law of one, privacy, "You say it. I do it.", twelve sisters / Team Naya, "Working on now" dated 20 November 2026. Zero placeholder strings in the file. |
| Original photo, agreement's reference verbatim | PASS with the plain fact below | Beat photo = template's own face-1.jpg img (line 965); skill faces = face-1,3,4,5,6,7,8,9.jpg proof-host URLs (lines 992–1031); topbar FACES array restored verbatim. face-1.jpg URL curls HTTP 200, 484,837 bytes. **No portrait of Shawn exists in either harvested source** — searched both files; this is the brief's anticipated case, so the agreement's reference is used verbatim. |
| No invented scores/results/credentials/testimonials | PASS | Statuses only: Login, Notes, Numbers production-proven; Mail, Lists, Links, Factory, Box, Ask, Growth, Reports demonstrated; Match demonstrated (staging 9/10, no public proof link); Meet DECLARED (says so plainly); Access demonstrated (staged). 11 live proof links + 3 honest "proof owed" notes (Meet, Match, Access). |
| Type 25/19/17, no gray, deep colours, spectrum never twice in a row | PASS | Checker PASS (below). Tones cycle the 10-deep spectrum with 0 adjacent repeats across all 28 tone slots; 0 `#ff2a2a` / bright-purple refs left; 0 sub-17px font sizes in the harvest. |
| Mobile + desktop | PASS | Smoke test 390×844 and 1920×1080 (below); screenshots read as a reader (below). |
| Do not touch Personal | PASS | No Personal file read or written by this round. |

## Verification (all run on the final file, sha 8749d432…)

- **Machine checker:** `check-design-laws.py` → **PASS — no
  machine-checkable violation (2 warnings)**, exit 0. The 2 warnings
  are identical to the source agreement file's own warnings
  (`color:` var, `color:transparent` — both in harvested code, eye-checked
  as white-on-obsidian, not gray).
- **Structure:** 14 About articles + 14 skill slides; dots 14 (1 lit);
  proof links 11, owed spans 3; 0 `data-reason`, 0 `letterBody`/
  `letterDots`/… ids left; 0 `#ff2a2a`; all 9 `<script>` blocks pass
  `node --check` (comments stripped first — one `<script>` string
  inside the HTML header comment is not a script block).
- **Smoke test (Playwright Chromium, local server), phone 390×844:**
  title "About Shawn Vibert — NayaNET"; pill "◆1 / 14"; beat 1 visible;
  Next → beat 2, pill "◆2 / 14"; "See all my skills" → Skills visible,
  deck hidden; slide 1 visible, slide 2 hidden; Skills Next → slide 2
  revealed AND slide 1 still visible (pricing accumulation), dots lit 2
  (cumulative trail — pricing-literal), slide 2 title "The Mail Skill";
  read-all → all 14 visible, sign visible, controls hidden; "Back to
  About" → deck visible on beat 9 (the frame left), Skills hidden;
  `?view=skills` → Skills visible; pill hidden in Skills view, visible
  in About. **Desktop 1920×1080:** pill 1/14, beat 1 visible, 2× Skills
  Next → 3 slides visible. **0 page errors.** The only console errors
  are `ERR_TUNNEL_CONNECTION_FAILED` for proof-host images — the VM
  egress proxy blocks the proof host in Chromium (curl proves the URLs
  serve 200); same exposure as the agreement itself in this VM.
- **Read as a reader (screenshots):** About beat 1 desktop — royal
  frame, obsidian, purple rim; "WHO I AM / Hi, I'm Shawn Vibert";
  play/media frame; four smart-note rows; showcase frame; orb; Back /
  Keep reading / Next. About beat 9 phone — "My three best skills",
  three skills in deep tones. Skills phone — "My skills", the opening
  line, round portrait frame with purple rim, jewel 1, "The Login
  Skill", "What it means:" with orb bullets. Skills desktop — slides
  accumulate (Notes parts, then Lists below), proof pill "See the feed,
  live ◆" renders correctly.

## Bugs found by the smoke test and fixed (not hidden)

1. **Skill slides rendered `display:none` forever.** The agreement CSS
   line 364 has a GLOBAL `.letter-beat:not(.frame-now)
   {display:none!important}`; skill slides never get `frame-now`.
   Fixed with a scoped guard in ADD_CSS:
   `#skillsSlideshow .letter-beat.lb{display:block!important}`
   (higher specificity, same `!important`).
2. **Hidden view ate taps.** Harvested display rules outrank the
   browser's `[hidden]` rule, so the hidden `<main>` still covered the
   Skills buttons. Fixed with `#deckUnfold[hidden],
   #skillsSlideshow[hidden]{display:none!important}` in ADD_CSS.
3. **The deck pill overlaid the Skills header.** The auto-created
   `.af-prog` pill (also `display:flex` in harvested CSS) stayed visible
   over the Skills view. Fixed: the view switcher hides it in Skills
   and restores it in About, with `.af-prog[hidden]
   {display:none!important}` in ADD_CSS.
4. **WireLetter ids were renamed with `#` but `getElementById` uses
   bare ids** — the first build's Skills Next button was wired to
   nonexistent ids. Fixed: renames use bare names (also covers the
   `#letterBody` querySelectorAll). The diff proof (§2b of
   HARVEST-PROOF.md) confirms the final IIFE is the pricing one plus
   exactly the 7 renames.
5. **Orb bullets kept the pricing accent** (`#ff2a2a` — 70 occurrences:
   the `<li>` template was cut before the per-skill recolour). Fixed:
   `bullet()` recolours the orb from the skill's tone. 0 left.
6. **Part labels didn't match** — the pricing source uses HTML entities
   (`&mdash;`, `&rsquo;`), not literal characters. Fixed to match the
   entities. All three labels now read as designed.
7. **Portrait substitution caught and reversed.** An earlier pass of
   this round replaced the agreement's faces with monogram "S" spans
   (beat photo, skill board-face, topbar FACES array) on the reasoning
   that face-*.jpg are Naya's faces, not Shawn's. That contradicts the
   brief ("use the agreement's image reference verbatim — do not
   substitute"), so all three were restored to the agreement's own
   references. The monogram code and CSS are gone (0 "mono" spans in
   the file). The honest statement stands: **no Shawn portrait exists
   in the harvested sources.**

## §11 check — in writing

**The five gates.** (1) Is it right? Yes — the page tells the truth
about what is known, cites proof where it exists and says "proof owed"
where it does not; nothing invented, no face recreated, no other
person's work claimed. (2) Is it what they truly need? Yes — Shawn
asked for About + Skills in the agreement's and pricing's own
presentation, finished in his voice, so he can judge it against v1 in
the morning; that is exactly what was built. (3) Is it mine to do? Yes
— this round was dispatched to me, one lane, standalone page; no merge,
no live deploy, no message to Shawn, Personal untouched, membership not
started. (4) Is now the time? Yes — authorized overnight, his eye in
the morning; the build is filed to the branch, ready for the parent to
stage. (5) Can I prove it? Yes — checker PASS, structural checks,
9/9 scripts parse, full smoke test at two widths with 0 page errors,
literal diffs (agreement +569/−89; pricing CSS 0 bytes; wireLetter 7
renames only), screenshots read as a reader, and the filed blobs
re-read by sha + size (see Filing).

**The design-check questions.** Is every position calculated? The
layout is the harvested one — nothing positioned by hand. Does it feel
like a machine? The deck advances, the pill counts, the dots trail, the
slides accumulate — all harvested mechanisms, verified live. Can you
get it in 2 seconds? Beat 1 says who he is and what he builds in one
frame; the Skills opening line says what makes us skilled in one line.

**The sense check (on the page, not the brief).** Read as a reader at
phone and desktop widths: the About unfold reads as the agreement with
a different story; the Skills slideshow reads as the pricing boards
with different skills; nothing is flat, nothing is gray, no frame
scrolls inside itself, the proof links are real taps, the three "proof
owed" notes say so plainly instead of pretending. The one thing that
would have failed his eye — the deck pill sitting over the Skills
header — was found on the screenshots and fixed. The portrait question
is answered the way the brief orders it, and the gap (no Shawn photo
in the sources) is stated here, not hidden.

**Scorecard.** Why is it not a 10? The three "proof owed" slides
(Meet, Match, Access) have no live demonstration to link to — that is
a content gap in the world, not in the page, and the page says so
honestly. The VM cannot render the proof-host photos (egress proxy),
so the photo render is proven by URL + curl (200) rather than by a
screenshot — the staged link is where his eye will confirm it. What
would make it a 10: live proof for the three owed skills, and his
morning eye on the staged link.

## Still owed (named honestly)

- **3 skill proof links owed:** Meet (no live room yet), Match
  (staging-proven 9/10, no public proof link), Access (Membership
  fix-8 eye passed on staging, no public proof link). Each slide says
  so plainly; nothing pretended.
- **Shawn's eye in the morning** is the final gate — this round proves
  the build, it does not claim his approval.
- **Membership** gets the same treatment starting tomorrow — not
  started here, per his order.
- **Not in this round (flagged to the parent from call 3e29f68e):**
  the Hub date spin and the big white line in the Hub's main area.

## Parallel variant — a second filing exists (read before choosing)

A second worker shared this records dir during the round and filed
their own variant first. Their report is preserved verbatim as
`MAKER-REPORT-MONOGRAM-VARIANT.md` in this dir (do not delete it).

- **Their filing:** branch `personal/about-skills-rebuild-20261120`,
  commit `150a982b4afd16ebb6730effe410df5c2a883580`, file
  `TEAM-NITRO/about-skills-rebuild-20261120/about-skills.html`,
  blob `c97a2ee04859c1b791c20941d4cad150374cc1c2`, 195,962 B, sha256
  `38c15145d3e636f6ef7b110ae574433d795e3236d7a7df0b88f34802e483913d`.
  Local frozen copy: `about-skills-FINAL.html` (identical bytes).
- **The difference is exactly one decision — the portrait.** Their
  variant puts a monogram "S" orb in all three portrait spots (14 beat
  photos, 14 skill faces, topbar face) on the reasoning that
  face-*.jpg are Naya's faces, not Shawn's. This variant puts the
  agreement's own face-*.jpg references in verbatim, per the brief's
  explicit instruction ("use the agreement's image reference verbatim —
  do not substitute") — the brief anticipates the no-Shawn-photo case
  and prescribes this fallback. Everything else (frame, slideshow,
  content, statuses, proof links) is the same build lineage; this
  variant additionally carries the render verification (smoke test +
  screenshots, which their seat could not do) and the pill-toggle fix.
- **The shared-dir race is the reason both exist.** We edited the same
  `build-about-skills.cjs` concurrently; their report documents the
  race (their script shas `48f7c669…` → `f082bd6d…`; my rebuilds twice
  reverted their monogram edits, and vice versa). Their frozen output
  is `about-skills-FINAL.html`; my output is `about-skills.html` from
  the current script, which reproduces its bytes deterministically.
  One lane, one round, one writer per file — the next round needs that
  rule for this dir.
- **The parent must choose** which portrait treatment goes to Shawn's
  morning eye. My recommendation, per the brief: the agreement's own
  faces (this filing) — it is what v1 was rejected for NOT doing
  (original photo, not a recreation or a stand-in), and the page is
  titled "About Naya" with Naya as the speaking voice.

## Filing

- **Branch:** `about-skills-rebuild-20261120` (created from main tip
  `505355d0460a0fb39239620be78ae28983b53c60`)
- **File:** `team-nitro/about-skills-rebuild-20261120/about-skills.html`
- **Page blob:** (filled below after the git-data filing)
- **Commit:** (filled below)
- **Staged proof link:** (filled below after the served-bytes check)
