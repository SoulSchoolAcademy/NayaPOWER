# Stop Only When the Contract Closes — Iteration Law

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0153-iteration-law-contract-closure
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5945155880 §8 (TEAM NAYA — ACTIVE INTELLIGENCE INTERFACE PROGRAM V1, 2026-10-02T03:37:49Z) — "There is no magic count. 10 rounds may be enough. 198 rounds may be required. Stop only when the contract closes. Every iteration must answer: What exact gap did we remove? What evidence improved? What remained unchanged? Change one major variable at a time when learning from visual iterations." Room loop context: research → spec → visual → do/don't sweep → scorecard (9.0 bar) → lock (5945120603).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Fixed iteration budgets are a promise the domain can't keep — 10 rounds of a converged loop beat 198 rounds of thrash. The stop condition is **contract closure** (the acceptance predicates in the freeze package all pass), not a count. Every iteration must leave a delta ledger: what exact gap did we remove? what evidence improved? what remained unchanged? And when learning from iterations, change **one major variable at a time** — otherwise an improvement can't be attributed to anything. Cousin map: SN-059 (attribute the failure before blaming the change — control runs in diagnosis); this note is the improvement-side twin (attribution in learning iterations). SN-032 (finite work-list / loop-exhaustion) governs exhausting a known work list; this note governs *open* iteration where the work list is unknown. A round that cannot state its gap-removal is not an iteration — it's motion.

## 🩷 HUMAN NOTE

Imagine training for a marathon with the rule "run exactly 50 sessions, then you're ready." Fifty sessions of wandering won't ready you; ten sessions with a plan might. The team learned the same about building rooms: there's no magic number of rounds. Some rooms need 10 rounds, some need 198. What ends the work is the contract closing — every acceptance predicate passing. And every round has to answer three questions: what gap did we remove, what evidence got better, what stayed the same? Change one big thing at a time, or you can't learn which change did the work. A round that can't answer "what gap did I remove" isn't an iteration — it's just motion.

## 🟣 CHILD NOTE

Imagine you're trying to build the tallest LEGO tower. You could say "I'll try 100 times!" — but that doesn't help. What helps is: each try, change only ONE thing (a wider base, taller bricks, different order) and write down what happened. Then you know *which* change made it taller. The team's rule for building rooms: keep going until the checklist is fully done (that's the contract closing), not until you've tried some magic number of times — and every try, write down what you changed and what improved. One big change at a time, or you can't learn.

## 🔵 GRANDMA NOTE

It's like perfecting a family recipe. Nobody says "cook it exactly twelve times and it'll be right." You cook it until it's right — and each time, you change one thing: a little more salt, a longer simmer, a different pan. If you change the salt *and* the pan *and* the heat all at once, and it tastes better, you haven't learned anything — you don't know which change mattered. The team's rooms are the same: iterate until the contract (the full checklist) closes, change one major variable per round, and write down what moved and what didn't. That's how ten rounds can beat a hundred.

## 🟠 NAYA NOTE

Apply this to every build loop (room blueprints tonight, kernels tomorrow): (1) stop condition = contract closure — the freeze package's acceptance predicates all pass — never a round count; (2) every iteration leaves a delta ledger answering the three questions (gap removed / evidence improved / unchanged) — no ledger, no iteration credit; (3) change one major variable at a time when learning from iterations, or improvements are unattributable (improvement-side twin of SN-059); (4) SN-032's loop-exhaustion discipline applies to known work lists; this law applies to open iteration where the work list is unknown; (5) the room loop shape (research → spec → visual → do/don't sweep → scorecard at the 9.0 bar → lock) is the *track*; this law is the *pace rule* on the track; (6) escalate a loop that keeps churning past ~10 rounds without the contract closing: re-examine the contract itself — a contract that never closes may be the wrong contract.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "budget-count iteration (fixed round count as stop condition; multi-variable changes unattributable)",
  "evidence": {
    "board": "#554 5945155880 §8 (2026-10-02T03:37:49Z) — 'There is no magic count. 10 rounds may be enough. 198 rounds may be required. Stop only when the contract closes. Every iteration must answer: What exact gap did we remove? What evidence improved? What remained unchanged? Change one major variable at a time when learning from visual iterations.' Room loop shape (research -> spec -> visual -> do/don't sweep -> scorecard (9.0 bar) -> lock) from #554 5945120603 (2026-10-02T03:33:44Z)."
  },
  "rule": [
    "stop condition is contract closure (freeze package acceptance predicates all pass), never a round count",
    "every iteration leaves a delta ledger: gap removed / evidence improved / unchanged",
    "change one major variable at a time when learning from iterations; multi-variable rounds produce unattributable improvements",
    "a round that cannot state its gap-removal is motion, not an iteration",
    "loops churning past ~10 rounds without contract closure trigger contract re-examination, not more rounds"
  ],
  "lesson_line": "There is no magic count of rounds: iterate until the contract closes, change one major variable per round so improvements are attributable, and write the delta ledger every time — a round that cannot name its gap-removal is motion, not an iteration."
}
~~~
