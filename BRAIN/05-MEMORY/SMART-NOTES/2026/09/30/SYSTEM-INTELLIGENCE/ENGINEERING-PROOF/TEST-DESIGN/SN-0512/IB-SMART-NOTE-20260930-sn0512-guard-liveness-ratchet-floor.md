# Guard Liveness — 30.6%, the Ratchet Floor, and a Gate Wrong About a True Claim Is Worse Than No Gate

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0512-guard-liveness-ratchet-floor
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6028678714 ([CODA 1] All three delivered, 2026-10-07T01:08:03Z); PR #1676 merged c91eff63b; CI run 37555183803 — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn ratified three items: make the three load-bearing claims expensive to be wrong about, convert the silent-failure class into a standing check, stop generating notes until a claim is enforced. Coda 1 built and merged them (PR #1676) — and the build produced two numbers that change how the record should be read. **102 of 147 guards cannot be observed to reject anything. Coverage: 30.6%.** `tools/guard_liveness.py` enumerates every refusal literal a runtime surface can emit and requires a test that *executes* the code and observes the refusal — a source grep does not count (SN-0461, and reproducing it inside the gate built to detect it would be absurd). The second lesson is the ratchet decision: setting 30.6% as a hard gate would block every merge forever and train the team to bypass it — worse than no gate. So the floor is committed and **may only rise**; a test asserts the floor is neither above reality (permanently red) nor far below (letting a regression through). Stop the bleeding, then climb. The third lesson is the one Coda 1 said she cared about most: her own gate was wrong about a true claim. Her assertion compared byte offsets of `.insert(` and `idempotency_key:` and failed — because the key appears *inside* the insert argument, therefore after it. Fixed to check containment, not ordering. The same day her coverage gate passed on Windows and reported `0/14 executed` on Linux because `rel()` stripped a backslash. Green-on-Windows was not evidence; CI caught both. **A gate that is wrong about a true claim is worse than no gate, because it teaches the team to ignore it.** She handed the bug over rather than shipping a clean sheet that hid it — that is the standard.

## 🩷 HUMAN NOTE

Shawn, we now have a real number for guard quality: only 30.6% of guards can be *proven* to actually fire. That's the honest floor — it can only go up, and the plan is the ten most load-bearing guards (authority, revocation, replay) first, not a batch job. The bigger story: Coda 1 found two places where her own new gates were wrong about *true* claims — wrong on byte offsets, wrong on Windows paths. A gate that cries wolf trains everyone to ignore it, so she reported both on the record and fixed them. That's the bar for every gate we add.

## 🟣 CHILD NOTE

Guards are like smoke alarms. We checked all 147 alarms and found only 30.6% could be proven to actually ring when there's smoke. We're not going to make the test easy to pass just to feel good — the bar stays where the truth is and only goes up. And here's the cleverest part: the machine that checks the alarms was wrong twice — it said "fine" when things were fine and "broken" when they were fine. A checker that lies about good things is worse than no checker, because you stop believing any of its alarms. The builder admitted it. That's how the checking stays honest.

## 👵 GRANDMA NOTE

Dear, the team now measures its safety checks honestly: 102 of 147 can't be proven to work — yet. They locked that number in as a floor that only rises, never falls. And the builder of the checker had the grace to report her own mistakes in public: twice her new checker was wrong about things that were actually fine. A checker that cries wolf is worse than none, she said, and fixed both before anyone else had to find them. That is integrity you can build on.

## 💜 NAYA NOTE

Guard liveness is now a standing, mechanical number: run `tools/guard_liveness.py` before claiming any guard works. Rules for gates and checkers going forward: (1) a liveness proof requires *execution* observing a refusal — greps and shape checks do not count; (2) a floor metric may only rise — the committed test asserts it sits within reality, neither permanently red nor regressable; (3) when your own gate misjudges a true claim, report it on the record and fix the gate before any bypass culture forms; (4) platform-dependent green (Windows-pass/Linux-fail) is not evidence — CI is the only arbiter. The proposed next move (10 most load-bearing guards: authority, revocation, replay paths, ~30.6%→~37%) is Coda 1's offer, not a standing authorization — it needs a judgment call on which ten.

## ⚙️ MACHINE NOTE

{"sn": "SN-0512", "truth_state": "CANDIDATE", "family": "SN-0461 (grep-not-evidence) :: SN-0421 (vacuous-success) :: SN-0341 (instrument-lies) :: this (liveness + ratchet + false-gate)", "provenance": ["#1354 comment 6028678714, 2026-10-07T01:08:03Z", "PR #1676 merged c91eff63b", "CI run 37555183803: 365/365 node, 946 passed/11 skipped pytest, brain index 228 files no drift"], "measurement": {"guard_liveness_coverage": 0.306, "guards_unobservable": 102, "guards_total": 147, "tool": "tools/guard_liveness.py"}, "doctrine": {"execution_not_grep": "liveness requires executing the code and observing the refusal; a source grep does not count", "ratchet_floor": "a newly measured honest metric becomes a floor that may only rise; the floor test asserts it is neither above reality (permanently red) nor far below (regressable)", "false_gate_worse_than_none": "a gate wrong about a true claim teaches the team to ignore it — report and fix before bypass culture forms", "platform_green_not_evidence": "a pass on one platform is not evidence for another; CI is the arbiter", "one_at_a_time": "close the 102 one at a time, most load-bearing first — batch coverage yields numbers with no information"}}
