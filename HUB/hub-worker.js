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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/pi/api/items" || url.pathname === "/pi/api/items/") {
      return handleItems(request, env, url);
    }
    if (url.pathname.startsWith("/pi/api/")) {
      return jsonResponse({ error: "unknown_api_route" }, 404);
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
