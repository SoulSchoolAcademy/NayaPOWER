# Smart Bar — verification evidence (2026-10-28, BUILD lane, Resolve seat)

Component: `smart-bar.js` (19,879 B, sha256 `79024b3ab8ebd99b…`)
Proof page: `proof.html` (1,760,703 B, sha256 `ac136b5a02be6ca5…`) =
`face-base.html` (1,735,560 B, sha256 `45e8c09b646accf0…`, fetched
`curl -sL https://pi-v4-preview.nayapower.workers.dev/` at 18:36Z) + one
injected chunk (25,143 B) before `</body>`. No other byte altered.

## (a) Syntax

```
$ node --check smart-bar.js && echo NODE_CHECK_OK     (node v24.22.1)
NODE_CHECK_OK
```

## (b) Component exactly once + both bar containers, in proof.html

The bars are DOM elements the component creates at runtime, so the
container evidence is (1) the creation code present exactly once in the
served bytes, and (2) a runtime mount test (§d) that finds both elements
in the mounted tree.

```
$ grep -c 'bar.id = "smartbar-top"' proof.html            → 1
$ grep -c 'bottomBar.id = "smartbar-bottom"' proof.html   → 1
$ grep -c 'window.SMARTBAR_TOP =' <injected chunk>        → 1  (the assignment)
$ grep -c 'SMART BAR — two-bar navigation component' proof.html → 1 (header marker)
$ grep -c '\n})();' <injected chunk>                      → 1  (one IIFE = one component)
```
(`window.SMARTBAR_BOTTOM =` appears twice in the chunk: the config
assignment + the usage example inside the component's own header comment,
smart-bar.js line 14. The component body itself is present exactly once.)

Byte-integrity of the injection (python, run in this dir):

```
chunk bytes: 25143
strip == face-base byte-for-byte: True     # proof.html minus the injected
                                           # chunk IS face-base.html, exactly
chunk contains component exactly once: 1 | IIFE closings: 1
```

## (c) Config counts, traced to the page's own content

**Top tabs: 13 configured = 13 sections the page itself exposes.**
Source: the face's own tab strip. `<nav class="tabrow" id="tabrow">` at
face-base.html line 72 is filled by `renderTabs()` (line 643) as
`["all","All"]` + GROUP_ORDER with GROUP_LABEL (lines 114/113) +
missions/rulings/journal/governing/overallsec/notplacedsec. The config
mirrors that array 1:1, labels verbatim:

| # | label (page's own words) | tabKey | wired to |
|---|---|---|---|
| 1 | All | `all` | `showTab("all")` |
| 2 | Personal & apps | `personal` | `showTab` + `[data-group="personal"]` |
| 3 | Hub & dashboard | `hub` | `showTab` + `[data-group="hub"]` |
| 4 | People, mail & match | `people` | `showTab` + `[data-group="people"]` |
| 5 | Factory, voice & membership | `factory` | `showTab` + `[data-group="factory"]` |
| 6 | Smart Notes feed | `feed` | `showTab` + `[data-group="feed"]` |
| 7 | To go in (files) | `togoin` | `showTab` + `[data-group="togoin"]` |
| 8 | The 25 missions | `missions` | `showTab` + `#missions` |
| 9 | Doubled-page rulings | `rulings` | `showTab` + `#rulings` |
| 10 | Day Journal | `journal` | `showTab` + `#journal` |
| 11 | Governing | `governing` | `showTab` + `#governing` |
| 12 | Overall list | `overallsec` | `showTab` + `#overallsec` |
| 13 | Not placed | `notplacedsec` | `showTab` + `#notplacedsec` |

`showTab(tab)` was read in the served bytes (line 654): it takes exactly
one string key, toggles `.groupsec` sections by `data-group` (sections
rendered at line 436 as `<section class="groupsec" data-group="…">`) and
the special sections by id, then scrolls the target into view itself.
So the primary wiring is `window.showTab(tabKey)` — the page's real
argument form, not a guess; `target` is only the fallback for hosts
without a tab function.

**Bottom tabs: 44 configured = the 44 entries of the page's own PAGES
registry** (`const PAGES = […]`, face-base.html line 102 — the whole
array sits on that one line; every entry below was parsed out of it
programmatically, none hand-typed). Each entry's `link.kind` +
`link.href` + `link.label` are the page's own words:

- **21 with a real url** — `link.kind = "live_route"` with an absolute
  https href, carried verbatim: personal-app, business-app, space-app,
  about, live-wall, today-personal, smart-growth-invites, smart-link,
  naya-notes, smart-lists, reports, certificate-identity → all
  `https://nayanet.live/personal` (the page's own routing: those apps
  live inside Personal today); home → `https://nayanet.live/`;
  intel-today → `/rooms/today`; library → `/rooms/library`;
  projects → `/projects`; connections → `/rooms/connections`;
  smart-mail → `/rooms/mail`; growth → `/rooms/growth`;
  booking → `/book`; welcome → `/welcome`. (10 distinct destinations.)
- **23 with url:null**, in two honest classes:
  - **8 × `pi_area_view`** — the page gives only an in-page fragment
    (`#area-…`) and labels it, in its own words, *"Not separately served
    yet"*: settings, dashboard, project-intelligence, smart-match,
    smart-factory, ask-naya, membership-affiliate, privacy-locks. A
    fragment into this same face is not the app's destination, so these
    are null and the no-destination behavior is what a tap exercises.
  - **15 × `none`** — `link.href` is null in the page itself:
    pricing ("No live route — preview files only"), smart-notes
    ("No separate live route verified"), walk-slide-02…10,
    walk-slide-end, walk-integrated, thankyou-connect,
    smart-match-first-run ("No live route — file in the supplied zip only").

Full per-entry trace: `config-trace.json` in this dir.

## (d) Behavior evidence — runtime test, 21/21 PASS

`node test-dom.js` executes the real `smart-bar.js` against a minimal
DOM shim (stubs, not a browser — see owed list) with a 2-tab top config
and a 3-tab bottom config including one url:null tab. Output:

```
PASS | both bars mounted
PASS | CSS injected (#smartbar-top{top:0} / #smartbar-bottom{bottom:0})
PASS | edge fades in CSS (mask-image linear-gradient)
PASS | reduced-motion CSS present
PASS | top pills = tabs x2 sets (duplicated set = seamless wrap)
PASS | TOP BAR HAS NO edit controls (no ⋯, no Add in top track HTML)
PASS | bottom pills = tabs x2 sets · bottom ⋯ per tab x2 · Add x2
PASS | body padding reserved | 52px/52px
PASS | top tap calls window.showTab(tabKey) | journal
PASS | null-url tap shows toast | "No destination yet — never a dead link"
PASS | null-url tap does NOT navigate
PASS | real-url tap navigates | https://nayanet.live/alpha
PASS | menu opens · menu items exact + in order (Edit / Set Purple
       Heart 💜 / Set Gold Star ⭐ / Remove)
PASS | persistence key naya.smarttabs.v1 written · heart persisted
PASS | hearted tab sorts FIRST after re-render · 💜 flag shown on pill
TOTAL: 21/21 PASS
```

## (e) Rule → code map (all line numbers are smart-bar.js)

| Settled rule | Where it lives |
|---|---|
| Top bar = very top, bottom bar = very bottom, both fixed | CSS lines 58–65 (`.smartbar{position:fixed}`, `#smartbar-top{top:0}`, `#smartbar-bottom{bottom:0}`) |
| Top drifts RIGHT, bottom drifts LEFT | `renderTop` line 234 `makeDrift(track, -1)`; `renderBottom` `makeDrift(track, +1)`; sign applied line 160 |
| Loads AT REST, drift never the opening state | `REST_MS = 5000` line 47; gate `now - born > REST_MS` line 159 |
| Drift pauses on touch/hover/focus/wheel, resumes ~6s | `poke()` line 165 (`RESUME_MS = 6000` line 48); listeners line 167 (pointerenter/pointerdown/focusin/touchstart/wheel); drag + wheel also move the offset by hand, lines 172–184 |
| Reduced motion: drift fully disabled | `reduceMotion` lines 54–55 checked in the frame gate line 158; CSS line 102 kills transitions |
| Speed "slowly" | `TRAVERSE_SECONDS = 90` line 49 — CANDIDATE inside the 60–120s band, labeled candidate in the file header; drift is one-way wrap (two sets, `buildTrack` lines 192–200) |
| Top bar NOT editable | `renderTop` lines 206–235 creates pills only — no ⋯, no Add, no remove/reorder anywhere in the top path (proven negatively by the runtime test) |
| Top tap pulls into the section | lines 219–232: `window.showTab(tab.tabKey)` (line 228) when tabKey + host showTab exist, else `scrollIntoView({behavior:"smooth"})` on `tab.target` |
| Bottom: real url navigates, no url says so | `renderBottom` click handler: `if (tab.url) location.href = tab.url; else toast("No destination yet — never a dead link")` (toast lines 119–128) |
| Bottom ⋯ menu, exactly Edit / Set Purple Heart 💜 / Set Gold Star ⭐ / Remove | `openMenu` — menu HTML carries exactly those four items in that order (runtime-verified) |
| ＋ Add (name + any URL) | `data-sb-add` pill in `renderBottom`; `openEditor(null)` — inline editor with Name + URL fields |
| Edit via the same editor | `openEditor(tab)`, prefilled; Save writes label + url, persists, re-renders |
| Hearts first, then stars, stable | `sortedTabs` lines 263–273 (rank heart 0 / star 1 / rest 2, original index tiebreak) |
| Persistence `naya.smarttabs.v1`, shared across pages | `STORAGE_KEY` line 44; `loadBottom` lines 243–258 (saved state wins over seed), `saveBottom` lines 260–262 (saved on every mutation) |
| Dark pills, bold labels, white at rest, own-color ignition, lift + glow | `.sb-pill` CSS (dark `#0b0b10`, `font-weight:700`, white glow at rest; `:hover/:focus-visible` sets color/border/glow to `var(--tc)`, `translateY(-3px)`, text-shadow) |
| Spectrum by position: purple blue green gold orange red magenta, cycling | `SPECTRUM` line 45 — the face's own palette (face-base.html line 110, identical values); `spectrum(i)` line 116 by rendered position |
| Edge fades, hidden scrollbars, smooth touch scrolling | mask-image fades 28px (CSS lines 62–63); `scrollbar-width:none` + track overflow hidden; drag/wheel handlers lines 172–184 |
| Chrome only — never restyles content | `reserveSpace` — the only page mutation besides the bars themselves: body padding-top/bottom += 52px bar height (runtime-verified 52px/52px) |
| Never mounts twice | guard line 52 (`if (document.getElementById("smartbar-top")) return;`) |

## (f) OWED — named plainly, not hidden

1. **No browser run.** This environment's headless Chromium renders
   nothing (standing environment fact), so there is no screenshot and
   no in-browser click-through. Behavior evidence is the node shim test
   (21/21) + code map above. A human or browser-capable seat opening
   `proof.html` is the remaining visual proof.
2. **Drift timing not machine-verified.** The shim runs no animation
   frames; rest-first (5s), pause/resume (6s), wrap, and the ~90s
   traverse are implemented in one 25-line mechanism (`makeDrift`,
   lines 147–190) and code-reviewed, not frame-measured.
3. **Drift speed is a CANDIDATE** (90s traverse, one-way wrap) — the
   standard settles only "slowly" + directions; numeric speed and
   wrap-vs-ping-pong per bar remain OWED in the spec (§5 item 3).
4. **Bottom-bar precedence OWED** (spec §5 item 2): once a citizen has
   saved tabs, the saved state wins over the page's seed config on
   later loads (f-01's harvested behavior). Whether favorites vs chosen
   vs default-all should merge differently is not settled; the
   component follows the harvested rule and invents nothing further.
5. **Top-bar persistence OWED** (spec §5 item 8): the top bar is not
   persisted at all — it renders from config every load. No source
   claims otherwise.
6. **Phone layout unproven** (spec §5 item 6): bars are fixed and
   full-width at any viewport, but no phone-width check was possible
   here; how much vertical room the two bars may take on a phone is
   still an open spec question.
7. **Hide rules not implemented — deliberately.** The standard's hide
   rules govern the OTHER bars in the stack (smart bar never closable,
   notifications always stay); the component ships no close control for
   itself, which is the rule. Hiding the page's pre-existing bars is
   the host page's business, not this component's.
8. **Menu heart/star items toggle** (Set again = unset). The settled
   menu labels are carried exactly; toggle-on-second-tap is f-01's
   working behavior, not separately settled words.
9. **12 of the 21 "real" bottom urls point at `/personal`** because the
   face's own registry routes those apps inside Personal today. The
   component carries the page's truth; when those apps get their own
   routes, only the config changes.
