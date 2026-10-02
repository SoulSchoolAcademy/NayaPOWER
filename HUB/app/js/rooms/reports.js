/* YOUR REPORTS — the synthesis pipeline.
   Reports are periodic intelligence synthesis: the substrate distilled on a rhythm.
   A report never copies objects — it synthesizes them and cites them. */

(function () {
  const { el, Board } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS } = C;
  const ACC = 'var(--accent-reports)';

  const CSS = `
  .rep-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#0b0e1e 0%,#0a0c14 60%,#08060d 100%);
    border:1px solid #7b8cff2e; box-shadow:0 30px 80px -20px #7b8cff33, inset 0 1px 0 #ffffff14; }
  .rep-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05;
    background:linear-gradient(115deg,#fff 30%,#c9d4ff 70%,#7b8cff); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .rep-doc { border-radius:18px; background:#0c0f1a; border:1px solid var(--line); padding:30px 32px; margin-top:20px; }
  .rep-doc h3 { font-size:22px; margin:0 0 4px; }
  .rep-doc .per { font-size:12px; color:var(--muted); letter-spacing:.14em; margin-bottom:18px; }
  .rep-sec { margin:20px 0; }
  .rep-sec h4 { font-size:13px; letter-spacing:.16em; color:var(--indigo); margin-bottom:10px; }
  .rep-cite { display:inline-block; margin:4px 6px 4px 0; padding:6px 12px; border-radius:999px;
    border:1px solid var(--line-soft); font-size:12px; cursor:pointer; color:var(--ink); background:transparent; }
  .rep-cite:hover { border-color:var(--indigo); }
  .rep-cite .mono { font-family:ui-monospace,monospace; font-size:10.5px; color:var(--muted); }
  .rep-archive { display:grid; gap:10px; margin-top:14px; }
  .rep-arch-row { display:flex; gap:14px; align-items:center; padding:14px 18px; border-radius:14px;
    background:#0c0f1a; border:1px solid var(--line); }
  .rep-arch-row .t { font-weight:700; font-size:14.5px; }
  .rep-arch-row .m { font-size:12px; color:var(--muted); }
  @media (max-width:640px) { .rep-hero { padding:26px 20px 22px; } .rep-doc { padding:22px 20px; } }`;
  if (!document.getElementById('rep-room-css')) {
    const st = el('style', '', CSS); st.id = 'rep-room-css'; document.head.appendChild(st);
  }

  function ReportsRoom() {
    const wrap = el('div');
    const hero = el('section', 'rep-hero');
    hero.innerHTML = `
      <div class="kicker" style="position:relative">REPORTS</div>
      <h1 class="rep-title">Synthesis,<br>on a rhythm.</h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        Reports distill the substrate into periodic intelligence. Every claim cites its objects;
        every object keeps its identity. A report is a lens with a memory.</p>
      ${C.fixtureBanner('Your Reports')}`;
    wrap.appendChild(hero);

    /* The current synthesis — built FROM the objects, citing them */
    const doc = el('article', 'rep-doc');
    const byKind = {};
    OBJECTS.forEach(o => { (byKind[o.kind] = byKind[o.kind] || []).push(o); });
    const citeBtn = o => `<button class="rep-cite" data-ev="${o.id}">${o.title} <span class="mono">${o.id.slice(-3)}</span></button>`;
    doc.innerHTML = `
      <h3>Week 40 — Intelligence Synthesis</h3>
      <div class="per">SEPT 29 – OCT 5, 2026 · SYNTHESIZED FROM ${OBJECTS.length} CANONICAL OBJECTS · FIXTURE</div>
      <div class="rep-sec"><h4>DECISIONS LOCKED</h4>
        <p style="color:#c9d2e8;font-size:14.5px;line-height:1.65">Two architectural rulings now govern the Hub build: the output-only law and the eleven-room rail. Both destroy as much as they create — which is what makes them decisions rather than preferences.</p>
        ${(byKind.decision || []).map(citeBtn).join('')}</div>
      <div class="rep-sec"><h4>LEARNING BANKED</h4>
        <p style="color:#c9d2e8;font-size:14.5px;line-height:1.65">The build got more honest twice: once about scores, once about a real rendering defect. Both learnings arrived with their proof attached.</p>
        ${(byKind.learning || []).map(citeBtn).join('')}</div>
      <div class="rep-sec"><h4>DISCOVERIES SURFACED</h4>
        <p style="color:#c9d2e8;font-size:14.5px;line-height:1.65">The three-pipeline model and the retrieval-only Ask Naya reframe what the Hub is allowed to be.</p>
        ${(byKind.discovery || []).map(citeBtn).join('')}</div>
      <div class="rep-sec"><h4>OPEN CARRY</h4>
        <p style="color:#c9d2e8;font-size:14.5px;line-height:1.65">Three loops remain open — the re-score, the registry re-fetch, the collision re-scan. Carried in the open, they are proof the system knows what it hasn't proven.</p></div>`;
    doc.querySelectorAll('.rep-cite').forEach(b =>
      b.addEventListener('click', () => C.openEvidence(OBJECTS.find(o => o.id === b.dataset.ev))));
    wrap.appendChild(doc);

    /* Archive — honest fixtures of the rhythm */
    const arch = Board({ accent: ACC, icon: 'report', title: 'Archive', sub: 'The rhythm, kept', lift: false });
    arch.body.innerHTML = `<div class="rep-archive">
      ${[['Week 39 — Foundation Synthesis', 'SEPT 22–28 · 11 objects · fixture'],
         ['Week 38 — Substrate Synthesis', 'SEPT 15–21 · 8 objects · fixture'],
         ['September — Monthly Intelligence', 'SEPT 1–30 · 31 objects · fixture']]
        .map(([t, m]) => `<div class="rep-arch-row"><div><div class="t">${t}</div><div class="m">${m}</div></div>
          <span style="margin-left:auto;font-size:11px;color:var(--muted);letter-spacing:.1em">FIXTURE</span></div>`).join('')}
      </div>
      <p style="font-size:12px;color:var(--muted);margin-top:12px">When the runtime connects, the archive fills with real syntheses — same shape, verified objects.</p>`;
    wrap.appendChild(arch);
    return wrap;
  }

  ReportsRoom.ownsHead = true;
  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.reports = ReportsRoom;
})();
