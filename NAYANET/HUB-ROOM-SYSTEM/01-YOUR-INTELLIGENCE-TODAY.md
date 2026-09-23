# 01 — Your Intelligence Today

## Product job
Give a human a high-value, truthful view of what their intelligence looks like today: what changed, what was created, what was learned, what was decided, what matters now, and what Naya can substantiate.

This is a room inside the Hub middle workspace, not a separate page.

## Presentation
Use the full middle workspace width available beneath the persistent search/header region. Do not reserve a permanent right rail for this room.

Visual language: deep black spatial background, restrained purple/indigo/green accents, large typography, physical 3D controls, clear hierarchy, visible provenance, generous spacing, and meaningful motion. Avoid dashboard clutter and tiny text.

## Screen hierarchy
1. Room header — Your Intelligence Today, current date, concise purpose, truth/state indicator.
2. Today Pulse — evidence-backed counts/statuses for intelligence captured, meaningful changes, learning, decisions, and activity. Unknown stays unknown; zero is not substituted for missing data.
3. What Changed — meaningful new/changed intelligence since the daily boundary. Each item shows type, time, source/provenance, privacy scope, and available evidence.
4. Intelligence stream — Personal / Collective / Activity modes. Collective is default. Switching mode must change actual projected content, not merely the label.
5. Naya synthesis — compact interpretation grounded in available evidence: what appears important, what remains uncertain, and what deserves attention.
6. Actions — Capture Smart Note, open Personal, open Collective, open Activity, inspect evidence.
7. Proof footer — runtime state, retrieval time, projection status, and provenance where exposed.

## Data rules
- Prefer canonical runtime/persistence data over browser-local fabrication.
- Personal intelligence remains private according to authority and privacy rules.
- Collective intelligence is shared only by consent and must not leak private content.
- Activity is a projection of real events; never synthesize fake activity to populate the room.
- No generated metric may be presented as observed fact.

## Interaction contract
- Opens from the sidebar without leaving the Hub shell.
- Search/header behavior remains coherent while active.
- Feed mode changes update content in-place.
- Selecting an item opens detail/evidence in the existing Hub interaction pattern.
- Capture opens Smart Notes without replacing the Hub with a new page.
- Returning preserves selected mode when appropriate, with Collective as canonical default.

## States
Loading: preserve room structure and show explicit retrieval state.
Empty: explain what is missing and provide a useful next action; never populate fake cards.
Unavailable: identify missing runtime capability and preserve the rest of the Hub.
Error: show actual boundary/error class where safe; never claim success.
Private: identify private intelligence without exposing content to an unauthorized surface.

## Acceptance / proof
PROVEN requires evidence that:
- sidebar navigation opens the room inside the middle workspace;
- the room does not create a second page or shell;
- Today Pulse values come from real available evidence;
- What Changed contains only observed/projected intelligence;
- Collective is the default mode;
- Personal, Collective, and Activity produce materially different projections when data exists;
- privacy boundaries are preserved;
- reload returns to a coherent Hub state;
- existing Hub navigation and frozen rooms still work;
- no permanent right rail is required by the room;
- implementation is identifiable by source commit and proof artifact/run.

## Freeze boundary
Once PROVEN, this room is frozen as a regression surface. Later room work may reuse its components/data contracts but may not remove or silently redefine its behavior.
