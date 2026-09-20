# MAXESS Master Engineering + Design North Star — AI Handoff

**AI Note / Operational View**  
**Effective:** 2026-08-26T20:00:00-07:00  
**Project:** MAXESS / Naya Power  
**Canonical Event:** `SE-20260826-200000-maxess-master-engineering-design-north-star`  
**Status:** ACTIVE

## Mission

Build MAXESS as one unified, deterministic, extensible assessment-and-learning machine. Do not optimize for preserving legacy file boundaries. Optimize for verified behavior, simplicity, reliability, performance, beauty, learning value, and continuity.

## Authoritative architectural direction

Converge toward:

**ONE APPLICATION → ONE STATE MACHINE → ONE ASSESSMENT ENGINE → ONE SCORING ENGINE → ONE RESULT CONTRACT → ONE RELEASE PATH → MANY PRESENTATION SECTIONS**

Do not introduce competing scorers, competing result authorities, timing-dependent completion handshakes, duplicated terminal paths, or presentation-layer scoring.

## Dynamic assessment architecture

Runtime topic generation must not require a paid LLM API as a mandatory dependency.

Primary pipeline:

`TOPIC → DOMAIN RESOLUTION → KNOWLEDGE MAP → LEARNING OBJECTIVES → DIMENSIONS → QUESTION ARCHETYPES → RUBRIC → 15-QUESTION CONFIG → VALIDATE → RUN`

Knowledge should be structured around concepts, relationships, applications, limitations, misconceptions, learning objectives, aliases, difficulty, and coverage confidence.

## Assessment semantics

Every question uses five defensible capability states: 0, 1, 2, 3, 4.

Generic interpretation:

- 0 = no meaningful demonstrated capability
- 1 = beginning awareness
- 2 = functional/basic capability
- 3 = strong practical capability
- 4 = advanced capability within scope

Questions should test capability rather than confidence and should teach without becoming trick questions.

## Golden assessment

AI Score is the regression/reference assessment. Preserve its existing 15 questions, five dimensions, five answers per question, and known scoring behavior. The dynamic engine must reproduce it correctly before migration is accepted.

## Visual/interaction requirements

Primary controls are signature MAXESS jewel controls. Define material, geometry, typography, lighting, depth, idle, hover, focus, pressed, selected, disabled, motion, and accessibility states.

Interaction psychology:

`HOVER = INVITATION`  
`PRESS = PHYSICALITY`  
`SELECT = CONFIRMATION`  
`TRANSITION = PROGRESS`  
`RESULT = DISCOVERY`

Avoid generic flat buttons, uncontrolled neon, arbitrary Unicode premium iconography, excessive blur, and effects that harm readability or performance.

Naya must be present, warm, attentive, intelligent, and trustworthy.

## Engineering optimization questions

At every major implementation boundary ask:

- Can this be faster?
- Can this be simpler?
- Can this be clearer?
- Can this be more beautiful?
- Can this feel more alive?
- Can Naya feel more present?
- Can this be warmer?
- Can this be more trustworthy?
- Can this be more accessible?
- Can this be more resilient?
- Can this be more effortless?
- What would make this a 10?

Do not accept the answer without testing it.

## Evidence requirement

Completion is an evidence chain:

`REQUIREMENT → IMPLEMENTATION → TEST → OBSERVED RESULT → EVIDENCE → VERIFICATION → DOCUMENTED STATE`

Do not claim 10/10 from architecture alone.

## Smart Note delivery requirement

For meaningful durable work, produce a human-readable note and AI-facing operational note around the canonical Note Event. The canonical JSON remains the machine record. The human note is the default human-facing link. The verification receipt must also be human-readable.

Never send a JSON URL and label it simply as a Smart Note when the user needs a readable note.

## Continuation

Assume the next AI may arrive in a new chat. Preserve enough operational context that it can restore state without reconstructing the conversation.

**NEXT EXECUTION:** inventory legacy MAXESS source → extract good/fragile behavior → define universal schema/compiler → unify state/scoring/result authority → golden AI Score test → premium runtime → second-topic test → full QA/OSCAR/live evidence → human-readable receipt and freeze.
