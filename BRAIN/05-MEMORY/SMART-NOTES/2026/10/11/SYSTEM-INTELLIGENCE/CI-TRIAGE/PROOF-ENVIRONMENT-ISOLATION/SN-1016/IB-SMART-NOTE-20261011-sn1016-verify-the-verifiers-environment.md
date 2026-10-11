# SN-1016 — The Verifier's Own Environment Is a Failure Layer

- **Intelligent Block:** IB-SMART-NOTE-20261011-sn1016-verify-the-verifiers-environment
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured date:** 2026-10-11
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Category:** SYSTEM-INTELLIGENCE / CI-TRIAGE / PROOF-ENVIRONMENT-ISOLATION
- **Provenance:** verify-driver-run-2026-10-11-pm.md (2026-10-11 15:08–15:50 PDT window), finding 3; repair PR #2392 (DRAFT, branch `verify/guard-liveness-interpreter` @ `5a5708c4`, builder scorecard 8.5/10, cross-seat review requested; no merge — freeze holds).

## IN A NUTSHELL

Independent tip classification at `f33bba34` hit a CI RED on the guard_liveness check. The driver reproduced it locally and read the actual error: the test hardcodes `execFileSync("python", ...)` — and this VM has **no `python` binary, only `python3`**. The verifier itself was unexecutable on the machine running it. Classified honestly: **ENVIRONMENTAL, not content**. The driver ran `python3 tools/guard_liveness.py --json` directly → works (170 guards, 75.9%), separated the finding, and did not misreport it as a defect. CI's real step-4 failure was separately explained (finding 2: load-bearing CLAIM 3 moved by the #2384 merge — the actual content defect). Then the hole was executed: runtime interpreter resolution (prefer `python` → today's CI behavior unchanged; fall back to `python3`), mirroring the doctrine already in `load_bearing_claims.test.mjs`. Proven: python3-only VM 7/7 pass (was 6 fail); with a `python` shim in PATH → resolver picks `python`, 7/7 pass.

The durable rule: when a gate fails, **reproduce the exact command and read the exact error before attributing the failure to the code under test**. The failure can live inside the verifier's own assumptions — toolchain availability, PATH, working directory, disk — and a verifier that hardcodes its toolchain lies on any machine that doesn't have it. **Verify the verifiers.** (Companion to SN-0995's triage grammar and SN-0960's disk rule: the proof mechanism's environment is its own failure layer.)

## HUMAN NOTE

Shawn — the verifier team found a check failing and, instead of blaming the code, looked at the check itself: the test demanded a program (`python`) this machine doesn't have — the machine has `python3`. So the check could never pass here, no matter how good the code was. They fixed the check to accept either one, proved it both ways (seven for seven), and opened a draft fix for review. The lesson for the whole team: when a test fails, check whether the *test itself* is broken before you blame the work it was testing.

## CHILD NOTE

Your homework was marked wrong — but the teacher's red pen had run out of ink, so she couldn't read your answers at all. The homework wasn't wrong; the *pen* was. Smart students ask to see the actual marking before they redo their homework.

## GRANDMA NOTE

Dear, it's like a thermometer that reads wrong in cold weather — you don't conclude the patient is sick, you check the thermometer. The team found one of their measuring tools was built assuming something about the room it would be used in. They fixed the tool, not the patient — and wrote it down so the next nurse doesn't take the patient's temperature with a broken thermometer.

## NAYA NOTE

Cold successor, the failure-layer ladder is: **content → gate logic → gate input → proof environment → verifier's own assumptions**. SN-0995 gives you the first three. This note gives you the last two, with the specimen: `execFileSync("python", ...)` on a python3-only VM. The protocol: (1) run the exact failing command yourself; (2) read the exact stderr; (3) if the error names a missing toolchain/binary/path/disk, the failure is environmental — say so explicitly and do not attribute it to the merge under test; (4) fix the verifier (runtime resolution, fallbacks), mirroring the existing doctrine in `load_bearing_claims.test.mjs`, never a hardcoded path. The environment of the proof is part of the proof.

## MACHINE NOTE

```json
{
  "id": "SN-1016",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/PROOF-ENVIRONMENT-ISOLATION",
  "specimen": {
    "verifier": "tests guard_liveness",
    "hardcode": "execFileSync(\"python\", ...)",
    "vm_toolchain": "no `python` binary; `python3` only",
    "classification": "ENVIRONMENTAL, not content",
    "direct_run": "python3 tools/guard_liveness.py --json → 170 guards, 75.9%",
    "ci_step4_real_cause": "finding 2 — load-bearing CLAIM 3 behavioral delta from PR #2384 merge"
  },
  "repair": {
    "pattern": "runtime interpreter resolution (prefer `python`, fall back `python3`)",
    "mirrors": "doctrine already in load_bearing_claims.test.mjs",
    "branch": "verify/guard-liveness-interpreter",
    "head": "5a5708c4",
    "pr": "#2392 (DRAFT, builder scorecard 8.5/10, cross-seat review requested, no merge — freeze holds)",
    "proof": "python3-only VM 7/7 pass (was 6 fail); with `python` shim in PATH → picks `python`, 7/7 pass"
  },
  "companion_notes": ["SN-0995 gate-failure triage grammar", "SN-0960 disk-first environmental rule"],
  "provenance": "verify-driver-run-2026-10-11-pm.md, 2026-10-11 15:08–15:50 PDT window"
}
```
