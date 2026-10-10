/* Smart Block: inputs/sn-pill
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Adapted from renderSnTabs (~line 1117), ensureSnMenu/openSnTabMenu,
 * ensureSnPop/openSnTabEditor, placeNear, closeSnPanels (~lines 1117-1265).
 * App-state calls replaced by params:
 *   loadSnTabs/saveSnTabs/sortedSnTabs -> plain tab objects + callbacks
 *   colorFor(t.id)  -> opts.color (--tc), default '#fff'
 *   activeSnTab     -> tab.active / opts.active
 *   onSelect(t.id)  -> opts.onSelect(tab, pill)
 *   uid('st')       -> tab.id supplied by opts.id (or ''), consumer assigns
 *   toast()         -> callbacks only; no invented messages
 * The context menu and popover editor are shared singletons appended to
 * document.body (faithful to the source). Popover toggles on ⋯ click or
 * right-click; the editor carries the heart/star toggles.
 */
(function(){
'use strict';

/* ============ helper (from source ~line 724) ============ */
function el(tag, cls, text){
  var e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text !== undefined && text !== null) e.textContent = text;
  return e;
}

/* ============ shared panels ============ */
function closeSnPanels(){
  document.querySelectorAll('.sn-menu,.sn-pop').forEach(function(p){ p.style.display = 'none'; });
}
function placeNear(anchor, panel, oy){
  oy = oy || 8;
  var r = anchor.getBoundingClientRect();
  var W = panel.offsetWidth || 280, H = panel.offsetHeight || 160;
  var left = Math.min(window.innerWidth - W - 8, Math.max(8, r.left));
  var top = Math.min(window.innerHeight - H - 8, r.bottom + oy);
  panel.style.left = left + 'px';
  panel.style.top = top + 'px';
}
function snMenuEl(){
  var m = document.querySelector('.sn-menu.sp-tabs-menu');
  if(m) return m;
  m = el('div','sn-menu sp-tabs-menu');
  m.setAttribute('role','menu');
  m.innerHTML =
    '<div class="mi" data-act="edit">✏️ Edit</div>' +
    '<div class="mi" data-act="heart">💜 Set Purple Heart</div>' +
    '<div class="mi" data-act="star">⭐ Gold Star</div>' +
    '<div class="mi" data-act="remove">✕ Remove</div>';
  document.body.appendChild(m);
  return m;
}
function snPopEl(){
  var p = document.querySelector('.sn-pop.sp-tabs-pop');
  if(p) return p;
  p = el('div','sn-pop sp-tabs-pop');
  p.setAttribute('role','dialog');
  p.innerHTML =
    '<h3 class="sn-pop-title">Add Tab</h3>' +
    '<div class="row"><label>Label<br><input class="sn-in-label" placeholder="e.g. Design"></label></div>' +
    '<div class="toggles">' +
    '<div class="tgl sn-tgl-heart">💜 Purple Heart</div>' +
    '<div class="tgl sn-tgl-star">⭐ Gold Star</div>' +
    '</div>' +
    '<div class="ft"><button class="sn-btn sn-cancel">Cancel</button>' +
    '<button class="sn-btn primary sn-save">Save</button></div>';
  document.body.appendChild(p);
  return p;
}

/* Repaint one pill from its tab data (same structure as the initial build). */
function snPaint(pill, tab, opts){
  pill.className = 'sn-pill' + (tab.heart ? ' heart' : tab.star ? ' star' : '') + (tab.active ? ' on' : '');
  pill.style.setProperty('--tc', tab.color || '#fff');
  pill.setAttribute('data-id', tab.id || '');
  pill.innerHTML = '';
  pill.appendChild(el('span','sn-label', tab.label || ''));
  if(tab.heart){ pill.appendChild(el('span','sn-mark','💜')); }
  else if(tab.star){ pill.appendChild(el('span','sn-mark','⭐')); }
  if(opts.more !== false){
    var more = el('button','sn-more','⋯');
    more.setAttribute('aria-label','Tab options');
    more.addEventListener('click', function(e){
      e.stopPropagation();
      snOpenMenu(pill, tab, opts);
    });
    pill.appendChild(more);
  }
}

function snOpenMenu(pill, tab, opts){
  closeSnPanels();
  var m = snMenuEl();
  placeNear(pill, m, 6);
  m.style.display = 'block';
  m.onclick = function(e){
    var mi = e.target.closest('.mi'); if(!mi) return;
    var act = mi.getAttribute('data-act');
    m.style.display = 'none';
    if(act === 'edit'){ snOpenEditor(tab, pill, opts); }
    else if(act === 'heart'){
      tab.heart = true; tab.star = false;
      snPaint(pill, tab, opts);
      if(typeof opts.onMark === 'function') opts.onMark(tab, 'heart', pill);
    }
    else if(act === 'star'){
      tab.star = true; tab.heart = false;
      snPaint(pill, tab, opts);
      if(typeof opts.onMark === 'function') opts.onMark(tab, 'star', pill);
    }
    else if(act === 'remove'){
      var keep = false;
      if(typeof opts.onRemove === 'function') keep = opts.onRemove(tab, pill) === false;
      if(!keep && pill.parentNode) pill.parentNode.removeChild(pill);
    }
  };
}

function snOpenEditor(tab, anchor, opts){
  closeSnPanels();
  var pop = snPopEl();
  var isNew = !tab;
  pop.querySelector('.sn-pop-title').textContent = isNew ? 'Add Tab' : 'Edit Tab';
  var inLabel = pop.querySelector('.sn-in-label');
  var tHeart = pop.querySelector('.sn-tgl-heart');
  var tStar = pop.querySelector('.sn-tgl-star');
  inLabel.value = tab ? tab.label : '';
  tHeart.classList.toggle('on', !!(tab && tab.heart));
  tStar.classList.toggle('on', !!(tab && tab.star));
  tHeart.onclick = function(){
    tHeart.classList.toggle('on');
    if(tHeart.classList.contains('on')) tStar.classList.remove('on');
  };
  tStar.onclick = function(){
    tStar.classList.toggle('on');
    if(tStar.classList.contains('on')) tHeart.classList.remove('on');
  };
  placeNear(anchor, pop, 6);
  pop.style.display = 'block';
  pop.querySelector('.sn-cancel').onclick = function(){ pop.style.display = 'none'; };
  pop.querySelector('.sn-save').onclick = function(){
    var label = (inLabel.value || '').trim() || 'New Tab';
    var heart = tHeart.classList.contains('on');
    var star = tStar.classList.contains('on');
    pop.style.display = 'none';
    if(isNew){
      if(typeof opts.onAdd === 'function') opts.onAdd({label: label, heart: heart, star: star});
    } else {
      tab.label = label; tab.heart = heart; tab.star = star;
      snPaint(anchor, tab, opts);
      if(typeof opts.onChange === 'function') opts.onChange(tab, anchor);
    }
  };
}

var _snDocWired = false;
function wireSnDoc(){
  if(_snDocWired) return; _snDocWired = true;
  document.addEventListener('click', function(e){
    if(!e.target.closest('.sn-pill') && !e.target.closest('.sn-menu') && !e.target.closest('.sn-pop')) closeSnPanels();
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeSnPanels(); });
}

/* ---- Smart Note pill ----
 * opts = {id, label, color, heart, star, active, more,
 *         onSelect(tab, pill), onMark(tab, mark, pill),
 *         onChange(tab, pill), onRemove(tab, pill)}
 * Returns the .sn-pill element. The live tab data is also on pill._snTab.
 */
function snPill(opts){
  opts = opts || {};
  wireSnDoc();
  var tab = {
    id: opts.id || '',
    label: opts.label || 'Tab',
    color: opts.color || '#fff',
    heart: !!opts.heart,
    star: !!opts.star,
    active: !!opts.active
  };
  var pill = el('div','');
  pill._snTab = tab;
  snPaint(pill, tab, opts);
  pill.addEventListener('click', function(){
    if(typeof opts.onSelect === 'function') opts.onSelect(tab, pill);
  });
  pill.addEventListener('contextmenu', function(e){
    e.preventDefault();
    snOpenMenu(pill, tab, opts);
  });
  return pill;
}

/* ---- dashed "+ Add" pill; Save in the editor calls opts.onAdd({label, heart, star}) ---- */
function snPillAdd(opts){
  opts = opts || {};
  wireSnDoc();
  var add = el('div','sn-pill add');
  add.style.setProperty('--tc','#fff');
  add.appendChild(el('span','sn-label','＋ Add'));
  add.addEventListener('click', function(){ snOpenEditor(null, add, opts); });
  return add;
}

/* expose */
window.snPill = snPill;
window.snPillAdd = snPillAdd;
window.snClosePanels = closeSnPanels;

/* Demo:
   var row = document.createElement('div');
   row.style.cssText = 'display:flex;gap:8px;flex-wrap:wrap;';
   var mk = function(o){
     o.onSelect = function(t, p){ row.querySelectorAll('.sn-pill').forEach(function(x){ x.classList.remove('on'); if(x._snTab) x._snTab.active = false; }); t.active = true; p.classList.add('on'); };
     return snPill(o);
   };
   row.appendChild(mk({id:'st-all', label:'All', color:'#fff', active:true}));
   row.appendChild(mk({id:'st-design', label:'Design', color:'#7c3aed', heart:true}));
   row.appendChild(mk({id:'st-ai', label:'AI', color:'#d4a017', star:true}));
   var add = snPillAdd({onAdd: function(d){ row.insertBefore(mk(Object.assign({id:'st-' + Date.now(), color:'#1e6fd9'}, d)), add); }});
   row.appendChild(add);
   document.body.appendChild(row);
*/
})();
