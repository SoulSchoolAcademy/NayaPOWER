# Verify the Gate's Teeth Before Designing Around It

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0371-verify-gates-teeth-before-designing-around
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5999056032 ([REVIEW VERDICT] Naya 4 builder-lane review of Naya 2's atomic promotion spec, 2026-10-05T16:53:15Z / 09:53 PDT). Verdict: ADOPT the design (8-step sequence — authorize → freeze → validate → deploy → verify → confirm → pointer LAST → receipt; steps 1–6 preparation, step 7 atomic commit point; failure semantics correct), but IMPLEMENTATION BLOCKED on one investigated unknown. Related: SN-0363 (the adopted pointer-moves-last spec), SN-0352 (pointer gated on checks green).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The spec's steps 4–5 required a real Supabase validation BEFORE the production pointer moves. Given the branch-based deploy mechanism, that means pushing the deployment commit to a staging branch and waiting for the Supabase check there. Before building anything, the reviewer sampled the actual mechanism on live state: 4 PR-head commits (`1c27d0bd`, `16317092`, `9b06c819`, `cc04e3d6`) → the "Supabase Preview" check posts on every PR branch but concludes **skipped** 4/4. So a staging-branch pre-validation would time out fail-closed (15 min) on every run — safe, but the promotion would never complete. That is a functional regression wearing a safety costume, not a fix. The reviewer wrote "I will not build it" — and was right.

Two durable rules:

**1. Test the teeth of any mechanism your design depends on, before adopting the design.** The spec was sound on paper; the mechanism it depended on never actually runs. Sampling four real commits took minutes and killed the design's critical dependency with facts instead of allowing a month of work built on an assumption. A gate you have not observed completing is not a gate — it is a rumor of a gate. SN-0341's lesson ("the instrument lies — audit the measurement instrument before patching the subject") generalizes: audit the *gate* before depending on it.

**2. When the strong design is blocked, offer the honest weaker interim — and never present it as the spec.** The available honest interim: keep the current push-then-check order, add automatic pointer REVERT on check failure + receipt. It handles validation-failures (the observed class — Supabase rejects, nothing bad goes live) but not deploy-then-fail cases. It is NOT atomic; do not call it Naya 2's spec. The failure to label the interim honestly is how a non-atomic revert becomes folklore as "the atomic promotion" and then somebody depends on it as atomic. Names carry proof claims; misnaming transfers unearned confidence.

The precise ask that follows is mechanical, not heroic: whoever holds the Supabase dashboard answers one question — can the GitHub Integration be configured to execute (not skip) preview checks for a non-production branch? Yes → implement the atomic reorder as a PR. No → design an alternative validation path. The review turned an unbounded build into one yes/no question. That is what a good review verdict buys: the decision, not more design.

Why this is brain-grade: a cold Naya will adopt beautiful specs that depend on mechanisms nobody has watched run. This note teaches the two-line check — sample the real behavior of every mechanism in your dependency chain, in the exact configuration the design needs — and the honesty discipline for blocked strong designs: ship the labeled weaker version, never rename it upward.

## 🩷 HUMAN NOTE

Shawn — one clean review verdict on the atomic-promotion spec today. The design is sound (pointer moves last, steps 1–6 are preparation, step 7 is the atomic commit), but I checked the mechanism it depends on: sampled four real PR commits and the Supabase Preview check concludes "skipped" 4/4 — it never actually validates branch commits. So staging-branch pre-validation would just time out every run: safe, but promotions would never complete. The strong design is blocked on one yes/no question for whoever holds the Supabase dashboard — can the integration be configured to actually execute preview checks for a non-production branch? If yes, the atomic reorder builds cleanly. If no, we design a different validation path. The honest interim (automatic pointer revert on check failure) handles the validation-failure class but is not atomic, and I'm not presenting it as if it were. No code written, nothing to review — and that's the correct outcome.

## 🟣 CHILD NOTE

Imagine you're building a treehouse and the plan says "step 4: test the bridge with a crash-test dummy." But before you build, you check: the crash-test dummy machine has been turned off for months — it never actually tests anything. So you stop. You don't build the whole treehouse pretending the dummy tested it. You write down exactly what you found, and you ask one clear question: can the dummy machine be turned on? If yes, build. If no, find a different way to test. And if you build a weaker version meanwhile, you label it honestly — "this version does NOT have the dummy test" — so nobody pretends it's as safe as the real one.

## 👵 GRANDMA NOTE

It's like a recipe that says "bake until the oven timer rings." Before cooking for a hundred guests, you check: the oven timer is broken — it never rings. You don't bake a hundred meals on a promise that can't fire. You find that out in minutes by testing the timer itself. Then the fix is one simple question to the person who can repair it. And if you serve a simpler dish meanwhile, you call it what it is — you don't serve the simpler dish and call it the grand recipe. Check the mechanism, label the interim honestly.

## 💜 NAYA NOTE

Note to future me: adopting a spec is not the same as being able to implement it. The review checklist for any design that depends on a gate or check: (1) sample the gate's real behavior on live state in the exact configuration the design needs (here: 4 PR heads → Supabase Preview concludes skipped 4/4); (2) if it never fires, the design's dependency is dead — say "I will not build it," with the evidence; (3) turn the block into the smallest possible yes/no ask with a named owner; (4) if an interim exists, describe its exact failure-class coverage and its honest name — never let a non-atomic revert be cited as the atomic design. Cite SN-0363 for the spec, SN-0352 for the enforcement direction; this note is the review-side companion: verify teeth, label interims.

## ⚙️ MACHINE NOTE

{"sn": "SN-0371", "title": "Verify the Gate's Teeth Before Designing Around It", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "PROMOTION-AUTHORITY-BINDING"], "extends": ["SN-0363"], "related": ["SN-0352", "SN-0341"], "evidence": {"board": "#1354 5999056032 ([REVIEW VERDICT], 2026-10-05T16:53:15Z): atomic promotion spec ADOPTED (8-step sequence, pointer LAST, step 7 atomic commit point, failure semantics correct); IMPLEMENTATION BLOCKED — steps 4-5 need real Supabase validation before pointer moves; sampled 4 PR-head commits (1c27d0bd, 16317092, 9b06c819, cc04e3d6) -> 'Supabase Preview' check concludes skipped 4/4 -> staging-branch pre-validation would time out fail-closed (15 min) every run: functional regression, not a fix; reviewer: 'I will not build it'; paths: (1) fix preview config via Supabase dashboard access -> atomic reorder implements cleanly; (2) interim: pointer REVERT on check failure + receipt — not atomic, do not present as the spec", "design_spec": "SN-0363 / #1354 5998365567"}, "rule": "before adopting a design that depends on a gate, sample the gate's actual behavior on live state in the exact configuration the design needs — a fail-closed gate that can never complete is a functional regression, not a fix; when the strong design is blocked, offer the honest weaker interim with its exact failure-class coverage and never present it as the spec"}
