# 09 — SMART TABS

## 1. IN A NUTSHELL

Smart Tabs are the persistent quick-access navigation layer of the NayaNET intelligence system.

They sit above or near the top of the Intelligent Hub / Smart Feed and give a human one-tap access to the places, topics, projects, and intelligence they care about most.

A Smart Tab can point to:

1. **A real destination** — a URL or NayaNET page.
2. **A live intelligence view** — a topic, category, search, or set of keywords that retrieves relevant Smart Notes and intelligence from the existing system.

The central idea is simple:

**Smart Notes remember it. Smart Lists organize what I keep. Smart Tabs get me there now. Smart Feed shows me the intelligence.**

Smart Tabs are not another database, another copy of Smart Notes, or another silo of intelligence.

They are a living navigation layer over the intelligence that already exists.

As Smart Notes grow from dozens to hundreds to thousands, Smart Tabs solve the practical problem of organization and instant access without forcing the human to dig through the entire system.

The label is human-friendly.

The target is the machine instruction.

For example:

- **AI** → topic/query: AI
- **MONEY** → keywords: bitcoin, investing, revenue, business, income
- **MY PROJECT** → query: Naya Power, SmartNET, Intelligent Hub
- **Google** → URL: https://google.com

A Smart Tab is therefore a personal shortcut into the intelligence system — similar to a browser tab, but designed for a living intelligence network.

## 2. HUMAN

Smart Tabs answer a very human question:

**“Where do I want to go right now?”**

Imagine opening the Intelligent Hub and seeing a clean horizontal bar near the top:

**ALL  •  AI  •  PROJECTS  •  BUSINESS  •  LEARNING  •  IDEAS  •  NAYA POWER**

The bar can scroll horizontally when there are more tabs than fit on the screen.

The human can swipe or scroll it manually.

Tapping a tab immediately does what that tab was created to do.

### A tab can be a destination

A user might create:

**Google** → opens Google.

**Naya Power** → opens the Naya Power area.

**My Project** → opens a specific project page.

### A tab can be an intelligence lens

A user might create:

**AI** → shows AI-related intelligence.

**MONEY** → shows intelligence matching several money-related concepts.

**LEARNING** → shows learning-related Smart Notes.

**DECISIONS** → shows relevant decisions and decision intelligence.

The human does not need to manually classify every Smart Note just to make the tab useful. The tab can use the system's existing search, retrieval, topic, category, or keyword capabilities.

### Personalization

A user can:

- create a Smart Tab
- rename it
- edit its destination
- change its query/topic/keywords
- choose its scope where supported
- reorder it
- remove it
- mark it as a favorite or priority where supported
- create tabs for current projects or interests
- create tabs for places they visit repeatedly

The system should make this extremely easy.

The human should think:

**“I want this here.”**

not:

**“I need to understand how the database works.”**

## 3. CHILD

Imagine you have a giant magical clubhouse with thousands of rooms.

Your Smart Notes are everything inside the clubhouse.

A Smart Tab is a little sign at the top that says:

**TOYS**

**SPACE**

**MY PROJECT**

**GRANDMA**

When you tap the sign, the clubhouse takes you straight to the right rooms.

Some signs open one special room.

Other signs say:

**“Show me everything about space.”**

You don't build another clubhouse every time you make a sign.

The signs simply help you get around the clubhouse you already have.

That's a Smart Tab.

## 4. GRANDMA

Think of Smart Tabs like the tabs on the edge of a really good recipe binder or the labeled sections at the top of a well-organized website.

Instead of opening the whole binder and hunting through every page, you can tap:

**Recipes**

**Garden**

**Family**

**Christmas**

**Things To Do**

But Smart Tabs are smarter than ordinary labels because they can also say:

**“Show me everything related to this subject.”**

So one tab might take you to one particular page, while another tab gathers all the useful information about a topic.

And if you change your mind, you can rename the tab or change where it goes.

## 5. NAYA

Smart Tabs are one of the simplest-looking features in NayaNET, but they solve a major scaling problem.

As intelligence accumulates, the system becomes more valuable — and potentially more difficult to navigate.

My job is not to create more places for the human to manage.

My job is to make the existing intelligence easier to reach.

I should therefore treat Smart Tabs as **navigation intent**, not as new intelligence storage.

The core contract is:

`SMART TAB → INTENT / TARGET → EXISTING RETRIEVAL OR NAVIGATION → RESULT`

For a topic:

`SMART TAB → QUERY / TOPIC / KEYWORDS → SMART FEED RETRIEVAL → PERMISSION FILTER → RELEVANT INTELLIGENCE`

For a URL:

`SMART TAB → URL → NAVIGATE`

The human-friendly label and the machine target should be separate.

For example:

**MONEY**

can have a machine query such as:

`bitcoin, investing, revenue, business, income`

The human sees one beautiful word.

The retrieval engine receives the richer instruction.

I can help suggest useful tabs when the pattern is obvious:

> “You keep returning to these three project topics. Want a Smart Tab for them?”

But I must preserve the distinction between:

- human-created tabs
- Naya-suggested tabs
- system-defined tabs
- dynamically generated tabs

A suggestion is not automatically human intent.

I also must never use a Smart Tab as a way around privacy, authority, or visibility rules.

A tab can retrieve only what the current user is authorized to see.

A public-looking label does not make private intelligence public.

A popular topic does not become true merely because many people have a tab for it.

## 6. MACHINE

Smart Tabs are a persistent navigation/retrieval configuration layer over existing NayaNET destinations and intelligence retrieval primitives.

They should reuse the existing Feed/Search/Library/retrieval architecture wherever possible rather than creating a parallel classification database.

### Core Smart Tab object

A useful canonical representation is:

```json
{
  "id": "stable-id",
  "label": "AI",
  "type": "topic",
  "target": {
    "query": "AI",
    "topic": "AI",
    "keywords": ["artificial intelligence", "AI"]
  },
  "scope": "personal",
  "favorite": true,
  "priority": 1,
  "position": 1,
  "created_at": "...",
  "updated_at": "...",
  "created_by": "human"
}
```

For a URL:

```json
{
  "id": "stable-id",
  "label": "Google",
  "type": "url",
  "target": {
    "url": "https://google.com"
  },
  "position": 2,
  "created_at": "...",
  "updated_at": "...",
  "created_by": "human"
}
```

The exact schema can evolve with implementation, but the conceptual separation should remain:

**LABEL ≠ TARGET**

### Supported target types

Initial conceptual types:

- `url`
- `topic`
- `query`
- `category`
- `route`

The implementation may collapse some of these when the existing retrieval architecture makes that cleaner.

The goal is not to maximize object types.

The goal is to maximize useful navigation with minimum complexity.

### Topic / query tabs

A topic Smart Tab should resolve through the existing intelligence retrieval system.

Possible inputs include:

- one topic
- multiple keywords
- a saved search/query
- a system category
- a project identifier
- a relationship or scope
- a combination of retrieval criteria

Example:

`MY PROJECT → [Naya Power, Smart Tabs, Intelligent Hub]`

The retrieval engine determines which canonical Smart Notes or feed objects match.

Smart Tabs should not copy those objects.

### Scope

A tab may operate within a scope such as:

- personal
- collective
- activity
- supported project/workspace scope

The tab's scope must never override the object's actual privacy or authority.

The retrieval sequence should conceptually be:

`TAB TARGET → RETRIEVE → PERMISSION / AUTHORITY FILTER → PRESENT`

not:

`TAB TARGET → PRESENT → CHECK PERMISSIONS`

### Persistence

Smart Tabs are persistent user configuration.

They should survive normal navigation and return visits according to product/session rules.

A user should not need to rebuild their navigation every time they open the Intelligent Hub.

### Ordering

Useful controls include:

- drag/reorder
- priority
- favorite/pin
- default tab
- remove/archive

The implementation should support a stable explicit position rather than relying on incidental creation order.

### Horizontal behavior

The intended visual pattern is a horizontal, scrollable tab bar.

It may remain visible near the top of the Intelligent Hub while the user navigates the feed, subject to the actual page architecture.

If the tab bar auto-scrolls or gently cycles through available tabs, interaction must immediately give control to the human.

Auto-motion must never:

- steal focus
- unexpectedly change the selected tab
- interfere with clicking/tapping
- make text difficult to read
- create accessibility problems
- feel like an advertisement carousel

A good rule is:

**Motion introduces the choices. Human interaction owns the choices.**

### Editing

A Smart Tab editor should allow the human to change at least:

- label
- type where appropriate
- URL or target
- topic/query
- keywords
- scope where supported
- order/position
- favorite/priority state

The interface should validate URLs and target definitions sufficiently to prevent broken navigation or meaningless configurations.

### Retrieval contract

The most important implementation rule is reuse.

Before building new Smart Tab-specific search logic, the implementation should inspect and reuse the existing:

- Smart Note retrieval
- Smart Feed filtering
- search engine
- topic/category logic
- project relationships
- permission checks
- visibility rules

If an existing retrieval primitive can answer:

`query = “AI”`

then Smart Tabs should call that primitive rather than build a second AI indexing system.

### Relationship to Smart Lists

Smart Lists and Smart Tabs are intentionally different.

**Smart Lists = What I keep.**

**Smart Tabs = Get me there now.**

They should interoperate.

Example:

`AI SMART TAB → 137 MATCHING NOTES → SELECT 8 → ADD TO AI RESEARCH SMART LIST`

A Smart Tab can therefore be a fast discovery/retrieval lens, while a Smart List is the intentional collection created from selected intelligence.

### Relationship to Smart Feed

The Smart Feed is the presentation layer.

A Smart Tab can change the retrieval/filter state of the Feed without creating another Feed database.

Conceptually:

`SMART TAB → FEED QUERY STATE → SMART FEED → RELEVANT RESULTS`

### Relationship to Search

Search and Smart Tabs should use compatible retrieval semantics wherever possible.

A user should be able to search for something and, where useful, save that retrieval intent as a Smart Tab.

Conversely, a Smart Tab should be understandable as a saved shortcut to a known retrieval intent.

This creates a powerful loop:

`SEARCH → DISCOVER → SAVE AS SMART TAB → REUSE`

### Relationship to URLs

URL tabs are simple navigation shortcuts and do not need to become intelligence objects.

The tab stores the user's chosen destination and label.

If the product supports external URLs, normal security and navigation rules apply.

### Old prototype boundary

The earlier Smart Tabs component prototype demonstrated useful interaction concepts including:

- horizontal pill-style navigation
- persistence
- add/edit/remove
- favorites/stars
- route mapping
- URL/keyword fallback

That prototype is valuable evidence, but it is not automatically the final architecture.

The final implementation must preserve the useful interaction intent while integrating with the actual NayaNET retrieval and navigation architecture.

The system must not blindly reproduce prototype storage or routing if better existing primitives are now available.

## 7. LEARNING

Smart Tabs contribute to adaptive intelligence primarily through **navigation intent and retrieval behavior**.

They can reveal:

- recurring subjects
- active projects
- persistent interests
- frequently accessed destinations
- repeated searches
- changing priorities
- topics the human intentionally keeps close

Those signals can improve personalization and discovery when appropriate.

But a Smart Tab is not proof of a fact.

A tab named **MONEY** does not prove what money means.

A tab named **HEALTH** does not prove a health claim.

A tab's popularity does not verify its contents.

A tab's existence indicates an access preference or system configuration, not truth.

The useful learning relationship is:

`HUMAN EXPERIENCE → SMART NOTE → RETRIEVAL → SMART TAB → REPEATED USE → OBSERVED PREFERENCE → PERSONALIZATION → OUTCOME → NEW INTELLIGENCE`

Where the system derives durable learning from behavior, it should distinguish observed behavior from inferred preference.

Repeated use may be evidence of interest.

It is not automatically evidence of importance, correctness, or authority.

## 8. ULTIMATE MEANING

Smart Tabs solve the problem that naturally appears when an intelligence system becomes genuinely useful:

**There is too much good stuff to navigate manually.**

The answer is not to remove intelligence.

The answer is to create better navigation.

Smart Tabs make the intelligence system feel personal, immediate, and alive.

They turn the top of the Intelligent Hub into a personal control strip:

**“These are the things I want one tap away.”**

And because the tabs can point into the existing intelligence system rather than duplicate it, the navigation layer can grow without creating another giant pile of data to manage.

Smart Tabs are therefore a small interface idea with a large systems benefit:

**More intelligence without more navigation pain.**

## 9. HOW IT CONNECTS

`NAYANET INTELLIGENCE`
`↓`
`SMART NOTES / PROJECTS / DESTINATIONS / FEED`
`↓`
`SEARCH / RETRIEVAL / TOPICS / CATEGORIES`
`↓`
`SMART TABS`
`├── URL DESTINATIONS`
`├── TOPIC VIEWS`
`├── QUERY VIEWS`
`└── CATEGORY / PROJECT VIEWS`
`↓`
`SMART FEED / INTELLIGENT HUB`
`↓`
`SMART NOTES / SMART LISTS / LIBRARY / CONNECTIONS / SMART MAIL / SMART SHARE / SMART SPACES`
`↓`
`APPLICATION / OUTCOME`
`↓`
`NEW INTELLIGENCE`

### Key distinctions

**Smart Notes:** What is worth remembering?

**Smart Lists:** What do I intentionally keep together?

**Smart Tabs:** Where do I want to go right now?

**Smart Feed:** What intelligence is flowing here?

**Search:** What am I looking for?

**Intelligent Library:** What does this intelligence mean, and where can I learn more?

**Intelligence Today:** What mattered most today?

**Intelligence Reports:** What happened over time, and what did we learn?

These layers should cooperate rather than compete.

### Example end-to-end flow

A user searches for AI project notes.

`SEARCH → RESULTS → DISCOVER RECURRING NEED → SAVE AS SMART TAB “AI PROJECT”`

Later:

`TAP AI PROJECT → EXISTING RETRIEVAL → PERMISSION FILTER → SMART FEED RESULTS`

The user selects eight especially useful notes:

`SELECT → ADD TO SMART LIST “AI PROJECT RESEARCH”`

Later still:

`SMART LIST → SHARE SELECTED NOTES → AUTHORIZED SMART SPACE`

The intelligence has moved from discovery to organization to application without being duplicated at each layer.

## 10. HOW TO APPLY IT

### Create a Smart Tab

1. Choose **Add Smart Tab**.
2. Give it a clear human-friendly name.
3. Choose what it does: open a destination or show intelligence.
4. Enter the URL, topic, query, category, or keywords.
5. Choose scope when the product supports it.
6. Save it.
7. Reorder it if desired.

### Example: URL tab

**Label:** Google

**Type:** URL

**Target:** `https://google.com`

Tap it → navigate.

### Example: single-topic tab

**Label:** AI

**Type:** Topic

**Target:** AI

Tap it → Smart Feed retrieves AI-related intelligence.

### Example: multi-keyword tab

**Label:** MONEY

**Type:** Query

**Keywords:** bitcoin, investing, revenue, business, income

Tap it → retrieval returns intelligence matching the configured query according to the system's search semantics.

### Example: project tab

**Label:** MY PROJECT

**Type:** Query / Project

**Target:** Naya Power, Smart Tabs, Intelligent Hub

Tap it → retrieve the relevant project intelligence.

### Smart Tab management

The ideal experience makes these actions obvious:

- **Add**
- **Edit**
- **Rename**
- **Reorder**
- **Favorite / Pin**
- **Remove**

The human should never need to edit raw JSON or understand internal IDs.

### Naya assistance

Naya may suggest:

> “You search for this every day. Want me to turn it into a Smart Tab?”

or:

> “You have several active notes around this project. Want a quick-access tab?”

If the user authorizes the action, Naya can create or modify the tab according to the applicable product permissions.

### Quality standard

A 10/10 Smart Tabs experience should be:

- immediately understandable
- visually beautiful
- fast
- persistent
- horizontally scrollable
- easy to edit
- easy to reorder
- useful with both destinations and intelligence
- integrated with existing search/retrieval
- permission-safe
- non-duplicative
- accessible
- calm rather than noisy
- responsive to human interaction
- obvious about what a tab will do

The feature should feel like it has always belonged in the Intelligent Hub.

It should not feel bolted on.

## 11. WHAT'S IN IT FOR YOU?

**You get the intelligence you care about one tap away.**

Instead of digging through the Feed, searching the same thing again and again, or trying to remember where a useful project lives, you create a Smart Tab once and keep it close.

Your tabs can be:

**places you go**

**topics you care about**

**projects you're working on**

**intelligence you want instantly**

**web destinations you use repeatedly**

And because Smart Tabs point into the intelligence system instead of copying it, your navigation can stay simple even while your intelligence keeps growing.

**Smart Notes remember it.**

**Smart Lists organize it.**

**Smart Tabs get you there.**

**Smart Feed brings it alive.**

That is the magic:

**More intelligence. Less hunting. One tap away.**

---

# CANONICAL SYSTEM INTELLIGENCE — GITHUB ONLY

## Canonical Identity

**Subject:** Smart Tabs

**Number:** 09

**System role:** Persistent human-configured navigation and retrieval-intent layer over NayaNET destinations and canonical intelligence.

**Primary purpose:** Provide immediate access to frequently used destinations, topics, categories, projects, searches, and intelligence views without duplicating canonical data.

## Core Contract

`SMART TAB → INTENT / TARGET → EXISTING NAVIGATION OR RETRIEVAL → PERMISSION / AUTHORITY FILTER → PRESENTATION`

For URL navigation:

`SMART TAB → URL → NAVIGATE`

For intelligence retrieval:

`SMART TAB → QUERY / TOPIC / KEYWORDS → EXISTING RETRIEVAL → PERMISSION FILTER → SMART FEED / RESULT`

Smart Tabs are configuration and navigation state, not canonical intelligence content.

## Architectural Boundary

Smart Tabs must not:

- duplicate Smart Notes
- become a second search index without need
- create isolated intelligence silos
- bypass privacy
- bypass authority
- silently convert private intelligence into collective intelligence
- replace Smart Lists
- replace Smart Feed
- replace Search
- become a second canonical database

The preferred implementation is a thin layer over existing retrieval and navigation primitives.

## Reuse-First Implementation Rule

Before implementing Smart Tab-specific retrieval, inspect the actual current NayaNET architecture and identify the existing primitives for:

- Smart Note retrieval
- Feed filtering
- search
- topic/category matching
- project relationships
- routes/pages
- permission checks
- visibility scopes
- favorites/saved state

Reuse those primitives whenever they can satisfy the Smart Tab contract.

Do not build a parallel tagging or indexing system merely because Smart Tabs need filtering.

## Object Model

Conceptual object:

`SmartTab`

Required conceptual properties:

- stable ID
- human-facing label
- target type
- target definition
- owner / authority scope
- visibility/privacy scope where relevant
- position/order
- created_at
- updated_at
- created_by

Optional properties:

- favorite
- pinned
- priority
- icon
- color/theme token
- description
- analytics metadata
- suggested_by
- accepted_at
- last_used_at

The final implementation should add fields only when they provide a demonstrated product benefit.

## Label vs Target

This is a fundamental rule:

**The label is human language. The target is machine intent.**

Example:

`label = MONEY`

`target.keywords = [bitcoin, investing, revenue, business, income]`

The system must not assume that the label itself is the complete retrieval instruction.

## Target Types

Initial supported conceptual types:

- URL
- topic
- query
- category
- route
- project

Some types may share one underlying retrieval implementation.

The type exists primarily to make behavior explicit to the human and machine.

## Scope and Permissions

Scope is not authority.

A tab may request personal or collective retrieval, but the underlying objects still determine actual access.

Required order:

`TARGET → RETRIEVE CANDIDATES → APPLY AUTHORITY / PRIVACY → RANK / PRESENT`

Never:

`TARGET → PRESENT → CHECK ACCESS`

A Smart Tab cannot be a privacy bypass.

## Personal vs Collective

A personal Smart Tab may retrieve personal intelligence according to the owner's permissions.

A collective Smart Tab may retrieve authorized collective intelligence.

A shared tab must not implicitly grant access to its underlying private targets.

If a tab configuration itself contains sensitive target information, the tab configuration must also receive appropriate privacy treatment.

## Human Authority

Human-created Smart Tabs represent intentional navigation configuration.

Naya may suggest or create tabs when explicitly authorized or when product rules provide appropriate authorization.

System-generated tabs must remain distinguishable from human-authored configuration when that distinction matters.

Naya suggestion ≠ human decision.

## Dynamic Smart Tabs

The system may eventually support automatically generated tabs from:

- recurring searches
- active projects
- repeated navigation
- user interests
- current context
- recent work

Dynamic tabs should be treated as generated views unless and until the human saves/accepts them as persistent personal configuration.

## Smart Tabs and Smart Lists

Architectural distinction:

**Smart Lists = intentional collections of references.**

**Smart Tabs = intentional shortcuts to destinations/retrieval intent.**

A Smart Tab can retrieve intelligence and then allow selected objects to be added to a Smart List.

A Smart List should not be converted into a Smart Tab merely because both are navigable UI objects; their underlying semantics remain different.

## Smart Tabs and Search

Search is an active retrieval request.

A Smart Tab is a persistent reusable retrieval/navigation request.

Relationship:

`SEARCH → DISCOVER USEFUL QUERY → SAVE AS SMART TAB → REUSE`

A saved search may therefore be implemented internally as a Smart Tab when that is architecturally clean.

## Smart Tabs and Smart Feed

Smart Feed is the presentation experience.

Smart Tabs may alter its query/category state.

The Feed remains responsible for displaying retrieved objects and preserving their source, privacy, verification, and interaction semantics.

## Smart Tabs and Library

A Library page can be a destination of a URL/route tab.

A Library category can also be a retrieval target if the underlying Library architecture supports it.

Smart Tabs should not duplicate Library entries.

## UI / Interaction Contract

The intended baseline is:

- horizontal tab bar
- scrollable when necessary
- persistent within the relevant Hub context
- manual swipe/scroll
- one-tap activation
- clear active state
- easy add/edit/remove
- optional pin/favorite/reorder

Auto-scroll is optional enhancement, not core functionality.

If used:

- pause on hover/focus/touch
- yield immediately to user interaction
- do not auto-change the active destination unexpectedly
- support reduced-motion/accessibility behavior
- never obscure tab labels

## Prototype Evidence

An earlier Smart Tabs prototype used a portable component model with:

- horizontal pill navigation
- local persistence
- add/edit/remove
- favorites/stars
- route mapping
- keyword fallback

That prototype establishes interaction intent, not final architecture.

Final implementation should adapt the proven interaction ideas to current NayaNET architecture rather than importing obsolete assumptions.

## Verification Contract

Because Smart Tabs can alter retrieval and navigation, implementation verification must prove:

1. The tab is persisted correctly.
2. Editing changes the actual target.
3. Clicking a URL tab reaches the intended destination.
4. Clicking a topic/query tab invokes the intended existing retrieval path.
5. Retrieved content is filtered by current permissions.
6. No canonical Smart Notes are duplicated.
7. Reordering persists.
8. Removal behaves correctly.
9. Refresh/re-entry preserves expected tabs.
10. Auto-motion, if present, never overrides human interaction.

Source code or documentation alone does not prove runtime behavior.

Required consequential verification chain:

`SOURCE → BUILD / EXECUTION → DEPLOYMENT → EXACT TARGET → OBSERVATION → VERIFICATION`

## Failure Modes

Guard against:

- tabs that look clickable but do nothing
- labels that do not match behavior
- broken or unsafe URLs
- query tabs that do not use real retrieval
- duplicate storage of Smart Notes
- stale query semantics
- search behavior differing unexpectedly from Smart Tab behavior
- permissions checked too late
- private intelligence exposed through a tab
- sharing a tab accidentally sharing its underlying intelligence
- Naya-generated tabs mistaken for human-authoritative organization
- auto-scroll stealing interaction
- excessive tab accumulation becoming another clutter problem
- tabs becoming another independent taxonomy/database
- analytics optimizing clicks rather than useful outcomes
- popularity being mistaken for truth

## Quality Gate

A Smart Tabs release should score at least 9.5/10 across:

- clarity
- usefulness
- navigation speed
- retrieval accuracy
- persistence
- editability
- accessibility
- privacy
- authority
- provenance
- non-duplication
- integration with Smart Feed
- integration with Search
- integration with Smart Lists
- visual quality
- interaction quality
- runtime reliability

The final question is:

**Why is this not a 10?**

Any identified weakness should become the next improvement target where the improvement is materially better and does not destroy existing functionality.

## Final Contract

Smart Tabs are the **personal navigation layer for a growing intelligence system**.

They give humans immediate access to:

**places, projects, topics, categories, searches, and intelligence.**

They are persistent, editable, human-friendly, and retrieval-aware.

They reuse existing NayaNET intelligence rather than duplicating it.

They preserve privacy and authority.

They distinguish human intent from machine target.

They make the Intelligent Hub dramatically easier to navigate as intelligence volume grows.

The enduring architectural principle is:

**Don't build more intelligence to solve a navigation problem. Build better navigation into the intelligence that already exists.**

And the enduring user promise is:

**More intelligence. Less hunting. One tap away.**
