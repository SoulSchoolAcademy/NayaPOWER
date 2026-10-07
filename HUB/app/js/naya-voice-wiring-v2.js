/* NayaVoice wiring v2 — for the current Hub (HUB/app/index.html).
 * Targets the real content selectors: article.timeline-item (.intel-title +
 * .intel-summary), div.activity-card (.activity-card-title + .narrative),
 * and K.board elements. MutationObserver catches runtime-rendered content.
 * NayaVoice engine (naya-voice.js) is unchanged — speak/stop/setProvider,
 * honest SYNTHESIZED VOICE label, Tier 2 seam.
 */
(function () {
  'use strict';

  function qq(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function q(s, r) { return (r || document).querySelector(s); }
  function text(el) { return (el && el.innerText || '').trim(); }

  // One card = one speakable unit. Returns {el, title, body} or null.
  function unitFor(card) {
    var title = text(q('.intel-title', card)) || text(q('.activity-card-title', card)) || text(q('.board-title', card)) || text(q('h3', card));
    var body = text(q('.intel-summary', card)) || text(q('.activity-card-narrative', card)) || text(q('.board-body', card)) || text(q('p', card));
    if (!title && !body) return null;
    return { el: card, title: title, body: body };
  }

  // Where the button goes: prominent top-right overlay on the card itself.
  function headerFor(card) {
    return card; // overlay positioning handled by CSS (.nv-play is absolute)
  }

  var activeBtn = null;
  function resetActive() {
    if (activeBtn) { setBtn(activeBtn, 'idle'); activeBtn = null; }
  }
  function setBtn(btn, mode) {
    btn.dataset.nvMode = mode;
    var ic = btn.querySelector('.nv-ic');
    btn.classList.toggle('playing', mode === 'playing');
    if (mode === 'playing') { btn.setAttribute('aria-label', 'Pause Naya'); if (ic) ic.textContent = '❚❚'; }
    else if (mode === 'done') { btn.setAttribute('aria-label', 'Replay Naya'); if (ic) ic.textContent = '↻'; }
    else { btn.setAttribute('aria-label', 'Play Naya'); if (ic) ic.textContent = '▶'; }
  }

  function wireCard(card) {
    if (card.dataset.nvWired) return;
    var unit = unitFor(card);
    if (!unit) return;
    card.dataset.nvWired = '1';
    var header = headerFor(card);
    if (q('.nv-play', header)) return;

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'nv-play';
    btn.innerHTML = '<span class="nv-ic" aria-hidden="true">▶</span>' +
      '<span class="nv-name">Play Naya</span>' +
      '<span class="nv-tag">' + (window.NayaVoice ? window.NayaVoice.voiceLabel : 'SYNTHESIZED VOICE') + '</span>';
    setBtn(btn, 'idle');

    btn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (!window.NayaVoice) return;
      if (btn.dataset.nvMode === 'playing') { window.NayaVoice.pause(); setBtn(btn, 'idle'); return; }
      if (btn === activeBtn) { window.NayaVoice.resume(); setBtn(btn, 'playing'); return; }
      window.NayaVoice.stop();
      resetActive();
      activeBtn = btn;
      setBtn(btn, 'playing');
      var speech = (unit.title ? unit.title + '. ' : '') + unit.body;
      window.NayaVoice.speak(speech.slice(0, 8000), {
        onend: function () { setBtn(btn, 'done'); if (activeBtn === btn) activeBtn = null; },
        onerror: function () { setBtn(btn, 'done'); if (activeBtn === btn) activeBtn = null; }
      });
    });

    header.appendChild(btn);
  }

  function scan() {
    if (!window.NayaVoice) return;
    qq('article.timeline-item, div.activity-card').forEach(wireCard);
  }

  var tries = 0;
  var boot = setInterval(function () {
    if (window.NayaVoice || ++tries > 100) {
      clearInterval(boot);
      if (!window.NayaVoice) return;
      scan();
      window.NayaVoice.onState(function (s) { if (s === 'idle') resetActive(); });
      new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
    }
  }, 100);
})();
