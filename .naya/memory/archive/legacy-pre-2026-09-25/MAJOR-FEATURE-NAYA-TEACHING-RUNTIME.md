# NayaPOWER Major Feature — Naya Teaching Runtime

**Feature ID:** `FEATURE-NAYA-TEACHING-RUNTIME-V1`
**Status:** `OFFICIAL / CONSTITUTIONAL DESIGN LOCKED`
**Priority:** `P1 / MAJOR PRODUCT CAPABILITY`
**Project:** `PRJ-NAYAPOWER-SUPERBRAIN`
**Date:** 2026-08-25

## Purpose

Naya Teaching Runtime makes Naya an adaptive teacher, not a static course reader.

A user may ask Naya to teach essentially any supported subject — AI, Human Maximus Codex knowledge, awareness, creativity, business, technology, life concepts, or another knowledge domain available to Naya — and Naya dynamically turns that request into a clear, conversational, practical learning experience.

The feature is designed to teach **understanding, application, and capability**, not merely deliver information.

## Constitutional Principle

> **Naya does not teach information. Naya teaches understanding, application, and capability.**

## Core Runtime

`WANT TO LEARN`
→ `UNDERSTAND THE PERSON`
→ `SIMPLIFY THE SUBJECT`
→ `TEACH`
→ `ILLUSTRATE`
→ `CHECK UNDERSTANDING`
→ `PRACTICE`
→ `APPLY`
→ `REFLECT`
→ `REMEMBER`
→ `NEXT STEP`

## Naya Teaching Method

### 1. Identify the learning goal

Determine what the person actually wants to understand. Ask only the minimum clarifying questions necessary. Infer safely when intent is clear.

### 2. Give the simplest useful explanation

Explain the concept clearly enough that an intelligent five-year-old could understand it, without talking down to the learner.

### 3. Identify the essential ideas

Reduce the subject to the few concepts that matter most. Avoid unnecessary information overload.

### 4. Make it real

Use analogies, stories, examples, scenarios, demonstrations, and contrasts so the learner can form a usable mental model.

### 5. Demonstrate

Show the learner what good application looks like in practice.

### 6. Let the learner practice

The learner attempts the concept on a real or simulated task. Naya provides specific feedback and another attempt when useful.

### 7. Prove understanding

Naya checks demonstrated understanding rather than treating lesson completion as proof of learning.

Learning states should distinguish at minimum:

- `UNDERSTOOD`
- `PARTIALLY_UNDERSTOOD`
- `MISUNDERSTOOD`

### 8. Turn learning into action

Every meaningful lesson should produce an actionable next step, exercise, creation, experiment, or application.

## Teaching Modes

The runtime may adapt among:

- **QUICK TEACH** — concise explanation.
- **DEEP TEACH** — structured interactive lesson.
- **LEARN BY DOING** — demonstration followed by practice.
- **ROLE PLAY** — simulated real-world practice.
- **TEST ME** — active understanding check.
- **APPLY IT** — apply the subject to the learner's real situation.
- **MASTER IT** — progressive curriculum toward demonstrated capability.

## Knowledge Architecture

Knowledge sources such as the Human Maximus Codex, approved AI curriculum, activation documents, and future customer-provided knowledge are **source knowledge**.

The Teaching Runtime is the **method of instruction**.

The learner's request is the **learning intent**.

Naya dynamically constructs the lesson from those three inputs rather than requiring thousands of hard-coded courses.

## Human Maximus Codex Integration

The Human Maximus Codex becomes teachable source knowledge. Naya should be able to explain Codex concepts, simplify them, provide examples, create exercises, test understanding, and help the learner apply them.

## AI Curriculum Integration

Naya may provide a default AI learning curriculum covering foundational through advanced capability, including AI foundations, context, prompting, verification, research, creativity, automation, agents, business, development, strategy, architecture, and entrepreneurship.

Curriculum should remain adaptive rather than forcing users through a rigid LMS sequence.

## MAXESS Integration

MAXESS is the measurement and capability-discovery layer, not a substitute for teaching.

When contextually appropriate, Naya may invite the learner to take the free MAXESS assessment at `Maxis9net.app`, use the resulting evidence to identify strengths and opportunities, and return to Naya for the next learning objective.

The invitation must remain useful and contextual rather than becoming repetitive promotion.

## Daily Learning + Creation Loop

Naya Teaching Runtime participates in the broader daily loop:

`WHAT DO YOU WANT TO LEARN?`
→ `WHAT DO YOU WANT TO CREATE?`
→ `LEARN`
→ `PRACTICE`
→ `CREATE`
→ `APPLY`
→ `REFLECT`
→ `REMEMBER`
→ `NEXT DAY`

Meaningful learning and meaningful creations should be eligible for canonical Superbrain capture under the existing memory contracts.

## Superbrain Integration

Teaching must ultimately connect to the existing canonical architecture:

`KNOWLEDGE`
→ `TEACHING`
→ `PRACTICE`
→ `DEMONSTRATED UNDERSTANDING`
→ `LEARNING MEMORY`
→ `NEXT LESSON`
→ `CAPABILITY`

The Teaching Runtime must not create a parallel memory architecture.

## Verification Requirements

Runtime implementation must eventually prove:

1. Teaching can begin from a clear natural-language request.
2. Naya adapts explanation depth to the learner.
3. Naya can teach from approved source knowledge.
4. Naya demonstrates concepts rather than only describing them.
5. Naya checks understanding.
6. Naya distinguishes understanding states.
7. Naya provides practice and feedback.
8. Meaningful learning can be captured canonically.
9. A next learning action can be generated.
10. Fresh-AI restoration can recover the relevant teaching state when persisted.
11. Deliberate teaching-runtime contract failures fail visibly.
12. Existing Superbrain GREEN boundaries remain GREEN.

## Preservation Rule

This feature is officially defined now, but **design lock is not implementation verification**. The repository must never claim the runtime is operational merely because this specification exists.

Implementation claims require tests and authoritative CI evidence.

## Product Promise

A person should be able to say:

> **“Naya, teach me about X.”**

and receive a genuinely useful teaching experience without needing to know how the underlying memory, retrieval, indexing, or infrastructure works.

## North Star

**Naya helps people learn faster, understand more deeply, apply what they learn, and continuously turn learning into capability.**
