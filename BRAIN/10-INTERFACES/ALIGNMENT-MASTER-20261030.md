# THE ALIGNMENT MASTER — NayaNET's 25 pages: URLs, bullseyes, the design contract, and the Smart Bar
Shawn's order, 2026-10-30. One document: every page listed with its URL, every page's bullseye (ultimate function, purpose, what it does, how it connects), the design contract the whole system follows, the Naya button standard, and the official Smart Bar spec. After this: each page gets updated to align — the fix type per page is named at the end.

**Rulings 2026-10-30 (Shawn, his review of /pi):** (1) Smart Search is NOT a separate app — it is a universal capability on every app (search the whole network from anywhere; quick tabs + search on all apps). The 26th slot is retired; the list is 25. (2) The Hub keeps its bars exactly as they are — the reference implementation, never redesigned; every app page carries the top + bottom Smart Bar, added where missing. (3) What he found missing in PI — the per-app bullseyes, the design-contract link, the Smart Bar link — gets INPUTTED into PI, and this document is linked from each app's page.

Status: TARGET DEFINITIONS + honest current state. Nothing here claims a page is complete. A bullseye is hit only on proof: a cold walk, phone first, different seat scoring 9+, no disqualifier.

Sources (never replaced, only built on): the 26 bullseye definitions (`bullseye-definitions-20261028.md`), the 26 alignment assessments + rollup (2026-10-29), the Naya Design Contract v1.1 (CANONICAL, ratified 2026-10-03) + Master Design Contract + `~/workspace/team-nitro/DESIGN-LANGUAGE.md` (the read-before-design trio), and the settled Smart Bar standard (DESIGN-LANGUAGE §2.2 + Shawn's 2026-10-30 refinement).

---

## 1. THE INVENTORY — all 25 pages with their URLs

| # | App | URL | Honest state today |
|---|-----|-----|-------------------|
| 1 | Home | nayanet.live/ | Live door; two hub services fighting over it (blocker named); 9.0 rework unlanded, needs Shawn's tap |
| 2 | Dashboard | nayanet.live/dashboard | Live model worker; true numbers unproven; own-route decision owed |
| 3 | Personal app | nayanet.live/personal | LIVE flagship (demo persona); the design-language source; per-section edits unverified |
| 4 | Business app | nayanet.live/business | Model worker; missing as its own finished surface |
| 5 | Space app | nayanet.live/space | Model worker; directory click doesn't open the real app yet |
| 6 | Intel Today | nayanet.live/rooms/today | Serves its own page; merge end-state (one ultimate Today) unresolved |
| 7 | Growth | nayanet.live/rooms/growth | Serves its own page; live defect: Personal-fragment smart links show "connection unavailable" |
| 8 | About | nayanet.live/about | TRAP — serves Hub home bytes today; the real About lives as a section inside Personal; redirect owed |
| 9 | Connections | nayanet.live/rooms/connections | Serves its own page; central claim broken on both doors; privacy repair FIRST |
| 10 | Smart Mail | nayanet.live/rooms/mail | Serves its own page; PRIVACY UNPROVEN — anon-readable invite log (P0); RLS repair queued; two-owner proof owed |
| 11 | Smart Lists | nayanet.live/lists | TRAP — serves Hub home bytes; pilot BUILT (my rendered review: 9.0, entry bar met); landing gated on Power's scorecard |
| 12 | Reports | nayanet.live/rooms/reports | Serves its own page; stats-as-button merge unbuilt |
| 13 | Settings | nayanet.live/settings | TRAP — serves Hub home bytes; the one Settings page unbuilt |
| 14 | Library | nayanet.live/rooms/library | Serves its own page as the archive; guide-first rebuild unbuilt |
| 15 | Project Intelligence | nayanet.live/pi | LIVE — the face serving; whole-face 10/10 + live chain still owed |
| 16 | Projects | nayanet.live/projects | Serves its own page; world view unbuilt; wears Smart Growth brand (correction owed) |
| 17 | Welcome | nayanet.live/welcome (+ /world/*) | LIVE door; most aligned page; birth chain (walk → finished pages) unproven end to end |
| 18 | Smart Notes | nayanet.live/s/&lt;id&gt; | Per-note pipeline proven live (SN-1905 at /s/sn1905); the One Flow (note → live feed card) unproven end to end |
| 19 | Smart Factory | nayanet.live/smartfactory | Now serves a real page (was a trap); engine still siloed on one box; curated repo move owed |
| 20 | Certificate / Identity | section inside Personal Settings (nayanet.live/personal) | Live as a section; remainder is Shawn's to name ("pretty much done, almost 100%") |
| 21 | Pricing | nayanet.live/pricing | TRAP — serves Hub home bytes; full-fidelity preview exists; settled pricing NOT live yet |
| 22 | Ask Naya | Hub Ask surface (nayanet.live) | In-app surface; voice daemon dies every tick (root cause diagnosed, fix briefed); ear gate open |
| 23 | Smart Match | system — no page (engine) | Engine built, lane-proven 9.5; production switch-on awaits Shawn's serving-chain ruling |
| 24 | Booking | nayanet.live/book | LIVE route (200) — the only verified live app route; persistence unproven; cold proofs owed |
| 25 | Smart Meet | no surface yet — to build | Decided, not built; C1 SETTLED (free = no audio/video; video paid up to 6; audio paid up to 10) |

**Smart Search is not row 26 — it is a universal capability** (Shawn's ruling 2026-10-30): search-the-network lives on EVERY app — quick tabs + search in every top bar, one search over the whole network. Spec'd in §6.26 below as a capability, not an app.

**The 27th:** 25 are settled. The live 27th question is **Messenger** — own app or inside Smart Mail — UNDECIDED, Shawn's call. (Ledger, Feed, Connect, Thank-you are system parts whose PI cards are owed; they are not separate apps.)

**Trap routes to cure (4):** /lists (pilot built, landing gated) · /settings · /pricing · /about (redirect). **To build:** Smart Meet surface · Smart Search face entry · Business/Space finished surfaces.

---

## 2. THE DESIGN CONTRACT — the law every page follows

This is the whole system in one breath, then the checkable rules. No page ships off-language. Ever.

**In one breath:** glossy obsidian black, lit from within. White light at rest; on touch, each thing ignites in its OWN spectrum color — edge only, text stays white. Everything is elevated, nothing is flat. Circles carry people and numbers; horizontal rectangles carry content. The spectrum walks purple → blue → green → gold → orange → red → magenta and never repeats a color twice in a row. One chrome, one navigation, one button DNA, on every page.

**The checkable laws:**

1. **Field:** near-black layered gradient ground (`#0B0D12` family; rooms as dark as `#020204`). No flat panel, no light surface anywhere. Every surface has a gradient and a finish — "glossy obsidian black, like a glossy city at night."
2. **Full width:** no max-width cage; content owns the width edge to edge. On mobile the page IS the full screen.
3. **Shapes:** content in horizontal 16:9 rectangles, stacked. Circles ONLY for avatars, orbs, icons, data-circles. Never squares, never vertical rectangles for content.
4. **No voids:** no empty spacing, no min-height deserts. If a region has nothing to say, it does not exist.
5. **Spectrum walk:** purple `#a06bff` → blue `#3fb8ff` → green `#2fe89e` → gold `#ffbf3d` → orange `#ff9a5a` → red `#ff5e6c` → magenta `#e84fff` → back to purple. Each section gets the NEXT color. Never the same color twice in a row. Color = position = identity: you know where you are by the color.
6. **White at rest, ignite on touch — EDGE ONLY:** every clickable edge shows a visible white rim (1.5–2px) at rest. On hover/touch, the BORDER and GLOW ignite in the element's OWN spectrum color. **The text never highlights — it stays white.** Text highlighting looks cheap.
7. **Elevation everywhere:** every element carries inset top light + inset bottom shade + outer glow + drop shadow. Boards within boards each raised — tiles sit ON their board, not in it. Nothing is flat.
8. **Twin pluses:** two identical 48px round buttons, extreme top corners, on EVERY page. Left opens the Nayanet Areas drawer; right opens the owner's ecosystem menu. Same size, same construction, same behavior everywhere.
9. **One button DNA** (§3 below). No flat buttons — flat is a defect, not a style.
10. **Inputs are wells, actions are buttons:** inputs recessed and dark inside with white text; actions raised; displays are lit panels. Never confused.
11. **Type:** headlines in a warm serif (Newsreader/Georgia); UI in Inter. Body 16px floor. White/silver text — NEVER gray body text.
12. **Orbs carry people and numbers:** every initial is a flowing orb (light sweep forever); stat circles lit, breathing, labeled.
13. **Living data:** every stat has shape + direction + a human sentence. A number in a black box is not a report.
14. **Timestamps alive:** date GREEN `#2fe89e`, time GOLD `#ffbf3d`, relative label recomputing — everywhere.
15. **Motion with meaning:** drift, breathing, ignition on the token clock (fast .18s / med .28s / slow .5s). Light moves first, words follow. And motion ALWAYS has an off switch (Calm setting + reduced-motion).
16. **No dead buttons, no fake liveness:** everything clickable does something real or it is removed. Device-local data labeled local. Empty states honest ("Nothing here yet" beats fake content).
17. **Voice-first:** dictation on every text entry; playback on every content block; text areas grow as you write.
18. **Nothing is a mystery:** every feature explained in plain words where it stands, with a tappable ⓘ for the fuller note.
19. **Harvest-first, never invent:** every component traces to a named existing part (Hub chrome, factory piece, os-*/ph-* grammar). Recreating a part that exists is a defect.
20. **Edit-only for existing pages:** fill, wire, polish, fix — never replace, never restyle. A redesign happens only when Shawn orders one in those words.
21. **Smart apps, not pages:** user-facing words are *app / smart app* — never *page* or *website*.
22. **Diamonds are the signature geometry:** bullets are jewels, not dots. The Welcome door keeps its 108 precision jewels, exactly.

---

## 3. OUR NAYA BUTTONS — the elite standard

This is what NayaNET is known for. Not good buttons. The most elite, highest-level, most high-tech, incredibly beautiful, awesome-to-use buttons anybody has ever touched. When someone touches a Naya button, they feel the difference — the light, the lift, the instant answer. Here is exactly what they are.

### 3.1 The anatomy — what a Naya button IS

- **Center:** really black (`#050505`). Not gray, not dark blue — black. The black makes the light mean something.
- **Text:** always white, always with an icon. The icon is never decoration — it says what the button does before the words do.
- **Rim:** a visible white border at rest, 1.5–2px, bright enough to SEE. This is the white light the whole system rests in.
- **Shape:** pill (999px radius) for actions; perfect circle for the chrome (the twin pluses, 48px) and icon buttons. Rectangles with 14–16px radius for tiles and rows.
- **Size:** minimum 44px touch target — a thumb never misses. Principal calls to action are 52px and up — the button you can't not see.
- **Depth:** the full elevation stack, always — inset top light (light catching the top edge), inset bottom shade, outer glow, drop shadow. A Naya button is a physical object made of light. Nothing about it is flat.

### 3.2 The states — a button is alive in every state

- **REST:** white light. Dark glass face (lighter crown, darker base), thin bright rim, white bold text. Quiet, confident, waiting.
- **HOVER / TOUCH:** the button ignites in its OWN spectrum color — the rim takes the color, a TWO-LAYER outer glow (tight + wide), a text-shadow kiss (glow AROUND the white letters — the letters themselves never change color), and the button LIFTS (`translateY(-2px)`). Chrome buttons ignite purple; themed buttons ignite their own color. The face stays dark. Color lives only in the light — never in the face, never in the text. (This is the trillion-dollar rule: the PI face once turned its pill text the button's color, and it looked cheap. Never again.)
- **PRESS:** the button answers instantly — `translateY(2px)`, the press you feel. Light moves first, words follow: the state changes animate BEFORE any text updates.
- **ACTIVE / SELECTED:** white-hot, never colored. A bright white rim and a soft white glow — color comes on hover, not on selection.
- **FOCUS:** keyboard focus is a first-class state, not an afterthought — visible, lit, unmistakable.
- **DISABLED:** honest — dimmed, no glow, no lift, and it says why (or it isn't there at all; a dead button is removed, never displayed dead).
- **LOADING:** the button breathes while it works — it never goes silent and never lies about being done.

### 3.3 The feel — why they feel different

- **Timing:** fast `.18s`, medium `.28s`, slow `.5s`, on one ease curve (`cubic-bezier(.16,.84,.22,1)`) across the whole system. Every button moves on the same clock — the system feels like one instrument.
- **The lift ladder:** buttons lift 2px, boards 5px, cards 6px, orbs 8px with a slight scale. Bigger things rise higher. The physics is consistent everywhere, so your hand learns it once.
- **The answer:** every tap gets an instant visible answer — the press, the glow, the change. A button that doesn't answer is broken, full stop.

### 3.4 The family — one DNA, job variants

- **Primary (NAYA-BTN-009):** the purple pill. `border:2px solid #a06bff`, glow `0 0 24px -4px #a06bff` at rest deepening to `0 0 36px -2px` on hover. The "do the thing" button.
- **Secondary:** same construction, white rim at rest — ignites in its own color on hover. The "also do this" button.
- **Semantic pills:** fixed meaning colors, learned once, true everywhere — LOVE red `#ff5e6c` · LIKE blue `#55b9ee` · FAVORITE gold `#ffd45a` · SAVE blue `#55b9ee` · CREATE SPACE purple `#9d75ff` · SHARE purple `#9d75ff`. White light idle, color on hover.
- **Small action chips:** the same DNA in miniature — pill, inset lip, drop shadow. An "on" state lights its edge and text-shadow in its own color but never floods.
- **The twin pluses:** the chrome — 48px round, glossy black, thin light rim, white + glyph. Left opens the Nayanet Areas drawer; right opens the owner's menu. Identical on every page.
- **Smart Tab pills:** the navigation buttons (§5) — same DNA, jewel icon per tab, spectrum color by position.
- **Switches:** real lit switches — recessed track, domed knob; ON takes the row's jewel color in rim, glow, and knob.
- **Icon jewels:** every icon sits in a raised, lit tile — radial dome light, 1.5px rim in its own color, glow, lit glyph. Never a bare glyph. Unique per destination, legible at a glance.

### 3.5 The promise

A Naya button is never flat, never dead, never silent, never confusing. It rests in white light, ignites in its own color, lifts when touched, answers when pressed, and tells the truth about what it does. That is the standard on all 26 pages — and it is what the Smart Bar carries across the whole network.

---

## 4. BOARDS, ICONS, ELEMENTS — the component language

- **Boards** (`.ph-card`): the unit of composition. `background:linear-gradient(180deg,#14141c,#0a0a10); border:2px solid rgba(255,255,255,.16); border-radius:20px; padding:28px.` Every board is ALIVE — hover/touch lifts it and ignites its edge in its own spectrum color. A board with no hover state does not ship.
- **Icons:** every icon in a raised lit jewel tile (own-color rim + glow), unique per destination, legible at a glance. Sizes: 23px / 27px nav / 28px header / 36px / 46px.
- **Orbs:** initials are flowing orbs — domed jewel disc, light sweep flowing around the initial forever, rotating hot arc for active people. Stat circles lit, breathing, labeled. Circles carry people and numbers; nothing else is a circle.
- **Wells vs buttons vs panels:** inputs are wells (recessed, dark inside, white text); actions are buttons (raised); displays are lit panels. Never confused.
- **Data:** every stat has shape + direction + a human sentence. Donuts are beveled jewels; week bars are lit objects that grow and breathe; funnels are flowing slabs with honest stages only (Recorded → Joined — "Opened" is unobservable and forbidden).
- **Feed cards:** newest-first, categorized by TOPIC never by kind. Every Smart Note card carries the live stamp: date green, time gold, relative label recomputing.
- **People rows:** full-width horizontal rows — orb left, name/fact stacked, action right. Never a mini-box grid.

---

## 5. THE SMART BAR — the official navigation of the whole network

One network, many apps: the SAME tab bar on every page, never reinvented per page. This is the connection piece — the thing people notice, the thing that sets NayaNET apart. It runs on every single page, top and bottom, and it is extraordinary.

### 5.1 The shape (both bars)

A rounded pill bar, dark glass face, thin light border at rest, white bold labels, a jewel icon per tab. The row never wraps — it scrolls, scrollbar hidden. Tabs take their spectrum color BY POSITION (purple → blue → green → gold → orange → red → magenta). The trillion-dollar rule binds every tab: **text stays white, always** — what ignites is the rim, the two-layer glow, and the text-shadow kiss, all in the tab's own color. Active tab: white-hot, never colored.

### 5.2 TOP BAR — the current app

- **What it is:** the app's FUNCTIONS — the navigation and buttons belonging to THIS app only.
- **Motion:** drifts slowly RIGHT, mirrored with the bottom bar. Gentle, one-way; pauses while a hand is on it.
- **Editable:** NO. No edit menu, no add. It is the app's own quick access — the same look as the bottom bar, but every tab is a door into this app's features: what each button does and what each feature is, one tap away.
- **Never closable.**

### 5.3 BOTTOM BAR — the whole network

- **What it is:** the WHOLE APP navigation — the ecosystem. Your world of apps, one tap away. Any URL entered into the system becomes a Smart Tab here immediately.
- **Motion:** drifts slowly LEFT, mirrored with the top bar.
- **Editable — by law:** the ⋯ menu on each tab offers **Edit / Set Purple Heart / Set Gold Star / Remove**, and a **＋ Add** pill rides at the end. Hearts sort first, then stars. This is YOUR network in YOUR order — star what you love, heart what is home, remove what isn't yours, add what is.
- **Never closable.** A tab with no destination says so — never a dead link.

### 5.4 The Hub rule (Shawn, 2026-10-30)

The Hub keeps its bars exactly as they are — top and bottom, the reference implementation the whole system harvests from. We do not redesign it, re-bar it, or move its bars. Every app page carries the top + bottom Smart Bar per §5.2/5.3, added where missing, in the same style, same buttons, same look — the whole system speaks the same language. (If the Hub's bar wants to scroll in place auto-organizing categories or sit at the top, that is a Hub-design decision for its own pass — not this program.)

### 5.5 Why it's the differentiator

No other network has this: two living bars, breathing in opposite directions, in the button language above — the top bar knowing exactly which app you're in and handing you its powers, the bottom bar carrying your whole world, arranged by your own hand with hearts and stars. It is on every page. It is the first thing that moves and the last thing you forget. That is what "extraordinary" means here.

**Companion chrome:** the twin pluses stay in the extreme top corners (left: Nayanet Areas drawer; right: owner's menu). One home per action — if a destination lives in the tab bar, it does not also get a button row (no duplicated navigation, ever).

---

## 6. THE BULLSEYE FOR EACH OF THE 25 (plus Smart Search as a universal capability)

For every app: its URL, its bullseye moment (imagine it finished), its ultimate function (what ONLY it does), what it does, how it connects — and the alignment fix owed (from the 2026-10-29 assessments: EDIT 20 · BUILD FRESH 2 · REDO 2 · REPLACE 1). Proof is the same for all: cold walk, phone first, different seat 9+, no disqualifier.

### 1. Home — nayanet.live/
- **Bullseye moment:** a visitor lands and in seconds knows what NayaNET is, where to start, and what is in it for them — and a citizen lands and is home.
- **Ultimate function:** the front door and the first impression. Nothing else is the door.
- **Does / connects:** door → Start walk, Connect, pricing, the citizen's personal home, Hub feed, Booking.
- **Fix:** EDIT — land the scored 9.0 rework through the single put-live path (needs Shawn's tap); resolve the two-hub-services fight; then the cold walk.

### 2. Dashboard — nayanet.live/dashboard
- **Bullseye moment:** one place where a citizen sees their whole life in the system — what is happening, what needs them, what is next — and acts on it without hunting.
- **Ultimate function:** the citizen's command view. It SHOWS; it never duplicates the apps it summarizes.
- **Does / connects:** the view inside the citizen's world app; Personal, Business, Space, Mail, Today, Growth, Reports, payouts surface (next Wednesday + status).
- **Fix:** EDIT — settle the own-route decision; wire every number to its true source (counts drill to their jobs).

### 3. Personal app — nayanet.live/personal
- **Bullseye moment:** "this is me" — who I am, what I'm into, my vision, mission, motto, goal, business, space — all born in the walk, all editable forever, one living page.
- **Ultimate function:** the citizen's own home and identity. No other app is the person.
- **Does / connects:** the format source the whole family harvests; hosts the Dashboard view, Today, Notes, Connections (bidirectional SHARE), Smart Mail inbox, Smart Lists, Growth invites, Reports stats.
- **Fix:** EDIT — complete the live page, never rebuild it (it IS the design-language source); per-section edit controls verified; Business/Space tabs completed.

### 4. Business app — nayanet.live/business
- **Bullseye moment:** a citizen's work has its own workspace — what they do, what they offer, what they're building and its goal — ready to meet customers and collaborators.
- **Ultimate function:** the business, kept distinct from the personal. Never merged into personal.
- **Does / connects:** own workspace; Personal (format source), Space (sibling), Booking, Meet, Mail, Growth.
- **Fix:** BUILD FRESH — assemble from the flagship chassis, never a new design; it is missing as its own finished surface today.

### 5. Space app — nayanet.live/space
- **Bullseye moment:** pick a topic and the space around it is there — the people, the conversation, the shared work, the room to gather.
- **Ultimate function:** space = the citizen's topic choice, made into a world. The personal view becomes the space view for the chosen topic.
- **Does / connects:** Personal (format source), Business (sibling), Connections, Mail, Match, Lists.
- **Fix:** EDIT — fix the directory click to open a real Space page from the flagship chassis; the space itself live and joinable, with per-page private-or-public choice.

### 6. Intel Today — nayanet.live/rooms/today
- **Bullseye moment:** "what matters today" — one ultimate view of today and its stats. No second stats page anywhere.
- **Ultimate function:** today + stats, ONE ultimate. A button on the main page, never two.
- **Does / connects:** the day's entry point — Personal, Dashboard, Reports drill-through, Day Journal (look back).
- **Fix:** EDIT — the canonical merge decision (one ultimate Today), different-seat rendered review, the one-stats law held on every surface showing a number.

### 7. Growth — nayanet.live/rooms/growth
- **Bullseye moment:** a citizen sees themselves growing — connections, spaces, reach, what is working — and knows the next step that grows it.
- **Ultimate function:** growth, measured honestly from real activity. Never invented clicks.
- **Does / connects:** the invite→join loop — Personal, Connections, Reports, membership/affiliate boundary, Smart Link.
- **Fix:** EDIT — fix the live defect (Personal-fragment smart links "connection unavailable") in place; retire the personal form into the serving master; honest empties only.

### 8. About — nayanet.live/about (redirect owed; the real About lives in Personal)
- **Bullseye moment:** anyone meeting a citizen reads, in order, who they are and what they stand for — and can ask, and get an answer that saves.
- **Ultimate function:** the citizen's story, in the locked order: motto → story → goals → mission → vision → loves → don'ts → facts → Q&A LAST. Personal pages say "my"; business/community pages say "our".
- **Does / connects:** the identity layer — Personal/Business/Space apps, Connections, Welcome.
- **Fix:** EDIT — enforce the locked order + shared-save in the existing Personal section; /about redirects (it is a trap today).

### 9. Connections — nayanet.live/rooms/connections
- **Bullseye moment:** one system, shared records — the people you know, the people you should meet, and the path between them. No second copy of the truth.
- **Ultimate function:** connections + people, ONE ultimate page with stats. Never two.
- **Does / connects:** the relationship/identity spine — Personal, Space, Smart Match, Smart Mail, Growth, /hub/connect, Smart Lists, About.
- **Fix:** EDIT — privacy repair FIRST, then fix both doors in place; split the record area (people vs AI-connect).

### 10. Smart Mail — nayanet.live/rooms/mail
- **Bullseye moment:** every message that matters reaches the right person, privately, on time — mail, instant messages, and scheduled mail from ONE scheduler; dictated first, played back after.
- **Ultimate function:** the ultimate mail system. Privacy is its gating feature: mail is read only by its communicators. (Privacy hole VERIFIED CLOSED 2026-10-30: anon-key reads on the invite log return 401. Two-owner proof still owed before any private-for-citizens claim.)
- **Does / connects:** the communication/notification spine — Personal/Business/Space, Memberships, Booking (scheduled leg), Connections, Intel Today. Three send modes: mail · instant message · post to feed. Messenger = a send mode question (own app vs inside Mail — UNDECIDED).
- **Fix:** EDIT — two-owner privacy proof on the existing backend first, then overflow pass + bulk-delete proof; archived_at DDL.

### 11. Smart Lists — nayanet.live/lists
- **Bullseye moment:** anything worth keeping together is a list — people, spaces, notes, things to do — and the list works everywhere it appears.
- **Ultimate function:** lists as a living, linkable collection, not a copied pile. Deep-links to original records.
- **Does / connects:** the organizing layer — Personal, Space, Messenger, Notes, Match; almost every app can be listed.
- **Fix:** REPLACE — the pilot is BUILT (my rendered review 2026-10-30: 0px overflow, 0 errors, 9.0 entry bar); landing gated on Power's different-seat scorecard → land → live check.

### 12. Reports — nayanet.live/rooms/reports
- **Bullseye moment:** one reports home — what happened, what it means, what is next — daily/weekly/monthly as the plan allows, with stats as a button INSIDE Reports. Never a second stats home.
- **Ultimate function:** reports + the stats button. The rooms library stays whole; stats never splits off.
- **Does / connects:** Personal (stats source), Today, Growth, Dashboard.
- **Fix:** EDIT — add the Stats button to the live /rooms/reports surface, harvesting the Personal section's flow verbatim.

### 13. Settings — nayanet.live/settings
- **Bullseye moment:** every switch a citizen needs, in one page, each saying plainly what it does — and no switch that does nothing.
- **Ultimate function:** ONE settings page. Only toggles that make sense.
- **Does / connects:** every app's toggles; Identity/Certificate; the Smart Bar; install-as-app lives here on every page.
- **Fix:** REDO — compose the one Settings page from harvested parts (Personal section + dashboard toggles); /settings is a trap today.

---

### 14. Library — nayanet.live/rooms/library
- **Bullseye moment:** everything worth keeping is findable again — the archive that guides first, then shows.
- **Ultimate function:** the archive. Guide-first, never a dump.
- **Does / connects:** every NayaPOWER area via guide entries; Smart Notes; Personal, Reports, Notes, Spaces.
- **Fix:** EDIT — restructure the live /rooms/library into the ruled guide shape, harvesting entry text from PI.

### 15. Project Intelligence — nayanet.live/pi
- **Bullseye moment:** one live place where every project, list, link, and note is seen and current — the work's mind, not a dashboard about the work — and a builder opens it and knows exactly what is done, what is next, and who owns it.
- **Ultimate function:** the single place for everything that matters — work AND the governing intelligence behind it (constitution, oath, design contract, brand), organized where the work lives.
- **Does / connects:** every card, every lane, the face, the Day Journal, the governing section.
- **Fix:** EDIT — the face is built and serving; finish the live chain in order (face-level different-login scorecard → consensus → 10/10 with no revert → Shawn's tap → live check + note-survival test). Never rebuild the face.

### 16. Projects — nayanet.live/projects
- **Bullseye moment:** a citizen's own workspaces, each with its own work, visible and moving — distinct from the record system that tracks them.
- **Ultimate function:** the own-workspace view. Projects (view) is never PI (record).
- **Does / connects:** PI record (one canonical record), Personal/Business/Space, Spaces.
- **Fix:** REDO — build the ruled world-view + project-view surface, harvesting existing workspace parts; correct the Smart Growth branding; per-seat to-do lists (every seat its own list, all seats seeing the shared shape).

### 17. Welcome — nayanet.live/welcome (+ /world/*)
- **Bullseye moment:** a stranger becomes a citizen in minutes — ten plain questions, one beautiful page each, and pages ready at the end, editable forever after.
- **Ultimate function:** the walk. Ten locked questions (who you are · what you're into and why · vision · mission · motto · personal goal · what you do · what you offer · what you're building and its goal · what kind of space you want and who you want to meet). Page 3 title locked: "Tell me who you are, in your own words."
- **Does / connects:** the ROOT — every citizen's pages are born here; Personal (birth), Connect, Onboarding, identity page; Smart Match rides the walk answers.
- **Fix:** EDIT — proof-first: the birth chain end to end (walk → finished, cleanly rendering pages with matches and a Smart Link, no hand-building between). New pages take a flagship page whole and swap only the middle.

### 18. Smart Notes — nayanet.live/s/&lt;id&gt; (+ Smart Feed)
- **Bullseye moment:** "smart note this" lands a Smart Note card on the Smart Feed in seconds — live data, beautiful format, with play, save, and share. Goal #1 — the experience everything else serves.
- **Ultimate function:** the note door and the feed card. Smart Notes are not Naya Notes — never merged in words.
- **Does / connects:** the shared MEMORY of the tree — every lane files in; Feed, Personal, Project Intelligence read back. The door chain: file with `## ` headers → one PUT → sync → author clicks the live /s/ link before anyone receives it.
- **Fix:** EDIT — wire the feed at its logical address; cold-prove the One Flow end to end, live ("smart note this" → live card).

### 19. Smart Factory — nayanet.live/smartfactory
- **Bullseye moment:** any Naya can build any page at any time — from the proven pieces, in the system's language, without waiting on one box or one seat.
- **Ultimate function:** the parts warehouse + generator. 566 earned pieces (542 interface + 24 functional) — the registry is the law; Power verified it.
- **Does / connects:** the ROOTS / tools shed — every interface harvests through it; GitHub (interfaces available there); every page; the design contract.
- **Fix:** EDIT — the curated move: exact files → repo paths shown to Shawn BEFORE the first push, interface-core only, one non-Nitro cold build as proof; then the factory builds from the repo. (Now serves a real page — the old trap entry is retired.)

### 20. Certificate / Identity — section inside Personal Settings (nayanet.live/personal)
- **Bullseye moment:** a citizen's identity is proved, portable, and theirs — one Smart Link, one identity, everywhere needed, and nothing about them leaks where it should not.
- **Ultimate function:** identity + certificate. The Smart Link is the citizen's own to claim; an unaided claim is the acceptance test.
- **Does / connects:** the DOOR KEY — one alias, one route, forever; everything hangs off identity. Personal Settings (live home), Connect, Onboarding, Smart Link routing.
- **Fix:** EDIT — Shawn names the remainder ("pretty much done, almost 100%" — his words, his to complete), then cold-prove certificate-at-join (rides the Welcome birth-chain proof). The certificate keeps its own language: black dominant, royal-purple accents, silver the family metal — never "fixed" into the walk.

### 21. Pricing — nayanet.live/pricing
- **Bullseye moment:** a visitor understands in one look what is free, what is paid, and why paying is gladly worth it — and pays without a maze.
- **Ultimate function:** the price and the promise. Gate = TIME (9-day free trial, no card, DEFAULTS TO MAX — full power on loan), not a maze of per-feature locks.
- **The settled pricing (SN-1905, the canon):** NayaNET $25/mo · $50/3mo · $150/yr · $300 lifetime (first 1,000 members, then closed forever). Naya Pro $50/mo · $300/yr (annual = half price). NayaNET Max $100/mo · $600/yr. NO REFUNDS — the trial is the guarantee. Referral/affiliate: 50% of revenue, everyone an affiliate by default. Payouts: "if we get paid, they get paid" — every second Wednesday, no holdback. Events: $150 per 1,000 LIVE heads per event (whatever the cost is, double it); affiliates earn on everything EXCEPT events. Plan switching: upgrades immediate with prorated difference; downgrades next cycle; no penalties.
- **Does / connects:** the GATE at the door — the whole tree's economy flows through it. Start page, Connect, Onboarding, Thank-you, ambassador dashboard.
- **Fix:** EDIT — land the existing full-fidelity preview at /pricing through the serving chain (trap today); then the money gates in order (checkout test-mode until merchant keys land at live checkout only; ambassador path end to end).

### 22. Ask Naya — Hub Ask surface (nayanet.live)
- **Bullseye moment:** one Ask surface in the Hub — ask anything, get a true answer in plain words, hear it if you want. Never a second Ask page.
- **Ultimate function:** ONE Ask surface. The mouth and the ear: answers in plain words + Naya's voice back (stream-first).
- **Does / connects:** Hub, Feed, Personal, every app's help. Ask bank: 48 answers.
- **Fix:** EDIT — close the proof gates: the voice daemon root cause (diagnosed 2026-10-30: Cloudflare-edge 403 on the voice worker — fix briefed, his hand or the additive route), the Ask path heard end to end by his ear (SN-1868 sample passed; the path gate stays open).

### 23. Smart Match — system, no page (engine)
- **Bullseye moment:** the right people and the right spaces find each other automatically — matches that are real, explained, and acted on. Not a list nobody opens.
- **Ultimate function:** the ONE auto-match algorithm. Kind: SYSTEM, not a page.
- **Does / connects:** walk answers in → matched people/spaces out → Booking (introduces) → Meet (hosts). Connections, Spaces, Personal.
- **Fix:** EDIT — post-merge verification first, then the production switch-on (awaits Shawn's serving-chain ruling), then the owed acceptance fields. Engine 9.5 is a LANE score — never an app score.

### 24. Booking — nayanet.live/book
- **Bullseye moment:** two people agree a time, and the time holds — taken times shown clearly, the slot held while finishing, only open times bookable, the meeting place chosen from four kinds.
- **Ultimate function:** the scheduler's booking leg. Four place-types: Smart Meet video/audio (paid gate travels) · in person · the guest's own link (Zoom etc.) · face to face.
- **Does / connects:** the middle of the chain — Match introduces → Booking sets the time → Meet hosts it. The ONE scheduler linked from Personal, Business, Space, Mail, Posts. Double-booking refused twice (guard + unique index).
- **Fix:** EDIT — wire live data into /book IN PLACE, never replace it (the only verified live app route); link-creation path, named-link render, three cold proofs (appointment, scheduled post, scheduled mail); persistence proven.

### 25. Smart Meet — no surface yet (to build)
- **Bullseye moment:** people who matched and booked simply meet — video or audio, browser to browser, clear and steady. The call itself is never the headline.
- **Ultimate function:** mesh P2P browser-to-browser calls. A QUIET capability — not what NayaNET is known for. **C1 SETTLED: free tier = NO audio, NO video; video = paid members only, up to 6 (layouts 2/3/4/6); audio = paid only, up to 10; over caps = monthly add-on.**
- **Does / connects:** the last link of the chain — Booking opens the call, the paid gate travels, the call is never mail. Smart Mail (scheduled meetings); Spaces (small-team private rooms, plan item).
- **Fix:** BUILD FRESH — the Meet surface, after the settled C1; screen share DECIDED (spec exists, not built); Naya-guided screen share DECLINED. Prove the surface, the paid gate travelling with it, and the limits held live under real calls.

### 26. SMART SEARCH — universal capability, NOT an app (Shawn's ruling 2026-10-30)

- **Bullseye moment:** on any app, type anything and the right thing in NayaNET answers first — the exact note, person, space, or page — and the click lands where it promised.
- **Ultimate function:** search-the-network, everywhere. Not a destination — a power every app carries.
- **Does / connects:** one search over the whole network's original records (notes + blocks first), exact-phrase tiers, /s/ deep links that resolve to the note not the feed root. Lives in every top Smart Bar (quick tabs + search) and as a search element on every app. Connects to: Feed, Notes, Connections, Library, every app's content.
- **Fix:** integrate the built ranker (measured 37/39 in lane) into the live chassis + refresh the corpus — then verify the same search box, same behavior, on every app. No separate app, no separate page, ever.

---

## 7. THE ALIGNMENT WORK — what "update each page" means

Now that the bullseyes are written and the contract is locked, each page gets brought to its bullseye — in the design contract, from harvested pieces, verified by the same-language check (§2). The fix type per page (from the 2026-10-29 assessments):

- **EDIT (20):** Home, Dashboard, Personal, Space, Intel Today, Growth, About, Connections, Smart Mail, Reports, Library, Project Intelligence, Welcome, Smart Notes, Smart Factory, Certificate/Identity, Pricing, Ask Naya, Smart Match, Booking. Fill, wire, polish, fix — the page that exists is the authority. Privacy gates first (Mail, Connections), then the traps (/pricing, /about redirect), then the chain proofs (Welcome birth chain → Booking persistence → Smart Notes One Flow).
- **BUILD FRESH (2):** Business app, Smart Meet. Assemble from the flagship chassis — never a new design. (Smart Meet after the settled C1, above.)
- **REDO (2):** Settings, Projects. Compose the one true page from harvested parts.
- **REPLACE (1):** Smart Lists — the pilot is BUILT and scored 9.0 (my rendered review, entry bar); landing rides Power's different-seat scorecard → land → live check. It is the proof this program works: one page, bullseye written, built harvest-only, reviewed rendered, verified different-seat, landed, live-checked.

**Every page, without exception, carries:** the twin pluses (§2.8) · the Smart Bar top + bottom (§5) · the button DNA (§3) · the spectrum walk (§2.5) · white-at-rest/edge-ignition (§2.6) · voice-first (§2.17) · the explanation standard (§2.18) · honest states (§2.16). A page missing any of these is not aligned — no exceptions, no "close enough."

**Proof, same for all (§6 head):** cold walk, phone first and laptop great, different seat 9+, no disqualifier. Self-scores are entry bars, never acceptance.

---

## 8. THE BUILD ORDER — grouped so connected apps sync together (Shawn, 2026-10-30)

One app after another, in this order. Connected apps ride together so they land in sync, talking to each other. The whole team builds — not one lane alone — every lane following this same document, the same Smart Bar, the same button DNA. No lane invents its own bars, its own buttons, its own look. Ever.

1. **ROOT:** Welcome → Personal → Certificate/Identity → About → Settings (birth → identity → story → switches)
2. **GRAPH:** Connections → Smart Match → Space app → Growth (people → match → gather → grow)
3. **WORDS:** Smart Mail → Smart Notes → Smart Lists → Library (messages → notes → lists → archive)
4. **WORK:** Dashboard → Intel Today → Reports → Projects → Project Intelligence (command → today → reports → workspaces → the record)
5. **MONEY:** Pricing → Business app → Booking → Smart Meet (gate → workspace → time → meet)
6. **DOORS:** Home → Ask Naya (door → voice)
7. **TOOLS:** Smart Factory (the shed that builds the rest, kept current as it goes)

**Smart Search** rides every group as the universal capability — the same search box, same behavior, on every app.

Per app, the pass is: how aligned is it → what does it need → what is its ultimate function (§6) → bring it up to date in the design contract (§2–§4) → Smart Bars top + bottom where missing (§5; Hub untouched per §5.4) → connections to the other apps wired → rendered review (phone + laptop, 0px, 0 errors) → self-score 9+ entry bar → different-seat scorecard → land → live check. Some take a while, some don't. The program does not stop below the bar.

*Written 2026-10-30 by Nitro, under the Read-Before-Design Gate (contract trio + DESIGN-LANGUAGE read first). Rulings applied same-day per Shawn's /pi review: Smart Search → universal capability (25 apps); Hub bars untouched. This document changes no page — it is the law the updates follow. Linked from every app's PI record; the per-app alignment program runs §8, one app at a time, Flow 2.*
