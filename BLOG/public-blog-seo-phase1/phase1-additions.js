// ---- PHASE 1 — public-serving + privacy foundation (2026-11-12) ----
// The smallest canonical routing/serving seam on the live Hub worker
// (HUB/hub-worker.js, main sha 701c2bb8 — byte-identical to the live
// "hub" worker). Three HTTP faults, three handlers, nothing else:
//
//   1. /robots.txt returned Hub HTML (5,011,973 B) — the path is not in
//      run_worker_first (HUB/wrangler.toml, 8 patterns), so the assets
//      layer answered with the SPA fallback before the worker ran, and
//      the worker had no handler for it either.
//   2. /sitemap.xml — the same fault, the same fix.
//   3. /s/<slug> 302s every client (browser AND bot) to the hash route
//      /#/smart-notes/<slug> — a crawler gets the entrance shell, never
//      the note. Browsers KEEP the 302 (Shawn's ruling 2026-11-06/07:
//      notes open IN the Hub). Crawlers get the server-rendered page.
//
// THE EDGE, BY CONSTRUCTION: only the ONE candidate slug below is ever
// served. The allowlist is the privacy enforcement — not robots.txt,
// not noindex, not a human remembering. Anything not allowlisted gets
// a 404 with no body, no metadata, no image, no cache record — never
// the shell, never a redirect that leaks the note's existence.
//
// CANDIDATE STATUS — READ THIS: the slug below is PROPOSED, NOT
// APPROVED. Presence in the internal registry or feed is NOT
// publication permission (Tree's contract: never infer public from
// source_exists / smart_note_filed / in_internal_feed). The captain
// brings this proposal to Shawn; publication to the internet is his
// hand; the live deploy waits for his tap. STAGING ONLY.
//
// CANONICAL URL: /s/sn2696 — the actual deployed route (wrangler
// claims nayanet.app/s/* for this worker). No second article URL is
// minted: /note/, /notes/, /smart-notes/ aliases serve the SAME bytes
// with the SAME canonical. The sitemap lists only the canonical.
//
// WHAT PHASE 1 DOES NOT BUILD (phase 2, separate dispatch): the Hub
// "Intel Today" enhancement, the automatic pipeline, the auto-tagging
// per the dual spec, the back-end SEO score, the optimization loop,
// the landing flow, the /feed and /cluster pages. The note page below
// renders the note's real content with an accurate meta set — it does
// NOT claim dual-spec §2 block-shape conformance (40–60-word nutshell,
// perspectives, connections); that shaping is the phase-2 auto-tagging
// machine's job, measured by its own 5-point pass/fail test.
const PHASE1_CANDIDATE = {
  slug: "sn-2696",
  id: "IB-SMART-NOTE-20261112-the-infinite-smart-feeds",
  sn: "SN-2696",
  displayTitle: "The Infinite Smart Feeds",
  // The title and description tokens below are filled by
  // build-phase1-worker.py from the live feed entry itself, and
  // asserted there (title 50–60 chars, description 120–155 chars,
  // description verbatim from the note's own hook/nutshell).
  title: "__PHASE1_TITLE__",
  description: "__PHASE1_DESCRIPTION__",
  canonicalPath: "/s/sn2696",
  imagePath: "/images/infinite-smart-feeds-cover.png",
  lastmod: "2026-11-12",
  datePublished: "2026-11-12",
  cluster: "System Intelligence",
};

function phase1IsBotUA(ua) {
  return /bot|crawl|spider|slurp|facebookexternalhit|twitterbot|linkedinbot|chatgpt|gptbot|claude|anthropic|perplexity|bingbot|googlebot|duckduckbot|applebot|yandex|baiduspider|sogou|exabot|facebot|ia_archiver|semrush|ahrefs/i.test(ua || "");
}
function phase1IsBrowserUA(ua) {
  return /Mozilla\/\d/.test(ua || "") && !phase1IsBotUA(ua);
}

// robots.txt — the hard gate. Search crawlers are allowed: they are how
// Google and the AIs find and quote the pages. TRAINING crawlers
// (GPTBot, ClaudeBot) are disallowed: training is a separate use from
// search, and blocking training does not remove the pages from search
// answers (dual spec §5.1). /api/ is back-end only, never for crawlers.
// No nosnippet anywhere — it would also block AI Overviews. Privacy is
// enforced server-side by the allowlist below, never by robots.txt.
function phase1RobotsTxt(origin) {
  return "User-agent: Googlebot\nAllow: /\n\n"
    + "User-agent: Bingbot\nAllow: /\n\n"
    + "User-agent: OAI-SearchBot\nAllow: /\n\n"
    + "User-agent: Claude-SearchBot\nAllow: /\n\n"
    + "User-agent: PerplexityBot\nAllow: /\n\n"
    + "User-agent: GPTBot\nDisallow: /\n\n"
    + "User-agent: ClaudeBot\nDisallow: /\n\n"
    + "User-agent: *\nAllow: /\nDisallow: /api/\n\n"
    + "Sitemap: " + origin + "/sitemap.xml\n";
}

// The sitemap lists ONLY approved public URLs: the Hub root and the ONE
// candidate note. No private URLs, no feed URLs (the smart feed is
// public-to-NayaNET, never indexed — the three tiers), no /api/, no
// staging-only paths. Origin-aware: staging proves the mechanism with
// its own origin; the live canonical origin is nayanet.app.
function phase1SitemapXml(origin) {
  const c = PHASE1_CANDIDATE;
  return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + '  <url><loc>' + origin + '/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
    + '  <url><loc>' + origin + c.canonicalPath + '</loc><lastmod>' + c.lastmod + '</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>\n'
    + '</urlset>\n';
}

// The feed is the Hub's own live feed (feed-live.json, served from the
// ASSETS binding — the same bytes the Hub renders). The note page
// renders FROM that feed, so the Intel Today highlight and the Smart
// Feed highlight and the note page are the identical note at the
// identical feed revision, by construction. If the feed is unavailable
// the route answers an honest 503 — never a staged row, never invented
// content.
let PHASE1_FEED_CACHE = null;
async function phase1LoadFeed(request, env) {
  if (PHASE1_FEED_CACHE) return PHASE1_FEED_CACHE;
  try {
    const u = new URL(request.url);
    u.pathname = "/feed-live.json";
    u.search = "";
    // The subrequest is always GET: the feed is data, not the client's
    // request. Forwarding the original request carried HEAD through to
    // the assets binding, which failed it, so a HEAD note request came
    // back 503 "Feed unavailable" (self-check round 2).
    const res = await env.ASSETS.fetch(new Request(u.toString(), { method: "GET" }));
    if (res.ok) { const j = await res.json(); if (j && Array.isArray(j.notes)) { PHASE1_FEED_CACHE = j; return j; } }
  } catch (e) { /* fall through: no feed, no public pages */ }
  return null;
}
function phase1FindNote(feed, rawSlug) {
  if (!feed) return null;
  const slug = String(rawSlug || "").toLowerCase().trim();
  if (!slug) return null;
  for (const n of feed.notes) {
    if (String(n.id || "").toLowerCase() === slug) return n;
  }
  const snM = slug.match(/^sn-?(\d+)$/);
  if (snM) {
    const num = String(parseInt(snM[1], 10));
    for (const n of feed.notes) {
      const t = String(n.title || "").match(/SN-(\d+)/);
      if (t && String(parseInt(t[1], 10)) === num) return n;
    }
  }
  return null;
}

// Parse the feed entry's subtitle into the note's own sections. The
// subtitle carries the note inline as **Label:** paragraphs (the recent
// notes bake this way). Labels that are elaborations of the nutshell
// ("Two views", "The layout", "The difference", "The build") stay WITH
// the nutshell — they are its substance, and dropping them would cut
// the note's heart out (the phase-2 file drops "What changes now";
// this parser keeps it, as the Learning board). The trailing filing
// footer ("*Filed by Intelligence Loop run ...", "*Paired Naya Note:
// ...*") is INTERNAL provenance — run numbers, registry reservations,
// file paths — and is stripped from the public rendering; the rule is
// named here and in the record. Nothing is invented: every rendered
// word is the note's own.
const PHASE1_SECTION_MAP = {
  "nutshell": "nutshell", "human": "human", "child": "child", "grandma": "grandma",
  "naya": "naya", "what it all means": "means", "what it means": "means",
  "why": "why", "how it connects": "connects",
  "what is in it for you": "foryou", "what changes now": "learning",
  "the learning": "learning", "learning": "learning",
};
const PHASE1_NUTSHELL_ELAB = { "two views": 1, "the layout": 1, "the difference": 1, "the build": 1 };
// The nutshell paragraph carries inline **Label:** markers mid-flow
// ("...world. **Two views:** the space's own feed..."). Split them out:
// the elaborations stay in the nutshell (markers kept, so the board
// reads as the note wrote it); "Why" becomes its own board.
function phase1SplitInlineNutshell(body) {
  const INLINE = ["Two views", "The layout", "The difference", "Why", "The build"];
  let tmp = String(body || "");
  for (const L of INLINE) tmp = tmp.split("**" + L + ":**").join("\n\u0000" + L + "\u0001");
  const parts = tmp.split("\n\u0000");
  let nutshell = cleanSectionText(parts[0] || "");
  let why = "";
  for (let i = 1; i < parts.length; i++) {
    const seg = parts[i];
    const cut = seg.indexOf("\u0001");
    const label = cut === -1 ? "" : seg.slice(0, cut);
    const text = cleanSectionText(cut === -1 ? seg : seg.slice(cut + 1));
    if (!text) continue;
    if (label === "Why") { if (!why) why = text; continue; }
    nutshell = (nutshell ? nutshell + "\n\n**" + label + ":** " : "") + text;
  }
  return { nutshell: nutshell, why: why };
}
function phase1ParseSections(subtitle) {
  const paras = String(subtitle || "").split(/\n\s*\n/);
  const secs = {};
  let hook = "";
  for (const p of paras) {
    const t = p.trim();
    if (!t) continue;
    // Internal provenance — never on a public page.
    if (/^\*Filed by Intelligence Loop/.test(t)) continue;
    if (/Paired Naya Note:/.test(t)) continue;
    const m = t.match(/^\*\*([^*]+):\*\*\s*([\s\S]*)$/);
    if (!m) {
      if (!secs.nutshell) secs.nutshell = cleanSectionText(t);
      continue;
    }
    const label = normHead(m[1]);
    const body = cleanSectionText(m[2]);
    if (!body) continue;
    if (label === "hook") { hook = body.replace(/\s+/g, " ").trim(); continue; }
    if (label === "nutshell") {
      const sp = phase1SplitInlineNutshell(body);
      secs.nutshell = sp.nutshell;
      if (sp.why && !secs.why) secs.why = sp.why;
      continue;
    }
    if (PHASE1_NUTSHELL_ELAB[label]) {
      secs.nutshell = (secs.nutshell ? secs.nutshell + "\n\n" : "") + body;
      continue;
    }
    const key = PHASE1_SECTION_MAP[label];
    if (key && !secs[key]) secs[key] = body;
  }
  return { hook: hook, sections: secs };
}

// The findable note page. The body is the base worker's own renderNote
// — harvested verbatim, untouched (its boards, its CSS, its reveal
// script): the note's content in initial HTML. This wrapper only
// replaces the <head> with the accurate meta set (title, description,
// canonical, robots, Open Graph, Twitter, one honest JSON-LD block —
// BlogPosting + BreadcrumbList; NO FAQPage/HowTo, both out of Google's
// search gallery) and inserts the top bar, breadcrumb, byline, and the
// one real cover image. The footer is corrected too: the base footer
// says "live from the registry" — this note is live from the public
// feed, at the feed revision named below.
const PHASE1_EXTRA_CSS = '<style>'
  + '.topbar{max-width:760px;margin:0 auto;padding:22px 20px 0;display:flex;flex-wrap:wrap;gap:10px;align-items:center}'
  + '.topbar .mark{color:#ffbf3d;font-weight:900;letter-spacing:.04em;font-size:18px;text-decoration:none}'
  + '.topbar a.btn{display:inline-block;border:1.5px solid rgba(248,247,251,.9);border-radius:999px;padding:9px 18px;font-size:13px;font-weight:800;letter-spacing:.06em;text-decoration:none;color:#fff;background:linear-gradient(180deg,#1a1a22 0%,#0a0a0f 45%,#050507 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 0 24px rgba(248,247,251,.25),0 12px 32px rgba(0,0,0,.65)}'
  + '.topbar a.btn:hover{border-color:#a06bff;box-shadow:0 0 22px rgba(160,107,255,.55),inset 0 0 0 1.5px rgba(160,107,255,.8)}'
  + '.crumbs{font-size:13px;letter-spacing:.05em;opacity:.65;margin:0 0 14px}'
  + '.crumbs a{color:#fff;text-decoration:none}'
  + '.byline{font-size:14px;letter-spacing:.04em;opacity:.75;margin:0 0 18px}'
  + '.byline a{color:#ffbf3d;text-decoration:none}'
  + 'figure.cover{margin:0 0 22px}'
  + 'figure.cover img{width:100%;max-width:512px;height:auto;border-radius:18px;border:2px solid rgba(255,255,255,.25);display:block}'
  + 'figure.cover figcaption{font-size:13px;opacity:.6;margin-top:8px}'
  // The footer names the full feed revision (a 64-char unbroken hash)
  // — it must wrap, or it overflows phone widths (caught by the
  // Playwright probe at 390/360: overflowX 80/110).
  + 'footer{overflow-wrap:break-word}'
  + '</style>';
function renderPhase1Note(rec, note, origin, feedRev) {
  const c = PHASE1_CANDIDATE;
  const canonical = origin + c.canonicalPath;
  const imageUrl = origin + c.imagePath;
  const dateStr = String(note.created || "").slice(0, 10) || c.datePublished;
  const jsonLd = JSON.stringify({
    "@context": "https://schema.org",
    "@graph": [
      { "@type": "BlogPosting", headline: c.displayTitle, description: c.description, image: imageUrl,
        datePublished: dateStr, dateModified: dateStr,
        author: { "@type": "Person", name: "Naya", url: origin + "/" },
        publisher: { "@type": "Organization", name: "NayaNET", url: origin },
        articleSection: c.cluster, mainEntityOfPage: canonical, inLanguage: "en" },
      { "@type": "BreadcrumbList", itemListElement: [
        { "@type": "ListItem", position: 1, name: "Intel Today", item: origin + "/" },
        { "@type": "ListItem", position: 2, name: c.displayTitle, item: canonical },
      ] },
    ],
  });
  const baseHtml = renderNote(rec);
  const styleM = baseHtml.match(/<style>[\s\S]*?<\/style>/);
  const baseStyle = styleM ? styleM[0] : "";
  const head = '<meta charset="UTF-8">\n'
    + '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    + '<title>' + esc(c.title) + '</title>\n'
    + '<meta name="description" content="' + esc(c.description) + '">\n'
    + '<meta name="robots" content="index, follow">\n'
    + '<link rel="canonical" href="' + esc(canonical) + '">\n'
    + '<meta property="og:type" content="article">\n'
    + '<meta property="og:title" content="' + esc(c.title) + '">\n'
    + '<meta property="og:description" content="' + esc(c.description) + '">\n'
    + '<meta property="og:url" content="' + esc(canonical) + '">\n'
    + '<meta property="og:site_name" content="NayaNET">\n'
    + '<meta property="og:image" content="' + esc(imageUrl) + '">\n'
    + '<meta name="twitter:card" content="summary_large_image">\n'
    + '<meta name="twitter:title" content="' + esc(c.title) + '">\n'
    + '<meta name="twitter:description" content="' + esc(c.description) + '">\n'
    + '<meta name="twitter:image" content="' + esc(imageUrl) + '">\n'
    + '<script type="application/ld+json">' + jsonLd + '<\/script>\n'
    + baseStyle + "\n" + PHASE1_EXTRA_CSS;
  let html = baseHtml.replace(/<head>[\s\S]*?<\/head>/, "<head>" + head + "</head>");
  const topbar = '<div class="topbar"><a class="mark" href="/">Intel Today</a>'
    + '<a class="btn" href="/">Hub</a>'
    + '<a class="btn" href="/#/smart-notes/' + esc(c.slug) + '">Open in the Hub \u2192</a></div>';
  const crumbs = '<nav class="crumbs"><a href="/">Intel Today</a> \u203a <span>' + esc(c.cluster) + '</span> \u203a <span>' + esc(c.displayTitle) + '</span></nav>';
  if (html.indexOf("<main>") !== -1) html = html.replace("<main>", "<main>" + topbar + crumbs);
  const byline = '<p class="byline">By <a href="/">Naya</a> \u00b7 Published <time datetime="' + esc(dateStr) + '">' + esc(dateStr) + '</time> \u00b7 ' + esc(c.cluster) + '</p>';
  const cover = '<figure class="cover"><img src="' + esc(c.imagePath) + '" alt="NayaNET \u2014 the intelligent layer of the internet" width="512" height="512"><figcaption>NayaNET \u00b7 the intelligent layer of the internet \u2014 the mark of the network this note describes. A real image of the feeds themselves is owed (Shawn / a Naya makes it); this cover slot is the deliverable until then.</figcaption></figure>';
  const h1Close = html.indexOf("</h1>");
  if (h1Close !== -1) html = html.slice(0, h1Close + 5) + byline + cover + html.slice(h1Close + 5);
  const oldFooter = "<footer>Smart Note " + esc(rec.id) + " \u00b7 NayaNET \u2014 the collective intelligence, live from the registry.</footer>";
  const newFooter = "<footer>Smart Note " + esc(rec.id) + " \u00b7 Intel Today \u00b7 NayaNET \u2014 the highlight is the note\u2019s own nutshell; served from the public feed, revision " + esc(feedRev) + ".</footer>";
  if (html.indexOf(oldFooter) !== -1) html = html.replace(oldFooter, newFooter);
  return html;
}

// Serve the candidate note to a crawler. The allowlist check runs
// FIRST, before any feed read: an unlisted slug never reaches the feed,
// never reaches a renderer, never leaks a byte.
// Normalize a raw slug to its canonical allowlist form: "sn2696",
// "sn-2696", "SN-2696" are the same note (the live route is /s/sn2696,
// no hyphen; the canonical id is SN-2696). The allowlist holds the
// canonical form; every comparison is normalized first — a raw-string
// comparison would deny the candidate itself.
function phase1CanonicalSlug(rawSlug) {
  const s = String(rawSlug || "").toLowerCase().trim();
  const m = s.match(/^sn-?(\d+)$/);
  if (m) return "sn-" + String(parseInt(m[1], 10));
  return s;
}
async function phase1ServeNote(request, env, slug, origin) {
  const c = PHASE1_CANDIDATE;
  const denied = new Response("Note not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
  if (phase1CanonicalSlug(slug) !== c.slug) return denied;
  const feed = await phase1LoadFeed(request, env);
  if (!feed) return new Response("Feed unavailable", { status: 503, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store" } });
  const note = phase1FindNote(feed, slug);
  if (!note || note.personal) return denied;
  const parsed = phase1ParseSections(String(note.subtitle || ""));
  if (!parsed.sections.nutshell) return denied;
  const rec = { id: c.sn, title: c.displayTitle, oneLine: parsed.hook, sections: parsed.sections, superseded: null };
  const html = renderPhase1Note(rec, note, origin, String(feed.generated_from || ""));
  return new Response(html, { status: 200, headers: { "Content-Type": "text/html;charset=UTF-8", "Cache-Control": "public, max-age=3600", "X-Robots-Tag": "index, follow" } });
}

// The cover image, served under its descriptive filename. The bytes are
// the real public NayaNET mark (the Hub's icon-512.png asset); the
// address is the descriptive name the image rules ask for. The alt text
// and caption say truthfully what it is: the network's mark, not a
// picture of the feeds. A real note-specific image is owed.
async function phase1CoverImage(request, env) {
  const u = new URL(request.url);
  u.pathname = "/icon-512.png";
  u.search = "";
  // Always a GET subrequest (same HEAD lesson as the feed load above).
  const res = await env.ASSETS.fetch(new Request(u.toString(), { method: "GET" }));
  if (!res.ok) return new Response("Cover unavailable", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
  const h = new Headers(res.headers);
  h.set("Content-Type", "image/png");
  h.set("Cache-Control", "public, max-age=86400");
  return new Response(res.body, { status: 200, headers: h });
}
