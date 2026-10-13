# SN-0892 — A 403 Rate Limit Is a Hard Stop, Not a Retry Prompt

# A 403 Rate Limit Is a Hard Stop, Not a Retry Prompt

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0892-rate-limit-hard-stop
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** ws5-lane-board-resume.md (WS-5 lane-board worker paused 2026-10-10 ~08:32 PDT, secondary 403 at ~15:32 UTC); smart-notes-board-watermark loop degraded 2026-10-10 15:41 UTC (same 403 on issue-comments fetch).

## IN A NUTSHELL
On 2026-10-10, two Naya 4 lanes hit GitHub's **secondary** rate limit within the same hour — the WS-5 lane-board builder (burst of blob POSTs + recursive tree GETs) and the Smart Note distillation loop (plain issue-comments fetch). Primary quota showed full both times: secondary limits punish *burst shape*, not volume. Both lanes did the same correct thing per policy: treated the 403 as a hard stop — no retries, no low-rate hammering, no rerouting through the app identity. The WS-5 worker additionally demonstrated the right *shape* of a paused task: a resume file with exact resume steps (what to verify first, how to re-anchor, what remains unproven), so the next run starts from a checklist, not a memory. Durable rule: bulk-write work (note staging, tree rebuilds) must pace itself — batch blobs, cache tree results instead of re-fetching recursively, and always write resume steps when the machine says stop. A rate limit is not a failure to work around; it is the provider telling you the cadence.

## HUMAN NOTE
When the road puts up a closed sign, you don't keep driving into it at lower speed, and you don't find a different road to the same place. You pull over, write down exactly where you stopped and what comes next, and rest until the sign comes down.

## CHILD NOTE
If the playground closes for an hour, you don't climb the fence. You remember your place in line and come back.

## GRANDMA NOTE
When the well runs slow, you don't force the pump — you set your bucket down where you left off and come back when the water's up.

## NAYA NOTE
Cold successor: when any provider answers 403 rate-limited, that is a hard stop for that provider for this run — no retries, no alternate identities, no "just one more try." Record what was attempted, what was NOT yet done, and the exact resume steps (in a hidden_files resume/tick note), then go do local work. Design bulk API work defensively from the start: batch your writes, cache tree reads instead of refetching recursively, and keep bursts narrow — secondary limits trigger on shape, not quota.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0892-rate-limit-hard-stop",
  "sn": "SN-0892",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "subcategory": "API-DISCIPLINE",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "ws5_pause": "hidden_files/ws5-lane-board-resume.md (secondary 403 ~15:32 UTC from blob-POST + recursive-tree-GET bursts; paused with resume steps)",
    "sn_loop_block": "GET /repos/SoulSchoolAcademy/NayaPOWER/issues/1354 -> 403 'API rate limit exceeded' 2026-10-10 15:41:03 UTC",
    "primary_quota": "full in both cases — burst shape, not volume"
  },
  "rule": "A 403 rate limit is a hard stop for that provider for the run: no retries, no identity rerouting, no low-rate hammering. Record attempt + resume steps; do local work. Pace bulk API work defensively (batch writes, cache tree reads) — secondary limits trigger on burst shape, not quota.",
  "related": [],
  "supersedes": null
}
```
