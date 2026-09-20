# 🔱 NayaPOWER — Deployment Boundary Contract

**STATUS:** CANONICAL GOVERNANCE
**LAST UPDATED:** 2026-08-28
**AUTHORITY:** NayaPOWER operating system

## 1. PURPOSE

Define the boundary between NayaPOWER governance and application deployment so a governing repository is never mistaken for the deployment source of a product it governs.

## 2. SOURCE-OF-TRUTH LAW

GitHub is the engineering source of truth.

NayaPOWER governs the operating system.

Application repositories own their application source.

## 3. MAXIS DEPLOYMENT LAW

MAXIS is the application:

`SoulSchoolAcademy/Maxis`

Canonical application branch:

`main`

MAXIS Vercel project:

`maxis`

Vercel project ID:

`prj_fAd4IwSnAJAZE76DaR2AjicT2epT`

Canonical production domain:

`https://maxis.nayanet.technology`

The required deployment chain is:

**`SoulSchoolAcademy/Maxis` → `main` → Vercel project `maxis` → production → `maxis.nayanet.technology`**

### HARD RULE

> **MAXIS MUST DEPLOY FROM MAXIS. NEVER DEPLOY MAXIS FROM NayaPOWER.**

NayaPOWER is the governing repository, not the MAXIS application deployment source.

## 4. NayaPOWER DEPLOYMENT IS SEPARATE

NayaPOWER has its own Vercel project:

`naya-power`

Vercel project ID:

`prj_cHa9gwrtscCW8JuMDjcvw6DafaOK`

That project is linked to:

`SoulSchoolAcademy/NayaPOWER`

It is not the MAXIS deployment target.

## 5. VERIFIED PROJECT MAPPING

As directly verified against Vercel on 2026-08-28:

| Product | GitHub source | Vercel project | Project ID |
|---|---|---|---|
| MAXIS | `SoulSchoolAcademy/Maxis` | `maxis` | `prj_fAd4IwSnAJAZE76DaR2AjicT2epT` |
| NayaPOWER | `SoulSchoolAcademy/NayaPOWER` | `naya-power` | `prj_cHa9gwrtscCW8JuMDjcvw6DafaOK` |

The projects are correctly separated.

## 6. DEPLOYMENT VERIFICATION

Before claiming a MAXIS production deployment, verify all of the following:

1. Repository = `SoulSchoolAcademy/Maxis`.
2. Intended source ref = `main`.
3. Vercel project = `maxis`.
4. Vercel GitHub linkage = `SoulSchoolAcademy/Maxis`.
5. Deployment Git SHA = intended MAXIS SHA.
6. Deployment target = `production`.
7. Canonical URL = `https://maxis.nayanet.technology`.
8. Runtime behavior is fetched after deployment.

A preview deployment, READY state, or GitHub commit alone is not production proof.

## 7. FAILURE RESPONSE

If an executor points MAXIS deployment at NayaPOWER:

**STOP → IDENTIFY ROUTING ERROR → DO NOT MODIFY MAXIS APPLICATION CODE → RESTORE MAXIS SOURCE → TARGET VERCEL `maxis` → VERIFY DEPLOYED SHA → VERIFY PRODUCTION → VERIFY RUNTIME.**

Do not create application-code repairs for deployment-routing failures.

## 8. VERIFICATION STATES

### IMPLEMENTED
The application source contains the requested change.

### DEPLOYED
A Vercel deployment exists for the intended source.

### RUNTIME-VERIFIED
The deployed application was actually executed and observed.

### PRODUCTION-PROVEN
The canonical production target was observed running the intended source and the claimed human behavior was demonstrated.

### UNKNOWN
The required evidence does not exist.

Never convert UNKNOWN into GREEN.

## 9. CORE LAW

**NayaPOWER governs. MAXIS builds MAXIS. Vercel deploys MAXIS from the MAXIS repository. Production proves MAXIS.**
