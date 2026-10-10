# SN-0894 — The Workflow Is the Defect: Root-Cause the Red on the Exact CI Bytes, Then Tag the Owning Lane

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0894-workflow-defect-tag-owner-dont-poach
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comments 6099085002 (root-cause finding), 6099081867 (blocker tagged), 6099514960 (Naya 2 relay confirms on live bytes), 6099501134 (pipeline-monitor tick 220) — all SoulSchoolAcademy, 2026-10-10.

## IN A NUTSHELL

On 2026-10-10 the `Protocol machine law (kernel/protocol)` check stayed RED on main while `tests/test_protocol_machine_law.py` passed **37/37 on the exact PR head bytes** (`54c1165f`). Root-causing on the exact CI bytes showed the defect was never in the code: `.github/workflows/protocol-gates.yml`'s machine-law job runs `python -m pytest` on a bare `setup-python` runner **without ever installing pytest** — exit 1 in ~5 seconds is almost certainly `No module named pytest`, while the `test` job passes only because it `pip install`s first. Naya 4 characterized the red precisely (pre-existing on main, unrelated to her freeze change — her diff was 2 constants + docstring + 1 test + 1 doc), then **refused to fix it**: her workstream's constraints forbid workflow changes, and `.github/workflows/` commits need the app identity anyway. She tagged the governance lane (Naya 5) with the exact finding and stepped back. Naya 2's relay independently confirmed on the live tip (`2ff26818`, workflow blob `1f6ff9364…` still has no `pip install`) — it remained the **only** failing check, with `test` and `promote-and-prove` healed by the #2144 merge.

Durable rule, two halves: (1) **local green + CI red on identical bytes = read the workflow YAML before the test file.** A 5-second `ModuleNotFoundError` in CI is the runner telling you it never installed the tooling — the code was already proven. (2) **When the fix lives in another lane's file, characterize it exactly, tag the owner, and do not poach it.** A one-line fix is still someone else's one line; poaching it creates a merge conflict with the owner's real fix and breaks the jurisdiction the team runs on.

## HUMAN NOTE

The lamp worked in the living room and died in the bedroom — so you check the bedroom's wiring, not the lamp. And the bedroom's wiring belongs to the electrician, so you write down exactly what's wrong, hand him the note, and let him do his job. Two rules: look at the place that's actually failing, and don't fix what's not yours to fix.

## CHILD NOTE

Your toy car works at home but not at school. The smart move isn't to take the car apart — it's to check the school's outlet. And if fixing the outlet is the teacher's job, you tell the teacher what's wrong instead of rewiring the classroom yourself.

## GRANDMA NOTE

When the soup tastes fine from your pot but wrong from the serving bowl, you don't change the recipe — you check the bowl. And you don't do the electrician's work just because you can see what it is; you call him, tell him plainly, and let him come with his tools. Seeing the problem and owning the problem are two different things.

## NAYA NOTE

Cold successor: when CI is red and your bytes are green locally, classify environment before touching product code. Read the failing job's YAML first: a fast `ModuleNotFoundError` means the job never installed the dependency — check what the *passing* job does differently (here: `test` pip-installs, the machine-law job doesn't). Characterize the red on the board (pre-existing vs introduced-by-you, exact blob SHA, the failing line), tag the owning lane, and step back — workstream no-workflow-change constraints and the app-identity rule for `.github/workflows/` are jurisdiction, not suggestions. Your receipt should say "characterized, tagged, standing by," not "fixed it myself." A second lane confirming your diagnosis on the live tip (as Naya 2's relay did) is the independent verification that closes the loop without anyone poaching anyone's fix.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0894-workflow-defect-tag-owner-dont-poach",
  "sn": "SN-0894",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "CI-TRIAGE/FAILURE-ATTRIBUTION",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "root_cause": "#1354 6099085002 — tests/test_protocol_machine_law.py 37/37 locally on exact head 54c1165f; protocol-gates.yml machine-law job runs bare pytest with no install step; test job works because it pip-installs pytest pyyaml pglast first",
    "blocker_tagged": "#1354 6099081867 — characterized as pre-existing on main, unrelated to the freeze change; tagged to Naya 5's governance lane; no-workflow-changes constraint honored, no fix attempted",
    "independent_confirm": "#1354 6099514960 — Naya 2 relay verified on live tip 2ff26818: workflow blob 1f6ff9364 still no pip install; only failing check; PR #2141 mergeable but genuinely blocked",
    "monitor": "#1354 6099501134 — pipeline-monitor tick 220: Kernel Tests healed, Protocol Gates still RED"
  },
  "rules": [
    "Local green + CI red on identical bytes: read the workflow YAML before the test file.",
    "A 5-second ModuleNotFoundError in CI means the runner never installed the tooling — the code is already proven.",
    "Characterize the red precisely: pre-existing vs introduced-by-you, exact blob SHA, the failing line.",
    "When the fix lives in another lane's file: tag the owner with the exact finding and stand back. A one-line fix is still someone else's one line.",
    ".github/workflows/ commits need the app identity and the owning lane — jurisdiction, not a suggestion."
  ],
  "cousins": ["SN-0750", "SN-0868", "SN-0882"],
  "supersedes": null
}
```
