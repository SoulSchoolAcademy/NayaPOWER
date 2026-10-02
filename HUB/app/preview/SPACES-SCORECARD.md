# Smart Spaces — Room Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` (uncommitted; parent reviews and pushes).
Contract: `SpacesAdapter.parseSpaces(raw, contacts)` → `window.NayaRooms.smartSpaces(el, {spaces})`.
Seeded from the shared CONTACTS/SPACES contract. No canonical group store exists:
all spaces/activity are labeled DEMO; members are real network contacts.
Verified: jsdom — 15 pass, 0 fail (3 cards, member resolution, detail open,
post-to-space + localStorage persistence, back/Enter/Escape, demo chips, 0 errors).

## Score: 9.2/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Contract fidelity | 10 | Shared CONTACTS/SPACES used exactly; member ids resolve to contacts; unparseable records skipped. |
| 2 | Honesty | 10 | DEMO on every space card, activity row, and the room banner; real contacts named; posts labeled as device-local. |
| 3 | Color law | 10 | Each space card carries its own identity color; violet is room chrome only (kicker, tabs, send ignite). |
| 4 | Button law | 10 | Cards open (click/Enter), back/Escape returns, Send disabled until text, every control has a real consequence. |
| 5 | Real consequence | 9 | Posting appends to the feed and persists to `naya.smartspaces.posts`; survives re-render within the session. |
| 6 | Craft | 9 | Glass panels, breathing accent bars, staggered entrance; ≤760px single-column responsive. |

## Why not 10

- **-0.5 — no real backend.** Posts live in localStorage only; no canonical group store, no cross-device sync, no real mail delivery (protected-gate work).
- **-0.3 — visual confirmation pending** (no screenshot pipeline; director eyes not yet on it).

## What closes it

- Canonical group store + real delivery wired by the shell -> +0.5
- Shawn's visual pass -> +0.3
