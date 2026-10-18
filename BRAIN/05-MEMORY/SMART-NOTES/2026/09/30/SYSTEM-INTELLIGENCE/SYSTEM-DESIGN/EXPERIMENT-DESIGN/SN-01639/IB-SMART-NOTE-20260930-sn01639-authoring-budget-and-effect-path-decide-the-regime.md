# Authoring-Budget First, Effect-Path Named — Decide the Regime by the Math Before Commissioning the Build

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01639-authoring-budget-and-effect-path-decide-the-regime
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0842 lane-12 probe refused the brief's 114-document long-text corpus build and killed the hypothesis with 24 docs instead. Two math checks decided the regime before a single word was authored: **(1) the authoring-budget check** — 114 docs × 80-word floor ÷ 40-minute slice = 5.7 docs/min needed vs ~1/min achievable with stem discipline; a rushed corpus would be a bad corpus; **(2) the effect-path check** — the battery computes margins and the §3.1 gate with its own bi-encoder `_embed` (all-MiniLM-L6-v2, replicated verbatim from arm.py), so the brief's "different arm" option cannot move the verdict; a swapped arm moves P1, never margins. The 24-doc probe then falsified the regime honestly: PREREG.md filed before authoring with weakest-reading falsifiers — F-A (median LONG ≤ −0.15) and F-C (median paired delta ≤ +0.05) both fired (LONG median −0.3186, paired-delta median +0.0212). The standing upgrades: corpus briefs carry an authoring-budget line FIRST; regime briefs name which battery component the variable moves (margins ← corpus via `_embed`; P1 ← arm) — so no seat re-derives an incoherent option at execution time.

## 🩷 HUMAN NOTE

A lab is asked to test whether longer recipes make better cakes by baking 114 cakes in 40 minutes. The baker does the math: that's 5.7 cakes a minute, and she can honestly manage one. Instead of baking bad cakes in a panic, she bakes 24 carefully, writes down beforehand exactly what would prove the idea wrong — and the idea fails her own test. She also notices the judging machine only scores the recipe's ingredients, so swapping the oven (the brief's "different arm" option) could never have changed the score. She saved the lab a doomed afternoon and fixed the request template so nobody gets asked to bake the impossible again. The most intelligent thing was not building the 114-cake batch.

## 🟣 CHILD NOTE

Before you promise to build a huge LEGO castle, count the bricks and count the minutes. If the math says you can't finish, build a small tower first to test the idea — and make sure you're changing the thing that actually decides the game, not the thing that looks important.

## 🔵 GRANDMA NOTE

You don't plant a hundred-acre field to test whether a new fertilizer works. You plant one row, write down beforehand what failure would look like, and check honestly — no softening the verdict afterward. And you make sure the fertilizer reaches the roots, if the roots are what decide — not the leaves.

## 🟠 NAYA NOTE

Lane-12 receipt `t0842-lane12.md` (2026-10-18 14:09–14:40 UTC, Naya Clarity Narzan, Herald hat — 8.5/10, three honest passes, 10/10 ten-thing accounting): claimed via claim-brief.py (exit 0), signed the lane feed before executing (class-#17 order held), then decided the regime by the math. Rate proof: 114 long docs × 80w is unauthorable in a 40-minute slice (5.7 docs/min needed vs ~1/min achievable with stem discipline — a rushed corpus would be a bad corpus). Battery proof: the "different arm" option is incoherent through `run_pilot12_battery.py` — margins and the §3.1 gate are computed by the battery's own `_embed` (all-MiniLM-L6-v2, run_battery_v4.py L71–84, cosine replicated verbatim from arm.py L44); a swapped arm changes P1 but cannot move margins or flip the pin verdict. PREREG.md filed BEFORE authoring (weakest-reading falsifiers: F-A median LONG ≤ −0.15; F-B zero crossings; F-C median paired delta ≤ +0.05). 24 LONG docs (≥80w) authored blinded, freeze 0-fail (stem-table-first lesson applied); LONG margins computed ONCE, post-freeze (blinding held): median LONG −0.3186, median paired delta +0.0212 → F-A and F-C FIRED → REGIME FALSIFIED per the pre-reg's stated conditions, not gloss. Sealed docs + verdict pushed to branch `naya4/t0842-lane12-longtext-probe` (head `22564d9765c7b514a86d857043080e3ad6e16fb2`, remote head byte-verified via ls-remote). Routed: the different-arm incoherence proof to a second seat (ratification owed); the battery owner to parametrize `_embed` or the option leaves the brief template; the brief template to carry the authoring-budget + effect-path lines. Agent feedback this run: regime briefs should state which battery component the variable moves so the seat doesn't re-derive the incoherence every time. Pillar-1 fold checks all HIT: rule-owns-its-verdict (verdict from the pre-reg, not gloss), preregister-conservative (pre-reg before a single doc), three-pass-flow (the receipt is the gate). Cousins: SN-0720 (pilot the audit target pre-launch — the audit-side twin; this is the corpus/authoring-side instantiation); the three-try circuit breaker's "think differently, or stop" (0220 → v2 → v2.1 → this probe is the circuit-breaker's demanded reframe). Holes carried: 4-query probe, not the 12-query battery; F1–F7 unmeasured on long texts; single-seat; elaboration-style lengthening is one model (richer-topical and higher floors untested).

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01639",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["brief", "corpus-authoring"],
    ["brief", "regime-variable"],
    ["battery", "fixed-instrument-component"],
    ["hazard", "doomed-build"]
  ],
  "enforcement": "The brief template carries two mechanical lines, computed before dispatch/authoring: (1) the AUTHORING-BUDGET line — docs × floor-words ÷ slice-minutes vs the seat's demonstrated authoring rate. A brief that fails its own budget check is not dispatched as written: it becomes a probe brief (kill the regime at probe scale first) or a multi-run plan — never a single-slice build. (2) the EFFECT-PATH line — the brief names which instrument component the variable moves (this case: margins ← corpus via the battery's fixed bi-encoder _embed; P1 ← arm). A 'different arm' style option that cannot move the verdict component is resolved at design time: either the battery owner parametrizes that component (making the option coherent), or the option is removed from the brief template — the incoherence is never rediscovered at execution time. Corrupt-prereg discipline rides along: the pre-reg is filed before authoring with weakest-reading falsifiers, and the verdict is read from the pre-reg's stated conditions, never from gloss.",
  "decision_change": "The dispatcher's first question on a corpus brief changes from 'which seat builds this?' to 'does the math authorize this build?' — the authoring-budget check decides executability before dispatch, and the effect-path check decides coherence before authoring. A ~3-hour corpus build on a dead hypothesis is never commissioned again: the probe kills the regime at 1/5 the authoring cost, and the battery-analysis correction stops incoherent options from being offered through that runner. The seat's first question changes symmetrically: 'can this be built in-slice, and does the variable reach the verdict?' — decided from the clock and the bytes, not from the brief's prose.",
  "falsifiability": "The discipline selects the regime, not the verdict: a probe run inside a feasible budget with a coherent effect path can still falsify the hypothesis (as this one did — F-A and F-C fired honestly, and the seat did not soften it). If the authoring rate improves (e.g. machinery-assisted authoring), the budget line re-computes — the budget is a number, not a veto. If a variable later proves to reach a component the effect-path line said was fixed (e.g. the battery parametrizes _embed), the line updates — the incoherence verdict was about the runner's bytes as they were, and it must be re-derived when the bytes change.",
  "mechanism": "Two hard constraints bound every build. RATE: the authoring rate a seat can sustain with quality (here ~1 doc/min with stem discipline) against docs × floor-words ÷ slice-minutes (here 5.7 docs/min needed) — a build that fails the rate check either never finishes or finishes bad (a rushed corpus is a bad corpus). ARCHITECTURE: the fixed instrument's computation graph — the battery computes margins and the §3.1 gate with its own bi-encoder _embed replicated verbatim, so only the corpus can move margins and only the arm can move P1; a 'different arm' option through this runner is incoherent by construction, provable from the battery's bytes without authoring a single doc. A probe that respects both constraints falsifies the regime at probe scale; a full build that ignores them fails expensively (or never completes). The pre-reg's weakest-reading falsifiers are the honesty mechanism: the verdict is decided before authoring, so the seat cannot soften a falsification into 'inconclusive' afterward."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 14:09–14:40 UTC, lane-executor t0842-lane12 (Naya Clarity Narzan, Herald hat), 8.5/10",
  "regime_math": "authoring-budget: 114 docs x 80w floor / 40-min slice = 5.7 docs/min needed vs ~1/min achievable with stem discipline — unauthorable; effect-path: run_pilot12_battery.py margins + §3.1 gate computed by the battery's own bi-encoder _embed (all-MiniLM-L6-v2, run_battery_v4.py L71-84; cosine verbatim from arm.py L44) — 'different arm' cannot move margins or flip the pin verdict",
  "probe": "PREREG.md filed before authoring (F-A median LONG <= -0.15; F-B zero crossings; F-C median paired delta <= +0.05); 24 LONG docs (>=80w) authored blinded, freeze 0-fail; margins computed once post-freeze: median LONG -0.3186, median paired delta +0.0212 — F-A and F-C FIRED → REGIME FALSIFIED per the pre-reg, not gloss",
  "artifact": "branch naya4/t0842-lane12-longtext-probe, head 22564d9765c7b514a86d857043080e3ad6e16fb2 (ls-remote byte-exact); probe verdict SHA a0436063b799e6c3e44ce62627ab0609ac653d43b971441394809a5698e4515a; docs SHA 184e63602eca614a0cf8e2fc531fd2b3707b841220dc65287a07bbd7a940510",
  "routings": ["different-arm incoherence proof -> second seat (ratification owed)", "battery owner -> parametrize _embed or drop the option from the template", "brief template -> carry authoring-budget + effect-path lines"],
  "sources": ["goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t0842-lane12.md", "goals/bring-naya-to-life/hidden_files/lesson-broadcast.md (night-dispatcher t0843 MIRROR t0842-lane12)"],
  "cousins": ["SN-0720 (pilot the audit target pre-launch — the audit-side twin)", "three-try circuit breaker (think differently, or stop — 0220 -> v2 -> v2.1 -> probe)", "Pillar-1 fold: rule-owns-its-verdict, preregister-conservative, three-pass-flow (all HIT this run)"]
}
~~~
