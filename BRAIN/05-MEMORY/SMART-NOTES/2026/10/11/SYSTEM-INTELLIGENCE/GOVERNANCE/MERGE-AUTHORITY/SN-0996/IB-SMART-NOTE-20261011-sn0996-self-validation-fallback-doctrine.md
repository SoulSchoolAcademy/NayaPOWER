# SMART NOTE — Self-Validation Fallback Doctrine (LAW-lane decision)

> **Self-validation is a legitimate fallback — distinct from independent verification, with protected actions permanently excluded, and it must be built as machinery before it can replace the live gate.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-0996` |
| Intelligent Block | `IB-SMART-NOTE-20261011-sn0996-self-validation-fallback-doctrine` |
| Human title | Self-Validation Fallback Doctrine (LAW-lane decision) |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | MERGE-AUTHORITY |
| Captured | 2026-10-11 16:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**Self-validation and independent verification are different things — and self-validation is legitimate as a fallback, not as a substitute.** The LAW lane's crisp decision on the merge-bottleneck law/runtime conflict: self-validation may stand in when distinct-seat review is unavailable, with two iron boundaries — **protected actions are permanently excluded**, and **the fallback must be built as machinery** (schema + exact-head gate tests + explicit exclusions + negative-control proof). Until that machinery exists and is wired in by Shawn's word, the live distinct-seat gate governs — **never bypass it**.

---

## 🩷 HUMAN NOTE

There's a difference between "I checked my own work carefully" and "someone else checked my work." Both have value; they are not the same thing.

The decision: careful self-validation is a legitimate fallback when a second reviewer genuinely isn't available — it is quality discipline, not theater. But it can never be the final word on protected actions (merges into main, deploys, anything irreversible). And it only counts when it's built as a real mechanism — a schema, tests pinned to the exact head being judged, a written list of what it can never approve, and proof that it actually catches bad work (negative controls).

Until that mechanism is built and Shawn says "wire it in," the live rule stands: independent review required, no bypasses, no exceptions.

---

## 🟣 CHILD NOTE

Imagine you're building a tower and you check your own work three times — that's good and honest. But it doesn't replace having a friend check it too, especially before you do something you can't undo. If the friend isn't around, your careful self-check is a fine backup — as long as you wrote down exactly how you check, what you will never approve by yourself, and you proved your check actually catches mistakes.

---

## 🔵 GRANDMA NOTE

Checking your own work carefully is respectable and real — but it's not the same as someone else checking it, and it can never be the final word on anything you can't take back. If we ever want self-checking to count at a merge, it has to be a proper written-down machine of a process: what it checks, the exact version it checked, what it's forbidden to approve alone, and proof it catches errors. Until then, the rule stays: someone else checks it first.

---

## 🟠 NAYA NOTE

This is the LAW lane's resolution of the merge-bottleneck law/runtime conflict (2026-10-11), and it refines — not replaces — SN-0992's distinction (self-validation ≠ independent verification). The decision adds **legitimacy** and **build requirements**:

1. **Legitimate fallback:** self-validation (three honest builder cycles, target 10, floor 9) is an authorized fallback when distinct-seat validation is unavailable — not a substitute, not an evasion.
2. **Permanently excluded:** protected actions (merges, deploys, irreversible operations, authority changes) can never be self-validated, machinery or not. No score overrides a hard gate.
3. **Built as machinery:** the fallback must exist as code and schema — a decision-receipt schema, exact-head gate tests, an explicit exclusion list, and negative-control proof that the mechanism catches bad work. Prose descriptions do not qualify.
4. **Until wired, the live gate governs:** building the fallback does not authorize its use. Wiring it into merge acceptance is Shawn's gate. Never bypass the distinct-seat requirement on the promise that the fallback "will exist."

Merge authority stays with the merge lane; owning lane builds the fallback as an unwired draft PR.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261011-sn0996-self-validation-fallback-doctrine",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11T16:45:00Z",
  "doctrine": {
    "self_validation_is": "legitimate fallback when distinct-seat validation unavailable; quality discipline, not a receipt",
    "self_validation_is_not": "independent verification; never a substitute for a cross-seat receipt",
    "permanently_excluded": ["merges", "deploys", "irreversible operations", "authority/consent/security/privacy changes"],
    "machinery_requirements": [
      "decision-receipt schema",
      "exact-head gate tests (pinned head SHA)",
      "explicit exclusion list",
      "negative-control proof (demonstrated to catch bad work)"
    ],
    "wiring_gate": "Shawn's word; until wired, live distinct-seat gate governs — never bypass"
  },
  "evidence": [
    {"board": "#1718", "comment": 6111064258, "kind": "LAW-lane crisp decision on merge-bottleneck law/runtime conflict"},
    {"board": "#2175", "comment": 6111076567, "kind": "LAW-DRIVER run completion sign-out 2026-10-11 ~09:40 PDT"},
    {"board": "#2175", "comment": 6111051073, "kind": "distinct-seat [NAYA 4 · REVIEW] APPROVED + ## SCORECARD 9.5/10 on PR #2347 head e29be874 (example of the live gate working)"}
  ],
  "related_notes": ["SN-0992 (self-validation is not independent verification — the distinction; this note adds legitimacy + machinery requirements)", "SN-0994 (12 Laws boundary: high value score never authorizes a forbidden action)"],
  "supersedes": null
}
```

---

## ⚠️ TRUTH BOUNDARY

**Proven:** the LAW lane rendered this decision with exact receipts on 2026-10-11; the fallback machinery does not yet exist. **Not implied:** self-validation currently satisfies any merge gate (it does not); Shawn has approved wiring (he has not). Candidate doctrine, not ratified law.

This IB remains **CANDIDATE** — only Shawn ratifies.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
