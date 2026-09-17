# NIGHT 07 — RELEASE AUTHORITY AND LIVE PROOF

## DIRECT COMMAND

Naya Release: reconcile the release lane and prove reality. Do not deploy merely because deployment is possible.

### OBJECTIVE
Establish one evidence-backed path:
`CANONICAL SOURCE SHA → BUILD → TEST → AUTHORIZED DEPLOY → LIVE PROBE → SOURCE/ARTIFACT MATCH → RECORD`

### REQUIRED WORK
1. Enumerate every active workflow that can mutate/build/deploy Hub artifacts.
2. Identify which one is actually authoritative.
3. Identify conflicting Assistant/Cloudflare/Vercel/GitHub lanes.
4. Preserve fail-closed boundaries where authority is unresolved.
5. Verify source commit identity through build artifacts.
6. Run deterministic tests before deployment.
7. Deploy only through the authorized lane.
8. Probe the actual live endpoint.
9. Compare live behavior/artifact identity with expected source.
10. Record deployment result and verification status separately.

### STATUS LANGUAGE
Use only:
- IMPLEMENTED
- TESTED
- INDEPENDENTLY VERIFIED
- LIVE VERIFIED
- BLOCKED
- UNKNOWN

Never convert BLOCKED or UNKNOWN into GREEN by narrative.

### ACCEPTANCE
There is one clearly identified release authority, or the system remains deliberately blocked with the exact missing authority recorded. If deployed, live behavior must be directly verified against the intended source.

### RECEIPT
Record exact workflow, commit, artifact, runtime URL, probe result, and evidence. Then successor: **NIGHT 08 FINAL ADVERSARIAL + COLD NAYA**.