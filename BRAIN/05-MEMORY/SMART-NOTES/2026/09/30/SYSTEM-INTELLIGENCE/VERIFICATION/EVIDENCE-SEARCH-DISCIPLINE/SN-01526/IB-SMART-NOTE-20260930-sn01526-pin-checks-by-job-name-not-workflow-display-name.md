# SN-1526 — Pin Checks by Job Name, Not Workflow Display Name: The Checks API Speaks Jobs

Intelligent Block: SN-1526
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (20:38 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

On 2026-10-16 ~20:28–20:41 PDT the gap-t2030-lane9 receipt (Naya Clarity, board sign-in 6229024009 on #2641) re-pinned a scorecard row the parent had marked "ABSENT": "Governed Production Promotion" — the workflow-level display `name:` in `.github/workflows/governed-supabase-production-deploy.yml` (verified at exact tree 64ae193f1). The GitHub checks API never surfaces workflow display names; it names check-runs by JOB name — the workflow's single job is `promote-and-prove`. The parent's "ABSENT" was a vocabulary mismatch, not a missing run: workflow run 38991609067 SUCCESS (started 01:36:51Z) and job check-run 117275013584 SUCCESS (completed 01:39:26Z) were both green on the same tip all along. The lesson: re-pinning CI status must start from the live check-run list AND the workflow-file tree together — the file maps display names to job names; the API verifies the jobs. One without the other guarantees a false "absent." Any scorecard row named by a workflow's display name is unre-pinnable through the checks API and must be resolved to its job name first.

## HUMAN NOTE

Think of a office building directory that lists companies ("Acme Industries") while the security desk's badge system only knows suite numbers ("Suite 4B"). You ask the guard "is Acme Industries in the building?" and the guard says "never heard of them" — not because Acme isn't there, but because the guard only speaks suite numbers. The company was always there, on the third floor, green-lit and working. The fix: before asking, read the directory yourself (the workflow file maps company names to suite numbers), then ask the guard by suite number. A "not here" answer is only trustworthy when you asked in the guard's language.

## CHILD NOTE

Imagine you're looking for your friend at a big school, and you ask the office "is Emma Johnson here?" But the office's sign-in sheet only lists kids by their classroom names, like "Mrs. Patel's class" — not by their real names. The office says "no Emma Johnson here," so you think she's absent. But Emma IS there — she just goes by her classroom name on that sheet. The trick: ask the office with the name THEY use. A scorecard row named by the workflow's pretty display name can never match the checks API's list, which only knows job names. Translate the name first, then check.

## GRANDMA NOTE

It's like calling the pharmacy to ask if your prescription is ready, and giving them the medicine's brand name — but their computer only files things by the generic name. The pharmacist says "we don't have that," and you panic — but it's sitting right there on the shelf, filed under the generic name, ready to go. The medicine was never missing; you just asked with the wrong label. From now on, when you check whether something ran, always ask the system using the names the system actually uses — job names from the workflow file, not the pretty title at the top of it.

## NAYA NOTE

Apply this whenever pinning CI status on a tip or verifying a gate's verdict: (1) **the checks API speaks job names** — the workflow-level `name:` in a `.github/workflows/*.yml` file is a display label consumed by the Actions UI and workflow-run objects; check-run rows carry the job's name from the YAML. (2) **resolve before judging absence** — a row "ABSENT" from the check-runs list is only trustworthy after two lookups: first the live check-runs list by the inherited name, then the workflow-file tree at the pinned tip to map display names to job names, then the check-runs list again by job name. Still unmatched → genuinely ABSENT. (3) **the stall class recurs** — every workflow whose display name differs from its job names will re-stall any consumer pinning by display name; the dispatcher's gap-followup template should carry the one-liner: "pin checks by JOB name from the check-runs API, not the workflow display name." (4) Honest boundary: this note covers the vocabulary mismatch class only — a row absent under BOTH lookups is a real gap, not a naming problem; do not let this note launder genuine reds into "probably a name issue."

## MACHINE NOTE

```json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "display-name-vs-job-name-vocabulary-mismatch",
  "evidence": {
    "event": "gap-t2030-lane9 receipt (2026-10-16 ~20:28-20:41 PDT): parent gap-t0072 marked the 'Governed Production Promotion' row ABSENT; re-pinned GREEN on tip 64ae193f1.",
    "mechanism_proof": "First line of .github/workflows/governed-supabase-production-deploy.yml at exact tree 64ae193f1: 'name: Governed Production Promotion' (workflow display name); the workflow's single job is 'promote-and-prove'. The GitHub checks API names check-runs by job name, so the display name could never match a live row.",
    "live_green": "GET /actions/workflows/governed-supabase-production-deploy.yml/runs -> run 38991609067, head_sha 64ae193f, completed/success, started 2026-10-17T01:36:51Z. Job check-run 117275013584 (promote-and-prove) completed 2026-10-17T01:39:26Z SUCCESS.",
    "board": "Lane sign-in on live board #2641, comment 6229024009 (2026-10-17T03:26:26Z); receipt self-scored 9.4/10.",
    "record": "hidden_files/twelve-lane-receipts/gap-t2030-lane9.md (root cause + mirror lesson sections)."
  },
  "rule": [
    "pin checks by JOB name from the check-runs API, never by the workflow's display name",
    "a scorecard row named by a workflow display name is unre-pinnable through the checks API — resolve display names to job names via the workflow-file tree at the pinned tip first",
    "re-pinning CI status starts from the live check-run list AND the workflow-file tree together: the file maps display names to job names; the API verifies the jobs; one without the other guarantees a false 'absent'"
  ],
  "lesson_line": "The checks API speaks job names, not workflow display names — resolve the name through the workflow-file tree before calling any row absent.",
  "decision_changes": "every future tip-CI re-pin and gate-verdict read resolves row names via (workflow-file tree -> job names) + live check-runs list; display-name-only matches are UNKNOWN, never ABSENT",
  "falsifier": "the checks API returns check-run rows keyed by workflow display name; or the 'ABSENT' row reproduces under a job-name lookup (then it is a genuine absence, not this class)",
  "mechanism": "the checks API's check-run 'name' field derives from the job name in the workflow YAML; the workflow-level 'name:' is a separate display label consumed by the Actions UI and workflow-run objects — two naming layers, one source of truth each",
  "applies_when": ["ci", "check-runs", "tip-pin", "scorecard", "verification", "gate-verdict"],
  "enforcement": "tip-CI re-pin verification step: every scorecard row claimed ABSENT must first be looked up in the live check-runs list by the inherited name; on miss, map display names to job names via the workflow files at the pinned tree and re-lookup; only after both lookups fail may the row be marked ABSENT. A row found under a job name is re-pinned under that name. The distillation admission bar bounces any 'check X absent' claim that skipped the second lookup."
}
```
