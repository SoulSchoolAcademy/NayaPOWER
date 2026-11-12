/* Smart Block JS: spaces/sp-inv-chip
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Chip builder adapted from source ~line 1333 (el('button','sp-inv-chip') with
 * sp-inv-chip-name + sp-inv-chip-join); invite list adapted from ~line 2086
 * (sp-invite-list / sp-invite-name / sp-invite-add). Only data plumbing changed;
 * class strings and DOM structure are source-faithful.
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
 * Invite chip — "tap to step into a room" card.
 *   opts: { name, accent, onJoin }
 *   name    — space name
 *   accent  — accent color, sets CSS var --sc (defaults to #7c3aed per block.css)
 *   onJoin  — click handler, receives (name)
 */
function spInvChip(opts){
  opts = opts || {};
  var name = opts.name || 'Unnamed Space';

  var chip = el('button','sp-inv-chip');
  if(opts.accent) chip.style.setProperty('--sc', opts.accent);
  chip.appendChild(el('span','sp-inv-chip-name', name));
  chip.appendChild(el('span','sp-inv-chip-join','Join \u2192'));
  if(typeof opts.onJoin === 'function'){
    chip.addEventListener('click', function(){ opts.onJoin(name); });
  }
  return chip;
}

/**
 * One invite-list row: avatar + name + Invite button.
 *   opts: { name, avatar, onAdd }
 *   avatar — optional pre-rendered avatar Element (from the avatar sibling block);
 *            source calls avatar(p,'sm') — replaced with a plain parameter.
 *   onAdd  — click handler, receives (name)
 */
function spInviteRow(opts){
  opts = opts || {};
  var name = opts.name || 'Unknown';

  var row = el('div','sp-invite-row');
  if(opts.avatar) row.appendChild(opts.avatar);
  row.appendChild(el('span','sp-invite-name', name));
  var add = el('button','sp-invite-add','＋ Invite');
  if(typeof opts.onAdd === 'function'){
    add.addEventListener('click', function(){ opts.onAdd(name); });
  }
  row.appendChild(add);
  return row;
}

/**
 * Invite list wrapper (scrollable, max-height 320px per block.css).
 *   rows — array of Elements (built by spInviteRow)
 */
function spInviteList(rows){
  var list = el('div','sp-invite-list');
  (rows || []).forEach(function(r){ list.appendChild(r); });
  return list;
}

// Demo:
// document.body.appendChild(spInviteList([
//   spInviteRow({name:'Ada Lovelace', onAdd:function(n){ alert('Invited ' + n); }}),
//   spInviteRow({name:'Grace Hopper'})
// ]));
// document.body.appendChild(spInvChip({name:'Design Guild', accent:'#7c3aed'}));
