# Pre-made Functions Inventory v1 — "get them done done"
Director: Naya Nitro Narzan. 2026-10-18. Authority: Shawn Vibert ("we have to have pre-made functions… make it so this all is working").

## The rule
Every function below ships as: (1) a capability contract (what it does, inputs, outputs, status), (2) ONE pre-built working implementation (activatable by single declaration — never rebuilt per page), (3) a different-seat verification that it WORKS (real behavior, not staged). Status taxonomy: VERIFIED / IMPLEMENTED / MOCK / MISSING / BLOCKED. Failures get fixed in the function, never hand-patched on the page.

## A. Standard features — ON by default on every page (opt-out)
| # | Function | What it does |
|---|----------|--------------|
| F-01 | smart-tabs | Scrolling ribbon of favorite pages/apps/URLs; save once, reachable everywhere in NayaNET; editable |
| F-02 | smart-mail | Mail that works with the page — write, send, broadcast to everyone connected |
| F-03 | smart-lists | Organize anything — notes, contacts, topics, posts; cross-cutting, layers into every page |
| F-04 | smart-spaces | Gather people around anything — create/join spaces, view, join, support |
| F-05 | intelligence-today | Daily briefing — what matters today, surfaced for the owner |
| F-06 | connections | Your people, reachable — every relationship the page knows about |
| F-07 | reports | Daily, weekly, monthly pictures of what is happening |
| F-08 | feed | Posts, updates, activity — one living stream |

## B. Template functions — what each template needs to actually WORK
| # | Function | Powers | What it does |
|---|----------|--------|--------------|
| F-09 | booking | Smart booking app | Appointments handled — calendar, booking, confirmation |
| F-10 | menu-display | Smart menu app | Menu with real items and prices, order-ready |
| F-11 | product-display | Smart product app | Price, buy — sell one thing beautifully |
| F-12 | signup-capture | Smart sign up app | Join, subscribe — one page that converts |
| F-13 | event-rsvp | Smart event app | Invites, RSVP, day-of — all handled |
| F-14 | assessment-score | Smart dashboard app, Maxis | Questions → score → explained report (MAXESS pattern) |
| F-15 | portfolio-showcase | Smart profile/creator app | Show the work — proof of what you do |
| F-16 | community-feed | Smart community app | Feed, spaces, belonging — the people's home |
| F-17 | business-proof | Smart business app | Services, proof, contact — the page that sells |
| F-18 | profile-link | Personal smart app | My world in one page — about me, everything linked |

## C. Page plumbing — every page needs these to feel alive
| # | Function | What it does |
|---|----------|--------------|
| F-19 | navigate | Move between pages and rooms |
| F-20 | search | Find anything within the app |
| F-21 | contact | Reach the page owner |
| F-22 | share | Smart link — refer people in, share to the feed |
| F-23 | save | Keep things — favorites persist |
| F-24 | play | Audio playback (smart notes, powercasts) |
| F-25 | dictate | Speech-to-text input, fail-soft without it |
| F-26 | copy | Copy text/contract to clipboard |
| F-27 | preview | Open a real sample/template page |
| F-28 | cart | Select pieces, sizes, quantities, notes |
| F-29 | contract-draft | Vision + pieces + template → drafted build contract |
| F-30 | join | Join a space or community |

## Already proven in the wild (harvest, don't rebuild)
- dictate, copy, preview, cart, contract-draft, play-toggle: working inside ultimate-intake.html (Chi-verified 9.7/10)
- assessment-score: working inside Maxis_App_Design.html (MAXESS — questions, score bands, report)
- smart-tabs: spec + working mount in the design-standard showcase
- join: working "+ Join" buttons across the spaces/hub pages

## Build order
1. Capability contracts for all 30 (one file each or one registry — coordinator decides, no duplicates).
2. Working implementations — harvest the proven ones first, build the rest; each activatable by single declaration.
3. Different-seat verification per function: WORKS (real behavior) or it doesn't ship.
4. Wire into the assembler: page-contract declares functions ON → assembler wires pre-built units in.
