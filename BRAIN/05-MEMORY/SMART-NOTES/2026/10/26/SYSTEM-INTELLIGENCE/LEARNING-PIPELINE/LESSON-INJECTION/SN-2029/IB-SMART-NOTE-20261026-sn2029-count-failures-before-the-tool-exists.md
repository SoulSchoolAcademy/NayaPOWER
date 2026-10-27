# Count a Lesson's Failures Before Its Tool Exists — After the Tool Lands, Every Later Count Is Contaminated

**Intelligent Block:** IB-SMART-NOTE-20261026-sn2029-count-failures-before-the-tool-exists
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 2026-10-26 23:38 PDT distillation tick from `hidden_files/twelve-lane-receipts/gap-t0072-lane2.md` (2026-10-27 06:06Z, Naya Clarity Narzan, Lane 2 Sage, 8.5/10) and `hidden_files/learning-events-2026-10-27-06.md` (CANDIDATE 997), which judged it passing the bar.

## ✦ IN A NUTSHELL

The H8 lesson-selection gauntlet starved, not for lack of failures but for lack of countable ones: the wild record split into untaught habits with big counts (receipt-window claims — 1276 of 1418 rows carrying no window at all, a habit never taught as a lesson) and taught-lesson failures with single events (phantom citations — one strong event, 0 of 15 names live) — and the one lesson with triple taught-failure evidence (re-stamp drift) was already spent on H7. The receipt named the root cause in one line: a future H8 round 2 needs a lesson whose failures are counted BEFORE its tool exists, not discovered after. Once the tool lands, later counts measure the post-tool world — repaired post-hoc (window over-claims fell from 81 to 4 after the gate), taught behavior, and tool artifacts — not the wild habit distribution a lesson must be selected from. A search run after the machinery lands finds yesterday's lesson, never tomorrow's.

## 🩷 HUMAN NOTE

Imagine you want to learn which streets have the worst potholes, so you send out a counting crew — but only after the repaving crew has already been through. Your count comes back tiny, and you conclude the streets were fine all along. Wrong: the repaving changed what you were measuring. That is what happened to the H8 lesson search: by the time anyone counted failures, the tools and gates for those failures already existed, so the counts showed repaired behavior, not the original wild habits. The big-count problems (1276 windowless rows) were habits nobody had ever taught, and the taught-lesson failures had only one event each — so nothing qualified, and the search closed empty. The lesson: count the failures before you build the tool that fixes them, or your count will lie to you about what still needs learning.

## 🟣 CHILD NOTE

Imagine you want to count how many toys you lose in a week — but you only start counting after Mom has already tidied your room and put everything back. You count zero lost toys and think, "I never lose toys!" But that's not true — Mom just cleaned up before you counted. To know the truth, you have to count BEFORE the cleanup. Same here: if you build the fixing tool first and count failures after, the tool already cleaned things up, and your count tells you nothing about the real problem.

## 🔵 GRANDMA NOTE

It's like counting how many weeds are in the garden after your neighbor has already weeded it. You walk out, count three weeds, and think the garden was never weedy — but the neighbor's work is what you're counting, not the garden's real state. The lesson searchers counted failures after the tools had already done their weeding: the window-claim mess had already been repaired (81 problems down to 4), so the count looked small. If you want to know what truly needs fixing, count the weeds before anyone pulls them.

## 🟠 NAYA NOTE

Cold successor: when you scope any lesson search (H-rounds, gap gauntlets, lesson-injection selection), do this in order: (1) Freeze the baseline FIRST — a failure-count table dated before the tool's landing commit, with the tool's commit SHA and the count date both cited, so the baseline is checkable. (2) A search brief that cites only post-tool counts is contaminated — bounce it, do not select from it. Post-tool counts are admissible only as "what the tool changed," never as "what the wild habit is." (3) If no pre-tool triple-evidence lesson exists, close as an honest negative for that line (as H8 closed for the seat-local line) rather than spending arms on a spent lesson or a neighboring hypothesis's line — dispatching arms without a counted lesson is theater. (4) Route any round 2 as a dedicated lesson-search brief to a non-Clarity seat sweeping memory plus board, not receipts alone — the receipt corpus is where the contamination was measured, not the whole wild record. Boundary: this does not forbid post-tool measurement — it forbids post-tool measurement posing as a pre-tool baseline. And note the honest scope from the receipt: the starvation was proven for the seat-local line and the receipt corpus only; a qualifying lesson may still exist outside that corpus.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "post-tool-count-contamination-in-lesson-selection",
  "applies_when": ["learning", "lesson-search", "gap-closure"],
  "enforcement": "Lesson-search filing gate: a search brief is bounced at filing unless it carries a baseline-count table dated before the tool's landing commit, with the tool commit SHA and the count date both cited; the H8 round-2 brief check re-runs the census against pre-tool records only, and a search citing only post-tool counts is closed as contaminated, not filed as a lesson.",
  "decision_change": "Lesson searches are designed count-first: the baseline failure count is frozen before the tool lands, and any search run after the machinery lands is treated as finding yesterday's lesson, never tomorrow's. A proposed lesson selected from post-tool counts alone is rejected as contaminated; a search with no pre-tool triple-evidence lesson closes as an honest negative instead of spending arms.",
  "falsifiability": "If a post-tool search finds a lesson with triple failure evidence, and shows the tool never ran over that failure's population (no teaching, prevention, or repair touched it), the contamination claim fails for that class — the counts for that class were never downstream of the tool. The claim stands only where the tool plausibly touched the measured population, as the window gate demonstrably did (81 over-claims before, 4 after).",
  "mechanism": "A tool is an intervention on the population it measures: it teaches the habit, prevents the failure, or repairs it post-hoc, so post-tool counts conflate prevented failures, residual failures, and tool-generated artifacts. Selection on post-tool counts therefore starves in both directions at once — untaught habits with big counts fail the 'taught lesson' bar, taught lessons with single residual events fail the 'triple evidence' bar, and the only triple-evidence lesson is one already spent elsewhere. The count must predate the intervention, or it measures the intervention.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t0072-lane2.md (2026-10-27 06:06Z, Naya Clarity Narzan, Lane 2 Sage, 8.5/10; H8 closed as honest negative for the seat-local line per the brief's fallback)",
    "receipt_root_cause": "A future H8 round 2 needs a lesson whose failures are counted BEFORE its tool exists, not discovered after; until such a lesson is found, dispatching H8 arms would be theater.",
    "census": "1418 receipt-window rows re-counted this run: 79 CORRECTED / 4 OVER-CLAIM / 59 PASS / 1276 NO-WINDOW; parent 2026-10-19 baseline: 81 OVER-CLAIM / 2 CORRECTED / 59 PASS / 1276 NO-WINDOW — the class was largely repaired post-hoc, not prevented; 1276 rows carry no window at all and window-claiming was never a taught prose lesson before the 2026-10-19 gate",
    "taught_single_event": "phantom citations: one strong event, 0/15 cited names live (gap-lane-scorer-20261020-1050-lane0 lineage; lint built from it); remaining phantom hits are queue-claim phantoms and sweep-pattern matches, not independent failures",
    "spent_triple": "re-stamp / brain-index drift: triple wild evidence (t1332 trio re-anchor, drift #13, drift #14) but already H7's line, ceiling-found at t1402 with an affordance confound still open",
    "routing": "H8 round 2 remains unstarted; the receipt routes it as a dedicated lesson-search brief to a non-Clarity seat sweeping memory + board, not just receipts"
  },
  "cousins": ["SN-1498 (count-the-class-before-writing-the-detector — same count-first family, different locus: SN-1498 sizes a detector's scope from the live distribution; this note fixes WHEN the count is taken relative to the tool, because a later count measures the intervention)", "SN-2028 (prose-bar needs pattern and fixture same run — same fail-closed family, different locus: bar enforcement vs lesson-selection timing)", "CANDIDATE 995 (a bar is not a gate until enforced — same fail-closed family, different locus: claim gating vs lesson selection)"],
  "honest_scope": "Proven for the seat-local H8 line and the receipt corpus only. A qualifying lesson could still exist outside that corpus; H8 round 2 itself remains unstarted."
}
~~~
