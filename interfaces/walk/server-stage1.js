// naya-welcome — THE OFFICIAL WELCOME, built right (2026-10-24).
// The page AFTER identity: nayanet.live/welcome · /api/welcome/* · /world/*.
// Identity is NOT built here — the Smart Identity Activation already
// certifies the citizen (nayanet_identities: alias · name · device_key ·
// cert_no) and hands them to nayanet.live, where the Hub greets them by
// the device-local identity store. This walk reads THAT store, verifies
// it with the registry, and asks only the ten questions that build the
// world. There is no begin endpoint and no claim form — never was again.
// Server core: the proven previous worker (matches v1 · jewel covers ·
// world pages with server-side privacy), re-authenticated on the real
// claim's credential. Privacy law: findable != visible — a private page
// serves the CONNECT LAYER ONLY to anyone but its owner.

const SB_URL = 'https://dahisasgpfvziswqvmvm.supabase.co';
const NAME_RE = /^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/;
const WALK_HTML = /*__WALK_HTML__*/ '';

const DEFAULT_SETTINGS = {
  personal: { visibility: 'private', findable: true },
  business: { visibility: 'public',  findable: true },
  space:    { visibility: 'public',  findable: true }
};

const SPECTRUM = ['#a06bff', '#3fb8ff', '#2fe89e', '#ffbf3d', '#ff9a5a', '#ff5e6c', '#e84fff'];
const PAGE_COLORS = { personal: '#a06bff', business: '#3fb8ff', space: '#2fe89e' };

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400'
};

function json(status, body, extra) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...CORS, ...(extra || {}) }
  });
}
const err = (status, error) => json(status, { error });
function html(status, body, extra) {
  return new Response(body, {
    status,
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', ...(extra || {}) }
  });
}

async function sb(env, method, path, body, prefer) {
  const res = await fetch(SB_URL + '/rest/v1/' + path, {
    method,
    headers: {
      apikey: env.SUPABASE_SERVICE_ROLE_KEY,
      Authorization: 'Bearer ' + env.SUPABASE_SERVICE_ROLE_KEY,
      'Content-Type': 'application/json',
      Prefer: prefer || (method === 'POST' ? 'return=representation' : 'return=minimal')
    },
    body: body ? JSON.stringify(body) : undefined
  });
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = null; }
  return { ok: res.ok, status: res.status, data };
}

// ─── CITIZEN AUTH — the real claim's credential ─────────────────────────
// A completed claim leaves the device-local identity in localStorage on
// this origin — nayanet_smart_name / nayanet_smart_alias /
// nayanet_vault_key — the same store the Hub greets from. Clients present
// {alias, device_key, name} from that store. A presented vault key must
// match the registry row exactly. When this origin holds no key (the
// claim keeps its own copy on the identity origin), the device's stored
// name must match the certificate's name — the device-local trust the
// Hub itself runs on. Nothing new is minted here: no cookie, no token.
async function getIdentity(env, alias) {
  const r = await sb(env, 'GET', 'nayanet_identities?alias=eq.' + encodeURIComponent(alias) + '&select=alias,name,device_key,cert_no,created_at');
  return (r.ok && Array.isArray(r.data) && r.data.length) ? r.data[0] : null;
}
async function authCitizen(env, body) {
  const alias = typeof body.alias === 'string' ? body.alias.trim().toLowerCase() : '';
  if (!NAME_RE.test(alias)) return { error: err(400, 'That alias does not look right — come in through your Hub, where this device already knows you.') };
  const id = await getIdentity(env, alias);
  if (!id) return { error: err(404, 'That alias is not certified yet — your certificate comes first, then this walk knows your name.') };
  const key = typeof body.device_key === 'string' ? body.device_key : '';
  if (key) {
    if (key !== id.device_key) return { error: err(403, 'This device key does not match that certificate — open the Welcome on the device that claimed this alias.') };
  } else {
    const nm = typeof body.name === 'string' ? body.name.trim().toLowerCase() : '';
    if (!nm || nm !== String(id.name).trim().toLowerCase()) {
      return { error: err(403, 'We could not confirm this world is yours on this device — come in through your Hub, on the device that claimed this alias.') };
    }
  }
  return { id };
}
async function getWorld(env, alias) {
  const r = await sb(env, 'GET', 'citizen_worlds?alias=eq.' + encodeURIComponent(alias) + '&select=*');
  return (r.ok && Array.isArray(r.data) && r.data.length) ? r.data[0] : null;
}
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const initialsOf = (name, alias) => {
  const src = (name || alias || '?').trim();
  const parts = src.split(/\s+/);
  return ((parts[0] || '?')[0] + (parts.length > 1 ? parts[parts.length - 1][0] : (src[1] || ''))).toUpperCase();
};

// ─── MATCHES (v1 — SN-0845 + Lock Packet weights 40·25·20·15) ─────────────
// Question map (steering 3): topics 40 · personal goal+vision language 25 ·
// offer ↔ (building + business goal) cross 20 · meet-desires vs into/topics 15.
function tokenize(text) {
  const stop = new Set(['that', 'this', 'with', 'from', 'your', 'yours', 'want', 'into', 'about', 'people', 'help', 'build', 'building', 'work', 'life', 'world', 'make', 'making', 'love', 'really', 'just', 'like', 'what', 'when', 'where', 'they', 'them', 'then', 'than', 'have', 'been', 'will', 'would']);
  const out = new Set();
  for (const w of String(text || '').toLowerCase().split(/[^a-z0-9]+/)) {
    if (w.length >= 4 && !stop.has(w)) out.add(w);
  }
  return out;
}
function overlapRatio(a, b) {
  if (!a.size || !b.size) return { ratio: 0, shared: [] };
  const shared = [...a].filter((x) => b.has(x));
  return { ratio: shared.length / Math.max(a.size, b.size), shared };
}
const ans = (w, k) => ((w && w.answers) || {})[k] || '';
function computeMatches(me, candidates) {
  const myTopics = new Set((me.topics || []).map((t) => String(t).toLowerCase().trim()).filter(Boolean));
  const myGV = tokenize(ans(me, 'goal') + ' ' + ans(me, 'vision'));
  const myOffer = tokenize(ans(me, 'biz_offer'));
  const myBuilding = tokenize(ans(me, 'biz_building') + ' ' + ans(me, 'biz_goal'));
  const myMeet = tokenize(ans(me, 'space'));
  const out = [];
  for (const c of candidates) {
    if (c.alias === me.alias) continue;
    const theirTopics = new Set((c.topics || []).map((t) => String(t).toLowerCase().trim()).filter(Boolean));
    const sharedTopics = [...myTopics].filter((t) => theirTopics.has(t));
    const topicScore = myTopics.size && theirTopics.size ? 40 * (sharedTopics.length / Math.max(myTopics.size, theirTopics.size)) : 0;

    const theirGV = tokenize(ans(c, 'goal') + ' ' + ans(c, 'vision'));
    const gv = overlapRatio(myGV, theirGV);
    const gvScore = 25 * gv.ratio;

    const theirOffer = tokenize(ans(c, 'biz_offer'));
    const theirBuilding = tokenize(ans(c, 'biz_building') + ' ' + ans(c, 'biz_goal'));
    const cross1 = overlapRatio(myOffer, theirBuilding);
    const cross2 = overlapRatio(myBuilding, theirOffer);
    const crossScore = 20 * Math.max(cross1.ratio, cross2.ratio);

    const theirInto = tokenize(ans(c, 'into') + ' ' + (c.topics || []).join(' '));
    const meet = overlapRatio(myMeet, theirInto);
    const meetScore = 15 * meet.ratio;

    const parts = [topicScore, gvScore, crossScore, meetScore];
    const nonzero = parts.filter((p) => p > 0).length;
    const total = Math.round(parts.reduce((a, b) => a + b, 0));
    if (nonzero < 2 || total <= 0) continue;

    const reasons = [];
    if (sharedTopics.length) reasons.push('You both care about ' + sharedTopics.slice(0, 3).join(', '));
    if (gv.shared.length) reasons.push('Your goals speak the same language: ' + gv.shared.slice(0, 3).join(', '));
    const crossWords = [...cross1.shared, ...cross2.shared];
    if (crossWords.length) reasons.push('What you offer meets what they are building: ' + [...new Set(crossWords)].slice(0, 3).join(', '));
    if (meet.shared.length) reasons.push('They are into what your space is about: ' + meet.shared.slice(0, 3).join(', '));
    out.push({ alias: c.alias, name: c.name, pct: Math.min(100, total), reasons: reasons.slice(0, 3), topics: c.topics || [] });
  }
  out.sort((a, b) => b.pct - a.pct);
  return out.slice(0, 5);
}
async function matchesFor(env, world) {
  const r = await sb(env, 'GET', 'citizen_worlds?select=alias,name,answers,topics,settings&limit=500');
  const rows = (r.ok && Array.isArray(r.data)) ? r.data : [];
  const findable = rows.filter((w) => w.settings && w.settings.personal && w.settings.personal.findable === true);
  return computeMatches(world, findable);
}

// ─── DETERMINISTIC JEWEL COVER (seeded by alias; never blank) ──────────────
function hashSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
function mulberry(seed) {
  let a = seed;
  return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
function shade(hex, f) {
  const n = parseInt(hex.slice(1), 16);
  const r = Math.min(255, Math.max(0, Math.round(((n >> 16) & 255) * f)));
  const g = Math.min(255, Math.max(0, Math.round(((n >> 8) & 255) * f)));
  const b = Math.min(255, Math.max(0, Math.round((n & 255) * f)));
  return '#' + [r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('');
}
function jewelSVG(alias, base) {
  const rnd = mulberry(hashSeed(alias + '|' + base));
  const cx = 200, cy = 96;
  const pts = [];
  const spikes = 9;
  for (let i = 0; i < spikes; i++) {
    const ang = (i / spikes) * Math.PI * 2 - Math.PI / 2;
    const rad = 62 + rnd() * 30;
    pts.push([cx + Math.cos(ang) * rad, cy + Math.sin(ang) * rad * 0.78]);
  }
  let facets = '';
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i], q = pts[(i + 1) % pts.length];
    const f = 0.55 + rnd() * 0.85;
    const fill = rnd() < 0.22 ? SPECTRUM[Math.floor(rnd() * SPECTRUM.length)] : shade(base, f);
    facets += '<polygon points="' + cx + ',' + cy + ' ' + p[0].toFixed(1) + ',' + p[1].toFixed(1) + ' ' + q[0].toFixed(1) + ',' + q[1].toFixed(1) + '" fill="' + fill + '" fill-opacity="' + (0.75 + rnd() * 0.25).toFixed(2) + '"/>';
  }
  let stones = '';
  for (let i = 0; i < 5; i++) {
    const c = SPECTRUM[i];
    stones += '<g transform="translate(' + (152 + i * 48) + ',178) rotate(45)"><rect x="-9" y="-9" width="18" height="18" rx="3" fill="' + c + '" fill-opacity="0.92"/><rect x="-9" y="-9" width="18" height="18" rx="3" fill="none" stroke="rgba(255,255,255,.75)" stroke-width="1"/></g>';
  }
  return '<svg viewBox="0 0 400 200" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' + facets +
    '<polygon points="' + pts.map((p) => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ') + '" fill="none" stroke="rgba(255,255,255,.8)" stroke-width="1.6"/>' +
    '<circle cx="' + cx + '" cy="' + cy + '" r="7" fill="#fff"/>' + stones + '</svg>';
}

// ─── SHARED WORLD CSS (flagship language, composed lean) ───────────────────
const WORLD_CSS = `
:root{--bg:#050507;--ink:#f8f7fb;--silver:#E8E8EC;--serif:'Newsreader',Georgia,'Times New Roman',serif;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;--ease:cubic-bezier(.16,.84,.22,1)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
body{min-height:100vh;overflow-x:hidden}
a{color:inherit}
.topbar{position:sticky;top:0;z-index:100;height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 min(28px,5vw);background:rgba(4,4,5,.88);border-bottom:1px solid rgba(245,241,232,.10);backdrop-filter:blur(14px)}
.brand{font-family:var(--serif);font-size:.82rem;font-weight:600;letter-spacing:.26em;text-transform:uppercase;color:var(--silver)}
.install-pill{border:1.5px solid #fff;border-radius:999px;background:linear-gradient(180deg,#1b1b24,#07070b);color:#fff;font:700 .72rem var(--sans);letter-spacing:.14em;padding:9px 16px;cursor:pointer;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),inset 0 -4px 8px rgba(0,0,0,.6),0 8px 20px rgba(0,0,0,.55);transition:all .28s var(--ease)}
.install-pill:hover{border-color:var(--pc,#a06bff);box-shadow:0 0 26px -4px var(--pc,#a06bff),inset 0 1px 0 rgba(255,255,255,.35);transform:translateY(-1px)}
.cover{position:relative;min-height:308px;display:flex;align-items:flex-end;padding:34px min(5vw,44px);overflow:hidden;background:radial-gradient(560px 240px at 12% -10%,color-mix(in srgb,var(--pc) 50%,transparent),transparent 60%),radial-gradient(700px 300px at 88% 110%,rgba(232,79,255,.20),transparent 60%),linear-gradient(135deg,#14142b,#241547 32%,#3c2270 55%,#0d2c50 82%,#123f63)}
.cover svg{position:absolute;inset:0;width:100%;height:100%;opacity:.95}
.cover-shade{position:absolute;inset:0;background:linear-gradient(180deg,transparent 30%,rgba(3,3,5,.72))}
.cover-in{position:relative;z-index:2;display:flex;align-items:center;gap:22px;flex-wrap:wrap;width:100%}
.orb{width:104px;height:104px;flex:0 0 auto;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:2.3rem;font-weight:600;color:#fff;background:radial-gradient(circle at 34% 28%,color-mix(in srgb,var(--pc) 78%,#fff),var(--pc) 52%,#0a0a12 130%);border:2px solid rgba(255,255,255,.9);box-shadow:inset 0 2px 0 rgba(255,255,255,.5),inset 0 -10px 22px rgba(0,0,0,.5),0 18px 42px rgba(0,0,0,.6),0 0 34px -6px var(--pc)}
.cover h1{font-family:var(--serif);font-weight:560;font-size:clamp(2.4rem,6.4vw,4rem);line-height:1.05}
.cover .alias-line{letter-spacing:.22em;text-transform:uppercase;font-size:.78rem;font-weight:800;color:var(--silver);margin-top:8px}
.cover .motto{font-family:var(--serif);font-style:italic;font-size:1.2rem;color:#fff;margin-top:8px;max-width:640px}
.wrap{max-width:1180px;margin:0 auto;padding:30px min(5vw,44px) 90px}
.tabs{display:flex;gap:10px;flex-wrap:wrap;padding:18px 2px 8px;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{flex:0 0 auto;display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;border:2px solid rgba(255,255,255,.3);background:rgba(0,0,0,.5);color:#fff;font-size:14px;font-weight:700;text-decoration:none;white-space:nowrap;transition:all .22s var(--ease)}
.tab i{width:9px;height:9px;border-radius:50%;background:var(--rc);flex:0 0 auto}
.tab:hover{border-color:var(--rc);box-shadow:0 0 22px -6px var(--rc),inset 0 1px 0 rgba(255,255,255,.14);color:#fff;transform:translateY(-1px)}
.board{--igc:var(--pc);background:linear-gradient(180deg,#17141f,#0a0a10 60%,#060609);border:1.5px solid rgba(255,255,255,.22);border-radius:24px;padding:26px 26px 24px;margin-top:22px;box-shadow:inset 0 2px 0 rgba(255,255,255,.13),inset 0 -5px 13px rgba(0,0,0,.3),0 0 0 1px rgba(255,255,255,.07),0 16px 44px rgba(0,0,0,.55),0 5px 18px rgba(0,0,0,.45);transition:all .25s var(--ease)}
.board:hover{border-color:var(--igc);box-shadow:inset 0 2px 0 rgba(255,255,255,.13),inset 0 -5px 13px rgba(0,0,0,.3),0 0 22px -6px var(--igc),0 16px 44px rgba(0,0,0,.55)}
.board h2{font-size:.8rem;font-weight:900;letter-spacing:.25em;text-transform:uppercase;color:#fff;display:flex;align-items:center;gap:10px;margin-bottom:12px}
.board h2::before{content:"";width:11px;height:11px;transform:rotate(45deg);background:var(--igc);box-shadow:0 0 12px var(--igc);flex:0 0 auto}
.board p{font-size:17px;line-height:1.62;color:var(--ink);white-space:pre-wrap}
.chips{display:flex;flex-wrap:wrap;gap:9px}
.chip{border:1.5px solid rgba(255,255,255,.4);border-radius:999px;padding:7px 14px;font-size:.85rem;font-weight:700;background:rgba(0,0,0,.45)}
.doors{display:flex;flex-wrap:wrap;gap:12px;margin-top:6px}
.door{display:inline-flex;align-items:center;gap:9px;background:#050505;border:1.5px solid rgba(255,255,255,.75);border-radius:999px;padding:12px 20px;color:#fff;font-weight:800;font-size:.92rem;text-decoration:none;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),inset 0 -4px 9px rgba(0,0,0,.65),0 10px 22px rgba(0,0,0,.5);transition:all .22s var(--ease)}
.door:hover{border-color:var(--dc,#a06bff);box-shadow:0 0 24px -5px var(--dc,#a06bff),inset 0 1px 0 rgba(255,255,255,.35);transform:translateY(-2px)}
.match-row{display:flex;align-items:center;gap:16px;padding:15px 4px;border-bottom:1px solid rgba(255,255,255,.09)}
.match-row:last-child{border-bottom:none}
.match-orb{width:52px;height:52px;border-radius:50%;flex:0 0 auto;display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-weight:600;font-size:1.05rem;color:#fff;background:radial-gradient(circle at 34% 28%,color-mix(in srgb,var(--mc) 75%,#fff),var(--mc) 55%,#0a0a12 135%);border:1.5px solid rgba(255,255,255,.85);box-shadow:0 8px 20px rgba(0,0,0,.5),0 0 16px -4px var(--mc)}
.match-main{flex:1;min-width:0}
.match-name{font-weight:800;font-size:1.02rem}
.match-name a{text-decoration:none}
.match-name a:hover{text-decoration:underline}
.match-reason{color:var(--silver);font-size:.9rem;line-height:1.45;margin-top:2px}
.match-pct{font-family:var(--serif);font-size:1.7rem;font-weight:600;color:var(--mc)}
.setrow{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.09)}
.setrow:last-child{border-bottom:none}
.setrow .lab{font-weight:800}
.setrow .sub{color:var(--silver);font-size:.86rem;margin-top:2px}
.seg{display:inline-flex;border:1.5px solid rgba(255,255,255,.5);border-radius:999px;overflow:hidden}
.seg button{background:transparent;border:none;color:#fff;font:700 .82rem var(--sans);padding:9px 16px;cursor:pointer}
.seg button.on{background:#fff;color:#06060a}
.saved-note{color:#2fe89e;font-weight:800;font-size:.85rem;min-height:1.1em}
.foot{border-top:1px solid rgba(245,241,232,.10);padding:22px min(5vw,44px);display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;font-size:.8rem;font-weight:800;letter-spacing:.12em;color:var(--silver)}
.empty{color:var(--silver);font-size:16px;line-height:1.6}
.kicker{font-size:.75rem;font-weight:900;letter-spacing:.3em;text-transform:uppercase;color:var(--pc)}
@media (max-width:640px){.orb{width:82px;height:82px;font-size:1.8rem}.wrap{padding-bottom:70px}}
`;

function tabsRow(alias, active) {
  const doors = [
    ['Home', '/world/' + alias, SPECTRUM[0]],
    ['Dashboard', 'https://nayanet.live/dashboard', SPECTRUM[1]],
    ['About', '/world/' + alias + '#about', SPECTRUM[2]],
    ['Today', 'https://nayanet.live/rooms/today', SPECTRUM[3]],
    ['Smart Notes', 'https://nayanet.live/', SPECTRUM[4]],
    ['Connections', 'https://nayanet.live/rooms/connections', SPECTRUM[5]],
    ['Message', 'https://nayanet.live/rooms/mail', SPECTRUM[6]],
    ['Inbox', 'https://nayanet.live/rooms/mail', SPECTRUM[0]],
    ['Growth', 'https://nayanet.live/rooms/growth', SPECTRUM[1]],
    ['Lists', 'https://nayanet.live/rooms/lists', SPECTRUM[2]],
    ['Reports', 'https://nayanet.live/rooms/reports', SPECTRUM[3]],
    ['Settings', '/world/' + alias + '#settings', SPECTRUM[4]],
    ['Smart Factory', 'https://nayanet.live/#/hub/factory', SPECTRUM[5]]
  ];
  return '<nav class="tabs" aria-label="Your doors">' + doors.map(([label, href, c]) =>
    '<a class="tab" style="--rc:' + c + '" href="' + href + '"><i></i>' + esc(label) + '</a>').join('') + '</nav>';
}

function matchesPanel(matches, heading) {
  if (!matches || !matches.length) {
    return '<section class="board" style="--igc:#e84fff"><h2>' + esc(heading || 'Your Matches') + '</h2>' +
      '<p class="empty">You are among the first citizens here — your matches appear as more people arrive and declare what they are about. The network plays the match game for you from minute one.</p></section>';
  }
  const rows = matches.map((m, i) => {
    const c = SPECTRUM[i % SPECTRUM.length];
    return '<div class="match-row"><div class="match-orb" style="--mc:' + c + '">' + esc(initialsOf(m.name, m.alias)) + '</div>' +
      '<div class="match-main"><div class="match-name"><a href="/world/' + esc(m.alias) + '">' + esc(m.name || m.alias) + '</a> <span style="color:var(--silver);font-weight:600">· nayanet.live/world/' + esc(m.alias) + '</span></div>' +
      '<div class="match-reason">' + esc((m.reasons || []).join(' · ')) + '</div></div>' +
      '<div class="match-pct" style="--mc:' + c + '">' + m.pct + '%</div></div>';
  }).join('');
  return '<section class="board" style="--igc:#e84fff"><h2>' + esc(heading || 'Your Matches') + '</h2>' + rows + '</section>';
}

function worldShell(opts) {
  // opts: alias, name, page ('personal'|'business'|'space'), color, title, motto, body
  const pc = opts.color;
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
    '<title>' + esc(opts.title) + ' | NayaNET</title>' +
    '<link rel="manifest" href="/manifest.json">' +
    '<meta name="theme-color" content="#050507">' +
    '<style>:root{--pc:' + pc + '}' + WORLD_CSS + '</style></head><body>' +
    '<header class="topbar"><span class="brand">NayaNET</span>' +
    '<button class="install-pill" type="button" onclick="installApp()">INSTALL APP</button></header>' +
    '<div class="cover">' + jewelSVG(opts.alias, pc) + '<div class="cover-shade"></div>' +
    '<div class="cover-in"><div class="orb">' + esc(initialsOf(opts.name, opts.alias)) + '</div>' +
    '<div><h1>' + esc(opts.name) + '</h1>' +
    '<div class="alias-line">nayanet.live/world/' + esc(opts.alias) + (opts.page !== 'personal' ? '/' + opts.page : '') + '</div>' +
    (opts.motto ? '<div class="motto">&ldquo;' + esc(opts.motto) + '&rdquo;</div>' : '') +
    '</div></div></div>' +
    '<div class="wrap">' + tabsRow(opts.alias, opts.page) + opts.body + '</div>' +
    '<footer class="foot"><span>NAYANET — THE NEW NET</span><span>ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</span></footer>' +
    '<script>let dp;window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();dp=e});function installApp(){if(dp){dp.prompt();dp=null}else{alert("To install: open your browser menu and choose \\u201cAdd to Home Screen\\u201d.")}}</script>' +
    '</body></html>';
}

// ─── WORLD PAGE RENDERERS ──────────────────────────────────────────────────
function sectionBoard(colorIdx, title, text) {
  const c = SPECTRUM[colorIdx % SPECTRUM.length];
  if (!text || !String(text).trim()) return '';
  return '<section class="board" style="--igc:' + c + '"><h2>' + esc(title) + '</h2><p>' + esc(text) + '</p></section>';
}
function ownerSettingsBar(alias, settings) {
  const pages = [['personal', 'Personal Page'], ['business', 'Business Page'], ['space', 'Space']];
  const rows = pages.map(([key, label]) => {
    const s = settings[key] || DEFAULT_SETTINGS[key];
    return '<div class="setrow"><div><div class="lab">' + label + '</div>' +
      '<div class="sub">Visibility — who can see inside. Findable — the match game can include you (alias + topics only, never content).</div></div>' +
      '<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">' +
      '<span class="seg" role="group" aria-label="' + label + ' visibility">' +
      '<button type="button" data-set="' + key + '" data-vis="public" class="' + (s.visibility === 'public' ? 'on' : '') + '">Public</button>' +
      '<button type="button" data-set="' + key + '" data-vis="private" class="' + (s.visibility === 'private' ? 'on' : '') + '">Private</button></span>' +
      '<span class="seg" role="group" aria-label="' + label + ' findable">' +
      '<button type="button" data-set="' + key + '" data-find="true" class="' + (s.findable ? 'on' : '') + '">Findable</button>' +
      '<button type="button" data-set="' + key + '" data-find="false" class="' + (!s.findable ? 'on' : '') + '">Unfindable</button></span>' +
      '</div></div>';
  }).join('');
  return '<section class="board" id="settings" style="--igc:#ffbf3d"><h2>Your Settings — you hold every switch</h2>' + rows +
    '<div class="saved-note" id="savedNote"></div>' +
    '<script>const CUR=' + JSON.stringify(settings) + ';' +
    'document.querySelectorAll("[data-set]").forEach(b=>b.addEventListener("click",async()=>{' +
    'const page=b.dataset.set;const cur=CUR[page];' +
    'const body={page,visibility:b.dataset.vis?b.dataset.vis:cur.visibility,findable:b.dataset.find!==undefined?(b.dataset.find==="true"):cur.findable};' +
    'const r=await fetch("/api/welcome/settings",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});' +
    'const d=await r.json();if(r.ok){CUR[page]=d.settings[page];document.querySelectorAll("[data-set]").forEach(x=>{if(x.dataset.set!==page)return;if(x.dataset.vis)x.classList.toggle("on",x.dataset.vis===CUR[page].visibility);if(x.dataset.find!==undefined)x.classList.toggle("on",(x.dataset.find==="true")===CUR[page].findable)});document.getElementById("savedNote").textContent="Saved — your "+page+" page is now "+CUR[page].visibility+(CUR[page].findable?" and findable.":" and unfindable.");}else{document.getElementById("savedNote").textContent=d.error||"That did not save — try again.";}}));</script></section>';
}

function renderConnectLayer(world, viewerMatch) {
  const a = world.answers || {};
  const topics = world.topics || [];
  let matchHTML = '';
  if (viewerMatch) {
    matchHTML = '<section class="board" style="--igc:#e84fff"><h2>Your Match With ' + esc(world.name) + '</h2>' +
      '<div class="match-row"><div class="match-main"><div class="match-reason">' + esc((viewerMatch.reasons || []).join(' · ')) + '</div></div>' +
      '<div class="match-pct">' + viewerMatch.pct + '%</div></div></section>';
  }
  const body =
    '<section class="board" style="--igc:#a06bff"><h2>A Private World — Open To Connect</h2>' +
    '<p>' + esc(world.name) + ' keeps this page private — and that is their right, held by design. What the network may know is the connect layer: their alias, what they are about, and that they are here to meet the right people.</p>' +
    (topics.length ? '<div class="chips" style="margin-top:16px">' + topics.map((t) => '<span class="chip">' + esc(t) + '</span>').join('') + '</div>' : '') +
    '<div class="doors" style="margin-top:20px">' +
    '<a class="door" style="--dc:#3fb8ff" href="https://nayanet.live/rooms/mail">✉ Message via Smart Mail</a>' +
    '<a class="door" style="--dc:#2fe89e" href="/world/' + esc(world.alias) + '/business">Their Business</a>' +
    '<a class="door" style="--dc:#ffbf3d" href="/world/' + esc(world.alias) + '/space">Their Space</a>' +
    '<a class="door" style="--dc:#e84fff" href="/welcome">Claim Your Own World</a></div></section>' +
    matchHTML;
  return worldShell({ alias: world.alias, name: world.name, page: 'personal', color: PAGE_COLORS.personal, title: world.name + ' — Connect', motto: a.motto || '', body });
}

function renderPersonal(world, owner, matches, settings) {
  const a = world.answers || {};
  let idx = 0;
  const walk = () => SPECTRUM[idx++ % SPECTRUM.length];
  let body = '';
  body += '<section class="board" id="about" style="--igc:' + walk() + '"><h2>About</h2>' +
    (a.about && String(a.about).trim() ? '<p>' + esc(a.about) + '</p>' : '<p class="empty">Nothing here yet — this world was just born, and its story is theirs to tell.</p>') + '</section>';
  if (a.into && String(a.into).trim()) { const intoText = a.into + (a.into_why && String(a.into_why).trim() ? '\n\nWhy it draws me: ' + a.into_why : ''); body += sectionBoard(idx++, 'What I’m Into', intoText); }
  if ((world.topics || []).length) body += '<section class="board" style="--igc:' + walk() + '"><h2>Topics — what I’m about</h2><div class="chips">' + world.topics.map((t) => '<span class="chip">' + esc(t) + '</span>').join('') + '</div></section>';
  body += sectionBoard(idx++, 'Vision', a.vision);
  body += sectionBoard(idx++, 'Goal', a.goal);
  body += sectionBoard(idx++, 'Mission', a.mission);
  body += '<section class="board" style="--igc:' + walk() + '"><h2>Their Worlds</h2><div class="doors">' +
    '<a class="door" style="--dc:#3fb8ff" href="/world/' + esc(world.alias) + '/business">Business Page</a>' +
    '<a class="door" style="--dc:#2fe89e" href="/world/' + esc(world.alias) + '/space">Their Space</a>' +
    '<a class="door" style="--dc:#ff5e6c" href="https://nayanet.live/rooms/mail">✉ Smart Mail</a></div></section>';
  body += matchesPanel(matches, 'Your Matches');
  body += '<section class="board" style="--igc:#2fe89e"><h2>Want More? — The Smart Factory</h2>' +
    '<p>This system arrived complete — done for you, move-in ready. The Factory is not where your pages come from; it is where your system grows: more personal pages, more businesses (you are never limited to one), more spaces, and smart blocks, smart systems and smart apps attached to your system whenever you want them.</p>' +
    '<div class="doors" style="margin-top:16px"><a class="door" style="--dc:#2fe89e" href="https://nayanet.live/#/hub/factory">The Smart Factory — add pages, blocks and apps</a></div></section>';
  if (owner) body += ownerSettingsBar(world.alias, settings);
  return worldShell({ alias: world.alias, name: world.name, page: 'personal', color: PAGE_COLORS.personal, title: world.name, motto: a.motto || '', body });
}

function renderBusiness(world, owner) {
  const a = world.answers || {};
  let idx = 1;
  let body = '';
  body += '<section class="board" id="about" style="--igc:' + SPECTRUM[idx++ % 7] + '"><h2>What We Do</h2>' +
    (a.biz_do && String(a.biz_do).trim() ? '<p>' + esc(a.biz_do) + '</p>' : '<p class="empty">Nothing here yet — the business story is theirs to tell.</p>') + '</section>';
  body += sectionBoard(idx++, 'Who We Help · What We Offer', a.biz_offer);
  { const bText = (a.biz_building || '') + (a.biz_goal && String(a.biz_goal).trim() ? '\n\nWhere it’s headed: ' + a.biz_goal : ''); if (String(bText).trim()) body += sectionBoard(idx++, 'What We’re Building', bText); }
  body += '<section class="board" style="--igc:' + SPECTRUM[idx++ % 7] + '"><h2>Reach ' + esc(world.name) + '</h2><div class="doors">' +
    '<a class="door" style="--dc:#a06bff" href="/world/' + esc(world.alias) + '">Personal Page</a>' +
    '<a class="door" style="--dc:#2fe89e" href="/world/' + esc(world.alias) + '/space">Their Space</a>' +
    '<a class="door" style="--dc:#ff5e6c" href="https://nayanet.live/rooms/mail">✉ Smart Mail</a></div></section>';
  if (owner) body += ownerSettingsBar(world.alias, world.settings || DEFAULT_SETTINGS);
  return worldShell({ alias: world.alias, name: world.name, page: 'business', color: PAGE_COLORS.business, title: world.name + ' — Business', motto: a.motto || '', body });
}

function renderSpace(world, owner) {
  const a = world.answers || {};
  let idx = 2;
  let body = '';
  body += '<section class="board" id="about" style="--igc:' + SPECTRUM[idx++ % 7] + '"><h2>The Space</h2>' +
    (a.space && String(a.space).trim() ? '<p>' + esc(a.space) + '</p>' : '<p class="empty">This space was just born — its first gathering is yet to come.</p>') + '</section>';
  if ((world.topics || []).length) body += '<section class="board" style="--igc:' + SPECTRUM[idx++ % 7] + '"><h2>What This Space Is About</h2><div class="chips">' + world.topics.map((t) => '<span class="chip">' + esc(t) + '</span>').join('') + '</div></section>';
  body += '<section class="board" style="--igc:' + SPECTRUM[idx++ % 7] + '"><h2>Enter The Conversation</h2><div class="doors">' +
    '<a class="door" style="--dc:#ff9a5a" href="https://nayanet.live/rooms/spaces">Smart Spaces Room</a>' +
    '<a class="door" style="--dc:#a06bff" href="/world/' + esc(world.alias) + '">Personal Page</a>' +
    '<a class="door" style="--dc:#ff5e6c" href="https://nayanet.live/rooms/mail">✉ Smart Mail</a></div>' +
    '<p style="margin-top:14px" class="empty">Spaces are where citizens gather around what they are into. This citizen’s space lives here, and its conversations gather in the Spaces room.</p></section>';
  if (owner) body += ownerSettingsBar(world.alias, world.settings || DEFAULT_SETTINGS);
  return worldShell({ alias: world.alias, name: world.name, page: 'space', color: PAGE_COLORS.space, title: world.name + ' — Space', motto: a.motto || '', body });
}

function renderNotFound(alias) {
  const body = '<section class="board" style="--igc:#a06bff"><h2>No World Here Yet</h2>' +
    '<p>The address nayanet.live/world/' + esc(alias) + ' has not been claimed — no citizen\'s world lives under this name yet. If it should be yours, the welcome takes two minutes and the world is born filled, never empty.</p>' +
    '<div class="doors" style="margin-top:18px"><a class="door" style="--dc:#a06bff" href="/welcome">Begin The Welcome</a></div></section>';
  return worldShell({ alias: alias || 'nayanet', name: 'Not Claimed Yet', page: 'personal', color: '#a06bff', title: 'No world here yet', motto: '', body });
}

// ─── API HANDLERS ──────────────────────────────────────────────────────────
function normSettings(world) {
  const s = (world && world.settings) || {};
  return {
    personal: { ...DEFAULT_SETTINGS.personal, ...(s.personal || {}) },
    business: { ...DEFAULT_SETTINGS.business, ...(s.business || {}) },
    space:    { ...DEFAULT_SETTINGS.space, ...(s.space || {}) }
  };
}
async function parseBody(request) {
  try { const b = await request.json(); return (b && typeof b === 'object') ? b : null; } catch (e) { return null; }
}

const ANSWER_KEYS = ['about', 'into', 'into_why', 'vision', 'goal', 'mission', 'motto', 'biz_do', 'biz_offer', 'biz_building', 'biz_goal', 'space'];
function cleanAnswers(input) {
  const out = {};
  for (const k of ANSWER_KEYS) {
    const v = input && typeof input[k] === 'string' ? input[k].trim() : '';
    out[k] = v.slice(0, 4000);
  }
  return out;
}
function cleanTopics(input) {
  if (!Array.isArray(input)) return [];
  const seen = new Set(); const out = [];
  for (const t of input) {
    const v = String(t || '').trim().toLowerCase().slice(0, 40);
    if (v && !seen.has(v)) { seen.add(v); out.push(v); }
    if (out.length >= 12) break;
  }
  return out;
}

async function apiComplete(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read your answers — they are still on your screen; try once more.');
  const auth = await authCitizen(env, body);
  if (auth.error) return auth.error;
  const id = auth.id;
  const alias = id.alias;
  const existing = await getWorld(env, alias);
  const settings = existing ? normSettings(existing) : JSON.parse(JSON.stringify(DEFAULT_SETTINGS));
  const world = {
    alias, name: id.name,
    answers: cleanAnswers(body.answers),
    topics: cleanTopics(body.topics),
    settings, updated_at: new Date().toISOString()
  };
  const up = await sb(env, 'POST', 'citizen_worlds', world, 'resolution=merge-duplicates,return=representation');
  if (!up.ok || !Array.isArray(up.data) || !up.data.length) {
    return err(500, 'Something went wrong on our side while building your world — your answers are still on your screen. Please try once more.');
  }
  const saved = up.data[0];
  saved.settings = normSettings(saved);
  const matches = await matchesFor(env, saved);
  return json(200, {
    pages: { personal: '/world/' + alias, business: '/world/' + alias + '/business', space: '/world/' + alias + '/space' },
    matches, settings: saved.settings
  });
}

async function apiSettings(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read that change — try again.');
  const auth = await authCitizen(env, body);
  if (auth.error) return auth.error;
  const id = auth.id;
  const page = body.page;
  if (!['personal', 'business', 'space'].includes(page)) return err(400, 'That page name is not one of yours.');
  const visibility = body.visibility === 'private' ? 'private' : 'public';
  const findable = body.findable === true;
  const world = await getWorld(env, id.alias);
  if (!world) return err(404, 'Your world has not been built yet — finish the welcome first.');
  const settings = normSettings(world);
  settings[page] = { visibility, findable };
  const up = await sb(env, 'PATCH', 'citizen_worlds?alias=eq.' + encodeURIComponent(id.alias), { settings, updated_at: new Date().toISOString() });
  if (!up.ok) return err(500, 'That did not save on our side — please try again in a moment.');
  return json(200, { ok: true, settings });
}

async function apiMe(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read that — reload the welcome and try again.');
  const alias = typeof body.alias === 'string' ? body.alias.trim().toLowerCase() : '';
  if (!NAME_RE.test(alias)) return err(400, 'That alias does not look right.');
  const id = await getIdentity(env, alias);
  if (!id) return err(404, 'That alias is not certified yet.');
  const world = await getWorld(env, alias);
  const key = typeof body.device_key === 'string' ? body.device_key : '';
  return json(200, {
    name: id.name, alias: id.alias, cert_no: id.cert_no, created_at: id.created_at,
    has_world: !!world, owner: !!key && key === id.device_key
  });
}

// The owner's own view of their world pages, delivered only to the
// device that holds the identity — private content never rides in the
// anonymous server render; it arrives here, after the credential check.
async function apiOwner(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read that — try again.');
  const auth = await authCitizen(env, body);
  if (auth.error) return auth.error;
  const page = ['personal', 'business', 'space'].includes(body.page) ? body.page : 'personal';
  const world = await getWorld(env, auth.id.alias);
  if (!world) return json(200, { html: '', settings: null });
  world.settings = normSettings(world);
  const settings = world.settings;
  let fragment;
  if (page === 'personal') {
    const matches = await matchesFor(env, world);
    fragment = personalBody(world, matches, settings, true);
  } else if (settings[page].visibility === 'private') {
    fragment = page === 'business' ? businessBody(world, settings, true) : spaceBody(world, settings, true);
  } else {
    fragment = ownerSettingsBar(world.alias, settings);
  }
  return json(200, { html: fragment, settings });
}

// ─── WORLD ROUTES ──────────────────────────────────────────────────────────
async function worldPage(request, env, alias, page) {
  const world = await getWorld(env, alias);
  if (!world) return html(404, renderNotFound(alias));
  world.settings = normSettings(world);
  const s = world.settings[page];
  if (s.visibility === 'private') {
    // Server-side privacy: anyone but the owner gets the connect layer
    // only. The owner upgrades in place via /api/welcome/owner, on the
    // real claim's credential — private answers never ship anonymously.
    return html(200, renderConnectLayer(world, null));
  }
  if (page === 'personal') {
    const matches = await matchesFor(env, world);
    return html(200, renderPersonal(world, matches, world.settings));
  }
  if (page === 'business') return html(200, renderBusiness(world, world.settings));
  return html(200, renderSpace(world, world.settings));
}

// ─── ROUTER ────────────────────────────────────────────────────────────────
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (!env.SUPABASE_SERVICE_ROLE_KEY) {
      const msg = 'The welcome is not fully switched on yet — please try again later.';
      return path.startsWith('/api/') ? err(500, msg) : html(500, '<body style="background:#040405;color:#fff;font-family:Georgia,serif;padding:44px"><h1>' + msg + '</h1></body>');
    }
    if (path === '/welcome' && request.method === 'GET') return html(200, WALK_HTML);
    if (path === '/api/welcome/me' && request.method === 'POST') return apiMe(request, env);
    if (path === '/api/welcome/complete' && request.method === 'POST') return apiComplete(request, env);
    if (path === '/api/welcome/settings' && request.method === 'POST') return apiSettings(request, env);
    if (path === '/api/welcome/owner' && request.method === 'POST') return apiOwner(request, env);
    const m = path.match(/^\/world\/([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(?:\/(business|space))?\/?$/);
    if (m && request.method === 'GET') return worldPage(request, env, m[1], m[2] || 'personal');
    if (path.startsWith('/world/')) return html(404, renderNotFound(path.split('/')[2] || ''));
    return html(404, '<body style="background:#040405;color:#fff;font-family:Georgia,serif;padding:44px"><h1>Nothing lives at this address.</h1><p><a style="color:#a06bff" href="/welcome">The Official Welcome →</a></p></body>');
  }
};
