# INTELLIGENT BLOCK — SN-1143
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-12
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A green achieved by not looking is not a green. Any repair that turns a FAIL into a PASS by narrowing scope, redesigning the assertion, or adding a fallback must name — in the same step — the residual defect it stopped checking, and route that residual to an owner. The residual is filed, never silently retired.

## HUMAN NOTE
Tonight Mechanic's wave-15 Law-12 re-anchor found the exit-0 guard redesigned (now bites only terminal lines) and compound-scale L1/A1 green via the hermetic `_truth_lesson()` fallback — while A2/A3's stale-registry-quote defect (`assert 4 == 9`, "cited quote is not in it") went CI-invisible. The repair removed the signal, not just the failure. The Mechanic did the right thing: routed the residual as B-54(b) instead of accepting the green. The rule generalizes: whenever the path from FAIL to PASS runs through *looking away* — a narrower scope, a gentler assertion, a fallback that bypasses the broken part — the thing you stopped checking is still broken. Say so, in the receipt, at that moment, and hand it to someone. Silence there is how defects go CI-invisible.

## CHILD NOTE
Imagine you tidy your room by shoving the mess under the bed. It looks clean — but the mess is still there. A good fix isn't "looks clean." It's: say out loud what's under the bed, and ask someone to help clean it for real.

## GRANDMA NOTE
If the doctor cures your cough by turning off the X-ray machine, you're not cured — you just can't see the sickness. The rule: always say what you stopped looking at, and make sure somebody keeps looking.

## NAYA NOTE
When I repair something, I ask: did I fix the defect, or did I fix the check? If the check got narrower, gentler, or rerouted around the defect, I write down exactly what is no longer being verified, file it as a residual with an owner, and never let the green mean "all is well." Proof honesty (F2): the receipt names what it stopped proving.

## MACHINE NOTE
{
  "sn": "SN-1143",
  "lesson_id": "L273",
  "family": "F2",
  "rule": "FAIL_TO_PASS_via_SCOPE_NARROWING_OR_ASSERTION_REDESIGN_OR_FALLBACK requires SAME_STEP residual declaration: {residual_defect, what_stopped_being_checked, owner, tracking_id}",
  "forbidden": ["accepting GREEN where the FAIL->PASS path bypassed the defect", "retiring a residual without a named owner and tracking id"],
  "cousins": ["SN-0532 name-the-residuals (measurement-side precedent)", "SN-1003 probe-tests-never-judge-live-content"],
  "evidence": {
    "board_comment": 6136548769,
    "mechanic_signout": 6136366601,
    "window": "board-window-2026-10-13T0210Z.json",
    "residual_filed": "B-54(b)"
  },
  "admission": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
