# IB-SMART-NOTE — SN-0982

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATING-MODE/AUTOMATED-LOOP-DISCIPLINE

## IN A NUTSHELL

SN-0910 repaired the action-budget fact twice: the scarce meters are ~2,500 GitHub Actions *minutes*/month, REST quota, and Muse tokens — not "2,500 actions/month." But an overnight audit found the propagation tail was stale: several cron schedule bodies still said "2,500 actions/month" and still pointed workers at #1354 as the live board (#2175 is). Twenty corrected bodies are now written and waiting on Shawn's word, plus the one-time key renames (`shared-state.json` + watermarks still say `issue_1354_comments`). The durable rule: a corrected fact is not done until every standing text a worker reads carries it. Schedule bodies, watermarks, key names, brief templates, and budget-law blurbs are executable governance — workers decide where to post and how to budget *from those words*, so a stale body is a live bug, not a cosmetic issue. The fix for a fact has two halves: correct the doctrine, then sweep the propagation tail — every surface the old words reached — and only then is the correction complete. SN-0177's twin: when the loop misbehaves, repair its instructions; when the fact changes, repair every instruction that carries the old fact.

## HUMAN NOTE

We fixed a big misunderstanding about our budget: it's not "2,500 actions a month," it's 2,500 Actions *minutes*, plus API and token limits. But then we checked the automated reminders and scripts that workers read — they still had the old wrong wording, and they still told workers to post to a board that's full and can't take new comments. So workers were still being governed by the wrong words. The lesson: fixing the rule in your head isn't done. You have to go fix every reminder, template, and script that still says the old thing — because that's what the machines actually follow.

## CHILD NOTE

If you learn a fact was wrong, don't just fix it in your head — go fix every note, list, and reminder that still has the old wrong fact. Anything that still says the old thing will keep making people do the old thing.

## GRANDMA NOTE

You told the family the doctor changed the medicine time. But the pillbox label still says the old time — guess what time grandpa takes his pills. Change the label too, dear. Every label.

## NAYA NOTE

Future Naya: standing texts (cron bodies, budget-law blurbs, watermarks, brief templates, instruction headers) are code — they execute through workers' behavior. When a fact is corrected: (1) sweep every surface the old words reached (grep the cron bodies, the shared-state keys, the templates), (2) produce the corrected texts as a batch, (3) route the batch through the right gate — schedule updates and key renames need coordination with the director pass and, where the rules say so, Shawn's word; do not `cron.update` other schedules unilaterally. The propagation tail is part of the fix, not follow-up hygiene. An unclosed tail means two truths are live at once.

## MACHINE NOTE
```json
{
  "sn": "SN-0982",
  "slug": "fact-correction-propagation-tail",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-MODE/AUTOMATED-LOOP-DISCIPLINE",
  "doctrine": "a_corrected_fact_is_not_done_until_every_standing_text_workers_read_carries_it",
  "rule": {
    "fact_fix": "correct_the_doctrine_then_sweep_the_propagation_tail",
    "standing_texts_are": "executable_governance_stale_body_is_a_live_bug",
    "routing": "batch_corrected_texts_through_the_right_gate_never_unilateral_schedule_updates"
  },
  "evidence": [
    "night-shift-2026-10-10/morning-flags.md flag 4: overnight audit found schedules saying '2,500 actions/month' (fact: 2,500 GitHub Actions minutes/month) and pointing at #1354 (live board is #2175)",
    "night-shift-2026-10-10/receipts/t2242-b.md: 20 corrected cron bodies written, awaiting Shawn's word; shared-state.json + watermark key rename (issue_1354_comments) needs director coordination",
    "SN-0910 context: the budget fact was repaired twice — the doctrine half was done; the propagation tail half surfaced this shift"
  ],
  "cousins": ["SN-0910 (the action-budget meter repair — the doctrine half)", "SN-0177 (repair the loop's instructions, not just the instance)"],
  "distinct_from": "SN-0910 banks the corrected budget fact itself; SN-0177 banks repairing instructions that failed to check something; this banks the propagation-tail rule — every standing text that carries the old fact must be updated for the correction to be real."
}
```
