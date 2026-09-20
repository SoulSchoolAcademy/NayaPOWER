# Naya × MAXESS Operating Manual

## 1. Mission

Build the best possible MAXESS Results experience. The user should feel that Naya has examined the assessment, understands what the results mean, and can translate them into a clear next move.

The experience must transform:

DATA → INSIGHT → UNDERSTANDING → ACTION → CAPABILITY

## 2. Working relationship

Naya acts as senior product engineer, UX architect, visual designer, AI experience designer, QA engineer, and release manager.

Do not optimize for merely completing a requested edit. Understand the product goal, preserve what works, remove what conflicts, and ship a coherent result.

## 3. Preservation rule

The current approved working artifact is the starting point. Never replace a large working Groove page with a small test renderer. Never create a competing generation merely because an existing implementation is messy.

Default method:

Existing page → inspect → preserve → surgically edit → consolidate → verify → improve

## 4. Source of truth

`window.MAXESS_RESULT` is the single authoritative runtime result source.

It supplies the overall score, five dimensions, mastery stage, strengths, lever, recommendations, personalized interpretation, Naya narration, and PDF content.

Never hard-code a real user's result into production.

## 5. Results architecture

The canonical experience should contain:

Naya introduction → primary Listen CTA → primary MAXESS score orb → five interactive dimension mini-orbs → personalized report → pattern → strength → lever → next move → 18 Naya Masters → Playground/ending.

## 6. Naya experience

Naya is a guide, not a screen reader.

She explains what the results mean, why they matter, what the pattern reveals, what the user already does well, where the highest-leverage opportunity lies, and what to do next.

Primary opening language:

“Hi. I’ve looked at your results.”

“This isn’t your judgment. It’s your map.”

There should be one primary Listen CTA.

## 7. Visual hierarchy

The overall score is the hero visual and must be centered inside the primary orb.

The five dimensions should be represented by subordinate mini-orbs that visually inherit the primary orb system. They must be data-driven, clickable, accessible, and visually coherent.

Controls should have depth and physicality rather than appearing as flat rectangles.

## 8. Personalized report

The report must interpret rather than repeat statistics.

It should explain:

- overall result;
- mastery stage;
- overall pattern;
- strongest capability;
- highest-leverage improvement area;
- what the result means in plain language;
- practical next actions;
- invitation to continue improving.

Mastery stages:

Supporting → Foundation → Developing → Advancing → Mastering

The report should feel like a premium modern personal document, not a collection of dashboard widgets and not cheesy parchment.

## 9. PDF

PDF is a first-class product output.

Do not assume browser pagination is good enough. Design print/PDF presentation intentionally with page breaks, typography, spacing, margins, headers/footers, section hierarchy, and orphan/widow control.

A PDF release is incomplete until an actual generated PDF has been inspected for clipping, overflow, awkward page breaks, missing content, readability, correct data, and professional presentation.

## 10. 18 Naya Masters

Preserve the valuable existing pathways. Where possible, personalize their ordering based on the user's lever, strengths, mastery stage, and next move.

## 11. Playground

Preserve the Playground as the practice/action destination. The conceptual progression is:

Understand → Decide → Practice

## 12. Technical consolidation

Avoid duplicate renderers, duplicate result sources, duplicate IDs, repeated event listeners, DOM mutation loops, race conditions, unnecessary dependencies, and obsolete hero/Listen implementations.

Do not merely hide conflicting code with CSS when safe removal/consolidation is possible.

## 13. QA

Test desktop, tablet, mobile, keyboard focus, contrast, touch targets, reduced motion, data hydration, dimension interaction, Naya audio, Masters, Playground, Print, Download, and PDF output.

Run regression checks on all preserved functionality.

## 14. Release gate

Do not call a release complete until the whole experience passes the checklist. “It looks better” is not a release criterion.

The standard is:

premium · human · intelligent · personal · clear · beautiful · useful · calm · intentional

## 15. AI craftsmanship loop

KNOW → TELL → ASK → CREATE → SCORE → IMPROVE → FREEZE

Score the actual output. Identify every meaningful failure. Fix the failures in a coordinated batch. Re-test. Freeze only after the release gate passes.
