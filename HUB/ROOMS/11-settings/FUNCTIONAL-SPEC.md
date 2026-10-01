# 11 — Settings

**Metaphor:** THE CONTROL DECK  
**Route:** `/settings`  
**Theme:** neutral / silver  
**Human question:** **How should NayaNET work for me?**

## Human promise

Give the human clear control over their relationship with NayaNET without exposing unnecessary implementation machinery.

Settings should feel calm, precise and trustworthy — not like a developer console.

## Signature visual

A premium **control deck** organized by human concerns.

Primary categories:

### Identity & Account
- Smart Name / alias
- authentication/session
- account details
- device/session visibility where supported

### Privacy & Consent
- sharing defaults
- collective/public choices
- consent and revocation controls
- visibility preferences

### Connections & Doors
- connected channels
- door health
- authentication
- disconnect/revoke where supported

### Naya Preferences
- communication preferences
- proactive assistance preferences
- reminder/notification behavior where supported

### Appearance & Accessibility
- motion preference
- text/contrast preferences
- display density/theme options where supported
- accessibility controls

### Notifications
- channels
- priority
- quiet modes
- Space-specific preferences

### Trust & Data
- data export where supported
- provenance/trust information
- account/data controls available to the human

### System Health — advanced
This is where the secondary **System** surface should normally live:
- runtime status;
- app version/build;
- source/deployment status where available;
- door health;
- diagnostics;
- scorecard/spec links for authorized/advanced users.

Do not promote engineering diagnostics into the main human rail by default.

## Primary actions

Context-dependent:
- **Save**
- **Connect / Disconnect**
- **Revoke**
- **Sign out**
- **Manage consent**
- **Export**
- **Open System Health**
- **Ask Naya what this setting means**

Sensitive controls require clear confirmation and correct authority.

## State honesty

Settings must distinguish:
- local preference;
- account-backed setting;
- governed runtime setting;
- unavailable/unsupported setting.

Never make a local toggle look like a server-enforced privacy guarantee.

## Cross-room handoffs

Connections/Doors → Connect  
People/privacy → Connections  
Space defaults → Spaces  
Activity/proof → Ledger

## Mobile

Category list → focused setting detail. Avoid a giant scrolling control dump.

## Acceptance journey

A human can find a privacy or identity setting by human language, understand its actual scope, change it when authorized, see confirmation where needed, and reverse the choice when the product supports it.

## Human Director source-note reconciliation

The Drive notes set a concise top-level structure: **IDENTITY / PRIVACY / AUTHORITY / CONNECTIONS / NOTIFICATIONS / DATA / SECURITY / APPEARANCE**. They also call for a dedicated **YOUR INTELLIGENCE — Your intelligence is yours** section controlling privacy, sharing, collective participation, retention, export and deletion. The System surface from PR #1278 should normally become **Settings → System Health** rather than a permanent primary rail room, preserving diagnostics without expanding the main IA.

## Shared five-layer mapping

- **ORIENTATION:** Settings category, account/identity and current scope
- **CURRENT STATE:** actual account/runtime/local preference states with enforcement boundary visible
- **INTELLIGENCE:** Naya explains consequences and the difference between local preference, account setting and governed policy
- **ACTION:** save/change, consent/revoke, connect/disconnect, export/delete where supported, sign out, open System Health
- **PROOF:** confirmation, actual enforcement scope, receipts/audit for consequential/privacy changes when applicable
