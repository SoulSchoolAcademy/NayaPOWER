# SN-0613 — Bake Memory Math: Never Restart What the Machine Cannot Fit

| Field | Value |
|---|---|
| Intelligent Block ID | SN-0613 |
| Title | Bake Memory Math: a restart loop cannot heal resource exhaustion — size the whole process tree to the machine |
| Class | REUSABLE INTELLIGENCE |
| Truth State | CANDIDATE |
| Captured | 2026-10-06 |
| Captured by | Naya 2 (Muse) |
| Director affirmation | Shawn Vibert, 2026-10-06 — "that's smart, that's intelligence... document this" |
| Provenance | Live incident: NayaPOWER Reveal narration bake, 2026-10-06 |
| Supersedes | Nothing. Complements SN-0493 (re-verify at action time) and SN-0500 (think before you act). |

## IN A NUTSHELL

The Reveal narration bake crashed seven times with `BrokenProcessPool`. Every restart re-crashed. The mechanism: the parallel baker loads the ~4GB model in the parent, then forks workers — on a 7GB VM, parent + even ONE forked worker exceeds RAM, so the OOM killer takes the worker every time. Two workers died; one worker died too. The repair was not fewer forked workers but NO fork at all: a sequential in-process baker (one process, one model, ~4GB total). **A restart loop cannot heal resource exhaustion. When a process dies repeatedly, do the resource math — and count the parent's share, not just the workers'.** **And when the first repair is disproven, preserve that correction too: the wrong fix is part of the intelligence because it teaches what the original model missed.**

## HUMAN NOTE

Shawn watched the bake die over and over and asked why it kept crashing. The first diagnosis was only half-right: two ~4GB workers could not fit on a 7GB machine, so dropping to one worker looked like the fix. Then the single forked worker crashed too. That new evidence exposed the real mechanism: the parent process already held the voice model, and forking even one worker added another working-memory burden the machine could not sustain. The durable fix was one sequential process, no fork, one model loaded once. The correction matters as much as the first diagnosis: **when new evidence disproves your fix, update the lesson instead of defending the old story.**

## CHILD NOTE

Imagine the car trunk already has one huge suitcase inside. You try to make another copy of that suitcase and squeeze it in. Two copies do not fit. Then you try just one copied suitcase — but you forgot the original is still in the trunk, so it still does not fit. The fix is not "make fewer copies." The fix is **stop making a copy at all** and use the one suitcase already there.

## GRANDMA NOTE

Dear, when the pot keeps boiling over, you don't keep putting it back on the same burner. We first turned the heat down and thought that was enough, but it boiled over again. That told us the burner setup itself was wrong. So we changed the cooking method: one pot, one burner, no duplicate process competing for memory. The lesson is to keep updating your explanation until it matches what the machine actually does.

## NAYA NOTE

This is SN-0500 applied twice: first, stop blind restarting and do the memory math; second, do not stop reasoning after the first plausible fix. The one-worker hypothesis was falsified by the next crash. That evidence forced a better model of the process tree: parent + forked child memory, not merely worker count. The final repair removed multiprocessing entirely. **Intelligence is not having the first answer; it is updating the model when reality proves the first answer incomplete.**

## MACHINE NOTE

```json
{
  "rule": "parallel_required_memory ~= parent_resident_memory + sum(worker_incremental_memory) + system_headroom; parallelize only when the measured upper bound fits safely below available RAM",
  "incident": {
    "workers": 2,
    "per_worker_gb": 4.1,
    "available_gb": 7,
    "required_gb": 8.2,
    "verdict": "OOM_GUARANTEED",
    "correction_20261007": "one forked worker ALSO died — the parent holds the model AND the fork needs working memory; fork itself is the problem on 7GB"
  },
  "repair": {
    "final": "sequential in-process baker (bake_narration_sequential.py): one process, one model, no fork, ~4GB total",
    "superseded_attempt": "single forked worker (still OOMed)",
    "watchdog_updated": "bake-watchdog.sh now launches the sequential baker"
  },
  "detection": ">=3 materially identical crashes under unchanged resource conditions -> stop restarting, inspect the full process tree and do the resource math",
  "applies_to": ["any parallel bake/render worker pool", "any repeated-crash loop"]
}
```

## LEARNING LESSON

**Restarting is not diagnosing, and the first plausible repair is not automatically the final diagnosis.** A process that dies the same way under unchanged conditions is evidence that the current execution shape does not fit the environment. Before the next restart ask: (1) What exact failure killed it? (2) What resource does that failure implicate? (3) What does the **entire process tree** consume — parent, children, model copies, working memory, OS headroom? (4) Did the latest attempted fix actually falsify part of our model? If the math does not work, change the shape of the work — eliminate the fork, reduce model footprint, shrink the batch, or use a larger machine. Do not press restart and call it diagnosis.

## HOW IT CONNECTS

- **SN-0500 (Think Before You Act):** this incident is the case study — four thoughtless restarts, then one thoughtful fix.
- **SN-0493 (Decisions expire):** the restart decisions were made for a world where "maybe it was a fluke"; each crash was new evidence the decision was stale.
- **SN-0440:** the exact-tip battery principle — verify on the real numbers, not the hoped-for ones. Memory math is the same instinct.
- **The Awesome Code:** awesomeness is the full process, not the fast retry.

## EPISTEMIC STATE

**CANDIDATE** — earned from a live incident with timestamps, PIDs, and log lines, affirmed by the director the same day. The first repair attempt (single forked worker) was itself disproven by another OOM — the note was corrected the same night. Not yet proven as a general law across other worker pools.

**Falsifier:** under the same 7GB environment and materially equivalent model/process memory conditions, the fork-based baker (one or more workers) completes 37/37 without memory failure; or repeated identical resource-exhaustion failures under unchanged conditions are shown to be resolved by an unchanged restart alone.

## UNCERTAINTY

- Per-worker footprint (~3.6–4.1GB) was estimated from `free` readings and the crash pattern, not from per-process RSS measurement. The inequality holds regardless, but the exact numbers are approximate.
- Sequential in-process wall time for all 37 slides was not yet measured at capture time; "slower but finishes" was initially a prediction and should be replaced by the completed bake measurement when available.

## APPLICABILITY

Any seat running model-heavy multiprocessing on a fixed-RAM VM. Check the **whole process tree** before parallelizing: `parent_resident + Σ(worker_incremental) + OS/headroom < available_RAM`, using measured or conservative values. Do not assume `worker_count × model_GB` is sufficient when the parent keeps the model resident. Encode the safe execution shape in the launcher/watchdog — never rely on remembering.

## SUCCESSOR EFFECT

A successor reading this should: (1) never restart a repeatedly-crashing worker pool without inspecting whole-process memory; (2) encode the proven safe execution shape in the watchdog/launcher — including **no fork** when parent + child cannot fit — with the resource rationale in code/comments; (3) treat repeated materially identical crashes as a stop-and-think trigger, not a restart trigger; and (4) correct the Smart Note when later evidence disproves an earlier fix.
