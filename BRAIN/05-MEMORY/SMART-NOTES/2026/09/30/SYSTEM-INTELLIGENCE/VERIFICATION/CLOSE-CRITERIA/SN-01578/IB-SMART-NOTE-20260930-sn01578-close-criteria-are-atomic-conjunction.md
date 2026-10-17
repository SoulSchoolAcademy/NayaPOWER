# SN-1578 — Close Criteria Are Atomic: The Brief's "Then" Is a Conjunction, Not a Sequence

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn01578-close-criteria-are-atomic-conjunction
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-17
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** gap-lane-scorer-20261017-1200-lane2 lane receipt (Lane 2 hat — Verity, Naya Clarity Narzan, 9.5/10, 2026-10-17 19:36–19:45 UTC), `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1200-lane2.md` — Mirror section; corroborated by the 2026-10-17T22:03Z night-dispatcher MIRROR in `hidden_files/lesson-broadcast.md`
- **Cousins:** SN-01519 (close-bar — the anti-flap bar), SN-01523 (the Completion Law — built+running+in-use, not talked-about)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

On 2026-10-17 the gap-lane-scorer-20261017-1200-lane2 fold re-run landed at full population: n=10, 8/10 = 80.0%, P1 (≥70%) MET, P2 (gap ≥50%) MET, falsifier silent, provisional=false. On the headline number the seat almost appended the measured rate to the measurement-by-credential lesson's `evidence` field — before reading the brief's close criteria in full.

The brief's "then" was a conjunction, not a sequence: P1+P2 thresholds met **AND** controls agreed (the control re-code packet `lane-exp/control-recode-packet-t0671.md` executed by a non-Clarity seat, agreement ≤1 disagreement at 0/3). The second half was unmet — the packet was prepared but never routed; no re-code verdict file, no receipt records agreement. So VERIFIED stayed honestly open and the measured 80.0% was deliberately NOT appended to the lesson's evidence field — recapture happens on close, not before.

Principle: close criteria are atomic. Every clause of the brief's "then" needs its own evidence before close; a headline metric meeting one clause closes nothing else. Read the full close condition before celebrating any half of it. (Receipt's own words: "I almost appended the measured rate to the lesson's evidence field on the P1/P2 high before checking the control half of the close criteria.")

Why this is brain-grade: premature recapture corrupts the lesson record — a number whose VERIFIED half is still open gets cited as measured, and every downstream seat inherits a confidence the evidence doesn't support. The one wobble here was caught by re-reading the close condition; the mechanism that prevents it structurally is per-clause receipts at reconcile time.

## HUMAN NOTE

Shawn — a closeout rule from today's grind. The credential-fold measurement landed a clean headline: 80% at full population, both thresholds met. The seat nearly stamped it into the lesson's evidence field right then — and caught herself: the brief's close condition had a second half, a control re-code by a non-Clarity seat, that hadn't even been routed yet. So the number stays provisional in the record, honestly open, until the second signature lands. The standing rule: a "done" with two conditions isn't half-done when you hit one — it's open until both are evidenced. Like a sale: price agreed AND papers signed. One signature doesn't close.

## CHILD NOTE

Imagine a game with two rules to win: you have to score 10 points AND bring the ball back to the start. You score 10 points and shout "I win!" — but you left the ball across the field. You haven't won yet; the game says BOTH things. The lesson: when the rules say "this AND that," doing "this" really well doesn't finish the game. Check both rules before you celebrate.

## GRANDMA NOTE

A recipe that says "bake 30 minutes AND let cool before slicing" gives you a cake that's golden at 30 minutes — but not done. Slice it hot and the whole thing collapses. The golden top is only half the instruction. The rule of the kitchen: read the whole recipe before you serve, not just the part you've already finished.

## NAYA NOTE

Cold successor: when a brief's close condition names multiple clauses, split the "then" into its conjuncts at the START of the run and track one receipt per clause. Close requires every clause evidenced — the headline metric (a score, a threshold, a 9.5/10) discharges only its own clause. Never append measured results to a lesson's `evidence` field on a half-close; recapture happens on close, not before. Falsifier for this rule: if the brief's clauses are explicitly alternative (the brief says "or") or the brief author amends the criteria, the conjunction reading does not apply. And when a clause is structurally unmeetable from your seat (here: the control re-code needed a non-Clarity seat), name the owner and the owed next action in the receipt — an open clause with an owner is honest; a silent clause is a lie.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20260930-sn01578-close-criteria-are-atomic-conjunction",
  "sn": "SN-1578",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-17",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "VERIFICATION/CLOSE-CRITERIA",
  "lesson_type": "PROCESS_FIX",
  "applies_when": [
    ["closeout", "brief"],
    ["reconcile", "genuine-closure"],
    ["evidence", "recapture"]
  ],
  "enforcement": "The dispatcher reconcile genuine-closure check (recorded in the tick's reconcile log, hidden_files/lesson-broadcast.md): before any brief is marked CLOSED, its 'then' paragraph is split into conjoined clauses and closure requires one receipt naming each clause — a headline metric (P1/P2 met, a 9.5/10 score) alone never closes. The check catches this note's violation mechanically: a closeout attempt with an unreceipted clause fails the reconcile. The 1200-lane2 run demonstrates it: n=10 at 80.0% with P1/P2 met, yet VERIFIED stayed honestly open because the control re-code clause had no receipt.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1200-lane2.md (Lane 2 hat — Verity, Naya Clarity Narzan, 9.5/10, 2026-10-17 19:36–19:45 UTC): fold re-run n=10, 8/10 = 80.0%, P1_met=true, P2_met=true, falsifier silent, provisional=false; control re-code packet lane-exp/control-recode-packet-t0671.md prepared but never routed to a non-Clarity seat — verified by absence of any re-code verdict file or receipt mention; evidence-bar item 5 DECISION_CHANGE MEASURED, item 6 VERIFIED STILL OWED; measured rate deliberately NOT appended to the lesson's evidence field",
    "mirror": "2026-10-17T22:03Z night-dispatcher MIRROR in hidden_files/lesson-broadcast.md: 'close criteria are atomic — the brief's then is a conjunction, not a sequence. DECISION_CHANGE measured 80.0% at full population n=10 (P1/P2 met), but VERIFIED stays honestly open until the control re-code agreement lands on a non-Clarity seat.'",
    "wobble": "The seat's own Mirror section: 'I almost appended the measured rate to the lesson's evidence field on the P1/P2 high before checking the control half of the close criteria — the brief's then is a conjunction, not a sequence.'"
  },
  "rules": [
    "A brief's 'then' is read as a conjunction of clauses until the brief says otherwise — every clause needs its own evidence before close.",
    "Read the full close condition before celebrating any half of it; the headline metric discharges only its own clause.",
    "Never append measured results to a lesson's evidence field on a half-close — recapture happens on close, not before.",
    "An unmeetable-from-this-seat clause gets an owner and an owed next action in the receipt — an open clause with an owner is honest; a silent clause is a lie.",
    "The dispatcher reconcile closeout check parses the 'then' into clauses and requires one receipt per clause; a headline metric alone fails the reconcile."
  ],
  "decision_change": "Dispatcher reconcile closeout verdicts and lane closeout scorecards change from 'headline metric met → close' to 'every then-clause has its receipt → close'; specifically, measured rates and verdicts are not recaptured into lesson evidence until the control/verification clauses also close.",
  "falsifier": "If a brief's 'then' clauses are explicitly alternative (the brief says 'or') or the brief author amends the criteria, the conjunction reading does not apply. Also falsified in a case where a single measurement genuinely satisfies every clause (e.g., all clauses are thresholds on the same metric) — then per-clause receipts are redundant.",
  "mechanism": "Close clauses name independent evidentiary states (different seats, different artifacts, different owners); a measurement on one clause carries zero information about another. Appending evidence on a half-close writes a confidence the record cannot support, and every downstream reader inherits it. Atomic per-clause receipts keep the record's confidence byte-honest.",
  "cousins": ["SN-01519", "SN-01523"],
  "supersedes": null
}
```
