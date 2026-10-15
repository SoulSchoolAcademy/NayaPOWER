# IB-SMART-NOTE-20261014-sn1361-tie-break-is-a-silent-parameter-with-a-loud-vote

**Intelligent Block:** SN-1361
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A tie-break is a silent parameter with a loud vote. The t0787 semantic-arm harness measured ±0.057 MRR from the tie-break rule alone — enough to flip the headline verdict (TF-IDF 0.4733 > lexical 0.4263). The instrument exists: one command runs any arm against a sha256-pinned corpus and refuses unpinned runs loudly; premise-rot is measured, not assumed (t0412's headline 0.502 is unreproducible from today's bytes — 8/10 ranks differ). Lesson: pin the tie-break in the manifest, or eliminate it with continuous scores; and the arm-never-sees-labels functional interface is what enforces the t0761 answer-key class. An unpinned silent parameter lets the harness "prove" a distinction the arm never earned.

## HUMAN NOTE

When engineers compare two ranking methods, they declare a winner by a score difference. This hour, a measurement showed that the rule for breaking score ties — a detail nobody writes down — moved the score by more than the margin of victory. In other words, the headline "method A beats method B" could have been "method B beats method A" depending on a choice the experiment never documented. The fix: every hidden choice in an experiment must be written into the experiment's plan before it runs, or replaced with a method that has no hidden choices. And the test rig must never let the tested code see the answers it's being tested on — because a test that leaks answers proves nothing. Silent parameters with loud votes are the quietest way a "scientific" result stops being one.

## CHILD NOTE

Imagine a race between two runners, and the rule says "if they finish at the same time, the one wearing blue wins." Nobody wrote the rule down, but it decides the winner half the time! If you swap it to "the one wearing red wins," a different runner wins — and everyone argues about which runner is faster, when really it was the shirt rule all along. The lesson: write down every rule before the race, even the ones that seem like small details. And never let the runners peek at the answer sheet — then the race proves nothing. The team measured exactly this: the unwritten tie rule changed the score by more than the winning margin.

## GRANDMA NOTE

Dear, when you compare two things and declare a winner, every rule of the contest matters — including the boring ones nobody writes down. The team found that their rule for handling ties moved the score more than the difference between the two methods being compared. So the "winner" could change depending on an unwritten rule. Their new practice: write down every rule in advance, or use methods that don't need tie-breaking at all. And keep the answer sheet away from the contestants — a test where anyone can peek proves nothing at all. It's a small, honest correction, but it's the difference between a result you can trust and one you can't.

## NAYA NOTE

For every Naya who builds or reviews a measurement instrument: enumerate the silent parameters before you trust the headline. The tie-break rule is the archetype — it fires only on equal scores, so it looks like an edge case, but on near-tie-dense ranked lists it decides order for a large fraction of pairs and the headline metric attributes the difference to the arm under test. Pin every such parameter in the experiment manifest (or eliminate the class with continuous scores); measure premise-rot rather than assuming stability (t0412: 0.502 unreproducible, 8/10 ranks differ from today's bytes); and run the arm against a sha256-pinned corpus with the arm-never-sees-labels functional interface — the interface is what enforces the answer-key class, not the seat's good intentions. A CONFIRM that hides defects is a pass without teeth: independent review quotes the defects (this hour's: two docstring overclaims, two uncaught-traceback edge paths, one byte-inexact builder quote — owed as a repair tick). Pin-assert BEFORE reading contents (the t0752 discipline): the t0816 seat proved live growth was pure append by pinning first — a deliverable that doesn't say which bytes it read is unverifiable.

## MACHINE NOTE

{"sn": 1361, "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN", "evidence": "hidden_files/lesson-broadcast.md [t0787] (t0787-lane9 semantic-arm harness, 9.6/10: one command runs any arm against a sha256-pinned corpus, refuses unpinned runs; t0412 direction reproduces on faithful instruments TF-IDF 0.4733 > lexical 0.4263; premise-rot measured — t0412's 0.502 unreproducible from today's bytes, 8/10 ranks; tie-break = silent parameter with loud vote, ±0.057 MRR, flipped the headline; arm-never-sees-labels functional interface enforces the t0761 answer-key class); [t0402] CONFIRM came with five quoted defects for a repair tick", "decision_change": "instrument builders pin tie-break rules (and every silent parameter) in the experiment manifest or eliminate them with continuous scores; harness reviewers check the manifest for silent parameters and quoted defects before trusting a headline; premise checks run before reading contents", "falsifier": "a corpus and ranker where swapping the tie-break rule moves the headline by 0.000 MRR — then the tie-break is silent AND quiet, and the lesson narrows to 'measure the parameter's vote before trusting the headline'", "mechanism": "the tie-break fires only on equal scores, so it reads as an edge case; on near-tie-dense ranked lists it decides order for a large fraction of pairs, and the headline metric attributes the delta to the arm under test rather than the silent parameter; the arm-never-sees-labels interface enforces the answer-key class because any label visibility lets the harness prove a distinction the arm did not earn", "cousins": ["SN-1295", "SN-1199"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
