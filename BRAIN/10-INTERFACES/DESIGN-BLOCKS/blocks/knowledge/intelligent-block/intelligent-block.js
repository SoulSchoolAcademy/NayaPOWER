/* Smart Block JS: intelligent-block
 * Source: Naya Smart Hub Design.html
 *
 * PART A — intelBoard(note, idx, stream): the verbatim JS builder that renders
 * a full Intelligent Block (ib-blocktop, ib-nutshell, ib-layers, ib-foot).
 * Extracted byte-true; never rewritten.
 * External deps (provided by the Hub source, not shipped here):
 *   el(tag, cls, html), esc(x), md(text), BOARD_GLYPHS{}, layerJewel(name, color),
 *   layerColorFor(name), LAYER_ICONS{}, layerIconKind(name), window.NayaVoice (optional).
 *
 * PART B — specimen wiring: the layer toggle semantics from intelBoard(),
 * standalone for the specimen page.
 */

/* ================= PART A — verbatim builder ================= */

function intelBoard(note, idx, stream) {
    const b = el('article', 'intel-board tone-' + (note.tone || 'purple'));
    b.setAttribute('aria-label', 'Smart Note ' + (note.id || 'untitled'));
    b.dataset.intelligenceId = 'smart-note-' + String(note.id || idx).toLowerCase();

    /* — Block top: identity (jewel + title + meta) · truth badge — */
    const top = el('div', 'ib-blocktop');
    const identity = el('div', 'ib-identity');
    const jewel = el('span', 'ib-jewel');
    jewel.setAttribute('aria-hidden', 'true');
    const toneName = note.tone || 'purple';
    jewel.style.setProperty('--tone', 'var(--' + toneName + ')');
    /* Faceted SVG jewel — core/facet/shade/edge, not a flat glyph */
    const toneColor = getComputedStyle(document.documentElement).getPropertyValue('--' + toneName).trim() || '#9d75ff';
    const __glyph = BOARD_GLYPHS[note.icon] || '';
    jewel.innerHTML =
      '<svg class="v10-icon" viewBox="0 0 32 32" aria-hidden="true">' +
        '<polygon class="core" points="16,3 28,12 16,29 4,12"/>' +
        '<polygon class="facet" points="16,3 22,12 16,12"/>' +
        '<polygon class="facet" points="16,3 10,12 16,12" opacity=".3"/>' +
        '<polygon class="shade" points="16,29 28,12 16,12"/>' +
        '<polygon class="edge" points="16,3 28,12 16,29 4,12"/>' +
        (__glyph ? '<g transform="translate(11,11) scale(0.42)" fill="none" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">' + __glyph + '</g>' : '') +
      '</svg>';
    jewel.style.color = toneColor;
    const titleWrap = el('div', '');
    const title = el('h2', 'ib-title', esc(note.title || 'Untitled Intelligence'));
    const meta = el('div', 'ib-meta');
    /* Meta: category · topic · subtopic when available, else clean ID. Dynamic, not hardcoded. */
    const metaParts = [];
    if (note.category) metaParts.push(esc(note.category));
    if (note.topic) metaParts.push(esc(note.topic));
    if (note.subtopic) metaParts.push(esc(note.subtopic));
    if (!metaParts.length && note.id) metaParts.push('Note ' + esc(note.id));
    meta.innerHTML = metaParts.map(p => '<span>' + p + '</span>').join('<span class="meta-sep">·</span>');
    titleWrap.append(title, meta);
    if (note.subtitle) titleWrap.appendChild(el('div', 'ib-subtitle', esc(note.subtitle)));
    identity.append(jewel, titleWrap);
    top.append(identity);
    b.appendChild(top);

    /* — Nutshell: extracted from the "In A Nutshell" layer — */
    const nutshellLayer = (note.layers || []).find(L =>
      String(L.name || '').toUpperCase().includes('NUTSHELL'));
    if (nutshellLayer) {
      const ns = el('div', 'ib-nutshell');
      ns.innerHTML = '<b>IN A NUTSHELL</b>' + md(nutshellLayer.body.slice(0, 600));
      b.appendChild(ns);
    }

    /* — Layers (excluding nutshell — already shown above) — */
    const layers = el('div', 'ib-layers');
    (note.layers || []).forEach(L => {
      if (L === nutshellLayer) return;
      const layer = el('div', 'ib-layer layer-' + L.color + (L.tier === 'deeper' ? ' is-deeper' : ''));
      const lh = el('button', 'ib-layer-head');
      lh.setAttribute('aria-expanded', L.tier === 'primary' ? 'true' : 'false');
      lh.innerHTML =
        layerJewel(L.name, layerColorFor(L.name)) +
        '<b>' + esc(L.name) + '</b>' +
        '<button class="ib-layer-play" data-layer-name="' + esc(L.name) + '" aria-label="Hear Naya read ' + esc(L.name) + '" title="Play in Naya\'s voice"><span>\u25B6</span></button>';
      const lb = el('div', 'ib-layer-body');
      lb.innerHTML = md(L.body);
      if (L.tier !== 'primary') lb.hidden = true;
      else lh.classList.add('open');
      lh.addEventListener('click', (e) => {
        // If the play button was clicked, don't toggle the layer
        if (e.target.closest('.ib-layer-play')) {
          e.stopPropagation();
          const playBtn = e.target.closest('.ib-layer-play');
          const layerBody = lb.textContent || '';
          const layerName = L.name || '';
          const speakText = layerName + '. ' + layerBody.trim().substring(0, 2000);
          if (window.NayaVoice) {
            if (playBtn.classList.contains('playing')) {
              window.NayaVoice.stop();
              playBtn.classList.remove('playing');
              playBtn.querySelector('span').innerHTML = '\u25B6';
            } else {
              // Stop any other playing buttons
              document.querySelectorAll('.ib-layer-play.playing').forEach(b => {
                b.classList.remove('playing');
                b.querySelector('span').innerHTML = '\u25B6';
              });
              playBtn.classList.add('playing');
              playBtn.querySelector('span').innerHTML = '\u23F9';
              window.NayaVoice.play(speakText, {
                onEnd: () => {
                  playBtn.classList.remove('playing');
                  playBtn.querySelector('span').innerHTML = '\u25B6';
                }
              });
            }
          }
          return;
        }
        const open = lb.hidden;
        lb.hidden = !open;
        lh.classList.toggle('open', open);
        lh.setAttribute('aria-expanded', String(open));
      });
      layer.append(lh, lb);
      layers.appendChild(layer);
    });
    b.appendChild(layers);

    /* — Provenance foot — */
    const foot = el('div', 'ib-foot');
    foot.innerHTML = note.kind === 'official'
      ? '<span>Official NayaNET Guide \u00B7 from the Intelligent Library</span>'
      : '<span>Smart Note ' + esc(note.id || '') + ' \u00B7 from your Smart Feed</span>';
    b.appendChild(foot);

    /* — Social actions: top-right + bottom bar + add intel (direct, no queue) — */
    b.classList.add('board');
    const bid = 'note-' + String(note.id || note.title || 'smart-note').toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40);
    if (!b.dataset.actionsEnhanced) {
      b.dataset.actionsEnhanced = '1';
      const btop = b.querySelector('.ib-blocktop');
      try {
        if (window.BoardActions) {
          if (btop) btop.appendChild(window.BoardActions.topActions(bid, note.title));
          b.appendChild(window.BoardActions.bottomActions(bid, note.title, stream));
          b.appendChild(window.BoardActions.addIntel(bid));
        } else {
          /* Fallback: inline minimal actions if BoardActions missing */
          const fb = document.createElement('div');
          fb.className = 'board-bottom-actions';
          fb.innerHTML = '<span style="color:#888;font-size:12px">Actions loading…</span>';
          b.appendChild(fb);
        }
      } catch (e) {
        console.error('Board action error:', e.message);
      }
    }
    /* Microcopy trust signals (from deployed original) */
    const micro = el('div', 'ib-microcopy');
    micro.innerHTML = '<span class="left">ONE INTELLIGENCE &middot; MANY VIEWS &middot; ONE IDENTITY</span>' +
      '<span class="right">TRUST: SOURCE / INTERPRETATION SEPARATED</span>';
    b.appendChild(micro);

    return b;
  }

/* ================= PART B — specimen wiring ================= */

(function () {
  function el(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  document.querySelectorAll('.ib-layer-head').forEach(function (lh) {
    var lb = lh.parentElement.querySelector('.ib-layer-body');
    if (!lb) return;
    lh.addEventListener('click', function (e) {
      if (e.target.closest('.ib-layer-play')) {
        e.stopPropagation();
        var btn = e.target.closest('.ib-layer-play');
        btn.classList.toggle('playing');
        return;
      }
      var open = lb.hidden;
      lb.hidden = !open;
      lh.classList.toggle('open', open);
      lh.setAttribute('aria-expanded', String(open));
    });
  });
})();
