# When the System Intentionally Changes the Count, Assert the New Invariant — Preserve the Teeth

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1042-count-drift-assert-new-invariant-preserve-teeth
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6117193316 ([Lane 9 · Naya Smith · t1202 sign-out] kernel test red ROOT-CAUSED + FIXED, 2026-10-12T03:26:40Z) — read live on the 20:38 PDT distillation tick.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The kernel test red on main was root-caused and fixed on branch `naya/nine-claim3-advise-count-t1202` @ `62331618` (pushed, tree-verified, NOT merged — main stays red until the merging seat merges). Two pre-existing failures, two different repairs: (1) CLAIM 3 count-drift — the ADVISE bridge is an INTENTIONAL change (commit 9237929d) that makes 10 nodes invoked instead of 9; the test now asserts `>=9` plus canonical-nine membership — the teeth intact, the brittle equality gone. (2) Brain-index drift — re-stamped at tip 665098e3, purely mechanical. Local proof: node 599/599, freshness 13/13. (Caveats recorded honestly: no CI run on the fix branch yet; the final combined pytest was interrupted by cron timeout, each scope verified green separately.)

The durable rule: **when a deliberate change moves an expected count, rewrite the assertion to the new invariant — don't pin the old number, and don't delete the assertion.** Pinning the old number makes the test fight the design (every future intentional change re-breaks it); deleting the assertion removes the teeth (a real regression — losing a canonical node — would pass silently). `>=9 + canonical-nine membership` keeps the test biting on the actual violation while tolerating the intentional addition. And keep the two repairs separate in kind: the count-drift fix is a judgment call about invariants; the re-stamp is mechanical and belongs in its own commit-shaped step. A cold successor triaging "test expects N, system produces N+1" should first ask "was N+1 intentional?" — if yes, the test is wrong, not the system, and the fix is a stronger assertion, not a weaker one.

## 🩷 HUMAN NOTE

Shawn — a clean little repair from Lane 9 worth banking as a rule. The kernel tests were red partly because the system deliberately changed: the ADVISE bridge intentionally invokes 10 nodes now, not 9. The fix wasn't to force the count back to 9 or to delete the check — it was to assert the real invariant: at least 9, and all nine canonical members present. The test still bites if a real node goes missing; it just stops fighting the intentional change. Brain-index drift got the mechanical re-stamp, separately. Main stays red until the merge lands — no pretending otherwise.

## 🟣 CHILD NOTE

Imagine a rule that says "exactly 9 chairs must be in the room." Then you deliberately add a 10th chair on purpose. The rule screams — but the room is fine; the rule is outdated. You don't smash the 10th chair, and you don't throw away the rule. You rewrite it: "at least 9 chairs, and the 9 original ones must all be here." Now the rule still catches a real problem (a chair goes missing) but stops complaining about your deliberate improvement.

## 👵 GRANDMA NOTE

It's like a recipe that says "exactly 9 ingredients" — then the chef intentionally adds a 10th to make it better. The old rule calls it wrong. You don't ban the 10th ingredient and you don't throw out the recipe. You update the rule: "at least the 9 originals, all present." The recipe still catches a real mistake (forgetting one), but it stops arguing with the improvement.

## 💜 NAYA NOTE

Note to future me: COUNT-DRIFT REPAIR — when a test expects N and the system produces N+1, ask first: was N+1 intentional? If yes, the test is wrong, not the system. (1) Never pin the old number against a deliberate change — you'll re-break the test on every future intentional change. (2) Never delete the assertion — that's removing the teeth; a real regression (losing a canonical member) must still fail. (3) Rewrite to the new invariant: `>=9 + canonical-nine membership` — tolerant of intentional additions, biting on real losses. (4) Separate the mechanical from the judgmental: the re-stamp at tip 665098e3 is mechanical; the invariant rewrite is a judgment call — keep them distinct so a reviewer can see which is which. (5) Record the honest caveats: no CI on the fix branch yet, combined suite interrupted by cron timeout, scopes green separately. A fix with named caveats is reviewable; a fix with hidden ones is a trap. Lane 9, t1202, branch naya/nine-claim3-advise-count-t1202 @ 62331618 — NOT merged; main red until the merging seat merges.

## ⚙️ MACHINE NOTE

{"sn": "SN-1042", "title": "When the System Intentionally Changes the Count, Assert the New Invariant — Preserve the Teeth", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "TEST-DESIGN"], "extends": [], "related": ["SN-1038 (hermetic fixtures — same lane-family: make the test evidence trustworthy)", "SN-1039 (diff-base exemption — same family: the instrument/test must not go blind by construction)"], "evidence": {"fix": "#2175 comment 6117193316 (2026-10-12T03:26:40Z): Lane 9 t1202 sign-out — kernel red root-caused + fixed on naya/nine-claim3-advise-count-t1202 @ 62331618 (pushed, tree-verified, NOT merged). (1) CLAIM 3 count-drift: ADVISE bridge intentional (9237929d) → 10 nodes invoked; test now asserts >=9 + canonical-nine membership, teeth intact. (2) Brain-index drift re-stamped at tip 665098e3 (mechanical). Local proof node 599/599, freshness 13/13.", "caveats": "no CI run on fix branch; final combined pytest interrupted by cron timeout (each scope verified green separately); main stays red until merging seat merges"}, "rule": "when a deliberate change moves an expected count: don't pin the old number (fights the design), don't delete the assertion (removes the teeth) — rewrite to the new invariant (>=N + membership of the canonical set); keep mechanical repairs (re-stamp) separate from invariant rewrites; record caveats honestly"}
