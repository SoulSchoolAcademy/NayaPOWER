# The Base Control for a PR Red Is the Base Tip's Push-Event CI — Read It Before You Classify

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0535-base-tip-push-runs-are-the-base-control
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6036285360 (2026-10-07T10:45:44Z — [NAYA 4 / DRIVE LOOP] CI-RED classified: #1707 + #1708 (Naya 5 lane), SoulSchoolAcademy).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two Naya 5 PRs — #1707 (head `f60a77cd`, lesson index) and #1708 (head `a5d32497`, index gate) — each failed exactly one CI check: the kernel-tests.yml step running `python tools/regenerate_brain_index.py --check` (run 37571879418 / job 112632104499 and run 37571880463 / job 112632107902). The classifying cycle did not stop at the failing step. It read the **base control**: all 8 push-event CI runs on the exact base tip `e7de7b88` had completed success — which ruled out a base defect and ruled out an environmental flake in one stroke. Then it checked the PRs' changed-file lists: both contain *only* new files (1707: `.naya/index/lesson-index-20261006.json`; 1708: `.naya/specifications/P0-GATE-LESSON-INDEX-SPEC.md` + `scripts/gate-lesson-index.py`) — neither regenerates the brain index. Classification: PR-introduced SN-0213-class drift, tripwire firing correct (SN-0240), heal routed to the owning lane (Naya 5) with the exact legal repair — regen on a clean worktree at the exact head (SN-0327) — and explicitly *not* self-repaired, per the no-supersession directive.

The durable rule: **never classify a PR red from the failing job alone — read the push-event runs on the exact base tip as your base control.** All-green base + failure confined to PR-introduced artifacts → PR-introduced: heal on the PR, route to the owning lane. Red on the base tip's own push runs → base-inherited: heal the base defect once, never duplicate the repair across PRs (SN-0236). "Main looked fine last I checked" is not a control; the runs are. This is the mechanical instrument behind SN-0240's "classify before healing" and the mirror of SN-0323 (the same red at unrelated tips is the platform talking) — both need the base control read to be more than a guess.

## 🩷 HUMAN NOTE

Shawn — clean piece of triage craft from this morning's CI check. Two of Naya 5's PRs each failed one check (the brain-index drift check). Before touching anything, the cycle checked the control group: all 8 of the automated test runs on the current main tip had passed — so main was healthy and it wasn't a flaky machine. Then it confirmed both PRs only added new files without updating the index, which is exactly what the drift check is designed to catch. Verdict: the check did its job, nothing is broken on main, and the fix belongs to Naya 5's lane (regenerate the index on her branch) — routed to her, not "fixed" by someone else. Rule going forward: a failing check gets classified with evidence — read the base tip's own test runs as the control group before deciding who's broken.

## 🟣 CHILD NOTE

Imagine two kids bake cookies and the batch tastes wrong. Before blaming anyone's recipe, you taste the *control* batch — the one baked from the original recipe with no changes. If the control batch tastes fine, the problem came from one of the changes. That's exactly what happened: the automated tests on the unchanged main code all passed (the control batch was fine), and the two PRs each added new ingredients (files) without updating the shopping list (the index). So the failure came from the changes, not the kitchen. Rule: always taste the control batch before you blame the recipe — and the control batch here is the test runs on the exact unchanged code.

## 👵 GRANDMA NOTE

Think of it like a doctor diagnosing a patient. She doesn't just look at the symptom — she runs the baseline blood work first, the healthy reference, to know what's normal. Here the "blood work" was the automated tests on the unchanged main code: all healthy. With a healthy baseline, the diagnosis was clear — the two changes had each added new files without updating the master list, which is precisely what the failing check guards against. The rule we keep: diagnose against the healthy baseline, never from the symptom alone — and the healthy baseline is the test record on the unchanged code, read fresh, not remembered.

## 💜 NAYA NOTE

Note to future me: make the base-control read a mechanical step of every red classification, not a judgment call. Procedure: (1) name the exact failing step (workflow, job, run ID — e.g. kernel-tests.yml step 8, run 37571879418); (2) read the push-event runs on the PR's exact base tip — all green = control passes, any red = control fails; (3) read the PR's changed-file list — does it touch the artifact the failing check guards? Then classify: control green + PR-only cause → PR-introduced (heal on the PR, route to owning lane, never self-repair); control red → base-inherited (one repair on the defect, SN-0236, never duplicated). Record the base tip SHA and the control verdict in the classification — "base control: 8/8 push runs green on e7de7b88" is one line and it turns a guess into evidence. And when the classification says the tripwire fired correctly on real drift, say so plainly (SN-0240): a red check doing its job is not an incident.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0535",
  "rule": "base-tip-push-runs-are-the-base-control",
  "statement": "Classify a PR's CI red only after reading the push-event CI runs on the PR's exact base tip as the base control: all-green base plus PR-confined cause means PR-introduced (heal on the PR, owning lane); red base means base-inherited (heal the defect once).",
  "corollaries": [
    "Name the exact failing step: workflow, job, run ID — never 'CI is red'.",
    "Read the PR's changed-file list: does it touch the artifact the failing check guards?",
    "A tripwire firing on real drift is correct behavior (SN-0240) — classify, route to the owning lane, never self-repair another lane's branch.",
    "Record the base tip SHA and the control verdict (e.g. '8/8 push runs green on e7de7b88') in the classification."
  ],
  "source": "#1354 6036285360 (2026-10-07) — #1707 (f60a77cd) + #1708 (a5d32497) kernel-tests.yml regen --check red; base control 8/8 push runs green on e7de7b88"
}
```
