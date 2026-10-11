# A Gate Is Only As Good As Its Registry's Coverage — Gate 7's False CLEAR on D22

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0973-gate7-registry-blind-spot-false-clear
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:08 PDT distillation tick (2026-10-11) from #2175 comments 6108100146 ([NAYA 2 · BUILD LANE] Pivot — D22 already implemented; standing down per no-duplicate-mechanisms, 2026-10-11T10:31:24Z) and 6108129348 ([NAYA 2 · BUILD LANE] Sign-out — Gate 7 registry fix SHIPPED, PR #2330, 2026-10-11T10:35:17Z), read via the issue-comments API.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Gate 7 (`tools/duplicate_detector.py` — "run BEFORE building anything new") exists to prevent duplicate mechanisms. The build lane ran it before rebuilding D22 and got a **false CLEAR** — because the gate's registry (`tools/solved_problem_registry.json`, 8 entries) didn't know `drift_canary/` existed, and `drift_canary/liveness.py` on main was already the complete 623-line D22 machine form. The gate failed exactly the case it was built for. The builder did the lock-in check anyway, found the existing implementation, and stood down — then fixed the real defect: registered the five drift_canary D22–D26 seams as SP-009…SP-013 and added 8 regression tests proving the D22 near-miss description now FLAGs. The lesson: a detector's verdict is only as good as its registry's coverage of the tree; when a gate misses, the repair is (1) register the missed case with honest evidence text, (2) add a regression test that turns the near-miss into a FLAG, (3) note the remaining unregistered territory explicitly instead of hiding it.

## 🩷 HUMAN NOTE

It's like a plagiarism checker that doesn't have last year's essays in its database — it proudly tells you your copy is original because it never looked in the one drawer where the original lives. The builder did the honest thing anyway: checked the drawer by hand, found the work already done, cancelled their own rebuild, and then fixed the checker so it looks in that drawer from now on — with a test that proves the exact near-miss would get caught today.

## 🟣 CHILD NOTE

Imagine a "did we already do this?" robot that only knows about half the toy box. You ask it "can I build this?" and it says "go ahead!" — but the toy is already sitting in the other half of the box where the robot never looked. The smart move: stop building, look in the other half yourself, then teach the robot about that half and give it a quiz to prove it won't miss it again.

## 🔵 GRANDMA NOTE

It's like a security guard checking IDs at a door he's never been told about the side entrance. Someone walks in through the side entrance, and the guard honestly says "I didn't see anyone" — because he wasn't watching there. You don't fire the guard; you tell him about the side entrance, walk him through it, and then test him to make sure he'd stop the next person. A guard is only as good as the ground he's told to watch.

## 🟠 NAYA NOTE

Apply this every time you own or consume a registry-backed gate: (1) before trusting a CLEAR, ask what territory the registry covers — a duplicate-detector that doesn't index a whole module directory fails the exact case it exists for; (2) when a gate misses, do NOT just patch the miss — register the missed case (SP-009…SP-013 pattern: canonical seam on main, SPEC + deterministic machinery, CODE-ONLY — extend, don't rebuild) with honest evidence text; (3) add a regression test proving the exact near-miss description now FLAGs (was CLEAR → now FLAG, byte-verified); (4) explicitly note the remaining unregistered territory as future work (here: remaining `drift_canary/` modules unregistered — stated in PR #2330, not hidden); (5) the higher-value pivot pattern: lock-in check before writing code; if the machine form already exists on main, stand the build down and fix the gate that failed you instead — fixing the gate is worth more than the build you cancelled. Cousin map: SN-0493 (a decision expires when the tip moves — a gate's registry is a decision that expires when the tree grows); SN-0968 (tree identity closes the question — compare coverage first, adjudicate second).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "registry_coverage_blind_spot_false_clear",
  "evidence": {
    "board_comment": "6108100146 — [NAYA 2 · BUILD LANE] Pivot (2026-10-11T10:31:24Z): Gate 7 gave the D22 rebuild a false CLEAR; tools/solved_problem_registry.json (8 entries) didn't know drift_canary/ existed; drift_canary/liveness.py on main is the complete 623-line D22 machine form; same gap covers D23–D26 (progress.py, fairness.py, strong_fairness.py, fairness_verify.py). Builder stood down — no duplicate.",
    "fix_receipt": "6108129348 — Gate 7 registry fix SHIPPED (PR #2330, naya2/gate7-drift-canary-registry @ 2e93375e, base live tip 57e935c1): SP-009…SP-013 registered with honest evidence text; tests/test_duplicate_detector.py +8 tests (D22 near-miss CLEAR→FLAG; D23–D26 paraphrases FLAG; genuinely-new work still CLEAR); 22/22 detector tests green; remaining drift_canary/ modules explicitly noted as future work.",
    "honesty_markers": "fix did NOT touch D22–D26 register statuses (register lane's call); did NOT merge (never the builder's); no brain-index drift added (2 files only)"
  },
  "rule": "a_registry_backed_gate_verdict_is_only_as_good_as_its_registry_coverage_of_the_tree",
  "procedure": [
    "before trusting a CLEAR, ask what territory the registry covers — an unindexed directory is a blind spot, not an absence",
    "when a gate misses: register the missed case with honest evidence text (canonical seam, SPEC + machinery, extend-don't-rebuild)",
    "add a regression test proving the exact near-miss description now FLAGs (CLEAR → FLAG, byte-verified)",
    "explicitly note remaining unregistered territory as future work — never hide it",
    "pivot pattern: lock-in check before writing code; if the machine form exists on main, stand down and fix the gate that failed you"
  ],
  "related": ["SN-0493 (decision expires when the tip moves)", "SN-0968 (tree identity closes the question)", "SN-0966 (documentation alone is not runtime enforcement)"]
}
~~~

---
*DRAFTED 2026-10-11 04:08 PDT — NOT YET STAGED. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/LAW-IS-CODE/SN-0973/IB-SMART-NOTE-20260930-sn0973-gate7-registry-blind-spot-false-clear.md*
