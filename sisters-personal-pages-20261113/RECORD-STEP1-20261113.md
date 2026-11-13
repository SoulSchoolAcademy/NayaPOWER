# RECORD — STEP 1: LINEAGE PROOF + SLOT MAP (Sisters' Personal Pages, 2026-11-13)

**Maker seat:** sisters' Personal pages round. **Work dir:** `team-nitro/sisters-personal-pages-20261113/`.
**Brief:** `BRIEF-SISTERS-PERSONAL-PAGES-20261113.md` (34,054 B, check-brief 9/9).
**Status:** Step 1 COMPLETE. No build yet. No deploy, no merge, no PR, no mail, no live touch.

## 0. ACTIVATION — read before any design work (2026-11-13 ~04:20–04:30Z)

- [x] 1. `THE-PLAYBOOK.md` — the HOW (Grade 6 locked in).
- [x] 2. `DESIGN-INTELLIGENCE-REPORT.md` — the WHY.
- [x] 3. `hub-board-edit/intelligent-block-rules-LAW-20261106.md` — the block rules, LAW (ratified 2026-11-06).
- [x] 4. `clarity-confirmation-act-DRAFT-20261106.md` — the Act (DRAFT; §2 conduct + §3 design read in full; §1/§4–§6 headings + status).
- [x] 5. `THE-NAYA-BRAND.md` — the brand.

### Applied-laws table (law + the part it produced)

| # | Law (source) | Part it produced in this round |
|---|---|---|
| 1 | Playbook Truth 1 — calculate, never eyeball; 8px grid; exact numbers | Every count in this record is a counted first-hand measurement (swap counts 20/20 live + 27/27 template, byte sizes, shas). No eyeballed claim. |
| 2 | Playbook Truth 10 / Harvest-first — use the parts registry; compose, don't create | The renderer embeds the Personal template itself (live v9 + two named fixes); zero invented parts. The swap machine is the clone round's `build-clone.py`, reused, not rewritten. |
| 3 | Playbook — white text, obsidian base, top-left light, slow motion | Carried by the harvested template bytes; the renderer changes labels only, never the CSS. |
| 4 | Intelligence Report — premium is exact numbers, real materials, slow motion; never "improve" what Shawn didn't ask to change | The renderer does not restyle, recolor, or re-space anything. The two template fixes carried are Shawn-ordered fixes, named as such, not maker improvements. |
| 5 | Intelligent Block Rules L1–L11 — one set of laws, every object real, one light, own-color ignition, white text | The story/motto/vision/mission/goal sections are the template's own Intelligent Block layers (`ib-layer`, `ib-nutshell`, jewel `os-jewel-h`); the renderer fills their text slots only. |
| 6 | Block Rules §4.3 — the nutshell is the distillation; §4.4–4.8 — the layers | The About view's sections (motto/vision/goals/mission/purpose/whatido) are the template's layer boards; the slot map below names each layer's source answer. |
| 7 | Clarity Act §2a — the five gates before every consequential action | Gates run below (§7) before the build-script edit. |
| 8 | Clarity Act §2d — never rebuild, compose don't create; harvest first; prove before reporting; never report done from scroll-0 alone | The fix is a renderer swap, not a new page; proof is served bytes + rendered pages at 1440/390/360, scroll 0 AND scrolled (Step 4). |
| 9 | Clarity Act §3b — the Real Object Law, seven principles | The cover (`.ph-cover` gradient), avatar orb, pills, buttons, bottom bar are the template's real objects, harvested whole. |
| 10 | THE-NAYA-BRAND — every button elite, every number alive, two-second test | Buttons/pills/bar/numbers are the template's own; the renderer adds no button, removes none, flattens none. |

## 1. GOVERNING STANDARD — SHAWN'S CHARGE, THE BILLION-DOLLAR HOME (04:20Z, above the brief)

Quoted, in substance, from `SHAWNS-CHARGE-20261113.md`:

> "We already have the billion-dollar home — the Personal page, the Business page, the Space page, the interconnected apps, one brand, one franchise, a matrix of high-level design with a distinct look and feel, like Bugatti. Not anyone can cook, but not everybody's a chef. We give every citizen the ultimate vehicle — why create a new one? The walk built a new thing (a card) instead of working on the home we already have. That is the new-employee mistake: instead of working on the high-tech home, they try to create a new product, and the new product is absolute garbage — grade-one stuff next to master-level work. A new employee's job BEFORE any work is to learn everything about how the product works and operates, get aligned and locked in with the current state, and be aware of how things work so they do things right. It is time to grow up, time to mature, time to get out of preschool — no more kid games."

**What it means for this round:** the fix is NOT a new page and NOT a new design. It is the Personal page itself, harvested byte for byte where it applies. The step-1 slot map below IS the new-employee proof — the maker proving they know the Personal page (its anatomy, its parts, how it operates) before changing anything. The changed walk must produce that same page, not a look-alike. If any part is invented instead of harvested, the round fails. **Evidence against the charge (harvest ledger):** every part on the staged pages traces to live Personal v9 bytes (sha `992ab18c…`) or the two named Shawn-ordered fixes; **built new: nothing.** The harvest ledger is §5 + the slot map (§6).

## 2. LINEAGE PROOF (one line)

**The deployed staging worker is the Q10-lineage worker (v22), and its `/pages/` renderer is byte-identical in both candidate build scripts — so the base file is the Q10 build script, `walk-questions-10-20261112/build-beginning-staging-worker.py`.**

Evidence (all first-hand, 2026-11-13 ~04:22–04:30Z):
- Deployed `/pages/sophia/sophia`: HTTP 200, 2,642 B, sha256 `82c5319c…`, the narrow card (`.wrap{max-width:680px}`, `YOUR PERSONAL PAGE`, one `Back to your Hub`) — confirms DIFFERENT, as the 04:11Z verdict said.
- Renderer regions (`pageBody` + `composePages` + `pageHtml`, Q10 lines 166–230 vs S2 lines 174–238): `diff` EMPTY, 3,784 B each — byte-identical. Either script generates the same `/pages/` bytes.
- The deployed WORKER is Q10-lineage, not S2: `/naya-a.jpg` serves HTTP 200, 484,837 B JPEG — the Q10-only KV route (the S2 script has no such route). Corroborated by the Q10 record: v22, deployment `2dcc6ecb…`, worker sha `61b17c9f…`, 4,343,251 B, 2026-11-13T01:51:39Z. The S2 dir's generated `.js` is 0 bytes (EPERM flake damage) and was never the deployed worker.
- The two scripts differ ONLY in: ROUND path, walk-sha assert, the joins insert (S2 carries the newer back-end fix), and the Q10 naya-picture route. No renderer difference.
- **Base file: `~/workspace/team-nitro/walk-questions-10-20261112/build-beginning-staging-worker.py`.** The template inside it is the source; the `.js` is a generated artifact.

## 3. Q10 SHA RECONCILIATION (read first-hand before rebuilding)

- Build script asserts walk sha `a3510446` (line 52) — STALE.
- The walk file the script actually reads (`ROUND/walk-beginning-fixed.html`): **3,365,491 B, sha256 `4e8500c2…`** — the gold-fixed LOCAL copy (Q10 record: names-page base `a3510446` → `4e8500c2` by the identical gold fix).
- The FILED Q10 walk (branch `walk/questions-10-20261112`, file `walk-beginning-fixed-q10-gold.html` locally): **3,364,147 B, sha256 `be55a494…`** — the Q10-filed copy (base `227a667e` → `be55a494` by the same gold fix; the two files' fixed rule block + gold strip are byte-identical per the Q10 record).
- **Reconciliation:** update the assertion to `4e8500c2` — the bytes that are there in the base file's own dir. The worker this round builds embeds `4e8500c2`.
- **Open v23 assembly decision (named, not silently chosen):** `4e8500c2` (local, names-page lineage) vs `be55a494` (filed, Q10 lineage) differ by 1,344 B because their BASES differ; both carry the identical gold fix. Which walk the v23 deploy worker embeds is the v23 assembler's call; this round's worker embeds `4e8500c2` and says so on its face. The renderer change is walk-independent (it does not touch the walk file).

## 4. LIVE PERSONAL V9 — HARVESTED FIRST-HAND

- `curl https://nayanet.app/personal` 2026-11-13 ~04:22Z: HTTP 200, **1,484,185 B, sha256 `992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50`** — EXACTLY the brief's expected values. Live bytes are the authority; the local copy was re-verified, not trusted.
- Template: `space-business-mirror-personal-20261112/template-composed.html`, **1,486,773 B, sha256 `61002d15…`** — re-verified first-hand against the fresh live harvest: the diff is EXACTLY 3 ops — the rooms-plus fix (2 hunks: `rooms.style.position=phone?'absolute':'fixed'` + its comment) and the 23-line hero-fix style block (`hero-fix-20261112`) before `</body>`. Nothing else.
- **Decision (recorded for the captain's double-check): the renderer embeds the COMPOSED template, not raw live v9.** Reason, measured: live v9 carries two defects Shawn already ordered fixed — hero overlap up to 3,596 px² at 390 (Change cover vs name) and rooms-plus occlusion up to 1,408 px² (clone round's probe, live Personal as control); the template reads 0×0 on both at every width. Serving raw live v9 would serve known defects to every citizen; the composed template IS live v9 plus exactly those two Shawn-ordered fixes, each proven by diff. The base is still live bytes (re-verified above); the fixes are named, not hidden.

## 5. STATIC-FILE SEARCH — SHAPE STAYS (a)

Search for static per-sister page files (repo, worktree, proof host), 2026-11-13 ~04:23Z:
- Local workspace `grep -rli "pages/sophia|pages/thea" --include="*.html"`: 11 hits — ALL references, none a page file: `user/files/index-2.html`, `family-activation-20261113/surface-fragment-twelve.html`, `team-transparency-hub-twelve.html`, `bottom-icons-ultimate-trio-20261113/hub-live.html` + `hub-fixed.html`, `factory-pipeline/hub-assets-staging/index.html`, two Naya notes, a screenshot, a pygments lexer. The match contexts are LINKS to the staged `/pages/` URLs (e.g. `https://naya-walk-beginning-staging.nayapower.workers.dev/pages/sophia/sophia`), not page content.
- Repo `git grep -l "pages/sophia|pages/thea" -- "*.html"` in `~/workspace/nayapower-repo`: ZERO hits.
- No `pages/<alias>` directory serves sisters anywhere.
- The serving path is proven by the code: `/pages/<alias>/<slug>` (build script lines 439–453) reads `page_<alias>_<kind>` from KV, falls back to Supabase `page_about`, renders via `pageHtml`. No static files exist in that path.
- **Shape stays (a): change the walk's builder. No file is named for (c) because none exists.**

## 6. THE SISTERS' BOX DATA — READ-BACK (read-only, never edited)

`GET /api/welcome/box?alias=` on staging, 12/12 HTTP 200, ~04:22Z:

| Sister | Box | Projects | Pages | Answers | Personal slug | Business slug | Space slug |
|---|---|---|---|---|---|---|---|
| sophia | 1 | 1 | 3 | 10 | sophia | sophias-lessons | the-learning-circle |
| thea | 1 | 1 | 3 | 10 | thea | theas-record | the-knowing-room |
| zoe | 1 | 1 | 3 | 10 | zoe | zoes-dispatch | the-doers-room |
| astraea | 1 | 1 | 3 | 10 | astraea | astraeas-gates | the-scales-room |
| vera | 1 | 1 | 3 | 10 | vera | veras-proof | the-proof-room |
| wren | 1 | 1 | 3 | 10 | wren | wrens-factory | the-builders-nest |
| iris | 1 | 1 | 3 | 10 | iris | iriss-bridge | the-bridge-room |
| ruth | 1 | 1 | 3 | 10 | ruth | ruths-circle | the-family-room |
| terra | 1 | 1 | 3 | 10 | terra | terras-ground | the-ground-room |
| esme | 1 | 1 | 3 | 10 | esme | esmes-offer | the-welcome-room |
| mira | 1 | 1 | 3 | 10 | mira | miras-vault | the-memory-room |
| aurelia | 1 | 1 | 3 | 10 | aurelia | aurelias-scorecard | the-golden-room |

- Every box: 1 box, 1 project, 3 pages, all ten answers (`about, into, vision, mission, motto, goal, biz_do, biz_offer, biz_building, space`) — correct, word-for-word. Store is `kv-fallback` (citizen_worlds insert refused 401 RLS — named in the Box note, as the S2 record says; the server-side key is his hand).
- **No cover, photo, avatar, or tagline field exists in any sister's Box** (grep over all 12 box JSONs: zero `cover`/`photo`/`avatar`/`image` fields). The cover and photo slots are therefore filled by the template's own cover and initial orb — see the slot map. Nothing is invented to fill them.

## 7. SLOT MAP — HOW THE PERSONAL PAGE TAKES EACH PART (the new-employee proof)

The template is a client-side app: the STATIC frame renders from the served HTML; the JS then fills the feed and sections from Supabase by `PAGE_ALIAS`. The renderer swaps the statics server-side; the JS fill rules decide what survives. Every rule below was read first-hand in the live bytes.

### 7a. The runtime rules (read in the template's JS — these govern the swaps)

- **Story:** `setStoryText()` is called ONLY when a story row exists (legacy `{k:'about'}` row, then the aboutsec `s:'story'` row wins). With no rows — the sisters have none — the static story stands. Mirrors (`localStorage naya.about` / `naya.aboutsec.story`) override only when present on that device. → **Static story swap survives.**
- **Sections:** the fill loop `['about','goals','mission','vision','love','dont','motto','purpose','whatido']` sets a section's text ONLY when a `smart_notes {k:'aboutsec', s:<key>}` row exists (`if (!tp || !sec.length) return;`). With no rows, the static text stands. → **Static section swaps survive.**
- **Seed rule (RETHINK + FIX-6):** for `goals/mission/vision`, if nothing was ever saved (`__osAboutSecs[key]===undefined`), the seeded static text IS the value — the JS adopts it into `__osAboutSecs` (unless it starts with "No "). → **Swapped vision/mission/goals statics become the page's own values, and Edit re-seeds from them.**
- **Motto — the one clobber:** static motto is EMPTY, and FIX-7 paints `No motto yet — tap Edit and put it in one line.` into `os-sec-motto-text` whenever no motto row/mirror exists — unconditionally overwriting static text. A statically injected motto WOULD be clobbered after the read resolves. → **The renderer injects the motto text into the empty element AND seeds `window.__osAboutSecs['motto']` with an inline script placed immediately before the main `<script>` block (the one containing `function loadAbout(){`, exactly 1 in the template). FIX-7's own condition (`__osAboutSecs['motto']!==undefined`) then skips the paint. This is data seeding through the page's own variable — the same pattern as its `PAGE_ALIAS` assignment — not a new part.**
- **Purpose / whatido:** no clobber path (fill loop returns with no rows; FIX-7 targets motto only). Static swaps stand.
- **Story voice:** the page-kind mechanism relabels `My Story` → `Our Story` at runtime for business/space (proven in the rendered DOM by the clone round). Section labels (`My motto`, `My vision`, …) are NOT relabeled — that is the template's own behavior on Business/Space clones too; kept as-is (harvest, don't invent).
- **Feed:** `fetchWall(200)` reads `smart_notes` / `naya_notes` by `owner_alias = PAGE_ALIAS`. Sisters have no rows → the template's honest empty state: `No posts yet — be the first to make a post on this feed.` (string present in the template, ×1). The feed is the citizen's own feed — empty because she has truly posted nothing.
- **Cover:** `.ph-cover` (`id="cvr"`) is a CSS gradient — radial purple/magenta/blue glows over `linear-gradient(135deg,#1a1a3e,#2d1b4e 30%,#4a2b7a 55%,#0f3460 80%,#16537e)`, 360px. NO image URL, no per-citizen cover anywhere. `Change cover` (×4) lets the citizen pick one later. → **Every citizen gets the template's cover gradient — never empty, never a gray band.**
- **Photo:** the avatar is a data-URI SVG (256×256) with stroke `#a06bff` (×1) and letter `N` (×1). → **Stroke stays `#a06bff` (the template's own — Personal's purple; no per-sister color exists in the Box); letter becomes the citizen's initial (first letter of `box.name`, uppercase). Initial orb by default; a face only by the citizen's own choice (no face data exists).**
- **Name/tagline on load:** `naya.name` in localStorage overwrites `pname` if present (the template's own behavior on live Personal too — kept, not changed; the probe uses fresh profiles). The tagline (`ptag`) is editable on click and is NOT overwritten from any backend row on load; the `sa$` pname/ptag writes run only inside the Smart Academy course overlay and restore after. → **Swapped name/tagline stand on cold load.**
- **Saves:** `PERSONAL_SAVE_URL = 'https://naya-save-staging.nayapower.workers.dev/api/personal/save'` — About-edit saves from staged pages already go to the staging save worker. Nothing to change.
- **Pills:** Naya Academy (×9) / AI Masterclass (×11) / Fast Action Club (×8) are the template's static shared courses — kept verbatim, never invented, never removed. (Shawn's videos are shared courses, not Personal identity — asserted present by the clone build.)
- **Buttons:** the 9 up-act buttons (Message · About · My World · Skills · Connections · Invite · Share · Join NayaNET · Settings) + `Add something` + the `+` menu (Make a post · Send a message · Add a Smart Link · Add to a list — 4 items, as live Personal carries them) + the bottom bar (trio + `+`, `bottombar` ×8, notif chips mail/activity/stats) are all inside the template bytes. Join href is `https://nayanet.app/joinus` (×3). **Harvested, never rebuilt.**

### 7b. The swap table — template slot → citizen supply (all counts asserted by the renderer at request time; a failed count fails loudly, never serves a half-swapped page)

Counts verified first-hand against the FRESH live file (20/20) AND the composed template (27/27, 0 mismatches).

| # | Template slot (live source) | Count | Renderer supplies (from the Box) |
|---|---|---|---|
| 1 | `<title>Shawn Vibert</title>` | 1 | `pg.headline` (pageNames title: personal `sophia`, business `Sophia's Lessons`, space `The Learning Circle`) |
| 2 | `>Shawn Vibert</div>` (pname) | 1 | `pg.headline` |
| 3 | `class="os-owner-name">Shawn Vibert</span>` | 1 | `pg.headline` |
| 4 | `localStorage.setItem('naya.name','Shawn Vibert')` | 1 | `box.name` (`Sophia`) |
| 5 | `pn.textContent='Shawn Vibert'` | 1 | `box.name` |
| 6 | `Memberships — Shawn Vibert` | 1 | `Memberships — ` + `pg.headline` |
| 7 | Story text (abouttext + os-story-text + 2 JS fallbacks) | 4 | personal: `about` · business: `biz_do + " " + biz_offer + " " + biz_building` · space: `space` |
| 8 | Tagline + `.` (static div + 2 JS) | 3 | personal/space: `into` · business: `biz_offer` |
| 9 | `Shawn&rsquo;s Smart Notes` | 1 | `box.name + &rsquo;s Smart Notes` |
| 10 | `Shawn&rsquo;s Naya Notes` | 1 | `box.name + &rsquo;s Naya Notes` |
| 11 | `>My Activity — tap for the full dashboard ↓</button>` | 1 | personal: keep `My Activity` · business/space: `Our Activity` (clone rule) |
| 12 | Avatar stroke `stroke%3D%22%23a06bff%22` | 1 | KEEP `#a06bff` (no swap — template's own color) |
| 13 | Avatar letter `middle%22%3EN%3C/text` | 1 | First letter of `box.name`, uppercase |
| 14 | `var baUser='Shawn'` | 1 | `box.name` |
| 15 | `||'Shawn'` | 1 | `box.name` |
| 16 | `|| 'Shawn'` | 1 | `box.name` |
| 17 | `return 'Shawn'` | 1 | `box.name` |
| 18 | `flagship-personal` literals | 7 | `alias` |
| 19 | `window.MSHIP_PAGE_KIND='personal'` | 1 | `pg` kind (`personal` / `business` / `space`) |
| 20 | Injector fallback `(… ? PAGE_ALIAS : 'flagship-community')` | 1 | `alias` |
| 21 | Vision static `A world where intelligence compounds and everybody wins.` | 1 | `vision` |
| 22 | Mission static `Build NayaNET — the intelligent highway for the AI age.` | 1 | `mission` |
| 23 | Goals static `One million citizens by 2027.` | 1 | `goal` |
| 24 | Motto empty `id="os-sec-motto-text" …></p>` | 1 | `motto` (injected text + `__osAboutSecs` seed script — see §7a) |
| 25 | Purpose static `No purpose written yet — …` | 1 | KEEP (no walk answer asks purpose; the empty state is the template's own, same as live Personal — honest, not invented) |
| 26 | Whatido static `No what-I-do yet — …` | 1 | `biz_do` (Q7, "what you do") |
| 27 | Story-tab statics | — | Covered by #7 (os-story-text is one of the 4) and by `syncStoryFields` (mirrors sec → story tab at runtime) |

**Kind mapping (words → pages):** Personal says "My Story", Business and Space say "Our Story" (page-kind mechanism). Personal story = `about`; Business story = the three `biz_*` answers in pageBody order; Space story = `space`. The `##` body composed by `pageBody` is NOT rendered by the template (it has no slot for it) — the template's About view IS the body: story + motto/vision/goals/mission/purpose/whatido sections, each fed by exactly one walk answer. `composePages`/`pageBody` stay untouched (they write the page records at completion time); only `pageHtml` changes (render time).

**What the renderer does NOT touch:** the sisters' Box data; the walk's ten questions, names page, end slide, Hub, claim/join flow; the live Personal page; live anything; the bottom bar's design (it arrives inside the template).

## 8. FIVE GATES (run before the build-script edit)

1. **Is it right?** Yes — every citizen gets the same beautiful world; it harms nobody; it fixes a wrong shape Shawn named himself, under his Billion-Dollar Home charge.
2. **Is it what they truly need?** Yes — his goal beneath the words is one world for everybody ("why would anyone get a different world than anybody else? They wouldn't").
3. **Is it mine to do?** Yes — the brief authorizes staged-only build work; no deploy, no merge, no PR, no mail, no live touch. The template file and build script are work files, not live systems.
4. **Is now the time?** Yes — lineage proven, template verified, proof set (12 sisters + 1 fresh citizen) ready, v23 is the deploy vehicle.
5. **Can I prove it?** Yes — done is defined in the brief §6; Step 4 proves it in Playwright at 1440/390/360, scroll 0 AND scrolled, with screenshots.

**All five yes → build.**

## 9. BUILD PLAN (Step 2, to be executed next)

1. In the base build script: add `TEMPLATE` (composed template path) + read + sha assert (`61002d15…`); update the walk assert `a3510446` → `4e8500c2` (§3); embed via `const PERSONAL_TEMPLATE = __PERSONAL__;` + `json.dumps` (the script's existing embedding shape).
2. Replace `pageHtml(alias, pg)` with `pageHtml(alias, pg, box)` applying the §7b swaps with counted assertions + the motto seed; keep `pageBody`/`composePages`/`hubHtml` untouched.
3. `/pages/` route: load `box_<alias>` from KV (fallback: Supabase `citizen_worlds` row); if no box, derive from `pg` (headline + `##` body sections) so a page without a box still renders with its own words.
4. Rebuild; verify the generated worker file is byte-identical to the hand edit (extract the renderer region from the generated worker and diff against the source region).
5. Hand the fixed worker file to the coordinator with its sha. No deploy — v23 is the vehicle.

---
*Step 1 filed 2026-11-13 ~04:30Z. All measurements first-hand; nothing taken on trust.*

---

## ADDENDUM A — THE FEED SHARPENING (Shawn, 2026-11-13 ~04:34–04:35Z; governing law, supersedes brief §6)

### The sharpening, quoted (filed at SHAWNS-FEED-SHARPENING-20261113.md; also MEMORY.md ~04:34Z)
"Getting the Personal page done is getting the Business done, the Spaces done, and the Memberships done all at once — because the Personal page CONTAINS the membership, contains the personal, contains all the major parts of it all. The feed: it is NOT an activity feed. The third tab is just the PUBLIC FEED — the main smart feed of NayaNET, the one everybody connects on. If you want to connect with people, that is the live feed. It is not your personal feed world, it is your WORLD feed world. So the tabs are: your Smart Notes, your Naya Notes, and the public/world feed. … you literally go to the Hub, the main Hub page, and you take that EXACT system — not one like it — you just take it and put it into the Personal page, and you just change some of the labels. That is pretty much it. … you turn the activity feed into a Naya WORLD feed: it automatically connects you with people of like minds who are online at that time, on the side, and organizes the feed for all the content related to everybody within the network — and those become the main feeds. Why: the current activity feed is just like notifications — that is not really activity, it is not the main feed."

### Self-caught error in §7 (corrected here, before the probe)
§7 recorded "activity `My Activity` → `Our Activity` only for business/space" and Step 2 implemented it (build script line 295). That was WRONG, caught by re-reading the template first-hand while applying the sharpening:
- The template has "Our Activity" ×0. The runtime My→Our relabel touches ONLY the story labels (`var label=mine?'My Story':'Our Story'`; the mount re-applies it to the story `<b>` only). The feed-name button is never relabeled by the template's JS. My renderer INVENTED an "Our Activity" label for business/space that the template never produces — an invention, not a harvest. The Billion-Dollar Home charge forbids exactly this. The swap is deleted and replaced by the sharpening relabel below. (The learning-loop note: a swap-table row carried from the clone record's phrasing without re-verifying it against the template bytes — verify every row against the template, not against the record of the record.)

### Hub harvest, first-hand (2026-11-13 ~04:40Z)
- `curl https://nayanet.app/hub`: HTTP 200, 5,013,119 B, sha256 `a4c08f4ab2b662f8…` (saved `/tmp/spp/hub-live.html`).
- Counts: 'Smart Notes' ×72 · 'Naya Notes' ×210 · 'Public Feed' ×0 · 'World Feed' ×0 · 'My Activity' ×0 · 'Activity' ×37 (mostly embedded spec prose, incl. the bottom-trio ruling "Smart Mail · Instant Messages · Activity") · 'Smart Organizer' ×5 · 'feed' ×498 · 'online' ×15.
- The Hub's feed bytes DIFFER from the Personal template's feed bytes: Hub has 'mwFeedName' ×0, 'data-mw-tab' ×0, 'mw-feedname' ×0, 'os-wall-meta' ×0. The Hub is a different page implementation; its live feed is the "Smart Feed" (Smart Notes) and its world-feed layout lives in its embedded spec prose ("down the center, the feed … off to the right, everybody online and highly matched to that topic — a sidebar top to bottom … their initial, their name, a nutshell … click to instant message, smart mail, audio talk, video meet").
- What is honestly true: the Personal template's feed is the same SHAPE the Hub's feed system has at network level (three feed kinds, three rows, organizer concept) as it exists on live Personal v9 — harvested byte-for-byte from live v9 (Step 1 §5). The label "Public Feed" exists in NEITHER page's bytes; it is Shawn's relabel, applied to the harvested system — exactly his build rule ("take that EXACT system … and just change some of the labels"). The online-on-the-side presence is the Hub's network-level shape; the Personal template carries 'online' ×0 — the Personal page's world feed shows the public feed content, and the online presence lives in the Hub's main feed view. NOT invented into the template, and recorded here as the boundary.
- The Personal page carries the membership and all major parts inside it (pills ×3, memberships doc, Smart Academy course overlay, Join) — finishing it finishes Business, Space, and Memberships in one move. That is what the probe shows board by board.

### Renderer change (Step 2, amended ~04:42Z)
The old `feed-activity` swap is deleted. Three counted swaps, ALL kinds (personal, business, space — the world feed has no My/Our form):
1. `feed-name-public`: `>My Activity — tap for the full dashboard ↓</button>` → `>Public Feed — tap for the full feed ↓</button>` (×1).
2. `feed-tab-public`: `id="mwTabActivity" data-mw-tab="activity" …><b>Activity</b></button>` → `…><b>Public Feed</b></button>` (×1).
3. `feed-default-public`: `<button type="button" data-v="activity">Activity</button>` (Default feed tab setting) → `…>Public Feed</button>` (×1).
Internal wiring kept (ids, `data-mw-tab="activity"`, `data-v="activity"`) — invisible, and the course code reads the tab label from the DOM (`tabLabels: [… sa$('mwTabActivity').textContent]`), so the swap flows through; no JS writes a hardcoded "Activity" label (grep: zero `textContent = 'Activity'` writes). Boundary, named: the notif-bar "Activity" chip, the bottom-bar "Activity" menu item (`{label:"Activity", target:"#dashboard"}`), and the Stats "Activity mix" donut are NOT the feed tab; they stay as the template carries them.
- Rebuilt worker: **5,890,568 B, sha256 `79b6f9625617da4aede380ebee994aa93ea6c69b6c413508271e7eaf49d295a7`** (replaces the d7c2fcde… build). Renderer region byte-identical to hand edit; 0 placeholders. Smoke (harness, after restart): sophia Personal 200 + sophia Business 200 — "Public Feed" ×3, "My Activity" ×0, "Our Activity" ×0, `<b>Activity</b>` ×0, both kinds. Titles correct.
- The probe's feed check is updated to the sharpening: third tab must read "Public Feed" on staged pages; the live control still reads "My Activity" (pre-sharpening live state) — the SAME verdict applies to everything EXCEPT the third-tab label, which differs BY LAW.

---

## ADDENDUM B — THE SEED-ANCHOR DEFECT (found by the probe, fixed ~04:50Z; Step 2/3 correction)

### What the probe found (run 1, pre-fix baseline: 490 pass / 121 fail at kill time — archived as spp-results-run1-prefix.json)
The staged sisters' pages carried **2 pageerrors on every load** — `'unterminated comment'` + `"unexpected token: keyword 'this'"` — while live Personal carried 0. The main script was dead: the feed never painted ("No posts yet" never appeared, although the served HTML contains it ×3), the About sections never filled, and the Supabase call pattern diverged from live (14 console errors vs live's 42 — same 7 tables, fewer attempts, because the dead script never issued its calls).

### Root cause (proven first-hand, not guessed)
The motto seed was inserted with `t.lastIndexOf("<script", li)` before `function loadAbout(){`. The main script block (`<script id="os-script">`, opens 581974) contains a comment `/* F5 … — the feed-board block is a separate <script> … */` — a literal `<script>` string INSIDE a JS comment. `lastIndexOf` found THAT `<script>` (the nearest one before loadAbout) and the seed landed inside the comment, splitting the main block in two:
- Block 7 ended mid-comment with the seed appended (`… separate <script>window.__osAboutSecs=…;`) → 'unterminated comment'.
- Block 8 began with the comment's continuation (` outside this IIFE …`) as bare code → "unexpected token: keyword 'this'".
Proven by extracting all 32 script blocks from the served page and node-checking each: exactly blocks 7 and 8 failed, with the seed visible inside the F5 comment at line 534.

### The fix
Anchor on the main block's own id tag, with a between-blocks assertion (build script, pageHtml, motto branch):
```
const si = t.indexOf('<script id="os-script">');
if (si < 0) throw new Error("personal-render: os-script tag not found");
if (t.indexOf('<script id="os-script">', si + 1) >= 0) throw new Error("personal-render: os-script tag not unique");
if (!t.slice(0, si).replace(/\s+$/, "").endsWith("</script>")) throw new Error("personal-render: os-script tag is not between blocks");
```
The seed is inserted immediately BEFORE `<script id="os-script">`. A failed anchor now throws (request 500s) instead of serving a broken page.
- Rebuilt worker: **5,891,299 B, sha256 `03f7dcc47c03e96ef5cc2fb4628487ede5d86a0c34cdb0437024840c07d89ca9`** (replaces 79b6f962…). Renderer region byte-identical to hand edit; 0 placeholders.
- Proof of the fix, three ways: (1) direct Node render — seed at 582491, BEFORE os-script at 582687, F5 comment's `<script>` intact at 620061; (2) harness render — seed at 582407, os-script at 582603, F5 intact at 619977; (3) all 32 script blocks from the served page node-check clean, seed its own block (178 B) before os-script (242 KB, intact).
- Browser smoke (Firefox, sophia 1440): pageerrors [] · console errors 14 (VM CORS artifact) · "No posts yet" True · "Public Feed" 2 in view · "My Activity" 0 · motto = Sophia's exact words · story = Sophia's about words · story title "My story".
- The lesson (learning loop): never anchor an insertion on a bare tag name inside a file that contains that tag name in strings/comments — anchor on a unique id, and assert the insertion point is between blocks. A counted swap that "succeeds" (no 500) can still split a script block; the proof is executing the page, not serving it.

### Probe-measurement corrections made in the same pass (probe bugs, not page bugs)
- Avatar: live Personal's orb is the template's static `N`, not `S` — the live control now expects `N`; sisters expect their initial.
- Feed rows: the template hardcodes first-name rows ("Shawn's Smart Notes"); the renderer uses the full box.name ("Sophia" — already first name; "SPP Walk One" for the fresh citizen). The probe now passes `feed_name` per page.
- "Add something" is the `#plusbtn` aria-label (plus a list-input placeholder) — innerText never contains it. The probe now reads the aria-label.
- Bottom bar: `position:fixed` elements have `offsetParent === null` in Firefox, so the old visibility check always failed. The probe now uses rect + computed display.
- Live motto reads `''` in this VM (Supabase fill fails + FIX-7 paint timing) — recorded, not asserted; the sisters' seeded motto IS asserted.
- `load_personal` wait raised 5s → 6s (the feed paints after the Supabase calls fail).

---

## ADDENDUM C — THE STORY-TITLE ELEMENT (probe bug, corrected ~05:20Z)

Probe part 2 reported 6 fails: Business/Space story title read "My story", expected "Our Story". The PROBE was wrong, not the page. The probe read `.ib-layer-head b` — the About view's static section heading ("My story", lowercase s), which the template never relabels by design. The relabel target is `#os-story-title`, set by `applyStoryLabels()` (template ~line 487889) from `window.MSHIP_PAGE_KIND` on DOMContentLoaded (+ a setTimeout re-run): personal → "My Story", business/space → "Our Story". The renderer sets `MSHIP_PAGE_KIND` per kind (counted swap, 1 occurrence).
- Re-check (proof/recheck-titles.py, Firefox): staged biz "Our Story" ✓, staged space "Our Story" ✓, staged personal "My Story" ✓ — all 6 Business/Space pages (sophia/thea/astraea × business/space), plus About story+motto still the citizen's words. The 6 wrong-element fails were removed from spp-results.json and replaced by 18 corrected checks (6 title-element + 6 title + 6 story/motto). Total after correction: 915 pass / 0 fail.
- Control note: live https://nayanet.app/business is a DIFFERENT page ("Acme Corp", a standalone demo Business app — no #pname, no .up-act, no #os-story-title), not the Personal-template Business page. It is not a control for the relabel. The valid controls are live Personal v9 (1:1) and the template's own mechanism, proven on staged pages; the clone round is the precedent for "Our Story" on Business/Space clones.
- Lesson (learning loop): a check that reads the wrong element reports the page broken when the page is right. Name the element in the check (the re-check does: "#os-story-title") and verify the mechanism's target first-hand before asserting.

## ADDENDUM D — L5: THE TEST IN HIS HEAD (six questions, in writing, 2026-11-13 ~05:25Z)

Asked about the finished work — the staged sisters' Personal pages (the Personal page, harvested, with the citizen's words):
1. Is this 10-star service? Yes — it is the live Personal page itself, which Shawn ships, with the citizen's own words in every slot and her smart cover in the banner. Nothing was taken away; nothing invented was added.
2. Would a stranger see the value in it and trust in it? Yes — her story, motto, vision, mission, goals and what she does are on the page in plain words, with the live gauge (246 teeth, needle in DOM), the three membership pills, and the public feed where she connects. Every claim on the page is her own words or a live number.
3. If they experienced it, would they get it? Yes — cover, name, tagline, pills, 9 named buttons, plus menu, composer, three named feed tabs. The button-click leg opened every one; none is dead.
4. Is it obvious? Yes — the page is the Personal page. A citizen who has seen one Personal page has seen them all; the only differences are her name, her words, her cover.
5. Is it useful? Helpful? Yes — it is her world: her story, her feed, her memberships, her people (Message, Connections, Invite), her Join. Finishing it finishes Business, Space and Memberships in one move, because the Personal page contains them all.
6. Is it done so clearly that it's evident what it does and what it is — and it does awesome? Yes — 915 checks, 0 fails, at 1440/390/360, scroll 0 and scrolled, against live Personal v9 board by board, plus a fresh citizen walked end-to-end from the login page who got the same world. The gate verdicts are identical live vs staged; the only overall FAIL is (a), which is live v9's own light jewel, identical on both.

---

## ADDENDUM E — PROBE CORRECTIONS, ROUND 2 (2026-11-13 ~05:35Z)

Two probe defects found by the probe's own evidence, both corrected with proof — neither was a page defect:
1. **Box re-read status-0 (7 fails).** probe2/probe3's `api_get` uses Python urllib, and the VM's egress path truncates some live-staging responses (`IncompleteRead`, `RemoteDisconnected`). curl returns 200 for the same URLs at the same time (astraea/wren/iris all 200 by curl while urllib failed). Re-run via curl: all 7 return 200 and read back word-for-word. Lesson: for live-staging reads, curl is the reliable path from this VM; urllib's failures are transport, not data.
2. **Plus-menu "Make a post" click (1 fail).** The probe used `get_by_text("Make a post", exact=True)`. The menu item's text is "✎ Make a post" (pencil icon prefix) — no exact match exists, correctly. Clicking the visible `.ph-plusitem` containing "Make a post" opens the creator (diag-plus.py: creator True, URL #home, screenshot spp-sophia-creator-390.png). Lesson: exact-text locators fail on icon-prefixed labels; match on the visible item.

---

## ADDENDUM F — FINAL TOTALS + SELF-CHECK ×3 (2026-11-13 ~05:40Z)

- The "915 pass / 0 fail" line in Addendum C was true at 05:20Z (after the story-title correction). Probe3 + the destinations pass added 254 more. **Final: 1,169 pass / 0 fail** (spp-results.json, notes[0] refreshed). Breakdown: live control 57 · sisters' Personal 528 · Business/Space samples 300 · button clicks + plus menu + creator 14 · fresh citizen sppw1 185 · Box re-reads 24 · gate parity 4 · anatomy 6 · L1–L7 7 · destinations 13 · corrected re-checks 31.
- **Test artifact, named:** the fresh citizen `sppw1` (alias "sppw1", June the grower/baker) wrote a REAL row to the live Supabase registry during the claim step — established practice (S2/Q10 used s2walk23/s2walk24) — and her Box/pages live in the HARNESS KV only, not live staging KV. Her data is a test artifact, not a sister. Her answers are fixed in spp-probe3.py.
- **Self-check round 1 (code, ~05:38Z):** worker sha 03f7dcc4… re-verified; renderer byte-identical .py vs .js (10,042 B); 0 placeholders; 25 swapCounted + 3 swapSplit; spot-render thea biz + aurelia space pass. NEW: "Our Activity" ×2 in the worker are BOTH inside my own comment (the Addendum A explanation), not walk-embedded — my earlier guess was wrong; corrected here.
- **Self-check round 2 (evidence, ~05:39Z):** 70 screenshots, all 69 expected present (1 extra: the live /business diag); results file parses, no check name in both pass and fail; gate files + 13 Box snapshots present. NEW: (a) the destinations leg was missing — the brief requires "every button clicked, every destination recorded" and the clicks leg recorded only "opens something" — fixed with diag-destinations.py (13 checks, spp-destinations.json); (b) results notes[0] was stale at 1156 — refreshed to 1169.
- **Self-check round 3 (fresh eyes, ~05:40Z):** brief Step 4 audit, requirement by requirement — 12 sisters board-by-board ✓ · fresh citizen ✓ · biz/space 3 sisters, one per voice (sophia A, thea B, astraea C) ✓ · every button + destinations ✓ · Box word-for-word ✓ · screenshots ✓ · gate + anatomy + L1–L7 ✓. NEW: the brief's "buttons 10" reconciles as 9 up-act + the plus button (the record's §7 lists 9 up-act + Add something + plus menu); the record had no Step 4/5 section — the final RECORD-SPP-20261113.md carries it; the (a) gate FAIL is inherited from live v9 and is named, not fixed (fixing it would change live v9 itself).
