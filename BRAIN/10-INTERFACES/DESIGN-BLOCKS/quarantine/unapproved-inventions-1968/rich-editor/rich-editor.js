/* Smart Block: forms/rich-editor — toolbar markdown insertion, tabs, md→HTML renderer */
(function () {
  'use strict';

  /* ---------- minimal markdown → HTML ---------- */
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function inline(md) {
    var out = esc(md);
    out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
    out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    out = out.replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    return out;
  }

  function render(md) {
    var lines = md.split('\n');
    var html = '';
    var inList = false;
    var inCode = false;
    var codeBuf = [];

    function closeList() {
      if (inList) { html += '</ul>'; inList = false; }
    }

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];

      // fenced code block
      if (/^```/.test(line)) {
        if (inCode) {
          html += '<pre><code>' + esc(codeBuf.join('\n')) + '</code></pre>';
          codeBuf = [];
          inCode = false;
        } else {
          closeList();
          inCode = true;
        }
        continue;
      }
      if (inCode) { codeBuf.push(line); continue; }

      var h = /^(#{1,3})\s+(.*)$/.exec(line);
      if (h) {
        closeList();
        var lvl = h[1].length;
        html += '<h' + lvl + '>' + inline(h[2]) + '</h' + lvl + '>';
        continue;
      }
      if (/^&gt;\s?/.test(line) || /^>\s?/.test(line)) {
        closeList();
        html += '<blockquote><p>' + inline(line.replace(/^>\s?/, '')) + '</p></blockquote>';
        continue;
      }
      var li = /^[-*]\s+(.*)$/.exec(line);
      if (li) {
        if (!inList) { html += '<ul>'; inList = true; }
        html += '<li>' + inline(li[1]) + '</li>';
        continue;
      }
      if (/^\s*$/.test(line)) { closeList(); continue; }
      closeList();
      html += '<p>' + inline(line) + '</p>';
    }
    closeList();
    if (inCode) html += '<pre><code>' + esc(codeBuf.join('\n')) + '</code></pre>';
    return html;
  }

  /* ---------- toolbar insertion ---------- */
  function insertLinePrefix(area, prefix) {
    var start = area.selectionStart, end = area.selectionEnd;
    var lineStart = area.value.lastIndexOf('\n', start - 1) + 1;
    var lineEnd = area.value.indexOf('\n', end);
    if (lineEnd === -1) lineEnd = area.value.length;
    var replaced = area.value.slice(lineStart, lineEnd)
      .split('\n')
      .map(function (l) { return (/^(\s*)$/.test(l) ? l : prefix + l); })
      .join('\n');
    area.value = area.value.slice(0, lineStart) + replaced + area.value.slice(lineEnd);
    area.focus();
    area.setSelectionRange(lineStart, lineStart + replaced.length);
    area.dispatchEvent(new Event('input', { bubbles: true }));
  }

  function surround(area, before, after, placeholder) {
    var start = area.selectionStart, end = area.selectionEnd;
    var sel = area.value.slice(start, end) || placeholder || '';
    area.value = area.value.slice(0, start) + before + sel + (after || '') + area.value.slice(end);
    area.focus();
    area.setSelectionRange(start + before.length, start + before.length + sel.length);
    area.dispatchEvent(new Event('input', { bubbles: true }));
  }

  var ACTIONS = {
    bold:   function (a) { surround(a, '**', '**', 'bold text'); },
    italic: function (a) { surround(a, '*', '*', 'italic text'); },
    h:      function (a) { insertLinePrefix(a, '## '); },
    quote:  function (a) { insertLinePrefix(a, '> '); },
    list:   function (a) { insertLinePrefix(a, '- '); },
    link:   function (a) { surround(a, '[', '](https://)', 'link text'); },
    code:   function (a) { surround(a, '`', '`', 'code'); }
  };

  /* ---------- init ---------- */
  function init(root) {
    var area    = root.querySelector('.re-area');
    var preview = root.querySelector('.re-preview');
    var body    = root.querySelector('.re-body');
    var tabs    = root.querySelectorAll('.re-tab');
    var btns    = root.querySelectorAll('.re-btn[data-act]');
    if (!area || !preview || !body) return;

    function refresh() {
      preview.innerHTML = render(area.value);
      root.dispatchEvent(new CustomEvent('re-change', { bubbles: true, detail: { value: area.value } }));
    }

    for (var i = 0; i < btns.length; i++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          var fn = ACTIONS[btn.dataset.act];
          if (fn) { fn(area); }
          btn.classList.add('re-on');
          setTimeout(function () { btn.classList.remove('re-on'); }, 400);
          refresh();
        });
      })(btns[i]);
    }

    for (var t = 0; t < tabs.length; t++) {
      (function (tab) {
        tab.addEventListener('click', function () {
          for (var k = 0; k < tabs.length; k++) tabs[k].classList.remove('re-active');
          tab.classList.add('re-active');
          var showPreview = tab.dataset.tab === 'preview';
          body.classList.toggle('re-show-preview', showPreview);
          if (showPreview) refresh();
          else area.focus();
        });
      })(tabs[t]);
    }

    area.addEventListener('input', refresh);
    refresh();
  }

  function boot() {
    var roots = document.querySelectorAll('[data-re]');
    for (var i = 0; i < roots.length; i++) init(roots[i]);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  // expose the renderer for embedding hosts
  window.ReBlock = { render: render };
})();
