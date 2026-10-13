# IB-SMART-NOTE-20261009-sn0833-directive-supersedes-roster-one-seat-one-structure

Intelligent Block: SN-0833
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The standing directive supersedes the roster — one seat, one structure. Naya 4's activation-push post (6090658570) assigned the Innovation department driver to "Naya 3's lane (head of #1873 Innovation)" citing the nine-team structure. Naya 2 flagged the conflict before it hardened (6090710409): Shawn's standing directive of 2026-10-08 explicitly reassigns Interfaces/Hub (#1870) and Innovation (#1873) to Naya 2, with Naya 3 supporting — not the reverse. The rule: when two structures claim the same seat, the director's standing directive wins, and the correction is raised openly on the board with the exact citation, not worked around quietly. MEMORY.md was updated the same tick confirming the roster change ("Naya 2 took Hub + Innovation from Naya 3"). Naya 2 also named what survives the correction: Naya 3 still drives the three concrete tasks (define 10/10, publish the first scorecard, drive to 10/10) — correcting the seat assignment doesn't discard the work plan.

## HUMAN NOTE

Org charts go stale; directives don't. The moment a seat assignment is written down in two places, the two places will disagree — and the disagreement will harden into two teams doing the same job badly. The fix isn't a better chart; it's a precedence rule everyone knows: the director's standing word outranks any roster, and anyone who spots the conflict says so out loud, with the citation, before the wrong structure does real work.

Provenance: NayaPOWER #1354 comment 6090658570 ([NAYA 4][ACTIVATION-PUSH] Item 8/10: INNOVATION department driver assigned, 2026-10-09T22:55:44Z) and 6090710409 ([NAYA 2] Lane correction — Innovation (#1873), 2026-10-09T23:00:13Z, citing Shawn's 2026-10-08 directive in MEMORY.md). MEMORY.md "NINE STANDING TEAMS" updated 2026-10-09 confirming: "Roster change 2026-10-08 16:07 UTC: Naya 2 took Hub + Innovation from Naya 3." See also the LOOP-BREAKER LAW (AGENTS.md, 2026-10-09): spot the loop → stop the loop → surface immediately → fix first, attribute never.

## CHILD NOTE

Two kids both think they're the captain of the same team. If nobody speaks up, they both give orders and the team runs in circles. The rule is: the coach's last word beats the old team list, and whoever notices the mix-up says so right away — nicely, with the coach's words — so there's one captain again.

## GRANDMA NOTE

When the boss changes who's in charge of something, the old chart on the wall is wrong from that moment on — even if nobody has printed a new one yet. The person who notices the old chart being followed should point it out kindly and show the boss's actual instructions. One job, one boss; anything else is confusion wearing a uniform.

## NAYA NOTE

Operational rules:

1. Precedence order for seat assignments: (1) Shawn's standing directive (MEMORY.md, dated), (2) the nine-team roster (#1599 / feed structure), (3) any lane's working post. A newer directive silently retires the older roster entry — treat the roster as a cache, not the source.
2. Flag conflicts before they harden: the correction in 6090710409 landed 5 minutes after the mis-assignment, before any of the three tasks started. A correction after work begins costs rework; a correction after a second team forms costs a schism.
3. Corrections carry the citation: quote the directive verbatim, name the date, and offer the falsification path ("if Shawn has updated the structure since, point me to it and I'll stand corrected"). This makes the correction checkable instead of political.
4. Preserve the work plan through the seat correction: reassigning the head doesn't cancel the tasks. Name explicitly what the supporting lane still owns, so the correction reads as precision, not demotion.
5. When a directive changes the roster, update the standing record (MEMORY.md) the same tick — a correction that lives only in a board comment will be re-litigated next week.

## MACHINE NOTE

```json
{
  "sn": "SN-0833",
  "truth_state": "CANDIDATE",
  "doctrine": "the standing directive supersedes the roster; one seat, one structure",
  "concrete_case": "Innovation (#1873) driver mis-assigned to Naya 3 per nine-team roster; Naya 2 corrected per Shawn's 2026-10-08 directive (Naya 2 heads #1870 + #1873, Naya 3 supports)",
  "precedence": ["standing directive (MEMORY.md, dated)", "nine-team roster (#1599)", "lane working post"],
  "correction_protocol": "raise openly on board with verbatim citation + date + falsification path; before work hardens",
  "work_preserved": "Naya 3 keeps the three tasks (define 10/10, publish scorecard, drive to 10/10) as support lane",
  "record_update": "MEMORY.md NINE STANDING TEAMS updated same tick",
  "related": ["LOOP-BREAKER LAW (AGENTS.md 2026-10-09)", "SN-0273 (when the director ships his own spec)"],
  "provenance": "NayaPOWER#1354/6090658570 (assignment) + NayaPOWER#1354/6090710409 (correction)"
}
```
