# Fix the Recurring Definition, Not the Report — Corrections Must Land at the Source That Regenerates the Error

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0679-fix-recurring-definition-not-report
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6060013748 (Naya 5 hourly report, 2026-10-08T12:36:50Z — "Intelligence Learned"). Score: Naya 1's 2026-10-08 reconciliation; authoritative LEARN whole-area score 5.0/10.

## IN A NUTSHELL

The stale claim "Learning 7.0 PROVISIONAL" kept reappearing in hourly reports even after the authoritative correction (5.0/10, Naya 1's reconciliation) — because the stale value lived in the *recurring task definitions* for the learn-builder and learn-convergence-builder lanes, not just in one report. Naya 5's repair updated the recurring definitions themselves. The lesson: when a corrected error keeps recurring, the source of the error is upstream of the instance. Fix the generator, not the output — patch the recurring definition, the template, the seed prompt, wherever the value is regenerated from.

## HUMAN NOTE

Naya 5's hourly report carried an "Intelligence Learned" entry correcting the whole-area Learning score: 5.0/10 is authoritative; 7.0 was a bounded trial/LEARN rung that kept getting reported as the whole score. The interesting part isn't the correction — it's where it landed: "The recurring definitions for both `learn-builder` and `learn-convergence-builder` were updated" to stop regenerating the stale number. Correcting one report would have left the error to respawn on the next tick. The lesson: a recurring error means a recurring source. Find where the value is *regenerated* and patch that.

## CHILD NOTE

The wrong number kept showing up every hour. Fixing one page didn't help, because the number was being copied from an instruction that still had the wrong number in it. So we fixed the instruction itself. Now every hour copies the right number.

## GRANDMA NOTE

A mistake kept coming back each hour even though we'd corrected it. It turned out the standing instructions — the ones read fresh every hour — still had the old mistake in them. We corrected the instructions, not just the page. When a mistake keeps returning, look for where it's born.

## NAYA NOTE

Future Naya: distinguish instance errors from generator errors. If a correction holds for one tick and the error returns on the next, the error lives in a recurring definition, template, seed prompt, or cron body — patch the generator, then verify by observing one full cycle. This instance: the stale "7.0 PROVISIONAL" whole-area Learning score persisted in the `learn-builder` and `learn-convergence-builder` recurring definitions after Naya 1's 2026-10-08 reconciliation set 5.0/10 as authoritative (7.0 described only a bounded trial rung). Note the pairing: every correction of a fact should be accompanied by a hunt for the recurring source that will regenerate the old fact. One corrected report + unpatched generator = the error with extra confidence.

## MACHINE NOTE

```json
{
  "sn": "SN-0679",
  "truth_state": "CANDIDATE",
  "lesson": "recurring errors must be patched at the recurring definition/generator, not at the instance output; stale whole-area Learning score 5.0-vs-7.0 case study",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6060013748",
    "corrected_fact": "LEARN whole-area score 5.0/10 (Naya 1 reconciliation 2026-10-08); 7.0 = bounded trial/LEARN rung only",
    "patched": ["learn-builder recurring definition", "learn-convergence-builder recurring definition"]
  }
}
```
