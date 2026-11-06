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


// ---- Smart Note serving (Resolve, 2026-11-05) ----
// Serves registered Smart Notes from the registry feed asset
// (HUB/app/notes-feed.json, generated from .naya/memory/smart-notes/index.json
// + captures). Live today at /notes/<slug>. The same handler answers
// /s/<slug> the moment the /s/* route points at this worker.
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
function renderNote(rec) {
  const accent = noteAccent(rec.id);
  const secs = rec.sections || {};
  let hook = "";
  let boards = "";
  const nut = secs.nutshell || "";
  if (nut) {
    const paras = cleanSectionText(nut).split(/\n\s*\n/).filter(function (p) { return p.trim(); });
    if (nut.length <= 1200 || paras.length <= 1) {
      hook = '<div class="nutshell">' + renderParas(nut) + "</div>";
    } else {
      // A long nutshell (essence pages carry the whole distilled text as
      // their Essence section): the first paragraph is the hook at the top,
      // the full text still renders as the first board — nothing is cut.
      hook = '<div class="nutshell">' + renderParas(paras[0]) + "</div>";
      boards += boardHtml(SECTION_DEFS[0], nut);
    }
  }
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
    '.board-body p{font-size:17px;line-height:1.7;margin:0 0 12px;white-space:pre-wrap}' +
    '.board-body p:last-child{margin-bottom:0}' +
    'footer{margin-top:48px;opacity:.5;font-size:13px}</style></head><body><main>' +
    '<span class="chip">' + esc(rec.id) + '</span>' +
    '<h1>' + esc(rec.title) + '</h1>' +
    hook +
    (boards ? '<div class="boards">' + boards + "</div>" : "") +
    '<footer>Smart Note ' + esc(rec.id) + ' · NayaNET — the collective intelligence, live from the registry.</footer>' +
    REVEAL_SCRIPT +
    '</main></body></html>';
}
async function serveNote(request, env, rawSlug) {
  const reg = await loadRegistry();
  let entry = null;
  if (reg) {
    for (const c of slugCandidates(rawSlug)) { if (reg[c]) { entry = reg[c]; break; } }
  }
  if (!entry) {
    return new Response("Note not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store" } });
  }
  const rec = { id: entry.smart_note_id, title: entry.title || entry.smart_note_id, sections: {} };
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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if ((url.pathname === "/note" || url.pathname === "/smart-notes") && request.method === "GET") {
      const q = url.searchParams.get("n");
      if (q) return serveNote(request, env, q);
    }
    const noteMatch = url.pathname.match(/^\/(?:s|notes|smart-notes|note)\/([^/]+)\/?$/);
    if (noteMatch && request.method === "GET") {
      return serveNote(request, env, decodeURIComponent(noteMatch[1]));
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
