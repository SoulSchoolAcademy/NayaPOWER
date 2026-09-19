# Smart Share — Engineering Specification

## What / why
Smart Share is the explicit consented sharing mechanism for eligible intelligence. It turns private intelligence into a deliberately scoped shared/public artifact only when the human and system authority rules permit it.

## Human interface
A share action should answer: **WHAT am I sharing? WITH WHOM? AT WHAT SCOPE? WHAT WILL THEY SEE?** Provide recipient/scope preview, source/provenance visibility, confirmation for consequential sharing, success receipt and clear failure/denial.

Possible targets: individual, selected people, connection group, Smart Space, collective/public scope where authorized. A single shared item never silently publishes its surrounding private context.

## Front end requirements
- Share entry points from Smart Note, List, Feed, Space and other eligible surfaces.
- Scope/recipient picker.
- Preview of exact shared object and audience.
- Item-level warnings for inaccessible/protected content.
- Confirmation for consequential publication.
- Receipt/result state.
- Revoke/unshare UI only where the backend contract supports it.

## Back end requirements
- Resolve canonical source object.
- Evaluate actor authority, owner rights, object visibility, recipient eligibility and publication rules.
- Produce an explicit share record/scope.
- Derive a privacy-safe projection where required rather than exposing private source fields.
- Preserve provenance.
- Emit event/receipt and ledger evidence when required.
- Recheck authority at execution/use time.
- Make repeated share requests idempotent where appropriate.

## Data / API contract
Conceptual share record: `share_id, actor_id, source_type, source_id, target_type, target_ids, scope, publication_state, created_at, revoked_at, provenance, receipt_ref`. Exact schema must follow existing publication/share contracts.

## Connections
`Notes/Lists → Share`; `Share → Collective Intelligence`; `Share → Spaces/Mail`; `Privacy → scope`; `Ledger → evidence`; `Feed → publication projection`; `Reports/Today → shared outcome signals`.

## Verification
Share one private item to one authorized recipient; verify exact scope; prove non-recipient denial; share a list containing protected content and prove no leakage; revoke if supported and prove access behavior; verify provenance and receipt; test duplicate/replay.

## Current state
**DEFINED** by `.naya/13` and privacy/publication contracts; runtime state must be inspected.

## Gap / next action
Map the existing sharing/publication runtime to this contract and prove item-level authorization plus explicit scope.

## Source authority
`.naya/2026-09-11-NAYAPOWER-13-SMART-SHARE-SMART-NOTE.md`; `.naya/2026-09-11-16-35-NAYAPOWER-25-PRIVACY-BY-CHOICE-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-46-IDENTITY-PRIVACY-PUBLICATION-CONTRACT.md`.


## COMPLETION CHECKLIST — 2026-09-19

- [x] Source contract identified
- [x] .naya authority identified
- [x] Privacy/publication authority identified
- [ ] Existing runtime mapped
- [ ] Canonical share record identified
- [ ] Authorized share proven
- [ ] Non-recipient denial proven
- [ ] Protected-content leakage test proven
- [ ] Revocation behavior proven where supported
- [ ] Source → build → runtime parity proven
- [x] Dated activity record exists
- [x] One next action recorded

**Current state:** DEFINED. See [2026-09-19 activity](../ACTIVITY/2026/09/19/SMART-SHARE.md).
