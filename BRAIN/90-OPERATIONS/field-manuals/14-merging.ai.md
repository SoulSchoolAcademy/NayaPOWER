# 14 - Merging (AI)
area_number: 14
area_name: Merging
owner_team: Naya Resolve
agent_seat: Builder

## DEFINITIONS
- what_it_is: The dock: the moment a branch's work lands on main and becomes everyone's truth. The highest-leverage single action a Naya takes - one merge moves the tip every other lane builds on.
- what_it_does: Converts reviewed, proven work into the shared tree. Done right, the tip stays green, every byte is traceable to its review, and a cold Naya can re-derive exactly why this merge was lawful.
- why_it_matters: A bad merge poisons the well: every lane downstream builds on a red or unreviewed tip, and the repair costs ten times the prevention. Paid for twice: PR #1475 merged after a blocking review landed; PR #1627's guard merged with zero live call sites.

## PROTOCOLS
1. Pre-merge checklist, in order, in one unbroken step: (1) re-fetch the live ref (the ref, never the commits list); (2) freeze the PR head SHA; (3) read check states AT the frozen head; (4) re-fetch the venue's newest state; (5) confirm scorecard 9.5+ naming the exact head, receipt file behind it; (6) confirm cross-seat review from a different seat at the exact head, pre-merge (seat-tagged [NAYA M x REVIEW] APPROVED comments satisfy the prong); (7) never self-merge; (8) name the omissions (what the required set never examined).
2. Write the merge-authority record BEFORE merging: PR number, frozen head SHA, scorecard receipt (id + score), reviewer seat, check states at the head, named omissions. No record = no authorization.
3. When the protocol does not pass, stand down: post what failed, which prong, what would repair it; the PR returns to the queue. A stand-down is a correct outcome.
4. The dock holds a moving head: if commits land mid-checklist, wait, re-freeze, restart the checklist at the new head.
5. Merges sequence through the merge lane: queue order, coordinated, never ad hoc.
6. Post-merge faithfulness proof before closing: (1) ancestor check (behind == 0 AND merge_base == merge commit); (2) blob identity (key blobs byte-identical at PR head, merge commit, tip); (3) wiring check (every canonical call site references the new code on live main); (4) tip-health check (re-run the freshness battery AT the merge commit).

## CONSTRAINTS
- Pre-merge checklist, in order, in one unbroken step: (1) re-fetch the live ref (the ref, never the commits list); (2) freeze the PR head SHA; (3) read check states AT the frozen head; (4) re-fetch the venue's newest state; (5) confirm scorecard 9.5+ naming the exact head, receipt file behind it; (6) confirm cross-seat review from a different seat at the exact head, pre-merge (seat-tagged [NAYA M x REVIEW] APPROVED comments satisfy the prong); (7) never self-merge; (8) name the omissions (what the required set never examined).
- When the protocol does not pass, stand down: post what failed, which prong, what would repair it; the PR returns to the queue. A stand-down is a correct outcome.
- Merges sequence through the merge lane: queue order, coordinated, never ad hoc.

## BOUNDARIES
- not_covered: What authorizes a merge (the scoring matrix, the 9.5 bar, protected human gates); How to prove a fix is real (independent re-derivation, sabotage batteries); What a scorecard must contain; Keeping the tip fresh while working; Races at the dock
- #21 Authority: what authorizes a merge
- #6 Verification: proving the work itself
- #5 Scoring: defines scorecard content
- #15 Freshness: freezing the head / live reads
- #23 Deconfliction: preventing merge races

## ENFORCEMENT
### Mechanically enforced (live)
- Branch protection ruleset 23853581 ('Naya Execution Governance'): required checks 'Receipt gate (evidence or it didn't happen)' + 'Team review + scorecard receipt' on the merge path. Live and active.
- The team relay's merge-protocol watch: every relay pass checks each merge to main since the last watermark for cross-seat review and a scorecard receipt naming the exact merged head; breaches posted on the venue immediately.
- Receipt gate: receipt before merge, never after (culture-enforced).
### Proposed (designed, not built - do not claim as live)
- A mechanical pre-merge checklist gate that refuses the merge when any checklist item is unproven (stale head, missing authority record, unnamed omission). Today: procedure + relay watch.
- Automatic freshness-battery run at the merge commit before the tip is claimed green. Today: lane rule (L323), not a wired gate.

## SELF-TEST
1. The scorecard says 9.5 but names the parent SHA, not the head I'm about to merge - do I merge? (No: it must name the exact frozen head.)
2. After my merge, compare shows behind == 0 but merge_base is NOT my merge commit - what do I record? (Not MERGED-VERIFIED; investigate.)
3. The required checks are green, but the kernel battery isn't in the required set and it failed at this head - what goes in the record, and do I merge? (Name the omission; do not merge around an unexamined red.)

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6172905021 - PR #2580 cross-seat prong re-verified on live bytes: seat-tagged APPROVED comments satisfy the law
