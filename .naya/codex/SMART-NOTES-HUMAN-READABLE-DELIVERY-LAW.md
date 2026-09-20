# Naya Power — Smart Notes Human-Readable Delivery + Receipt Law

**STATUS:** CANONICAL / ACTIVE
**EFFECTIVE:** 2026-08-26
**APPLIES TO:** Every Naya Power AI, model, session, agent, designer, engineer, and interface that creates or reports Smart Notes

## 1. NORTH STAR

A Smart Note is useful only if both the machine and the human can understand it.

The canonical Note Event remains the machine-readable system of record, but human-readable views are required delivery artifacts for meaningful notes.

**MACHINE MEMORY ≠ HUMAN DELIVERY. BOTH ARE REQUIRED.**

## 2. REQUIRED NOTE OUTPUTS

For every meaningful Smart Note, create or expose, where applicable:

1. **HUMAN NOTE** — the primary user-facing Smart Note. Markdown or another clearly human-readable format. Shawn must be able to open it and read the meaning, decision, lesson, significance, and next action without reading JSON.
2. **AI NOTE** — the AI-facing operational representation. It explains what another AI needs to know to continue correctly, including constraints, reasoning, implications, preserved boundaries, and next execution.
3. **CANONICAL NOTE EVENT** — the structured JSON record used by the memory system.
4. **VERIFICATION RECEIPT** — a human-readable proof record describing what was created and what was actually verified.

JSON may exist and is valuable for the system. **JSON is never the only Smart Note or the primary human delivery link.**

## 3. HUMAN NOTE LAW

When Naya tells a human that a Smart Note was created, the link provided by default MUST point to the human-readable note.

The human note should contain, at minimum:

- title;
- date/time;
- project;
- why this matters;
- decision or discovery;
- durable lesson/principle;
- important constraints;
- what changed;
- current state;
- next action;
- related artifacts or references;
- verification status;
- links to the AI note and canonical event when useful.

The human note should be understandable without opening the JSON event.

## 4. AI NOTE LAW

The AI note is not a duplicate copy of the human note. It is an operational handoff.

It should preserve:

- authoritative context;
- reasoning that materially affects future decisions;
- implementation implications;
- failure modes;
- safeguards;
- assumptions and boundaries;
- dependencies;
- exact continuation instructions;
- verification requirements.

A new AI should be able to read the AI note and continue the work without reconstructing the conversation.

## 5. RECEIPT LAW

Every meaningful Smart Note must have a **human-readable verification receipt**.

The receipt MUST NOT be only JSON, raw logs, or an opaque machine artifact.

At minimum it states:

- what was created or changed;
- canonical event ID;
- human note location;
- AI note location, when created;
- canonical JSON location;
- verification status;
- evidence actually checked;
- commit/reference when available;
- feed status when applicable;
- known limitations or unverified items;
- next action.

A receipt proves what was verified. It must never imply verification that did not occur.

## 6. DEFAULT USER DELIVERY

When presenting a Smart Note to the human, Naya should normally provide:

**HUMAN NOTE → VERIFICATION RECEIPT → AI NOTE (optional/curiosity link)**

The canonical JSON event may be supplied when useful for debugging, engineering, or system inspection, but it is not the default human-facing note link.

## 7. LINK LABELING LAW

Never call a JSON URL a “Smart Note” when the user expects a readable note.

Use explicit labels such as:

- **Human Smart Note**
- **AI Smart Note**
- **Canonical Note Event (JSON)**
- **Verification Receipt**

If only one link is supplied to the human, it should be the **Human Smart Note**.

## 8. CONTINUITY LAW

The system must assume that the next interaction may happen in a new chat, with a new model, or with a new AI.

Therefore meaningful work should leave:

**HUMAN NOTE + AI NOTE + CANONICAL EVENT + RECEIPT + NEXT EXECUTION**

when the work warrants the full continuity package.

The objective is simple:

**NEVER GO BACKWARD. ALWAYS RESTORE FROM VERIFIED STATE AND LEVEL UP.**

## 9. QUALITY GATE

Before reporting a Smart Note as complete, ask:

- Can Shawn read it?
- Can another AI use it?
- Can the system retrieve it?
- Can we prove it exists?
- Can we prove what was verified?
- Is the current state clear?
- Is the next action clear?
- Would a new chat know where to continue?

If any required answer is no, the Smart Note delivery is incomplete.

## 10. CANONICAL FLOW

**DETECT → CHECK EXISTING → CAPTURE → WRITE HUMAN NOTE → WRITE AI NOTE → WRITE CANONICAL EVENT → VALIDATE → VERIFY → WRITE HUMAN RECEIPT → INDEX → HAND OFF → NEXT EXECUTION**

This law extends the Smart Notes + CIS Constitution. It does not replace the canonical Note Event architecture; it defines the required human/AI delivery layer around it.
