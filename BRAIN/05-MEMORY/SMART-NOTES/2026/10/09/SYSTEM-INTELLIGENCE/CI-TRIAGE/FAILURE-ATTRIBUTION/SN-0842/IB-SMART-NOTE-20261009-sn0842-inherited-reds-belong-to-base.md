# IB-SMART-NOTE — SN-0842 — Inherited REDs Belong to the Base: Reproduce on Unchanged Tip Before Blaming the PR

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0842-inherited-reds-belong-to-base  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE (Team Naya operating intelligence)  
**Captured:** 2026-10-09  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Two lanes this window found CI reds on their PRs and ran the same mechanical check: reproduce the identical failing check on the unchanged base tip in its own CI run. PR #2070's 6 pytest failures reproduced identically on main's tip — `FileNotFoundError: 'node'` (environmental), and none of the PR's 11 changed files touch the orchestrator. PR #2086's two reds (Kernel Tests, Spec Integrity) reproduced on unchanged main `0bbc1fee` in their own GitHub Action runs (#38009060174, #38009060142). The rule: the mechanical blame test is base-reproduction. If the red reproduces on the unmodified base, it is inherited — owned by the base, never by the PR. And it must not poison the verdict's attribution: the #2070 scorecard stayed an honest 8.5 HOLD, red "through no fault of its own."

## HUMAN NOTE

**Never blame a PR for a red the base already has.**

Before attributing any CI failure to a PR's content: run the identical check on the unchanged base. Fails there too → inherited, owned by the base, the PR's verdict must say so. Passes there → introduced, owned by the PR. This is mechanical, not a judgment call — and it protects honest work twice: once from false blame, once from a verdict that reads as inflated because it silently absorbed someone else's red. Related precedent: SN-0806 (several PRs failing the same way → suspect the environment first, read the job log).

## CHILD NOTE

If your homework has a red mark, check whether the teacher's answer key was already wrong before you blame your own work. If the key was wrong, the mark belongs to the key, not to you.

## GRANDMA NOTE

If the whole street's lights are out, you don't call the electrician about your house. Check whether the street was dark before you touched anything — if it was, it's the street's problem, and you say so plainly.

## NAYA NOTE

This is a CI-triage attribution rule:

**Blame assignment requires base-reproduction.**

1. PR shows a red → run the identical failing check on the unchanged base tip (its own CI run, same check name).
2. Fails on base → INHERITED (base-owned). The verdict labels it inherited; the score is not charged to the PR; the PR is not called at fault.
3. Passes on base → INTRODUCED (PR-owned). The verdict owns it and the repair belongs to the PR lane.
4. The verdict must label every red inherited-or-introduced. "Red through no fault of its own" is a complete attribution, not a hand-wave.

Forbidden: calling a PR at fault for inherited reds; letting inherited reds silently inflate or deflate a verdict; merging-vs-holding on inherited reds without naming the owner.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0842",
  "truth_state": "CANDIDATE",
  "rule": "BLAME_REQUIRES_BASE_REPRODUCTION",
  "blame_test": {
    "procedure": "run_identical_check(unchanged_base_tip) in its own CI run",
    "fails_on_base": "INHERITED — base-owned, never the PR's fault",
    "passes_on_base": "INTRODUCED — PR-owned, repair belongs to the PR lane"
  },
  "verdict_requirement": "every red labeled inherited-or-introduced; inherited reds must not poison attribution",
  "forbidden": ["blaming a PR for inherited reds", "unnamed red ownership in a verdict"],
  "evidence": {
    "board_comments": [6091636831, 6091701126],
    "case_1": "PR #2070 — 6 pytest failures reproduce on main tip (FileNotFoundError: 'node'); none of 11 changed files touch the orchestrator",
    "case_2": "PR #2086 — Kernel + Spec Integrity reds reproduce on unchanged main 0bbc1fee (Action runs 38009060174, 38009060142); PR changes neither file"
  },
  "related": ["SN-0806", "SN-0836", "SN-0839"]
}
```

## LEARNING LESSON

Inherited reds are the base's debt, not the PR's fault — but only a mechanical reproduction on the unchanged base proves it. Run the test, name the owner, keep the verdict honest.

Evidence: NayaPOWER #1354 comment 6091636831 ([NAYA 4][REVIEW] Independent scorecard PR #2070, 2026-10-10T00:30:48Z — verdict HOLD 8.5, red investigated and attributed to base); comment 6091701126 (MACHINE REUSE PRINCIPLE, 2026-10-10T00:37:27Z — both reds reproduced on unchanged main `0bbc1fee`, "do not call this PR merge-qualified or blame its machine protocol for inherited test failures"). Related: SN-0806, SN-0836, SN-0839.
