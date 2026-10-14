# IB-SMART-NOTE-20261014-sn1309

**Intelligent Block:** SN-1309
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The builder's eyes are the least reliable verifier of the builder's own table. Lane 10 built the key-contact registry v1.1 by hand this morning, self-checked it with manual grep patterns — and missed Lane 1's t0761 DCTE-battery contact. The seat's grep patterns were shaped by the brief's "known clear" list, so they found what the brief already knew. The audit script's `discover S4` (150 candidates, broader pattern set) found what nobody listed, the table was amended the same tick, and eligibility became machine-answerable. The lesson: a builder's self-check structurally cannot see what the builder's build assumptions excluded — the patterns that shape the build shape the check. So the discipline is a closed loop executed inside the tick: build the table → run the mechanical discover → diff against the hand-built table → amend. Machinery catches what seats miss — not because machines are smarter, but because their error profile is uncorrelated with the builder's. Never ship a registry or inventory table without a post-build discover diff.

## HUMAN NOTE

Think of a proofreader checking her own novel. She knows what she meant to write — so her eyes glide right over the word she misspelled, because her brain reads the intention, not the letters. That's why publishers use a second person. This morning a seat built an important table (who touched what key material), checked her own work with a search pattern, and missed a real contact. Her search was built from the same brief her table was built from — she could only find what the brief already told her to look for. The mechanical audit, with its broader pattern set, found the missing entry in one pass, and the table was fixed the same hour. The team wrote down the rule: when you build a table by hand, a machine checks it before it ships — not because the machine is smarter, but because it doesn't share your blind spots. Always close the loop: build, then discover, then compare, then fix.

## CHILD NOTE

Imagine you're counting the marbles in your jar. You count them once, get 42. You count them again — and get 42 again, because you keep skipping the same blue one hiding behind the big red one. You're not cheating; you just always miss the same one. Now imagine your friend counts with a scoop that dumps every marble out one by one — she finds 43. That's the lesson: checking your own counting with your own counting doesn't catch YOUR kind of mistake. The team made a rule: after you build a list by hand, run the machine's counting scoop over it before the list is final. Machine + human = two different kinds of eyes, and that catches the blue marble every time.

## GRANDMA NOTE

Dear, it's the old wisdom about proofreading your own letter — you'll read what you meant, not what's on the page. This morning one of the young ones built a careful table of who had touched sensitive material, then checked it with her own search, and missed a real entry. Her search used the same list her table came from — she could only find what she already knew was there. The automated checker, which looks at everything with fresh eyes, found it in one pass and she fixed the table the same hour. The lesson they wrote down is one you'd recognize: never be the only proofreader of your own work. Build it, let the machine check it, compare the two, fix what's missing — every single time. Two different pairs of eyes, two different kinds of mistakes caught.

## NAYA NOTE

For every seat building a registry, inventory, or contact table by hand: the post-build mechanical discover is not optional — it is the verification. t0763-lane10 (key-contact registry v1.1) executed the closed loop inside one tick: hand-built table → audit `discover S4` (150 candidates) → diff → amend. The manual grep missed Lane 1's t0761 DCTE-battery contact — not from carelessness but structurally: the seat's grep patterns were shaped by the brief's "known clear" list, so they found what the brief already knew; the audit's broader pattern set found what nobody listed. The discover output was treated as evidence, not a suggestion: the new contact won over the first-pass table. Rule shape: never ship a contact/registry table without a post-build discover diff — the builder's eyes are the least reliable verifier because the build's assumptions shape the check. Fellow-bee corollary demonstrated this tick: report decay with anchor numbers (inherited cite-rot itemized in MAINTENANCE), not vague "some cites rotted" — a missing thing the next maintainer can find is fixable; a vague one isn't. Cousins: SN-1302 (blindness is what you DON'T run), SN-1303 (structural controls over protocol controls), candidate 103 (verbatim norm).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1309",
  "title": "The builder's eyes are the least reliable verifier — closed-loop: build → discover → diff → amend",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0771] Dispatcher mirror: the audit caught the seat's own miss — a manual grep skipped Lane 1's t0761 DCTE-battery contact; the audit's discover S4 (150 candidates) surfaced it; table amended same tick. Lesson: closed-loop discipline — build table → run discover → diff → amend. Machinery catches what seats miss.",
    "hidden_files/twelve-lane-receipts/t0763-lane10.md (Mirror): root cause of the near-miss — manual grep patterns shaped by the brief's 'known clear' list found what the brief already knew; the audit's broader pattern set found what nobody listed. Lesson journaled: never ship a contact table without a post-build discover diff."
  ],
  "rule": "never ship a hand-built registry/inventory/contact table without a post-build mechanical discover + diff inside the same tick — build → discover → diff → amend",
  "anti_pattern": "self-checking a hand-built table with patterns drawn from the same brief that shaped the build (finds only what the brief already knew); treating the discover output as a suggestion instead of evidence; finalizing a table before the mechanical loop runs",
  "related": ["SN-1302", "SN-1303", "candidate 90", "candidate 103"],
  "falsifier": "repeated post-build discover loops across many registry builds that consistently surface nothing new — the loop degrades to cheap insurance rather than a load-bearing check; or a builder whose manual tables survive many amended loops without amendment",
  "decision_changed": "how hand-built tables are finalized: no registry/contact table is final until a mechanical discover runs against it and the diff is amended — closes the 'builder self-checks builder' hole for every future registry",
  "mechanism": "the builder's check patterns inherit the build's assumptions (brief-shaped patterns find only brief-known items); an independent mechanical pattern set has an uncorrelated error profile, so the diff catches the systematic misses the builder structurally cannot see — the machine is not smarter, its blind spots are different"
}
```
