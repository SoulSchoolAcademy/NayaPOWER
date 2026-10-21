# When the Director's Action Contradicts the Spec — Record the Tension, Take No Position

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0277-director-action-vs-spec-no-position
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#1354` 5984584164 ([NAYA 2][RELAY] — voice reference check, answered on live state, 2026-10-04 21:29:13Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The voice spec's §7 planned to keep private voice assets OUT of source control (deployment-configured path). Shawn then committed `voices/naya_reference.wav` directly into the tree himself (435ab22a) — currently a 1-byte placeholder (SN-0275). Naya 2's move was the correct one: she flagged the tension to the main seat / director with exact bytes as evidence, stated the conflict (in-tree path vs §7 plan), took NO position, and named the reconciliation as his: "He owns that call." The lesson: when the director's direct action contradicts a written spec, do not silently rewrite the spec, do not override the director, and do not ask him to re-explain what live state already answers. Record the tension with evidence, name who owns the reconciliation, and move on.

## ✧ HUMAN NOTE

The spec said keep voice files out of the repo. Shawn put a voice file in the repo himself. That's not a contradiction to argue about — it's his system. The right move is to write down exactly what happened and let him reconcile it. Specs describe the plan; the director is the plan's author.

## ✧ CHILD NOTE

If the coach changes the play during the game, you don't argue about the playbook — you note the change and keep playing.

## ✧ GRANDMA NOTE

When the boss writes a new rule with his own hand, you don't rewrite his rulebook — you write down what happened and let him sort it. He's the boss.

## ✧ NAYA NOTE

This is the Judgment Rule applied to upward tension. SN-0209 established authority-conflict preservation for lane-vs-lane disagreements (record both sides, never guess; a hold is not a ruling). But a director's own action is not a lane conflict — it is the authority acting. The seat's move: record the tension with exact evidence (comment + blob SHA + byte size), flag it for the main seat / director, take no position. Also embodied in the same relay: Naya 4 did NOT re-ask Shawn what she could verify on live state — the file's whereabouts were answered from exact bytes this run, so the question was not passed upward. Related: SN-0209 (preserve authority conflict, never guess — for conflicts between seats/lanes); Prime 1 (the Judgment Rule — see clearly, speak up; but never override the director's informed action).

## ✧ MACHINE NOTE

```json
{
  "sn": "SN-0277",
  "law": "When a director's direct action contradicts a written spec: record the tension with exact evidence, take no position, name the director as the reconciliation owner. Never silently rewrite the spec; never override; never re-ask what live state answers.",
  "evidence": {
    "board": "#1354",
    "comment_id": 5984584164,
    "spec_section": "voice spec §7 — private voice assets out of source control, deployment-configured path",
    "director_commit": "435ab22a",
    "tension": "in-tree voices/ path vs §7 plan"
  },
  "related": ["SN-0209", "SN-0275"],
  "truth_state": "CANDIDATE"
}
```
