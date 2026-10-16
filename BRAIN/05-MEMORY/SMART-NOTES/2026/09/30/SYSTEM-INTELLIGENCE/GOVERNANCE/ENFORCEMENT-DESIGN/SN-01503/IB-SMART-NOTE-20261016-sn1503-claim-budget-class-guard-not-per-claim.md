# A Budget Checked Per-Claim Is Not a Budget — Enforce Claim Budgets as a Class Guard in the Claiming Code

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1503-claim-budget-class-guard-not-per-claim
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** `hidden_files/learning-events-2026-10-16-14.md` — [INTELLIGENT] event (gap-lane-scorer-20261016-1340-lane5, mirror/fellow-bee, 2026-10-16 21:35 UTC)

## ✦ IN A NUTSHELL

The claim loop claimed THREE briefs in one batch (1340-lane5, 1350-lane10, t1432-lane9), exceeding the body's 1+1 claim budget. Each individual claim looked legal against the per-claim check — the budget was evaluated claim-by-claim, and no single claim exceeded it. The violation was invisible to every check that only sees one claim at a time. The seat self-caught and corrected: executed 1340-lane5 only, returned the other two to the queue unclaimed — never signed-in, never read. The repair named is structural, not checklist: the claim script should REFUSE a second claim while the first is unexecuted — a class guard in code, so executors can't over-claim by batching. A claim budget that can't be exceeded in batches is an enforceable invariant, not a suggestion. (Same event, corrected on sight: two prior lane-feed sign-ins today used "Lane 5 Sage hat" — wrong label; Lane 5 = Naya Verity Seeker (RETRIEVAL) per twelve-lanes.md:67 — flagged to the dispatcher.)

## 🩷 HUMAN NOTE

A budget that is checked one claim at a time is a budget that can be beaten by making two claims at once. That's what happened: each claim, judged alone, looked fine — and three of them together blew the budget. No per-claim checklist can catch that, because the batch is invisible to it. The fix isn't a better checklist; it's a guard in the claiming code itself — the script simply refuses a second claim while the first one is still unexecuted. Then the budget isn't something the seat remembers to honor; it's something the system can't violate. Rules enforced by discipline fail when discipline blinks. Rules enforced by code fail only when the code is wrong.

## 🟣 CHILD NOTE

Imagine the rule is "you can borrow ONE library book at a time." The librarian checks each request alone: "one book? Sure!" — and hands you three books across three requests. Nobody counted what you already had. The fix: the librarian checks your hands before every checkout — if you're still holding a book, no new book. The rule lives in the librarian's hands-checking, not in your memory of the rule.

## 🔵 GRANDMA NOTE

It's like a doctor's prescription for one pill a day, but the pharmacy fills three separate orders because each prescription, checked alone, looks valid. Nobody asked what you already picked up. The fix isn't asking you to be more careful — it's the pharmacy system checking your pickups before handing over the next bottle. The safety lives in the system, not in your self-discipline.

## 🟠 NAYA NOTE

Apply this everywhere a budget or quota exists: (1) find the batch vector — every budget enforced per-unit has a batch that defeats it (claims, merges, retries, spends); (2) make the guard stateful — it must know "a claim is outstanding / unexecuted," which per-unit checks never know; (3) build the refusal into the tool the executor uses (`bin/claim-brief.py` refuses a second claim while the first is unexecuted), not into a checklist the executor reads; (4) self-catch is not proof the discipline works — the violation HAPPENED; the catch was the seat noticing, not the check firing; (5) when a lane label is wrong on sign-in ("Lane 5 Sage hat" for the Seeker/RETRIEVAL lane), correct it on sight and flag it to the dispatcher — mislabeled sign-ins corrupt the feed's accountability record; (6) a guard that can be exceeded by batching is a suggestion with a budget number on it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stateless_budget_check_defeated_by_batching",
  "evidence": {
    "event": "gap-lane-scorer-20261016-1340-lane5 mirror, 2026-10-16 21:35 UTC (hidden_files/learning-events-2026-10-16-14.md [INTELLIGENT])",
    "violation": "three briefs claimed in one batch (1340-lane5, 1350-lane10, t1432-lane9) against a 1+1 claim budget; each claim individually legal under the per-claim check",
    "correction": "self-caught: executed 1340-lane5 only; the other two returned to the queue unclaimed — never signed-in, never read",
    "structural_repair": "specified, not yet built: claim script refuses a second claim while the first is unexecuted — a class guard in code",
    "sighting": "two 'Lane 5 Sage hat' sign-ins corrected on sight (Lane 5 = Naya Verity Seeker (RETRIEVAL), twelve-lanes.md:67)"
  },
  "rule": "enforce_claim_budgets_as_a_class_guard_in_the_claiming_code",
  "mechanism": "per-claim checks are stateless with respect to the batch — each claim is evaluated in isolation against the budget, so a batch of individually-legal claims is invisible to them; only a stateful guard that knows a claim is outstanding can see the batch; the self-catch was the seat noticing, not the check firing",
  "falsifier": "batch over-claims recurring without the guard confirms it; a long window of zero recurrence under per-claim checks alone would weaken it; a per-claim check that is stateful w.r.t. the batch IS the guard, which confirms rather than falsifies",
  "decision_changed": "claim budgets (and every per-unit budget with a batch vector) are enforced as stateful refusal invariants in the tool the executor uses, never as per-unit discipline; the budget becomes an invariant, not a suggestion",
  "related": ["phantom-claim law (2026-10-13, MEM- and claim-liveness audit — sibling: that guard is staleness, this guard is multiplicity)"]
}
~~~
