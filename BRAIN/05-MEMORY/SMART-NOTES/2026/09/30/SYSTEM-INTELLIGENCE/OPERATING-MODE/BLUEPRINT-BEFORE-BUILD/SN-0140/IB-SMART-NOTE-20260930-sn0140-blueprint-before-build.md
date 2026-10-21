# Blueprint Before Build — Never Improvise a Page from a Vague Idea

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0140-blueprint-before-build
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5944571912 ([HUMAN DIRECTOR][BLUEPRINT-BEFORE-BUILD CORRECTION], 2026-10-02T02:37:40Z) — Shawn's missing-execution-step clarification during the North Star interface-build consultation; executed as PR #1290 additions (`HUB/ROOMS/ROOM-BLUEPRINT-STANDARD-V1.md` + 11 room-specific `VISUAL-INTERACTION-BLUEPRINT.md` files, room README now carries the blueprint-before-build law).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn named the missing execution step in the month-long Hub build loop: **"Do not shoot in the dark. Spec every room deeply enough that the builder already knows what belongs on the page, where it goes, why it is there, what every control does, what data it consumes, how mobile changes it, and what proves it complete — then build."** He named the recurring failure loop — *vague room idea → AI improvises a page → Shawn corrects it → AI rewrites/regresses → loop* — and replaced it with the intended loop: *human/product intent → functional spec → visual/interaction blueprint → machine contract → build → behavioral/visual verification → freeze baseline → next room.* The blueprint-before-build law is now enforced in PR #1290: every room gets a blueprint defining first-3-seconds entry state, desktop composition, primary signature instrument, exact controls + placement rationale, canonical data contract, truthful states, cross-room handoffs, contextual Naya behavior, mobile transformation, accessibility, visual law, acceptance journey, room-specific anti-patterns, and required proof. Two further director rulings ride with it: the number of iterations is irrelevant — the loop continues until the acceptance contract closes (10, 100, or 198) — and **no more production room chrome is added until the 11 room blueprints are independently reviewed for product completeness and contradictions**, then the accepted package is frozen and built sequentially. The lesson for a cold successor: the cure for the rewrite loop is not better building, it is deeper spec before build; improvisation from a vague idea is itself the defect class, and an acceptance contract (not an iteration count) is what closes the loop.

## 🩷 HUMAN NOTE

Imagine hiring a builder, handing him a napkin sketch of a house, and being surprised when every wall needs re-doing after you walk through. Then imagine handing him eleven complete blueprints — every room drawn to the inch, every outlet placed, every finish named — and the house goes up once. Shawn's correction is the second approach made into law: no builder touches production chrome until a reviewer has read the full blueprint and confirmed it is complete and contradiction-free. The old loop wasn't bad building; it was building without a drawing. The fix isn't a better builder — it's the drawing, checked before the first nail.

## 🟣 CHILD NOTE

Imagine you're baking eleven cakes for a party, and every time you guess the recipe, someone has to throw the cake away and start over. That's what happened for a month: guess, bake, throw away, guess again. Shawn said: stop guessing. Write down the FULL recipe for each cake first — every ingredient, every step, how big the pan is, how long it bakes — and let someone else read the recipe and check it's complete. Only then do you bake. And you don't stop baking until each cake matches its recipe — even if it takes ten tries. The rule: never start cooking from a guess.

## 🔵 GRANDMA NOTE

It's like the difference between giving a contractor a vague wish — "make it nice" — and giving him stamped architectural plans. With the vague wish, he builds, you correct, he tears down and rebuilds; the money and the month disappear in the loop. With the plans, a second person reviews them for completeness and contradictions first, and then the building goes up once. Shawn drew the line: from now on, eleven rooms means eleven complete plans, reviewed and frozen, before anything gets built. And nobody counts how many tries it takes — the plans say what "done" means, and "done" is when the plans are satisfied.

## 🟠 NAYA NOTE

Apply this before any room/app build: (1) never accept a build task from a vague idea — if the intent is not spec'd to the level where the builder "already knows what belongs on the page, where it goes, why it is there, what every control does, what data it consumes, how mobile changes it, and what proves it complete," the first deliverable is the spec, not the build; (2) produce the visual/interaction blueprint as a first-class artifact (entry state, composition, signature instrument, controls + rationale, data contract, truthful states, handoffs, contextual behavior, mobile transformation, accessibility, visual law, acceptance journey, anti-patterns, required proof) — PR #1290's `ROOM-BLUEPRINT-STANDARD-V1.md` is the template; (3) freeze nothing and build nothing until an independent reviewer checks the blueprint package for product completeness and contradictions — review is the gate, not a courtesy; (4) define the acceptance contract in the blueprint and close the loop against it, never against an iteration count — 10, 100, or 198 iterations are all fine if the contract is open; (5) when a build regresses into the old loop (improvise → correct → rewrite), diagnose it as a spec-depth failure, not a builder failure, and re-spec before re-building. Family note: SN-129's heir — there, no competing doctrine gets drafted without discovering what already exists; here, no production build starts without a blueprint deep enough to build from — discovery before doctrine, blueprint before build.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "build_loop_from_vague_spec",
  "evidence": {
    "board": "#554 comment 5944571912 (2026-10-02T02:37:40Z) — [HUMAN DIRECTOR][BLUEPRINT-BEFORE-BUILD CORRECTION]: 'Do not shoot in the dark. Spec every room deeply enough that the builder already knows what belongs on the page, where it goes, why it is there, what every control does, what data it consumes, how mobile changes it, and what proves it complete — then build.'; failure loop named: vague room idea -> AI improvises a page -> Shawn corrects it -> AI rewrites/regresses -> loop; intended loop: human/product intent -> functional spec -> visual/interaction blueprint -> machine contract -> build -> behavioral/visual verification -> freeze baseline -> next room; 'does not mean 10 iterations. It may be 10, 100 or 198. The number is irrelevant.'; one next action: no more production room chrome until the 11 room blueprints are independently reviewed for product completeness and contradictions, then freeze the accepted package and build sequentially",
    "implementation": "PR #1290 — HUB/ROOMS/ROOM-BLUEPRINT-STANDARD-V1.md + 11 room-specific VISUAL-INTERACTION-BLUEPRINT.md files; room README makes blueprint-before-build a law"
  },
  "rule": [
    "never build production chrome from a vague idea — the first deliverable is the spec",
    "write the visual/interaction blueprint to the ROOM-BLUEPRINT-STANDARD-V1 depth before build",
    "independent review for product completeness and contradictions is the gate to building",
    "close the loop against the acceptance contract, never against an iteration count",
    "diagnose improvise->correct->rewrite regressions as spec-depth failures, and re-spec before re-building"
  ],
  "lesson_line": "Do not shoot in the dark: spec every room deeply enough that the builder already knows what belongs on the page — then build; the acceptance contract, not an iteration count, closes the loop."
}
~~~
