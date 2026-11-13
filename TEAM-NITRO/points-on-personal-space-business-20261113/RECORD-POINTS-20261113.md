# RECORD — Points on Personal, Space, Business (maker, 2026-11-13)

## What it is

The gold points pill from the staged Smart Skills page now sits in the name row
on Personal, Space, and Business — one pill per page, beside the name, showing
the citizen's real live points — and the three heroes now sit in the same place
at every width. Staged only. Nothing live touched, nothing merged, nothing
deployed.

**The pill, harvested verbatim** from
`smart-skills-page-20261113/smart-skills-page.html` lines 2082–2086 (markup)
and 1974–1982 (CSS — already byte-identical in the Personal bytes at lines
2133–2142, so only the element was missing):

```html
<div class="ph-points" id="pointsdisplay" title="Your Naya points">
  <span class="ph-points-star">✦</span>
  <span id="pointscount">…</span>
  <span class="ph-points-label">pts</span>
</div>
```

The ONE permitted change: the initial `#pointscount` content is `…` (the page's
own loading glyph), never `0` — the Skills page's `0` is a placeholder with no
writer behind it, and copying it would copy the placeholder.

**The three files (branch `points/personal-space-business-20261113`,
`TEAM-NITRO/points-on-personal-space-business-20261113/`):**

| File | SHA-256 | Bytes | What it is |
|---|---|---|---|
| `personal-points.html` | `eb0173c99920d28f12e1ad2942b452fcfd170bcbfa920af141da6354db4c8b95` | 1,486,494 | Live Personal (sha `992ab18c…`) + pill + wiring + hero-fix block |
| `space-points.html` | `f7eced7b39570f312c9c741805b2ce548d0e31f80ec54dcabcfbaef158aab613` | 1,487,462 | Space clone rebuilt from the new Personal bytes via the clone builder |
| `business-points.html` | `f8c769fb301c0dab6313c6126d07ba71a242df5b5de259c6caac096a6bcc2481` | 1,487,266 | Business clone rebuilt from the new Personal bytes via the clone builder |

**Staged links** (proof host, fresh `cb` = the staged sha; receipts cite the
staged sha read fresh — verified § Proof):

- Personal: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/points-on-personal-space-business-20261113/personal-points.html&ref=points/personal-space-business-20261113&cb=eb0173c99920d28f12e1ad2942b452fcfd170bcbfa920af141da6354db4c8b95
- Space: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/points-on-personal-space-business-20261113/space-points.html&ref=points/personal-space-business-20261113&cb=f7eced7b39570f312c9c741805b2ce548d0e31f80ec54dcabcfbaef158aab613
- Business: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/points-on-personal-space-business-20261113/business-points.html&ref=points/personal-space-business-20261113&cb=f8c769fb301c0dab6313c6126d07ba71a242df5b5de259c6caac096a6bcc2481

## Why it matters

A citizen opening their world could not see their own points anywhere — the
pill existed on exactly one staged page and nowhere else. The order was the
same pill, the same place, the citizen's real number, on all three pages. The
round also closes the hero gap the captain's eye-check found: on live Personal
at 390 the name sat clipped behind the Change-cover button (measured:
`#pname` y=13, `#cvrbtn` y=6–54, boxes intersecting), while the clones sat
337 px lower (`#pname` y=350). After this round the three heroes are one page:
`#pname` top edge spread 0 px at 390, 1440, and 360, and Change cover never
touches the name at any width.

## How to apply it — the exact change, and the exact wiring site

**E1 — pill markup.** Inserted directly after `#pname` inside the existing
name flex row (`display:flex;align-items:center;gap:14px;flex-wrap:wrap;`),
same line numbers on all three files: **`personal-points.html:4713–4717`**
(and `space-points.html` / `business-points.html:4713–4717`). No CSS added —
the harvested `.ph-points` block was already on the page.

**E2 — wiring.** The pill reads the same `total` the points board's donut
renders, in the same tick. Exact site: **`personal-points.html:18330–18336`**
(same lines on both clones), immediately after the donut write at
**18324–18326** (`donutWrap.innerHTML = … '<text …>'+total+'</text>' …
`POINTS`), inside `loadPointsBoard`'s charts IIFE:

```js
/* POINTS PILL (2026-11-13): the hero pill beside the name (#pointscount)
   shows this same total — the same tick the donut's total lands, so the
   pill and the donut can never disagree in one session. Guarded on
   window._dashD: before the live rows land the pill keeps its loading
   glyph (…) instead of printing a false 0. */
try{ var _pc = document.getElementById('pointscount');
  if (_pc && window._dashD) _pc.textContent = total.toLocaleString(); }catch(_){}
```

The chain it reads from, in the same file: `window._dashD` (live rows, set at
line 12479) → `ldData()` (17570) → the orb sum over `LD_NODES` (17541) in
`loadPointsBoard` (17922), whose `total` is the donut's center number. The
canonical `ldScore()` (17581, 2× value table) feeds the spine score
(`osBuildSpine`, 17808; `window._osSpine`), which the big number
(`#os-se-val`) sweeps to — see Finding F2 below for how the two numbers
relate. The pill follows the donut total, per the brief's wiring rule.

**E3 — hero alignment.** The 23-line `<style id="hero-fix-20261112">` block,
harvested byte-identical from
`page-audit-remeasure-20261112/personal-hero-fix.html`, inserted before
`</body>` on Personal only (`personal-points.html:22315–22337`; the clones
already carry it at :22329). At ≤807 px it returns `.ph-head` to flow layout
(`position:relative;margin-top:-70px`) instead of absolute `bottom:0` of the
cover — the measured cause of the live-Personal name clip. No other layout
rule changed.

**Clone build.** The clones were rebuilt through a lane-local adaptation of
`space-business-mirror-personal-20261112/build-clone.py`
(`build-clones-points.py` in this dir) — the original script and the audit
files it reads are untouched. Why an adaptation: the original script composes
its template from the audit rooms file + hero block, not from
`personal-live.html`, so the pill had to enter the template at its source.
The lane-local `rooms-points.html` (sha
`553ec8660c8c8918fae11444ea8c8ad18574dff3aa18985d4ef3ccdc353109ef`) is the audit
rooms file (sha `da03200e…`, untouched) + E1 + E2 only. Same swap table, same
assertions (24 swap lines Space, 25 Business — identical counts to the
original build), same integrity checks. Composed template
`template-points-composed.html` sha
`a7827dc4b0538af4b6bc5ae0637b2727a10a1b235acfe91dc781a018853a7b19`.

**Diff audit (what changed, nothing else):**

- Personal vs live Personal: exactly 3 inserts — pill (4712–4717), wiring
  (18329–18336), hero-fix block (22314–22337). Nothing else.
- Space/Business vs previous staged clones: exactly 2 inserts each — pill
  (4712–4717) and wiring (18329–18336). Nothing else.
- Personal vs the clone template: only the pre-existing rooms-plus hunks
  (the rooms fix stays clone-only, as before — a divergence this round
  carries forward, not one it introduces).

## Proof — measurements (Firefox, real browser, local files + staged links)

Method: `probe-baseline.py` (pre-edit baseline on the three base files),
`probe-verify.py` (post-edit geometry), `probe-harness.py` (fixture
harness), all in this dir; screenshots `proof-firefox-<page>-<w>-<top|end>.png`
(18 shots) + `skills-ref-<w>-top.png` (reference). Baseline JSON
`probe-baseline-firefox.json`, verify JSON `probe-verify-firefox.json`,
harness JSON `probe-harness.json`.

### Baseline (pre-edit, the cause, measured first)

| Page | 390 `#pname` y | 1440 `#pname` y | 360 `#pname` y | `#cvrbtn` ∩ `#pname` @390 |
|---|---|---|---|---|
| Personal (live bytes) | 13 | 314.2 | 33 | **YES** — name clipped behind Change cover |
| Space clone | 350 | 314.2 | 480 | No |
| Business clone | 350 | 314.2 | 480 | No |

Cause: live Personal lacks the hero-fix block, so at phone widths its
`.ph-head` is absolute `bottom:0` of the 420 px cover while the head itself
is ~407 px tall — the name rides up into the cover's top band where Change
cover lives. The clones carry the fix, so their heads sit in flow below the
cover. Reference: staged Skills page at 390 — pill beside the name, fully
visible; pill rendered width 118.4 px, name "Anaya" 75 px, info column 228 px.

### Post-edit geometry (all three pages, 390 / 1440 / 360)

| Check | 390 | 1440 | 360 |
|---|---|---|---|
| Pill present (exactly 1 per page) | ✓ all three | ✓ all three | ✓ all three |
| `#pname` top edge (Personal / Space / Business) | 350 / 350 / 350 — **spread 0** | 311.2 / 311.2 / 311.2 — **spread 0** | 483 / 483 / 483 — **spread 0** |
| Pill immediately right of name, 14 px gap, same row | **NO — wraps** (see F3) | ✓ gap exactly 14.0 on all three | ✓ gap exactly 14.0 on all three |
| `#cvrbtn` ∩ `#pname` | No, all three | No, all three | No, all three |
| Overflow (start and end) | 0 px, all three | 0 px, all three | 0 px, all three |
| Pill initial text (live data blocked) | `…` on all three | `…` on all three | `…` on all three |
| Console errors | 42/page — all Supabase CORS blocks, identical set to baseline (see below) | same | same |

Eye-check (screenshots read by eye): at 390 the three heroes are
indistinguishable except name/tagline/avatar — name, gold pill below it,
tagline, same buttons, Change cover top-right clear of the name. At 1440 the
pill sits immediately right of the name exactly as on the Skills reference.
H1 (pill by the name at 390) — present and fully visible, wrapped below the
name (F3). H2 — by eye in the harness session the pill reads the same number
the code path computes (see harness). H3 — the three heroes read as one page
at scroll 0, 390 and 1440. H4 — Change cover never covers the name at 390.
H5 — hover: computed `box-shadow` and `transform` of the pill are identical
before/after hover on every page — which is exactly the harvested pill's
behavior (its CSS carries a `transition` but no `:hover` rule); the pill
behaves like the harvested one, no more and no less.

### Fixture harness — the wiring, proven (proof ran: fixture harness)

Live Supabase data cannot load in this VM: all 42 console errors are
`Cross-Origin Request Blocked` on `https://dahisasgpfvziswqvmvm.supabase.co`
calls from `file://` — the same limit the brief names. That is a measurement
limit, not permission to fake a number, so the wiring is proven with a
fixture `window._dashD` of exactly the shape the live loader builds
(`postTimes`, `noteTimes`, `invTimes`, `msgTimes`, `saveTimes` arrays +
`_dashLinkT`), fresh page per fixture. No fixture number is presented as a
citizen's real number.

| Fixture | Counts | Donut total (page's own `LD_NODES` table, recomputed independently) | Pill | Match | Spine score (`osBuildSpine`, for reference) | Pill after spine lands |
|---|---|---|---|---|---|---|
| A | 4 posts, 2 notes, 1 invite, 3 msgs, 5 saves, 1 join | 245 | **245** | ✓ | 540 | 245 (unchanged) |
| B | 10 posts | 250 | **250** | ✓ | 500 | 250 (unchanged) |
| C | all zero (genuinely new citizen) | 0 | **0** | ✓ | 0 | 0 (unchanged) |

All 9 cells (3 pages × 3 fixtures) match. The pill **changes when the
fixture changes** (245 → 250 → 0) — wired, not printed — and is stable 1 s
after the write with the fixture intact at read time. Note on fixture A: the
donut total is 245, not 255, because the saves node in `LD_NODES` carries
no `tkey`/`map`, so saves contribute 0 to the donut total (the page's own
table, read back from `window.LD_NODES` in the harness — not an assumption).
No live session could run: with live data blocked, `window._dashD` stays
undefined and the pill honestly keeps `…`.

**Staged proof:** staged bytes curl-verified equal to the local files
(Personal `eb0173c9…`, Space `f7eced7b…`, Business `f8c769fb…`, byte counts
identical). Staged geometry probe re-ran on the proof-host links
(`probe-staged.py`, `probe-staged-firefox.json`, screenshots
`proof-staged-firefox-<page>-<w>-<top|end>.png`, 18 shots): every box
identical to the local run — `#pname` top spread 0 px at 390 / 1440 / 360,
pill immediately right of the name with exactly 14.0 px gap at 1440 and
360, wrapped below the name at 390 (same y=404 on all three), `#cvrbtn`
never intersects the name, overflow 0 px everywhere. The staged 390
screenshot is byte-identical to the local 390 screenshot (sha
`8b84af30…`). Staged harness (same run): fixture A pill 245 and fixture B
pill 250 on all three staged pages, 6/6, fixture intact at read. Live data
stayed unloaded on staged too (`window._dashD` undefined, pill `…`):
Supabase is blocked from this VM even from the `https` staged origin — 42
console errors per page/width, all the same 7 Supabase CORS tables as
local (one cell, Space 360, logged 44 — a retry duplicate of the same
tables, no new error kind, no non-Supabase error anywhere staged).

## Findings the round surfaced (named, not hidden)

**F1 — the donut the brief cites never renders.** `loadPointsBoard` writes
its donut SVG into `#os-donut-wrap` (`personal-points.html:18296`), but no
element with that id exists anywhere in the static HTML or the live DOM —
even with the Dashboard view open (`#os-ring-wrap` is likewise absent; the
only donut wraps on the page are the class-based front/report donuts,
`#os-dash-donut` / `#os-rep-donut`). All 10 occurrences of `os-donut-wrap`
in the file were enumerated: 4 CSS rules, 2 static class divs, 2
`closest()` calls, 1 `getElementById`, 1 comment-adjacent line — no creation
site. So the donut's SVG total is never painted on Personal today. The
wiring still sets the pill from the same `total` variable in the same code
path (the variable is real; the paint target is missing), and the harness
proves pill == that `total`. Repairing the missing donut element is out of
this round's scope — it would be inventing a component, not the pill round —
and is flagged here for the captain as a follow-on decision.

**F2 — the pill and the big number are two different numbers by the page's
own design.** The pill shows the donut `total` (the undoubled orb sum:
fixture A 245). The big number `#os-se-val` sweeps to `displayTotal` =
`_featuredCenter(total)`, i.e. the spine score (2× `ldScore`: fixture A
540, B 500, C 0 — confirmed by calling the page's own exposed
`window.osBuildSpine` on the fixture). The harness proves the pill does NOT
follow the spine: after the spine lands, the pill stays 245 / 250 / 0 while
the big number sweeps toward 540 / 500 / 0. (In the harness the headless
rAF runs slow, so the big number was read mid-sweep — 90 / 83 / 0 — heading
to the spine score; the target, not the mid-sweep value, is the evidence.)
The brief's wiring rule is pill == donut total, and that is what is wired.
Which number a citizen should see beside their name — the donut's 245 or
the gauge's 540 — is a captain's call; this round surfaces it with the
numbers instead of choosing silently. (In a time-pill window the big number
would show a period delta — fixture A: hour 90, day 220 — while the pill
stays the all-time donut total.)

**F3 — at 390 the pill wraps below the name on all three pages.** The
name row's info column is 228 px wide at 390 (avatar 110 + gap 20 + padding
16 × 2 = 358 of 390). Pill width is 118.4 px (measured on the reference).
Name + 14 px gap + pill: Personal 159.6 + 14 + 118.4 = 292.0; Space 192.2 +
14 + 118.4 = 324.6; Business 129.1 + 14 + 118.4 = 261.5 — all wider than 228,
so the row's `flex-wrap:wrap` drops the pill to a second line, left-aligned
under the name (pill y=404, name y=350–390, identical on all three pages).
At 1440 and 360 the pill sits immediately right of the name with exactly
the 14 px gap on all three pages. The wrap is identical on all three pages,
fully visible, never clipped, never overlapping — the heroes still read as
one page — but the brief's "same row at all three widths" criterion is
geometrically unmeetable at 390 with the harvested pill, the existing names,
and the existing 228 px column. No layout rule was invented to force it
(that would break the harvest law and the clone law); the numbers are here
for the captain to rule on — accept the wrap at 390, or order a layout
follow-on.

## No-regressions

- Live Personal re-curled after the work: **sha `992ab18c…`, 1,484,185 B —
  unchanged**. Live Hub re-curled: sha
  `8a20953365d757f7224636eedaf8c18e07dcc3f2f9bae3b202d7cafb71bc1b33`,
  4,990,447 B. No baseline Hub sha was on file in this brief, so Hub
  "unchanged" rests on the absence of any live write by this round (no live
  route, deploy, or edit was made anywhere), not on a sha comparison — stated
  plainly.
- Smart Skills page untouched: sha `8c2565a7…` re-verified after the work.
- Original clone script and audit files untouched (their shas re-verified:
  live `992ab18c…`, hero-fix `8d0273fc…`, rooms `da03200e…`).
- Console errors: 42 per page/width, **identical in kind and count to the
  baseline** — every one a Supabase CORS block (`invites`, `memberships`,
  `smart_links`, `smart_link_daily_stats`, `smart_link_dimension_stats`,
  `smart_mail_threads`, `smart_notes`). No jsdelivr failure appeared in this
  VM's run (the Skills round's `SEC_ERROR_UNKNOWN_ISSUER` on the Supabase
  CDN did not reproduce here — the bundle path differs by page). No new
  network call, no new secret, no new grant, no new file outside the lane
  branch. No page error (`pageerror`) in any probe run.
- One pill per page (`#pointsdisplay` count = 1 at every width on every
  page); no second points display; no placeholder `0` and no hand-written
  number anywhere in the edited files (`#pointscount` occurs exactly 4
  times per file: CSS selector, element, writer, wiring comment); the
  `.ph-points.bump` class exists in the harvested CSS but nothing on the
  page ever adds it (as on the Skills page — no bump writer was harvested
  because none exists there).

## Laws L1–L7 / design-contract gate (a)–(i) — self-check

- L1 stranger test: PASS at 1440/360 (name + gold pill + tagline in 2 s);
  at 390 the pill is below the name, still name + points + tagline in 2 s.
- L2 perfect words: PASS — no dictation pasted anywhere; no new wording.
- L3 title+subtitle+nutshell: PASS — hero is name, pill, tagline, nothing more.
- L4 Naya speaks, faces alternate: PASS — taglines untouched, citizens' own voice.
- L5 test in his head: PARTIAL — the three heroes read as one page, but the
  390 wrap (F3) is a visible difference from the Skills reference, which
  keeps the pill beside the name at 390.
- L6 `##` note format: PASS — this record and the scorecard follow it.
- L7 one ultimate ten: NOT CLAIMED — see scorecard; F3 blocks a 10.
- (a) zero white/light backgrounds: PASS — obsidian throughout, gold pill on
  obsidian as harvested. (b) raised/elevated: PASS — harvested pill object.
  (c) numbers alive: PASS — harness proves the number moves with the data.
  (d) no text-in-image: PASS. (e) no bare text blocks: PASS — pill is a real
  object. (f) no look-alike: PASS — markup + CSS harvested verbatim.
  (g) `##` format: PASS. (h) no dictation-blunt phrases: PASS.
  (i) title+subtitle+nutshell + faces alternate: PASS.

## Done / not done

**Done:** pill beside the name on all three pages (same row 1440/360,
wrapped below at 390); pill wired to the donut total in the same tick
(harness 9/9); heroes aligned to 0 px spread at all widths; Change cover
clear of the name everywhere; zero overflow; staged links filed on the lane
branch and byte-verified; live untouched.
**Not done:** same-row pill at 390 (F3 — geometrically blocked, captain's
call); live-session proof of pill == donut (live data cannot load in this
VM — CORS; the fixture harness stands in its place, stated plainly); the
missing `#os-donut-wrap` target (F1 — follow-on decision); the
pill-vs-big-number question (F2 — captain's call); Chromium cross-check
not run (Firefox only — VM Chromium was untested this round; the brief's
method names Firefox).

## § Staged run — filled

Filed on branch `points/personal-space-business-20261113`: first commit
`40ecff926` (build + record + scorecard + probes + local proof), second
commit (staged probe + this filled section — see git log). Staged shas
re-read fresh after the second push: Personal `eb0173c9…`, Space
`f7eced7b…`, Business `f8c769fb…` — identical to the local files and to the
`cb` values in the links above.
