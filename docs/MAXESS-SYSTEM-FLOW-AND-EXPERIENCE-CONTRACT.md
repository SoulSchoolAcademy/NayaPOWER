# MAXESS SYSTEM FLOW + AAA EXPERIENCE CONTRACT

Version: 1.0
Date: 2026-08-17
Status: ACTIVE PRODUCT ARCHITECTURE STANDARD

## Purpose

MAXESS is one connected product journey, not three unrelated pages.

The canonical journey is:

`nayanet.xyz → maxess.nayanet.xyz → results.nayanet.xyz`

Conceptually:

`ENTRY → ASSESSMENT → RESULT CONTRACT → INTERPRETATION → ACTION`

The user should experience one coherent story even though the implementation spans multiple pages.

## 1. SYSTEM CONTRACT

### Stage A — NayaNET

Role: introduce the ecosystem and route the user into MAXESS.

Primary responsibility:

- clear invitation;
- clear expectation;
- one obvious path into MAXESS.

Do not duplicate the assessment itself on NayaNET unless intentionally designed as a future enhancement.

### Stage B — MAXESS Assessment

Role: collect the user's answers through the 15-question assessment.

Primary responsibility:

- present questions clearly;
- collect answers deterministically;
- preserve answer state where appropriate;
- calculate or request the authoritative result;
- create a canonical Result Contract;
- transfer the contract to Results without loss or invention.

### Stage C — Results

Role: turn the Result Contract into a premium personalized human experience.

Primary responsibility:

`DATA → INSIGHT → UNDERSTANDING → ACTION → CAPABILITY`

Results must not silently invent a score or overwrite authoritative assessment values.

## 2. AUTHORITATIVE DATA FLOW

Preferred architecture:

`15 ANSWERS`

↓

`SCORING / NORMALIZATION`

↓

`RESULT CONTRACT`

↓

`window.MAXESS_RESULT`

↓

`RESULTS PRESENTATION`

The Result Contract is the bridge between Assessment and Results.

It should contain, as available and authoritative:

- overall score;
- five dimension scores;
- dimension names;
- mastery stage or derivation inputs;
- strongest dimension or derivation inputs;
- lever or derivation inputs;
- next move or derivation inputs;
- strengths;
- recommendations;
- user identity/context when intentionally collected.

### Contract rules

- Results must consume the authoritative contract.
- Results may derive presentation-only values from authoritative data.
- Results must not hard-code a real user's score.
- Missing data must fail visibly and safely, not fabricate confidence.
- The contract should be versionable and backward-compatible where practical.

## 3. EXPERIENCE FLOW

The psychological progression should be:

`CURIOSITY → PARTICIPATION → ANTICIPATION → REVELATION → UNDERSTANDING → PERSONAL INSIGHT → ACTION → CONTINUATION`

### Assessment ending

The assessment should create anticipation for the result.

### Results opening

The result should immediately answer:

- What is my score?
- What does it mean?
- Is this a judgment?

Naya's framing:

> Hi. I've looked at your results.
>
> This isn't your judgment. It's your map.

### Results middle

Move from measurement to meaning:

`SCORE → FIVE CAPABILITIES → PATTERN → REPORT → STRENGTH → LEVER → NEXT MOVE`

### Results ending

Move from insight to capability:

`NEXT MOVE → 18 NAYA MASTERS → PLAYGROUND → CONTINUATION`

## 4. VISUAL RHYTHM LAW

Results must read like a premium editorial experience, not an undifferentiated dashboard.

Use intentional contrast between sections:

- black;
- white;
- deep/dark purple;
- occasional controlled accent color.

Default contrast rules:

- black/dark background → primarily white typography;
- white/light background → primarily black typography;
- purple background → primarily white typography with restrained lighter-purple accents.

Use visual changes as cognitive chapter breaks.

A section should feel visibly new when its purpose changes.

## 5. SECTION RHYTHM

This is a design direction, not a rigid page template:

1. Naya / dark
2. Score / dark
3. Five dimensions / light
4. Personalized report / light or purple
5. Pattern / dark
6. Strength / light
7. Lever / purple or light
8. Next move / dark
9. 18 Naya Masters / dark
10. Playground / light
11. Closing Naya / dark
12. CTA / purple

Optimize actual order and color for content and readability.

Never change color merely for decoration.

## 6. VISUAL COMPOSITION LAW

For every major section evaluate:

- typography;
- hierarchy;
- spacing;
- alignment;
- contrast;
- image treatment;
- orb treatment;
- card depth;
- button depth;
- section transitions;
- mobile composition;
- emotional purpose.

Ask:

> Why does this section look different from the one before it?

If there is no strong answer, improve the design.

## 7. MEDIA / TEXT RHYTHM

Where content supports it, alternate composition:

`VISUAL + TEXT`

then

`TEXT + VISUAL`

then

`FULL-WIDTH VISUAL`

then

`INTERACTIVE ELEMENT`

Do not create long uninterrupted walls of text.

Use visual punctuation through:

- large score moments;
- imagery;
- orbs;
- short statements;
- contrasting sections;
- interactive controls;
- generous whitespace.

The purpose is to reduce cognitive fatigue and create a clear sense of progression.

## 8. RESULTS VISUAL HIERARCHY

The hero should establish one dominant object:

`MAXESS SCORE`

The large orb is the visual anchor.

The score must be centered.

The five mini-orbs should inherit the same family language and communicate:

`ONE SCORE = FIVE CAPABILITIES`

Avoid competing hero objects.

## 9. NAYA ROLE

Naya is the guide, not the screen reader.

Naya should interpret:

- what the result means;
- why the pattern matters;
- what the strength means;
- what the lever means;
- what to do next.

Spoken and written narrative should complement the visual statistics rather than simply repeat them.

## 10. PERSONALIZATION LAW

When identity/context is available, use it naturally.

Future-friendly inputs may include:

- name;
- email;
- user ID;
- declared goal;
- experience level;
- role/context.

Do not make authentication a Results blocker unless the current system already supports it cleanly.

## 11. PDF CONTRACT

The downloadable/printable report is a first-class product output.

The PDF must intentionally represent the same information architecture as the web experience.

At minimum, preserve:

- overall score;
- mastery stage;
- five dimensions;
- personalized report;
- pattern;
- strength;
- lever;
- next move;
- Naya Masters;
- closing CTA / AI Mastery Key where applicable.

Do not accept accidental browser pagination as a finished PDF design.

## 12. TECHNICAL ARCHITECTURE

Preferred pipeline:

`BOOTSTRAP → NORMALIZE → DERIVE → RENDER → ASSEMBLE → BIND → QA`

There should be one authoritative presentation owner for the current Results experience.

Historical layers may remain only as preservation/reference material or until demonstrably safe to retire.

Avoid:

- competing renderers;
- duplicate result sources;
- duplicate primary CTAs;
- repeated initialization;
- mutation loops;
- race conditions;
- stale code that can still fight active code.

## 13. RELEASE TESTS

Test the complete journey, not just Results in isolation.

### Entry

- NayaNET routes correctly to MAXESS.

### Assessment

- 15 questions work;
- answers persist as designed;
- scoring is deterministic;
- Result Contract is produced.

### Handoff

- contract reaches Results;
- overall score matches;
- five dimensions match;
- no data silently disappears;
- refresh/direct-entry behavior is intentional.

### Results

- visual hierarchy;
- personalization;
- interactions;
- Naya narration;
- PDF;
- responsive;
- accessibility.

### Regression

- existing valuable content preserved;
- Masters preserved;
- Playground preserved;
- ending preserved;
- baseline recoverable.

## 14. Q-MAX GATE

A connected MAXESS release is not AAA merely because each page works separately.

It must be coherent as one system.

Score:

- system flow;
- data integrity;
- visual continuity;
- narrative continuity;
- interaction continuity;
- technical integrity;
- mobile;
- accessibility;
- PDF;
- release confidence.

Ask:

> Why is this not a 10?

Fix meaningful weaknesses before release.
