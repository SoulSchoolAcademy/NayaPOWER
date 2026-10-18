/* NayaFunction: f-22-share v1.0.0
   What: smart link — copy the page link + share-to-feed composer.
   Activation: <div data-fn="f-22-share" data-fn-config='{"url":"https://example.com/app","title":"My Naya app","text":"Look at this"}'></div>
   Config:
     url: the page link to share (default: location.href at activate time).
     title: label shown in the composer (default document.title).
     text: pre-filled composer text (default "").
     feedGlobal: window global name of the feed unit's store (default "NayaFeed").
     queueKey: localStorage key for queued shares when no feed store is present
       (default "naya.fn22.feed-queue.v1").
     accent: hex — button chrome color (default #2fe89e green).
   Ready behavior: "Copy smart link" copies url to clipboard (with execCommand fallback) and confirms.
     "Share to feed" writes {title,text,url,at} to the feed unit's store if window[feedGlobal].add
     exists; otherwise the share is queued in localStorage AND the link is copied — the
     confirmation always says honestly which path ran. No pretending a share landed.
   Connected behavior: none.
   Backend twin: feed unit store (window.NayaFeed.add).
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (NF._r[id]) return; NF._r[id] = def; };

function copyText(text, done){
  function legacy(){
    var ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    done(ok);
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function(){ done(true); }, function(){ legacy(); });
  } else { legacy(); }
}

NF.register('f-22-share', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    var url = config.url || window.location.href;
    var title = config.title || document.title || 'Shared from Naya';
    var queueKey = config.queueKey || 'naya.fn22.feed-queue.v1';
    var feedGlobal = config.feedGlobal || 'NayaFeed';
    var accent = config.accent || '#2fe89e';

    root.innerHTML = '';
    var wrap = document.createElement('div');

    var t = document.createElement('p');
    t.textContent = 'Share "' + title + '"';
    t.style.cssText = 'color:#ffffff;font-size:15px;font-weight:600;margin:0 0 12px;';
    wrap.appendChild(t);

    var linkRow = document.createElement('div');
    linkRow.style.cssText = 'display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;';
    var link = document.createElement('span');
    link.textContent = url;
    link.style.cssText = 'flex:1 1 200px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;' +
      'color:#F8F7FB;font-size:13px;padding:12px 14px;background:#0b0b10;border:1px solid rgba(255,255,255,.28);border-radius:10px;';
    var copyBtn = document.createElement('button');
    copyBtn.type = 'button'; copyBtn.textContent = 'Copy smart link';
    copyBtn.className = 'nf22-copy';
    linkRow.appendChild(link); linkRow.appendChild(copyBtn);
    wrap.appendChild(linkRow);

    var ta = document.createElement('textarea');
    ta.rows = 3; ta.placeholder = 'Say something about it...';
    ta.setAttribute('aria-label', 'Share message');
    ta.value = config.text || '';
    ta.style.cssText = 'width:100%;box-sizing:border-box;padding:12px 14px;font-size:15px;color:#ffffff;' +
      'background:#0b0b10;border:1.5px solid rgba(255,255,255,.55);border-radius:12px;outline:none;margin-bottom:10px;';
    wrap.appendChild(ta);

    var shareBtn = document.createElement('button');
    shareBtn.type = 'button'; shareBtn.textContent = 'Share to feed';
    shareBtn.className = 'nf22-share';
    wrap.appendChild(shareBtn);

    [copyBtn, shareBtn].forEach(function(b){
      b.style.cssText = 'padding:12px 24px;font-size:15px;font-weight:700;color:#ffffff;background:#0b0b10;' +
        'border:1.5px solid rgba(255,255,255,.55);border-radius:12px;cursor:pointer;transition:border-color .18s,box-shadow .18s;';
      b.addEventListener('mouseover', function(){ b.style.borderColor = accent; b.style.boxShadow = '0 0 18px -4px ' + accent; });
      b.addEventListener('mouseout', function(){ b.style.borderColor = 'rgba(255,255,255,.55)'; b.style.boxShadow = 'none'; });
    });

    var ok = document.createElement('p');
    ok.style.cssText = 'color:#F8F7FB;font-size:14px;margin:12px 0 0;min-height:20px;';
    wrap.appendChild(ok);

    copyBtn.addEventListener('click', function(){
      copyText(url, function(doneIt){
        ok.textContent = doneIt ? 'Smart link copied — share it anywhere.' : 'Copy did not work here — the link is shown above.';
      });
    });

    shareBtn.addEventListener('click', function(){
      var text = ta.value.trim();
      var post = { title: title, text: text, url: url, at: new Date().toISOString() };
      var store = window[feedGlobal];
      if (store && typeof store.add === 'function') {
        try {
          store.add(post);
          ok.textContent = 'Shared to the feed.';
          ta.value = '';
          return;
        } catch (e) {
          console.warn('[f-22-share] feed store threw — falling back to queue', e);
        }
      }
      // No feed unit present (or it failed): queue + clipboard, and SAY SO — no staged behavior.
      try {
        var q = JSON.parse(localStorage.getItem(queueKey) || '[]');
        if (!Array.isArray(q)) q = [];
        q.push(post);
        localStorage.setItem(queueKey, JSON.stringify(q));
      } catch (e) { console.warn('[f-22-share] queue write failed', e); }
      copyText(url, function(){
        ok.textContent = 'No feed connected — your share is queued (' + queueKey + ') and the link was copied.';
      });
      ta.value = '';
    });

    root.appendChild(wrap);
    return { destroy: function(){ root.innerHTML = ''; } };
  }
});
})();
