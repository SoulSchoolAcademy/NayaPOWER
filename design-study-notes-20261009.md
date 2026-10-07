# Design Study Notes — 2026-10-09
## Shawn's directive: "Study. Take lots of notes."
## "Take the best of all the code... the highest level of buttons and boards that can possibly be created"

Source files studied: all 11 room HTML files + Naya_Design_Standard_Showcase__1-2.html + V2 review packet.
All CSS below is VERBATIM from the reference files. Nothing theorized.

---

## 1. THE MASTER BUTTON: `.cx-btn`
Source: `Naya_Design_Standard_Showcase__1-2.html` (verbatim)

```css
.cx-btn {
  position:relative; overflow:hidden;
  padding:15px 32px; border-radius:999px;
  font-size:14px; font-weight:800; letter-spacing:.1em;
  cursor:pointer; font-family:inherit; color:#fff;
  text-shadow:0 1px 3px rgba(0,0,0,.9), 0 0 12px rgba(255,255,255,.35);
  background:linear-gradient(180deg,#232329,#0a0a0d 55%,#050506);
  border:1.5px solid rgba(255,255,255,.75);
  display:inline-flex; align-items:center; gap:10px;
  box-shadow:
    inset 0 2px 3px rgba(255,255,255,.35),
    inset 0 -4px 8px rgba(0,0,0,.7),
    0 0 26px rgba(255,255,255,.32),
    0 0 60px -12px rgba(255,255,255,.25),
    0 16px 36px rgba(0,0,0,.75);
  animation:btn-breathe 4s ease-in-out infinite;
  transition:border-color .22s, box-shadow .25s, transform .15s var(--ease);
}
.cx-btn::after {
  content:""; position:absolute; top:0; bottom:0; width:45%; left:-60%;
  background:linear-gradient(105deg, transparent, rgba(255,255,255,.22), transparent);
  transform:skewX(-18deg);
  animation:btn-shimmer 5s ease-in-out infinite;
  pointer-events:none;
}
.cx-btn:hover {
  border-color:var(--chrome);
  transform:translateY(-3px) scale(1.02);
  animation:none;
  box-shadow:
    inset 0 2px 3px rgba(255,255,255,.4),
    inset 0 -4px 8px rgba(0,0,0,.6),
    0 0 36px rgba(255,255,255,.38),
    0 0 52px -4px var(--chrome),
    0 0 90px -12px var(--chrome),
    0 20px 42px rgba(0,0,0,.7);
}
.cx-btn:active {
  transform:translateY(1px) scale(.97);
  animation:none;
  box-shadow:
    inset 0 3px 10px rgba(0,0,0,.8),
    inset 0 -2px 6px rgba(0,0,0,.6),
    0 0 20px -4px var(--chrome),
    0 8px 20px rgba(0,0,0,.7);
}
@keyframes btn-breathe {
  0%,100%{box-shadow:inset 0 2px 3px rgba(255,255,255,.35), inset 0 -4px 8px rgba(0,0,0,.7), 0 0 26px rgba(255,255,255,.32), 0 0 60px -12px rgba(255,255,255,.25), 0 16px 36px rgba(0,0,0,.75);}
  50%{box-shadow:inset 0 2px 3px rgba(255,255,255,.42), inset 0 -4px 8px rgba(0,0,0,.68), 0 0 36px rgba(255,255,255,.42), 0 0 76px -10px rgba(255,255,255,.32), 0 18px 40px rgba(0,0,0,.78);}
}
@keyframes btn-shimmer {
  0%{left:-60%;} 55%{left:130%;} 100%{left:130%;}
}
```

### Why each value was chosen (apprentice analysis):

1. **`inset 0 2px 3px rgba(255,255,255,.35)`** — THE top light. 2px tall (not 1px), 35% white. This is what makes it look like a physical object with light hitting the top edge. Our v3 used only `inset 0 1px 0 rgba(255,255,255,.9)` — thinner and flatter.

2. **`inset 0 -4px 8px rgba(0,0,0,.7)`** — THE bottom shade. 4px deep, 70% black, blurred 8px. This is the counterweight to the top light — it makes the button look ROUND, like a physical pill. **Our v3 was completely missing this.** This is a major reason ours felt flat.

3. **`0 0 26px rgba(255,255,255,.32)`** — tight white glow. The button has a halo even at rest.

4. **`0 0 60px -12px rgba(255,255,255,.25)`** — wide white aura (negative spread keeps it tight). Ambient presence.

5. **`0 16px 36px rgba(0,0,0,.75)`** — deep drop shadow. 16px down, 36px blur. The button FLOATS.

6. **`border:1.5px solid rgba(255,255,255,.75)`** — the white rim. 1.5px (not 1px), 75% white. Visible, present, catches the eye.

7. **`text-shadow:0 1px 3px rgba(0,0,0,.9), 0 0 12px rgba(255,255,255,.35)`** — text has BOTH a dark drop (readability) and a white glow (luminosity). Text looks lit from within.

8. **`background:linear-gradient(180deg,#232329,#0a0a0d 55%,#050506)`** — vertical gradient, lighter at top. Even on a dark button, the top is lighter. Light comes from above. Always.

9. **`btn-breathe 4s`** — the shadow stack breathes. At 50%, every glow value increases ~20%. The button is ALIVE at rest, not static.

10. **`btn-shimmer 5s`** — a 45%-wide skewed white band sweeps across every 5 seconds. Light catches the button periodically. Note: shimmer pauses at 130% from 55-100% (rest period between sweeps).

11. **Hover: `translateY(-3px) scale(1.02)`** — lifts AND grows. Not just one. The button reaches toward you.

12. **Hover shadow adds TWO chrome glow layers** (`0 0 52px -4px var(--chrome), 0 0 90px -12px var(--chrome)`) — tight bright + wide soft. This is the "ignite" — the color doesn't just appear, it RADIATES.

13. **Active: `translateY(1px) scale(.97)`** — presses DOWN and SHRINKS. The inset shadows go dark (`inset 0 3px 10px rgba(0,0,0,.8)`). The button is physically pressed INTO the surface. This is real press physics, not just a scale.

14. **`animation:none` on hover/active** — CRITICAL. The breathe animation is killed on interaction so the hover shadow actually renders. (We fixed this same bug in v3.)

---

## 2. SHAWN'S BUTTON LAW (verbatim from code comments)

From reports.html:
> "SHAWN'S BUTTON LAW (2026-10-02): silver-white at rest, theme color on highlight."

Repeated across spaces.html, connect.html, mail.html, ledger.html, library.html:
> "Drawer buttons: silver-luminous at rest, ignite identity color on hover"

The law is consistent: **white/silver at rest → theme color on interaction.** Never colored at rest (except the single primary CTA per room).

---

## 3. THE SHARED CHROME: `.naya-corner-btn`
Identical across ALL 11 files (verbatim):

```css
.naya-corner-btn {
  flex:none; width:44px; height:44px; border-radius:14px;
  border:1px solid rgba(232,234,242,.42);
  background:linear-gradient(145deg,rgba(26,20,36,.9),rgba(11,10,16,.9));
  color:#fff; cursor:pointer; display:grid; place-items:center;
}
.naya-corner-btn:hover {
  border-color:#9d75ff;
  box-shadow:0 0 20px -2px #9d75ff, 0 0 6px #9d75ff, 0 8px 20px rgba(0,0,0,.6);
}
.naya-corner-btn:active {
  /* same as hover + */ transform:scale(.94);
}
```

Notes:
- 44px touch target (Apple HIG minimum)
- 145deg gradient (diagonal light, not vertical — subtle variation for chrome vs buttons)
- Silver border `rgba(232,234,242,.42)` — this specific silver appears in EVERY file. It's the standard.
- Hover glow pattern: `0 0 20px -2px COLOR, 0 0 6px COLOR` — wide soft + tight bright. Same pattern everywhere.
- Active is just `scale(.94)` — simple, fast, physical.

---

## 4. THE MASTER BOARD: `.board`
Source: `Naya_Design_Standard_Showcase__1-2.html` (verbatim)

```css
.board {
  position:relative; overflow:hidden;
  border:2px solid color-mix(in srgb, var(--ic) 55%, rgba(255,255,255,.45));
  border-radius:22px; padding:28px 32px;
  background:linear-gradient(165deg,rgba(26,24,22,.92),rgba(10,10,12,.94));
  box-shadow:
    inset 0 2px 3px rgba(255,255,255,.16),
    inset 0 -5px 14px rgba(0,0,0,.55),
    0 30px 75px rgba(0,0,0,.7),
    0 0 55px -6px var(--ic),
    0 0 120px -20px var(--ic);
  transition:box-shadow .3s var(--ease), border-color .3s var(--ease), transform .3s var(--ease);
}
.board::before {  /* left accent bar */
  content:""; position:absolute; left:0; top:0; bottom:0; width:7px;
  background:linear-gradient(180deg,#fff,var(--ic));
  box-shadow:0 0 30px var(--ic), 0 0 60px -6px var(--ic);
}
.board::after {  /* top light line */
  content:""; position:absolute; top:0; left:18px; right:18px; height:1px;
  background:linear-gradient(90deg, transparent, rgba(255,255,255,.42), transparent);
  pointer-events:none;
}
.board:hover {
  transform:translateY(-3px);
  border-color:color-mix(in srgb, var(--ic) 65%, rgba(255,255,255,.6));
  box-shadow:
    inset 0 2px 3px rgba(255,255,255,.2),
    inset 0 -5px 14px rgba(0,0,0,.5),
    0 36px 84px rgba(0,0,0,.72),
    0 0 78px -4px var(--ic),
    0 0 150px -16px var(--ic);
}
```

Notes:
- Same 5-layer shadow formula as the button, scaled up for boards
- `::before` = 7px glowing accent bar on the left (white → theme color gradient)
- `::after` = 1px light line across the top (fades at edges)
- Border mixes theme color 55% with white 45% — the border itself glows with identity
- Drop shadow is MASSIVE: `0 30px 75px rgba(0,0,0,.7)` — boards float high

---

## 5. V2 BUTTON (from review packet)
```css
.btn {
  --glow:var(--purple);
  min-height:54px; padding:11px 24px;
  background:linear-gradient(150deg,#13121a 0%,#050505 58%,#111119 100%);
  border:1.8px solid #fffffff0;  /* NEAR-WHITE border */
  border-radius:999px; color:#fff; font-size:16px; font-weight:750;
  box-shadow:
    inset 0 1px #ffffff65,        /* strong top highlight */
    0 15px 30px #000d,             /* deep drop */
    0 0 17px -6px #fff8;           /* white halo */
}
.btn:hover {
  border-color:var(--glow);
  box-shadow:inset 0 1px #fff8, 0 12px 31px #000a, 0 0 22px var(--glow);
  transform:translateY(-2px);
}
.btn:active {
  transform:translateY(2px);
  box-shadow:inset 0 2px 8px #000e;  /* pressed IN */
}
```

Notes:
- `border:1.8px solid #fffffff0` — nearly OPAQUE white border. Bolder than cx-btn's 75%.
- `font-weight:750` — between bold and extrabold. Precise.
- `min-height:54px` — larger than today's 42px. More presence.

---

## 6. TODAY.HTML BUTTON SYSTEM
```css
.btn {
  --btn-accent: var(--room-accent, var(--magenta));
  min-height:42px; padding:0 22px; border-radius:999px;
  border:1px solid color-mix(in srgb, var(--btn-accent) 45%, transparent);
  background:linear-gradient(145deg,
    color-mix(in srgb, var(--btn-accent) 26%, #1a1424),
    color-mix(in srgb, var(--btn-accent) 10%, #0b0a10));
  font-size:12.5px; font-weight:800; letter-spacing:.06em;
  box-shadow:var(--depth-hi), 0 10px 26px #000a,
    0 0 22px color-mix(in srgb, var(--btn-accent) 26%, transparent);
}
.btn:hover {
  transform:translateY(-2px); filter:brightness(1.12);
  box-shadow:var(--depth-hi), 0 16px 36px #000b,
    0 0 34px color-mix(in srgb, var(--btn-accent) 40%, transparent);
}
.btn:active { transform:translateY(0) scale(.985); }
```

Notes:
- Uses `color-mix()` throughout — theme color is MIXED into backgrounds, not flat-applied
- `--btn-accent` inherits from `--room-accent` — every room's buttons automatically use the room color
- `filter:brightness(1.12)` on hover — simple but effective lift

---

## 7. DESIGN TOKENS (from today.html :root)

```css
--bg: #050507; --bg-raise: #0b0a10; --bg-panel: #0d0c12; --bg-card: #14101b;
--ink: #f8f7fb; --ink-dim: #ddd9e4;
--line: #ffffff18; --line-soft: #ffffff0d;
--depth-hi: inset 0 1px #fff6;
--depth-drop: 0 18px 42px #000b;
--depth-deep: 0 20px 48px #000d;
--ease: cubic-bezier(.16,.84,.22,1);
--dur-fast: .18s; --dur-med: .28s;
--radius-lg: 17px; --radius-pill: 999px;
--font: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
--voice: "Cormorant Garamond", Georgia, serif;  /* editorial/voice surfaces */
```

Spectrum (12 colors): purple #9d75ff, indigo #6675ff, sapphire #4f8ff7, blue #55b9ee, teal #40d3bb, emerald #35e0a1, green #55e39a, lime #b8ee57, yellow #f1d75a, gold #e8c766, orange #ff9a5a, rich-orange #ff7a3d, red #ff5e6c, magenta #d86cff

---

## 8. WHERE OUR V3 FALLS SHORT (honest gap analysis)

Our v3 `.hero-btn-face`:
```css
background:linear-gradient(180deg, #ffffff 0%, #f3f5fb 48%, #d8def0 100%);
box-shadow:
  inset 0 1px 0 rgba(255,255,255,.9),
  inset 0 -2px 8px rgba(105,120,170,.42),
  0 0 0 1.5px rgba(0,0,0,.5),
  0 2px 6px rgba(0,0,0,.5),
  0 14px 36px rgba(0,0,0,.55),
  0 0 44px -6px rgba(var(--c),.55);
```

Gap vs `.cx-btn`:
1. **Top highlight too thin:** we use `inset 0 1px 0` — master uses `inset 0 2px 3px`. The 2px height + 3px blur creates a SOFTER, more physical light catch. Ours is a hard 1px line.
2. **Bottom shade too weak:** we use `inset 0 -2px 8px rgba(105,120,170,.42)` (bluish, 42%) — master uses `inset 0 -4px 8px rgba(0,0,0,.7)` (black, 70%, twice as deep). Ours doesn't create the "round pill" feeling.
3. **Missing white glow layers:** master has TWO white glow layers at rest (`0 0 26px rgba(255,255,255,.32)` + `0 0 60px -12px rgba(255,255,255,.25)`). We have none — our glow is only the theme color.
4. **Drop shadow too shallow:** we use `0 14px 36px` — master uses `0 16px 36px rgba(0,0,0,.75)`. Close, but master's is darker.
5. **No breathe animation:** master breathes the shadow stack every 4s. Ours has a conic rotation but not shadow breathing.
6. **No shimmer sweep:** master has the ::after shimmer every 5s. We don't.
7. **Border:** we use `0 0 0 1.5px rgba(0,0,0,.5)` (dark outline) — master uses `1.5px solid rgba(255,255,255,.75)` (white border). For white buttons, we need a different border strategy.
8. **Text:** master uses dual text-shadow (dark drop + white glow). We should verify ours.

---

## 9. THE SYNTHESIS: What to build

Take the master's DIMENSIONALITY (5-layer shadow formula, breathe, shimmer, press physics) and apply it to WHITE pearl faces (Shawn's "white at rest" directive) with spectrum ignition on hover.

The formula for each hero button:
- Face: white pearl gradient (lighter top → slightly darker bottom)
- Border: visible white/silver rim (1.5px+)
- Shadow stack (5 layers):
  1. `inset 0 2px 3px rgba(255,255,255,.5)` — strong top light
  2. `inset 0 -4px 10px rgba(0,0,0,.18)` — bottom shade (subtler on white)
  3. `0 0 28px rgba(255,255,255,.35)` — white glow
  4. `0 0 70px -12px [theme]` — theme aura
  5. `0 18px 44px rgba(0,0,0,.6)` — deep drop
- Breathe: shadow stack pulses every 4s
- Shimmer: white band sweeps every 5-6s
- Hover: ignite in theme color (border → theme, add theme glow layers), lift -3px, scale 1.02
- Active: press in (translateY(1px) scale(.97)), inset shadows go dark
- Text: dark text on white with subtle shadow for depth
