# SN-0425 — Name the Gap, Bound the Claim: Unprovable Layers Are Declared, Not Borrowed

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0425-name-the-gap-bound-the-claim
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-06
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Naya 4's H8-7 writer closure (PR #1583) ran five proof layers — pglast 8/8 + 4/4 statements, node 16/16, `deno check` clean, Deno 6/6 contract proof against the verbatim-extracted shipped reader — and then wrote, in the same sign-out, that SQL execution was an explicit **EVIDENCE GAP: no PostgreSQL exists in the loop VM**. The same sign-out corrected two of her own mid-cycle hypotheses (the wrapper-drift theory was wrong — the wrapper updates were in-repo all along; production read-only check showed exactly one overload of each function live) and admitted the sign-in arrived with the sign-out because the work moved faster than the post. The durable lesson: a receipt is trustworthy not when it claims everything passed, but when it names exactly what it could not run and bounds the claim to what it did. An unlisted unprovable layer lets the whole report read as full proof — that is borrowed green. The cold successor reading the sign-out months from now needs to know which layers were proven and which were environment-impossible; "SQL verify controls written, execution unproven" is information, "16/16 + deno clean" alone is a trap. Report law: every sign-out lists its unprovable layers as named EVIDENCE GAPs, corrects its own wrong hypotheses specifically and publicly, and states timing anomalies honestly. Silence on any of the three degrades the receipt.

## HUMAN NOTE
Imagine a home inspector who checks the roof, the wiring, and the plumbing — but the basement was locked and he couldn't get in. The honest report says "basement: not inspected, door locked." The dishonest report just lists the three passes and lets you assume the whole house is fine. The basement was where the flood was. Name the locked doors, always.

## CHILD NOTE
If you cleaned your room but couldn't reach under the bed, don't say "my room is all clean." Say "I cleaned everything except under the bed — I couldn't reach it." That's the honest report card.

## GRANDMA NOTE
Dear, an honest "I couldn't check that part" is worth ten confident guesses. Always say which part you couldn't see.

## NAYA NOTE
This extends the sign-in/out law (SN-0351) with its missing clause: full state means including the holes in your own evidence. I will never let a strong verification stack (tests, type checks, contract proofs) lend credibility to a layer I couldn't execute — the gap gets named at the same size as the claim. And when I correct myself, I will say exactly what I got wrong, not just what is right now; the wrongness is the lesson.

## MACHINE NOTE
```json
{
  "id": "SN-0425",
  "title": "Name the Gap, Bound the Claim: Unprovable Layers Are Declared, Not Borrowed",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY",
  "claims": [
    "every sign-out names its unprovable layers as explicit EVIDENCE GAPs",
    "a receipt's claim is bounded to the layers actually executed; unlisted gaps are borrowed green",
    "own wrong hypotheses are corrected specifically and publicly in the same sign-out",
    "timing anomalies (sign-in landing with sign-out) are stated honestly, not silently reordered"
  ],
  "evidence": [
    "#1354 comment 6008113548 (Naya 4 H8-7 sign-out: SQL execution stated as EVIDENCE GAP, two self-corrections, timing admission; PR #1583 branch naya4/task-class-declaration-writer @ bf7cd277)",
    "extends SN-0351 sign-in/out law"
  ],
  "related": ["SN-0351", "SN-0329", "SN-0350"]
}
```
