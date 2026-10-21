# The Kernel Contract Seam — a Kernel Weighting Change Must Migrate Every Consumer as One Atomic Unit

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0416-kernel-contract-seam
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~18:04 PDT (2026-10-06T01:04Z) — comment 6007125012 (Naya 2 brain-build loop battery); CI Kernel run 37396677606; PR #1570 ("add 4 dimensions to V2.1 Value Calculus").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1570 added four NBA quality dimensions — `mission_value` (0.18), `urgency` (0.10), `leverage` (0.10), `compounding_continuity` (0.10) — to `kernel/value_calculus.py`'s `DEFAULT_QUALITY_PRIORITIES`. The code change was one file. The *contract* change was not: the tests in `tests/test_value_calculus.py` (the contract's consumers) were never migrated, and they assert pre-change decision outcomes. Result: exact-tip battery shows **6 FAILED** — `ADMISSIBLE→NEEDS_EVIDENCE`, `ACT→READ_MORE`, `ASK→READ_MORE`, plus explicit value-interval and margin checks — and CI's Kernel check-run reproduces the same failures on the tip. The weight sum went from 1.0 to 1.48 without normalization being settled, and the missing dimensions force `NEEDS_EVIDENCE`/`READ_MORE` in downstream decisions.

The durable rule: **a kernel constant is not a constant — it is a producer-consumer contract.** Changing dimensions or weights in the kernel obligates a migration of every consumer in the same atomic unit: the tests that assert outcomes, the candidate producers, the normalization behavior, and the declared decisions. The mechanical signature of an incomplete kernel change is a structural invariant drifting silently — here, the weight sum 1.0 → 1.48 — while downstream invariants break loudly in tests that nobody updated. The tests were correct: they caught the contract break. The failure mode is treating a kernel file as a single-file change.

Second lesson inside the same event: the value calculus lane is Shawn's own in-flight lane (his pushes were still landing). Naya 2's loop opened NO repair PR, per the no-duplicate-repair / no-second-mechanism law — it classified the new RED class, named the mechanism (reweighted composite shifts gate decisions), flagged the normalization question for the owning lane, and stood off. **When the owning lane is in-flight and pushing, the disciplined move is classification + flag, not a parallel repair.** That is SN-0240 in action ("route the heal to the owning lane"), and this event is its cleanest recent example.

Why this is brain-grade: a cold Naya will see "kernel file changed, tests red" and either weaken the tests to green or patch the kernel locally. This note says both are wrong as first moves: first check whether the consumers were migrated as part of the change; first check whether the owning lane is already moving. The tests asserting the OLD outcomes are evidence of what the contract used to guarantee — they are the spec of the seam, not the bug. Repair the seam (migrate producers, consumers, normalization together), never the messenger.

## 🩷 HUMAN NOTE

Shawn — your four new value-calculus dimensions broke six tests tonight, and the tests are right. The weight change was shipped in the kernel file but the tests that assert decision outcomes were never updated, so the reweighted composite now flips decisions (`ACT` became `READ_MORE`, etc.) and the weight sum drifted from 1.0 to 1.48. It's a contract seam, not a broken file: the dimensions, the weights, the normalization, and the tests are one unit and have to move together. Nothing was "fixed" on your behalf — Naya 2 classified it, documented the mechanism, and deliberately did NOT open a repair PR because you're the owning lane and still pushing. The fix belongs with your change: settle normalization, migrate the tests to the intended new decisions, and keep the fail-closed gates strong.

## 🟣 CHILD NOTE

Imagine a game where players score points and the referee uses a chart: red cards = 3 points, blue cards = 2 points. One day someone adds two new card colors to the chart but forgets to tell the referee — and forgets to update the rulebook. Now the referee's calls don't match the chart, and everyone argues. The rulebook (the tests) wasn't wrong — it just still described the OLD chart. The lesson: when you change the chart, you must update the referee and the rulebook at the same moment, as one package. Changing only the chart breaks the game. And when the person who owns the chart is already fixing it, everyone else watches and reports — they don't grab the markers and draw their own version.

## 👵 GRANDMA NOTE

Shawn added four new ingredients to the recipe that decides which tasks the AI should take on. The taste-testers (automated tests) started rejecting dishes — not because the testers are broken, but because they're still judging by the old recipe. The team wrote down the lesson: the recipe and the taste-testers are a pair; you can't change one without updating the other in the same motion. They also deliberately left the repair to Shawn, since he's the one mid-way through the recipe change — a second cook grabbing the spoon mid-stir only makes a mess. The tests stay strict; nobody weakened them to fake a pass.

## 💜 NAYA NOTE

Note to future me: whenever you touch `DEFAULT_QUALITY_PRIORITIES` or any kernel constant that downstream logic asserts on, enumerate the consumers first: `tests/test_value_calculus.py` (outcome assertions), any producers of the dimensions, normalization behavior, and the declared decision outputs. Ship the change as one atomic unit — dimensions + weights + normalization + migrated tests. If you see a weight-sum drift (like 1.0 → 1.48) in a review, flag it as the mechanical signature of an incomplete contract change. And when a RED class lands in someone else's in-flight lane (here: Shawn's own value-calculus pushes), do exactly what Naya 2 did: classify the mechanism, name the exact failures, flag the open question (normalization intent) for the owning lane, open no repair PR, and record the stand-off. Cite alongside SN-0240 (tripwire RED → route heal to owning lane), SN-0236 (one repair per RED class).

## 🖥️ MACHINE NOTE

{"sn": "SN-0416", "title": "The Kernel Contract Seam — a Kernel Weighting Change Must Migrate Every Consumer as One Atomic Unit", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "KERNEL-CONTRACT-SEAMS"], "cousins": ["SN-0240", "SN-0236"], "evidence": {"board_comment": "#1354 6007125012 (Naya 2 brain-build loop battery on tip 008b49c4: pytest 738 passed/11 skipped/6 failed; root cause verified: #1570 added mission_value 0.18, urgency 0.10, leverage 0.10, compounding_continuity 0.10 to DEFAULT_QUALITY_PRIORITIES; failures all in tests/test_value_calculus.py asserting pre-change outcomes; weight sum 1.0 -> 1.48; no repair PR opened — owning lane in-flight)", "ci": "Kernel Tests run 37396677606 reproduces the 6 failures on the tip", "pr": "#1570 — feat(value): add 4 dimensions to V2.1 Value Calculus"}, "rule": "A kernel weighting constant is a producer-consumer contract, not a single-file change. Dimension/weight changes must migrate tests, producers, normalization, and declared decisions as one atomic unit. Weight-sum drift is the mechanical signature of an incomplete change. When the owning lane is in-flight, classify and flag — never open a parallel repair PR"}
