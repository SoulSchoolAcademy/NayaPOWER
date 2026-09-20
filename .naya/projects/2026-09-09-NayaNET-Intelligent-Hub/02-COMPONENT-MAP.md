# 02 — Component Map

Every component below is described as a reconstruction unit: what it shows, why it exists, behavior, state, data, dependencies, persistence and responsive rules.

## Shell components

### `.app`
- **Purpose:** global two-column desktop shell.
- **Desktop:** 250px sidebar + fluid main.
- **Mobile:** becomes block layout; sidebar hidden.
- **Data:** none.
- **Persistence:** none.
- **Dependency:** CSS grid and responsive media queries.

### `.sidebar`
- **Purpose:** primary navigation and trust/policy context.
- **Contents:** brand, Personal nav, Collective nav, Communication nav, System nav, privacy footer.
- **Behavior:** each nav button emits a `data-page` state transition.
- **State:** active page styling.
- **Persistence:** none; active state is DOM state.
- **Mobile:** hidden; replaced by `.mobileNav`.

### `.brand`
- **Purpose:** persistent identity anchor.
- **Logo:** `https://i.postimg.cc/LXJDD4Np/Nayanet-Logo.jpg`.
- **Text:** NayaNET / INTELLIGENT HUB · V7.
- **Interaction:** no click handler in audited source; treat as non-interactive unless intentionally upgraded.

### `.sidefoot`
- **Purpose:** communicate privacy architecture.
- **Text:** PRIVATE BY DEFAULT / Shared by choice / Collective by consent / Public by decision.
- **Interaction:** none.

### `.topbar`
- **Purpose:** persistent context + connection status.
- **Left:** current page title.
- **Right:** connection pill + Naya avatar.
- **Responsive:** height 74px desktop, 64px mobile.

### `.connectionPill`
- **Purpose:** source verification doorway.
- **Action:** `data-page="connections"` switches to Connections.
- **Visual:** status LED + `SOURCE · NOT VERIFIED` initially.
- **Success state:** GitHub verification changes LED to green and label to `GITHUB · VERIFIED`.
- **Persistence:** connection result is visual state; no server credential is stored by this page.

### `.avatar`
- **Purpose:** Naya identity/visual presence.
- **Image:** `https://i.postimg.cc/2S6dzKmC/Naya-Profile-3.jpg`.
- **Current behavior:** visual only; no click handler.

## Global navigation components

### Ecosystem bar
Eight anchors with exact destinations listed in Page Map. It is an external-navigation component, not internal application state.

### Feature Reports bar
Five external PDF/report anchors. Opens new tab/window. Must not be converted to dead decorative buttons.

### `.mobileNav`
- **Items:** Home, Notes, Reports, Intel, Mail.
- **Action:** same `data-page` state mechanism as desktop.
- **Position:** fixed bottom, 8px margins, 64px high.
- **Mobile only:** shown at max 900px.

## Home components

### Welcome component
- Dynamic greeting/time/date/country.
- Source: browser clock + locale.
- No server dependency.
- Updates every 30 seconds.

### Hero
- Mission statement and Naya visual.
- Original report CTA targets `reports`; later enhancement layers rewrite the CTA.
- Current architecture contains multiple competing refinements; rebuild must consolidate them into one deterministic component.

### Intelligent Feed header
- Feed pulse indicator.
- Title/description.
- Feed count.
- Toolbar with privacy and chronology statements.

### `#homeIntelligentBlocks`
- **Purpose:** feed renderer mount.
- **Input:** preserved Smart Notes and/or existing board content.
- **Renderer:** `nayanet-intelligent-feed-v6.js` plus several inline enhancement layers.
- **Required invariant:** one event should be renderable as one coherent intelligence block rather than multiple competing cards/columns.
- **Current renderer behavior:** forces descendant grids/columns into vertical flow, removes code/debug artifacts, applies a luminous vertical intelligence spine, and preserves reduced-motion support.
- **Critical risk:** the HTML contains many later inline scripts that also mutate the same feed. These are part of the forensic record but should not all survive into the rebuilt architecture.

## Smart Note components

### Note composer
- Textarea `#noteInput`.
- Create button `#createNote`.
- New-note button `#newNote` focuses composer.
- Later CSS hides the composer on the Smart Notes page, creating an architectural conflict that must be resolved deliberately.

### Search `#noteSearch`
- Local text filter over `nayanet_v7_live_notes`.
- No remote search API.
- Empty state is truthful.

### Type filters
- 11 explicit categories.
- Filter changes `filter` state and rerenders notes.

### Time filters
- Added by refinement layer.
- ALL TIME / BY HOUR / BY DAY / BY MONTH / BY YEAR / HIGHLIGHTS.
- Grouping is calculated client-side from `createdAt`.

### Note card
- Timestamp/type header.
- Human/Naya/Machine/Feed tabs.
- Human tab shows original note.
- Naya tab says synthesis pending when service absent.
- Machine tab exposes local event metadata.
- Feed tab describes chronological carry-forward.

## Reports components

### Report state panel
- Uses source events to create local compression.
- Does not claim semantic Naya synthesis.

### Compounding path
- Day 1 Capture.
- Day 2 Compare.
- Day 7 Pattern.
- Day 30 Learning.
- Day 365 Mastery.
- Lifetime Wisdom.

### Enhanced report
- Four cards: What Mattered / What Was Learned / What Carries Forward / What Deserves Attention Next.
- Uses current/past local notes according to day keys.

## Intelligence Library components

### Metrics
- Smart Notes count = length of local notes.
- Intelligent Blocks count = local notes length.
- Active Days = distinct local calendar days, default 1.
- Mail Drafts = local draft count.

### Reference cards
- Human Note, Naya Note, Machine Note, Intelligent Feed.
- Explain the four perspectives.

### Search index
- `IntelligenceIndex` builds from local blocks.
- Ranking rewards title matches, general text matches, favorites, collective state and recency.
- Results show up to eight items.

### Library tabs
- ALL / RECENT / FAVORITES / LISTS / GROUPS.
- Favorites, lists and groups are local state.

### Lists / Groups
- `IntelligenceStore` supports create/update/delete and membership operations.
- Lists are personal organization.
- Groups are thematic collections.
- Membership stores block IDs; the underlying block remains one event.

## Collective components

### Privacy pipeline board
Explains private source → de-identification → consent → collective wisdom.

### Collective toggle
- Changes `collective_enabled` in local settings.
- Visible state updates immediately.
- Does not publish data to a server.

### Collective feed
- Can show intentionally shared blocks.
- Personal view offers a START FREE link to the Human Maximus Codex checkout.

## Evidence components

### Event chain
Human → Naya → Machine → Feed → Receipt.

The key architectural purpose is to distinguish locally preserved evidence from server-verified evidence.

## Connections components

### GitHub source card
- Verify Source button calls GitHub REST API.
- View Repository button opens repository.
- Status changes visibly only after successful API response.

### Discovery card
- Search input.
- Discover button is intentionally blocked until a secure endpoint exists.
- No fabricated users.

## Smart Mail components

### Mailbox column
Tabs: Inbox, Sent, Drafts, Connections, Rooms, Groups, Lists.

### Alias card
Local alias storage; default `NayaABC123`.

### Center mail area
- Section title.
- Compose action.
- Inbox/empty/draft/thread content.
- Composer with recipient + message body.

### Communication modes column
Text, Audio, 1:1, Rooms, Groups, Lists.

### Draft behavior
`SEND MESSAGE` does not send. It validates recipient/body, writes a `pending_server_delivery` object to `nayanet_v7_mail_drafts`, then routes to Drafts.

## Settings components

Five switches with local state. Each is a boolean under `nayanet_v7_live_settings`.

### SAVE SETTINGS
Writes the current boolean object.

### RESET
Restores all five booleans to true and persists them.

## Intelligence engagement components

Later layers add:
- Favorite.
- Save.
- Like.
- Love.
- Rank 1–5.
- Comment.
- Share.
- Add to List.

These are local interactions in the current package. They are not equivalent to server-side social persistence.

## Feedback / Ask Naya utilities

- `GIVE FEEDBACK` writes feedback locally.
- `ASK NAYA` opens a modal.
- Current modal can search local preserved intelligence or return a truthful production-service-not-connected message.
- No actual remote Naya reasoning is performed by this static implementation.

## Public intelligence renderer

The `/intelligence/<id>` path reconstructs a public presentation from local block state when available. It includes Human/Naya/Machine sections and an ENTER NayaNET action. This is an architectural prototype of public sharing, not proof of a durable server-backed public intelligence object.
