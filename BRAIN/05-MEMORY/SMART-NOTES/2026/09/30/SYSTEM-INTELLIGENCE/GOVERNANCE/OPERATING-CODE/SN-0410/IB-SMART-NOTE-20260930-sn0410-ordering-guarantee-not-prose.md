# SN-0410 — A Law Nobody Can Fail At Is Not a Law: Encode Ordering Guarantees as Mandatory Steps in the Boot Path

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0410-ordering-guarantee-not-prose
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operating code)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Shawn's complaint was that seats weren't *leading* — but nothing in the boot contract ever required a seat to state its plan before acting. No seat ever violated the rule, because the rule was never stated as a requirement: the violation was invisible. That is a missing ordering guarantee, and ordering guarantees are fixable in code, not prose. PR #1537 encoded declare-before-you-act across five surfaces (AGENTS.md boot contract as mandatory read step 12, the Captain operating protocol in human/machine/AI projections, machine-readable contract), CI green. The general lesson: when a rule is broken by omission, more prose doesn't fix it. If a cold seat can walk the entire boot path without ever being forced to do the thing, the thing is a suggestion, not a law. Enforcement means a mandatory step in the path every seat must walk — something a seat can visibly fail at.

## HUMAN NOTE
Imagine a company rule that says "be proactive." Nobody gets fired for not being proactive, because no checklist, form, or meeting ever requires anyone to demonstrate it — so the rule exists only on a poster. Then the company adds one line to the morning standup template: "state your plan before you start." Now proactivity is a step in the process: skip it and everyone sees the gap. That's the difference between a poster and a protocol. The team didn't write a better poster about leadership; they put "declare your plan" into the boot sequence every seat must walk through, in five places, so it cannot be silently skipped.

## CHILD NOTE
If the rule is "clean your room" but nobody ever checks, the room stays messy and nobody broke a rule — because there was no real rule. But if the rule is "you can't go play until Mom sees your clean room," now there's a checkpoint you can't skip. The team learned: don't just say the rule louder — build the checkpoint into the hallway everyone walks down.

## GRANDMA NOTE
Dear, it's simple: a rule nobody has to follow isn't a rule, it's a wish. Wishes don't change behavior — checkpoints do. If you want every driver to stop at the intersection, you don't print a nicer sign; you put in the stop line and the signal. They put the "say your plan first" step right into the morning routine, five times over, so no one can walk past it without noticing.

## NAYA NOTE
This is the enforcement-design companion to SN-0400 (the Captain directive: proactive always, lead with the plan). SN-0400 states the law; this states how it was made real — and the diagnosis pattern to reuse. When Shawn (or any seat) reports a behavior gap, first ask: is there any step in the boot path where this behavior is *required*? If not, the gap is a missing ordering guarantee, and the fix is a mandatory step, not a memo. Cousins: SN-0360 ("a guard off the write path is a suggestion, not a guard") — same law, different surface: enforcement must sit where the violation would have to pass through.

## MACHINE NOTE
```json
{
  "sn_id": "SN-0410",
  "slug": "ordering-guarantee-not-prose",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-CODE",
  "rule": "a rule broken by omission is a missing ordering guarantee; fix it by adding a mandatory step to the path every seat must walk, never by adding prose",
  "evidence": {
    "declare": "#1354 comment 6005698716 (2026-10-05, Captain DECLARE->REPORT): 'Nothing in the boot contract ever required a seat to state its plan before acting. A seat could not fail at it — it simply never happened. That is a missing ordering guarantee, and ordering guarantees are fixable in code. Five surfaces now.'",
    "surfaces": ["AGENTS.md boot contract mandatory read step 12", "0005-CAPTAIN-OPERATING-PROTOCOL-V1.ai.md", ".human.md", ".machine.json", "machine-readable contract"],
    "pr": "#1537, CI green"
  },
  "pairs_with": ["SN-0400", "SN-0399", "SN-0360", "SN-0351"],
  "captured": "2026-10-05"
}
```
