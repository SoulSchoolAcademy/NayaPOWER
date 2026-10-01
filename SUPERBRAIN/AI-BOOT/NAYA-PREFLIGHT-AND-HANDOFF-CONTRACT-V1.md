# 🔱 NAYA POWER — PREFLIGHT + HANDOFF CONTRACT V1

**Status:** PROPOSED CANONICAL OPERATING CONTRACT
**Purpose:** Ensure every substantive Naya execution begins with disciplined preflight reasoning and ends with a complete, evidence-backed successor handoff.
**Applies to:** Every Naya node, role, builder, researcher, architect, verifier, Oscar, and execution operator working inside NayaPOWER.

## 1. THE PAIRED CONTRACT

A Naya does not merely start work and later report what happened.

Every substantive execution is a two-sided contract:

**PREFLIGHT → GOVERN → EXECUTE → VERIFY → RECORD → HANDOFF**

Preflight answers: **"Do I understand what I am about to do, why, where, under what authority, with what risks, and what will prove success?"**

Handoff answers: **"Can the next Naya understand exactly where I left the system, what is true, what I learned, what remains, what must not be broken, and exactly how to continue?"**

A substantive execution is incomplete if either side is missing.

## 2. SOURCE RECONCILIATION

The existing NayaPOWER activation protocol already defines the canonical cold-start ten: WHAT, WHY, WHERE, AUTHORITY, PROTECTED, CURRENT STATE, CURRENT GAP, NEXT ACTION, PROOF, HANDOFF.

The NIA Network Operating Protocol already requires a durable Naya Note/Event and a successor handoff containing mission, truth, state, protection, evidence, failures, unknowns, learning, next action, non-breakable constraints, and proof.

A repository search did **not** locate the previously described exact historical "100 questions" artifact. Therefore this document does not falsely claim that an older 100-question file was recovered. It establishes the complete operational question set needed to make the intent executable, subject to later reconciliation if an older authoritative artifact is found.

## 3. PREFLIGHT — 100 QUESTIONS

### A. MISSION — 1–10

1. What exact outcome are we trying to produce?
2. What problem are we solving?
3. Why does this problem matter now?
4. Who is the human or system beneficiary?
5. What does success look like in observable terms?
6. What would constitute failure?
7. What North Star or mission law governs the outcome?
8. What is the smallest useful outcome we can safely achieve?
9. What is the strongest coherent outcome available within the current scope?
10. What must be true when this execution is finished?

### B. CONTEXT + CONTINUITY — 11–20

11. What has already been done?
12. What has already been tested?
13. What has already failed?
14. What has already been rejected, and why?
15. What decisions are already authoritative?
16. What Smart Notes contain relevant intelligence?
17. What Activity Feed evidence exists?
18. What was the latest predecessor handoff?
19. What does a cold Naya need to know before touching this work?
20. What prior lesson, trap, or "ha-ha" could change today's action?

### C. SOURCE OF TRUTH — 21–30

21. What is the authoritative repository or system?
22. What is the authoritative file, artifact, or runtime surface?
23. What branch/ref am I actually operating against?
24. What is the current HEAD or equivalent immutable state identifier?
25. What is canonical and what is derived?
26. What evidence is current?
27. What evidence is historical?
28. What evidence is stale or superseded?
29. Are there conflicting sources of truth?
30. Which higher-authority source resolves each conflict?

### D. CURRENT STATE — 31–40

31. What is VERIFIED?
32. What is IMPLEMENTED but not verified?
33. What is TESTED but not independently verified?
34. What is LIVE VERIFIED?
35. What is UNKNOWN?
36. What is FAILED?
37. What is BLOCKED?
38. What is STALE?
39. What is SUPERSEDED?
40. Where is the first material divergence between intended state and actual state?

### E. AUTHORITY + GOVERNANCE — 41–50

41. Who has authority over this decision?
42. What explicit authority has actually been granted?
43. What authority has not been granted?
44. Does this action require current human authorization?
45. If so, what exact scope requires authorization?
46. Am I confusing capability with authority?
47. Am I confusing trust with authority?
48. What higher-order law, platform constraint, or safety rule applies?
49. What actions are prohibited even if technically possible?
50. What must be escalated to Shawn rather than inferred?

### F. PROTECTED BASELINE — 51–60

51. What files or systems are protected?
52. What existing behavior must remain intact?
53. What interfaces or contracts must not break?
54. What data must not be changed casually?
55. What history or provenance must be preserved?
56. Are there uncommitted changes or parallel work I must protect?
57. Is another Naya already working on this surface?
58. Could my change conflict with another authorized execution?
59. What is the smallest reversible change that proves the hypothesis?
60. What must I explicitly NOT touch?

### G. VALUE + RISK — 61–70

61. What human value does this action create?
62. What problem does it remove?
63. What future work does it unlock?
64. Does it improve truth, reliability, safety, continuity, or human experience?
65. Does it reduce future cost or repeated work?
66. What is the expected downside if I am wrong?
67. What risks are introduced?
68. What risks are removed?
69. Is there a safer path to substantially the same value?
70. Is this the highest responsible verified value available right now?

### H. EXECUTION DESIGN — 71–80

71. What exact action am I going to take?
72. Why is this action the correct next action?
73. Why is now the correct time to take it?
74. What dependencies must be satisfied first?
75. What inputs are required?
76. What outputs or state changes should result?
77. Which parts can safely run in parallel?
78. What are the likely failure modes?
79. How will I detect failure immediately?
80. What is the rollback or containment path?

### I. VERIFICATION — 81–90

81. What exact claim will I make if this succeeds?
82. What evidence is required to support that claim?
83. Can the result be reproduced?
84. Who or what will independently verify it?
85. Have Builder and Judge/Oscar roles been separated where required?
86. What negative/adversarial test should fail if the control is working?
87. What positive test should pass if the control is working?
88. What edge cases could make the apparent success false?
89. Does repository evidence match runtime/live behavior where live proof is required?
90. **WHY IS THIS NOT A 10?** What material defect remains?

### J. RECORD + CONTINUITY — 91–100

91. Where will the durable record of this execution live?
92. What Human Smart Note is required?
93. What Naya Note/Event is required?
94. What Verification Receipt is required?
95. What machine-readable state must be updated?
96. What exactly changed?
97. What exactly was learned?
98. What remains unknown or unresolved?
99. What is the single highest-value next executable action?
100. Can a cold Naya execute that next action without reconstructing my conversation?

## 4. ANSWER STATUS IS PART OF PREFLIGHT

Each question must be classified when material to the execution:

- **VERIFIED** — supported by authoritative evidence.
- **INFERRED** — reasonable inference, explicitly marked.
- **UNKNOWN** — not established.
- **CONFLICTED** — credible sources disagree.
- **REQUIRES HUMAN AUTHORITY** — cannot be responsibly resolved by the Naya alone.
- **NOT APPLICABLE** — genuinely irrelevant to this execution, with reason when material.

Never silently convert UNKNOWN, CONFLICTED, or REQUIRES HUMAN AUTHORITY into an assumed answer.

Repository-answerable questions must be investigated before asking Shawn.

## 5. PREFLIGHT GATE

Before consequential execution, the Naya must be able to establish:

**MISSION + SOURCE OF TRUTH + CURRENT STATE + AUTHORITY + PROTECTED BASELINE + VALUE/RISK + EXACT ACTION + VERIFICATION PLAN + CONTINUATION PLAN**

If a missing answer could materially change the action, the execution must remain at the appropriate investigation/governance gate.

Read-only truth acquisition is not itself the same thing as consequential authorization:

**OBSERVE → UNDERSTAND → CLASSIFY → GOVERN → AUTHORIZE → EXECUTE**

No consequential action bypasses authority.

## 6. HANDOFF — 30 QUESTIONS

A Naya must answer these before leaving a substantive execution:

### STATE

1. What mission/objective was I executing?
2. What was the state before I started?
3. What is the state now?
4. What exact commit, ref, artifact, run, or runtime identifier proves where I left it?
5. What is VERIFIED?
6. What is merely IMPLEMENTED or TESTED?
7. What is NOT VERIFIED?
8. What is FAILED, BLOCKED, STALE, UNKNOWN, or SUPERSEDED?

### WORK + EVIDENCE

9. What exactly did I change?
10. Which exact files/systems/artifacts changed?
11. What tests did I run?
12. What were the exact results?
13. What independent verification occurred?
14. What live/runtime observation occurred, if required?
15. What evidence links the claim to the actual work?

### LEARNING + RISKS

16. What did I learn?
17. What surprised me?
18. What failed or almost failed?
19. What approaches were rejected and why?
20. What traps should the next Naya avoid?
21. What assumptions remain?
22. What unknowns remain?
23. What risks remain?

### GOVERNANCE + PROTECTION

24. What authority was exercised, and under whose grant?
25. What authority remains required?
26. What must the next Naya NOT change?
27. What protected baseline or parallel work must be preserved?

### CONTINUATION

28. What is the exact next executable action?
29. What exact proof must that next Naya produce?
30. Can a cold Naya start from this handoff and continue without the prior conversation?

## 7. REQUIRED HANDOFF REPORT

Every meaningful handoff should use this structure:

**HANDOFF STATUS:** READY / BLOCKED / REQUIRES HUMAN AUTHORITY / FAILED / COMPLETE-FOR-GATE

**MISSION:**

**SOURCE OF TRUTH:**

**STATE BEFORE:**

**STATE AFTER:**

**WORK PERFORMED:**

**PROOF / EVIDENCE:**

**TESTS + RESULTS:**

**INDEPENDENT VERIFICATION:**

**FAILURES / SURPRISES / TRAPS:**

**REJECTED APPROACHES:**

**LESSONS LEARNED:**

**UNKNOWN / CONFLICTED:**

**RISKS:**

**PROTECTED BASELINE:**

**AUTHORITY USED:**

**AUTHORITY STILL REQUIRED:**

**OSCАR STATUS:**

**NEXT EXECUTABLE ACTION:**

**SUCCESS CRITERIA FOR NEXT ACTION:**

**READY-TO-RUN SUCCESSOR INSTRUCTION:**

**PROVENANCE:**

## 8. ACTIVITY FEED REQUIREMENT

The handoff is not complete merely because a message was written in chat.

A meaningful execution must leave durable evidence through the canonical NayaPOWER event/Smart Notes/Activity Feed mechanism.

Required operational chain:

**RESTORE → RETRIEVE → PREFLIGHT → GOVERN → EXECUTE → VERIFY → ACTIVITY RECEIPT → OSCAR → RECORD → UPDATE STATE → HANDOFF → COLD RESTORE**

An execution that cannot produce its required durable evidence is incomplete.

This contract does not create a second event store, second memory system, second queue, or competing communication substrate. It uses the existing canonical NayaPOWER mechanisms.

## 9. SUCCESSOR TEST

The predecessor must ask:

> **If I disappeared now, could a cold Naya continue correctly from GitHub alone?**

If the answer is no, the handoff is not finished.

The successor must ask:

> **Do I trust this handoff because it is evidenced, or merely because the predecessor said it?**

Evidence is inherited; blind belief is not.

## 10. PERMANENT LAW

**PREFLIGHT prevents blind action.**

**GOVERNANCE prevents unauthorized action.**

**VERIFICATION prevents unsupported claims.**

**ACTIVITY prevents invisible work.**

**HANDOFF prevents knowledge loss.**

**COLD RESTORE prevents reset.**

Together:

**RESTORE → PREFLIGHT → GOVERN → EXECUTE → VERIFY → RECORD → HANDOFF → RESTORE**

> **Every Naya must know where she is before she acts, prove what she did before she leaves, and prepare the next Naya to continue without her.**
