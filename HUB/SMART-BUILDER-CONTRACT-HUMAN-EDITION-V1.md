# THE SMART BUILDER CONTRACT — HUMAN EDITION

**Date:** 2026-10-17  
**Status:** Human-readable product-intent contract; proposed canonical contract pending Director review and the corresponding AI/machine contracts.  
**Owner:** Shawn Vibert, Human Director  
**Scope:** NayaPOWER, NayaNET, Smart Builder, Smart Apps, templates, personal-world pages, connected services, and their shared experience.

This document captures the product intent in human language. It must be translated into the AI operating contract and machine-readable schemas only after the Human Director confirms that this edition preserves the full intent. It does not override NayaPOWER's existing laws, authorization rules, privacy requirements, or proof standards.

## 1. The vision

NayaNET helps people turn an idea, a need, a business, a project, or their personal world into a **Smart App**: a useful, mobile-first, connected experience that can present information, communicate, answer questions, publish, organize a community, and perform authorized work for its owner.

We are not merely building a website builder. We are building a faster, more intelligent way to assemble active apps around a person's world.

**The promise:** “Not 24 days. Not 24 weeks. A working app in 24 hours—and sometimes in 24 minutes.” Time depends on the app's complexity, the connections and permissions required, and how quickly the owner provides input. This is a target and product promise to validate through real builds, not a guarantee that every possible app can be completed in that time.

**Positioning:** “Build smart. Stay connected. Let intelligence do the work. Be a wise one.” The experience should make the intelligent choice the easy choice: pre-built starting points, sensible defaults, clear options, and Naya doing the hard work.

## 2. What a Smart App is

A Smart App is a small, useful application assembled from a shared, governed system of reusable design, components, templates, integrations, and actions.

A Smart App should be:
- **Active, not merely present:** it can do useful work, not just display a static page.
- **Intelligent:** Naya can help the owner define, build, operate, and improve it.
- **Connected:** it can link to the owner's authorized services, content, people, and projects.
- **Mobile-first:** its primary experience is designed for a phone, with desktop supported as a larger presentation of the same product.
- **Installable:** every eligible app should be delivered as an installable Progressive Web App (PWA) by default, with a clear “Install app” path and honest compatibility/offline states.
- **Composable:** the owner can add or remove boards, buttons, panels, capabilities, and integrations without rebuilding the whole app.
- **Governed:** actions respect identity, permissions, privacy, consent, provenance, and the owner's authority.
- **Reusable:** a successful build can be saved as a template so others can start from proven work.
- **Honest:** unavailable, unconnected, unauthorized, unverified, or failed capabilities must be shown truthfully.

A page is the entry point, not the whole product. The page is where the app's useful experience lives; the shared NayaPOWER/NayaNET substrate supplies identity, intelligence, events, permissions, and governed actions.

## 3. The central experience: click, choose, build

The default path must remove the blank-page problem and minimize technical questions.

1. **Choose a starting point.** Select a ready-made template, start from a saved template, or describe the outcome in plain language.
2. **Let Naya make a sensible first draft.** Naya proposes the topic/category, structure, content prompts, layout, design, components, and likely useful features from the owner's stated goal.
3. **Answer only what matters.** Ask short, contextual questions with multiple-choice answers and good defaults. Accept partial answers where possible. Do not force the owner to answer questions Naya can safely infer or defer.
4. **Choose or adjust components.** The owner can keep the template as-is or add, remove, reorder, or replace boards, buttons, sections, slide-over panels, and actions.
5. **Connect the owner's world.** Offer relevant integrations such as GitHub, Google Drive, and other supported services. Explain the access requested and what it enables before authorization.
6. **Preview the real experience.** Preview on mobile dimensions, inspect navigation and actions, and show which features are ready, connected, need permission, or are still unavailable.
7. **Publish and install.** Publish when all required gates are satisfied; provide a shareable URL and an install-to-phone path when supported.
8. **Keep improving it.** Naya helps the owner add features, automate work, learn from activity, and revise the app without losing working behavior.

The owner's job is to explain what they want and make meaningful choices. Naya's job is to do the analysis, propose a coherent build, assemble it, test it, and explain what is genuinely ready.

## 4. Templates are a first-class product

Templates are not decorative examples. They are reusable starting contracts that encode a known purpose, layout, components, default actions, questions, design rules, permissions, and acceptance checks.

Every template should define:
- who it is for and the job it helps them do;
- its default sections, boards, buttons, and navigation;
- mobile behavior and installable-app requirements;
- recommended content and image/icon needs;
- available action modules and required integrations;
- the minimum questions Naya must ask;
- privacy, audience, permissions, and moderation defaults;
- what is optional, what requires a connection, and what is not yet supported;
- validation and acceptance checks;
- author, version, provenance, license/reuse terms, and update history.

### Initial starter template collection and priority hypothesis

Templates are starting compositions, not mutually exclusive product silos. People may combine multiple templates/rooms into one connected Smart App or personal hub. The ranking below is a **hypothesis about general-population usefulness**, not a fact. We must ship, observe real usage, and revise the order from evidence.

1. **My Personal World** — the flagship personal front door: who I am, chosen profiles, projects, apps, and ways to connect.
2. **Today Briefing** — a daily view of what matters now, current activity, useful priorities, and next actions.
3. **Smart List / Organizer** — a focused starting experience for organizing notes, contacts, topics, posts, tasks, resources, or other items into useful lists.
4. **Business Landing** — a simple business home for offerings, contact paths, FAQs, and updates.
5. **Booking / Appointment** — a service and booking experience where a real, authorized booking provider is available.
6. **Product / Offer Page** — a product, offer, initiative, or campaign with clear information and next steps.
7. **Event / Workshop** — event information, participation, updates, and registration where supported.
8. **Community Hub / Smart Space** — shared purpose, posts, questions, moderation, and participation when enabled.
9. **Creator / Portfolio** — selected work, identity, media, publications, and collaboration paths.
10. **Menu / Price List** — a clear, editable menu or catalog of services, options, and prices.
11. **Signup / Interest Page** — an opt-in form or registration path with honest consent and data handling.
12. **Dashboard** — a more specialized operational view, ranked lower for general first-time use but valuable for some roles.

The earlier Knowledge Base, Smart Blog, Learning Library, Project/Launch, and Team/Organization compositions remain useful patterns and rooms/modules. They should not disappear just because the first public-facing ranking is limited to twelve. Their best structures can be included as optional rooms, variants, or saved templates rather than forcing users to choose exactly one.

### Templates compose; standard features travel with the app

A template is a recommended starting arrangement, not a limit on what the app can become. A user may start with My Personal World, then add Today Briefing, Smart Lists, a business page, a community Space, and other rooms. These parts should share identity, permissions, design, navigation, and canonical events instead of becoming disconnected mini-apps.

The app should arrive as a **complete, useful first-day experience**, with standard feature choices preselected. The build intake should show clear checkboxes, checked by default for standard features; the owner can uncheck, remove, or add features before or after the first build. Naya should explain a material dependency instead of hiding it. "Complete on day one" is the target experience—not permission to pretend an unimplemented or unverified feature works.

Cross-cutting standard features include:
- **Smart Mail**, where supported and authorized;
- **Smart Lists**, usable to organize different kinds of items—not just a dedicated "list page";
- **Smart Spaces**, for connected rooms/community where desired;
- **Connections**, to supported services and people, each with its own permission and connection state;
- **Ask Naya/Muse access**, where the actual integration and authorization exist;
- **Today / activity / reports**, where canonical event data supports them;
- **Smart Notes and Smart Links**, with capture, persistence, and learning proof kept distinct;
- **notifications and automation**, only when configured, authorized, and verified.

Feature selection is a composition step, not a new architecture. The same module contract and resolver must govern every template and room. A function is available to execute only when it is implemented, its requirements are met, and the required permission/authority is granted. Otherwise it stays blocked with a useful reason. A reported resolver or test is not accepted as independently proven until the wiring team verifies it against the real activation path. Unknown functions fail closed.

### Privacy and network visibility are owner-controlled choices

The app starts private when the owner's intent is unclear, but privacy is a **choice and control**, not a permanent restriction. Owners can deliberately make selected pages or a whole NayaNET presence public, keep them private, or share with selected people/collaborators. The UI should make the audience setting understandable and easy to change.

Connections to Muse/Naya, GitHub, other supported services, and NayaNET each need their own explicit setting and authorization. Connecting a service does not automatically publish its data. Making a profile public does not make private notes, credentials, connected-source contents, drafts, or private rooms public. Public-network participation and publication must be intentional, scoped, and reversible where technically possible.

Templates may be community-created. Owners should be able to **save a successful app as a template**, keep it private or choose to share/publish it, and let others use it as a starting point. Reuse must preserve attribution and license terms. A template copy starts a new instance; it must not accidentally expose the original owner's private data, credentials, content, audience, or connected accounts.

The template library should support browse/search, categories, previews, clear feature requirements, versioning, provenance, and honest maturity labels. A template that has not passed its acceptance checks must not be represented as verified or production-ready.

## 5. My Personal World: the flagship template

The flagship experience is: **“This is who I am. This is my world. Here is how you can connect with it.”**

The owner can assemble a personal page/app that includes, at their choice:
- their introduction, story, interests, skills, work, projects, and current focus;
- selected social profiles and external sites;
- their NayaNET pages, Smart Apps, public projects, and related Spaces;
- chosen articles, posts, media, work samples, and useful links;
- clear ways for friends, collaborators, clients, or communities to ask questions, connect, follow updates, or build together;
- a private personal control-center view that helps them navigate their connected world.

The owner controls what is public, shared with selected people, limited to collaborators, or private. “My world is connected” must never mean “everything is exposed.” The public personal page is a curated window, not a copy of every private account.

A visitor should be able to understand the person's world and, where the owner allows, move from the page into related projects, apps, conversations, or Spaces. Each destination should retain its own permissions and identity.

## 6. Connect the owner's world

A Smart App should be able to connect to the tools and knowledge sources its owner already uses, rather than force them to migrate everything into a new silo.

Potential connections include Google Drive, GitHub repositories, supported social services, communication tools, calendars, and other supported apps. Availability depends on real connectors and permissions; a service must not be shown as connected merely because it appears in the interface.

For each connection, the product must make clear:
- what account or source is being connected;
- what access is requested and why;
- whether access is read-only or can create, edit, publish, send, or delete;
- which app features will use the connection;
- what content is visible to Naya, visitors, collaborators, or the public;
- how to review, narrow, revoke, or disconnect access.

Naya and Muse should complement each other: the owner's personal Smart App can be the accessible front door to their world, while Naya/Muse can help operate and connect that world through authorized integrations. They must use the same governed identity and permission model—not duplicate the owner's world into competing stores of truth.

For knowledge-connected apps, Naya should answer from authorized sources, distinguish source-backed information from inference, show provenance where appropriate, and say when the answer is unknown. A GitHub knowledge-base connection is one possible source, not a universal prerequisite or a claim that every user has a repository.

## 7. Standard capabilities and action modules

The builder should proactively recommend standard features that make an app useful. The owner should not have to know every feature name before Naya can suggest it.

### Core experience defaults
- Mobile-first layout and navigation.
- Clear slide-over/side panels and touch-friendly interactions where they improve navigation.
- Strong responsive behavior and accessible contrast, type, controls, and focus states.
- App identity, title, icon, theme, and install experience.
- Shareable page/app URL and clear sharing controls.
- Useful empty, loading, offline, disconnected, unauthorized, and error states.
- Feed/activity and reporting hooks when supported by the canonical event model.
- A help/ask-Naya path where appropriate.
- Preview, validation, and a clear publish/readiness state.

### Optional action modules
- **Ask Naya:** answer questions using approved knowledge and tools.
- **Comments and questions:** allow visitors or members to interact when enabled by the owner.
- **Posts and mini-blog:** publish updates, articles, offers, or intelligence to the page.
- **Scheduled publishing:** prepare and schedule posts for a chosen time and cadence.
- **Smart Mail:** send email through supported, authorized connections and respect recipient consent and communication preferences.
- **Invitations and notifications:** invite relevant people to a page, project, or Space and notify them through supported channels.
- **Smart Space:** connect a page/project to a community space for discussion, participation, support, and collaboration.
- **Knowledge sync:** use an approved connected source such as GitHub or Google Drive as a grounded knowledge base.
- **Smart Notes and Smart Links:** capture useful discoveries and provide navigable links while keeping capture, persistence, and learning proof distinct.
- **Automation:** run a defined task or workflow on an event or schedule, with clear scope, owner, status, and failure handling.
- **Reports / NINA:** summarize relevant activity and state over daily, weekly, monthly, and yearly horizons when the data exists.
- **Save as template:** turn a successful app configuration into a reusable starting point.
- **Future growth/referral tools:** help users invite others and understand referral activity only after the feature is built, consent-aware, and verified.

These are modular capabilities, not promises that every connector or action already exists. The builder must disclose capability status before an owner relies on it.

## 8. Community is a natural option, not a forced exposure

A Smart App should make community participation easy when it fits the purpose. Owners can enable comments, questions, posts, collaboration, or a related Space. They can also choose a quiet, read-only, private, or personal experience.

The default should be safe and understandable:
- no public posting, mass invitations, or outbound messages without clear owner intent and the required permissions;
- no visitor-generated content without an appropriate moderation and abuse-handling model;
- no exposure of private notes, account data, unpublished drafts, or connected-source content by accident;
- clear controls for audience, comments, notifications, and removal/reporting;
- attribution and correction paths for shared material.

The goal is to create useful action in the network—not spam, forced social features, or growth at the expense of people.

## 9. Mobile-first, installable by default

Mobile is the primary design target. Each Smart App should feel like a polished, focused mobile app—not a desktop website squeezed onto a small screen.

The standard includes:
- a phone-first layout and navigation model;
- touch-sized controls and natural transitions, including slide-over panels where appropriate;
- responsive layouts that also work well on desktop;
- an installable PWA manifest, app identity, icons, and service-worker/offline behavior when supported and appropriate;
- a visible install path on supported devices/browsers, with accurate instructions when installation is unavailable;
- a coherent launch, return, loading, and error experience;
- privacy-conscious storage and safe session behavior.

The owner should not need to know image dimensions. When a page needs a hero image, cover, logo, or app icon, Naya should create or adapt suitable assets where image generation is available, or explain what input is needed. The builder should validate dimensions, crop, contrast, legibility, and focal point automatically. It should offer a preview and allow the owner to regenerate or choose another asset.

“Installable by default” is a product standard, not permission to claim that every browser supports every PWA feature or that offline behavior exists without implementation and tests.

## 10. Active intelligence: from a page to an app that works for you

Naya should help owners ask practical questions such as:
- “Can you answer common questions on my page?”
- “Can you publish an update every weekday?”
- “Can you prepare this offer and schedule it for tomorrow?”
- “Can you invite the people who opted in to updates?”
- “Can you send a Smart Mail to members of this project?”
- “Can you sync my approved knowledge base so visitors can ask questions?”
- “Can you connect this page to a Space and show project updates there?”
- “Can you help automate this recurring part of my business?”

Naya should evaluate the request, identify the necessary systems and permissions, explain material consequences, propose the simplest safe workflow, build or configure it when supported, test it, and report what actually works.

Execution rules:
- Capability does not grant authority.
- Read access does not imply write or send permission.
- Publishing, sending messages, changing connected systems, spending money, destructive actions, and other consequential operations require the relevant authorization and safeguards.
- Schedules must show cadence, time zone, content source, destination, owner, pause/cancel controls, and failure notifications.
- Automation must be observable and stoppable; it must not silently continue after permissions are revoked or required connections fail.
- For uncertain, unsafe, unsupported, or unauthorized actions, explain the blocker and offer the nearest safe next step.
- Never claim a task ran, a message was sent, a post was published, or a connection works unless there is evidence.

## 11. One shared system, not a pile of disconnected mini-apps

Every Smart App should reuse the same canonical NayaPOWER/NayaNET foundations wherever applicable: identity, project identity, events, permissions, provenance, design tokens, reusable components, connector contracts, and verification rules.

A page, feed item, report, Smart Note, Smart Link, Space, scheduled post, or notification may be a projection or event related to the same underlying project. These projections must not become competing sources of truth.

Core laws:
- One canonical capture and event path; projections reuse it.
- No duplicate brain, ledger, graph, calculator, or shadow learning store.
- **Available ≠ connected ≠ authorized ≠ working ≠ verified.**
- **Implemented ≠ verified ≠ production-proven.**
- **Stored ≠ learned.**
- A link is not proof of persistence; a rendered page is not proof of working actions.
- Unknown or blocked states must not be treated as success.
- Preserve source, author, version, permission, evidence, and correction history when relevant.

The product should be assembled from reusable modules and contracts, not copied into ten separate implementations that drift apart.

## 12. Feed, NINA, reports, learning, and community form one loop

The Smart Builder participates in the wider NayaNET loop:

**BUILD → SEE → LEARN → SHARE → CONNECT → GROW → BUILD BETTER**

- **Build:** create a page, project, or Smart App.
- **See:** understand its current state in the Smart Feed and through NINA/reporting.
- **Learn:** capture discoveries as Smart Notes; use Smart Links for navigation and sharing without overstating what they prove.
- **Share:** choose what to publish and who should see it.
- **Connect:** bring the work into a related Space or collaboration.
- **Grow:** invite and notify people through authorized, consent-aware features.
- **Build better:** let verified, attributed, permission-appropriate learning help the next person.

Daily, weekly, monthly, and yearly reports should be different views of the same canonical evidence—not separately invented totals. The feed should communicate what changed, why it matters, its state, who owns it, and the next useful action. Personal/private activity stays private unless deliberately shared.

## 13. The experience standard

The experience should feel effortless to the owner because the system has done the hard thinking.

- No blank-page trap.
- No needless questionnaire.
- No jargon when plain language will do.
- No requiring users to resize assets or understand technical configuration.
- No disconnected settings spread across unrelated screens when they can be managed in context.
- No dead buttons or decorative controls that imply an action exists.
- No fake “AI is working” animation when no work is occurring.
- No successful-looking preview that hides missing integrations.
- No forcing a community feature on someone who wants a private app.
- No making the owner rediscover routine omissions during manual QA.

Use progressive disclosure: the default path is simple; advanced configuration is available when wanted. The owner can start from a template, accept the recommended build, and customize details only when they care to.

## 14. Build, verification, and release order

We must use our own Hub and Smart Builder workflow first. **Our working Hub is the dogfood test and proof source.** We should not sell a template or promise a capability as proven until we have used it ourselves and independently verified its real behavior.

Recommended sequence:

1. **Freeze the human intent.** Confirm this edition covers the product before generating AI and machine contracts.
2. **Inspect the current canonical system.** Identify existing builder, Hub, feed, reporting/NINA, Smart Notes/Links, Spaces, mail, connector, design, and authorization contracts. Reuse what exists; do not invent a parallel architecture.
3. **Define the shared Smart App contract.** Establish identity, template manifest, module interfaces, permission model, event/provenance model, mobile/PWA standard, and acceptance checks.
4. **Build and verify the Personal World template first.** It proves identity, profile, selected links, privacy controls, connected-world navigation, mobile experience, and install path.
5. **Build the reusable template system.** Pick template, preview, customize components, save as private template, publish/share a template with attribution and versioning, and create an isolated new instance.
6. **Activate core page behavior.** Real content, navigation, share controls, feed/report projection, and useful empty/error states.
7. **Add one action module at a time.** Prioritize Ask Naya with approved knowledge, comments/questions and moderation, posts/mini-blog, scheduled publishing, Smart Mail/invitations, and project-linked Spaces according to dependencies and verified value.
8. **Connect real services.** Begin with the supported connector most valuable to the real build. Implement least-privilege scopes, connection state, revocation, provenance, and failure handling.
9. **Run the full journey.** Build from template → customize → connect → preview → publish → install on phone → use actions → share → interact → capture learning → authorized reuse → confirm feed/report consistency.
10. **Independently verify and repair.** Test mobile and desktop, permissions, privacy, accessibility, failures, regressions, and the actual end-to-end behavior. Fix failures before declaring completion.
11. **Package the proven result.** Save reusable templates and contracts only from a tested build; publish clear maturity status and limitations.
12. **Expand the library.** Add the remaining starter templates and community-created templates, applying the same quality bar.

The task list must track each deliverable with an owner, state, evidence, blocker, and next action. “Written,” “implemented,” “verified,” and “production-proven” are separate states.

## 15. Acceptance: what complete looks like

A Smart Builder release is not complete because a mockup looks good or a route renders. The declared scope is complete only when a cold user can perform the relevant journey and evidence proves it.

Minimum acceptance for the shared builder:
- choose a template or describe an outcome;
- receive a coherent, mobile-first draft with sensible defaults;
- change sections, boards, buttons, and modules without breaking unrelated behavior;
- understand which questions remain and answer them in context;
- generate or validate needed visual assets without requiring the user to know technical dimensions;
- see honest connector, permission, and capability states;
- preview and publish through the real supported path;
- install the app where the platform supports it;
- operate its enabled features and see useful error/recovery states;
- control visibility, sharing, connected accounts, schedules, and outbound communication;
- save a template and reuse it without leaking the source owner's private information;
- see canonical activity reflected consistently in feed and reports when those projections are in scope;
- pass independent checks for security, privacy, mobile usability, accessibility, and required permissions.

Each template adds purpose-specific acceptance checks. Each action module must have evidence of the real action, not only a successful UI click.

## 16. What we will measure

Measure real human value, not merely the number of pages generated.

Useful measures include:
- time from intent to a usable, verified app;
- proportion of cold users who finish a build without assistance;
- number of clarification questions the system avoids without guessing unsafely;
- successful mobile install and task completion rates;
- percentage of visible controls that perform their stated action;
- connector authorization success, revocation behavior, and failure recovery;
- scheduled post/message execution success with consent and authorization intact;
- template reuse and improvement without privacy leakage;
- user understanding of what is public, private, connected, and automated;
- verified learning reuse and reduced repeat work;
- defect, rollback, abuse, and privacy-incident rates.

The 24-minute/24-hour ambition must be measured by app complexity and verified outcome. Speed never overrides safety, consent, quality, or truthful status.

## 17. Product principles that cannot be traded away

1. **People first.** Human dignity and safety are not optimization variables.
2. **Owner control.** The person controls their identity, content, connections, audiences, and automations.
3. **Private by default when unclear.** Do not infer permission to publish, expose, invite, or send.
4. **Truth over theater.** Never simulate completion, connectivity, learning, or intelligence.
5. **Least privilege.** Ask only for the access a feature actually needs.
6. **Reusable by design.** Templates and modules should compound quality instead of multiplying incompatible implementations.
7. **One canonical truth.** All views and modules reuse the governed underlying state.
8. **Evidence before claims.** Demonstrate working behavior before declaring it ready.
9. **Simple first, powerful when needed.** Defaults carry the burden; advanced controls remain available.
10. **Learn and improve.** Verified outcomes should make future builds faster, clearer, and more useful without leaking private data.

## 18. The promise to the builder

You bring the goal, your knowledge, your choices, and your permission. Naya helps turn them into a useful app. You can begin with a proven template, personalize it, connect your world, and add active capabilities as you need them. Your app can introduce you, serve your customers, publish your ideas, answer from your approved knowledge, bring people together, and automate authorized work.

You should not have to become a software engineer to get the benefit of software. You should be able to say what you need, see a clear proposal, make the choices that matter, and get a working result with honest proof of what is ready.

**Build smart. Connect your world. Let intelligence do the work. Be a wise one.**

---

## Human Director review boundary

This is the **human edition only**. The AI operating edition and machine-readable contract/schema are intentionally not included yet. After the Human Director confirms or revises this understanding, those editions must map back to this document, identify the canonical source, define enforceable states and permissions, and include tests/acceptance criteria. They must not silently add product promises or weaken these laws.
