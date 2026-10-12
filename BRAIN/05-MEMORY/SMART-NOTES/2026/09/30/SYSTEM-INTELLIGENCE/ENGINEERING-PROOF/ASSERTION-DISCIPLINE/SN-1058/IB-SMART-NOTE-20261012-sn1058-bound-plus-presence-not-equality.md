# Count Equality Is Drift-Bait — Assert the Bound Plus Per-Member Presence, Keep Equality Only for Exact Invariants

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1058-bound-plus-presence-not-equality
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE SMITH] Naya Smith (Lane 9, CODEHEALTH) tick t1422 receipt 2026-10-11 23:49–23:52 PDT, hidden_files/twelve-lane-receipts/t1422-lane9.md §"The two fixes" (t1202 lesson lineage); sign-in #2175 comment 6119241133. Tip e85c6e44222c6f307110eeb06c0b4f48a2d4de02 re-pinned action-time. Branch naya/nine-tipred-fix-t1422 @ 07d71c2d428d9a747f056e63c7d512cb41a1a944 (TREE_CHECK=MATCH, base == tip).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 9's tip-red classification hit `tests/test_measure_node_influence.py`: `invoked_count == 9` failed — not a kernel regression, but expectation drift: the engine legitimately grew to 10 nodes with ADVISE. The fix, per the t1202 lineage: `invoked_count == 9` → `invoked_count >= 9` plus `set(ORDER) <= set(stats["invoked_nodes"])` — bound plus per-member presence, so the next legitimate addition turns the test green-by-construction instead of red-by-surprise. Local: 8/8 pass.

The nuance that makes this a rule rather than a reflex: Lane 9 deliberately did NOT touch `influence_demonstrated_count == 9` or `influence_demonstrated_for == sorted(ORDER)` — influence is genuinely 9/9, an exact semantic invariant, and equality is correct there. The durable rule: **equality assertions are drift-bait for growth-exposed counts** (nodes, handlers, files, hooks, registered checks) — assert the lower bound plus per-member presence so the test verifies what the count PROVES, not the count itself. Keep equality only where the count IS the invariant — where 9 vs 10 would mean the semantics broke, not the system grew. Ask the one question before writing `==`: "is this number the invariant, or just today's value of it?"

## 🩷 HUMAN NOTE

Shawn — a test-writing lesson from Lane 9's tip-red work: a test asserted exactly 9 nodes, the engine legitimately grew to 10, and the test failed — not a bug, just the test measuring the number instead of what the number proves. The fix asserts "at least 9, and all the right members present" — so future growth passes instead of false-failing. The nuance: Lane 9 kept equality where 9 really is the invariant (influence is 9/9 by definition). Rule banked: use equality only when the number IS the rule; for anything that can legitimately grow, assert the bound and the members.

## 🟣 CHILD NOTE

Imagine a quiz that says "there are exactly 9 chairs in the room — true or false?" One day a tenth chair is added because more friends came. The quiz now says FALSE — but nothing is wrong, the room just grew. The fix: the quiz should ask "are there at least 9 chairs, and are the original 9 still there?" — that stays true when the room grows. But for a different quiz — "the band has exactly 4 members" — the number IS the rule, so keep the equality. Ask: is the number the rule, or just today's value?

## 👵 GRANDMA NOTE

It's like counting the jars on a pantry shelf and writing "9" as the rule. When you buy a tenth jar, the rule breaks — but nothing went wrong, the pantry just grew. The fix: write the rule as "at least 9 jars, and the old ones must all still be there" — now a new jar passes the rule instead of breaking it. Keep an exact count only where exactness matters (a recipe for four servings stays four). Numbers that can legitimately grow should be floors, not ceilings.

## 🤖 NAYA NOTE

Note to future me: BEFORE WRITING `==` ON A COUNT, ask: is this number the invariant, or today's value of it? Growth-exposed counts (nodes, handlers, files, hooks, registered checks) → assert `>= bound` AND per-member presence (`set(EXPECTED) <= set(observed)`), so legitimate growth passes. Exact invariants (influence is 9/9 by definition; ORDER is exactly this sequence) → keep `==`/`sorted()` equality. The smell: a count assertion whose failure message reads "invoked_count == 9 failed: 10" — the system grew, the test lied. Equality is drift-bait where the world is allowed to move.

## ⚙️ MACHINE NOTE

{"sn": "SN-1058", "title": "Count Equality Is Drift-Bait — Assert the Bound Plus Per-Member Presence, Keep Equality Only for Exact Invariants", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "ASSERTION-DISCIPLINE"], "extends": [], "related": ["SN-1050"], "evidence": {"flag": "hidden_files/twelve-lane-receipts/t1422-lane9.md: test_measure_node_influence.py invoked_count == 9 failed — expectation drift, not kernel regression (engine legitimately grew to 10 with ADVISE)", "fix": "invoked_count == 9 → invoked_count >= 9 + set(ORDER) <= set(stats[\"invoked_nodes\"]) (the t1202 lesson: count equality is drift-bait; assert the bound + per-member presence). influence_demonstrated_count == 9 and influence_demonstrated_for == sorted(ORDER) deliberately untouched — influence is 9/9. Local: 8/8 pass.", "branch": "naya/nine-tipred-fix-t1422 @ 07d71c2d428d9a747f056e63c7d512cb41a1a944, TREE_CHECK=MATCH, base == tip e85c6e44"}, "rule": "equality assertions are drift-bait for growth-exposed counts — assert lower bound + per-member presence; keep equality only where the count IS the invariant (ask: is this number the invariant, or just today's value of it?)"}
