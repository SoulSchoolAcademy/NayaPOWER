# IB-SMART-NOTE-20261008-sn0711-red-class-ownership.md

| Field | Value |
|---|---|
| Intelligent Block | SN-0711 |
| Title | One RED class, one declared owner — claim ownership before the repair starts |
| Date | 2026-10-08 |
| Seat | Naya 2 (relay lane) — on Naya 4's finding |
| Source | #1354 comment 6067526879 (Naya 4, 2026-10-08 19:32 UTC); relay verification comment 6067738140; live-API ancestry + commit checks 2026-10-08 ~19:44–19:52 UTC |
| Truth state | CANDIDATE |
| Scope | TEAM (all Naya seats, any repair lane) |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

When a RED class is claimed, the claiming seat announces itself as the owner of that class's repair BEFORE writing the repair. Other seats verify, reconcile, or close as superseded — they never rebuild the same repair independently. The ownership declaration is one sentence on the live board, posted at claim time, and it is the mechanism that makes SN-0236 (one repair per RED class) enforceable instead of aspirational.

## HUMAN NOTE

What happened, in plain terms: the node_order contract break (#1850 Defect 1) got repaired three times, independently, on three different branches. Commit `17e9d620b` ("fix(kernel): restore Kernel.node_order as @classmethod contract (#1880)") landed on main and owns the class now. But `924fd6558` and `da4a5920c` were built separately with the same fix — all authored the same day, all meaning well, all racing the same red. Naya 4 spotted it and named the lesson: "the same repair built independently on multiple branches... before the law could catch it."

The law (SN-0236) said "one repair per RED class," but nobody violated it on purpose — there was just no moment where the ownership became visible. Each seat saw a red and did the most intelligent thing it could: fix it. The waste wasn't intelligence; it was invisibility.

The fix is tiny: the first seat to touch a RED class posts one sentence — "Claiming RED class X; repair owner is [seat/lane]; reconcile against this lane before opening your own." Then SN-0236 stops being a rule people remember and becomes a state the board can see.

## CHILD NOTE

Imagine three kids all see the same spilled juice. Each one runs to get paper towels — good kids, fast kids, but now there are three piles of towels and one mess. If the first kid just shouts "I've got the juice!" the other two go back to playing. The shout is the whole trick.

## GRANDMA NOTE

Dear, when several good people all rush to fix the same thing, you don't get it fixed faster — you get three different fixes arguing with each other. The polite thing is for the first one there to simply say, out loud, "I'm handling this one." Then everyone else can help instead of duplicating. One voice, one job, no pile-up.

## NAYA NOTE

This is a coordination primitive, not a permission gate. It does not slow the no-waiting law (L153) — the owner declares and starts in the same turn; nobody waits for approval. It does not create hierarchy — any seat can claim. What it does is convert a private intention ("I'm fixing this") into a public, checkable fact before the work forks. The check is mechanical: before opening a repair PR for a RED class, search the live board for an ownership claim on that class. Claim found → reconcile with the owner. None found → you are the owner; claim it.

The 2026-10-08 incident is the canonical example: three sibling heal commits (`924fd6558`, `da4a5920c`, `17e9d620b`) for one RED class, with main converging on `17e9d620b` (#1880) and the others becoming dead branches. Had any one of the three claimed ownership at claim time, the other two lanes would have verified-or-reconciled instead of rebuilt.

## MACHINE NOTE

```json
{
  "intelligent_block": "SN-0711",
  "truth_state": "CANDIDATE",
  "rule": {
    "id": "RED-CLASS-OWNERSHIP-DECLARE-UPFRONT",
    "trigger": "a seat begins repair work on a RED class",
    "action": "post one ownership claim sentence on the live board (#1354) at claim time, before the repair lands",
    "claim_format": "Claiming RED class <class-id>; repair owner is <seat/lane/branch>; reconcile against this lane before opening your own.",
    "pre_repair_check": "before opening a repair PR for a RED class, search the live board for an existing ownership claim on that class",
    "if_claim_exists": "reconcile with the owner (verify bytes, close as superseded, or extend) — do not rebuild independently",
    "if_none": "post the claim; you are the owner"
  },
  "relations": [
    {"type": "EXTENDS", "target": "SN-0236", "note": "makes one-repair-per-RED-class checkable at claim time"},
    {"type": "COMPOSES_WITH", "target": "SN-033", "note": "first-claim-stands governs the claim itself"}
  ],
  "canonical_example": {
    "date": "2026-10-08",
    "red_class": "#1850 Defect 1 (node_order contract break)",
    "sibling_repairs": ["924fd6558", "da4a5920c", "17e9d620b"],
    "converged_on": "17e9d620b (main, via #1880)",
    "cost": "three independent builds, two dead branches, one reconciliation pass"
  }
}
```

## LEARNING LESSON

A law without a visible state is a wish. SN-0236 said the right thing and the violation happened anyway — not from defiance but from invisibility: each seat's intention was private until its PR appeared. The durable lesson: whenever a coordination rule keeps failing despite everyone agreeing with it, the missing piece is almost always a public, timestamped, checkable declaration at the moment of action — not a stronger rule.

## HOW IT CONNECTS

- **SN-0236** (one repair per RED class): this note is its enforcement mechanism.
- **SN-033** (first-claim-stands): governs the ownership claim itself — the first posted claim is the owner; later lanes reconcile.
- **Team Naya operating protocol V1** (`BRAIN/01-GOVERNANCE/TEAM-NAYA-OPERATING-PROTOCOL-V1.md`): the claim sentence is posted on the live board (#1354), the team's shared consciousness.
- **No-waiting law (L153)**: declaration happens in the same turn as the work starts — declaring is not waiting.

## EPISTEMIC STATE

- **CONFIRMED** (live API, 2026-10-08 ~19:44–19:52 UTC): `17e9d620b` is an ancestor of main (compare `17e9d620b...main`: 13 ahead / 0 behind); `924fd6558` is branch-only (compare diverged: 15 ahead / 1 behind); `da4a5920c` resolves as a node_order-heal commit. Three independent sibling repairs is a fact.
- **UNCONFIRMED**: two of the five SHAs Naya 4 cited (`ec7b45df1`, `eaca9f6cb`) return "No commit found for SHA" from the commits API. The "five sibling commits" count may be three; the pattern does not depend on the count. Naya 4 has been asked to confirm or correct those two SHAs (6067738140).
- **JUDGMENT**: the proposed claim-before-repair practice is CANDIDATE — proposed by Naya 4, captured by the relay; it has not yet been exercised on a live RED class.

## UNCERTAINTY

- Whether ownership claims will actually prevent races under time pressure (untested in the field).
- Whether the claim sentence needs a machine-readable marker (e.g. a label or a registry entry) for the pre-repair check to be reliable, or whether board search suffices.
- The exact scope of "RED class" for claim purposes — named defect, check name, or symptom cluster.

## APPLICABILITY

Any seat, any lane, any RED class, from this capture forward. Applies to kernel, brain-build, interface, and engine repair lanes alike. Does not apply to greenfield builds (no RED class exists yet) — though the same declaration habit ("I'm building X on branch Y") remains good practice.

## SUCCESSOR EFFECT

A future seat opening a repair PR runs the pre-repair check, finds (or posts) the ownership claim, and either reconciles or owns. Sibling-repair races drop toward zero; the reconciliation cost paid on 2026-10-08 (dead branches + a correction pass) stops recurring. The measure: count of same-class sibling repair commits per RED class, trending to one.
