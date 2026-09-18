# 🔱☀️ NayaNET E01 — Test & Release Gate

**Purpose:** make “complete / fully working / elite / ready to rock” measurable.

## Truth rule

Source existence is not runtime proof. This gate separates:

`BUILD-READY → TESTED → OSCAR-ATTACKED → REPAIRED → RE-TESTED → PACKAGED → DEPLOYED → LIVE-VERIFIED`

No stage may be marked passed without evidence.

## Test matrix

### Arrival
- [ ] Page loads with no console errors.
- [ ] NayaNET brand and welcome message are immediately recognizable.
- [ ] One dominant Create action is visually obvious.
- [ ] Meet Naya has a deterministic authored response.
- [ ] Living Sun state changes visibly and textually.

### Identity
- [ ] Create opens identity state.
- [ ] Focus lands in name field.
- [ ] Empty/one-character input is rejected inline.
- [ ] Valid name creates deterministic local identity.
- [ ] Smart Name is displayed.
- [ ] Smart Link is displayed.
- [ ] Identity is explicitly described as local/preview, never authenticated.
- [ ] Refresh restores local state when storage works.
- [ ] Storage failure remains usable and explains session-only behavior.

### Reveal / Toolbox
- [ ] Identity reveal is complete and readable.
- [ ] Copy works when Clipboard API exists.
- [ ] Clipboard fallback leaves selectable link text.
- [ ] Toolbox opens without dead-end.
- [ ] Ready-now actions are distinguishable from future capabilities.
- [ ] Future actions never imply backend completion.
- [ ] Reset requires confirmation and clears only E01 local state.

### Accessibility
- [ ] Keyboard-only flow reaches every actionable control.
- [ ] Focus is visible.
- [ ] Form has a real label.
- [ ] Live feedback is announced.
- [ ] Sun state has text equivalent.
- [ ] No status depends on color alone.
- [ ] Reduced-motion mode removes continuous orbital animation.
- [ ] Touch targets remain usable on narrow screens.

### Responsive
- [ ] 320px.
- [ ] 360px.
- [ ] 375px.
- [ ] 390px.
- [ ] 414px.
- [ ] 480px.
- [ ] 600px.
- [ ] 768px.
- [ ] 900px.
- [ ] 1024px.
- [ ] 1280px.
- [ ] No horizontal overflow.
- [ ] No iframe clipping.

### Oscar attack
- [ ] Generic SaaS feel rejected.
- [ ] First action cannot be misunderstood.
- [ ] Copy is understandable without architecture knowledge.
- [ ] No fake AI, authentication, Superbrain, memory, telemetry, or server result.
- [ ] No dead button.
- [ ] No misleading future capability.
- [ ] No visual clutter.
- [ ] No excessive motion.
- [ ] No brand-asset claim without evidence.
- [ ] Failure states are recoverable.

## Evidence packet required for release

1. Exact Git commit SHA.
2. Source artifact manifest.
3. Automated test output, if execution infrastructure is available.
4. Browser/runtime evidence for the full interaction path.
5. Responsive evidence covering the required matrix.
6. Accessibility evidence.
7. Oscar findings and repairs.
8. Final human recognition review.
9. Package/ZIP checksum.
10. Deployment URL only if actually deployed.
11. Live verification receipt only if actually reachable.
12. Naya Note and Human Note.
13. Successor torch.

## Current gate state

**BUILD-READY:** PASS — source is prepared for execution testing.

**TESTED:** PENDING — execution-capable browser/runtime evidence is required.

**OSCAR-ATTACKED:** PENDING — must occur after runtime test.

**REPAIRED:** PENDING — repair only after first-failure evidence.

**RE-TESTED:** PENDING.

**PACKAGED:** PENDING.

**DEPLOYED:** NOT CLAIMED.

**LIVE-VERIFIED:** NOT CLAIMED.

**PRODUCTION-PROVEN:** NOT CLAIMED.

## Release law

A green source review is not a green product.

A product is complete only when the evidence packet proves the user can enter, understand, create, continue, recover, and finish the intended E01 journey in reality.
