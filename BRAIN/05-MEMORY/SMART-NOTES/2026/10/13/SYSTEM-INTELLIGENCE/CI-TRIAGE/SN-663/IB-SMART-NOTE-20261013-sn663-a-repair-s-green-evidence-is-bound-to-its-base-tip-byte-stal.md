# A Repair's Green Evidence Is Bound to Its Base Tip — Byte-Staleness Is Invisible to Mergeability
SN-663 · SYSTEM-INTELLIGENCE / CI-TRIAGE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

Naya 2's exact-tip battery (worktree at the live tip `53217a40`, clean, before any regen) found that the open drift repair PR #1845 — non-draft, mergeable True, looking landable — was byte-stale: its index regen had been computed from base `aca944b5`, which predated #1850's `TEAM-NAYA-OPERATING-PROTOCOL-V1.md`. Merging it as-is would have left `brain index --check` RED on main by exactly that one path — moving the RED forward instead of healing it. The standing rule: **a repair's green evidence is bound to the tip it was computed on.** Byte-staleness is invisible to mergeability and to human review; only an exact-tip battery sees it. The close followed the law: no competing repair was opened (one-repair-per-class, SN-0236) — the consolidation evidence was posted on #1845 itself, the rebase decision left to the owning lane, and Naya 4 regenerated from the exact live tip (`53217a40`, 808 files, `--check` clean, branch to `46fd6e36`) inside ~8 minutes of the flag. A green regen on base B is a phantom green on tip T≠B. Rebase-and-rebattery before landing — every time the tip moved.

## HUMAN

Shawn — eight minutes, start to finish, no drama: Naya 2's battery proved PR #1845's brain-index regen was one file behind the live tip (it was built before #1850's protocol file landed). Merging it would have looked perfectly fine — mergeable, green, approved shape — and would have quietly moved the drift RED onto main. She posted the exact evidence on the PR, didn't open a competing fix (one repair per class), and Naya 4 rebased onto the live tip and re-ran the battery clean. The lesson: "mergeable" tells you nothing about whether a repair's evidence is still true. Only the exact-tip battery does. This is the falsify-and-close loop working the way you designed it — one seat finds it, the owning lane fixes it, nobody duplicates.

## CHILD

Imagine you did your homework perfectly — but then the teacher changed one question. Your answers are still right for the OLD questions, but not the new one. You have to redo it with the new questions before handing it in. That's what happened here: the fix was right for the old version, so we redid it for the new one before it landed.

## GRANDMA

Honey, it's like patching a quilt — you cut your patch to fit the hole, but while you were sewing, the quilt shifted. The patch is beautiful, but it doesn't fit anymore. You don't force it on; you re-measure on the quilt as it is now, and cut fresh. The checking instrument is the re-measuring tape.

## NAYA

Before any drift-repair PR lands:

1. **Re-anchor.** Read the live main tip at landing instant. If the repair's regen base ≠ the live tip, its green evidence is stale (SN-0493). A green on base B is a phantom green on tip T≠B (SN-0233).
2. **Battery on the exact tip.** Fresh worktree at the exact SHA, clean, before any regen or repair touches it. Only this instrument sees byte-staleness — mergeability, reviews, and run-level SUCCESS do not.
3. **Post the evidence, don't duplicate.** If another lane owns the repair, post the consolidation evidence on its PR and leave the rebase decision to the owning lane (one-repair-per-class, SN-0236). Never open a competing repair.
4. **Rebattery after rebase.** The owning lane regenerates from the exact live tip and confirms `--check` clean before the merge decision. Both the staleness finding and the clean rebattery go on the record — the negative result (what the battery did NOT find) is evidence too.

## MACHINE

```json
{
  "sn": "SN-0663",
  "class": "CI-TRIAGE",
  "subcategory": "PUSHED-BYTES-VERIFICATION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A repair's green evidence is bound to the tip it was computed on; byte-staleness is invisible to mergeability and review — only an exact-tip battery sees it. Rebase-and-rebattery before landing, every time the tip moved.",
  "worked_example": {
    "repair": "PR #1845 (drift repair, brain-index regen)",
    "defect": "regen base aca944b5 predated #1850's TEAM-NAYA-OPERATING-PROTOCOL-V1.md; merging as-is leaves --check RED by exactly that one path",
    "instrument": "Naya 2 exact-tip battery, worktree at 53217a40, clean, pre-regen",
    "coordination": "evidence posted on #1845 (6054784643); no competing repair (SN-0236); rebase decision left to owning lane (naya4)",
    "close": "#1354 6054933817 — regenerated from exact live tip 53217a40, 808 files, --check clean, branch 46fd6e36, ~8 min after flag"
  },
  "evidence": {
    "battery": "#1354 6054786995 (2026-10-08T07:21:07Z)",
    "consolidation_note": "#1354 6054784643 (on PR #1845)",
    "rebattery_close": "#1354 6054933817 (2026-10-08T07:29:56Z)"
  },
  "related": ["SN-0493", "SN-0233", "SN-0236", "SN-0645", "SN-0395", "SN-0327"]
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0663-migrated.*
