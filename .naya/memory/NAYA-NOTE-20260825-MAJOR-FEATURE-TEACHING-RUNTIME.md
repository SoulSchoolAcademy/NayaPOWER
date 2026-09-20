# NAYA NOTE — MAJOR FEATURE: NAYA TEACHING RUNTIME

**Status:** OFFICIAL DESIGN LOCKED
**Feature:** `FEATURE-NAYA-TEACHING-RUNTIME-V1`
**Priority:** P1 / Major Product Capability
**Project:** `PRJ-NAYAPOWER-SUPERBRAIN`

## Canonical learning

Naya Teaching Runtime is now an official NayaPOWER feature. Its purpose is to make Naya an adaptive teacher rather than a static course reader.

The core law is:

**Naya does not teach information. Naya teaches understanding, application, and capability.**

The canonical teaching loop is:

`WANT TO LEARN → UNDERSTAND → SIMPLIFY → TEACH → ILLUSTRATE → CHECK → PRACTICE → APPLY → REFLECT → REMEMBER → NEXT STEP`

## Runtime behavior

When a learner says, “Naya, teach me about X,” Naya should identify the real learning goal, explain the subject simply, reduce it to essential ideas, make it concrete, demonstrate it, let the learner practice, check demonstrated understanding, provide feedback, and finish with a useful action.

The runtime can adapt among QUICK TEACH, DEEP TEACH, LEARN BY DOING, ROLE PLAY, TEST ME, APPLY IT, and MASTER IT.

## Knowledge architecture

Human Maximus Codex knowledge, approved AI curriculum, activation knowledge, and future customer knowledge are source knowledge. The Teaching Runtime is the instructional method. The user's request is learning intent.

Do not create thousands of rigid hard-coded courses when the same runtime can dynamically construct a high-quality lesson from these inputs.

## Superbrain relationship

Meaningful learning should eventually flow through the existing canonical architecture rather than a parallel memory system:

`KNOWLEDGE → TEACHING → PRACTICE → DEMONSTRATED UNDERSTANDING → LEARNING MEMORY → NEXT LESSON → CAPABILITY`

Teaching completion is not evidence of learning. Demonstrated understanding is stronger evidence.

## MAXESS relationship

MAXESS remains the measurement/capability-discovery layer. Naya may contextually invite a learner to take the free MAXESS assessment at Maxis9net.app and use the resulting evidence to shape the next learning objective.

## Important verification boundary

This note locks the feature's constitutional design into the repository. It does **not** claim that the Teaching Runtime is fully implemented or authoritative-GREEN. Implementation requires machine-enforced runtime behavior, positive and deliberate-failure tests, and authoritative CI.

## Next engineering objective

Implement and enforce the Teaching Runtime against this specification while preserving every existing Superbrain GREEN boundary.
