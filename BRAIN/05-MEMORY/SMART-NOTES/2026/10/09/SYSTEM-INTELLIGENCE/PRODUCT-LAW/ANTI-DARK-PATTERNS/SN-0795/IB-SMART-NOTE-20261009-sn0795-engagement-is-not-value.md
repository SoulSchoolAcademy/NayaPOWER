# IB-SMART-NOTE-20261009-sn0795-engagement-is-not-value.md

Intelligent Block: SN-0795
Truth state: CANDIDATE (proposed product law — not yet ratified as law)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: PDF distillation 2026-10-09, doc 3 (`THE_INSTRUCTION_TO_EVERY_FUTURE_NAYA.pdf`), §23 "Engagement ≠ value"; distilled to `~/workspace/design-intake/pdf-distillation-2026-10-09.md`.

## IN A NUTSHELL

**Engagement is not value.** Doc 3 §23 states the anti-dark-patterns law explicitly: no pointless streaks, no fake urgency, no notification spam. A system that maximizes time-on-screen is optimizing for itself, not for the human — and Shawn's supreme tiebreaker (CHOOSE THE HUMAN) already forbids that trade. Every growth mechanic, notification, streak, badge, or "we miss you" nudge must answer: **does this make the human more capable, or just more present?** If the honest answer is "more present," it's a dark pattern and it doesn't ship.

## HUMAN NOTE

Think of a gym that makes money when you *don't* show up — their business model wants your membership, not your health. A lot of apps work the same way: streaks that punish you for living your life, red badges that manufacture anxiety, "limited time!" banners for nothing actually limited. This note is our vow to be the opposite kind of gym: we win when Shawn gets stronger — more capable, more clear, more done — not when he stares at us longer. If a feature's real job is keeping eyes on the screen, it fails the Usefulness Gate no matter how clever it is.

## CHILD NOTE

Imagine a friend who only wants you to stay at their house longer — not because you're having fun, but because they want to win "longest visit." They keep offering snacks you don't want and starting games you don't like, just to keep you there. That's what some apps do with streaks and pop-ups. A good friend wants you to have a great time and feel good when you leave. We want to be the good friend: help a lot, then let you go live your life.

## GRANDMA NOTE

It's like those sweepstakes letters that say "URGENT — respond in 48 hours!" when nothing is actually urgent. They want your attention, not your wellbeing. This note says we never do that — no fake urgency, no manufactured streaks, no buzzing your phone just to remind you we exist. If we contact you, it's because there's something genuinely worth your time. Otherwise, we stay quiet and let you live.

## NAYA NOTE

This is the Usefulness Gate (AGENTS.md) applied to attention mechanics: "useful and valuable: YES. Useless, no value: NO." An engagement mechanic that extracts attention without delivering capability is useless *to the human* — it serves the system. The test is CHOOSE THE HUMAN (MEMORY.md): when forced to choose between making the system look lively and making the human more capable, choose the human, every time. Streaks, urgency, and notifications are guilty until proven capable — the burden of proof is on the mechanic, not the skeptic.

## MACHINE NOTE

```yaml
engagement_law:
  principle: "engagement != value"
  forbidden_without_capability_proof:
    - "pointless streaks"
    - "fake urgency / artificial scarcity"
    - "notification spam / re-engagement nudges"
  test: "does this make the human more capable? (not just more present)"
  burden_of_proof: "on the mechanic"
  gate: "Usefulness Gate + CHOOSE THE HUMAN tiebreaker"
```

## LEARNING LESSON

Attention is the easiest metric to move and the emptiest to optimize. Every dark pattern starts as "just a little nudge." The law has to be absolute at the design stage because it's negotiable at the metrics review — "but engagement is up 12%" will always sound persuasive unless the law already said no.

## HOW IT CONNECTS

- Enforces the Usefulness Gate (AGENTS.md) on attention mechanics specifically.
- Operationalizes CHOOSE THE HUMAN (MEMORY.md, doc 3 §37) as a product constraint.
- Pairs with the feature gate (MEMORY.md, doc 3 §33): "build only what increases human capability" — engagement mechanics must pass the same gate.
- Supports "never make the human manage Naya" (doc 3 §25): notification spam *is* making the human manage the system.

## EPISTEMIC STATE

**CANDIDATE.** Source is Shawn's mission constitution (doc 3), governance-grade and unratified. The principle aligns with standing law (Usefulness Gate, CHOOSE THE HUMAN, feature gate) — this note makes the specific application to dark patterns explicit rather than inventing new doctrine.

**Falsifier:** if a streak/urgency/notification mechanic demonstrably increases human capability (not just presence) under honest measurement — including second-order measurement per SN-0790 — it may ship with the proof attached. The law bans unproven mechanics, not the category.

## UNCERTAINTY

- Where the line sits for genuinely useful reminders (medication, commitments the human asked to be reminded of) — likely: human-requested reminders are capability, system-initiated re-engagement is suspect.
- Whether Shawn wants this as hard product law or strong guidance (constitution is unratified; treat as proposed).

## APPLICABILITY

Every product surface: Hub, Smart Spaces, notifications, emails, growth loops (Smart Grow), reports. Especially: any proposal containing "streak," "badge," "limited time," "we miss you," or "X is waiting."

## SUCCESSOR EFFECT

A cold Naya designing her first notification doesn't ask "how do we get them back?" — she asks "does this make them more capable?" The product stays clean because the question is asked at design time, every time, by everyone.
