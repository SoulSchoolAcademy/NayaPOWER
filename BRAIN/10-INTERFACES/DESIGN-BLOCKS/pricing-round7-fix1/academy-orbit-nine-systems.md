# Academy Orbit — Nine Systems
**Filed:** 2026-11-07 (pricing round 7 fix1, F5). **Status:** filed object, in use (systems slide).
**Source:** the Academy source's `.orbit` / `.orbit-ring` / `.center` / `.node` (NAYA_ACADEMY.md), adapted — the flat numbered squares ("01 Personality / 02 Brain") were DELETED per Addition 4 order 2. The nine systems come in the Academy way: real objects on a black floor, Naya presenting at the edge.
**Construction:** center portrait (NAYA_POWER.jpg, 240px desktop) + toothed gear ring (purple, NAYA-JWL-016 language: rotating conic-gradient sunburst rays + purple glow) + nine nodes at Academy angles −90,−50,−10,30,70,110,150,190,230, each with a spectrum-accent dome stud + a capsule label. Phone: the orbit becomes a grid (fix7k2/k3) — center on its own row (150px), nine chips in a 3×3 grid; the sunburst is hidden on phone (it would paint over the chips); the center is `position:relative` so its img sizes to the 150px center, not the whole container (the fix7k root cause), with `left:auto; top:auto` (the desktop left/top only made sense with the desktop translate).
```css
.sys-orbit{--orbit-size:min(680px,86vw); position:relative; width:var(--orbit-size);
    height:calc(var(--orbit-size) + 90px); margin:8px auto 28px;}
.sys-orbit-ring{position:absolute; left:50%; top:50%; width:var(--orbit-size); aspect-ratio:1;
    transform:translate(-50%,-50%); border:1px solid rgba(255,255,255,.2); border-radius:50%;
    box-shadow:0 0 70px rgba(138,92,255,.1), inset 0 0 70px rgba(138,92,255,.06);}
.sys-orbit-center{position:absolute; left:50%; top:50%; width:min(240px,34vw); aspect-ratio:1;
    transform:translate(-50%,-50%); border-radius:50%; display:grid; place-items:center; z-index:5; overflow:hidden;
    border:1px solid rgba(255,255,255,.42);
    background:radial-gradient(circle at 50% 48%, #211b2b 0 30%, #100c18 58%, #050308 80%, #000 100%);
    box-shadow:inset 18px 15px 44px rgba(255,255,255,.1), inset -42px -45px 82px rgba(0,0,0,.94),
      0 55px 110px rgba(0,0,0,.95), 0 0 130px rgba(138,92,255,.25), 0 0 60px rgba(160,107,255,.35);}
.sys-orbit-sunburst{position:absolute; left:50%; top:50%; width:340px; height:340px; transform:translate(-50%,-50%);
    border-radius:50%; z-index:1; pointer-events:none;
    background:repeating-conic-gradient(from 0deg, rgba(160,107,255,.30) 0deg 5deg, transparent 5deg 10deg);
    -webkit-mask:radial-gradient(circle, transparent 0 62%, #000 64% 100%);
    mask:radial-gradient(circle, transparent 0 62%, #000 64% 100%);
}
.sys-node{position:absolute; left:50%; top:50%; width:150px; text-align:center; z-index:8;
    transform:translate(-50%,-50%) rotate(var(--a)) translateY(calc(var(--orbit-size)/-2 + 44px)) rotate(calc(-1 * var(--a)));}
.sys-node-dot{position:relative; display:block; width:18px; height:18px; margin:0 auto; border-radius:50%;
    background:radial-gradient(circle at 30% 25%, #fff, var(--accent) 42%, #000 100%);
    box-shadow:0 0 0 4px rgba(255,255,255,.06), 0 0 24px var(--accent);}
.sys-node-name{display:inline-block; margin-top:8px; padding:7px 11px; border-radius:999px;
    background:linear-gradient(180deg, rgba(18,15,23,.96), #030303); border:1px solid var(--accent);
    color:#fff; font-size:11px; font-weight:800; letter-spacing:.06em; text-transform:uppercase;
    box-shadow:0 12px 26px rgba(0,0,0,.68);}
```
```html
<div class="sys-orbit" aria-label="The nine systems orbiting Naya">
      <div class="sys-orbit-ring" aria-hidden="true"></div>
      <div class="sys-orbit-sunburst" aria-hidden="true"></div>
      <div class="sys-orbit-center"><img src="banner-assets/NAYA_POWER.jpg" alt="Naya — the nine systems orbit her"><span>NAYA</span></div>
      <div class="sys-node" style="--a:-90deg; --accent:var(--purple);"><span class="sys-node-dot"></span><span class="sys-node-name">Personality</span></div>
      <div class="sys-node" style="--a:-50deg; --accent:var(--blue);"><span class="sys-node-dot"></span><span class="sys-node-name">Brain</span></div>
      <div class="sys-node" style="--a:-10deg; --accent:var(--green);"><span class="sys-node-dot"></span><span class="sys-node-name">Notes</span></div>
      <div class="sys-node" style="--a:30deg; --accent:var(--gold);"><span class="sys-node-dot"></span><span class="sys-node-name">Lead Mode</span></div>
      <div class="sys-node" style="--a:70deg; --accent:var(--orange);"><span class="sys-node-dot"></span><span class="sys-node-name">Law</span></div>
      <div class="sys-node" style="--a:110deg; --accent:var(--red);"><span class="sys-node-dot"></span><span class="sys-node-name">Scorecarding</span></div>
      <div class="sys-node" style="--a:150deg; --accent:var(--magenta);"><span class="sys-node-dot"></span><span class="sys-node-name">Language</span></div>
      <div class="sys-node" style="--a:190deg; --accent:var(--purple);"><span class="sys-node-dot"></span><span class="sys-node-name">Design</span></div>
      <div class="sys-node" style="--a:230deg; --accent:var(--blue);"><span class="sys-node-dot"></span><span class="sys-node-name">Coder</span></div>
    </div>
```
