# HOLO-RESEARCH — The Most Incredible Data Presentations on Earth (and Beyond)

Research mission: find the most stunning high-tech, holographic, 3D presentations of data ever made — and design our own invented mix. Written 2026-10-09 for the Naya Lego Library.

## The 10 Most Stunning Examples

### 1. NASA "Eyes" Suite (JPL) — space as a living instrument
Real NASA mission data rendered as explorable 3D worlds: Eyes on the Solar System, Eyes on the Earth, Deep Space Network Now. Built for mission teams first, released to the public. You fly through real spacecraft positions in real time.
**Steal:** trust in real data + the feeling of piloting an instrument, not reading a page. Time as a scrubber (1950–2050 data). Live telemetry as starlight.
→ https://www.jpl.nasa.gov/apps/

### 2. Territory Studio screen graphics (Iron Man, Guardians, The Martian, Avengers)
The studio that invented modern sci-fi HUDs. Their rule: every screen must be *readable at a glance* even when alien — viewers deduce each screen's job without understanding its controls. For Guardians they avoided symmetry and all familiar conventions to feel otherworldly. For The Martian they researched real glove-touch operation.
**Steal:** icons speak, text whispers. Every element has a *job* you read instantly. Deliberate asymmetry for the extraordinary. Restraint in the familiar, invention in the new.
→ https://gizmodo.com/inside-the-wild-ui-design-of-guardians-of-the-galaxy-1623829439

### 3. teamLab "Crystal Universe" — infinite light points
Seemingly endless light points forming a 3D space you walk inside; visitors reshape it with their phones. Dark entryways compress the senses before expansive rooms release them — a spiritual journey from limitation to awakening.
**Steal:** the *scale shift* — compression then release. Data that surrounds you, not data you look at. Darkness as a design material (black ground is sacred).
→ https://www.teamlab.art/ (Crystal Universe, Planets TOKYO)

### 4. Wind maps (Agafonkin's earth.nullschool / cambecc/earth lineage)
Thousands of GPU particles advected through real wind fields — data as weather. Key technical insights from the lineage: screen-accumulation buffers give long tails for free; drop-rate bumps correct density so fast wind doesn't look denser; bilinear interpolation of coarse grids by hand beats hardware-linear.
**Steal:** the Tidal Field is already this. Go further: particles that *carry numbers*, streams whose width = volume, currents colored by meaning.
→ https://github.com/stergiotis/boxer/blob/HEAD/doc/adr-background-work/vector-field-flow-visualization-survey.md

### 5. Audio-reactive visualizers (Cymatica, VyzFlow, ISF shaders)
Music visualizers solved "make numbers feel alive" years ago: dual-core engines (fast rhythm path + deep texture path), GLSL vertex displacement driven by data, bloom + chromatic aberration + glow post-processing, debris fields that expand/rotate/shift color with intensity.
**Steal:** the dual-path idea — a fast path (immediate response, kicks/snares) and a deep path (texture, harmonics). Our data pulses should work the same: instant value response + slow character response. Bloom is not decoration; it's *energy made visible*.
→ https://github.com/aayushmanmk/cymatica-engine

### 6. Looking Glass / Light Field Lab — true holography
Glasses-free light-field displays: the Looking Glass 8K reproduces directionality of every light ray; Light Field Lab's SolidLight projects objects "indistinguishable from reality." No headsets.
**Steal (on flat screens):** the *visual language* of holography — scanline interference, depth slices, parallax between layers. What we render now trains the eye for when the hardware arrives.
→ https://medium.com/through-the-looking-glass/colossal-holograms-b7f86f5925bd

### 7. DARPA UPSD — the holographic sandtable
A real, built, 360° full-parallax 3D planning table for urban battle data — freeze, rotate, zoom, 20 simultaneous viewers. Full parallax: correct light in every direction.
**Steal:** data as a *table you gather around*. Our constellation + orbital views are one step from this. Think multi-user later.
→ https://www.spacedaily.com/reports/DARPA_Successfully_Completes_3D_Holographic_Display_Technology_Demonstration_Program_999.html

### 8. Hypervsn at Sphere Las Vegas — 420 units, 9×15m floating image
The largest holographic wall ever built: 420 synchronized spinning-LED blades forming one cohesive floating image. Pure spectacle, but the lesson is *synchronization* — hundreds of independent units moving as one organism.
**Steal:** our instruments should feel like one organism — when a query resolves, every module reacts together.
→ https://www.avinteractive.com/markets-news/venues/hypervsns-largest-ever-holographic-display-seen-at-sphere-03-10-2023/

### 9. High-end watch dials (haute horlogerie)
The most beautiful data instruments ever made by humans: guilloche patterns, moon phases, tourbillons. Rules from the craft: legibility is sacred, materials matter, the dial's *texture* is the message, target zones beat raw numbers.
**Steal:** this is the DNA of the ±9 gauge below. A data instrument should feel like a ten-thousand-dollar object.
→ (design reference; see gauge design section)

### 10. Cornell dynamic-display ergonomics (the science of reading instruments)
Preferred: dark background + light numbers (validates black ground). Moving pointer on fixed scale (not the reverse). Semi-circular/circular displays preferred over linear where possible. Target zones faster than raw values.
**Steal:** these are machine-checked laws for our gauge: fixed dial, moving light, zone-marked ±9.
→ https://ergo.human.cornell.edu/DEA3250Flipbook/DEA3250notes/dyndisplay.html

---

## Techniques Worth Stealing (concrete)

1. **Screen-accumulation buffer for trails** — fade previous frame instead of clearing; zero-cost particle tails. (Already used in our Tidal Field; extend to the gauge.)
2. **Dual-path reactivity** — fast path (instant value changes) + deep path (slow character/momentum). From music visualizers.
3. **Depth-slice parallax** — 2–3 ghost layers of the same graphic at different depths, drifting apart with cursor. Cheap holography on flat screens.
4. **Bloom as energy** — additive glow whose intensity = data magnitude. Not decoration; information.
5. **Chromatic aberration on motion** — slight RGB split on fast-moving elements sells speed and light.
6. **Drop-rate density correction** — in flow fields, raise reset probability with speed so fast data doesn't look denser. (From wind-map lineage.)
7. **Bilinear hand-interpolation** — when rendering from coarse grids, interpolate manually for smoothness.
8. **Compression → release pacing** — dark tight entry, then expansive reveal. From teamLab. Our boot sequence should do this.
9. **Icon-first, text-last** — Territory Studio rule: every element's job must be readable at a glance.
10. **Fixed scale, moving light** — the gauge needle should be light, the dial should be machined. (Ergonomics law.)

---

## The ±9 Circular 4D Gauge — Design Proposal

**Shawn's concept:** a chart where below the line is −9, above is +9, the line itself is 0. Not hard limits — values run to ±infinity — but ±9 gives visual structure: a center point, an average zone, a beautiful visual. Make it circular: a 4D grid in the middle extending in width and depth. It becomes a *calculator* — a visual instrument for measuring anything on a −9..+9 scale with infinite range beyond.

### What it is
**THE NAYA DIAL.** A circular instrument — part compass, part radar, part haute-horlogerie watch dial — that measures any scored metric. Every score in the Naya system (design calculator scores, value calculus, engine 10/10 scores, Smart Stats magnitudes) flows through one universal instrument.

### Anatomy
- **The Zero Ring** — the horizontal center line, bent into a circle. A machined ring at radius R₀. This is the datum of the universe: everything is measured *from* this ring.
- **The +9 / −9 arcs** — above the ring: positive territory, +1..+9, colored green→gold (achievement). Below: negative territory, −1..−9, colored magenta→purple (creation energy / warning, per spectrum meaning). Ticks at each integer, machined like a watch crown.
- **The 4D grid** — in the middle of the dial, a perspective grid extending in width (x) and depth (z), faintly glowing, receding toward a vanishing point *behind* the dial. Time (the 4th dimension) animates it: the grid breathes, pulses flow along its lines from past (edges) to present (center). You look *into* the measurement.
- **The needle of light** — not a physical needle: a beam of light that sweeps to the value. Moving light on a fixed scale (ergonomics law). Its glow intensity = |value|.
- **The reading** — the number, floating at center over the grid, in white. Breathes gently.

### Behavior at extreme values
- **Within ±9:** the needle points to the tick. Normal, beautiful, precise.
- **Beyond ±9 (to ±infinity):** the needle *pins* at the ±9 stop — and the dial responds: the arc beyond the stop ignites. A comet trail extends past the tick, its length growing logarithmically with the overshoot (log scale keeps infinity displayable). The ring itself brightens; at |v| > 18 (2× range), the whole dial shifts hue toward white-hot. You *feel* the excess without breaking the instrument.
- **Logarithmic overflow:** displayed_overflow = log₂(|v|/9) extra ring-segments lit. Infinity becomes "more rings," never a broken needle.
- **History:** a fading trail of past readings ghosts behind the needle — the last 12 readings as dimmer echoes. The dial remembers.

### Why circular, why ±9
- Circular = no dead ends, no "off the chart." Infinity wraps as intensity, not as an edge.
- ±9 = Shawn's natural scale (9.0 is the floor, 10 is the horizon). The gauge and the scoring law share a number — the instrument *is* the philosophy made physical.
- The 4D grid in the middle makes it a *calculator*: you don't just read a value, you see it *in context* — width (breadth of evidence), depth (confidence), time (momentum). One glance tells you value, confidence, and direction.

### Specimen data mapping (example)
Query "give me the stats on my design system": design calculator score 98 → normalized to the dial as +8.8 (elite zone, green→gold arc). Momentum +2.3 → needle leans forward with a comet trail. Confidence (12 samples) → grid depth intensity.

### Build order
1. Static dial specimen (SVG: rings, ticks, grid, machined finish) — week 1
2. Needle-of-light + value animation — week 1
3. Log-overflow comet trails + history echoes — week 2
4. Fuse with instruments: dial as the *readout head* of the Tidal Field (wells feed dial readings) and the Orbital System (each orb gets a micro-dial on hover)

---

## Fusion Map — Which Instruments Absorb These Ideas

| Our instrument | Fuses with | Result |
|---|---|---|
| Tidal Field | Wind maps (#4) + dual-path reactivity (#2) | Wells get fast/deep response paths; particle density corrected by drop-rate bump; streams carry numbers |
| Spiral Ledger | teamLab pacing (#3) + watch dials (#9) | Compression→release reveal; guilloche-textured rings; cycle markers machined like a chronograph |
| Pulse Core | Music visualizers (#5) | FFT-style band splitting: split the pulse into bass/mid/treble-equivalent bands (volume/momentum/volatility), each driving a different visual layer |
| Orbital System | NASA Eyes (#1) + DARPA sandtable (#7) | Time scrubber; "gather around" multi-focus; real-data trust |
| Convergence Engine | Hypervsn sync (#8) | All instruments react together on query resolution — one organism |
| **NEW: The Naya Dial** | Watch dials (#9) + ergonomics (#10) + holographic depth (#6) | The universal readout head — every number in the system can surface through it |

---

*The puzzle is to understand it. The dial is understanding, made into an instrument.*
