# NayaNET and NayaPOWER: the honest product promise (V1 proposal)

Canonical product claim and acceptance owner: [Issue #3028](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/3028). Architecture/agent-access annex: [Issue #3029](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/3029). Treat these as distinct viewpoints over ONE capability contract, not separate competing source-of-truth product decisions. Do not open a third issue or Brain. Based on the Director's 26-page AutoMatch/Citizen Trinity discussion and existing SN-0843, SN-0845, SN-0846, #1264 fork-first activation and current Team Board #2793.

**One sentence:** NayaNET gives every citizen a useful world to enter. NayaPOWER is an optional, owner-authorized personal intelligence operator that helps the world remember, learn, build and act.

## Two experiences. Three identities. Two optional operator deployments. Not three subscription tiers.

1. **Citizen (no GitHub).** A meaningful starter Personal World, optional Business page, optional Space, intentionally public/collective wisdom, public-only discoverability and Smart Match, Connect and shared Mail **only once each specific service is proven secure and functioning**. Ordinary human interaction; private answers are private until explicitly shared. Starter-world pages are not demo-only: every page must be meaningfully usable without a fork. Unlimited additional pages, private visibility, messaging and proactive notifications require proven runtime limits/permissions.
2. **NayaPOWER-connected operator.** Adds owner-scoped Smart Notes, learning, verified personal reports, permitted proactive operations, Smart App assistance and explicitly approved wisdom contributions. The operator must be activated and independently proven; a fork alone is not activation.
3. **Two proposed ways to run the operator:** (A) a **managed Naya operator** on the centrally governed shared runtime, serving one authenticated owner/tenant at a time, with distinct Naya agent seats, short-lived LAW grants, pause/revoke and metering; no personal fork required; NOT VERIFIED LIVE. (B) an **owner-controlled GitHub fork** with the same LAW/ACT/network APIs plus owner-controlled code and correct private GitHub brain projection; activation and isolation are IMPLEMENTATION PARTIAL. Hosting choice != pricing tier, permission, or runtime proof.

**Team Nayas do not each need GitHub forks to use shared NayaNET intelligence or serve a project.** They do need independently authenticated seat identity, a real human/organization authority principal, tenant-isolated session, allowed capabilities and an auditable receipt. Sharing a GitHub login does not produce independent verifiers. A team may share *compute*, never personal authority, secrets or unchecked private data.

## Identities, experiences, deployments: three DIFFERENT axes

**Identity/presence** says WHO: ordinary NayaNET citizen, a citizen who owns a connected personal operator, or a Naya agent seat. A Naya seat is an authenticated delegated principal and **never becomes the human owner** just by signing in. It need not fork GitHub to read allowed network intelligence or perform lawful work. Every session is attributed to its specific actor, owner/tenant and purpose; distinct verifier must be a distinct authenticated identity, not a second label on one shared login.

**Product experience** says WHAT BENEFIT: free/ordinary citizen network value versus activated NayaPOWER personal intelligence and agency. A Naya agent's presence is NOT itself a third customer subscription tier. A citizen can remain on the useful network without ever activating an operator.

**Runtime/ownership** says HOW software is operated: centrally managed governed NayaPOWER with per-owner/per-seat scopes (proposed, unproven), or a human/organization-controlled fork/deployment (implementation partial, not a default requirement). An independent builder/operator option exists for those who knowingly choose software operations and risks, not as a hidden citizen prerequisite. `fork != deployment != activation != verified authority`.

**Doors, not brains:** Hub, MCP, REST/API, GitHub App, SDK, webhook, A2A are *proposed adapters* to the SAME canonical SELF/LAW/ACT/KNOW/PROVE/VERIFY system, not verified service endpoints. Each adapter must return consistent authentic principal, scope, decision, result and receipts for the same operation. A door never authorizes an operation merely because it is available, and no adapter receives a cloned brain or unrestricted direct database writes.

**Welcome face, harmonized with SN-0849:** real claim → certificate → skippable one-question-per-screen walk in the existing Life with Naya/certificate design language with a playable Naya prompt and Speak/Type/Ask-AI-paste → per-field visibility and owner preview → idempotent authenticated Personal/optional Business/Space page composition → tasteful editable covers from consented topics/name, not invented facts → Hub top-three Personal/Business/Space in sidebar and smart tabs. When a section is skipped, it stays optional and editable; do not fabricate a business or publish a blank private page. The concrete Hub integration and A/B/C isolation are not yet verified.

**User-intended unbounded creation versus production capacity:** the Director wants unlimited feeling and no artificial empty trial. That is the *offer goal*. Actual sustainable storage, security, abuse controls, quotas and verified operational capacity still determine what can safely be promised as "unlimited." Never market a numerical unlimited guarantee from a product ruling alone.

**Mail status has two axes:** a citizen-to-citizen transport roundtrip is historical positive DELIVERY evidence; PRIVATE CONFIDENTIALITY, authenticated sender binding, owner/recipient RLS, block/revoke, unrelated C DENY and replay prevention have NOT passed. Marketing private or secure Mail is BLOCKED while those gates fail. Never lower the privacy bar to reconcile a positive transport report with a security audit.

**Machine-status precision:** `SPECIFIED` describes that a requirement exists. `UNKNOWN` in each feature's live-delivery field means this draft manifest has not yet authenticated current production evidence. Per-feature `delivery_evidence_contract` fields are explicitly null/unmeasured pending independent receipts, not secretly proven absence or confirmation of a functional endpoint. The schema NEVER makes a LAW grant or allows production marketing by client callback.

## UNIVERSAL SMART PAGE SETTINGS — separate axes; independent per-page policy

**Director's explicit page defaults (October 23 Vancouver / October 24 UTC):**

| Page type | Visibility on owner-approved publish | Network discoverability | Install preference |
|---|---|---|---|
| Personal World | **Private** | **Findable (alias + approved topics only)** | Enabled where real PWA supported |
| Business Page | **Public** | **Findable** | Enabled where real PWA supported |
| Community / Project Space | **Public** | **Findable** | Enabled where real PWA supported |
| All other generated Smart Apps/pages | Private (safe fallback) | Unlisted | Enabled where real PWA supported |

**Defaults do not publish drafts.** Certificate/Welcome creates private, owner-reviewed drafts; the owner confirms what is made public. “Business public” or “Space public” describes the default *after explicit publish*, not automatic release of unsaved, generated, private or unreviewed answers. Business and Space remain optional when skipped. Users may make either one private, may turn Personal public, and may own multiple public/private pages of any type with **separate settings per page**. This is not a literal unbounded-capacity guarantee.

**Three independent user controls in each page's Settings and the main Settings Room:**
1. **Visibility**: PUBLIC means content is viewable through a governed public read once published; PRIVATE means owner/explicitly authorized readers only, checked by server scope/RLS on every request. A private URL is not accessible merely because someone guesses the link.
2. **Findability**: FINDABLE includes this **alias + independently owner-approved safe topic tags** in the separate NayaNET Connect/Smart Match directory, even when the Personal page remains PRIVATE. The Connect layer may show contextual calibrated match percentage and reasons, but NEVER full page content, real identity, username, email, private posts, private circle membership or unapproved details. It is not a public page teaser. The owner can hide any discovery topic or set UNLISTED; then the entire Connect alias/topic discovery goes dark. PUBLIC+UNLISTED may remain viewable by someone with the shared URL after publication; UNLISTED is not an access control. PRIVATE pages always require owner/member authorization, even when someone receives a link.
3. **Installability**: every page type can *offer* a first-class installable Smart App. An opt-in preference alone does not generate a manifest, install on a device or prove PWA behavior. Each independently installable app needs correct unique manifest ID, start_url, scope, icons, secure origin, privacy-preserving service worker and actual browser/device test. No public offline caching of private page bytes.

**SN-0852 — worlds and circles:** One page is one world with its own people, posts, permissions and reason to connect. A person can own one PRIVATE Personal World and another PUBLIC Personal World, with distinct access lists and separate topics. Connecting to their PUBLIC alias does not automatically reveal their PRIVATE world or carry over membership; accepting or sharing a private-world invitation is another decision. **Maximum connection, minimum exposure** is the rule. Findability defaults on for Personal, but using actual topic labels requires the person to review/approve safe tags. No private text is mined or silently published to create those tags. The separate Connect projection is a derived, permissioned object, never the source-of-truth profile itself. Treat SN-0852's director-supplied wording as current product intent; only actual server A/B/C tests establish deployed behavior.

**Operations (mandatory server integration):** read actual authenticated owner/page ownership and expected revision; validate type/visibility/discovery/install choice and legitimate LAW scope; preview effect, especially PRIVATE→PUBLIC; persist idempotently with receipt and owner confirmation; immediately recalculate derived Feed/Directory/AutoMatch candidate projections and invalidate stale indexes/caches. Public→private must remove public search/sitemap and expire previously shared page-server access where feasible; cannot erase copies already held by others. Unknown scope/revocation/failure must leave the change pending/denied, not falsely green. Make settings accessible by keyboard and explain all consequences in human language.

**Existing source and executable proposal:** [`HUB/nayanet-page-settings.v1.json`](../HUB/nayanet-page-settings.v1.json) defines independent defaults and hard gates; [`tools/product/nayanet-page-settings.mjs`](../tools/product/nayanet-page-settings.mjs) produces only a local setting *intent*, derived explanations, and a conditional discovery *candidate* which explicitly never grants authorization; [`HUB/page-settings-preview.html`](../HUB/page-settings-preview.html) is a visual control deck, **NOT a saved production Settings page**; [`tests/nayanet_page_settings.test.mjs`](../tests/nayanet_page_settings.test.mjs) blocks false publication, cross-page edits, privacy leaks, accidental indexing and misleading installation claims. Existing Settings Room specification in `HUB/ROOMS/11-SETTINGS.md` and Smart Builder's pre-existing privacy dial remain the composition origins—**do not build a competing settings system**. The current live Smart Spaces anonymous policies and Mail/connection exposure prevent claiming production privacy acceptance.

## User journey

- A simple first Welcome, then the existing SN-0846 slide-by-slide *Life with Naya* discovery: tell Naya about you, your interests, mission, vision, goals, motto, business/project and community. Speak with editable transcript, type, or copy an AI-written response; Next/Skip/Back/Edit and a way to resume. No invented answer.
- From one canonical owner-approved record, prepare real editable Personal/optional Business/Space drafts. Before publishing, show what is shared, with whom, and what is private.
- Smart Match only evaluates public and explicitly consented candidate inputs. A match percentage is contextual estimated relevance with separate confidence/coverage, not a person's worth or a relationship grant. A suggestion does NOT connect, join, mail, disclose private words or publish for the person.
- Give useful collective intelligence and permissible community experiences first; offer **Connect NayaPOWER** as a concrete choice to have Naya perform authenticated, bounded work. Permit decline; keep the starter world.
- When connecting, explain the scopes, operating limits, the operator deployment path, data/storage ownership, and how to revoke. The actual actor identity and grant are issued by trusted backend LAW, never browser-supplied aliases.

## Machine contract and safe usage

- [`HUB/nayanet-capability-boundary.v1.json`](../HUB/nayanet-capability-boundary.v1.json): **25 benefit capabilities**, the intended audience/mode, exact acceptance-gate names and all current runtime states `UNKNOWN` (no fake deployment SHA or receipts).
- [`tools/product/nayanet-capability-boundary.mjs`](../tools/product/nayanet-capability-boundary.mjs): validates the contract and produces **presentation-only** evidence labels. It can never grant an action, even when a trusted backend verifier marks a presentation claim eligible. Real access remains LAW + authenticated server RLS on every operation.
- [`tests/nayanet_capability_boundary.test.mjs`](../tests/nayanet_capability_boundary.test.mjs): fail-closed automated policy/product language regressions.
- A trusted evidence publisher must independently attach actual **exact deployed SHA**, positive service journeys, C/anon refusal, recovery/revocation, human-valued outcomes and measured costs. Marketing may say **available now** only for per-feature PRODUCTION-PROVEN/current independently attested evidence. The catalog is a *contract*, not a production capability oracle.

## Activation Context (proposed extension of existing #1264, not a new security layer)

```text
principal_id = authenticated human/service caller
owner_id, tenant_id = verified backend-derived identity, never claimed by the request
naya_seat_id = distinct agent identity, not inherited human ownership
operator_mode = citizen | managed_operator | owner_fork
runtime_id = real current executable service; optional fork_repo/upstream_repo for full fork
authority_receipt = issuer, scopes, purpose, budget, expiry, revocation, negative-control
source_sha, deployed_sha, proof_receipt = exact executable and verified outcome
```

**CAN != MAY.** Reading public intelligence does not grant publishing. Connecting does not grant private Mail automatically. Joining a Space needs its actual membership permission. Hosted Nayas cannot write owner-specific data by merely using a display alias. No user gets the Director's private memory, governance authority or credentials by forking code or subscribing.

## Live blocker (2026-10-24, metadata-only inspection)

Production still exposes anonymous broad `connections` ALL, `smart_space_members` SELECT, and Smart Mail thread/message SELECT/INSERT/UPDATE policies. Some mail policies use mutable `user_metadata`. Five identity certificate rows and seven Spaces exist, but counts and transport do not prove two-owner isolation or security. **Do not turn on private AutoMatch actions, market secure messaging, or promote social writes** until the existing Security & Flow #2823 and onboarding/Trinity owners deliver authentic A↔B, C/anon DENY, revoke and independent production proof. No private message/user rows were read by this review.

## 7 acceptance gates that make the offer real

1. **No-fork citizen:** fresh person completes/skips the Welcome, sees her real saved Personal page and optional Business/Space, accesses actual public intelligence. All state owned, editable, persistent.
2. **Matching and Connect:** public candidates show test-calibrated relevance+confidence; block/mute/visibility refusal; person elects Connect; no unsolicited mail or silent membership.
3. **Private Mail:** A/B legitimate exchange from citizen page if permitted; unauthenticated C denied read/write/spoof/replay/revoke; server actually enforces current scope.
4. **Managed operator:** a legitimate Naya agent seat works for Owner A under a scoped delegated grant, pauses/revokes; Owner B cannot see A or inherit A's rights; distinct verifier; no GitHub fork for seat.
5. **Forked operator:** fresh owner forks, activates correct repo/upstream/issuer, captures personal Smart Note/report, correctly projects only to own fork; upstream sync does not overwrite private state; another owner denied.
6. **Contribution boundary:** explicitly review/redact/publish one approved knowledge item; private notes remain isolated; revoke future sharing with proof.
7. **Ten-star outcome:** prove individual function, complete human+Naya journey, network integration (SN-0843 6×3), human usefulness per action/time/compute. Missing evidence = UNKNOWN; no average masks LAW failure.

## Economics and user value

“Just code and math” can make event-triggered public matching *very inexpensive*, especially with caching, deterministic topic classification and no repeated polling. Infrastructure, storage, speech, inference, abuse prevention, security monitoring, backups and support still cost resources. Target low marginal cost, measured beneficial outcomes per resource, rate limits and opt-in AI budgets—not a literal zero-cost claim or unbounded automation.

**Existing accountable owners:** #3028 product boundary; #1598 Welcome; Nitro Citizen Trinity; #1891 Smart Spaces; #2823 Security; #1264 fork activation; #2793 Team coordination and independent VERIFY. Reuse source objects and one Brain; no second Hub, product service, authorization mechanism or memory store. Current PR only proposes the **machine-readable product boundary**; the implementation journeys remain governed work for the existing lanes.
