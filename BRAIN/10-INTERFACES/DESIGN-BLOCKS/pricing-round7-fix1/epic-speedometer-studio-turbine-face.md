# Epic Speedometer — Studio Turbine Face
**Filed:** 2026-11-07 (pricing round 7 fix1). **Status:** filed object, in use on the pricing page (calculator + live mirror + demo gauge).
**Source:** the pricing page's own calculator gauge, rebuilt in fix1 (F12). **Honest note:** no verbatim epic speedometer exists in the Academy source (grep of NAYA_ACADEMY.md for `speed` = 0 hits; `speedometer|gauge|needle|dial` = only generic radial-gradient lines; ACADEMY-PARTS.md line 65 confirms the speedometer IS the pricing page's own calculator). The Dashboard sibling is a score dial (0–100), not a dollars dial — re-scaling would be a redraw, not verbatim. Per Addition 4's fallback, the flat SVG arc was DELETED and the gauge face is the Studio turbine image inside a physical gold bezel object, with a live needle. No new flat arc was drawn.
**Visual reference:** `banner-assets/pricing-supercharger-alt-studio.webp` (the turbine gauge as a real object).
**Construction:** gold bezel object + toothed gear ring (repeating-conic-gradient teeth + radial mask, learned from the Dashboard score gear) + concentric silver rings on the face + purple jewel centre hub + live needle (`#calc-needle`, same id/JS/angles as the verified round-7 file: `rotate(72deg)` @ $4,500, `rotate(-63deg)` @ $750, `rotate(-84.6deg)` @ $150) + counting readout + auto-demo ($750 → $4,500, no touch). The live mirror (`#live-needle`) and the demo gauge (`#demo-needle`, 0–100 Power Score) share the construction.
**Fix1 file sha at filing:** `e165822f3c195b0e…` (see MANIFEST.md for the full sha).
```css
.speedo-object{position:relative; width:360px; max-width:100%; aspect-ratio:1/1; margin:0 auto; border-radius:50%;
    background:radial-gradient(circle at 35% 28%, #3a3a46 0%, #17171e 38%, #0a0a0f 70%, #050507 100%);
    border:3px solid #ffbf3d;
    box-shadow:0 0 0 6px #14141a, 0 0 0 8px rgba(255,191,61,.35), inset 0 2px 0 rgba(255,255,255,.35),
      inset 0 -18px 34px rgba(0,0,0,.8), 0 24px 60px rgba(0,0,0,.8), 0 0 60px rgba(255,191,61,.28);
    overflow:visible;}
.speedo-object::before{content:""; position:absolute; inset:-15px; border-radius:50%; z-index:-1;
    background:repeating-conic-gradient(from 0deg, #c9c9d8 0deg 3deg, #33333e 3deg 6deg);
    -webkit-mask:radial-gradient(circle, transparent 0 78%, #000 79% 100%);
    mask:radial-gradient(circle, transparent 0 78%, #000 79% 100%);}
.speedo-face{position:absolute; inset:14px; width:calc(100% - 28px); height:calc(100% - 28px);
    object-fit:cover; object-position:center 32%; border-radius:50%; filter:saturate(1.05) contrast(1.03);
    box-shadow:0 0 0 2px #c9c9d8, 0 0 0 4px #17171f, inset 0 0 0 2px rgba(255,255,255,.18);}
.speedo-needle{position:absolute; left:calc(50% - 3px); bottom:50%; width:6px; height:42%; z-index:4;
    background:linear-gradient(180deg,#fff2c4,#ffbf3d 60%,#b97e0e); border-radius:3px 3px 0 0;
    transform-origin:50% 100%; box-shadow:0 0 12px rgba(255,191,61,.7);
    transition:transform .5s cubic-bezier(.2,.8,.2,1);}
#calc-needle{transform-origin:180px 178px; transition:transform .5s cubic-bezier(.2,.8,.2,1);}
```
