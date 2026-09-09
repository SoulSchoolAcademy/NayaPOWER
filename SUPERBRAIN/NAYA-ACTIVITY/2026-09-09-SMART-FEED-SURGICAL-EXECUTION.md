# Naya 16 Activity Record

## 2026-09-09 — Smart Feed surgical execution

**STATUS:** EXECUTION IN PROGRESS / RELEASE BLOCKED UNTIL RUNTIME PROOF
**ACTION ID:** `SMART-FEED-20260909-SURGICAL-EXECUTION`
**NAYA:** Implementation Naya
**PROJECT:** NayaNET Intelligent Hub Smart Feed
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**BRANCH:** `main`
**LATEST HEAD AT RECORD:** `4fabca154f52da76f508064451497db467e6a6e1`

### 01 — WHAT IS HAPPENING NOW?
The canonical React Smart Feed is being upgraded surgically. Automated deployment runs exposed a legacy JavaScript upgrade layer in `scripts/v7-intelligent-upgrade.js` that can generate the old user-facing intelligence/control surface. It is not referenced by the canonical React Hub and has been removed rather than hidden.

### 02 — WHAT ARE WE ACTUALLY TRYING TO ACHIEVE?
Preserve the canonical Smart Feed and approved Hub shell, make Collective Intelligence the default, strengthen the Smart Board hierarchy and interaction layout, remove internal Superbrain product UI, and prove source-to-runtime parity.

### 03 — WHAT DOES THE EXISTING SYSTEM ACTUALLY DO?
`SmartFeedBoard.tsx` already contains the three-lens selector, In a Nutshell hero, Human/Child/Grandma/Naya/Machine/Weaver perspectives, learning layer, Trust/Provenance/Privacy, Related Intelligence, Smart Space, engagement, comments, contextual Ask Naya, and Create Smart Space. Its local state was previously shared across events; it is now keyed by `event_id` so one intelligence cannot overwrite another.

### 04 — WHAT COULD I BE MISUNDERSTANDING?
The first source search did not expose the legacy upgrade layer because the relevant source was in a script outside the canonical React tree. The deployment artifact gate caught it. Therefore “not imported by React” is not enough when another script can inject UI into the product.

### 05 — WHAT ARE THE CONSEQUENCES OF EACH OPTION?
Rebuilding the Hub risks destroying approved architecture. CSS hiding violates the directive. Leaving the legacy injector in the repository leaves a competing source capable of recreating the unwanted UI. The surgical choice is to remove the unused legacy injector and strengthen source/artifact/runtime guards.

### 06 — WHAT MATTERS MOST?
The exact public runtime must agree with the canonical source and artifact. The user's observation remains the controlling product reality if it contradicts automation.

### 07 — WHAT SHOULD I DO?
Remove the legacy user-facing injector, preserve the canonical React renderer, strengthen forbidden-UI detection, and run the canonical build/deploy/runtime verification again.

### 08 — WHAT SHOULD I NOT DO?
Do not redesign the Hub shell. Do not expose Naya 16. Do not add Superbrain controls. Do not create a second Smart Feed or favorites architecture. Do not use a generic `CAPTURE` string check that can false-positive on unrelated dependency text; detect the actual operator-control cluster instead.

### 09 — EXECUTE SURGICALLY
Completed changes in this execution chain: Smart Feed state is event-scoped; Activity is explicitly labelled `ACTIVITY FEED`; Favorite and Save have explicit accessible labels; the fixture source label was changed from `NayaNET Intelligence Capture` to `NayaNET Intelligence Event` to avoid conflating a content noun with the forbidden operator control; the canonical workflow now scans source, artifact, and runtime for the actual forbidden UI; the legacy `scripts/v7-intelligent-upgrade.js` injector has been removed.

### 10 — VERIFY THE CHANGE
The canonical workflow reached artifact inspection and caught the legacy injector as a real forbidden source. A subsequent false-positive on the generic word `CAPTURE` was traced to bundle text rather than the operator panel and the guard was narrowed to operator-control clusters. The current head requires a fresh canonical deployment verification.

### 11 — TRACE REALITY END-TO-END
SOURCE → canonical React SmartFeedBoard/App + legacy injector audit → Vite artifact → aged-art-7c12 Worker → independent runtime checks. The workflow requires route parity, JS asset retrieval, cognition-engine retrieval, product markers, forbidden operator-cluster absence, and current source-commit parity.

### 12 — PRODUCE RECEIPTS
Receipts available now: implementation commits `9733227eaf752cc965e7400a0651f20ad4fb25d6`, `18b84f02f634e4f1782dff28820dee436988fead`, `664bcb6f5cc613b5a4a745e49133fc8408f78c9e`, `bbcb6c171a44ee4a5cc054c2ed78a7a00bf428c6`, and `4fabca154f52da76f508064451497db467e6a6e1`; canonical workflow run `34415920725` exposed the legacy injector and stopped before release; a new push-triggered run has not yet appeared for `4fabca154f52da76f508064451497db467e6a6e1`, so deployment/runtime proof remains pending.

### 13 — CHALLENGE MY OWN CONCLUSION
A successful text-marker scan cannot prove visual layout. A competing Cloudflare deployment or browser/service-worker cache can still make the user see a different product. If the canonical Worker returns a clean artifact but the user's exact visible page still shows the old controls, inspect the exact URL and competing deployment path rather than changing Smart Feed code again.

### 14 — REPORT CONFIDENCE
**MEDIUM / RELEASE BLOCKED.** The source-level legacy injector has been removed. End-to-end public-runtime removal and visual parity are not yet proven.

### 15 — DETERMINE WHAT MATTERS NEXT
Trigger or obtain the canonical deployment from the current head, inspect the resulting job output, then independently compare the exact public runtime with the user's observed UI.

### 16 — LEARN AND CHANGE THE SYSTEM
Permanent guardrails now include: source scan for forbidden operator UI, artifact scan for forbidden product markers, operator-cluster detection instead of generic `CAPTURE` detection, route parity, runtime asset checks, and source-commit parity. The visual gate remains separate and must never be implied by static success.

**16-PROTOCOL CHECK:** PASS — current execution state and contradiction are recorded.

**RELEASE-TRIGGER NOTE:** This record update exists solely to create a new main-branch push after the legacy injector removal, because the canonical workflow's current public trigger history shows the preceding run was manually dispatched on the prior commit. No product behavior is added by this note.
