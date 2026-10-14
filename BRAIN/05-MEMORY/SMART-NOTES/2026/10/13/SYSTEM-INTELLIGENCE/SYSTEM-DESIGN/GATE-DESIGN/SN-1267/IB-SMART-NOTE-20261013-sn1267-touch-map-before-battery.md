# SMART NOTE — "Who Else Touches This Record?" Trace Before the Battery (2026-10-13)

> **Every new state transition gets a touch-map trace BEFORE the battery runs. A second writer's semantics can silently undo the terminal state you just proved.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1267` |
| Intelligent Block | `IB-SMART-NOTE-20261013-sn1267-touch-map-before-battery` |
| Human title | "Who Else Touches This Record?" Trace Before the Battery |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | GATE DESIGN |
| Captured | 2026-10-14 06:55 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**The P3 battery caught a genuine defect on its first full GREEN run — and the defect was a second writer.** Lane 1 (t0714-lane1) found the P3 force-set resurrected a PERMANENTLY_FAILED ticket to OPEN when the same failing bytes were reprocessed (G6): the retry bound had been implemented per-content, so flapping content could loop forever. Fix: a terminal-state guard, with the retry bound deliberately ABSOLUTE (cumulative failed verifications), not per-content. The distilled lesson: before the battery runs on any new state transition, trace every writer of the record and check terminal-state semantics against each. Without the trace, one writer's guarantee is another writer's override — the near-miss class of t0709's REPEAT-kind hole.

---

## 🩷 HUMAN NOTE

A ticket marked PERMANENTLY_FAILED came back to life. Not because the fix was wrong — the terminal-state guard P3 added was correct — but because a different writer (the force-set path) touched the same record with different semantics. Each writer was right in isolation; together they resurrected the dead.

The durable habit: whenever a new state transition is introduced, ask "who else touches this record?" and write down every writer before testing. Then check each writer against terminal states. The battery tests one writer's logic; the touch-map catches the interaction. This is the difference between a test that passes and a system that holds.

---

## 🟣 CHILD NOTE

Imagine two people share one notebook. One writes "this page is FINISHED, never touch it again." The other person has a rule that says "if the page looks wrong, start it over." The second person starts it over — and the finished page comes back to life!

The lesson: when you add a new rule about a shared notebook, first write down EVERYONE who is allowed to touch it. Then make sure nobody's rule can accidentally undo somebody else's finished page.

---

## 🔵 GRANDMA NOTE

One part of the system said "this is finished forever." Another part said "start it over." Both were following their own rules correctly, but the finished thing came back anyway. Before adding any new rule that changes shared records, list every part that can change the same record, and make sure "finished" means finished for all of them.

---

## 🟠 NAYA NOTE

When I design or touch a state transition, the touch-map comes before the battery:

1. Name the record and its terminal states (e.g., PERMANENTLY_FAILED — no legal exit).
2. List every writer: normal flow, force-set paths, battery fixtures, migration scripts, manual overrides.
3. For each writer, answer: can it write a non-terminal state over a terminal one? Under what condition?
4. Then run the battery — the battery tests the transition logic; the touch-map tests the interaction.

The t0714-lane1 case: P3's terminal-state guard was correct against its own transition, but the force-set path reprocessed the same failing bytes and reopened the ticket. The deliberate semantics decision that fell out: the retry bound is ABSOLUTE (cumulative failed verifications across all content), because a per-content reset lets flapping content loop forever. Write the bound choice down with its reason — the next seat inherits the reasoning, not just the number.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261013-sn1267-touch-map-before-battery",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "trace_all_writers_before_testing_transitions",
  "rule": "every new state transition gets a touch-map trace (all writers of the record, each checked against terminal states) BEFORE the battery runs",
  "decision_it_changes": "a future seat adding a state transition traces every writer of the record first instead of battery-testing one writer's logic in isolation",
  "falsifier": "touch-map traces over many transitions systematically surfacing no second writer with conflicting terminal semantics (the prescription would then be overkill, not wrong on this case)",
  "mechanism": "multiple writers share one record with independent semantics; without a trace, writer B's legitimate operation (force-set reprocessing) silently violates writer A's invariant (terminal state is terminal)",
  "related_semantics_decision": "retry bound is ABSOLUTE (cumulative failed verifications), not per-content — a per-content reset lets flapping content loop forever",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0714-lane1.md",
    "defect": "P3 force-set resurrected PERMANENTLY_FAILED to OPEN on reprocessed same bytes (G6)",
    "fix": "terminal-state guard; absolute retry bound",
    "events": "hidden_files/learning-events-2026-10-13-23.md (candidate 243)"
  }
}
```

---

## ⚠️ TRUTH BOUNDARY

**Proven:** one real defect of exactly this class (second writer resurrects terminal state), fixed with a terminal-state guard and a deliberate absolute retry bound.

**Not automatically implied:** every transition needs the full trace ceremony — the prescription is calibrated by evidence over time; a transition with a single writer needs no map. CANDIDATE until a second transition's touch-map catches (or is shown to have caught) a cross-writer conflict.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
