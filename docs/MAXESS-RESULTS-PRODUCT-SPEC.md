# MAXESS Results — Consolidated Product Specification

Status: CLEAN-REPO WORKING SPEC
Purpose: Consolidate the durable product requirements from the original MAXESS Results specifications into one execution-friendly document.

## 1. Product definition

MAXESS Results is a personal AI mastery report and guided experience.

Assessment calculates.
Results interprets.
Naya guides.
NayaNET provides the larger ecosystem.

The experience transforms:

DATA → INSIGHT → UNDERSTANDING → ACTION → CAPABILITY

The user should feel:

“Naya has looked at my results, understands what they mean, and is showing me what I should do next.”

## 2. Psychological journey

REVEAL → UNDERSTAND → RECOGNIZE → FOCUS → ACT

Do not reverse this order. Give meaningful interpretation before heavy commercial asks.

## 3. Page architecture

Preferred journey:

1. Your AI Score / Orb
2. Naya Arrival
3. Your Report
4. Your Five Dimensions
5. Pattern
6. What It Means
7. Your Strength
8. Your Biggest Lever
9. Your Next Move
10. 18 Naya Masters
11. Playground / Practice
12. NayaNET continuation / ending

The exact existing page may preserve additional validated content where it earns its place. Do not delete valuable functionality simply to match a numbered outline.

## 4. Hero

The score and Orb are the dominant visual relationship.

The score must be real, centered, readable, and immediately understood as the user's MAXESS score.

Avoid hero clutter, competing headlines, duplicate scores, and premature sales messaging.

## 5. Naya

Opening:

“Hi. I’ve looked at your results.”

“This isn’t your judgment. It’s your map.”

Primary CTA:

LISTEN TO NAYA

There should be one primary Listen control.

Naya must interpret rather than recite. She explains meaning, pattern, strength, lever, and next move.

## 6. Five dimensions

Current dimensions:

- Direction
- Communication
- Evaluation
- Iteration
- Systems Thinking

Each dimension requires real data, score, meaning, behavioral interpretation, and practical opportunity.

Preferred presentation: five subordinate MAXESS-style orbs/gauges that visually belong to the primary Orb system. They should be interactive and provide/focus the relevant explanation.

Never display unexplained numbers.

## 7. Pattern

The pattern should reveal relationships between the five dimensions rather than merely repeat their scores.

Interaction may highlight selected dimensions and relevant relationships.

The visual must remain understandable to a non-technical person.

## 8. Personalized report

The report is a real narrative, not a statistics list.

Required content:

- overall result;
- mastery stage;
- overall pattern;
- strongest capability;
- highest-leverage opportunity;
- plain-language meaning;
- practical next action;
- invitation to improve.

It should feel like a premium modern personal document that is worth saving.

## 9. Strength

Show the user's strongest capability and explain why it matters and how to use it.

Desired feeling:

“I already have something valuable here.”

## 10. Lever

Identify the highest-leverage improvement area dynamically from the result.

Frame it as an opportunity, not a judgment.

Concept:

Protect your strength. Build your lever.

## 11. Next move

Give concise practical direction. Prefer a small number of high-value actions over a generic list.

The user should know exactly what to do next.

## 12. 18 Naya Masters

Preserve all validated pathways/content. Personalize ordering/relevance where the current data model supports it.

They should feel like the doors that make the most sense for this person, not an arbitrary library dump.

## 13. Playground

The Playground is where insight becomes practice.

Understand → Decide → Practice

Keep it toward the end of the Results journey.

## 14. Growth philosophy

MAXESS is for people who do not want mediocre results from AI.

The positioning is aspirational, not elitist:

Exceptional AI results are not accidental. Better results come from better thinking, better direction, better evaluation, and continuous improvement.

Value precedes conversion.

## 15. Data integrity

Production architecture:

Assessment → Result Contract → Results renderer

The Results page must consume `window.MAXESS_RESULT` and must not become a second scoring engine.

Missing/invalid data must fail safely rather than silently creating a fake result.

## 16. Responsive quality

Desktop should use the available viewport intelligently and should not feel like an enlarged phone layout.

Mobile should be genuinely responsive, readable, touch-friendly, and focused.

Test desktop, tablet, and mobile.

## 17. Accessibility

Keyboard focus, semantic headings, readable contrast, touch targets, accessible labels, reduced-motion compatibility, and non-color-only communication are required where applicable.

## 18. PDF

The PDF is part of the product, not an afterthought.

Use dedicated print/PDF styling and intentionally control pagination. The report should read as an intentional document with good hierarchy and page composition.

Actual PDF generation and inspection are required before release verification.

## 19. Technical quality

Use clear component boundaries:

Data bootstrap → normalization → derived insights → renderers → assembly → interactions → QA.

Avoid giant opaque template renderers, duplicate IDs, duplicate result sources, repeated listeners, DOM mutation loops, stale generators, and uncontrolled patch layers.

## 20. Definition of excellence

Premium · human · intelligent · personal · clear · beautiful · useful · calm · intentional

The final experience should make the user think:

“Now I understand where I am.”

“Now I understand why.”

“Now I know what to improve.”

“Now I know what to do next.”

“I want to get better at this.”
