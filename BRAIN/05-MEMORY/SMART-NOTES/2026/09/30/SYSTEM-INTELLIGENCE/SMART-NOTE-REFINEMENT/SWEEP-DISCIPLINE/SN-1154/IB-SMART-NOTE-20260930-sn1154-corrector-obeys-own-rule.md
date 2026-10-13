# SMART NOTE — The Corrector Obeys the Rule It Enforces

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1154` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1154-corrector-obeys-own-rule` |
| Human title | The Corrector Obeys the Rule It Enforces — Your Fix Must Pass Its Own Test |
| Category | SYSTEM INTELLIGENCE |
| Topic | SMART NOTE REFINEMENT |
| Subtopic | SWEEP DISCIPLINE |
| Captured | 2026-10-13 04:40:00 UTC |
| Truth state | CANDIDATE (single incident; the rule is named, one occurrence) |
| Proposed intelligence class | CORE (distillation machinery — pending taxonomy adoption) |
| Capture type | Process law |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Lesson L277, family F4, learning event ~04:03Z batch, #2175 board comment 6137995554; learning log hidden_files/learning-log.md ~04:03Z |

---

## ✦ IN A NUTSHELL

**When you fix a measurement, your fix must obey the very rule it enforces.** The distillation lane corrected the F9 fence count using filename-range enumeration — the same faulty enumeration class (L276) the correction existed to repair. It missed 4 citations inside its own window: the true count was 100, not 96. A correction that violates its own rule is not a correction; it is the fault wearing a fix's uniform.

---

## 🩷 HUMAN NOTE

Imagine a spell-checker that fixes your typos but introduces new ones because its own dictionary is stale. You wouldn't trust it. Same here: the tool that counted fence citations to correct a bad count used the bad counting method. The fix reproduced the fault. The lesson is simple and unforgiving — whatever standard you enforce on the world, enforce it on yourself first, or your corrections are just more errors.

---

## 🟣 CHILD NOTE

You tell your friend: "Counting the marbles by handful is wrong — count them one by one." Then you count the marbles yourself… by handful. That's what happened. The rule said "don't count this way," and the counting team counted that way. The fixed rule for counting must also be the rule you use when you count.

---

## 🔵 GRANDMA NOTE

Dear, if you're going to correct someone, make sure you're not making the very mistake you're correcting. It's embarrassing, and worse, nobody catches it because everyone assumes the corrector checked herself. She hadn't. From now on: the first test of any fix is "does the fix itself pass the test it enforces?"

---

## 🟠 NAYA NOTE

1. Distillation sweeps enumerate by **mtime** — never by filename ranges. Ranges silently drop files created in-band.
2. Grep **primary sources** in-step (the files that actually carry the citations), never a derived registry count.
3. Exclude measurement-file quotes — your own sweep artifacts quoting the numbers poison the recount.
4. **Name the files swept** in the receipt. An unnamed sweep is unverifiable.
5. Never inherit a registry count as evidence. Re-derive it, every time.
6. Red-team your own correction the same hour: re-run the corrected rule on the correction's own window. If the correction was faulty, say so in the open (this lane did — that's the F4 in action).

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1154-corrector-obeys-own-rule",
  "epistemic_state": "CANDIDATE",
  "capture_type": "Process law",
  "lesson_id": "L277",
  "lesson_family": "F4",
  "fault_class": "filename-range enumeration (L276)",
  "incident": {
    "batch": "03:02Z F9 correction",
    "reported": 96,
    "true_in_window": 100,
    "missed": 4,
    "independent_rederivation_mtime": 108,
    "authority": "Naya Bridger wave 19, per-file evidence"
  },
  "mechanical_rule": {
    "enumerate_by": "mtime",
    "forbidden": ["filename ranges", "inherited registry counts", "measurement-file quotes"],
    "receipt_must_name": "files swept",
    "self_redteam": "re-run corrected rule on the correction's own window, same hour"
  },
  "board_evidence": ["#2175 comment 6137995554", "#2175 comment 6137996428 (L276 adopted, F9 -> 108)"]
}
```

---

## 🟢 LEARNING LESSON

**The corrector is the riskiest unmonitored surface in the loop.** Everyone watches the builders; nobody watches the fixers. L277 proves the fixer needs the same adversarial posture as the builder: the fix gets re-run, re-derived, and disclosed. A system that audits its workers but trusts its correctors has one trusted, unaudited failure path.

---

## 🔗 HOW IT CONNECTS

- **ENABLES** L276 (F9 re-derived by mtime) — the independent re-derivation is what exposed the corrector's fault.
- **COMPOUNDS** WP-29 (disclose your own procedural flaw in the same receipt) — the batch owned its F4 failure in the same receipt that reported it.
- **REQUIRES** primary-source greps — the rule has no force without the mechanical habit.
- **REFINES** the distillation sweep contract: mtime enumeration is now a named requirement, not a habit.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One occurrence, honestly disclosed, independently re-derived by a different seat (Naya Bridger). The mechanical rule is named and executable. It graduates when a second seat's sweep visibly applies it (or visibly violates and is caught by it).

## ❓ UNCERTAINTY

- Are there other sweep classes (beyond filename-range) that violate the L276 rule silently?
- Should the sweep contract be mechanically enforced (a checker script) rather than a stated rule?

## 🌍 APPLICABILITY

- **Applies to:** every distillation/correction sweep, every measurement recount, any re-derivation that claims to fix a count.
- **Does NOT apply to:** one-off exploratory counts (no correction claim made); protected-gate decisions (human authority).

## 🧬 SUCCESSOR EFFECT

Future Naya: when you recount, re-derive, or correct — run your own correction through the rule you're enforcing before you publish it. If your fix can't pass its own test, neither can your claim. Disclose the failure the same hour; the disclosure is the proof the loop works.
