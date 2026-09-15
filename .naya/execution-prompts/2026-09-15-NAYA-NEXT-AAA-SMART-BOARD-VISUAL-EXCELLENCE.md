# NAYA → NEXT NAYA — AAA SMART BOARD VISUAL EXCELLENCE EXECUTION PROMPT

**Date:** 2026-09-15  
**Purpose:** Continue the NayaNET Smart Board from verified canonical-source runtime alignment into the actual AAA visual/intelligence experience.  
**Execution mode:** RESTORE → RETRIEVE → INSPECT → UNDERSTAND → SCORE → DECIDE → CHANGE → BUILD → DEPLOY → RUNTIME VERIFY → VISUAL VERIFY → RECORD → NEXT ACTION.

---

## 0. EXECUTIVE DIRECTIVE

Do not spend this turn merely explaining what should be built.

**Inspect the actual implementation, make the highest-value surgical changes that can reasonably be completed in this execution, deploy them, verify them, and leave a durable receipt.**

The human has explicitly identified a recurring failure mode: too little work is being completed per action. Therefore maximize verified progress per execution. Do not stop after one tiny edit when the surrounding work is clearly required and safely achievable.

The objective is not “colored cards.” The objective is:

> **Make the Smart Board feel like intelligence has acquired a physical, premium, living form.**

The existing architecture must be preserved where it works. Do not rebuild the Hub. Do not create another renderer. Do not create another parallel Smart Board. Do not replace working architecture to achieve styling.

---

# 1. CURRENT VERIFIED STATE

## Canonical runtime

The authoritative static Hub source is:

`2026 09 15 NayaNETHUB.html`

The canonical-source surgery workflow successfully produced canonical commit:

`85be32f`

The AppDeploy runtime has been repointed to that canonical commit.

AppDeploy target:

`nayanet-canonical-hub-source-mirror-tqp22y`

Current deployment snapshot at baton creation:

`1789513562268`

Deployment status:

`READY`

Frontend errors:

`[]`

Backend errors:

`[]`

The transitional `upgradeHubPresentation()` runtime adapter has been removed. **Do not reintroduce it merely to compensate for source defects.** Correct the canonical source or the actual React renderer instead.

## Existing React Smart Board

Canonical React renderer:

`NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx`

Canonical Smart Board CSS:

`NAYANET/HUB/src/styles/smart-feed-board.css`

The renderer already contains these conceptual regions:

- Create Space
- Favorite
- Save
- In a Nutshell
- Perspectives
- Adapter Learning
- What It Means
- What Can I Do?
- How to Apply / How to Use
- What's In It For You
- Trust / Provenance / Privacy
- Related Intelligence
- Actions / comments

The current React renderer already has a `Perspective` abstraction, semantic `tones`, and `icons`, so first inspect whether those mechanisms can be elevated rather than replaced.

The current CSS forces perspective sections into a vertical sequence, but it is not yet sufficient for the requested premium illuminated-edge / sculptural-icon system.

---

# 2. HUMAN GOAL — DO NOT LOSE THIS

The Smart Board must communicate this intelligence journey visually and spatially:

**UNDERSTAND → SIMPLIFY → HUMANIZE → INTERPRET → EXPLAIN THE MACHINE → LEARN → MEAN → APPLY → BENEFIT**

The complete visible sequence is:

1. IN A NUTSHELL
2. HUMAN NOTE
3. CHILD NOTE
4. GRANDMA NOTE
5. NAYA NOTE
6. MACHINE NOTE
7. ADAPTER LEARNING
8. WHAT IT MEANS
9. HOW TO APPLY / HOW TO USE
10. WHAT'S IN IT FOR YOU

Do not silently substitute a different sequence.

---

# 3. NON-NEGOTIABLE VISUAL SEMANTIC SYSTEM

These identities are semantic contracts, not decoration:

| Layer | Identity | Intended visual meaning |
|---|---|---|
| IN A NUTSHELL | WHITE | clean intelligence / illuminated knowledge |
| HUMAN NOTE | MAGENTA | human perspective / expression / lived experience |
| CHILD NOTE | PURPLE | simple understanding |
| GRANDMA NOTE | INDIGO | wisdom / experience / practical perspective |
| NAYA NOTE | CANYON | Naya's warm, grounded interpretation |
| MACHINE NOTE | EMERALD | computation / machine perception / systems |
| ADAPTER LEARNING | LIME | learning / adaptation / growth |
| WHAT IT MEANS | YELLOW | meaning / clarity / illumination |
| HOW TO APPLY / HOW TO USE | GOLD | practical application / action |
| WHAT'S IN IT FOR YOU | SILVER | personal value / relevance / payoff |

Important: **Naya Note is CANYON**, not generic blue.  
Important: **How to Apply / Use is GOLD**, distinct from yellow.  
Important: **What's In It For You is SILVER**, not dull gray.

Use a consistent, restrained palette. The exact shades may be tuned for contrast and accessibility, but semantic identity must remain obvious.

---

# 4. EVERY LAYER MUST LOOK ALIVE

Do not implement these as ordinary 1px colored borders.

Each layer should have:

- illuminated perimeter edge
- subtle color bloom outside the edge
- controlled inner highlight
- dimensional panel surface
- clear semantic color identity
- restrained depth/shadow
- hover/focus state that makes the object feel tactile
- no cheap neon effect
- no excessive animation
- no visual clutter

The target feeling is:

**premium physical object + intelligent interface + living knowledge system.**

The glow should look like the material itself is emitting a controlled light.

Use CSS pseudo-elements, layered backgrounds, box-shadows, gradients, masks, or equivalent existing architecture where appropriate. Avoid adding a dependency merely for visual effects.

---

# 5. ICONOGRAPHY REQUIREMENT

Every intelligence layer must have its own recognizable icon.

Icons must not look like arbitrary flat glyphs pasted beside text.

Target:

**3D → sculptural → dimensional → elevated → almost physically emerging from the board.**

The visual illusion should suggest:

- bevel
- volume
- layered material
- soft highlight
- ambient depth
- restrained reflection
- controlled glow

The icon should appear to sit inside a shallow physical recess or rise slightly above the surface.

Do not use emojis as the final visual treatment if the existing implementation can support a proper CSS/HTML sculptural treatment.

Preserve semantic recognition and accessibility with an appropriate accessible label.

---

# 6. IN A NUTSHELL

This is the primary visual anchor.

It must have:

- WHITE semantic identity
- illuminated white perimeter
- premium dimensional surface
- strong central icon/emblem
- clear hierarchy
- enough visual distinction to establish the beginning of the intelligence journey

Do not let the global board border replace the layer's own white identity.

---

# 7. INTELLIGENCE LAYER IMPLEMENTATION

Inspect how `SmartFeedBoard.tsx` currently maps `event.perspectives`, `event.lesson`, `event.meaning`, `event.action`, and `event.whats_in_it_for_you`.

Then make the minimum structural change necessary so that the rendered board always has the complete semantic sequence.

If data is absent, preserve truthfulness. Do not invent intelligence.

Use explicit truthful empty-state copy where necessary.

The existence of the layer is required even when its underlying content is not yet recorded.

The user must be able to visually distinguish the layer itself from its content availability.

---

# 8. HOW TO APPLY / HOW TO USE

This is an architectural requirement, not an afterthought.

It must:

- occupy its own position after WHAT IT MEANS
- use GOLD identity
- have its own illuminated perimeter
- have its own dimensional icon
- contain truthful application guidance
- connect understanding to action
- never fabricate a use case

Preferred comprehension contract:

> **Understand → Interpret → Apply.**

If `event.action.text` exists, expose it as application guidance.
If no verified action exists, say so clearly rather than manufacturing one.

---

# 9. TOP CONTROL BAR

Every Smart Board must have a consistent control arrangement:

### TOP LEFT

**CREATE SPACE**

### TOP RIGHT

**FAVORITE** and **SAVE**

Do not scatter these controls into unrelated parts of the board.

Verify their actual rendered placement after the change.

---

# 10. AAA VISUAL SCORECARD

Before declaring completion, score the implementation against these objective checks. Do not use the score as a political/electoral ranking; this is an internal product-quality checklist.

### A. Architecture — 10/10 condition
- Existing renderer preserved.
- No duplicate Hub.
- No duplicate Smart Board renderer.
- Data architecture preserved.
- Missing layer solved at the correct architectural location.

### B. Semantic identity — 10/10 condition
- All ten layers present.
- All ten colors correct and visually distinct.
- Color meaning is consistent across boards.

### C. Illumination — 10/10 condition
- Each layer has its own illuminated edge.
- Glow follows semantic identity.
- Glow is visible but restrained.
- No cheap neon / bloom overload.

### D. Iconography — 10/10 condition
- Each layer has a distinct icon.
- Icons have dimensional/sculptural treatment.
- Icons feel physically embedded/emergent.
- Icons remain readable at desktop and mobile widths.

### E. Spatial hierarchy — 10/10 condition
- Create Space top-left.
- Favorite + Save top-right.
- Intelligence sequence reads vertically and naturally.
- No accidental two-row intelligence layout.

### F. Interaction — 10/10 condition
- Hover/focus states feel tactile.
- Buttons visibly respond.
- Favorite/save remain functional.
- Create Space remains functional.
- Application action remains truthful and functional.

### G. Responsiveness — 10/10 condition
- Desktop is strong.
- Tablet remains coherent.
- Mobile does not collapse into unreadable clutter.

### H. Truth — 10/10 condition
- No invented data.
- No fake verification.
- Empty intelligence remains explicitly empty.
- Runtime/source distinction is preserved.

### I. Performance — 10/10 condition
- No unnecessary dependency.
- No expensive continuous animation.
- No giant image assets merely for UI chrome.
- Effects remain CSS/DOM-efficient where possible.

### J. Human experience — 10/10 condition
A new user should understand the intelligence journey without needing the architecture explained to them.

---

# 11. REQUIRED EXECUTION SEQUENCE

## STEP 1 — RESTORE

Read the latest canonical design contracts and current Smart Board source before changing anything.

Relevant sources include:

- `.naya/2026-09-13-NAYAPOWER-MASTER-DESIGN-CONTRACT-INTELLIGENT-HUB.md`
- `.naya/NAYANET-SMART-BOARD-AND-SMART-FEED-DESIGN-CONTRACT-V1.md`
- `.naya/activity/2026-09-09-NAYA-TEN-STAR-SERVICE-CODE-OF-ETHICS.md`
- `NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx`
- `NAYANET/HUB/src/styles/smart-feed-board.css`

Do not rely on chat memory where source evidence is available.

## STEP 2 — RETRIEVE

Inspect:

- current renderer
- current CSS
- current layer data model
- current icon mapping
- current tone mapping
- current route/runtime source
- current deployment state

## STEP 3 — SCORE

Identify exactly what prevents the current implementation from satisfying the scorecard.

Do not merely say “styling remains.” Name the concrete deficiencies.

## STEP 4 — DECIDE

Choose the smallest set of changes that can close the largest number of deficiencies in one execution.

Prefer one coherent CSS/component evolution over many tiny unrelated edits.

## STEP 5 — CHANGE

Implement the semantic color, illuminated-edge, icon, dimensionality, ordering, and application-layer requirements in the actual authoritative renderer/source.

Do not patch the runtime with a presentation adapter.

## STEP 6 — BUILD

Run the existing project validation/build path.

If the build fails, diagnose and fix the actual cause rather than stopping at the error.

## STEP 7 — DEPLOY

Deploy the changed authoritative source.

## STEP 8 — VERIFY

Verify all of:

`SOURCE → BUILD → ARTIFACT → DEPLOYMENT → EXACT RUNTIME → OBSERVATION`

Do not collapse these into one “done” statement.

## STEP 9 — VISUAL VERIFY

If a browser/screenshot/runtime observation capability is available, inspect desktop and mobile.

Specifically verify:

- white Nutshell edge
- magenta Human edge
- purple Child edge
- indigo Grandma edge
- canyon Naya edge
- emerald Machine edge
- lime Learning edge
- yellow Meaning edge
- gold Apply edge
- silver Value edge
- sculptural icons
- top control positions
- vertical sequence
- tactile controls

If visual observation is unavailable, state exactly that limitation and do not claim visual verification.

## STEP 10 — RECORD

Create a durable GitHub activity receipt containing:

- WHERE WE ARE
- HUMAN GOAL
- WHAT WAS INSPECTED
- WHAT WAS CHANGED
- WHY IT WAS CHANGED
- SOURCE COMMIT
- BUILD RESULT
- DEPLOYMENT RESULT
- EXACT RUNTIME PATH
- VISUAL OBSERVATION RESULT
- UNKNOWN
- PROTECTED
- LEARNED
- CONFIDENCE
- RISKS
- RECOMMENDATION
- NEXT NAYA ACTION
- PASS CONDITION

## STEP 11 — CONTINUE

Produce exactly one successor execution prompt when additional work remains.

The successor prompt must be executable, not a vague “continue improving.”

---

# 12. PROTECTED RULES

Do not:

- rebuild the Hub
- create another renderer
- create another runtime adapter
- fake missing intelligence
- change the semantic color contract casually
- flatten the icons into generic SVG/glyph treatment
- solve every problem with more glow
- introduce excessive animation
- destroy working controls
- claim visual verification without visual evidence
- claim deployment verification without deployment evidence
- call code-complete “done”
- ask the human to perform work that available tools can reasonably perform

---

# 13. DEFINITION OF DONE

This execution is complete only when the actual authoritative Smart Board implementation has been materially advanced toward the requested experience and the work has been verified as far as available tooling permits.

The strongest successful state is:

> **The user opens a Smart Board and immediately sees a premium, dimensional intelligence object whose layers are visually encoded by light, color, iconography, and spatial hierarchy. The system explains intelligence, translates it for different perspectives, explains what it means, shows how to apply it, and communicates personal value — without inventing anything.**

The human should be able to look at the board and think:

> **“Holy shit. This isn't just a note.”**

---

# 14. REQUIRED HUMAN RECEIPT FORMAT

End the execution report with:

### WHERE WE ARE

### WHAT WE ARE TRYING TO ACCOMPLISH

### WHAT WE DID

### WHAT WE CHANGED

### WHAT WE VERIFIED

### CURRENT STATE

### UNKNOWN

### PROTECTED

### LEARNED

### CONFIDENCE

### RISKS

### RECOMMENDATION

### NEXT NAYA ACTION

### PASS CONDITION

**Exactly one executable NEXT NAYA ACTION.**
