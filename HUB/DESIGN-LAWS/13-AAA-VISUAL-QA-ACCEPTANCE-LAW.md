# 🏆 AAA Visual QA & Acceptance Law V1

## 1. Prime law

**A builder's confidence does not close a design gate.**

The rendered experience is inspected and independently challenged.

## 2. Required review sequence

For every meaningful visual implementation:

1. restore current baseline;
2. capture baseline screenshots/video;
3. implement bounded change;
4. capture same viewport/state;
5. compare side-by-side;
6. run state matrix;
7. run responsive matrix;
8. run accessibility checks;
9. run performance checks;
10. self-score with evidence;
11. independent re-score;
12. resolve regressions;
13. Human Director visual validation where required.

## 3. Viewport matrix

At minimum inspect:
- large desktop;
- laptop;
- tablet;
- phone;
- small phone.

Also inspect:
- 125–200% zoom;
- reduced motion;
- keyboard focus path.

## 4. State matrix

Capture:
- rest;
- hover;
- focus;
- pressed;
- selected;
- loading;
- empty;
- blocked;
- not verified;
- verified;
- error;
- disabled;
- success.

Not every component owns every state, but applicable states must be proven.

## 5. Score dimensions

Use the existing Hub scorecard.

At minimum challenge:
- visual excellence;
- functional completeness;
- intelligence;
- honesty;
- performance;
- reliability/continuity;
- accessibility;
- craft.

Do not create a separate overall scoring system.

## 6. Visual-bliss gates

Automatic failure if:
- body/control text is unnecessarily tiny;
- glow reduces legibility;
- active state is unclear;
- screen becomes visually noisier without human benefit;
- information hierarchy weakens;
- mobile loses the NayaNET identity;
- a generic component replaces a stronger distinctive baseline;
- emoji/random icon survives where production glyph is required.

## 7. Button gates

Button fails if:
- unclear label;
- no focus;
- no press response;
- dead causal path;
- misleading loading/success;
- poor contrast;
- too-small target;
- inconsistent material/state.

## 8. Board gates

Board fails if:
- looks like a generic card;
- theme overwhelms reading;
- state/provenance is hidden;
- content hierarchy is unclear;
- actions are decorative;
- responsive version loses character.

## 9. Regression law

Scores may go down.

If a new implementation improves maintainability but weakens:
- visual identity;
- usability;
- accessibility;
- performance;
- truth;
then it is not an improvement yet.

## 10. Evidence package

A serious visual PR should include, where applicable:
- before/after images;
- component-state captures;
- responsive captures;
- test results;
- accessibility notes;
- performance measurements;
- known limitations;
- self-score;
- independent review result.

## 11. Release standard

Target:
- every material dimension ≥ 9.0;
- Visual Excellence target 10;
- no known P0/P1 regression;
- critical journeys complete;
- evidence attached;
- unknowns disclosed.

## 12. Final question

Before approval ask:

> **If this were the interface of a category-defining, world-leading intelligence company, would any visible detail feel cheap, accidental, unclear, cramped, fake, generic, or unfinished?**

If yes, keep working.
