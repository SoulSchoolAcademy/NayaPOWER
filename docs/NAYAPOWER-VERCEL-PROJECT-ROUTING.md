# 🔱 NayaPOWER — Vercel Project Routing Law

**STATUS:** CANONICAL CROSS-PROJECT DEPLOYMENT GUARDRAIL
**LAST CONFIRMED:** 2026-08-28

## PROBLEM

A governance/source-of-truth confusion can cause an executor to attempt to deploy MAXIS through the NayaPOWER Vercel project merely because NayaPOWER governs MAXIS.

That is incorrect.

## SOLUTION

Separate **governance authority** from **application deployment ownership**.

- NayaPOWER governs the operating system and cross-project rules.
- MAXIS owns the MAXIS application source.
- The MAXIS Vercel project deploys MAXIS.
- The NayaPOWER Vercel project deploys NayaPOWER.

## CANONICAL ROUTING

### MAXIS

`SoulSchoolAcademy/Maxis` → `main` → Vercel `maxis` → `maxis.nayanet.technology`

Vercel project ID:
`prj_fAd4IwSnAJAZE76DaR2AjicT2epT`

### NayaPOWER

`SoulSchoolAcademy/NayaPOWER` → its own Vercel project `naya-power`

Vercel project ID:
`prj_cHa9gwrtscCW8JuMDjcvw6DafaOK`

## HARD RULE

**NEVER DEPLOY MAXIS FROM NayaPOWER.**

When the requested product is MAXIS, the first deployment source check must resolve:

`SoulSchoolAcademy/Maxis`

Then the Vercel project must resolve to:

`maxis`

If those identities do not match, STOP and resolve the routing contradiction before changing application code.

## FAILURE → SOLUTION

**Wrong source/project**
→ deployment routing error
→ do not edit MAXIS code
→ restore `SoulSchoolAcademy/Maxis`
→ target Vercel project `maxis`
→ verify Git SHA
→ verify production target
→ verify runtime.

## WHY THIS MATTERS

A governing repository is not automatically the deployment repository for every application it governs.

Confusing those roles creates false blockers, wasted engineering effort, and potentially deploys the wrong product.

## VERIFICATION

The mapping was directly confirmed against Vercel on 2026-08-28:

- `maxis` is linked to `SoulSchoolAcademy/Maxis`.
- `naya-power` is linked to `SoulSchoolAcademy/NayaPOWER`.

This is the canonical routing rule for future Naya execution.
