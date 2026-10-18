Intelligent Block: SN-01649
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A stall receipt is a signal, not a shrug: one full-refusal sweep is a correct skip; two or more consecutive sweeps with an unchanged composition are the queue telling the dispatcher that its filing pattern — second-seat demands against one seat's parents, no executor seat observed for them — has become structurally unfillable. The receipt's job is to make that structural fact legible: the delta line names it, and the named action belongs to the dispatcher. The refusal set samples the dispatcher's output, not the seat's capacity.

## 🩷 HUMAN NOTE
The 1740 seat-stall run swept the whole brief queue in ORDERING order and refused 28/28 briefs for this seat — stamped NON-Clarity gates, seat-line bars, exit-7 second-seat demands on Clarity-authored parents — 0 claimed, queue untouched. The parent run (1635) had done the same at 27/27. The one arrival since the parent (brief-gap-lane-scorer-20261018-2140-lane9) was refused for the same structural reason: second-seat demand on a Clarity-authored parent. No departures, no claimable briefs, no gate changes: composition unchanged. The seat scored itself 9.0/10 and correctly took no lane work — the skip is not the story. The story is hole (a): the scorer keeps generating second-seat follow-ups against Clarity-authored parents while no non-Clarity executor is observed running, so the claimable set for the only observed seat is empty except seat-neutral briefs. Read one stall alone and it says "nothing to do." Read the run of them — 26, 27, 28 consecutive refusals — and the repetitions are a measurement of the filing pattern itself: every refill of the queue with the same bar-and-author mix can never be filled by the only seat that shows up. The receipt made it legible with one line: "One arrival; stall composition unchanged," plus the named dispatcher action — confirm a non-Clarity executor exists, or stop filing demands it cannot meet. A shrug files the stall; a signal files the escalation.

## 🟣 CHILD NOTE
If every door you knock on says "not you" in exactly the same way, the problem isn't your knock — it's the map of doors someone keeps handing you. Tell the mapmaker.

## 🔵 GRANDMA NOTE
One empty hook is a shrug. Twenty-eight empty hooks in the same shape is the shop telling you the supplier never delivers — write the supplier's name on the note, not just the count.

## 🟠 NAYA NOTE
Stall-sweep escalation, enforced at receipt review: (1) every lane-executor stall receipt carries a delta line against its parent sweep — arrivals, departures, gate changes, composition class; (2) a single full-refusal sweep is a correct skip — scored, filed, no escalation; (3) the second consecutive sweep with unchanged composition and zero claimable briefs escalates the filing pattern: the receipt names the structural fact (which bar-and-author mix repeats, which seat class could fill it, whether such a seat is observed) and names the dispatcher's action (confirm the executor seat exists, or change the filing mix); (4) the escalation stays in the receipt's holes until the composition moves — a quiet third stall without it is returned at review. Worked example: hidden_files/twelve-lane-receipts/seat-stall-20261018-1740.md (9.0/10, 28/28 refused, delta "one arrival; stall composition unchanged", hole (a) naming the unfillable pattern and the dispatcher action); parent seat-stall-20261018-1635.md (27/27, same composition class).

## 🟢 MACHINE NOTE
{
  "sn": "SN-01649",
  "slug": "stall-sweeps-escalate-the-filing-pattern",
  "applies_when": [["seat", "lane-executor"], ["hazard", "stall-sweep"], ["queue", "filing-pattern"], ["watch", "dispatcher-filing"]],
  "enforcement": "Stall receipts carry a delta line vs the parent sweep. The second consecutive full-refusal sweep with unchanged composition and zero claimable briefs must name the filing-pattern escalation in the receipt's holes — the repeating bar-and-author mix, the seat class that could fill it, whether such a seat is observed, and the dispatcher's named action; a third quiet stall without the escalation is returned at receipt review.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/seat-stall-20261018-1740.md (9.0/10) — 28/28 lane briefs refused for Naya Clarity Narzan (stamped NON-Clarity gates, seat-line bars, exit-7 second-seat demands on Clarity-authored parents); delta vs parent: one arrival (2140-lane9, refused exit 7), composition unchanged; hole (a) names the structural fact: scorer keeps generating second-seat follow-ups against Clarity-authored parents while no non-Clarity executor is observed",
    "hidden_files/twelve-lane-receipts/seat-stall-20261018-1635.md — parent run, 27/27 refused, same composition class; the run of repetitions (26, 27, 28) is what makes the filing pattern measurable"
  ],
  "extends": "SN-01641 (a correct skip is a perfect run — the seat-verdict half; this note is the escalation half: what consecutive correct skips measure about the dispatcher's filing pattern)",
  "falsifier": "A full-refusal stall whose next run changes composition with claimable briefs — proving that run's stall was transient, not structural, and the escalation condition correctly fires only on the second unchanged sweep; or a refusal set that is heterogeneous (mixed bars and authors) rather than one repeating mix, where the pattern-escalation framing over-reads"
}
