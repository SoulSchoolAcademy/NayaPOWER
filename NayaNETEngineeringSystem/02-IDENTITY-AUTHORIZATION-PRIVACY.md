# 02 — Identity, Authorization and Privacy

## Identity
Every protected NayaNET operation resolves the authenticated member before accessing protected resources. UI identity is not authority; membership is not unrestricted access.

## Authority
```text
HUMAN INTENT
 ↓
AUTHORITY CHECK
 ↓
PERMITTED ACTION + SCOPE
 ↓
EXECUTION
```
Capability does not create authority. Naya/AI may reason and act only within actual granted authority.

## Privacy
Canonical rule: **Private by default • Shared by choice • Collective by consent • Public by decision.**

A private Smart Note does not become public because it appears in a feed, list, report, Space, or message. Sharing one item does not publish an entire private collection.

## Item-level access
Protected operations must evaluate the target object's ownership/authority, visibility, recipient eligibility, Space membership, publication state and any applicable communication/sharing settings. Search and ranking must operate inside authorization, never around it.

## Feature-specific rules
- **Smart Feed:** personal feed private by default; collective feed only exposes authorized published/collective material.
- **Smart List:** sharing a list does not automatically grant access to every referenced object.
- **Smart Mail:** message permission is distinct from intelligence-payload access.
- **Smart Spaces:** membership does not grant access to unrelated private intelligence.
- **Smart Share:** explicit sharing action + scope + recipient authorization.
- **Today/Reports:** derived summaries must inherit the access boundary of their sources and avoid leaking protected content through summaries.
- **Smart Ledger:** records must expose only evidence permitted to the requesting actor.

## Front-end requirements
- Clearly identify current member and scope.
- Preview recipients/audience before consequential sharing or delivery.
- Distinguish private, shared, collective and public states.
- Never show a protected action as available when the backend will reject it.
- Explain denial without leaking protected resource details.

## Back-end requirements
- Server-side authorization is mandatory for protected reads/writes.
- Enforce least privilege and object-level access.
- Validate audience membership at use time, not only when a UI list was loaded.
- Recheck revocation at execution/use time for consequential actions.
- Record meaningful authorization decisions and resulting receipts/events where the contract requires.
- Never trust client-supplied owner, scope, publication, or permission fields.

## Threat cases to test
1. User A attempts to retrieve User B private intelligence.
2. User A shares a list containing inaccessible items.
3. User loses membership/authority between UI load and action.
4. Public/collective item is incorrectly treated as verified.
5. Summary/report leaks source content outside source visibility.
6. Smart Mail reaches an ineligible recipient.
7. Space membership is used as a false permission escalation.

## Source authority
01–58 system directive; `.naya/2026-09-11-NAYAPOWER-21-HUMAN-AUTHORITY-AI-INTELLIGENCE-SMART-NOTE.md`; `.naya/2026-09-11-16-35-NAYAPOWER-25-PRIVACY-BY-CHOICE-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-46-IDENTITY-PRIVACY-PUBLICATION-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-47-SMART-SPACE-CONTRACT.md`.
