/* YOUR CONNECTIONS — the intelligence graph.
   Objects are nodes; recorded connections are edges. The graph is drawn from
   the objects' own connects fields — no invented relationships. */

(function () {
  const { el, Board } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS, byId } = C;
  const ACC = 'var(--accent-connections)';

  const CSS = `
  .con-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#170e06 0%,#0e0a07 60%,#08060d 100%);
    border:1px solid #ff9a5c2e; box-shadow:0 30px 80px -20px #ff9a5c33, inset 0 1px 0 #ffffff14; }
  .con-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05;
    background:linear-gradient(115deg,#fff 30%,#ffd9bd 70%,#ff9a5c); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .graph-wrap { border-radius:18px; background:#0d0a08; border:1px solid var(--line); margin-top:20px;
    padding:10px; overflow:hidden; }
  .graph-wrap svg { display:block; width:100%; height:auto; }
  .g-node { cursor:pointer; }
  .g-node circle.halo { fill:none; stroke-width:1.5; opacity:.5; }
  .g-node:hover circle.halo, .g-node:focus circle.halo { opacity:1; stroke-width:2.5; }
  .g-edge { stroke:#ffffff22; stroke-width:1.2; }
  .g-label { fill:#cfc8de; font-size:10px; font-weight:600; }
  @media (max-width:640px) { .con-hero { padding:26px 20px 22px; } }`;
  if (!document.getElementById('con-room-css')) {
    const st = el('style', '', CSS); st.id = 'con-room-css'; document.head.appendChild(st);
  }

  /* Deterministic layout: ring positions from index — no fake physics */
  function layout(n, i, W, H) {
    const cx = W / 2, cy = H / 2, rx = W * 0.36, ry = H * 0.34;
    const a = (i / n) * Math.PI * 2 - Math.PI / 2;
    return [cx + rx * Math.cos(a), cy + ry * Math.sin(a)];
  }
  const cssColor = v => ({ magenta: '#d86cff', blue: '#55b9ee', green: '#55e39a', orange: '#ff9a5c', purple: '#9d75ff', indigo: '#7b8cff' }
    [v.replace('var(--', '').replace(')', '')] || '#fff');

  function ConnectionsRoom() {
    const wrap = el('div');
    const hero = el('section', 'con-hero');
    const edgeCount = OBJECTS.reduce((a, o) => a + (o.connects || []).length, 0);
    hero.innerHTML = `
      <div class="kicker" style="position:relative">CONNECTIONS</div>
      <h1 class="con-title">Drawn from the objects<br>themselves.</h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        ${OBJECTS.length} nodes · ${edgeCount} recorded edges. Every edge below comes from an object's own
        <i>connects</i> field — the graph invents nothing.</p>
      ${C.fixtureBanner('Your Connections')}`;
    wrap.appendChild(hero);

    const W = 720, H = 460;
    const pos = {};
    OBJECTS.forEach((o, i) => { pos[o.id] = layout(OBJECTS.length, i, W, H); });
    let edges = '', nodes = '';
    OBJECTS.forEach(o => {
      (o.connects || []).forEach(tid => {
        if (!pos[tid]) return;
        const [x1, y1] = pos[o.id], [x2, y2] = pos[tid];
        edges += `<line class="g-edge" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"/>`;
      });
    });
    OBJECTS.forEach((o, i) => {
      const [x, y] = pos[o.id];
      const col = cssColor(KIND_META[o.kind].accent);
      const short = o.title.length > 26 ? o.title.slice(0, 26) + '…' : o.title;
      nodes += `<g class="g-node" data-id="${o.id}" tabindex="0" role="button" aria-label="${o.title} — open evidence">
        <circle class="halo" cx="${x}" cy="${y}" r="20" stroke="${col}"/>
        <circle cx="${x}" cy="${y}" r="7" fill="${col}"/>
        <text class="g-label" x="${x}" y="${y + 34}" text-anchor="middle">${short.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text>
      </g>`;
    });
    const gw = el('div', 'graph-wrap');
    gw.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Intelligence graph: ${OBJECTS.length} nodes, ${edgeCount} edges">${edges}${nodes}</svg>`;
    gw.querySelectorAll('.g-node').forEach(g => {
      const open = () => C.openEvidence(byId(g.dataset.id));
      g.addEventListener('click', open);
      g.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
    });
    wrap.appendChild(gw);

    const leg = Board({ accent: ACC, icon: 'nodes', title: 'Reading the graph', sub: 'What edges mean', lift: false });
    leg.body.innerHTML = `<p style="color:var(--muted);font-size:13.5px;max-width:640px">
      An edge means one object recorded a connection to another — <i>what connects</i>, answered structurally.
      Select any node to open its evidence, including its full connection list. When the runtime connects,
      this graph grows from real recorded relationships — still never invented.</p>`;
    wrap.appendChild(leg);
    return wrap;
  }

  ConnectionsRoom.ownsHead = true;
  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.connections = ConnectionsRoom;
})();
