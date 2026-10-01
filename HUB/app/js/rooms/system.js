/* SYSTEM — the Hub knows itself.
   The project intelligence, baked into the product: live scorecard,
   roadmap phases, door registry, spec reference. */

function SystemRoom() {
  const { el, Icons, Board, Pill } = window.NayaUI;
  const R = window.NayaRuntime;
  const wrap = el('div');
  const ACC = 'var(--accent-system)';

  /* ——— Scorecard ——— */
  const dims = [
    ['Visual Excellence', 9.0, 'The concept baseline is the visual law; this app inherits it through tokens.'],
    ['Functional Completeness', 4.5, 'Shell, routing, Connect doors, and local capture are real. Runtime-backed rooms are honest about waiting.'],
    ['Intelligence', 3.0, 'The nine-node kernel took its first breath; the Hub↔kernel link is the next build.'],
    ['Honesty', 9.0, 'Every state truthful by construction — the runtime never invents data.'],
    ['Performance', 8.0, 'Zero build step, tiny payload, GPU-composited motion. Measured on device, not assumed.'],
    ['Reliability & Continuity', 7.0, 'Stateless views; drafts persist locally; canonical state waits on the governed runtime.'],
    ['Accessibility', 7.5, 'Keyboard paths, visible focus, reduced-motion support, semantic landmarks. Audit pending.'],
    ['Craft', 8.5, 'One icon family, one depth grammar, one spectrum — no cheap edges by design.'],
  ];
  const score = Board({
    accent: ACC, icon: 'core',
    title: 'The 10/10 scorecard — live',
    sub: 'Scored in the open, every phase. Nothing is done until it scores.',
    lift: false,
  });
  const rows = dims.map(([name, s, note]) => `
    <div style="display:grid;grid-template-columns:1fr auto;gap:4px 14px;padding:12px 0;border-bottom:1px solid var(--line-soft)">
      <div style="font-weight:800;font-size:15px">${name}</div>
      <div style="font-weight:800;font-size:15px;color:${s >= 9 ? 'var(--green)' : s >= 7 ? 'var(--gold)' : 'var(--orange)'}">${s.toFixed(1)}</div>
      <div style="grid-column:1/-1;color:var(--muted);font-size:14px">${note}</div>
      <div style="grid-column:1/-1;height:6px;border-radius:6px;background:#ffffff10;overflow:hidden">
        <div style="width:${s * 10}%;height:100%;border-radius:6px;background:linear-gradient(90deg,var(--gold),var(--orange));box-shadow:0 0 10px #e8c76666"></div>
      </div>
    </div>`).join('');
  const avg = (dims.reduce((a, d) => a + d[1], 0) / dims.length).toFixed(1);
  score.body.innerHTML = `
    <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:6px">
      <span style="font-size:44px;font-weight:800;background:linear-gradient(120deg,var(--gold),var(--orange));-webkit-background-clip:text;background-clip:text;color:transparent">${avg}</span>
      <span style="color:var(--muted);font-size:14px;letter-spacing:.14em">CURRENT COMPOSITE · BAR IS 9.0</span>
    </div>${rows}`;
  wrap.appendChild(score);
  wrap.appendChild(el('div', '', '<hr class="hr">'));

  /* ——— Roadmap ——— */
  const phases = [
    ['Phase 1 — Foundation', 'live', 'App shell, router, tokens, component system, honest states. This build.'],
    ['Phase 2 — Rooms come alive', 'soon', 'Each room earns its controls against the component system; no room ships a dead control.'],
    ['Phase 3 — Doors open', 'soon', 'Canonical door contracts go live against the governed runtime, in registry order.'],
    ['Phase 4 — Intelligence in', 'soon', 'Search, feed, and notes read the canonical substrate with provenance.'],
    ['Phase 5 — Polish to 10', 'soon', 'Motion audit, accessibility audit, performance budget — every dimension to 9.0+.'],
  ];
  const road = Board({ accent: ACC, icon: 'report', title: 'Roadmap', sub: 'Where this Hub is going', lift: false });
  road.body.innerHTML = phases.map(([t, s, d]) => `
    <div style="display:flex;gap:14px;align-items:flex-start;padding:11px 0;border-bottom:1px solid var(--line-soft)">
      <div style="padding-top:2px">${Pill(s)}</div>
      <div><div style="font-weight:800;font-size:15px">${t}</div>
      <div style="color:var(--muted);font-size:14px">${d}</div></div>
    </div>`).join('');
  wrap.appendChild(road);
  wrap.appendChild(el('div', '', '<hr class="hr">'));

  /* ——— Door registry mirror ——— */
  const reg = Board({ accent: ACC, icon: 'connect', title: 'Door registry', sub: 'The same ten doors, as the runtime sees them', lift: false });
  reg.body.innerHTML = `
    <div style="display:grid;gap:8px">
      ${R.DOORS.map(d => `
        <div style="display:flex;align-items:center;gap:12px;padding:9px 4px;border-bottom:1px solid var(--line-soft)">
          <span style="width:10px;height:10px;border-radius:50%;background:${d.accent};box-shadow:0 0 10px ${d.accent};flex:none"></span>
          <span style="font-weight:700;font-size:14px;min-width:170px">${d.name}</span>
          <span style="flex:1">${Pill(d.status)}</span>
        </div>`).join('')}
    </div>`;
  wrap.appendChild(reg);
  wrap.appendChild(el('div', '', '<hr class="hr">'));

  /* ——— Spec reference ——— */
  const spec = Board({ accent: ACC, icon: 'library', title: 'Build law', sub: 'The canonical spec this app is built against', lift: false });
  spec.body.innerHTML = `
    <p style="color:var(--muted);font-size:14px;margin-bottom:12px">
      <b style="color:var(--ink)">HUB/app/SPEC.md</b> — project intelligence V2: the eight dimensions,
      the phased plan, the door inventory, the visual law. Versioned in the repository, next to the code it governs.
    </p>
    <p style="color:var(--muted);font-size:14px">Runtime adapter <b style="color:var(--ink)">v${R.version}</b> · spec ref <b style="color:var(--ink)">${R.specRef}</b></p>`;
  wrap.appendChild(spec);

  return wrap;
}

window.NayaRooms = window.NayaRooms || {};
window.NayaRooms.system = SystemRoom;
