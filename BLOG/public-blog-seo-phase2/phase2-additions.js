// ---- PHASE 2 — the machine's language + the highlight chain + the net (2026-11-13) ----
// Generalizes the phase-1 machine from ONE candidate note to EVERY note
// in the feed. Phase-1 additions are FROZEN (the proven seam); this file
// is the new seam, composed after it by build-phase2-worker.py.
//   base (hub-worker-harvested-main.js)
//   + phase1-additions.js (robots, 2-URL sitemap, ONE candidate, denial)
//   + phase2-additions.js (THIS file: every note, full sitemap, net)
//   + phase-2 routes (inserted before the phase-1 routes block)
//
// THE EDGE, BY CONSTRUCTION: a note is served publicly only if (1) it is
// in the feed, (2) personal is falsy (the phase-1 truthiness gate, kept
// verbatim — 2 notes carry personal:null and pass it exactly as phase 1
// passed them; see the record), (3) it carries renderable content
// (a nutshell resolves from its subtitle or its layers — a note with no
// resolvable nutshell is denied, never rendered half-empty). Denial is
// one identical 404 for unknown / personal / unservable slugs — no
// oracle, no leaked byte. On STAGING the allowlist is the full feed
// (1,058 notes). On LIVE it is Shawn's approvals only, starting with
// SN-2696 — this round never writes a live allowlist entry.
//
// CONTENT MODEL (first-hand from the feed, revision
// registry@37c542f6f1525de29ed31e04ce7d06f01112065ad4fd48ccb17bc70d3e6f7ea7):
// - 66 notes carry **Hook:**/**Nutshell:** labels in the subtitle
//   (the phase-1 parse path, harvested verbatim).
// - 801 notes carry plain-prose subtitles; 186 carry other labels.
// - 5 notes (2026-11-13) carry an EMPTY subtitle — but their layers[]
//   carry the whole labeled text in a 'human' layer body.
// - 1,057 of 1,058 notes carry layers[] (structured sections).
// So the resolver tries, in order: subtitle parse -> layer-body parse
// -> layer-key sections -> plain-prose first paragraph. Nothing is
// invented: every rendered word is the note's own (subtitle or layers).
//
// TITLE / DESCRIPTION are MACHINE-GENERATED from the note's own words
// (never retyped, never invented): the title is the note's display
// title + NayaNET, extended with the note's own nutshell/topic words
// only until it lands in 50-60 chars; the description is the note's own
// sentences in order (hook, nutshell, why, means, ...) accumulated to
// 120-155 chars. The score report names every note where the machine
// cannot land in range — the machine never invents words to fill it.
//
// THE SCORE (back-end only, never public, never on the page): the
// 5-point test — (1) nutshell 40-60 words, (2) title 50-60 chars,
// (3) description 120-155 chars, (4) JSON-LD valid + exactly one
// canonical, (5) cluster + related links present. Point 1 is a property
// of the NOTE, not the meta: the machine does not rewrite nutshells, so
// a note whose nutshell is not 40-60 words scores 4/5 at best and is
// named in the score report. That is the honest result (see record).
//
// THE NET: related notes come ONLY from the system's own grouping —
// (a) shared topics, (b) shared Smart Lists (the build-time list index
// below, read from the live store at build time), (c) shared cluster.
// Each related link shows WHY (same topic / same list / same cluster).
// Auto-Match is NEVER a source: it scores PEOPLE, never notes.
//
// THE LIST INDEX below is a BUILD-TIME snapshot of the live store
// (public.smart_lists + public.smart_list_items, item_kind smart_note).
// At build time the live store held ZERO smart_note items in 12 live
// lists, so the index carries the round's clearly-test-titled list
// (removed after proof — the final deploy carries the re-read index).

// ---- Clusters: harvested VERBATIM from the staged Hub shell ----
// (hub-shell-bars-20261113/index-intel-today.html, INTEL_CLUSTERS +
// intelClusterOf — the Hub's own smart-tab categories. The shell is the
// authority; this copy must match it byte for byte in keys + weights.)
const PHASE2_CLUSTERS = [
  { slug: 'intelligent-internet', label: 'The Intelligent Internet', color: '#55b9ee', keys: ['intelligent internet', 'new internet', 'intelligent layer', 'new net', 'intelligent net', 'civilization', 'portal', 'the new net'] },
  { slug: 'ai-is-hiring', label: 'AI Is Hiring', color: '#ffbf3d', keys: ['ai is hiring', 'hiring', 'taking jobs', 'jobs', 'get paid', 'earn', 'earning', 'revenue', 'pay your bills', 'pay their bills', 'money to pay'] },
  { slug: 'nayanet-naya', label: 'NayaNET / Naya', color: '#9d75ff', keys: ['she is anaya', 'naya means', 'wise one', 'narzan', 'anaya'] },
  { slug: 'smart-notes', label: 'Smart Notes / Learn in a Minute', color: '#55e39a', keys: ['learn in a minute', 'learn anything', 'in about a minute', 'intelligent block', 'nutshell', 'smart note'] },
  { slug: 'private-network', label: 'The Private Network / Your Vault', color: '#6675ff', keys: ['private network', 'your vault', "we don't sell your data", "don't sell your data", 'no ads', 'not reading your mail', "don't read your mail", 'private secure vault', 'privacy', 'deleted by default', 'deletion by default', 'secure vault'] },
  { slug: 'ambassador', label: 'Ambassador', color: '#ff9a5a', keys: ['ambassador', 'invite the world', 'paid every wednesday', 'every wednesday', 'invite people', 'affiliate'] },
];
function phase2ClusterOf(note) {
  const hay = (((note.topics || []).join(' ')) + ' ' + (note.title || '') + ' ' + String(note.subtitle || '').slice(0, 1200)).toLowerCase();
  let best = null, bestScore = 0;
  for (const c of PHASE2_CLUSTERS) {
    let s = 0;
    for (const k of c.keys) { if (hay.indexOf(k) !== -1) s += (k.length > 12 ? 3 : (k.indexOf(' ') !== -1 ? 2 : 1)); }
    if (s > bestScore) { bestScore = s; best = c.slug; }
  }
  return best || 'nayanet-naya';
}
function phase2ClusterLabel(slug) {
  for (const c of PHASE2_CLUSTERS) if (c.slug === slug) return c.label;
  return 'NayaNET / Naya';
}
function phase2ClusterColor(slug) {
  for (const c of PHASE2_CLUSTERS) if (c.slug === slug) return c.color;
  return '#9d75ff';
}

// The Smart Lists snapshot (build-time; token filled by
// build-phase2-worker.py from a live store read):
// { "<note id lowercased>": [{ "listId": "...", "listTitle": "..." }] }
const PHASE2_LIST_INDEX = __PHASE2_LIST_INDEX__;

// ---- Small text helpers (mirrors of the Python build script) ----
function phase2StripMd(t) {
  return String(t || "").replace(/[*_`#>\[\]()!]/g, " ").replace(/\s+/g, " ").trim();
}
function phase2FirstSentence(s) {
  const flat = String(s || "").replace(/\s+/g, " ").trim();
  if (!flat) return "";
  const m = flat.match(/^.*?[.!?](?=\s|$)/);
  return m ? m[0] : flat;
}
function phase2Sentences(txt) {
  const flat = String(txt || "").replace(/\s+/g, " ").trim();
  if (!flat) return [];
  const parts = flat.match(/[^.!?]+[.!?]+["']?|[^.!?]+$/g) || [];
  return parts.map(function (s) { return s.trim(); }).filter(Boolean);
}
function phase2TrimWords(s, max) {
  s = String(s || "").trim();
  if (s.length <= max) return s;
  const cut = s.slice(0, max);
  const sp = cut.lastIndexOf(" ");
  const head = (sp > 20 ? cut.slice(0, sp) : cut).replace(/[,;:\u2014\u2013-]+$/, "").trim();
  return head;
}
function phase2TitleCase(s) {
  return String(s || "").split("-").filter(Boolean).map(function (w) {
    return w.charAt(0).toUpperCase() + w.slice(1);
  }).join(" ");
}

// ---- Display title: the note's own id slug, title-cased ----
function phase2DisplayTitle(note) {
  const id = String(note.id || "");
  const t = String(note.title || "").trim();
  // The two odd ids whose title field IS the display title.
  if (/^WELCOME TO NAYA$/i.test(t)) return "Welcome To Naya";
  if (/^THE WISE ONE$/i.test(t)) return "The Wise One";
  let m = id.match(/^(?:IB-SMART-NOTE|NN)-\d{8}-(.+)$/);
  if (m) return phase2TitleCase(m[1]);
  m = id.match(/^IB-SMART-NOTE-SMART-NOTE-\d{8}-sn\d+-(.+)$/i);
  if (m) return phase2TitleCase(m[1]);
  // Odd ids: strip a trailing date, title-case what is left.
  const core = id.replace(/-\d{4}-\d{2}-\d{2}$/, "").replace(/-/g, " ").trim();
  if (core) return core.split(/\s+/).map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase(); }).join(" ");
  // Last resort: the title field with its SN prefix stripped.
  const tm = t.replace(/^SN-\d+\s*[·•]\s*/i, "").trim();
  return tm || "Untitled Note";
}
function phase2SnLabel(note) {
  const m = String(note.title || "").match(/SN-(\d+)/);
  if (m) return "SN-" + String(parseInt(m[1], 10));
  const m2 = String(note.id || "").match(/sn(\d+)/i);
  if (m2) return "SN-" + String(parseInt(m2[1], 10));
  return String(note.id || "note");
}
function phase2CanonicalSlug(note) {
  const id = String(note.id || "").toLowerCase();
  const m = id.match(/sn-?(\d+)/);
  // Prefer the SN form (the live route is /s/sn2696, no hyphen).
  const snM = String(note.title || "").match(/SN-(\d+)/);
  if (snM) return "sn" + String(parseInt(snM[1], 10));
  if (m) return "sn" + String(parseInt(m[1], 10));
  return id;
}
function phase2CanonicalSlugForRaw(rawSlug) {
  const s = String(rawSlug || "").toLowerCase().trim();
  const m = s.match(/^sn-?(\d+)$/);
  if (m) return "sn" + String(parseInt(m[1], 10));
  return s;
}

// ---- Content resolution: subtitle parse, then layers, then prose ----
const PHASE2_LAYER_MAP = {
  "nutshell": "nutshell", "in a nutshell": "nutshell",
  "human": "human", "human note": "human",
  "child": "child", "child note": "child",
  "grandma": "grandma", "grandma note": "grandma",
  "naya": "naya", "naya note": "naya",
  "meaning": "means", "what it means": "means", "what it all means": "means",
  "why-it-matters": "why", "why it matters": "why",
  "how-it-connects": "connects", "how it connects": "connects",
  "whats-in-it-for-you": "foryou", "what is in it for you": "foryou",
  "what's in it for you": "foryou",
  "the-learning": "learning", "the learning": "learning", "learning": "learning",
};
function phase2ParseContent(note) {
  const parsed = phase1ParseSections(String(note.subtitle || ""));
  let hook = parsed.hook || "";
  const sections = Object.assign({}, parsed.sections);
  const layers = Array.isArray(note.layers) ? note.layers : [];
  // Layer bodies can carry the whole labeled text (the 5 empty-subtitle
  // notes file it under a 'human' layer). Parse each body the same way;
  // first wins per section, so the subtitle stays authoritative.
  for (const L of layers) {
    const body = String((L && L.body) || "");
    if (!body.trim()) continue;
    const p = phase1ParseSections(body);
    if (!hook && p.hook) hook = p.hook;
    for (const k of Object.keys(p.sections)) {
      if (!sections[k]) sections[k] = p.sections[k];
    }
  }
  // Layer-key sections for bodies that carry no **Label:** paragraphs.
  for (const L of layers) {
    const key = PHASE2_LAYER_MAP[normHead(String((L && L.key) || (L && L.name) || ""))];
    if (key && !sections[key]) {
      const body = cleanSectionText(String((L && L.body) || ""));
      if (body) sections[key] = body;
    }
    if (!hook && normHead(String((L && L.key) || "")) === "hook") {
      hook = cleanSectionText(String((L && L.body) || "")).replace(/\s+/g, " ").trim();
    }
  }
  // Plain prose: the first paragraph IS the nutshell.
  if (!sections.nutshell) {
    const first = cleanSectionText(String(note.subtitle || "").split(/\n\s*\n/)[0] || "");
    if (first) sections.nutshell = first;
  }
  if (!sections.nutshell) {
    for (const L of layers) {
      const body = cleanSectionText(String((L && L.body) || ""));
      if (body) { sections.nutshell = body.split(/\n\s*\n/)[0]; break; }
    }
  }
  return { hook: hook, sections: sections, servable: !!sections.nutshell };
}

// ---- Title: display + brand, extended ONLY with the note's own words ----
function phase2Title(note, content) {
  const SUF = " \u00b7 NayaNET"; // 11 chars; head budget 39..49
  const display = phase2DisplayTitle(note);
  let head = display;
  if (head.length > 49) head = phase2TrimWords(head, 49);
  if (head.length < 39) {
    const nutFirst = phase2FirstSentence(phase2StripMd(content.sections.nutshell || ""));
    if (nutFirst) head = phase2TrimWords(head + " \u2014 " + nutFirst, 49);
  }
  if (head.length < 39) {
    const topics = note.topics || [];
    if (topics.length) head = phase2TrimWords(head + " \u2014 " + String(topics[0]), 49);
  }
  if (head.length < 39) head = phase2TrimWords(head + " \u2014 smart note", 49);
  return head + SUF;
}

// ---- Description: the note's own sentences, in order, to 120-155 ----
function phase2Description(note, content) {
  const order = ["hook", "nutshell", "why", "means", "connects", "foryou", "learning", "human", "child", "grandma", "naya"];
  const seen = {};
  const sents = [];
  const pushFirst = function (text) {
    const s = phase2FirstSentence(phase2StripMd(text || ""));
    if (s && !seen[s]) { seen[s] = 1; sents.push(s); }
  };
  pushFirst(content.hook);
  for (const k of order.slice(1)) pushFirst(content.sections[k]);
  // A second sentence from the nutshell if the first ones are short.
  const nutSents = phase2Sentences(phase2StripMd(content.sections.nutshell || ""));
  for (const s of nutSents.slice(1, 3)) { if (!seen[s]) { seen[s] = 1; sents.push(s); } }
  let desc = "";
  for (const s of sents) {
    const next = desc ? desc + " " + s : s;
    if (next.length > 155) break;
    desc = next;
    if (desc.length >= 120) break;
  }
  if (desc.length >= 120) return desc;
  // Word-boundary trim of the accumulated sentences + the next one.
  let acc = desc;
  for (const s of sents) {
    if (acc.indexOf(s) !== -1) continue;
    const next = acc ? acc + " " + s : s;
    if (next.length <= 155) { acc = next; continue; }
    const cut = next.slice(0, 154);
    const sp = cut.lastIndexOf(" ");
    acc = (sp > 100 ? cut.slice(0, sp) : cut).trim() + "\u2026";
    break;
  }
  return acc;
}

// ---- The back-end SEO score: the 5-point test, per note ----
function phase2SeoScore(note, content, meta, relatedCount) {
  const nutWords = content.sections.nutshell
    ? content.sections.nutshell.replace(/\s+/g, " ").trim().split(" ").filter(Boolean).length : 0;
  const p1 = nutWords >= 40 && nutWords <= 60;
  const p2 = meta.title.length >= 50 && meta.title.length <= 60;
  const p3 = meta.description.length >= 120 && meta.description.length <= 155;
  const p4 = !!(meta.title && meta.description && meta.canonicalPath); // JSON-LD valid + one canonical, by construction
  const p5 = !!(meta.cluster && relatedCount >= 3);
  const fails = [];
  if (!p1) fails.push("nutshell:" + nutWords + "w");
  if (!p2) fails.push("title:" + meta.title.length + "c");
  if (!p3) fails.push("description:" + meta.description.length + "c");
  if (!p4) fails.push("jsonld/canonical");
  if (!p5) fails.push("cluster/related:" + relatedCount);
  return { score: (p1 ? 1 : 0) + (p2 ? 1 : 0) + (p3 ? 1 : 0) + (p4 ? 1 : 0) + (p5 ? 1 : 0),
    nutWords: nutWords, points: { nutshell: p1, title: p2, description: p3, jsonld: p4, cluster: p5 }, fails: fails };
}

// ---- Related notes: the system's own grouping ONLY ----
function phase2Related(note, feed) {
  const cluster = phase2ClusterOf(note);
  const topics = note.topics || [];
  const myId = String(note.id || "").toLowerCase();
  const listHere = PHASE2_LIST_INDEX[myId] || [];
  const byId = {};
  for (const n of feed.notes) byId[String(n.id || "").toLowerCase()] = n;
  const seen = {};
  const out = [];
  const push = function (n, reason) {
    const id = String(n.id || "").toLowerCase();
    if (!n || id === myId || seen[id] || out.length >= 6) return;
    seen[id] = 1;
    out.push({ slug: phase2CanonicalSlug(n), title: phase2DisplayTitle(n), reason: reason });
  };
  // (a) shared topics — most recent first (created desc, feed order kept
  // inside equal dates by the feed's own order).
  const topicNotes = feed.notes.filter(function (n) {
    if (String(n.id || "").toLowerCase() === myId) return false;
    const ts = n.topics || [];
    return topics.some(function (t) { return ts.indexOf(t) !== -1; });
  });
  topicNotes.sort(function (a, b) { const x = String(a.created || ""), y = String(b.created || ""); return x === y ? 0 : (x < y ? 1 : -1); });
  for (const n of topicNotes) {
    const shared = (n.topics || []).filter(function (t) { return topics.indexOf(t) !== -1; })[0];
    push(n, "Same topic: " + shared);
  }
  // (b) shared Smart Lists — notes sharing a list with this note.
  for (const e of listHere) {
    for (const id of Object.keys(PHASE2_LIST_INDEX)) {
      if (id === myId) continue;
      const entries = PHASE2_LIST_INDEX[id];
      if (entries.some(function (x) { return x.listId === e.listId; })) push(byId[id], "Same list: " + e.listTitle);
    }
  }
  // (c) shared cluster.
  const clusterNotes = feed.notes.filter(function (n) {
    return String(n.id || "").toLowerCase() !== myId && phase2ClusterOf(n) === cluster;
  });
  clusterNotes.sort(function (a, b) { const x = String(a.created || ""), y = String(b.created || ""); return x === y ? 0 : (x < y ? 1 : -1); });
  for (const n of clusterNotes) push(n, "Same cluster: " + phase2ClusterLabel(cluster));
  return out;
}

// ---- The generalized note renderer (phase-1 renderer, generalized) ----
const PHASE2_EXTRA_CSS = '<style>'
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
  + 'footer{overflow-wrap:break-word}'
  // The net: related links are elevated boards with their reason, never
  // a bare list (design-contract (e)). Same board language as the note.
  + '.related{margin-top:34px}'
  + '.related h2{font-size:20px;letter-spacing:.06em;margin:0 0 6px}'
  + '.related .rel-nav{font-size:14px;opacity:.8;margin:0 0 16px}'
  + '.related .rel-nav a{color:#ffbf3d;text-decoration:none}'
  + '.related ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}'
  + '.related .rel-card{--lc:#9d75ff;border:2px solid color-mix(in srgb, var(--lc) 42%, #fff 8%);border-radius:18px;background:linear-gradient(145deg,#101319,#050607);box-shadow:inset 0 1px #ffffff1c,0 14px 30px #00000090,0 0 20px color-mix(in srgb, var(--lc) 10%, transparent);padding:16px 20px;transition:transform .35s ease,box-shadow .35s ease,border-color .35s ease}'
  + '.related .rel-card:hover{transform:translateY(-3px);border-color:color-mix(in srgb, var(--lc) 70%, #fff 10%);box-shadow:inset 0 1px #ffffff2e,0 20px 40px #000000a8,0 0 60px color-mix(in srgb, var(--lc) 34%, transparent)}'
  + '.related .rel-card a{color:#fff;font-size:17px;font-weight:700;text-decoration:none}'
  + '.related .rel-card .why{font-size:13px;letter-spacing:.05em;opacity:.7;margin:6px 0 0}'
  + '</style>';
function phase2RenderNote(rec, note, meta, origin, feedRev, related) {
  const canonical = origin + meta.canonicalPath;
  const imageUrl = origin + PHASE1_CANDIDATE.imagePath;
  const dateStr = String(note.created || "").slice(0, 10) || "2026-11-12";
  const cluster = meta.cluster;
  const clusterLabel = phase2ClusterLabel(cluster);
  const jsonLd = JSON.stringify({
    "@context": "https://schema.org",
    "@graph": [
      { "@type": "BlogPosting", headline: meta.displayTitle, description: meta.description, image: imageUrl,
        datePublished: dateStr, dateModified: dateStr,
        author: { "@type": "Person", name: "Naya", url: origin + "/" },
        publisher: { "@type": "Organization", name: "NayaNET", url: origin },
        articleSection: clusterLabel, mainEntityOfPage: canonical, inLanguage: "en" },
      { "@type": "BreadcrumbList", itemListElement: [
        { "@type": "ListItem", position: 1, name: "Intel Today", item: origin + "/" },
        { "@type": "ListItem", position: 2, name: clusterLabel, item: origin + "/?cluster=" + cluster },
        { "@type": "ListItem", position: 3, name: meta.displayTitle, item: canonical },
      ] },
    ],
  });
  const baseHtml = renderNote(rec);
  const styleM = baseHtml.match(/<style>[\s\S]*?<\/style>/);
  const baseStyle = styleM ? styleM[0] : "";
  const head = '<meta charset="UTF-8">\n'
    + '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    + '<title>' + esc(meta.title) + '</title>\n'
    + '<meta name="description" content="' + esc(meta.description) + '">\n'
    + '<meta name="robots" content="index, follow">\n'
    + '<link rel="canonical" href="' + esc(canonical) + '">\n'
    + '<meta property="og:type" content="article">\n'
    + '<meta property="og:title" content="' + esc(meta.title) + '">\n'
    + '<meta property="og:description" content="' + esc(meta.description) + '">\n'
    + '<meta property="og:url" content="' + esc(canonical) + '">\n'
    + '<meta property="og:site_name" content="NayaNET">\n'
    + '<meta property="og:image" content="' + esc(imageUrl) + '">\n'
    + '<meta name="twitter:card" content="summary_large_image">\n'
    + '<meta name="twitter:title" content="' + esc(meta.title) + '">\n'
    + '<meta name="twitter:description" content="' + esc(meta.description) + '">\n'
    + '<meta name="twitter:image" content="' + esc(imageUrl) + '">\n'
    + '<script type="application/ld+json">' + jsonLd + '<\/script>\n'
    + baseStyle + "\n" + PHASE2_EXTRA_CSS;
  let html = baseHtml.replace(/<head>[\s\S]*?<\/head>/, "<head>" + head + "</head>");
  const topbar = '<div class="topbar"><a class="mark" href="/">Intel Today</a>'
    + '<a class="btn" href="/">Hub</a>'
    + '<a class="btn" href="/?cluster=' + esc(cluster) + '">' + esc(clusterLabel) + '</a>'
    + '<a class="btn" href="/#/smart-notes/' + esc(phase2CanonicalSlugForRaw(meta.snSlug)) + '">Open in the Hub \u2192</a></div>';
  const crumbs = '<nav class="crumbs"><a href="/">Intel Today</a> \u203a <a href="/?cluster=' + esc(cluster) + '">' + esc(clusterLabel) + '</a> \u203a <span>' + esc(meta.displayTitle) + '</span></nav>';
  if (html.indexOf("<main>") !== -1) html = html.replace("<main>", "<main>" + topbar + crumbs);
  const byline = '<p class="byline">By <a href="/">Naya</a> \u00b7 Published <time datetime="' + esc(dateStr) + '">' + esc(dateStr) + '</time> \u00b7 ' + esc(clusterLabel) + '</p>';
  const cover = '<figure class="cover"><img src="' + esc(PHASE1_CANDIDATE.imagePath) + '" alt="NayaNET \u2014 the intelligent layer of the internet" width="512" height="512"><figcaption>NayaNET \u00b7 the intelligent layer of the internet \u2014 the mark of the network this note describes. A real image of the feeds themselves is owed (Shawn / a Naya makes it); this cover slot is the deliverable until then.</figcaption></figure>';
  const h1Close = html.indexOf("</h1>");
  if (h1Close !== -1) html = html.slice(0, h1Close + 5) + byline + cover + html.slice(h1Close + 5);
  // The net, on the page: cluster links + related notes with reasons.
  let relHtml = '<nav class="related" aria-label="Related notes"><h2>Related in this cluster</h2>'
    + '<p class="rel-nav">Cluster: <a href="/?cluster=' + esc(cluster) + '">' + esc(clusterLabel) + '</a> \u00b7 <a href="/">Intel Today</a></p>';
  if (related.length) {
    relHtml += '<ul>';
    for (const r of related) {
      relHtml += '<li><article class="rel-card" style="--lc:' + phase2ClusterColor(cluster) + '"><a href="/s/' + esc(r.slug) + '">' + esc(r.title) + '</a><p class="why">' + esc(r.reason) + '</p></article></li>';
    }
    relHtml += '</ul>';
  } else {
    relHtml += '<p class="rel-nav">No related notes in the system\u2019s own grouping for this note yet \u2014 the cluster and Hub links above are the net for now.</p>';
  }
  relHtml += '</nav>';
  const footIdx = html.lastIndexOf("<footer>");
  if (footIdx !== -1) html = html.slice(0, footIdx) + relHtml + html.slice(footIdx);
  const oldFooter = "<footer>Smart Note " + esc(rec.id) + " \u00b7 NayaNET \u2014 the collective intelligence, live from the registry.</footer>";
  const newFooter = "<footer>Smart Note " + esc(rec.id) + " \u00b7 Intel Today \u00b7 NayaNET \u2014 the highlight is the note\u2019s own nutshell; served from the public feed, revision " + esc(feedRev) + ".</footer>";
  if (html.indexOf(oldFooter) !== -1) html = html.replace(oldFooter, newFooter);
  return html;
}

// Find a note by the phase-2 canonical slug. The phase-1 finder only
// matches a full id or an "SN-<digits>" inside the TITLE — and 806 of
// the 1,058 notes carry the SN number only in the ID (their titles are
// plain, e.g. "The Right Thing, Finished Completely"), so the phase-1
// finder 404s them even though the sitemap lists them. The phase-2
// canonical slug is the URL contract, so it is tried FIRST; the phase-1
// finder stays as the fallback so every phase-1 URL keeps working
// (full id, /s/sn2696 with SN-2696 in the title).
function phase2FindNote(feed, slug) {
  const want = String(slug || "").toLowerCase().trim();
  if (!want) return null;
  for (const n of feed.notes) {
    if (phase2CanonicalSlug(n) === want) return n;
  }
  return phase1FindNote(feed, slug);
}

// Serve ANY allowlisted note to a crawler. Denial is one identical 404
// for unknown / personal / unservable slugs — decided before any byte
// of the note is rendered. Browsers never reach this function (the
// phase-2 routes call it only for non-browser UAs).
async function phase2ServeNote(request, env, slug, origin) {
  const denied = new Response("Note not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
  const feed = await phase1LoadFeed(request, env);
  if (!feed) return new Response("Feed unavailable", { status: 503, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store" } });
  const note = phase2FindNote(feed, slug);
  if (!note || note.personal) return denied;
  const content = phase2ParseContent(note);
  if (!content.servable) return denied;
  const cluster = phase2ClusterOf(note);
  const displayTitle = phase2DisplayTitle(note);
  const meta = {
    displayTitle: displayTitle,
    title: phase2Title(note, content),
    description: phase2Description(note, content),
    canonicalPath: "/s/" + phase2CanonicalSlug(note),
    cluster: cluster,
    snSlug: phase2CanonicalSlug(note),
  };
  const related = phase2Related(note, feed);
  // The score is computed (back-end only) so the machine can be audited
  // against the score report; it is never rendered on the page.
  const score = phase2SeoScore(note, content, meta, related.length);
  void score;
  const rec = { id: phase2SnLabel(note), title: displayTitle, oneLine: content.hook, sections: content.sections, superseded: null };
  const html = phase2RenderNote(rec, note, meta, origin, String(feed.generated_from || ""), related);
  return new Response(html, { status: 200, headers: { "Content-Type": "text/html;charset=UTF-8", "Cache-Control": "public, max-age=3600", "X-Robots-Tag": "index, follow" } });
}

// The generalized sitemap: the Hub root + every SERVABLE allowlisted
// note (a URL in the sitemap that 404s is a sitemap error, so unservable
// notes are listed nowhere — they are named in the score report).
async function phase2SitemapXml(request, env, origin) {
  const feed = await phase1LoadFeed(request, env);
  if (!feed) return null;
  let urls = '  <url><loc>' + origin + '/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n';
  let count = 0;
  const seen = new Set();
  for (const note of feed.notes) {
    if (note.personal) continue;
    const content = phase2ParseContent(note);
    if (!content.servable) continue;
    // Ten SN numbers are filed twice (two different notes, one number —
    // the collision is Shawn's call to fix, never silently chosen here),
    // so ten canonical slugs cover twenty notes. A sitemap must not list
    // the same URL twice: emit each unique canonical once. The second
    // note of a colliding pair stays reachable by its full-id URL.
    const canon = '/s/' + phase2CanonicalSlug(note);
    if (seen.has(canon)) continue;
    seen.add(canon);
    const lastmod = String(note.created || "").slice(0, 10) || "2026-11-12";
    urls += '  <url><loc>' + origin + canon + '</loc><lastmod>' + lastmod + '</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>\n';
    count++;
  }
  return { xml: '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n', count: count };
}
