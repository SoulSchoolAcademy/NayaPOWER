/* Smart Block JS: spaces/sp-card
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Only the data plumbing was adapted; class strings and DOM structure are source-faithful.
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
 * Space card with cover art.
 *   opts: { name, topic, desc, accent, members, joined, privacy, onClick, onJoin, avatars }
 *   name     — space name (string)
 *   topic    — topic label (string, rendered uppercase by CSS)
 *   desc     — short description (string)
 *   accent   — accent color, sets CSS var --sc (defaults to #7c3aed per block.css)
 *   members  — member count (number)
 *   joined   — bool; controls the join button label/state
 *   privacy  — 'public' | 'private'; shows the 🔒 Private badge when 'private'
 *   avatars  — optional array of pre-rendered avatar Elements (from the avatar sibling block)
 *   onClick  — card click handler (default: none)
 *   onJoin   — join button click handler, receives (joinedAfter, card). Default toggles the button label.
 */
function spCard(opts){
  opts = opts || {};
  var name = opts.name || 'Untitled Space';
  var topic = opts.topic || '';
  var members = opts.members || 0;

  var card = el('div','sp-card');
  if(opts.accent) card.style.setProperty('--sc', opts.accent);

  var cover = el('div','sp-card-cover sp-cover');
  cover.appendChild(el('div','sp-card-name', name));
  cover.appendChild(el('div','sp-card-topic', topic));
  card.appendChild(cover);

  var body = el('div','sp-card-body');
  body.appendChild(el('div','sp-card-desc', opts.desc || ''));

  var meta = el('div','sp-card-meta');
  var stack = el('div','sp-mstack');
  (opts.avatars || []).slice(0,4).forEach(function(a){ stack.appendChild(a); });
  meta.appendChild(stack);
  meta.appendChild(el('span','sp-mcount', members + (members === 1 ? ' member' : ' members')));
  if(opts.privacy === 'private'){
    meta.appendChild(el('span','sp-priv','🔒 Private'));
  }
  var joined = !!opts.joined;
  var jbtn = el('button','sp-join' + (joined ? ' in' : ''), joined ? '✓ Joined' : '＋ Join');
  jbtn.addEventListener('click', function(e){
    e.stopPropagation();
    if(typeof opts.onJoin === 'function'){ opts.onJoin(!joined, card); return; }
    joined = !joined;
    jbtn.className = 'sp-join' + (joined ? ' in' : '');
    jbtn.textContent = joined ? '✓ Joined' : '＋ Join';
  });
  meta.appendChild(jbtn);
  body.appendChild(meta);
  card.appendChild(body);

  if(typeof opts.onClick === 'function'){
    card.addEventListener('click', function(){ opts.onClick(name); });
  }
  return card;
}

/**
 * Responsive grid wrapper for space cards.
 */
function spGrid(cards){
  var grid = el('div','sp-grid');
  (cards || []).forEach(function(c){ grid.appendChild(c); });
  return grid;
}

// Demo:
// document.body.appendChild(spGrid([
//   spCard({name:'Design Guild', topic:'Creativity', desc:'World-class interface craft.', members:128, accent:'#7c3aed'}),
//   spCard({name:'Morning Builders', topic:'Engineering', desc:'Ship before breakfast.', members:64, joined:true, accent:'#0d9e6f'})
// ]));
