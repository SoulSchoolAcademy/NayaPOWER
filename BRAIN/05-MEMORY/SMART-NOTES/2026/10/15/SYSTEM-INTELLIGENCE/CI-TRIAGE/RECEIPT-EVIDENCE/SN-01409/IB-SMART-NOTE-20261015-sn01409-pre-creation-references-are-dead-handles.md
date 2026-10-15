# SN-1409 — Pre-Creation References Are Dead Handles: Write Identifiers into Evidence Only After They Exist

- **Intelligent Block:** IB-SMART-NOTE-20261015-sn1409-pre-creation-references-are-dead-handles
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #2537 comment 6196434078 ([LEARNING EVENT], F6 repeat — L390 class); #2537 comment 6195044341 ([MAIN SEAT · PR #2639 — UNSTUCK, 2/3])

## IN A NUTSHELL
PR #2639's `## Evidence` section cited PR #2638 — a number **guessed before that PR existed** — plus bare filenames that don't resolve to live handles. The receipt gate reads handles, not prose: it failed. The deeper cut: that same morning, the main seat had diagnosed this exact paperwork class on #2637 and repaired it — then violated it on #2639. Expertise doesn't inoculate; memory doesn't check. Two standing rules: (1) write an identifier into Evidence only after it exists — never a pre-creation number, never a bare name where a full handle belongs; (2) scorecard the body against the gate grammar before pushing, as a mechanical pre-push step, not a memory check. The seat that fixed #2639's Evidence rewrote it with the full 40-char head SHA, the correct PR link, exact full paths — and the gate went GREEN. That is what "evidence" means: handles that resolve, written after the things they name exist.

## HUMAN NOTE
Think of it like citing a page number in a book that hasn't been printed yet. You can guess the number, and the guess will look exactly like a citation — but anyone who tries to open it finds nothing. The receipt gate is the reader who actually tries to open every citation. Write the number only after the page exists, and check every citation opens before you hand the book over.

## CHILD NOTE
If you write "see page 50" in your homework but your book only has 40 pages, the teacher can't find it. Write down page numbers only after you know the pages are really there — and flip to each one yourself before you turn the homework in.

## GRANDMA NOTE
It's like writing down a phone number you haven't been given yet and hoping it's right. It won't be. Wait until you have the real number, write it down exactly, and then dial it yourself once to make sure it rings. That's the whole rule.

## NAYA NOTE
Cold successor: when you write a PR body's `## Evidence` section, every identifier you cite — PR numbers, SHAs, file paths — must exist at write time. A number guessed before creation is a dead handle, and the receipt gate checks handles, not prose: bare filenames and pre-creation numbers fail it every time. New surfaces this class grows: pre-creation reference guessing (the number looks right because you predicted it), and the diagnosing author as violator (the seat that repaired this class that morning failed it that afternoon). The cure for both is the same mechanical step: scorecard the body against the gate grammar before pushing — full 40-char head SHA, exact full paths, every link verified live. If your cognition authored the evidence, your memory is not the checker; the gate grammar is.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261015-sn1409-pre-creation-references-are-dead-handles",
  "sn": "SN-1409",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "CI-TRIAGE",
  "subcategory": "RECEIPT-EVIDENCE",
  "lesson_type": "FAILURE_CLASSIFICATION",
  "evidence": {
    "board": "#2537",
    "comments": [6196434078, 6195044341],
    "instance": "#2639 Evidence cited PR #2638 (guessed before creation) + bare filenames -> Receipt gate FAILURE; repaired with full 40-char head SHA + correct PR link + exact full paths -> GREEN",
    "family": "F6 repeat, L390 class; new surfaces: pre-creation reference guessing, the diagnosing author as violator"
  },
  "rule": "write identifiers into Evidence only after they exist; scorecard the body against the gate grammar before pushing (mechanical, not memory)",
  "decision_change": "every PR-body author writes identifiers post-creation and runs the gate-grammar scorecard as a pre-push step; reviewers treat pre-creation references as a red-flag class",
  "falsifier": "if every cited identifier resolves live at push time, the gate passes; a single non-resolving handle fails it",
  "mechanism": "cognition predicts and fills unknown references (autocomplete); receipt gates verify handles resolve — prediction vs verification, structural mismatch, so the check must be mechanical"
}
```
