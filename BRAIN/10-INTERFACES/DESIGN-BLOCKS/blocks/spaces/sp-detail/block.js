/* Smart Block JS: spaces/sp-detail
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Adapted from renderDetail (source ~line 1458). Only the DETAIL SHELL is extracted —
 * cover + head row + title/topic/desc + action row + content container. Tab logic is
 * intentionally excluded (see README; tabs come from the tabs/sp-dtabs sibling block).
 * Only data plumbing changed; class strings and DOM structure are source-faithful.
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
 * Space detail view shell: cover, head row (title/topic/desc), action row, content container.
 *   opts: { name, topic, desc, accent, members, privacy, joined,
 *           onBack, onJoin, onInvite, onMessage, onMail }
 *   members  — member count (number)
 *   privacy  — 'public' | 'private'; topic line shows '🔒 Private' or 'Public' (source-faithful)
 *   joined   — bool; controls the join button label/state
 *   accent   — accent color, sets CSS var --sc (defaults to #7c3aed per block.css)
 *   onJoin   — called with (joinedAfter) when the join button is clicked
 *   onInvite / onMessage / onMail — action-button handlers (default: no-op)
 *
 * Returns the .sp-detail element; its tab content container is available as wrap.content
 * (the .sp-dcontent element) for the tabs sibling block to fill.
 */
function spDetail(opts){
  opts = opts || {};
  var name = opts.name || 'Untitled Space';
  var members = opts.members || 0;

  var wrap = el('div','sp-detail');
  if(opts.accent) wrap.style.setProperty('--sc', opts.accent);

  // Back
  var back = el('button','sp-back','← All Spaces');
  if(typeof opts.onBack === 'function') back.addEventListener('click', opts.onBack);
  wrap.appendChild(back);

  // Header
  var head = el('div','sp-dhead');
  var hcover = el('div','sp-dcover');
  hcover.appendChild(el('div','sp-dtitle', name));
  hcover.appendChild(el('div','sp-dtopic',
    (opts.topic || '') + (opts.privacy === 'private' ? ' · 🔒 Private' : ' · Public')));
  head.appendChild(hcover);
  head.appendChild(el('div','sp-ddesc', opts.desc || ''));

  // Head row: member count + action buttons
  var hrow = el('div','sp-dhrow');
  hrow.appendChild(el('span','sp-dcount', members + (members === 1 ? ' member' : ' members')));

  var joined = !!opts.joined;
  var jbtn = el('button','sp-join' + (joined ? ' in' : ''), joined ? '✓ Joined' : '＋ Join Space');
  jbtn.addEventListener('click', function(){
    joined = !joined;
    jbtn.className = 'sp-join' + (joined ? ' in' : '');
    jbtn.textContent = joined ? '✓ Joined' : '＋ Join Space';
    if(typeof opts.onJoin === 'function') opts.onJoin(joined);
  });
  hrow.appendChild(jbtn);

  var inviteBtn = el('button','sp-invite-btn','✉ Invite');
  if(typeof opts.onInvite === 'function') inviteBtn.addEventListener('click', function(){ opts.onInvite(); });
  hrow.appendChild(inviteBtn);

  var msgBtn = el('button','sp-invite-btn','💬 Message Space');
  if(typeof opts.onMessage === 'function') msgBtn.addEventListener('click', function(){ opts.onMessage(); });
  hrow.appendChild(msgBtn);

  var mailSpBtn = el('button','sp-invite-btn','✉ Mail Space');
  if(typeof opts.onMail === 'function') mailSpBtn.addEventListener('click', function(){ opts.onMail(); });
  hrow.appendChild(mailSpBtn);

  head.appendChild(hrow);
  wrap.appendChild(head);

  // Content container (filled by the tabs sibling block)
  var content = el('div','sp-dcontent');
  wrap.appendChild(content);
  wrap.content = content;

  return wrap;
}

// Demo:
// var d = spDetail({name:'Design Guild', topic:'Creativity', desc:'World-class interface craft.',
//   members:128, accent:'#7c3aed'});
// d.content.textContent = 'Tab content goes here.';
// document.body.appendChild(d);
