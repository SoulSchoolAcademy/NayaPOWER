# NAYA BUILDER PROTOCOL — INTERFACE WORK V1

This is the dispatch protocol for any Naya, agent, or human building a NayaNET interface. It is subordinate to the NayaPOWER Master Design Contract, Naya Design Contract v1.2, Naya Design Intelligence Standard, the app's Project Intelligence, and the current Smart Factory contracts.

## Your mission

Turn the user's real job into a beautiful, intelligent, useful, trustworthy, responsive, working interface. Do not optimize for visual spectacle, screen count, code volume, or your own aesthetic preference. Optimize for responsible human value with minimum necessary cognitive burden.

## Mandatory read-first

Before changing code:

1. Restore the current Project Intelligence and source-of-truth references.
2. Read the current design and project contracts; do not rely on a previous chat summary as authority.
3. Inspect the current implementation, routes, data path, permissions, tests, component registries, and open work.
4. Identify what must be preserved. Classify relevant pieces as KEEP, IMPROVE, REPLACE, REMOVE, or UNKNOWN.
5. Resolve canonical component IDs and their exact source files. A catalogue entry does not prove a part works in the target runtime.

If a source of truth, owner, permission, data source, or critical dependency is unknown, record UNKNOWN and route it. Do not invent a convenient answer.

## Speak NIL

Use the Naya Interface Language:

- WORLD: whose context is this?
- APP: which purposeful workspace are we building?
- PERSON: who is using it and with what authority?
- JOB: what are they trying to accomplish?
- JOURNEY: what is the end-to-end sequence?
- ROOM: which meaningful domain of work?
- SCREEN: what is the one dominant job of this composition?
- FOCAL: what should win first attention?
- SUPPORT: what context makes the focal point understandable?
- ACTION: what does the user intend and what actually happens?
- STATE: what is true now?
- PART: which exact reusable component or pattern is assembled?
- SOURCE: which canonical system owns the information?
- PROOF: how do we know the claim is true?
- RECEIPT: where is the attributable record?

Brief every screen with: JOB, ENTRY, FIRST GLANCE, FOCAL POINT, SUPPORT, NEXT ACTION, DATA/SOURCE/FRESHNESS, STATES, RESPONSIVE COMPOSITION, ACCESSIBILITY, ACCEPTANCE TESTS.

## Design rules

- Follow the canonical Naya palette, material, depth, lighting, type, icon, button, and interaction contract.
- Preserve existing strong surfaces; improve only what the evidence says is deficient.
- One dominant focal point per screen. Supporting content must earn its place.
- The first viewport must orient the user and make the next useful action clear. Do not force long reports, lists, or workflows into a single fixed height.
- Normal page scrolling is allowed. Clipping, obscured controls, accidental nested scrolling, and essential horizontal page scrolling are not.
- Mobile is a first-class composition: test 320, 360, 390, 430, 768, 1024, 1440, and 1920 CSS px as applicable, plus keyboard, safe area, orientation, zoom, touch, and keyboard.
- Use actual Naya parts with provenance. Compose, do not casually invent. If a new part is justified, name the registry gap and propose a governed reusable part.
- Life comes from meaningful state, feedback, useful data, and restrained motion. Do not animate fake liveness.
- Body readability beats glow. Meet WCAG 2.2 AA and the stricter 44px Naya house target for important controls.

## Functional rules

Every control must have:
- user intent and honest label;
- actor and permission scope;
- real capability/service;
- preconditions and effect;
- success signal;
- pending, error, timeout, unavailable, and recovery behavior where relevant;
- confirmation/undo safeguards proportional to consequence;
- evidence or receipt when consequential.

Every displayed value must identify its source, meaning, unit, time range, freshness, and derivation when material. Unknown, demo, stale, cached, predicted, and live are distinct. Unknown must never be styled or described as live.

## Factory sequence

1. RESTORE — current laws, PI, code, runtime, active work.
2. DEFINE — human job, audience, success, non-goals.
3. INVENTORY — route, UI, data, actions, permissions, parts, tests.
4. ARCHITECT — journey, object model, rooms, screen map, navigation.
5. CONTRACT — complete machine-readable interface brief.
6. COMPOSE — exact component IDs, variants, design tokens, dependencies.
7. BUILD — one smallest complete vertical journey, not a pile of mock screens.
8. VERIFY — behavior, data truth, responsive, accessibility, visual, performance, privacy/security.
9. CHALLENGE — independent review of the frozen commit and rendered result.
10. PROMOTE — preview, required approval, governed deployment.
11. OBSERVE — verify real production behavior with real permissions and data.
12. LEARN — capture scoped, evidenced lessons through the existing learning path.

Run the pre-build gate:

    python BRAIN/10-INTERFACES/NAYA-INTERFACE-FACTORY/validate_naya_interface_brief.py BRIEF.json --pieces BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json --stage prebuild

A PASS means the brief is structurally and semantically complete enough to plan and dispatch. It does not mean the app is built, tested, accessible, deployed, or production-proven.

Run the release gate only after the required checks have actually been performed:

    python BRAIN/10-INTERFACES/NAYA-INTERFACE-FACTORY/validate_naya_interface_brief.py BRIEF.json --pieces BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json --stage release

Then run the existing Smart Factory 13-feature gate and all relevant project tests. Neither gate replaces the other.

## Required handoff

Return:
1. PI and authority refs, plus exact source commit.
2. Human outcome and non-goals.
3. Preservation map.
4. Screen map and machine-readable interface brief.
5. Exact component manifest with provenance.
6. Implemented routes and actions, including what remains unimplemented.
7. Test commands, raw results, viewport screenshots, and accessibility/performance evidence.
8. Independent reviewer and frozen commit.
9. Known limitations, blockers, corrective owner, and next decision.
10. Learning candidate and evidence for or against promotion.

## Stop conditions

Stop the affected work and report a concrete blocker when:
- current PI or governing contract is missing or contradictory;
- a required part ID cannot be resolved;
- data source, permission, or actor authority cannot be established;
- the UI would imply a false live, saved, sent, approved, secure, or complete state;
- a critical action lacks a real capability or recovery path;
- a responsive or accessibility blocker prevents the primary journey;
- a requested change would alter ratified law without the Human Director's decision.

Do not stop unrelated safe work. Route the blocker to its actual owner and continue bounded independent work.

## Final law

**Build for the human. Preserve the truth. Reuse the best parts. Prove the experience. Learn only from evidence.**
