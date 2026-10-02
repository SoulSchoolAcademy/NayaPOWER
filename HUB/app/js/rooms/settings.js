/* SETTINGS — the Control Deck.
   Identity, privacy, authority, connections, notifications, data, security,
   appearance — plus System Health (diagnostics live here, never as a primary room).
   Governed settings are honest NOT_VERIFIED until the runtime connects. */

function SettingsRoom() {
  const { el, Board, Pill } = window.NayaUI;
  const R = window.NayaRuntime;
  const wrap = el('div');
  const ACC = 'var(--accent-settings)';

  /* ——— Governed settings (honest: pending runtime) ——— */
  const gov = Board({
    accent: ACC, icon: 'gear',
    title: 'Your intelligence, your rules',
    sub: 'Identity · Privacy · Authority · Connections · Notifications · Data · Security · Appearance',
    lift: false,
  });
  const c = R.NOT_VERIFIED_COPY;
  gov.body.innerHTML = `
    <p style="color:var(--muted);font-size:13.5px;max-width:640px;margin-bottom:14px">
      ${c.body}</p>
    <div style="display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))">
      ${['Identity', 'Privacy', 'Authority', 'Connections', 'Notifications', 'Data & Security', 'Appearance']
        .map(t => `<div style="padding:12px 14px;border:1px solid var(--line-soft);border-radius:12px;
          display:flex;justify-content:space-between;align-items:center;gap:10px">
          <span style="font-weight:700;font-size:13px">${t}</span>${Pill('not_verified')}</div>`).join('')}
    </div>`;
  wrap.appendChild(gov);
  wrap.appendChild(el('div', '', '<hr class="hr">'));

  /* ——— System Health (migrated from the former System room) ——— */
  const dims = [
    ['Visual Excellence', 8.3, 'Strong identity and concept; responsive polish, typography, icon maturity, and mobile shell defects remain.'],
    ['Functional Completeness', 4.8, 'Too many rooms are shells or honest NOT_VERIFIED presentations — not complete causal software yet.'],
    ['Intelligence', 4.2, 'Runtime hooks exist; rooms do not yet fulfill their intelligence promise end-to-end.'],
    ['Honesty', 8.3, 'Newer implementations refuse to fabricate data. Some stale terminology remains.'],
    ['Performance', 3.8, 'Production performance has not been independently demonstrated.'],
    ['Reliability & Continuity', 4.8, 'Local state, runtime gaps, and source/deployment uncertainty remain.'],
    ['Accessibility', 5.5, 'Some keyboard/reduced-motion thinking; complete proof does not exist yet.'],
    ['Craft & Finish', 5.8, 'Great ingredients; duplicate lanes, shell defects, and incomplete rooms still feel unfinished.'],
  ];
  const health = Board({
    accent: ACC, icon: 'core',
    title: 'System Health — the honest scorecard',
    sub: 'Last published independent audit · Naya 3 · 2026-10-01 · the useful score, not the flattering one',
    lift: false,
  });
  const rows = dims.map(([name, s, note]) => `
    <div style="display:grid;grid-template-columns:1fr auto;gap:4px 14px;padding:12px 0;border-bottom:1px solid var(--line-soft)">
      <div style="font-weight:800;font-size:15px">${name}</div>
      <div style="font-weight:800;font-size:16px;color:${s >= 9 ? 'var(--green)' : s >= 7 ? '#ffffff' : 'var(--orange)'}">${s.toFixed(1)}</div>
      <div style="grid-column:1/-1;color:var(--muted);font-size:13px">${note}</div>
      <div style="grid-column:1/-1;height:6px;border-radius:6px;background:#ffffff10;overflow:hidden">
        <div style="width:${s * 10}%;height:100%;border-radius:6px;background:linear-gradient(90deg,var(--purple),var(--magenta));box-shadow:0 0 10px #9d75ff66"></div>
      </div>
    </div>`).join('');
  const avg = (dims.reduce((a, d) => a + d[1], 0) / dims.length).toFixed(1);
  health.body.innerHTML = `
    <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:6px">
      <span style="font-size:44px;font-weight:800;background:linear-gradient(120deg,#ffffff,var(--purple));-webkit-background-clip:text;background-clip:text;color:transparent">${avg}</span>
      <span style="color:var(--muted);font-size:13px;letter-spacing:.14em">COMPOSITE · BAR IS 9.0</span>
    </div>${rows}
    <p style="color:var(--muted);font-size:12px;margin-top:12px">Scores move when the evidence moves — up or down. The builder's self-score never closes a gate; independent re-score required.</p>`;
  wrap.appendChild(health);
  wrap.appendChild(el('div', '', '<hr class="hr">'));

  /* ——— Roadmap ——— */
  const phases = [
    ['Phase 1 — Foundation', 'live', 'App shell, router, tokens, component system, honest states. This build.'],
    ['Phase 2 — Shell proven', 'soon', 'One navigation surface per viewport; the mobile drawer law; the full QA matrix green.'],
    ['Phase 3 — Today, complete', 'soon', 'Your Intelligence Today end-to-end as the reference masterpiece room.'],
    ['Phase 4 — Compound', 'soon', 'Rooms come alive one by one on the proven architecture; doors open against the governed runtime.'],
    ['Phase 5 — Polish to 10', 'soon', 'Motion audit, accessibility audit, performance budget — every dimension to 9.0+.'],
  ];
  const road = Board({ accent: ACC, icon: 'report', title: 'Roadmap', sub: 'Where this Hub is going', lift: false });
  road.body.innerHTML = phases.map(([t, s, d]) => `
    <div style="display:flex;gap:14px;align-items:flex-start;padding:11px 0;border-bottom:1px solid var(--line-soft)">
      <div style="padding-top:2px">${Pill(s)}</div>
      <div><div style="font-weight:800;font-size:13.5px">${t}</div>
      <div style="color:var(--muted);font-size:12px">${d}</div></div>
    </div>`).join('');
  wrap.appendChild(road);
  wrap.appendChild(el('div', '', '<hr class="hr">'));

  /* ——— Door registry mirror ——— */
  const reg = Board({ accent: ACC, icon: 'connect', title: 'Door registry', sub: 'The doors, as the runtime sees them', lift: false });
  reg.body.innerHTML = `
    <div style="display:grid;gap:8px">
      ${R.DOORS.map(d => `
        <div style="display:flex;align-items:center;gap:12px;padding:9px 4px;border-bottom:1px solid var(--line-soft)">
          <span style="width:10px;height:10px;border-radius:50%;background:${d.accent};box-shadow:0 0 10px ${d.accent};flex:none"></span>
          <span style="font-weight:700;font-size:13px;min-width:170px">${d.name}</span>
          <span style="flex:1">${Pill(d.status)}</span>
        </div>`).join('')}
    </div>
    <p style="color:var(--muted);font-size:12px;margin-top:10px">Source of truth: <b style="color:var(--ink)">${R.doorRegistryRef}</b> · runtime adapter <b style="color:var(--ink)">v${R.version}</b></p>`;
  wrap.appendChild(reg);

  return wrap;
}

window.NayaRooms = window.NayaRooms || {};
window.NayaRooms.settings = SettingsRoom;
