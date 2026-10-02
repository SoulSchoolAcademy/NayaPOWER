/* SMART LEDGER — the proof chain.
   Every canonical object entered the substrate through a governed event.
   The Ledger is the chain of those entries: what happened, when, with what
   provenance — the accountability layer. Nothing here is a balance sheet. */

(function () {
  const { el, Board } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS } = C;
  const ACC = 'var(--accent-ledger)';

  const CSS = `
  .led-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#161206 0%,#0e0c08 60%,#08060d 100%);
    border:1px solid #f1d75a2e; box-shadow:0 30px 80px -20px #f1d75a2b, inset 0 1px 0 #ffffff14; }
  .led-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05; color:#fff; }
  .led-title em { font-style:normal; color:#f1d75a; }
  .chain { position:relative; margin-top:24px; padding-left:26px; }
  .chain::before { content:""; position:absolute; left:8px; top:8px; bottom:8px; width:2px;
    background:linear-gradient(#f1d75a88, #f1d75a22); }
  .link { position:relative; border-radius:16px; background:#12100a; border:1px solid var(--line);
    padding:18px 20px 18px 22px; margin-bottom:14px; }
  .link::before { content:""; position:absolute; left:-24px; top:24px; width:12px; height:12px; border-radius:50%;
    background:var(--lk-accent); box-shadow:0 0 12px var(--lk-accent); }
  .link .ev { font-size:11px; letter-spacing:.16em; font-weight:800; color:var(--lk-accent); }
  .link h4 { font-size:15.5px; margin:6px 0 4px; }
  .link .pr { font-size:12.5px; color:var(--muted); font-family:ui-monospace,monospace; }
  .link .ops { display:flex; gap:8px; margin-top:12px; }
  @media (max-width:640px) { .led-hero { padding:26px 20px 22px; } }`;
  if (!document.getElementById('led-room-css')) {
    const st = el('style', '', CSS); st.id = 'led-room-css'; document.head.appendChild(st);
  }

  function LedgerRoom() {
    const wrap = el('div');
    const hero = el('section', 'led-hero');
    hero.innerHTML = `
      <div class="kicker" style="position:relative">ACCOUNTABILITY</div>
      <h1 class="led-title">What happened,<br><em>provably.</em></h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        The Ledger chains every governed entry: object, event, provenance, truth state.
        Verify anything — the chain shows its work.</p>
      ${C.fixtureBanner('Smart Ledger')}`;
    wrap.appendChild(hero);

    const chain = el('div', 'chain');
    chain.setAttribute('aria-label', 'Proof chain');
    [...OBJECTS].sort((a, b) => new Date(a.ts) - new Date(b.ts)).forEach((o, i) => {
      const km = KIND_META[o.kind];
      const t = new Date(o.ts).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZone: 'America/Los_Angeles' });
      const link = el('div', 'link');
      link.style.setProperty('--lk-accent', km.accent);
      link.innerHTML = `
        <div class="ev">ENTRY ${String(i + 1).padStart(3, '0')} · ${o.kind.toUpperCase()} RECORDED</div>
        <h4>${o.title}</h4>
        <div class="pr">${o.id}<br>${t} PT · ${o.provenance.by}<br>truth: ${o.truth_state} · consent: ${o.consent}</div>
        <div class="ops"><button class="btn btn-ghost" data-ev><span>Verify object</span></button></div>`;
      link.querySelector('[data-ev]').addEventListener('click', () => C.openEvidence(o));
      chain.appendChild(link);
    });
    wrap.appendChild(chain);

    const note = Board({ accent: ACC, icon: 'ledger', title: 'Chain integrity', sub: 'What the Ledger guarantees', lift: false });
    note.body.innerHTML = `<p style="color:var(--muted);font-size:13.5px;max-width:640px">
      Each entry binds an object to its governed event: identity, timestamp, provenance, truth state, consent.
      Entries are append-only — corrections arrive as new entries that supersede, never as edits.
      When the runtime connects, this chain is anchored to real governed events.</p>`;
    wrap.appendChild(note);
    return wrap;
  }

  LedgerRoom.ownsHead = true;
  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.ledger = LedgerRoom;
})();
