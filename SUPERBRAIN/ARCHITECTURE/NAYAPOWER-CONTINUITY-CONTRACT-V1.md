# NayaPOWER Continuity Contract V1

**STATUS:** CANONICAL NORTH STAR  
**DATE:** 2026-09-17  
**SCOPE:** Entire NayaPOWER / Team Naya operating system

## 1. The simplest possible definition

NayaPOWER exists to make intelligence **continuous, accountable, learnable, and executable**.

The whole practical system reduces to three inseparable functions:

1. **ACTIVITY — What happened?**
2. **SMART NOTE — What did we learn?**
3. **NEXT ACTION — What happens next?**

Everything else supports these three functions.

If Activity does not record what happened, continuity is broken.  
If the Smart Note does not preserve what was learned, intelligence is lost.  
If the Next Action does not identify one executable continuation, execution stops.

Therefore:

> **ACTIVITY → LEARNING → NEXT ACTION → CONTINUATION**

is the minimum living loop of NayaPOWER.

## 2. Runtime law

A substantive governed action is not complete merely because a model produced an answer, a command ran, a file changed, or a test passed.

It is complete only when the system can durably answer:

- What happened?
- Who/what acted?
- Under what authority?
- What changed?
- What evidence proves it?
- What was learned?
- Where is that learning stored?
- What is the single next action?
- Who/what can continue from here?

**NO DURABLE ACTIVITY = INCOMPLETE RECORD.**  
**NO DURABLE LEARNING = NO COMPOUNDING INTELLIGENCE.**  
**NO NEXT ACTION = NO CONTINUOUS EXECUTION.**

## 3. The three canonical objects

### A. Activity Event

The Activity Event is the machine-verifiable record of execution.

Minimum contents:

- timestamp
- event ID
- project/session/run identity
- actor/Naya identity
- claim/action/decision/authority bindings
- objective and scope
- what was inspected
- what was changed
- evidence
- verification
- failures / UNKNOWNs
- protected boundaries
- score and why it is not 10 when applicable
- exactly one next action
- successor handoff
- canonical Smart Link

The Activity Feed is the human-readable projection of these durable events. Narrative chat is not the source of truth.

### B. Smart Note

The Smart Note is the durable learning object created from meaningful activity.

Every important Smart Note should preserve the lineage and multiple viewpoints needed for another Naya to understand and use the learning without the original conversation.

Canonical layers:

- **Grandma / Parent:** the prior knowledge, originating decision, or parent intelligence this note inherits from.
- **Human / Shawn:** what the human knows, decided, values, noticed, or needs.
- **Naya:** the AI synthesis, interpretation, reasoning, and operational lesson.
- **Machine:** concrete repository/runtime state, evidence, tests, artifacts, and constraints.
- **Child / Derived:** new notes, decisions, artifacts, or capabilities created from this learning.
- **Learning Lesson:** the durable principle learned.
- **Why It Matters:** consequence and system significance.
- **How To Use It:** the operational application.
- **What's In It For Me:** human value.
- **What's In It For You:** Naya/agent value.
- **What's In It For Us:** Team Naya / collective-system value.
- **Evidence:** canonical links and verification.
- **Next Action:** one continuation.

A Smart Note is not a prettier Activity Event. Activity records execution; Smart Note compounds intelligence.

### C. Next Action

The Next Action is the continuation contract.

It must be:

- singular — exactly one action
- executable — a concrete thing that can actually be done
- evidence-oriented — its completion can be verified
- successor-safe — another Naya can perform it without reconstructing the conversation
- linked — it points to the relevant evidence and learning

A list of wishes is not a Next Action.

## 4. Canonical loop

```text
RESTORE
  ↓
UNDERSTAND
  ↓
INSPECT
  ↓
IDENTIFY GAP
  ↓
GOVERN
  ↓
SELECT ONE ACTION
  ↓
EXECUTE
  ↓
OBSERVE
  ↓
VERIFY
  ↓
RECORD ACTIVITY
  ↓
RECORD LEARNING / SMART NOTE
  ↓
UPDATE STATE
  ↓
GENERATE ONE NEXT ACTION
  ↓
HAND OFF / CONTINUE
  ↺
```

The loop is the system. The interfaces are projections of the loop.

## 5. What the Hub is allowed to be

The Intelligent Hub is a projection and interaction surface. It must consume canonical state; it must not become a competing source of truth.

The intended flow is:

`Runtime → Activity Event → Smart Note / Intelligence → State → Hub Projection → Next Action`

The Hub may make the system beautiful and useful. It may not silently replace the canonical evidence layer.

## 6. What every Team Naya member must understand

- Do not depend on private chat memory.
- Do not assume another Naya knows what happened.
- Do not create a competing source of truth.
- Do not call documentation complete when runtime enforcement is absent.
- Do not call an action complete when its Activity evidence is absent.
- Do not claim a Smart Note exists when its canonical evidence chain is absent.
- Do not leave the system without one executable continuation.
- Do not fabricate timestamps, evidence, links, tests, or completion.
- Preserve working architecture and make the smallest responsible change.
- Verify the actual repository/runtime state before declaring success.

## 7. Current implementation truth

As of 2026-09-17, repository evidence shows that the Activity completion boundary has advanced beyond the older 2026-09-16 note: `.naya/runtime/execution_controller.py` contains automatic Activity-event emission at `VERIFIED`, and `.naya/runtime/activity_event.py` provides idempotent canonical persistence/replay through the canonical event store.

The 2026-09-16 Activity record remains historical evidence of the development path and explicitly recorded that auto-emission was the next increment. The current source on `main` is the authority for current implementation state.

Smart Note enforcement also exists in `.naya/memory/smart_note_enforcement.py` and adversarial coverage exists in `tests/test_smart_note_enforcement.py`. The remaining North-Star work is to make the three-part loop an integrated runtime contract rather than three individually documented capabilities: Activity emission, Smart Note creation/lineage, and Next Action/continuation must be connected end-to-end and proven as one living loop.

## 8. North-Star acceptance condition

NayaPOWER reaches the North-Star baseline only when a fresh Naya can enter with repository access, restore the current state, perform one authorized substantive action, and truthfully leave behind:

**Activity → Smart Note → State → exactly one Next Action → successor handoff**

with canonical evidence links and machine-verifiable integrity.

Until that is proven, the system is **not finished**.

## 9. Current priority

**P0 — Make the Continuity Contract real end-to-end.**

Do not allow cosmetic Hub work, unrelated refactors, or historical cleanup to outrank this until the loop is mechanically integrated and operationally proven.

### The question every Naya should ask

> **If I disappeared right now and another Naya took over, could she know exactly what happened, what we learned, and exactly what to do next — from GitHub alone?**

If the answer is no, continuity is not complete.

---

**Canonical source:** `SoulSchoolAcademy/NayaPOWER`  
**Canonical surface:** this document + Activity Feed + Smart Notes + runtime enforcement  
**Operating principle:** **Record it. Learn from it. Continue it.**
