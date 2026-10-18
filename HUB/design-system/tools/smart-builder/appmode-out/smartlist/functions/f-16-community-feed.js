/* NayaFunction: f-16-community-feed v1.0.0
   What: Post composer -> rendered feed -> like + reply, persisted in localStorage
   Activation: <div data-fn="f-16-community-feed" data-fn-config='{...}'></div>
   Config: {
     title: feed heading (default "Community")
     subtitle: line under the heading
     composerPlaceholder: textarea placeholder (default "Share something with the community...")
     namePlaceholder: name field placeholder (default "Your name")
     postLabel: publish button label (default "Post")
     seedPosts: [{ author*, text*, time:"2h ago" }] — shown only when the store is empty
     storageKey: localStorage key for posts+likes (default "naya-fn-community-feed")
     accent: unit accent token (default #3fb8ff)
     allowLikes: true/false (default true)
     allowReplies: true/false (default true)
     maxLength: max characters per post (default 600)
   }
   Ready behavior: compose posts, like/unlike, reply inline; everything persists
     locally across reloads. Fully client-side, zero backend.
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

var F16_CSS = [
'.f16-wrap{max-width:620px;margin:0 auto;padding:22px 18px 30px;color:#fff}',
'.f16-title{color:#fff;font-size:26px;margin:0 0 6px}',
'.f16-sub{color:#c9c9d4;font-size:15px;margin:0 0 16px}',
'.f16-composer{background:rgba(255,255,255,.03);border:1.5px solid #fff;border-radius:16px;padding:15px;margin-bottom:18px}',
'.f16-name{width:100%;box-sizing:border-box;background:#050507;border:1px solid rgba(255,255,255,.25);color:#fff;border-radius:10px;padding:9px 12px;font-size:14px;margin-bottom:10px}',
'.f16-text{width:100%;box-sizing:border-box;background:#050507;border:1px solid rgba(255,255,255,.25);color:#fff;border-radius:10px;padding:10px 12px;font-size:14.5px;min-height:74px;resize:vertical;font-family:inherit}',
'.f16-name:focus,.f16-text:focus{outline:none;border-color:var(--ac)}',
'.f16-crow{display:flex;justify-content:space-between;align-items:center;margin-top:10px}',
'.f16-count{color:#8a8a99;font-size:12px}',
'.f16-btn{background:transparent;border:1.5px solid #fff;color:#fff;border-radius:999px;padding:9px 22px;font-size:14px;font-weight:650;cursor:pointer;transition:all .16s ease}',
'.f16-btn:hover{border-color:var(--ac);box-shadow:0 0 14px rgba(255,255,255,.10);transform:translateY(-1px)}',
'.f16-btn.off{opacity:.35;cursor:not-allowed;transform:none;box-shadow:none}',
'.f16-post{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.16);border-radius:16px;padding:14px 15px;margin-bottom:12px}',
'.f16-phead{display:flex;align-items:center;gap:10px;margin-bottom:8px}',
'.f16-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--ac),#1a1a24);display:flex;align-items:center;justify-content:center;font-weight:750;font-size:15px;color:#fff;flex:0 0 auto}',
'.f16-who{flex:1 1 auto;min-width:0}',
'.f16-author{color:#fff;font-size:14px;font-weight:650;margin:0}',
'.f16-time{color:#8a8a99;font-size:12px;margin:0}',
'.f16-body{color:#fff;font-size:14.5px;line-height:1.55;margin:0 0 10px;white-space:pre-wrap;word-wrap:break-word}',
'.f16-actions{display:flex;gap:8px}',
'.f16-act{background:transparent;border:1px solid rgba(255,255,255,.35);color:#fff;border-radius:999px;padding:5px 14px;font-size:13px;cursor:pointer;transition:all .15s ease;display:inline-flex;align-items:center;gap:6px}',
'.f16-act:hover{border-color:var(--ac)}',
'.f16-act.liked{border-color:var(--ac);box-shadow:0 0 10px rgba(255,255,255,.10)}',
'.f16-replies{margin:10px 0 0;padding-left:14px;border-left:2px solid rgba(255,255,255,.18)}',
'.f16-reply{margin:8px 0}',
'.f16-reply .f16-body{font-size:13.5px;margin-bottom:4px}',
'.f16-replybox{display:flex;gap:8px;margin-top:10px}',
'.f16-replybox input{flex:1 1 auto;background:#050507;border:1px solid rgba(255,255,255,.25);color:#fff;border-radius:10px;padding:8px 12px;font-size:13.5px}',
'.f16-replybox input:focus{outline:none;border-color:var(--ac)}',
'.f16-empty{color:#8a8a99;font-size:14px;padding:10px 0}'
].join('\n');

function f16esc(v){
  return String(v == null ? '' : v)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;").replace(/'/g,"&#039;");
}

function f16uid(){
  return 'p' + Date.now().toString(36) + Math.floor(Math.random()*1e6).toString(36);
}

NF.register('f-16-community-feed', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (root.dataset.fnBound){ return { destroy: function(){} }; }
    root.dataset.fnBound = '1';

    var title = config.title || 'Community';
    var subtitle = config.subtitle || '';
    var composerPlaceholder = config.composerPlaceholder || 'Share something with the community...';
    var namePlaceholder = config.namePlaceholder || 'Your name';
    var postLabel = config.postLabel || 'Post';
    var storageKey = config.storageKey || 'naya-fn-community-feed';
    var accent = config.accent || '#3fb8ff';
    var allowLikes = config.allowLikes !== false;
    var allowReplies = config.allowReplies !== false;
    var maxLength = config.maxLength || 600;
    var seeds = Array.isArray(config.seedPosts) ? config.seedPosts : [];

    var styleEl = document.createElement('style');
    styleEl.setAttribute('data-f16','1');
    styleEl.textContent = F16_CSS;
    root.appendChild(styleEl);

    /* ---------- store: localStorage with in-memory fail-soft fallback ---------- */
    var mem = null;
    function load(){
      try {
        var raw = localStorage.getItem(storageKey);
        if (raw === null || raw === undefined) return null;
        var d = JSON.parse(raw);
        return Array.isArray(d) ? d : null;
      } catch(e){ return mem; }
    }
    function save(posts){
      try { localStorage.setItem(storageKey, JSON.stringify(posts)); }
      catch(e){ mem = posts; }
    }

    var posts = load();
    if (posts === null){
      posts = seeds.map(function(s, i){
        return {
          id: f16uid() + i,
          author: String(s.author || 'Member'),
          text: String(s.text || ''),
          time: String(s.time || ''),
          ts: Date.now() - (seeds.length - i) * 60000,
          likes: 0, liked: false,
          replies: []
        };
      });
      save(posts);
    }

    var replyOpen = {};

    function timeLabel(p){
      if (p.time) return p.time;
      var mins = Math.max(0, Math.round((Date.now() - (p.ts || Date.now())) / 60000));
      if (mins < 1) return 'just now';
      if (mins < 60) return mins + 'm ago';
      var h = Math.floor(mins / 60);
      if (h < 24) return h + 'h ago';
      return Math.floor(h / 24) + 'd ago';
    }

    function initial(name){
      name = String(name || '?').trim();
      return (name.charAt(0) || '?').toUpperCase();
    }

    function replyHtml(r){
      return '<div class="f16-reply"><div class="f16-phead">' +
        '<span class="f16-avatar" aria-hidden="true">' + f16esc(initial(r.author)) + '</span>' +
        '<span class="f16-who"><p class="f16-author">' + f16esc(r.author) + '</p>' +
        '<p class="f16-time">' + f16esc(timeLabel(r)) + '</p></span></div>' +
        '<p class="f16-body">' + f16esc(r.text) + '</p></div>';
    }

    function render(){
      var holder = document.createElement('div');
      renderListHtml(holder);
      var list = holder.innerHTML;

      root.insertAdjacentHTML('beforeend',
        '<div class="f16-wrap" data-f16-view="main" style="--ac:' + f16esc(accent) + '">' +
          '<h3 class="f16-title">' + f16esc(title) + '</h3>' +
          (subtitle ? '<p class="f16-sub">' + f16esc(subtitle) + '</p>' : '') +
          '<div class="f16-composer">' +
            '<input type="text" class="f16-name" placeholder="' + f16esc(namePlaceholder) + '" maxlength="60" aria-label="Your name">' +
            '<textarea class="f16-text" placeholder="' + f16esc(composerPlaceholder) + '" maxlength="' + maxLength + '" aria-label="Your post"></textarea>' +
            '<div class="f16-crow"><span class="f16-count" data-f16-cc>0 / ' + maxLength + '</span>' +
            '<button type="button" class="f16-btn f16-postbtn">' + f16esc(postLabel) + '</button></div>' +
          '</div>' +
          '<div data-f16-list>' + list + '</div>' +
        '</div>');
      prune();
    }

    function prune(){
      var vs = root.querySelectorAll('[data-f16-view]');
      for (var i=vs.length-1;i>0;i--) vs[i].remove();
    }

    /* re-render only the post list, keeping composer text intact */
    function renderInto(listEl){
      var holder = document.createElement('div');
      renderListHtml(holder);
      listEl.innerHTML = holder.innerHTML;
    }

    function renderListHtml(holder){
      var list = posts.length ? posts.map(function(p){
        var likeBtn = allowLikes
          ? '<button type="button" class="f16-act' + (p.liked ? ' liked' : '') + '" data-like="' + f16esc(p.id) + '" aria-pressed="' + (p.liked ? 'true' : 'false') + '">&#9825; ' + (p.likes || 0) + '</button>'
          : '';
        var replyBtn = allowReplies
          ? '<button type="button" class="f16-act" data-reply="' + f16esc(p.id) + '">Reply' + (p.replies && p.replies.length ? ' (' + p.replies.length + ')' : '') + '</button>'
          : '';
        var replyList = (allowReplies && p.replies && p.replies.length)
          ? '<div class="f16-replies">' + p.replies.map(replyHtml).join('') + '</div>' : '';
        var replyBox = (allowReplies && replyOpen[p.id])
          ? '<div class="f16-replybox"><input type="text" data-replyinput="' + f16esc(p.id) + '" placeholder="Write a reply..." maxlength="280" aria-label="Write a reply"><button type="button" class="f16-btn" data-send="' + f16esc(p.id) + '" style="padding:8px 16px;font-size:13px">Send</button></div>'
          : '';
        return '<article class="f16-post" data-post="' + f16esc(p.id) + '">' +
          '<div class="f16-phead"><span class="f16-avatar" aria-hidden="true">' + f16esc(initial(p.author)) + '</span>' +
          '<span class="f16-who"><p class="f16-author">' + f16esc(p.author) + '</p>' +
          '<p class="f16-time">' + f16esc(timeLabel(p)) + '</p></span></div>' +
          '<p class="f16-body">' + f16esc(p.text) + '</p>' +
          '<div class="f16-actions">' + likeBtn + replyBtn + '</div>' +
          replyList + replyBox +
        '</article>';
      }).join('') : '<p class="f16-empty">No posts yet — be the first to share.</p>';
      holder.innerHTML = list;
    }

    function findPost(id){
      for (var i=0;i<posts.length;i++) if (posts[i].id === id) return posts[i];
      return null;
    }

    function publish(){
      var nameEl = root.querySelector('.f16-name');
      var textEl = root.querySelector('.f16-text');
      if (!nameEl || !textEl) return;
      var text = textEl.value.trim();
      if (!text) {
        textEl.focus();
        textEl.style.borderColor = '#ff5e6c';
        setTimeout(function(){ textEl.style.borderColor = ''; }, 900);
        return;
      }
      posts.unshift({
        id: f16uid(),
        author: nameEl.value.trim() || 'Member',
        text: text.slice(0, maxLength),
        time: '',
        ts: Date.now(),
        likes: 0, liked: false,
        replies: []
      });
      save(posts);
      textEl.value = '';
      var cc = root.querySelector('[data-f16-cc]');
      if (cc) cc.textContent = '0 / ' + maxLength;
      renderInto(root.querySelector('[data-f16-list]'));
    }

    function onClick(e){
      var t = e.target.closest ? e.target.closest('button') : null;
      if (!t || !root.contains(t)) return;
      if (t.classList.contains('f16-postbtn')){ publish(); return; }
      var likeId = t.getAttribute('data-like');
      if (likeId){
        var p = findPost(likeId);
        if (p){
          p.liked = !p.liked;
          p.likes = Math.max(0, (p.likes || 0) + (p.liked ? 1 : -1));
          save(posts);
          renderInto(root.querySelector('[data-f16-list]'));
        }
        return;
      }
      var replyId = t.getAttribute('data-reply');
      if (replyId){
        replyOpen[replyId] = !replyOpen[replyId];
        renderInto(root.querySelector('[data-f16-list]'));
        if (replyOpen[replyId]){
          var inp = root.querySelector('[data-replyinput="' + replyId + '"]');
          if (inp) inp.focus();
        }
        return;
      }
      var sendId = t.getAttribute('data-send');
      if (sendId){
        var inp = root.querySelector('[data-replyinput="' + sendId + '"]');
        var p2 = findPost(sendId);
        if (inp && p2 && inp.value.trim()){
          p2.replies = p2.replies || [];
          p2.replies.push({ author: 'You', text: inp.value.trim().slice(0, 280), time: '', ts: Date.now() });
          save(posts);
          renderInto(root.querySelector('[data-f16-list]'));
        }
      }
    }

    function onInput(e){
      if (e.target && e.target.classList && e.target.classList.contains('f16-text')){
        var cc = root.querySelector('[data-f16-cc]');
        if (cc) cc.textContent = e.target.value.length + ' / ' + maxLength;
      }
    }

    function onKey(e){
      if (e.key === 'Enter' && e.target && e.target.getAttribute && e.target.getAttribute('data-replyinput')){
        e.preventDefault();
        var sendId = e.target.getAttribute('data-replyinput');
        var p = findPost(sendId);
        if (p && e.target.value.trim()){
          p.replies = p.replies || [];
          p.replies.push({ author: 'You', text: e.target.value.trim().slice(0, 280), time: '', ts: Date.now() });
          save(posts);
          renderInto(root.querySelector('[data-f16-list]'));
        }
      }
    }

    root.addEventListener('click', onClick);
    root.addEventListener('input', onInput);
    root.addEventListener('keydown', onKey);
    render();

    return { destroy: function(){
      root.removeEventListener('click', onClick);
      root.removeEventListener('input', onInput);
      root.removeEventListener('keydown', onKey);
    } };
  }
});
})();
