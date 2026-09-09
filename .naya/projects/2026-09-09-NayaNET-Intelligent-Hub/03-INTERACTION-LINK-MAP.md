# 03 — Interaction + Link Map

## A. Internal navigation contract

Every internal page control uses `data-page` and the central `showPage(name)` handler.

### Navigation action
1. User clicks a desktop sidebar button, mobile nav button, connection pill, or internal `data-page` CTA.
2. Click handler prevents default behavior.
3. All `.page` sections lose `active`.
4. Target `#page-<name>` receives `active`.
5. All `[data-page]` controls update active styling.
6. Topbar page title is updated from the `titles` map.
7. Page-specific renderer runs.
8. Browser scrolls to top.

This is client-side state navigation, not a route request.

## B. Every desktop sidebar control

### PERSONAL
- **Home** → `home` → renders Home Feed.
- **Smart Notes** → `notes` → renders memory.
- **Reports** → `reports` → renders Daily Intelligence.
- **Intelligence Library** → `intelligence` → renders metrics/library/reference layer.

### COLLECTIVE
- **Collective** → `collective` → renders privacy/collective surface.
- **Evidence** → `evidence` → renders proof chain.
- **Connections** → `connections` → renders authorized-source and discovery controls.

### COMMUNICATION
- **Smart Mail** → `mail` → renders native communication workspace.

### SYSTEM
- **Settings** → `settings` → renders local operating controls.

## C. Topbar controls

### Connection pill
- Click → `connections`.
- Initial label: `SOURCE · NOT VERIFIED`.
- After successful GitHub API verification: `GITHUB · VERIFIED` and green LED.

### Naya avatar
- No click handler in audited source.
- Must not be treated as a hidden navigation control unless intentionally specified in rebuild.

## D. Ecosystem links

| Visible control | Destination | Behavior |
|---|---|---|
| HOME | `https://hmclibrary.groovemember.net/home` | native anchor |
| NAYA POWER | `https://academy.nayanet.app/` | native anchor |
| “5” DAY CHALLENGE | `https://academy.nayanet.app/` | native anchor |
| ENTER FREE | `https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab` | native anchor |
| POWERCASTS | `https://nayanet.groovepages.com/powerplayer` | native anchor |
| WHITE PAPER | `https://nayanet.groovepages.com/whitepaper` | native anchor |
| ABOUT US | `https://nayanet.groovepages.com/aboutus` | native anchor |
| HMC LOGIN | `https://hmclibrary.groovemember.net/login` | native anchor |

## E. Feature report links

All are external anchors with new-tab behavior.

- SMART NOTES → Google Drive file `19sRtp22aAn35wNoqqpNiZHkaFGmUOxoP`.
- NO DEAD ENDS → Google Drive file `1LgRmYAQ85AB6mmu6Qp2ovghyd1lP-FNh`.
- CONTEXT LAW → Google Drive file `1N-XzV3_RCTHuLdp4leZNlOo7ITFwrICR`.
- “10” STAR SERVICE → Google Drive file `1F9M66i5Av_oJcIa5dve-U0mMeAgYKczT`.
- ADAPTIVE LEARNING → Google Drive file `1dcViGUqV7GKnNBCYybbAEEKuOoZw3-XC`.

## F. Home actions

### Original DAILY INTELLIGENCE REPORT
- Click → `reports`.
- Later intelligence refinement can replace it with `WHAT SHOULD I KNOW TODAY?`.
- Current final intent should be deterministic: focus intelligence search/today surface, not run two competing actions.

### Naya / hero visual
- No independent click behavior.

### Feed block controls
Depending on active renderer layers, controls include:
- **Favorite** → toggle local favorite state.
- **Save** → toggle local saved state.
- **Like** → toggle local like state.
- **Love** → toggle local love state.
- **Rank** → prompt for 1–5; persist local rating.
- **Comment** → modal/prompt; append local comment.
- **Share** → native share when supported, otherwise clipboard or share-provider popup.
- **List** → select a local Naya List; membership stores block ID.

## G. Smart Notes interactions

### + NEW SMART NOTE
- Switches to `notes`.
- Focuses `#noteInput`.

### CREATE INTELLIGENT BLOCK
1. Read textarea.
2. Trim.
3. If empty, focus textarea and stop.
4. Create local object `{id, createdAt, text, type}`.
5. Type inferred from keyword heuristics.
6. Insert at front of `notes`.
7. Persist to `nayanet_v7_live_notes`.
8. Clear input.
9. Reset filter to ALL.
10. Rerender Notes.
11. Rerender Home Feed.
12. Recalculate Library metrics.

### Type filters
- Set global `filter` value.
- Re-render note list.
- No data mutation.

### Memory search
- Filters notes whose text includes the query.
- No remote request.

### Note tabs
- HUMAN → original source text.
- NAYA → pending-production message when service absent.
- MACHINE → JSON-like event metadata.
- INTELLIGENT FEED → carry-forward description.

### Time filters
- Hour/day/month/year → client-side grouping.
- Highlights → today's notes, or latest five if today is empty.

## H. Reports interactions

### GENERATE TODAY / REFRESH REPORT
- Reads locally preserved notes.
- Produces truthful local synthesis.
- No remote model call.
- Does not claim server verification.

## I. Intelligence Library interactions

### Search
- Local index over available blocks.
- Title match receives stronger score.
- Text/tag match receives smaller score.
- Favorites and recency can increase score.

### Library tabs
- ALL → all blocks.
- RECENT → sort by update time.
- FAVORITES → local favorite filter.
- LISTS → blocks assigned to lists.
- GROUPS → blocks assigned to groups.

### Lists / Groups
- Create → local ID + name + description + empty block membership.
- Edit → update local metadata.
- Delete → remove collection, not underlying intelligence block.
- Add block → append block ID if absent.
- Remove block → remove membership only.

## J. Collective interactions

### COLLECTIVE: ON/OFF
- Toggles `collective_enabled`.
- Persists in local settings.
- Changes eligibility statement.
- Does not publish to a collective backend.

### OPEN SETTINGS
- Internal navigation to `settings`.

### Personal view START FREE
- External destination: `https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab`.

## K. Evidence interactions

There are no destructive actions. The page is an inspection/proof surface.

## L. Connections interactions

### VERIFY SOURCE
- Fetch: `https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER`.
- Success → status text + green LED + `GITHUB · VERIFIED`.
- Failure → visible error and no success claim.

### VIEW REPOSITORY
- Opens `https://github.com/SoulSchoolAcademy/NayaPOWER` in a new tab/window.

### DISCOVER
- Current behavior: alert explaining secure discovery endpoint is unavailable.
- No people are fabricated.

### OPEN SMART MAIL
- Internal navigation to `mail`.

## M. Smart Mail interactions

### Mailbox tabs
- Inbox → clear inbox state.
- Sent → truthful empty/success boundary.
- Drafts → reads `nayanet_v7_mail_drafts`.
- Connections / Rooms / Groups / Lists → show contextual empty/placeholder state and OPEN COMPOSER action.

### + COMPOSE / COMPOSE
- Opens composer.
- Hides inbox area.
- Focuses recipient field.

### SEND MESSAGE
1. Read recipient and body.
2. If either missing, show required-field message; do not persist/send.
3. Otherwise create local draft object with `pending_server_delivery`.
4. Save to `nayanet_v7_mail_drafts`.
5. Show truthful blocked-delivery message.
6. Re-render mail and metrics.
7. Open Drafts.

### CANCEL
- Hide composer.
- Restore inbox content.

## N. Settings interactions

### Individual toggle
- Flip boolean in in-memory `settings` object.
- Toggle visual `.on` class.
- Not persisted until SAVE unless another subsystem explicitly saves the state.

### SAVE SETTINGS
- Write `nayanet_v7_live_settings`.
- Show `SAVE VERIFIED · settings persisted locally.`

### RESET
- Restore all five settings to true.
- Persist.
- Show `RESET VERIFIED · defaults restored locally.`

## O. Global feedback

### GIVE FEEDBACK
- Modal with Idea / Suggestion / Bug / Feature Request / Experience / Other.
- Stores feedback object locally.
- No remote ticket/API call in current package.

### ASK NAYA
- Opens support modal.
- Current static response explicitly states production Superbrain connection is not connected.
- Local search can provide a source-backed answer from preserved blocks in later V7 layers.
- No fabricated remote answer.

## P. Public intelligence interaction

`/intelligence/<id>`:
- Decode ID.
- Find local block.
- If absent → `Intelligence not found` page with ENTER NayaNET link.
- If present → render title, summary, Human, Naya, Machine and ENTER NayaNET.
- Target may use ambassador URL/ref state.

## Q. State and persistence map

| State | Storage | Persistent? | Server? |
|---|---|---:|---:|
| Smart Notes | `nayanet_v7_live_notes` | yes, browser-local | no |
| Settings | `nayanet_v7_live_settings` | yes, browser-local | no |
| Mail drafts | `nayanet_v7_mail_drafts` | yes, browser-local | no |
| Alias | `nayanet_v7_alias` | yes, browser-local | no |
| Intelligence engagement | `nayanet_v7_surgical_v1` and `nayanet_intelligent_blocks_v2` | yes, browser-local | no |
| Feed actions | `nayanet_intelligent_feed_actions_v1` | yes, browser-local | no |
| Ambassador/ref | local storage + URL ref | yes, browser-local when captured | no |
| GitHub verification | DOM state | session/runtime | API read only |
| Naya semantic synthesis | not present in static package | no | pending production service |
| Mail delivery | not present | no | pending production endpoint |
| People discovery | not present | no | pending secure endpoint |
