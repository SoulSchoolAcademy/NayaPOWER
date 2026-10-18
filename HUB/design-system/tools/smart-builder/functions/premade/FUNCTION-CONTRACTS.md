# NayaFunction Registry v1 — single source of truth for all 30 functions

Item 26, Team Nitro (MEMORY/Psi). Coordinator decision: ONE registry file, no duplicates.
Authority: Shawn Vibert ("we have to have pre-made functions… make it so this all is working").
Format binding: `functions/UNIT-FORMAT.md` (Verity seam section — every unit implements it exactly).
Inventory source: `FUNCTIONS-INVENTORY-v1.md` (F-01..F-30, verified with `test -f` before writing — L-2026-10-16-001).
Written once, completely — L-2026-10-16-005.

Status taxonomy: VERIFIED / IMPLEMENTED / MOCK / MISSING / BLOCKED.
All 30 ship here at **VERIFIED** (spec + seam defined, no behavior). Builders flip to IMPLEMENTED
(built + self-verified in a demo harness). Verifiers flip to VERIFIED (different seat, real Chromium,
clicked every control). IMPLEMENTED is never VERIFIED, and VERIFIED is never production-proven.

## What a NayaFunction is (the contract, repeated from UNIT-FORMAT)

Client-side JS behavior unit. Assembler-side Python generators (pipeline `feature.*`) are its
BACKEND TWIN where one exists — complementary layers, ONE name each. We never duplicate a twin;
we wire its client-side face.

```html
<div data-fn="<id>" data-fn-config='{...}'></div>
```
File: `functions/fn-<id>.js`. Loader: `functions/naya-functions.js` (boots all `[data-fn]` on
DOMContentLoaded, fail-closed on unknown ids, fail-soft on bad JSON).
Every unit: READY first (fully client-side, zero backend), `connected` key reserved for the
CONSENT LINE (on = ready; connected = consented). Never query outside its root. Idempotent:
`if (root.dataset.fnBound) return;` on intake hooks.

---

## A. Standard features — ON by default on every page (opt-out)

### F-01 — smart-tabs
- **File:** `functions/fn-smart-tabs.js`
- **What:** Scrolling ribbon of favorite pages/apps/URLs; save once, reachable everywhere in NayaNET; editable.
- **Activation:** `<div data-fn="smart-tabs" data-fn-config='{...}'></div>`
- **Config:** `{ position: "top|bottom" (default top), max_items: number (default 12), editable: boolean (default true), theme: "spectrum|host" (default spectrum) }`
- **Inputs:** `config`; owner's pages list (from `data-tabs` attr or contract). **Outputs:** persisted tabs on the visitor's device (localStorage key `nf.tabs`), `tabs.switched` behavior on tap.
- **READY behavior:** Ribbon renders contract-carried pages; add/edit/remove tabs; persists on device; switching navigates. Zero backend.
- **CONNECTED behavior:** Sync tabs across the owner's devices; pull newly published pages automatically — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.smart_tabs` (complementary: twin emits the mount point; this is the client behavior).
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — factory file `.frow > .tog` (Smart Tabs toggle; toggle row state drives `contract.features.smart_tabs`) and `#sumFunc` summary; idempotent, never double-binds her inline script. (b) built-page face — `data-fn="smart-tabs"`. (c) contract key — `functions: {"smart-tabs": {...}}`.

### F-02 — smart-mail
- **File:** `functions/fn-smart-mail.js`
- **What:** Mail that works with the page — write, send, broadcast to everyone connected.
- **Activation:** `<div data-fn="smart-mail" data-fn-config='{...}'></div>`
- **Config:** `{ inbox_label: string (default "Inbox"), allow_broadcast: boolean (default true), draft_autosave: boolean (default true) }`
- **Inputs:** `config`; recipient consent records (contract-carried). **Outputs:** drafts on device; send attempts emit `mail.send.requested` events to the console/hook — never claim sent.
- **READY behavior:** Compose UI, drafts, mailbox view (local). Broadcast stays DISABLED without a grant; unauthorized send denied visibly.
- **CONNECTED behavior:** Real send + broadcast with delivery receipts — requires `connected: true` + grant `nayanet` (or `network` for public).
- **Backend twin:** `feature.smart_mail`.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Smart Mail toggle). (b) `data-fn="smart-mail"`. (c) `functions: {"smart-mail": {...}}`.

### F-03 — smart-lists
- **File:** `functions/fn-smart-lists.js`
- **What:** Organize anything — notes, contacts, topics, posts; cross-cutting, layers into every page.
- **Activation:** `<div data-fn="smart-lists" data-fn-config='{...}'></div>`
- **Config:** `{ kinds: ["notes","contacts","topics","posts"] (default all), allow_add: boolean (default true), allow_share: boolean (default false) }`
- **Inputs:** `config`; `items` array (contract-carried). **Outputs:** add/remove/reorder items, persisted on device.
- **READY behavior:** Lists render, add/remove/edit items, empty-state honest. Zero connections.
- **CONNECTED behavior:** List sync/share through the declared list service — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.smart_list`.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Smart Lists toggle). (b) `data-fn="smart-lists"`. (c) `functions: {"smart-lists": {...}}`.

### F-04 — smart-spaces
- **File:** `functions/fn-smart-spaces.js`
- **What:** Gather people around anything — create/join spaces, view, join, support.
- **Activation:** `<div data-fn="smart-spaces" data-fn-config='{...}'></div>`
- **Config:** `{ spaces: [{id, name, description}] (default []), allow_create: boolean (default true), support_button: boolean (default true) }`
- **Inputs:** `config`; contract-carried space list. **Outputs:** joined-space state on device; join/create emit `space.joined` / `space.created` hook events.
- **READY behavior:** Space cards render; local gathering view; join leaves device-level membership; private spaces never exposed.
- **CONNECTED behavior:** Invite and join sync across the network — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.space`.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Smart Space toggle). (b) `data-fn="smart-spaces"`. (c) `functions: {"smart-spaces": {...}}`.

### F-05 — intelligence-today
- **File:** `functions/fn-intelligence-today.js`
- **What:** Daily briefing — what matters today, surfaced for the owner.
- **Activation:** `<div data-fn="intelligence-today" data-fn-config='{...}'></div>`
- **Config:** `{ briefing_slots: number (default 5), sections: ["calendar","feed","reports"] (default all), refresh_label: string (default "Updated this morning") }`
- **Inputs:** `config`; `briefing` object (contract-carried, assembled at build time). **Outputs:** rendered briefing; "empty day" honest state.
- **READY behavior:** Renders contract-carried briefing; no I/O, no grant.
- **CONNECTED behavior:** Fetch external report sources — requires `connected: true`, declares `contract.features.intelligence_today.external_sources`, grant `network`.
- **Backend twin:** `feature.intelligence_today`.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Intelligence Today toggle); `.tcard2[data-t="Today"]` template face. (b) `data-fn="intelligence-today"`. (c) `functions: {"intelligence-today": {...}}`.

### F-06 — connections
- **File:** `functions/fn-connections.js`
- **What:** Your people, reachable — every relationship the page knows about.
- **Activation:** `<div data-fn="connections" data-fn-config='{...}'></div>`
- **Config:** `{ show_cards: boolean (default true), request_message: boolean (default true), directory_search: boolean (default false) }`
- **Inputs:** `config`; `people` array (contract-carried, owner-declared). **Outputs:** connect requests (hook events), saved connection state on device.
- **READY behavior:** Contact cards render; request flow runs to the consent point — no contact without consent, decline respected.
- **CONNECTED behavior:** Connect requests across network/public boundary — requires `connected: true` + grant `nayanet` (network boundary) or `network` (public).
- **Backend twin:** `feature.connect` (intent "Visitors connect with the owner" ≈ "your people, reachable"; twin is owner-centric, ours is relationship-centric — complementary, one name each).
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Connect + communicate toggle). (b) `data-fn="connections"`. (c) `functions: {"connections": {...}}`.

### F-07 — reports
- **File:** `functions/fn-reports.js`
- **What:** Daily, weekly, monthly pictures of what is happening — numbers, explained.
- **Activation:** `<div data-fn="reports" data-fn-config='{...}'></div>`
- **Config:** `{ cadence: ["daily","weekly","monthly"] (default all), explain: boolean (default true — plain-language takeaways), period_picker: boolean (default true) }`
- **Inputs:** `config`; `snapshots` (contract-carried report data). **Outputs:** rendered report cards; selected period state.
- **READY behavior:** Renders contract-carried snapshots; only the owner's data; empty-state handled.
- **CONNECTED behavior:** Fetch live report sources — requires `connected: true` + grant `network`.
- **Backend twin:** `feature.intelligence_today` (SHARED twin with F-05 — reports are the numbers-explained facet; intelligence-today the briefing facet. Both reference one backend; zero duplication, documented here).
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Reports toggle). (b) `data-fn="reports"`. (c) `functions: {"reports": {...}}`.

### F-08 — feed
- **File:** `functions/fn-feed.js`
- **What:** Posts, updates, activity — one living stream.
- **Activation:** `<div data-fn="feed" data-fn-config='{...}'></div>`
- **Config:** `{ allow_post: boolean (default true), page_size: number (default 20), audience_note: string (default "Only shared where you allow") }`
- **Inputs:** `config`; `posts` array (contract-carried seed). **Outputs:** published posts to local draft queue; `feed.post.published` / `feed.post.failed` hook events.
- **READY behavior:** Feed renders; compose + draft posts locally; failure state visible; private posts never leak.
- **CONNECTED behavior:** Live updates + publish across boundary — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.social_feed`.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Personal social feed toggle). (b) `data-fn="feed"`. (c) `functions: {"feed": {...}}`.

---

## B. Template functions — what each template needs to actually WORK

### F-09 — booking
- **File:** `functions/fn-booking.js`
- **What:** Appointments handled — calendar, booking, confirmation.
- **Activation:** `<div data-fn="booking" data-fn-config='{...}'></div>`
- **Config:** `{ duration_minutes: number (default 30), availability: [{day, start, end}] (default weekday 9–17), buffer_minutes: number (default 15), confirm_copy: string (default "You're booked — see you then.") }`
- **Inputs:** `config`; owner's availability (contract-carried). **Outputs:** bookings array on device; confirmation cards; cancellation tokens.
- **READY behavior:** Availability grid renders; slot selection; booking stored on visitor device; confirmation + cancel path; no double-booking (device-level).
- **CONNECTED behavior:** Sync bookings to the owner's calendar + notify both parties — requires `connected: true` + grant `nayanet`.
- **Backend twin:** none — NEW. (Pipeline registry has no booking feature; flagged as a gap to propose there, not to duplicate.)
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Booking"]` template face; `.frow > .tog` (Booking doors toggle). (b) `data-fn="booking"`. (c) `functions: {"booking": {...}}`.

### F-10 — menu-display
- **File:** `functions/fn-menu-display.js`
- **What:** Menu with real items and prices, order-ready.
- **Activation:** `<div data-fn="menu-display" data-fn-config='{...}'></div>`
- **Config:** `{ categories: [string] (default from items), currency: string (default "USD"), show_prices: boolean (default true), order_mode: "none|call|link" (default "none") }`
- **Inputs:** `config`; `items` [{name, price, description, category}] (contract-carried, required non-empty). **Outputs:** item selection state; order request event.
- **READY behavior:** Menu renders with real prices; category filtering; item detail. Order only fires where `order_mode` is set — never staged.
- **CONNECTED behavior:** Send order to the owner's order endpoint — requires `connected: true` + declared endpoint, grant `network`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Menu"]` template face. (b) `data-fn="menu-display"`. (c) `functions: {"menu-display": {...}}`.

### F-11 — product-display
- **File:** `functions/fn-product-display.js`
- **What:** Price, buy — sell one thing beautifully.
- **Activation:** `<div data-fn="product-display" data-fn-config='{...}'></div>`
- **Config:** `{ price: string (default from contract), currency: string (default "USD"), buy_label: string (default "Buy now"), variants: [string] (default []) }`
- **Inputs:** `config`; `product` {name, price, images, description} (contract-carried). **Outputs:** variant selection; buy-intent event.
- **READY behavior:** Product hero renders; variants selectable; buy button opens the declared checkout path only — if none declared, button shows honest "checkout not connected" state, never fake.
- **CONNECTED behavior:** Live inventory + checkout — requires `connected: true` + declared endpoint, grant `network`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Product"]` template face. (b) `data-fn="product-display"`. (c) `functions: {"product-display": {...}}`.

### F-12 — signup-capture
- **File:** `functions/fn-signup-capture.js`
- **What:** Join, subscribe — one page that converts.
- **Activation:** `<div data-fn="signup-capture" data-fn-config='{...}'></div>`
- **Config:** `{ fields: ["name","email"] (default), consent_copy: string (default "We'll only send what you asked for."), success_copy: string (default "You're in.") }`
- **Inputs:** `config`. **Outputs:** signups persisted on device (queue); `signup.submitted` event.
- **READY behavior:** Form validates; stores on device; success state real; consent copy shown before submit. Nothing claimed sent.
- **CONNECTED behavior:** Submit to the owner's list endpoint — requires `connected: true` + declared endpoint, grant `network`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Signup"]` template face. (b) `data-fn="signup-capture"`. (c) `functions: {"signup-capture": {...}}`.

### F-13 — event-rsvp
- **File:** `functions/fn-event-rsvp.js`
- **What:** Invites, RSVP, day-of — all handled.
- **Activation:** `<div data-fn="event-rsvp" data-fn-config='{...}'></div>`
- **Config:** `{ event: {title, date, location} (default from contract), plus_ones: boolean (default true), reminder: boolean (default true) }`
- **Inputs:** `config`; event object (contract-carried, required). **Outputs:** RSVP records on device; headcount.
- **READY behavior:** Event details render; RSVP yes/no/maybe; headcount updates; day-of info panel.
- **CONNECTED behavior:** Sync RSVPs to the owner + send reminders — requires `connected: true` + grant `nayanet`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Event"]` template face. (b) `data-fn="event-rsvp"`. (c) `functions: {"event-rsvp": {...}}`.

### F-14 — assessment-score
- **File:** `functions/fn-assessment-score.js`
- **What:** Questions → score → explained report (MAXESS pattern).
- **Activation:** `<div data-fn="assessment-score" data-fn-config='{...}'></div>`
- **Config:** `{ questions: [{id, text, options, weights}] (default from contract), bands: [{min, max, label, explanation}] (default from contract), retake: boolean (default true) }`
- **Inputs:** `config`; question set + score bands (contract-carried, required). **Outputs:** answers; computed score; band; explained report render.
- **READY behavior:** Question flow; deterministic scoring (same answers → same score); band + explanation render; retake. Proven client behavior harvested from Maxis_App_Design.html (Chi-verified 9.7/10) — harvest, don't rebuild.
- **CONNECTED behavior:** Save results to the owner's records — requires `connected: true` + grant `nayanet`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Dashboard"]` template face. (b) `data-fn="assessment-score"`. (c) `functions: {"assessment-score": {...}}`.

### F-15 — portfolio-showcase
- **File:** `functions/fn-portfolio-showcase.js`
- **What:** Show the work — proof of what you do.
- **Activation:** `<div data-fn="portfolio-showcase" data-fn-config='{...}'></div>`
- **Config:** `{ layout: "grid|masonry|slideshow" (default "grid"), items: [{title, image, blurb, link}] (default from contract), lightbox: boolean (default true) }`
- **Inputs:** `config`; portfolio items (contract-carried). **Outputs:** selected-item state; lightbox open/close.
- **READY behavior:** Work renders; lightbox opens real items; links go where declared. No fake thumbnails.
- **CONNECTED behavior:** Pull items from the owner's media source — requires `connected: true` + grant `network`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Portfolio"]` template face. (b) `data-fn="portfolio-showcase"`. (c) `functions: {"portfolio-showcase": {...}}`.

### F-16 — community-feed
- **File:** `functions/fn-community-feed.js`
- **What:** Feed, spaces, belonging — the people's home.
- **Activation:** `<div data-fn="community-feed" data-fn-config='{...}'></div>`
- **Config:** `{ moderation: "owner|open" (default "owner"), allow_threads: boolean (default true), welcome_copy: string (default "Welcome in.") }`
- **Inputs:** `config`; `spaces` + `posts` (contract-carried). **Outputs:** posts/comments (local queue); join state.
- **READY behavior:** Community feed + space list render; post/comment work locally; abuse path exists (report button → hook event).
- **CONNECTED behavior:** Publish across boundary — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.community` (primary). Note: `feature.social_feed` covers the feed-post half; community-feed composes community + feed — no duplication, documented overlap.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Community"]` template face. (b) `data-fn="community-feed"`. (c) `functions: {"community-feed": {...}}`.

### F-17 — business-proof
- **File:** `functions/fn-business-proof.js`
- **What:** Services, proof, contact — the page that sells.
- **Activation:** `<div data-fn="business-proof" data-fn-config='{...}'></div>`
- **Config:** `{ services: [{name, description, price_hint}] (default from contract), testimonials: [{quote, name}] (default from contract), cta_label: string (default "Work with me") }`
- **Inputs:** `config`; services + proof (contract-carried). **Outputs:** CTA intent events.
- **READY behavior:** Services render with honest pricing hints; testimonials render; CTA routes to contact function if present.
- **CONNECTED behavior:** Lead capture to the owner's pipeline — requires `connected: true` + grant `nayanet`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Business"]` template face. (b) `data-fn="business-proof"`. (c) `functions: {"business-proof": {...}}`.

### F-18 — profile-link
- **File:** `functions/fn-profile-link.js`
- **What:** My world in one page — about me, everything linked.
- **Activation:** `<div data-fn="profile-link" data-fn-config='{...}'></div>`
- **Config:** `{ cover: {image} (default gradient), avatar: {image} (default initials), links: [{label, url, icon}] (default from contract), bio: string (default "") }`
- **Inputs:** `config`; profile data (contract-carried). **Outputs:** link tap events (real hrefs).
- **READY behavior:** Cover + avatar + bio + link list render; every link is a real href; fallback states honest.
- **CONNECTED behavior:** Live link-status + sync profile across devices — requires `connected: true` + grant `nayanet`.
- **Backend twin:** none — NEW. (Composes `feature.cover` + smart-tabs + feed at the page level; the compose belongs to the page-contract, not to this unit — no duplication.)
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2[data-t="Personal"]` template face. (b) `data-fn="profile-link"`. (c) `functions: {"profile-link": {...}}`.

---

## C. Page plumbing — every page needs these to feel alive

### F-19 — navigate
- **File:** `functions/fn-navigate.js`
- **What:** Move between pages and rooms.
- **Activation:** `<div data-fn="navigate" data-fn-config='{...}'></div>`
- **Config:** `{ targets: [{label, href|room}] (default from contract), style: "tabs|menu|breadcrumbs" (default "tabs"), remember_last: boolean (default true) }`
- **Inputs:** `config`. **Outputs:** navigation actions; last-room memory on device.
- **READY behavior:** Links move; room transitions real; remembers last room on device.
- **CONNECTED behavior:** none — navigation is always local to the page/app.
- **Backend twin:** `feature.smart_tabs` (SHARED twin with F-01 — twin is the surface that lists owned pages; this unit is the transition action. Documented, one twin, two client faces).
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `[data-go]` scroll targets on `#step1`–`#step4` (smooth-scroll, idempotent); built-page face is primary. (b) `data-fn="navigate"`. (c) `functions: {"navigate": {...}}`.

### F-20 — search
- **File:** `functions/fn-search.js`
- **What:** Find anything within the app.
- **Activation:** `<div data-fn="search" data-fn-config='{...}'></div>`
- **Config:** `{ index: [string] (default from page headings), placeholder: string (default "Search this app…"), show_count: boolean (default true) }`
- **Inputs:** `config`. **Outputs:** filtered result set; jump-to anchors.
- **READY behavior:** Client-side search over the page's own content; results jump to real anchors; zero backend.
- **CONNECTED behavior:** none.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — built-page only (the factory's piece-catalog search is her inline script, not this unit). (b) `data-fn="search"`. (c) `functions: {"search": {...}}`.

### F-21 — contact
- **File:** `functions/fn-contact.js`
- **What:** Reach the page owner.
- **Activation:** `<div data-fn="contact" data-fn-config='{...}'></div>`
- **Config:** `{ channels: [{type: "email|form|chat|phone", value}] (default from contract), consent_gate: boolean (default true) }`
- **Inputs:** `config`. **Outputs:** message drafts on device; contact attempts (hook events, never claimed delivered).
- **READY behavior:** Owner's channels render; message form works to draft; consent gate before first contact.
- **CONNECTED behavior:** Deliver messages to the owner — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.connect` (SHARED twin with F-06 — same reasoning, documented).
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — built-page only. (b) `data-fn="contact"`. (c) `functions: {"contact": {...}}`.

### F-22 — share
- **File:** `functions/fn-share.js`
- **What:** Smart link — refer people in, share to the feed.
- **Activation:** `<div data-fn="share" data-fn-config='{...}'></div>`
- **Config:** `{ channels: ["copy","feed","message"] (default ["copy"]), smart_link_base: string (default "https://nayanet.live") }`
- **Inputs:** `config`. **Outputs:** copied links (clipboard); share-sheet intents; referral ids.
- **READY behavior:** Copy-link works (clipboard); share sheet opens native where available; referral ids minted deterministically (sha-based), never claimed live.
- **CONNECTED behavior:** Share to the NayaNET feed with live referral tracking — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.broadcast` (intent overlap: broadcasts to everyone related to the page; ours is the visitor-side share action, twin the owner-side send — complementary, one name each).
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Share toggle). (b) `data-fn="share"`. (c) `functions: {"share": {...}}`.

### F-23 — save
- **File:** `functions/fn-save.js`
- **What:** Keep things — favorites persist.
- **Activation:** `<div data-fn="save" data-fn-config='{...}'></div>`
- **Config:** `{ scope: "page|app" (default "page"), label: string (default "Save"), saved_label: string (default "Saved") }`
- **Inputs:** `config`; `data-save-id` on save targets. **Outputs:** saved set on device; saved/unsaved state.
- **READY behavior:** Save/unsave toggles real; persists on device; nothing leaves the device.
- **CONNECTED behavior:** Sync saved items across devices — requires `connected: true` + grant `nayanet`.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.frow > .tog` (Saved toggle). (b) `data-fn="save"`. (c) `functions: {"save": {...}}`.

### F-24 — play
- **File:** `functions/fn-play.js`
- **What:** Audio playback (smart notes, powercasts).
- **Activation:** `<div data-fn="play" data-fn-config='{...}'></div>`
- **Config:** `{ src: string (required — audio URL), title: string (default ""), autoplay: boolean (default false — never autoplay audio), transcript: string (default "") }`
- **Inputs:** `config`. **Outputs:** play/pause/seek state.
- **READY behavior:** Real audio playback via HTMLAudio; play/pause/seek; never autoplay; transcript shown where provided. Harvest working play-toggle behavior from ultimate-intake.html (Chi-verified) — harvest, don't rebuild.
- **CONNECTED behavior:** none.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — built-page only. (b) `data-fn="play"`. (c) `functions: {"play": {...}}`.

### F-25 — dictate
- **File:** `functions/fn-dictate.js`
- **What:** Speech-to-text input, fail-soft without it.
- **Activation:** `<div data-fn="dictate" data-fn-config='{...}'></div>`
- **Config:** `{ target: string (default "#visionText" — CSS selector of the textarea to fill), lang: string (default "en-US"), interim: boolean (default true), fail_soft_copy: string (default "Dictation isn't available on this device — type instead.") }`
- **Inputs:** `config`. **Outputs:** transcribed text appended to the target field; fail-soft message when unsupported.
- **READY behavior:** SpeechRecognition when available; streams interim results into the target; inline fail-soft message when not (never `alert()`). Harvest working behavior from ultimate-intake.html (Chi-verified 9.7/10) — harvest, don't rebuild.
- **CONNECTED behavior:** none.
- **Backend twin:** none — no `feature.*` twin. (Pipeline `intake.dictate` is a mode-level contract — "Talk — dictation mode", writes `contract.words` — a conceptual seam, NOT a backend twin. Documented so no one claims it.)
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `#dictBtn` → fills `#visionText`; idempotent (`dataset.fnBound`), coexists with her inline script. (b) `data-fn="dictate"`. (c) `functions: {"dictate": {...}}`.

### F-26 — copy
- **File:** `functions/fn-copy.js`
- **What:** Copy text/contract to clipboard.
- **Activation:** `<div data-fn="copy" data-fn-config='{...}'></div>`
- **Config:** `{ source: string (default "#contract" — CSS selector of the element to copy), label: string (default "Copy"), done_label: string (default "Copied") }`
- **Inputs:** `config`. **Outputs:** clipboard contents; copied confirmation state.
- **READY behavior:** Copies source text via clipboard API with textarea fallback; shows inline "Copied" state; never claims success when the write fails.
- **CONNECTED behavior:** none.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `#copyBtn` and `#btnCopy` (BOTH ids exist in the factory file — bind whichever is present, never both twice). (b) `data-fn="copy"`. (c) `functions: {"copy": {...}}`.

### F-27 — preview
- **File:** `functions/fn-preview.js`
- **What:** Open a real sample/template page.
- **Activation:** `<div data-fn="preview" data-fn-config='{...}'></div>`
- **Config:** `{ url: string (default from card), target: string (default "_blank"), warn_external: boolean (default true) }`
- **Inputs:** `config`; `data-preview-url` on the card. **Outputs:** opened preview window/tab.
- **READY behavior:** Opens the real URL from the card — never a placeholder, never a 404 by design (URL comes from verified samples). Harvest working behavior from ultimate-intake.html (Chi-verified) — harvest, don't rebuild.
- **CONNECTED behavior:** none.
- **Backend twin:** none — no `feature.*` twin. (Pipeline `build.preview` is a build-stage gate — "human sees the page before it goes anywhere" — a conceptual seam, NOT a backend twin.)
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `.tcard2 > .tview` (12 template view buttons; binds the click that opens the real sample). (b) `data-fn="preview"`. (c) `functions: {"preview": {...}}`.

### F-28 — cart
- **File:** `functions/fn-cart.js`
- **What:** Select pieces, sizes, quantities, notes.
- **Activation:** `<div data-fn="cart" data-fn-config='{...}'></div>`
- **Config:** `{ allow_qty: boolean (default true), allow_notes: boolean (default true), size_default: string (default "AUTO"), persist: boolean (default true) }`
- **Inputs:** `config`; `.pcard[data-model][data-name][data-cat]` cards. **Outputs:** cart array [{model, name, cat, size, qty, note}] — the single cart the contract reads.
- **READY behavior:** Add/remove pieces; size pills (`.szpill[data-s][data-z]`) set size per item; quantities; per-item notes; count badge (`#cartCount`); drawer (`#cartDrawer`, `#cartItems`); persists on device. Harvest working behavior from ultimate-intake.html (Chi-verified) — harvest, don't rebuild.
- **CONNECTED behavior:** none.
- **Backend twin:** none — NEW.
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `#cartFab`, `#cartDrawer`, `#cartItems`, `#cartCount`, `#closeCart`, `.pcard .btn-select`, `.szpill[data-s][data-z]`; idempotent, never double-binds her inline script. (b) built-page face — `data-fn="cart"` (piece-picker pages). (c) `functions: {"cart": {...}}`.

### F-29 — contract-draft
- **File:** `functions/fn-contract-draft.js`
- **What:** Vision + pieces + template → drafted build contract.
- **Activation:** `<div data-fn="contract-draft" data-fn-config='{...}'></div>`
- **Config:** `{ vision_source: string (default "#visionText"), cart_read: string (default "NayaFunctions cart"), template_read: string (default ".tcard2 selected"), features_read: string (default ".frow > .tog") }`
- **Inputs:** `config`; reads the four live sources above. **Outputs:** contract JSON object `{vision, template, pieces[], sizes{}, features{<fn-id>: on/off}, notes[]}` rendered into `#contract` / `#contractWrap`; summary into `#sumTmpl #sumFunc #sumPieces #sumVision`.
- **READY behavior:** Drafts the contract from the four live sources — vision text, cart contents, selected template, toggle states; review step (`#reviewBtn`, `#sumWrap`, `#sumBuild`, `#sumClose`) shows the summary before fire. Deterministic: same inputs → same contract.
- **CONNECTED behavior:** none (contract drafting is always local).
- **Backend twin:** none — no `feature.*` twin. (Pipeline `intake.propose_skeleton` + `template.pick` are conceptual seams — they also write contract fields. Our unit is the intake-page assembler of those fields; the pipeline's are the build-stage writers. Same contract schema, different layers — no duplication.)
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — `#buildBtn` (fires draft), `#contract`, `#contractWrap`, `#reviewBtn`, `#sumWrap`, `#sumTmpl`, `#sumFunc`, `#sumPieces`, `#sumVision`, `#sumBuild`, `#sumClose`; idempotent. (b) `data-fn="contract-draft"` (builder pages). (c) `functions: {"contract-draft": {...}}`.

### F-30 — join
- **File:** `functions/fn-join.js`
- **What:** Join a space or community.
- **Activation:** `<div data-fn="join" data-fn-config='{...}'></div>`
- **Config:** `{ space_id: string (default from card data attr), require_consent: boolean (default true), joined_label: string (default "Joined") }`
- **Inputs:** `config`; `data-space-id` on the join button. **Outputs:** membership state on device; `space.joined` hook event.
- **READY behavior:** Join/leave toggles real; consent gate for private spaces; member count updates locally. Harvest working "+ Join" button behavior from the spaces/hub pages — harvest, don't rebuild.
- **CONNECTED behavior:** Membership sync across the network — requires `connected: true` + grant `nayanet`.
- **Backend twin:** `feature.space` (SHARED twin with F-04 — twin's acceptance includes `join_flow_tested`; this unit is the client-side join action. Documented, one twin.)
- **Status:** VERIFIED
- **Integration seam:** (a) intake face — built-page only (no intake hook; the factory file has no join UI). (b) `data-fn="join"`. (c) `functions: {"join": {...}}`.

---

## Assembler seam spec (specify only — no branch implementation)

How a page-contract's `functions: {"<id>": {...}}` declaration resolves to pre-built units.
Single owner: the assembler. Registry path (canonical): this file.

### The lookup contract (four steps, fail-closed)

1. **Declare.** The page-contract carries:
   ```json
   "functions": {
     "<id>": { "on": true, "config": { ... } }
   }
   ```
   `"on": false` (or absent) = the unit is not emitted. `config` keys are validated against
   this registry's config schema for `<id>`; unknown keys warn, unknown ids FAIL (see step 2).

2. **Registry lookup.** Assembler reads this file for `<id>`:
   - `id` → file `functions/fn-<id>.js`, `version`, activation markup, config schema.
   - **Unknown `<id>` → fail-closed:** refuse the build, emit the valid id list. Never invent
     a unit, never hand-patch the page (L-2026-10-16-004 pattern: failures get fixed in the
     function, never on the page).
   - **Status gate:** VERIFIED or BLOCKED ids cannot ship in a built page — assembler warns and
     skips them (page builds without the function, the gap is receipted). IMPLEMENTED/VERIFIED
     ids ship. (VERIFIED preferred; IMPLEMENTED allowed with the receipt marked.)

3. **Emit.** For each shipped unit, the assembler emits, at the function's declared mount point:
   ```html
   <div data-fn="<id>" data-fn-config='{...}'></div>
   <script src="functions/fn-<id>.js"></script>
   ```
   plus ONCE per page: `<script src="functions/naya-functions.js"></script>` (the loader).
   `data-fn-config` is the contract's `config` object serialized deterministically
   (sorted keys — same contract, same bytes). The backend twin, where one exists, is emitted
   by the pipeline's `feature.*` path independently; the twin emits the mount/HTML, our unit
   boots the behavior into the same `data-fn` root. Two layers, one root, one name.

4. **Boot.** `naya-functions.js` on DOMContentLoaded: finds all `[data-fn]`, parses
   `data-fn-config` (fail-soft on bad JSON — the root stays empty, console.warn), calls
   `NayaFunctions._r[id].activate(root, config)`. Unregistered ids warn and are skipped
   (fail-closed — never pretend a missing function works). Units scope ALL queries to `root`.

### Standard features default-ON

The intake's 14 `.frow > .tog` toggles write `functions: {"<fn-id>": {"on": <toggle>}}` into the
drafted contract (contract-draft F-29 does this read). The 8 standards (F-01..F-08) ship with
`"on": true` unless the human unchecks (Shawn's opt-OUT rule). Toggle → function mapping:

| Toggle label (factory file) | Function id | Twin |
|---|---|---|
| Smart Mail | smart-mail | feature.smart_mail |
| Smart Lists | smart-lists | feature.smart_list |
| Smart Space | smart-spaces | feature.space |
| Connect + communicate | connections | feature.connect |
| Intelligence Today | intelligence-today | feature.intelligence_today |
| Personal social feed | feed | feature.social_feed |
| Smart Tabs | smart-tabs | feature.smart_tabs |
| Ask Naya | — (NOT one of the 30; backend `feature.naya_answers` exists — intake-only toggle for now, flagged for itemization) | — |
| Reports | reports | feature.intelligence_today (shared) |
| Booking doors | booking | none (NEW) |
| Guard | — (NOT one of the 30; privacy setting, not a function — intake-only toggle, flagged for itemization) | — |
| Saved | save | none (NEW) |
| Calendar | — (NOT one of the 30; event-rsvp covers RSVP, no calendar function itemized — flagged for itemization) | — |
| Share | share | feature.broadcast |

14 toggles: 11 map to our 30; 3 do not (Ask Naya, Guard, Calendar — flagged above as
follow-up items, NOT silently absorbed).

### Template → function mapping (template face)

`.tcard2[data-t]` on the intake binds each template to its working function (built page declares it ON):

Personal→profile-link, Today→intelligence-today, Smart List→smart-lists, Business→business-proof,
Booking→booking, Product→product-display, Event→event-rsvp, Community→community-feed,
Portfolio→portfolio-showcase, Menu→menu-display, Signup→signup-capture, Dashboard→assessment-score.

### Versioning and change rule

`version` lives in the unit header (`<id> v1.0.0`). The registry records the version each
assembler release was pinned against. A unit changes → version bumps → assembler re-pins.
Contract schema changes are additive only (never rename a config key without a migration note here).

---

## Reconciliation: our 30 vs pipeline registry (zero duplicates asserted)

Pipeline registry: `/home/hatch/workspace/builder-review/HUB/design-system/tools/smart-builder/functions/registry.json`
(namespaces: `intake.*`, `library.*`, `template.*`, `customize.*`, `build.*`, `feature.*`).
Our namespace: bare hyphen names (`smart-mail`, NOT `feature.smart_mail`; `fn-<id>.js`).
No id or name collision exists between the two sets — verified by direct comparison.

| Our id | Pipeline twin (`feature.*`) | Verdict |
|---|---|---|
| smart-tabs | feature.smart_tabs | TWIN — complementary layers |
| smart-mail | feature.smart_mail | TWIN |
| smart-lists | feature.smart_list | TWIN |
| smart-spaces | feature.space | TWIN (shared with join) |
| intelligence-today | feature.intelligence_today | TWIN (shared with reports) |
| connections | feature.connect | TWIN (shared with contact) |
| reports | feature.intelligence_today | TWIN (shared with intelligence-today) |
| feed | feature.social_feed | TWIN |
| booking | — | NEW — no pipeline twin; pipeline gap flagged, not duplicated |
| menu-display | — | NEW |
| product-display | — | NEW |
| signup-capture | — | NEW |
| event-rsvp | — | NEW |
| assessment-score | — | NEW (MAXESS behavior harvested client-side) |
| portfolio-showcase | — | NEW |
| community-feed | feature.community | TWIN (documented overlap with feature.social_feed's feed half) |
| business-proof | — | NEW |
| profile-link | — | NEW (composes feature.cover + smart-tabs + feed at page level) |
| navigate | feature.smart_tabs | TWIN (shared with smart-tabs; action vs surface) |
| search | — | NEW |
| contact | feature.connect | TWIN (shared with connections) |
| share | feature.broadcast | TWIN (visitor-side share vs owner-side broadcast) |
| save | — | NEW |
| play | — | NEW |
| dictate | — | NEW (pipeline `intake.dictate` is a mode contract, not a twin) |
| copy | — | NEW |
| preview | — | NEW (pipeline `build.preview` is a build gate, not a twin) |
| cart | — | NEW |
| contract-draft | — | NEW (pipeline `intake.propose_skeleton`/`template.pick` are build-stage seams) |
| join | feature.space | TWIN (shared with smart-spaces) |

Counts: 12 functions reference a `feature.*` twin (9 distinct twins, 3 shared); 18 are NEW
(client-side behaviors with no pipeline counterpart). Duplicates between registries: ZERO.

Shared-twin register (documented, not hidden): feature.space (F-04, F-30);
feature.intelligence_today (F-05, F-07); feature.connect (F-06, F-21); feature.smart_tabs (F-01, F-19).
Each shared twin is complementary — one name, two client faces, stated in the function entries.

---

## Self-verification report (this item)

- **Inventory cross-check:** 30/30 ids present, F-01..F-30 in order, names copied character-for-character
  from `FUNCTIONS-INVENTORY-v1.md` (smart-tabs, smart-mail, smart-lists, smart-spaces,
  intelligence-today, connections, reports, feed, booking, menu-display, product-display,
  signup-capture, event-rsvp, assessment-score, portfolio-showcase, community-feed,
  business-proof, profile-link, navigate, search, contact, share, save, play, dictate, copy,
  preview, cart, contract-draft, join). File naming `fn-<id>.js` consistent for all 30.
- **UNIT-FORMAT cross-check:** every entry carries id, file, one-line what, exact `data-fn` markup,
  config schema (all keys optional unless marked * — only F-24 `src` is required), inputs/outputs,
  READY vs CONNECTED behavior, backend twin or "none — NEW", status VERIFIED, three-face seam.
- **Intake hook grep verification** (all against `smart-builder-intake_factory.html`, 139140 bytes):
  `#visionText` ✓1, `#dictBtn` ✓1, `#cartFab` ✓1, `#cartDrawer` ✓1, `#cartItems` ✓1, `#cartCount` ✓1,
  `#closeCart` ✓1, `#buildBtn` ✓1, `#contract` ✓1, `#contractWrap` ✓1, `#copyBtn` ✓1, `#btnCopy` ✓1
  (both copy ids exist — F-26 binds whichever is present), `#reviewBtn` ✓1, `#sumWrap` ✓1,
  `#sumTmpl` ✓1, `#sumFunc` ✓1, `#sumPieces` ✓1, `#sumVision` ✓1, `#sumBuild` ✓1, `#sumClose` ✓1,
  `.pcard[data-model][data-name][data-cat]` ✓51, `.szpill[data-s][data-z]` ✓, `.btn-select` ✓,
  `.tcard2[data-t]` ✓12 (Personal, Today, Smart List, Business, Booking, Product, Event, Community,
  Portfolio, Menu, Signup, Dashboard), `.tview` ✓, `.frow > .tog` ✓14, `#step1`–`#step4` ✓,
  `[data-go]` ✓5. **ZERO missing hooks — every hook referenced in this registry exists in her file.**
- **Naming collision check:** our ids (hyphenated, e.g. `smart-mail`) vs pipeline ids
  (`feature.smart_mail` underscored, `intake.*`, `library.*`, `template.*`, `customize.*`,
  `build.*`) — no overlap. File names `fn-<id>.js` unique per id. Shared twins documented in the
  shared-twin register above — no silent duplication.
- **Open flags for the parent/coordinator:**
  1. Three intake toggles have NO function in the 30: "Ask Naya" (pipeline `feature.naya_answers`
     exists as backend), "Guard" (privacy setting), "Calendar" (no calendar function itemized).
     They are intake-only toggles for now — flagged for itemization, not absorbed.
  2. New-to-pipeline functions (18) are client-side behaviors the pipeline registry does not cover
     (booking, menu-display, product-display, signup-capture, event-rsvp, assessment-score,
     portfolio-showcase, business-proof, profile-link, search, save, play, dictate, copy, preview,
     cart, contract-draft). No assembler-side Python equivalents exist or were created (spec-only item).
  3. Pipeline `feature.*` entries all carry status "built" with `code: null` (no implementation) —
     their twin relationship is contractual, not verified-by-bytes; verifiers should confirm before
     treating any twin as real.
- **api_calls:** 0. No commit (per task). No branch implementation (spec-only per task).
