/* NayaNET 509 AAA — REAL SMART FEED CONTENT RENDERER
 * Source-of-truth payload is generated at build time from the repository file:
 * SMART FEED CONTENT
 * This layer replaces the demonstration/mock feed blocks with the actual canonical
 * Smart Notes while preserving the existing C4 board architecture and interaction layer.
 */
(() => {
  'use strict';
  const PAYLOAD = '__SMART_FEED_B64__';
  if (!PAYLOAD || PAYLOAD === '__SMART_FEED_B64__') return;

  const esc = (v) => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const dec = () => { try { return decodeURIComponent(escape(atob(PAYLOAD))); } catch (_) { try { return atob(PAYLOAD); } catch (e) { return ''; } } };
  const source = dec();
  if (!source) return;

  const tones = ['#ffffff','#d86cff','#9d75ff','#55b9ee','#55e39a','#e8c766','#ff5e6c','#ff4fd8','#6675ff'];
  const glyphs = ['◈','✦','◇','◉','✧','◆','⬢','✺','✦'];

  function parseNotes(text) {
    return text.split(/={20,}/).map(x => x.trim()).filter(Boolean).map((raw, i) => {
      const lines = raw.split(/\r?\n/);
      const head = (lines.shift() || '').trim();
      if (!/SMART NOTE/i.test(head)) return null;
      const title = (lines.shift() || '').trim();
      const body = lines.join('\n').trim();
      const parts = body.split(/\n(?=\d+\.\s)/g);
      const sections = {};
      parts.forEach(part => {
        const m = part.match(/^(\d+)\.\s*([^\n]+)\n?([\s\S]*)$/);
        if (m) sections[Number(m[1])] = { name: m[2].trim(), text: m[3].trim() };
      });
      return { number: i + 1, title, sections };
    }).filter(Boolean);
  }

  function sectionBody(text) {
    return esc(text).replace(/\n/g, '<br>');
  }

  function actions() {
    return `<div class="actions" role="group" aria-label="Intelligence actions">
      <button class="action create" type="button" data-c4-kind="create-space">＋ CREATE SPACE</button>
      <button class="action favorite" type="button" data-c4-kind="favorite">★ FAVORITE</button>
      <button class="action save" type="button" data-c4-kind="save">SAVE</button>
      <button class="action love" type="button" data-c4-kind="love" aria-pressed="false">❤️ LOVE</button>
      <button class="action like" type="button" data-c4-kind="like" aria-pressed="false">LIKE</button>
      <span class="naya509-rating" data-c4-kind="rating" role="group" aria-label="Rate this intelligence">
        <span class="ratingLabel">RATE THIS INTELLIGENCE</span>
        <span class="ratingStars">${[1,2,3,4,5].map(n => `<button type="button" class="ratingStar" data-rating="${n}" aria-label="Rate ${n} out of 5">★</button>`).join('')}</span>
      </span>
      <button class="action share" type="button" data-c4-kind="share">＋ SHARE INTEL</button>
    </div>`;
  }

  function board(note, idx) {
    const tone = tones[idx % tones.length];
    const sections = Object.keys(note.sections).map(Number).sort((a,b) => a-b);
    const nutshell = note.sections[1];
    const layers = sections.filter(n => n !== 1).map(n => {
      const s = note.sections[n];
      const label = s.name.replace(/^IN A NUTSHELL$/i, 'NUTSHELL');
      return `<article class="layer" style="--layer:${tone}">
        <div class="layerHead"><span class="dot"></span><b>${esc(label)}</b><span class="state">SMART NOTE · ${String(note.number).padStart(2,'0')}</span></div>
        <div class="layerBody">${sectionBody(s.text)}</div>
      </article>`;
    }).join('');
    return `<article class="block naya509-board" data-real-smart-note="${idx + 1}" style="--tone:${tone}">
      <div class="blockInner">
        <div class="blockTop">
          <div class="identity"><div class="glyph">${glyphs[idx % glyphs.length]}</div><div><h3>${esc(note.title)}</h3><div class="meta"><span>SMART NOTE ${String(note.number).padStart(2,'0')}</span><span>CANONICAL INTELLIGENCE</span></div></div></div>
          <div class="truth">SOURCE CONTENT</div>
        </div>
        ${nutshell ? `<div class="nutshell"><b>IN A NUTSHELL</b><p>${sectionBody(nutshell.text)}</p></div>` : ''}
        <div class="layers">${layers}</div>
        ${actions()}
        <div class="blockFoot"><span>REAL SMART NOTE CONTENT · SOURCE: SMART FEED CONTENT</span><span>INTELLIGENCE EVENT ${String(note.number).padStart(2,'0')}</span></div>
      </div>
    </article>`;
  }

  function run() {
    const blocks = document.querySelector('.blocks');
    if (!blocks) return false;
    const notes = parseNotes(source);
    if (!notes.length) return false;
    const signature = notes.map(n => n.title).join('|');
    if (blocks.dataset.nayaRealSignature === signature && blocks.querySelectorAll('[data-real-smart-note]').length === notes.length) return true;
    blocks.innerHTML = notes.map(board).join('');
    blocks.dataset.nayaRealSignature = signature;
    document.documentElement.dataset.nayaRealSmartFeed = 'true';
    return true;
  }

  function style() {
    if (document.getElementById('naya509-real-content-style')) return;
    const s = document.createElement('style'); s.id = 'naya509-real-content-style';
    s.textContent = `
      .naya509-board{min-height:0!important;padding:34px 38px 42px 42px!important}
      .naya509-board .blockInner{max-width:1500px!important;margin:0 auto!important}
      .naya509-board .meta,.naya509-board .truth,.naya509-board .state{font-size:12px!important;line-height:1.35!important}
      .naya509-board .layerHead b{font-size:15px!important}
      .naya509-board .layerBody{font-size:18px!important;line-height:1.62!important;color:#e1dce5!important}
      .naya509-board .nutshell b{font-size:13px!important}
      .naya509-board .nutshell p{font-size:21px!important;line-height:1.58!important}
      .naya509-board .actions{align-items:center!important}
      .naya509-board .action{font-size:14px!important;min-height:50px!important;padding:0 16px!important}
      .naya509-board .ratingLabel{font-size:12px!important}
      .naya509-board .ratingStar{font-size:27px!important;width:42px!important;height:42px!important}
      @media(max-width:760px){.naya509-board{padding:26px 18px 34px 28px!important}.naya509-board .layerBody{font-size:17px!important}.naya509-board .nutshell p{font-size:19px!important}.naya509-board .action{font-size:13px!important}.naya509-board .ratingStar{width:38px!important;height:40px!important}}
    `;
    document.head.appendChild(s);
  }

  let scheduled = false;
  function schedule() { if (scheduled) return; scheduled = true; requestAnimationFrame(() => { scheduled = false; run(); }); }
  function boot() { style(); run(); const blocks = document.querySelector('.blocks'); if (blocks && !blocks.dataset.nayaRealObserver) { const mo = new MutationObserver(() => { if (blocks.dataset.nayaRealRendering === '1') return; schedule(); }); mo.observe(blocks,{childList:true}); blocks.dataset.nayaRealObserver='1'; } }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, {once:true}); else boot();
})();
