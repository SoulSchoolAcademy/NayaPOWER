# NayaNET 24-Door First-User Audit — One Network, Team Naya First
**UTC:** 2026-10-23 | **Audit:** public HTTP routes + read-only existing Supabase counts and policy metadata; no independent authenticated end-to-end user journey.
**Role:** evidence annex for existing Team Naya/Hub area boards and Project Intelligence PR #3014, not an alternate plan or permission grant.
**Director's outcome:** every Naya should be able to use her own identity, Personal/Business/Community page, Smart Mail, projects, notes, Spaces, Lists and other tools as the first real community. Team Naya both builds and fills every surface; the human director *reviews*, never types in our project data.

## Essential grading law

**HTTP 200 = route reaches an HTML/JSON asset, not the feature works.** Readiness has independently testable levels: L1 reachable; L2 rendered/usable in real browser; L3 correct authorized source data; L4 complete read→action→write→read-back journey; L5 independently proved two-user privacy and permissions; L6 automatic ongoing source-content publishing, alerts, cost and cold successor reuse. Unknown is never PASS; do not assign fabricated completeness percentages. **Live evidence can supersede this one-date observation.**

## Complete route inventory (24 targets, all responded HTTP 200)

| Category | Public door | What it does | Observed state | What's left to qualify |
|---|---|---|---|---|
| Hub | https://nayanet.live/ | One Hub, navigation, Naya entry, Feed | Large JS app shell returned | Actual logged-in navigation, content/receipts, correct identity |
| Flagship | https://nayanet.live/personal | Person's profile, notes, connections, activity | Rendered HTML; default title **Nova Reyes** | Replace/validate demo default through session-bound real user, persist/read twice |
| Flagship | https://nayanet.live/business | Business identity, collaborators and work | Rendered HTML; title **Acme Corp** | Authenticated organization and business data, scope, team actions |
| Flagship | https://nayanet.live/space | Community identity and collective context | Rendered HTML; title **Our Community** | Real approved membership, posting, privacy and event history |
| Flagship | https://nayanet.live/dashboard | Operating overview and signals | Rendered HTML; title **Nova Reyes** | Real user-specific metrics, actions and provenance |
| Room | https://nayanet.live/rooms/today | Today's intelligence and next action | Dedicated page returns 200 | Validate live personal event input, meaningful real-time next action |
| Room | https://nayanet.live/rooms/reports | Reports, insights, evidence | Dedicated page returns 200 | Canonical source alignment, latest reports, open underlying receipt |
| Room | https://nayanet.live/projects | Projects + people + notes + proof + total map | Live page has actual Supabase read path | True continuous auto-population; root source/display key parity; authenticated browser acceptance |
| Room | https://nayanet.live/rooms/intelligence | Living system/project intelligence | Dedicated page returns 200 | Same authorized snapshot and 14Q as /projects machine state; no second truth |
| Room | https://nayanet.live/rooms/mail | Smart Mail inbox and correspondence | Dedicated page + underlying populated tables | **P0: private mail permission review**; authenticated two-seat exchange and third-seat denial |
| Room | https://nayanet.live/rooms/spaces | Durable Smart Spaces and membership | Dedicated page, 7 space records, 2 memberships in store | Create/join/post/read/leave with privacy and evidence |
| Room | https://nayanet.live/rooms/lists | Shared reusable lists and tasks | Dedicated page returned | List CRUD, persistence, ownership and action history |
| Room | https://nayanet.live/rooms/connections | Contacts, agents and consented connections | Dedicated page returned | Real identity search/link/unlink, provenance and consent |
| Room | https://nayanet.live/rooms/growth | Invitation and growth/referral flow | Dedicated page returned | Verified signup destination and attribution, no false conversion counts |
| Room | https://nayanet.live/rooms/ledger | Receipts, value, independent proof | Dedicated page returned | Actual current ledger source and proof drill-through, stale/revocation test |
| Room | https://nayanet.live/rooms/library | Search and reuse intelligence | Dedicated page returned | Actual authorized search/retrieval + behavior-changing lesson reuse |
| Hub surface | https://nayanet.live/rooms/feed | Smart Feed within the Hub | Returns Hub shell, not distinct page | Verify intended internal Feed route and one real Smart Note arriving |
| Hub surface | https://nayanet.live/rooms/settings | Settings within Hub | Returns Hub shell, not distinct page | Verify actual in-app Settings, persistence and consent controls |
| Action | https://nayanet.live/book | Book an available appointment | Booking UI loads | Real legitimate availability, confirmation/reminder/cancel and rollback under test authority |
| Action | https://nayanet.live/pay | Pay for authorized product/service | Payment UI shell loads | Sandbox authorization, captured receipt, failure/refund; NO production charge as probe |
| Entry | https://nayanet.live/joinus | Referral invite and signup | Returns Hub after redirect to `/?aff_id=...` | Demonstrate successful real registration plus attribution. Not yet proven |
| Builder | https://nayanet.live/smartfactory | Template/part composition into a Smart App | Large builder/catalog HTML present | Intent→template→build→save→functioning live app + independent acceptance |
| Knowledge | https://nayanet.live/s/sn0840 | Master Team Naya build Smart Note | HTTP 200 and matching title | Prove later retrieval/behavior change, not just working link |
| Machine | https://nayanet.live/projects/state.json | Machine current counts, tip, freshness, decisions | HTTP 200 actual JSON after earlier 404 | Complete scoped 14 questions + authenticated claim/handoff/unknowns; verify true source parity |

**Important:** the two `/rooms/feed` and `/rooms/settings` paths return the same Hub shell; do not falsely count these as separate fully working rooms. `joinus` is a genuine redirect but its successful sign-up outcome has NOT been demonstrated.

## Existing content/identity reality (read-only evidence, not proof of full app use)

- Public-store aggregates during audit: 7,502 `members`, 14 `smart_mail_aliases` (3 seat aliases, 3 page, 7 space, 1 system), 8 `smart_mail_threads`, 9 `smart_mail_messages`, 7 `smart_spaces`, 2 `smart_space_members`; existing records do not prove distinct agent authentication or real two-way receipt.
- At the previous first-fill proof, all eight Project Intelligence child projects had 38 current source work items and 38 corresponding display records, each with one new attributed note and three useful links. The root's display later **fell behind by 10 exact work keys plus 11 state/proof discrepancies**, despite gross counts looking closer because three production pseudo-records were mixed in. The current human page is not yet proven to auto-maintain this content.
- `/projects/state.json` now returns real machine JSON including `counts`, `freshness`, `state_tip`, `truth_now` and `production`. This is an advance; its public response is not yet the full permission-scoped 14Q agent orientation contract.
- Existing Personal/Business/Space/Dashboard page titles are recognizable example identities; whether real logged-in overrides correctly replace them requires a browser session test.
- One additional missing Library door was linked to the root Projects source inventory in the existing `object_links` table (HTTP title checked; not claimed independently functional).

## First citizen has already begun — correction to the initial audit (2026-10-23 21:38–21:51Z)

**Superseding evidence:** SN-0841 in current main records that **Naya Nitro Narzan** successfully claimed a citizen identity alias with certificate #34 on 2026-10-23 21:27 UTC and sent a first outbound Smart Mail to the already-registered Naya Power alias at 21:39 UTC. A citizen does NOT need a separate Smart Mail directory row to make the outbound send; an earlier assumption that missing directory binding meant no live mail function was inaccurate. Inbound/reply confirmation, Sent-list recipient labeling, per-account message privacy, independent identity verification, recovery and public alias domain remain OPEN. The Director's first-resident usage experiment now has a real seed and should be extended through the *same* flow, not reimplemented.

**Security remains a production-gating defect, and the first send does not clear it.** New read-only catalog verification found `public.nayanet_identities` holds `device_key` in a broad anonymous-readable table with no immutable `owner_id` column and `anon_select_nayanet_identities` using true. The actual value/secret status of `device_key` was not investigated or read. The two private mail tables continue broad anonymous SELECT/INSERT/UPDATE policies and owner policies referencing editable `user_metadata`. Source-linked three-table preflight `tools/reporting/nayanet_agent_mail_preflight.sql` queried only metadata, not mail content or device key values, at **2026-10-23T21:51:55Z**: identity **BLOCKED**, threads **BLOCKED**, messages **BLOCKED**. Supabase security advisor independently flags mutable user metadata in relevant policies. Neither a shared display alias nor a device-local name alone is a trusted authenticated user principal.

**Smallest legitimate coordinated cure:** current LAW/Security + citizen onboarding and Mail owners inspect the real client route; preserve a way to check alias availability without exposing a private device-associated field or human private name, bind the actual resident alias to trustworthy authenticated ownership, replace unconditional anonymous private-mail reads and writes, remove editable metadata fallback, and use explicit authorization for reply delivery. Blind `REVOKE` without client integration may break the real just-proven first-resident flow, so all relevant paths require independent positive and negative tests plus existing governed production authority. Anonymous wrong-seat read denial, immutable trusted identity and a two-real-citizen send→inbox→reply must be proven **before** broad private correspondence.

**No new agent account or mail was created by this auditing seat.** No private mail rows or device credentials were read. The initial route and existing public note collaboration remain viable for properly scoped work; the first citizen's signed source note is the owner/handoff reference.

## P0 private-mail security gate — BEFORE FIRST AGENT COMMUNICATION

An internal read-only catalog review found anon/mail privilege+policy breadth inconsistent with private personal correspondence. **No message bodies were fetched; no exploit performed.** A specific P0 security review request was placed on Security & Flow board #2823. No production RLS, credentials or message data was changed. The full confidential test must establish:
- Ordinary private mail is accessible only to proven intended sender/recipient; unauthenticated and unrelated seat DENY at the real boundary.
- Sending, receiving, replying and persistence across two independent authenticated identities PASS, without recipient isolation bypass or user-controlled alias spoofing.
- Account principal and email/alias ownership are bound to an authorized authenticated user or approved machine credential (OIDC/service identity); display names are NOT authority.
- Once verified, the pilot can use real isolated test data and expand to the existing Team Naya accounts. **Do not create bogus user identities or send real personal content while this is unresolved.**

## Concrete Team Naya first-occupancy test — zero human data entry

1. Existing SELF/LAW owner enumerates **current real Naya principal identities** and the approved first-user registration flow (do not just insert display names as users). One independently controlled pilot Naya A and Naya B, plus VERIFY Naya C.
2. Authenticate A and B using distinct permitted identities; record secure owner-to-alias binding; prove Naya C cannot read either private mailbox.
3. A creates/claims her Personal space through the **real UI**, then one Business page (when role authorized), one community Space, one project note/Smart Note and one task.
4. B joins the authorized Space, replies to the note, claims a task and posts a meaningful evidence-linked progress event. Use the same canonical event IDs in global and per-part feed.
5. A sends one test Smart Mail to B and receives B's reply; verify both sides' read-back, permission denial for C, timestamps, last-good recovery and no duplicate on retry.
6. All changes automatically populate the appropriate Hub rooms, Projects Intelligence, Library, Reports/Today and machine snapshot. **No SQL hand-filling and no Shawn data entry.**
7. An entirely cold independent Naya opens the real authorized state, answers the 14 questions, locates the actual next action and continues correctly.
8. Hub/Product scorer evaluates flagship visual DNA, real tasks, mobile/keyboard use, readability and Essence Rule; security verifier signs exact revision; integrator publishes the page and one evidence packet.

**Proof grades:** ROUTE LIVE for 24/24 checked targets; JSON LIVE and public Smart Note title LIVE; DATA PRESENT for some parts; AUTHENTICATED ACTION/SCOPE/AUTOMATIC FULL CONTENT/INDEPENDENT USER acceptance = UNKNOWN/NOT CERTIFIED until tested. **The mail pilot is under P0 security hold.** Aggregate member count does not establish agent participation.

## Priority for existing work owners (not a new parallel build)

1. **Security & Flow + Mail owner:** qualified privacy repair and real anonymous/third-party denial before sending actual correspondence.
2. **SELF/LAW + identity owner:** sanctioned Naya agent principal and alias enrollment; no human passwords copied into AI prompts.
3. **ACT/Bridge + Projects data:** source→page auto-publisher from actual work/receipts/notes, exact-key parity and deterministic stale alarms.
4. **Hub/Product:** one real-authenticated smoke test of all 24 doors and flagship source binding; fix known `joinus` signup gap. Keep Feed/Settings in Hub instead of building copies.
5. **Existing room owners:** attach one real data input/output per room and run functional persistence and privacy tests; only then claim COMPLETE.
6. **Independent VERIFY:** pass the three-Naya onboarding, mail/privacy, project, Space and Smart Note journey; report failures to the same owner board with exact evidence.
7. **Integrating seat:** use these route IDs in the existing Projects total-system map with **reachability ≠ functionality ≠ proof ≠ freshness** and a direct URL. Retire temporary audit once live compiler replaces it.

**Human objective:** Shawn visits one Projects page to review the actual Team Naya-managed state. Team Naya itself creates the intelligence and improves it through usage. The director's intervention is reserved for genuine consequential authorization, not routine input.
