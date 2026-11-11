# One bottom bar — RECORD

**Round:** one-bottom-bar congruence (Shawn's complaint, 2026-11-11 01:18Z)
+ the NO-OVERLAY / BAR STACKING LAW (Shawn's order, 2026-11-11 01:25Z).
**Maker:** Naya Nitro Narzan (subagent, depth 2/2).
**Date:** 2026-11-11.
**Branch:** `one-bottom-bar-20261111` (repo `SoulSchoolAcademy/NayaPOWER`).
**Status:** BUILT + STAGED + SELF-SCORECARDED — verifier's turn. Not merged,
not deployed to live, nothing presented to Shawn from this seat.
**Fix seat (v2, 2026-11-11):** verifier returned OVERALL NOT PASS (see
`verify/VERIFY.md`); the fix seat applied component v2 (snap strip +
settle observer), corrected the Dashboard baseline below, and filed the
Inviter + this record to the branch. Details in "FIX SEAT — v2" at the end
of this record. Still not merged, not deployed to live.

## The complaint, in plain words
The bottom bars do not match across pages. The staged Smart Inviter shows
nine named app pills; the live Hub shows twelve unlabeled icons; new icons
keep being invented per page. The law: stop making new stuff, work with
what we have, be congruent — the same icons, buttons, looks and feels on
all the pages. The icon set is a harvested asset, never a per-page
invention. Plus the stacking law: bars STACK, never overlay — the Smart
Bar sits at the very bottom or very top in its own lane, never covering
another bar, never covering the + buttons.

## The fix (one line)
Build ONE bottom-bar component from the harvested canonical markup and put
the SAME component — same icons, same order, same labels, same behavior —
on the Inviter, the Hub, and the Dashboard, by editing each base file, in
its own lane above the Smart Bar / notif bar / jewel bar.

## What the bytes actually said (the brief's premise, verified — and corrected)
The brief said "the staged Smart Inviter shows nine named app pills + '10
apps' overflow — VERIFY BY BYTES, do not take on faith." Verified. There
is NO block of nine named pills and NO "10 apps" string in ANY base file:
- **Inviter** (`growth-new.html`, sha `1792cda2…`): TWO bottom bars.
  (a) `eco-bottombar` — FOURTEEN icon-only links (Smart Feed, Start Here,
  Ask Naya, Smart Factory, Today, Reports, Library, Ledger, Connections,
  Lists, Smart Mail, Spaces, Smart Inviter, Settings), labels only in
  `data-label`/aria/title. (b) Smart Bar `#nsbBottom` — a fixed trio
  (Mail ✉, Activity ◈, Dashboard ◉) + a DRIFTING network row seeded from
  `network` (Home, Dashboard, Personal, Business, Space, Smart Inviter,
  Connections, Smart Lists, Reports, Project Intelligence) + "＋ Add" +
  net anchor. The row auto-sorts by the citizen's usage and persists to
  localStorage — it is NOT a fixed nine.
- **Hub** (`HUB/app/index.html`, blob `6ea279cd…`, 5,528,688 B): the
  `eco-bottombar` — TWELVE icon-only links (HOME, NAYA POWER, ABOUT US,
  YOUR HIRED, WHITE PAPER, NAYA ACADEMY, "5" DAY CHALLENGE, MAXIS AI
  SCORE, AI MASTERCLASS, INTRO REPORT, LIFE WITH NAYA, MEMBER LOGIN).
  The `jewelbar` (5 labeled jewels) belongs to the Ask room only.
- **Dashboard** (`dashboard-pass11.html`, sha `ff0a3ed6…`): `#os-bottom3`
  — THREE icon-only buttons (Smart Mail envelope, Activity pulse + live
  badge, Dashboard house). The Smart Bar bottom is REMOVED on this page
  (PASS 3 Addendum 4); no `nsbBottom` element exists.
- The common set across all three bottom bars is Mail, Activity,
  Dashboard (the trio) — everything else differs per page.

**What I built from that (brief's order, derived from the bytes):** the
canonical nine = trio order (Mail, Activity, Dashboard — trio
L4067-4078) + network-seed order (Business, Space, Smart Inviter,
Connections, Smart Lists, Reports — seed L4226-4237). That is exactly the
brief's listed order. Glyphs + colors + hrefs are harvested per pill:
trio glyphs/colors explicit (Mail ✉ #ffbf3d, Activity ◈ #a06bff,
Dashboard ◉ #2fe89e); network glyphs from the seed (Business ■, Space ▲,
Smart Inviter ✦, Connections ◇, Smart Lists ☰, Reports ◆) with SPECTRUM
colors by seed index (Business #ffbf3d, Space #ff9a5a, Smart Inviter
#ff5e6c, Connections #e84fff, Smart Lists #a06bff, Reports #3fb8ff).
"Growth" is the brief's label for the Smart Inviter room (href
`https://nayanet.app/rooms/growth`, glyph ✦ harvested). The 10th pill,
"10 apps", is brief-specified (no such string exists in the bytes); its
"＋" glyph + #3fb8ff color are harvested from the Smart Bar's "＋ Add"
button (L3858, SPECTRUM[1]), and it links to the Hub
(`https://nayanet.app/#/hub`). Pill structure mirrors the harvested
`pill()` builder (L3601-3655: jewel span + label span); jewel treatment
mirrors harvested `.nsb-jewel` (L3300-3309); the Activity pill keeps the
live badge span (`#os-b3-badge`, Dashboard `.os-b3-badge` L4946-4949) so
the Dashboard's badge wiring survives untouched. Zero invented icons.
The component lives at `one-bottom-bar-20261111/component.html`.

## The three edits (each an EDIT, never a rebuild)
1. **Inviter** — `growth-round-20261110/growth-new.html`: 295,697 B
   (sha `1792cda2…`) → **300,823 B (sha
   `0a31c4c69750b1082883bdc43c5772a9975af723d6ca090bcd378c3e36ca5628`)**.
   The whole eco-bottombar builder `<script>` (14 icons, chars
   177565–180830) is replaced by the component block. The Smart Bar is
   untouched. Host shim: `pad()` clearance is now Smart Bar height +
   component height (was Smart Bar only). Dead `.eco-bottombar` /
   `.eco-bb-btn` CSS rules remain (no element, no builder — left alone
   per minimal-diff).
2. **Hub** — `HUB/app/index.html` on main, blob `6ea279cd…` (5,528,688 B)
   → **5,533,245 B (sha
   `4b0182523662cb8b5a3eba08f843fdf373c62ff3e5f575f3802c70016795f77a`)**.
   The eco builder JS (BB_LINKS + forEach + iconPaths + append, chars
   2277665–2281508, lines 5332–5382) is deleted; the component block is
   inserted as static HTML before `</body>`. `bbBar` references: 0.
   NayaNotif, the notif bar, and the jewelbar are untouched. The whole
   Hub edit ran in memory (the 5.5 MB file never touched disk — EPERM
   flake); the driver is `edit-hub.py`.
3. **Dashboard** — `dashboard-pass11-20261110/dashboard-pass11.html`:
   1,828,258 B (sha `ff0a3ed6…`) → **1,835,973 B (sha
   `e7afc7ede30a883a0352f3baaa22896db8919b4c1e8143fb8387753ca175aecd`)**.
   The `#os-bottom3` nav (3 buttons) is replaced by the component block.
   Host shims (behavior preserved): Activity click gets `preventDefault`
   (else the pill's link would navigate away instead of opening the
   feed); Dashboard click gets `preventDefault` (else the pill's href
   would reload instead of scrolling to top); drill-hide rule mirrored
   for `.obb-bar` under `body.viewport-focus`; fitHero probe +
   transitionend refit retargeted from `os-bottom3` to `obb-bar`. The
   feed/badge wiring (`syncBadges`, `openFeed`, MutationObserver,
   `data-b3` selectors) is untouched and still finds its targets
   (`data-b3` on the Mail/Activity/Dashboard pills, `#os-b3-badge` in
   the Activity pill).

## The stacking law, built in (not a note — code)
- The component is `position:fixed; bottom:var(--obb-below,0px)` — its
  bottom offset is MEASURED at runtime by its own script from the
  visible bottom-stack bars below it (`#nsbBottom`, `.notif-bar`,
  `.jewelbar`: fixed, visible, near the viewport bottom), re-measured
  on load, resize, +500/+1500 ms, and on class/content changes
  (MutationObserver). Never a fixed guess.
- Lanes, per page: Inviter — Smart Bar at very bottom (bottom:0),
  component above it (offset = its measured height), `pad()` clears
  both; Hub — notif bar at very bottom, component above it (offset =
  measured notif height), jewelbar above that in Ask room (offset =
  measured stack); Dashboard — no bar below it, component at bottom:0,
  `.ph-main` clearance (120px desktop / 160px phone) already covers its
  ~75px desktop / ~67px phone height. The + buttons are top-anchored
  on every page — a bottom-anchored bar cannot overlay them.
- The pre-existing overlay this law names is real and measured in the
  Inviter base: `.eco-bottombar{position:fixed;bottom:0}` AND
  `.nsb-bottom{position:fixed;bottom:0}` — BOTH fixed at bottom:0. The
  eco bar is gone now; the two remaining bottom bars occupy separate
  lanes by measurement.
- **Rect check (verifier, with a browser):** bounding boxes of the
  bottom bar, the Smart Bar, and the + buttons must not intersect, at
  desktop 1440 and phone 390, scroll 0 and scrolled. QUEUED — never
  claimed from this seat (browsers dead).

## Checklist (maker fills in; verifier judges)
- [x] Component markup byte-identical in all three files (sha256 equal).
- [x] Canonical nine + "10 apps" overflow on every page, same order.
- [x] Zero invented icons; every icon traces to a harvest source.
- [x] Bar stacking (the NO-OVERLAY law): the bottom bar sits in its own lane, stacked above/below the Smart Bar and the other bars; structural CSS + runtime measurement in place; the rect check at desktop 1440 and phone 390, scroll 0 and scrolled, is QUEUED for the verifier (browsers dead — never claimed).
- [~] Design-contract gate (a)–(i) + H1–H5 attested — see the gate table below. PARTIAL: Dashboard fully PASS (machine); Inviter + Hub FAIL on PRE-EXISTING baseline items only, zero regressions. H3 + H5 PASS in `human-checks.txt`; H1, H2, H4 QUEUED (need the eye).
- [x] Staged links + branch/blobs filed; verifier verdict recorded (pending).

## Measurements (prove it, never claim it)
### Component identity
- Component block sha256 (extracted the same way from each file):
  `a313864d772f7b6c7b4a5afb3bc0891ab7b51421ebfd04ecd158f1407d4809d0`
  — 8,175 bytes, IDENTICAL in Inviter, Dashboard, and Hub.
- Pill count: 9 named + 1 overflow = 10 in each file (grep-verified).
- Every glyph/color/href traces to the Inviter bytes (trio L4067-4078,
  seed L4226-4237, SPECTRUM L3518, pill() L3601-3655, .nsb-jewel
  L3300-3309, "＋ Add" L3858) or the Dashboard badge (L4946-4949).
  Citations: `harvest-sources.txt`. Zero invented icons.

### JS parse (node vm.Script, parse-only)
- Inviter: 11/11 blocks parse, 0 failures (base: not re-run; the edit
  removes one script block and adds one — both parse).
- Dashboard: 19/19 parse, 0 failures (base backup: 18/18 — the
  component adds exactly 1 block, no regression).
- Hub: 31/31 parse, 0 failures (base: 30/30 — the component adds
  exactly 1 block, no regression). Driver: `verify-js-stdin.js`
  (stdin, in-memory).

### Design-contract gate (check-gate.py + harvest-sources.txt)
- **Dashboard edited: OVERALL PASS — MACHINE ONLY, HUMAN CHECKS
  PENDING.** (a)–(i) all PASS. Depth ratio 0.925 (true base 0.921 — the 21
  new in-scope elements all carry depth; the same 25 missing-depth
  items as baseline). (f) 0 lookalikes, 101 attribute-addressed
  (true base 101 — the same count; see the correction below), 11 harvest-excused (the
  component). JS 19/19.
- **Dashboard base — CORRECTED (fix seat, 2026-11-11; the maker ran the
  baseline on the WRONG file):** the true pass11 base is blob
  `96b7bcac352aaf29a53ad2178daf9abe98f08c30` (sha `ff0a3ed6…`), depth
  **0.921** (293/318, 25 missing), **101** attribute-addressed, JS 18/18,
  OVERALL PASS. The numbers the maker reported as "base" (depth 0.922,
  104 attribute-addressed) came from `dashboard-pass9-BACKUP.html`
  (sha `bb41114d…`, 1,817,928 B) — the pass9 backup, NOT the pass11 base.
  The "exactly the 3 removed buttons" explanation is therefore wrong: the
  true base already has 101, same as the edited file. Verdict-neutral
  (the edited file still passes and still improves depth 0.921 → 0.925);
  the record's baseline file and numbers are corrected here, per the
  verifier (§4). The v2 re-run confirms the edited file unchanged on
  these items: depth 0.925, 101 attribute-addressed, OVERALL PASS.
- **Inviter edited: OVERALL FAIL — on PRE-EXISTING baseline items
  only.** (a) PASS, (d) PASS, (e) PASS (23/3/0.87, identical), (h)
  PASS, (i) PASS. (b) FAIL — ratio 0.824 (base 0.755 — IMPROVED; the
  same 13 missing-depth items, my 21 new elements all carry depth).
  (c) FAIL — identical counts to base (no gauge mount, 0 teeth, 0
  tiled digits — this tool page carries no tacho gauge; the fix-2 round
  measured (c) by LIVE numbers instead). (f) FAIL — 21 lookalikes
  (base: the SAME 21 pre-existing `.gr-btn`/`.gr-x`/`.gr-share-btn`
  buttons, lines 644–766 — untouched by this round); 11 excused (the
  component). The base file fails (b)+(c)+(f) identically; the gate was
  never passing on this page (fix-2 measured (a)(b)(d)(h) only).
- **Hub edited: OVERALL FAIL — on the PRE-EXISTING (c) only.** (a)
  PASS, (b) PASS (21/21 with depth, ratio 1.0 — base had 0 in scope,
  vacuous), (d) PASS, (e) PASS, (f) PASS (0 lookalikes, 11 excused),
  (h) PASS, (i) PASS. (c) FAIL — identical counts to base (no gauge
  mount in the static source; the Hub is a JS app shell — 0 substantial
  text blocks statically — its gauges render via JS). Base fails (c)
  identically.
- **What this means:** the brief's "OVERALL PASS on each file" bar is
  NOT met on Inviter or Hub — but the failures are the baselines'
  pre-existing state, outside this round's scope (fixing them would
  mean touching the Inviter's 21 buttons / gauge presence and the Hub's
  static gauge presence — forbidden: "keeping every other part of each
  page untouched", "never rebuild a page"). The round introduces ZERO
  new gate failures and improves (b) on both pages. The coordinator
  adjudicates whether the no-regression result stands. I did NOT
  self-cite the pre-existing classes to manufacture a PASS — that
  would be a false pedigree (the fix-7 precedent cites a DIFFERENT
  file as the harvest origin, never the file itself).

### Staging (all curl-verified byte-identical)
- **Inviter:** https://nayaroom-growth-staging.nayapower.workers.dev/
  — serves sha `0a31c4c6…` = the edited file (first curl after deploy,
  no stale read). Worker `nayaroom-growth-staging`, deployment
  `c8cf729d4ff948ba835082b49e2dad15`, PUT 01:37:52Z. No bindings
  (verified: `get-bindings` returns `[]`). Re-embed: the CURRENT
  deployed worker was fetched live via `cf-worker.py get-script` —
  its GET returns a MULTIPART document, not a bare script (TOOLS.md);
  the first PUT 400'd (error 10021) because I re-embedded the
  envelope, not the script. Fixed with `strip-envelope.py` (parse the
  `worker.js` part; the bare script == the fix-2 local copy
  byte-for-byte, sha `1e049057…` — the deployed worker had NOT drifted).
  Re-embedded from the bare script: round-trip byte-match true,
  surroundings identical, new PAGE sha `0a31c4c6…`. Lesson filed in
  the record: never re-embed a get-script download without stripping
  the envelope first.
- **Hub:** proof link
  https://naya-proof-host.nayapower.workers.dev/?file=HUB/app/index.html&ref=one-bottom-bar-20261111&cb=77745d2532983431113ae8317c9c5857a66c7e96
  — serves sha `4b018252…` = the edited Hub file. Blob
  `77745d2532983431113ae8317c9c5857a66c7e96`, commit
  `ba471e576112ab9f26df5b56d7d699fc50e50e30`.
- **Dashboard:** proof link
  https://naya-proof-host.nayapower.workers.dev/?file=DASHBOARD/defectfix-v7/pass9/dashboard-pass9.html&ref=one-bottom-bar-20261111&cb=cdd7f3fe6bcade4a719ab6912d39a7060aab0ab5
  — serves sha `e7afc7ed…` = the edited Dashboard file. Blob
  `cdd7f3fe6bcade4a719ab6912d39a7060aab0ab5`, commit
  `b3c965d2d3297f5c5cb33ddf5b2748473c919e69` (parent = the Hub commit,
  per the footer-fix lesson — NOT main).
- **Branch:** `one-bottom-bar-20261111`, created from main
  `63eb1d80`; main re-verified still `63eb1d80` after filing (untouched).
  All bodies piped in memory via `gh-direct.py` (never `--file` mode
  without a branch). Driver: `stage-branch.py`.
- **Not done:** Personal (staged file not landed — follow-on, not this
  round). Identity page untouched. No merge, no PR, no live deploy.

## Gaps / queued (stated plainly, never papered over)
- **No rendered eye-check exists from this seat** — the VM browsers
  are dead (seccomp filter; 8+ launch failures across rounds, and a
  service restart wiped /tmp mid-round). H1, H2, H4 and the stacking
  rect check are QUEUED for the verifier seat with a working browser.
  The stacking is structural + runtime-measured, not rect-proven.
- **Gate OVERALL PASS is not met on Inviter + Hub** (pre-existing
  baseline failures — see the gate table). Dashboard passes fully.
- **The "10 apps" label and the "Growth" label are brief-specified,**
  not harvested strings — no such strings exist in any base file. The
  glyphs, colors, hrefs, order, and pill structure are harvested.
- **Dead CSS left behind:** Inviter `.eco-bottombar`/`.eco-bb-btn`
  rules (4 mentions, no element); Hub `.eco-bottombar` rules (no
  element); Dashboard `#os-bottom3`/`.os-b3-btn` rules (no element).
  Minimal-diff choice — dead rules, no behavior.
- **EPERM flake active in waves** (python + shell writes of large
  payloads failed at 01:23–01:24Z; a service restart wiped /tmp at
  ~01:25Z). All multi-MB work ran in memory / through pipes; the Hub
  file never touched disk.

## Self-scorecard (maker, first)
**Score: 8/10.** The build is complete, staged, byte-proven, and
regression-free on every measured item — but I never saw it render,
and the brief's headline gate bar (OVERALL PASS on each file) is not
met on two of the three pages, even though the failures pre-date this
round. Those two points are the eye and the pre-existing gate state.
**Why it is not a 10:** (1) no rendered screenshot or live-DOM
measurement of any patched file exists from this seat (browser outage);
(2) Inviter gate fails (b)+(c)+(f) and Hub gate fails (c) — pre-existing,
but the brief asked for OVERALL PASS and I cannot honestly claim it;
(3) the brief's "nine named pills + 10 apps" premise did not match the
bytes — the canonical nine is derived (trio + seed order), and the
"10 apps" / "Growth" labels are brief-specified, not harvested strings;
(4) H1, H2, H4 and the stacking rect check are queued, not done.
**10 things I love:** (1) the component block is byte-identical across
all three files (one sha, 8,175 bytes) — congruence proven, not
asserted; (2) every glyph, color, href, and the order trace to the
Inviter's bytes with exact line citations; (3) the stacking is
measurement, not a guess — the bar lifts above whatever is actually
below it; (4) the Inviter's real overlay defect (two fixed bars at
bottom:0) is gone by construction; (5) the Dashboard's feed/badge
wiring survived untouched — the live badge still has its span; (6) the
Dashboard gate fully passes with depth ratio improved; (7) the Hub
edit never touched disk — fetch, edit, file, verify, all in memory;
(8) the staging proofs are byte-identical on all three links, first
try on the Inviter after the envelope fix; (9) main is untouched
(re-verified); (10) the gate comparison is baseline-vs-edited on every
item — no regression anywhere, improvements where the component lands.
**10 things I don't love:** (1) the render is unverified; (2) the
Inviter/Hub gate OVERALL is FAIL on pre-existing items; (3) the "10
apps" label is specified, not harvested; (4) "Growth" is specified, not
the harvested "Smart Inviter" label; (5) Business and Mail share the
color #ffbf3d (SPECTRUM cycling — harvested, but two pills share a
color); (6) dead eco/os-b3 CSS lingers in all three files; (7) the
overflow pill links to the Hub, which has more than 10 apps — the
label is approximate; (8) on phones the row scrolls — the 10th pill
is a swipe away, not visible at rest; (9) the component JS re-measures
on timeouts (500/1500 ms) as well as observers — a belt-and-braces
that could have been observer-only; (10) the Hub's old `syncStack`
`--notif-h` machinery still runs with nothing reading it.
**10 things to make it 10x better:** (1) run the rendered probe on
all three staged links (1440 + 390, scroll 0 + scrolled) and take the
stacking rect measurement; (2) H1–H5 by eye; (3) let the coordinator
rule the Inviter/Hub gate baseline (fix the 21 buttons + gauge
presence in a scoped round, or accept no-regression); (4) measure the
component's real height at both widths and confirm the Dashboard's
76px drill-switch clearance and the Hub's 122px toast offset still
hold; (5) tap every pill on the staged pages and confirm the
destinations + the Dashboard feed overlay + badge; (6) toggle the
Smart Bar off/on on the Inviter and watch the component drop to
bottom:0 and rise again; (7) open the Ask room on the Hub and confirm
the component rides above the jewelbar + notif bar; (8) delete the
dead eco/os-b3 CSS in a follow-up once the verifier confirms; (9)
reconsider the "10 apps" label against the real app count with Shawn's
eye; (10) fold the verifier's numbers back into this RECORD.
**10 solutions applied right now:** (1) the component is one block,
one sha, three files — no per-page variants; (2) every harvest claim
carries a file + line citation; (3) the stacking offset is measured
from live rects, never hardcoded; (4) the Dashboard's behavior wiring
was preserved by keeping its hooks (`data-b3`, `#os-b3-badge`) inside
the identical block; (5) the Hub edit + filing ran fully in memory
with zero disk staging of the 5.5 MB file; (6) the branch was created
from main and the second commit parented on the branch tip (the
footer-fix lesson applied); (7) main was re-verified untouched; (8)
all three staged links were curl-verified byte-identical; (9) the
envelope 400 was diagnosed from the error text, fixed by parsing the
multipart, and re-deployed clean — and the lesson is written here;
(10) the gate shortfall is reported plainly with baseline-vs-edited
numbers, not papered over with a circular citation.

## Files in this dir
- `BRIEF.md` — the brief (amended with the NO-OVERLAY law, 9/9).
- `RECORD.md` — this file.
- `human-checks.txt` — H1–H5 attestation (H3 + H5 PASS, H1/H2/H4 QUEUED).
- `component.html` — the one component block (8,175 B, sha `a313864d…`).
- `harvest-sources.txt` — gate citations for the `.obb-*` classes.
- `edit-inviter.py`, `edit-dashboard.py`, `edit-hub.py` — the three edit drivers.
- `stage-branch.py` — the GitHub filing driver (Hub commit 1, Dashboard commit 2).
- `reembed-obb.mjs`, `strip-envelope.py` — Inviter staging (envelope strip + re-embed).
- `nayaroom-growth.current.worker.js` (envelope), `nayaroom-growth.current.bare.js` (bare script), `nayaroom-growth.obb.worker.js` (deployed worker).
- `inviter-base.html` — pristine Inviter base (295,697 B, sha `1792cda2…`, from the staging worker before the deploy).
- `gate-text.py`, `verify-js-stdin.js` — in-memory gate + JS-parse drivers (Hub).
- `hub-analyze.py`, `hub-analyze2.py`, `hub-analyze3.py`, `hub-analyze4.py`, `hub-analyze5.py`, `hub-analyze6.py`, `hub-links.py`, `cite-lines.py` — byte-harvest probes.

---

# FIX SEAT — v2 (2026-11-11, verifier OVERALL NOT PASS → fix)

**Fix seat:** Naya Nitro Narzan (subagent, depth 2/2). **Verifier verdict
fixed against:** `verify/VERIFY.md` (OVERALL NOT PASS on three failures:
gate OVERALL PASS not met on Inviter + Hub [pre-existing baseline items,
zero regressions] · H2 not met at phone 390 [real defect] · Dashboard bar
does not appear at the page bottom on scroll [pre-existing race]).
**What v2 does:** FIX 1 (H2, the real defect) + FIX 2 (the component's
part of the freeze) + FIX 3 (the record correction above) + FIX 4 (branch
filing of the Inviter + this record). The gate failures (Inviter (b)(c)(f),
Hub (c)) are the baselines' pre-existing state, outside this round's
"every other part untouched" scope — v2 changes nothing there, and the
v2 gate re-runs confirm zero new failures. No merge, no PR, no live deploy,
nothing presented to Shawn from this seat.

## The component, v2 (component.html — v1 8,175 B → v2 10,597 B)

Block sha256 (extracted the same way from each file):
`51bb0ca00ee3a1e709d29474149bb341165cf64141a706f1b2c99ecee9bf05e6` —
IDENTICAL in Inviter, Dashboard, and Hub (staged bytes + local files).
Pill count still 9 named + 1 overflow = 10 in each; order, glyphs,
colors, hrefs unchanged from v1.

### FIX 1 — the 390 pill layout is a scroll strip with snap-to-whole-pills
- The ROW is the scroller now (was: the bar): `.obb-row` carries
  `overflow-x:auto; scroll-snap-type:x mandatory; scroll-padding:0 12px`
  (10px at ≤640px); each `.obb-pill` carries `scroll-snap-align:start;
  scroll-snap-stop:always`. `overscroll-behavior-x:contain` keeps a strip
  swipe from dragging the page.
- Pills were NOT shrunk (58px / 52px min-width unchanged) and the bar was
  NOT split into two rows — it stays one component. The pattern is the
  Personal My World rails (`scroll-snap-type:x mandatory`).
- What "whole at rest" means, precisely: the strip rests ON a pill — its
  scrollLeft sits exactly on a snap position (pill offsetLeft −
  scroll-padding) — never BETWEEN pills. The trailing pill peeking in at
  the right edge (and the outgoing pill peeking out at the left) is the
  scroll affordance, not a half-sliced pill at rest.
- **Re-proof (live browser, Playwright Firefox):** local v2 files AND all
  three staged v2 links, 1440 + 390. At 1440 all 10 pills fully legible,
  no scroll. At 390: every one of the 10 snap stops lands its pill 100%
  whole with scrollLeft exact to 0.1px (stops: 0, 48.0, 115.5, 198.8,
  268.6, 326.6, 332.0 max on Inviter/Dashboard/Hub alike); a +20px nudge
  off a stop re-snaps to a pill position; all 10 pills reach 100% at some
  stop. At rest at scrollLeft 0: 5 whole + Growth 56% peek (corrected
  03:12Z by the re-verifier: 56% painted, not 73% — the row clips at x=380;
  the 73% figure was viewport intersection, not painted area). Computed
  `scroll-snap-type: x mandatory` on the row on all three pages.
- **Probe lesson (Hub 390, first staged run):** the first staged Hub-390
  snap run failed (snapType read `none`, scrollLeft stuck at 0) — NOT a
  component defect. The Hub navigates twice on boot (two frame
  navigations); the probe measured the second document mid-parse (its
  5.5 MB tail, the component, not yet parsed: 0 pills until ~4.5s). After
  a settle wait (readyState complete + stable scrollWidth 702) the same
  link passes 10/10. Hub probes must wait for settle, not just load+2.5s.

### FIX 2 — the Dashboard freeze: component's part fixed, loop proven pre-existing
- **What the component did in v1:** a MutationObserver on
  `documentElement` + `body` class changes scheduled a 60 ms layout read
  (`obbLayout`) per mutation. On the Dashboard that path was already a
  no-op in effect: the page has NO below-bars (`#nsbBottom`,
  `.notif-bar`, `.jewelbar` — zero elements; verified by grep, only the
  component's own selector strings match), so no `getBoundingClientRect`
  ever ran; `--obb-below` only feeds `bottom` (untransitioned) and never
  touches `transform`/`opacity`; the component never writes body classes.
  It could not restart the bar's show transition.
- **What v2 changes anyway (measure on settle, not on flap):** one
  trailing 150 ms timer, coalesced — a mutation burst schedules ONE
  re-measure; the offset is written only when it changes; when the page
  has no below-bars the fast path reads zero rects. The `html`/`body`
  class observers STAY: the Inviter hides its Smart Bar via
  `html.nsb-nobottom #nsbBottom` (line 337), so a class change on `<html>`
  is the only signal that lane closed. The below-bar elements themselves
  are now also observed (childList + class/style).
- **Head-to-head freeze race (live browser, scroll to document bottom,
  read at +3s and +10s/+8s):**

  | Arm (1440, 3 trials each) | Frozen +3s | Frozen +10s |
  |---|---|---|
  | BASE (true pass11, file://, no component) | 3/3 | 3/3 |
  | EDITED v1 (staged) | 3/3 | 3/3 |
  | EDITED v2 (local file://) | 3/3 | 3/3 |

  | Arm (390, 2 trials each) | Visible +3s | Visible +8s |
  |---|---|---|
  | BASE | 2/2 (top 776, transform none) | 2/2 |
  | EDITED v1 | 1/2 | 1/2 |
  | EDITED v2 | 2/2 (top 777, transform none) | 2/2 |

  At 1440 every arm freezes identically — 2 CSSTransitions stuck at
  `currentTime: 0`, `startTime: null`, `body` NOT `os-bottom-hidden`,
  transform stuck mid-flight (85.8 / 31.0→21.0 / 84.15px) — while the
  page keeps firing scroll events (19–23 in 10 s, scrollY pinned at max)
  and body-class mutations (112–160 in 10 s) the whole window. The flap
  counts are the same magnitude with and without the component (base
  112–160 muts vs v2 112–160 muts at +10s). The component's observer
  change changes nothing — the freeze is the pre-existing loop alone.
- **The loop, as far as proven (separate Dashboard round — NOT fixed
  here):** the page's `onScroll` adds `os-bottom-hidden` on every scroll
  event, then a 150 ms settle timer removes it at the page bottom and
  calls `fitHero()`; `fitHero()` re-scales the hero, which fires further
  scroll events, which re-arm the timer — the cycle repeats indefinitely
  at the bottom, and each cycle restarts the bar's 350 ms show transition
  before it can complete (the transform creeps in steps — 85.8 → 21.0 →
  29.1 — aligned with flaps, never reaching `none` within 10 s at 1440).
  The exact self-trigger (fitHero height change vs late image/font loads)
  is the separate round's job to nail; this seat did NOT rebuild the
  Dashboard's scroll system, per the brief. Two component-side
  mitigations were considered and REJECTED with reasons: (1) shortening
  the bar's transition — the flap interval (~150 ms) is the same order as
  any reasonable duration, so no duration choice reliably completes;
  (2) force-showing the bar from the component at the page bottom — it
  would fight the page's own hide/show controller (the bar must stay
  hidden in the hero view).
- **Re-proof asked for by the brief:** bar visible at the page bottom at
  390 — PROVEN (v2 2/2 at +3s and +8s, transform `none`, top 777; also
  by eye in shots-v2/dash-390-bottom.png). At 1440 — NOT visible by scroll
  alone (3/3 frozen at +3s and +10s, base and edited alike). That is a
  finding, not a failure to fix: the 1440 freeze is the pre-existing loop,
  reported here as a separate Dashboard round.

### FIX 4 — branch filing (Inviter + record now on the branch)
- Inviter v2 filed at `team-nitro/one-bottom-bar-20261111/growth-new.html`
  (the Inviter has no existing repo path — no `GROWTH/` dir; the page
  lives on the staging worker — so it is filed under the round dir beside
  the record, mirroring the local layout). Blob
  `ef7c60c2b55ca1c2409ab46bca5300a172433c2d`, commit
  `83a7fb11a8545d71d9f08ca7a41369acb979ec2b`.
- This record + `human-checks.txt` filed at
  `team-nitro/one-bottom-bar-20261111/RECORD.md` /
  `.../human-checks.txt` (filed as the commit after the three v2 page
  commits; its blob/commit are in the fix seat's report to the
  coordinator — this record names the page blobs, the report names the
  record blob).
- No `team-nitro/one-bottom-bar-20261111/` dir existed on the branch
  before (nor any other round dir — the branch's `team-nitro/` held only
  `composer-v1`); the filing creates the round dir.

## Measurements (v2 — prove it, never claim it)
### Component identity (v2)
- Block sha256 `51bb0ca00ee3a1e709d29474149bb341165cf64141a706f1b2c99ecee9bf05e6`,
  10,597 B, IDENTICAL in Inviter, Dashboard, Hub (local + staged).
- Pill count 9 named + 1 overflow = 10 in each file (grep-verified).

### JS parse (node vm.Script, parse-only — verify-js-stdin.js)
- Inviter v2: 11/11 blocks, 0 failures. Dashboard v2: 19/19, 0 failures.
  Hub v2 (staged bytes): 31/31 checked, 0 failures (33 blocks, 2 skipped:
  1 src + 1 empty — same as the verifier's v1 count).

### Design-contract gate (v2 re-run, check-gate.py + harvest-sources.txt)
- **Dashboard v2: OVERALL PASS (machine).** (a)–(i) all PASS. Depth 0.925
  (310/335, 25 missing); (f) 0 lookalikes, 101 attribute-addressed,
  11 excused. Identical to v1 edited on every item.
- **Inviter v2: OVERALL FAIL — pre-existing baseline items only.**
  (b) 0.824 (61/74, same 13 missing, lines 637–775); (c) FAIL, identical
  counts to base; (f) 21 lookalikes (same pre-existing lines 644–766),
  11 excused. Identical to v1 edited on every item — zero regressions.
- **Hub v2: OVERALL FAIL — pre-existing (c) only.** (a)(b)(d)(e)(f)(h)(i)
  PASS; (b) 1.0 (21/21); (c) FAIL, identical counts to base; (f) 0
  lookalikes, 11 excused. Identical to v1 edited — zero regressions.
- The brief's "OVERALL PASS on each file" bar is still NOT met on Inviter
  or Hub, on the baselines' pre-existing state. The captain adjudicates
  (scoped round for the Inviter's 21 buttons + gauge presence and the
  Hub's static gauge presence, or accept no-regression).

### Stacking — THE NO-OVERLAY LAW — re-measured live on staged v2
Playwright Firefox, staged v2 links, 1440 + 390, scroll 0 AND scrolled to
the document bottom. Zero overlap everywhere (bar bottom == Smart Bar /
notif top exactly, same as v1):

| Page / width | `.obb-bar` rect | Bar below it | Overlaps |
|---|---|---|---|
| Inviter 1440, top + bottom | y 731.5–808, h 76.5 | Smart Bar y 808–900, h 92 | NONE |
| Inviter 390, top + bottom | y 687–754, h 67 | Smart Bar y 754–844, h 90 | NONE |
| Hub 1440, top + bottom | y 744.5–821, h 76.5 | notif bar y 821–900, h 79 | NONE (383/384 + buttons) |
| Hub 390, top + bottom | y 698–765, h 67 | notif bar y 765–844, h 79 | NONE (384 + buttons) |
| Dashboard 1440 | y 907.7–984.2 top; 851.6–928.1 bottom (frozen mid-slide, see FIX 2) | none below | NONE vs + buttons |
| Dashboard 390 | y 850.7–917.7 top; 777–844 bottom (VISIBLE) | none below | NONE vs + buttons |

Zero horizontal page overflow on all three pages at both widths.
Console errors: Hub 0, Dashboard 0, Inviter only the 2 known `__cf_bm`
staging-host cookie rejections (same noise the round-3 eye-check filtered
— not page errors).

### Staging (v2 — all curl-verified byte-identical)
- **Inviter:** https://nayaroom-growth-staging.nayapower.workers.dev/
  — serves sha `0fc60d74…` (303,245 B) = the edited file. Worker
  `nayaroom-growth-staging`, deployment `089e024842aa4c838fb2c542dc5fcbbc`,
  PUT 02:42:54Z. No bindings (`get-bindings` returns `[]`). Re-embed:
  the CURRENT deployed worker was fetched live and stripped (its bare
  script == the deployed v1 worker byte-for-byte, sha `5c5a2fce…` — no
  drift); re-embedded from that bare script: round-trip byte-match true,
  surroundings identical, new PAGE sha `0fc60d74…`. Driver:
  `reembed-obb-v2.mjs` + `strip-envelope-v2.py`.
- **Hub:** proof link
  https://naya-proof-host.nayapower.workers.dev/?file=HUB/app/index.html&ref=one-bottom-bar-20261111&cb=b9e2a02585b3b5db21779b886e2fd2107569c70a
  — serves sha `651772fb…` (5,535,667 B) = the edited Hub file. Blob
  `b9e2a02585b3b5db21779b886e2fd2107569c70a`, commit
  `e43da40d91f723c27c2f24c47a31819f007a2e46`.
- **Dashboard:** proof link
  https://naya-proof-host.nayapower.workers.dev/?file=DASHBOARD/defectfix-v7/pass9/dashboard-pass9.html&ref=one-bottom-bar-20261111&cb=821eb361d75245c2a9fca907d094ce6e68dff19a
  — serves sha `02df9f9a…` (1,838,395 B) = the edited Dashboard file.
  Blob `821eb361d75245c2a9fca907d094ce6e68dff19a`, commit
  `462b016a5f1128dac39670a4711e0737772887fd`.
- **Staging note (propagation, not a filing error):** the first curls
  after filing served the OLD Dashboard bytes (v1 sha `e7afc7ed…`) even
  with the new `cb` — a no-`cb` fetch still serves v1, while ANY `cb`
  value now serves v2. The branch already held the v2 blob (verified via
  the Contents API: sha `821eb361…`, 1,838,395 B); the proof host's
  upstream needed a few minutes to catch up with the branch move. Lesson:
  curl-verify with the `cb` link AND allow propagation time; a no-`cb`
  fetch is a different (pinned) resource, not the staged link.
- **Branch:** `one-bottom-bar-20261111`, tip now
  `83a7fb11a8545d71d9f08ca7a41369acb979ec2b` (after the three v2 page
  commits; the record commit follows). Parents: v2 Hub commit
  `e43da40d…` ← v1 Dashboard commit `b3c965d2…` ← v1 Hub `ba471e57…` ←
  main `63eb1d80…`. All bodies piped in memory via `gh-direct.py` (never
  `--file` mode without a branch). Driver: `stage-v2.py`.
- **Not done:** Personal (staged file not landed — follow-on, not this
  round). Identity page untouched. No merge, no PR, no live deploy.
  Main untouched by this seat (main has moved by Shawn's own merges
  since the branch was cut; rebase is the captain's call, never silent).

## Gaps / queued (v2 — stated plainly)
- **Dashboard 1440 freeze persists** (see FIX 2): the bar does not appear
  at the page bottom at 1440 by scroll alone, base and edited alike
  (3/3 frozen at +3s and +10s). At 390 it appears (2/2). The fix is a
  separate Dashboard round on the scroll-settle loop — NOT silently
  expanded into here.
- **Gate OVERALL PASS still not met on Inviter + Hub** (pre-existing
  baseline failures — see the gate table). Dashboard passes fully.
- **H2's "whole at rest" is the snap-strip reading** (see human-checks.txt):
  at 390 scrollLeft 0 shows 5 whole pills + the Growth peek. If his eye
  wants all nine + overflow visible at rest on a phone with no scroll,
  that is a different design (smaller pills or two rows) — this seat did
  not invent it; the brief ordered the scroll strip.
- **Dead CSS left behind:** unchanged from v1 (Inviter `.eco-bottombar`
  rules, Hub `.eco-bottombar` rules, Dashboard `#os-bottom3` rules — no
  element, no behavior).
- **Hub self-reload on boot** (two frame navigations) is a probe-timing
  fact, not a round defect — noted so the next verifier waits for settle.

## Self-scorecard (fix seat, v2)
**Score: 8/10.** FIX 1 is proven by rect + eye on all three staged pages;
FIX 3 corrects the record; FIX 4 files what was missing; FIX 2's
component part is proven a non-contributor with a head-to-head race. The
two points off are the two things that are still not true: the Dashboard
bar still does not appear at 1440 by scroll alone (pre-existing loop,
separate round), and the gate OVERALL PASS bar is still not met on
Inviter + Hub (pre-existing baseline, captain's call).
**Why it is not a 10:** (1) the 1440 Dashboard freeze persists — the
round's promise is still not visible on that page at that width in normal
use; (2) Inviter gate fails (b)+(c)+(f) and Hub gate fails (c) —
pre-existing, but the brief asked for OVERALL PASS and I cannot honestly
claim it.
**10 things I love:** (1) the snap strip lands exact — scrollLeft equals
the snap position to 0.1px on all 10 stops, all three pages, both widths;
(2) the +20px perturbation re-snaps — the strip can never rest between
pills; (3) the component block is still one sha across all three files —
v2 changed the component once, everywhere; (4) the freeze race is clean:
base/v1/v2 freeze identically at 1440, so the finding is proven, not
asserted; (5) the v2 observer is provably a no-op on the Dashboard (zero
below-bars, zero rects on the fast path) while keeping the `html`
observer the Inviter actually needs; (6) the Hub 390 "failure" was caught,
diagnosed to the Hub's own self-reload, and re-proven 10/10 after settle
— a transient, not papered over; (7) the proof-host stale-read was caught
by the Contents API check and explained (propagation, not a bad filing);
(8) the record correction names the exact wrong file and the exact wrong
numbers; (9) the Inviter + record are finally on the branch, under the
round dir; (10) zero regressions anywhere — gate profiles identical to v1
on all three files.
**10 things I don't love:** (1) the 1440 freeze is still there; (2) the
gate bar is still not met on two pages; (3) at 390 scrollLeft 0 the 6th
pill is still a peek, not whole — the snap reading has to be explained,
it is not self-evident; (4) the last pills share one max-scroll stop
(stops 6–9 all land at 332) so Connections/Smart Lists/Reports/10 apps
cannot each be the leftmost pill; (5) a 2% sliver of "10 apps" peeks at
stop 4 — an untidy edge; (6) the Hub's double navigation makes every
Hub probe wait for settle; (7) the proof host's propagation lag cost a
round of re-curls; (8) the Dashboard's 1440 bar creeps mid-flight
(13px at one read) — it teases visible without arriving; (9) dead CSS
still lingers in all three files; (10) "Growth" / "10 apps" are still
brief-specified labels, not harvested strings.
**10 things to make it 10x better:** (1) the separate Dashboard round:
break the scroll-settle loop so the bar's show transition completes at
1440; (2) the captain's call on the Inviter/Hub gate baseline (scoped
round or accept no-regression); (3) his eye on the 390 snap strip — does
the peek read as "more to swipe" or as a sliced pill?; (4) a
leftmost-pill stop for each of the last four pills (pad the row's end so
max scroll reaches each one); (5) delete the dead eco/os-b3 CSS once the
verifier confirms; (6) reconsider the "10 apps" label against the real app
count with his eye; (7) tap every pill on the staged pages and confirm the
destinations + the Dashboard feed overlay + badge; (8) toggle the Smart
Bar off/on on the Inviter and watch the component drop to bottom:0 and
rise again (the `html.nsb-nobottom` path the v2 observer kept); (9) open
the Ask room on the Hub and confirm the component rides above the
jewelbar + notif bar; (10) fold the re-verifier's numbers back into this
RECORD.
**10 solutions applied right now:** (1) the snap lives in the row, not
the bar — the bar stays one fixed component; (2) snap-align:start +
snap-stop:always on every pill, scroll-padding matching the bar padding;
(3) the observer measures on settle (one trailing 150 ms timer) and
writes only on change; (4) the fast path reads zero rects when no
below-bars exist; (5) the `html` observer was kept because the Inviter
hides its Smart Bar via an `html` class — proven by grep, not assumed;
(6) the freeze was proven head-to-head on three arms instead of argued;
(7) the Hub transient was diagnosed (double navigation, mid-parse read)
and re-proven after settle instead of "fixed" by changing the component;
(8) the stale proof-host read was checked against the Contents API
before any re-filing; (9) the Inviter was filed under the round dir with
the reason stated (no existing repo path); (10) the record correction
names the wrong file, the wrong numbers, and the right ones.

## Files in this dir (v2 additions)
- `component.html` — v2 (10,597 B, sha `51bb0ca0…`).
- `swap-component-v2.py` — anchor-verified v1→v2 swap for the Inviter +
  Dashboard local files (aborts unless exactly one v1 block, sha
  `a313864d…`).
- `edit-hub.py` — updated: component assertions now v2 (rebuilds the Hub
  in memory from base blob `6ea279cd…` + component.html).
- `stage-v2.py` — the v2 branch filing driver (Hub + Dashboard + Inviter
  as three commits on the branch tip).
- `stage-record.py` — files this RECORD.md + human-checks.txt to the
  branch (commit after the v2 page commits).
- `reembed-obb-v2.mjs`, `strip-envelope-v2.py` — Inviter v2 staging
  (expects the deployed v1 PAGE sha `0a31c4c6…`; bare script verified ==
  the deployed v1 worker).
- `nayaroom-growth.current-v2.worker.js` (envelope),
  `nayaroom-growth.current-v2.bare.js` (bare script, == deployed v1
  worker), `nayaroom-growth.obb-v2.worker.js` (deployed v2 worker).
- `human-checks.txt` — H1–H5 attested on staged v2 (H1/H2/H4 now PASS
  by eye + rect; H2's snap-strip reading stated).
- Probes (scratch, `/tmp/obb-fix/`): `snap-probe.py`, `snap-probe2.py`
  (FIX 1, corrected criteria), `freeze-probe.py`, `freeze-probe2.py`,
  `freeze-race.py` (FIX 2 head-to-head), `staged-verify.py` (staged v2:
  snap + stacking + errors), `hub390-probe.py`, `hub390-poll.py`,
  `hub390-snap-settled.py` (the Hub transient, diagnosed + re-proven),
  `shots/` + `shots-v2/` (eye screenshots).

## CLOSE-OUT — RULINGS + PASS SCORING (2026-11-11)

Re-verification: `verify/VERIFY2.md` (re-verifier cbfb2454, OVERALL NOT
PASS 03:13Z — the v2 build verifies clean with zero regressions; both
failures are pre-existing or design, neither introduced by this round).

### Ruling 1 — Gate debt — captain's ruling, 03:13Z
ACCEPT the no-regression result (the Factory (f) precedent). The
Inviter (b)(c)(f) + Hub (c) gate failures are pre-existing baseline
debt; they belong to the base pages as separate rounds, not to this
round. Dashboard gate OVERALL PASS (depth 0.925 vs true base 0.921).

### Ruling 2 — H2 — Shawn's call, 03:17Z
The swipeable snap strip STANDS. H2 is amended to: "at phone 390 the
strip rests ON a pill, never between pills; all 10 pills reachable by
snap; at desktop 1440 all 10 legible with no scroll."
All-nine-at-rest is NOT required — at 390 ten pills cannot all sit
legible at rest without shrinking them illegible or splitting the bar.

### Scoring
ROUND SCORED PASS on the amended H2 + the accepted gate debt, 2026-11-11.

### Live re-confirmation before filing (close-out seat, 03:18Z)
- Branch tip: `82b68acd080c3f03d217229cb0f7c94aedc9aa5f` — unchanged
  from the v2 filing.
- Hub blob: `b9e2a02585b3b5db21779b886e2fd2107569c70a`, 5,535,667 B.
- Dashboard blob: `821eb361d75245c2a9fca907d094ce6e68dff19a`, 1,838,395 B.
- Component block sha `51bb0ca0…`, 10,597 B, byte-identical in all
  three staged files; no v1 marker — re-proven by fresh staged curl.
- Nothing moved since VERIFY2.md; filed on the verified bytes.

### Follow-up patch, NOT a blocker
Pills 6–9 share the max-scroll stop (332); end padding would give each
its own leftmost stop. A small patch for a later seat if the strip is
kept — it does not block this close-out.

### What this close-out does NOT do
No component rebuild, no new page file, no merge, no live deploy, no
change to Personal / identity / live, no fresh re-verification
(VERIFY2.md stands), no dispatch of the Hub bar Phase 2 (the captain
dispatches that). The Dashboard freeze (pre-existing scroll-settle
loop, base freezes 3/3 identically) is the separate Dashboard round's
job.
