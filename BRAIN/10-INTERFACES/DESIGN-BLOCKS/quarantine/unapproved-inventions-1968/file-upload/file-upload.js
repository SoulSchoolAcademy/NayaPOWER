/* Smart Block: forms/file-upload — drag/drop, input fallback, simulated progress, remove */
(function () {
  'use strict';

  var TYPE_MAP = [
    { t: 'img',   re: /\.(png|jpe?g|gif|webp|svg|avif|bmp)$/i, label: 'IMG' },
    { t: 'doc',   re: /\.(pdf|docx?|txt|md|rtf|pages)$/i,      label: 'DOC' },
    { t: 'audio', re: /\.(mp3|wav|ogg|m4a|flac)$/i,            label: 'AUD' },
    { t: 'video', re: /\.(mp4|webm|mov|mkv)$/i,               label: 'VID' },
    { t: 'zip',   re: /\.(zip|rar|7z|tar|gz)$/i,               label: 'ZIP' },
    { t: 'code',  re: /\.(js|ts|css|html|json|py|sh|yml|md)$/i,label: 'DEV' }
  ];

  function typeOf(name) {
    for (var i = 0; i < TYPE_MAP.length; i++) {
      if (TYPE_MAP[i].re.test(name)) return TYPE_MAP[i];
    }
    return { t: 'code', label: 'FILE' };
  }

  function fmtSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  }

  function init(root) {
    var zone  = root.querySelector('.fu-dropzone');
    var input = root.querySelector('.fu-dropzone input[type="file"]');
    var list  = root.querySelector('.fu-list');
    if (!zone || !list) return;

    function addFile(file) {
      var info = typeOf(file.name || '');
      var row = document.createElement('div');
      row.className = 'fu-row';
      row.innerHTML =
        '<div class="fu-type" data-type="' + info.t + '">' + info.label + '</div>' +
        '<div class="fu-meta">' +
          '<span class="fu-name"></span>' +
          '<span class="fu-size">' + fmtSize(file.size || 0) + '</span>' +
          '<div class="fu-bar"><div class="fu-fill"></div></div>' +
        '</div>' +
        '<div class="fu-status">✓</div>' +
        '<button type="button" class="fu-remove" aria-label="Remove file">×</button>';
      row.querySelector('.fu-name').textContent = file.name || 'untitled';
      list.appendChild(row);

      var remove = row.querySelector('.fu-remove');
      remove.addEventListener('click', function (e) {
        e.stopPropagation();
        row.remove();
      });

      // Simulated upload progress (demo only — wire to real upload here)
      var fill = row.querySelector('.fu-fill');
      var p = 0;
      var timer = setInterval(function () {
        if (!row.isConnected) { clearInterval(timer); return; }
        p = Math.min(100, p + 4 + Math.random() * 12);
        fill.style.width = p + '%';
        if (p >= 100) {
          clearInterval(timer);
          row.classList.add('fu-done');
        }
      }, 120);
    }

    function handleFiles(files) {
      for (var i = 0; i < files.length; i++) addFile(files[i]);
    }

    ['dragenter', 'dragover'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) {
        e.preventDefault();
        zone.classList.add('fu-dragover');
      });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) {
        e.preventDefault();
        zone.classList.remove('fu-dragover');
      });
    });
    zone.addEventListener('drop', function (e) {
      var dt = e.dataTransfer;
      if (dt && dt.files && dt.files.length) handleFiles(dt.files);
    });
    if (input) {
      input.addEventListener('change', function () {
        handleFiles(input.files);
        input.value = '';
      });
    }
  }

  function boot() {
    var roots = document.querySelectorAll('[data-fu]');
    for (var i = 0; i < roots.length; i++) init(roots[i]);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
