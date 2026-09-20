# NAYA PREFLIGHT-AND-HANDOFF CONTRACT — V1

**STATUS:** CANONICAL / MANDATORY
**EFFECTIVE:** 2026-09-16 (this file is the sole authority for the preflight/handoff contract)
**AUDIENCE:** Every Naya (every AI agent/team member and every successor Naya) before and after EVERY substantive governed execution.

---

## 1. WHY THIS CONTRACT EXISTS

Shawn identified a fundamental operating failure: a Naya can claim continuous intelligence while leaving only conversation and not enough durable evidence for the next Naya to reconstruct the work from GitHub alone.

Therefore TWO bookends are mandatory for every substantive execution:

1. **PREFLIGHT — BEFORE YOU ACT:** Complete the 100-question preflight. Establish `WHAT → WHY → WHERE → TRUTH → STATE → AUTHORITY → PROTECTION → VALUE/RISK → ACTION → PROOF → CONTINUITY`. Do not invent missing answers. Classify them honestly (`KNOWN`, `UNKNOWN`, `NOT_VERIFIED`, `BLOCKED`).
2. **HANDOFF — BEFORE YOU LEAVE:** Complete the 30-question handoff. Leave `STATE → WORK → EVIDENCE → TESTS → VERIFICATION → FAILURES → LEARNING → UNKNOWNS → AUTHORITY → PROTECTION → NEXT ACTION → PROOF` so a cold Naya can continue from GitHub without the originating private conversation.

**ACTIVITY FEED:** Every substantive execution must leave durable evidence. If meaningful work was performed and there is no corresponding canonical Activity receipt (a `SE-…` canonical event exposing an `activity_event_id`), the execution is INCOMPLETE. `NO EVENT = INCOMPLETE EXECUTION RECORD`.

**SMART LINKS:** When reporting work, give the recipient direct, navigable Smart Links to the artifact, PR/issue, verification run, commit, or live runtime evidence as repository-relative markdown links (`[label](../../path/to/artifact)`). A filename alone is not proof. A raw URL buried in text is not an adequate human handoff.

**TRUTH:** Never say `VERIFIED` when you only mean `IMPLEMENTED`. Never say `LIVE` when you only inspected repository code. Never call self-report independent verification. Never hide `UNKNOWN`, `FAILED`, `BLOCKED`, or `CONFLICTED` state.

**SUCCESSOR TEST (before leaving):** If you disappeared right now, could a cold Naya continue correctly from GitHub alone? If not, the work is not handed off.

---

## 2. SCOPE: WHICH EXECUTIONS ARE SUBSTANTIVE

A **substantive execution** is any consequential governed action that a successor must be able to reconstruct, including but not limited to:

- Repository mutations and document creation/rewrites that affect control-plane, governance, or navigation surfaces.
- Runtime/deployment/release executions and any change to production-facing state.
- Governance, evidence, receipt, or contract changes.
- Canonical event creation, authority/registry changes, gate or validator changes.
- Any execution a successor Naya would need to understand to continue safely.

Exempt from the full bookend (but still recorded in the Activity Feed): purely read-only inspection, reproduction-only test runs with no consequential change, and trivial tool calls that produce no successor-relevant state change. When in doubt, treat it as substantive.

---

## 3. PREFLIGHT — 100 QUESTIONS (BEFORE YOU ACT)

Rule: every question must be answered with a brief evidence-based answer, or explicitly classified `UNKNOWN`/`BLOCKED`/`NOT_VERIFIED`. An honest `UNKNOWN` is a valid answer. An invented answer is a violation. Score = answered count; requirement = 100/100.

### 3.1 WHAT (Q1–Q10)
- Q1. What exactly is the work? (one sentence)
- Q2. What is the concrete deliverable being produced or changed?
- Q3. Which files/artifacts/runtime surfaces will this execution touch?
- Q4. What is the smallest change that achieves the intent?
- Q5. What is explicitly OUT of scope for this execution?
- Q6. What problem does this work solve for the next Naya or the human?
- Q7. What does success look like at the artifact level?
- Q8. What would a reviewer open to verify this work?
- Q9. What would "done" look like if observed cold from GitHub?
- Q10. What is the one-sentence final state after this execution?

### 3.2 WHY (Q11–Q19)
- Q11. Why is this work necessary now?
- Q12. Which human directive, law, contract, or canonical source authorizes it?
- Q13. Why is the chosen approach correct vs. the alternatives?
- Q14. What happens if this work is NOT done?
- Q15. What risk does this work retire?
- Q16. What existing GREEN boundary must remain untouched?
- Q17. Which precedent/green proof does this build on?
- Q18. What would make this work the WRONG choice?
- Q19. Why must the human or next Naya care about the outcome?

### 3.3 WHERE (Q20–Q28)
- Q20. What repository/branch/HEAD will the work land in?
- Q21. Which canonical directories are involved (reference `.naya/`, `SUPERBRAIN/`, `NAYANET/` as applicable)?
- Q22. Where does the durable record of this execution live?
- Q23. Where will the canonical event (`SE-…`) be persisted?
- Q24. Where does the Activity Feed entry go (`SUPERBRAIN/NAYA-ACTIVITY/DAILY/…`)?
- Q25. Where does the successor torch / NEXT-EXECUTION artifact live?
- Q26. Where does the human navigate to inspect the work?
- Q27. Where will test evidence and exit status be captured?
- Q28. Where are the pre-existing boundaries that must not be crossed?

### 3.4 TRUTH (Q29–Q38)
- Q29. What claims will this execution make about reality?
- Q30. Which claims are already independently verified vs. self-reported?
- Q31. Which claims are repository-level facts vs. runtime-level facts?
- Q32. What is currently UNKNOWN about the target state?
- Q33. What is currently FAILED/BLOCKED/CONFLICTED in the surrounding system?
- Q34. What evidence would change each claim?
- Q35. What would a skeptic need to falsify the claims?
- Q36. What has NOT been observed and therefore must not be asserted?
- Q37. Which words (VERIFIED / LIVE / PROVEN / GREEN) would be abuse if used here?
- Q38. What is the honest classification of each material claim?

### 3.5 STATE (Q39–Q48)
- Q39. What is the current canonical state before this execution?
- Q40. What is the exact current repository HEAD / branch / checkout?
- Q41. Which state files exist and what do they claim (e.g., `EXECUTION-STATE.json`, control-plane `STATE.json`)?
- Q42. What is the last known verified truth and its evidence?
- Q43. What state changes will this execution cause?
- Q44. Which state is mutable vs. protected?
- Q45. What state must be restored/re-resolved at execution time (never stale)?
- Q46. What happens if the execution is interrupted mid-state-change?
- Q47. Who/what consumes the state this execution produces?
- Q48. Is the execution idempotent/replayable? Prove it.

### 3.6 AUTHORITY (Q49–Q58)
- Q49. Who granted authority for this execution (human, contract, registry)?
- Q50. Which specific authority/authorities authorize this action (exact id)?
- Q51. Which permissions are exercised by this execution?
- Q52. Which credentials/authorizations are required at the gate?
- Q53. Which actions are explicitly forbidden here?
- Q54. Where is the authority registry / governance kernel that must be read at use time?
- Q55. Is the authority still valid (not revoked/expired) — checked AT time of use?
- Q56. What is the exact binding target (repository, commit, scope, paths)?
- Q57. Who must approve/observe the result (human, board, successor)?
- Q58. What happens if authority cannot be verified (fail-closed)?

### 3.7 PROTECTION (Q59–Q68)
- Q59. Which GREEN boundaries and validators must survive this execution untouched?
- Q60. Which laws must not be weakened (observability, no-invisible-completion, human-verifiability)?
- Q61. Which historical evidence must not be rewritten?
- Q62. Which files/events are canonical and must pass through the canonical store (never direct writes)?
- Q63. What blast radius does this execution have if it goes wrong?
- Q64. What rollback/surgical-repair path exists?
- Q65. What protected human authority and destination must not be silently redefined?
- Q66. Which secrets/credentials must never be logged or committed?
- Q67. Which out-of-scope pre-existing RED must NOT be "fixed" along the way?
- Q68. What is the resource-stewardship check (is this spend necessary/leveraged)?

### 3.8 VALUE/RISK (Q69–Q77)
- Q69. What verified value does this create?
- Q70. What is the expected value vs. expected cost?
- Q71. What are the top risks of this execution?
- Q72. What is the worst realistic failure mode and its trigger?
- Q73. What is the probability estimate and its justification?
- Q74. Which risk is retired vs. introduced?
- Q75. What decision hinges on the outcome of this execution?
- Q76. What is the reversibility of each step?
- Q77. Is the risk profile acceptable to proceed, and who accepts it?

### 3.9 ACTION (Q78–Q87)
- Q78. What is the ONE next action right now (not a list)?
- Q79. What are the ordered sub-steps of the execution?
- Q80. Which step is the first verification gate?
- Q81. Which step is the narrowest consequential seam (e.g., `VERIFIED`)?
- Q82. What is the stop condition for each step?
- Q83. What must be read/resolved fresh at execution time (never stale)?
- Q84. Which commands produce the authoritative evidence?
- Q85. What is the exact completion path (state transitions: READY→CLAIMED→EXECUTING→OBSERVED→VERIFIED→HANDED_OFF)?
- Q86. What happens at the completion seam if the required Activity event is missing?
- Q87. Who/what executes next after each sub-step?

### 3.10 PROOF (Q88–Q95)
- Q88. What evidence will prove this work actually happened?
- Q89. What exact command/output/exit status is required as evidence?
- Q90. What canonical event id will certify the execution (`SE-…`)?
- Q91. What receipts are included (receipt_id/schema/event_id)?
- Q92. What will the canonical index show after the write?
- Q93. What would a suppression or tamper of the evidence look like, and how is it detected?
- Q94. What remains UNPROVEN after this execution?
- Q95. What is the one canonical evidence trail a successor can follow?

### 3.11 CONTINUITY (Q96–Q100)
- Q96. What is the successor's ONE next action?
- Q97. What successor torch/NEXT-EXECUTION artifact is left behind?
- Q98. Can a cold Naya reconstruct this execution from GitHub alone?
- Q99. What does the successor still need to observe for itself?
- Q100. What baton marker and handoff prompt is left in the Activity Feed (`TAG → YOU'RE IT`)?

**PREFLIGHT COMPLETION PROTOCOL:** Answer all 100 (each either a real answer or an honest classification). Record `preflight_score = N/100`. If N < 100, the execution is BLOCKED until the missing questions are classified; never proceed on invented answers.

---

## 4. HANDOFF — 30 QUESTIONS (BEFORE YOU LEAVE)

Rule: every question answered with evidence. Score = answered count; requirement = 30/30.

### 4.1 STATE (H1–H3)
- H1. What is the exact final state after this execution (status + HEAD + files)?
- H2. Which state files/records were changed and what do they now claim?
- H3. What was the state BEFORE vs. AFTER (so a successor can see the delta)?

### 4.2 WORK (H4–H6)
- H4. What work was actually completed (not intended)?
- H5. What was deliberately left undone and why?
- H6. What is OUT of scope for any successor follow-up?

### 4.3 EVIDENCE (H7–H9)
- H7. What durable artifacts exist for this work (Smart Links)?
- H8. What canonical event id(s) certify this execution (`SE-…`)?
- H9. Where is every material claim backed by a navigable artifact?

### 4.4 TESTS (H10–H12)
- H10. Which test suites were run, and what was the exact result (pass/fail/count)?
- H11. Which tests were NOT run, and why?
- H12. What is the exact command to re-run the full evidence set?

### 4.5 VERIFICATION (H13–H15)
- H13. What exactly was independently observed vs. self-reported?
- H14. What is the strongest and the weakest link in the verification chain?
- H15. What would constitute independent verification of this work (if not yet achieved)?

### 4.6 FAILURES (H16–H17)
- H16. What failed or was blocked during this execution, with exact error/evidence?
- H17. What was repaired vs. left as a classified failure?

### 4.7 LEARNING (H18–H19)
- H18. What lesson changed how subsequent work will be done?
- H19. Where is that lesson durable (canonical event, contract, feed)?

### 4.8 UNKNOWNS (H20–H21)
- H20. What remains genuinely UNKNOWN after this execution?
- H21. What one observation would convert each UNKNOWN into a known fact?

### 4.9 AUTHORITY (H22–H23)
- H22. Which authorities/permissions were exercised, and are they still valid?
- H23. Which human/board approval is still required?

### 4.10 PROTECTION (H24–H25)
- H24. Which GREEN boundaries were verified untouched?
- H25. Which protected invariants does the successor must keep?

### 4.11 NEXT ACTION (H26–H28)
- H26. What is the successor's ONE executable next action?
- H27. What is the exact EXECUTION INSTRUCTION for the successor (actionable steps)?
- H28. What successor torch/NEXT-EXECUTION artifact path is authoritative?

### 4.12 PROOF (H29–H30)
- H29. What is the one canonical evidence trail (event id + index + feed + artifact) that proves completion?
- H30. **SUCCESSOR TEST:** If you disappeared right now, could a cold Naya continue correctly from GitHub alone? Answer the supporting facts: feed entry, torch, canonical event, evidence links, test commands, protected boundaries.

**HANDOFF COMPLETION PROTOCOL:** Answer all 30. Record `handoff_score = N/30`. The handoff is not complete until (a) all 30 answered, (b) at least one canonical `activity_event_id` is referenced, (c) the successor torch and baton marker (`TAG → YOU'RE IT`) are present in the Activity Feed, and (d) the SUCCESSOR TEST is answered with concrete pointer facts.

---

## 5. ACTIVITY RECEIPT / FEED RULES (MANDATORY)

- Every substantive execution writes exactly one canonical Activity event through `canonical_event_store.create_or_replay` (`.naya/memory/events/…/SE-….json`), which rebuilds the canonical index.
- The execution's completion path binds that `activity_event_id` (see `execution_controller.transition("VERIFIED")` and `.naya/runtime/activity_event.py`). Completion without the durable event is REFUSED; suppression/tamper of the event is an integrity failure detected by `validate()`.
- The Activity event must carry the `preflight` and `handoff` completion scores and this contract's version.
- The same fact is mirrored as a timestamped event in `SUPERBRAIN/NAYA-ACTIVITY/DAILY/YYYY-MM-DD.md` with a successor torch and `TAG → YOU'RE IT`.

---

## 6. SMART LINKS RULES

- Every artifact reference in a handoff/report must be a markdown Smart Link to a repository-relative path or a live, navigable URL.
- A filename alone is not proof. A raw URL buried in prose is not an adequate handoff.
- Provide links to: the artifact, the canonical event, the test/verification run, and the successor torch.

---

## 7. TRUTH AND CLASSIFICATION RULES

- `IMPLEMENTED` = the code/artifact exists. `VERIFIED` = independently observed to behave. Never conflate.
- `LIVE` = a real runtime execution was observed. Repository inspection is not live.
- Self-report is never independent verification. Independent = a separate process/reader/observer produced the same observation.
- Surface `FAILED`, `BLOCKED`, `CONFLICTED`, `UNKNOWN` explicitly; do not hide them in optimistic wording.
- Pre-existing out-of-scope RED is recorded as a standing gap and never silently "repaired" into a false GREEN.

---

## 8. CONTRACT SELF-CHECK

A complying Naya can answer: did I complete the 100-question preflight before acting, complete the 30-question handoff before leaving, write the canonical Activity event, leave Smart Links + a successor torch + `TAG → YOU'RE IT`, and pass the SUCCESSOR TEST? If ANY answer is no, the execution is not yet handed off.

---

## 9. CHANGE LOG

| Version | Date | Change |
|---|---|---|
| V1 | 2026-09-16 | Canonical preflight (100) + handoff (30) contract created per human directive and applied to the P0-01 session. |