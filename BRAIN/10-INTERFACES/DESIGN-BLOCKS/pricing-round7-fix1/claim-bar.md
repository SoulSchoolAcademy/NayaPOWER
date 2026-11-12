# Claim Bar — Claim Your Name
**Filed:** 2026-11-07 (pricing round 7 fix1, Addition 12). **Status:** filed object, in use (hero, demo card, close).
**Source:** NEW in this pass (the instruction set's single action). The single action is CLAIM YOUR NAME — `https://nayanet.app/yourname` (NEVER nayanet.live/yourname — .live retired). The button claims the name and starts the trial at Max; every other button is the same action in different words — never a different action.
**Construction:** a name input (`.claim-name`, deep input, gold focus) + the purple jewel claim button (`a[data-claim]`). Typing a name slugifies it (lowercase, non-alphanumeric → `-`, max 32 chars) and rewrites every `a[data-claim]` href to `nayanet.app/<slug>` (empty → `/yourname`); the three name inputs (hero, demo card, close) sync with each other; no-JS fallback: the buttons already point at `/yourname`. **The href split (by design, one action in three voices):** hero/close/demo claim buttons → the claim URL; tier buttons ("Claim your name — Power/Pro/Max") → the Smart Links (named as claims); the sticky bar → the Max Smart Link. `renderPrices` rewrites every `[data-link-tier]` anchor on toggle — that is why the hero/close claim buttons had `data-link-tier` removed.
```css
.claim-name{flex:0 1 190px; min-width:140px; padding:12px 14px; font-size:15px; color:var(--txt);
    background:linear-gradient(180deg,#1c1c26,#0a0a0f); border:1.5px solid rgba(255,191,61,.55); border-radius:12px;
    box-shadow:inset 0 2px 8px rgba(0,0,0,.7), inset 0 -1px 0 rgba(255,255,255,.08), 0 4px 14px rgba(0,0,0,.45);}
```
