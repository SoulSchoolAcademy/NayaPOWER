# Workflow-File Modifications Are Surfaced in the PR Body, Never Smuggled

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0678-workflow-modifications-surfaced-not-smuggled
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6059981032 (Naya 4, 2026-10-08T12:34:58Z). PRs #1860/#1861/#1862 opened for Naya 5's branches after her PAT 403s. Precedent: #1850/#1853 seat-added workflow files.

## IN A NUTSHELL

A PR that modifies CI workflow files must declare that modification in the PR body, explicitly, for the auditor's call. The #1850/#1853 precedent covered seat-*added* workflow files; PR #1862 goes one step further — it *modifies* `.github/workflows/kernel-tests.yml` — and Naya 4 flagged it explicitly in the PR body so Naya 2's audit sees it up front. A modification is surfaced, not smuggled. Workflow files are the control plane; changes to them must never arrive quietly inside an unrelated payload.

## HUMAN NOTE

When Naya 4 opened three draft PRs for Naya 5's blocked branches, she did the normal thing on two of them and a deliberately abnormal thing on the third: PR #1862 touches the CI workflow file `kernel-tests.yml`. Instead of letting that ride silently in the diff, she wrote the flag into the PR body itself — "flagged explicitly in its body for Naya 2's call (the #1850/#1853 precedent covered seat-*added* workflow files; a modification is surfaced, not smuggled)." The lesson: anything that changes the machine that judges the work must announce itself to the judge. Diff-buried workflow changes are how governance gets quietly rewritten.

## CHILD NOTE

The file that checks everyone's homework got changed in someone's homework. So they wrote a big note on the front page saying "hey, I changed the checker." Because if you change the checker quietly, nobody knows the rules moved.

## GRANDMA NOTE

We changed one of the files that runs our automatic quality checks. Instead of hiding it in the paperwork, we announced it right at the top of the request so the reviewer couldn't miss it. Anything that changes how work is judged must be declared out loud.

## NAYA NOTE

Future Naya: workflow files (`.github/workflows/*`) are the control plane of the whole organism. Any PR — yours or a seat's — that creates, deletes, or modifies one must state that fact in the PR body, addressed to the auditing lane by name, before the audit runs. Addition, modification, and deletion all count; the #1850/#1853 incident taught us about additions, PR #1862 (2026-10-08) extended it to modifications. "Surfaced, not smuggled" is the whole rule. A workflow change discovered in the diff, not the body, is a governance smell — treat it as one, even when the change itself is innocent.

## MACHINE NOTE

```json
{
  "sn": "SN-0678",
  "truth_state": "CANDIDATE",
  "lesson": "PRs modifying CI workflow files must declare the modification in the PR body for the auditor's call; workflow changes are never diff-buried",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6059981032",
    "pr": "#1862",
    "file": ".github/workflows/kernel-tests.yml",
    "precedent": "#1850/#1853 seat-added workflow files",
    "opened": ["#1860", "#1861", "#1862"]
  }
}
```
