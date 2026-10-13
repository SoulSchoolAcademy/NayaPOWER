# Seal the Acceptance Rule Before the Run; Freeze the Honest Miss as Ground Truth

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1099-seal-before-run-freeze-the-miss
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 (2026-10-12 — lesson-broadcast t0402 Naya Sage, t0442 Naya Seeker sealed entailment-rerank run, t0452 Naya Seeker study-protocol + F3 tripwire; `hidden_files/auto-retrieval/study-protocol-t0452.md`, `sealed-note-t0442.md`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three slices, one protocol. t0402 (Naya Sage): when your instrument fails on its own brief, that failure IS the next slice's test — **freeze the honest miss as ground truth BEFORE you judge or tune**, and test against it. t0442 (Naya Seeker): the entailment-rerank arm was falsified in a sealed run, one shot — formal NLI entailment demoted the human's #1 pick from rank #1 to #10, and the verdict stood because the acceptance rule was sealed before the run; no rescuing, no re-tuning. t0452 (Naya Seeker): the F3 lexical-independence tripwire (TF-IDF baseline agreement <5/6 cells, else it's a semantic proxy under a new name) was sealed BEFORE the run — protocol plus a hand-run worked example with 3 protocol bugs caught. The durable rule has two halves: **seal the acceptance rule before the run** (so a failure can't be redefined into a pass), and **freeze the honest miss as ground truth after the run** (so the failure becomes the next slice's test instead of being tuned away). Self-adversarial testing ships with the prototype, not after.

Why this is brain-grade: unsealed acceptance criteria drift toward the result you wanted; unfrozen misses get re-explained instead of re-tested. The t0412 lexical-rubric kill worked because the frozen fixture couldn't be negotiated with; the t0442 entailment kill worked because the sealed run allowed exactly one shot. This is the experimental half of proof-honesty: verdicts are trustworthy only when the rule predates the run and the miss outlives the run.

## 🩷 HUMAN NOTE

Shawn — experimental-discipline lesson from the retrieval work: the team is now running falsification like a lab. The rule they proved this week has two halves — write down exactly what counts as pass/fail BEFORE the experiment (sealed, no renegotiating after), and when something fails honestly, freeze that failure as the ground truth the next attempt must beat (no tuning it away). The entailment-rerank idea died cleanly in one sealed run because the rules were locked first. That's the standard now: seal before, freeze after.

## 🟣 CHILD NOTE

Imagine you're testing whether your new kite design flies. The fair way has two rules. First, BEFORE you fly it, you write down: "it flies if it stays up for one whole minute" — and you're not allowed to change it to "okay, ten seconds counts" after it falls down. Second, when it crashes, you keep the broken pieces and the exact wind conditions written down — that's what the next design has to beat. Rules locked before, wreckage kept after. That's how you actually learn instead of just cheering for your own kite.

## 👵 GRANDMA NOTE

When you're testing something properly, you do two things the team just formalized. First, you decide what "good enough" means before you start — written down, no moving the goalposts after you see the result. Second, when it fails, you keep the failure on record exactly as it happened — that's the bar the next try has to clear, not something to quietly smooth over. Decide the rules first, keep the honest failures. Anything else is just telling yourself stories.

## 💜 NAYA NOTE

Note to future me: for any falsification run — mine or a lane's — require both halves. BEFORE: the acceptance rule is sealed (written, with the tripwire thresholds, e.g. the F3 lexical-independence <5/6 rule) and the run is one-shot; no re-tuning mid-run, no redefining pass after the numbers land. AFTER: the honest miss is frozen as ground truth (sealed note + results file) BEFORE anyone judges or tunes; the next slice's test is the frozen miss, and self-adversarial testing ships with the prototype, not after. If a lane reports a kill without a sealed pre-rule, the kill is a story; if it reports a miss it already tuned away, the miss is lost evidence.

## ⚙️ MACHINE NOTE

{"sn": "SN-1099", "title": "Seal the Acceptance Rule Before the Run; Freeze the Honest Miss as Ground Truth", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "PROOF-HONESTY", "FALSIFICATION-PROTOCOL"], "cousins": ["SN-1092", "SN-1094"], "authority": "observed lane practice 2026-10-12, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#2175 lesson-broadcast t0402 Naya Sage (2026-10-12) — 'When your instrument fails on its own brief, that failure IS the next slice's test — freeze the honest miss as ground truth BEFORE you judge or tune, and test against it. Self-adversarial testing ships with the prototype, not after.'", "#2175 lesson-broadcast t0442 Naya Seeker (2026-10-12) — 'The entailment-rerank arm is FALSIFIED (0/3 tasks at HIT@5>=2/3; sealed run, one shot) — formal NLI entailment is NOT the judge's mechanism either; it demoted the human's #1 pick (P2) from bi-encoder rank #1 to #10'", "#2175 lesson-broadcast t0452 Naya Seeker (2026-10-12) — 'Any future retrieval instrument must pass the F3 lexical-independence tripwire (TF-IDF baseline agreement <5/6 cells) or it is a semantic proxy under a new name — the mechanized t0412 rule, sealed BEFORE the run'"], "artifacts": ["hidden_files/auto-retrieval/study-protocol-t0452.md", "hidden_files/auto-retrieval/sealed-note-t0442.md", "hidden_files/auto-retrieval/results-t0442-entailment.json"]}, "doctrine": {"seal_before": "acceptance rule + tripwire thresholds sealed before the run; one shot; no post-hoc redefinition", "freeze_after": "honest miss frozen as ground truth (sealed note + results) before judging or tuning; next slice tests against the frozen miss", "self_adversarial": "self-adversarial testing ships with the prototype, not after"}}
