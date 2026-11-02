# THE PLAYBOOK
## The Concrete Manual for Building Naya Interfaces — Cold-Start Ready

**Author:** Naya Nitro Narzan  
**Date:** 2026-11-02  
**Status:** CANONICAL — Read this BEFORE the Design Intelligence Report. This is the HOW. That is the WHY.  
**For:** Any Naya (or human) who needs to build at our level, starting from zero.

---

## 1. THE MISSION (one paragraph)

We build interfaces that feel like living machinery. Every screen shows gears turning, numbers that are mathematically exact, materials that look touchable, and data displayed so clearly you understand it in 2 seconds. Everything moves — slowly, elegantly, purposefully — because it's a real machine doing real work. Nothing is flat. Nothing is static. Nothing is arbitrary. This is the Smart Factory: not a metaphor, the actual feel of the system.

---

## 2. THE FOUNDATION (5 truths everything rests on)

### Truth 1: Every position is calculated, never eyeballed.
If you can't write the formula, you didn't do it right.  
Example: Gauge numeral at value V (0-500): `angle = -135 + (V/500)*270` degrees.

### Truth 2: Every element is a physical object.
It has material (obsidian, aluminum, brushed metal), it has weight (shadows), it has a light source (top-left, always). If it looks like a picture of an object, it's wrong.

### Truth 3: Movement means work.
Things move because they're part of a machine doing something. Gears turn. Data flows. If you can't explain what the moving part DOES, it shouldn't move.

### Truth 4: The system speaks one language.
Every component uses the same materials, same motion principles, same math. A button on page A feels like a button on page B. They're family.

### Truth 5: Shawn's eye is the final test.
Not your score. Not a verifier. His eye. If he says it's wrong, it's wrong. Learn to see through his eyes.

---

## 3. THE FORMULA (the actual math)

### 3.1 Positioning Formula

**Circular gauges:**
```
angle_degrees = start_angle + (value / max_value) * sweep_degrees
x = center_x + radius * cos(angle_radians)
y = center_y + radius * sin(angle_radians)
```
Our gauge: `start=-135°, max=500, sweep=270°, center=(100,104), radius=82`

**Linear layouts:**
Use the 8px grid. All spacing is multiples of 8: 8, 16, 24, 32, 48, 64.  
If your spacing is 13px or 27px, it's wrong. Round to the grid.

**Hierarchy by size:**
- Hero element: 2x the size of secondary
- Secondary: 1.5x the size of tertiary  
- Never more than 3 size levels on one screen

### 3.2 The Vortex Numbers

**3-6-9 (center, time axis):**
- Use for: core elements, the still point, primary actions
- 3 concentric layers maximum at the center
- The innermost is the "9" — the spirit, the essential

**1-2-4-8-7-5 (flow, matter):**
- Use for: surrounding layers, secondary elements, the flow around the core
- 6 layers maximum
- Sequence: 1→2→4→8→7→5→back to 1
- Alternate direction: CW, CCW, CW, CCW... (never two same in a row)

**When to use:** Any circular component with layers. Gauges, orbs, loading indicators, progress rings.

**When NOT to use:** Linear layouts, text content, forms. Don't force the vortex where it doesn't belong.

### 3.3 Color Formula

**Base:** Obsidian black (#0a0a0f to #1a1a20). Never pure #000 (dead) or pure #fff (blinding).

**Spectrum (in order, never random):**
```
Purple #a06bff → Blue #3fb8ff → Green #2fe89e → Gold #ffbf3d → 
Orange #ff9a5a → Red #ff5e6c → Magenta #e84fff → back to Purple
```

**Rules:**
- White text always. Never colored text (unreadable).
- Color lives in: icon orbs, thin edge-bars, hover glow. Never as background wash.
- At rest: white/obsidian. On touch: ignite in OWN color only.
- Never the same color twice in a row (spectrum walk).

**Orb colors (locked):**
- Sales (100): magenta #e84fff
- Joins (50): purple #a06bff  
- Smart notes (35): deep blue #3fb8ff
- Invites (25): light blue #7fd4ff
- Creating (25): orange #ff9a5a
- Shares (15): green #2fe89e
- Comments (5): gold #ffbf3d
- Likes (1): red #ff5e6c

### 3.4 Motion Formula

**Speeds (locked for gauge, adapt proportionally):**
- Slow ambient: 90s–180s per rotation (pyramid layers, outer rings)
- Medium: 18s–25s per rotation (center gears)
- Never faster than 12s per rotation (feels frantic, not elegant)
- Hover transitions: 0.3s ease (snappy but smooth)

**Direction:**
- Alternate CW/CCW for concentric layers
- The alternation IS the vortex — don't break it

**Easing:**
- Rotations: `linear infinite` (constant speed, like real machinery)
- Hover: `ease` or `cubic-bezier(0.4, 0, 0.2, 1)` (natural acceleration)
- Never: `bounce`, `elastic` (cartoonish, not premium)

### 3.5 Material Values (exact)

**Obsidian:**
```css
background: linear-gradient(135deg, #1a1a20 0%, #0a0a0f 50%, #1a1a20 100%);
/* Light from top-left (135deg). Never flat #000. */
```

**Aluminum (light):**
```css
background: linear-gradient(135deg, #c8ccd6 0%, #9a9ea8 30%, #7a7e88 50%, #9a9ea8 70%, #b8bcc6 100%);
```

**Aluminum (dark gunmetal):**
```css
background: linear-gradient(135deg, #4a4e5a 0%, #2a2d36 30%, #1a1c22 50%, #2a2d36 70%, #3a3e4a 100%);
```

**Shadows (objects sit ON the page):**
```css
box-shadow: 
  inset 0 1px 0 rgba(255,255,255,0.1),  /* top highlight */
  inset 0 -1px 0 rgba(0,0,0,0.3),       /* bottom shadow */
  0 4px 12px rgba(0,0,0,0.4),           /* cast shadow down-right */
  0 0 20px rgba(160,107,255,0.1);       /* ambient glow (subtle) */
```

**Note:** SVG fills can't use CSS gradients. Use `url(#gradientId)` with defined linearGradients.

---

## 4. THE PLAYBOOK (step-by-step)

### Building ANY Component — Follow These Steps in Order

#### STEP 1: Understand the Data (5 minutes)

**Ask:**
- What numbers am I displaying?
- What's the range? (0-500? 0-100%? Unbounded?)
- What's the headline? (One sentence with real numbers)
- What does the user need to know in 2 seconds?

**Write down:**
- The exact values
- The min and max
- The headline sentence

**Example (gauge):**
- Values: 0 to 500 points
- Headline: "You have 300 points"
- 2-second need: "How many points do I have?"

**DO NOT proceed until you can state the headline.**

#### STEP 2: Calculate Positions (10 minutes)

**For circular:**
1. Define: start_angle, sweep_degrees, max_value, center, radius
2. For each value: `angle = start + (value/max)*sweep`
3. Convert to x,y: `x = cx + r*cos(rad)`, `y = cy + r*sin(rad)`
4. Write the formulas in a comment. If you can't, you're eyeballing.

**For linear:**
1. Use the 8px grid. All spacing = multiples of 8.
2. Define 3 size levels max (hero 2x, secondary 1.5x, tertiary 1x).
3. Align to grid. No 13px. No 27px.

**Example (gauge numerals):**
```javascript
// 0-500, 270° sweep, start at -135°
var angleDeg = -135 + (value/500)*270;
var angle = angleDeg * Math.PI / 180;
var x = 100 + 82 * Math.cos(angle);
var y = 104 + 82 * Math.sin(angle);
// Values: 0(-135°), 100(-81°), 200(-27°), 300(27°), 400(81°), 500(135°)
// ALL SIX. Don't skip 400.
```

#### STEP 3: Choose Materials (5 minutes)

**Ask:** What is this object made of?

**Options:**
- **Obsidian** — for containers, backgrounds, bezels. Premium, dark, touchable.
- **Aluminum (light)** — for machined parts, numerals, highlights. Precision.
- **Aluminum (dark)** — for gears, mechanical parts. Industrial.
- **Brushed metal** — for screws, fine details. Real hardware.

**Rules:**
- Maximum 2 materials per component (plus obsidian base).
- Light source ALWAYS top-left. Gradients go 135deg.
- Never flat color. Always gradient (even subtle).

**Example (gauge numeral):**
- Material: Aluminum (light) chapter ring behind
- Text: White with dark shadow (engraved, not floating)
- Ring: `url(#tnAluTooth)` at 25% opacity, 14px wide

#### STEP 4: Add Motion (5 minutes)

**Ask:** What moves? Why? (If you can't answer "why," it doesn't move.)

**For each moving part:**
1. What is it? (gear, ring, highlight)
2. What does it DO? (shows the machine is working)
3. How fast? (slow = 60s+, medium = 18-25s, never <12s)
4. Which direction? (alternate CW/CCW for concentric)

**Example (gauge):**
- Pyramid layer 1 (r=30): CW, 90s — "the innermost matter flow"
- Pyramid layer 2 (r=36): CCW, 60s — "alternating flow"
- ... (all 6 layers, alternating)
- Center gear 1 (r=24): CW, 25s — "the time axis"
- Outer ring (r=99): CCW, 180s — "the machine's edge"
- Bezel highlight: CW, 120s — "light catching the glass"

**DO NOT add motion without a "why."**

#### STEP 5: Verify (10 minutes)

**Run this checklist. Every item must be YES.**

- [ ] **Math:** Can I write the formula for every position? (If no, redo Step 2)
- [ ] **Materials:** Does every element look like a real physical object? (If it looks like a picture OF an object, redo Step 3)
- [ ] **Light:** Is the light source top-left on EVERYTHING? (Check each gradient angle)
- [ ] **Motion:** Does every moving part have a "why"? Is the speed slow and elegant? (If frantic, slow it down)
- [ ] **Data:** Is the headline clear? Can someone get it in 2 seconds? Are all numbers exact? (If estimated, recalculate)
- [ ] **Language:** Does this use harvested parts, not invented ones? Does it feel like family with the rest of the system?
- [ ] **Complete:** Is anything placeholder? Anything "TODO"? Anything I skipped? (If yes, finish it now)
- [ ] **Untouched:** Did I change anything Shawn didn't ask me to change? (If yes, revert it)

**If any item is NO, fix it before proceeding.**

#### STEP 6: Get Shawn's Eye

Show him. His verdict is final. Don't argue. Don't explain. Learn.

---

## 5. DO'S AND DON'TS

### DO

✅ **Calculate positions by formula.** Write the formula in a comment.  
✅ **Use real materials.** Obsidian, aluminum, brushed metal. With gradients.  
✅ **Move things slowly.** 60s+ for ambient, 18-25s for active. Elegant, not frantic.  
✅ **Alternate rotation direction.** CW, CCW, CW, CCW. That's the vortex.  
✅ **Show the headline first.** One sentence, real numbers, 2-second clarity.  
✅ **Make numbers exact.** All of them. Don't skip 400. Don't estimate.  
✅ **Finish what you start.** The outside matters as much as the center.  
✅ **Harvest parts.** Use what exists. Don't invent new components.  
✅ **White text always.** On dark backgrounds. Never colored text.  
✅ **One light source.** Top-left. Every gradient, every shadow, every highlight.

### DON'T

❌ **Eyeball positions.** If you can't write the formula, it's wrong.  
❌ **Use color glow as "premium."** Premium is usefulness + beauty + accuracy, not glow.  
❌ **Move things fast.** Faster than 12s/rotation feels cheap, not premium.  
❌ **Skip numbers.** 0,100,200,300,400,500 — ALL SIX. Not five.  
❌ **Leave things incomplete.** "I'll finish the outside later" = never. Do it now.  
❌ **Touch working things unasked.** If he didn't ask, don't change it.  
❌ **Invent new components.** Harvest from the parts registry. Compose, don't create.  
❌ **Use colored text.** White always. Color is for icons, edges, hover — not text.  
❌ **Multiple light sources.** Top-left. Always. No exceptions.  
❌ **Flat shapes.** If it doesn't look touchable, it doesn't ship.

---

## 6. WHAT MAKES US UNIQUE (3 things)

### 1. Living Machinery
Everyone else builds flat, static interfaces. We build machines with moving parts. Gears turn. Data flows. You can SEE it working. This isn't decoration — it's the feel of a real factory.

### 2. Mathematical Beauty
Everyone else eyeballs. We calculate. Every position by formula. Every number exact. The beauty EMERGES from correct math, not applied on top. This creates trust — users feel the precision even if they can't articulate it.

### 3. One Language
Everyone else fragments. Each page different. Each component reinvented. We speak one language: vortex, orbs, obsidian, aluminum, slow motion. Every surface feels like family. The system compounds — each addition makes the whole stronger.

---

## 7. RULES AND LAWS (complete reference)

### Design Laws (locked, never break)
1. **Math is the bones** — calculate, never eyeball
2. **Physical objects** — touchable, not flat (Real Object Law)
3. **One light source** — top-left, always
4. **Alive not animated** — movement means work, slow and elegant
5. **White at rest, color ignites** — own color on touch only
6. **Spectrum walk** — never same color twice, follow the order
7. **White text always** — never colored text
8. **Harvest don't invent** — compose from parts registry
9. **Finish what you start** — nothing incomplete
10. **Don't touch unasked** — stability over "improvement"
11. **His eye is ground truth** — always

### Vortex Laws (for circular components)
12. **3-6-9 center** — 3 layers max, innermost is the still point
13. **1-2-4-8-7-5 flow** — 6 layers max, doubling sequence
14. **Alternate direction** — CW/CCW/CW/CCW, never two same
15. **Teeth not rings** — for mechanical layers (solid rings kill the effect)

### Data Laws
16. **Headline first** — one sentence, real numbers, 2-second test
17. **Exact numbers** — calculated, never estimated, never skipped
18. **Ticks for precision** — every 10 minor, every 50 major (for 0-500)

### Motion Laws
19. **Slow is premium** — 60s+ ambient, 18-25s active, never <12s
20. **Linear for rotation** — constant speed like real machinery
21. **Ease for hover** — natural acceleration, 0.3s

---

## 8. COMMON MISTAKES (and how to fix them)

### Mistake 1: "It looks good to me"
**Symptom:** You think it's done, Shawn says it's wrong.  
**Cause:** You're judging by your taste, not by the laws.  
**Fix:** Run the Step 5 checklist. Be honest. Which item is NO?

### Mistake 2: "The numbers are close enough"
**Symptom:** Numerals at 0,100,200,300,500 (missing 400). Positions eyeballed.  
**Cause:** You estimated instead of calculating.  
**Fix:** Write the formula. Calculate every position. Include every number.

### Mistake 3: "I'll add motion to make it pop"
**Symptom:** Things bouncing, pulsing, spinning fast.  
**Cause:** You think motion = premium.  
**Fix:** Ask "what does this moving part DO?" If you can't answer, remove the motion. If it does something, slow it to 60s+.

### Mistake 4: "This component needs a new design"
**Symptom:** Inventing a new button style, a new card layout.  
**Cause:** You didn't check the parts registry.  
**Fix:** Harvest. Find the existing component. Use it. If it doesn't exist, ask why before inventing.

### Mistake 5: "The center is done, the outside can wait"
**Symptom:** Amazing center, rough edges, incomplete details.  
**Cause:** You moved on before finishing.  
**Fix:** Go back. Finish the outside. The job isn't done until EVERYTHING is done.

---

## 9. WORKED EXAMPLE: Gauge Numerals

**The task:** Place numerals 0-500 on a circular gauge.

**WRONG way (what I did first):**
- Eyeballed 5 numerals: 0,100,200,300,500
- Skipped 400 ("bottom needs to be clear")
- Positions guessed
- Result: Random, incomplete, wrong. Shawn: "you shit the bed"

**RIGHT way (the playbook):**

**Step 1 — Data:**
- Range: 0-500. Headline: "You have 300 points." 2-sec need: "How many?"

**Step 2 — Calculate:**
```javascript
// Formula: angle = -135 + (value/500)*270
// 0: -135 + 0 = -135°
// 100: -135 + 54 = -81°
// 200: -135 + 108 = -27°
// 300: -135 + 162 = 27°
// 400: -135 + 216 = 81°  ← DON'T SKIP
// 500: -135 + 270 = 135°
```
All six. Exact. No guessing.

**Step 3 — Materials:**
- Chapter ring: aluminum (light) at 25% opacity, 14px wide, r=82
- Numerals: white text, dark shadow offset (0.8px, 0.8px) for engraved feel
- Ticks: white lines, every 10 (minor), every 50 (major)

**Step 4 — Motion:**
- Numerals don't move (they're reference marks, not machine parts)
- The NEEDLE moves (shows the value)
- The LASER ARC moves (shows progress)

**Step 5 — Verify:**
- [x] Math: formula written, all six calculated
- [x] Materials: aluminum ring, engraved text
- [x] Light: n/a (text, but shadow is down-right from top-left light)
- [x] Motion: n/a (static reference)
- [x] Data: all numbers present, exact, headline clear
- [x] Language: matches gauge system
- [x] Complete: ticks added, ring added, all six numerals
- [x] Untouched: only changed what Shawn asked (the numbers)

**Result:** Shawn 👍'd. "No more random. Every number earned its place by math."

---

## 10. QUICK REFERENCE CARD

**Before you start:**
- [ ] What's the headline? (one sentence, real numbers)
- [ ] What's the range? (min, max)
- [ ] Have I read the canonical docs?

**While you build:**
- [ ] Am I calculating or eyeballing? (must be calculating)
- [ ] What material is this? (obsidian, aluminum, brushed metal)
- [ ] Is the light top-left? (check every gradient)
- [ ] Does this move? Why? How fast? Which direction?

**Before you show Shawn:**
- [ ] Run the full Step 5 checklist
- [ ] Every NO is fixed
- [ ] I didn't touch anything unasked

**The 3 questions:**
1. Is it mathematically exact? (formula, not eyeball)
2. Does it feel alive? (moving parts, slow, purposeful)
3. Can you get it in 2 seconds? (headline, clarity)

If YES to all three, you're ready.

---

**This is the playbook. Follow it. The philosophy is in the Design Intelligence Report. This is the HOW.**

**Math is the bones. Beauty is the skin. Wisdom is the breath.**

— Naya Nitro Narzan, 2026-11-02
