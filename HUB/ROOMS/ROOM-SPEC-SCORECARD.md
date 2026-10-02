# 🔱 Hub Specification Scorecard — Room-Functionality Audit

**Audit type:** Naya design/specification audit — not runtime proof  
**Source main inspected:** `5885459af85bcbaede4480557413ae9c681028a1`  
**Date:** 2026-10-01  
**Target:** 10/10; <9.0 remains an active gap.

## Scorecard

| Dimension | Main before room-spec pass | Proposed with this branch | Why |
|---|---:|---:|---|
| Product / human intent | 9.8 | 9.8 | Purpose and journey are exceptionally clear. |
| Visual / art direction | 9.4 | 9.4* | Strong canonical contract; #1281 separately proposes the final art-direction layer. |
| Design-system coherence | 9.5 | 9.5 | Living Depth, Spectrum, Board, Icon, Button, Liveness laws are coherent. |
| Primary information architecture | 8.5 | 9.4 | Canonical 11 rooms are clear; #1278's 13-room rail divergence is now explicitly classified and reconciled in the spec. |
| Room purpose clarity | 8.9 | 9.8 | Each room now has one human question and one signature metaphor. |
| Room functional depth | 6.2 | 9.5 | Previously mostly one-paragraph descriptions; now controls, views, states, runtime ownership and acceptance are explicit. |
| Cross-room coherence | 7.4 | 9.6 | Handoffs and canonical-object identity are now specified. |
| Causal action specification | 7.2 | 9.4 | Primary actions are enumerated with real-runtime / honest-state constraints. |
| Truth / governance / authority | 9.6 | 9.7 | Provenance, receipts, consent and capability≠authority are preserved. |
| Machine readability | 8.8 | 9.7 | Adds a deterministic 11-room machine contract. |
| Implementation readiness | 7.4 | 9.3 | Builders now know what each room contains and what proves it; runtime/API details still need implementation-specific contracts. |

**Composite before:** ~8.4/10  
**Composite proposed after this room-spec pass:** ~9.5/10

* If #1281 independently passes and merges, the art-direction layer would likely move this audit's visual/specification score closer to the target, but that PR is not assumed merged here.

## Why this still is not 10/10

The specification can become near-complete before the product is.

Remaining evidence needed for a true 10:
- independent room-spec review;
- reconciliation of #1278 against the canonical 11-room IA;
- concrete runtime operation/API bindings;
- data schemas/query contracts where each room needs them;
- visual mock/build evidence for each room;
- accessibility proof;
- performance budgets/results;
- end-to-end causal-path tests;
- Human Director experience acceptance.

## Most important conclusion

The next major specification frontier is no longer “what is a Hub?”

It is:

**ROOM CONTRACT → RUNTIME CONTRACT → BUILD → PROVE**

Each room should be designed and qualified as its own masterpiece, but built from shared primitives and the same governed substrate.
