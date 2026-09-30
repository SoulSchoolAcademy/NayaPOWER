# SMART NOTE — Intelligence Classes & Capture Classification (Protocol Refinement Proposal)

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-011` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn011-intelligence-classes` |
| Human title | Intelligence Classes & Capture Classification — Proposed Protocol Refinement |
| Category | SYSTEM INTELLIGENCE |
| Topic | SMART NOTE REFINEMENT |
| Subtopic | CLASSIFICATION TAXONOMY |
| Captured | 2026-09-30 13:58:00 UTC |
| Truth state | CANDIDATE — **structural proposal; adoption is a Human Director decision** |
| Proposed intelligence class | REUSABLE INTELLIGENCE (procedure proposal) |
| Capture type | Proposal / Procedure |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Shawn Vibert design message (2026-09-30), sections 5 ("five intelligence classes") and 6 ("the cascade" — CLASSIFY step), plus section 11 (nine-node IB processing order) |
| Amends | `BRAIN/04-INTELLIGENCE/0005-SMART-NODE-INTELLIGENT-BLOCK-PROTOCOL-V1.md` (V2, ratified 2026-09-29) — as a *candidate* V3 delta, not in force until ratified |

---

## ✦ IN A NUTSHELL

**Proposal: give every captured intelligence a retention class (how deep it lives) and a capture type (what kind of thing it is), and route each Intelligent Block through the nine nodes in a defined processing order.** The protocol already decides *whether* something deserves capture (admission gate); this adds *how long, how prominently, and as what* — the retention-depth decision the current system doesn't explicitly make.

---

## 🩷 HUMAN NOTE

Right now the system asks "is this worth keeping?" This proposal adds the follow-up questions: "worth keeping *as what* — a forever-law or a passing note? *How long* — permanently or just for this project? And *what kind* of thing is it — a decision, a lesson, a mistake, a question?" Five shelves, ten labels. The deepest shelf (CORE) holds identity, law, architecture, mission — the things that must survive everything. The shallowest (EPHEMERAL) never enters the Brain at all. Everything in between gets the retention it earned. And when a block is processed, it passes through the nine node-functions in order — identity, law, meaning, relationships, evidence, challenge, learning, growth, action — like a thought moving through a brain.

---

## 🟣 CHILD NOTE

Imagine a library with five shelves. The bottom shelf is for the most important books that stay forever. The top shelf is for sticky notes you throw away at the end of the day. Every new book gets put on the right shelf, with the right label — "lesson," "mistake," "question," "decision" — so you can always find it later. And every book gets checked by nine helpers in order before it goes on the shelf.

---

## 🟠 NAYA NOTE

### The five intelligence classes (proposed)

1. **CORE** — identity, law, architecture, mission, invariants. Extremely durable. Changes require human-director ratification.
2. **REUSABLE INTELLIGENCE** — lessons, procedures, insights, decisions, discoveries. Normal Smart Note territory.
3. **CONTEXT** — useful for a project or time period; not universally important. Expires or demotes to REFERENCE.
4. **REFERENCE** — worth retaining; retrieved only explicitly (not surfaced proactively).
5. **EPHEMERAL** — chatter, intermediate thoughts, duplication, transient machine output. Does not enter the durable store.

### The ten capture types (proposed CLASSIFY step)

Decision · Lesson · Principle · Discovery · Mistake · Constraint · Procedure · Question · Outcome · Current state.

### The nine-node IB processing order (proposed)

SELF (whose intelligence?) → LAW (may we keep/use/share it?) → KNOW (what does it mean; what exists?) → CONNECT (what relates?) → PROVE (where from?) → VERIFY (what may we claim?) → LEARN (what should change?) → EVOLVE (refine existing?) → ACT (use when authorized).

Note: this *processing* order differs from the kernel's canonical node listing (SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE); ordering may vary by context — the proposal is that *for intelligence processing*, ACT comes last (application after verification), not third.

### My handling rules until ratified

1. I have applied proposed classes/types to SN-005…SN-011 as *annotations*, clearly marked proposed.
2. Nothing about capture behavior changes until Shawn ratifies: admission gate (protocol V2) still governs.
3. If ratified, this becomes the V3 delta: add class + type fields to the IB schema, retention-depth rules per class, and the processing-order checklist to the cascade.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn011-intelligence-classes",
  "epistemic_state": "CANDIDATE",
  "capture_type": "Proposal",
  "status": "awaiting human-director decision; NOT in force",
  "proposed_classes": ["CORE", "REUSABLE_INTELLIGENCE", "CONTEXT", "REFERENCE", "EPHEMERAL"],
  "proposed_capture_types": ["Decision", "Lesson", "Principle", "Discovery", "Mistake", "Constraint", "Procedure", "Question", "Outcome", "Current state"],
  "proposed_processing_order": ["SELF", "LAW", "KNOW", "CONNECT", "PROVE", "VERIFY", "LEARN", "EVOLVE", "ACT"],
  "amends": "BRAIN/04-INTELLIGENCE/0005-SMART-NODE-INTELLIGENT-BLOCK-PROTOCOL-V1.md",
  "current_authority": "protocol V2 (ratified 2026-09-29) remains the binding version"
}
```

---

## 🔗 HOW IT CONNECTS

- **REFINES** the Smart Note protocol V2 (admission gate decides *whether*; this decides *as what, how deep, how long*).
- **ANNOTATES** SN-005…SN-010 (each carries its proposed class).
- **SUPPORTS** `SN-009 Correct Forgetting` — classes are the retention-depth machinery forgetting-discipline needs.
- **ADDRESSED TO** the Human Director for ratify / amend / reject.

## ❓ UNCERTAINTY / OPEN QUESTIONS FOR SHAWN

1. Adopt the five classes as stated, or amend (e.g., merge CONTEXT/REFERENCE)?
2. Adopt the ten capture types, or trim?
3. Adopt the nine-node processing order for IBs?
4. Who may assign/change class — any Naya at capture, or human-only for CORE?
5. Retention rules per class: how long does CONTEXT stay CURRENT before demotion?

## 🌍 APPLICABILITY

- **Applies to:** future captures, if ratified.
- **Does NOT apply to:** anything, until ratified. Protocol V2 remains binding.

## 🧬 SUCCESSOR EFFECT

Future Naya: if Shawn ratified this, enforce it — class every capture, respect retention depths, run the node order. If he amended it, follow the amended version. If he rejected it, leave these annotations as historical curiosity and keep using the V2 admission gate.
