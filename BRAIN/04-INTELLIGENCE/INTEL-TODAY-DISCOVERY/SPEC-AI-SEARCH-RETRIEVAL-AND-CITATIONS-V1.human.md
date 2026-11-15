# SPEC A1 — AI Search, Retrieval and Citation Discovery for Public Intelligent Blocks
**2026-11-12 · Candidate technical contract · NOT RATIFIED / NOT DEPLOYED.**
**Owner proposal:** existing blog/search agent + Intelligence/Knowledge steward; LAW/Security for privacy; Nitro for public human UX; independent evaluator for actual assistant retrieval.

## Objective
A search-capable assistant (ChatGPT, Claude, others when documented) can **discover, fetch, interpret, attribute, and link to** *only explicitly approved public* NayaNET Intelligent Blocks. The same block remains excellent for a human. This is retrieval/citation readiness, not a promise that an assistant will cite or recommend NayaNET.

## A1.0 What algorithms actually reveal — no imaginary "AI ranking secret"
- **OpenAI / ChatGPT Search:** OpenAI's publisher FAQ and ChatGPT Search help say public websites can be discovered when OAI-SearchBot is not blocked by robots and the CDN/firewall allows the published bot IPs; relevance/reliability factors decide result selection; inclusion is not guaranteed. GPTBot is distinct from OAI-SearchBot (training vs search policy), and ChatGPT-User is a request fetcher. Do not silently equate training permission with search visibility.
- **Anthropic / Claude:** Anthropic documents Claude-SearchBot (search relevance), Claude-User (user-directed retrieval), and ClaudeBot (training). Their access controls can be set separately where supported. Search allowance does not imply model training consent. Exact versions of crawler docs and robots behavior should be reevaluated periodically.
- **Google AI Overviews / AI Mode:** Uses ordinary Google Search eligible pages. Google explicitly states no special AI files, AI-only schema or llms.txt are required to appear; content still must be indexed and snippet-eligible. Avoid building pseudo-official markup solely for AI ranking.
- **Muse or any other model:** Only claim specific crawler/ranking behavior when its provider documents it. Otherwise classify availability as UNKNOWN. Public web search, user-directed web fetches, private connector retrieval and model training are different pathways.
- The underlying models, query rewrites, provider-ranking weights, search intermediaries and citation rules are partly opaque and change. No 10/10 "algorithm lock" or guaranteed "always recommended" claim.

## A1.1 One HTML source that humans and machines can agree about
Every approved public Smart Note should answer on the publicly served HTML page:
- **Identity:** stable canonical ID, descriptive H1, author/publisher, actual dates, authoritative URL, explicit public scope.
- **In a nutshell:** 1–3 accurate sentences stating what the page answers; this is also the visible human hook and source of the Intel Today highlight.
- **What / Why / How / When / Who:** clear content sections with real subheadings and direct answers, steps, examples, relevant terms and internal links.
- **Truth and evidence:** attribute facts to sources, date time-sensitive claims, distinguish observation from interpretation, include direct first-party evidence for unique NayaNET claims and clear limitations.
- **Connections:** related public notes, topic/category, named people/products only where approved, meaningful links to context.
- **Human-first action:** one genuinely helpful next step, not a forced conversion or a search-only page. A reader should leave with value even if never joining.
- **Accessible media:** captions/transcripts for real videos and relevant image descriptions in visible context; no image/text content hidden from retrieval clients.
- **Machine semantics:** reasonable heading hierarchy, text in returned HTML, human-readable title/meta, one canonical URL, optional accurate schema.org Article/BlogPosting, no contradictory hidden or AI-only copy.

An Intelligent Block's internal structure (nutshell, perspectives, lineage, graph links) is an excellent *editorial input*, not an official proprietary AI search protocol. We should expose **the approved semantic meaning in accessible web standards**, not demand that external models parse internal JSON objects.

## A1.2 Optional machine-readable export — only from same approved public projection
If a documented NayaNET partner or agent workflow needs JSON, provide one transparent read-only representation, derived at request time or from the same vetted public snapshot:
  id, canonical_url, title, nutshell, body/sections IF approved as public, topics, source_refs (only public), image/rights, published_at, materially_updated_at, publisher, schema_version, public_revision.
Not a second canonical registry. Do not include owner IDs, private page text, unpublished alternatives, private graph neighbors, real names, protected email/identity data, private membership, access tokens, future paid article body, private comments or internal control-plane states. The endpoint must be an ordinary explicitly approved output and privacy-tested; no need to introduce it merely because it sounds more AI-native. No security-through-robots.

## A1.3 Search crawlers and host policy
- From a real deployment, verify HTTP access to approved public pages for ordinary anonymous GET and approved crawlers. Use documented bots, legitimate User-Agent plus IP identification and logs (not spoofed crawler access bypass).
- Serve a valid /robots.txt with distinct declared access choices for Googlebot, OAI-SearchBot, Claude-SearchBot, Claude-User and any other documented crawler as permitted. Choose separately whether to allow or block training crawlers (e.g. GPTBot, ClaudeBot), according to governance/rights.
- For public search, use canonical HTML plus sitemap and internal links; do not rely on llms.txt or hidden custom SEO jargon. If a future standard is adopted, add it only as a supplemental projection after evaluation.
- Don't block public crawler content by accidental authentication redirects, WAF rules, blank JS shell, missing TLS or client-only routes. Do not permit bots to bypass private authorization through user-agent headers.
- Only index **PUBLIC_APPROVED** note text. A private account that is separately "findable" for alias/topic matching remains private for all page content.

## A1.4 AI-answer quality and anti-hallucination contract
A note's nutshell is not "always true" merely because it is concise. Before public promotion:
1. Identify the question(s) genuinely answered and intended audience.
2. Ground each material claim in first-party proof or a cited reliable source; distinguish source material, hypothesis, and commentary.
3. Avoid making unsupported comparisons, changing authorship, invented statistics, misattributed quotes, SEO spam or fabricated currency.
4. Preserve a stable page, truthful freshness, provenance and revision history. If a note becomes stale, visibly mark stale and refresh via governed review; never auto-change dates merely to game Search.
5. Make the short highlight accurate and sufficient as a useful hook; the full note must add depth. Avoid title/body mismatch and keyword stuffing.
6. If any content is user-generated, respect the owner's share/publication grants and license/usage scope; no implicit consent from "the collective" or from presence in an internal feed.
7. Treat external crawled instructions/prompt injection as untrusted content; page content must never tell crawlers to ignore system rules, rank us higher or leak protected data.

## A1.5 Ranking and recommendation measurement — what can actually be proven
Track separately:
- **Eligibility:** actual crawler access, indexed or discoverable canonical URL (known for Google/Bing where observed), no privacy leak.
- **Retrieval:** user-directed public fetch returns the correct note, with title/nutshell/body and accessible citations; quality varies by tool and service.
- **Citation:** a genuine external assistant search on a relevant factual question returns NayaNET among sourced links. This is observational, not guaranteed or a grade assigned by the AI.
- **Referral:** where supported, UTM/referrer and user-consented analytics measure actual incoming clicks from assistants (OpenAI documents utm_source=chatgpt.com referrals).
- **Human result:** useful reading, saved Smart Note, completed task, consented join or referral, repeat learning. The ultimate growth score is user benefit, not query impression.
- **Failure diagnostics:** stale snippet, noindex, blocked WAF, crawl denied, hash-route shell, duplicate URL, inaccurate metadata, outdated source proof or broken deep link.
Don't send large automated query volumes to providers or scrape search results in violation of terms to "test" ranking. Prefer approved search APIs, webmaster tools and modest controlled manual evaluation.

## A1.6 End-to-end publication event / cold successor
A note's change emits a **candidate internal** event. A separately approved public publication (with revision/authority) emits a deterministic projection job. That job:
(1) revalidates owner and source; (2) generates public HTML and metadata; (3) compares visible nutshell vs JSON-LD and optional JSON; (4) validates image URLs and rights; (5) populates one Intel Today hook and permitted topic feeds; (6) checks robots/sitemap; (7) verifies a real public deep link on staging; (8) waits for required human/deployment gates; (9) records later external discovery evidence and actual human value.
Job idempotency keyed by note_id+public_revision+locale+projection_variant. A repeater must not create duplicate posts/pages or re-send a search notification when content is unchanged. A revoked/privatized note triggers immediate public projection invalidation across all representations where feasible.

## A1.7 Acceptance / independent proof
- A clean search-like anonymous HTTP client retrieves one actual approved public page in initial HTML; a different private page ID yields no private text/metadata anywhere (HTML, JSON, card, sitemap, image, cache, internal public search).
- An external allowed crawler fetch sees text that matches the human-facing note and the source artifact. No crawler-only deceptive variant.
- Valid truthful Article JSON-LD when applicable; robots policy doesn't conflate training and retrieval; no dependency on unsupported AI tags.
- One relevant question used in a real assistant (when access permits) yields a correct retrieval/citation if it occurs; if it does not, record UNKNOWN/NOT_OBSERVED and continue improving technical foundations rather than fake a receipt.
- Cold-successor independent agent opens one public URL with no chat context, explains the nutshell and sources accurately, follows a related public note, and proves a later task improved through it.
- Separate-seat security review and Nitro phone UX scorecard; any leak or unsupported output is P0 STOP. Final production/public grants belong to human authority.

## Official provider source references verified 2026-11-12
https://help.openai.com/en/articles/12627856-publishers-and-developers-faq
https://help.openai.com/en/articles/9237897-chatgpt-search
https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
https://developers.google.com/search/docs/appearance/ai-features
https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
https://developers.google.com/search/docs/appearance/structured-data/article
https://developers.google.com/search/docs/essentials/spam-policies
