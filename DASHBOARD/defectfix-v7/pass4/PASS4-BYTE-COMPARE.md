# PASS-4 BYTE-COMPARE — the minis ARE the v74 calculator gauge

Source A (v74): `PRICING/pricing-live.html`, blob `a2d06d5b` (sha256 `7a0b837c481f5dfce041dcd3faf5e72c2cdf4c184316604efa21f2bd3dc76db8`), whose tntacho block is byte-identical to `pricing/rebuild/tntacho.js.html` (53,673 B; verified by extraction diff — only a trailing newline).
Source B (pass-4): `dashboard-pass4.html` — `templateCalc(sc)`, `calcDialNumerals(sc)`, `calcTickLines(sc)`, `mountMiniCalc`.

## template() (v74) vs templateCalc(sc) (pass-4) — signature line excluded

Diff lines: 72 (0 = byte-identical modulo the signature line).

```diff
--- v74
+++ pass4-templateCalc
@@ -17,6 +17,15 @@
               '<stop offset="55%" stop-color="#7a7e88"/>' +
               '<stop offset="72%" stop-color="#8f93a0"/>' +
               '<stop offset="88%" stop-color="#b9bdc8"/>' +
+              '<stop offset="100%" stop-color="#d6d9e0"/>' +
+            '</linearGradient>' +
+            /* PASS 4 (fail 6): tnAluHub was referenced by .tn-gear-hub but
+               NEVER defined — the gear hubs had no valid fill. Silver,
+               matching mBrushed. */
+            '<linearGradient id="tnAluHub" x1="0%" y1="0%" x2="100%" y2="100%">' +
+              '<stop offset="0%" stop-color="#eef0f4"/>' +
+              '<stop offset="38%" stop-color="#9a9ea8"/>' +
+              '<stop offset="55%" stop-color="#7a7e88"/>' +
               '<stop offset="100%" stop-color="#d6d9e0"/>' +
             '</linearGradient>' +
             /* 2026-11-02 — SHAWN: Shiny obsidian black. Polished black glass.
@@ -153,13 +162,13 @@
               gearTeeth(100, 104, 99, 48, 0) +
             '</g>' +
           '</g>' +
-          /* === LAYER 4: DIAL — 0-500, ticks, numerals === */
+          /* === LAYER 4: DIAL — the stat's own scale, ticks, numerals === */
           /* 2026-11-02 — SHAWN: Make it REAL. Dial is RECESSED below bezel.
              Inner shadow at the edge creates the depth. */
           '<circle cx="100" cy="104" r="84" fill="#050607"/>' +
           '<circle cx="100" cy="104" r="84" fill="none" stroke="#000" stroke-width="4" opacity=".7"/>' +
           '<circle cx="100" cy="104" r="82" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="1"/>' +
-          tickLines() +
+          calcTickLines(sc) +
           /* 2026-11-02 — SHAWN: "Get rid of all those numbers." Dial numerals REMOVED.
              They return ONLY at the edge, done right. See LAYER 5B. */
           '<path class="tn-tacho-track" d="' + ARC_D + '"/>' +
@@ -212,7 +221,7 @@
           /* 2026-11-02 — SHAWN: numerals BACK, but CORRECT. Real speedometer geometry:
          0 at bottom-left (135°), 500 at bottom-right (45°), sweep across the TOP.
          angle = 135 + (v/500)*270. */
-          '<g class="tn-edge-numerals">' + dialNumerals() + '</g>' +
+          '<g class="tn-edge-numerals">' + calcDialNumerals(sc) + '</g>' +
           /* === LAYER 6: MOVEMENT — concentric fine gears, counter-rotating === */
           '<g class="tn-tacho-mech" aria-hidden="true">' +
             '<circle cx="100" cy="104" r="30" fill="url(#mCavity)"/>' +
@@ -271,6 +280,11 @@
           '<rect x="87" y="173" width="26" height="3" rx="1.5" fill="rgba(0,0,0,.7)"/>' +
           '<rect x="87" y="182" width="26" height="1.5" rx=".75" fill="rgba(255,255,255,.08)"/>' +
           '<text class="tn-tacho-svgnum" x="100" y="183" text-anchor="middle" style="font-size:8px;font-family:Georgia,serif;">…</text>' +
+          /* 2026-11-08 — SHAWN'S EYE: the lap text ("3RD LAP — 1K") is OFF the
+             dial — no text over the dial, ever. The lap line lives BELOW the
+             gauge now, as HTML (.tn-tacho-lapline, painted by paintLap), clear
+             of the object. The svgnum above stays: it is the dial's own
+             numeral, below the arc, in its inset plate. */
           '' +
           /* === LAYER 9: PURPLE ACCENT ARC === */
           '<path d="M 148 130 A 56 56 0 0 1 152 142" stroke="#a06bff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>' +
@@ -289,13 +303,9 @@
         '<div class="tn-tacho-bands"><span class="tn-tacho-bandlo"></span><span class="tn-tacho-bandhi"></span><span class="tn-tacho-bands-label"></span></div>' +
         '<div class="tn-tacho-truth" hidden></div>' +
       '</div>' +
-      /* FIX-9 (Pricing fix pass 1): the bandline is BACK — the design review
-         orders it visible ("$X of $10 000 — next rung"). It lives AFTER the
-         dialwrap close, as its own line genuinely BELOW the dial (the FIX
-         1e-iii position), so it cannot block the gauge face. This reverses
-         the FIXE2-lane1 removal below; the render must prove it sits below
-         the dial without blocking it. */
-      '<div class="tn-tacho-bandline"></div>' +
+      /* 2026-11-08 — SHAWN'S EYE: the lap line, below the gauge, clear of the
+         object. paintLap writes it; hidden when there is no lap to name. */
+      '<div class="tn-tacho-lapline" hidden></div>' +
       /* 2026-11-07 — FIXE2-lane1 (Defect 1a, Shawn's eye 15:21Z): the bandline
          span is GONE. It rendered "44 of 500 — Stirring at 1,000" at the
          gauge's lower rim, blocking the gauge presentation. paintBandChrome
```

## dialNumerals() (v74) vs calcDialNumerals(sc) (pass-4)

Diff lines: 32 (0 = byte-identical modulo the signature line).

```diff
--- v74
+++ pass4-templateCalc
@@ -1,21 +1,18 @@
-  function dialNumerals(){
-    /* 2026-11-02 — SHAWN: Numbers must be EXACT, not random. Like a real gauge.
-       FIX-9: the dial is dollars, fixed 0-$10K — $0, $1K, $2K ... $10K, every
-       1000 labeled. Ticks every 200, major every 1000. All calculated:
-       angle = 135 + (v/10000)*270. Stamped in the machine — engraved, not
-       floating text. */
+  function calcDialNumerals(sc){
+    /* v74 dialNumerals, byte-for-byte except the vals/labels: the dial is
+       the stat's OWN scale (11 labels, 0..max), never $0–$10K pasted on a
+       board whose stats differ. Geometry identical to v74. */
     var h = '', i;
-    var vals = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000];
+    var vals = [];
+    for (i = 0; i <= 10; i++) vals.push(sc.max * i / 10);
     for (i = 0; i < vals.length; i++){
       var val = vals[i];
-      var label = (val === 0) ? '$0' : '$' + (val/1000) + 'K';
-      var angleDeg = 135 + (val/10000)*270;
+      var label = calcLabel(sc, val);
+      var angleDeg = 135 + (val / sc.max) * 270;
       var angle = angleDeg * Math.PI / 180;
       var x = 100 + 79 * Math.cos(angle);
       var y = 104 + 79 * Math.sin(angle);
-      /* shadow copy for depth (engraved look) */
       h += '<text x="' + (x+0.9).toFixed(1) + '" y="' + (y+3.4).toFixed(1) + '" text-anchor="middle" class="tn-dial-num-shadow">' + label + '</text>';
-      /* 2026-11-02 — FIX: CSS fill:url() unreliable. Set fill directly as attribute. */
       h += '<text x="' + x.toFixed(1) + '" y="' + (y+2.3).toFixed(1) + '" text-anchor="middle" class="tn-dial-num">' + label + '</text>';
     }
     return h;
```

## tickLines() (v74) vs calcTickLines(sc) (pass-4)

Diff lines: 53 (0 = byte-identical modulo the signature line).

```diff
--- v74
+++ pass4-templateCalc
@@ -1,13 +1,12 @@
-  function tickLines(){
-    /* 2026-11-02 — SHAWN: ticks like the reference. White, scale-accurate:
-       every 10 minor, every 50 major. Long white majors, short minors.
-       The little lines that make it feel real. */
+  function calcTickLines(sc){
+    /* v74 tickLines, byte-for-byte except the steps: minor every max/50,
+       major every max/10, at the midpoints between numerals — the same
+       270° sweep, the same white ticks, the same bezel + dial screws. */
     var h = '', v, rad;
-    /* 2026-11-02 — SHAWN: Ticks at MIDPOINTS between numerals (25,75,125...).
-       Like the Bugatti: numeral, tick, numeral, tick. VISIBLE, pro. */
-    for (v = 10; v < 500; v += 10){
-      if (v % 50 === 0) continue;
-      var angleDeg = 135 + (v/500)*270;
+    var step = sc.max / 50, major = sc.max / 10;
+    for (v = step; v < sc.max; v += step){
+      if (Math.abs(v % major) < 1e-9) continue;
+      var angleDeg = 135 + (v / sc.max) * 270;
       rad = angleDeg * Math.PI / 180;
       var rr1 = 78, rr2 = 86;
       var sw = 2.5;
@@ -18,28 +17,18 @@
            '" y2="' + (104 + rr2 * Math.sin(rad)).toFixed(1) +
            '" stroke="#ffffff" stroke-width="' + sw + '" opacity="' + op + '"/>';
     }
-    /* 2026-11-02 — REMOVED duplicate numerals. dialNumerals() is the single source.
-       tickLines() does ticks only. */
-    /* 2026-11-02 — BUGATTI DIAL SCREWS. 4 screws at the dial corners.
-       Like the real instrument — they hold the dial in place.
-       2026-11-02 — FIX: r=70 (were hidden at r=80). All 4 must be visible. */
     var screwAngles = [45, 135, 225, 315];
     for (var si = 0; si < screwAngles.length; si++){
       var sa = screwAngles[si] * Math.PI / 180;
       var sx = 100 + 58 * Math.cos(sa), sy = 104 + 58 * Math.sin(sa);
-      /* screw head — larger, more visible */
       h += '<circle cx="' + sx.toFixed(1) + '" cy="' + sy.toFixed(1) + '" r="4" class="tn-dial-screw"/>';
-      /* screw slot (random rotation for realism) */
       var slotA = (screwAngles[si] * 1.7) * Math.PI / 180;
       var x1 = sx + 2.8 * Math.cos(slotA), y1 = sy + 2.8 * Math.sin(slotA);
       var x2 = sx - 2.8 * Math.cos(slotA), y2 = sy - 2.8 * Math.sin(slotA);
       h += '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) +
            '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" class="tn-dial-screw-slot"/>';
-      /* highlight — catches the light */
       h += '<circle cx="' + (sx-1).toFixed(1) + '" cy="' + (sy-1).toFixed(1) + '" r="1.2" fill="rgba(255,255,255,.3)"/>';
     }
-    /* 2026-11-02 — REFERENCE BUILD. Bezel screws: 4 on the outer bezel
-       at 12, 3, 6, 9 o'clock. Like the luxury gauge — they hold the bezel. */
     var bezelAngles = [90, 0, 270, 180];
     for (var bi = 0; bi < bezelAngles.length; bi++){
       var ba = bezelAngles[bi] * Math.PI / 180;
```

## Code-only diff (comments stripped)

template code diff lines: 51 | numerals: 25 | ticks: 43

```diff
--- v74-code
+++ pass4-code
@@ -12,6 +12,13 @@
               '<stop offset="55%" stop-color="#7a7e88"/>' +
               '<stop offset="72%" stop-color="#8f93a0"/>' +
               '<stop offset="88%" stop-color="#b9bdc8"/>' +
+              '<stop offset="100%" stop-color="#d6d9e0"/>' +
+            '</linearGradient>' +
+            
+            '<linearGradient id="tnAluHub" x1="0%" y1="0%" x2="100%" y2="100%">' +
+              '<stop offset="0%" stop-color="#eef0f4"/>' +
+              '<stop offset="38%" stop-color="#9a9ea8"/>' +
+              '<stop offset="55%" stop-color="#7a7e88"/>' +
               '<stop offset="100%" stop-color="#d6d9e0"/>' +
             '</linearGradient>' +
             
@@ -140,7 +147,7 @@
           '<circle cx="100" cy="104" r="84" fill="#050607"/>' +
           '<circle cx="100" cy="104" r="84" fill="none" stroke="#000" stroke-width="4" opacity=".7"/>' +
           '<circle cx="100" cy="104" r="82" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="1"/>' +
-          tickLines() +
+          calcTickLines(sc) +
           
           '<path class="tn-tacho-track" d="' + ARC_D + '"/>' +
           '<path class="tn-tacho-fill" d="' + ARC_D + '" stroke="url(#tnSpectrumFlow)"/>' +
@@ -177,7 +184,7 @@
           '<circle cx="100" cy="104" r="79" fill="none" stroke="url(#mObsidian)" stroke-width="22" opacity="1"/>' +
           '<circle cx="100" cy="104" r="69" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="1"/>' +
           
-          '<g class="tn-edge-numerals">' + dialNumerals() + '</g>' +
+          '<g class="tn-edge-numerals">' + calcDialNumerals(sc) + '</g>' +
           
           '<g class="tn-tacho-mech" aria-hidden="true">' +
             '<circle cx="100" cy="104" r="30" fill="url(#mCavity)"/>' +
@@ -231,6 +238,7 @@
           '<rect x="87" y="173" width="26" height="3" rx="1.5" fill="rgba(0,0,0,.7)"/>' +
           '<rect x="87" y="182" width="26" height="1.5" rx=".75" fill="rgba(255,255,255,.08)"/>' +
           '<text class="tn-tacho-svgnum" x="100" y="183" text-anchor="middle" style="font-size:8px;font-family:Georgia,serif;">…</text>' +
+          
           '' +
           
           '<path d="M 148 130 A 56 56 0 0 1 152 142" stroke="#a06bff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>' +
@@ -249,7 +257,7 @@
         '<div class="tn-tacho-truth" hidden></div>' +
       '</div>' +
       
-      '<div class="tn-tacho-bandline"></div>' +
+      '<div class="tn-tacho-lapline" hidden></div>' +
       
       
       '<div class="tn-tacho-cap" hidden></div>' +
```

```diff
--- v74-code
+++ pass4-code
@@ -1,17 +1,16 @@
-  function dialNumerals(){
+  function calcDialNumerals(sc){
     
     var h = '', i;
-    var vals = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000];
+    var vals = [];
+    for (i = 0; i <= 10; i++) vals.push(sc.max * i / 10);
     for (i = 0; i < vals.length; i++){
       var val = vals[i];
-      var label = (val === 0) ? '$0' : '$' + (val/1000) + 'K';
-      var angleDeg = 135 + (val/10000)*270;
+      var label = calcLabel(sc, val);
+      var angleDeg = 135 + (val / sc.max) * 270;
       var angle = angleDeg * Math.PI / 180;
       var x = 100 + 79 * Math.cos(angle);
       var y = 104 + 79 * Math.sin(angle);
-      
       h += '<text x="' + (x+0.9).toFixed(1) + '" y="' + (y+3.4).toFixed(1) + '" text-anchor="middle" class="tn-dial-num-shadow">' + label + '</text>';
-      
       h += '<text x="' + x.toFixed(1) + '" y="' + (y+2.3).toFixed(1) + '" text-anchor="middle" class="tn-dial-num">' + label + '</text>';
     }
     return h;
```

```diff
--- v74-code
+++ pass4-code
@@ -1,10 +1,10 @@
-  function tickLines(){
+  function calcTickLines(sc){
     
     var h = '', v, rad;
-    
-    for (v = 10; v < 500; v += 10){
-      if (v % 50 === 0) continue;
-      var angleDeg = 135 + (v/500)*270;
+    var step = sc.max / 50, major = sc.max / 10;
+    for (v = step; v < sc.max; v += step){
+      if (Math.abs(v % major) < 1e-9) continue;
+      var angleDeg = 135 + (v / sc.max) * 270;
       rad = angleDeg * Math.PI / 180;
       var rr1 = 78, rr2 = 86;
       var sw = 2.5;
@@ -15,24 +15,18 @@
            '" y2="' + (104 + rr2 * Math.sin(rad)).toFixed(1) +
            '" stroke="#ffffff" stroke-width="' + sw + '" opacity="' + op + '"/>';
     }
-    
-    
     var screwAngles = [45, 135, 225, 315];
     for (var si = 0; si < screwAngles.length; si++){
       var sa = screwAngles[si] * Math.PI / 180;
       var sx = 100 + 58 * Math.cos(sa), sy = 104 + 58 * Math.sin(sa);
-      
       h += '<circle cx="' + sx.toFixed(1) + '" cy="' + sy.toFixed(1) + '" r="4" class="tn-dial-screw"/>';
-      
       var slotA = (screwAngles[si] * 1.7) * Math.PI / 180;
       var x1 = sx + 2.8 * Math.cos(slotA), y1 = sy + 2.8 * Math.sin(slotA);
       var x2 = sx - 2.8 * Math.cos(slotA), y2 = sy - 2.8 * Math.sin(slotA);
       h += '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) +
            '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" class="tn-dial-screw-slot"/>';
-      
       h += '<circle cx="' + (sx-1).toFixed(1) + '" cy="' + (sy-1).toFixed(1) + '" r="1.2" fill="rgba(255,255,255,.3)"/>';
     }
-    
     var bezelAngles = [90, 0, 270, 180];
     for (var bi = 0; bi < bezelAngles.length; bi++){
       var ba = bezelAngles[bi] * Math.PI / 180;
```

## Allowed-difference audit

Every differing line matches an allowed pattern (parameterization or a documented retention). No unexplained differences — PASS.

## What the compare proves

- The dial SVG body (defs, gears, needle, hub, crystal, accent arc, chapter ring, screws) is byte-identical to v74 except the enumerated lines.
- The purple jewel (mRuby), purple spectrum, purple accent arc are the v74 values, restored — not the dashboard gold.
- The dial numerals/ticks read the stat's OWN scale (counts / % / $), never a copied $0–$10K — per Shawn's 21:50Z amendment.
- `mountMiniCalc` is the only live mini mounter: 10 drill sites + `_osMountSlMinis` (link cells + board cells + Reports cells). The old `mountMini` survives only as the fallback in `_osMountSlMinis` and in the disabled orb-upgrade code path.
