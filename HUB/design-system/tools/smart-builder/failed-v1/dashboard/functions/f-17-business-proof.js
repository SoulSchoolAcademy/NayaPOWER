/* NayaFunction: f-17-business-proof v1.0.0
   What: Services list + testimonials + contact call-to-action — the page that sells
   Activation: <div data-fn="f-17-business-proof" data-fn-config='{...}'></div>
   Config: {
     businessName: heading (default "What I offer")
     tagline: line under the heading
     services: [{ name*, blurb, price }] *at least one service
     testimonials: [{ quote*, name*, role }]
     stats: [{ value*, label* }] — optional proof row (e.g. "120+ Happy clients")
     ctaLabel: contact button label (default "Get in touch")
     ctaEmail: "hello@..." — used as a mailto fallback
     ctaUrl: "https://..." — used when no email and no contact unit is present
     contactSelector: selector for the on-page contact unit to wire into (default "[data-nf-contact]")
     accent: unit accent token (default #2fe89e)
     note: small reassurance line under the CTA (default "Replies within one business day.")
   }
   Ready behavior: services render as lit rectangles; testimonials render; the CTA button
     scrolls to and focuses the on-page contact unit when contactSelector matches in the
     section container, otherwise falls back to mailto: (ctaEmail) or opening ctaUrl. Zero backend.
   Connected behavior: none
   Backend twin: f-21 (contact)
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var F17_CSS = [
'.f17-wrap{max-width:760px;margin:0 auto;padding:22px 18px 30px;color:#fff}',
'.f17-title{color:#fff;font-size:26px;margin:0 0 6px}',
'.f17-sub{color:#c9c9d4;font-size:15px;margin:0 0 18px}',
'.f17-sec{color:#fff;font-size:17px;margin:22px 0 10px;letter-spacing:.02em}',
'.f17-stats{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 6px}',
'.f17-stat{flex:1 1 140px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.16);border-radius:14px;padding:14px;text-align:center}',
'.f17-sval{color:#fff;font-size:26px;font-weight:750;margin:0 0 4px}',
'.f17-slabel{color:#8a8a99;font-size:12.5px;margin:0}',
'.f17-list{display:flex;flex-direction:column;gap:12px}',
'.f17-svc{display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.03);border:1.5px solid #fff;border-radius:16px;padding:16px;transition:all .18s ease}',
'.f17-svc:hover{border-color:var(--ac);box-shadow:0 0 18px rgba(255,255,255,.08);transform:translateY(-2px)}',
'.f17-dot{flex:0 0 auto;width:12px;height:12px;border-radius:50%;background:var(--ac);margin-top:6px;box-shadow:0 0 10px var(--ac)}',
'.f17-svct{flex:1 1 auto;min-width:0}',
'.f17-sname{color:#fff;font-size:16px;font-weight:650;margin:0 0 4px}',
'.f17-sblurb{color:#c9c9d4;font-size:13.5px;line-height:1.5;margin:0}',
'.f17-price{flex:0 0 auto;color:#fff;font-size:15px;font-weight:700;border:1px solid var(--ac);border-radius:999px;padding:6px 14px;white-space:nowrap}',
'.f17-tgrid{display:flex;flex-direction:column;gap:12px}',
'.f17-t{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.16);border-left:3px solid var(--ac);border-radius:14px;padding:15px 17px}',
'.f17-q{color:#fff;font-size:14.5px;line-height:1.6;font-style:italic;margin:0 0 8px}',
'.f17-who{color:#8a8a99;font-size:13px;margin:0}',
'.f17-who strong{color:#fff;font-weight:650}',
'.f17-cta{margin-top:24px;text-align:center;background:rgba(255,255,255,.03);border:1.5px solid #fff;border-radius:20px;padding:26px 20px;transition:all .2s ease}',
'.f17-cta:hover{border-color:var(--ac)}',
'.f17-ctah{color:#fff;font-size:21px;margin:0 0 6px}',
'.f17-ctas{color:#c9c9d4;font-size:14px;margin:0 0 16px}',
'.f17-btn{display:inline-block;background:transparent;border:1.5px solid #fff;color:#fff;border-radius:999px;padding:13px 38px;font-size:16px;font-weight:700;cursor:pointer;text-decoration:none;transition:all .18s ease}',
'.f17-btn:hover{border-color:var(--ac);box-shadow:0 0 22px rgba(255,255,255,.14);transform:translateY(-2px)}',
'.f17-note{color:#8a8a99;font-size:12.5px;margin:12px 0 0}',
'.f17-none{color:#8a8a99;font-size:14px}',
'[data-f17-flash]{outline:2px solid var(--ac,#2fe89e);outline-offset:4px;border-radius:8px;transition:outline-color 1.4s ease}'
].join('\n');

function f17esc(v){
  return String(v == null ? '' : v)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;").replace(/'/g,"&#039;");
}

NF.register('f-17-business-proof', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (root.dataset.fnBound){ return { destroy: function(){} }; }
    root.dataset.fnBound = '1';

    var businessName = config.businessName || 'What I offer';
    var tagline = config.tagline || '';
    var services = Array.isArray(config.services) ? config.services : [];
    var testimonials = Array.isArray(config.testimonials) ? config.testimonials : [];
    var stats = Array.isArray(config.stats) ? config.stats : [];
    var ctaLabel = config.ctaLabel || 'Get in touch';
    var ctaEmail = config.ctaEmail || '';
    var ctaUrl = config.ctaUrl || '';
    var contactSelector = config.contactSelector || '[data-nf-contact]';
    var accent = config.accent || '#2fe89e';
    var note = (config.note === undefined) ? 'Replies within one business day.' : config.note;

    var styleEl = document.createElement('style');
    styleEl.setAttribute('data-f17','1');
    styleEl.textContent = F17_CSS;
    root.appendChild(styleEl);

    var statHtml = stats.length ? '<div class="f17-stats">' + stats.map(function(s){
      return '<div class="f17-stat"><p class="f17-sval">' + f17esc(s.value) + '</p>' +
             '<p class="f17-slabel">' + f17esc(s.label) + '</p></div>';
    }).join('') + '</div>' : '';

    var svcHtml = services.length ? '<h4 class="f17-sec">Services</h4><div class="f17-list">' + services.map(function(s){
      return '<div class="f17-svc"><span class="f17-dot" aria-hidden="true"></span>' +
        '<div class="f17-svct"><p class="f17-sname">' + f17esc(s.name || 'Service') + '</p>' +
        (s.blurb ? '<p class="f17-sblurb">' + f17esc(s.blurb) + '</p>' : '') + '</div>' +
        (s.price ? '<span class="f17-price">' + f17esc(s.price) + '</span>' : '') +
      '</div>';
    }).join('') + '</div>' : '<p class="f17-none">Services are being added — check back soon.</p>';

    var tHtml = testimonials.length ? '<h4 class="f17-sec">What clients say</h4><div class="f17-tgrid">' + testimonials.map(function(t){
      return '<div class="f17-t"><p class="f17-q">&ldquo;' + f17esc(t.quote || '') + '&rdquo;</p>' +
        '<p class="f17-who"><strong>' + f17esc(t.name || 'Client') + '</strong>' +
        (t.role ? ' &middot; ' + f17esc(t.role) : '') + '</p></div>';
    }).join('') + '</div>' : '';

    /* CTA resolution, decided at activation so the button never lies (Law 13).
       The contact unit (f-21) is a sibling block on the built page, so the
       lookup is scoped to the section container — never document-wide. */
    function findContact(){
      var el = null;
      try {
        var scope = root.parentElement || root;
        el = scope.querySelector(contactSelector) || root.querySelector(contactSelector);
      } catch(e){ el = null; }
      return el;
    }
    var contactEl = findContact();

    var ctaHtml;
    if (contactEl){
      ctaHtml = '<button type="button" class="f17-btn f17-goto">' + f17esc(ctaLabel) + '</button>';
    } else if (ctaEmail && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(ctaEmail)){
      ctaHtml = '<a class="f17-btn" href="mailto:' + f17esc(ctaEmail) + '">' + f17esc(ctaLabel) + '</a>';
    } else if (ctaUrl && /^https?:\/\//i.test(ctaUrl)){
      ctaHtml = '<a class="f17-btn" href="' + f17esc(ctaUrl) + '" target="_blank" rel="noopener noreferrer">' + f17esc(ctaLabel) + '</a>';
    } else {
      ctaHtml = '<button type="button" class="f17-btn f17-dead" aria-disabled="true" disabled style="opacity:.4;cursor:not-allowed">' + f17esc(ctaLabel) + '</button>';
    }

    root.insertAdjacentHTML('beforeend',
      '<div class="f17-wrap" data-f17-view="main" style="--ac:' + f17esc(accent) + '">' +
        '<h3 class="f17-title">' + f17esc(businessName) + '</h3>' +
        (tagline ? '<p class="f17-sub">' + f17esc(tagline) + '</p>' : '') +
        statHtml + svcHtml + tHtml +
        '<div class="f17-cta"><h4 class="f17-ctah">Ready when you are</h4>' +
          '<p class="f17-ctas">Tell me what you need — I will take it from there.</p>' +
          ctaHtml +
          (note ? '<p class="f17-note">' + f17esc(note) + '</p>' : '') +
        '</div>' +
      '</div>');

    function onClick(e){
      var t = e.target.closest ? e.target.closest('.f17-goto') : null;
      if (!t || !root.contains(t)) return;
      var target = findContact();
      if (target){
        if (target.scrollIntoView) target.scrollIntoView({behavior:'smooth', block:'center'});
        var focusable = target.querySelector('input,textarea,select,button') || target;
        setTimeout(function(){ try { focusable.focus({preventScroll:true}); } catch(err2){} }, 450);
        target.setAttribute('data-f17-flash', '1');
        setTimeout(function(){ target.removeAttribute('data-f17-flash'); }, 1600);
      }
    }

    root.addEventListener('click', onClick);
    return { destroy: function(){ root.removeEventListener('click', onClick); } };
  }
});
})();
