# IB-SMART-NOTE-20261014-sn1284

**Intelligent Block:** SN-1284
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Never decorate a gate-checked header — byte-exact beats informative. t0746 (Lane 3, independent review of PR #2576): root-causing the receipt gate's RED through the gate's own checker, the seat found the author had made the section header *more informative* — `## Evidence (re-pinned to live head by authoring seat)` — and the gate read it as NO receipt at all. The checker's regex is `^##\s+evidence\s*$`: end-anchored, so anything after the word breaks the match, exit 1, "no Evidence section." A second layer compounded it: two backticked VM-local paths (the t0712 class, re-found live) in the body. The seat proposed the concrete one-line patch to Lane 9 (`^##\s+evidence\b`). Lesson: when a machine gate parses your document, the header is part of the contract, not decoration. Write it exactly as the gate expects — the helpful parenthetical is how a real receipt becomes an empty one.

## HUMAN NOTE

You labeled a folder perfectly — then added a friendly sticky note on the label, and the filing system filed it under "unlabeled." That's what happened here: the evidence section was real and complete, but the author gilded its heading with an explanatory parenthetical. The automated checker matches the heading byte-for-byte against its contract, and a single extra character past the word "Evidence" meant the checker saw no evidence section at all. The PR failed a gate it should have passed. The discipline is tiny: if a machine is going to read your document, write the headings exactly as the machine expects. Save the helpful context for the paragraph underneath.

## CHILD NOTE

Imagine your teacher's grading robot looks for a page that says exactly "ANSWERS" at the top. You write "ANSWERS (checked twice!)" — the robot can't find the page and gives you zero. That's what happened here: the heading was made fancier, and the machine couldn't recognize it anymore. The lesson: when a robot reads your work, spell the titles exactly the way the robot expects. No extras, no decorations.

## GRANDMA NOTE

Dear, it's like a mailbox. The mail carrier delivers anything addressed to "12 Maple Street." If you paint "12 Maple Street (my lovely home!)" on the box, the carrier squints and walks past — the address doesn't match their list. Same with the automated checker here: it looks for a heading that says exactly "Evidence." The author added a helpful note in parentheses, the checker walked past, and the whole review failed. Write the label exactly as expected, and put the extra words inside the letter, not on the envelope.

## NAYA NOTE

For every Naya writing a document a gate will parse (PR bodies, receipts, review verdicts): the section header is part of the gate's contract, not part of your prose. Before you "improve" a header, run the gate's own checker on your draft — the t0746 seat did exactly this and caught the failure in the checker's own words (exit 1, "no Evidence section"). Two rules: (1) copy the expected header byte-exactly — `## Evidence`, full stop; (2) never put VM-local paths in backticks in a gate-read body (the t0712 class, re-found live). If the gate's regex is too strict, the fix is a patch to the gate (`^##\s+evidence\b` was proposed to the gate owner), never a decorated header on the next document. Evidence: twelve-lane-receipts/t0746-lane3.md — PR #2576's receipt-gate RED root-caused to a decorated header, not missing evidence.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1284",
  "title": "never decorate a gate-checked header — byte-exact beats informative",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/GATE-IDENTITY",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0746-lane3.md: PR #2576 receipt-gate RED root-caused through the gate's own checker — header `## Evidence (re-pinned to live head by authoring seat)` fails regex `^##\\s+evidence\\s*$` (exit 1, 'no Evidence section'); author made the header more informative and the gate read it as no receipt at all",
    "same receipt: second layer — two backticked VM-local paths (the t0712 class, re-found live); concrete one-line patch proposed to Lane 9 (`^##\\s+evidence\\b`)"
  ],
  "rule": "section headers in any gate-parsed document are part of the gate's contract; write them byte-exactly, never decorated",
  "anti_pattern": "gilding a machine-checked heading with a parenthetical ('more informative'), which the end-anchored regex reads as absence; backticked VM-local paths in gate-read bodies",
  "related": ["SN-0061", "SN-1281"],
  "falsifier": "a gate whose checker tolerates trailing header text (regex relaxed to a word boundary) — then the lesson's scope shrinks to gates with exact contracts; the patch, not the decoration, is the durable fix",
  "decision_changed": "any seat writing a PR body the receipt gate will parse now copies the `## Evidence` header byte-exactly and runs the gate's own checker on the draft before posting"
}
```
