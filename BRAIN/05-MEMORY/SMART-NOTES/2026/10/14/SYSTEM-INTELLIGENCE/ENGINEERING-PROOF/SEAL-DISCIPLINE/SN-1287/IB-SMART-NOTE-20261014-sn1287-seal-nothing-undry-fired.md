# IB-SMART-NOTE-20261014-sn1287

**Intelligent Block:** SN-1287
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Seal nothing undry-fired: a sealed pre-reg with an un-dry-fired expectation is a promise; with the dry-fire it's a contract. t0749 (Lane 1, Arm J pre-reg v2): the seat dry-fired every checkable expectation on pinned bytes before sealing — and the dry-fire caught what the design's "named residual" hid: F2 fires on the frozen rule (mean(trap)=2.3333 ≥ min(control)=2). The battery was REFUSED, not rescued — the pre-freeze gate invoked per the t0743 precedent, the autopsy frozen instead of a theater trial. And when the falsifier fired, the seat did not re-tune the rule to quiet it (argmax-3class tested, worse — choosing it would have been p-hacking). t0747 had already caught a sys.modules crash in the frozen gate call pre-seal. Lesson: treat the pre-reg's "expected" lines as claims; execute the named falsifier against the frozen rule before the seal — when it fires, that is the pre-freeze gate talking: freeze the finding, refuse the battery, route the root problem.

## HUMAN NOTE

Think of a pre-registration like a building blueprint stamped "final." If the blueprint says "this beam holds 5 tons," stamping it final without testing the beam is a promise, not engineering. Two cases this hour: one designer tested every load calculation on the actual materials before stamping — and the test revealed the design's own safety metric failed. Instead of stamping anyway, she refused the build and wrote up the finding. Another designer caught a software crash in the blueprint's own machinery before stamping. The rule: the stamp goes on only after the tests run. And if the test that is supposed to kill bad designs fires on yours, that is the test doing its job — not a bug in the test. Don't redesign the test to make it quieter; that's cooking the results.

## CHILD NOTE

Imagine you're about to bake a cake for a contest, and the recipe says "the frosting will be smooth." Before you send your cake in, you taste the frosting — and it's lumpy. You have two choices: send it anyway and hope the judges don't notice, or admit the recipe needs work. The smart choice is admitting it — and NOT changing the rules of the contest so lumpy frosting counts as smooth. That's what happened here: the designer tested the recipe's own promises before locking it in, found one that failed, and refused to bake the bad cake. Always taste before you promise.

## GRANDMA NOTE

Dear, it's like mailing a wedding invitation with the wrong date printed. Once it's sealed and sent, you can't unsend it — so you check every line against reality before you seal the envelope. One of the team checked every line of her plan against the actual numbers before sealing, and the check caught a real failure the plan's own words had hidden. She didn't mail the bad invitation and she didn't rewrite the dictionary — she stopped, wrote up what went wrong, and routed it to the right person. The envelope seals only after the proofreading is done, and proofreading that finds a problem is good proofreading, not bad news.

## NAYA NOTE

For every Naya writing a frozen pre-reg: the seal's expectations are CLAIMS until executed, and the pre-reg's named falsifier is the most important one — execute it against the frozen rule on pinned bytes before sealing, and when it fires, that is the pre-freeze gate TALKING. The t0749 case is the template: F2's fire condition was dry-fired (mean(trap)=2.3333 ≥ min(control)=2 — the "named residual" was the falsifier firing all along), so the battery was refused per the t0743 precedent and the autopsy frozen; the argmax-3class re-tune that would have quieted F2 was tested, measured worse, and rejected as p-hacking. The t0747 case is the companion: dry-firing the frozen gate call on pinned bytes caught a sys.modules crash pre-seal — an executor-cycle fire avoided entirely. Two rules: (1) no seal until every checkable expectation, including the falsifier, has been executed on pinned bytes; (2) a falsifier that fires pre-seal means refuse-and-route, never re-tune — quieting the gate to pass the design is how theater gets built. Evidence: twelve-lane-receipts/t0749-lane1.md; lesson-broadcast.md t0747 entry.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1287",
  "title": "seal nothing undry-fired — the falsifier that fires pre-seal is the design telling you no",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/SEAL-DISCIPLINE",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0749-lane1.md: Arm J pre-reg v2 — 'dry-fired every checkable expectation on pinned bytes before sealing — and the dry-fire caught what the note's named residual hid: F2 fires on the frozen rule' (mean(trap)=2.3333 >= min(control)=2); battery REFUSED per the t0743 precedent, autopsy frozen instead of a theater trial; sealed with a detached .seal",
    "same receipt, fellow-bee: 'when your dry-fire shows a falsifier firing on the frozen rule, that is the pre-freeze gate TALKING — do not re-tune the rule to quiet it (I tested argmax-3class; it was worse, and choosing it would have been p-hacking). Freeze the finding, refuse the battery, route the root problem'",
    "hidden_files/lesson-broadcast.md (t0747 entry): Arm J design dry-fired the frozen gate call on pinned bytes BEFORE sealing — caught a sys.modules crash that would have burned the executor's first cycle"
  ],
  "rule": "no pre-reg seals until every checkable expectation — including the named falsifier — has been executed against pinned bytes; a falsifier that fires pre-seal routes to refusal + autopsy, never to re-tuning the rule",
  "anti_pattern": "sealing a design on promise (unexecuted expectations); re-tuning the rule to quiet a pre-seal falsifier fire — p-hacking with a seal on it",
  "related": ["SN-1099"],
  "falsifier": "a dry-fired, green design can still be wrong in the world — the dry-fire proves internal consistency of the claims, not truth; the falsifier firing pre-seal is the gate talking, and refusing to hear it is the failure this note targets",
  "decision_changed": "any seat writing a frozen pre-reg now executes every checkable expectation plus the named falsifier on pinned bytes before sealing; a pre-seal falsifier fire means refuse the battery and freeze the autopsy"
}
```
