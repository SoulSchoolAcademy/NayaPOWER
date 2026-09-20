# NAYA POWER — WELCOME IDENTITY & PWA ENTRY CONTRACT V1

DATE: 2026-09-12
STATUS: CANONICAL P0 ENTRY CONTRACT V1
NUMBER: 56
AUTHORITY: SUBORDINATE TO CONSTITUTION, GOVERNANCE, #46, #48, #51, #52, #55
PURPOSE: Define the exact user journey from NayaNET entrance through identity activation into the user's Intelligent Hub.

---

## 1. PRODUCT ENTRY JOB

The NayaNET entrance is the front door to the living network.

Its job is not to be a separate destination from the Hub.

Its job is:

**IDENTIFY → CONFIGURE IDENTITY → AUTHORIZE → ENTER HUB → REMEMBER USER SAFELY**

---

## 2. FIRST-USE JOURNEY

The intended first-use journey is:

1. User arrives at `welcome.nayanet.app`.
2. User enters/confirm their real Smart Name.
3. Naya suggests a clean Smart Alias.
4. User accepts or edits the alias.
5. System shows the resulting Smart Link.
6. System shows the resulting Smart Mail identity.
7. User activates.
8. Identity/session is established by the real identity service.
9. User enters their Intelligent Hub.
10. Hub opens in the user's authenticated context.

The final activation destination is the user's Hub, not Academy.

Academy may remain a destination inside the Hub or a linked product surface.

---

## 3. RETURNING USER JOURNEY

When a user launches the installed NayaNET app/PWA:

**VALID SESSION → RESTORE USER → OPEN USER HUB**

The system must not require the user to repeat identity configuration on every launch.

If the session is invalid or expired:

**INVALID SESSION → SAFE AUTH / WELCOME BOUNDARY**

The system must never silently create a new alias or new identity because local session data is missing.

---

## 4. IDENTITY MODEL

The following concepts must remain distinct:

### Smart Name

The user's human-facing chosen name.

### Smart Alias

The user's canonical NayaNET-friendly identity handle.

### Smart Link

The canonical web identity/address derived from the authorized alias.

### Smart Mail ID

The user's communication identity derived from the authorized alias, subject to the actual mail implementation.

### Account Identity

The secure backend identity record that owns authorization, sessions, privacy, and persistent user data.

### Device Session

A device-specific authenticated session/credential bound to the account identity.

Local storage alone is not an account identity.

---

## 5. ALIAS RULES

Alias normalization may remove unsupported characters for presentation, but the production system must also enforce:

- uniqueness;
- reserved-name protection;
- length limits;
- allowed character rules;
- collision handling;
- ownership;
- authorization;
- rename policy;
- publication state.

The client may preview an alias.

Only the authoritative identity service may establish ownership.

---

## 6. CURRENT SOURCE REALITY

The supplied entrance implementation currently:

- accepts `name` from the query string or session storage;
- derives a normalized alias client-side;
- displays Smart Name, Smart Alias, Smart Link, and Smart Mail ID;
- creates a local `nayanet_vault_key` using `Math.random()`;
- stores alias/name in `localStorage`;
- redirects activation to `https://academy.nayanet.app/`.

This is suitable as a prototype experience but is not sufficient as the final secure identity implementation.

The final implementation must replace local-only identity establishment with the canonical identity/session service.

---

## 7. ACTIVATION DESTINATION

Temporary:

`https://academy.nayanet.app/`

Final:

**CANONICAL USER HUB URL / ROUTE**

The exact production Hub URL must be established by #55 runtime reconciliation before hard-coding it into the entrance.

This prevents the entrance from being coupled to an unverified runtime.

---

## 8. PWA / APP INSTALL

The entrance may provide installation guidance, but installation is not the authentication mechanism.

The production PWA must have:

- valid web manifest;
- stable application identity/name;
- official icon set;
- start URL targeting the authenticated Hub entry strategy;
- display mode appropriate to the experience;
- service worker where required;
- update strategy;
- offline/degraded behavior;
- safe session restoration;
- logout/identity invalidation handling.

The start URL must not bypass authorization.

Recommended pattern:

**APP START → SESSION RESTORE → HUB OR AUTH**

rather than a static unauthenticated page that merely redirects.

---

## 9. SMART LINK BEHAVIOR

A Smart Link must resolve to the correct authorized public/private surface according to publication state.

A Smart Link must not expose private intelligence merely because the alias is known.

Private content requires authorization.

Public content requires explicit publication state.

---

## 10. SECURITY RULES

The entrance must not use:

- `Math.random()` as a security credential;
- client-side localStorage as the authoritative identity database;
- query-string name alone as proof of identity;
- hard-coded private credentials;
- implicit authorization based on possession of a URL.

Production identity must be server-authoritative and session-secured.

---

## 11. UX PRESERVATION

The current entrance's visual direction is valuable and should be preserved where it supports the intended experience:

- obsidian/black foundation;
- white typography;
- restrained electric purple;
- green readiness/activation state;
- elevated card depth;
- strong activation CTA;
- clear Smart Name / Alias / Link / Mail preview;
- installation affordance.

The transition into the Hub should feel like entering the same NayaNET world, not being sent to an unrelated website.

---

## 12. FAILURE STATES

The entrance must explicitly handle:

- alias unavailable;
- identity service unavailable;
- session restore failure;
- activation failure;
- Hub unavailable;
- PWA install unsupported;
- expired session;
- revoked identity;
- unauthorized Smart Link;
- deployment/runtime mismatch.

Every consequential failure must tell the truth and provide the best next action.

---

## 13. VERIFICATION

Production acceptance requires an independently observed sequence:

**NEW USER → IDENTITY CREATED → ALIAS OWNED → ACTIVATION → HUB SESSION → HUB LOAD**

Then:

**APP CLOSE → APP REOPEN → SESSION RESTORE → SAME HUB IDENTITY**

Then:

**SESSION INVALIDATED → REOPEN → AUTH BOUNDARY**

No successful redirect alone proves this behavior.

---

## 14. CURRENT BLOCKER

The supplied entrance source and the currently publicly observed `welcome.nayanet.app` response must be reconciled before production replacement is declared complete.

The exact production source location for the supplied entrance code is not yet established inside `SoulSchoolAcademy/NayaPOWER`.

Do not overwrite an unknown external source blindly.

---

## 15. DEFINITION OF DONE

The entrance is complete when:

**WELCOME → IDENTITY → ALIAS → SMART LINK / MAIL → ACTIVATION → AUTHORIZED HUB**

works for a real user, and:

**APP ICON → SESSION RESTORE → SAME HUB**

works for returning users without creating duplicate identities.

The exact runtime, source, and evidence must agree.
