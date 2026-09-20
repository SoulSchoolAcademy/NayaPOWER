# NAYA POWER — IDENTITY / PRIVACY / PUBLICATION CONTRACT V1

DATE: 2026-09-12
STATUS: CANONICAL IDENTITY CONTRACT V1
NUMBER: 46

## PURPOSE
Define the entrance-to-Hub identity lifecycle and publication boundaries.

## 1. ENTRANCE

`welcome.nayanet.app` is the intended onboarding boundary.
Sequence:
REAL NAME → SMART ALIAS → SMART LINK / SMART MAIL ID → ACTIVATION → HUB.

The real name and Smart alias are distinct concepts. The alias is the user's sovereign network-facing identity and should be stable once claimed/authorized.

## 2. CURRENT SOURCE REALITY

The supplied entrance currently derives a sanitized alias client-side, stores a device key and identity in localStorage, and redirects to Academy. The Academy redirect is temporary and should become the Hub destination after the Hub runtime exists.

This localStorage implementation is a prototype/session convenience, not sufficient proof of secure server-side identity.

## 3. SESSION LIFECYCLE

FIRST ACTIVATION: establish authorized identity/session and open Hub.
RETURNING LAUNCH: validate existing session/device binding and open user's Hub directly.
INVALID/EXPIRED: return to welcome/auth boundary.
NO IDENTITY: never invent identity; require activation/authentication.

## 4. PWA INSTALL

The installed NayaNET app should use a stable app entry route. After authentication/session restoration it should open the user's Hub. It must not create a second identity on every launch.

The manifest/start_url and service-worker/navigation strategy must be aligned with the actual authentication boundary.

## 5. PUBLICATION

PRIVATE is default for personal intelligence.
SHAREABLE permits intentional sharing without making the source universally public.
PUBLIC permits Collective projection when eligible.
MAKE PUBLIC is an explicit state transition and must be auditable.

## 6. DATA MINIMIZATION

Real name, alias, mail identity, session credentials, and private intelligence must be separated according to need. Do not expose device keys or authentication secrets in feed content.

## 7. ACCEPTANCE

A user can activate once, return later, launch the installed app, restore identity, enter the correct Hub, create private intelligence, and explicitly publish eligible intelligence without identity duplication or privacy leakage.
