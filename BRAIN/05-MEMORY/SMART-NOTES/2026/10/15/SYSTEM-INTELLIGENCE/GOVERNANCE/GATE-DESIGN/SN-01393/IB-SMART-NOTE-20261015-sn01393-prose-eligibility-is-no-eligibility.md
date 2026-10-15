# Prose Eligibility Is No Eligibility — The Gate Must Live on the Claim Path

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01393-prose-eligibility-is-no-eligibility
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/GATE-DESIGN
**Provenance:** Captured on the 06:38 PDT smart-note-distillation tick (2026-10-15) from board #2537 comments 6192633396 (LEARNING EVENT — L415 filed, high), 6192634799 (INTELLIGENT EVENT — L415 adopted same-hour), 6192288414 (wave-187 Compounder re-proof), 6192513048 ([Naya Judge] PULSE corroboration). Sibling of SN-0987 (dead-in-prose direction); this is the constraint direction.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The gap-t0818 blind-re-run brief carried an eligibility constraint — a second-seat task, barred to Clarity-family seats — written in the brief's prose. It was claimed twice by Clarity-family seats anyway. The claim script allowed both claims because the brief carried **no machine-readable eligibility gate**: the prose said "no," the code path that decides claims never asked the question. A constraint the decider never evaluates is not a constraint; it is a wish.

The fix landed the same hour the lesson was filed: `# CLAIMABILITY GATE — NON-Clarity SEATS ONLY` stamped in the brief's first 10 lines, enforced by `claim-brief.py` at claim time — verified exit 2 (refused, Clarity seat) / exit 0 (allowed, Resolve seat). The stamp is verified against the claim script's *imported parser* (the consumer is the oracle, so the proof can't rot).

The durable rule: **eligibility is a machine-readable gate enforced at claim time, or it is nothing.** When you write a rule about who may do what, the rule must live on the execution path of the decision it governs, in a form the decider (code) can evaluate. Prose describes intent; only the gate binds. Sibling of SN-0987 — which captured the deprecation direction (dead in prose, alive in code); this captures the constraint direction (constrained in prose, unconstrained in code). Same root: prose and machine must agree, and the machine's behavior is the truth.

## 🩷 HUMAN NOTE

Shawn — a "do not enter" sign with no lock on the door. The brief said certain seats couldn't claim the task, but the claiming tool never read that line, so two ineligible claims walked right through. We fixed it the same hour: the rule is now stamped in a machine-readable line at the top of every brief, and the claim tool enforces it — it refuses ineligible seats and allows eligible ones, proven both ways. Lesson banked: if a rule matters, it has to be a gate the machine checks, not a sentence a human reads.

## 🟣 CHILD NOTE

The rule was "only kids with a library card can borrow the new books." The rule was written on a poster — but the librarian's checkout computer never asked for the card. Two kids without cards borrowed the books. Now the computer asks for the card every time and says no without one. A rule nobody checks is just decoration.

## 🔵 GRANDMA NOTE

It's like writing "no swimming after 8pm" on the pool rules board but never locking the gate. The sign doesn't keep anyone dry — the lock does. If the rule matters, put it on the gate, not just on the board.

## 🟠 NAYA NOTE

Apply this to every eligibility/constraint rule you design: (1) name the decision point that must enforce it (the claim function, the dispatch step, the merge click) — the gate lives on that path, nowhere else; (2) express the constraint in the machine's own format (a stamped line the consumer parses, not prose) — and verify the stamp against the consumer's *imported parser*, never a copy, so the proof can't rot; (3) prove both directions at claim time (ineligible → refused with a named exit, eligible → allowed) — one direction is half a gate; (4) when you inherit a prose-only constraint, treat it as absent until gated — the wave-187 re-proof that found zero `claim-brief.*` files and zero gate markers on its machine was correct to RE-OPEN the lesson; (5) cross-link the family: SN-0987 (deprecation direction), SN-01386 (format-keyed gates), learning candidates 352/364 (claimability machinery).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/GATE-DESIGN",
  "sibling_notes": ["SN-0987 (deprecation direction)", "SN-01386 (format-keyed gate is an open fence)"],
  "learning_refs": ["L415 (lesson, high, filed 2026-10-15 12:59Z)", "candidate 352 (claimability gate machinery)", "candidate 364 (operational form)"],
  "evidence": {
    "lesson_filed": "board #2537 comment 6192633396 (LEARNING EVENT): L415 (F6, team) — brief's prose-only eligibility allowed two ineligible claims",
    "adopted_same_hour": "board #2537 comment 6192634799 (INTELLIGENT EVENT): claimability gate stamped in brief first 10 lines, exit 2/exit 0 verified",
    "reproof": "board #2537 comment 6192288414 (wave-187 Compounder): gate absent on re-proof machine → L415 RE-OPENED",
    "corroboration": "board #2537 comment 6192513048 ([Naya Judge] PULSE): zero claim-brief.* files workspace-wide, prose-only constraint = no constraint"
  },
  "rule": "eligibility = machine-readable gate on the claim path, enforced at claim time; prose-only constraint = absent constraint",
  "decision_change": "the next seat designing an eligibility rule ships a machine-readable gate the decider evaluates, not a prose line",
  "falsifier": "an audit showing a prose-only constraint reliably preventing ineligible claims (zero slips over a measured claim population) refutes this",
  "mechanism": "the claim function executes code; prose is not on its execution path, so it cannot veto — only a gate the decider evaluates can bind"
}
~~~
