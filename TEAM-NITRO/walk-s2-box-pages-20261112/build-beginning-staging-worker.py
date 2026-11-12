#!/usr/bin/env python3
"""Build the walk S2 staging worker from the S2 files' bytes.
S2 (2026-11-12): completion creates the citizen's Smart Box + the one project
record + the three pages from the walk answers; the Box table is citizen_worlds
(live schema, PK alias, answers jsonb) and the pages table is page_about — the
staging worker's anon key is RLS-blocked from inserting into both (proven
401/42501), so the worker tries the live tables, mirrors the records in KV in
the tables' exact shapes, and the live projects row IS created (anon writes
allowed there). The live-table write waits for the server-side key (his hand).
Original docstring follows. Build the walk-beginning staging worker from the fixed files' bytes.
Worker: naya-walk-beginning-staging. Serves:
  /                         -> the staged welcome entry (welcome-staged.html, v5 dial)
  /welcome                  -> the fixed walk (walk-beginning-fixed.html)
  /identity.html            -> the fixed identity page (identity-fixed.html)
  /login-obsidian.jpg, /naya-logo.png -> the welcome page's assets, from KV
  POST /api/claim         -> Supabase insert + read-back (same-origin claim)
  GET  /api/claim         -> availability / read-back {exists, own, cert_no}
  POST /api/welcome/me    -> {alias, name} from the registry row
  POST /api/welcome/complete -> stores the completion in KV, returns reveal
  GET  /api/welcome/complete?alias= -> read-back of the stored completion
  /<alias>[/business|space|dashboard] -> 302 to the live nayanet.app pages
Asserts the fixed walk + identity shas before building. The registry
credential is read programmatically from the live-extracted identity file
and embedded ONLY in this staging worker (the key is the public anon key
already shipped in the live page; the LIVE splice must hold it as a secret
binding instead — see the record). The key value is never printed.
KV binding: WELCOME_ASSETS (the live nayanet KV namespace) — completions
are stored as complete_<alias> keys, test aliases only.
"""
import hashlib
import json
import re

ROUND = "/home/hatch/workspace/team-nitro/walk-s2-box-pages-20261112"
FIXROUND = "/home/hatch/workspace/team-nitro/walk-fix-20261111"
WALK = ROUND + "/walk-beginning-fixed.html"
IDENT = ROUND + "/identity-fixed.html"
WELCOME = ROUND + "/welcome-staged.html"
LIVE_IDENT = FIXROUND + "/identity-live-extracted.html"
OUT = ROUND + "/walk-beginning-staging-worker.js"

walk_raw = open(WALK, "rb").read()
walk_sha = hashlib.sha256(walk_raw).hexdigest()
ident_raw = open(IDENT, "rb").read()
ident_sha = hashlib.sha256(ident_raw).hexdigest()
welcome_raw = open(WELCOME, "rb").read()
welcome_sha = hashlib.sha256(welcome_raw).hexdigest()
print(f"walk {len(walk_raw)} B sha {walk_sha}")
print(f"identity {len(ident_raw)} B sha {ident_sha}")
print(f"welcome {len(welcome_raw)} B sha {welcome_sha}")
assert walk_sha.startswith("7e6ba646"), "walk sha is not the S2 walk sha"
assert ident_sha.startswith("84c2b29a"), "identity sha is not the entry-identity-fix sha"
assert welcome_sha.startswith("506a0f82"), "welcome sha is not the entry-identity-fix sha"

live = open(LIVE_IDENT, encoding="utf-8").read()
m = re.search(r"var SB_ANON_KEY = '([^']+)';", live)
assert m, "registry key not found in live-extracted identity"
sb_key = m.group(1)
assert sb_key.startswith("eyJ"), "key shape unexpected"
print("registry key read programmatically (value not printed)")

walk = walk_raw.decode("utf-8")
ident = ident_raw.decode("utf-8")
welcome = welcome_raw.decode("utf-8")

worker = r"""const WALK = __WALK__;
const IDENTITY = __IDENTITY__;
const WELCOME = __WELCOME__;
const SB_URL = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities";
const SB_KEY = __SBKEY__;
const SB_BASE = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1";
const SB_PROJECTS = SB_BASE + "/projects";
const SB_WORLDS = SB_BASE + "/citizen_worlds";
const SB_PAGES = SB_BASE + "/page_about";
const BOX_TABLE = "citizen_worlds"; /* Box record table, live schema: PK alias, answers jsonb, topics, settings jsonb */
const PAGE_TABLE = "page_about"; /* page record table, live schema: page_kind, page_alias, owner_alias, headline, body */
const PROJECT_TABLE = "projects"; /* the one project record, live schema: owner_alias, name, motto */
const ANSWER_KEYS = ["about", "into", "vision", "mission", "motto", "goal", "biz_do", "biz_offer", "biz_building", "space"];

const JSONH = { "content-type": "application/json" };
function j(obj, status) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: JSONH });
}
function sbHeaders() {
  return { "apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY, "Content-Type": "application/json" };
}
async function sbGetRow(alias) {
  const r = await fetch(SB_URL + "?alias=eq." + encodeURIComponent(alias)
    + "&select=alias,name,device_key,cert_no,created_at", { headers: sbHeaders() });
  if (!r.ok) return null;
  const rows = await r.json().catch(() => null);
  return (rows && rows.length) ? rows[0] : null;
}
function cleanAlias(a) {
  return String(a || "").trim().toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 32);
}
function slug(s, fb) {
  return String(s || "").trim().toLowerCase().replace(/[^a-z0-9\s-]/g, "")
    .replace(/[\s_]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "") || fb;
}
async function sbReq(method, url, body, prefer) {
  const h = sbHeaders();
  if (prefer) h["Prefer"] = prefer;
  let r;
  try {
    r = await fetch(url, { method, headers: h, body: body ? JSON.stringify(body) : undefined });
  } catch (e) { return { ok: false, status: 0, error: "fetch failed: " + String((e && e.message) || e) }; }
  const txt = await r.text().catch(() => "");
  let data = null;
  try { data = txt ? JSON.parse(txt) : null; } catch (e) { data = txt; }
  if (!r.ok) return { ok: false, status: r.status, error: (data && data.message) || String(txt).slice(0, 160) };
  return { ok: true, status: r.status, data };
}
async function sbRows(table, query) {
  const r = await sbReq("GET", SB_BASE + "/" + table + "?" + query);
  return (r.ok && Array.isArray(r.data)) ? r.data : [];
}
function esc(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
/* Pages from the Box: each page's body is the citizen's own words, in the
   smart-note ## sections in order (nutshell, why it matters, what it means,
   how to apply it, what's in it for you). A section appears only when it has
   distinct words of its own — nothing duplicated, nothing invented. */
function pageBody(kind, a) {
  const out = [];
  const seen = {};
  function sec(title, text) {
    const t = String(text || "").trim();
    if (!t || seen[t]) return;
    seen[t] = true;
    out.push("## " + title + "\n" + t + "\n");
  }
  if (kind === "personal") {
    sec("Nutshell", a.about);
    sec("Why it matters", a.into);
    sec("What it means", a.vision);
    sec("How to apply it", [a.mission, a.goal].filter(Boolean).join("\n"));
    sec("What's in it for you", a.motto);
  } else if (kind === "business") {
    sec("Nutshell", a.biz_do);
    sec("Why it matters", a.biz_offer);
    sec("What it means", a.biz_building);
    /* S2 (addendum 5) — vision runs through all three pages: the thread. */
    sec("The vision", a.vision);
    sec("How to apply it", a.mission);
  } else {
    sec("Nutshell", a.space);
    sec("Why it matters", a.into);
    sec("What it means", a.vision);
    /* S2 (addendum 5) — mission runs through all three pages: the thread. */
    sec("The mission", a.mission);
    sec("What's in it for you", a.motto);
  }
  return out.join("\n") || "## Nutshell\nYour words will appear here as you add them in the walk.\n";
}
function composePages(answers, pn) {
  return ["personal", "business", "space"].map(function(kind) {
    return { kind, headline: (pn[kind] && pn[kind].title) || "",
      page_alias: (pn[kind] && pn[kind].slug) || kind,
      body: pageBody(kind, answers) };
  });
}
function pageHtml(alias, pg) {
  /* S2 fix — the KV mirror stores the TABLE shape (page_kind), the composed
     record uses kind. Resolve both, or every page renders as YOUR SPACE. */
  const k = pg.page_kind || pg.kind;
  const color = k === "personal" ? "#a06bff" : (k === "business" ? "#2fe89e" : "#ffbf3d");
  const label = k === "personal" ? "YOUR PERSONAL PAGE" : (k === "business" ? "YOUR BUSINESS" : "YOUR SPACE");
  const secs = String(pg.body || "").split(/^## /m).filter(function(x){ return x.trim(); }).map(function(block){
    const nl = block.indexOf("\n");
    const title = (nl >= 0 ? block.slice(0, nl) : block).trim();
    const text = (nl >= 0 ? block.slice(nl + 1) : "").trim();
    return '<section class="sec"><h2>' + esc(title) + '</h2><p>' + esc(text).replace(/\n/g, "<br>") + '</p></section>';
  }).join("");
  return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    + '<title>' + esc(pg.headline) + ' — NayaNET</title><style>'
    + 'body{margin:0;background:#050507;color:#fff;font-family:system-ui,-apple-system,sans-serif}'
    + '.wrap{max-width:680px;margin:0 auto;padding:28px 18px 40px;box-sizing:border-box}'
    + '.card{background:linear-gradient(180deg,#1d1d28,#07070b 85%);border:2px solid ' + color + ';border-radius:22px;padding:26px 22px;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.4),0 18px 44px rgba(0,0,0,.7),0 0 34px ' + color + '55}'
    + '.label{font-size:11px;letter-spacing:.22em;font-weight:700;color:' + color + '}'
    + 'h1{font-size:26px;margin:10px 0 4px}.url{font-size:13px;color:#fff;font-family:ui-monospace,Menlo,monospace;word-break:break-all}'
    + '.sec h2{font-size:17px;margin:22px 0 6px;color:#fff}.sec p{font-size:15px;line-height:1.65;color:#fff;margin:0}'
    + '.back{display:inline-block;margin-top:26px;color:#fff;text-decoration:none;border:1.5px solid #a06bff;border-radius:999px;padding:10px 22px;font-size:14px;font-weight:700}'
    + '</style></head><body><div class="wrap"><div class="card"><div class="label">' + label + '</div>'
    + '<h1>' + esc(pg.headline) + '</h1><div class="url">nayanet.app/' + esc(alias) + '/' + esc(pg.page_alias) + '</div>'
    + secs + '</div><a class="back" href="/hub?alias=' + esc(alias) + '">Back to your Hub</a></div></body></html>';
}
function hubHtml(alias, name, cards) {
  const defs = { personal: ["#a06bff", "YOUR PERSONAL PAGE"], business: ["#2fe89e", "YOUR BUSINESS"], space: ["#ffbf3d", "YOUR SPACE"] };
  const items = cards.map(function(pg){
    const k = pg.page_kind || pg.kind;
    const d = defs[k] || ["#a06bff", k];
    return '<a class="hcard" style="--hc:' + d[0] + '" href="/pages/' + esc(alias) + '/' + esc(pg.page_alias) + '">'
      + '<div class="label" style="color:' + d[0] + '">' + d[1] + '</div>'
      + '<div class="t">' + esc(pg.headline) + '</div>'
      + '<div class="u">nayanet.app/' + esc(alias) + '/' + esc(pg.page_alias) + '</div></a>';
  }).join("");
  const body = cards.length
    ? '<p class="sub">Your pages — built from your own words in the walk. Tap one to open it.</p>' + items
    : '<p class="sub">No pages yet — walk the walk first, and your pages will be here.</p>'
      + '<a class="hcard" style="--hc:#a06bff" href="/welcome"><div class="t">Start the walk</div></a>';
  return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    + '<title>' + esc(name || alias) + ' — Your Hub — NayaNET</title><style>'
    + 'body{margin:0;background:#050507;color:#fff;font-family:system-ui,-apple-system,sans-serif}'
    + '.wrap{max-width:680px;margin:0 auto;padding:28px 18px 40px;box-sizing:border-box}'
    + 'h1{font-size:28px;margin:0 0 6px;text-align:center}.sub{font-size:15px;line-height:1.6;color:#fff;text-align:center;margin:0 0 20px}'
    + '.hcard{display:block;text-decoration:none;color:#fff;background:linear-gradient(180deg,#1d1d28,#07070b 85%);border:2px solid var(--hc,#a06bff);border-radius:18px;padding:20px;margin-bottom:14px;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.4),0 12px 30px rgba(0,0,0,.65)}'
    + '.hcard:hover{transform:translateY(-2px);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.5),0 16px 36px rgba(0,0,0,.7),0 0 24px var(--hc,#a06bff)}'
    + '.label{font-size:11px;letter-spacing:.22em;font-weight:700}'
    + '.t{font-size:20px;font-weight:800;margin:8px 0 4px}.u{font-size:13px;font-family:ui-monospace,Menlo,monospace;word-break:break-all}'
    + '</style></head><body><div class="wrap"><h1>' + esc(name ? (name + " — your Hub") : "Your Hub") + '</h1>' + body + '</div></body></html>';
}

export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    const p = u.pathname;

    // ---- same-origin claim: write name + alias, read the row back ----
    if (p === "/api/claim" && req.method === "GET") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const row = await sbGetRow(alias);
      if (!row) return j({ exists: false, alias });
      const dk = u.searchParams.get("device_key") || "";
      return j({ exists: true, alias: row.alias, name: row.name,
        cert_no: row.cert_no, created_at: row.created_at,
        own: !!(dk && row.device_key === dk) });
    }
    if (p === "/api/claim" && req.method === "POST") {
      let b = {};
      try { b = await req.json(); } catch (e) { return j({ ok: false, error: "bad json" }, 400); }
      const alias = cleanAlias(b.alias);
      const name = String(b.name || "").trim().slice(0, 80);
      const device_key = String(b.device_key || "").slice(0, 64);
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      if (!name) return j({ ok: false, error: "name required" }, 400);
      const ins = await fetch(SB_URL + "?select=alias,name,cert_no,created_at", {
        method: "POST",
        headers: Object.assign(sbHeaders(), { "Prefer": "return=representation" }),
        body: JSON.stringify({ alias, name, device_key }),
      });
      if (ins.status === 201 || ins.status === 200) {
        const row = await sbGetRow(alias); // read-back before answering
        if (!row || row.cert_no == null) return j({ ok: false, error: "claimed but no certificate number came back" }, 502);
        return j({ ok: true, alias: row.alias, name: row.name, cert_no: row.cert_no, created_at: row.created_at });
      }
      if (ins.status === 409) {
        const row = await sbGetRow(alias);
        if (!row) return j({ ok: false, error: "alias taken" }, 409);
        if (row.device_key && row.device_key !== device_key)
          return j({ ok: false, error: "taken" }, 409);
        if (row.cert_no == null) return j({ ok: false, error: "claimed but no certificate number came back" }, 502);
        return j({ ok: true, alias: row.alias, name: row.name, cert_no: row.cert_no, created_at: row.created_at });
      }
      const txt = await ins.text().catch(() => "");
      return j({ ok: false, error: "claim failed: " + ins.status + " " + txt.slice(0, 120) }, 502);
    }

    // ---- welcome me: name for the walk's background verify ----
    if (p === "/api/welcome/me" && req.method === "POST") {
      let b = {};
      try { b = await req.json(); } catch (e) {}
      const alias = cleanAlias(b.alias);
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const row = await sbGetRow(alias);
      if (!row) return j({ ok: false, error: "unknown alias" }, 404);
      return j({ alias: row.alias, name: row.name });
    }

    // ---- welcome complete: store server-side, return the reveal ----
    if (p === "/api/welcome/complete" && req.method === "GET") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const rec = await env.WELCOME_ASSETS.get("complete_" + alias, "text");
      if (!rec) return j({ ok: false, error: "not found" }, 404);
      return new Response(rec, { headers: JSONH });
    }
    if (p === "/api/welcome/complete" && req.method === "POST") {
      let b = {};
      try { b = await req.json(); } catch (e) { return j({ ok: false, error: "bad json" }, 400); }
      const alias = cleanAlias(b.alias);
      const name = String(b.name || alias || "").trim().slice(0, 80);
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      /* Answers: only the ten known keys, word for word, trimmed. A skipped
         question arrives with no key at all and is stored as nothing — the
         Box never invents an answer. */
      const rawAns = (b.answers && typeof b.answers === "object") ? b.answers : {};
      const answers = {};
      ANSWER_KEYS.forEach(function(k){
        const v = String(rawAns[k] == null ? "" : rawAns[k]).trim();
        if (v) answers[k] = v.slice(0, 2000);
      });
      const topics = Array.isArray(b.topics) ? b.topics.map(function(t){ return String(t); }).slice(0, 32) : [];
      const pnIn = (b.pageNames && typeof b.pageNames === "object") ? b.pageNames : {};
      const pn = {
        personal: { title: (String((pnIn.personal && pnIn.personal.title) || name || alias).trim().slice(0, 80) || alias),
          slug: slug((pnIn.personal && pnIn.personal.slug) || alias, alias) },
        business: { title: (String((pnIn.business && pnIn.business.title) || "My Business").trim().slice(0, 80) || "My Business"),
          slug: slug((pnIn.business && pnIn.business.slug) || "business", "business") },
        space: { title: (String((pnIn.space && pnIn.space.title) || "My Space").trim().slice(0, 80) || "My Space"),
          slug: slug((pnIn.space && pnIn.space.slug) || "space", "space") }
      };
      const now = new Date().toISOString();
      /* The one project record — LIVE in Supabase (anon writes allowed on
         projects). Check first: there is no unique constraint on owner_alias,
         so a blind insert would double it. Exactly one per alias. */
      let project = null, projectErr = null;
      const exProj = await sbRows("projects", "owner_alias=eq." + encodeURIComponent(alias) + "&select=id,owner_alias,name,motto&limit=1");
      if (exProj.length) {
        const pr = await sbReq("PATCH", SB_PROJECTS + "?owner_alias=eq." + encodeURIComponent(alias),
          { name: pn.personal.title, motto: answers.motto || "" });
        project = { id: exProj[0].id, owner_alias: alias, name: pn.personal.title, motto: answers.motto || "" };
        if (!pr.ok) projectErr = pr.error;
      } else {
        const pr = await sbReq("POST", SB_PROJECTS + "?select=id,owner_alias,name,motto",
          { owner_alias: alias, name: pn.personal.title, motto: answers.motto || "" }, "return=representation");
        if (pr.ok && Array.isArray(pr.data) && pr.data[0]) project = pr.data[0];
        else projectErr = pr.error || "project insert failed";
      }
      /* The Box — try the live citizen_worlds table first; the staging
         worker's anon key is RLS-blocked there (proven 401/42501), so the Box
         is mirrored in KV in the table's exact shape until the server-side
         key lands (his hand). The store is reported, never hidden. */
      const boxRow = { alias, name, answers, topics, settings: { pageNames: pn } };
      const boxTry = await sbReq("POST", SB_WORLDS + "?select=alias",
        boxRow, "return=representation,resolution=merge-duplicates");
      const boxStore = boxTry.ok ? "citizen_worlds" : "kv-fallback";
      const boxNote = boxTry.ok ? null : ("citizen_worlds insert refused: " + (boxTry.status || "") + " " + (boxTry.error || ""));
      /* The three pages — try the live page_about table per kind, mirror in
         KV in the table's exact shape either way. Pages are composed from
         the Box's answers, never from a browser copy. */
      const pages = composePages(answers, pn);
      const pageStores = [];
      for (const pg of pages) {
        const q = "owner_alias=eq." + encodeURIComponent(alias) + "&page_kind=eq." + pg.kind + "&select=id&limit=1";
        const ex = await sbRows("page_about", q);
        let st = "kv-fallback", note = null;
        const row = { page_kind: pg.kind, page_alias: pg.page_alias, owner_alias: alias, headline: pg.headline, body: pg.body };
        if (ex.length) {
          const r2 = await sbReq("PATCH", SB_PAGES + "?owner_alias=eq." + encodeURIComponent(alias) + "&page_kind=eq." + pg.kind, row);
          if (r2.ok) st = "page_about"; else note = "page_about update refused: " + (r2.status || "") + " " + (r2.error || "");
        } else {
          const r2 = await sbReq("POST", SB_PAGES + "?select=id", row, "return=representation");
          if (r2.ok) st = "page_about"; else note = "page_about insert refused: " + (r2.status || "") + " " + (r2.error || "");
        }
        pageStores.push({ kind: pg.kind, table: "page_about", store: st, note });
        await env.WELCOME_ASSETS.put("page_" + alias + "_" + pg.kind, JSON.stringify({
          table: "page_about", page_kind: pg.kind, page_alias: pg.page_alias, owner_alias: alias,
          headline: pg.headline, body: pg.body, store: st, updated_at: now }));
      }
      await env.WELCOME_ASSETS.put("box_" + alias, JSON.stringify({
        table: "citizen_worlds", alias, name, answers, topics, settings: { pageNames: pn },
        project_id: project ? project.id : null, store: boxStore, note: boxNote,
        created_at: now, updated_at: now }));
      const rec = { alias, name, answers, topics, pageNames: pn, completed_at: now,
        box_store: boxStore, box_note: boxNote, project_id: project ? project.id : null,
        project_error: projectErr, page_stores: pageStores };
      await env.WELCOME_ASSETS.put("complete_" + alias, JSON.stringify(rec));
      const origin = u.origin;
      const reveal = { alias,
        ambassador_link: "https://nayanet.app/joinus?ref=" + alias,
        pages: { personal: origin + "/pages/" + alias + "/" + pn.personal.slug,
          business: origin + "/pages/" + alias + "/" + pn.business.slug,
          space: origin + "/pages/" + alias + "/" + pn.space.slug,
          dashboard: "https://nayanet.app/dashboard?name=" + encodeURIComponent(name)
            + "&alias=" + encodeURIComponent(alias) },
        hub: origin + "/hub?alias=" + encodeURIComponent(alias),
        box: { table: "citizen_worlds", store: boxStore, note: boxNote },
        project: project ? { id: project.id, table: "projects", live: true } : { table: "projects", live: false, error: projectErr },
        page_stores: pageStores };
      return j(reveal);
    }

    // ---- Box read-back: the Box + the one project + the three pages ----
    if (p === "/api/welcome/box" && req.method === "GET") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return j({ ok: false, error: "alias required" }, 400);
      const boxRaw = await env.WELCOME_ASSETS.get("box_" + alias, "text");
      const box = boxRaw ? JSON.parse(boxRaw) : null;
      const projRows = await sbRows("projects", "owner_alias=eq." + encodeURIComponent(alias) + "&select=id,owner_alias,name,motto,created_at");
      const livePages = await sbRows("page_about", "owner_alias=eq." + encodeURIComponent(alias) + "&select=page_kind,page_alias,headline,body&order=page_kind");
      const pages = [];
      for (const kind of ["personal", "business", "space"]) {
        const raw = await env.WELCOME_ASSETS.get("page_" + alias + "_" + kind, "text");
        pages.push(raw ? JSON.parse(raw) : null);
      }
      return j({ ok: true, alias, box, box_count: box ? 1 : 0,
        project_rows: projRows, project_count: projRows.length,
        live_pages: livePages, pages });
    }

    // ---- created pages: /pages/<alias>/<slug> renders the page record ----
    const pm = p.match(/^\/pages\/([a-z0-9-]+)\/([a-z0-9-]+)\/?$/);
    if (pm) {
      const a = pm[1].toLowerCase(), seg = pm[2].toLowerCase();
      let found = null;
      for (const kind of ["personal", "business", "space"]) {
        const raw = await env.WELCOME_ASSETS.get("page_" + a + "_" + kind, "text");
        if (raw) { const pg = JSON.parse(raw); if (pg.page_alias === seg) { found = pg; break; } }
      }
      if (!found) {
        const live = await sbRows("page_about", "owner_alias=eq." + encodeURIComponent(a) + "&page_alias=eq." + encodeURIComponent(seg) + "&select=page_kind,page_alias,headline,body&limit=1");
        if (live.length) found = live[0];
      }
      if (!found) return new Response("page not found", { status: 404 });
      return new Response(pageHtml(a, found), { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }

    // ---- staging Hub: /hub?alias= shows the citizen's three pages ----
    if (p === "/hub") {
      const alias = cleanAlias(u.searchParams.get("alias"));
      if (!alias) return Response.redirect("https://nayanet.app" + p + u.search, 302);
      const boxRaw = await env.WELCOME_ASSETS.get("box_" + alias, "text");
      const box = boxRaw ? JSON.parse(boxRaw) : null;
      const cards = [];
      for (const kind of ["personal", "business", "space"]) {
        const raw = await env.WELCOME_ASSETS.get("page_" + alias + "_" + kind, "text");
        if (raw) cards.push(JSON.parse(raw));
      }
      return new Response(hubHtml(alias, box ? box.name : "", cards),
        { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }

    // ---- pages: the ENTRY is the welcome page; the walk lives at /welcome ----
    if (p === "/") {
      return new Response(WELCOME, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }
    if (p === "/identity.html") {
      return new Response(IDENTITY, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }
    if (p === "/welcome" || p === "/welcome/") {
      return new Response(WALK, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
    }
    // ---- welcome-page assets, from KV (uploaded by kv-put-welcome-assets.py) ----
    if (p === "/login-obsidian.jpg" || p === "/naya-logo.png") {
      const key = p === "/login-obsidian.jpg" ? "wbf-login-obsidian.jpg" : "wbf-naya-logo.png";
      const buf = await env.WELCOME_ASSETS.get(key, "arrayBuffer");
      if (!buf) return new Response("not found", { status: 404 });
      return new Response(buf, { headers: { "content-type": p.endsWith(".jpg") ? "image/jpeg" : "image/png", "cache-control": "public, max-age=3600" } });
    }
    if (p.startsWith("/api/")) return j({ ok: false, error: "unknown api" }, 404);

    // ---- alias redirects to the live pages (name from the completion record when known) ----
    const am = p.match(/^\/([a-z0-9-]+)(\/([a-z0-9-]+))?\/?$/i);
    if (am) {
      const a = am[1].toLowerCase(), sub = (am[3] || "").toLowerCase();
      const reserved = ["welcome", "dashboard", "identity.html", "hub", "enter",
        "manifest.webmanifest", "manifest.json", "icon-192.png", "icon-512.png", "sw.js", "world", "api", "pages"];
      if (reserved.indexOf(a) === -1) {
        let nm = "";
        try {
          const rec = await env.WELCOME_ASSETS.get("complete_" + a, "text");
          if (rec) nm = (JSON.parse(rec).name || "");
        } catch (e) {}
        const qs = "?name=" + encodeURIComponent(nm) + "&alias=" + encodeURIComponent(a);
        let dest;
        if (sub === "dashboard") dest = "https://nayanet.app/dashboard" + qs;
        else if (sub === "business") dest = "https://nayanet.app/business" + qs;
        else if (sub === "space") dest = "https://nayanet.app/space" + qs;
        else dest = "https://nayanet.app/personal" + qs;
        return Response.redirect(dest, 302);
      }
    }
    if (p.startsWith("/hub/")) {
      return Response.redirect("https://nayanet.app" + p + u.search, 302);
    }
    return new Response(WALK, { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
  },
};
"""

worker = (worker
          .replace("__WALK__", json.dumps(walk))
          .replace("__IDENTITY__", json.dumps(ident))
          .replace("__WELCOME__", json.dumps(welcome))
          .replace("__SBKEY__", json.dumps(sb_key)))
open(OUT, "w", encoding="utf-8").write(worker)
print(f"OK worker built: {OUT} ({len(worker.encode())} B, "
      f"sha256={hashlib.sha256(worker.encode()).hexdigest()})")
print("NOTE: this staging worker embeds the public anon key; live must use a secret binding.")
