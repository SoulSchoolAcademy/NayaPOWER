"""
PROTOCOL — Machine Law for Team Naya Operating Protocol
=======================================================
The operating protocol is not a document agents are asked to remember.
It is machinery agents cannot bypass.

This package implements the enforceable gates:
- read_receipt: prove the agent read and understood the protocol
- cold_start_gate: mandatory boot sequence for fresh agents (tests the AGENT)
- protocol_integrity_gate: validates the protocol manifest itself (tests the LAW)
- authority_gate: machine-checkable protected-gate enforcement
- quality_gate: 9.0+ delivery enforcement before anything reaches Shawn
- cold_successor_test: acceptance test that state survives the agent
- minimal_action: smallest effective change as a checkable proposal
- learning_capture: every cycle declares its lesson (with provenance) or states why none
- repeat_learning_gate: unresolved known repeats mechanically block sign-out as LEARNING_HOLD
- takeover: stalled-lane takeover rules as code

Data:
- protocol_manifest.json: all laws, gates, truth states, prohibitions as executable data

Law checks (checks/):
- tip_freshness: claimed SHA must match origin/main (SN-0493)
- decision_log: >=2 options scored, winner = top scorer, gates checked (SN-0522)
- scorecard: 7 dimensions, weights sum to 1.0, totals recomputed (SN-0523)
- action_log: fix verified + reported, no gate crossed without approval (SN-0575)
- delivery_evidence_gate: build + verification evidence, scorecard >=9.0 (SN-0526)

Prime 2: THE LAW IS THE CODE.
"""
