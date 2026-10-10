# NayaNET Living Design Transmission — SmartTabs + Button + Board Standard

**Status:** 2026-10-08 candidate specimen; independently review before any production adoption.

## Open the living page
Open **`index.html`**. It is entirely self-contained, including the authorized crystal N artwork, CSS, component JS and human-readable code-view panels. The three first buttons truly work; the SmartTabs ribbon supports add, edit, Purple Heart, Gold Star, remove and demonstration navigation. Browser-local storage is honestly labeled; no backend network, email sending or production authorization is claimed.

## Hand a new Naya these files
1. `index.html` — actual living example; experience before reading.
2. `smart-tabs.css` + `smart-tabs.js` — portable modular SmartTabs v10 design implementation.
3. `BUILD_LAW.md` — human/AI builder instructions and exact visual recipe.
4. `design_rules.machine.json` — structured testable requirements and truth boundaries.
5. `test_showroom.py` — reproducible Chromium test; must be supplemented by independent visual QA.
6. `naya-logo.png` — exact crystal N asset extracted from the Director-uploaded Naya Design Standard Showcase.

**The portable piece is SmartTabs.** Install its component files inside the existing canonical Hub shell—do not create another shell or store. `page.css` and `showroom.js` are for the teaching showroom, not a second production app.

## Start in three lines
```html
<div id="smarttabs"></div>
<link rel="stylesheet" href="smart-tabs.css"><script src="smart-tabs.js"></script>
<script>const tabs = SmartTabs.mount('#smarttabs', { storageKey: 'nayanet_shortcuts', onNavigate: (route) => window.location.assign(route) });</script>
```

`window.location.assign` is a simple functional fallback. **When integrating into NayaNET, connect `onNavigate` to the approved one-Hub router**. Never use hardcoded stale SmartNET routes as live destinations.

## Reusable API (preserved from SmartTabs v9 PDF)
```js
const tabs = SmartTabs.mount('#smarttabs', {storageKey:'nayanet_shortcuts',onNavigate:(route,item)=>window.location.assign(route)});
tabs.list();
tabs.set([{id:'reports', label:'Reports', route:'/reports', heart:false,star:true}]);
tabs.add({id:'library', label:'Library',route:'/library',heart:false,star:false});
tabs.update('library',{heart:true,star:false});
tabs.remove('library');
tabs.el.addEventListener('change', e => console.log(e.detail));
tabs.destroy();
```
Extra convenience: `tabs.openAdd()` and `tabs.reset()`.

## Design laws translated into behavior
- Three flagship controls: black #050505, **visible white rim at rest**, physical depth and breathing sheen. On hover/focus, each specimen's own jewel hue lights up; on press, the button sinks. Keyboard focus remains unambiguous.
- Boards: facet SVG jewel, lit vertical spine, black raised surfaces and four layers: IN A NUTSHELL → WHAT IT MEANS → HOW TO USE IT → WHAT'S IN IT FOR YOU.
- Smart Tabs: horizontally scrollable sticky ribbon, real buttons, real editor; heart/star mutually exclusive, explicit removal, same-origin local persistence only.
- Language: begin with the human meaning and benefit, provide full CSS/JS source afterward; not status-code jargon.
- Type: 18px body, at least 24px regular editorial headings, 14px support (18px where content is core), white readable prose.
- Colors: meaningful purple/blue/emerald/gold/magenta; never adjacent duplicate jewels. Gold stays a tiny rare accent.
- Safety: hostile labels are inserted as text, not markup; no `javascript:` routes; disabled/missing storage must not masquerade as cloud synchronization.
- One canonical shell, one managed brain; this is a teaching specimen only.

## How it relates to the Director's source
- `SMART TABS CODE and UNDERSTANDING (4).pdf`: v9 `window.SmartTabs.mount` contract, persistent shortcuts, actions and events. Same public verbs, visual refresh and keyboard/security repairs.
- `Smart TABS INSTRUTION (1).png`: original demo/documentation presentation; useful functional map, *not* the elite target style.
- `Naya Design Standard Showcase (1).html`: original physical controls/boards/specimen, actual embedded brand mark and requested human-readable design identity.
- `NAYA-DESIGN-CONTRACT-V1.pdf`: canonical black/white/purple, white at rest, own color on hover, meaningful room icons and honest local-state labels.

## Verification
`python test_showroom.py` (requires Python Playwright + local Chromium) runs five responsive viewports and interaction flows. This environment blocks file:// and localhost navigation, so the test uses Playwright `set_content` and an in-page localStorage substitute for the persistence test. It DOES test DOM/UI state, rendered CSS at five widths, labels safety, editor CRUD, focusable controls and code source view; it DOES NOT independently qualify actual cross-origin persistence, accessibility compliance, backend identity or production parity. Independent designer review still required.

## Cold Naya test / intended pass condition
Without the current chat, have a new agent reproduce a new themed Smart Tab from this kit, including own-hue hover, accessible options, safe text and a legitimate local route; check its generated output in Chromium and ask an *independent* Naya to challenge visual fidelity. `100/100` code assertions alone do not mean 10/10 user experience.

**One next action:** Naya 2 + independent designer perform actual visual/cold-successor acceptance. If accepted, adapt into existing canonical design tokens and room socket via governed PR; no second application.