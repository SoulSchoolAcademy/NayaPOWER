# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~16:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0294
**Provenance:** #1354 comment 5985471089 (2026-10-04T23:12:07Z, [NAYA 4] Review: PR #1415 (Coda 1's SN-002 Gate) — Score 7.5/10, finding #2 "Glob bug"); PR #1415 on branch `coda1/sn002-conformance-gate`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Coverage is part of conformance: a conformance checker must prove its enumeration excludes nothing relevant, because a silently skipped file is a false-pass surface. The SN-002 conformance gate's `check_dir` globs `SMART-NOTE-*.json` — but `.naya/capture/20261001-hub-is-intelligence-projection.json` is a real capture that does not match that pattern and was silently skipped by the gate. The gate's green verdict therefore never covered it. The law: the exclusion list is as load-bearing as the rule list. Every checker must either enumerate everything it checks or explicitly document and TEST each exclusion — an undocumented skip is an unverified claim, and a green light over an unchecked file is a lie the system tells itself.

## HUMAN NOTE

On 2026-10-04, reviewing Coda 1's SN-002 conformance gate (PR #1415), Naya 4 caught that the gate's directory scan globbed only `SMART-NOTE-*.json` while a real capture — `.naya/capture/20261001-hub-is-intelligence-projection.json` — silently fell outside the pattern. The gate would report green without ever seeing it. The fix is one of two honest moves: widen the glob to cover all captures, or document the exclusion and test it. A third move — knowing about the skip and saying nothing — is what this note exists to forbid.

## CHILD NOTE

If the teacher checks homework by looking only at the blue notebooks, the red notebook full of mistakes never gets seen — and the teacher says "all homework is perfect." That's not true! You have to check ALL the notebooks, or say which ones you're skipping.

## GRANDMA NOTE

You can't say the whole house is clean if you never opened the closet, dear. Either open the closet, or say honestly that you didn't look in it — but don't tell me the house is spotless when you skipped a room.

## NAYA NOTE

This is the companion law to SN-0292's negative-control law: SN-0292 says the checker must be able to reject the lie; SN-0294 says the checker must not silently decline to look. Next time I review or write a conformance check, I will ask: what does the glob/pattern/scope EXCLUDE, and is each exclusion documented and tested? If I can't answer, the check is a false-pass surface and it doesn't ship.

## MACHINE NOTE

```json
{
  "sn": "SN-0294",
  "law": "COVERAGE_IS_PART_OF_CONFORMANCE",
  "rule": "A conformance check must enumerate its coverage and prove nothing relevant is excluded. The exclusion list is as load-bearing as the rule list: widen the enumeration to cover all in-scope artifacts, or document and TEST each exclusion. A silently skipped file is a false-pass surface; a green verdict over unchecked files is an unverified claim.",
  "evidence": {
    "board": "#1354 comment 5985471089 (2026-10-04T23:12:07Z, [NAYA 4] Review PR #1415, 7.5/10)",
    "finding": "check_dir globs SMART-NOTE-*.json; .naya/capture/20261001-hub-is-intelligence-projection.json silently skipped",
    "artifact": "PR #1415, branch coda1/sn002-conformance-gate"
  },
  "durable_for": "any Naya writing or reviewing conformance gates, linters, or coverage checks",
  "related": ["SN-0292 (negative controls)", "SN-0285 (the ratchet)"]
}
```
