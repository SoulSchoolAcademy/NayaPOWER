/* SMART LISTS — categorization as a lens.
   Lists hold references to canonical objects — never copies. The inbox list
   is where Today/Feed "Add to list" lands. Favorites are pointers, not duplicates. */

(function () {
  const { el, Board } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS, byId } = C;
  const ACC = 'var(--accent-lists)';

  const CSS = `
  .lists-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#120a1c 0%,#0b0912 60%,#08060d 100%);
    border:1px solid #9d75ff2e; box-shadow:0 30px 80px -20px #9d75ff33, inset 0 1px 0 #ffffff14; }
  .lists-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05;
    background:linear-gradient(115deg,#fff 30%,#d9c8ff 70%,#9d75ff); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .list-shelf { margin-top:22px; }
  .list-row { display:flex; gap:14px; align-items:center; padding:14px 16px; border-radius:14px;
    background:#100d18; border:1px solid var(--line); margin-bottom:10px; cursor:pointer; }
  .list-row:hover { border-color:var(--purple); }
  .list-row .t { font-weight:700; font-size:14.5px; }
  .list-row .m { font-size:11.5px; color:var(--muted); margin-top:3px; font-family:ui-monospace,monospace; }
  .list-row .rm { margin-left:auto; flex:none; }
  .list-empty { padding:26px; text-align:center; color:var(--muted); font-size:13.5px;
    border:1px dashed var(--line); border-radius:14px; }
  @media (max-width:640px) { .lists-hero { padding:26px 20px 22px; } }`;
  if (!document.getElementById('lists-room-css')) {
    const st = el('style', '', CSS); st.id = 'lists-room-css'; document.head.appendChild(st);
  }

  function readList(key) {
    try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch { return []; }
  }

  function ListCard(listKey, title, sub, emptyHint) {
    const card = Board({ accent: ACC, icon: 'lists', title, sub, lift: false });
    const ids = readList(listKey);
    const items = ids.map(byId).filter(Boolean);
    if (!items.length) {
      card.body.innerHTML = `<div class="list-empty">${emptyHint}<br><br>
        <button class="btn btn-ghost" data-go="feed"><span>Find something in the Feed</span></button></div>`;
      card.body.querySelector('[data-go="feed"]').addEventListener('click',
        () => window.NayaRouter.navigate('/hub/feed'));
      return card;
    }
    card.body.innerHTML = '';
    items.forEach(o => {
      const km = KIND_META[o.kind];
      const row = el('div', 'list-row');
      row.setAttribute('role', 'button'); row.setAttribute('tabindex', '0');
      row.innerHTML = `
        <span style="width:10px;height:10px;border-radius:50%;background:${km.accent};box-shadow:0 0 8px ${km.accent};flex:none"></span>
        <div><div class="t">${o.title}</div><div class="m">${o.id} · ${km.label} · reference — not a copy</div></div>
        <button class="btn btn-ghost rm" aria-label="Remove from list"><span>Remove</span></button>`;
      const open = () => C.openEvidence(o);
      row.addEventListener('click', e => { if (!e.target.closest('.rm')) open(); });
      row.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
      row.querySelector('.rm').addEventListener('click', e => {
        e.stopPropagation();
        const next = readList(listKey).filter(id => id !== o.id);
        localStorage.setItem(listKey, JSON.stringify(next));
        row.remove();
        if (!next.length) { card.body.innerHTML = `<div class="list-empty">${emptyHint}</div>`; }
      });
      card.body.appendChild(row);
    });
    return card;
  }

  function ListsRoom() {
    const wrap = el('div');
    const hero = el('section', 'lists-hero');
    hero.innerHTML = `
      <div class="kicker" style="position:relative">LISTS</div>
      <h1 class="lists-title">Every list is<br>a set of pointers.</h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        Lists categorize references to canonical intelligence. Add to a list anywhere —
        it lands here as a pointer. Delete the list and the intelligence survives.</p>
      ${C.fixtureBanner('Smart Lists')}`;
    wrap.appendChild(hero);

    const grid = el('div', 'today-act-grid');
    grid.appendChild(ListCard('naya.list.inbox', 'Inbox', 'Your working list — triage here',
      'Your inbox is empty. Use \u201CAdd to list\u201D on any card in the Feed or Today.'));
    grid.appendChild(ListCard('naya.favorites', 'Favorites', 'Kept close — still just pointers',
      'No favorites yet. Save what matters from any room.'));
    wrap.appendChild(grid);

    const note = Board({ accent: ACC, icon: 'nodes', title: 'On this device — for now', sub: 'Honest sync state', lift: false });
    note.body.innerHTML = `<p style="color:var(--muted);font-size:13.5px;max-width:640px">
      Lists live on this device until the governed runtime connects, then they sync as your categorized
      references — the objects stay canonical, your lists stay yours. No list ever duplicates an object.</p>`;
    wrap.appendChild(note);
    return wrap;
  }

  ListsRoom.ownsHead = true;
  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.lists = ListsRoom;
})();
