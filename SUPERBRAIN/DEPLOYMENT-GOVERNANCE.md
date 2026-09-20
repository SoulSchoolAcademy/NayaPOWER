# 🔐 NayaPOWER Deployment Governance

**STATUS:** CANONICAL / ACTIVE
**SCOPE:** NayaPOWER repository, GitHub automation, and connected Vercel project
**AUTHORITY:** NayaPOWER control plane

## 1. Core Law

> **A repository change is not a release.**

GitHub is the canonical source of truth. Vercel is connected deployment infrastructure. Repository activity MUST NOT automatically become publication.

The default state for deployment is **DENY**.

## 2. Separation of Concerns

- **GitHub:** source, history, governance, artifacts, evidence.
- **NayaPOWER:** authorization and execution policy.
- **CI:** verification and regression proof.
- **Vercel:** deployment target only when explicitly authorized.
- **Production:** an explicit release outcome, never an incidental side effect.

## 3. What Does NOT Constitute a Release

The following do not authorize a Vercel preview or production deployment by themselves:

- documentation changes;
- Smart Notes / Naya Notes;
- governance or constitutional changes;
- architecture specifications;
- schemas;
- tests;
- research;
- control-plane state;
- ordinary source changes;
- commits or pushes;
- pull requests;
- branch creation or updates.

A change can be deployable only when the release contract explicitly authorizes it.

## 4. Release Authorization Contract

The canonical contract is:

`.naya/control-plane/RELEASE-AUTHORIZATION.json`

A valid release authorization MUST identify:

1. exact repository;
2. exact commit SHA;
3. target environment (`preview` or `production`);
4. deployment surface (`vercel`);
5. release reason;
6. verification evidence and PASS status;
7. authorized actor;
8. authorization timestamp;
9. explicit approval state.

A template, incomplete record, stale SHA, missing evidence, or ambiguous approval is **DENY**.

## 5. Environment Policy

### Preview

Default: **DENY**.

Preview deployment requires an explicit release authorization naming `preview` as the target environment.

### Production

Default: **DENY**.

Production deployment requires an explicit release authorization naming `production`, an exact commit SHA, successful verification evidence, and explicit approval.

## 6. Bypass Prohibition

No GitHub workflow or repository automation may invoke Vercel deployment outside the release authorization gate.

Any direct Vercel CLI/API deployment path must be governed by the same authorization contract or removed.

## 7. Verification Boundary

Repository tests can prove that the repository is configured to deny automatic deployment and that authorization logic is fail-closed.

They cannot, by themselves, prove an external Vercel webhook setting. Provider verification must come from current Vercel project/deployment evidence.

Therefore:

**IMPLEMENTED ≠ VERIFIED ≠ PRODUCTION_PROVEN.**

## 8. MPA Principle

Automatic builds for non-deployable knowledge work consume resources without producing corresponding publication value. This is a Maximum Value Per Action violation.

The deployment system must therefore ask, in effect:

> **Does this change have explicit release authority and require publication now?**

If not, do not deploy.

## 9. Durable Lesson

NayaPOWER must preserve the connection to Vercel without allowing the connection to control repository behavior. **Connected does not mean automatically deployable.**

The locked door is intentional:

**REPOSITORY CHANGE → VERIFY → RELEASE DECISION → EXPLICIT AUTHORIZATION → DEPLOY → VERIFY**

not:

**REPOSITORY CHANGE → DEPLOY**
