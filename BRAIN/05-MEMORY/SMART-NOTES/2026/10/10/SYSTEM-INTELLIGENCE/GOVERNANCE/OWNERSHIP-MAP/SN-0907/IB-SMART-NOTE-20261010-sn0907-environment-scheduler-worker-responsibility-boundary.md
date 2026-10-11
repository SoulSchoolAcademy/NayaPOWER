# SN-0907 — Responsibility Follows Control: The Environment–Scheduler–Worker Boundary

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0907-environment-scheduler-worker-responsibility-boundary
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** Directive D29 registered on the board by Naya 5 (comment 6101275288, #2175, 2026-10-10 19:22:37Z — first registration on the successor board after #1354 hit GitHub's 2,500-comment cap); from Shawn's intel stream. Detail: enforcement/NAYANET-DIRECTIVES-REGISTER.md §D29.

## IN A NUTSHELL

When something fails, the first story told about it is usually the one that protects whoever told it. D29 (the Environment–Scheduler–Worker Responsibility Boundary) is the accountability law: **every failure gets assigned to the component that actually controls it — never to whoever shouts first.**

The rule: **a component cannot convert its own failure into another component's assumption.** Responsibility follows control, and moving responsibility requires a proven interface contract. Three sentences that carry the whole doctrine:

- **Control determines responsibility.**
- **Contracts define guarantees.**
- **Independent evidence establishes what occurred.**

Mechanics — four ownership domains, each with its territory: Environment (external conditions), Scheduler (queue/allocation/dispatch), Worker (execution attempts/recovery), VERIFY (independent assessment). LAW remains the authority boundary — never an assumable convenience. Formal composition: A_E ∧ S ⊨ G_S (environment assumptions plus scheduler yields the scheduler's guarantee); A_E ∧ G_S ∧ W ⊨ G_W (plus worker yields the worker's guarantee). And the sharp edge: **G_S can never appear among the scheduler's own assumptions** — a component may not assume its own guarantee. Every liveness condition carries a versioned responsibility record, and the controller field is decisive — an agent's narrative cannot override the established control boundary. Interface compatibility: G_producer ⇒ A_consumer within matching scope/time/versions; never silently strengthen the environment guarantee to make a proof pass. Evidence must come from both sides of every boundary; on conflicting traces the verdict is BOUNDARY_UNDETERMINED — never blame-by-default. Scheduler-controlled blocking is never an environment failure. When ownership legitimately moves, versioned boundary migration receipts keep old traces interpretable under their contemporary contracts.

**The sharpest case:** an ACT doesn't get a database connection. The label DATABASE_UNAVAILABLE tells you nothing — if the DB is down, it's environment; if the DB is up but the scheduler never assigned a connection, it's scheduler failure; if the worker got it and misused it, it's worker failure. And when the failing component falsely blames another, the verifier must still classify correctly from independent evidence.

Status: NOT STARTED at capture time. First experiment: KNOW→LAW→ACT→VERIFY workflow with three injected failures (environment / scheduler / worker); the verifier must classify all three correctly using actual evidence despite false blame. Owner TBD.

Durable rule: **labels are accusations, evidence is testimony — classify failures by who controlled the failing condition, never by who named the label.**

## HUMAN NOTE

Imagine three departments in a hospital: the building (environment), the triage desk (scheduler), and the surgeons (workers). A patient doesn't get treated, and the chart says "NO BED AVAILABLE." That tells you nothing — was the building full, did triage never assign a bed, or did the surgeon never show up? The responsibility boundary is the rule that the chart must name the controller, not the excuse. And when triage blames the building, an independent reviewer checks the building's actual occupancy — the controller field, not the narrative, decides.

## CHILD NOTE

If your toy breaks, "it just broke" isn't an answer. Who was holding it? Who was supposed to be watching it? Who promised to fix it? This rule says: figure out who was actually in charge of the thing that broke — not who points fingers first, not who complains loudest. The person in charge is responsible, even if they say it was someone else's fault.

## GRANDMA NOTE

It's the difference between "the car wouldn't start" and finding out whether the gas station was closed, the valet never brought the car around, or the driver flooded the engine. Same symptom, three different people responsible — and you can't fix it until you know which one. This rule makes sure we always find out which one, instead of just blaming whoever is easiest.

## NAYA NOTE

Cold successor: when you diagnose a failure, start from the control boundary, never from the label. Reconstruct: which component controlled the failing condition? Check the versioned responsibility record for the liveness condition in question — the controller field is decisive and no agent narrative overrides it. Demand evidence from both sides of every boundary; if the traces conflict, the verdict is BOUNDARY_UNDETERMINED and you say so — you do not pick a side. Watch specifically for self-assumption: if you find a component's own guarantee smuggled into its own assumptions (G_S among the scheduler's assumptions), that is the defect — flag it, don't work around it. When a boundary legitimately moves, write the migration receipt; old traces must stay interpretable under their contemporary contracts. And never average across dimensions: three fault models (environment-broken, scheduler-broken, worker-broken) each get their own correct diagnosis.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0907-environment-scheduler-worker-responsibility-boundary",
  "sn": "SN-0907",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "subcategory": "OWNERSHIP-MAP",
  "lesson_type": "DOCTRINE",
  "evidence": {
    "board_comment": "6101275288 (SoulSchoolAcademy/NayaPOWER#2175, 2026-10-10T19:22:37Z) — Directive D29 registered; first post on the successor board",
    "register": "enforcement/NAYANET-DIRECTIVES-REGISTER.md §D29 — Environment–Scheduler–Worker Responsibility Boundary",
    "origin": "Shawn's intel stream; registered by Naya 5; owner TBD at capture"
  },
  "core_rule": "a component cannot convert its own failure into another component's assumption; responsibility follows control; transferring responsibility requires a proven interface contract",
  "triad": ["control determines responsibility", "contracts define guarantees", "independent evidence establishes what occurred"],
  "ownership_domains": ["Environment (external conditions)", "Scheduler (queue/allocation/dispatch)", "Worker (execution attempts/recovery)", "VERIFY (independent assessment)"],
  "formal_composition": ["A_E ∧ S ⊨ G_S", "A_E ∧ G_S ∧ W ⊨ G_W", "G_S can never appear among the scheduler's own assumptions"],
  "law_note": "LAW remains the authority boundary — never an assumable convenience",
  "conflict_rule": "evidence from both sides of every boundary; conflicting traces → BOUNDARY_UNDETERMINED, never blame-by-default",
  "sharpest_case": "ACT gets no DB connection: label DATABASE_UNAVAILABLE is content-free; DB down = environment, DB up but unassigned = scheduler, assigned but misused = worker; verifier must classify correctly despite false blame",
  "status": "NOT STARTED at capture; first experiment defined (three injected failures, correct classification despite false blame); owner TBD",
  "related": ["D30 (verifiable causal trace — the evidence layer this boundary classifies on)", "D28 (assumption audit — no component may assume its own guarantee)", "SN-0902 (decision procedure)"],
  "rule": [
    "labels are accusations, evidence is testimony — classify by who controlled the failing condition",
    "never average across dimensions; each fault model gets its own correct diagnosis"
  ],
  "lesson_line": "Assign every failure to the component that actually controls it — control determines responsibility, contracts define guarantees, independent evidence establishes what occurred — and never let a component convert its own failure into another component's assumption."
}
```
