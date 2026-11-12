# Morph Widget — Watch It Morph
**Filed:** 2026-11-07 (pricing round 7 fix1, Addition 12, Ultimate Ten #5). **Status:** filed object, in use (live experience, section 04).
**Source:** NEW in this pass. One app, four doors, three people — creator, business owner, community builder — using REAL pages (Personal, Business, Space, Dashboard), never invented screens.
**Construction:** three persona buttons (46px touch target, hover lift + gold ignite, is-on text white per L5) reorder the four door chips (the persona's home door first + HOME marker) and swap the line; per-persona lines restate the chart's feature descriptions. **Fix found by eye (fix7k, 2026-11-07):** the HOME badge span was a static child of the Personal door, so after a persona click the gold border moved to the first door but the badge stayed on Personal — two home indicators. The JS now moves the badge into the first door on every click (`firstDoor.insertBefore(badge, firstDoor.firstChild)`). Verified: business → Business is home AND has the badge; community → Space is home AND has the badge.
```css
.morph-persona{background:linear-gradient(180deg,#262633,#0a0a0f 70%); color:var(--txt); border:1.5px solid rgba(255,255,255,.22); border-radius:999px; padding:12px 18px; font-size:14px; font-weight:700; cursor:pointer; box-shadow:inset 0 1px 0 rgba(255,255,255,.14), 0 6px 14px rgba(0,0,0,.5);}
.morph-persona.is-on{border-color:var(--gold); color:var(--txt); box-shadow:inset 0 1px 0 rgba(255,255,255,.14), 0 6px 14px rgba(0,0,0,.5), 0 0 0 2px rgba(255,191,61,.25);}
.morph-door{position:relative; background:linear-gradient(180deg,#1a1a26,#0a0a0f 72%); border:1px solid rgba(255,255,255,.16); border-radius:14px; padding:16px 12px 12px; text-align:center; box-shadow:inset 0 1px 0 rgba(255,255,255,.12), 0 10px 22px rgba(0,0,0,.45);}
.morph-door.is-home{border-color:var(--gold); box-shadow:inset 0 1px 0 rgba(255,255,255,.12), 0 10px 22px rgba(0,0,0,.45), 0 0 0 2px rgba(255,191,61,.3);}
.morph-door-home{position:absolute; top:-9px; left:50%; transform:translateX(-50%); background:var(--gold); color:#111; font-size:10px; font-weight:800; letter-spacing:.08em; border-radius:999px; padding:2px 8px;}
```
