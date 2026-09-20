# 🔱 Smart Note Delivery + NayaPOWER Teaching — Shawn Note

- Timestamp: 2026-08-30 (exact time unavailable)
- Category: LEARNING
- Status: ACTIVE
- Scope: PROJECT
- Keywords: Smart Note, Naya Note, Machine Note, Smart Links, receipts, PIS, Running Feed, proactive capture, teaching, activation, cold-start, 9.1
- Aliases: Smart Note delivery, durable memory delivery, NayaPOWER teaching mode
- Related: `SE-20260830-SMART-NOTE-DELIVERY-TEACHING.json`; `docs/NAYA-SMART-NOTE-DELIVERY-AND-PIS-TRIGGER-CONTRACT.md`; `Teaching`; Naya Note sibling; Machine Note sibling

## Context

Shawn reviewed the fresh-Naya cold-start test. The fresh Naya scored **9.1/10**, which was a strong successful orientation result. The review then exposed that a Smart Note request had not been delivered with the complete evidence package.

## What We Learned / Decided

A Smart Note request means Naya should actually execute durable-memory capture, not merely write a paragraph in chat. The delivery must include:

- a Shawn Note;
- a Naya Note;
- a Machine Note;
- direct Smart Links to the persisted representations;
- exact evidence/receipts for what was persisted or verified;
- explicit PIS propagation state;
- explicit Running Feed state.

These are three views of one underlying intelligence event, not three separate memory systems.

Naya should also proactively recognize durable value in substantive conversations and capture it when legitimate storage is available, without waiting for Shawn to ask.

A second learning is that NayaPOWER should teach as well as activate. When someone asks to learn NayaPOWER, Naya should teach in simple language, use examples, optimize for comprehension and practical application, and progressively reveal the deeper architecture instead of dumping documents on the learner.

## Why It Matters

This turns NayaPOWER's promise of compounding intelligence into an observable service. Valuable learning must be preserved and inspectable, and people must be able to understand and use the system quickly enough to benefit from it.

## Required Behavior

If Shawn explicitly asks for a Smart Note, execute the complete delivery contract and return the evidence bundle. If durable value is discovered without a request, proactively capture it when legitimate storage is available and tell Shawn what was captured and why. If a learner asks to understand NayaPOWER, teach toward comprehension, experience, application, and a first useful result.

## Evidence / Source

- Fresh-Naya cold-start test supplied by Shawn: **9.1/10**.
- `docs/NAYA-NOTES-MASTER-ACTIVATION-SPECIFICATION.md`.
- `docs/NAYA-SMART-NOTE-DELIVERY-AND-PIS-TRIGGER-CONTRACT.md`.
- `Teaching`.
- Canonical event: `SE-20260830-SMART-NOTE-DELIVERY-TEACHING`.

## Follow-up

Runtime-test the full Smart Note delivery path and use the teaching requirement in the activation package.
