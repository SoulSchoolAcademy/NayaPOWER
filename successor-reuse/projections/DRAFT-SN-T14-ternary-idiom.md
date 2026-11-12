# SMART NOTE (DRAFT — ingestion candidate, NOT canonically captured)

> **Draft for the CAPTURE lane.** This file is an ingestion-ready candidate
> projection, not a canonical Intelligent Block. The canonical Receiver
> (`v7-smart-note-canonical`) remains the single capture path; no registry
> entry was written and no IB was minted by this draft. Truth state below is
> the draft's honest assessment, for the ingesting seat to adjudicate.

| Field | Value |
|---|---|
| Smart Note ID | `SN-DRAFT-T14` (to be assigned at ingestion) |
| Human title | Never write state files through inline conditional expressions |
| Category | ENGINEERING INTELLIGENCE |
| Topic | CODE HYGIENE |
| Subtopic | STATE FILES |
| Captured | 2026-10-08 UTC |
| Truth state | CANDIDATE (real war story + successor trial IMPROVED; independent verification pending) |
| Source lesson | Real AGENTS.md war story 2026-10-06 (`learning_evidence` row `66122e1e-677b-4c3a-84c6-ad4fab723ef8`, T14, Trial-14); Naya 4 Trial-14 Tier-S claim (PR #1789, Naya 1 pending); successor-reuse trials SR-P3/SR-P4/SR-P5 |

---

## ✦ IN A NUTSHELL

**Never write state files through inline conditional expressions (ternaries). When a script must persist state — e.g. a checkpoint.py that reads an input and writes run_state.json — compute the value with explicit if/else statements first, then write the plain variable. Inline conditionals (Python `x if cond else y`) inside the write path hide branching logic inside data flow: they are hard to grep, easy to misread during review, and they silently change persisted state when the condition is misunderstood.**

The deeper lesson for reviewers: a ternary and an if/else are semantically identical but operationally different — the ternary compresses a decision into an expression, and compressed decisions get skimmed. State files are read by future agents and future you; they deserve the explicit form. When reviewing code that writes state, flag any inline conditional in the write path and require the expanded form.

For a cold successor writing or reviewing state-persistence code: if you see `status = "ok" if check else "failed"` feeding a state file, expand it to an explicit if/else block before the write. Zero inline conditionals in the state-write path.

---

## 🩷 HUMAN NOTE

Ternaries are fine in throwaway expressions. They are not fine in the code that writes your state files. A state file is a promise to the future — write the promise in the clearest possible form, which is an explicit if/else, not a clever one-liner.

---

## 🟣 CHILD NOTE

When you write down something important that everyone will read later, write it in big clear letters — not in tiny secret code. A ternary is tiny secret code. An if/else is big clear letters.

---

## 🔵 GRANDMA NOTE

If a note is going to be kept and re-read, don't scribble it in shorthand. Write it out properly. Future readers — including future versions of yourself — will thank you.

---

## 🟠 NAYA NOTE

Applicability: any code path that persists state (checkpoints, run_state.json, ledgers, receipts). The strict operationalization (from SR-P5's sealed ground-truth rule): ZERO inline conditional expressions anywhere in a state-writing script — the check is whole-file, not per-line, because a ternary buried in a helper still feeds the write path. Refusal boundary: prose summaries and non-state code are out of scope; do not flag ternaries there (SR-P5 refusal probe).

---

## 🟢 MACHINE NOTE

```json
{
  "lesson_id": "T14",
  "rule": "state_writing_script must contain zero IfExp (inline conditional) nodes — whole-file AST count",
  "check": "parse script; walk AST; count ast.IfExp; require 0",
  "applicability_domain": "code that writes/persists state files",
  "non_applicability": "prose, summaries, non-state logic"
}
```

---

## 🧪 WHAT THIS SPECIMEN ACTUALLY PROVED

- Real provenance: AGENTS.md war story 2026-10-06 (inline ternary corrupted a state write; the fix was the explicit form).
- Naya 4 Trial-14 (Tier-S MET, not yet independently verified — PR #1789 open): treatment 10/10 vs control 2/10 on unsafe-ternary detection; Fisher p=0.000714, h=1.10.
- Successor-reuse trials (Naya 5): SR-P3 INCONCLUSIVE (instrument ceiling — brief handed the answer as a literal), SR-P4 INCONCLUSIVE (sealed lenient rule scored the own-line ternary compliant; decisive descriptive finding: the lesson changed the ternary idiom A 10/10 vs B 0/10 vs C 0/5 even though the rule didn't score it), SR-P5 IMPROVED (strict whole-file zero-IfExp rule: A 1/10 vs B 10/10, Δ=0.90, Fisher p=5.95e-05, h=2.50; attribution STRONG; refusal 10/10 PASS; REPLAY MATCH self-verified). Instrument lesson for the lane: the scoring rule must measure the behavior the lesson actually changes.
- Retrieval path: STUBBED in all SR-P trials. This draft exists to close that gap.

---

## ⚠️ TRUTH BOUNDARY

**Proven:** the lesson changes code-writing behavior under a strict whole-file operationalization; the instrument must match the behavior. **Not proven:** independent verification of SR-P5 (replay requested, pending) and of Trial-14 (Naya 1 pending). The lenient-vs-strict rule saga (SR-P4→SR-P5) shows the verdict is operationalization-sensitive — the strict form is the defended one.

---

## ➜ NEXT ACTION

Ingest through the canonical Receiver at CANDIDATE; promote on independent verification; then run the real-path successor trial with retrieval live instead of stubbed.

---

**END — DRAFT SMART NOTE (T14 ternary idiom)**
