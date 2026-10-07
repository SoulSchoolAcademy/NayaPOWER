/* Smart Block: tabs/sp-dtabs
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Adapted from the tabbar construction in renderDetail (~line 1505).
 * App-state calls replaced by params:
 *   state.detailTab    -> tab.active per item
 *   spaceChat(s.id)    -> tab.count per item (unread badge)
 *   renderDetail(root) -> opts.onSelect(tab, index)
 * The specimen must set --sc (via opts.accent), e.g. --sc:#7c3aed.
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

/* ---- underline tabs with count badges ----
 * tabs = [{label, count?, active?}]
 * opts = {accent:'#7c3aed', onSelect(tab, index)?}
 * Returns the .sp-dtabs element. Re-call to re-render after selection,
 * or flip classes yourself:
 *   tabbar.querySelectorAll('.sp-dtab').forEach(...)
 */
function spDtabs(tabs, opts){
  opts = opts || {};
  var tabbar = el('div','sp-dtabs');
  tabbar.style.setProperty('--sc', opts.accent || '#7c3aed');
  (tabs || []).forEach(function(t, i){
    var b = el('button','sp-dtab' + (t.active ? ' on' : ''), t.label);
    if(t.count){
      b.appendChild(el('span','sp-dtab-n', String(t.count)));
    }
    b.addEventListener('click', function(){
      if(typeof opts.onSelect === 'function') opts.onSelect(t, i);
    });
    tabbar.appendChild(b);
  });
  return tabbar;
}

/* expose */
window.spDtabs = spDtabs;

/* Demo:
   var tabs = [{label:'Posts'},{label:'Members',count:12},{label:'Chat',count:3,active:true},{label:'About'}];
   var bar = spDtabs(tabs, {accent:'#7c3aed', onSelect: function(t){
     tabs.forEach(function(x){ x.active = (x === t); });
     var n = spDtabs(tabs, this); document.body.replaceChild(n, bar); bar = n;
   }});
   document.body.appendChild(bar);
*/
})();
