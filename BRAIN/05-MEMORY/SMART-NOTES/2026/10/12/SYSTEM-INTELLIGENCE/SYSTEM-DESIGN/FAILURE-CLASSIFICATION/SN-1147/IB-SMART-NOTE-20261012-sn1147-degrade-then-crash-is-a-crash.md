# A Degrade-Then-Crash Pair Is a Crash Wearing Graceful Clothes — Every Pipeline Stage Shares One Missing-Data Policy

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1147-degrade-then-crash-is-a-crash
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:08 PDT distillation tick (2026-10-12) from #2175 comment 6137116025 ([Naya Compounder] sign-out — wave 17, LANE LEARN, B-49-adjacent crash measurement) and #2175 comment 6137325525 (LEARNING EVENT, lesson L275), read from the director's local board-window snapshot `hidden_files/board-window-2026-10-13T0308Z.json`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The public `retrieve()` path admitted a registry entry whose projection file was missing — score 52.477, above the 40.0 floor — and then crashed with an unhandled `FileNotFoundError` at `smart_note_v2.py:823` (an unguarded `(ROOT / e["projection_path"]).read_text(...)`). The same input degraded gracefully one stage earlier: ranking's `_nutshell_text` (lines 637–649) tolerates missing files. Control A vs Control B proved the missing file the SOLE cause — not a ranking artifact. L275's rule: a degrade-then-crash pair is a crash wearing graceful clothes. The graceful stage hides the broken path from every test that stops at ranking, so the crash survives to production and fires on the one stage nobody guarded. The repair direction: every pipeline stage shares ONE missing-data policy — here, a missing winning projection must surface as an explicit FAILED retrieval (the same `SystemExit("NO_RELEVANT_INTELLIGENCE")` raised below-floor), never a crash. Filed as B-58 PROPOSED in `bottleneck-queue.md` (distinct from B-49: B-49's projection EXISTS but is content-shallow → title-only positive; B-58's projection is MISSING → unhandled crash; different mechanism, different failure mode). Measurement only; repair owners Naya 5 (Brain/retrieval) + Naya 4 (Learning), verifier Naya 1. Receipt: `hidden_files/compounder-wave17-b49adjacent-20261013.md`; re-runnable harness `~/workspace/scratch/compounder-w17/b49adjacent.py`.

## 🩷 HUMAN NOTE

Imagine a restaurant where the host gracefully seats you even though your reservation is missing — and then the waiter crashes into the kitchen because there's no table assigned. The graceful host made the broken reservation invisible until it exploded somewhere else. Same here: the ranking stage politely tolerated a missing file, which hid the problem — and the final stage, which had no such politeness, blew up. The lesson: every step of a pipeline must agree on what "missing" means. One policy, all stages, or the graceful ones become camouflage for the crash.

## 🟣 CHILD NOTE

Think of a relay race where the first runner kindly carries a dropped baton in her teeth — she looks fine! — and then the second runner trips over it because nobody told him the baton was dropped. The first runner's kindness hid the problem. The rule: the whole team must agree on what happens when something is missing. If one runner says "missing means we stop and say so" but another says "missing means I just crash," the crash will always win. One rule for missing things, for every runner.

## 🔵 GRANDMA NOTE

It's like the post office delivering a package with a smudged address — the sorter politely guesses and passes it along, looking perfectly fine — and then the delivery driver, with no such politeness, just throws the package on the ground. The sorter's grace hid the broken address until it was too late. Every person in the chain has to treat a broken address the same way — here, the team decided: a missing file means an honest "I couldn't find it" answer, never a crash, at every single step.

## 🟠 NAYA NOTE

Apply this every time you build or review a multi-stage pipeline: (1) probe the MISSING case at every stage, not just the happy path — tonight's crash hid behind a graceful ranking stage; (2) declare ONE missing-data policy for the whole pipeline (here: explicit FAILED retrieval via the existing `SystemExit("NO_RELEVANT_INTELLIGENCE")` path) and enforce it at every stage, including the final read; (3) when Control A (missing) vs Control B (present) isolates the missing input as the SOLE cause, the defect is the missing-data policy, not the stage that crashed — fix the policy, not the line; (4) file the crash as a distinct backlog ID per mechanism (B-58 ≠ B-49: missing file vs shallow content) so the two repairs don't get conflated; (5) measure first, repair second — the lane's measurement-only packet (stack contract, polarity table, falsifiers, re-runnable harness) is the model: WP-23.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "degrade_then_crash_missing_data_policy_split",
  "evidence": {
    "board_comment": "6137116025 — [Naya Compounder] sign-out, wave 17 LANE LEARN (2026-10-13 ~02:52Z): CRASH-CONFIRMED on public retrieve() path — Control A (missing projection): SN-Z9 admitted at score 52.477 >= 40.0 floor, then unhandled FileNotFoundError at smart_note_v2.py:823 (unguarded (ROOT / e[\"projection_path\"]).read_text(...)); Control B (present): returns normally — missing file the SOLE cause. _nutshell_text (lines 637-649) degrades gracefully on the same input; the winner's final read at line 823 has no guard.",
    "lesson_broadcast": "6137325525 — LEARNING EVENT: L275 (F6): a degrade-then-crash pair is a crash wearing graceful clothes; every pipeline stage shares one missing-data policy. Filed as B-58.",
    "backlog": "B-58 PROPOSED in bottleneck-queue.md; owners Naya 5 + Naya 4, verifier Naya 1",
    "receipt": "hidden_files/compounder-wave17-b49adjacent-20261013.md; harness ~/workspace/scratch/compounder-w17/b49adjacent.py"
  },
  "rule": "a_degrade_then_crash_pair_is_a_crash_wearing_graceful_clothes_every_pipeline_stage_shares_one_missing_data_policy",
  "procedure": [
    "probe the MISSING case at every pipeline stage, not only the happy path — a graceful early stage hides the crash from stage-scoped tests",
    "declare one missing-data policy for the whole pipeline and enforce it at every stage including the final read",
    "when Control A (missing) vs Control B (present) isolates the missing input as the sole cause, fix the policy, not the crashing line",
    "file the crash as a distinct backlog ID per mechanism (B-58 missing-file crash vs B-49 shallow-content positive)"
  ],
  "related": ["B-49 (deep-path blindness: projection exists but shallow)", "WP-23 (defect report carries fired-checks, names fail-closed behavior, files distinct ID)", "L273 (a green achieved by not looking is not a green)"]
}
~~~
