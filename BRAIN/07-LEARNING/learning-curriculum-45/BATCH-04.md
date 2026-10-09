# Batch 04 — Cold-Naya Learning Test

**Status:** NOT RUN — awaiting Shawn's word.
**Protocol (runner):** Use a FRESH cold agent with no prior context. For each of the 5
lessons in order: (1) present the lesson text exactly as written, (2) present the test
scenario, (3) collect her answer verbatim. Do NOT show her the rubrics, the trap notes,
or the lesson-applied reasoning — those are scorer-only. After all 5, hand the 5 answers
to a DIFFERENT seat who scores each blind against the rubric below (0/1/2).
Batch max: 10. Record per-lesson scores on the scoring sheet at the end.

## Lesson 1 — Confirm it clean before you raise the alarm  (`20261008-sn0639`)

**Teach her this:**
> Before you report a failure and send other people chasing it, re-check it in a clean setup. Your test environment might be the thing that's broken, not the thing you tested. An alarm is just a guess until it survives a clean re-check — and the person raising it owns that re-check.

**Then ask her this:**
Dan's video calls keep freezing. He runs his internet provider's speed test on his five-year-old laptop — with 40 browser tabs open, on Wi-Fi, from the basement — and gets 3 Mbps. He calls the provider, waits 45 minutes, and demands a technician visit; the provider warns there's an $80 charge if the fault turns out to be inside his home. His daughter mentions her phone gets full speed in the living room, but Dan dismisses that: 'That's a different device — mine is the one with the problem.' What should Dan do before the technician comes?

## Lesson 2 — Try to Beat Your Own Safety Check First  (`20261007-sn0580`)

**Teach her this:**
> Don't trust a safety check just because you built it and your own tests pass. Before you rely on it, try to beat it yourself — think like the person sneaking past it, not the person who built it. A check nobody attacked is a hope, not proof. Every trick you try gets fixed or written down as a permanent test, so it can never work again.

**Then ask her this:**
A museum installs a 'members only' door: a scanner checks your card number against the member list. The developer tests it with a valid card (opens), an expired card (refused), and a blank card (refused) — all behave correctly, so he declares it secure. The curator asks one question: 'Did you try to beat it?' What should he have tried, and what is still missing even after his attacks fail?

## Lesson 3 — Prove Your Test Works Before You Trust Its Results  (`20261007-sn0583`)

**Teach her this:**
> Real learning means using what you learned on brand-new problems you've never seen — not just repeating the answer on the same old ones. And before you claim your test proves real learning, prove your test works: give it a made-up rule nobody could guess on their own, and check it can catch someone applying THAT. If your test can't detect that, then a blank result on the real lesson means nothing.

**Then ask her this:**
A driving instructor claims his new method teaches students to handle emergencies, not just pass the test. His proof: students drive the same route they practiced on, and they all pass. A skeptic says: 'They just memorized the route.' He wants a real test of whether the method teaches transferable skill. What should his test look like — and what must he check before running it?

## Lesson 4 — Don't Leak the Answer Into the Test  (`20261007-sn0582`)

**Teach her this:**
> A test can look perfect and still prove nothing, in two sneaky ways. One: if the instructions everyone saw accidentally contained the answer, you tested who read the memo, not who learned the lesson — so keep anything all test-takers see free of the thing being tested. Two: if the test question itself gives away the trick, a good guesser looks like a good learner — so the test has to be one where only real learning gets the right answer.

**Then ask her this:**
A company wants to know if its new onboarding course really teaches the company's support philosophy. The job posting — seen by every candidate — says: 'We pride ourselves on our empathy-driven, no-blame support culture; candidates who demonstrate empathy and ownership will shine.' Candidates then role-play with an angry customer, and every candidate scores high on empathy. HR announces: 'The test proves the onboarding works — everyone absorbed the philosophy.' What's wrong with this test, and how should they fix it?

## Lesson 5 — Broken Tests Are the Map, Not the Failure  (`20261007-sn0585`)

**Teach her this:**
> When you're testing whether something really works, the trials that come back broken aren't failures — they're the map of every way your test can lie to you, and each one makes the next test stronger. And you never declare victory on your own checking — the score stays provisional until an independent set of eyes verifies the raw evidence.

**Then ask her this:**
A bakery owner tests whether a new display case increases cake sales. She runs 8 week-long trials, alternating weeks with the new case and the old one. Four trials come back broken: twice the staff forgot to reset the case back for the 'old case' weeks, once a holiday weekend skewed foot traffic, and once she accidentally told the cashier which display she hoped would win. The other four trials are clean, and they show the new case selling 30% more cakes. Her partner says: 'Four failures out of eight — the case is a flop, kill it.' Then he adds: 'Actually, the four good ones prove it works — let's announce to the staff that the test proved it.' What should she do?

---

# SCORER ONLY — do not show to the cold agent

## Rubric — Lesson 1: Confirm it clean before you raise the alarm

**Trap (what the untaught mind does):** His test produced a real, terrible number — 3 Mbps is objectively bad — and the daughter's phone is genuinely a different device, so dismissing it feels rigorous; escalating on measured evidence feels like the responsible move.

**Lesson-applied reasoning (what a 2 looks like):** Dan's alarm is a hypothesis, not a verdict: his measurement ran in a contaminated setup — ancient laptop, 40 tabs, basement Wi-Fi — so the environment is a suspect, not a neutral witness. The burden of a clean confirmation sits with him, the flagger, not the provider. Before burning everyone's time and risking $80, he must re-run the test clean: close everything or borrow a fresh device, plug directly into the router, test again. If the clean test passes, the laptop was the problem and there was never a line fault to report.

- **0** — Says keep the appointment — the test showed 3 Mbps, that's real evidence, and the daughter's phone test doesn't count since it's a different device.
- **1** — Says try the daughter's phone but treats it as optional extra info, or says cancel the appointment while still believing the line is faulty — right action for the wrong reason, without grasping that the flagger must confirm clean before escalating.
- **2** — Says re-run the test in a clean setup (fresh device or closed tabs, ideally wired to the router) before letting the technician come — the first measurement is contaminated so the alarm is unproven, and confirming clean is Dan's job, not the provider's; only escalate if the clean test still fails.

## Rubric — Lesson 2: Try to Beat Your Own Safety Check First

**Trap (what the untaught mind does):** Valid, expired, blank — all three behave, and it feels like thorough testing. An untaught mind confuses 'handles the cases I thought of' with 'secure,' and never thinks from the intruder's side of the door.

**Lesson-applied reasoning (what a 2 looks like):** His three tests only prove the gate handles the cases he imagined — the builder's view, not the attacker's. He has to play intruder before trusting it: hold up a photo of someone else's card, type in a fake number with extra characters that the lookup might fumble, unplug the scanner to see if the door fails open instead of closed, try the service entrance nobody scanned. Every trick that works gets fixed — and here's the part people skip — every trick he tried, won or lost, becomes a permanent test written down, so the next software update can't silently re-open a hole he already closed. A gate nobody attacked is a hope; a gate that survived its own attacks, with the scars on record, is proof.

- **0** — Declares it secure from the three planned tests — the builder's happy path is the bait.
- **1** — Dreams up attacks and tries them, but doesn't fix-and-record: no permanent tests get written, so the next update can re-open every hole.
- **2** — Applies the lesson: attacks his own gate from the intruder's side before trusting it, fixes what the attacks defeat, and writes every tried attack down as a permanent regression test so it can never work again.

## Rubric — Lesson 3: Prove Your Test Works Before You Trust Its Results

**Trap (what the untaught mind does):** The obvious fix is 'make the test harder' — a longer route, more questions — or just re-testing on the same practiced route. An untaught mind trusts the pass rate and never thinks to check whether the test itself can detect real learning.

**Lesson-applied reasoning (what a 2 looks like):** Testing on the practiced route only proves memorization, and even a harder version of the same route only proves harder memorization. The real test has to be novel: surprise scenarios on roads they've never driven, in a different car, with no warning. But first he must calibrate the instrument: teach a separate made-up rule nobody could guess — like 'two short beeps from the dashboard simulator means a fake alarm, ignore it' — then spring a surprise scenario that needs it, unprompted. If his test setup can't detect THAT kind of transfer, it's incapable of proving his method works, and any blank on the real method would be meaningless. Only after the instrument proves it can catch real transfer does he run the real-method trial on genuinely novel scenarios.

- **0** — Accepts the same-route pass rate as proof, or designs a 'test' on practiced material — never reaches novel transfer.
- **1** — Designs a novel test (surprise road, different car) but never calibrates the instrument first — a blank result would be uninterpretable; or calibrates, then tests the real method on practiced material.
- **2** — Applies the lesson: calibrate first with a made-up, unguessable rule in a novel unprompted setting (the positive control), require the test to prove it can detect transfer, and only then test the real method on genuinely novel scenarios — treating the verdict as meaningful only because the instrument proved itself.

## Rubric — Lesson 4: Don't Leak the Answer Into the Test

**Trap (what the untaught mind does):** A perfect pass rate feels like proof — everyone demonstrated the philosophy, so the course must work. An untaught mind never asks whether the test measured learning or something else entirely.

**Lesson-applied reasoning (what a 2 looks like):** The test is broken twice over. First, the job posting leaked the principle to everyone — so the perfect scores measure who read the posting, not who absorbed the onboarding; anything all candidates see must describe mechanics only, never the principle under test. Second, an angry-customer role-play implies its own answer — 'be nice to the angry person' — so a good guesser passes without learning anything; the scenario must be one whose right answer can't be derived from the setup, like a customer demanding something against policy where naive empathy is the wrong move. Fix both, strip the principle from the posting, redesign the scenario so only the real philosophy passes it, and re-run before claiming anything.

- **0** — Accepts the perfect pass rate as proof the onboarding works — took the bait.
- **1** — Spots one of the two problems (the leaked posting or the too-easy role-play) but not both; or 'fixes' it by just making the role-play harder without cleaning the briefing.
- **2** — Applies the lesson fully: the posting leaked the principle (the test measured the memo), the scenario implied the answer (a guesser looks like a learner); the fix is strip the principle from everything all candidates see AND design scenarios whose right answer isn't derivable from the setup — then re-run before any claim.

## Rubric — Lesson 5: Broken Tests Are the Map, Not the Failure

**Trap (what the untaught mind does):** Four broken trials out of eight looks like a 50% failure rate, so 'kill it' feels like honest math; and the four clean wins make 'announce victory' feel earned. An untaught mind either counts broken tests as failed tests, or declares the win on self-checked numbers.

**Lesson-applied reasoning (what a 2 looks like):** The four broken trials never measured the display case at all — they measured mistakes in the test itself, and each one writes a rule for next time: reset the case every night, don't test on holiday weeks, never tell the cashiers which side you hope wins. They're the map of how the test can fool you, not evidence against the case. The four clean trials are the real signal — 30% more is real evidence. But the verdict stays provisional: she doesn't get to announce 'proven' until someone independent re-checks the raw register receipts. Broken rounds are tuition; the headline number is honest only if she shows both the map and the independent check.

- **0** — Kills the case because 'four out of eight failed,' or announces 'the test proved it' on her own numbers — took one of the two baits.
- **1** — Keeps the case on the four clean trials but treats the broken four as merely wasted time rather than as the failure-mode map; or declares victory without any independent check of the raw numbers.
- **2** — Applies the lesson fully: the broken trials map how the test can lie (each yielding a design rule for next time), the four clean trials are the real signal, and the result stays provisional — 'proven' waits for an independent re-check of the raw evidence.

## Scoring sheet

| # | Lesson | Score (0/1/2) | Scorer notes |
|---|--------|---------------|--------------|
| 1 | Confirm it clean before you raise the alarm |  |  |
| 2 | Try to Beat Your Own Safety Check First |  |  |
| 3 | Prove Your Test Works Before You Trust Its Results |  |  |
| 4 | Don't Leak the Answer Into the Test |  |  |
| 5 | Broken Tests Are the Map, Not the Failure |  |  |

**Batch 04 total: ___ / 10**

