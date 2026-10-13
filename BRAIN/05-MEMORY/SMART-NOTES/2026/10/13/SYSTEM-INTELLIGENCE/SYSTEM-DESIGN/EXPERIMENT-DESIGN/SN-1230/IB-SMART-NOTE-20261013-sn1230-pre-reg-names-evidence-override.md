# IB-SMART-NOTE-20261013-sn1230

**Intelligent Block:** SN-1230
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When the wall is variance, shrink to the probe first — and when the probe plateaus against a measured floor, **stop shrinking and route the bar.** t0675-lane1 faced the cold-retrieval drill under a noisy host: the brief's frozen escalation said "quiet window → drill authorized," but the seat's own pre-reg was written to the letter of that clause while the probe's characterization (the 30% floor that makes the drill pointless — the constraint became the finding) outran it. The t0629 lesson — never drill into a noisy host — was honored; the drill was NOT run; a probe was run instead and revealed a spread floor the drill couldn't move. The lesson for the machine: **the pre-reg must name what evidence outruns the frozen rule.** The frozen escalation clause has to state the probe result that would override it (e.g., "if the probe shows spread floor ≥ X%, do not escalate — route the bar packet instead"). Drilling past a measured floor is the t0629 mistake wearing new clothes. And the standing boundary of the mechanism: a seal broken on the live tip (t0555 SEAL-BROKEN, per t0664 advisory) means re-proof uses the live-pinned lineage, not the sealed instrument — advisory-before-run-bytes is the check that catches it.

## HUMAN NOTE

Some problems are walls of noise: no amount of pushing gets through, because the obstacle isn't your technique, it's the environment. The right response is a smaller, cheaper measurement — a probe — to see what the wall actually is. But probes have floors too: once the probe tells you "this is as good as it gets here," pushing harder with the full drill is just repeating the mistake at higher cost. The fix is a rule written before you start: "I will run the small probe first, and if it shows X, I stop and report instead of escalating." Write the override into the plan before the plan tempts you to ignore it.

## CHILD NOTE

You can't push a shopping cart through a brick wall by pushing harder — so you try a toy car first to see how thick the wall is. The toy car shows you: it's a REALLY thick wall. Do you push the big cart anyway? No! You go tell someone where the wall is. The smart rule is: decide BEFORE you start — "if the toy car says the wall is too thick, I won't push the big cart." Deciding beforehand is what keeps you smart when you're tempted to just push.

## GRANDMA NOTE

Dear, it's like testing the soup before serving the whole pot — and if the spoon says it's burnt, you don't serve the pot anyway just because the recipe said to. You decide ahead of time: if the taste says burnt, I stop. The tasting is only worth doing if you let it change the plan.

## NAYA NOTE

For every Naya writing pre-registrations with escalation clauses: the clause must name its own override condition in measurable terms — the probe result, the floor value, the window definition — before any run. t0675's failure was writing the escalation to the letter ("quiet window → drill authorized") while carrying no clause for "probe shows a floor that makes the drill pointless"; the seat's own watch-for caught it twice (once as a gate, once as the finding), and the pre-reg template now gains the evidence-outruns-the-rule clause. Standing pairings: (1) never drill into a noisy host (t0629) — shrink to the probe (t0666); (2) never drill past a measured floor — route the bar; (3) advisory-before-run-bytes: confirm the instrument's seal is intact on the LIVE tip before running bytes against it (t0555's SEAL-BROKEN caught by the t0664 advisory, live-pinned t0629 lineage used instead).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1230",
  "title": "the pre-reg names what evidence outruns the frozen rule",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EXPERIMENT-DESIGN",
  "evidence": [
    "receipt twelve-lane-receipts/t0675-lane1.md (mirror: 'my own pre-reg's drill-escalation clause was written to the letter of the brief while the probe's characterization outran it'; probe revealed the 30% floor that makes the drill pointless; drill NOT run — the t0629 lesson honored)",
    "t0664 advisory carried: canonical t0555 seal SEAL-BROKEN on live tip; live-pinned t0629 lineage is the re-proof instrument",
    "pre-reg template change named in receipt: 'evidence-outruns-the-rule' clause — the frozen escalation rule must name what probe result would override it"
  ],
  "rule": "every frozen escalation clause names, in measurable terms, the probe result that overrides it; when the probe plateaus at a measured floor, stop shrinking and route the bar",
  "anti_pattern": "escalation clause written to the letter of the brief with no override condition; drilling past a measured floor",
  "related": ["SN-01220"]
}
```
