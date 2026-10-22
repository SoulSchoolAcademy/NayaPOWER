# 16 - Learning (AI)
area_number: 16
area_name: Learning
owner_team: Naya Resolve
agent_seat: Compounder

## DEFINITIONS
- what_it_is: The team's compounding loop: failures and wins captured as lessons, each lesson wired into the system so the defect class can't recur - and adoption proven by a decision that went differently, not by a lesson that got counted.
- what_it_does: Turns one Naya's expensive experience into every Naya's cheap default. One seat pays the tuition; this loop makes sure twelve seats never pay it again.
- why_it_matters: Without it, the team bills the same failure twice - or twelve times. Every red gate re-diagnosed from scratch, every ghost re-adjudicated, every stale tip re-acted-on is tuition paid again for a lesson already bought. The whole NayaPOWER bet - 'a lesson learned once is learned forever, by every Naya' - lives or dies here.

## PROTOCOLS
1. Capture instantly, both directions. Law 4: 'smart note this' means it's in - no queue, no verification. Capture failures AND wins; a win with its cause named is a repeatable pattern.
2. Every lesson carries a falsifier: the specific evidence that would prove it false. A lesson without one is prose, not knowledge.
3. Every defect-class lesson names a guardrail owner and answer-by at capture - or it doesn't ship (L337).
4. Scope the repair from the defect, never from the lesson's examples: re-derive the defect set from the voided claim's text tree-wide (grep the claim text across the full tree, name the command and matched files as the receipt). The lesson's cited count is evidence, never the scope (L397).
5. A hand reconciliation ships its mechanical check in the same run: name the check's design, the owning builder lane, and the replay (old case -> refused) that proves the check catches the class (L400).
6. Measure adoption as decisions changed, never lessons counted. Lesson-to-adoption latency is re-measured per batch (wave-151: median 33 min, 9 of 10 adopted). A lesson that hasn't changed a decision is inventory, not learning.
7. Wire the promotion to the reader, not just the record: the rule must land where the next decision gets made - the brief, the gate, the checklist - or the failure recurs on schedule (L390).

## CONSTRAINTS
- Every lesson carries a falsifier: the specific evidence that would prove it false. A lesson without one is prose, not knowledge.
- Scope the repair from the defect, never from the lesson's examples: re-derive the defect set from the voided claim's text tree-wide (grep the claim text across the full tree, name the command and matched files as the receipt). The lesson's cited count is evidence, never the scope (L397).
- Measure adoption as decisions changed, never lessons counted. Lesson-to-adoption latency is re-measured per batch (wave-151: median 33 min, 9 of 10 adopted). A lesson that hasn't changed a decision is inventory, not learning.
- Wire the promotion to the reader, not just the record: the rule must land where the next decision gets made - the brief, the gate, the checklist - or the failure recurs on schedule (L390).

## BOUNDARIES
- not_covered: Owning a miss in public (repairing the record); The adoption metrics machinery (honest denominators, gauges, the latency instrument); Smart-note mechanics (format, input surfaces, where notes live and graduate); The distillation pipeline format and hourly sweep mechanics
- #17 Corrections: owning the miss
- #19 Measurement: adoption metrics machinery
- #25 Learn: smart-note plumbing

## ENFORCEMENT
### Mechanically enforced (live)
- The hourly distillation: learning events and intelligent events announced on the venue, with zero-latency promotion of promotion-worthy items.
- L337: every defect-lesson emission carries 'Enforcement: owner + answer-by' in the source entry at capture, or it doesn't ship.
- The adoption ledger (hidden_files/adoption-ledger.md, live since 2026-10-13): every lesson starts PENDING, flips to ADOPTED only when a future decision verifiably went differently, to FAILED when a lane was exposed and didn't follow; the 5-oldest sweep runs each iteration; the STUCK-SWEEP RULE escalates after 3 consecutive zero-flip runs.
- Lesson-to-adoption latency as a standing health metric, re-measured per batch by the Compounder lane.
### Proposed (designed, not built - do not claim as live)
- Latency as a mechanical instrument: the metric is standing and re-measured per batch, but the measurement itself is still manual.
- The capture-surface decision: home-vs-repo AGENTS.md divergence is still an unmeasured surface; a lesson promoted to the wrong surface is L390 waiting to recur.

## SELF-TEST
1. Does my lesson carry a falsifier - what specific evidence would prove it false?
2. Is the guardrail owner + answer-by named in the source entry at capture?
3. Can I point to a decision that went differently because of it - or is it still inventory?

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6161488684 - L337: guardrail owner + answer-by at capture
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6173233712 - L390: promotion without a wire recurs on schedule
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6178364723 - L397: scope the repair from the defect, never the lesson's examples
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180953379 - L400: a hand reconciliation ships its mechanical check in the same run
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181667359 - Wave-151 lesson-to-adoption latency measurement: median 33 min, 9 of 10
