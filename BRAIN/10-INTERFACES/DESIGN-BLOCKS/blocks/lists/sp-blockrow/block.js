/* Smart Block JS: lists/sp-blockrow
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Adapted from openBlockPicker (source ~line 1616): sp-blockrow with sp-blockrow-t/
 * sp-blockrow-c inside sp-blocklist. Only data plumbing changed; class strings and
 * DOM structure are source-faithful.
 */

/* ============ helpers (from source ~line 724) ============ */
function el(tag, cls, text){
  var e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text !== undefined && text !== null) e.textContent = text;
  return e;
}

/* ============ builders ============ */

/**
 * Block list: rows with title + uppercase category label.
 *   items — array of { title, category, action }
 *     title    — row title (string)
 *     category — category label, rendered UPPER-CASE (source-faithful)
 *     action   — optional { label, active, onClick }; emitted as the source's
 *                'sp-pin-act' button ('✓ Pinned' when active). sp-pin-act is
 *                styled by a sibling block, not this block's CSS (see README).
 */
function spBlockList(items){
  var list = el('div','sp-blocklist');
  (items || []).forEach(function(b){
    var row = el('div','sp-blockrow');
    var info = el('div');
    info.appendChild(el('div','sp-blockrow-t', b.title));
    info.appendChild(el('div','sp-blockrow-c', String(b.category || '').toUpperCase()));
    row.appendChild(info);
    if(b.action){
      var btn = el('button','sp-pin-act' + (b.action.active ? ' on' : ''), b.action.label || 'Pin');
      if(typeof b.action.onClick === 'function' && !b.action.active){
        (function(item){ btn.addEventListener('click', function(){ b.action.onClick(item); }); })(b);
      }
      row.appendChild(btn);
    }
    list.appendChild(row);
  });
  return list;
}

// Demo:
// document.body.appendChild(spBlockList([
//   {title:'The Awesome Thesis', category:'Intelligence'},
//   {title:'Judgment Rule', category:'Governance', action:{label:'Pin', active:false, onClick:function(b){ console.log('pin', b.title); }}},
//   {title:'Value Function', category:'Governance', action:{label:'✓ Pinned', active:true}}
// ]));
