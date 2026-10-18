# NayaFunction unit format v1 — Item 26 (locked by coordinator 2026-10-18, revised per Shawn's 02:44Z ruling)

## Integration target: VERITY'S INTERFACE WINS
Primary DOM: `/home/hatch/workspace/user/files/smart-builder-intake_factory.html`
("Smart Factory — pick your pieces", 139140 bytes; fallback: `smart-builder-intake-2026-10-18-v5__1.html`).
Team Nitro does plumbing; Verity finishes the interface. Units NEVER reshape her page —
they attach to her hooks, idempotently.

## Her stable hooks (from the factory file — verify with grep before wiring)
- `#visionText` (textarea), `#dictBtn` — dictate
- `#cartFab`, `#cartDrawer`, `#cartItems`, `#cartCount`, `#closeCart` — cart
- `#buildBtn`, `#contract`, `#contractWrap`, `#copyBtn`, `#btnCopy` — contract-draft + copy
- `#reviewBtn`, `#sumWrap`, `#sumTmpl`, `#sumFunc`, `#sumPieces`, `#sumVision`, `#sumBuild`, `#sumClose`, `[data-go]` — review step (NEW in factory version)
- `.pcard[data-model][data-name][data-cat]` > `.szpill[data-s][data-z]`, `.btn-select`, `.btn-notes` — piece cards (51)
- `.tcard2[data-t]` > `.tview` — template cards (12)
- `.frow` > `.tog` (14 toggles: Smart Mail, Smart Lists, Smart Space, Connect + communicate,
  Intelligence Today, Personal social feed, Smart Tabs, Ask Naya, Reports, Booking doors,
  Guard, Saved, Calendar, Share) — feature on/off state
- `#step1`..`#step4` — scroll targets

## Two faces per function
1. **Intake face** (her page): the 5 intake units (dictate, copy, preview, cart, contract-draft)
   attach to her hooks above. IDEMPOTENT: `if (root.dataset.fnBound) return;` then set the flag —
   her inline script may already wire the same hooks; the unit must not double-bind or fight it.
   Long-term the inline script is replaced by unit activation; the unit is the canonical implementation.
2. **Built-page face** (assembler output): ALL 30 units activate by single declaration:
   `<div data-fn="<id>" data-fn-config='{...}'></div>` + `naya-functions.js` loader.
   The page-contract declares `functions: {"<id>": {...}}` → assembler emits the div + script tag.

## The contract (top of every file)

## The contract (top of every file)
```js
/* NayaFunction: <id> v1.0.0
   What: <one line>
   Activation: <div data-fn="<id>" data-fn-config='{...}'></div>
   Config: { ... } — every key documented, all optional unless marked *
   Ready behavior: <what works with zero backend>
   Connected behavior: <what the `connected` config key unlocks, or "none">
   Backend twin: <pipeline feature id or "none">
*/
```

## The code shape
```js
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return; // one function, one implementation — never double-register
  NF._r[id] = def;
};
NF.register('<id>', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    // 1. Fail soft: if required DOM/config is absent, do nothing harmful (L-2026-10-17-004)
    // 2. Wire ONLY elements inside `root` — never document-wide queries
    // 3. Every visible control must DO something real (Shawn's function law)
    return { destroy: function(){ /* unbind everything */ } };
  }
});
})();
```

## Loader (naya-functions.js)
- On DOMContentLoaded: find all `[data-fn]`, parse `data-fn-config` JSON (fail-soft on bad JSON),
  call `NayaFunctions._r[id].activate(el, config)` for registered ids; unregistered ids get a
  console.warn and are skipped (fail-closed — never pretend a missing function works).

## Laws for units
- READY first: every unit works fully client-side with zero backend. `connected` key is reserved.
- No staged behavior: if a control is visible, it works. Nothing decorative pretends to function.
- No flat dead controls: units use host-page classes where possible; minimal inline style for function only.
- Vanilla JS, no dependencies, deterministic (same config → same behavior), versioned.
- Never query outside `root`. Never `alert()` (use inline fail-soft messaging, like dictate does).
- White text in any unit-rendered copy (Law 1).

## Verification bar
Builder ships a `demo-<group>.html` harness mounting every unit in the group with sample configs.
A DIFFERENT seat loads it in real Chromium and clicks every control for real behavior.
Status only becomes VERIFIED on that seat's evidence. IMPLEMENTED = built + self-verified only.
