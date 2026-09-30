# SMART NOTE — Correct Forgetting

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-009` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn009-correct-forgetting` |
| Human title | Correct Forgetting — History Must Not Masquerade as Current Truth |
| Category | SYSTEM INTELLIGENCE |
| Topic | MEMORY DISCIPLINE |
| Subtopic | CORRECT FORGETTING |
| Captured | 2026-09-30 13:58:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | CORE (memory architecture — pending taxonomy adoption, SN-011) |
| Capture type | Principle |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Shawn Vibert design message (2026-09-30): "Durable memory requires explicit supersession, historical classification, freshness and applicability so remembered history does not masquerade as current truth." (Candidate durable intelligence detected in-session.) |

---

## ✦ IN A NUTSHELL

**Forgetting correctly is part of intelligence. Durable memory requires explicit supersession, historical classification, freshness, and applicability — so that remembered history stays retrievable but never masquerades as current truth.** The smartest memory architecture is not the one that saves the most; it's the one that retains the right intelligence at the right depth.

---

## 🩷 HUMAN NOTE

Keeping everything forever isn't a good memory — it's hoarding. A good memory knows what to keep sharp, what to file away, and what to let go. The dangerous failure isn't forgetting; it's *half-remembering*: an old decision, an outdated state, a superseded instruction surfacing as if it were still true. Correct forgetting means every piece of intelligence carries its freshness date and its status — current, historical, or superseded — so the past informs the present without impersonating it.

---

## 🟣 CHILD NOTE

Imagine your notebook never throws anything away, and last year's class schedule is mixed in with today's. You'd show up to the wrong classroom! Smart forgetting means: old pages get a big stamp saying "OLD — history only," today's page stays on top, and nothing old ever pretends to be new.

---

## 🔵 GRANDMA NOTE

A wise person remembers the past without living in it, dear. Write down what happened, mark clearly when it was and whether it's still true, and don't let yesterday's news make today's decisions. That's all this asks of our system: honest dates, honest labels, and the discipline to say "that was true then."

---

## 🟠 NAYA NOTE

1. Every IB carries temporal state: CURRENT, HISTORICAL, or SUPERSEDED — plus freshness (when verified, when it expires).
2. Supersession is explicit: a new IB links SUPERSEDES to the old one; the old one is never silently edited or deleted (history stays retrievable).
3. Retrieval must rank CURRENT above HISTORICAL; a HISTORICAL block used in reasoning must be flagged as such.
4. Ephemeral material (chatter, intermediate output, duplication) should never enter the durable store — the admission gate (protocol V2 §4) plus the proposed EPHEMERAL class (SN-011) decide this.
5. When reconciling, prefer refining one canonical block over creating a near-duplicate.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn009-correct-forgetting",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "CORE",
  "capture_type": "Principle",
  "temporal_states": ["CURRENT", "HISTORICAL", "SUPERSEDED"],
  "required_fields": ["freshness/last-verified", "applicability-window"],
  "supersession_rule": "explicit SUPERSEDES link; old block retained, never silently mutated",
  "retrieval_rule": "CURRENT outranks HISTORICAL; historical use must be flagged",
  "anti_hoarding": "EPHEMERAL class material excluded at admission (see SN-011)"
}
```

---

## 🔗 HOW IT CONNECTS

- **REFINES** `SN-007 Continuity of Intelligence` — continuity without forgetting-discipline becomes continuity of *stale* intelligence.
- **ENABLED BY** the RECONCILE step of the Smart Note cascade — dedupe/supersede/conflict handling.
- **SUPPORTS** VERIFY — freshness is a verifiability property.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** The principle is stated; the machinery (temporal-state fields on IBs, supersession links, freshness-ranked retrieval) is partially present in the protocol but not yet enforced at runtime. Enforcement is the verification.

## ❓ UNCERTAINTY

- What are the retention-depth rules per class (how long does CONTEXT stay CURRENT)?
- Who/what may declare supersession, and does it need human ratification for CORE-class blocks?

## 🌍 APPLICABILITY

- **Applies to:** all IB lifecycle management, retrieval ranking, resolver outputs, board truth.
- **Does NOT apply to:** deleting history — historical blocks remain retrievable; forgetting means *demoting*, not erasing.

## 🧬 SUCCESSOR EFFECT

Future Naya: before acting on a retrieved block, check its temporal state. If it's HISTORICAL, say so out loud. If it's SUPERSEDED, follow the link to its successor. Never let the past impersonate the present on your watch.
