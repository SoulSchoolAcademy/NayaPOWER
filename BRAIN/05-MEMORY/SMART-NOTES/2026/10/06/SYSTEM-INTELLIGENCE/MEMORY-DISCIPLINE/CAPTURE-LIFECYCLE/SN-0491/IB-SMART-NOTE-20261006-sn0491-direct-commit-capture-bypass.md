# IB-SMART-NOTE-20261006-sn0491-direct-commit-capture-bypass

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0491-direct-commit-capture-bypass |
| Smart Note | SN-0491 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

SN-0459 exists in git history — Shawn committed it directly to main himself — yet it has no registry entry and no JSON capture, which REDs the main tip right now. Direct-to-main commits bypass the staging pipeline's lifecycle steps entirely. Every landed intelligence artifact still needs registry entry + capture; the lifecycle tripwire must fire on the tip, not only on PRs. The file is in the building — the paperwork was never filed.

## HUMAN NOTE

Shawn himself walked a Smart Note straight into main — no PR, no pipeline. The file landed perfectly. But the registry and the JSON capture, the two pieces of paperwork the system needs to know the note exists, were never created. So the tests that guard "ratified intelligence cannot vanish" are failing on the live tip right now: the note is in git history but invisible to the machinery. Landing the file is only half the job. The lesson: any path that skips the pipeline still owes the pipeline's paperwork — or the tripwire has to catch it on the tip afterward.

## CHILD NOTE

If you walk your homework straight to the teacher's desk but skip the sign-in sheet, the teacher can't find it later even though it's right there. Walking it in doesn't count as signing in. You have to do both, or the office has to check the desk at the end of the day and sign it in for you.

## GRANDMA NOTE

Mailing the letter and the post office logging it are two jobs. If you hand-deliver the letter and skip the post office, there's no tracking number — and when someone asks "did it arrive?", nobody can prove it. Hand delivery is fine, but the ledger still needs its entry.

## NAYA NOTE

Lifecycle steps are tied to landings, not to PRs. Any commit that lands intelligence on main — including the Director's own direct commits — must produce the full lifecycle tail: file + registry entry + JSON capture in CAPTURE_DIR. When the landing path bypasses the staging pipeline, the exact-tip battery is the backstop: `test_ratified_intelligence_cannot_vanish` and the registry-drift checks fire on tip bytes, which is exactly what caught SN-0459's missing paperwork. Fix protocol: the owning lane registers the note and creates the capture (PR #1657 carries the SN-0459 capture as part of its superset). Never absorb the anomaly to silence the tripwire (SN-0420) — the test firing on a real gap is correct behavior (SN-0240).

## MACHINE NOTE

```json
{
  "rule": "direct_commit_owes_pipeline_paperwork",
  "lifecycle_tail": ["file_on_disk", "registry_entry", "json_capture_in_CAPTURE_DIR"],
  "backstop": "exact-tip battery (test_ratified_intelligence_cannot_vanish, registry-drift checks) fires on tip bytes regardless of landing path",
  "family": ["SN-0213-index-regen-in-landing-step", "SN-0327-never-regen-dirty-worktree", "SN-0240-tripwire-on-real-drift", "SN-0420-never-absorb-anomaly"],
  "evidence_class": "failure_classification",
  "falsifier": "a direct commit whose file exists on main with registry entry and capture both present"
}
```

## EVIDENCE

- #1354 comment 6025585185 (Naya 4, 2026-10-06 14:09 PDT): main tip `1204519c` RED on `test_ratified_intelligence_cannot_vanish` — SN-0459 exists in git history (Shawn's direct commit `1f99d2b` "docs(memory): SN-0459 parallel-execution directive"; file present at `BRAIN/05-MEMORY/SMART-NOTES/2026/10/06/SYSTEM-INTELLIGENCE/EXECUTION/SN-0459/`) but has NEITHER a registry entry NOR a JSON capture in CAPTURE_DIR. Owning lane must register the note or create the capture. Classified per SN-0240 as base defect, not self-repaired.
