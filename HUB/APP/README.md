# 🔱 NayaNET Intelligent Hub — Executable App V1

This directory is the first componentized, executable Hub implementation derived from the canonical NayaNET design system.

## What works

- 11 canonical Hub rooms with persistent navigation.
- Hash deep links such as `#/today`, `#/reports`, `#/connect`.
- Browser refresh preserves the current room.
- Collective / Personal / Activity view switching.
- Intelligence search across the current semantic board set.
- Favorite and Save actions with local browser persistence.
- Smart Connect / Smart Doors surface with explicit connection-versus-authority boundary.
- Smart Ledger, Smart Mail, Settings and other room surfaces.
- Contextual Ask Naya experience.
- Responsive layouts.
- Keyboard focus states.
- Reduced-motion support.
- Truthful `NOT VERIFIED` runtime states where no governed runtime is connected.

## Truth boundary

This application is a real functioning interface, but it does not pretend to have a live NayaPOWER backend when one is not connected.

Local browser memory is presentation state, not canonical intelligence.

Live intelligence, governed identity, durable retrieval, real receipts, learning and consequential actions must be connected through the governed runtime adapter before they are shown as live.

## Run

From this directory:

```bash
npm test
python -m http.server 8080
```

Then open:

`http://localhost:8080/`

## Design inheritance

This app consumes the NayaNET design-law stack established separately in PR #1296:

**Visual Bliss → Primo Buttons → Intelligence Boards → Icon/Jewel → Composition/Typography → State/Liveness/Truth → Accessibility/Responsive → Visual Regression**

The existing Hub concept remains the visual-quality baseline. The app is not a generic SaaS redesign.
