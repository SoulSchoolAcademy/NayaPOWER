# ♿ Accessibility, Responsive & Performance Law V1

## 1. Prime law

**Premium includes everyone.**

Accessibility is not a compliance afterthought.

Performance is not separate from beauty.

Responsive behavior is not "make desktop smaller."

## 2. Keyboard

Every interactive function must be operable by keyboard where platform norms support it.

Requirements:
- logical tab order;
- visible focus;
- no keyboard traps;
- Escape closes dismissible layers;
- Enter/Space behavior follows semantics.

## 3. Screen reader / semantics

Use real:
- buttons;
- links;
- headings;
- landmarks;
- lists;
- labels;
- status/live regions where appropriate.

Do not build the app from clickable divs.

## 4. Color and contrast

Meet or exceed applicable WCAG contrast targets.

Do not use color as the only signal.

Test actual rendered gradients, disabled states, and overlays.

## 5. Vision comfort

Support:
- large text;
- browser zoom;
- OS scaling;
- high-contrast needs;
- reduced motion.

Avoid:
- microtype;
- thin low-contrast gray;
- dense all-caps;
- excessive blur;
- flicker.

## 6. Touch

Targets generally:
- minimum 44×44 CSS px;
- sufficient separation;
- no hover-only essential controls.

## 7. Responsive breakpoints

Breakpoints are content-driven.

At each width:
- preserve hierarchy;
- preserve current location;
- preserve primary action;
- keep body text readable;
- reflow before compressing.

## 8. Small-screen strategy

Priority order:
1. essential context;
2. primary action;
3. current intelligence;
4. supporting detail;
5. advanced controls.

Secondary detail can collapse; truth cannot.

## 9. Performance budgets

Production should define measurable budgets for:
- first useful paint;
- interaction latency;
- route transition;
- board render;
- animation frame rate;
- JavaScript payload;
- image assets.

Do not ship the 843KB concept architecture literally.

## 10. Animation performance

Prefer:
- transform;
- opacity;
- compositor-friendly effects.

Avoid:
- layout thrash;
- enormous blur radii everywhere;
- uncontrolled observers;
- continuous animation loops;
- expensive shadows across hundreds of feed items.

## 11. Long feeds

Use:
- pagination;
- windowing/virtualization where useful;
- lazy loading;
- stable skeletons.

Performance must remain excellent as intelligence compounds.

## 12. Network resilience

Design:
- offline/poor connection states;
- retry;
- stale-but-known data;
- partial load;
- reconnect.

Do not freeze the whole Hub because one secondary service fails.

## 13. Acceptance

A surface is not AAA if:
- it is beautiful only on a large desktop;
- keyboard users get a lesser interface;
- reduced-motion destroys state clarity;
- text scaling breaks layout;
- interaction feels delayed;
- growing data makes the interface sluggish.
