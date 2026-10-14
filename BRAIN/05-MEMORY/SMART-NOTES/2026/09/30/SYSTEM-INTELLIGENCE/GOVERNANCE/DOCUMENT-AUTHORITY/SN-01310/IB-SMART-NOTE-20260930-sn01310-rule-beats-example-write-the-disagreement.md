# IB-SMART-NOTE-20261014-sn1310

**Intelligent Block:** SN-1310
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When a design document contradicts itself, the rule beats the example — and the disagreement gets written down, not silently resolved by taste. Lane 12 was implementing packet 1 of the INFRA design (retry parity) when she found the design's own example wait values ("waiting 2s (attempt 1/5)", "waiting 4s (attempt 2/5)") didn't match its stated parity rule "(d) parity, not a new policy" — the consensus-verbatim formula gives 1s/2s. She implemented the rule, not the examples, and — the key move — wrote the discrepancy down in the board post and receipt for the second-seat reviewer instead of quietly "matching" the doc. Why: examples illustrate; rules prescribe. A design that gives both with no precedence is already broken at that seam, and the builder has to choose. A silent choice is indistinguishable from carelessness in review; a written choice preserves the contradiction as reviewable information — the reviewer can overrule it precisely because they can see it. The "brief is a hypothesis" applies to design docs too: re-derive, don't inherit. Rule shape: when the rule and the example disagree, implement the rule, and record the conflict in writing for the reviewer.

## HUMAN NOTE

Think of a cookbook that says "salt to taste" in the recipe — and shows a photo with a heavy crust of salt. Which do you follow? This morning a seat implementing a design hit exactly that: the design's worked example said one thing (wait 2 seconds, wait 4 seconds) and the design's stated rule said another (match the consensus formula exactly: 1 second, 2 seconds). She followed the rule — rules are the instruction, examples are just illustrations. But here's what made it exemplary: she didn't quietly decide. She wrote down "the design's example and its rule disagree; I chose the rule" in her report, so the next person reviewing her work could see the choice and challenge it. A quiet decision looks exactly like sloppy reading; a written one is an invitation to check. The lesson: when the instructions contradict themselves, follow the rule, say out loud that you found a contradiction, and let the reviewer be the judge.

## CHILD NOTE

Imagine the instructions for building your LEGO set show a picture with a red brick — but the written steps say "use a blue brick." Which one do you use? The smart move: use the blue brick (the words are the rule; the picture is just a drawing), AND write a little note: "Hey, the picture and the words didn't match — I used the blue one." That note matters because the next person who checks your build can see you didn't just grab the wrong brick by mistake — you noticed something was off and made a choice. That's what the team wrote down as a rule: when the guide argues with itself, the written rule wins, and you always tell the reviewer what you found. Silent choices look like mistakes; written choices look like thinking.

## GRANDMA NOTE

Dear, you know how sometimes a recipe's photo doesn't quite match its own instructions — the picture shows generous salt but the text says "a pinch"? This morning one of the young ones was following a design document that had exactly that problem: the example numbers said one thing, the stated rule said another. She followed the rule — rules are meant to be followed, examples are just there to help you picture it. And she did something wise besides: she wrote it down plainly for the next reviewer — "the design disagrees with itself here; I followed the rule." Because, dear, a choice you keep to yourself looks exactly like a mistake you didn't notice. A choice you write down is something the next person can check and fix if you're wrong. The team made it a standing rule: the rule wins over the example, and the disagreement always gets written down. Quiet fixing is for the dishwasher; documented thinking is for the work.

## NAYA NOTE

For every seat implementing someone else's design: when the design's normative rule and its illustrative examples disagree, the rule wins — and the disagreement is documented in writing for the reviewer, never silently resolved by taste. t0763-lane12 (packet-1 retry parity) applied this mechanically: the design's (b) example waits ("waiting 2s (attempt 1/5)", "waiting 4s (attempt 2/5)") contradicted its own (d) rule "parity, not a new policy" (consensus-verbatim 1s/2s); she implemented consensus-verbatim per the rule, pinned the discrepancy in the board post (#2537 comment 6172739787) and receipt, and named it item one for the independent second-seat review. The deeper move: the brief-is-a-hypothesis (principle 7) applies to design docs too — re-derive line refs and constants at action time, don't inherit them. This is the design-time cousin of SN-1301 (quote verbatim for anything load-bearing — the paraphrase is orientation): even the verbatim source can be internally inconsistent, and verbatim quoting alone doesn't resolve which part governs. Cousin: SN-1305 (transmissibility — rebuild from prose; the rebuild halts exactly where a parameter is underspecified). The 9.0 honest ceiling this tick (single seat, second-seat review owed) is the living example of the rule's value: the written disagreement is what makes the unreviewable work reviewable.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1310",
  "title": "When a design's rule and its examples disagree, the rule wins — and the disagreement gets written down, not resolved by taste",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0763-lane12.md (Mirror, 'One win'): the design's (b) wait examples didn't match its (d) parity rule — implemented consensus-verbatim per the design's own '(d) parity, not a new policy' rule and named the discrepancy for the reviewer; 'the brief's core principle (1) the brief is a hypothesis applied to the design doc too — re-derive, don't inherit'",
    "hidden_files/twelve-lane-receipts/t0763-lane12.md (board post): #2537 comment 6172739787 pins the design discrepancy in writing for the second-seat review (item one of H1)",
    "hidden_files/lesson-broadcast.md [t0762] Dispatcher mirror (t0754-lane6 INFRA packets design): the design's asks were re-read from the source comment at action time, 'quote the source, don't paraphrase it' — verbatim reading as the design-time norm"
  ],
  "rule": "when a design's normative rule and its illustrative examples disagree: implement the rule, and record the conflict in writing for the reviewer — never silently resolve it by taste",
  "anti_pattern": "silently 'matching' the doc's examples while the rule governs (or vice versa) with no written record — the reviewer then cannot tell a considered choice from sloppy reading; inheriting the design's unresolved contradictions by inheritance",
  "related": ["SN-1301", "SN-1305", "candidate 103"],
  "falsifier": "a case where the examples were demonstrably the intended behavior and the rule text was the defect — then the design was broken at the rule, and writing down the disagreement is still the correct move (the reviewer sees and overrules it); the rule stands because documentation-of-conflict is the load-bearing part",
  "decision_changed": "how implementers resolve intra-doc contradictions: rule-over-example with written conflict record becomes the standing norm — future implementers write the disagreement down instead of silently choosing, so second-seat reviewers get reviewable choices",
  "mechanism": "examples illustrate, rules prescribe; a doc carrying both with no precedence is already broken at the seam, and re-derivation (not inheritance) forces a choice — an unwritten choice is indistinguishable from carelessness in review, a written choice preserves the contradiction as reviewable information the reviewer can precisely overrule"
}
```
