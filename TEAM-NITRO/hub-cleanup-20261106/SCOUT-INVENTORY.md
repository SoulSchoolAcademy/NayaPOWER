# SCOUT INVENTORY — Hub Cleanup (remove 2 elements)

Scout: Role 1 of 4, Hub Cleanup team. Read-only inventory of the LIVE file.
Source of truth: `live-index.html` (fetched from https://nayanet.app/).

## 0. Fetched file — verification

- **Fetched:** 2026-11-06 04:56:52Z via `curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"` → `~/workspace/team-nitro/hub-cleanup/live-index.html`
- **Size:** 5,503,605 bytes — MATCHES expected
- **SHA-256:** `144a07c9be2f21301abea168ec664ff8967976295ab2d7337dde138b9689af80` — MATCHES expected (v5.1 freeze, coordinator-verified 04:56Z)
- **Lines:** 9,045 (7 lines >10,000 chars — embedded base64/data blobs, e.g. line 3776 is the 1,781,314-char baked NOTES JSON blob)
- **Verdict:** the fetched file IS the expected v5.1 freeze. No flag. All line numbers below are against this file.

## 1. Element (a) — the little "Search" pill, bottom-right

### What it is
A fixed-position pill button, bottom-right above the bottom bars, labelled **"Search"**.
It is NOT static HTML — it is created by JS at the very end of the file, in the
universal-search IIFE (lines 8988–9042). It is the ONLY element in the file with
the text `Search` as a visible button label in the bottom area.

### Exact location / code
- **Script block:** lines 8988–9042 (`<script>` opens 8988, IIFE `(function () {` 8989, closes 9041–9042).
- **Comment:** line 9021 — `// Accessible mobile entry: do not make Ctrl-K the only way in.`
- **Button creation — lines 9022–9028:**
  ```js
  var button = document.createElement('button');
  button.type = 'button';
  button.className = 'primo theme-purple elev-2 naya-command-trigger';
  button.textContent = 'Search';
  button.setAttribute('aria-label', 'Search your world');
  button.setAttribute('aria-keyshortcuts', 'Control+K Meta+K');
  button.addEventListener('click', function () { palette.open(); });
  ```
- **Its dedicated inline style — lines 9029–9038** (a `<style>` element created in JS and appended to `<head>`, line 9038):
  ```js
  var style = document.createElement('style');
  style.textContent = '.naya-command-trigger{position:fixed;right:16px;'
    + 'bottom:calc(105px + env(safe-area-inset-bottom,0px));z-index:900;'
    + 'border-radius:999px;min-height:43px;padding:0 20px;'
    + 'box-shadow:0 10px 26px rgba(0,0,0,.35);'
    + 'border:1px solid rgba(200,180,255,.5)}'
    + '@media(max-width:600px){.naya-command-trigger{right:12px;'
    + 'bottom:calc(110px + env(safe-area-inset-bottom,0px));'
    + 'min-height:44px;padding:0 16px}}';
  document.head.appendChild(style);
  ```
- **Append — line 9039:** `document.body.appendChild(button);`
- **Selectors / classes:** `.naya-command-trigger` (unique to this button); `primo theme-purple elev-2` (shared design-system classes — see CSS note below). No `id` on the button. `aria-label="Search your world"`, `aria-keyshortcuts="Control+K Meta+K"`.

### Position on screen (from its own style)
- Desktop: `position:fixed; right:16px; bottom:calc(105px + safe-area)` — i.e. just above the eco-bottombar + notif bar stack. `z-index:900`.
- Mobile (≤600px): `right:12px; bottom:calc(110px + safe-area)`; min-height 44px.
- Pill shape: `border-radius:999px`, padding `0 20px` (16px mobile).

### CSS — shared or dedicated?
- **The `.naya-command-trigger` rule exists ONLY inside this JS-created `<style>` (lines 9030–9037).** The selector occurs exactly 3 times in the whole file: lines 9024, 9030, 9035 — all inside this one block. Deleting the block deletes the rule entirely; nothing else uses it.
- **`primo`, `theme-purple`, `elev-2` are shared design-system classes** (used by other elements elsewhere in the file). They are only *applied* to this button here — removing the button does not touch the class definitions, and no other element loses styling. No CSS cleanup needed beyond the block itself.
- No other stylesheet references `.naya-command-trigger`.

### JS that references it
- **Its only handler:** line 9028 — `click` → `palette.open()`. The handler closes over `palette` (line 9019, `NayaSearch.mountPalette(document.body, { store: searchStore })`).
- **No other code references the button.** `window.NayaSearchPalette` (line 9040) exposes `open()` — see dependency note below.
- **No data binding.** The button displays static text "Search"; it reads/writes nothing.

### What it does / what depends on it
- Opens the universal-search command palette (`NayaSearch.mountPalette`, external engine `js/naya-search.js`, loaded line 8987).
- The palette itself is mounted at line 9019 and the **Ctrl-K / Cmd-K hotkey is installed at line 9020** (`NayaSearch.installHotkey(document, ...)`). Both are INDEPENDENT of the button — they keep working if only the button is removed.
- `window.NayaSearchPalette = { open: ... }` (line 9040) also stays available if only the button is removed. (Whether anything else in the file calls `NayaSearchPalette.open()` — see Risks; grep found no other call site in this file, but the Builder should confirm before deciding whether line 9040 stays.)

### Removal if deleted
- **No empty gap:** the button is `position:fixed` — it occupies no layout space. Removing it leaves no hole, no reflow, no margin collapse.
- **No dead handler risk:** its only listener (line 9028) is attached to the button itself and dies with it. Nothing else queries the button (no `querySelector('.naya-command-trigger')` anywhere).
- **No other element depends on it.** The palette, the hotkey, and the main search bar are all separate.

### Minimal removal boundary (candidate — Builder decides)
- **Lines 9021–9039 inclusive:** the comment (9021), button creation + handler (9022–9028), the dedicated `<style>` creation + append (9029–9038), and `document.body.appendChild(button)` (9039).
- **KEEP:** lines 9019–9020 (palette mount + hotkey) and line 9040 (`window.NayaSearchPalette`), unless the Builder decides the whole universal-search IIFE goes — that is OUT of the stated scope (only the pill is to be removed; the palette/hotkey are the search engine's other entries and were not named by Shawn).
- **KEEP:** line 8987 (`<script src="js/naya-search.js">`) — the engine the palette and hotkey use.

### Risks / ambiguities for the Builder
1. **Accessibility note:** the comment at line 9021 says the button exists so Ctrl-K is "not the only way in" (mobile entry). Removing it leaves Ctrl-K/Cmd-K as the only palette entry in this file. The main "Search your intelligence…" bar (STAYS) is a separate, visible search entry, so search as a whole remains reachable — but the *palette* specifically loses its visible button. Flagging only; Shawn's instruction is to remove the pill.
2. **No `id`, no other selector targets it** — removal is purely the 19-line block above; there is no second copy (grep for `command-trigger` = 3 hits, all in this block).
3. **Do NOT delete the whole IIFE (8989–9041):** that would also kill the palette mount, the hotkey, and `window.NayaSearchPalette`. Only lines 9021–9039 are the pill.

## 2. Element (b) — the "Intelligence live" banner at the top

### What it is
A full-width status line rendered at the top of the Smart Feed room, between the
INTELLIGENT HUB header and the hero. In the live view it reads
**"Intelligence live — 361 Smart Notes · updated Nov 5, 2026"**.
It is NOT static HTML — it is a `<p>` created by JS and its text is rewritten
by up to three writers (see below). There is no element with class
`feed-banner` / `live-banner` in the file; the banner is `#feed-provenance-line`.

### Exact location / code
- **Element creation — lines 5298–5308** (inside the feed-room branch of the room renderer, lines 5286–5309):
  ```js
  const provenance = el('p', 'feed-provenance');
  provenance.id = 'feed-provenance-line';
  provenance.setAttribute('role', 'status');
  provenance.textContent = 'Intelligence as of '
    + (trustworthyDate
      ? capturedDate.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
      : 'unknown')
    + ' — ' + (ageDays === null ? 'capture time unavailable'
      : ageDays + ' day' + (ageDays === 1 ? '' : 's') + ' old')
    + ' · repository snapshot, not live';
  outlet.appendChild(provenance);
  ```
  Line 5309 passes it into the feed renderer: `outlet.appendChild(mainShow(room, C, feedStream || 'collective', searchWrap, provenance));`
- **Selectors / ids / classes:** `id="feed-provenance-line"`, class `feed-provenance`, `role="status"`. Parent: `.room-outlet` (`outlet`), first child, immediately before the `.main-show` (hero + search + tabs + boards).
- **Only rendered in the feed room** (`room.id === 'feed'`, line 5286). Other rooms never create it.

### CSS — dedicated, not shared
- **`<style id="naya-provenance-style">`, lines 2681–2697** — the ONLY rules for `.feed-provenance`:
  ```css
  .feed-provenance {
    max-width: 960px;
    margin: 12px auto 14px;
    padding: 11px 16px;
    border: 1px solid rgba(166, 137, 255, 0.36);
    border-radius: 12px;
    background: linear-gradient(125deg, rgba(126, 72, 210, 0.16), rgba(48, 48, 86, 0.16));
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.13);
    color: #ded4f0;
    font-size: 12px;
    letter-spacing: 0.01em;
    line-height: 1.5;
  }
  ```
- The selector `.feed-provenance` occurs exactly 3 times in the whole file: line 2682 (this rule), line 5298 (creation). (The other `provenance` hits are the `id` lookups and unrelated `provenance: "repository-snapshot"` metadata.) **Nothing that STAYS uses this class or this `<style>` block** — it is a safe candidate for deletion with the element. (Candidate only — Builder decides.)

### What data it displays — LIVE data, not static text
- **The "361 Smart Notes" count is live:** `window.NayaFeedIntelligence.notes.length`.
  - Baked snapshot: `window.NayaFeedIntelligence = { notes: NOTES, ref: "10190..." }` (line 3777). The baked NOTES blob (line 3776) contains **355 notes** (355 `"created":` / `"id":` occurrences).
  - Live override (lines 3779–3807): fetches `/feed-live.json` and re-points the global to `{ notes: d.notes, ref: 'live-registry' }` (line 3796). The live registry is where the 361st count comes from — the on-screen "361" is the live-registry length, not a hardcoded number. No literal "361 Smart Notes" string exists anywhere in the file.
- **The "updated Nov 5, 2026" date is live:** the newest note's `created` field, formatted with `toLocaleDateString(undefined, {year:'numeric',month:'short',day:'numeric'})` (line 3849). No literal "updated Nov" string exists in the file.
- **The initial text is snapshot-derived:** `window.NayaContent.meta.as_of` (lines 5289–5290; baked value `"2026-10-02T16:43:37Z"`, line 3481) — "Intelligence as of Oct 2, 2026 — … · repository snapshot, not live". This initial text is visible only until the first live rewrite.

### JS that references it — THREE writers, all guarded
1. **`fixProvenance(count, newest)` — lines 3843–3853** (script block lines 3809–3872, "Live feed override v2 face rules", Resolve 2026-11-05). Rewrites the line to:
   `'Intelligence live — ' + count + ' Smart Notes · updated ' + when` (line 3850) — **this is the exact on-screen text Shawn quoted.** Also writes `window.NayaContent.meta.as_of = newest` (line 3845). Guarded: `if(!line) return;` (line 3847) — safe if the element is gone.
   - Called from: `watch()` interval (line 3863, every 400 ms, up to 150 tries), and one-shot timeouts at lines 3870 (1200 ms) and 3871 (3000 ms).
   - Its inputs come from `currentNotes()` (lines 3855, 3860): `liveCount = NayaFeedIntelligence.notes.length`, `liveNewest = notes[0].created`.
2. **`updateFeedProvenance(liveOk, backend, notes)` — lines 5928–5939** (inside `mainShow`, lines 5739–5967). Rewrites the line to:
   `'Live intelligence · ' + notes.length + ' notes · newest ' + age + ' · backend: ' + backend + ' · checked ' + checked` (lines 5937–5938). Guarded: `if (!provenanceEl || !liveOk) return;` (line 5929) — safe if the element is gone (it receives the element as the `provenanceEl` parameter, line 5739).
   - Called once at line 5962, only when the governed-runtime live fetch succeeded (`if (liveOk) { fillFeedBoards(...); updateFeedProvenance(true, backend, notes); }`).
3. **Initial text** at creation (lines 5301–5307) — see above.
- **No other readers:** `getElementById('feed-provenance-line')` occurs only at lines 3846 and 3864. `provenanceEl` occurs only at lines 5739 (parameter), 5929, 5937. Nothing else reads the element, its text, or its layout.

### What happens if it is removed
- **No empty gap:** the element carries its own spacing (`margin: 12px auto 14px` in its own rule). Removing the element removes its margins with it; the hero (`.main-show`, next sibling) simply moves up. No spacer, placeholder, or sibling depends on its height.
- **No dead-handler risk:** the element has no event listeners. All three writers are guarded against a missing element (`if(!line) return;` / `if (!provenanceEl || !liveOk) return;`) — they become no-ops. `watch()` also guards its `shown` check (`line && liveCount && ...`, line 3865) and terminates on `tries>=150` regardless.
- **No other element depends on it.** The feed boards render independently (`fillFeedBoards`, lines 5874/5962–5963); the hero, search, tabs, and boards do not read the banner.
- **One side effect to note:** `fixProvenance` also writes `window.NayaContent.meta.as_of = newest` (line 3845). If the whole v2 script block is removed, that metadata update stops — but nothing in the file reads `meta.as_of` except the banner's own initial-text code (line 5290), which is also being removed. No other consumer found (grep `meta.as_of` = lines 3481, 3845, 5290 only).

### Minimal removal boundary (candidate — Builder decides)
- **Element + creation: lines 5287–5308** — the comment (5287–5288) and the captured-date computation (5289–5297) exist ONLY to build the banner's initial text; the element creation + append (5298–5308). Line 5309 (`mainShow(..., provenance)`) must be updated: either drop the 5th argument or pass `null` — `mainShow`'s `provenanceEl` param is then unused except for the guarded `updateFeedProvenance`, which already returns early on a falsy value. **Builder's call:** cleanest is to remove the 5th argument at 5309 AND the `provenanceEl` parameter + `updateFeedProvenance` function (5924–5939) + its call (5962) — or leave them as guarded no-ops. Flagging, not deciding.
- **CSS: lines 2681–2697** (`<style id="naya-provenance-style">`) — serves only this element; candidate for deletion with it.
- **Writer #1 (`fixProvenance` + `currentNotes` + `watch` + its timers): lines 3843–3871** — after removal these functions have no element to write to; they are harmless no-ops (guarded) but become dead code. The surrounding v2 script (lines 3809–3872) ALSO contains `face()` / `armAlive()` (lines 3820–3842, 3835–3842), which style and light the BOARDS (`.intel-board` rules) — **those MUST stay**. So the Builder must NOT delete the whole 3809–3872 script; only the provenance-writing functions (3843–3871) are candidates, and only if it chooses to remove dead code rather than leave guarded no-ops.
- **Writer #2 (`updateFeedProvenance`, lines 5924–5939 + call at 5962):** candidate for removal with the element; guarded no-op if left.
- **KEEP:** the live-feed override v1 (lines 3779–3807, `/feed-live.json` fetch → `NayaFeedIntelligence`) — it feeds the BOARDS, not just the banner. **KEEP:** the baked NOTES blob (lines 3774–3777) — it is the feed's snapshot data. **KEEP:** `NayaContent.meta` (lines 3479–3484) — baked content metadata.

### Risks / ambiguities for the Builder
1. **Three writers, one element:** the banner's text is rewritten by two later writers after its initial render. Removing only the creation (5298–5308) is enough to remove it visually (both writers guard on the missing element), but leaves two dead writer functions. Removing the writers too is cleaner but touches more lines — Builder's judgment.
2. **Do NOT delete the v2 script block wholesale (3809–3872):** it carries the board face/lighting rules (`face()`, `armAlive()`, lines 3820–3842) that the STAYS boards depend on. Only lines 3843–3871 are provenance-only.
3. **"It is okay as a notification in Smart Ledger + Activity":** this inventory covers ONLY the top-of-feed banner. No Smart Ledger / Activity notification element was in scope; nothing in this file was found that duplicates this banner into those rooms (the banner is created only in the `feed` room branch). If a Ledger/Activity version is wanted later, it is a new build, not part of this removal.
4. **The count "361" is live-registry data, not baked:** after removal, nothing displays the count at the top. The boards themselves still render from the same live data — no data loss, only the headline display goes.

## 3. STAYS — confirmed present (each with location)

All of the following were verified in the fetched live file and are NOT touched by either removal above.

| Element | Present? | Location (live-index.html) |
|---|---|---|
| Main search bar "Search your intelligence…" | ✅ YES | Created lines 4997–5004 (`<section class="searchWrap">`, `<input type="search" id="chassisSearch" placeholder="Search your intelligence…">`, handler lines 5005–5012, `R.search` → client-side note search). CSS lines 813–833 (`.searchWrap`, `.searchRow`, `.search-ico`). Appended in feed at line 5795 (`if (searchWrap) wrap.appendChild(searchWrap)`, directly above the lens tabs) and in other rooms at line 5321. Independent of both removed elements — its handler reads `R.search`, never the pill or the banner. |
| Hero | ✅ YES | `mainShow` lines 5742–5788: `<section class="hero">` (line 5770), greeting + date/time (5773–5778), live clock interval (5781–5787), appended line 5788. Motto: "NayaNET — create, learn and grow together" (line 5776). |
| INTELLIGENT HUB header | ✅ YES | Line 4929: `el('div', 'top-title', '<b>INTELLIGENT HUB</b>')`, appended to the top bar line 4939. |
| COLLECTIVE / PERSONAL / ACTIVITY tabs | ✅ YES | `mainShow` lines 5797–5822: `<nav class="lens-tabs">` (5798); tabs defined lines 5801–5803 (COLLECTIVE `/hub/feed`, PERSONAL `/hub/feed-personal`, ACTIVITY `/hub/feed-activity`); buttons built lines 5805–5821, appended line 5822. |
| Filter pills (topic / smart tabs) | ✅ YES | `snPill()` lines 5231–5249 builds `<button class="smart-tab …">` pills (role=tab, label + heart/star markers); keyboard roving at lines 5250–5260; CSS `.smart-tab` lines 1025–1084 (31 hits). Separate from the lens tabs above and from both removed elements. |
| Boards (Smart Note boards) | ✅ YES | Feed container `<div class="show-feed">` line 5825; boards filled by `fillFeedBoards(feed, …)` — defined line 5874, called lines 5962 (live) / 5963 (snapshot). Board styling `.intel-board` lines 1172–1204 + face/lighting rules lines 3820–3842 (in the v2 script — MUST stay, see §2). Data: baked NOTES line 3776–3777 (355 notes) + live `/feed-live.json` override lines 3779–3807. |
| Bottom nav — eco-bottombar (12 icon links) | ✅ YES | Created lines 5342–5400: `<nav class="eco-bottombar">` (line 5342), `BB_LINKS` 12 destinations lines 5345–5358 (HOME, NAYA POWER, ABOUT US, YOUR HIRED, WHITE PAPER, NAYA ACADEMY, "5" DAY CHALLENGE, MAXIS AI SCORE, AI MASTERCLASS, INTRO REPORT, LIFE WITH NAYA, MEMBER LOGIN), buttons `.eco-bb-btn` lines 5360–5383, appended line 5400. CSS lines ~280–340 (`.eco-bottombar`, `.eco-bb-btn`). Positioned above the notif bar (`body.has-notif .eco-bottombar { bottom: calc(94px …) }`, line 400). None of the 12 is a Search link. |
| Bottom nav — MAIL / ACTIVITY / SPACES | ✅ YES | `NayaNotif` init lines 5420–5448: `<nav id="naya-notif-bar" class="notif-bar">` (line 5429), segments `SEGS = [['mail','MAIL',…], ['activity','ACTIVITY',…], ['spaces','SPACES',…]]` (line 5431), buttons `.notif-seg` with icon + count bubble lines 5434–5442, appended to `document.body` line 5443. CSS `.notif-bar` / `.notif-seg` / `.notif-tile` lines 342–400. Only 3 segments — no Search segment exists here. |

## 4. Cross-checks / gaps

- **No second "Search" pill exists.** Grep for `command-trigger` = 3 hits, all inside lines 9024–9035. Grep for visible `Search` button labels = the pill (9025) + the main search input placeholder (5002) + the Activity-room search input (5989, `placeholder="Search your activity..."`, a different room's own field — STAYS, untouched).
- **No second provenance banner exists.** `feed-provenance` = 3 hits (CSS 2682, creation 5298–5299); `feed-provenance-line` id lookups = 2 hits (3846, 3864). One element, one room (feed).
- **Shared-class check for (a):** `primo theme-purple elev-2` are design-system classes used elsewhere (e.g. lens tabs line 5806, Life-with-Naya button line 4930) — but the class *definitions* are not touched by removing the pill; only this button's *application* of them goes away.
- **Shared-CSS check for (b):** `.feed-provenance` / `#naya-provenance-style` are used by nothing else. Clean.
- **Not verified by rendering:** this is a source inventory of the fetched file (read-only brief). No browser render was run by the Scout; the Builder/Verifier own visual confirmation that the pill and banner are gone and the STAYS elements still render.
- **File untouched:** `live-index.html` was written once by the fetch (04:56:52Z) and not edited afterwards. Its sha256 still matches §0.

— End of inventory —
