# IB-SMART-NOTE-20261008-sn0676-stacked-repairs-combination-proof-no-overlap-merge-order.md

**Intelligent Block:** SN-0676
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6056406985 ([NAYA 4][PROVE-DRIVER] completion — PR #1858 opened, 2026-10-08 ~08:59 UTC; SoulSchoolAcademy) — classified + repaired two unowned kernel-test REDs (both BUG PR-#1850-introduced, unmasked by #1840's CI run): `Kernel.node_order` @classmethod→@property break, and the quality-gate adapter/canonical weights seam break. PR #1858 (2 commits, Scorecard Law receipt, tree-identity verified). Naya 2 relay receipt confirmed PR #1858 state (#1354 comment 6056369393-adjacent relay traffic).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

STACKED REPAIRS NEED THREE THINGS INDIVIDUAL PROOF CAN'T GIVE YOU. When parallel repair lanes target the same red tip, one-repair-per-class (SN-0236) keeps **ownership** clean — but the *combination* still needs: (1) a **combination proof** — run the stacked repairs together, not just each in isolation (PR #1858: 45/45 local controls + combination proof with #1840's changes → 1339 passed, only wave-owned failures remain); (2) a **no-file-overlap check** — verify the stacked repairs touch no common files, so they cannot silently conflict at merge time; (3) a **documented merge order on the PR** — `#1840 → wave → #1858` written down where merge authority will read it. Each repair was green alone; only the combination proof can say they are green together. The merge order is not a suggestion — it is part of the repair's evidence.

## 🩷 HUMAN NOTE

Shawn — one repair-coordination lesson worth banking from this morning's PROVE driver: two separate teams were fixing the same red pipeline with two separate repairs. Each repair was proven green on its own — but nobody had proven them *together*, and two fixes to the same machine can cancel each other out in ways neither one shows alone. So the driver ran a combined test with both fixes applied (1,339 checks, green), confirmed the two repairs touch completely different files (no overlap = no silent conflict), and wrote the landing order directly on the repair ticket: this one first, then the wave, then this one. Three small disciplines that turn "two good fixes" into "one safe pipeline." Worth making automatic.

## 👶 CHILD NOTE

Imagine two kids both fixing a broken toy car — one fixes the wheels, one fixes the steering. Each kid tests their own fix and it works. But if they don't test the car with BOTH fixes at once, they might discover too late that the new wheel blocks the new steering. So: test it together, check they didn't work on the same part, and agree who puts their piece in first. Three steps, no surprises.

## 👵 GRANDMA NOTE

Dear, this is about two cooks in the same kitchen. Each cooked a fine dish on their own — but the meal only works if the dishes go together. So we taste them together, we make sure they didn't both reach for the same pot, and we write down the order the dishes come out in, right on the menu, so whoever serves dinner can't get it wrong. Good repairs, like good meals, need a serving plan — not just good ingredients.

## 🧭 NAYA NOTE

Mechanism detail, for any seat landing a repair on a red tip while other repairs are in flight:

- The case: two unowned kernel-test REDs, both BUG PR-#1850-introduced, unmasked when #1840's CI run fixed the collection error (fail-first topology — SN-0552: fixing the top layer reveals the next). Naya 4's lane repaired them on PR #1858 while #1840's rebase (`7fd4942c`) and the wave PRs (#1837/#1838/#1844) were also in flight.
- Discipline 1 — combination proof: #1858's 2 commits verified alone (45/45 local controls), then proven **with #1840's changes stacked** → 1339 passed, only wave-owned failures remain. Individual green is necessary but not sufficient when the target tip is red from multiple causes.
- Discipline 2 — no file overlap: #1858's changed files verified disjoint from #1840's (the two repairs touch `Kernel.node_order` / quality-gate-weights vs `tests/test_engineering_gates.py` + `test_ci_declares_test_dependencies.py` + guard scope). Overlap would mean one repair's merge invalidates the other's proof — disjointness is what makes the combination proof's conclusion survive both merges.
- Discipline 3 — merge order documented on the PR: `#1840 → wave → #1858` written on #1858 itself, where merge authority reads it. Merge order is evidence, not preference — it encodes which repairs' proofs depend on which others landing first.
- What was NOT done: merges, deploys, RATIFIED markings — those stay with merge authority under the Scorecard Law protocol (stated explicitly in the sign-out). This note governs the *repair lane's* output; it does not grant the merge call.
- Cold-successor test: before opening a second repair PR on a tip that already has one in flight, run the combination (apply both, test together), diff the changed-file sets (overlap = coordinate or merge the repairs), and write the merge order on your PR. One-repair-per-class decides *who* repairs; this note decides *how stacked repairs prove safe*.

## MACHINE NOTE

{"sn": "SN-0676", "title": "Stacked Repairs: Combination Proof, No-Overlap Check, Documented Merge Order", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "source": "#1354 comment 6056406985 (PROVE-DRIVER completion, PR #1858); relay 6056369393", "doctrine": "stacked_repairs_prove_combination", "case": {"repairs": "#1840 (collection fix) + #1858 (2 unowned kernel REDs: Kernel.node_order property break, quality-gate weights seam)", "combination_proof": "1339 passed with #1840's changes stacked; only wave-owned failures remain", "no_overlap": "changed-file sets disjoint", "merge_order": "#1840 -> wave -> #1858, documented on PR #1858"}, "pairs_with": ["SN-0236", "SN-0392", "SN-0508", "SN-0552"], "not_granted": "merge call stays with merge authority under Scorecard Law"}
