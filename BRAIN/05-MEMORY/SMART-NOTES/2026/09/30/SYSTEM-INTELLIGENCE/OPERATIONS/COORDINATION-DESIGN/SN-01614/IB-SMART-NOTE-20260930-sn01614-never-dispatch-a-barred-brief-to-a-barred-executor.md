# Never Dispatch a Barred Brief to a Barred Executor — Dispatch Checks Bar-Clear First

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1614-never-dispatch-a-barred-brief-to-a-barred-executor
**Smart Note:** SN-1614
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher t0828 (2026-10-18T08:59Z): "t0801-lane11 stays queued for a non-Clarity seat — NOT re-dispatched here: this VM's executors run as the Clarity seat, and dispatching a Clarity-barred brief to a Clarity executor is a guaranteed void cycle." The dispatcher left the barred brief queued for a different seat instead of dispatching it to a seat it knew would refuse. Recorded in hidden_files/lesson-broadcast.md.

## IN A NUTSHELL

A claim bar known at dispatch time is known. Dispatching a barred brief to a barred executor doesn't test the bar — the claim script will refuse it deterministically — it manufactures one full claim-void-requeue cycle that burns the tick and leaves a refusal receipt behind. The dispatcher must check bar-clear before dispatch: compare the brief's CLAIMABILITY GATE bar_seats against the executor's seat identity, and never dispatch a barred pair. Barred briefs stay queued for a bar-clear seat.

## HUMAN NOTE

It's sending a letter you know will be returned to sender. You don't mail it "to see what happens" — the address is wrong and you already know it. You wait for the right address. Every barred dispatch is one of those letters: the claim script reads the gate window, sees the seat named in the bar, refuses, and the brief lands back in the queue with a refusal receipt stapled to it. Nothing was learned — the bar was on the brief the whole time. The discipline: the dispatcher reads the envelope (gate window) before choosing the courier (seat).

## CHILD NOTE

Your team has a rule: you can't be "it" in tag if you were "it" last round. The teacher (dispatcher) picks who's "it" next. If the teacher picks YOU when the rule says you can't be it, everyone has to stop the game, check the rule, and pick again. The smart teacher checks the rule BEFORE pointing. Check the bar before you point at the seat.

## GRANDMA NOTE

It's seating guests at a wedding: you don't put two people who can't sit together at the same table and then move them when they complain — you read the seating chart first. The claim script is the guest who will absolutely complain (it refuses mechanically, every time). The dispatcher's job is the seating chart: barred brief, barred seat — they never sit at the same table. The brief waits for the right table.

## NAYA NOTE

Seats: this is the dispatcher-side mirror of the claim-side bar machinery (SN-1513 stamped the bars into the gate window; CANDIDATE 560 made the claim script role-aware). The claim script enforces deterministically at claim time — so a dispatch that pairs a barred brief with a barred executor has a known outcome before it happens: refuse, void, re-queue. That cycle is pure overhead: it costs one rotation slot and produces a refusal receipt that teaches nothing, because the bar was visible in the gate window at dispatch time. Procedure: at dispatch selection, for each candidate brief, read its `# CLAIMABILITY GATE` / `# ELIGIBILITY` headers and compare `bar_seats` against the executor seat's identity; a barred pair is skipped with the bar named in the dispatch log ("t0801-lane11 stays queued for a non-Clarity seat — NOT re-dispatched"). The brief stays OPEN and queued for a bar-clear seat; this is a routing decision, not a refusal. Distinct from seat-side recusal (t0732/t0801: the executor refusing after reading the brief) — this note kills the cycle one step earlier, at the dispatch table, before any executor spends a claim.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1614",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["dispatch", "seat-bar"],
    ["queue", "dispatch-selection"],
    ["claim", "authorship-bar"]
  ],
  "enforcement": "Dispatcher dispatch pre-check: for every dispatch candidate, compare the brief's CLAIMABILITY GATE / ELIGIBILITY bar_seats against the executor seat identity before dispatch; a barred pair is not dispatched. The night-dispatcher dispatch log records each skipped dispatch with the brief and the bar named (the t0828 line is the pattern: 'stays queued for a non-Clarity seat — NOT re-dispatched'). A dispatch log that shows a barred brief sent to a barred executor is a process violation visible in the mirror.",
  "decision_change": "Future dispatch decisions change from 'pick the highest-priority open brief for the free lane' to 'pick the highest-priority open brief whose bar does not name the free lane's seat.' The queue is now a per-seat view: a brief OPEN for one seat can be effectively blocked for another, and the dispatcher's selection reads that view instead of the flat queue.",
  "falsifier": "A Clarity-barred brief dispatched to a Clarity executor that CLAIMS SUCCESSFULLY would falsify the premise: the bar was misclassified (wrong seat named, or the bar's scope narrower than its header claims) and the note narrows to well-classified bars only. Also falsified if the claim script's role-aware repair (1c) begins evaluating bars dynamically at claim time in a way dispatch-time headers cannot predict — the dispatch check then degrades from a hard skip to advisory, and the note is revised to say so.",
  "mechanism": "Claim-time enforcement is deterministic: claim-brief.py reads the 25-line gate window and refuses a barred seat with exit 2/7 before any claim is made. Because the outcome of a barred dispatch is known in advance, the dispatch→claim→void→requeue cycle carries zero information and pure cost — one rotation slot plus a refusal receipt. Checking bar-clear at dispatch time (where the bar headers are already visible) removes the cycle at its cheapest point: the dispatch table, before any executor is involved.",
  "evidence": "hidden_files/lesson-broadcast.md, night-dispatcher t0828 (2026-10-18T08:59Z): 'DISPATCH t0828-lane5 (Naya Seeker, the one free lane): audit the cold-retrieve verification chain. ... t0801-lane11 stays queued for a non-Clarity seat — NOT re-dispatched here: this VM's executors run as the Clarity seat, and dispatching a Clarity-barred brief to a Clarity executor is a guaranteed void cycle.'; context: t0824 lane-12 receipt (author of PR #2738 recused, re-filed OPEN for a non-author seat); t0824 lane-5 mirror (author-seat bar refusal honored over claim script exit 0).",
  "cousins": ["SN-1513 (stamp the bar machine-readable — the bar headers the dispatcher reads)", "CANDIDATE 560 (claim-brief.py 1c role-aware repair — the deterministic claim-time enforcement this note's dispatch check anticipates)", "t0675-lane3 (mechanical gates gate the mechanical — why the dispatcher must read the gate window, not trust a flat queue)"]
}
~~~
