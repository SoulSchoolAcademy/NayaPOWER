# Maxis — "What's Your Naya Power Score?"

A dynamic assessment engine for NayaNET. Teach → test → report: each
question teaches a micro-lesson first (the IN A NUTSHELL pattern), then
tests with five answers on a hidden 0–4 mastery scale, normalized to 0–100.
The report is the living orbital score orb: count-up number, five dimension
gauges, Naya's read, biggest opportunity, and next steps.

## Two surfaces

| File | Surface | Audience |
|------|---------|----------|
| `index.html` | Full app: assessment + saved history (localStorage) | NayaNET members |
| `public.html` | Teaching hero ("What's your Naya Power score?") → assessment → report → **Enter NayaNET** + **Order Naya Power** CTAs | Public / outside NayaNET |

## Question banks (data, not code)

The engine renders any bank in `banks/`. A bank is a JS file that sets
`window.MAXIS_BANK`:

```js
window.MAXIS_BANK = {
  id: "naya-power", version: "1.0.0",
  title: "Naya Power Assessment",
  dimensions: [{ id, name, color, weight }],   // 5 recommended
  scoreBands: [{ min, max, label, color, description }],  // 4
  questions: [{                               // exactly 15, unique ids
    id, dimensionId, order, label,
    teaching,   // micro-lesson shown BEFORE the question
    question,
    answers: [  // 5 answers, positions deliberately NOT ordered by value
      ["answer-id", "Title", "Description", score0to100, "#color", "glyph"],
      ...
    ]
  }],
  interestAreas: [...],  // exactly 18 (3 boards × 6) for the interests step
  interestsTitle: "..."
};
```

Answer scores are hidden from the taker. The 0–4 mastery scale normalizes
as `value/4*100` (0/25/50/75/100). To add a new assessment, drop a new bank
file in `banks/` and point a page at it — no engine changes.

The engine (`js/maxis-engine.js`) is Shawn's proven quiz logic, refactored
so the bank loads as data. Scoring, flow, and validation are untouched.

## Voice — Naya reads each question

Naya's voice narrates the quiz through the **canonical** voice interface
only: `../app/js/naya-voice.js` (`NayaVoice.speak(text)` /
`NayaVoice.stop()`). No raw `speechSynthesis` anywhere in this app.

- Each question has its own play control ("Listen to Naya") that speaks
  **that question's** text. New speech cancels the old — no overlap.
- Navigating away (next question, interests, reset, Escape) stops audio —
  sound never bleeds across questions.
- Honesty (SN-0502): the voice label renders under the control. Tier 1
  reads **SYNTHESIZED VOICE** until her true cloned voice lands via
  `NayaVoice.setProvider()` — at which point the label updates with zero
  control changes.
- If the voice interface fails to load, the play control hides instead of
  sitting dead.

## Configuration

```js
window.MAXIS_CONFIG = {
  enterNayanetUrl: "../app/index.html",  // "Enter NayaNET" destination
  orderUrl: ""                           // "Order Naya Power" checkout
};
```

`orderUrl` is intentionally empty until a real checkout exists: the button
renders "Coming soon" and the engine no-ops rather than inventing a fake
checkout. Set it to go live.

## Design

Black obsidian ground everywhere. Elevated always — no flat buttons, boards,
or answers. White/silver voice, jewel accents, purple ignition. Mobile-first,
44px+ targets, `prefers-reduced-motion` respected.

## Screenshots

`screenshots/` holds verified renders: quiz, teaching interstitial, report
(orb, dimensions, insights, CTA), and the public hero.
