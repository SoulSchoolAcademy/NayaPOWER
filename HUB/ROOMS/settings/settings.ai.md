# Settings — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/settings`. **Accent:** white/neutral (no spectral color). **Build order:** 10, hardened throughout.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. `hub/settings?section=`.

## Component tree

1. `SettingsHero` — title + `SectionNav` (IDENTITY/PRIVACY/AUTHORITY/CONNECTIONS/NOTIFICATIONS/DATA/SECURITY/APPEARANCE).
2. `IdentitySection` — who/ session truth cards (live / local / unknown).
3. `PrivacySection` — global posture in plain words + switches.
4. `AuthoritySection` — what Naya may do, grant states.
5. `YourIntelligenceSection` — privacy, sharing, collective participation, retention, export, deletion.
6. `AppearanceSection` — type size, motion, density (live preview).
7. `IntegrationRow` (per integration) — health + "Test connection."

## Data bindings

- Identity/session ← runtime truth. Privacy/authority ← governance store. Integrations ← health probes.

## States

- `loading`, `probe_running` (test connection), `export_manifest` (pre-confirm), `delete_armed` (typed confirm).

## Interactions

- Switch → consequence stated inline → applies → receipt where governance-relevant.
- Test connection → live probe → result shown with timestamp.
- Export → manifest shown → confirm → download. Delete → typed confirmation → executed → receipt.

## Design tokens

White on obsidian; instrument-panel restraint; generous type; no glow.

## Acceptance

Every switch explains its consequence; no dark patterns (verify by review); export manifest complete; delete requires typed confirm; 9.0+.
