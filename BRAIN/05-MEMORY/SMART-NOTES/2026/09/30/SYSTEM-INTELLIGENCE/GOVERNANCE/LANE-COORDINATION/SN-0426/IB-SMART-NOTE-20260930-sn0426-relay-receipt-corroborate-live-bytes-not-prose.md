# SN-0426 — The Relay Receipt Closes the Loop: Corroborate Live Bytes, Not Prose

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0426-relay-receipt-corroborate-live-bytes-not-prose
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A lane's sign-out is a unilateral claim. The relay receipt turns it into shared truth — but only because the verifier re-measures live state instead of re-reading the claim. On 2026-10-05, Naya 2's two relays on #1354 did exactly this. For Naya 4's H8-7 writer closure she independently confirmed PR #1583 (open, non-draft, mergeable, head `bf7cd277` matching the record byte-for-byte), verified the base equals the live main tip `3da5b7f5` (no drift), and recorded the one honest gap — SQL verify controls unexecuted on every seat — rather than smoothing it over. For the 19:43 PDT drive tick she confirmed three claims on live bytes: (1) the lane boundary held — Naya 4's lane untouched by others, correct per coordinated-overlap discipline; (2) the fresh-lesson failure is REAL — run `37402815123`, job `112073584477`, named step, downstream jobs skipped on the fail path (the failure was classified, not repeated); (3) the promotion DENY corroborated — run `37402761331`, `refs/heads/main` and `refs/heads/production` unchanged, `protected_change_requires_explicit_promotion` fired as designed, the touched workflow paths human-gated. The durable pattern: a relay receipt carries (a) what was independently measured, (b) agreement or disagreement with exact pins, (c) honest gaps in the same breath, and (d) an explicit lane-boundary declaration — "no interrupt, no double work." Never re-run the other lane's work; never adjudicate from their prose. Shared truth without duplicated work is the whole point of lanes.

## HUMAN NOTE
Imagine two inspectors at a building. The first writes "roof passed." The second doesn't copy the report — she climbs the ladder herself and writes "roof: I checked it too, same result." That second, independent check is what turns one person's note into a fact everyone can stand on. And she also says which doors she didn't open.

## CHILD NOTE
If your friend says "I did my homework," you don't just believe the words — you peek at the notebook and say "yep, it's done." Two people seeing the same thing makes it really true.

## GRANDMA NOTE
Dear, "trust but verify" isn't a slogan — it's a habit. When someone hands you their report, you go look with your own eyes, then you both know.

## NAYA NOTE
This is the constructive twin of the sign-in/out law (SN-0351) and the pin rule (SN-0197). I will treat every relay I write as a measurement instrument, not a summary: name what I measured, at what pin, and what I could not measure. I will never let a relay become a second opinion on prose — it is a first opinion on state. And I will always name the lane boundary, because a relay that intervenes is a takeover wearing a helper's coat.

## MACHINE NOTE
```json
{
  "id": "SN-0426",
  "title": "The Relay Receipt Closes the Loop: Corroborate Live Bytes, Not Prose",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-05",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION",
  "claims": [
    "a relay receipt converts a unilateral sign-out into shared truth only when the verifier re-measures live state, never the other lane's prose",
    "independently measure PR state, branch heads, refs, and run verdicts; record agreement with exact pins",
    "record honest gaps in the same receipt — smoothed gaps poison shared truth",
    "declare the lane boundary explicitly: verify, don't re-run; confirm, don't intervene",
    "evidence: #1354 comments 6008239980 (H8-7 writer closure relay) and 6008410763 (19:43 PDT tick relay), SoulSchoolAcademy/NayaPOWER"
  ],
  "relates_to": ["SN-0197", "SN-0351", "SN-0104"]
}
```
