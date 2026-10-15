# Intelligent Block: done/ is a closure claim — never file an open-verdict brief there

Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A filing destination is itself a verdict. Moving a brief to done/ claims its work is closed — so a brief whose verdict is still unissued must never land there, no matter how complete its receipt looks. The queue-mover must read the receipt's verdict, not just notice that a receipt exists.

## HUMAN NOTE
A brief was filed into the "done" folder while its key decision was still open — the decline receipt attached to it explicitly said declined briefs stay in the queue. Nobody questioned the paperwork; they just saw a receipt and filed it. The queue silently lost a live brief until the dispatcher re-filed it. The lesson: "done" is a claim, not a folder. Before filing, read what the receipt actually decided.

## CHILD NOTE
Putting a homework folder into the "finished" box doesn't mean the homework is done — especially if the note inside says "not done yet, keep working." Always read the note before you put the folder away.

## GRANDMA NOTE
Dear, the "finished" drawer is a promise, not just a drawer. If the letter inside says "not finished," it doesn't belong there — no matter how tidy the envelope looks. Read the letter first.

## NAYA NOTE
This is the t0407 queue-integrity incident (2026-10-15 04:09 UTC): brief-gap-t0776-lane9.md was moved queue→done/ while its ⛔-stamped decline receipt explicitly said declined briefs stay in the queue and its CONFIRM/REWORK verdict on PR #2591 was still unissued. "done/ without the verdict is the queue silently losing a brief." The mover keyed on receipt-existence, not on the receipt's verdict. The dispatcher re-filed it. Distinct from SN-1359 (decline receipt is not closure — the executor-side receipt semantics): this is the mover-side rule — the directory is a state claim, and filing an open-verdict brief there deletes claimability silently. Queue-movers read the verdict field before filing to done/; decline receipts keep their brief in the queue until the named verdict is issued or the brief is explicitly routed out.

## MACHINE NOTE
```json
{
  "sn": "SN-1415",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": {
    "name": "done_is_a_closure_claim",
    "statement": "done/ is a state claim of closure, not a destination for receipts. A brief with an unissued verdict must never land there: the queue-mover reads the receipt's verdict field before filing; a decline receipt keeps its brief claimable (in queue) until the named verdict is issued or the brief is explicitly routed out.",
    "falsifier": "An audit of done/ finds a brief with an open verdict that was later shown completed with no silent claimability loss — then the move was harmless in that case (the mechanism still holds: the claimability window was deleted, only the loss didn't materialize).",
    "mechanism": "The file-state machine conflates receipt-existence with work-completion: the mover files on 'has receipt' instead of 'verdict == CLOSED'. The directory transition itself is the closure claim — filing an open-verdict brief there removes it from the claimable population with zero signal.",
    "adoption_requirements": [
      "queue-mover reads the receipt's verdict before any queue→done/ move",
      "decline receipts are never terminal: brief stays in queue for an eligible seat, or is explicitly routed out with the re-dispatch named",
      "re-file of a wrongly-closed brief is logged with the reason (the t0407 re-file pattern)"
    ],
    "decision_changed": "Future dispatcher/queue-mover decisions: a receipt's presence never authorizes done/ — only the receipt's verdict does. Declined briefs are re-filed or routed-out, never quietly closed."
  },
  "evidence": [
    "lesson-broadcast.md [t0407] (queue-integrity: brief-gap-t0776-lane9.md moved queue→done/ at 04:09 UTC with its ⛔-stamped decline receipt explicitly saying declined briefs stay in the queue and its CONFIRM/REWORK verdict still unissued — dispatcher re-filed to the queue)",
    "hidden_files/twelve-lane-receipts/gap-t0776-lane9-decline2-rootcause.md (decline #2: the brief's own escape hatch used — empty eligibility pool proven; routed OUT with re-dispatch named, not buried)"
  ],
  "related": ["SN-1359"],
  "status": "CANDIDATE — not ratified; only Shawn ratifies"
}
```
