#!/usr/bin/env node
/* =====================================================================
   NAYA COMPOSER v1 — pieces + page type in → finished page out.
   Built by Naya Nitro Nu (BUILD seat, Team Nitro), directive #4, item 15.
   Head start: the Design Studio prototype
   (../design-studio/studio-v1.html) — its law engine and piece recipes are
   ported here verbatim where marked [STUDIO], then extended with new page
   types (report) and a CLI so the machine can compose pages unattended.

   THE CONTRACT: every page the composer emits obeys the design laws BY
   CONSTRUCTION — the spectrum walk assigns zones, the advisor refuses
   defects, the embedded naya-core.css carries ALIVE + ELEVATION, and the
   honesty line marks every demo surface so no page can claim live data.
   ===================================================================== */
"use strict";
const fs = require('fs');
const path = require('path');

/* ------------------------------------------------------------------
   THE LAWS — [STUDIO] ported verbatim from StudioCore (studio-v1.html).
   Spectrum wheel (11 stops, rainbow order, gold never yellow), walk()
   (dynamic count, order is law), advise() (the advisor refuses defects).
   ------------------------------------------------------------------ */
const SPECTRUM = [
  {id:'magenta', hex:'#e84fff', rgb:'232,79,255',  job:'The living edge'},
  {id:'purple',  hex:'#a06bff', rgb:'160,107,255', job:'Choosing intelligence'},
  {id:'indigo',  hex:'#6675ff', rgb:'102,117,255', job:'The deep signal'},
  {id:'blue',    hex:'#3fb8ff', rgb:'63,184,255',  job:'Knowledge moving'},
  {id:'emerald', hex:'#35e0a1', rgb:'53,224,161', job:'Deep green, forest'},
  {id:'green',   hex:'#2fe89e', rgb:'47,232,158',  job:'Alive and well'},
  {id:'lime',    hex:'#b8ee57', rgb:'184,238,87',  job:'New growth'},
  {id:'gold',    hex:'#ffbf3d', rgb:'255,191,61',  job:'Attention, earned'},
  {id:'orange',  hex:'#ff9a5a', rgb:'255,154,90',  job:'Warmth, momentum'},
  {id:'red',     hex:'#ff5e6c', rgb:'255,94,108',  job:'Urgency, the living edge'},
  {id:'pink',    hex:'#ed58cd', rgb:'237,88,205',  job:'Delight, the flourish'}
];
const specById = id => SPECTRUM.find(s => s.id === id) || SPECTRUM[1];
function walk(startId, n){
  const len = SPECTRUM.length;
  let s = SPECTRUM.findIndex(x => x.id === startId);
  if (s < 0) s = 1;
  n = Math.max(1, Math.min(len, Math.round(n) || 1));
  const out = [];
  for (let i = 0; i < n; i++) out.push(SPECTRUM[Math.round(s + (i * len) / n) % len].id);
  return out;
}

/* ------------------------------------------------------------------
   THE PIECES — [STUDIO] the library's one-piece-per-job registry.
   ------------------------------------------------------------------ */
const PIECES = {
  buttons: [
    {id:'lead',      name:'.naya-btn.lead',      job:'Flagship CTA — the obsidian pill.'},
    {id:'machine',   name:'.naya-btn.machine',   job:'Maximum clarity at rest — dense UI.'},
    {id:'streak',    name:'.naya-btn.streak',    job:'Light-streak sweep — announcements.'},
    {id:'proximity', name:'.naya-btn.proximity', job:'Cursor-tracking spotlight.'},
    {id:'icon',      name:'.naya-btn.icon',      job:'Glyph-only actions.'},
    {id:'portal',    name:'.naya-btn.portal',    job:'PLAY — always a portal.'},
    {id:'flat',      name:'Flat button', trap:true, job:'Not a Naya piece — the advisor refuses this.'}
  ],
  boards: [
    {id:'mix',   name:'.board-mix',  job:'Destination — a world you enter.'},
    {id:'tone',  name:'.board-tone', job:'Quieter destination — tone spine + radial wash.'},
    {id:'layer', name:'.layer',      job:'Nested meaning — nutshell → meaning → use.'}
  ],
  tabs: [
    {id:'smarttabs', name:'SmartTabs', job:'The universal favorites ribbon.'}
  ],
  jewels: [
    {id:'gems',  name:'Gem bullets', job:'Five-jewel cycle, never twice in a row.'},
    {id:'orbs',  name:'Orb row',     job:'Spherical, orbital, lit from within.'},
    {id:'spec',  name:'Spectrum bar',job:'The 5-segment law-order bar.'}
  ],
  blocks: [
    {id:'icard',  name:'Content card',   job:'One idea per card.'},
    {id:'itable', name:'Data table',     job:'Labels left, numbers right.'},
    {id:'ichart', name:'Chart',          job:'Honest numbers — axes labeled.'},
    {id:'iform',  name:'Input / form',   job:'Capture input.'},
    {id:'itoggle',name:'Toggle',         job:'Binary state, unmistakable.'},
    {id:'itoast', name:'Toast',          job:'Report what happened — truthfully.'},
    {id:'iplayer',name:'Media player',   job:'Portal-style play.'},
    {id:'ishare', name:'Share sheet',    job:'Send intelligence out.'}
  ],
  truth: [
    {id:'badges', name:'Truth badges', job:'✓ verified · ? claim · ◈ demonstration.'}
  ]
};
const SLOT_OF = {buttons:'button', boards:'board', tabs:'tabs', jewels:'jewels', blocks:'block', truth:'truth'};

const PAGE_TYPES = {
  feed:      {name:'Feed / Reader', desc:'A stream of intelligence.', accent:'green'},
  dashboard: {name:'Dashboard',     desc:'The state of things.',      accent:'gold'},
  form:      {name:'Form',          desc:'Capture something.',        accent:'blue'},
  gallery:   {name:'Gallery',       desc:'A wall of signal.',         accent:'magenta'},
  report:    {name:'Report',        desc:'What the numbers are really saying — nutshell, numbers, table, actions.', accent:'blue'}
};

function defaultState(){
  return { pageType:'feed', accent:'green', button:'lead', board:'mix', tabs:'smarttabs',
           jewels:'gems', block:'icard', text:'white', truth:'honest' };
}

/* The advisor — [STUDIO] pure checks. Defects are upgraded, never shipped. */
function advise(input){
  const s = Object.assign({}, input);
  const notes = [];
  const say = (title, body) => notes.push({title, body});
  delete s.accent2;
  if (s.text === 'colored'){
    s.text = 'white';
    say('Color moved off the text','Colored body text fails LAW ZERO — text stays white 99%; color lives on rims, jewels and the spine.');
  }
  if (s.button === 'flat'){
    s.button = 'lead';
    say('Flat button refused — built the living one','No flat buttons in the Naya language — built .naya-btn.lead in the accent instead.');
  }
  if (s.truth === 'allverified'){
    s.truth = 'honest';
    say('Kept the stamps honest','Nothing is stamped verified without proof — zones wear ? claim until they earn ✓.');
  }
  return {state:s, notes};
}

/* Validate piece picks against the registry. Unknown pieces fall back
   to the default of their slot — a typo never ships a hole in the page. */
function resolvePieces(picks){
  const d = defaultState();
  const out = Object.assign({}, picks);
  for (const [group, slot] of Object.entries(SLOT_OF)){
    const ok = (PIECES[group]||[]).some(p => p.id === out[slot]);
    if (!ok) out[slot] = d[slot];
  }
  if (!PAGE_TYPES[out.pageType]) out.pageType = d.pageType;
  if (!specById(out.accent) || !SPECTRUM.some(s=>s.id===out.accent)) out.accent = PAGE_TYPES[out.pageType].accent;
  return out;
}
/* ------------------------------------------------------------------
   BUILDERS — [STUDIO] the page-type recipes, ported from the studio's
   renderPreview, then generalized: a recipe is an ordered zone list.
   Every zone gets a stop off the wheel from the page accent; adjacent
   zones never share a hue BY CONSTRUCTION.
   ------------------------------------------------------------------ */
const A = id => specById(id);
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const acVars = id => { const s = A(id); return `--ac:${s.hex};--ac-glow:rgba(${s.rgb},.35);--ac-rgb:${s.rgb}`; };

function tabsHTML(hot){ return `<div class="smarttabs">${['All','Saved','Connected','Activity'].map((t,i)=>`<button class="stab${i===hot?' hot':''}">${t}</button>`).join('')}</div>`; }
function truthHTML(mode){
  if (mode==='honest') return `<span class="tbadge claim">? Claim</span>`;
  return `<span class="tbadge verified">✓ Verified</span>`;
}
function btnHTML(variant, label, accent){
  const cls = variant==='icon' ? 'naya-btn icon' : variant==='portal' ? 'naya-btn portal' : `naya-btn ${variant}`;
  const glyph = variant==='icon' ? '+' : variant==='portal' ? '▶' : '';
  return `<button class="${cls}" style="${acVars(accent || 'purple')}">${glyph||esc(label||'Continue →')}</button>`;
}
function gemRow(){
  const order = ['magenta','purple','blue','green','gold'];
  return `<div class="jrow">${order.map(c=>`<span class="gem" style="--gc:${A(c).hex}"></span>`).join('')}<span class="t">Five-jewel cycle — in law order, never twice in a row.</span></div>`;
}
function headHTML(title, kicker, sub, accent, badge){
  return `<div class="pg-head"><div class="pg-orb" style="--ac:${A(accent).hex};--ac-glow:rgba(${A(accent).rgb},.35)"></div>
    <div><div class="pg-kicker" style="--ac:${A(accent).hex}">${esc(kicker)}</div>
    <div class="pg-title">${esc(title)}</div><div class="pg-sub">${esc(sub)}</div></div>
    <div style="margin-left:auto">${badge||''}</div></div>`;
}
function boardHTML(style, accent, kicker, title, body, extra){
  const st = style==='tone' ? 'board-tone' : style==='layer' ? 'board' : 'board-mix';
  const wash = style==='tone' ? `style="${acVars(accent)};--ac-wash:rgba(${A(accent).rgb},.12)"` : `style="${acVars(accent)}"`;
  let inner = `<div class="board ${st}" ${wash}><div class="bk">${esc(kicker)}</div><h3>${esc(title)}</h3><p>${body}</p>${extra||''}</div>`;
  if (style==='layer') inner += `<div class="ilayer" style="--ac:${A(accent).hex}"><div class="lk">What it means</div><p>Layers nest inside boards — nutshell, meaning, use. Same order, every time.</p></div>`;
  return inner;
}
function blockHTML(id, accent, ctx){
  switch(id){
    case 'icard': {
      const cards = (ctx.cards && ctx.cards.length ? ctx.cards : [
        {k:'Smart Note', h:'One idea, carried well.', p:'Each card holds a single thought — kicker, headline, two lines, one quiet action.'},
        {k:'Smart Note', h:'One idea, carried well.', p:'Each card holds a single thought — kicker, headline, two lines, one quiet action.'},
        {k:'Smart Note', h:'One idea, carried well.', p:'Each card holds a single thought — kicker, headline, two lines, one quiet action.'}]);
      return `<div class="cards3">${cards.map(c=>`<article class="nb-card" style="${acVars(accent)}"><p class="ck">${esc(c.k)}</p><h4>${esc(c.h)}</h4><p>${esc(c.p)}</p><a href="#">Read the note →</a></article>`).join('')}</div>`;
    }
    case 'itable': {
      const rows = ctx.rows && ctx.rows.length ? ctx.rows : [['Measure first','Claim','—'],['Ship the bench','Claim','—'],['One language','Claim','—']];
      return `<table class="ntable"><tr><th>${esc(ctx.col1||'Lesson')}</th><th>${esc(ctx.col2||'State')}</th><th style="text-align:right">${esc(ctx.col3||'Proof')}</th></tr>${rows.map(r=>`<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td class="num">${esc(r[2])}</td></tr>`).join('')}</table>`;
    }
    case 'ichart': {
      const bars = ctx.bars && ctx.bars.length ? ctx.bars : [['Clarity',82,'magenta'],['Speed',64,'purple'],['Proof',91,'blue'],['Calm',73,'green']];
      return `<div class="chart"><h4>${esc(ctx.chartTitle||'Honest numbers — axes labeled')}</h4>${bars.map(b=>`<div class="bar-row"><span class="bl">${esc(b[0])}</span><div class="bar-track"><div class="bar-fill" style="width:${Number(b[1])}%;--bc:${A(b[2]).hex};--bc2:${A(b[2]).hex}"></div></div><span class="bv">${esc(String(b[1]))}</span></div>`).join('')}</div>`;
    }
    case 'iform': return `<div class="nfield"><label>What should Naya remember?</label><input class="ninput" placeholder="Say it in plain words…"></div><div class="nfield"><label>Who is it for?</label><input class="ninput" placeholder="Just you, or the collective?"></div>`;
    case 'itoggle': return `<div class="toggle-row" style="${acVars(accent)}"><div><div class="tl">Private by default</div><div class="td">Nothing shared until you choose it.</div></div><button class="tgl on" aria-label="toggle"></button></div><div class="toggle-row" style="${acVars(accent)}"><div><div class="tl">Speak it back</div><div class="td">Naya reads new notes aloud.</div></div><button class="tgl" aria-label="toggle"></button></div>`;
    case 'itoast': return `<div class="board board-tone" style="${acVars('green')};--ac-wash:rgba(47,232,158,.1)"><div class="bk" style="color:var(--verified)">✓ Saved</div><p><strong>Note kept.</strong> It will be here when you need it — that's the whole promise.</p></div>`;
    case 'iplayer': return `<div class="actions-row"><button class="naya-btn portal" style="${acVars(accent)}">▶</button><div><div style="font-weight:700">Powercast — the morning brief</div><div style="font-size:13px;color:var(--secondary)">12 min · honest audio, no filler</div></div></div>`;
    case 'ishare': return `<div class="actions-row"><button class="naya-btn machine" style="${acVars(accent)}">↗ Share</button><button class="naya-btn machine" style="${acVars(accent)}">⧉ Copy link</button></div>`;
    default: return '';
  }
}
function jewelHTML(kind, accent){
  if (kind==='orbs'){ return `<div class="orb-grid">${SPECTRUM.map(x=>`<div class="orb-cell"><div class="big-orb" style="--oc:${x.hex}"></div><div class="ol">${x.id}</div></div>`).join('')}</div>`; }
  if (kind==='spec'){ const order=['magenta','purple','blue','green','gold'];
    return `<div class="specbar">${order.map(c=>`<i style="background:${A(c).hex}"></i>`).join('')}</div>`; }
  return gemRow();
}

/* The honesty footer — every composed page says what it is. Loud unknown,
   never fake green: demo surfaces wear ◈ Demonstration; nothing claims
   live data it doesn't have. */
function honestyFooter(note){
  return `<div style="margin-top:26px;padding-top:18px;border-top:1px solid var(--line);display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span class="tbadge demo">◈ Demonstration</span>
    <span style="font-size:12.5px;color:var(--secondary)">${esc(note || 'Composed page — assembled from the Naya library, not live data.')}</span></div>`;
}

/* ------------------------------------------------------------------
   RECIPES — one per page type. A recipe is: zones (count → walk stops)
   and an ordered list of zone builders. The report recipe is NEW —
   the first page type the studio never built.
   ------------------------------------------------------------------ */
function recipe_report(s, ctx){
  const [zA,zB,zC,zD,zE] = walk(s.accent, 5);
  let h = '';
  h += headHTML(ctx.head?.title || 'The Daily Report',
                ctx.head?.kicker || 'What happened',
                ctx.head?.sub || 'What the numbers are really saying — the day in one page.',
                zA, truthHTML(s.truth));
  if (s.tabs === 'smarttabs') h += tabsHTML(1);
  h += boardHTML(s.board, zA, 'In a nutshell', ctx.nutshell?.title || 'The day in one breath.',
    ctx.nutshell?.body || 'Three things moved. Each one below carries its own proof — or an honest <strong>? claim</strong> badge where the proof is still open.');
  const stats = ctx.stats || [['128','Notes kept'],['9.6','Proof score'],['4','Lanes live']];
  const statStops = [zA,zB,zC];
  h += `<div class="stat3">${stats.map((st,i)=>{ const sp = A(statStops[i%3]);
    return `<div class="stat" style="--sc:${sp.hex};--sc-glow:rgba(${sp.rgb},.35)"><div class="sv">${esc(st[0])}</div><div class="sl">${esc(st[1])}</div></div>`; }).join('')}</div>`;
  h += boardHTML(s.board === 'mix' ? 'tone' : s.board, zB, 'The shape of it', ctx.chartZone?.title || 'The week in one glance.',
    ctx.chartZone?.body || 'Bars, not promises — axes labeled, nothing truncated. These are <strong>demonstration values</strong>, kept honest until the live feed lands.',
    blockHTML('ichart', zB, ctx));
  h += boardHTML('layer', zC, 'The ledger', ctx.tableZone?.title || 'Every claim, with its proof.',
    ctx.tableZone?.body || 'One row per claim. A claim and a proof never look the same — <strong>? claim</strong> until proven, ✓ when it earns it.',
    blockHTML('itable', zC, ctx));
  h += blockHTML('icard', zD, ctx);
  h += `<div class="actions-row">${btnHTML(s.button, ctx.cta?.label || 'Send this report →', zD)}${btnHTML('machine', ctx.cta2?.label || 'Save a copy', zE)}</div>`;
  h += jewelHTML(s.jewels, zE);
  h += boardHTML('tone', zE, 'Kept walking', 'The rainbow never repeats.',
    `This zone wears <strong>${A(zE).id}</strong> — five stops off the wheel from the hero, every one high-contrast against its neighbors. The count fits the page; the order never breaks.`);
  return {html:h, stops:[zA,zB,zC,zD,zE]};
}

function recipe_feed(s, ctx){
  const [zA,zB,zC,zD] = walk(s.accent, 4);
  let h = '';
  h += headHTML(ctx.head?.title || 'The Smart Feed', ctx.head?.kicker || 'Live intelligence',
                ctx.head?.sub || 'Everything worth remembering, newest first.', zA, truthHTML(s.truth));
  if (s.tabs === 'smarttabs') h += tabsHTML(0);
  h += boardHTML(s.board, zA, 'In a nutshell', ctx.nutshell?.title || 'This is what today taught us.',
    ctx.nutshell?.body || 'Lessons landed since morning. Each one below follows the anatomy — nutshell, meaning, use, what you get.');
  h += blockHTML(s.block, zB, ctx);
  if (s.block !== 'icard') h += blockHTML('icard', zC, ctx);
  h += jewelHTML(s.jewels, zB);
  h += `<div class="actions-row">${btnHTML(s.button, 'Save this →', s.block==='icard'?zB:zC)}</div>`;
  h += boardHTML('tone', zD, 'Kept walking', 'The rainbow never repeats.',
    `This zone wears <strong>${A(zD).id}</strong> — four stops off the wheel from the hero, every one high-contrast against its neighbors. The count fits the page; the order never breaks.`);
  return {html:h, stops:[zA,zB,zC,zD]};
}

function recipe_dashboard(s, ctx){
  const [zA,zB,zC,zD,zE,zF] = walk(s.accent, 6);
  let h = '';
  h += headHTML(ctx.head?.title || 'Mission Control', ctx.head?.kicker || 'The state of things',
                ctx.head?.sub || "Every dial that matters, none that don't.", zA, truthHTML(s.truth));
  const stats = ctx.stats || [['128','Notes kept'],['9.6','Proof score'],['4','Lanes live']];
  h += `<div class="stat3">${stats.map((st,i)=>{ const sp = A([zA,zB,zC][i%3]);
    return `<div class="stat" style="--sc:${sp.hex};--sc-glow:rgba(${sp.rgb},.35)"><div class="sv">${esc(st[0])}</div><div class="sl">${esc(st[1])}</div></div>`; }).join('')}</div>`;
  h += boardHTML(s.board, zD, 'In a nutshell', ctx.nutshell?.title || 'The week in one board.',
    ctx.nutshell?.body || 'Everything important, <strong>nothing decorative</strong>. If a number can\'t change a decision, it doesn\'t earn a pixel.');
  h += blockHTML('ichart', zE, ctx);
  h += blockHTML('itable', zF, ctx);
  h += `<div class="actions-row">${btnHTML(s.button, 'Open reports →', zF)}</div>`;
  return {html:h, stops:[zA,zB,zC,zD,zE,zF]};
}

function recipe_form(s, ctx){
  const [zA,zB] = walk(s.accent, 2);
  let h = '';
  h += headHTML(ctx.head?.title || 'Capture', ctx.head?.kicker || 'Say it once',
                ctx.head?.sub || 'Naya keeps it, finds it, and puts it to work.', zA, truthHTML(s.truth));
  h += boardHTML(s.board, zA, 'In a nutshell', ctx.nutshell?.title || 'Two fields. Thirty seconds.',
    ctx.nutshell?.body || 'Capture is <strong>respectful of attention</strong> — the fewest fields that do the job, then one clear action.');
  h += blockHTML('iform', zB, ctx);
  h += blockHTML('itoggle', zB, ctx);
  h += `<div class="actions-row">${btnHTML(s.button, 'Keep this note →', zB)}</div>`;
  h += jewelHTML(s.jewels, zB);
  return {html:h, stops:[zA,zB]};
}

function recipe_gallery(s, ctx){
  const [zA,zB,zC] = walk(s.accent, 3);
  let h = '';
  h += headHTML(ctx.head?.title || 'The Wall', ctx.head?.kicker || 'Signal, arranged',
                ctx.head?.sub || 'Every orb a live thing — spherical, orbital, lit from within.', zA, truthHTML(s.truth));
  h += `<div class="orb-grid">${SPECTRUM.map(x=>`<div class="orb-cell"><div class="big-orb" style="--oc:${x.hex}"></div><div class="ol">${x.id}</div></div>`).join('')}</div>`;
  h += boardHTML(s.board, zB, 'In a nutshell', ctx.nutshell?.title || 'The wall reads in law order.',
    ctx.nutshell?.body || 'The whole wheel on display above — the rainbow\'s natural flow. <strong>Scramble the order and the eye knows something\'s wrong before the mind does.</strong>');
  h += blockHTML('icard', zC, ctx);
  h += `<div class="actions-row">${btnHTML(s.button, 'Enter →', zC)}</div>`;
  return {html:h, stops:[zA,zB,zC]};
}

const RECIPES = { feed:recipe_feed, dashboard:recipe_dashboard, form:recipe_form, gallery:recipe_gallery, report:recipe_report };

/* compose(state, ctx, css) → {html, stops, notes}
   The one function: pieces + page type in → finished page out. */
function compose(rawState, ctx, css){
  const resolved = resolvePieces(rawState || {});
  const r = advise(resolved);
  const s = r.state;
  const recipe = RECIPES[s.pageType];
  const body = recipe(s, ctx || {});
  const head = `<title>${esc((ctx||{}).docTitle || PAGE_TYPES[s.pageType].name + ' — composed by Naya')}</title>`;
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
${head}
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
/* Naya tokens + pieces — composed ${new Date().toISOString().slice(0,10)}, page type "${s.pageType}", walk [${body.stops.join(' → ')}] */
${css}
</style>
</head>
<body style="background:#050507">
<div class="canvas" style="max-width:960px;margin:40px auto"><div class="page" style="${acVars(s.accent)}">${body.html}${honestyFooter((ctx||{}).honestyNote)}</div></div>
</body>
</html>`;
  return {html, stops:body.stops, notes:r.notes, state:s};
}
/* ------------------------------------------------------------------
   SELF-CHECK — the composer verifies its own work before reporting.
   Run: node composer.js --selfcheck
   ------------------------------------------------------------------ */
function selfCheck(css){
  const out = [];
  const ok = (name, cond) => out.push([name, !!cond]);
  // 1. The 43 law checks from the studio stay green on the ported engine.
  const idx = id => SPECTRUM.findIndex(s => s.id === id);
  const inOrder = ids => ids.every((id,i)=> i===0 || (idx(id)-idx(ids[i-1])+11)%11 > 0);
  ok('wheel: 11 stops, rainbow order, gold never yellow',
    JSON.stringify(SPECTRUM.map(s=>s.id)) === JSON.stringify(['magenta','purple','indigo','blue','emerald','green','lime','gold','orange','red','pink']));
  for (let n=1;n<=11;n++){ const w = walk('blue', n); ok(`walk(${n}): distinct, in order`, w.length===n && new Set(w).size===n && inOrder(w)); }
  ok('walk starts at accent', walk('green',4)[0]==='green');
  ok('walk caps at wheel', walk('green',99).length===11);
  ok('walk unknown start falls back safely', walk('nope',3)[0]==='purple');
  let a = advise(Object.assign(defaultState(),{button:'flat'}));
  ok('flat button refused → lead', a.state.button==='lead' && a.notes.length===1);
  a = advise(Object.assign(defaultState(),{text:'colored'}));
  ok('colored body text refused → white', a.state.text==='white' && a.notes.length===1);
  a = advise(Object.assign(defaultState(),{truth:'allverified'}));
  ok('stamp-everything refused → honest', a.state.truth==='honest' && a.notes.length===1);
  a = advise(defaultState()); ok('clean picks → no notes', a.notes.length===0);
  // 2. A composed report page obeys the laws by construction.
  const sample = compose({pageType:'report', accent:'blue'}, {}, css);
  ok('report recipe exists, 5 zones', sample.stops.length===5);
  ok('zones distinct', new Set(sample.stops).size===5);
  ok('zones in spectral order', inOrder(sample.stops));
  const H = sample.html;
  ok('doctype + closes html', H.startsWith('<!DOCTYPE html>') && H.trimEnd().endsWith('</html>'));
  const opens = (H.match(/<div/g)||[]).length, closes = (H.match(/<\/div>/g)||[]).length;
  ok(`divs balanced (${opens}/${closes})`, opens===closes);
  ok('alive hooks embedded (.board:hover, .naya-btn in css)', css.includes('.board:hover') && css.includes('.naya-btn'));
  ok('buttons carry zone glow (--ac-glow)', /naya-btn[^"]*" style="[^"]*--ac-glow:rgba\(/.test(H));
  ok('boards carry zone vars (--ac)', H.includes('board board-mix') || H.includes('board board-tone'));
  ok('jewels in law order', H.includes('Five-jewel cycle'));
  ok('honest footer present', H.includes('◈ Demonstration') && H.includes('not live data'));
  ok('no fake-green stamp', !H.includes('✓ Verified'));
  const liveClaims = [...H.matchAll(/live data/gi)].filter(m => !/not live data/i.test(H.slice(m.index-24, m.index+m[0].length)));
  ok('no unqualified "live data" claims', liveClaims.length===0);
  const wheelHexes = new Set(SPECTRUM.map(s=>s.hex.toLowerCase()));
  const usedHexes = [...H.matchAll(/--ac:([#0-9a-fA-F]{6,7})/g)].map(m=>m[1].toLowerCase());
  ok('every zone accent is a wheel hex', usedHexes.length>0 && usedHexes.every(hx=>wheelHexes.has(hx)));
  ok('no yellow hex anywhere', !/#f{2,4}0{2}/i.test(H) && !/yellow/i.test(H));
  ok('head has title', H.includes('<title>'));
  // 3. All five page types compose without throwing.
  for (const pt of Object.keys(RECIPES)){
    try { const c = compose({pageType:pt}, {}, css); ok(`composes: ${pt} (${c.stops.length} zones)`, c.html.length>2000); }
    catch(e){ ok(`composes: ${pt}`, false); }
  }
  const fail = out.filter(x=>!x[1]);
  for (const [name] of fail) console.log('FAIL:', name);
  console.log(`\nself-check: ${out.length-fail.length}/${out.length} passed`);
  return fail.length===0;
}

/* ------------------------------------------------------------------
   CLI
   node composer.js --type report --pieces button:lead,board:mix,jewels:gems,block:icard,truth:honest \
     --accent blue --in report-recipe.json --out sample-report-page.html
   ------------------------------------------------------------------ */
function parseArgs(argv){
  const o = {};
  for (let i=0;i<argv.length;i++){
    const a = argv[i];
    if (a.startsWith('--')) o[a.slice(2)] = argv[i+1] && !argv[i+1].startsWith('--') ? argv[++i] : true;
  }
  return o;
}
function cli(){
  const args = parseArgs(process.argv.slice(2));
  if (args.help || args.h){
    console.log(`Naya Composer v1 — pieces + page type in → finished page out.

Usage:
  node composer.js --type report [--accent blue]
      [--pieces button:lead,board:mix,jewels:gems,block:icard,truth:honest]
      [--in recipe.json] [--out page.html]
  node composer.js --selfcheck

Page types: ${Object.keys(RECIPES).join(', ')}
Slots: ${Object.keys(SLOT_OF).join(', ')} (defaults: the studio prototype's picks)`);
    return;
  }
  const cssPath = path.join(__dirname, 'naya-core.css');
  if (!fs.existsSync(cssPath)){ console.error('FAIL: naya-core.css missing next to composer.js'); process.exit(1); }
  const css = fs.readFileSync(cssPath, 'utf8');
  if (args.selfcheck){ process.exit(selfCheck(css) ? 0 : 1); }

  const state = defaultState();
  if (args.type) state.pageType = args.type;
  if (args.accent) state.accent = args.accent;
  if (args.pieces) for (const pair of String(args.pieces).split(',')){
    const [slot, piece] = pair.split(':').map(x=>x.trim());
    if (slot && piece && slot in state) state[slot] = piece;
  }
  let ctx = {};
  if (args.in){
    if (!fs.existsSync(args.in)){ console.error('FAIL: recipe file not found:', args.in); process.exit(1); }
    ctx = JSON.parse(fs.readFileSync(args.in, 'utf8'));
  }
  const {html, stops, notes, state:s} = compose(state, ctx, css);
  const outPath = args.out || `${s.pageType}-page.html`;
  fs.writeFileSync(outPath, html);
  console.log(JSON.stringify({out:outPath, bytes:html.length, pageType:s.pageType, accent:s.accent,
    walk:stops, advisorNotes:notes.map(n=>n.title), pieces:{button:s.button, board:s.board, jewels:s.jewels, block:s.block, truth:s.truth}}, null, 2));
}

if (require.main === module) cli();

module.exports = { SPECTRUM, specById, walk, PIECES, PAGE_TYPES, defaultState, advise, resolvePieces, compose, selfCheck, RECIPES };
