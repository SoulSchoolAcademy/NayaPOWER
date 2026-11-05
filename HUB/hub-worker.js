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
async function loadPageNutshell(projectionPath) {
  if (!projectionPath) return "";
  try {
    const res = await fetch(RAW_BASE + projectionPath);
    if (res.ok) {
      const md = await res.text();
      const m = md.match(/##\s*In A Nutshell\s*\n+([\s\S]+?)(?:\n##|$)/i);
      if (m) return m[1].replace(/\s+/g, " ").trim().slice(0, 600);
    }
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
function renderNote(rec) {
  const accent = noteAccent(rec.id);
  const views = [["The full picture", rec.human], ["Simply", rec.simple], ["For grandma", rec.grandma], ["Naya's view", rec.naya]]
    .filter(function (v) { return v[1]; })
    .map(function (v) { return '<section class="view"><h2>' + esc(v[0]) + '</h2><p>' + esc(v[1]) + '</p></section>'; }).join("\n");
  const deep = (rec.ai || rec.machine)
    ? '<details class="deep"><summary>For AIs and machines</summary>' +
      (rec.ai ? '<h3>AI view</h3><p>' + esc(rec.ai) + '</p>' : '') +
      (rec.machine ? '<h3>Machine view</h3><p class="mono">' + esc(rec.machine) + '</p>' : '') + '</details>'
    : '';
  const meta = [rec.category, rec.topic, rec.subtopic].filter(Boolean).join(' · ');
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
    '<title>' + esc(rec.title) + ' — ' + esc(rec.id) + ' · NayaNET</title><style>' +
    ':root{--accent:' + accent + '}' +
    '*{box-sizing:border-box}body{margin:0;background:#050607;color:#fff;font-family:Georgia,serif;padding:40px 20px 80px}' +
    'main{max-width:720px;margin:0 auto}' +
    '.chip{display:inline-block;border:1px solid var(--accent);color:var(--accent);border-radius:999px;padding:3px 12px;font-size:13px;letter-spacing:.08em;margin-bottom:18px}' +
    'h1{font-size:34px;line-height:1.2;margin:0 0 8px}.meta{opacity:.65;font-size:14px;margin-bottom:26px}' +
    '.nutshell{font-size:20px;line-height:1.6;border-left:3px solid var(--accent);padding:6px 0 6px 18px;margin:0 0 34px}' +
    '.view{margin:0 0 26px}.view h2{font-size:15px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}' +
    '.view p{font-size:17px;line-height:1.65;margin:0;white-space:pre-wrap}' +
    '.deep{margin-top:30px;border-top:1px solid #2a2d33;padding-top:16px}.deep summary{cursor:pointer;color:var(--accent)}' +
    '.deep h3{font-size:13px;letter-spacing:.12em;text-transform:uppercase;opacity:.8}.deep p{font-size:15px;line-height:1.6;white-space:pre-wrap}.mono{font-family:ui-monospace,monospace;font-size:13px}' +
    'footer{margin-top:48px;opacity:.5;font-size:13px}</style></head><body><main>' +
    '<span class="chip">' + esc(rec.id) + '</span>' +
    '<h1>' + esc(rec.title) + '</h1>' +
    (meta ? '<div class="meta">' + esc(meta) + '</div>' : '') +
    (rec.essence ? '<p class="nutshell">' + esc(rec.essence) + '</p>' : '') +
    views + deep +
    '<footer>Smart Note ' + esc(rec.id) + ' · NayaNET — the collective intelligence, live from the registry.</footer>' +
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
  const rec = { id: entry.smart_note_id, title: entry.title || entry.smart_note_id, category: entry.category || "", topic: entry.topic || "", subtopic: entry.subtopic || "", essence: "", human: "", simple: "", grandma: "", naya: "", ai: "", machine: "" };
  const cap = await loadCapture(entry.intelligent_block_id);
  if (cap && cap.intelligence) {
    const i = cap.intelligence;
    rec.title = i.title || rec.title;
    rec.essence = i.essence || "";
    rec.human = i.human_view || "";
    rec.simple = i.simple_view || "";
    rec.grandma = i.grandma_view || "";
    rec.naya = i.naya_view || "";
    rec.ai = i.ai_view || "";
    rec.machine = i.machine_view || "";
  }
  if (!rec.essence) rec.essence = await loadPageNutshell(entry.projection_path);
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
