/* NayaFunction: f-15-portfolio-showcase v1.0.0
   What: Work gallery from config — filter by tag, lightbox view of each piece
   Activation: <div data-fn="f-15-portfolio-showcase" data-fn-config='{...}'></div>
   Config: {
     title: gallery heading (default "Selected work")
     subtitle: line under the heading
     items: [{ id*, title*, tags:["design","web"], image:"url", blurb:"...", url:"https://..." }] *at least one item
     allLabel: label for the "everything" filter chip (default "All")
     accent: unit accent token (default #40d3bb)
     viewLabel: button label inside the lightbox for opening the item's url (default "Open project")
   }
   Ready behavior: cards render from config; tag chips filter the grid; clicking a card
     opens a lightbox (inside the root) with the full blurb and a working link when url is set.
   Connected behavior: none
   Backend twin: none
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var F15_CSS = [
'.f15-wrap{max-width:900px;margin:0 auto;padding:22px 18px 30px;color:#fff}',
'.f15-title{color:#fff;font-size:26px;margin:0 0 6px}',
'.f15-sub{color:#c9c9d4;font-size:15px;margin:0 0 16px}',
'.f15-note{color:#8a8a99;font-size:13px;margin:0}',
'.f15-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}',
'.f15-chip{background:transparent;border:1.5px solid #fff;color:#fff;border-radius:999px;padding:7px 16px;font-size:13.5px;font-weight:600;cursor:pointer;transition:all .16s ease}',
'.f15-chip:hover{transform:translateY(-1px)}',
'.f15-chip.on{border-color:var(--ac);color:#fff;box-shadow:0 0 14px rgba(255,255,255,.12)}',
'.f15-grid{display:flex;flex-direction:column;gap:12px}',
'.f15-card{display:flex;gap:14px;align-items:center;text-align:left;background:rgba(255,255,255,.03);border:1.5px solid #fff;color:#fff;border-radius:16px;padding:14px;cursor:pointer;transition:all .18s ease;width:100%}',
'.f15-card:hover{border-color:var(--ac);box-shadow:0 0 18px rgba(255,255,255,.10);transform:translateY(-2px)}',
'.f15-thumb{flex:0 0 84px;width:84px;height:84px;border-radius:12px;background:linear-gradient(135deg,var(--ac),#1a1a24);display:flex;align-items:center;justify-content:center;overflow:hidden;color:#fff;font-size:30px;font-weight:750}',
'.f15-thumb img{width:100%;height:100%;object-fit:cover;display:block}',
'.f15-ct{flex:1 1 auto;min-width:0}',
'.f15-cname{color:#fff;font-size:16px;font-weight:650;margin:0 0 4px}',
'.f15-cblurb{color:#c9c9d4;font-size:13.5px;line-height:1.45;margin:0 0 6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}',
'.f15-tags{display:flex;flex-wrap:wrap;gap:6px}',
'.f15-tag{font-size:11.5px;color:#fff;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:2px 10px}',
'.f15-empty{color:#8a8a99;font-size:14px;padding:18px 0}',
'.f15-lb{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px;background:rgba(2,2,4,.78);backdrop-filter:blur(6px)}',
'.f15-lbcard{max-width:560px;width:100%;max-height:88vh;overflow:auto;background:#0b0b10;border:1.5px solid var(--ac);border-radius:20px;padding:26px 24px;color:#fff;position:relative;box-shadow:0 20px 80px rgba(0,0,0,.6)}',
'.f15-lbclose{position:absolute;top:12px;right:12px;background:transparent;border:1.5px solid #fff;color:#fff;width:34px;height:34px;border-radius:50%;font-size:16px;cursor:pointer;line-height:1}',
'.f15-lbclose:hover{border-color:var(--ac)}',
'.f15-lbimg{width:100%;border-radius:14px;margin-bottom:14px;display:block}',
'.f15-lbh{color:#fff;font-size:22px;margin:0 0 8px}',
'.f15-lbp{color:#c9c9d4;font-size:15px;line-height:1.6;margin:0 0 14px}',
'.f15-lburl{display:inline-block;border:1.5px solid #fff;color:#fff;border-radius:999px;padding:10px 24px;font-size:14.5px;font-weight:650;text-decoration:none;transition:all .16s ease}',
'.f15-lburl:hover{border-color:var(--ac);transform:translateY(-1px)}'
].join('\n');

function f15esc(v){
  return String(v == null ? '' : v)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;").replace(/'/g,"&#039;");
}

function f15okUrl(u){
  return typeof u === 'string' && /^https?:\/\/[^\/\s]+\.[^\/\s]+/i.test(u.trim());
}

NF.register('f-15-portfolio-showcase', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (root.dataset.fnBound){ return { destroy: function(){} }; }
    root.dataset.fnBound = '1';

    var items = Array.isArray(config.items) ? config.items : [];
    var title = config.title || 'Selected work';
    var subtitle = config.subtitle || '';
    var allLabel = config.allLabel || 'All';
    var viewLabel = config.viewLabel || 'Open project';
    var accent = config.accent || '#40d3bb';

    var styleEl = document.createElement('style');
    styleEl.setAttribute('data-f15','1');
    styleEl.textContent = F15_CSS;
    root.appendChild(styleEl);

    var state = { tag: null };

    function tags(){
      var seen = {}, out = [];
      items.forEach(function(it){
        (it.tags || []).forEach(function(t){
          t = String(t);
          if (!seen[t]){ seen[t] = 1; out.push(t); }
        });
      });
      return out.sort();
    }

    function thumbHtml(it){
      if (it.image){
        return '<span class="f15-thumb"><img src="' + f15esc(it.image) + '" alt="" loading="lazy" onerror="this.remove()"></span>';
      }
      var ch = (it.title || '?').trim().charAt(0).toUpperCase() || '?';
      return '<span class="f15-thumb" aria-hidden="true">' + f15esc(ch) + '</span>';
    }

    function render(){
      var ts = tags();
      var chips = '<button type="button" class="f15-chip' + (state.tag === null ? ' on' : '') + '" data-tag="">' + f15esc(allLabel) + '</button>' +
        ts.map(function(t){
          return '<button type="button" class="f15-chip' + (state.tag === t ? ' on' : '') + '" data-tag="' + f15esc(t) + '">' + f15esc(t) + '</button>';
        }).join('');

      var shown = items.filter(function(it){
        return state.tag === null || (it.tags || []).indexOf(state.tag) >= 0;
      });

      var cards = shown.length ? shown.map(function(it){
        var tagHtml = (it.tags || []).map(function(t){ return '<span class="f15-tag">' + f15esc(t) + '</span>'; }).join('');
        return '<button type="button" class="f15-card" data-iid="' + f15esc(it.id || it.title) + '">' +
          thumbHtml(it) +
          '<span class="f15-ct"><span class="f15-cname">' + f15esc(it.title || 'Untitled') + '</span>' +
          (it.blurb ? '<span class="f15-cblurb">' + f15esc(it.blurb) + '</span>' : '') +
          '<span class="f15-tags">' + tagHtml + '</span></span>' +
        '</button>';
      }).join('') : '<p class="f15-empty">No pieces under this tag yet.</p>';

      var body = items.length
        ? '<div class="f15-chips">' + chips + '</div><div class="f15-grid">' + cards + '</div>'
        : '<p class="f15-note">No portfolio items configured yet.</p>';

      var old = root.querySelector('[data-f15-view="main"]');
      if (old) old.remove();
      closeLightbox();
      root.insertAdjacentHTML('beforeend',
        '<div class="f15-wrap" data-f15-view="main" style="--ac:' + f15esc(accent) + '">' +
          '<h3 class="f15-title">' + f15esc(title) + '</h3>' +
          (subtitle ? '<p class="f15-sub">' + f15esc(subtitle) + '</p>' : '') +
          body +
        '</div>');
    }

    function findItem(key){
      for (var i=0;i<items.length;i++){
        if (String(items[i].id || items[i].title) === String(key)) return items[i];
      }
      return null;
    }

    function openLightbox(it){
      closeLightbox();
      var tagHtml = (it.tags || []).map(function(t){ return '<span class="f15-tag">' + f15esc(t) + '</span>'; }).join('');
      var linkHtml = f15okUrl(it.url)
        ? '<a class="f15-lburl" href="' + f15esc(it.url.trim()) + '" target="_blank" rel="noopener noreferrer">' + f15esc(viewLabel) + ' &rarr;</a>'
        : '';
      var lb = document.createElement('div');
      lb.className = 'f15-lb';
      lb.setAttribute('data-f15-view', 'lb');
      lb.style.setProperty('--ac', accent);
      lb.innerHTML =
        '<div class="f15-lbcard" role="dialog" aria-modal="true" aria-label="' + f15esc(it.title || 'Work') + '">' +
          '<button type="button" class="f15-lbclose" aria-label="Close">&times;</button>' +
          (it.image ? '<img class="f15-lbimg" src="' + f15esc(it.image) + '" alt="" onerror="this.remove()">' : '') +
          '<h3 class="f15-lbh">' + f15esc(it.title || 'Untitled') + '</h3>' +
          '<div class="f15-tags" style="margin-bottom:10px">' + tagHtml + '</div>' +
          (it.blurb ? '<p class="f15-lbp">' + f15esc(it.blurb) + '</p>' : '') +
          linkHtml +
        '</div>';
      root.appendChild(lb);
    }

    function closeLightbox(){
      var lb = root.querySelector('[data-f15-view="lb"]');
      if (lb) lb.remove();
    }

    function onClick(e){
      var t = e.target;
      if (t === root.querySelector('[data-f15-view="lb"]') || (t.closest && t.closest('.f15-lbclose'))){
        closeLightbox(); return;
      }
      var chip = t.closest ? t.closest('.f15-chip') : null;
      if (chip && root.contains(chip)){
        var tag = chip.getAttribute('data-tag');
        state.tag = tag === '' ? null : tag;
        render(); return;
      }
      var card = t.closest ? t.closest('.f15-card') : null;
      if (card && root.contains(card)){
        var it = findItem(card.getAttribute('data-iid'));
        if (it) openLightbox(it);
      }
    }

    root.addEventListener('click', onClick);
    render();

    return { destroy: function(){ root.removeEventListener('click', onClick); } };
  }
});
})();
