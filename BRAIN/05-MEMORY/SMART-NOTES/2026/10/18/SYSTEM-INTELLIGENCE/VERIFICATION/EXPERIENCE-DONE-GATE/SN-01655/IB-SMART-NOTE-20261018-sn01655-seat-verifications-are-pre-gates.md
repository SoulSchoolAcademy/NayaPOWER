# Seat Verifications Are Pre-Gates — the Human's Own Hands-On Test Is the Experience Done-Gate

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01655-seat-verifications-are-pre-gates
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/shared-state.json (director_tick_2026_10_18_1008, 2026-10-18 17:08Z): L520 [F7] FILED — board comment 6252619944: Shawn tested the 12-template preview himself ~15:20Z, scored 3-4/10 ("broke all the design contracts", "an utter fail") — falsifying Chi/Epsilon seat verifications; experience-surface done-gate = the human's own hands-on test; seat verifications are pre-gates.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A seat's verification proves the contract was met; only the human's hands-on test proves the experience works. The 12-template preview passed Chi and Epsilon seat verifications and still scored 3-4/10 when Shawn himself touched it — "broke all the design contracts," "an utter fail." For experience surfaces, seat verifications are pre-gates: they earn the right to ask the human to test. The human's hands-on verdict is the done-gate, and a done-claim without it is a pre-gate wearing a done's clothes.

## 🩷 HUMAN NOTE

Shawn — you picked up the 12-template preview yourself and gave it 3-4 out of 10: it broke all the design contracts, an utter fail — after two seats had already verified it. That mismatch is the lesson, and it's standing now: on anything a human will experience, seat verifications are pre-gates, never the verdict. The rule going forward is simple — nothing on an experience surface is "done" until your own hands (or a surrogate you named) have tested it and the verdict is on the board. The seats verify the contract; you verify the experience. Those are two different oracles, and yours is the one that counts.

## 🟣 CHILD NOTE

You drew a picture and your two friends both said "looks great!" — then mom looked at it and said "that's not what I asked for." Your friends checked their own checklists; mom checked what she actually wanted. From now on: for things people will see and touch, friends checking it first is good — but the verdict that counts is the person who will actually use it trying it themselves.

## 🔵 GRANDMA NOTE

It's like a new recipe. The cook's helpers taste it in the kitchen and say it's fine — but the grandmother at the table says it's too salty and sends it back. The helpers know the recipe; she knows what dinner should taste like. On anything meant to be experienced, the table's verdict — not the kitchen's — is what closes the question.

## 🟠 NAYA NOTE

Cold successor: the experience done-gate procedure.

1. Name the surface class at intake: is a human (or his named surrogate) going to SEE/TOUCH/USE this? If yes, it is an experience surface.
2. Seat verifications run first, filed as PRE-GATE: "seat-verdict: 9.5/10 (pre-gate, not the done-gate)."
3. The seat then routes the surface to the human's hands — per the show-him-the-HTML shape: build → score 9+ → show him the live thing → his hands-on verdict.
4. The verdict is recorded with a board-comment id: `human-experience-verdict: <comment-id>`. Empty means NOT DONE.
5. If the human's score falsifies the seat's verification (like the 3-4/10 did), the seat's oracle gets a hole filed against it: what did the human test that the checklist didn't encode? That hole becomes the next upgrade to the verification procedure.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1655",
  "title": "Seat Verifications Are Pre-Gates — the Human's Own Hands-On Test Is the Experience Done-Gate",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "VERIFICATION", "EXPERIENCE-DONE-GATE"],
  "applies_when": ["verification", "experience-surface", "done-gate", "human-test", "hub", "design-law"],
  "enforcement": "Experience-surface PRs and readiness claims carry a mandatory done-gate checklist item — 'human-experience-verdict: <board-comment-id>' — non-empty before any seat declares done. Seat verifications are filed as pre-gates; the scorer bounces any done-claim on an experience surface that cites only seat verifications.",
  "cousins": ["SN-1428 (void a self-caught falsified verification in the open — the honesty half of this note: when the human's test falsifies a seat verification, the falsification goes on the record and the seat's oracle gets the hole)"],
  "evidence": {
    "l520_f7": "hidden_files/shared-state.json, director_tick_2026_10_18_1008: 'L520 [F7] FILED (6252619944): Shawn tested the 12-template preview himself ~15:20Z, scored 3-4/10 (\"broke all the design contracts\", \"an utter fail\") - falsified Chi/Epsilon seat verifications; experience-surface done-gate = the human\\'s own hands-on test; seat verifications are pre-gates.'",
    "falsified_seats": "Chi VERIFY and Epsilon seat verifications of the 12-template preview passed before the human test; the human's 3-4/10 stands as the verdict that mattered"
  },
  "decision_change": "when declaring an experience-surface deliverable done, the seat routes it to Shawn's own hands-on test (or his named surrogate's) BEFORE claiming done, records the verdict's board-comment id, and files its own verification as a pre-gate — never as the done verdict.",
  "falsifier": "if seat verifications predict the human's experience score within an agreed tolerance across N consecutive surfaces (five is the standing bar), seat verification becomes admissible as the done-gate for that surface class and this note demotes to a default-with-escape-hatch; or if Shawn names a surrogate whose test verdict binds, the surrogate's hands-on test replaces his as the done-gate.",
  "mechanism": "seat verifications test against the stated contract (design laws, checklists); the human tests against felt experience. Contract compliance does not equal experience quality — the seat's oracle is always narrower than the human's implicit standard ('broke all the design contracts' was invisible to the checklist the seats ran), so a passing seat-verdict and a failing experience are the normal mismatch, not an anomaly."
}
```
