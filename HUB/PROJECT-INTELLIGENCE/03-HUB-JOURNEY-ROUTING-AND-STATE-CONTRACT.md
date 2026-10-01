# 03 — Hub Journey, Routing & State Contract

## 1. Canonical journey

```
WELCOME
   ↓
IDENTITY
   ↓
INTELLIGENT HUB
```

This is the default successful product journey.

Academy, Powercast, White Paper, About Us and other destinations remain optional ecosystem destinations.

## 2. Current repository mismatches

Observed on the current baseline:

### Welcome mismatch
`HUB/NAYANET WELCOME PAGE.html` routes toward `identity.html`, but no `identity.html` exists in the current HUB directory. The physical file is:

`HUB/NAYANET INDENITY PAGE.html`

The filename itself contains the historical typo **INDENITY**.

### Identity mismatch
The Identity concept references:
- `index.html`;
- `hub.html`;
- a worker URL.

But current `HUB/hub.html` is the **Powercast player**, not the Intelligent Hub.

### Duplicate identity risk
The large Hub concept also injects a Hub-side auth/identity gate. Once Identity becomes a real successful onboarding boundary, the Hub must not force the person through a second conflicting onboarding flow.

## 3. Production route contract

Recommended logical routes:

- `/` or `/welcome` → Welcome;
- `/identity` → Identity;
- `/hub` → Intelligent Hub;
- `/hub/:room` → selected Hub room;
- `/powercast` → Powercast.

Legacy static filenames may redirect to canonical routes for compatibility.

Do not let filenames define product architecture.

## 4. Welcome contract

Purpose: **Invitation and recognition.**

Preserve:
- obsidian entrance;
- orbital/spectral jewel language;
- central portal;
- premium motion;
- name-first recognition;
- minimal ecosystem links.

Do not overload Welcome with system architecture.

Successful action:
**ENTER NAYANET → Identity**

Required states:
- rest;
- name input;
- responding / transition;
- invalid/empty;
- reduced-motion;
- route failure.

## 5. Identity contract

Purpose: **Governed activation and orientation.**

Identity should visually feel like the system recognizes a real human/session and prepares their intelligence environment.

It should establish/display, where applicable:

- human display identity;
- authenticated session;
- stable internal user identity;
- NayaNET alias/namespace;
- Naya identity;
- privacy state;
- NayaPOWER connection state;
- app-install state;
- connection/integration state;
- exact next action.

### Important
A localStorage alias or random device key may be used only as non-authoritative presentation/cache where appropriate. It cannot stand in for the governed identity/session boundary.

Successful action:
**ENTER NAYANET → Intelligent Hub**

## 6. Hub entry contract

On entry, the Hub must answer quickly:

- Who am I here as?
- Is my intelligence connected?
- What is current?
- What matters now?
- What can I do?
- What is blocked/unknown?
- What should happen next?

Do not expose infrastructure unless it helps the human act or trust the system.

## 7. Universal state vocabulary

Every meaningful interactive surface should deliberately design:

- REST;
- HOVER;
- FOCUS;
- ACTIVE / SELECTED;
- LOADING / SYNCING;
- SUCCESS / VERIFIED;
- EMPTY;
- BLOCKED;
- UNAUTHORIZED;
- ERROR;
- OFFLINE / DISCONNECTED;
- UNKNOWN;
- DISABLED.

Animation must reflect real state. It must never create the impression that backend work succeeded when it did not.

## 8. Browser behavior

The production Hub is an application.

Required:
- deep-linkable rooms;
- back/forward navigation;
- refresh recovery;
- route guards;
- preserved legitimate session state;
- no loss of canonical intelligence due to client refresh;
- clear 404/recovery path.

## 9. Privacy language

The interface should preserve:

> **Private by default. Shared by choice. Collective by consent. Public by decision.**

Sharing/connection state must be deliberate and legible.

## 10. Acceptance

Journey PASS requires:

**OPEN WELCOME → ENTER NAME → IDENTITY ESTABLISHED → ENTER HUB → LOAD GOVERNED CURRENT STATE → OPEN ROOM → PERFORM REAL ACTION OR HONESTLY REFUSE → OBSERVE RESULT → REFRESH → STATE REMAINS COHERENT**

A screenshot alone is not journey proof.
