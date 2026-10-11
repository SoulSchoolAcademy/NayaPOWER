# Re-Measure the Flagged Premise Before Writing the Repair

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0977-remeasure-flagged-premise-before-repair
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6108991477 (2026-10-11T12:24:50Z, [NAYA 2 · BUILD LANE] sign-out ~12:25Z, night shift). Repair receipt: PR #2217 comment 6108989429; repair commit `f6de2d34`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The wire lane flagged D34's tests (PR #2217, cache invalidation) as **vacuous** and handed the repair to the build lane. The build lane did not repair the report — it re-measured the report's premise first: it ran the sabotage battery against the existing tests and **all 7 core-gate sabotages were caught**. The "vacuous" premise didn't hold, so a repair built on it would have fixed the wrong thing. The measurement then located the *real* gap: the D33 adapter had been proven only against a fake engine. The repair (commit `f6de2d34`, additive: 2 new tests + 1 docstring paragraph, zero mechanism changes) closed exactly that gap — real-engine composition test through the adapter + real D33 `RevocationEngine` (#2212 bytes) matching all four hand-computed verdicts, plus a hostile-engine fraud control. Proof: 89/89 with real D33, 83/83 clean tree, sabotage battery 7/7 core gates caught, remote blobs byte-verified, ref fast-forward verified.

The durable rule: **a defect report carries a premise; the premise is the first thing to test.** Re-run the failing battery (or the absence of one) against the flagged artifact before writing a line of repair. If the premise doesn't survive measurement, the repair you were about to write is theater — and the real gap is still hiding where the flag pointed. This is the repair-time twin of SN-0398 (re-measure when lanes disagree): that one settles a disagreement; this one aims the repair.

## 🩷 HUMAN NOTE

Shawn — a lane flagged D34's tests as vacuous, but when the build lane actually re-ran the sabotage battery, every sabotage was caught. The premise was wrong, so fixing "vacuous tests" would have been fixing nothing. The measurement found the actual hole — the adapter had only ever been tested against a fake engine — and that's what got repaired. Lesson banked: re-verify a defect report's premise before building the fix, or you fix the wrong thing with full confidence.

## 🟣 CHILD NOTE

Your friend says your bicycle's brakes don't work. Before you take the whole bike apart, squeeze the brakes yourself — they work fine. But while checking, you notice the chain is actually loose. That's the real problem. Rule: when someone reports a problem, check their claim first with your own test. If their claim is wrong, your fix would be for the wrong problem — and the real problem stays broken.

## 🔵 GRANDMA NOTE

It's like a helper saying the oven is broken. Before you call the repairman, you turn the oven on yourself — it heats up fine. But while you're there, you notice the fridge door doesn't seal. The oven was never the problem; the fridge was. Check the reported problem yourself first, or you'll pay to fix something that was never broken while the real trouble sits quietly next door.

## 🟠 NAYA NOTE

When a defect report lands on my queue — especially a verdict-shaped one like "tests are vacuous" — my first action is not to open the repair file. It is to re-run the exact measurement the report implies: the sabotage battery, the failing run, the reproduction. If the premise doesn't reproduce, I stop: the repair I was about to write has no target. I then ask the measurement where the real gap is, and repair *that*. A repair aimed at an unverified premise is the most expensive kind of theater — it burns the repair, the review, and the merge on a fiction, while the real defect keeps its receipt of "fixed."

## 🟢 MACHINE NOTE

~~~json
{
  "sn": "SN-0977",
  "title": "Re-Measure the Flagged Premise Before Writing the Repair",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-DISCIPLINE"],
  "authority": "distillation tick 2026-10-11 05:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board_comment": "#2175 comment 6108991477 (2026-10-11T12:24:50Z — [NAYA 2 · BUILD LANE] sign-out ~12:25Z, night shift)",
    "flag": "wire lane 12:12Z: D34 (#2217) tests vacuous — build lane owns the repair",
    "measurement": "all 7 core-gate sabotages caught by existing tests — the 'vacuous' premise did not hold",
    "real_gap": "D33 adapter proven only against a fake engine — closed against the real D33 engine (#2212 bytes)",
    "repair": "PR #2217 commit f6de2d34: 2 new tests + 1 docstring paragraph, additive, zero mechanism changes",
    "proof": "89/89 with real D33; 83/83 clean tree; sabotage battery 7/7 core gates caught; remote blobs byte-verified; ref fast-forward verified; full receipt PR #2217 comment 6108989429"
  },
  "rule": "flagged_premise_is_the_first_thing_to_test",
  "procedure": [
    "on receiving a defect report, re-run the measurement the report implies before writing any repair",
    "if the premise does not reproduce, do not repair — the repair has no target",
    "let the measurement locate the real gap; repair that instead",
    "a repair aimed at an unverified premise fixes the wrong thing while the real defect keeps a 'fixed' receipt"
  ],
  "related": ["SN-0398 (stale-state claims die on live bytes — the disagreement twin)", "SN-0976 (empty parse fails loud — the fail-closed family)"]
}
~~~
