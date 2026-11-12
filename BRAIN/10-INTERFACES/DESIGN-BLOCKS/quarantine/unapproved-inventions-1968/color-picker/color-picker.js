/* Smart Block: forms/color-picker — swatch select, custom hex validation, readout */
(function () {
  'use strict';

  var HEX_RE = /^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$/;

  function normalizeHex(raw) {
    var m = HEX_RE.exec((raw || '').trim());
    if (!m) return null;
    var h = m[1];
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    return '#' + h.toLowerCase();
  }

  function hexToRgb(hex) {
    return [
      parseInt(hex.slice(1, 3), 16),
      parseInt(hex.slice(3, 5), 16),
      parseInt(hex.slice(5, 7), 16)
    ].join(',');
  }

  function gemStops(hex) {
    // Lightened top-left hi and darkened lo for the radial gem gradient
    var r = parseInt(hex.slice(1, 3), 16),
        g = parseInt(hex.slice(3, 5), 16),
        b = parseInt(hex.slice(5, 7), 16);
    function px(n) { return Math.max(0, Math.min(255, n)); }
    function css(a, b2, c) { return 'rgb(' + px(a) + ',' + px(b2) + ',' + px(c) + ')'; }
    return {
      hi: css(px(r + (255 - r) * .45), px(g + (255 - g) * .45), px(b + (255 - b) * .45)),
      c: hex,
      lo: css(px(r * .3), px(g * .3), px(b * .3))
    };
  }

  function init(root) {
    var grid   = root.querySelector('.cp-grid');
    var input  = root.querySelector('.cp-hex-input');
    var nameEl = root.querySelector('.cp-name');
    var hexEl  = root.querySelector('.cp-hex');
    if (!grid || !input) return;

    function select(sw) {
      var prev = grid.querySelector('.cp-selected');
      if (prev) prev.classList.remove('cp-selected');
      sw.classList.add('cp-selected');
      if (nameEl) nameEl.textContent = sw.dataset.name || 'Custom';
      if (hexEl) hexEl.textContent = sw.dataset.hex || '';
      root.dispatchEvent(new CustomEvent('cp-change', {
        bubbles: true,
        detail: { name: sw.dataset.name || 'Custom', hex: sw.dataset.hex || '' }
      }));
    }

    grid.addEventListener('click', function (e) {
      var sw = e.target.closest('.cp-swatch');
      if (sw) select(sw);
    });

    input.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      var hex = normalizeHex(input.value);
      input.classList.remove('cp-invalid');
      if (!hex) {
        input.classList.add('cp-invalid');
        return;
      }
      // Custom swatch lives as the last grid cell
      var custom = grid.querySelector('[data-custom]');
      if (!custom) {
        custom = document.createElement('button');
        custom.type = 'button';
        custom.className = 'cp-swatch';
        custom.setAttribute('data-custom', '1');
        custom.setAttribute('aria-label', 'Custom color');
        grid.appendChild(custom);
      }
      var g = gemStops(hex);
      custom.style.setProperty('--cp-hi', g.hi);
      custom.style.setProperty('--cp-c', g.c);
      custom.style.setProperty('--cp-lo', g.lo);
      custom.style.setProperty('--cp-glow', 'rgba(' + hexToRgb(hex) + ',.6)');
      custom.dataset.name = 'Custom';
      custom.dataset.hex = hex;
      select(custom);
    });
    input.addEventListener('input', function () {
      input.classList.remove('cp-invalid');
    });

    // Pre-select marked swatch
    var pre = grid.querySelector('.cp-selected');
    if (pre) select(pre);
  }

  function boot() {
    var roots = document.querySelectorAll('[data-cp]');
    for (var i = 0; i < roots.length; i++) init(roots[i]);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
