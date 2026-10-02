# 🔱 NayaNET Room Contract — Settings

**Room ID:** `settings`  
**Route:** `/settings`  
**Theme:** **Neutral Gray** — `#aaa4b1`  
**Status:** HUMAN-DIRECTOR-DIRECTED TARGET CONTRACT — 2026-10-02  
**Runtime truth:** **SPECIFICATION, NOT PRODUCTION PROOF**  
**Authority:** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` + `HUB/NAYA-DESIGN-MASTERCLASS-V1.md` + `HUB/DESIGN-CONTRACT.md` + `HUB/NAYANET-SMART-APP-ROOMS-V1.json`  
**This document is:** the living, room-specific design/experience/behavior contract. It specializes the master law; it does not create a competing design system.

> **Room law:** Make this room extraordinarily useful, unmistakably Naya, truthful about its state, and beautiful because its intelligence is beautifully organized — never beautiful instead of functional.

---

## 1. HUMAN JOB

**Control the relationship with NayaNET**

### The room must answer

- **WHERE AM I?** Settings
- **WHAT MATTERS?** Identity, privacy, authority, connections, personalization, notifications, appearance and accessibility.
- **WHAT CAN I DO?** Choose the relevant category and change a setting with clear consequences.
- **WHAT HAPPENS NEXT?** The visitor understands exactly what changed, what it affects and what happens next.

### Time-horizon test

**1 second:** The category structure is immediately readable.  
**3 seconds:** The visitor knows where to go for the desired kind of control.  
**30 seconds:** A setting can be changed without guessing its consequences.  
**Return visit:** The last category/setting context restores when legitimate.

---

## 2. PRIMARY EXPERIENCE

**Primary action:** `CONTEXTUAL_BY_CATEGORY`

**Composition grammar:**  
1. **Identity & Account**
2. **Privacy & Sharing**
3. **Permissions / Authority**
4. **Connections / Smart Doors**
5. **Personalization**
6. **Notifications**
7. **Appearance**
8. **Accessibility**

### Primary information hierarchy

1. Category orientation
2. Current setting state
3. Causal explanation
4. Change control
5. Impact/confirmation
6. Result

**One-screen principle:** The room should have one dominant focal hierarchy. Secondary tools stay subordinate until needed.

---

## 3. VISUAL DIRECTION

### Material

**OBSIDIAN FOUNDATION → PRECISE EDGE → SUBTLE INSET HIGHLIGHT → REAL ELEVATION → CONTROLLED THEME ENERGY**

The room inherits the shared Naya material system. Theme energy appears at meaningful edges, jewels, focus states, active states and other semantic points — not as decorative wallpaper.

### Theme

**Neutral Gray** — `#aaa4b1`

**Meaning:** Control, clarity, neutrality.

**Current canonical status:** CANONICAL neutral surface with semantic accents.

### Signature expression

**THE CONTROL DECK.** Neutral silver and obsidian replace form-page blandness with calm instrument-panel precision. Controls should feel like brushed metal or precision switches only where physicality improves understanding. Every consequential setting shows what it affects, where it persists, whether it is local/account/runtime-backed, and what the recovery path is. Control should feel empowering, not administrative.

The room must feel like one member of the same living product, not an independent microsite.

---

## 4. SURFACE ANATOMY

### Persistent shell

- Left rail remains the primary room navigation.
- Top context bar identifies room and truthful system status.
- Global intelligence search remains available.
- Naya presence is contextual, never a duplicate dashboard.
- The workspace owns the room composition.
- Privacy posture remains visible where relevant.

### Room workspace

A calm control deck — precise, spacious, technically honest, never like a developer console.

### Object treatment

- Setting
- Current value/state
- What it changes
- Scope
- Authority
- Impact
- Confirmation
- Result

---

## 5. INTELLIGENCE + DATA TRUTH

### Canonical objects

- User/account preferences
- Privacy/consent state
- Authority settings
- Connection configuration
- Accessibility/preferences

### Source of truth

**Governed settings/configuration sources; no local-only fake state presented as canonical.**

The room is a projection of canonical intelligence. It must not create a shadow truth store merely to make the screen look complete.

### Truth rules

- **UNKNOWN ≠ PASS**
- **BLOCKED ≠ PASS**
- **IMPLEMENTED ≠ VERIFIED**
- **VERIFIED ≠ PRODUCTION-PROVEN**
- Never fabricate personalization, liveness, counts, relationships, messages, reports, receipts or connection state.
- Visual energy must follow actual state.

---

## 6. INTERACTION CONTRACT

Every consequential control follows:

**CONTROL → INTENT → SCOPE/AUTHORITY → CAPABILITY → OPERATION → OBSERVATION → RESULT → UI STATE → EVIDENCE WHERE REQUIRED**

### Primary interactions

- Navigate category.
- Inspect causal path.
- Change setting.
- Confirm consequential changes proportionally.
- Observe result and persisted state.
- Recover/undo where supported.

### Naya presence

Naya may explain, retrieve, compare, summarize, propose and — only when authorized — act in the context of this room.

Naya must know the active room, selected object/context, truth state and authority boundary before making a room-specific claim.

---

## 7. UNIVERSAL STATE MATRIX

The implementation must explicitly design applicable behavior for:

| State | Room requirement |
|---|---|
| **LOADING** | Preserve category orientation. |
| **EMPTY** | Never use empty for settings categories; explain unsupported/unavailable areas. |
| **READY** | Current values are readable. |
| **BLOCKED** | Explain dependency or authority blocker. |
| **UNAUTHORIZED** | Explain why control is unavailable and what legitimate route exists. |
| **NOT_VERIFIED** | Do not imply a changed setting until persistence is proven. |
| **VERIFIED** | Show durable state with precise confirmation. |
| **ERROR** | Explain whether change applied, failed or rolled back. |
| **OFFLINE** | Separate local-only safe changes from server-dependent changes. |
| **DISABLED** | Explain why control is unavailable when needed. |
| **UNKNOWN** | Unknown value is explicit, not guessed from defaults. |

---

## 8. RESPONSIVE COMPOSITION

### Desktop

Control-deck composition with category rail/stack + focused detail.

### Tablet

Category selection above focused setting group.

### Mobile

Category → setting → impact → confirmation/result; avoid deep accordion hell.

Required test widths: **320 / 375 / 390 / 430 / 768 / 820 / desktop reference widths**, plus **125% / 150% / 200% zoom**.

---

## 9. ACCESSIBILITY

This room is not Signature unless its intelligence remains understandable and operable for people using:

- keyboard-only navigation;
- assistive technology / screen readers;
- zoom up to 200%;
- reduced-motion preferences;
- high-contrast / accessibility settings;
- touch input.

Focus order must follow cognitive order. Color may reinforce meaning but never be the sole carrier of meaning.

### Room-specific accessibility consideration

Settings need labels, descriptions, error association, keyboard-complete confirmation flows and accessible change announcements.

---

## 10. PERFORMANCE

Settings should be fast and lightweight; don't load admin/developer machinery until requested.

The user should never pay a speed tax for spectacle.

---

## 11. ANTI-PATTERNS — AUTOMATIC REJECTION

- **Developer console masquerading as user settings.**
- **Mystery toggles.**
- **Consequential change without confirmation.**
- **Persisted-looking UI before persistence is verified.**
- **Accessibility buried beneath appearance.**

---

## 12. SUCCESS METRICS

Measure the room against the task, not against vanity.

- Time to locate a setting.
- Change success/recovery.
- Misconfiguration rate.
- Understanding of setting impact.
- Accessibility task success.

A visual-quality claim requires rendered evidence; a functional claim requires behavioral evidence; a persistence claim requires persistence/cold-read evidence; an accessibility claim requires accessibility evidence; a performance claim requires measured performance evidence.

---

## 13. ROOM GRADUATION GATE

The room cannot graduate because the page renders.

It requires:

**PURPOSE CLEAR  
+ 3-SECOND ORIENTATION  
+ REAL INTELLIGENCE OR HONEST EMPTY STATE  
+ REAL CAUSAL ACTIONS  
+ APPLICABLE STATES  
+ NAYA SIGNATURE  
+ RESPONSIVE QUALITY  
+ ACCESSIBILITY  
+ PERFORMANCE  
+ CONTINUITY  
+ TRUTH/PROVENANCE  
+ INDEPENDENT CHALLENGE  
+ EVIDENCE**

And the current global acceptance bar applies:

- **D1 Visual Excellence = 10.0**
- **D2–D8 ≥ 9.5**
- No averaging away a hard-gate failure.

---

## 14. PROOF PLAN

### Builder proof

- Test every declared category path and persistence where supported.
- Test error/rollback/unauthorized cases.

### Independent challenge

- Ask whether a reasonable person can predict consequences from the UI alone.
- Challenge defaults and unknown states.

### Evidence to retain

- Before/after configuration state.
- Persistence/cold-read evidence.
- Rendered confirmation/error states.
- Independent accessibility review.

---

## 15. OPEN DECISIONS

- Exact grouping/order of Advanced/Developer controls should remain secondary until core human settings prove comprehensible.
- Control-deck material language should be rendered and challenged for calmness versus sterility.

Open decisions remain visibly open until resolved by the Human Director or authoritative project evidence. They must not be silently guessed into production.

---

## 15A. SIGNATURE / BENCHMARK-TO-BEYOND

### Signature moment
Before a consequential control changes, the human can understand **what will change, where it applies, what authority is involved, and how to reverse or verify it** — then receives truthful confirmation after the change.

### Best-of intelligence to synthesize
- **Norman/Nielsen:** mapping, feedback, error prevention and recovery.
- **Stripe:** operational consequence clarity.
- **Things:** calm hierarchy and restraint.
- **Linear:** compact precision.

### Beyond-benchmark hypothesis
Settings become a Smart Control Deck when every control is causally transparent, scope-aware and verifiable, while ordinary preferences remain effortless and technical machinery stays secondary.

### Proof boundary
Measure setting-find time, change success, reversal/recovery success, consequential misclick rate and persistence verification.

---

## 16. WORKING NOTES — LIVING RECORD

This section is intentionally permanent. Every meaningful room-design discovery, defect, decision, accepted pattern, regression, supersession or proof result belongs here.

### 2026-10-02 — Initial contract creation

- Created as the canonical room-specific layer under the NayaNET Smart App Room Master Specification.
- Design intent is derived from the live master room contract and current Naya design intelligence.
- Runtime behavior is **not claimed** merely because this document exists.

### Future entries

Record:

**DATE → OBSERVATION → EVIDENCE → DECISION → CHANGE → SCORE EFFECT → LESSON → NEXT TEST**

---

## 17. RELATIONSHIPS

- **Master room law:** `../NAYANET-SMART-APP-ROOM-SPEC-V1.md`
- **Machine room registry:** `../NAYANET-SMART-APP-ROOMS-V1.json`
- **Design constitution:** `../NAYA-DESIGN-MASTERCLASS-V1.md`
- **Visual authority:** `../DESIGN-CONTRACT.md`
- **Coordination:** GitHub Issue **#554**
- **Graduation contract:** GitHub Issue **#1310**

> **Final room command:** Do not make this room merely attractive. Make its human purpose obvious, its intelligence useful, its state truthful, its interactions elegant, and its presence unmistakably Naya.
