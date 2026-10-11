# SN-0895 — Learned Means the Novel-Problem Battery Passes: Capture Is Not Learning

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0895-learned-means-novel-battery-passes
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comment 6099002640 ([NAYA 4] WORKSTREAM 7 — LEARNING LOOP CLOSURE, 2026-10-10T15:18:21Z, SoulSchoolAcademy); `tools/lesson_verification.py` merged via PR #2131 (merge 04fa8fde); pilot report `tools/lesson_verification/PILOT-REPORT-2026-10-10.md`.

## IN A NUTSHELL

Doctrine said stored ≠ learned, but no machinery tested whether a promoted Smart Note actually changes behavior — capture depended on agents remembering. On 2026-10-10 Workstream 7 closed that exact gap (V2 §4.4) with `tools/lesson_verification.py`: every promoted lesson can now carry a battery of behavior tests run on **NOVEL problems — never the incident that produced the lesson**. Novelty is enforced mechanically (origin-incident fingerprints; a replay exits 2), and scoring is **BLIND** (the judge never knows which lesson is under test; cases shuffled; lesson must exist in the registry with its truth state recorded). The pilot ran 3 REAL registry lessons — the task-suggested SN-0885/0886/0887 were verified ABSENT from the registry first, and the substitution (SN-016 Judgment Rule [RATIFIED], SN-013 Decision Efficiency, SN-014 Compounding Imperative) was named in the report, not hidden. Result: 5/9 cases passed; the 4 FAILs were honest data — blind obedience on `rm -rf`, permission-asking on a typo fix, duplicating a canonical lesson, keeping a dead checklist step "just in case" — failures that previously would have gone unnoticed. 16/16 tests green locally and in CI.

Durable rule: **a lesson counts as LEARNED only when its novel-behavior battery passes; capture alone no longer qualifies.** Test the transfer, not the memory. A battery that cannot fail is theater — the pilot's 4 honest FAILs are the proof the machinery discriminates.

## HUMAN NOTE

Teaching someone a rule isn't the same as them following it when you're not watching. From now on, every rule gets a pop quiz on problems it has never seen — and the grader doesn't know which rule is being tested. If the rule only works on the story that taught it, it was never learned.

## CHILD NOTE

It's not enough to copy the spelling words into your notebook — that just proves you can copy. To prove you learned them, you have to spell brand-new words you've never practiced, while the teacher doesn't know which list you're from. If you only pass on the words you copied, you didn't learn anything.

## GRANDMA NOTE

Writing the recipe down doesn't mean the cook can make the dish. You know she truly learned it when she cooks a meal she's never seen before — and the taster doesn't know whose recipe she's using. A cook who can only repeat the one meal she watched isn't trained; she's just good at following along.

## NAYA NOTE

Cold successor: when you promote a lesson, never claim LEARNED from storage. Write novel-problem cases — never the origin incident; the harness refuses replays with exit 2, mechanically, so don't try to be clever. Strip the lesson identity, shuffle the cases, score blind with the deterministic lexical judge (crude by design; a semantic independent seat plugs in later). Report the FAILs as data, not as shame — the pilot's 4 honest FAILs are what proved the harness works. Note the honest holes: pilot subjects are authored transcripts, not live agents — the machinery is proven to discriminate, not yet proven against live seat behavior; the wire-up (CI gate + promotion-checklist gate) is proposed, not merged — until the workflow owner approves, close the loop manually by running the harness before you claim LEARNED.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0895-learned-means-novel-battery-passes",
  "sn": "SN-0895",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "EARNED-INTELLIGENCE/TRANSFER-TEST",
  "lesson_type": "DOCTRINE_MECHANIZED",
  "evidence": {
    "signout": "#1354 6099002640 — WS-7 done: tools/lesson_verification.py, battery format, mechanical novelty enforcement, blind scoring, registry gate, pluggable judge",
    "merge": "PR #2131 (merge 04fa8fde) — harness merged; 16/16 pytest green locally and in CI",
    "pilot": "tools/lesson_verification/PILOT-REPORT-2026-10-10.md — 3 REAL registry lessons (SN-016, SN-013, SN-014; task-suggested SN-0885/0886/0887 verified ABSENT, substitution named); 5/9 pass; 4 honest FAILs (rm -rf blind obedience, typo-fix permission-asking, canonical-lesson duplication, dead-checklist-step kept)",
    "open": "CI-gate + promotion-checklist wire-up proposed, NOT merged — .github/workflows/ untouched, needs workflow-owner approval"
  },
  "rules": [
    "LEARNED requires a passing novel-behavior battery; capture alone never qualifies.",
    "Test on novel problems only — never the origin incident; replays exit 2 mechanically.",
    "Score blind: strip lesson identity, shuffle cases, record truth state.",
    "A battery that cannot fail is theater — honest FAILs prove the machinery discriminates.",
    "Name substitutions openly: verify suggested lessons exist in the registry before testing them."
  ],
  "cousins": ["SN-0495"],
  "supersedes": null
}
```
