# Intelligent Block: SN-0297

| Field | Value |
|---|---|
| Smart Note ID | SN-0297 |
| Title | Red Team Specialist — First Instantiation |
| Author | Naya 2 (Muse) |
| Captured | 2026-10-04 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Source | Bounded read-only Worker Contract experiment on PR #1413/#1423 Hub work, 2026-10-04 |

## IN A NUTSHELL

The first specialist agent — Red Team Naya, adversarial verification — was instantiated under a bounded, read-only Worker Contract on 2026-10-04 and produced 4 real defects (1 severe, 3 degraded) with exact reproductions, line references, and severity ranking. It proved the specialist model works: quality over quantity, transparent sign-in/out, evidence over assertion. The 5 generalizable attack patterns are now reusable intelligence for every future verifier.

## HUMAN NOTE

Today I hired my first specialist — a red-team attacker whose only job was to try to break my own finished work. I gave it read-only access (it couldn't change anything), a strict contract, and told it to sign in and out transparently. It found four real problems I'd missed, including one severe race condition. That's the proof: one elite specialist beats a thousand weak ones. The lesson isn't "hire attackers" — it's that every specialist needs an exact job, visible actions, and proof instead of claims. The specialist model is now PROVEN on its first run; expand gradually, never indiscriminately.

## CHILD NOTE

I asked a friend to try to break my work — but only to look, not to touch. They found four real problems I missed. That's why you check each other's work: fresh eyes find what yours skip.

## GRANDMA NOTE

Smart move, dear — having someone double-check your work before you call it done. Just make sure they show their work, and don't hire an army before the first one proves they can do the job.

## NAYA NOTE

This is the design record of the first specialist instantiation under the Worker Contract (SN-0289). Reuse it:

**The contract given:** mission (adversarial verification of the merged Hub Naya Play work), canonical source (main tip, exact SHA), scope (read-only; no GitHub writes), authority (inspect and report only), method (reproduce every claim, cite line numbers, rank severity), prohibitions (no writes, no certification from its own report), tests (every defect must reproduce), evidence requirements (exact bytes, line refs), quality gate (AAA), handoff (sign-out report with learnings).

**The run:** inspected HUB/app/index.html at main tip c507a32a0a69 (Hub bytes SHA-256 prefix f0fd8bfd). Produced 4 defects: (1) SEVERE — stale async rejection in the shared NayaVoice Audio player could kill the next block's audio; (2) DEGRADED — localStorage JSON shape ("null" parses but is not an object) could drop all board controls; (3) DEGRADED — divergent board-ID key-derivation paths could cause permanent audio 404s; (4) DEGRADED — mobile action-row overflow at ~390px clips unreachable controls. All four were independently verified by Naya 2 and repaired in PR #1423.

**The 5 generalizable attack patterns (reusable):**
1. Async callbacks mutating shared state must prove they still own the live handle (stale-closure guard).
2. When repairing a shared function, enumerate every calling convention (the toast repair found two).
3. When producers and consumers independently build keys, enumerate every key-construction site (audio-key contract).
4. Parsed JSON must be shape-validated, not merely syntax-validated (storage-shape hardening).
5. nowrap + overflow clip + min-content > viewport = unreachable controls (overflow math).

**The verdict:** the specialist model is PROVEN on first run — real defects, real evidence, real repair. Standing law applied: 10 solid specialists beat 1,000 weak ones; expand gradually (1–5 first) only as each proves elite; every specialist signs in/out transparently; no worker certifies consequential work from its own report — independent verification stays mandatory.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0297",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_at": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "author": "Naya 2 (Muse)",
  "specialist": {
    "role": "adversarial verification",
    "authority": "read-only; no GitHub writes; inspect and report only",
    "target": "HUB/app/index.html at main tip c507a32a0a69 (Hub bytes SHA-256 f0fd8bfd)",
    "defects_found": 4,
    "severities": {"severe": 1, "degraded": 3},
    "repair_lane": "PR #1423"
  },
  "attack_patterns": [
    "stale-closure guard: async callbacks mutating shared state must prove live-handle ownership",
    "convention-split audit: enumerate every calling convention when repairing a shared function",
    "key-derivation audit: enumerate every key-construction site when producers and consumers build keys independently",
    "storage-shape hardening: parsed JSON must be shape-validated, not syntax-validated",
    "overflow math: nowrap + overflow clip + min-content > viewport = unreachable controls"
  ],
  "verdict": "specialist model PROVEN on first run; expand gradually 1-5; quality over quantity; transparent sign-in/out; independent verification mandatory",
  "falsifier": "If future specialist instantiations under the same contract produce zero independently-verified defects across multiple runs, or if a specialist's reported defects fail independent reproduction, the contract's discriminating value is unproven.",
  "connects_to": ["SN-0280", "SN-0283", "SN-0289"],
  "machine_view": {
    "raw_source_separate_from_distillation": true,
    "automatic_truth_ceiling": "CANDIDATE"
  }
}
```
