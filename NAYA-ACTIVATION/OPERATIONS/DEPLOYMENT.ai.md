# DEPLOYMENT — AI TONGUE

**Source (human tongue):** `NAYA-ACTIVATION/OPERATIONS/DEPLOYMENT.md`
**Machine tongue:** `NAYA-ACTIVATION/OPERATIONS/deployment.machine.json`

## Rule

Deployment is a boundary, not proof.

## Order (exact)

SOURCE → TEST → REVIEW → AUTHORIZED DEPLOY → RUNTIME VERIFY → RECORD

## Evidence semantics

A deployment receipt proves deployment occurred. It does not by itself prove production behavior.

If production parity fails, investigate the actual request and runtime contract. Do not weaken acceptance gates to obtain a green result.

**Production claims require production evidence.**
