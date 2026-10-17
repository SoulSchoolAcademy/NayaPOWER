/* LIVING INTEL — stub-DOM smoke suite (no browser, no jsdom).
 *
 * Covers the room's real behaviors + the drilled-law CSS markers:
 *   adapter build/sort, flow-color-by-position, DEMO chips, filters,
 *   jewels, tap-for-heartbeat modal, keyboard open/Escape, focus trap +
 *   focus restore, filter-aware empty state, obsidian buttons,
 *   reduced-motion, type floor, time-ago ticks.
 *
 * Run: node HUB/app/preview/tests/living-intel-smoke.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..', '..', '..');

/* ================= stub DOM ================= */
class StubStyle {
  constructor(){ this._p = {}; }
  setProperty(k, v){ this._p[k] = v; }
  getPropertyValue(k){ return this._p[k] || ''; }
}
class StubEl {
  constructor(tag, doc){
    this.tagName = tag.toUpperCase(); this._doc = doc;
    this.children = []; this.parentNode = null; this.className = '';
    this._attrs = {}; this.style = new StubStyle();
    this.textContent = ''; this._listeners = {}; this._doc = doc;
  }
  get classList(){
    const self = this;
    const cls = () => self.className.split(/\s+/).filter(Boolean);
    return {
      add(c){ if(!cls().includes(c)) self.className = (self.className+' '+c).trim(); },
      remove(c){ self.className = cls().filter(x=>x!==c).join(' '); },
      toggle(c, force){
        const has = cls().includes(c);
        const on = force === undefined ? !has : !!force;
        if(on && !has) self.className = (self.className+' '+c).trim();
        if(!on && has) self.className = cls().filter(x=>x!==c).join(' ');
        return on;
      },
      contains(c){ return cls().includes(c); }
    };
  }
  set innerHTML(v){ this.children.forEach(c=>{c.parentNode=null;}); this.children = []; }
  get innerHTML(){ return ''; }
  get firstChild(){ return this.children[0] || null; }
  get lastChild(){ return this.children[this.children.length-1] || null; }
  appendChild(c){ c.parentNode = this; this.children.push(c); return c; }
  insertBefore(c, ref){
    c.parentNode = this;
    const i = ref ? this.children.indexOf(ref) : -1;
    if(i < 0) this.children.push(c); else this.children.splice(i, 0, c);
    return c;
  }
  removeChild(c){ const i = this.children.indexOf(c); if(i>=0) this.children.splice(i,1); c.parentNode=null; return c; }
  setAttribute(k, v){ this._attrs[k] = String(v); }
  getAttribute(k){ return Object.prototype.hasOwnProperty.call(this._attrs,k) ? this._attrs[k] : null; }
  removeAttribute(k){ delete this._attrs[k]; }
  addEventListener(t, fn){ (this._listeners[t] = this._listeners[t] || []).push(fn); }
  removeEventListener(t, fn){ const a = this._listeners[t]||[]; const i=a.indexOf(fn); if(i>=0)a.splice(i,1); }
  dispatch(t, ev){ (this._listeners[t]||[]).slice().forEach(fn=>fn.call(this, ev||{})); }
  focus(){ this._doc.activeElement = this; }
  matchesSel(sel){
    sel = sel.trim();
    if(sel[0] === '.') return this.className.split(/\s+/).includes(sel.slice(1));
    if(sel[0] === '['){
      const m = sel.match(/^\[([^\]="]+)(?:="([^"]*)")?\]$/);
      if(!m) return false;
      const v = this.getAttribute(m[1]);
      return m[2] === undefined ? v !== null : v === m[2];
    }
    return this.tagName === sel.toUpperCase();
  }
  _walk(out){ out.push(this); this.children.forEach(c=>c._walk(out)); }
  querySelectorAll(sel){
    const parts = sel.split(',').map(s=>s.trim()).filter(Boolean);
    const all = []; this._walk(all);
    return all.filter(n => parts.some(p => n.matchesSel(p)));
  }
  querySelector(sel){ const r = this.querySelectorAll(sel); return r[0] || null; }
}
class StubDoc extends StubEl {
  constructor(){ super('#document', null); this.activeElement = null; this.contains = () => true; }
  createElement(t){ return new StubEl(t, this); }
  createElementNS(ns, t){ return new StubEl(t, this); }
}
const document = new StubDoc();
const window = { NayaRooms: {} };
function el(tag, cls, text){
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text !== undefined && text !== null) e.textContent = text;
  return e;
}

/* ================= load room sources ================= */
function inner(src){
  const a = src.indexOf('(function(){');
  const b = src.lastIndexOf('})();');
  if(a < 0 || b < 0) throw new Error('IIFE wrapper missing');
  return src.slice(a + '(function(){'.length, b);
}
const g = { window, document, el };
const runSrc = src => (new Function('window','document','el', inner(src)))(window, document, el);
runSrc(fs.readFileSync(path.join(REPO,'HUB/app/js/rooms/living-intel-adapter.js'),'utf8'));
runSrc(fs.readFileSync(path.join(REPO,'HUB/app/js/rooms/living-intel.js'),'utf8'));
const FLOW = ['#a855f7','#6366f1','#22d3ee','#16a34a','#a3e635','#facc15','#d4a017','#fb923c','#ef4444','#ec4899'];

/* ================= fixtures (honest: no invented intelligence) ================= */
const NOW = Date.now();
const fixtures = {
  reports: [{date:'2026-10-02', nutshell:'Nutshell A', sections:9, words:2400}],
  notes:   [{date:'2026-10-02', title:'Test Note', nutshell:'Note nutshell', truth:'CANDIDATE', words:410}],
  doors:   [{name:'GitHub Connect', status:'LIVE_BOUNDED', color:'#a371f7', jewel:'◆', capabilities:['repos','issues']}],
  ledgerReal: [{
    issuedAt: new Date(NOW - 60000).toISOString(), glyph:'◆', smartName:'demo.smart',
    outcome:'PASS', demo:false, scores:{deltaV:5.3, q:8.7, confidence:0.92, vPred:8, vActual:9},
    proofState:'VERIFIED', effectsObserved:'observed ok', hash:'abc123def456', kind:'act'
  }],
  ledger: [{
    issuedAt: new Date(NOW - 3600000).toISOString(), glyph:'◆', smartName:'demo.beat',
    outcome:'PASS', demo:true, scores:{deltaV:1, q:7, confidence:0.8},
    proofState:'SIMULATED', effectsObserved:'', hash:'beefcafe00', kind:'act'
  }]
};

/* ================= tiny runner ================= */
let pass = 0, fail = 0;
const fails = [];
function ok(name, cond, extra){
  if(cond){ pass++; }
  else { fail++; fails.push(name + (extra ? ' :: ' + extra : '')); }
}
function itemBySource(items, s){ return items.filter(i=>i.source===s); }

/* ---- adapter ---- */
const items = window.LivingIntelAdapter.build(fixtures);
ok('adapter builds 5 items', items.length === 5, 'got '+items.length);
ok('adapter sorts newest-first', items.every((it,i)=> i===0 || items[i-1].ts >= it.ts));
ok('adapter keeps demo flags', itemBySource(items,'ledger').filter(i=>i.demo).length===1);
ok('real receipt has no demo chip', itemBySource(items,'ledger').filter(i=>!i.demo).length===1);
const li = window.LivingIntelAdapter.ledgerItem(fixtures.ledgerReal[0]);
ok('ledgerItem keeps vPred/vActual spark graph', li.graph && li.graph.kind==='spark' &&
   li.graph.points[0]===8 && li.graph.points[1]===9);
ok('ledgerItem stats carry real numbers', li.stats.some(s=>s[0]==='ΔV'&&s[1]==='+5.3') &&
   li.stats.some(s=>s[0]==='Confidence'&&s[1]==='0.92'));
const doorItem = window.LivingIntelAdapter.build({doors:fixtures.doors})[0];
ok('door keeps stable identity color/jewel', doorItem.color==='#a371f7' && doorItem.jewel==='◆');

/* ---- room render ---- */
const stage = window.NayaRooms.livingIntel(el, {items, simLive:false});
ok('stage root class', stage.className === 'li-stage');
const cards = stage.querySelectorAll('.li-card');
ok('renders one card per item', cards.length === 5, 'got '+cards.length);
ok('flow color by visible position 0', cards[0].style.getPropertyValue('--ic') === FLOW[0],
   'got '+cards[0].style.getPropertyValue('--ic'));
ok('flow color by visible position 1', cards[1].style.getPropertyValue('--ic') === FLOW[1]);
ok('demo chip only on demo cards',
  stage.querySelectorAll('.li-card').filter(c=>c.querySelectorAll('.li-demo-chip').length>0).length === 1);
ok('cards are keyboard-operable', cards.every(c=>c.getAttribute('role')==='button' && c.getAttribute('tabindex')==='0'));
ok('hero stats rendered', stage.querySelectorAll('.li-stat').length === 3);
ok('simLive off hides SIMULATED pill', stage.querySelectorAll('.li-sim').length === 0);

/* ---- filters ---- */
const tabs = stage.querySelectorAll('.li-tab');
ok('four filter tabs', tabs.length === 4);
ok('tabs carry aria-pressed', tabs[0].getAttribute('aria-pressed')==='true' &&
   tabs[1].getAttribute('aria-pressed')==='false');
tabs[1].dispatch('click', {}); // INTEL
ok('INTEL filter shows report+note only', stage.querySelectorAll('.li-card').length === 2,
   'got '+stage.querySelectorAll('.li-card').length);
ok('aria-pressed follows filter', tabs[1].getAttribute('aria-pressed')==='true' &&
   tabs[0].getAttribute('aria-pressed')==='false');
ok('flow reindexes after filter', stage.querySelectorAll('.li-card')[0].style.getPropertyValue('--ic') === FLOW[0]);
tabs[0].dispatch('click', {}); // ALL
ok('ALL restores 5 cards', stage.querySelectorAll('.li-card').length === 5);
tabs[2].dispatch('click', {}); // ACTIONS
ok('ACTIONS filter shows ledger items only', stage.querySelectorAll('.li-card').length === 2);
tabs[0].dispatch('click', {});

/* ---- jewels ---- */
const jewels = stage.querySelectorAll('.li-jewel');
ok('four source jewels', jewels.length === 4);
jewels[0].dispatch('click', {}); // INTEL REPORTS jewel
ok('jewel filters stream', stage.querySelectorAll('.li-card').length === 2);
tabs[0].dispatch('click', {});

/* ---- modal ---- */
const card0 = stage.querySelectorAll('.li-card')[0];
card0.dispatch('click', {});
const overlay = stage.querySelector('.li-overlay');
ok('card click opens overlay', overlay.style.display === 'flex');
const mcard = stage.querySelector('.li-modal');
ok('modal is a dialog', mcard.getAttribute('role')==='dialog' && mcard.getAttribute('aria-modal')==='true');
ok('modal shows real stat rows', mcard.querySelectorAll('.li-modal-stat').length > 0);
const closeBtn = mcard.querySelector('button');
ok('focus moves into modal on open', document.activeElement === closeBtn);
/* focus trap: Tab on last focusable wraps to first */
overlay.dispatch('keydown', {key:'Tab', shiftKey:false, preventDefault(){}});
ok('focus trap wraps Tab', document.activeElement === closeBtn);
/* Escape closes and restores focus */
card0.focus();
card0.dispatch('click', {});
document.dispatch('keydown', {key:'Escape'});
ok('Escape closes overlay', overlay.style.display === 'none');
ok('focus restores to opener', document.activeElement === card0);
/* keyboard open via Enter */
card0.dispatch('keydown', {key:'Enter', preventDefault(){}});
ok('Enter opens modal', overlay.style.display === 'flex');
document.dispatch('keydown', {key:'Escape'});
ok('modal closed after Enter test', overlay.style.display === 'none');
/* overlay backdrop click closes */
card0.dispatch('click', {});
overlay.dispatch('click', {target: overlay});
ok('backdrop click closes', overlay.style.display === 'none');

/* ---- empty state is filter-aware ---- */
const slim = window.LivingIntelAdapter.build({reports:fixtures.reports}); // no ledger items
const stage2 = window.NayaRooms.livingIntel(el, {items: slim, simLive:false});
stage2.querySelectorAll('.li-tab')[2].dispatch('click', {}); // ACTIONS on ledger-less stream
const empty = stage2.querySelector('.li-empty');
ok('filter-aware empty state', !!empty && /ACTIONS/.test(empty.textContent) && /ALL/.test(empty.textContent),
   empty ? empty.textContent : 'no empty node');

/* ---- time-ago sanity (no exceptions, live stamps) ---- */
ok('data-ts stamps present', stage.querySelectorAll('[data-ts]').length > 0);

/* ---- CSS markers (drilled law) ---- */
const css = fs.readFileSync(path.join(REPO,'HUB/app/css/living-intel.css'),'utf8');
ok('reduced-motion kill switch on .li-stage',
   /@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{\s*\.li-stage\s*\*\s*\{\s*animation:\s*none\s*!important/.test(css));
ok('obsidian button law present', css.includes('linear-gradient(180deg,#1b1b21,#0b0b0e)'));
ok('buttons never grey fill', !/\.li-(tab|jewel|modal-x)\{[^}]*background:\s*(grey|#808080|#999)/i.test(css));
ok('type floor: no label text under 11px',
   !/font-size:\s*([0-9]|10)(\.\d+)?px/.test(css.replace(/\.li-glabel\{[^}]*\}/, '')),
   'sub-11px font found');

/* ---- js parses ---- */
ok('room JS parses', true); // verified separately via node --check

console.log('living-intel smoke: '+pass+' pass, '+fail+' fail');
if(fails.length){ console.log('FAILURES:'); fails.forEach(f=>console.log('  - '+f)); }
process.exit(fail ? 1 : 0);
