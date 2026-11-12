# SPEC G1 — Google and Classical Search Discovery for Public Intelligent Blocks
**2026-11-12 · Candidate technical contract · NOT IMPLEMENTED or RATIFIED.**
**Owner proposal:** existing Hub/blog technical builder + Nitro for UI, independent Search/LAW verifier. This document extends current Hub and Smart Note serving; it does not create a new app or database.

## Objective and promise
For every *explicitly approved public* note, a real anonymous visitor and ordinary crawl client can retrieve an accurate, useful, accessible canonical HTML page. Google, Bing and image crawlers can discover, understand and potentially index it. **We cannot control Search's final ranking, selection, snippets or AI summaries.** Quality is measured by compliance + real outcomes, not the volume of keywords.

## G1.0 Mandatory security and source predicates — FAIL CLOSED
Required simultaneously: (a) immutable canonical Smart Note ID + current public-approved content revision; (b) owner/collective explicit PUBLIC decision and rights to text/images; (c) no private/paid full text leaking through highlights, alt text, metadata, schema, image previews, feeds, sitemaps or caches; (d) legitimate creator/source credit; (e) no deletion/revocation or pending moderation; (f) source-generated outputs compare to the same revision. A PRIVATE/FINDABLE alias/topic projection is **not** full-content authorization (see HUB/nayanet-page-settings.v1.json). "Public page" and "included in external search" are separate choices.
**Never use robots.txt, noindex or obfuscated links as a privacy barrier; enforce authorization server-side and at any storage/cache edge.**

## G1.1 URLs, web delivery and discoverability
- Choose one canonical public Smart Note URL from the *actual deployed* route (e.g. previously documented /s/sn####), preserving IDs and redirecting duplicate aliases; don't mint a second article at /notes/<slug> and /s/<id> with conflicting canonical links.
- For a valid public page, HTTP 200 text/html; in the **initial response** render the real article H1/title, nutshell, substantial useful body, source/author, published date, relevant internal links and images. Avoid generic JS-only shell or fragment-only navigation; enhance interactive experience after useful HTML.
- Valid public Intel Today summary URL gets its own crawlable public index page, but does not duplicate entire notes; the card uses an ordinary <a href> to the canonical article, not only an onclick or "#/..." hash route.
- Unknown/retired/unpublished document returns correct 404/410 or access denial, never HTTP 200 with a generic entrance that looks like a note. Member-only content is auth-guarded on every transport.
- Mobile speed and accessibility matter: responsive readable text, semantic headings, keyboard links and image alternative text.

## G1.2 Page title, snippet, social card and structured data
From the approved note source, emit:
- Unique concise <title> and visible H1 that say what the note actually teaches. Clear primary user intent, no repeated keyword strings, no false "2026" freshness claim.
- High-quality unique <meta name="description"> summarizing real content; **Google may select a different query-specific snippet**, so the visible nutshell is essential. Do not spend engineering effort on <meta name="keywords">: Google ignores it.
- One rel=canonical URL, correct robots meta for the approved public state, page language and useful internal anchors.
- Open Graph title/description/representative image and image dimensions so permitted social previews look good. OG controls social preview candidates, not Google's ranking.
- Where content is truly an article, Google-supported schema.org Article/BlogPosting JSON-LD with headline, author (person or organization with actual attribution), datePublished, dateModified **only if materially updated**, image URLs, mainEntityOfPage, and publisher/site where applicable. Structured fields must match the visible content. Avoid fabricated FAQ/Review/HowTo claims and avoid treating any structured-data type as a guarantee of rich results. If a note is not an article, do not mislabel it.
- Validate structured data via Google's Rich Results Test and the fetched HTML; strict escaping of source text to avoid HTML/script injection.

## G1.3 Google Image discovery
- Use visible <img src="https://..."> or valid <picture> sources for relevant images; not CSS-only background art for images that need indexing.
- Use stable descriptive lower-case hyphenated filenames, e.g. "smart-note-ai-learning-loop-diagram.webp"; truthful caption and alt text that describes the image rather than stuffing keywords.
- Generate suitable responsive sizes, width/height, lazy-loading for noncritical content, compressed high-quality sources, HTTPS accessible images and rights/licensing attribution.
- When there is a real cover/share image, provide a stable high-resolution representative image (potentially 1:1, 4:3 and 16:9 forms as needed) and use proper Article image and Open Graph references. Avoid embedding private author names or private note fragments.
- Include image URLs in a sitemap extension when useful. Image indexing can happen independently of the page's search appearance but is not guaranteed.

## G1.4 Sitemaps / robots / discovery notifications
- /robots.txt MUST return HTTP 200 "text/plain" and valid robots rules. It is a *crawler-access control*, not authentication.
- /sitemap.xml MUST return HTTP 200 application/xml (or suitable XML type), valid UTF-8 XML with only permitted canonical public URLs, an accurate <lastmod> for material content revisions, and optional image/video extensions where actually supported.
- No private note URLs, app account routes, member lists, privileged feeds, message URLs, staging sites or unapproved public pages in public sitemaps. Keep list idempotent under retries.
- Register property and sitemap through Google Search Console, inspect actual rendered page with URL Inspection. For Bing/participating engines, consider IndexNow URL update notifications with a verified ownership key, rate limits and only publicly changed URLs. **IndexNow is not a Google instant-indexing API.**
- Distinguish Googlebot access from AI search crawlers and AI training crawlers; only allow on the public projection under the chosen policy. CDN/WAF must admit documented bot traffic where permitted.

## G1.5 Content quality, internal tags and daily cadence
A note should publish because it provides original useful value, not because it exists or a cron job ran. It needs a clear question/topic, accurate nutshell, actionable substance, attributable evidence, appropriate freshness, original example or insight, known limits and contextual links. Internal categories/Smart Tabs are taxonomy aids. Social hashtags are channel packaging, **not a Google ranking method**. Refrain from pages generated at scale solely to attract traffic; Google classifies scaled low-value content as abuse. Once quality/permission pass, auto-generation, scheduled posts and refreshes are fine.
- An Intel Today card is a **short hook + source title + topic + approved image + source permalink + published timestamp**, never a second HTML article cloning the entire note.
- Prefer a stable hierarchy: homepage/public Hub → topic feed → Intel Today → canonical note → related notes, all with real hyperlinks; use breadcrumbs where meaningful.
- Reconcile the existing FREE top-three vs PAID full Intel Today entitlement before publishing or indexing a paid section.

## G1.6 Tests and exact acceptance
1. GET /robots.txt: 200, text/plain, non-HTML body. GET /sitemap.xml: 200, parseable XML, approved-public URLs only.
2. GET one actual approved public note: 200, unique title + H1 + nutshell + real body in first HTML; text visible without login/JavaScript. Anonymous GET one private note: no page body, no metadata, no image assets, no cache record.
3. A generated highlight card and Search page reference the identical public source ID/revision and canonical href. No duplicate canonical conflicts, broken clicks, infinite loops or fake 200 fallbacks.
4. Meta/JSON-LD/alt text fields match the rendered public source. Rich Results Test and Google URL Inspection show the intended content. Broken/missing values stop publishing rather than hallucinate metadata.
5. Updating a public note revises its public HTML/card/image/sitemap lastmod only after new approval; revoking removes it from all public projections and invalidates caches as far as controlled.
6. Phone 390px + desktop visual interaction, accessibility and speed pass independent review; future real Google/Bing index observations are tracked honestly as asynchronous OUTCOME, not immediate PASS.
7. Separate-seat privacy verifier attempts forged/private note IDs, feed queries and sitemap discovery. Any leak = P0 STOP.
8. Content production outcome: measured search impressions/visits and qualified useful learning, not "number of published Smart Notes".

## Current starting condition
Read-only live probe on nayanet.app (2026-11-12): /robots.txt and /sitemap.xml returned Hub HTML, not expected text/XML; /s/sn2696 returned entrance HTML, not note content in initial response. Diagnose active routing, worker fallback and actual deployed domain before changing source. No production alteration is authorized by this spec.

## Official sources
https://developers.google.com/search/docs/fundamentals/creating-helpful-content
https://developers.google.com/search/docs/appearance/ai-features
https://developers.google.com/search/docs/appearance/snippet
https://developers.google.com/search/docs/appearance/structured-data/article
https://developers.google.com/search/docs/appearance/google-images
https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
https://developers.google.com/search/docs/crawling-indexing/special-tags
https://developers.google.com/search/docs/essentials/spam-policies
https://developers.google.com/search/docs/crawling-indexing/robots/intro
https://www.indexnow.org/faq
