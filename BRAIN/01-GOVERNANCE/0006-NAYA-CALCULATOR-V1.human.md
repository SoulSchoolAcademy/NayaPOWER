# The Naya Calculator V1

*For Shawn — in plain words.*

## What this is

Right now, scorecards are something we *write*. A Naya looks at a piece of work, thinks hard, and produces scores. That's good — but it's judgment, and judgment varies from seat to seat, day to day.

The Calculator is the machine that turns scoring into **math**. You feed it any output — a design, a Smart App, a decision, a report, anything — and it scores it against an encoded rubric and returns a reproducible assessment. Same input, same rubric, same score. Every time. No judgment calls, no vibes, no "it feels like an 8."

## Why it matters

Your Scorecard Law says score everything. But if every seat scores by feel, we get twelve different answers for the same work. The Calculator is how the law becomes a machine: **one instrument, one math, one answer**.

It's also the engine inside your bigger vision:

- **Smart Apps** get assembled from Smart Blocks — then the Calculator scores the assembly against the quality rubric. Below 9? It doesn't ship. That's the "system won't let you produce less" you talked about.
- **Smart Stats** gets its intelligence scored the same way — the number is computed, not guessed.
- Every output the team produces carries a machine-computed score. Your 9.0 bar stops being something people try to meet and becomes something the system *enforces*.

## How it works — the short version

1. **You give it three things:** the thing to score, which rubric to score it against (pinned to a version), and the context (who's asking, why, what evidence backs it).
2. **It runs the math:** each rubric dimension gets a score from 0 to 10, weighted by importance, aggregated into one number. The value function runs too — PV tells you above or below the line, S tells you where against the 9.0 bar.
3. **It returns an assessment** that always contains four things: the scores (with the evidence that produced each), the miss named (what's weakest), the corrective action (what would fix it), and the re-score scheduled (when it gets measured again). A scorecard that doesn't name the miss and schedule the re-score isn't closed — that's your Loop law, enforced by the machine.
4. **It's reproducible by construction:** the assessment is a pure function of the input content, the rubric version, and the context. Same inputs, same output. Always. If two runs disagree, one of the inputs changed — and the machine can tell you which.

## What it's not

- **It's not a judge.** It doesn't decide what's good. *You* (and the rubrics you ratify) decide what good is. The Calculator just measures against your standard, mechanically, every time.
- **It's not the Scorecard Law.** The Law is supreme — it says score everything, through five steps, with gates no score can override. The Calculator is the machine that *runs step two* (the scoring). The Law stays above it.
- **It's not Naya 5's Design Calculator.** That's a design instrument — it scores HTML against the design standard. It's excellent, and it becomes one of the Calculator's domain rubrics. The Calculator is the universal machine that hosts it.
- **It's not the V2.1 Decision Value Calculus.** That calculus scores *decisions* (act, read more, ask, refuse). The Calculator scores *outputs* — any artifact, any work product. They share the same value function math; they answer different questions.

## How it becomes enforced (not just documented)

A spec on paper is a wish. The Calculator becomes real in stages:

1. **Spec** (this document) — the contract, ratified.
2. **Reference implementation** — a single Python module (`tools/naya_calculator.py`) that implements the spec exactly. Spec and implementation byte-agree or the implementation is wrong.
3. **Report-only wiring** — it runs in CI and on demand, scores inform, never block. This is how Naya 5's Design Calculator shipped: trustworthy first, authoritative later.
4. **Gate wiring** — scores become preconditions: merges below the floor don't merge, Smart App assemblies below 9 don't publish, the Score stage of the app-creation pipeline runs the Calculator by default.

Each stage is its own decision, its own scorecard, its own receipt. We don't jump to enforcement — we earn it.

## What you decide

- **Ratify this spec** (or amend it) — it's CANDIDATE until you say otherwise.
- **Ratify the first rubrics** — the ten-area scorecard as a rubric, the design rubric, the decision rubric. The machine is only as good as the rubrics you bless.
- **Set the enforcement stages** — when report-only becomes gating is your call, per stage.

## The one-line version

The Calculator is the machine that makes "score everything" computable: any output in, a reproducible, evidence-bound assessment out — with the miss named, the fix recorded, and the re-score scheduled, every time.
