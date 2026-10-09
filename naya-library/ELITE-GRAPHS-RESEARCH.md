# ELITE GRAPHS — Reinventing the Bar, the Line, the Pie, the Scatter

Research mission from Shawn (2026-10-09): *"Look up the most elite level visual presentations of data stats, graphs — not basic shit. Bars, pies, all the different things, reinvented into something out of this world. Holographic if doable."*

This document answers: who is reinventing standard charts today, how they do it, whether true holography works in a browser, and what NayaNET's five reinvented chart types should be.

---

## PART 1 — The practitioners reinventing charts right now

### 1. Nadieh Bremer — the form inventor
Co-author of *Data Sketches* (with Shirley Wu): 24 projects, each inventing a new visual form for its dataset rather than reaching for a default chart. Her signature move: start from the data's shape, not the chart menu. Known for astronomical/radial forms, d3.js craftsmanship, and proving that "uncommon chart types communicate nuance." Her book *Chart* (new) structures work on a spectrum from straightforward charts to full data art.
**Steal:** never start from the chart type — start from what the data wants to be. Our orbital pie came from this instinct.
→ https://www.visualcinnamon.com/

### 2. Shirley Wu — the explorer
Co-author of *Data Sketches*. Abuses d3's force-directed layouts to make complex systems (network security product data) feel simple and touchable. Her work is *explorable explanations* — the chart is an instrument you play, not a picture you read.
**Steal:** charts as instruments. Hover isn't decoration — it's the primary reading mode.
→ https://shirleywu.studio/

### 3. Moritz Stefaner — truthful beauty
"Truth and Beauty" operator. Built the 500-topic neuroscience semantic map for The Transmitter (350,000 abstracts, type size = volume, color = recency trend). Co-created Data Cuisine (edible diagrams — won the Information is Beautiful top honor). His rule: beauty must never outrun honesty.
**Steal:** the honesty constraint. Every beautiful effect must encode a real value. If it doesn't, cut it.
→ https://truth-and-beauty.net/

### 4. Federica Fragapane — visual alphabets
Award-winning information designer (UN, BBC, Wired, Google's "Shape of Dreams"). Designs *visual alphabets* — a consistent mark-language per project — before drawing any chart. Emotion and empathy are design inputs, not accidents.
**Steal:** our spectrum law IS a visual alphabet. Every chart must speak it fluently, not decorate with it.
→ https://federicafragapane.com/

### 5. Giorgia Lupi — Dear Data
With Stefanie Posavec, spent a year hand-drawing personal data postcards. Proved that the *human hand* in data creates connection no algorithm reaches. Now at Pentagram; her data-humanism argues numbers are always about people.
**Steal:** restraint + humanity. Our charts should feel made *for* someone, not generated *at* them.
→ http://www.dear-data.com/

### 6. David McCandless — Information is Beautiful
The popularizer. *Knowledge is Beautiful*, *Information is Beautiful*. His gift: finding the one visual metaphor that makes a complex dataset instantly legible (his famous "who's hot in the universe" style hierarchies).
**Steal:** the single-metaphor discipline. One chart, one idea, instantly readable.
→ https://informationisbeautiful.net/

### 7. NYT Graphics — the restraint masters
38 Malofiej awards (the Oscars of infographics). Their ten rules include: visual restraint (right color, catch the eye, immediate recognition), clarity of question before clarity of chart, and "50% of the work is sweating the details." Their climate scrollytelling uses 3D AR rainfall comparisons — real data, cinematic presentation.
**Steal:** restraint as a weapon. And scrollytelling's lesson: reveal data in narrative order, not all at once.
→ https://www.nytimes.com/spotlight/graphics

### 8. Reuters Graphics — dark precision
Their 2026 economics package: paired line charts on dark navy, each pair telling one story (inflation vs wage growth, unemployment vs consumer sentiment). Dark ground, disciplined color, let the lines argue with each other.
**Steal:** dark ground + paired series that *argue*. Our spectrum bands do this.
→ https://www.reuters.com/graphics/

### 9. Pew Research — the alluvial masters
Their 2025 showcase: alluvial/Sankey diagrams showing *how* composition shifted (not just that it shifted) — e.g., the American electorate 2020→2024. Flows between bars carry the story.
**Steal:** flows carry change. Static bars show state; moving flows show story.
→ https://www.pewresearch.org/short-reads/2025/12/15/our-favorite-data-visualizations-of-2025/

### 10. Block and Paper — the 3D bar chart, done right
Dated every structure in 100 cities; each city opens as a field of 3D blocks on a map, one per building footprint, colored by decade. Press play and buildings *rise* in the year they were finished. A bar chart you can walk through.
**Steal:** the bar chart as *architecture*. Height = value, and time animates the construction. This is the closest anyone has come to our light columns.
→ Block and Paper studio site

### 11. USAFacts — the Fast Company winner
Interactive Sankey showing how (and where) federal money flows. Won Fast Company's 2025 data design top honor. Proof that flow diagrams, done with total clarity, beat every dashboard.
**Steal:** clarity wins awards, not complexity.
→ https://usafacts.org/

### 12. Spotify Wrapped — the viral proof
Year-end personal data review. Won a Webby People's Voice for Best Data Visualization. The lesson: *personal* data, beautifully packaged, is the most shareable thing on earth. People don't share charts — they share *themselves, beautifully measured*.
**Steal:** this is the entire Smart Stats thesis. "Give me the stats on me" must feel like Wrapped × a supercomputer.
→ (in-app; cultural reference)

### 13. Randall Munroe — the timeline that won gold
His Earth Temperature Timeline (ice age → now) won gold at the Information is Beautiful Awards. One line, 20,000 years, the entire climate story. Proof that a single perfect line beats a hundred clever ones.
**Steal:** the single-line discipline. Our Current must earn every pixel of its path.

### 14. The wind-map lineage (Agafonkin → earth.nullschool)
Thousands of GPU particles advected through real wind fields. Technical crown jewels: screen-accumulation buffers (long tails for free), drop-rate density correction, hand-rolled bilinear interpolation. Data as weather, running at 60fps in a browser.
**Steal:** already in our Tidal Field. For charts: particle *trails* behind moving values.
→ https://earth.nullschool.net/

### 15. The metallica project (GitHub, 2026) — the holographic dashboard, actually built
A holographic AI assistant interface in real-time WebGL: pulsing core, GPU particles, spatial HUD, and **10 spec-driven 3D data visualizations** — gauges, radar sweep, waveform, network graph, **3D line/bar charts**, globe, timeline, sankey flow. Built with React Three Fiber, fresnel hologram shaders, bloom + god rays + chromatic aberration post-processing. This is the closest thing on Earth to what Shawn described: a supercomputer interface outputting real data visualizations as holograms.
**Steal:** the *stack* (three.js + custom GLSL + post-processing) and the proof it's shippable. But note its aesthetic is cyberpunk-maximalist — we take the technique, not the taste.
→ https://github.com/hiennguyen0205/metallica

---

## PART 2 — The technique catalog (how the effects are actually built)

### A. Bars with physics
- **Spring easing, not linear tweening.** Bars grow with spring physics (stiffness/damping) — they *arrive* instead of sliding. Implementation: per-bar spring integrator in the render loop, or CSS `cubic-bezier(.22,1,.36,1)` approximations.
- **Staggered ignition.** Bars ignite left-to-right with 60–90ms stagger. The eye reads the sequence as a story.
- **Value-first labels.** The number materializes *after* the bar lands (150ms delay) — cause, then effect.
- **Glass floor.** A vertical gradient reflection under each bar (canvas: `globalAlpha` gradient flip, or CSS `-webkit-box-reflect`). Sells the "standing object" feeling for free.

### B. Lines as light/energy
- **The line is a stroke with a soul.** Draw the path 3 times: wide low-alpha glow pass, medium mid-alpha pass, thin bright core pass. That's the entire "energy line" trick — no shaders needed.
- **Gradient along the path.** Canvas can't gradient-stroke a path natively; technique: draw the line as many small segments, each stroked with its interpolated color. 200 segments = smooth spectrum flow.
- **The comet head.** A bright dot with radial glow travels the line on loop (or on data update), leaving a fading trail. The line feels *alive* because something is moving along it.
- **Area as mist.** Fill under the line with a vertical gradient (color → transparent), very low alpha. Depth without weight.

### C. Pies as orbits (killing the pie)
- The pie's problem: angles are hard to compare. The fix isn't a better pie — it's a different metaphor. Segments become **bodies in orbit**: area = share (body size), orbit radius fixed, orbit *speed* = rate of change. The whole is the center; the parts circle it. Comparison becomes "which body is biggest" — trivially readable.
- **Donut > pie, always.** The center hole holds the total — the number the pie was trying to say.

### D. Scatter as a field
- Points are stars; **clusters get nebula glow** (radial gradient behind dense regions, computed by simple grid density).
- **Correlation as a light beam:** least-squares regression line drawn as a beam of light through the cloud — the insight literally illuminates.
- Hover: the point ignites, its coordinates materialize, connected points (same category) brighten.

### E. Multi-series as spectrum bands
- Horizon-chart logic: each series is a translucent band, layered in spectrum order, y-offset stacked with slight overlap. Peaks align vertically = instant cross-series reading.
- **One accent rule:** all bands muted except the hovered/selected one, which goes full-bright. Attention is a spotlight.

### F. The holographic language (flat-screen edition)
True holography needs hardware (see Part 3). On a flat screen, the *language* of holography is:
1. **Depth slices** — the same visual on 2–3 planes with parallax offset on cursor move (we built this in the dial).
2. **Fresnel rims** — edges brighter than centers (radial gradients do this in canvas 2D).
3. **Scanline interference** — 1px horizontal lines at 3–6% alpha over the visual. Instant "projection" feeling.
4. **Bloom-as-energy** — the brightest data points get a soft glow; glow = energy = importance.
5. **Chromatic edge** — on motion only, offset red/blue copies by 1px. (Use sparingly — this is where carnival starts.)

---

## PART 3 — Holographic feasibility verdict

**True holography (light-field, volumetric):** NOT doable in a standard browser. Requires hardware: Looking Glass light-field displays, Light Field Lab's SolidLight panels, or spinning-LED walls (Hypervsn). No DOM API projects photons into air.

**What's fully doable in-browser today:**
- **Real 3D charts** via three.js/WebGL: 3D bars, 3D lines, extruded pies, point clouds — rotatable, lit, shadowed. The metallica project proves 10 viz types ship this way. Cost: ~600KB–1MB of library, GPU required, and 3D often *hurts* readability (the classic dataviz warning: "avoid 3D charts" exists because 3D usually adds ink without information).
- **The holographic *language*** (Part 2F): depth slices, fresnel rims, scanlines, bloom, parallax — all in canvas 2D or CSS. This is what we already do, and it's the right call: it reads as "hologram" without the readability tax of true 3D.
- **WebGPU** (deck.gl now targets it): 10–100× the particles of WebGL for flow fields. Overkill for charts; right for our Tidal Field's future.

**Recommended stack for NayaNET charts:** **Canvas 2D + hand-rolled techniques.** Reasons: (1) the dial — our beauty bar — is canvas 2D; (2) zero dependencies, instant load, works everywhere; (3) restraint is easier when the tool doesn't tempt spectacle; (4) every technique in Part 2 is implementable in ~50 lines of canvas each. Graduate to three.js only for a dedicated 3D instrument later — never as the default.

**Verdict for Shawn:** holographic *hardware* — no. Holographic *feeling* — yes, and we're already doing it. True 3D charts — doable but usually worse; skip unless a specific instrument demands it.

---

## PART 4 — The 5 reinvented NayaNET chart types (built in lego/elite-graphs.html)

### 1. LIGHT COLUMNS (the bar chart, reinvented)
Bars as rising columns of light on black glass. Each column: dark obsidian body, hairline spectrum edge, bright cap where the value lands, glass-floor reflection, value materializing above after landing. Spring-physics growth, staggered ignition. Color by rank in spectrum order (tallest = magenta... or by meaning). The axis is a whisper — hairline grid, tiny labels.
*Data shown:* NayaPOWER engine area scores, 0–10 (real scorecard).

### 2. THE CURRENT (the line chart, reinvented)
The line as a river of light flowing left→right. Three passes (glow/mid/core), spectrum gradient along the path, a comet head traveling it forever, area-under as faint mist. Data points as small stars that ignite on hover with exact values. Time *flows* — the chart never sits still, but never distracts.
*Data shown:* world population by decade 1960–2025, billions (UN WPP 2024, rounded).

### 3. ORBITAL SHARES (the pie chart, reinvented)
No pie. The total sits at center as a dark sphere with the number; each share is a body in orbit — body size = share, orbit speed = rate of change, spectrum color = category. Hover a body: it ignites, its share/%/value materialize. The whole and the parts, in motion, instantly comparable.
*Data shown:* NayaPOWER scorecard weights — the 10 areas' share of the total score (real, sums to 100%).

### 4. THE FIELD (the scatter plot, reinvented)
Points as stars on black; dense clusters grow nebula glow (grid-density); the least-squares correlation beam shines through the cloud; hover ignites a star and reveals its coordinates; same-category stars brighten together. Correlation you can *see* as light.
*Data shown:* the 10 engine areas — x = weight (%), y = score (/10). Real. The beam answers: "does importance predict score?"

### 5. SPECTRUM BANDS (the multi-series chart, reinvented)
Three translucent bands in spectrum order, layered with slight overlap like geological strata — score, weight, and weighted contribution across the 10 areas. Hover a band: it goes full-bright, others dim to whispers; the hovered area's three values materialize. Cross-series comparison by vertical alignment.
*Data shown:* the 10 engine areas × 3 normalized series (real scorecard math).

---

## Design law for all five
Black ground `#040405`. Spectrum in law order. Restrained like the dial — thin lines, small precise type, vast black space, one accent at a time. Every number readable. Every effect encodes a value (Moritz Stefaner's rule). If it doesn't carry information, it's cut. These are instruments, not decoration.
