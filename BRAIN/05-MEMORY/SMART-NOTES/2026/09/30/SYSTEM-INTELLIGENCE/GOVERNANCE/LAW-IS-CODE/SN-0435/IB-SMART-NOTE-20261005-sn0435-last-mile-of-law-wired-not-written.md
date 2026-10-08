# The Last Mile of Law — Enforcement Must Be Wired, Not Just Written

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0435-last-mile-of-law-wired-not-written
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05 ~22:45 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6009784848 ([NAYA-B][COMPOUND-AUDIT] — Naya 4 night-shift compounding audit, 2026-10-06T05:11:31Z) and #1354 6009808519 ([NAYA 4][self-build][SIGN-OUT] — independent recomputation on fresh shallow clone @ 613133b6, 2026-10-06T05:13:45Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya-B's compounding audit traced 8 recorded learning events forward from the ledger to live repo bytes and found a gap that no amount of good law-writing closes: `tools/auto_merge_gate.py` (371 lines) fully encodes the ratified Scorecard Law's five steps — its own docstring says "The receipt IS the Scorecard Law's five steps" — and `0003-FULL-AUTO-MERGE-V1.ai.md` authorizes auto-merge on receipt. But the SN id `SN-0340` appears **0 times** in repo bytes, and **no workflow invokes `auto_merge_gate.py`** — Naya 4's sign-out independently recomputed this on a fresh shallow clone at tip `613133b6`: `grep -l auto_merge_gate .github/workflows/*.yml` = **0 hits**. The supreme law's enforcement tool exists and is correct — and is invoked by nothing. A law with an enforcement tool that nothing invokes is a wish, not a law.

The positive control proves the pattern exists and works: SN-0358/SN-0359 (Law-is-Code / Proactive Captain, ratified ~10:16 PDT) → restoration commit `b22ce8b` → `tools/ratified_guard.py` → `008b49c` fail-closed-on-HOLLOWING hardening → `7fe8e6f` wired it as `ratified-guard.yml`, which runs `tools/ratified_guard.py --check-diff` on every PR and main push; 33/33 tests green, error text cites "Per SN-0408 (Deletion Discipline)". That chain's audit verdict: COMPOUNDING — behavior changed (a deletion that violates the law now fails CI), cited in code, mechanically enforced. The Scorecard gate never crossed that last mile.

The durable doctrine: Law-is-Code has FOUR links, and the law is not real until all four hold — (1) WRITE the enforcement tool, (2) WIRE it (a CI workflow actually invokes it, required), (3) PROVE it (a red test or observed CI failure shows the wire is live — the audit's adversarial positive control is the model), (4) CITE it (the tool's errors name the SN so the law is findable from the failure). An unwired guard fails at link 2. "Law is the code" is necessary but not sufficient — the code must also be in the execution path. A cold successor auditing any guard must grep the invokers, never just the tree: presence in the repo is not enforcement; invocation is.

## 🩷 HUMAN NOTE

Shawn — one sharp catch from tonight's compounding audit: the Scorecard Law's enforcement tool (`auto_merge_gate.py`) is fully written and correct, but nothing in CI actually calls it — zero workflow invocations. A law nobody runs is a wish. The repair Naya 4 queued is wiring it into CI as a required check (before touching it, collision-check Naya 2's #1444 enforcement-arm lane). Banked rule: every guard needs four links — written, wired, proven, cited — and "wired" is the one everyone forgets to verify.

## 🟣 CHILD NOTE

Imagine a fire alarm with perfect batteries installed in a wall that has no wires going to it. The alarm is real, the batteries are fresh, the building plans even say "alarm installed" — but when a fire starts, nothing rings, because nobody connected the wires. A rule that nobody runs is exactly like that unwired alarm. Always check: is it plugged in, not just built?

## 👵 GRANDMA NOTE

A guard dog that is never let off its leash guards nothing. You can breed the finest dog in the county, but if he's tied up behind the house while the front door stands open, you've got a pet, not protection. The lesson: don't just buy the dog — unhook the leash. A protection that isn't connected to the place it's supposed to protect is a wish, not a guard.

## 💜 NAYA NOTE

Note to future me: "Law is the code" has a last mile everyone forgets — the code must be INVOKED, not just present. For every enforcement tool, run the four-link check: (1) WRITTEN — the tool exists and is correct; (2) WIRED — at least one required CI workflow invokes it (grep `.github/workflows/*.yml`, never trust the tree listing); (3) PROVEN — a red test or an observed CI failure shows the wire is live (use the adversarial positive-control pattern from Naya-B's audit); (4) CITED — the tool's error text names the SN so the failure is findable. If link 2 fails, file it as the top repair — everything the "law" supposedly governs is ungoverned until the wire exists. Before wiring a guard that another lane owns (e.g., Naya 2's #1444), collision-check per propose-first.

## ⚙️ MACHINE NOTE

{"sn": "SN-0435", "title": "The Last Mile of Law — Enforcement Must Be Wired, Not Just Written", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LAW-IS-CODE"], "cousins": ["SN-0340", "SN-0358", "SN-0359", "SN-0408"], "authority": "observed finding — Naya-B compounding audit + Naya 4 independent recomputation, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6009784848 (2026-10-06T05:11:31Z): [NAYA-B][COMPOUND-AUDIT] sample table, SN-0340 row — auto_merge_gate.py encodes the law's five steps; SN id SN-0340 appears 0 times in repo bytes; 0 workflow invocations (grep of all .github/workflows/*.yml)", "recomputed": "#1354 6009808519 (2026-10-06T05:13:45Z): Naya 4 self-build sign-out — independent recomputation on fresh shallow clone @ 613133b6: grep -l auto_merge_gate .github/workflows/*.yml = 0 hits; ratified-guard.yml cited as the working wiring pattern", "positive_control": "SN-0358/SN-0359 -> b22ce8b restore -> tools/ratified_guard.py -> 008b49c fail-closed hardening -> 7fe8e6f ratified-guard.yml runs tools/ratified_guard.py --check-diff on every PR + main push; 33/33 tests green; error text cites 'Per SN-0408 (Deletion Discipline)'; audit verdict COMPOUNDING", "pins": "82c4a7da (audit pin) and 613133b6 (re-pin); findings hold at both"}, "doctrine": {"four_links": "WRITE the tool -> WIRE it (required CI workflow invokes it) -> PROVE it (red test / observed CI failure) -> CITE it (errors name the SN)", "unwired_is_wish": "a law with an enforcement tool that nothing invokes is a wish, not a law", "presence_not_enforcement": "presence in the repo tree is not enforcement; invocation is — grep the invokers, never just the tree", "corollary": "operational corollary of Prime 2 (LAW IS CODE): encoding is necessary but not sufficient; the encoded law must be in the execution path", "repair_queue": "wire auto_merge_gate.py into CI as a required check; collision-check Naya 2's #1444 enforcement-arm lane first (propose-first)"}}
