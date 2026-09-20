# 01 — NayaNET Intelligent Hub Page Map

## 1. Shell / global entry points

### Desktop shell
- **Left sidebar:** fixed/sticky 250px rail. It is the primary internal page switcher.
- **Topbar:** sticky 74px header. Left side displays current page title; right side contains source connection status and Naya avatar.
- **Ecosystem bar:** sticky horizontal link strip beneath the topbar.
- **Main:** page content area.
- **Feature Reports bar:** fixed bottom desktop strip containing five external PDF/report links.

### Mobile shell
- Desktop sidebar is hidden at `max-width:900px`.
- Topbar reduces to 64px.
- A fixed five-item bottom navigation replaces the sidebar.
- Ecosystem links remain horizontally scrollable.
- Feature Reports bar moves above the mobile bottom navigation.
- Mail's internal three-column workspace collapses to one column; the first mailbox column is hidden and the communication-modes column remains below the center area.

## 2. Internal page-state map

The application is one HTML document. Navigation is state-based through `data-page`, not separate HTML URLs.

| Page state | Internal key | Purpose | Main entry points | Main exits |
|---|---|---|---|---|
| Home / Your Intelligence Today | `home` | Primary intelligence feed and orientation surface | sidebar, mobile Home, connection from boot | sidebar, mobile nav, ecosystem links |
| Smart Notes | `notes` | Capture, search, filter and inspect persistent local intelligence | sidebar, mobile Notes, NEW SMART NOTE | all global nav |
| Daily Intelligence | `reports` | Daily compression of source events and carry-forward intelligence | sidebar, mobile Reports, Home report CTA | all global nav |
| Intelligence Library | `intelligence` | Search/reference layer and organized intelligence library | sidebar, mobile Intel, page metrics | all global nav |
| Collective | `collective` | Consent boundary for eligible de-identified collective intelligence | sidebar | Settings, all global nav |
| Evidence | `evidence` | Proof/receipt view distinguishing local evidence from verified backend evidence | sidebar | all global nav |
| Connections | `connections` | Authorized sources and people-discovery boundary | sidebar, connection pill, Connections CTA | Smart Mail, all global nav |
| Smart Mail | `mail` | Native private-network communication workspace | sidebar, mobile Mail, Open Smart Mail | all global nav |
| Settings | `settings` | Operating controls and privacy/intelligence switches | sidebar, Collective, all global nav | all global nav |

## 3. Ecosystem link map — exact current destinations

These are literal external `href` destinations in the audited source.

1. **HOME** → `https://hmclibrary.groovemember.net/home`
2. **NAYA POWER** → `https://academy.nayanet.app/`
3. **“5” DAY CHALLENGE** → `https://academy.nayanet.app/`
4. **ENTER FREE** → `https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab`
5. **POWERCASTS** → `https://nayanet.groovepages.com/powerplayer`
6. **WHITE PAPER** → `https://nayanet.groovepages.com/whitepaper`
7. **ABOUT US** → `https://nayanet.groovepages.com/aboutus`
8. **HMC LOGIN** → `https://hmclibrary.groovemember.net/login`

The important architectural note is that the visible **“5” DAY CHALLENGE** and **NAYA POWER** currently resolve to the same academy URL. A rebuild must preserve that exact mapping unless the destination is intentionally changed and documented.

## 4. Feature Reports link map — exact current destinations

Desktop: fixed bottom strip. Mobile: fixed above mobile navigation.

1. **SMART NOTES** → `https://drive.google.com/file/d/19sRtp22aAn35wNoqqpNiZHkaFGmUOxoP/view?usp=sharing`
2. **NO DEAD ENDS** → `https://drive.google.com/file/d/1LgRmYAQ85AB6mmu6Qp2ovghyd1lP-FNh/view?usp=sharing`
3. **CONTEXT LAW** → `https://drive.google.com/file/d/1N-XzV3_RCTHuLdp4leZNlOo7ITFwrICR/view?usp=sharing`
4. **“10” STAR SERVICE** → `https://drive.google.com/file/d/1F9M66i5Av_oJcIa5dve-U0mMeAgYKczT/view?usp=sharing`
5. **ADAPTIVE LEARNING** → `https://drive.google.com/file/d/1dcViGUqV7GKnNBCYybbAEEKuOoZw3-XC/view?usp=sharing`

All five use `target="_blank"` and `rel="noopener"`.

## 5. Home page map

### Welcome strip
- Dynamic greeting uses local browser time.
- Dynamic time/date use `Intl.DateTimeFormat`.
- Country is inferred from browser locale with a small CA/US/GB/AU/NZ map and defaults to Canada.
- This is presentation state; it is not server identity.

### Original hero
- Eyebrow: `NAYANET INTELLIGENT HUB · V7`.
- Headline explains connecting source, capturing what matters and compounding learning.
- Naya portrait panel says `Naya is here. LISTEN · EXPLAIN · GUIDE`.
- Original CTA initially points to the Daily Intelligence page, then later refinement layers can replace the visible CTA with `WHAT SHOULD I KNOW TODAY?` and focus the search field.
- Because multiple additive scripts rewrite the same surface, the rebuild must collapse this into one deterministic renderer.

### Intelligent Feed
- Header: `Intelligent Feed` in base source; later refinement layers rewrite the visible heading to variants including `SMART NOTES · INTELLIGENT BLOCKS` and `What should I know today?`.
- Feed count reports live-memory/local-event state.
- Feed toolbar says `ONE EVENT · MANY PERSPECTIVES` and `PRIVATE BY DEFAULT · chronological`.
- Feed mount: `#homeIntelligentBlocks`.
- `nayanet-intelligent-feed-v6.js` is loaded as a renderer/normalization layer.
- The source feed model supports one event with Human, Naya, Machine, and Intelligent Feed perspectives plus optional behavior/lesson content.

## 6. Smart Notes page map

- Header: `Smart Notes` / persistent intelligence.
- New-note composer exists in base HTML but later CSS hides it in favor of a memory-first surface; this conflict must be resolved in the rebuild.
- Search input: `Search your intelligence memory…`.
- Type filters: ALL, INSIGHT, MISTAKE, BREAKTHROUGH, DECISION, IDEA, LESSON, QUESTION, GOAL, WIN, OPPORTUNITY.
- Time organization layer adds: ALL TIME, BY HOUR, BY DAY, BY MONTH, BY YEAR, HIGHLIGHTS.
- Note cards expose Human / Naya / Machine / Intelligent Feed tabs.
- Current local persistence key: `nayanet_v7_live_notes`.

## 7. Daily Intelligence page map

- Header: `Daily Intelligence`.
- Base CTA: `GENERATE TODAY`; refinement changes it to `REFRESH REPORT`.
- Base page describes compounding path: Day 1 → Day 2 → Day 7 → Day 30 → Day 365 → Lifetime.
- Enhanced report uses: WHAT MATTERED / WHAT WAS LEARNED / WHAT CARRIES FORWARD / WHAT DESERVES ATTENTION NEXT.
- Current synthesis is local source synthesis, not remote Naya AI.

## 8. Intelligence Library page map

- Metrics: Smart Notes, Intelligent Blocks, Active Days, Mail Drafts.
- Four foundational perspectives: Human Note, Naya Note, Machine Note, Intelligent Feed.
- Later layers add searchable library, tabs for ALL / RECENT / FAVORITES / LISTS / GROUPS, engagement actions, lists and groups.
- Search is local and ranks title/text/tag matches.

## 9. Collective page map

- Privacy pipeline: NOTE PRIVATE → REPORT PRIVATE → EXTRACT VALUE → STRIP IDENTITY → SHARE CONSENT → COLLECTIVE WISDOM.
- Collective toggle controls local participation state.
- Settings is the deeper operating control.
- No private raw Smart Note is supposed to become public/collective silently.

## 10. Evidence page map

- Human: count of locally preserved events.
- Naya: pending production intelligence service.
- Machine: event identity/timestamp.
- Feed: count of current feed events.
- Receipt: explicitly says no verified server receipt in static package.
- This page is a truth boundary, not a cosmetic status dashboard.

## 11. Connections page map

### GitHub source
- Displays SoulSchoolAcademy / NayaPOWER as first authorized source.
- `VERIFY SOURCE` calls `https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER`.
- On success, connection pill becomes `GITHUB · VERIFIED` and green.
- `VIEW REPOSITORY` opens `https://github.com/SoulSchoolAcademy/NayaPOWER`.

### People discovery
- Input accepts topic/place, example `AI · Kelowna`.
- `DISCOVER` currently produces a truthful blocked alert because secure discovery endpoint is absent.
- `OPEN SMART MAIL` switches to `mail`.

## 12. Smart Mail page map

- Mailbox tabs: Inbox, Sent, Drafts, Connections, Rooms, Groups, Lists.
- Private alias display: default `NayaABC123`, overridable by local storage key `nayanet_v7_alias`.
- Communication modes: Text, Audio, 1:1, Rooms, Groups, Lists.
- Compose UI collects recipient alias and body.
- Send currently preserves a pending draft locally; it does **not** deliver to a server.
- Draft storage key: `nayanet_v7_mail_drafts`.

## 13. Settings page map

Five switches:
1. Smart Notes automatic
2. Intelligence layer
3. Connection notifications
4. Smart Mail
5. Collective contribution

Buttons:
- SAVE SETTINGS → writes local settings.
- RESET → restores all five defaults to true.

Settings storage key: `nayanet_v7_live_settings`.

## 14. Global floating utilities

Later intelligence layers can inject:
- `GIVE FEEDBACK` → stores feedback locally in `nayanet_v7_surgical_v1` or the V7 upgrade state.
- `ASK NAYA` → opens a local support modal. In the current static package, it explicitly refuses to fabricate a remote Superbrain answer.

## 15. Public intelligence path

The integrated intelligence layer defines a public path pattern:
`/intelligence/<encoded-block-id>`.

The deployment worker serves the Hub shell for `/intelligence/*`, so the route is an application-level path rather than a separate backend page. A public block is reconstructed from local runtime state in the current static implementation; this is not yet a server-backed durable public intelligence store.
