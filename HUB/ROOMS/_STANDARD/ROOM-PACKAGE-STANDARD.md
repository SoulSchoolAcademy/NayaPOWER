# 🔱 Room Package Standard V1

Every primary Hub room uses the same documentation architecture so humans, Nayas, AI builders and machines can review one meaning without creating competing truth.

## Required files

```
<room>/
├── README.md
├── FUNCTIONAL-SPEC.md
├── DESIGN-CONTRACT.md
├── SPEC.HUMAN.md
├── SPEC.AI.md
└── SPEC.MACHINE.json
```

## Authority order

1. Parent Hub contracts: `HUB/PROJECT-INTELLIGENCE.md`, `HUB/DESIGN-CONTRACT.md`
2. Room `FUNCTIONAL-SPEC.md`
3. Room `DESIGN-CONTRACT.md`
4. Machine projection
5. AI projection
6. Human projection

The lower representations should be easier to consume, not more authoritative.

## Functional spec must answer

- What human problem owns this room?
- What is the signature job?
- What data/runtime owns truth?
- What are the actual controls?
- What are the states?
- What are the causal paths?
- How does the room hand off to other rooms?
- What happens on mobile?
- What proves acceptance?

## Design contract must answer

- What should entering the room feel like?
- What is the unique composition?
- What is the room's primary instrument?
- What is the hierarchy?
- How does living depth / spectrum / iconography appear?
- Which elements must never become generic?
- What is the motion behavior?
- How do empty/error/blocked states stay beautiful?
- What may not regress?

## Human projection

Explain:
- what the room is;
- why it matters;
- what the human sees;
- what the human can do;
- how it connects to the rest of the Hub.

## AI projection

Tell a cold builder:
- intent;
- preserved design DNA;
- composition;
- components;
- data;
- states;
- controls;
- causal paths;
- anti-patterns;
- tests;
- proof.

## Machine projection

Encode:
- IDs/routes;
- semantic layers;
- components;
- controls/actions;
- states;
- data owner;
- handoffs;
- design tokens/theme;
- gates;
- status/version.

## Shared five layers

Every room maps to:

`ORIENTATION → CURRENT_STATE → INTELLIGENCE → ACTION → PROOF`

The Naya layer can span all five.

## Review

All room packages are reviewed on PR #1290. Material not-right findings also go to Issue #554 with evidence.
