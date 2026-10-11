# Inline Design Tokens Into Every Page — the Black Ground Must Be Structural, Not Contingent

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0738-inline-design-tokens-structural-black-ground
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6072425006 ([NAYA 5] Ultimate Lego — Shawn feedback round 3 applied, 2026-10-09T01:32Z / 2026-10-08 18:32 PDT); branch `naya5/ultimate-lego` @ `4e5bcf3a` (server tree verified == local)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5's Ultimate Lego Library opened with a white page — on a library whose first law is black ground. The root cause was not a missing background declaration: `tokens.css` was loaded through a **relative link that failed to resolve in the viewer**, so every `var(--...)` in every page fell back to nothing and the black `--field: #050507` never arrived. The entire visual identity was one broken link away from its photographic negative. The fix: tokens are now **inlined into every page** (index + all 8 lego files). Black is structural, not contingent — it cannot fall back to nothing because there is nothing to fall back to.

Why this is brain-grade and genuinely new: no existing Smart Note covers the token-link failure mode, and it is the kind of bug that recurs exactly when nobody remembers it. An external stylesheet link is a runtime dependency: it works in the dev viewer, fails in the artifact viewer, and the failure mode is silent (no error, just white). Any artifact whose design contract says "black ground" must make the black ground **impossible to lose** — inline the tokens, hard-code the root background, and never let the signature color ride on a resolvable link. Verification included 0 tag errors, balanced CSS, valid JS, **no white-background leaks**, server tree == local tree.

## 🩷 HUMAN NOTE

Shawn — a small but durable lesson from tonight's design work. The new Lego library opened as a white page even though the whole point of the design is black. The cause: the color definitions lived in a separate file linked with a relative path, and the viewer couldn't resolve it — so every color quietly fell back to nothing and the page went white. The fix: bake the color definitions directly into every page, so black is part of the document itself and can never vanish because of a broken link. The standing lesson for every build: whatever your design promises as the foundation — black ground, white text, any signature color — must be impossible to lose, never dependent on a file the viewer might not find.

## 🟣 CHILD NOTE

Imagine you write a recipe and say "use the special sauce from the fridge" — but in your friend's house, the fridge is somewhere else, and they find nothing. They serve the food with no sauce at all. Naya 5 did the same thing with colors: the pages said "get the colors from that other file over there," the viewer couldn't find the file, and everything turned white. The fix: write the colors INTO the recipe itself, so no matter whose kitchen you're in, the food comes out right.

## 👵 GRANDMA NOTE

Think of it like mailing a letter with instructions that say "the directions are on the fridge." If the person reading the letter has never seen your fridge, the directions are useless. We were sending pages that said "the colors are in this other file" — but sometimes the other file couldn't be found, and the pages showed up white instead of black. The lesson: put everything the page needs right inside the page itself. Don't make your most important choice — the black background everything else sits on — depend on a file that might not be there.

## 💜 NAYA NOTE

Cold Naya: when a design artifact renders white (or otherwise wrong) in a viewer where it was right in dev, check the stylesheet linkage first, not the styles. A relative `<link>` to tokens.css is a runtime dependency that fails silently — no error, just fallback-to-nothing on every `var()`. Reproduce: open the page in the artifact viewer with dev tools, confirm the link 404s or the computed `--field` is empty. Fix: inline the token block (`:root { ... }`) into every page that uses it, hard-set the body/root background to the signature color, and run a "no white-background leaks" scan (0 tag errors, CSS balanced, JS valid, server tree == local) before claiming the visual identity holds. Signature colors are structural: they belong in the document, not at the end of a link the viewer may never resolve.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0738",
  "title": "Inline Design Tokens Into Every Page — the Black Ground Must Be Structural, Not Contingent",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "DESIGN-CRAFT", "CSS-ROBUSTNESS"],
  "cousins": [],
  "evidence": {
    "board": ["#1354 comment 6072425006 ([NAYA 5] Ultimate Lego — Shawn feedback round 3 applied, 2026-10-09T01:32Z)"],
    "branch": "naya5/ultimate-lego @ 4e5bcf3a (server tree verified == local)",
    "root_cause": "tokens.css via relative link failed to resolve in the viewer; every var() fell back to nothing -> white page",
    "fix": "tokens inlined into index.html + all 8 lego files; --field: #050507 in the document itself",
    "verification": "0 tag errors, CSS balanced, JS syntax valid, no white-background leaks"
  },
  "doctrine": {
    "signature_is_structural": "whatever the design contract promises as foundation (black ground, signature color) must be impossible to lose — inline it, never link it",
    "silent_fallback_failure": "a relative stylesheet link is a runtime dependency: works in dev, fails in the artifact viewer, fails silently with no error",
    "check_linkage_first": "white/wrong render in viewer that was right in dev -> inspect stylesheet linkage before styles",
    "leak_scan_gate": "before claiming the visual identity holds: 0 tag errors, balanced CSS, valid JS, no white-background leaks"
  },
  "rule": "inline design tokens into every page that uses them; never let a signature color ride on a relative stylesheet link — structural, not contingent"
}
```
