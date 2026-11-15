# Intel Today — Human-First, Machine-Readable Discovery Report
**Status: DRAFT SPEC / NOT RATIFIED / NOT DEPLOYED. 2026-11-12.**
**Director principle:** We align with search engines, AI retrieval and machine interfaces HOW; a ten-star, safe human learning and connection experience is WHY.

## Decision in one paragraph
Do **not** create a second blog/knowledge store. Make only **specifically approved public** Smart Notes/Intelligent Blocks into canonical, crawlable HTML pages and project their short truthful nutshells as cards into the existing Hub / Intel Today / topic Smart Feeds. Internal search and external crawlers consume the same authorized source facts; their respective indexes and presentation differ. **Never open the full Hub, personal pages or a privileged feed emitter to the public by default.** One note, one authority, one public page, many views.

## Confirmed repo facts (source-grounded)
- At the fresh main snapshot c0ec06ccf6b5e468163089f3f9e8872769c370ea, HUB/FEEDS/emit_hub_feeds.py emits room JSON from a server-side Supabase Management helper that explicitly bypasses RLS. Its existing TODAY source includes intelligence index metadata and Smart Note artifact excerpts, while its Smart Feed query explicitly filters owner_scope != PRIVATE. **Existing TODAY emission is not a safe-by-default permissioned public publication pipeline** merely because its fields are short.
- HUB/nayanet-page-settings.v1.json is marked PROPOSED_NOT_DEPLOYED and distinguishes PRIVATE/PUBLIC page content from UNLISTED/FINDABLE Connect discoverability. Its own governance law says private pages cannot enter full-content public search and a private/findable account may expose at most independently approved alias/topics.
- Existing Intel Today merge brief BRAIN/10-INTERFACES/merge-briefs-2026-10-26/brief-07-intel-today.md describes a FREE top-3-per-day preview and a PAID full view (SN-1862) and assigns Nitro the UI lane. **Making a public preview is not authorization to publish the paid/full corpus.** New public-content policy and current plan must be reconciled before change.
- Existing Smart Note routes, feed cards, registry, privacy scopes and link semantics already exist. This proposal extends their projection; no new database, separate Hub or new Smart Note numbering is authorized.
- The user reports that two agents are working in parallel on public Hub blog/search and public Feed/Messenger. **Their build status and acceptances were not independently confirmed in this audit.** Deconflict before code.

## Observed live HTTP probes — 2026-11-12 (read-only, nayanet.app, Windows HTTP client)
| URL | Observed status and response | Qualification |
| --- | --- | --- |
| / | 200, 620,962-byte HTML titled "NayaNET - Main entrance, variant C..." | A public entrance exists |
| /robots.txt | 200, ~5,012,340-byte HTML titled "NayaNET — The Intelligent Hub" | Not a valid plain-text robots.txt response |
| /sitemap.xml | 200, ~5,012,340-byte HTML titled "NayaNET — The Intelligent Hub" | Not an XML sitemap response |
| /s/sn2696 | 200, 620,962-byte entrance HTML | Not a first-response HTML document containing this note |
These results do not prove every browser journey is broken or that a particular engine has indexed the page. **They do prove the tested endpoints cannot yet satisfy a basic static crawler contract** on those requests. Reprobe with response URL/header/body on the exact live deployment; avoid assuming another domain shares these results.

## Truth about search algorithms
There are **two related discovery concerns, not two secret formulas**:
1. Google/Bing: crawlable URL, permitted indexing, unique original helpful visible content, descriptive title and links, relevant images, appropriate supported structured data, sitemap and performance. Google says AI Overviews/AI Mode use ordinary Search SEO fundamentals and do **not** require special AI files/schema. Google explicitly ignores meta-keywords; snippet text is chosen dynamically and may differ from our description.
2. AI assistants: a retrievable and attributable factual answer with evidence, freshness, clear context, stable links and allowed search crawler access. OpenAI documents OAI-SearchBot for ChatGPT Search; Anthropic documents Claude-SearchBot and Claude-User for its search/user retrieval. Search access and AI-training policies are distinct; do not confuse GPTBot/ClaudeBot with the search crawlers. **No recommendation/citation guarantee** by ChatGPT, Claude, Muse, Bing or Google. Nothing in external documentation proves a Muse-specific public ranking control.
No keyword stuffing, fake topical breadth, changing publication dates to simulate freshness, or endless low-value machine-created pages. Google explicitly warns against scaled content abuse.

## A single governed publish/learn river
AUTHOR/CAPTURE → FILE/REGISTER/VERIFY NOTE → OWNER/COLLECTIVE PUBLICATION REVIEW → PUBLIC_CONTENT_APPROVED → GENERATE CANONICAL PAGE (HTML + images + metadata + permitted schema) → INDEXABLE CHECK → INTEL TODAY NUTSHELL HIGHLIGHT → APPROVED TOPIC SMART FEEDS → SITEMAP/CRAWLER ACCESS → EXTERNAL DISCOVERY → REAL FIRST VALUE → OUTCOME / ATTRIBUTION → LEARN → COLD SUCCESSOR.
- **Important:** Filing or changing a Smart Note triggers an internal candidate highlight immediately; *public* projection triggers only after explicit scope, consent, safety, quality, uniqueness and publication gates.
- The public Intel Today card is an extract/entry point, **not a competing duplicate article**. It links to the note's one canonical HTML permalink. Feed, blog, search and card renderers must point at the same source revision.
- Internal search indexes may include user-authorized private material in a separately enforced tenant scope. External crawlers must receive **only** public-approved bytes.
- Revoke/unpublish immediately removes public manifest entries, feed cards, sitemap, images and caches where under our control, changes serving access to deny/410 where appropriate, and emits removal/recrawl requests where supported. External copies cannot be promised erased.

## One ten-star Intelligent Block example (hypothetical structure)
Public note: "How to save a reusable AI lesson"; nutshell: "Capture a useful lesson once, preserve the evidence, retrieve it on the next task, and verify the improvement." The visible note offers:
- The nutshell in 1–2 sentences (human hook that also defines the topic accurately).
- What/why/who; practical steps and a worked example.
- What was directly proven, dated evidence, caveats and source links.
- Related approved public Smart Notes and topics (real anchor links).
- Relevant, captioned and accessible descriptive image.
- One clear next useful action: "Try this method" rather than forced sign-up.
The same visible words populate a unique page title, a concise meta description (which search engines may rewrite), an accurate Open Graph card, an Article/BlogPosting structured-data object when appropriate, and the Intel Today card. **No hidden contradictory AI-only prose.**

## Priority order (proposed, high to low)
1. **P0 Privacy publication boundary:** audit all feed producers, owner scopes and actual access; deny public until explicitly approved.
2. **P0 Server-served canonical note URL:** get the actual verified public note text in initial HTML; retain one canonical route, real 404/410, and direct deep-link behavior.
3. **P0 Correct /robots.txt and /sitemap.xml on production:** text/plain and valid XML; sitemap enumerates ONLY public-approved URLs.
4. **P0 Preserve existing Free/Paid Intel Today contract:** reconcile top-3/free/full-paid and public digest policy before exposing content.
5. Generate per-note truthful title/description/OG image, author, publish/modified dates, breadcrumbs and contextual links from source.
6. Add source-supported JSON-LD Article/BlogPosting where content genuinely qualifies, and test semantic/visible equality.
7. Add descriptive indexable images, alt text, names, sizes and an image discovery route; never leak private cover images.
8. Link public Hub, Intel Today nutshell highlights, topic feeds and actual note permalink; dedupe, stable IDs, idempotent events.
9. Create lawful crawler configuration and Search Console/Bing reporting; consider IndexNow for participating engines, NOT a Google indexing guarantee.
10. Measure qualified search/AI referral visits, useful learning outcomes, privacy denials, freshness and cold-successor reuse.

## Real proof required
- On the real deployed domain: robots returns 200 text/plain with actual rules; sitemap returns 200 valid XML and no private URLs; public Note GET returns 200 and visible H1/nutshell/body/source in HTML without JS login; unknown/retired note returns genuine 404/410; private Note GET denies body and private metadata to anonymous clients, **even when URL guessed**.
- Search Console URL Inspection and Bing Webmaster Tools validate discovery; AI crawler config and page accessibility are checked without simulating a false referral or inventing ranking.
- Publish/unpublish tests cover all mirrors: public feed, Intel Today, aliases, social cards, sitemap, JSON-LD, image URLs, RSS/exports, CDN cache and internal index.
- Nitro verifies 390px phone and desktop, direct card→note navigation, visual quality, readable image alt and fast load.
- Later proof: one public note is actually fetched/indexed (where observed), a real visitor reaches it, learns/acts and optionally joins; a future Naya reuses the recorded discovery lesson successfully.
- A 10/10 *readiness score* is an internal acceptance rubric, never "the Google algorithm rated us 10/10".

## Ownership / constraints / successors
- **Shawn**: final authority over changing public/private content policies, paid/free lines and deployment.
- **Existing blog/search agent**: current Hub and note serving/crawler technical lane. **Feed/Messenger agent**: authorized public feed projection and linking, without private message exposure.
- **Nitro**: all public Hub, Intel Today, card and mobile UX; preserve existing one Hub.
- **LAW/Security**: classification, RLS, private-by-default, revocation and public projection.
- **Independent verifier**: HTTP crawler proof, visible-content/JSON-LD equality, user journey and privacy attack cases.
- **Integrator**: source/dedup/contract coordination, evidence and quality gates; no competing backend.

**Exact next action:** Assign the existing Hub/blog technical owner to **reproduce and correct the live /robots.txt, /sitemap.xml and /s/<real-public-note> serving contract on staging**, with an independent P0 privacy gate; only after that enable automatic public highlights. Keep this proposal in review; do not merge or deploy without protected checks.

## Official references, verified 2026-11-12
- Google people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google structured Article: https://developers.google.com/search/docs/appearance/structured-data/article
- Google images: https://developers.google.com/search/docs/appearance/google-images
- Google JavaScript SEO: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Google supported metadata: https://developers.google.com/search/docs/crawling-indexing/special-tags
- Google spam policy: https://developers.google.com/search/docs/essentials/spam-policies
- OpenAI publisher crawler: https://help.openai.com/en/articles/12627856-publishers-and-developers-faq
- Anthropic crawlers: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Bing/participating engines IndexNow: https://www.indexnow.org/faq
