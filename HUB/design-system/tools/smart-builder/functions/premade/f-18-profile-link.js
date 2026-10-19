/* NayaFunction: f-18-profile-link v1.0.0
   What: Link hub — avatar, bio, and link buttons from config; every button opens its URL
   Activation: <div data-fn="f-18-profile-link" data-fn-config='{...}'></div>
   Config: {
     name: display name (default "Me")
     handle: "@handle" line under the name
     avatar: image URL (falls back to an initial medallion) or "" for the medallion
     bio: one-to-two line bio
     links: [{ label*, url*, note }] *at least one link — each must be http(s) or mailto
     accent: unit accent token (default #e84fff)
     heading: small heading above the buttons (default "My world")
   }
   Ready behavior: renders the hub; every link is validated at activation — bad URLs
     render as visibly disabled "unavailable" buttons, never as dead links. Good links
     open in a new tab (same tab for mailto). Fully client-side.
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

var F18_CSS = [
'.f18-wrap{max-width:480px;margin:0 auto;padding:30px 20px 34px;color:#fff;text-align:center}',
'.f18-card{background:rgba(255,255,255,.03);border:1.5px solid #fff;border-radius:24px;padding:30px 24px;transition:border-color .2s ease}',
'.f18-card:hover{border-color:var(--ac)}',
'.f18-avatar{width:104px;height:104px;border-radius:50%;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:750;color:#fff;background:linear-gradient(135deg,var(--ac),#1a1a24);overflow:hidden;border:2px solid rgba(255,255,255,.4)}',
'.f18-avatar img{width:100%;height:100%;object-fit:cover;display:block}',
'.f18-name{color:#fff;font-size:24px;margin:0 0 4px}',
'.f18-handle{color:#8a8a99;font-size:14px;margin:0 0 10px}',
'.f18-bio{color:#c9c9d4;font-size:14.5px;line-height:1.6;margin:0 0 20px}',
'.f18-head{color:#fff;font-size:12px;letter-spacing:.18em;text-transform:uppercase;margin:0 0 12px;opacity:.85}',
'.f18-links{display:flex;flex-direction:column;gap:10px}',
'.f18-link{display:flex;align-items:center;gap:12px;background:transparent;border:1.5px solid #fff;color:#fff;border-radius:14px;padding:13px 16px;text-decoration:none;font-size:15px;font-weight:600;transition:all .18s ease;text-align:left}',
'.f18-link:hover{border-color:var(--ac);box-shadow:0 0 18px rgba(255,255,255,.10);transform:translateY(-2px)}',
'.f18-link .f18-dot{flex:0 0 auto;width:10px;height:10px;border-radius:50%;background:var(--ac);box-shadow:0 0 8px var(--ac)}',
'.f18-link .f18-lt{flex:1 1 auto;min-width:0}',
'.f18-link .f18-ll{color:#fff;display:block}',
'.f18-link .f18-ln{color:#8a8a99;font-size:12.5px;font-weight:400;display:block;margin-top:2px}',
'.f18-link .f18-go{color:#fff;font-size:18px;flex:0 0 auto}',
'.f18-link.dead{opacity:.38;cursor:not-allowed;transform:none;box-shadow:none}',
'.f18-link.dead:hover{border-color:#fff;box-shadow:none;transform:none}',
'.f18-none{color:#8a8a99;font-size:14px}'
].join('\n');

function f18esc(v){
  return String(v == null ? '' : v)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;").replace(/'/g,"&#039;");
}

/* Verification: only real, openable destinations become live buttons. */
function f18verify(u){
  if (typeof u !== 'string') return null;
  var s = u.trim();
  if (/^mailto:[^\s@]+@[^\s@]+\.[^\s@]+$/i.test(s)) return { href: s, kind: 'mailto' };
  if (/^https?:\/\/[^\s\/$.?#].[^\s]*$/i.test(s)){
    try {
      var host = s.split('/')[2] || '';
      if (host.indexOf('.') > 0) return { href: s, kind: 'web' };
    } catch(e){}
  }
  return null;
}

NF.register('profile-link', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (root.dataset.fnBound){ return { destroy: function(){} }; }
    root.dataset.fnBound = '1';

    var name = config.name || 'Me';
    var handle = config.handle || '';
    var avatar = config.avatar || '';
    var bio = config.bio || '';
    var links = Array.isArray(config.links) ? config.links : [];
    var accent = config.accent || '#e84fff';
    var heading = config.heading || 'My world';

    var styleEl = document.createElement('style');
    styleEl.setAttribute('data-f18','1');
    styleEl.textContent = F18_CSS;
    root.appendChild(styleEl);

    var avatarHtml = avatar
      ? '<div class="f18-avatar"><img src="' + f18esc(avatar) + '" alt="' + f18esc(name) + '" onerror="this.remove()"></div>'
      : '<div class="f18-avatar" aria-hidden="true">' + f18esc((name.trim().charAt(0) || '?').toUpperCase()) + '</div>';

    var linksHtml = links.length ? links.map(function(l){
      var v = f18verify(l.url);
      if (v){
        var extra = v.kind === 'web' ? ' target="_blank" rel="noopener noreferrer"' : '';
        return '<a class="f18-link" href="' + f18esc(v.href) + '"' + extra + '>' +
          '<span class="f18-dot" aria-hidden="true"></span>' +
          '<span class="f18-lt"><span class="f18-ll">' + f18esc(l.label || v.href) + '</span>' +
          (l.note ? '<span class="f18-ln">' + f18esc(l.note) + '</span>' : '') + '</span>' +
          '<span class="f18-go" aria-hidden="true">&rarr;</span></a>';
      }
      /* verified fail: visibly disabled, never a dead link */
      return '<span class="f18-link dead" aria-disabled="true" title="This link is unavailable">' +
        '<span class="f18-dot" aria-hidden="true"></span>' +
        '<span class="f18-lt"><span class="f18-ll">' + f18esc(l.label || 'Link') + '</span>' +
        '<span class="f18-ln">unavailable</span></span></span>';
    }).join('') : '<p class="f18-none">No links added yet.</p>';

    root.insertAdjacentHTML('beforeend',
      '<div class="f18-wrap" data-f18-view="main" style="--ac:' + f18esc(accent) + '">' +
        '<div class="f18-card">' +
          avatarHtml +
          '<h3 class="f18-name">' + f18esc(name) + '</h3>' +
          (handle ? '<p class="f18-handle">' + f18esc(handle) + '</p>' : '') +
          (bio ? '<p class="f18-bio">' + f18esc(bio) + '</p>' : '') +
          '<p class="f18-head">' + f18esc(heading) + '</p>' +
          '<div class="f18-links">' + linksHtml + '</div>' +
        '</div>' +
      '</div>');

    return { destroy: function(){} };
  }
});
})();
