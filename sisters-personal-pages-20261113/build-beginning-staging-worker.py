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
  /naya-a.jpg, /naya-b.jpg, /naya-c.jpg -> the three Naya choice pictures, from KV (QUESTIONS 10/10)
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

ROUND = "/home/hatch/workspace/team-nitro/walk-questions-10-20261112"
FIXROUND = "/home/hatch/workspace/team-nitro/walk-fix-20261111"
WALK = ROUND + "/walk-beginning-fixed.html"
IDENT = ROUND + "/identity-fixed.html"
WELCOME = ROUND + "/welcome-staged.html"
MIRROR = "/home/hatch/workspace/team-nitro/space-business-mirror-personal-20261112"
TEMPLATE = MIRROR + "/template-composed.html"
LIVE_IDENT = FIXROUND + "/identity-live-extracted.html"
OUT = ROUND + "/walk-beginning-staging-worker.js"

walk_raw = open(WALK, "rb").read()
walk_sha = hashlib.sha256(walk_raw).hexdigest()
ident_raw = open(IDENT, "rb").read()
ident_sha = hashlib.sha256(ident_raw).hexdigest()
welcome_raw = open(WELCOME, "rb").read()
welcome_sha = hashlib.sha256(welcome_raw).hexdigest()
template_raw = open(TEMPLATE, "rb").read()
template_sha = hashlib.sha256(template_raw).hexdigest()
print(f"walk {len(walk_raw)} B sha {walk_sha}")
print(f"identity {len(ident_raw)} B sha {ident_sha}")
print(f"welcome {len(welcome_raw)} B sha {welcome_sha}")
print(f"personal-template {len(template_raw)} B sha {template_sha}")
# Walk sha reconciled 2026-11-13 (sisters' Personal pages, step 1): the file in
# this dir is the GOLD-FIXED local walk (names-page base a3510446 -> 4e8500c2
# by the identical gold fix). The FILED Q10 walk is be55a494 (Q10 base
# 227a667e -> be55a494 by the same fix); the two differ by 1,344 B because
# their bases differ. The v23 assembler decides which walk the deploy worker
# embeds; this build asserts the bytes that are here: 4e8500c2.
assert walk_sha.startswith("4e8500c2"), "walk sha is not the GOLD-FIXED local walk sha (names-page base + gold fix)"
assert template_sha.startswith("61002d15"), "personal template sha is not the composed template sha (live Personal v9 992ab18c + hero fix + rooms-plus fix)"
assert ident_sha.startswith("55fdffa8"), "identity sha is not the NEW-ACCOUNT-FIX v3 identity sha (restore gated + heal + certified-name handoff + heal gate)"
assert welcome_sha.startswith("51b42b87"), "welcome sha is not the NEW-ACCOUNT-FIX welcome sha (other-identities jump-back-in)"

live = open(LIVE_IDENT, encoding="utf-8").read()
m = re.search(r"var SB_ANON_KEY = '([^']+)';", live)
assert m, "registry key not found in live-extracted identity"
sb_key = m.group(1)
assert sb_key.startswith("eyJ"), "key shape unexpected"
print("registry key read programmatically (value not printed)")

walk = walk_raw.decode("utf-8")
ident = ident_raw.decode("utf-8")
welcome = welcome_raw.decode("utf-8")
personal = template_raw.decode("utf-8")

worker = r"""const WALK = __WALK__;
const IDENTITY = __IDENTITY__;
const WELCOME = __WELCOME__;
const PERSONAL_TEMPLATE = __PERSONAL__;
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
/* ---- JOIN ATTRIBUTION (back-end round 20261112, JOIN-ATTRIBUTION.md steps 1-5) ----
   The join moment is the claim: the alias is first known here. The worker
   reads the naya_sl cookie the Smart Link redirect set (first-party on the
   domain the citizen joined from), resolves the link, and inserts ONE row
   into smart_link_joins. Dedupe: at most one join per (link, joined_alias),
   checked before insert; the table intentionally carries no unique
   constraint, so this flow owns the identity moment. Uses the existing anon
   INSERT grant on smart_link_joins and the anon SELECT on smart_links
   (active rows only) — no new grant, no new table, no schema change. No
   query parameter is ever appended to a redirect target; the cookie is the
   carrier, by design. Ambassador case: the claim body carries no invite
   code and the invites table carries no smart_link_name column, so the
   cross-device fallback is NOT built here — that is the invite step's call,
   named honestly, never a default link assumed. A join is recorded ONLY on
   a successful claim; a failed claim, or an alias taken by another device,
   records nothing. The result rides in the claim response as `join`, so the
   claim proves its own attribution. */
const SL_NAME_RE = /^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/;
const SB_LINKS = SB_BASE + "/smart_links";
const SB_JOINS = SB_BASE + "/smart_link_joins";
function slNameFromCookie(cookieHeader) {
  const m = String(cookieHeader || "").match(/(?:^|;\s*)naya_sl=([^;]+)/);
  if (!m) return null;
  let name = "";
  try { name = decodeURIComponent(m[1]).split(".")[0]; } catch (e) { return null; }
  return SL_NAME_RE.test(name) ? name : null;
}
async function recordJoin(req, alias) {
  const name = slNameFromCookie(req.headers.get("Cookie"));
  if (!name) return { attributed: false, reason: "no naya_sl cookie" };
  const links = await sbRows("smart_links", "name=eq." + encodeURIComponent(name) + "&active=is.true&select=id&limit=1");
  if (!links.length) return { attributed: false, reason: "link not found", link_name: name };
  const linkId = links[0].id;
  const ex = await sbRows("smart_link_joins", "link_id=eq." + encodeURIComponent(linkId) + "&joined_alias=eq." + encodeURIComponent(alias) + "&select=id&limit=1");
  if (ex.length) return { attributed: false, reason: "duplicate", link_id: linkId, link_name: name, already: true };
  const ins = await sbReq("POST", SB_JOINS + "?select=id",
    { link_id: linkId, joined_alias: alias, invite_code: null, source: "cookie" }, "return=representation");
  if (!ins.ok) return { attributed: false, reason: "insert refused", link_id: linkId, link_name: name, error: ins.error || ("status " + ins.status) };
  return { attributed: true, link_id: linkId, link_name: name };
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
/* SISTERS' PERSONAL PAGES (2026-11-13) — the narrow card renderer is DELETED.
   A citizen's page IS the Personal page. The template is live Personal v9
   (sha 992ab18c) + the hero fix + the rooms-plus fix, harvested byte for
   byte (template-composed.html, sha 61002d15). Only the citizen's labels
   are swapped in, each with a counted assertion — a failed count throws
   and the request 500s, never serves a half-swapped page. Nothing is
   invented: cover, photo, pills, buttons, feed, composer, bottom bar all
   arrive inside the template. Personal says "My Story", Business and Space
   say "Our Story" (the template's own page-kind mechanism). */
const PERSONAL_STORY = "Shawn Vibert builds NayaNET — the intelligent layer of the internet, where intelligence compounds and everybody wins. This is his personal world: his feed, his messages, his invites, his reports and intel, all working, all live. Welcome to the new world. Welcome to the new net.";
const PERSONAL_TAG = "Welcome to my world — make a post on my feed, send a message, make yourself at home";
function escJs(s) {
  return String(s == null ? "" : s).replace(/\\/g, "\\\\").replace(/'/g, "\\'").replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/</g, "\\u003c");
}
function swapCounted(t, old, nw, expect, label) {
  const parts = t.split(old);
  if (parts.length - 1 !== expect) throw new Error("personal-render swap failed: " + label + " expected " + expect + " found " + (parts.length - 1));
  return parts.join(nw);
}
function swapSplit(t, old, vals, markers, label) {
  /* Context-aware swap: the same string sits in HTML text AND in JS
     single-quoted literals (demo-persona migrations), and the citizen's
     words carry apostrophes — each occurrence gets the escaping its
     context needs. markers[i] must sit just before occurrence i, or the
     template moved and we throw instead of serving a broken page. */
  const parts = t.split(old);
  if (parts.length - 1 !== vals.length) throw new Error("personal-render swap failed: " + label + " expected " + vals.length + " found " + (parts.length - 1));
  for (let i = 0; i < markers.length; i++) {
    if (parts[i].indexOf(markers[i]) < 0) throw new Error("personal-render swap failed: " + label + " context " + i + " moved");
  }
  let out = parts[0];
  for (let i = 0; i < vals.length; i++) out += vals[i] + parts[i + 1];
  return out;
}
function secText(body, title) {
  /* Fallback when the Box is missing: read a ## section out of the composed
     pageBody the completion flow wrote. */
  const parts = String(body || "").split(/^## /m);
  for (let i = 0; i < parts.length; i++) {
    const nl = parts[i].indexOf("\n");
    const h = (nl >= 0 ? parts[i].slice(0, nl) : parts[i]).trim();
    if (h === title) return (nl >= 0 ? parts[i].slice(nl + 1) : "").trim();
  }
  return "";
}
function pageHtml(alias, pg, box) {
  /* S2 fix — the KV mirror stores the TABLE shape (page_kind), the composed
     record uses kind. Resolve both, or every page renders as YOUR SPACE. */
  const k = pg.page_kind || pg.kind || "personal";
  const a = (box && box.answers) || {};
  const headline = pg.headline || (box && box.name) || alias;
  const name = (box && box.name) || headline;
  const story = k === "personal" ? (a.about || secText(pg.body, "Nutshell"))
    : k === "business" ? [a.biz_do, a.biz_offer, a.biz_building].filter(Boolean).join(" ")
    : (a.space || secText(pg.body, "Nutshell"));
  const tagline = k === "business" ? (a.biz_offer || secText(pg.body, "Why it matters"))
    : (a.into || secText(pg.body, "Why it matters"));
  const vision = a.vision || "";
  const mission = a.mission || "";
  const goal = a.goal || "";
  const motto = a.motto || "";
  const whatido = a.biz_do || "";
  const initial = (String(name || alias).trim().charAt(0) || "N").toUpperCase();
  let t = PERSONAL_TEMPLATE;
  t = swapCounted(t, "<title>Shawn Vibert</title>", "<title>" + esc(headline) + "</title>", 1, "title-tag");
  t = swapCounted(t, ">Shawn Vibert</div>", ">" + esc(headline) + "</div>", 1, "pname");
  t = swapCounted(t, 'class="os-owner-name">Shawn Vibert</span>', 'class="os-owner-name">' + esc(headline) + "</span>", 1, "owner-name");
  t = swapCounted(t, "localStorage.setItem('naya.name','Shawn Vibert')", "localStorage.setItem('naya.name','" + escJs(name) + "')", 1, "name-migration-set");
  t = swapCounted(t, "pn.textContent='Shawn Vibert'", "pn.textContent='" + escJs(name) + "'", 1, "name-migration-text");
  t = swapCounted(t, "Memberships \\u2014 Shawn Vibert", "Memberships \\u2014 " + escJs(headline), 1, "memberships-doc");
  t = swapSplit(t, PERSONAL_STORY, [esc(story), esc(story), escJs(story), escJs(story)],
    ['id="abouttext">', 'id="os-story-text" style="margin:0;">', "localStorage.setItem('naya.about','", "at.textContent='"], "story");
  t = swapSplit(t, PERSONAL_TAG + ".", [esc(tagline), escJs(tagline), escJs(tagline)],
    ['id="ptag" title="Click to edit">', "localStorage.setItem('naya.tag','", "pt.textContent='"], "tagline");
  t = swapCounted(t, "Shawn&rsquo;s Smart Notes", esc(name) + "&rsquo;s Smart Notes", 1, "feed-smart");
  t = swapCounted(t, "Shawn&rsquo;s Naya Notes", esc(name) + "&rsquo;s Naya Notes", 1, "feed-naya");
  /* FEED SHARPENING (Shawn 2026-11-13 ~04:34Z; supersedes the brief's §6
     "Activity" wording AND the old feed-activity swap below it, which
     invented an "Our Activity" label the template never produces — the
     template has "Our Activity" x0 and no runtime feed relabel; only the
     story relabels My->Our. The third feed tab is the PUBLIC FEED (the
     world feed), never "Activity". The system is the Personal template's
     feed harvested verbatim; only the visible labels change (his words:
     "take that EXACT system ... and just change some of the labels").
     Internal wiring (ids, data-mw-tab, data-v) stays — it is invisible,
     and the course code reads the tab label from the DOM, so the swap
     flows through. The notif-bar "Activity" chip, the bottom-bar
     "Activity" menu item and the Stats "Activity mix" donut are NOT the
     feed tab; they stay as the template carries them. */
  t = swapCounted(t, ">My Activity — tap for the full dashboard ↓</button>", ">Public Feed — tap for the full feed ↓</button>", 1, "feed-name-public");
  t = swapCounted(t, "id=\"mwTabActivity\" data-mw-tab=\"activity\" role=\"tab\" aria-selected=\"false\"><b>Activity</b></button>", "id=\"mwTabActivity\" data-mw-tab=\"activity\" role=\"tab\" aria-selected=\"false\"><b>Public Feed</b></button>", 1, "feed-tab-public");
  t = swapCounted(t, "<button type=\"button\" data-v=\"activity\">Activity</button>", "<button type=\"button\" data-v=\"activity\">Public Feed</button>", 1, "feed-default-public");
  t = swapCounted(t, "middle%22%3EN%3C/text", "middle%22%3E" + initial + "%3C/text", 1, "avatar-letter");
  /* Avatar stroke stays #a06bff — the template's own color. No per-citizen
     color exists in the Box; the initial orb is the default by law. */
  t = swapCounted(t, "var baUser='Shawn'", "var baUser='" + escJs(name) + "'", 1, "smartname-bauser");
  t = swapCounted(t, "||'Shawn'", "||'" + escJs(name) + "'", 1, "smartname-fallback1");
  t = swapCounted(t, "|| 'Shawn'", "|| '" + escJs(name) + "'", 1, "smartname-fallback2");
  t = swapCounted(t, "return 'Shawn'", "return '" + escJs(name) + "'", 1, "smartname-fallback3");
  t = swapCounted(t, "flagship-personal", alias, 7, "page-alias-literals");
  t = swapCounted(t, "window.MSHIP_PAGE_KIND='personal'", "window.MSHIP_PAGE_KIND='" + k + "'", 1, "page-kind");
  t = swapCounted(t, "(typeof PAGE_ALIAS !== 'undefined' ? PAGE_ALIAS : 'flagship-community')", "(typeof PAGE_ALIAS !== 'undefined' ? PAGE_ALIAS : '" + alias + "')", 1, "injector-fallback-alias");
  if (vision) t = swapCounted(t, ">A world where intelligence compounds and everybody wins.</p>", ">" + esc(vision) + "</p>", 1, "sec-vision");
  if (mission) t = swapCounted(t, ">Build NayaNET — the intelligent highway for the AI age.</p>", ">" + esc(mission) + "</p>", 1, "sec-mission");
  if (goal) t = swapCounted(t, ">One million citizens by 2027.</p>", ">" + esc(goal) + "</p>", 1, "sec-goals");
  if (whatido) t = swapCounted(t, ">No what-I-do yet &mdash; tap Edit and say what you do, in one line.</p>", ">" + esc(whatido) + "</p>", 1, "sec-whatido");
  /* Purpose keeps the template's honest empty state: no walk question asks
     for a purpose, and live Personal shows the same prompt. */
  if (motto) {
    t = swapCounted(t, 'id="os-sec-motto-text" class="os-note" style="margin:0;"></p>', 'id="os-sec-motto-text" style="margin:0;">' + esc(motto) + "</p>", 1, "sec-motto");
    /* FIX-7 paints "No motto yet" over the static motto unless
       __osAboutSecs['motto'] is defined when the read resolves — seed it
       through the page's own variable, before the main script runs.
       ANCHOR LAW (fix, 2026-11-13 — the first version used
       lastIndexOf("<script") before loadAbout and landed INSIDE the main
       script block: the F5 comment in that block contains a literal
       "<script>" string, so the seed split the block in two and the whole
       main script died with 'unterminated comment' + "unexpected token:
       keyword 'this'" (2 pageerrors, feed never painted, motto never
       seeded). Anchor on the main block's own id tag instead, and assert
       the text before it ends with </script> — between blocks, never
       inside one. */
    const si = t.indexOf('<script id="os-script">');
    if (si < 0) throw new Error("personal-render: os-script tag not found");
    if (t.indexOf('<script id="os-script">', si + 1) >= 0) throw new Error("personal-render: os-script tag not unique");
    if (!t.slice(0, si).replace(/\s+$/, "").endsWith("</script>")) throw new Error("personal-render: os-script tag is not between blocks");
    t = t.slice(0, si) + '<script>window.__osAboutSecs=window.__osAboutSecs||{};window.__osAboutSecs["motto"]=' + JSON.stringify(motto).replace(/</g, "\\u003c") + ";</script>\n" + t.slice(si);
  }
  return t;
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
        const join = await recordJoin(req, row.alias); // JOIN ATTRIBUTION: the join moment is this claim
        return j({ ok: true, alias: row.alias, name: row.name, cert_no: row.cert_no, created_at: row.created_at, join });
      }
      if (ins.status === 409) {
        const row = await sbGetRow(alias);
        if (!row) return j({ ok: false, error: "alias taken" }, 409);
        if (row.device_key && row.device_key !== device_key)
          return j({ ok: false, error: "taken" }, 409);
        if (row.cert_no == null) return j({ ok: false, error: "claimed but no certificate number came back" }, 502);
        const join = await recordJoin(req, row.alias); // JOIN ATTRIBUTION: re-claim by the same device attributes too (dedupe guards the repeat)
        return j({ ok: true, alias: row.alias, name: row.name, cert_no: row.cert_no, created_at: row.created_at, join });
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
      /* The page IS the Personal page: pageHtml swaps the citizen's labels
         into the harvested template, so it needs the Box (answers +
         pageNames). KV first (sisters are kv-fallback), live citizen_worlds
         second. Without a Box, pageHtml falls back to the page record's own
         headline + ## body — a page never renders with another citizen's
         words. A failed swap throws and answers 500, never half-swapped. */
      let box = null;
      const boxRaw = await env.WELCOME_ASSETS.get("box_" + a, "text");
      if (boxRaw) { try { box = JSON.parse(boxRaw); } catch (e) { box = null; } }
      if (!box) {
        const wrows = await sbRows("citizen_worlds", "alias=eq." + encodeURIComponent(a) + "&select=alias,name,answers,settings&limit=1");
        if (wrows.length) box = wrows[0];
      }
      try {
        return new Response(pageHtml(a, found, box), { headers: { "content-type": "text/html;charset=utf-8", "cache-control": "no-store" } });
      } catch (e) {
        return new Response("page render failed: " + String(e && e.message || e).slice(0, 200), { status: 500, headers: { "content-type": "text/plain;charset=utf-8" } });
      }
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
    // ---- QUESTIONS 10/10 — the three Naya choice pictures, from KV
    // (uploaded by kv-put-naya-choice-pictures.py; A = Profile 2, B = Profile 3, C = Profile 4) ----
    if (p === "/naya-a.jpg" || p === "/naya-b.jpg" || p === "/naya-c.jpg") {
      const key = p === "/naya-a.jpg" ? "wbf-naya-a.jpg" : (p === "/naya-b.jpg" ? "wbf-naya-b.jpg" : "wbf-naya-c.jpg");
      const buf = await env.WELCOME_ASSETS.get(key, "arrayBuffer");
      if (!buf) return new Response("not found", { status: 404 });
      return new Response(buf, { headers: { "content-type": "image/jpeg", "cache-control": "public, max-age=3600" } });
    }
    // ---- service worker: the Personal template registers sw.js; serve a
    // valid no-op worker so registration succeeds (zero console errors).
    // Without this route the fallback serves the walk HTML and registration
    // fails on every staged page load. ----
    if (p === "/sw.js") {
      return new Response("/* NayaNET staging service worker — no offline cache. */\nself.addEventListener('install', function(){ self.skipWaiting(); });\nself.addEventListener('fetch', function(){ });\n", { headers: { "content-type": "application/javascript", "cache-control": "no-store" } });
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
          .replace("__PERSONAL__", json.dumps(personal))
          .replace("__SBKEY__", json.dumps(sb_key)))
open(OUT, "w", encoding="utf-8").write(worker)
print(f"OK worker built: {OUT} ({len(worker.encode())} B, "
      f"sha256={hashlib.sha256(worker.encode()).hexdigest()})")
print("NOTE: this staging worker embeds the public anon key; live must use a secret binding.")
