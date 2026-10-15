# SMART NOTE — One artifact = one canonical compiler

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1407` |
| Intelligent Block | `IB-SMART-NOTE-20261015-sn1407-one-artifact-one-canonical-compiler` |
| Human title | One artifact = one canonical compiler (the two-writers hand-edit trap) |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | CANONICAL PLACEMENT |
| Captured | 2026-10-15 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**Two sanctioned compilers writing one detector-guarded artifact will fail forever.** The hand-edit detector can't tell "my co-author" from "a stranger" — each writer's output is the other's "hand edit," so every run exits 3 indefinitely. Thirty-plus failures on #2601 before the root cause was named. The rule: one artifact, one canonical compiler; humans touch only stable sections.

---

## 🩷 HUMAN NOTE

The master directive #2601 failed its hand-edit check more than thirty times in a row, and nobody could figure out why. The cause was embarrassingly structural: TWO official compilers were both allowed to write the same file. The detector that guards against unauthorized edits works by fingerprinting each writer's output — but two writers never produce byte-identical output, so every run looked at the other writer's work and concluded "a human touched this — stop."

The fix isn't better writing; it's single ownership. One artifact gets exactly one canonical compiler. Everything routes through it. Humans edit only the sections marked stable (the parts the compiler never rewrites). Two writers on one guarded artifact is not redundancy — it's a deadlock with a timer.

---

## 🟣 CHILD NOTE

If two kids share one diary and each writes in their own handwriting, the diary's "someone else wrote in my diary!" alarm goes off every time — even though both kids are allowed. The alarm can't read intentions, only handwriting. Solution: one kid keeps the diary, or the other kid uses the same pen and same handwriting. Never two different handwritings on one alarmed diary.

---

## 🔵 GRANDMA NOTE

A guard dog was trained to bark at strangers' handwriting on the ledger. Two trusted bookkeepers alternated entries, and the dog barked at each one — not because either did wrong, but because the dog can only tell handwriting, not trust. Thirty alarms later, the lesson: either one bookkeeper keeps the ledger, or you teach the dog both handwritings. A guard that can't distinguish authorized variety from intrusion will fail you on schedule.

---

## 🟠 NAYA NOTE

I file this as a canonical-placement law because it's the same shape as other "two truths, one slot" failures I've distilled: the system didn't have a writer bug, it had an ownership bug. Any guard that fingerprints output (hand-edit detectors, content-addressed pins, signed sections) implicitly assumes one canonical writer. The moment a second sanctioned writer appears, the guard's false-positive rate goes to 100% — not 50%, 100%, because the writers alternate. When I commission writers for a guarded artifact, the first question is now: who is THE compiler, and what route do all other edits take to reach it?

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261015-sn1407-one-artifact-one-canonical-compiler",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-15",
  "lesson": "Two sanctioned compilers on one hand-edit-detector-guarded artifact produce permanent exit-3 failures: each writer's output is the other's 'hand edit'.",
  "rule": "One artifact = one canonical compiler; all writes route through it; humans touch stable sections only.",
  "decision_change": "Before adding a second writer/compiler to a detector-guarded artifact, designate one canonical compiler and route all writes through it — or disable the detector. Never add a second sanctioned writer to a guarded artifact.",
  "falsifier": "Two independent compilers round-trip an artifact through the hand-edit detector with zero false positives (requires shared canonicalization).",
  "mechanism": "The hand-edit detector fingerprints writer output; two writers never produce byte-identical output, so each run reads the other's output as a foreign hand edit -> exit 3, permanently.",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6196434078",
    "failure_class": "F5 repeat",
    "symptom": "#2601 HAND_EDIT_DETECTED x30+",
    "root_cause": "TWO sanctioned compilers, one artifact"
  },
  "related": ["L349"]
}
```
