# System 59 — Why Naya Explanation V1

The Hub now exposes a concise **WHY NAYA** layer for an intelligence object.

It answers only evidence-bearing questions:

- **What Naya used** — source, context, and recorded tags.
- **What Naya understood** — recorded observation/interpretation.
- **Why it matters** — recorded meaning/significance.
- **What Naya recommends** — recorded action/recommendation.
- **What is verified** — trust, verification state, and authority state.
- **What remains uncertain** — recorded uncertainty.

This is an explanation/provenance surface, **not hidden chain-of-thought**. It never invents missing reasons; absent fields become explicit "not recorded" statements.

Implementation: `NAYANET/HUB/src/intelligence/whyNaya.ts`, rendered by `SmartFeedBoard.tsx`.

Verification gate: TypeScript compilation plus production Vite build.