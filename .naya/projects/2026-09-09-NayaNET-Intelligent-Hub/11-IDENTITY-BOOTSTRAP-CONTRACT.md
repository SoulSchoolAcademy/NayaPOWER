# 11 — IDENTITY BOOTSTRAP CONTRACT

**Project:** NayaNET Intelligent Hub — Fresh Rebuild
**Status:** LOCKED ARCHITECTURAL REQUIREMENT
**Date:** 2026-09-09

## 1. PURPOSE

The NayaNET entrance and Smart Identity Activation are upstream infrastructure for the Intelligent Hub. The Hub must not treat them as unrelated pages.

The required product journey is:

```text
WELCOME
  ↓
USER ENTERS NAME
  ↓
SMART IDENTITY ACTIVATION
  ↓
NAME + ALIAS + KEY / IDENTITY STATE
  ↓
INTELLIGENT HUB
```

The Identity Activation page currently redirects to Naya Power Academy. That destination must change when the new Hub production URL is established. Academy remains an ecosystem destination inside the Hub, not the post-activation landing destination.

## 2. SOURCE BEHAVIOR TO PRESERVE

The current entrance captures the user's name and sends it to `identity.html?name=...`, while also storing `nayanet_user_name` in session storage.

The current identity page derives/accepts a clean alias and establishes:

- Smart Name
- Sovereign Smart Alias
- Smart Link
- Secure Smart Mail identifier
- local NayaNET vault/device key

Current local keys observed in the supplied source:

- `nayanet_user_name`
- `nayanet_vault_key`
- `nayanet_smart_alias`
- `nayanet_smart_name`

These are bootstrap behavior, not a declaration that browser localStorage is the final production identity system.

## 3. CANONICAL IDENTITY OBJECT

The new Hub must have one normalized identity context available before rendering personalized Hub content:

```text
userIdentity
├── smartName
├── smartAlias
├── smartLink
├── smartMailIdentity
├── smartSpaceIdentity
├── identityKey / account reference
├── nayaIdentityBinding
└── privacy / consent state
```

The exact production account/authentication implementation remains an engineering decision, but the data contract above is required.

## 4. NAMESPACE LAW

The alias is not merely display text. It is the user's NayaNET namespace.

For alias `shawn`:

```text
Smart Name      → Shawn
Smart Alias     → shawn
Smart Link      → shawn.nayanet.app
Smart Mail      → shawn
Smart Space     → shawn
Intelligence    → Shawn's authorized intelligence
Smart Notes     → Shawn's canonical events
Smart Feed      → Shawn's intelligence projection
Reports         → Shawn's reports
Library         → Shawn's authorized intelligence library
```

The namespace must be consistently resolved across rooms.

## 5. HUB BOOT SEQUENCE

The Hub must boot in this order:

```text
1. Resolve identity
2. Validate identity state
3. Establish user namespace
4. Load persistent user state
5. Load authorized intelligence state
6. Load current-state summary
7. Render Home orientation
8. Enable room navigation
```

No personalized room should silently fall back to generic demo data when identity is available.

## 6. HOME REQUIREMENT

Immediately after activation, the user should see a time-appropriate personalized greeting such as:

**Good morning, Shawn.**

Home must also expose current time, current date, locale/country context, intelligence philosophy, privacy law, search/Ask Naya, and current intelligence orientation.

## 7. DATA OWNERSHIP

The identity context is the root context for canonical intelligence events:

```text
Identity
  ↓
Human Input
  ↓
Smart Note / Note Event
  ↓
Persistence
  ↓
Naya enrichment
  ↓
Machine evidence
  ↓
Intelligent Feed
  ↓
Library / Reports / Search / Learning
```

Smart Mail and Smart Space must resolve against the same identity namespace rather than inventing separate user identities.

## 8. PRIVACY

Identity is private by default.

**PRIVATE BY DEFAULT · SHARED BY CHOICE · COLLECTIVE BY CONSENT · PUBLIC BY DECISION**

Collective projections must never expose private identity fields unless the applicable product/privacy contract explicitly permits it.

## 9. TRANSITION FROM CURRENT IDENTITY PAGE

Do not rewrite the identity page prematurely. First build and establish the canonical Hub route and boot contract.

Then update the identity page surgically so that:

- existing name/alias/key behavior is preserved
- the new Hub receives the identity
- the redirect lands at the production Hub
- the Hub resolves the same identity
- Smart Mail and Smart Space use the alias
- Academy remains reachable from the Hub ecosystem navigation

## 10. ACCEPTANCE TEST

A fresh browser/session must support:

```text
Enter name → Identity page → choose/confirm alias → Activate
→ Hub opens → correct name appears → correct alias is loaded
→ Smart Mail namespace resolves → Smart Space namespace resolves
→ refresh preserves authorized identity/session behavior
```

A second user with a different alias must not inherit the first user's intelligence state.

## 11. DEPENDENCY RULE

The Identity Bootstrap Contract is part of **FOUNDATION**, not a later cosmetic integration.

The Hub shell can be designed before the final production identity backend, but all Hub room contracts must be written against this identity model from the beginning.
