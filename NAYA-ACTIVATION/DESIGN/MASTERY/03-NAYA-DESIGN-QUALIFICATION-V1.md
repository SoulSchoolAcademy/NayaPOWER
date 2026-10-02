# 🔱 NAYA DESIGN QUALIFICATION V1
## Automatic diagnostics + independent craft review without inventing a competing scorecard

**Status:** PROPOSED CANONICAL QUALIFICATION LAYER  
**Parent scorecard:** project-specific scorecard remains authoritative. For the Hub, use D1–D8 in `HUB/PROJECT-INTELLIGENCE.md`.  
**Rule:** This document supplies evidence and failure predicates. It does not replace the canonical product score.

---

# 1. QUALIFICATION MODEL

A design candidate must pass four classes:

```
A. HARD GATES
B. DESIGN DIAGNOSTICS
C. CANONICAL PRODUCT SCORECARD
D. INDEPENDENT REVIEW
```

A high average cannot compensate for a hard-gate failure.

Examples:
- a beautiful page with dead controls fails;
- an accessible page with fake VERIFIED state fails;
- a strong desktop page that collapses on mobile fails;
- a 9.6 self-score with no independent challenge is not qualified.

---

# 2. HARD GATES

Automatic rework if any applicable predicate is true.

## Truth
- fake data presented as real;
- simulated activity presented as live;
- VERIFIED without evidence;
- connected without backend evidence;
- stale data presented as current;
- unknown silently converted to empty/success.

## Function
- primary control has no causal path and no honest unavailable state;
- route is dead;
- back/reload loses required state without disclosure;
- action claims success before observable consequence.

## Completion
- declared route/page missing;
- placeholder counted as complete;
- shell or first slice used to close multi-page scope;
- material TODO hidden outside completion matrix.

## Accessibility
- primary journey not keyboard operable;
- focus invisible;
- critical state depends on color only;
- body text below project floor without explicit justified exception;
- core interaction unusable at 200% zoom;
- reduced-motion mode loses meaning.

## Responsive
- horizontal overflow in supported viewport;
- duplicated primary navigation;
- mobile loses essential action/state;
- desktop composition merely stacks into incoherent mobile cards.

## Performance
- repeated layout-thrashing interaction;
- decorative continuous animation causing material cost;
- unusable interaction latency on agreed target device;
- concept/laboratory artifact shipped as monolithic production architecture when a lighter path exists.

## Regression
- accepted baseline visibly/functionally worsened without approved tradeoff;
- stronger prior component replaced by generic default for engineering convenience.

---

# 3. THE 20 DESIGN DIAGNOSTIC LENSES

Score each applicable lens 0–10 with evidence. These are **diagnostics**, not a new canonical overall score.

## Q01 PURPOSE CLARITY
Can a person tell what this surface is for?

Maps primarily to: D2, D8.

## Q02 THREE-SECOND ORIENTATION
Where am I? What matters? What can I do?

Maps: D1, D2, D8.

## Q03 INFORMATION HIERARCHY
Primary, secondary and tertiary information are visually distinct.

Maps: D1, D8.

## Q04 COMPOSITION
The page is deliberately composed rather than tiled from available components.

Maps: D1, D8.

## Q05 TEXT RESTRAINT
Copy explains only what interface structure/state cannot carry more effectively.

Maps: D1, D8.

## Q06 TYPOGRAPHY / READABILITY
Type size, contrast, line length, rhythm and weight support comfortable reading.

Maps: D1, D7, D8.

## Q07 SPACING / GEOMETRY
Spacing rhythm and shape families feel intentional.

Maps: D1, D8.

## Q08 MATERIAL / LIGHT
Depth, edge, highlight and shadow create coherent object physics without obscuring content.

Maps: D1, D8.

## Q09 COLOR SEMANTICS
Color communicates identity/state/meaning rather than decoration.

Maps: D1, D4, D8.

## Q10 ICON / GLYPH COHERENCE
One family, correct importance, readable at use size.

Maps: D1, D7, D8.

## Q11 CONTROL PHYSICS
Rest, hover, focus, press, loading, disabled and result states are intentional.

Maps: D1, D2, D7, D8.

## Q12 STATE HONESTY
Loading, empty, blocked, unknown, verified, error etc. correspond to actual truth.

Maps: D4.

## Q13 CAUSAL COMPLETENESS
Visible actions reach real capability or honest refusal/unavailable state.

Maps: D2, D4.

## Q14 INTELLIGENCE VALUE
The surface uses Naya intelligence to reduce burden or improve decisions rather than adding AI theater.

Maps: D3, D8.

## Q15 PROVENANCE / TRUST
Evidence is reachable where consequence/trust requires it.

Maps: D3, D4, D6.

## Q16 RESPONSIVE IDENTITY
The same product identity and task clarity survive across viewports.

Maps: D1, D7, D8.

## Q17 ACCESSIBILITY
Keyboard, semantics, contrast, touch, zoom, reduced motion.

Maps: D7.

## Q18 PERFORMANCE FEEL
The interaction feels immediate and motion remains smooth.

Maps: D5.

## Q19 DISTINCTION / ANTI-GENERIC
The page could not be swapped unchanged into generic SaaS without losing meaning.

Maps: D1, D8.

## Q20 CONTINUITY / COMPLETION
The page belongs to a complete coherent app and preserves state/context appropriately.

Maps: D2, D6, D8.

---

# 4. DIAGNOSTIC INTERPRETATION

Suggested meaning only:

- **0–4.9:** broken / missing / materially poor
- **5.0–6.9:** recognizable structure, not release quality
- **7.0–8.4:** strong but material weaknesses remain
- **8.5–8.9:** near the project bar; still not ≥9
- **9.0–9.4:** elite/release-capable if canonical scorecard and hard gates also pass
- **9.5–9.9:** near-perfect current standard
- **10:** no material improvement currently known for this lens under current evidence

Do not round 8.95 into 9.0 to pass a gate.

---

# 5. SELF-ANALYSIS EVIDENCE PACKAGE

For each material page:

```
source_sha
route
state
viewport
screenshot_refs
interaction_test_refs
console_errors
overflow_result
keyboard_result
zoom_result
reduced_motion_result
performance_result
runtime_truth
known_limits
Q01..Q20 diagnostics
canonical D1..D8 score contribution
builder_findings
repair_actions
```

Unknown remains unknown.

---

# 6. INDEPENDENT REVIEW PROTOCOL

The independent reviewer must not begin from the builder's narrative alone.

Review in this order:

1. rendered artifact;
2. task/purpose;
3. interaction behavior;
4. state behavior;
5. mobile;
6. accessibility;
7. performance evidence;
8. canonical contract;
9. builder score.

This reduces anchoring.

Required adversarial questions:
- What would a first-time user misunderstand?
- What is visually loud without being important?
- What is important but visually quiet?
- What text exists because structure is weak?
- What control implies capability it does not have?
- What looks generic?
- What regressed?
- What breaks on mobile/zoom?
- What would an accessibility expert reject?
- What evidence is missing?
- Is any scope missing behind a strong screenshot?

---

# 7. SIGNATURE REVIEW

Evaluate the 10 signature traits from the Constitution.

A candidate may be visually beautiful but not yet signature-quality if:
- it could belong to any premium SaaS;
- it uses the right colors but generic composition;
- it has Naya jewels but weak hierarchy;
- it is “futuristic” but not calm/useful;
- it hides truth to preserve aesthetics.

Signature is earned through coherent decisions.

---

# 8. AUTOMATIC SCORECARDING — WHAT MACHINES CAN MEASURE

Automatable evidence includes:
- font-size floors;
- contrast ratios;
- missing labels/ARIA;
- touch target sizes;
- horizontal overflow;
- duplicate nav landmarks;
- broken links/routes;
- console errors;
- missing reduced-motion treatment;
- animation durations/continuous loops;
- performance metrics;
- screenshots at canonical viewports;
- visual-diff percentage/regions;
- dead controls where test harness can determine consequence;
- completion-matrix state consistency.

Machine checks cannot conclusively measure:
- beauty;
- emotional resonance;
- composition quality;
- originality;
- signature strength;
- whether the right thing is emphasized.

Treat automated scoring as evidence, not aesthetic authority.

---

# 9. RELEASE GATE

For the Hub:

1. no hard-gate failure;
2. canonical D1–D8 each ≥9.0;
3. D1 target 10;
4. independent re-score complete;
5. applicable browser/runtime evidence attached;
6. critical journeys complete;
7. no known material regression;
8. remaining unknowns explicit;
9. Human Director visual validation when required by current project law.

The bar may rise as the system learns.

---

# 10. REPAIR PRIORITY FORMULA

When multiple findings exist, rank using:

```
PRIORITY =
USER_BURDEN
× SEVERITY
× SCOPE
× REGRESSION_RISK
× REUSE_VALUE
÷ REPAIR_COST
```

Use ordinal/normalized values; do not pretend the formula is objective physics.

Purpose: repair the most consequential weakness before adding decorative polish.

---

# 11. MASTER QUESTION

Before qualification:

> **Would a demanding ordinary human, an elite product designer, an accessibility expert, a front-end engineer and a proof reviewer all find this unusually well made for their own reasons?**

If one of those perspectives reveals a material flaw, keep working.
