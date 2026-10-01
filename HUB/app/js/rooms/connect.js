/* CONNECT — Smart Connect. One brain. Many doors.
   Every door shows what it is, who it's for, its honest status,
   and a real connect action — never a fake one. */

function ConnectRoom() {
  const { el, Icons, Board, DoorCard, toast } = window.NayaUI;
  const R = window.NayaRuntime;
  const wrap = el('div');

  const intro = Board({
    accent: 'var(--accent-connect)', icon: 'connect',
    title: 'One brain. Many doors.',
    sub: 'Humans, AIs, machines, developers, and organizations all reach the same governed intelligence — each through the door that fits. Connection never silently creates permission.',
    lift: false,
  });
  intro.body.innerHTML = `
    <p style="color:var(--muted);font-size:13px;max-width:640px">
      A door is a <b style="color:var(--ink)">channel</b>, not an architecture. Behind every door below sits
      NayaPOWER — the same memory, the same judgment, the same receipts.
      The server enforces identity, scope, and authorization for every authenticated door.
    </p>`;
  wrap.appendChild(intro);
  wrap.appendChild(el('div', '', '<hr class="hr">'));

  const grid = el('div', 'board-grid');
  const sorted = [...R.DOORS].sort((a, b) => ((a.priority ?? 99) - (b.priority ?? 99)));
  sorted.forEach(door => {
    grid.appendChild(DoorCard(door, d => {
      const res = R.connectDoor(d.id);
      toast(res.message, d.accent);
    }));
  });
  wrap.appendChild(grid);

  wrap.appendChild(el('div', '', '<hr class="hr">'));

  /* ——— Roadmap: future door ideas, NOT in the canonical registry ——— */
  const road = Board({
    accent: 'var(--accent-connect)', icon: 'clock',
    title: 'On the roadmap',
    sub: 'Future door ideas — not in the canonical registry yet',
    lift: false,
  });
  road.body.innerHTML = `
    <div style="display:grid;gap:10px">
      ${R.DOOR_ROADMAP.map(r => `
        <div style="display:flex;gap:12px;align-items:baseline;padding:11px 4px;border-bottom:1px solid var(--line-soft)">
          <span class="pill soon"><span class="dot"></span>IDEA</span>
          <div><b style="font-size:13.5px">${r.name}</b>
          <div style="color:var(--muted);font-size:12.5px;margin-top:2px">${r.desc}</div></div>
        </div>`).join('')}
    </div>
    <p style="color:var(--muted);font-size:12.5px;margin:14px 0 0">
      These are ideas with working agreements forming. The Hub will not pretend they are
      live — or even contracted — until the canonical door registry says so.
    </p>`;
  wrap.appendChild(road);

  wrap.appendChild(el('div', '', '<hr class="hr">'));

  const law = Board({
    accent: 'var(--accent-connect)', icon: 'shield',
    title: 'The Door Law',
    sub: 'What every door guarantees',
    lift: false,
  });
  law.body.innerHTML = `
    <ul style="margin:0;padding-left:18px;color:var(--ink-dim);font-size:13px;display:grid;gap:8px">
      <li>Doors expose what Naya <b style="color:var(--ink)">can</b> do. LAW decides what Naya <b style="color:var(--ink)">may</b> do. ACT does it. VERIFY checks what happened.</li>
      <li><b style="color:var(--ink)">CONNECTED ≠ AUTHORIZED.</b> Connection never silently creates permission.</li>
      <li>No agent connects directly to the underlying store — every door passes through governance.</li>
      <li>Every crossing leaves a receipt. Anonymous doors do not exist.</li>
      <li>A door that isn't live says so — on the door itself, not in fine print.</li>
    </ul>
    <p style="color:var(--muted);font-size:11.5px;letter-spacing:.06em;margin:14px 0 0">
      DOOR INVENTORY MIRRORS THE CANONICAL REGISTRY ·
      BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json
    </p>`;
  wrap.appendChild(law);

  return wrap;
}

window.NayaRooms = window.NayaRooms || {};
window.NayaRooms.connect = ConnectRoom;
