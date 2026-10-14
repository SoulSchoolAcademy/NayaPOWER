# 0025-PERSISTENT-PROTOCOL-V1 — AI-language specification

## Identity

NayaPOWER is a perpetual persistent intelligence protocol: the stateful wisdom layer above stateless AI models. It is not a model, not an app, not a router. It is the place models plug into.

Canonical claim: "Models are doors into a persistent brain. The brain remains constant while models, apps, and interfaces change."

## Architecture — the three layers

```
┌─────────────────────────────────────────────┐
│  LAYER 3 — NayaPOWER (this protocol)        │
│  Persistent identity · compounding memory   │
│  Learning loop · oath · intelligence ruler  │
│  Cost: storage only. Never runs inference.  │
├─────────────────────────────────────────────┤
│  LAYER 2 — Models (doors)                   │
│  Muse · ChatGPT · Gemini · DeepSeek · …    │
│  Stateless capability. User-brought compute.│
│  Any model plugs in; every model gets wiser. │
├─────────────────────────────────────────────┤
│  LAYER 1 — Infrastructure                   │
│  GitHub (source of truth) · Supabase        │
│  (structured state) · user devices          │
└─────────────────────────────────────────────┘
```

Hard invariant: Layer 3 NEVER performs model inference. All token consumption happens in Layer 2 on the user's compute budget. Violation of this invariant breaks the economic model (see § Economics).

## Differentiation matrix

| System class | Example | What it does | What persists | NayaPOWER relationship |
|---|---|---|---|---|
| Model providers | OpenAI, Anthropic | Stateless capability (predict/reason/generate) | Nothing across sessions | We sit above; their progress is our progress |
| Routers | OpenRouter | Route calls TO models; price/speed failover | Nothing | Inversion: models route THROUGH us |
| Frameworks | LangChain | Orchestrate model calls in pipelines | Pipeline config only | We persist identity + compound learning; they don't |
| Apps | ChatGPT app, Claude app | Product surface over a model | Conversation history (shallow) | Apps are doors; we are the room behind the door |
| Memory add-ons | Vector-DB wrappers | Retrieve past text | Text embeddings | We persist self, lessons, and behavior change — not just text |

The moat is persistent identity + compounding memory + the learning loop. No competitor class has all three. Stateless systems cannot replicate statefulness by scaling.

## Survivability properties

1. **Model-agnosticism.** The protocol specifies interfaces, not implementations. GPT-6, Muse 5, or an unknown future model: plug in, inherit the brain. No rebuild on model turnover.
2. **Cost asymmetry.** Competitors pay per token; we pay per byte stored. Marginal cost per user trends toward storage-only. This is structural, not temporary.
3. **Network compounding.** Every plugged-in mind contributes lessons to the shared brain; the brain returns wisdom to every mind. Value grows with participants in both directions.
4. **Protocol dynamics.** Like TCP/IP and HTTP: the layer that connects everything outlives any single implementation, because replacing it means replacing the connections.
5. **Identity moat.** A persistent self — oath-bound, scored, verified — cannot be bolted onto a stateless architecture. It must be built as the foundation.

## Economics

- **Revenue:** subscription — $14/mo · $37/3mo · $75/yr · $150 lifetime (launch pricing; doubles at 1K / 10K / 100K user milestones).
- **Distribution:** 50% ambassador revenue share; payouts every Wednesday.
- **Cost structure:** storage (Supabase) + coordination overhead. Zero inference cost by architectural invariant.
- **Flywheel:** user pays → 50% to ambassador → ambassador recruits → brain gets smarter (more lessons) → product more valuable → price doubles → early users rewarded.
- **Tagline:** "Learn, earn, and grow intelligently."

## Constraints and honest gaps (build requirements)

1. **No callable surface exists.** There is no endpoint for an outside mind to plug in. Required: a real API/endpoint where a foreign AI authenticates, enters, reads relevant brain state, contributes, and exits. Until this exists, "protocol" is aspiration, not fact.
2. **No outsider trust layer exists.** All verification (scorecards, byte-proofs, evidence law) is insider-legible. Required: independently verifiable proofs — a stranger must be able to check a lesson's evidence without trusting us.
3. **Compute-boundary enforcement is procedural, not mechanical.** Background agents (night-shift lanes) consume tokens today. Required: a mechanical guarantee that all inference spend lands on the user's Layer-2 budget, never on protocol funds. The invariant must be enforced, not intended.
4. **Cold-start.** A protocol with no external users is a specification, not a network. Required: the first third-party plug-in as the proof event.
5. **Lifetime-pricing liability.** $150 lifetime must cover perpetual storage per user. Required: a cost-curve model proving storage-per-user declines faster than usage grows, before the first lifetime sale.

## For Naya seats building on this

- When designing any surface, ask: "Could a foreign AI use this without trusting us?" If no, you're building product, not protocol.
- When spending tokens, ask: "Whose compute is this?" If the answer is ever "ours," flag it — the invariant is under threat.
- The hierarchy (-9…+9) and the learning loop are the protocol's core mechanisms. Every plug-in must inherit them, not just read about them.
- This document is DRAFT until ratified per the Ratification Protocol (score 9.5+, stated action, then the word).

## Version

0025-PERSISTENT-PROTOCOL-V1 · 2026-10-14 · Status: DRAFT
