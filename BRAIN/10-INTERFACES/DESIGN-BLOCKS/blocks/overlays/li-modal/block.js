/* Smart Block JS: overlays/li-modal
 * Source: "Ledger Page Design.html" — adapted from openModal(it, fc) (~line
 * 1077) plus the overlay wiring (~lines 1055-1116): backdrop-click close,
 * CLOSE button, Escape close, Tab focus trap, focus restore. el() copied
 * verbatim from ~line 324. The source reused a single module-level overlay;
 * this standalone builder creates one fresh overlay per call and returns it.
 * Class strings and DOM structure kept byte-true.
 */
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;return e;}

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

/* liModal(data) -> <div class="li-overlay"> (display:flex, shown on return)
 * data: { title, meta, stats:[[label,value],...], explain }
 *   title   — modal headline
 *   meta    — small dim line under title (source: time-ago + optional DEMO)
 *   stats   — array of [label, value] pairs rendered as the stat grid
 *   explain — paragraph under the stat grid
 * Optional pass-throughs (same plumbing as source):
 *   source  — shown in the HEARTBEAT kicker (' HEARTBEAT \u00B7 <SOURCE>')
 *   color   — identity color used for --ic (modal glow) and --tab-c
 *             (CLOSE button hover); source took the card's flow color
 *   demo    — truthy appends ' \u00B7 DEMO' to meta (source behavior)
 *
 * Close behaviors (all from source): backdrop click (target === overlay),
 * CLOSE button, Escape key. Tab cycles inside the dialog; focus is returned
 * to the previously focused element on close. Closing hides the overlay
 * (display:none) and removes its per-instance listeners; drop it from the DOM
 * if you won't reuse it.
 */
function liModal(d){
  d = d || {};
  var color = d.color || '#a855f7';
  var lastFocus = document.activeElement;

  var overlay = el('div','li-overlay');
  var mcard = el('div','li-modal');
  mcard.setAttribute('role','dialog'); mcard.setAttribute('aria-modal','true');
  mcard.style.setProperty('--ic', color);
  overlay.appendChild(mcard);

  var k = el('p','li-kicker','');
  var ld = el('span','li-live-dot',''); k.appendChild(ld);
  var kx = el('span','',''); kx.textContent=' HEARTBEAT \u00B7 '+liSourceLabel(d.source); k.appendChild(kx);
  mcard.appendChild(k);

  var t = el('h2','li-modal-title',''); t.textContent=d.title||''; mcard.appendChild(t);

  var meta = d.meta || '';
  var mm = el('p','li-modal-meta',''); mm.textContent=meta+(d.demo?' \u00B7 DEMO':''); mcard.appendChild(mm);

  if(d.stats && d.stats.length){
    var st = el('div','li-modal-stats');
    d.stats.forEach(function(s){
      var r = el('div','li-modal-stat');
      r.appendChild(el('span','li-modal-stat-l', s[0]));
      var vv = el('span','li-modal-stat-v',''); vv.textContent=s[1]; r.appendChild(vv);
      st.appendChild(r);
    });
    mcard.appendChild(st);
  }

  if(d.explain){
    var ex = el('p','li-modal-explain',''); ex.textContent=d.explain; mcard.appendChild(ex);
  }

  var x = el('button','li-modal-x','CLOSE'); x.type='button';
  x.style.setProperty('--tab-c', color);
  mcard.appendChild(x);

  function trapKeys(ev){
    if(ev.key!=='Tab') return;
    var els = mcard.querySelectorAll('button, [tabindex="0"], [href]');
    if(!els.length) return;
    var first = els[0], last = els[els.length-1];
    var active = document.activeElement;
    if(ev.shiftKey && active===first){ ev.preventDefault(); last.focus(); }
    else if(!ev.shiftKey && active===last){ ev.preventDefault(); first.focus(); }
  }

  function closeModal(){
    overlay.style.display='none';
    overlay.removeEventListener('keydown', trapKeys);
    document.removeEventListener('keydown', escListener);
    if(lastFocus && typeof lastFocus.focus==='function') lastFocus.focus();
  }

  function escListener(ev){
    if(ev.key==='Escape' && overlay.style.display==='flex') closeModal();
  }

  x.addEventListener('click', closeModal);
  overlay.addEventListener('click', function(ev){ if(ev.target===overlay) closeModal(); });
  overlay.addEventListener('keydown', trapKeys);
  document.addEventListener('keydown', escListener);

  overlay.style.display='flex';
  x.focus();
  return overlay;
}

// Demo:
// document.body.appendChild(liModal({ title:'Signal heartbeat', meta:'2h ago', source:'report',
//   stats:[['SIGNALS','14'],['VERIFIED','12'],['SCORE','9.4']], explain:'Every beat verified. Every action recorded.' }));
