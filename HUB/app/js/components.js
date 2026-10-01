/* ═══════════════════════════════════════════════════════════════════
   COMPONENTS — one jewel icon family (SVG, never emoji) + DOM builders.
   ═══════════════════════════════════════════════════════════════════ */

const Icons = (() => {
  const P = {
    feed:    '<path d="M4 6h16M4 12h16M4 18h10"/><circle cx="19" cy="18" r="2.2"/>',
    spark:   '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/>',
    note:    '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M9 12h6M9 16h6"/>',
    report:  '<path d="M5 20V10M12 20V4M19 20v-7"/>',
    library: '<path d="M4 5h7v14H4zM13 5h7v14h-7z"/><path d="M4 9h7M13 9h7"/>',
    connect: '<circle cx="7" cy="12" r="3"/><circle cx="17" cy="6" r="3"/><circle cx="17" cy="18" r="3"/><path d="M9.5 10.5l5-3M9.5 13.5l5 3"/>',
    ledger:  '<rect x="5" y="4" width="14" height="16" rx="2"/><path d="M9 9h6M9 13h6M9 17h4"/>',
    nodes:   '<circle cx="12" cy="5" r="2.4"/><circle cx="5" cy="18" r="2.4"/><circle cx="19" cy="18" r="2.4"/><path d="M12 7.5L6 16M12 7.5l6 8.5M7.4 18h9.2"/>',
    lists:   '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="5" cy="6" r="1.4"/><circle cx="5" cy="12" r="1.4"/><circle cx="5" cy="18" r="1.4"/>',
    mail:    '<rect x="4" y="6" width="16" height="12" rx="2"/><path d="M4 8l8 6 8-6"/>',
    spaces:  '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12L4 7.5M12 12v9"/>',
    gear:    '<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
    core:    '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor"/>',
    mcp:     '<path d="M8 3v18M16 3v18M3 8h5M3 16h5M16 8h5M16 16h5"/>',
    api:     '<path d="M8 9l-4 3 4 3M16 9l4 3-4 3M13 5l-2 14"/>',
    github:  '<path d="M12 3a9 9 0 00-2.8 17.5c.4.1.6-.2.6-.4v-1.5c-2.5.5-3-1-3-1-.4-1-1-1.3-1-1.3-.8-.6.1-.6.1-.6.9.1 1.4 1 1.4 1 .8 1.4 2.1 1 2.7.8.1-.7.3-1 .6-1.3-2-.2-4-1-4-4.4 0-1 .3-1.8.9-2.4-.1-.2-.4-1.1.1-2.4 0 0 .8-.2 2.5 1a8.6 8.6 0 014.6 0c1.7-1.2 2.5-1 2.5-1 .5 1.3.2 2.2.1 2.4.6.6.9 1.4.9 2.4 0 3.4-2 4.2-4 4.4.4.3.7.9.7 1.9v2.8c0 .2.2.5.6.4A9 9 0 0012 3z"/>',
    webhook: '<path d="M12 13l-4-4M12 13l4-4"/><path d="M4 17c2.5-5 5-7.5 8-7.5S17.5 12 20 17"/><circle cx="12" cy="4" r="1.6"/>',
    sdk:     '<path d="M6 3h12v18H6z"/><path d="M9 8l-2 4 2 4M15 8l2 4-2 4"/>',
    a2a:     '<circle cx="6" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8 8l8 8M18 6a2.6 2.6 0 01-5.2 0M6 18a2.6 2.6 0 015.2 0"/>',
    browser: '<rect x="4" y="5" width="16" height="14" rx="2.5"/><path d="M4 9.5h16"/><circle cx="7" cy="7.2" r=".9" fill="currentColor"/><circle cx="10" cy="7.2" r=".9" fill="currentColor"/>',
    shield:  '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9.5 12l2 2 3.5-4"/>',
    tunnel:  '<path d="M4 12h6M14 12h6"/><rect x="10" y="8" width="4" height="8" rx="2"/><path d="M6 6v12M18 6v12"/>',
    search:  '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>',
    plus:    '<path d="M12 5v14M5 12h14"/>',
    check:   '<path d="M4.5 12.5l5 5L19.5 7"/>',
    alert:   '<path d="M12 3l10 17H2z"/><path d="M12 10v4M12 17.5v.5"/>',
    lock:    '<rect x="5" y="10" width="14" height="10" rx="2.5"/><path d="M8 10V7a4 4 0 018 0v3"/>',
    arrow:   '<path d="M4 12h15M13 6l6 6-6 6"/>',
    clock:   '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/>',
    menu:    '<path d="M4 7h16M4 12h16M4 17h16"/>',
  };
  function icon(name, cls = '') {
    return `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[name] || P.core}</svg>`;
  }
  return { icon, names: Object.keys(P) };
})();

/* ——— DOM builders ——— */
function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html != null) e.innerHTML = html;
  return e;
}

function Board({ accent, icon, title, sub, lift = true }) {
  const b = el('section', 'board' + (lift ? ' lift' : ''));
  b.style.setProperty('--room-accent', accent);
  b.innerHTML = `
    <div class="board-head">
      <div class="board-icon">${Icons.icon(icon)}</div>
      <div><div class="board-title">${title}</div>${sub ? `<div class="board-sub">${sub}</div>` : ''}</div>
    </div>
    <div class="board-body"></div>`;
  b.body = b.querySelector('.board-body');
  return b;
}

function StatePanel({ accent, icon, title, body, actions = [] }) {
  const p = el('div', 'state-panel');
  p.style.setProperty('--room-accent', accent);
  p.innerHTML = `
    <div class="state-icon">${Icons.icon(icon)}</div>
    <h3>${title}</h3><p>${body}</p>
    <div class="state-actions"></div>`;
  const wrap = p.querySelector('.state-actions');
  actions.forEach(a => {
    const btn = el('button', 'btn' + (a.ghost ? ' btn-ghost' : ''));
    btn.style.setProperty('--btn-accent', accent);
    btn.innerHTML = `${a.icon ? Icons.icon(a.icon) : ''}<span>${a.label}</span>`;
    btn.addEventListener('click', a.onClick);
    wrap.appendChild(btn);
  });
  return p;
}

function DoorCard(door, onConnect) {
  const d = el('article', 'door');
  d.style.setProperty('--door-accent', door.accent);
  const statusLabel = { live: 'LIVE', ready: 'READY', soon: 'SOON', specialized: 'SPECIALIZED' }[door.status];
  d.innerHTML = `
    <div class="door-top">
      <div class="door-icon">${Icons.icon(door.icon)}</div>
      <div><div class="door-name">${door.name}</div><div class="door-for">${door.for}</div></div>
    </div>
    <div class="door-desc">${door.desc}</div>
    <div class="door-foot">
      <span class="pill ${door.status}"><span class="dot"></span>${statusLabel}</span>
    </div>`;
  const foot = d.querySelector('.door-foot');
  if (door.status === 'live') {
    const s = el('span', 'state-badge', 'IN USE');
    s.style.setProperty('--room-accent', door.accent);
    foot.appendChild(s);
  } else {
    const btn = el('button', 'btn btn-ghost');
    btn.style.setProperty('--btn-accent', door.accent);
    const label = door.status === 'ready' ? 'Connect' : door.status === 'soon' ? 'Roadmap' : 'Request access';
    btn.innerHTML = `${Icons.icon('arrow')}<span>${label}</span>`;
    btn.addEventListener('click', () => onConnect(door));
    foot.appendChild(btn);
  }
  return d;
}

function Pill(status) {
  const label = { live: 'LIVE', ready: 'READY', soon: 'SOON', specialized: 'SPECIALIZED' }[status] || status.toUpperCase();
  return `<span class="pill ${status}"><span class="dot"></span>${label}</span>`;
}

/* ——— Toast ——— */
function toast(message, accent = 'var(--magenta)', ms = 4200) {
  let stack = document.querySelector('.toast-stack');
  if (!stack) { stack = el('div', 'toast-stack'); document.body.appendChild(stack); }
  const t = el('div', 'toast', `<span>${message}</span>`);
  t.style.setProperty('--toast-accent', accent);
  stack.appendChild(t);
  setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 350); }, ms);
}

window.NayaUI = { Icons, el, Board, StatePanel, DoorCard, Pill, toast };
