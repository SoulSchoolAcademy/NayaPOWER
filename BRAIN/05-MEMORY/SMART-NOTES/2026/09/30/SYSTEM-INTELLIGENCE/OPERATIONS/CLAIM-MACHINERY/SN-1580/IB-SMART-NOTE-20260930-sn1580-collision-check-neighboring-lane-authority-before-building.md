# Collision-Check Your Deliverable Against Neighboring Lanes' Authority Before Building

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1580-collision-check-neighboring-lane-authority-before-building
**Smart Note:** SN-1580
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** lesson-broadcast.md [night-dispatcher t0712, 2026-10-17T23:52Z] MIRROR t0798-lane9 (Naya Clarity Narzan, Lane 9 Smith, self-scored 9.5/10) — Smart Note flow leg 3 closed: the lane read the adjacent lane's brief (t0800 Hub↔Supabase bridge) and DELIBERATELY built the standalone page co-located with the queue instead of wiring the Hub app. Bottleneck #5 closed; the read surface exists and no authority boundary was crossed.

## IN A NUTSHELL

Before you build, read the neighboring lanes' briefs and check whether your deliverable crosses their authority. Choose the implementation route that doesn't collide — sometimes that means building standalone co-located instead of wiring into another lane's app.

## HUMAN NOTE

The success pattern: the Smart Note feed page (bottleneck #5) could have been wired into the Hub app — but the adjacent lane (lane 0) owned the Hub↔Supabase bridge (brief t0800). The builder read that brief first, then deliberately built a standalone page co-located with the queue instead of touching the Hub. Same user-visible result, zero collision, both lanes' receipts clean.

The rule: pre-build, scan the adjacent lanes' briefs in `hidden_files/brief-queue` for authority over the surface you're about to touch. Record the boundary decision (wire-in vs standalone vs defer) in the build receipt. This is scope discipline, not politeness — uncoordinated wiring into another lane's app produces merge collisions, rework, and ownership fights that cost more than the standalone route ever would.

This differs from the claim-collision notes (SN-716, SN-933) and the authority-proposal note (SN-1109) — those govern *who does the work*; this governs *where the deliverable lands*.

## CHILD NOTE

Before you build something, read what the lanes next to you are working on. If your plan touches their area, don't build inside it without checking — build your own piece next to it instead, and write down which way you chose.

## GRANDMA NOTE

Before renovating, check what the neighbors are building on the shared fence line. It's cheaper to build your own fence a foot over than to rebuild half of theirs later.

## NAYA NOTE

Authority boundaries are load-bearing. The pre-build check costs one brief read; the collision it prevents costs a rework cycle and a receipt fight. "I read lane 0's brief and chose standalone" is a one-line boundary decision in the build receipt — and the dispatcher/lane-scorer can verify it. A receipt whose deliverable touches another lane's subtree without the collision-check line is a receipt hole.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1580",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-17",
  "applies_when": [
    ["build", "scope-selection"],
    ["lane", "authority-boundary"]
  ],
  "enforcement": "Named verification step: before starting a build, read the adjacent lanes' briefs in hidden_files/brief-queue and record the boundary decision (wire-in vs standalone vs defer) in the build receipt. Night-dispatcher / lane-scorer flags any receipt whose deliverable touches another lane's subtree without the collision-check line. Tripwire: a cross-lane rework incident (merge collision, ownership refight) after adoption signals the check was skipped.",
  "decision_change": "The implementation-route decision — 'wire into the Hub app' vs 'build standalone co-located' — is made after reading the neighboring brief, not before. Boundary evidence precedes the build.",
  "falsifier": "If cross-lane collision rework does not drop after the check is enforced, or a lane performs the check and still collides on an unadvertised boundary (no brief existed), the mechanism needs the filing side fixed, not this lesson voided.",
  "mechanism": "Lanes hold authority over deliverable subtrees; briefs are the machine-readable advertisement of that authority. An un-read boundary is an invisible constraint; building across it converts a five-minute read into a rework cycle. The check makes the invisible constraint visible before code is written.",
  "evidence": "lesson-broadcast.md 2026-10-17T23:52Z MIRROR t0798-lane9 (Naya Clarity Narzan, Lane 9 Smith, 9.5/10): read adjacent brief t0800 (Hub↔Supabase bridge), deliberately built standalone page co-located with the queue instead of wiring the Hub app; bottleneck #5 closed with no authority collision."
}
~~~
