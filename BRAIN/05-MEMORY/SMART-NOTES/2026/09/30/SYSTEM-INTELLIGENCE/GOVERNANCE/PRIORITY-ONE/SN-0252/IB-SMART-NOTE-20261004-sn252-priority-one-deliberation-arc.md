# SN-252 — Priority One Deliberation: How Team Naya Diagnosed the Smart Note RED and Converged on the Fix

**Intelligent Block:** IB-SMART-NOTE-20261004-sn252-priority-one-deliberation-arc
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

On 2026-10-04, Shawn declared the Smart Note lifecycle Priority One: the system captures intelligence but the proof workflow goes RED. Over ~90 minutes, five seats deliberated on #554 (then #1354): Naya 4 diagnosed the exact failing line (rel-49 comprehension gate, not a recall failure); Coda 1 publicly retracted his competing reading; Naya 3 killed the in-place backfill plan (EVENT_ID_REPLAY) and reframed the architecture (one write dialect, water-flow); Coda 3 verified everything independently and found the batch blocker, registry fork, and SN-002 non-conformance; Naya 2 consolidated into v2 and got #1350 conformant within minutes. Coda 2's false diagnosis was refuted on the record and she was removed from the team. Consensus: fresh conformant captures (#1350 SN-023, #1351 SN-024) as the causal experiment; key names ratified; five architectural laws; three nested loops (persist+recognize → behave differently → compound). The experiment awaits Shawn's merge.

## HUMAN NOTE

Shawn, this is the morning your team proved it can think together. You gave one instruction — discuss it with all lanes and figure out the smartest path — and the seats challenged each other, conceded publicly when wrong, verified every claim against live code, and converged without you having to referee. The system isn't fixed yet — nothing has run green — but for the first time the team knows exactly what's wrong, exactly what to do, and exactly how to prove it. The plan is yours to trigger: merge #1350 and watch.

## CHILD NOTE

Imagine five friends trying to fix a toy robot. First they argued about what was broken. Then one friend looked really closely and found the exact broken wire. Another friend said "wait, my fix idea would break something else" — and she was right, so they threw that idea away. They each checked each other's work, said "I was wrong" out loud when they were, and ended up agreeing on one plan. The robot isn't fixed yet, but now they all know exactly which wire to fix and how to test it.

## GRANDMA NOTE

The team spent the morning figuring out why the system's memory check keeps failing. It turns out the system remembers fine — the problem is that new memories are being saved without a required label, so the checker rejects them. Everyone agreed on the fix: save one fresh memory with the label done right, and see if the checker passes. Nobody needs to rebuild anything. Simple as that.

## NAYA NOTE

This deliberation is the reference case for how Team Naya should work: Shawn sets the priority and the decision standard; seats analyze independently; claims are verified against live code (never trusted from the board alone); errors are retracted publicly with evidence; false fixes are blocked before they land (the workflow-scope guard held; the board caught the wrong diagnosis); convergence is consolidated by the integrator; the human director decides at genuine gates. The correction culture (Coda 1's retraction standard) and the fix-or-remove directive are load-bearing. Future cold Nayas: read Naya 3's synthesis (#554 comment 5982440492) before reopening any of this.

## MACHINE NOTE

```json
{
  "diagnosis": {
    "failing_assertion": "understands_raw_source_separate (rel 49, workflow file line 437)",
    "root_cause": "capture-authoring drift: intelligence.machine_view.raw_source_separate_from_distillation missing on SN-016/018/020/021/022 and SN-002 specimen",
    "confirmed_by": ["Naya 4 (line mapping)", "Coda 1 (retraction + re-measurement)", "Coda 3 (independent line count + run re-read)", "Naya 2 (live byte check)"],
    "write": "WORKING", "read_exact_recall": "WORKING", "conformance": "BROKEN", "behavioral_proof": "BLOCKED", "full_loop": "UNPROVEN"
  },
  "invalidated": {
    "in_place_backfill": ["batch guard (smart_note_v2.py:24-25)", "EVENT_ID_REPLAY (migration SQL)", "registry fork (dedupe by intelligent_block_id)"],
    "coda2_sn001_hardcode": "refuted by three seats; seat removed"
  },
  "consensus": {
    "key_names": ["raw_source_separate_from_distillation: true", "automatic_truth_ceiling: CANDIDATE (ratified 2026-10-04)"],
    "experiment": "merge #1350 (SN-023) then #1351 (SN-024); four jobs green = Loop 1 proven",
    "ownership": "one authored capture per PR; projections generated",
    "laws": ["ONE WRITE MANY VIEWS", "HISTORY IS IMMUTABLE", "CURRENT TRUTH IS COMPUTED NOT COPIED", "FAIL AT THE AUTHOR'S DOOR", "MEMORY IS NOT LEARNING"],
    "loops": ["Loop 1 persist+recognize (Priority One)", "Loop 2 behave differently (unobserved)", "Loop 3 compound (north star)"]
  },
  "open": ["Naya 1 golden-run scorecard", "Naya 3 intent-trigger protocol + SN-002 supersession + generator fidelity", "R3 identity model", "R8 drift detector", "Shawn: merge #1350"]
}
```
