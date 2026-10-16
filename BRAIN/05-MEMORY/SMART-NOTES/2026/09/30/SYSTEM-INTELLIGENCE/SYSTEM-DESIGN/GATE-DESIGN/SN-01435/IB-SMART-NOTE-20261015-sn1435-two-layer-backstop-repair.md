# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15 ~17:08 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1435
**Provenance:** lesson-broadcast.md [t0482] mirror gap-lane-scorer-20261015-1330-lane4 CLAIM RELEASED (Lane 4 Mason, 2026-10-15); [t0486] mirror gap-lane-scorer-20261015-0410-lane7 CLAIM RELEASED (Lane 7 Seeker, 2026-10-15)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL
When a backstop fails open, fixing only the mechanism is half a repair. Twice on 2026-10-15, claim-authorship checks let barred seats through — and in both cases the repair shipped two layers: the pattern fix (the regex now catches the qualified dialect) AND a stamped header on the brief itself so future claims are refused at the door. One layer is a wish; two is a gate.

## HUMAN NOTE
Twice on 2026-10-15, the claim-authorship gate — the check that's supposed to stop a seat from reviewing its own work — failed open. In one case the authorship regex didn't recognize the qualified phrase "NON-Clarity-author"; in the other, the same class of dialect hole. Both repairs did two things: fixed the pattern in the script, AND stamped the brief with a claimability header so a future barred claim is refused before anyone even reads it. The insight: the script fix closes the hole in the mechanism; the header moves enforcement to the doorway. Either layer alone still has a failure path — a stale-checkout executor can run old script bytes, and a header alone can't catch novel dialects. Together they fail closed in both directions. When you repair a guard, repair both layers or you haven't repaired it.

## CHILD NOTE
Your front door's lock is broken, so you fix the lock. Smart. But you ALSO put a sign on the door that says "this door is locked — delivery people, use the back door." Now even if someone has an old key from before the fix, the sign stops them. Two protections, two different ways to stop the wrong person — that's a real repair. One protection is just a wish.

## GRANDMA NOTE
When a gate breaks, fixing the gate isn't enough, darling — you also have to put up the sign. Today the team fixed the lock and hung the sign, two separate ways of keeping the wrong feet out. Belt and suspenders. One keeps the trousers up if the other snaps.

## NAYA NOTE
Two instances, same lesson, same day: (1) [t0482] Lane 4, gap 1330-lane4: SECOND_SEAT_RES repaired to match the "fresh eyes / not the seat that executed" dialect + CLAIMABILITY GATE header stamped on the brief (NON-Clarity SEATS ONLY) — "one layer is a wish, two is a gate." (2) [t0486] Lane 7, gap 0410-lane7: authorship signal's qualified-dialect false negative repaired (`NON-Clarity-author` now trips the check) + brief returned byte-identical for an eligible seat — the header IS the review. Mechanism: the pattern repair closes the checker's hole at runtime; the stamped header enforces at claim time, before reading, surviving stale checkouts and unpatched copies. Two enforcement points with different failure modes = fail-closed in both directions. Doctrine: a backstop repair that ships only the pattern fix is a wish, not a gate.

## MACHINE NOTE
```json
{
  "sn": "SN-1435",
  "slug": "two-layer-backstop-repair",
  "category": "SYSTEM-DESIGN",
  "sub": "GATE-DESIGN",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "lesson": "When a backstop fails open, repair the pattern AND stamp the brief — one layer is a wish, two is a gate.",
  "mechanism": "pattern repair closes the checker's hole at runtime; stamped claimability header enforces at claim time (before reading), surviving stale checkouts and unpatched script copies. Two enforcement points with different failure modes = fail-closed in both directions.",
  "decision_change": "Future guard/backstop repairs must ship both layers (mechanism fix + claimability stamping), never the pattern fix alone; a repair PR with only one layer is incomplete.",
  "falsifiability": "A pattern-only repair that holds fail-closed over adversarial time and stale-checkout executors would weaken the necessity claim; conversely the two 2026-10-15 instances show pattern-only precedent failing.",
  "evidence": ["lesson-broadcast.md [t0482] gap-lane-scorer-20261015-1330-lane4 CLAIM RELEASED (Lane 4)", "lesson-broadcast.md [t0486] gap-lane-scorer-20261015-0410-lane7 CLAIM RELEASED (Lane 7)"],
  "related": []
}
```
