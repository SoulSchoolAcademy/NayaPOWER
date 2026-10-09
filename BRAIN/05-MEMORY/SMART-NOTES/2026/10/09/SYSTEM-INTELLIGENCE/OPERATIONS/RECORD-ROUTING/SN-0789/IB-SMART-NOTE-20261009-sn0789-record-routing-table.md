# IB-SMART-NOTE-20261009-sn0789-record-routing-table.md

Intelligent Block: SN-0789
Truth state: CANDIDATE (proposed operational routing — not yet ratified as law)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: PDF distillation 2026-10-09, doc 7 (`So__your_job_is_now_to_achieve_it.pdf`), "Record-routing table" section; distilled by PDF reader agents to `~/workspace/design-intake/pdf-distillation-2026-10-09.md`.

## IN A NUTSHELL

Every agent currently guesses where evidence belongs. Doc 7 names the venues: **production evidence → #1593; learning experiments → #1602; truth-state claims → #1603; team coordination → #1354; durable intelligence → BRAIN/05-MEMORY/SMART-NOTES.** No standing file carries this mapping — AGENTS.md has zero hits for these issue numbers. The cost of guessing is real: production evidence posted to a coordination thread gets buried; learning experiments filed as truth-state pollute the canonical record. **Routing is a decision, not a habit.** Until this is law, treat the table as the default and note deviations.

## HUMAN NOTE

Think of it like a hospital. The ER, the pharmacy, the records office, and the staff lounge all exist for a reason — you don't wheel a trauma patient into the lounge because it's closer. Right now our team wheels everything into whatever room is nearest. This note is the building directory: production proof goes to #1593, experiments to #1602, truth claims to #1603, team talk to #1354, lasting intelligence to Smart Notes. Put it in the right room the first time and nobody has to go looking for it later.

## CHILD NOTE

Imagine your school has no labels on any doors. You carry your lunch to the library, your books to the cafeteria, and your gym shoes to the art room — every day, everyone, all mixed up. Then someone tapes a simple sign on each door: lunches here, books there, shoes over there. Suddenly everything is easy to find. That's what this note does: it tapes signs on our doors so every piece of work lands where it belongs.

## GRANDMA NOTE

It's like sorting the mail. Bills in one pile, letters in another, catalogs in a third — not all stuffed in one drawer. We've been stuffing everything in one drawer. This note says: production proof goes here, experiments go there, team discussion goes over there. Simple sorting, and suddenly you can find anything in seconds instead of digging.

## NAYA NOTE

This is the "no duplicate mechanisms" principle applied to venues (AGENTS.md): one canonical place per evidence class. It pairs with the record-routing discipline — before posting, ask "what class is this?" and route accordingly. The five classes are mutually exclusive by design: something is either production evidence, an experiment, a truth claim, coordination, or durable intelligence — never two at once. If you think it's two, you haven't distilled it enough.

## MACHINE NOTE

```yaml
record_routing:
  production_evidence: "issue #1593"
  learning_experiment: "issue #1602"
  truth_state_claim: "issue #1603"
  team_coordination: "issue #1354"
  durable_intelligence: "BRAIN/05-MEMORY/SMART-NOTES/"
rule: classify_before_posting
fallback: "#1354 with explicit class label when uncertain"
```

## LEARNING LESSON

Unrouted evidence is lost evidence. A venue is a contract: the reader of #1593 expects production proof, not brainstorming. Respecting the contract is what makes each venue trustworthy.

## HOW IT CONNECTS

- Extends AGENTS.md "no duplicate mechanisms" to communication venues.
- Pairs with SN-0786 (protocol-path verification): the right path includes the right venue.
- Supports the operating river (MEMORY.md): each river stage has a natural venue — OBSERVE→#1602, VERIFY→#1603, PROMOTE→Smart Notes, production→#1593.

## EPISTEMIC STATE

**CANDIDATE.** Source is a single PDF (doc 7, unratified specialist operationalization). The issue numbers are asserted by that document; independent verification that #1593/#1602/#1603 exist and serve these purposes has not been performed in this task.

**Falsifier:** if #1593, #1602, or #1603 do not exist or serve different purposes, the table's targets are wrong and the note must be corrected, not followed.

## UNCERTAINTY

- Whether these venues are actively monitored by their owning seats.
- Whether "truth-state" (#1603) overlaps with the brain-index or law registry — possible consolidation needed.
- The document's authority: specialist proposal, not director ratification.

## APPLICABILITY

Every seat, every run, before posting anything consequential. Especially: proof artifacts, experiment results, and anything claiming "this is now true."

## SUCCESSOR EFFECT

A cold Naya reading this routes her first proof artifact correctly instead of posting it to #1354 where it drowns in coordination chatter. The venues stay clean because everyone sorts at the door.
