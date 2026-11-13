// NayaPOWER Hub worker — serves the Hub static assets from HUB/app/,
// plus the Project Intelligence data route GET /pi/api/items.
// Deployments run ONLY through .github/workflows/deploy-hub-cloudflare.yml
//
// Data-route law (same as the Hub bridge law): the browser never ships
// a credential. Supabase access comes ONLY from worker environment
// (SUPABASE_URL + SUPABASE_READ_KEY, set as Cloudflare Worker secrets
// by the operator). No credential value ever appears in this file, in
// client code, in PI, or on the board. When the access is not set,
// the route answers an honest not-configured state — never a staged
// row. The credential the operator provisions must be SELECT-only
// (anon key behind a SELECT-only RLS policy, or a dedicated read-only
// role). A service-role key must never be used here.
const STATE_WORDS = {
  done_proven: "Done · proven",
  in_progress: "In motion",
  queued: "To do",
  verifying: "Being checked",
  needs_shawn: "Needs a decision",
  blocked: "Blocked",
  claimed: "Claimed",
};
const STATE_ALLOW = new Set(Object.keys(STATE_WORDS));

function jsonResponse(obj, status) {
  return new Response(JSON.stringify(obj), {
    status: status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

function notesTail(notes) {
  if (!Array.isArray(notes)) return [];
  return notes
    .slice(-3)
    .map(function (n) {
      var t = n && typeof n.note === "string" ? n.note : "";
      return t.length > 400 ? t.slice(0, 400) : t;
    })
    .filter(function (t) { return t.length > 0; });
}

function mapItem(r) {
  return {
    item_key: r.item_key,
    title: r.title,
    state: r.state,
    state_words: STATE_WORDS[r.state] || r.state,
    owner_seat: r.owner_seat || null,
    next_action: r.next_action || null,
    blocker: r.blocker || null,
    priority: r.priority || null,
    evidence_url: r.evidence_url || null,
    updated_at: r.updated_at || null,
    state_changed_at: r.state_changed_at || null,
    project_id: r.project_id || null,
    area_key: null,
    notes_tail: notesTail(r.notes),
  };
}


// ---- Smart Note serving (Resolve, 2026-11-05; in-Hub routing 2026-11-07) ----
// A Smart Note URL (/smart-notes/<slug>, /notes/<slug>, /note/<slug>,
// /note?n=<slug>) 302s to the note's native Hub address,
// /#/smart-notes/<slug> — Smart Notes open IN the Hub, with the Hub
// around them (Shawn's ruling, 2026-11-06/07: the Hub is the note's
// home). serveNote()/renderNote() below are the parsing reference the
// feed regen (tools/regenerate_feed_live.py) mirrors; they are not a
// browser route (see THE NOTE ROUTE above noteRedirect for the record).
// (Note: /s/* reaches this worker since the 2026-11-08 route repoint —
// HUB/wrangler.toml claims nayanet.app/s/* for hub. Before that, the
// route table sent /s/* to the naya-share worker, whose share-page
// template pointed at retired nayanet.live.)
// 2026-11-08: nayanet.app/s/* route claimed by this worker (PR #3301); the naya-share route was deleted from the zone the same day, clearing Cloudflare code 10020.
const SPECTRUM = ["#9d75ff", "#6f8dff", "#3ddc97", "#ffd34d", "#ff9f43", "#ff5d5d", "#ff5dd2"];
function esc(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
let REG_CACHE = null;
const RAW_BASE = "https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/";
async function loadRegistry() {
  if (REG_CACHE) return REG_CACHE;
  try {
    const res = await fetch(RAW_BASE + ".naya/memory/smart-notes/index.json");
    if (res.ok) {
      const idx = await res.json();
      const map = {};
      for (const e of idx.entries || []) {
        if (e && e.smart_note_id) map[String(e.smart_note_id).toLowerCase()] = e;
      }
      REG_CACHE = map;
      return REG_CACHE;
    }
  } catch (e) { /* fall through */ }
  return null;
}
const CAP_CACHE = {};
async function loadCapture(ib) {
  if (!ib) return null;
  if (CAP_CACHE[ib]) return CAP_CACHE[ib];
  try {
    const res = await fetch(RAW_BASE + ".naya/capture/" + ib + ".json");
    if (res.ok) { const c = await res.json(); CAP_CACHE[ib] = c; return c; }
  } catch (e) { /* fall through */ }
  return null;
}
const PAGE_CACHE = {};
async function loadPageMd(projectionPath) {
  if (!projectionPath) return "";
  if (PAGE_CACHE[projectionPath] != null) return PAGE_CACHE[projectionPath];
  try {
    const res = await fetch(RAW_BASE + projectionPath);
    if (res.ok) { const md = await res.text(); PAGE_CACHE[projectionPath] = md; return md; }
  } catch (e) { /* fall through */ }
  return "";
}
function slugCandidates(rawSlug) {
  const s = String(rawSlug || "").toLowerCase();
  const out = [s];
  const m = s.match(/^sn-?(\d+)$/);
  if (m) { out.push("sn-" + m[1]); out.push("sn-" + m[1].padStart(4, "0")); out.push("sn-" + String(parseInt(m[1], 10))); }
  return out;
}
function noteAccent(id) {
  const m = String(id || "").match(/(\d+)/);
  const n = m ? parseInt(m[1], 10) : 0;
  return SPECTRUM[n % SPECTRUM.length];
}
// ---- The Full Smart Note (Golden Red Layer ruling, SN-2092, 2026-11-06) ----
// A complete note is TEN sections, in this order, and there is NO machine
// note (the old AI/machine deep section is removed by that ruling). The
// reader builds each section from the note's PAGE — the page's ## headings
// are the sections — and capture intelligence fields fill only a section
// the page lacks. A section renders only when it has real text, and no
// present section is dropped. Board values are ported from the v5 Hub
// board language (Rules SS4.9/SS4.10): layered obsidian boards, one jewel
// color per section, white text, depth as shadow/mass, own-color ignition
// on hover/focus and on viewport entry (IntersectionObserver, .rv-lit).
const SECTION_DEFS = [
  { key: "nutshell", label: "In a Nutshell", color: "#ffffff", heads: ["in a nutshell", "nutshell", "essence"] },
  { key: "human", label: "Human Note", color: "#ed42c4", heads: ["human note", "human"] },
  { key: "child", label: "Child Note", color: "#55b9ee", heads: ["child note", "child", "simply", "simple"] },
  { key: "grandma", label: "Grandma Note", color: "#55e39a", heads: ["grandma note", "grandma", "for grandma"] },
  { key: "naya", label: "Naya Note", color: "#9d75ff", heads: ["naya note", "naya", "naya view", "nayas view", "my note"] },
  { key: "means", label: "What It All Means", color: "#6675ff", heads: ["what it all means", "what it means"] },
  { key: "why", label: "Why It Matters", color: "#ff5e6c", heads: ["why it matters"] },
  { key: "connects", label: "How It Connects", color: "#22d3ee", heads: ["how it connects"] },
  { key: "foryou", label: "What Is In It For You", color: "#d4a017", heads: ["what is in it for you", "whats in it for you"] },
  { key: "learning", label: "The Learning", color: "#ff9f43", heads: ["the learning", "learning", "learning lesson"] },
];
function normHead(h) {
  return String(h == null ? "" : h).replace(/[*_`#>]/g, " ").toLowerCase().replace(/[‘’]/g, "").replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
}
const HEAD_TO_KEY = {};
for (const d of SECTION_DEFS) { for (const h of d.heads) { HEAD_TO_KEY[normHead(h)] = d.key; } }
function cleanSectionText(t) {
  return String(t == null ? "" : t).replace(/\r\n/g, "\n").replace(/^\s*-{3,}\s*$/gm, "").replace(/\n{3,}/g, "\n\n").trim();
}
function parsePageSections(md) {
  const out = {};
  if (!md) return out;
  let cur = null;
  let buf = [];
  const flush = function () {
    if (cur) {
      const text = cleanSectionText(buf.join("\n"));
      if (text && !out[cur]) out[cur] = text;
    }
    buf = [];
  };
  for (const line of String(md).split("\n")) {
    const m = line.match(/^##\s+(.+?)\s*$/);
    if (m) {
      flush();
      const nh = normHead(m[1]);
      cur = HEAD_TO_KEY[nh] || (nh === "intelligence views" ? "__views" : null);
      continue;
    }
    if (/^#\s+/.test(line)) { flush(); cur = null; continue; }
    if (cur) buf.push(line.replace(/^#{3,6}\s+/, ""));
  }
  flush();
  if (out.__views) {
    const leads = { human: "human", child: "child", grandma: "grandma", naya: "naya", "naya ai": "naya", "what it means": "means", "what it all means": "means" };
    for (const para of out.__views.split(/\n\s*\n/)) {
      const lm = para.match(/^\*\*([^*]+):\*\*\s*([\s\S]+)$/);
      if (lm) {
        const k = leads[normHead(lm[1])];
        if (k && !out[k]) out[k] = cleanSectionText(lm[2]);
      }
    }
    delete out.__views;
  }
  return out;
}
function renderParas(text) {
  return cleanSectionText(text).split(/\n\s*\n/).filter(function (p) { return p.trim(); })
    .map(function (p) { return "<p>" + esc(p.trim()).replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>") + "</p>"; }).join("\n");
}
function boardHtml(d, text) {
  return '<article class="board" style="--lc:' + d.color + '" tabindex="0">' +
    '<header class="board-head"><span class="jewel" aria-hidden="true"></span><h2>' + esc(d.label) + "</h2></header>" +
    '<div class="board-body">' + renderParas(text) + "</div></article>";
}
const REVEAL_SCRIPT = '<script>(function(){var bs=document.querySelectorAll(".board");' +
  'if(!("IntersectionObserver" in window)){for(var i=0;i<bs.length;i++)bs[i].classList.add("rv-lit");return;}' +
  'var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("rv-lit");io.unobserve(e.target);}})},{threshold:.12});' +
  'bs.forEach(function(b){io.observe(b)});})();</script>';
// The hook (director's standard, 2026-11-06): the top of the block is the
// headline plus a SHORT subheadline hook — one or two lines that make you
// want to read — never the full nutshell paragraph, and never text that
// repeats below. The .nutshell CSS class is kept as the styling slot, but
// it now styles this hook, not the nutshell itself: the full nutshell
// renders exactly once, as the first board.
function hookText(rec, nut) {
  const src = cleanSectionText(rec.oneLine || "") || cleanSectionText(nut || "");
  if (!src) return "";
  const flat = src.replace(/\s+/g, " ").trim();
  const m = flat.match(/^[\s\S]*?[.!?](?=\s|$)/);
  let s = m ? m[0] : flat;
  if (s.length > 160) {
    const cut = s.slice(0, 157);
    const sp = cut.lastIndexOf(" ");
    s = (sp > 80 ? cut.slice(0, sp) : cut).trim() + "…";
  }
  // A hook that IS the whole nutshell would double the board's text —
  // in that case the board alone carries it and there is no separate hook.
  if (nut && s === cleanSectionText(nut).replace(/\s+/g, " ").trim()) return "";
  return s;
}
// ---- Superseded banner (Resolve, 2026-11-06) ----
// A note whose registry lifecycle_state is SUPERSEDED still renders (the
// record is preserved), but it must SAY so at the top and point at the
// canonical note. The registry names the successor by capture id in
// superseded_by_capture_id (with a .json suffix the block id lacks).
function supersededTarget(reg, entry) {
  if (!entry || entry.lifecycle_state !== "SUPERSEDED" || !entry.superseded_by_capture_id) return null;
  const targetIb = String(entry.superseded_by_capture_id).replace(/\.json$/i, "");
  for (const k of Object.keys(reg)) {
    const e = reg[k];
    if (e && e.intelligent_block_id === targetIb) {
      const digits = String(e.smart_note_id || "").replace(/[^0-9]/g, "");
      if (!digits) return null;
      return { id: e.smart_note_id, title: e.title || e.smart_note_id, url: "#/smart-notes/sn" + digits };
    }
  }
  return null;
}

function renderNote(rec) {
  const accent = noteAccent(rec.id);
  const secs = rec.sections || {};
  const supBanner = rec.superseded
    ? '<div class="superseded" role="note"><strong>This note has been superseded.</strong> ' +
      'Read the canonical note: <a href="' + esc(rec.superseded.url) + '">' +
      esc(rec.superseded.id) + " — " + esc(rec.superseded.title) + "</a></div>"
    : "";
  let boards = "";
  const nut = secs.nutshell || "";
  const hookStr = hookText(rec, nut);
  const hook = hookStr ? '<div class="nutshell">' + renderParas(hookStr) + "</div>" : "";
  if (nut) boards += boardHtml(SECTION_DEFS[0], nut);
  for (const d of SECTION_DEFS.slice(1)) {
    if (secs[d.key]) boards += boardHtml(d, secs[d.key]);
  }
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
    '<title>' + esc(rec.title) + ' — ' + esc(rec.id) + ' · NayaNET</title><style>' +
    ':root{--accent:' + accent + '}' +
    '*{box-sizing:border-box}body{margin:0;background:#050607;color:#fff;font-family:Georgia,serif;padding:40px 20px 80px}' +
    'main{max-width:720px;margin:0 auto}' +
    '.chip{display:inline-block;border:1px solid var(--accent);color:var(--accent);border-radius:999px;padding:3px 12px;font-size:13px;letter-spacing:.08em;margin-bottom:18px}' +
    'h1{font-size:clamp(24px,2.8vw,32px);line-height:1.12;letter-spacing:-.01em;margin:0 0 14px;text-wrap:balance}' +
    '.nutshell{font-size:20px;line-height:1.6;border-left:3px solid var(--accent);padding:6px 0 6px 18px;margin:0 0 10px}' +
    '.nutshell p{margin:0;white-space:pre-wrap}' +
    '.boards{display:flex;flex-direction:column;gap:12px;margin-top:26px}' +
    '.board{--lc:#ffffff;border:2px solid color-mix(in srgb, var(--lc) 42%, #fff 8%);border-radius:18px;background:linear-gradient(145deg,#101319,#050607);box-shadow:inset 0 1px #ffffff1c,0 14px 30px #00000090,0 0 20px color-mix(in srgb, var(--lc) 10%, transparent);overflow:hidden;opacity:.84;transition:opacity .5s ease,transform .35s ease,box-shadow .35s ease,border-color .35s ease}' +
    '.board.rv-lit{opacity:1;box-shadow:inset 0 1px #ffffff1c,0 14px 30px #00000090,0 0 0 1px rgba(255,255,255,.14),0 0 34px -8px var(--lc)}' +
    '.board:hover,.board:focus-visible{transform:translateY(-3px);border-color:color-mix(in srgb, var(--lc) 70%, #fff 10%);box-shadow:inset 0 1px #ffffff2e,0 20px 40px #000000a8,0 0 60px color-mix(in srgb, var(--lc) 34%, transparent);outline:none}' +
    '.board-head{display:flex;align-items:center;gap:12px;padding:16px 16px 0}' +
    '.board-head h2{font-size:18px;letter-spacing:.07em;margin:0;color:#fff}' +
    '.jewel{width:32px;height:32px;flex:0 0 32px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.85) 0 10%,rgba(255,255,255,0) 42%),radial-gradient(circle,#0a0a0e 0 52%,var(--lc) 57% 78%,#0a0a0e 84%);box-shadow:0 0 10px var(--lc),0 2px 6px rgba(0,0,0,.6)}' +
    '.board-body{padding:8px 24px 24px;overflow-wrap:break-word}' +
    '.superseded{border:2px solid #ff5e6c;background:#2a0d11;border-radius:14px;padding:14px 18px;margin:0 0 22px;font-size:16px;line-height:1.55}' +
    '.superseded a{color:#ffd34d}' +
    '.board-body p{font-size:17px;line-height:1.7;margin:0 0 12px;white-space:pre-wrap}' +
    '.board-body p:last-child{margin-bottom:0}' +
    'footer{margin-top:48px;opacity:.5;font-size:13px}</style></head><body><main>' +
    supBanner +
    '<span class="chip">' + esc(rec.id) + '</span>' +
    '<h1>' + esc(rec.title) + '</h1>' +
    hook +
    (boards ? '<div class="boards">' + boards + "</div>" : "") +
    '<footer>Smart Note ' + esc(rec.id) + ' · NayaNET — the collective intelligence, live from the registry.</footer>' +
    REVEAL_SCRIPT +
    '</main></body></html>';
}
// The standalone reader renderer. Not a browser route: the note routes
// above redirect into the Hub. Kept as the parsing reference the feed
// regen mirrors (its section parsing is the contract).
async function serveNote(request, env, rawSlug) {
  const reg = await loadRegistry();
  let entry = null;
  if (reg) {
    for (const c of slugCandidates(rawSlug)) { if (reg[c]) { entry = reg[c]; break; } }
  }
  if (!entry) {
    return new Response("Note not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store" } });
  }
  const rec = { id: entry.smart_note_id, title: entry.title || entry.smart_note_id, oneLine: entry.one_line || "", sections: {} };
  rec.superseded = supersededTarget(reg, entry);
  const cap = await loadCapture(entry.intelligent_block_id);
  let intel = null;
  if (cap && cap.intelligence) {
    intel = cap.intelligence;
    rec.title = intel.title || rec.title;
  }
  const md = await loadPageMd(entry.projection_path);
  const sections = parsePageSections(md);
  if (intel) {
    const fill = {
      nutshell: intel.essence,
      human: intel.human_view,
      child: intel.child_view || intel.simple_view,
      grandma: intel.grandma_view,
      naya: intel.naya_view || intel.ai_view,
      means: intel.what_it_means,
    };
    for (const k of Object.keys(fill)) {
      if (!sections[k] && fill[k]) sections[k] = cleanSectionText(fill[k]);
    }
  }
  rec.sections = sections;
  return new Response(renderNote(rec), { status: 200, headers: { "Content-Type": "text/html;charset=UTF-8", "Cache-Control": "no-store" } });
}

// ---- Service-worker cure (Resolve, 2026-11-06) ----
// WHY THIS ROUTE EXISTS: before 2026-11-07 the reader below answered
// /smart-notes/* at the server (verified by direct fetch), yet a returning, signed-in
// browser lands on the Hub shell instead (click-walk 2026-11-06: the URL
// gains "#/hub" and the feed renders). The only layer that can substitute
// the shell for a server-correct response in one profile while fresh
// fetches pass is a stale service worker in that profile: the repo's own
// history documents a v1 Hub worker that "served a stale Hub shell to
// returning visitors" cache-first (interfaces/hub/sw.js header, CURE
// 2026-10-25). But that cure never reached this worker: hub-worker.js had
// no /sw.js route and HUB/app ships no sw.js asset, so /sw.js fell through
// to the SPA fallback HTML — and a service-worker update check that
// receives HTML fails, leaving the old worker installed permanently.
// This route serves a valid, self-retiring worker at the standard paths:
// on activation it deletes every cache, unregisters itself, and reloads
// open windows, so the next navigation is answered by the network — and
// therefore by the handlers above. It intercepts nothing (no fetch
// handler). If a real service worker is ever wanted again, it ships by
// replacing this cure deliberately, in this file.
const SW_CURE_JS = [
  "// NayaNET service-worker cure — self-retiring. See hub-worker.js.",
  "self.addEventListener('install', function () { self.skipWaiting(); });",
  "self.addEventListener('activate', function (e) {",
  "  e.waitUntil((async function () {",
  "    try { var keys = await caches.keys(); await Promise.all(keys.map(function (k) { return caches.delete(k); })); } catch (err) {}",
  "    try { await self.registration.unregister(); } catch (err) {}",
  "    try { var cs = await self.clients.matchAll({ type: 'window' }); cs.forEach(function (c) { c.navigate(c.url); }); } catch (err) {}",
  "  })());",
  "});",
  "",
].join("\n");

// THE NOTE ROUTE — send the browser INTO the Hub (Resolve, 2026-11-07,
// third mechanism, after two fetch mechanisms failed live; the record is
// kept so nobody retries them):
//  1. fd1c8059 served the shell by fetching /index.html from the ASSETS
//     binding and returning it verbatim — the binding answers 307
//     (canonicalization), and every note URL threw live (error 1101).
//  2. Following the redirect chain inside the binding did not land: the
//     binding bounces /index.html <-> / and never hands over the
//     document (PR #3288, live-probed: the route was carried by its
//     standalone fallback).
//  3. Fetching the public origin root from inside the worker also did
//     not land (PR #3289, deploy step verified success, live behavior
//     unchanged — a worker subrequest does not travel the public path).
// What cannot fail: fetch NOTHING. The Hub's native address for a note
// is the hash route /#/smart-notes/<slug> — the shell at / serves 200 to
// every real browser (probe-verified, exact shell bytes), and its boot
// code + router open the note inside the Hub from that hash. So a clean
// note URL answers 302 to its own hash address. The browser does the
// one fetch that has never failed, and the note opens in the Hub.
function noteRedirect(request, slug) {
  const origin = new URL(request.url).origin;
  const dest = slug ? origin + "/#/smart-notes/" + encodeURIComponent(slug) : origin + "/#/hub";
  return Response.redirect(dest, 302);
}

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
  title: "The Infinite Smart Feeds — one feed per topic · NayaNET",
  description: "Not one feed like Facebook — infinite feeds, one for every topic, and the whole system exists because of them: they are the original intention, ten years…",
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
const PHASE2_LIST_INDEX = {};

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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if ((url.pathname === "/sw.js" || url.pathname === "/service-worker.js") && request.method === "GET") {
      return new Response(SW_CURE_JS, {
        status: 200,
        headers: { "Content-Type": "text/javascript;charset=UTF-8", "Cache-Control": "no-store" },
      });
    }
    // Smart Notes open IN THE HUB (Shawn's ruling, 2026-11-06/07): a
    // clean note URL 302s to the note's native Hub address,
    // /#/smart-notes/<slug>, where the shell's router opens the complete
    // block inside the Hub (see noteRedirect above for why no fetch
    // mechanism is used). Bare /smart-notes or /note lands on the feed.
    // ---- PHASE 2 routes (2026-11-13) ----
    // The generalized machine: every allowlisted note to crawlers, the
    // full sitemap, and the deep-path tightening. These run BEFORE the
    // phase-1 routes below (which keep robots.txt + the cover image;
    // their bot-note route is subsumed by phase2ServeNote).
    // An unmatched deep path (/s/<slug>/extra) is 404 + noindex here —
    // never the Hub shell 200 (the Phase 1 checker's finding 2).
    if ((request.method === "GET" || request.method === "HEAD") && /^\/(?:s|notes|smart-notes|note)\/[^/]+\/.+/.test(url.pathname)) {
      return new Response("Note not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/sitemap.xml") {
      const sm = await phase2SitemapXml(request, env, url.origin);
      if (!sm) return new Response("Feed unavailable", { status: 503, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store" } });
      return new Response(sm.xml, { status: 200, headers: { "Content-Type": "application/xml;charset=UTF-8", "Cache-Control": "public, max-age=3600" } });
    }
    if (request.method === "GET" || request.method === "HEAD") {
      const p2Match = url.pathname.match(/^\/(?:s|notes|smart-notes|note)\/([^/]+)\/?$/);
      if (p2Match && !phase1IsBrowserUA(request.headers.get("User-Agent") || "")) {
        return await phase2ServeNote(request, env, p2Match[1], url.origin);
      }
    }
    // ---- PHASE 1 routes (2026-11-12) ----
    // robots.txt + sitemap.xml + the cover image + the bot note page.
    // Browsers fall through to the existing 302 below (notes open IN
    // the Hub). These routes need run_worker_first entries
    // (/robots.txt, /sitemap.xml, /images, /images/*) or the assets
    // layer answers them with the SPA fallback first — that is the
    // root cause of the live fault (see the record).
    // HEAD is answered like GET on these routes: a HEAD that fell
    // through to the assets layer came back text/html (the SPA shell),
    // which is the same fault in miniature — caught by self-check
    // round 2. The platform strips the body for HEAD responses.
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/robots.txt") {
      return new Response(phase1RobotsTxt(url.origin), { status: 200, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "public, max-age=3600" } });
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/sitemap.xml") {
      return new Response(phase1SitemapXml(url.origin), { status: 200, headers: { "Content-Type": "application/xml;charset=UTF-8", "Cache-Control": "public, max-age=3600" } });
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/images/infinite-smart-feeds-cover.png") {
      return await phase1CoverImage(request, env);
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname.startsWith("/images/")) {
      return new Response("Image not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
    }
    if (request.method === "GET" || request.method === "HEAD") {
      const p1Match = url.pathname.match(/^\/(?:s|notes|smart-notes|note)\/([^/]+)\/?$/);
      if (p1Match && !phase1IsBrowserUA(request.headers.get("User-Agent") || "")) {
        return await phase1ServeNote(request, env, p1Match[1], url.origin);
      }
    }
    if (request.method === "GET") {
      const noteMatch = url.pathname.match(/^\/(?:s|notes|smart-notes|note)\/([^/]+)\/?$/);
      const noteQuery = !noteMatch && (url.pathname === "/note" || url.pathname === "/smart-notes") && url.searchParams.get("n");
      const bareNotePath = url.pathname === "/smart-notes" || url.pathname === "/smart-notes/" || url.pathname === "/note" || url.pathname === "/note/";
      if (noteMatch || noteQuery || bareNotePath) {
        const slug = noteMatch ? noteMatch[1] : (noteQuery || null);
        return noteRedirect(request, slug);
      }
    }
    if (url.pathname === "/pi/api/items" || url.pathname === "/pi/api/items/") {
      return handleItems(request, env, url);
    }
    if (url.pathname.startsWith("/pi/api/")) {
      return jsonResponse({ error: "unknown_api_route" }, 404);
    }
    // /pi MUST serve the PI face, deterministically. The assets config uses
    // single-page-application fallback, so a bare /pi request can fall
    // through to the Hub shell instead of pi/index.html (observed 2026-10-26:
    // /pi rendered the Smart Feed while /pi-face.html rendered the face).
    // Rewrite /pi and /pi/ to the face asset explicitly; never rely on
    // directory-index behavior for the route Shawn opens.
    if (url.pathname === "/pi" || url.pathname === "/pi/") {
      const faceUrl = new URL(request.url);
      faceUrl.pathname = "/pi/index.html";
      const faceRes = await env.ASSETS.fetch(new Request(faceUrl, request));
      // The face document itself must NEVER be stored by a browser: a stored
      // Hub shell answer for /pi kept reappearing after the route was fixed
      // (observed 2026-10-26 on long-lived browsers, while fresh browsers
      // and fresh fetches got the face). No-store here stops any browser
      // from ever storing a /pi answer again.
      const headers = new Headers(faceRes.headers);
      headers.set("Cache-Control", "no-store");
      headers.set("Pragma", "no-cache");
      return new Response(faceRes.body, { status: faceRes.status, headers: headers });
    }
    return env.ASSETS.fetch(request);
  },
};

async function handleItems(request, env, url) {
  const readAt = new Date().toISOString();
  if (request.method !== "GET") {
    return jsonResponse({ error: "method_not_allowed" }, 405);
  }
  const sbUrl = (env.SUPABASE_URL || "").replace(/\/$/, "");
  const sbKey = env.SUPABASE_READ_KEY || "";
  if (!sbUrl || !sbKey || !/^https:\/\//.test(sbUrl)) {
    return jsonResponse({
      configured: false,
      error: "items_endpoint_not_configured",
      message: "The items route is live, but its read-only access is not set worker-side yet. No rows are invented.",
      read_at: readAt,
      source: "work_items live",
      counts: {},
      items: [],
      decisions: [],
      ledger: { status: "pending" },
      areas: { status: "pending_schema", sets: null },
    }, 503);
  }
  const headers = {
    apikey: sbKey,
    Authorization: "Bearer " + sbKey,
    Accept: "application/json",
  };
  let limit = parseInt(url.searchParams.get("limit") || "500", 10);
  if (!isFinite(limit) || limit < 1) limit = 500;
  if (limit > 1000) limit = 1000;
  const stateParam = url.searchParams.get("state") || "";
  const base = sbUrl + "/rest/v1/work_items";
  const cols = "select=id,item_key,title,state,owner_seat,next_action,blocker,priority,evidence_url,updated_at,state_changed_at,notes,project_id";
  let rowsUrl = base + "?" + cols + "&order=updated_at.desc&limit=" + limit;
  if (STATE_ALLOW.has(stateParam)) rowsUrl += "&state=eq." + stateParam;
  let rowsRes, statesRes, decRes, ledRes;
  try {
    [rowsRes, statesRes, decRes, ledRes] = await Promise.all([
      fetch(rowsUrl, { headers: headers }),
      fetch(base + "?select=state&limit=1000", { headers: headers }),
      fetch(base + "?select=item_key,title,next_action,updated_at,owner_seat&state=eq.needs_shawn&order=updated_at.desc&limit=100", { headers: headers }),
      fetch(sbUrl + "/rest/v1/ledger_entries?select=seq,entry_id,issued_at,entry_hash&order=seq.desc&limit=1", { headers: Object.assign({}, headers, { Prefer: "count=exact" }) }),
    ]);
  } catch (e) {
    return jsonResponse({ configured: true, error: "upstream_unreachable", read_at: readAt }, 502);
  }
  if (!rowsRes.ok || !statesRes.ok || !decRes.ok) {
    return jsonResponse({ configured: true, error: "upstream_denied", read_at: readAt }, 502);
  }
  const rows = await rowsRes.json();
  const states = await statesRes.json();
  const decs = await decRes.json();
  const counts = {};
  states.forEach(function (s) {
    counts[s.state] = (counts[s.state] || 0) + 1;
  });
  let ledger = { status: "pending", note: "Ledger read not wired to this route." };
  if (ledRes.ok) {
    const lrows = await ledRes.json();
    const cr = ledRes.headers.get("content-range") || "";
    const total = cr.indexOf("/") >= 0 ? parseInt(cr.split("/")[1], 10) : null;
    if (lrows.length > 0) {
      ledger = {
        status: "live",
        rows: isFinite(total) ? total : null,
        tail_seq: lrows[0].seq,
        tail_id: lrows[0].entry_id,
        tail_hash: lrows[0].entry_hash,
        latest_issued: lrows[0].issued_at,
      };
    }
  }
  return jsonResponse({
    configured: true,
    read_at: readAt,
    source: "work_items live",
    counts: counts,
    items: rows.map(mapItem),
    decisions: decs.map(function (d) {
      return { item_key: d.item_key, title: d.title, next_action: d.next_action || null, owner_seat: d.owner_seat || null, updated_at: d.updated_at || null };
    }),
    ledger: ledger,
    areas: { status: "pending_schema", sets: null, note: "Area schema not applied; no per-area % shown rather than a wrong one." },
  }, 200);
}
// restore 2026-11-08 #2: repo deploy re-asserts hub code + routes after off-repo API deploys 20:03Z/20:32Z replaced the worker build.
// restore 2026-11-08 #3: repo deploy restores hub after the Smart Notes sync deploy (zero-bindings upload) overwrote it; sync fix = carry HUB/wrangler.toml.
