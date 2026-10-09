/* Smart Block JS: feed/li-card
 * Source: "Ledger Page Design.html" — adapted from cardNode(it, idx, animate)
 * (~line 903). el() helper copied verbatim from ~line 324. sourceLabel and
 * timeAgo copied from source (~lines 1190, 694). App-state references
 * (FLOW cycling by index, state.search title-highlight, direct openModal
 * binding) are replaced with plain data params. Class strings and DOM
 * structure are kept byte-true.
 */
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;return e;}

var LI_FLOW = ['#a855f7','#6366f1','#22d3ee','#16a34a','#a3e635'];

function liSourceLabel(s){
  return {report:'INTEL REPORT', note:'SMART NOTE', ledger:'LEDGER', connect:'CONNECT'}[s] || String(s||'').toUpperCase();
}

function liTimeAgo(ts){
  var s = Math.max(0, Math.floor((Date.now()-ts)/1000));
  if(s < 60) return 'just now';
  var m = Math.floor(s/60); if(m < 60) return m+'m ago';
  var h = Math.floor(m/60); if(h < 24) return h+'h ago';
  var d = Math.floor(h/24); if(d < 7) return d+'d ago';
  return Math.floor(d/7)+'w ago';
}

/* liCard(data) -> <article class="li-card">
 * data: { title, summary, source, time, jewel, hint }
 *   title   — card headline (string)
 *   summary — nutshell body text (string, optional)
 *   source  — 'report' | 'note' | 'ledger' | 'connect' | any label
 *   time    — ms epoch timestamp; rendered as time-ago
 *   jewel   — glyph shown in the top row (string)
 *   hint    — hint pill text; defaults to 'TAP FOR HEARTBEAT'
 * Optional pass-throughs (same plumbing as source):
 *   meta    — small mono line under summary (dropped from signature, kept as-is)
 *   demo    — truthy adds the DEMO chip
 *   color   — identity color (--ic); defaults to LI_FLOW[index % 5]
 *   index   — card index for --i (bar animation stagger) and color cycling
 *   animate — truthy: staggered entry animation (animationDelay), falsy: no entry anim
 *   flash   — truthy: adds the `li-flash` class (liflash animation hook)
 *   onOpen  — function(data); click / Enter / Space calls it (source bound openModal)
 */
function liCard(d){
  d = d || {};
  var idx = d.index || 0;
  var color = d.color || LI_FLOW[idx % LI_FLOW.length];
  var card = el('article','li-card');
  card.style.setProperty('--ic', color);
  card.style.setProperty('--i', idx);
  if(d.animate) card.style.animationDelay = Math.min(idx*0.04, 0.8)+'s';
  else card.style.animation = 'none';
  if(d.flash) card.classList.add('li-flash');
  card.setAttribute('role','button'); card.setAttribute('tabindex','0');
  card.setAttribute('aria-label','Inspect: '+(d.title||''));

  var top = el('div','li-card-top');
  var jw = el('span','li-card-j',''); jw.textContent=d.jewel||''; top.appendChild(jw);
  top.appendChild(el('span','li-card-s', liSourceLabel(d.source)));
  var ta = el('span','li-card-t',''); ta.textContent=liTimeAgo(d.time); ta.setAttribute('data-ts', d.time);
  top.appendChild(ta);
  if(d.demo) top.appendChild(el('span','li-demo-chip','DEMO'));
  card.appendChild(top);

  var t = el('h2','li-card-title',''); t.textContent=d.title||''; card.appendChild(t);
  if(d.summary){ var n=el('p','li-card-n',''); n.textContent=d.summary; card.appendChild(n); }
  if(d.meta){ var m=el('p','li-card-m',''); m.textContent=d.meta; card.appendChild(m); }

  var hint = el('span','li-card-hint', d.hint || 'TAP FOR HEARTBEAT');
  card.appendChild(hint);

  if(typeof d.onOpen==='function'){
    card.addEventListener('click', function(){ d.onOpen(d); });
    card.addEventListener('keydown', function(ev){
      if(ev.key==='Enter'||ev.key===' '){ ev.preventDefault(); d.onOpen(d); }
    });
  }
  return card;
}

// Demo:
// var node = liCard({ title:'Signals converge on the 10/10 push', summary:'Nine lanes report green against live bytes.', source:'report', time:Date.now()-36e5, jewel:'\u25C6', hint:'TAP FOR HEARTBEAT', index:0, animate:true, onOpen:function(d){ console.log('open', d.title); } });
// document.querySelector('.li-stage').appendChild(node);
