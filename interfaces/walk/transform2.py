#!/usr/bin/env python3
"""Stage 2 of the Welcome-Right build: finish the server transform on
server-stage1.js — worldShell gains the owner-upgrade script + #worldRoot,
ownerSettingsBar loses its cookie-era inline script (the shell's delegated
binder owns settings now), and the world renderers split into body
builders (reused by /api/welcome/owner) + shell wrappers. Finally the
assembled walk document is embedded and worker.js is written."""
import json, os

HERE = "/home/hatch/workspace/welcome-build"
# Candidate builds MUST NOT overwrite the live worker.js: set WORKER_OUT to
# write elsewhere (e.g. worker-LIVE-CANDIDATE.js). Default keeps old behavior.
WORKER_OUT = os.environ.get('WORKER_OUT', HERE + '/worker.js')
srv = open(HERE + "/server-stage1.js").read()

def replace_between(s, a, b, new):
    i = s.index(a); j = s.index(b, i)
    return s[:i] + new + s[j:]

# ---------------------------------------------------------------- worldShell
WORLD_SHELL = r"""function worldShell(opts) {
  // opts: alias, name, page ('personal'|'business'|'space'), color, title, motto, body, layer
  const pc = opts.color;
  const layer = opts.layer || 'full';
  // The owner upgrade: the page ships privacy-safe; if THIS device holds
  // the page's own identity (the Hub's localStorage store), the full
  // owner view is fetched from /api/welcome/owner on the real claim's
  // credential and swapped in. Settings clicks are bound here, once.
  const ownerScript = '<script>(function(){' +
    'var PA=' + JSON.stringify(opts.alias) + ',PG=' + JSON.stringify(opts.page) + ',LG=' + JSON.stringify(layer) + ';' +
    'function ls(k){try{return localStorage.getItem(k)||""}catch(e){return""}}' +
    'var al=(ls("nayanet_smart_alias")||"").trim().toLowerCase();if(!al||al!==PA)return;' +
    'var cred={alias:al,device_key:ls("nayanet_vault_key"),name:ls("nayanet_smart_name")};var SET=null;' +
    'function bind(){document.querySelectorAll("[data-set]").forEach(function(b){b.addEventListener("click",async function(){if(!SET)return;var pg=b.dataset.set,cur=SET[pg];var body=Object.assign({},cred,{page:pg,visibility:b.dataset.vis?b.dataset.vis:cur.visibility,findable:b.dataset.find!==undefined?(b.dataset.find==="true"):cur.findable});var r=await fetch("/api/welcome/settings",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});var d={};try{d=await r.json()}catch(e){}var note=document.getElementById("savedNote");if(r.ok&&d.settings){SET=d.settings;document.querySelectorAll("[data-set]").forEach(function(x){if(x.dataset.set!==pg)return;if(x.dataset.vis)x.classList.toggle("on",x.dataset.vis===SET[pg].visibility);if(x.dataset.find!==undefined)x.classList.toggle("on",(x.dataset.find==="true")===SET[pg].findable)});if(note)note.textContent="Saved \u2014 your "+pg+" page is now "+SET[pg].visibility+(SET[pg].findable?" and findable.":" and unfindable.");}else if(note){note.textContent=d.error||"That did not save \u2014 try again."}})});}' +
    'fetch("/api/welcome/owner",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.assign({},cred,{page:PG}))}).then(function(r){return r.json()}).then(function(d){if(!d||!d.html)return;SET=d.settings||null;var root=document.getElementById("worldRoot");if(!root)return;if(PG==="personal"||LG==="connect"){root.innerHTML=d.html}else{dv=document.createElement("div");dv.innerHTML=d.html;root.appendChild(dv)}bind();}).catch(function(){});' +
    '})();</' + 'script>';
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
    '<div class="wrap">' + tabsRow(opts.alias, opts.page) + '<div id="worldRoot">' + opts.body + '</div></div>' +
    '<footer class="foot"><span>NAYANET — THE NEW NET</span><span>ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</span></footer>' +
    '<script>let dp;window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();dp=e});function installApp(){if(dp){dp.prompt();dp=null}else{alert("To install: open your browser menu and choose \\u201cAdd to Home Screen\\u201d.")}}</script>' +
    ownerScript +
    '</body></html>';
}

"""
srv = replace_between(srv, 'function worldShell(opts) {', '// ─── WORLD PAGE RENDERERS', WORLD_SHELL)

# ---------------------------------------------------------------- settings bar (scriptless)
SETTINGS_BAR = r"""function ownerSettingsBar(alias, settings) {
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
    '<div class="saved-note" id="savedNote"></div></section>';
}

"""
srv = replace_between(srv, 'function ownerSettingsBar', 'function renderConnectLayer', SETTINGS_BAR)

# ---------------------------------------------------------------- body builders
PERSONAL = r"""function personalBody(world, matches, settings, owner) {
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
  return body;
}
function renderPersonal(world, matches, settings) {
  const a = world.answers || {};
  return worldShell({ alias: world.alias, name: world.name, page: 'personal', color: PAGE_COLORS.personal, title: world.name, motto: a.motto || '', body: personalBody(world, matches, settings, false), layer: 'full' });
}

"""
srv = replace_between(srv, 'function renderPersonal', 'function renderBusiness', PERSONAL)

BUSINESS = r"""function businessBody(world, settings, owner) {
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
  if (owner) body += ownerSettingsBar(world.alias, settings);
  return body;
}
function renderBusiness(world, settings) {
  const a = world.answers || {};
  return worldShell({ alias: world.alias, name: world.name, page: 'business', color: PAGE_COLORS.business, title: world.name + ' — Business', motto: a.motto || '', body: businessBody(world, settings, false), layer: 'full' });
}

"""
srv = replace_between(srv, 'function renderBusiness', 'function renderSpace', BUSINESS)

SPACE = r"""function spaceBody(world, settings, owner) {
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
  if (owner) body += ownerSettingsBar(world.alias, settings);
  return body;
}
function renderSpace(world, settings) {
  const a = world.answers || {};
  return worldShell({ alias: world.alias, name: world.name, page: 'space', color: PAGE_COLORS.space, title: world.name + ' — Space', motto: a.motto || '', body: spaceBody(world, settings, false), layer: 'full' });
}

"""
srv = replace_between(srv, 'function renderSpace', 'function renderNotFound', SPACE)

# connect layer must declare its layer so the owner upgrade replaces (not appends)
old_conn = "title: world.name + ' — Connect', motto:"
assert srv.count(old_conn) == 1
srv = srv.replace(old_conn, "title: world.name + ' — Connect', layer: 'connect', motto:", 1)

# ---------------------------------------------------------------- THE JOINING (2026-10-24)
# Bind Power's activation engine (branch naya-power/welcome-engine-v1,
# scorecarded 9.5) to the walk's completion: the v1 matcher block is
# replaced by a faithful JS port of smart_match.py v1.4 (concept tier
# included), and apiComplete gains the engine's activation receipts —
# idempotent ambassador issuance + coverage accounting. The walk's
# questions, flow, face and design are untouched.
MATCHER_V14 = r"""// ─── SMART MATCH v1.4 — the engine port (THE JOINING, 2026-10-24) ─────────
// Faithful JS port of the engine matcher (tools/welcome-engine/
// smart_match.py, branch naya-power/welcome-engine-v1), so the walk scores
// EXACTLY what the engine scores. Weights 40/25/20/15. Topics and goals
// are two-tier: raw = 50% phrase overlap + 50% word overlap; family = 50%
// raw + 50% concept coverage — and the concept tier stays SILENT when
// neither side touches the taxonomy (a taxonomy gap is not misalignment).
// Offers<->needs and wants use signature overlap (declared terms +
// concepts + stemmed content words, glue words stoplisted). A match
// surfaces only on >= 2 independent signals. Reasons always ride along.
const SM_WEIGHTS = { topics: 0.40, goals: 0.25, offers_needs: 0.20, wants: 0.15 };
const SM_TAXONOMY = {
  MAKING: ['building', 'creation', 'templates', 'apps', 'step 7', 'app creation'],
  SHIPPING: ['execution', 'delivery', 'ship', 'waves', 'build loop'],
  PROVING: ['testing', 'validation', 'quality', 'quality control', 'evidence', 'proof', 'verification', 'audit'],
  CONNECTING: ['integration', 'systems', 'network', 'coordination', 'the platform'],
  SPEAKING: ['voice', 'speech', 'audio', 'streaming', 'synthesis', 'ear test'],
  TALKING: ['mail', 'messaging', 'communication', 'conversation', 'questions', 'answers', 'listening', 'scheduling'],
  THINKING: ['distillation', 'essence', 'reflection', 'learning', 'analysis', 'critical thinking', 'root cause', 'derivation', 'project intelligence'],
  CLEARING: ['blockers', 'problem solving', 'conflict resolution', 'risk', 'risk review', 'reliability', 'unblocking'],
  GUIDING: ['strategy', 'project leadership', 'orientation', 'home', 'long-term strategy', 'design'],
  DECIDING: ['performance rulings', 'governance', 'decisions'],
  PUBLISHING: ['smart notes', 'feed', 'publishing', 'flow', 'publishing path', 'notes'],
  PEOPLE: ['citizens', 'usage', 'readers', 'material']
};
const SM_TERM2CONCEPTS = {};
for (const [c, terms] of Object.entries(SM_TAXONOMY)) for (const t of terms) (SM_TERM2CONCEPTS[t] = SM_TERM2CONCEPTS[t] || new Set()).add(c);
function smConceptsOf(terms) {
  const out = new Set();
  for (const t of terms || []) { const cs = SM_TERM2CONCEPTS[t]; if (cs) for (const c of cs) out.add(c); }
  return out;
}
function smCoeff(A, B) {
  if (!A.size || !B.size) return { ratio: 0, shared: [] };
  const shared = [...A].filter((x) => B.has(x)).sort();
  return { ratio: shared.length / Math.min(A.size, B.size), shared };
}
function smStem(w) {
  if (w.length > 5 && w.endsWith('ing')) {
    w = w.slice(0, -3);
    if (w.length > 3 && w[w.length - 1] === w[w.length - 2]) w = w.slice(0, -1);
  } else if (w.length > 4 && w.endsWith('ies')) {
    w = w.slice(0, -3) + 'y';
  } else if (w.length > 3 && w.endsWith('s') && !w.endsWith('ss')) {
    w = w.slice(0, -1);
  }
  return w;
}
function smWords(terms) {
  const out = new Set();
  for (const t of terms || []) {
    for (const w of String(t).toLowerCase().replace(/,/g, ' ').split(/\s+/)) {
      if (w.length > 2) out.add(smStem(w));
    }
  }
  return out;
}
function smFamily(aTerms, bTerms) {
  const phrase = smCoeff(new Set(aTerms || []), new Set(bTerms || []));
  const word = smCoeff(smWords(aTerms), smWords(bTerms));
  const raw = 0.5 * phrase.ratio + 0.5 * word.ratio;
  const rawShared = [...new Set([...phrase.shared, ...word.shared])].sort();
  const ca = smConceptsOf(aTerms), cb = smConceptsOf(bTerms);
  if (!ca.size && !cb.size) return { score: raw, rawShared, conShared: [] };
  const con = smCoeff(ca, cb);
  return { score: 0.5 * raw + 0.5 * con.ratio, rawShared, conShared: con.shared };
}
const SM_CROSS_STOPWORDS = new Set(['help', 'want', 'wants', 'need', 'needs', 'people', 'person', 'someone', 'others', 'with', 'from', 'that', 'this', 'more']);
function smCrossSig(terms) {
  const sig = new Set(terms || []);
  for (const c of smConceptsOf(terms)) sig.add(c);
  for (const t of terms || []) {
    for (const w of String(t).toLowerCase().replace(/,/g, ' ').split(/\s+/)) {
      if (w.length > 3 && !SM_CROSS_STOPWORDS.has(w)) sig.add(smStem(w));
    }
  }
  return sig;
}
function smCross(aTerms, bTerms) { return smCoeff(smCrossSig(aTerms), smCrossSig(bTerms)); }
function smPyRound(x) {
  // Python's round() — half-to-even — so walk scores agree with the
  // engine's to the point, not just within it.
  const f = Math.floor(x), d = x - f;
  if (d < 0.5) return f;
  if (d > 0.5) return f + 1;
  return f % 2 === 0 ? f : f + 1;
}
function smScore(a, b) {
  const t = smFamily(a.topics, b.topics);
  const g = smFamily(a.goals, b.goals);
  const on1 = smCross(a.offers, b.needs), on2 = smCross(b.offers, a.needs);
  const on = (on1.ratio + on2.ratio) / 2;
  const w1 = smCross(a.wants, [...(b.topics || []), ...(b.offers || [])]);
  const w2 = smCross(b.wants, [...(a.topics || []), ...(a.offers || [])]);
  const w = (w1.ratio + w2.ratio) / 2;
  const parts = { topics: t.score, goals: g.score, offers_needs: on, wants: w };
  const relevance = smPyRound(100 * (SM_WEIGHTS.topics * parts.topics + SM_WEIGHTS.goals * parts.goals + SM_WEIGHTS.offers_needs * parts.offers_needs + SM_WEIGHTS.wants * parts.wants));
  const signals = Object.keys(parts).filter((k) => parts[k] > 0);
  const reasons = [];
  const shared = [...new Set([...t.rawShared, ...t.conShared])].sort();
  if (shared.length) reasons.push('shared: ' + shared.slice(0, 5).join(', '));
  const gshared = [...new Set([...g.rawShared, ...g.conShared])].sort();
  if (gshared.length) reasons.push('shared goals: ' + gshared.slice(0, 3).join(', '));
  const fits = [...new Set([...on1.shared, ...on2.shared])].sort();
  if (fits.length) reasons.push('offer/need fit: ' + fits.slice(0, 3).join(', '));
  const wanted = [...new Set([...w1.shared, ...w2.shared])].sort();
  if (wanted.length) reasons.push('wanted connection: ' + wanted.slice(0, 3).join(', '));
  return { score: relevance, rank: relevance, signals, surface: signals.length >= 2, parts, reasons };
}
// The engine's phrase extraction (welcome_engine.extract_phrases):
// split on commas/semicolons/'and', strip one conversational lead-in,
// keep phrases of <= 7 words.
const SM_LEAD_INS = ['i love ', "i'm into ", 'i am into ', 'im into ', 'my goal is ', 'my mission is ', 'my vision is ', 'i want to ', 'i want ', 'i do ', "i'm ", 'i am ', 'my motto is '];
function smExtractPhrases(text) {
  if (!text) return [];
  const out = [];
  for (let c of String(text).split(/[,;•\n]| and /)) {
    c = c.trim().toLowerCase().split(/\s+/).filter(Boolean).join(' ');
    for (const lead of SM_LEAD_INS) { if (c.startsWith(lead)) { c = c.slice(lead.length); break; } }
    c = c.replace(/^[ .!]+/, '').replace(/[ .!]+$/, '');
    if (c && c.split(' ').length <= 7 && c.length > 1) out.push(c);
  }
  return out;
}
// A citizen's world -> the engine's profile vector. The engine's slot map
// (welcome_engine.SLOTS) translated to the walk's ten questions:
//   topics <- topic chips + phrases(into) + phrases(space)
//   goals  <- phrases(goal) + phrases(vision) + phrases(mission) + phrases(biz_goal)
//   offers <- phrases(biz_do) + phrases(biz_offer)
//   needs  <- (the walk asks no needs question — honestly empty)
//   wants  <- phrases(space) (Q10 asks who you want to meet, same breath)
function smBuildVector(world) {
  const a = (world && world.answers) || {};
  const uniq = (arr) => [...new Set(arr)].sort();
  return {
    topics: uniq([...(world.topics || []).map((t) => String(t).toLowerCase().trim()).filter(Boolean), ...smExtractPhrases(a.into), ...smExtractPhrases(a.space)]),
    goals: uniq([...smExtractPhrases(a.goal), ...smExtractPhrases(a.vision), ...smExtractPhrases(a.mission), ...smExtractPhrases(a.biz_goal)]),
    offers: uniq([...smExtractPhrases(a.biz_do), ...smExtractPhrases(a.biz_offer)]),
    needs: [],
    wants: uniq(smExtractPhrases(a.space))
  };
}
// Coverage accounting — the engine's coverage() with its PAGE_FIELDS
// translated to the walk's answers. personal.values has no walk source:
// the walk never asks it, so it is named "missing" — exactly as the
// engine names unasked fields, never papered over. Business fields are
// accounted only when a business was declared (any business answer
// given), mirroring the engine's has_business gate. States: filled /
// filled_thin (<3 words — counts as filled, named as a follow-up
// candidate) / skipped (asked, left empty) / missing (never asked).
function smCoverageFor(world) {
  const a = (world && world.answers) || {};
  const val = (k) => (typeof a[k] === 'string' ? a[k] : '');
  const bizDesc = [val('biz_do'), val('biz_offer')].filter((s) => s.trim()).join(' ');
  const hasBiz = !!(val('biz_do').trim() || val('biz_offer').trim() || val('biz_building').trim() || val('biz_goal').trim());
  const src = [
    ['personal.topics', val('into').trim() ? val('into') : (world.topics || []).join(', ')],
    ['personal.values', null],
    ['personal.goal', val('goal')],
    ['personal.vision', val('vision')],
    ['personal.mission', val('mission')],
    ['personal.motto', val('motto')],
    ['personal.what_i_do', val('biz_do')],
    ['personal.offers', val('biz_offer')],
    ['business.description', bizDesc],
    ['business.goal', val('biz_goal')],
    ['space.purpose', val('space')]
  ];
  const fields = {}; const thin = [];
  for (const [name, text] of src) {
    if (name.startsWith('business.') && !hasBiz) continue;
    if (text === null) { fields[name] = 'missing'; continue; }
    if (text.trim()) {
      if (text.trim().split(/\s+/).length < 3) { fields[name] = 'filled_thin'; thin.push(name); }
      else fields[name] = 'filled';
    } else fields[name] = 'skipped';
  }
  const states = Object.values(fields);
  const total = states.length;
  const filled = states.filter((s) => s.startsWith('filled')).length;
  const accounted = states.filter((s) => s !== 'missing').length;
  return { fields, thin, filled_pct: total ? smPyRound(100 * filled / total) : 100, accounted_pct: total ? smPyRound(100 * accounted / total) : 100 };
}
function computeMatches(me, candidates) {
  const myVec = smBuildVector(me);
  const out = [];
  for (const c of candidates) {
    if (c.alias === me.alias) continue;
    const r = smScore(myVec, smBuildVector(c));
    if (!r.surface) continue;
    out.push({ alias: c.alias, name: c.name, pct: Math.min(100, r.score), reasons: r.reasons.slice(0, 3), topics: c.topics || [] });
  }
  out.sort((x, y) => (y.pct - x.pct) || (x.alias < y.alias ? -1 : x.alias > y.alias ? 1 : 0));
  return out.slice(0, 5);
}
async function matchesFor(env, world) {
  const r = await sb(env, 'GET', 'citizen_worlds?select=alias,name,answers,topics,settings&limit=500');
  const rows = (r.ok && Array.isArray(r.data)) ? r.data : [];
  const findable = rows.filter((w) => w.settings && w.settings.personal && w.settings.personal.findable === true);
  return computeMatches(world, findable);
}

"""
srv = replace_between(srv, '// ─── MATCHES (v1', '// ─── DETERMINISTIC JEWEL COVER', MATCHER_V14)

API_COMPLETE_JOINED = """async function apiComplete(request, env) {
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
  // THE JOINING — activation, the engine's contract (SET B): the
  // citizen's ambassador link is issued at completion, idempotently —
  // the registry's own pattern (on conflict do nothing; alias is the
  // primary key) — and the coverage accounting rides the receipt.
  const ambassadorLink = 'https://nayanet.live/joinus?ref=' + alias;
  const ambRow = await sb(env, 'GET', 'ambassador_links?alias=eq.' + encodeURIComponent(alias) + '&select=alias');
  if (!(ambRow.ok && Array.isArray(ambRow.data) && ambRow.data.length)) {
    await sb(env, 'POST', 'ambassador_links', { alias, link_url: ambassadorLink }, 'resolution=ignore-duplicates,return=minimal');
  }
  const coverage = smCoverageFor(saved);
  const matches = await matchesFor(env, saved);
  return json(200, {
    pages: { personal: '/world/' + alias, business: '/world/' + alias + '/business', space: '/world/' + alias + '/space' },
    matches, settings: saved.settings,
    ambassador_link: ambassadorLink, coverage
  });
}

"""
srv = replace_between(srv, 'async function apiComplete', 'async function apiSettings', API_COMPLETE_JOINED)
print("joining checks:",
      "| smScore:", srv.count('function smScore'),
      "| concept tier:", srv.count('SM_TAXONOMY'),
      "| coverage fn:", srv.count('function smCoverageFor'),
      "| ambassador issuance:", srv.count('ambassador_links'),
      "| old tokenize gone:", srv.count('function tokenize'))

# ─── FLAGSHIP WORLD PAGES (2026-10-24, Shawn-ordered correction) ───
# The /world renderer used to invent thin pages (~14.5 KB) + an invented
# jewel SVG cover. It now renders the REAL flagship pages whole (the
# ~602 KB living app at nayanet.live/personal|business|space), with only
# the middle data regions filled from the citizen's stored world and the
# citizen's real cover (from the Smart Note cover system, geometry ported
# from factory-pipeline/generate-share-card.py) in the cover slot.
# Pipeline note: this section runs AFTER the JOINING block and AFTER the
# stage-2 world surgeries, and its sweep supersedes them (their functions
# live inside the swept region). It runs BEFORE the walk embed.
FLAGSHIP_JS = r"""
// ── FLAGSHIP WORLD PAGES ──
// Template: the live flagship Personal document, EMBEDDED AT BUILD TIME.
// Why not fetched at request time: diagnosed 2026-10-24 (via a temporary
// __tpldiag endpoint, since removed) — a subrequest from inside this
// worker to https://nayanet.live/personal returns the HUB document
// (5,308,126 bytes, title 'NayaNET — The Intelligent Hub'), NOT the
// flagship, under both default and browser User-Agents. Same-zone worker
// subrequests do not take the /personal → naya-model-personal route, so
// a runtime fetch would poison every world page with the Hub shell.
// The build fetches the live bytes (validated on markers) and embeds
// them; when the flagship shell itself changes, re-run this pipeline and
// redeploy. One template serves all three pages; the page delta set
// (accent tokens, avatar letter/stroke, My/Our wording, demo identity)
// is applied at render time.
const FLAGSHIP_TEMPLATE = __FLAGSHIP_TEMPLATE_JSON__;
const FLAGSHIP_PAGE = {
  personal: { gem: '#9d6bff', accent: '#a06bff', mine: 'My', ours: 'My' },
  business: { gem: '#3fb8ff', accent: '#3fb8ff', mine: 'My', ours: 'Our' },
  space:    { gem: '#2fe89e', accent: '#2fe89e', mine: 'My', ours: 'Our' }
};
const DEMO_STRINGS = ['Nova Reyes', 'Acme Corp', 'Our Community',
  'flagship-personal', 'flagship-business', 'flagship-community'];

async function flagshipTemplate() { return FLAGSHIP_TEMPLATE; }

// ── The Smart Note cover system, as a deterministic SVG ──
// Geometry ported from factory-pipeline/generate-share-card.py (the
// LOCKED standard: 1200x630; black-diamond ground; diamond-N emblem in
// a ring at centre-top; NAYANET.LIVE; title <=2 lines; body <=3 lines
// centred in the band below the title; five spectrum gems at the bottom)
// and generate-space-cover.py (accent glow behind the emblem + accent
// title underline). Same ground, same emblem, same typography treatment,
// same gems — with the citizen's own title/text in place of the note's.
function coverSVG(title, body, accent) {
  const ac = accent || '#a06bff';
  const GEMS = ['#e84fff', '#a06bff', '#3fb8ff', '#2fe89e', '#ffbf3d'];
  const ex = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const wrap = (text, max) => {
    const words = String(text || '').split(/\s+/).filter(Boolean);
    const lines = []; let cur = '';
    for (const w of words) {
      const t = cur ? cur + ' ' + w : w;
      if (t.length > max && cur) { lines.push(cur); cur = w; } else cur = t;
    }
    if (cur) lines.push(cur);
    return lines;
  };
  let tLines = wrap(title, 36); let tSize = 48; let tLH = 58;
  if (tLines.length > 2) { tLines = wrap(title, 44); tSize = 40; tLH = 50; }
  if (tLines.length > 2) { tLines = tLines.slice(0, 2); if (tLines[1].length > 44) tLines[1] = tLines[1].slice(0, 43) + '…'; }
  const bLines = wrap(body, 72).slice(0, 3);
  const titleTop = 225;
  const titleEnd = titleTop + tLines.length * tLH;
  const bandTop = titleEnd + 10, bandBottom = 440;
  const bTop = bandTop + Math.max(0, Math.floor((bandBottom - bandTop - bLines.length * 30) / 2));
  // Faceted black ground, seeded by the title — deterministic per citizen.
  let h = 2166136261; const seedStr = String(title || '');
  for (let i = 0; i < seedStr.length; i++) { h ^= seedStr.charCodeAt(i); h = Math.imul(h, 16777619); }
  const rnd = () => { h |= 0; h = (h + 0x6D2B79F5) | 0; let t = Math.imul(h ^ (h >>> 15), 1 | h); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const tones = ['#0a0a12', '#101018', '#14101f', '#0d1420', '#12121c', '#0b0b10', '#181826', '#1c1626', '#0f1a24'];
  // Dense crystalline field: a jittered grid, two triangles per cell,
  // edge to edge — the PIL generator's photographic black-diamond ground,
  // approximated in vector (the worker cannot run PIL at request time).
  // A few thin glint edges carry the crystalline read.
  let facets = '';
  const cols = 12, rows = 6, cw = 1200 / cols, ch = 630 / rows;
  const grid = [];
  for (let gy = 0; gy <= rows; gy++) {
    grid[gy] = [];
    for (let gx = 0; gx <= cols; gx++) {
      grid[gy][gx] = [gx * cw + (gx > 0 && gx < cols ? (rnd() - 0.5) * cw * 0.7 : 0),
                      gy * ch + (gy > 0 && gy < rows ? (rnd() - 0.5) * ch * 0.7 : 0)];
    }
  }
  const pt = (p) => Math.round(p[0]) + ',' + Math.round(p[1]);
  for (let gy = 0; gy < rows; gy++) {
    for (let gx = 0; gx < cols; gx++) {
      const a = grid[gy][gx], b = grid[gy][gx + 1], c = grid[gy + 1][gx], d = grid[gy + 1][gx + 1];
      const t1 = tones[Math.floor(rnd() * tones.length)], t2 = tones[Math.floor(rnd() * tones.length)];
      facets += '<polygon points="' + pt(a) + ' ' + pt(b) + ' ' + pt(d) + '" fill="' + t1 + '"/>';
      facets += '<polygon points="' + pt(a) + ' ' + pt(d) + ' ' + pt(c) + '" fill="' + t2 + '"/>';
    }
  }
  for (let i = 0; i < 14; i++) {
    const gx = 1 + Math.floor(rnd() * (cols - 1)), gy = 1 + Math.floor(rnd() * (rows - 1));
    facets += '<line x1="' + Math.round(grid[gy][gx][0]) + '" y1="' + Math.round(grid[gy][gx][1]) + '" x2="' + Math.round(grid[gy][gx + 1][0]) + '" y2="' + Math.round(grid[gy][gx + 1][1]) + '" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>';
  }
  // Accent glow behind the emblem: a soft radial falloff (the space-cover
  // treatment), never a solid blob.
  const glow = '<defs><radialGradient id="acg" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="' + ac + '" stop-opacity="0.28"/><stop offset="100%" stop-color="' + ac + '" stop-opacity="0"/></radialGradient></defs>' +
    '<ellipse cx="600" cy="95" rx="150" ry="105" fill="url(#acg)"/>';
  const emblem = '<circle cx="600" cy="95" r="70" fill="#0b0b11" stroke="' + ac + '" stroke-width="3"/>' +
    '<polygon points="600,28 668,95 600,162 532,95" fill="none" stroke="' + ac + '" stroke-width="5"/>' +
    '<text x="600" y="126" font-family="Georgia, serif" font-size="84" font-weight="700" fill="#ffffff" text-anchor="middle">N</text>';
  const brand = '<text x="600" y="196" font-family="DejaVu Sans, Arial, sans-serif" font-size="24" font-weight="700" letter-spacing="3" fill="#ffffff" text-anchor="middle">NAYANET.LIVE</text>';
  let titleSvg = '';
  tLines.forEach((ln, i) => {
    titleSvg += '<text x="600" y="' + (titleTop + 38 + i * tLH) + '" font-family="DejaVu Sans, Arial, sans-serif" font-size="' + tSize + '" font-weight="700" fill="#ffffff" text-anchor="middle">' + ex(ln) + '</text>';
  });
  const underline = '<rect x="520" y="' + (titleEnd + 14) + '" width="160" height="4" fill="' + ac + '"/>';
  let bodySvg = '';
  bLines.forEach((ln, i) => {
    bodySvg += '<text x="600" y="' + (bTop + 17 + i * 30) + '" font-family="DejaVu Sans, Arial, sans-serif" font-size="21" fill="#e8e8ec" text-anchor="middle">' + ex(ln) + '</text>';
  });
  let gems = '';
  GEMS.forEach((g, i) => {
    const cx = 600 + (i - 2) * 95, cy = 482;
    gems += '<g><polygon points="' + cx + ',445 ' + (cx + 37) + ',482 ' + cx + ',519 ' + (cx - 37) + ',482" fill="' + g + '" opacity="0.92" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>' +
      '<polygon points="' + cx + ',464 ' + (cx + 18) + ',482 ' + cx + ',500 ' + (cx - 18) + ',482" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/></g>';
  });
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">' +
    '<rect width="1200" height="630" fill="#050507"/>' + facets + glow + emblem + brand + titleSvg + underline + bodySvg + gems + '</svg>';
}

// ── Flagship render: whole shell, middle swapped ──
function renderFlagshipDoc(tpl, world, page, matches) {
  const cfg = FLAGSHIP_PAGE[page] || FLAGSHIP_PAGE.personal;
  const a = world.answers || {};
  const topics = world.topics || [];
  const has = (v) => String(v == null ? '' : v).trim().length > 0;
  const first = (v, n) => String(v || '').slice(0, n);
  // Page-slot mapping, verbatim from the walk's answers.
  let slots, tagline, coverBody;
  if (page === 'business') {
    slots = { motto: a.motto, story: a.biz_do, about: a.biz_offer, goals: a.biz_goal, mission: a.biz_building, vision: a.vision, love: topics.join(', ') };
    tagline = a.motto || first(a.biz_do, 120);
    coverBody = a.biz_do || a.biz_offer || '';
  } else if (page === 'space') {
    slots = { motto: a.motto, story: a.space, about: topics.join(', '), goals: a.goal, mission: a.mission, vision: a.vision, love: '' };
    tagline = a.motto || first(a.space, 120);
    coverBody = a.space || a.motto || '';
  } else {
    // About slot is built pre-escaped (esc on each answer part; the <br>
    // separators are structural, not citizen text) and inserted verbatim.
    slots = { motto: a.motto, story: a.about, about: (has(a.into) ? esc(a.into) : '') + (has(a.into_why) ? (has(a.into) ? '<br><br>Why it draws me: ' : '') + esc(a.into_why) : ''), goals: a.goal, mission: a.mission, vision: a.vision, love: topics.join(', ') };
    tagline = a.motto || first(a.about, 120);
    coverBody = a.motto || a.about || '';
  }
  let doc = tpl;
  // Display-only: the flagship's wall welcome post stores its [[fm-auto]]
  // dedup token verbatim in the note (renaming it would re-fire the post);
  // the wall card must never show the token to a visitor. Storage and the
  // guard query are untouched — only the displayed body is stripped.
  doc = doc.split("esc(j.b||'')").join("esc((j.b||'').replace(/^\\[\\[fm-auto\\]\\]\\s*/,''))");
  // All replacements use function form: citizen text may contain '$'
  // sequences, which String.replace would otherwise expand ($&, $1, ...).
  const rep = (old, neu) => {
    if (!doc.includes(old)) throw new Error('flagship anchor missing: ' + old.slice(0, 60));
    doc = doc.replace(old, () => neu);
  };
  // Page delta set (verified: the three flagships differ ONLY in these).
  doc = doc.split('#9d6bff').join(cfg.gem);
  doc = doc.replace('stroke%3D%22%23a06bff%22', 'stroke%3D%22%23' + cfg.accent.slice(1) + '%22');
  doc = doc.replace('%22middle%22%3EN%3C/text%3E', '%22middle%22%3E' + esc(world.name ? world.name.trim().charAt(0).toUpperCase() : 'N') + '%3C/text%3E');
  if (page !== 'personal') {
    const ours = [['My story', 'Our story'], ['My motto', 'Our motto'], ['My goals', 'Our goals'], ['My mission', 'Our mission'], ['My vision', 'Our vision'], ['What I love', 'What we love'], ["What I don't", "What we don't"], ['My facts', 'Our facts']];
    for (const [m, o] of ours) { if (doc.includes(m)) doc = doc.replace(m, o); }
  }
  // Identity, verbatim. Page-agnostic patterns: the template fetched is
  // always the Personal document, but the delta set is applied FIRST
  // (above), so these patterns must match whichever demo identity the
  // page carries — never anchor on one page's demo strings.
  const repRe = (re, neu) => {
    if (!re.test(doc)) throw new Error('flagship anchor missing: ' + re);
    // A function replacement must be PASSED to replace, not wrapped: the
    // wrapper returns the function object, which replace stringifies into
    // the page (this leaked 'function (m, p1, p2) {...}' as visible text
    // in the name and tagline slots). String replacements keep the arrow
    // wrapper so citizen '$' sequences are never expanded.
    doc = (typeof neu === 'function') ? doc.replace(re, neu) : doc.replace(re, () => neu);
  };
  repRe(/<title>[^<]*<\/title>/, '<title>' + esc(world.name) + '</title>');
  repRe(/(<div class="ph-nm" id="pname"[^>]*>)[^<]*(<\/div>)/, function (m, p1, p2) { return p1 + esc(world.name) + p2; });
  if (!doc.includes('os-owner-name')) throw new Error('flagship anchor missing: os-owner-name');
  doc = doc.replace(/(<span class="os-owner-name">)[^<]*(<\/span>)/g, function (m, p1, p2) { return p1 + esc(world.name) + p2; });
  repRe(/var PAGE_ALIAS = '[^']*';/g, "var PAGE_ALIAS = '" + esc(world.alias) + "';");
  repRe(/(<div class="ph-tg" id="ptag"[^>]*>)[^<]*(<\/div>)/, function (m, p1, p2) { return p1 + esc(tagline) + p2; });
  // About slots: fill verbatim; empty answers leave the flagship's own
  // honest prompt text (never invented, never the demo persona text).
  const slotAnchors = {
    motto: 'No motto yet &mdash; tap Edit and put it in one line.',
    goals: 'No goals written yet &mdash; tap Edit and name the first one.',
    mission: 'No mission written yet &mdash; tap Edit and say what this app is here to do.',
    vision: 'No vision written yet &mdash; tap Edit and describe where this is heading.',
    about: 'Nothing here yet &mdash; tap Edit and write the first line about this app.',
    love: 'Nothing here yet &mdash; tap Edit and add the first thing.'
  };
  for (const key of ['motto', 'goals', 'mission', 'vision', 'about', 'love']) {
    const v = slots[key];
    if (!has(v)) continue;
    // Personal About is pre-escaped at construction (see above); every
    // other slot is escaped here. Citizen text never enters raw.
    doc = doc.replace(slotAnchors[key], () => (key === 'about' && page === 'personal') ? v : esc(v));
  }
  // Story slot: whichever demo paragraph the page carries (each flagship
  // has its own) is replaced by the citizen's story, or the honest prompt.
  doc = doc.replace(/(<p id="abouttext">)[^<]*(<\/p>)/, function (m, p1, p2) { return p1 + (has(slots.story) ? esc(slots.story) : 'Nothing here yet — tap Edit and write the first line.') + p2; });
  // Cover slot: the citizen's real cover, first child of #cvr.
  const cover = '<img src="data:image/svg+xml;utf8,' + encodeURIComponent(coverSVG(world.name, coverBody, cfg.accent)) + '" alt="Cover of ' + esc(world.name) + '" style="width:100%;height:100%;object-fit:cover" />';
  rep('<div class="ph-cover" id="cvr">', '<div class="ph-cover" id="cvr">' + cover);
  // Alias-scope the device-local keys: unscoped keys would bleed one
  // identity's edits into another citizen's page on a shared device.
  const scopeKeys = ['naya.name', 'naya.tag', 'naya.about', 'os.photo', 'fm.photo', 'fm.coverPos', 'os.connected'];
  for (const k of scopeKeys) doc = doc.split("'" + k + "'").join("'" + k + '.' + world.alias + "'");
  doc = doc.split('naya.setting.').join('naya.setting.' + world.alias + '.');
  // Matches card (Personal only), in the flagship's own component language,
  // placed before the dashboard section in the home view.
  if (page === 'personal' && matches && matches.length) {
    doc = doc.replace('<div class="ph-sec os-view" data-os-view="dashboard"', () => matchesCard(matches) + '<div class="ph-sec os-view" data-os-view="dashboard"');
  }
  // Owner script: public pages only. The owner sees a flagship-language
  // settings fragment appended to #settings; the binder posts to
  // /api/welcome/settings with the device credential.
  doc = doc.replace('</body>', () => flagshipOwnerScript(world.alias, page) + '</body>');
  // Fail closed: a demo string surviving means a substitution was missed
  // — never serve demo data on a citizen page.
  for (const d of DEMO_STRINGS) { if (doc.includes(d)) throw new Error('demo string survived render: ' + d); }
  return doc;
}

function matchesCard(matches) {
  const rows = matches.map((m, i) => {
    const c = SPECTRUM[i % SPECTRUM.length];
    return '<div style="display:flex;gap:12px;align-items:center;margin-top:12px">' +
      '<div style="width:44px;height:44px;flex:none;border-radius:50%;display:grid;place-items:center;font-weight:800;color:#fff;background:radial-gradient(circle at 34% 28%,' + c + ',' + c + ' 60%,#0a0a12 135%);border:1.5px solid rgba(255,255,255,.6)">' + esc(initialsOf(m.name, m.alias)) + '</div>' +
      '<div style="flex:1;min-width:0"><div style="font-weight:700;color:#fff"><a style="color:#fff" href="/world/' + esc(m.alias) + '">' + esc(m.name || m.alias) + '</a> <span style="color:#c9c9d4;font-weight:600">· nayanet.live/world/' + esc(m.alias) + '</span></div>' +
      '<div class="os-note" style="margin:4px 0 0">' + esc((m.reasons || []).join(' · ')) + '</div></div>' +
      '<div style="font-weight:900;font-size:1.2rem;color:' + c + '">' + m.pct + '%</div></div>';
  }).join('');
  return '<div class="ph-card" id="os-matches" style="--ac:#e84fff;"><h3><span class="os-jewel os-jewel-h" style="--jc:#e84fff">✦</span> Your Matches</h3>' +
    '<p class="os-note" style="margin:0 0 4px">People the match game found for you — alias and declared signals only, never private content.</p>' + rows + '</div>';
}

function settingsFragment(alias, settings) {
  const pages = [['personal', 'Personal'], ['business', 'Business'], ['space', 'Space']];
  const rows = pages.map(([pg, label]) => {
    const s = settings[pg] || { visibility: 'private', findable: false };
    const active = (yes) => yes ? ' style="border-color:#ffbf3d;box-shadow:0 0 18px -4px #ffbf3d"' : '';
    return '<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px">' +
      '<span style="font-weight:700;min-width:84px">' + label + '</span>' +
      '<button class="ph-btn" data-set="' + pg + '" data-vis="public"' + active(s.visibility === 'public') + '>Public</button>' +
      '<button class="ph-btn" data-set="' + pg + '" data-vis="private"' + active(s.visibility === 'private') + '>Private</button>' +
      '<button class="ph-btn" data-set="' + pg + '" data-find="true"' + active(s.findable === true) + '>Findable</button>' +
      '<button class="ph-btn" data-set="' + pg + '" data-find="false"' + active(s.findable === false) + '>Not findable</button></div>';
  }).join('');
  return '<div class="ph-card" id="os-owner-settings" style="--ac:#ffbf3d;"><h3><span class="os-jewel os-jewel-h" style="--jc:#ffbf3d">✦</span> Your Settings — you hold every switch</h3>' +
    '<p class="os-note" style="margin:0">Only you can change these. A private page shows visitors the connect layer only; findable pages appear in NayaNET search.</p>' +
    rows + '<p class="os-note" id="savedNote" style="margin:12px 0 0"></p></div>';
}

function flagshipOwnerScript(alias, page) {
  return '<script>(function(){' +
    'function ls(k){try{return localStorage.getItem(k)||""}catch(e){return""}}' +
    'var al=(ls("nayanet_smart_alias")||"").trim().toLowerCase();if(!al||al!==' + JSON.stringify(alias) + ')return;' +
    'var cred={alias:al,device_key:ls("nayanet_vault_key"),name:ls("nayanet_smart_name")};var SET=null;' +
    'fetch("/api/welcome/owner",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.assign({},cred,{page:' + JSON.stringify(page) + '}))}).then(function(r){return r.json()}).then(function(d){if(!d||!d.html)return;SET=d.settings||null;var set=document.getElementById("settings");if(set)set.insertAdjacentHTML("beforeend",d.html);bind();}).catch(function(){});' +
    'function bind(){document.querySelectorAll("#os-owner-settings [data-set]").forEach(function(b){b.addEventListener("click",async function(){if(!SET)return;var pg=b.dataset.set;var cur=SET[pg];var body=Object.assign({},cred,{page:pg,visibility:b.dataset.vis?b.dataset.vis:cur.visibility,findable:b.dataset.find!==undefined?(b.dataset.find==="true"):cur.findable});var r=await fetch("/api/welcome/settings",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});var dd={};try{dd=await r.json()}catch(e){}var note=document.getElementById("savedNote");if(r.ok&&dd.settings){SET=dd.settings;document.querySelectorAll("#os-owner-settings [data-set]").forEach(function(x){if(x.dataset.set!==pg)return;var on=x.dataset.vis?x.dataset.vis===SET[pg].visibility:(x.dataset.find==="true")===SET[pg].findable;x.style.borderColor=on?"#ffbf3d":"";x.style.boxShadow=on?"0 0 18px -4px #ffbf3d":"";});if(note)note.textContent="Saved — your "+pg+" page is now "+SET[pg].visibility+(SET[pg].findable?" and findable.":" and unfindable.");}else if(note){note.textContent=dd.error||"That did not save — try again."}})});}' +
    '})();</' + 'script>';
}

function gateOwnerScript(alias, page) {
  return '<script>(function(){' +
    'function ls(k){try{return localStorage.getItem(k)||""}catch(e){return""}}' +
    'var al=(ls("nayanet_smart_alias")||"").trim().toLowerCase();if(!al||al!==' + JSON.stringify(alias) + ')return;' +
    'var cred={alias:al,device_key:ls("nayanet_vault_key"),name:ls("nayanet_smart_name"),page:' + JSON.stringify(page) + '};' +
    'fetch("/api/welcome/owner",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(cred)}).then(function(r){return r.json()}).then(function(d){if(!d||!d.full)return;document.open();document.write(d.full);document.close();}).catch(function(){});' +
    '})();</' + 'script>';
}

function gateShell(title, body, ownerScript) {
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
    '<title>' + esc(title) + ' | NayaNET</title>' +
    '<style>body{margin:0;background:#050507;color:#f8f7fb;font-family:Georgia,serif}' +
    '.top{padding:22px 24px;border-bottom:1px solid rgba(255,255,255,.14);font-weight:800;letter-spacing:.18em}' +
    '.wrap{max-width:760px;margin:0 auto;padding:32px 20px 48px}' +
    '.card{border:1.5px solid rgba(160,107,255,.55);border-radius:18px;padding:26px 28px;background:linear-gradient(180deg,#17171f,#0a0a0f);box-shadow:0 16px 40px rgba(0,0,0,.55)}' +
    '.card h2{margin:0 0 12px;font-size:1.6rem}.card p{line-height:1.6;color:#e8e8ec}' +
    '.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}.chip{border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:6px 12px;font-size:.85rem}' +
    '.doors{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}.door{display:inline-block;border:1.5px solid rgba(255,255,255,.7);border-radius:999px;padding:10px 18px;color:#fff;text-decoration:none;font-weight:700}' +
    '.foot{max-width:760px;margin:0 auto;padding:0 20px 40px;color:#9a9aa8;font-size:.85rem;letter-spacing:.12em}</style></head><body>' +
    '<div class="top">NAYANET</div><div class="wrap">' + body + '</div>' +
    '<div class="foot">NAYANET — THE NEW NET · ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</div>' +
    (ownerScript || '') + '</body></html>';
}

function renderConnectLayer(world, viewerMatch, page) {
  const a = world.answers || {};
  const topics = world.topics || [];
  let matchHTML = '';
  if (viewerMatch) {
    matchHTML = '<div class="card" style="margin-top:18px;border-color:#e84fff"><h2>Your Match With ' + esc(world.name) + '</h2>' +
      '<p>' + esc((viewerMatch.reasons || []).join(' · ')) + '</p><p style="font-size:1.4rem;font-weight:900">' + viewerMatch.pct + '%</p></div>';
  }
  const body =
    '<div class="card"><h2>A Private World — Open To Connect</h2>' +
    '<p>' + esc(world.name) + ' keeps this page private — and that is their right, held by design. What the network may know is the connect layer: their alias, what they are about, and that they are here to meet the right people.</p>' +
    (topics.length ? '<div class="chips">' + topics.map((t) => '<span class="chip">' + esc(t) + '</span>').join('') + '</div>' : '') +
    '<div class="doors">' +
    '<a class="door" href="https://nayanet.live/rooms/mail">✉ Message via Smart Mail</a>' +
    '<a class="door" href="/world/' + esc(world.alias) + '/business">Their Business</a>' +
    '<a class="door" href="/world/' + esc(world.alias) + '/space">Their Space</a>' +
    '<a class="door" href="/welcome">Claim Your Own World</a></div></div>' +
    matchHTML;
  return gateShell(world.name + ' — Connect', body, gateOwnerScript(world.alias, page || 'personal'));
}

function renderNotFound(alias) {
  const body = '<div class="card"><h2>No World Here Yet</h2>' +
    '<p>The address nayanet.live/world/' + esc(alias) + ' has not been claimed — no citizen\'s world lives under this name yet. If it should be yours, the welcome takes two minutes and the world is born filled, never empty.</p>' +
    '<div class="doors"><a class="door" href="/welcome">Begin The Welcome</a></div></div>';
  return gateShell('No world here yet', body, '');
}
"""

# Build-time template acquisition: fetch the LIVE flagship bytes, validate
# markers, embed as a JSON string. Fallback: the checked-in artifact
# welcome-build/flagship-template.html (refreshed on every live fetch).
import subprocess as _sp
_FLAGSHIP_LIVE = 'https://nayanet.live/personal'
try:
    # curl, not urllib: the edge 403s Python-urllib and truncates its reads.
    _cp = _sp.run(['curl', '-sS', '--fail', '--max-time', '60', '-A',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
                   _FLAGSHIP_LIVE], capture_output=True, timeout=90)
    assert _cp.returncode == 0, 'curl exit ' + str(_cp.returncode) + ' ' + _cp.stderr.decode('utf-8', 'ignore')[:200]
    _tpl_bytes = _cp.stdout.decode('utf-8')
    assert 'ph-cover' in _tpl_bytes and 'PAGE_ALIAS' in _tpl_bytes, 'live flagship markers missing'
    open('flagship-template.html', 'w').write(_tpl_bytes)
    print('FLAGSHIP TEMPLATE: live fetch OK,', len(_tpl_bytes), 'bytes, artifact refreshed')
except Exception as _e:
    _tpl_bytes = open('flagship-template.html').read()
    assert 'ph-cover' in _tpl_bytes and 'PAGE_ALIAS' in _tpl_bytes, 'checked-in template markers missing'
    print('FLAGSHIP TEMPLATE: live fetch failed (%s); using checked-in artifact,' % _e, len(_tpl_bytes), 'bytes')
FLAGSHIP_JS = FLAGSHIP_JS.replace('__FLAGSHIP_TEMPLATE_JSON__', json.dumps(_tpl_bytes), 1)
assert '__FLAGSHIP_TEMPLATE_JSON__' not in FLAGSHIP_JS

# Sweep: hashSeed .. normSettings region out, flagship block in. This takes
# the invented jewel generator + its helpers (hashSeed, mulberry, shade)
# plus the thin-shell renderers (WORLD_CSS, tabsRow, matchesPanel,
# worldShell, sectionBoard, ownerSettingsBar, renderConnectLayer,
# renderPersonal/Business/Space, renderNotFound) — all superseded below.
_start = srv.index('function hashSeed')
_end = srv.index('function normSettings')
srv = srv[:_start] + FLAGSHIP_JS.strip() + '\n\n' + srv[_end:]

# worldPage: flagship render, privacy gate preserved exactly.
_NEW_WORLDPAGE = r"""async function worldPage(request, env, alias, page) {
  const world = await getWorld(env, alias);
  if (!world) return html(404, renderNotFound(alias));
  world.settings = normSettings(world);
  const s = world.settings[page];
  if (s.visibility === 'private') {
    // Server-side privacy: anyone but the owner gets the connect layer
    // only. The owner upgrades in place via /api/welcome/owner, on the
    // real claim's credential — private answers never ship anonymously.
    return html(200, renderConnectLayer(world, null, page));
  }
  let tpl;
  try { tpl = await flagshipTemplate(); }
  catch (e) { return html(502, gateShell('Template unreachable', '<div class="card"><h2>Try Again In A Moment</h2><p>The page template is unreachable right now — nothing about this world has changed. Reload to try again.</p></div>', '')); }
  let matches = [];
  if (page === 'personal') matches = await matchesFor(env, world);
  try {
    return html(200, renderFlagshipDoc(tpl, world, page, matches));
  } catch (e) {
    return html(502, gateShell('Page could not be built', '<div class="card"><h2>Try Again In A Moment</h2><p>This page could not be built from the flagship template — nothing about this world has changed. Reload to try again.</p></div>', ''));
  }
}

"""
srv = replace_between(srv, 'async function worldPage', 'export default {', _NEW_WORLDPAGE)

# apiOwner: same auth contract as the old one (authCitizen: device_key
# exact match, else stored-name match — the Hub's own trust level), world
# loaded by the AUTHENTICATED alias, never the requested one. Private
# pages: the owner gets the FULL flagship page in place. Public pages:
# the flagship-language settings fragment for #settings.
_NEW_APIOWNER = r"""async function apiOwner(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read that — try again.');
  const auth = await authCitizen(env, body);
  if (auth.error) return auth.error;
  const page = ['personal', 'business', 'space'].includes(body.page) ? body.page : 'personal';
  const world = await getWorld(env, auth.id.alias);
  if (!world) return json(200, { html: '', settings: null });
  world.settings = normSettings(world);
  const pages = { personal: '/world/' + world.alias, business: '/world/' + world.alias + '/business', space: '/world/' + world.alias + '/space' };
  const s = world.settings[page];
  if (s.visibility === 'private') {
    // Owner of a private page gets the FULL flagship page, in place.
    let tpl;
    try { tpl = await flagshipTemplate(); }
    catch (e) { return json(502, { error: 'template unreachable' }); }
    let matches = [];
    if (page === 'personal') matches = await matchesFor(env, world);
    try {
      const full = renderFlagshipDoc(tpl, world, page, matches);
      return json(200, { full, settings: world.settings, pages, matchScore: matches.length ? matches[0].pct : null });
    } catch (e) { return json(502, { error: 'page could not be built' }); }
  }
  return json(200, {
    html: settingsFragment(world.alias, world.settings),
    settings: world.settings,
    pages
  });
}

"""
srv = replace_between(srv, 'async function apiOwner', '// ─── WORLD ROUTES', _NEW_APIOWNER)

# apiComplete: reveal cards carry the citizen's real covers (cover system).
_old_ret = 'ambassador_link: ambassadorLink, coverage'
assert srv.count(_old_ret) == 1, 'apiComplete return anchor not unique: ' + str(srv.count(_old_ret))
srv = srv.replace(_old_ret, _old_ret + ''',
    covers: {
      personal: coverSVG(id.name, saved.answers.motto || saved.answers.about || '', '#a06bff'),
      business: coverSVG(id.name, saved.answers.biz_do || saved.answers.biz_offer || '', '#3fb8ff'),
      space: coverSVG(id.name, saved.answers.space || saved.answers.motto || '', '#2fe89e')
    }''')

print('FLAGSHIP: jewelSVG remnants:', srv.count('jewelSVG'), '| hashSeed:', srv.count('hashSeed'), '| mulberry:', srv.count('mulberry'), '| coverSVG:', srv.count('coverSVG'), '| flagshipTemplate:', srv.count('flagshipTemplate'), '| renderFlagshipDoc:', srv.count('renderFlagshipDoc'), '| gateShell:', srv.count('gateShell'))

# embed the walk document
walk = open(HERE + "/walk.html").read()
assert "/*__WALK_HTML__*/ ''" in srv
srv = srv.replace("/*__WALK_HTML__*/ ''", json.dumps(walk), 1)

open(WORKER_OUT, "w").write(srv)
print("worker bytes:", len(srv.encode()), "->", WORKER_OUT)
print("checks:",
      "| begin route:", srv.count('/api/welcome/begin'),
      "| apiBegin:", srv.count('apiBegin'),
      "| naya_owner cookie:", srv.count('naya_owner'),
      "| me:", srv.count('/api/welcome/me'),
      "| owner:", srv.count('/api/welcome/owner'),
      "| complete:", srv.count('/api/welcome/complete'),
      "| settings:", srv.count('/api/welcome/settings'),
      "| WALK_HTML set:", 'const WALK_HTML = "' in srv)
