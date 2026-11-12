/* Smart Block: chat/sp-chat
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Adapted from renderChatTab (~line 1854) and the post composer in
 * renderPostsTab (~line 1659). App-state calls replaced by params:
 *   spaceChat()   -> messages array param
 *   personById()  -> {name, color} fields on each message
 *   toast()       -> callbacks / silent no-op
 *   addChatMsg()  -> onSend / onPost callbacks
 *   toggleRecording() -> onMic callback
 *   openSchedulePicker() -> onSchedule callback
 * avatar() replaced by a minimal inline-styled initial-letter circle
 * (the source's sp-ava class has no CSS in this block).
 */
(function(){
'use strict';

/* ============ helpers (from source ~line 724) ============ */
function el(tag, cls, text){
  var e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text !== undefined && text !== null) e.textContent = text;
  return e;
}
function fmtTime(ts){
  var d = new Date(ts), now = new Date();
  var diff = now - d;
  if(diff < 60000) return 'just now';
  if(diff < 3600000) return Math.floor(diff/60000) + 'm ago';
  if(diff < 86400000) return Math.floor(diff/3600000) + 'h ago';
  return d.toLocaleDateString(undefined, {month:'short', day:'numeric'});
}
/* Minimal initial-letter avatar (replaces source avatar(); sp-ava has no CSS here). */
function spAvatarCircle(name, color, size){
  var a = el('div', null, String(name || '?').trim().charAt(0).toUpperCase());
  var s = size || 30;
  a.style.cssText = 'width:' + s + 'px;height:' + s + 'px;border-radius:50%;flex:0 0 auto;' +
    'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:' +
    Math.round(s * 0.42) + 'px;color:#fff;background:' + (color || '#8b93a3') +
    ';font-family:inherit;';
  return a;
}

/* ---- one chat message: .sp-chat-msg ---- */
/* m = {name, color, text, ts, audioLabel?} */
function spChatMsg(m, opts){
  opts = opts || {};
  var b = el('div','sp-chat-msg');
  b.appendChild(spAvatarCircle(m.name, m.color, 30));
  var body = el('div','sp-chat-body');
  var head = el('div','sp-chat-head');
  head.appendChild(el('span','sp-chat-name', m.name || 'Someone'));
  head.appendChild(el('span','sp-chat-time', fmtTime(m.ts || Date.now())));
  body.appendChild(head);
  if(m.audioLabel && typeof window.spAudioMsg === 'function'){
    /* audio message: hand off to the sp-audio-msg block when present */
    body.appendChild(window.spAudioMsg({label: m.audioLabel, accent: opts.accent}));
    if(m.text) body.appendChild(el('div','sp-chat-text', m.text));
  } else if(m.audioLabel){
    body.appendChild(el('div','sp-chat-text','🎤 ' + m.audioLabel));
  } else {
    body.appendChild(el('div','sp-chat-text', m.text || ''));
  }
  b.appendChild(body);
  return b;
}

/* ---- message list: .sp-chat-list ---- */
/* messages = [{name, color, text, ts, audioLabel?}] */
/* opts = {accent:'#7c3aed'} — sets --sc on the list container */
function spChatList(messages, opts){
  opts = opts || {};
  var list = el('div','sp-chat-list');
  if(opts.accent) list.style.setProperty('--sc', opts.accent);
  if(!messages || !messages.length){
    list.appendChild(el('div','sp-empty','No messages yet. Start the conversation.'));
  }
  (messages || []).forEach(function(m){
    list.appendChild(spChatMsg(m, opts));
  });
  return list;
}
/* Append a message to an existing list element (keeps the specimen simple). */
function spChatAppend(list, m, opts){
  var empty = list.querySelector('.sp-empty');
  if(empty) list.removeChild(empty);
  list.appendChild(spChatMsg(m, opts || {}));
  list.scrollTop = list.scrollHeight;
}

/* ---- chat composer (text input + mic + send) ---- */
/* opts = {placeholder, accent, name, onSend(text), onMic(btn)} */
function spChatComposer(opts){
  opts = opts || {};
  var input = el('div','sp-chat-input');
  if(opts.accent) input.style.setProperty('--sc', opts.accent);
  var ti = el('input','sp-chat-ti');
  ti.type = 'text';
  ti.placeholder = opts.placeholder || ('Message ' + (opts.name || 'the space') + '…');
  var send = el('button','sp-chat-send','Send');
  function doSend(){
    var text = ti.value.trim();
    if(!text) return;
    if(typeof opts.onSend === 'function') opts.onSend(text);
    ti.value = '';
  }
  send.addEventListener('click', doSend);
  ti.addEventListener('keydown', function(e){ if(e.key === 'Enter') doSend(); });
  input.appendChild(ti);
  var micBtn = el('button','sp-mic-btn','🎤');
  micBtn.title = 'Voice message';
  micBtn.addEventListener('click', function(){
    if(typeof opts.onMic === 'function') opts.onMic(micBtn);
    /* no default recording behavior: wired by the consumer (e.g. toggleRecording) */
  });
  input.appendChild(micBtn);
  input.appendChild(send);
  return input;
}

/* ---- post composer (textarea + schedule + post) ---- */
/* opts = {placeholder, schedLabel?, onPost(text, sched), onSchedule(current, setFn)} */
function spPostComposer(opts){
  opts = opts || {};
  var comp = el('div','sp-composer');
  var ta = el('textarea','sp-composer-ta');
  ta.placeholder = opts.placeholder || 'Share something…';
  comp.appendChild(ta);
  var crow = el('div','sp-composer-row');
  var schedBtn = el('button','sp-sched-btn','🕐 Schedule');
  var sched = null;
  schedBtn.addEventListener('click', function(){
    if(typeof opts.onSchedule === 'function'){
      opts.onSchedule(sched, function(sel){
        sched = sel;
        schedBtn.textContent = '🕐 ' + sel.label;
        schedBtn.classList.add('set');
        postBtn.textContent = 'Schedule Post';
      });
    } else {
      /* standalone default: toggles a scheduled state */
      sched = sched ? null : {label: 'Scheduled'};
      schedBtn.textContent = sched ? '🕐 Scheduled' : '🕐 Schedule';
      schedBtn.classList.toggle('set', !!sched);
      postBtn.textContent = sched ? 'Schedule Post' : 'Post';
    }
  });
  crow.appendChild(schedBtn);
  var postBtn = el('button','sp-post-btn','Post');
  postBtn.addEventListener('click', function(){
    var text = ta.value.trim();
    if(!text) return;
    if(typeof opts.onPost === 'function') opts.onPost(text, sched);
    ta.value = '';
    sched = null;
    schedBtn.textContent = '🕐 Schedule';
    schedBtn.classList.remove('set');
    postBtn.textContent = 'Post';
  });
  crow.appendChild(postBtn);
  comp.appendChild(crow);
  return comp;
}

/* expose */
window.spChatList = spChatList;
window.spChatMsg = spChatMsg;
window.spChatAppend = spChatAppend;
window.spChatComposer = spChatComposer;
window.spPostComposer = spPostComposer;

/* Demo:
   var list = spChatList([
     {name:'Naya', color:'#7c3aed', text:'Welcome to the space 👋', ts: Date.now()-1000*60*42},
     {name:'Shawn', color:'#1e6fd9', text:'Looking sharp. Ship it.', ts: Date.now()-1000*60*5}
   ], {accent:'#7c3aed'});
   document.body.appendChild(list);
   document.body.appendChild(spChatComposer({
     placeholder:'Message Design Space…', accent:'#7c3aed',
     onSend: function(t){ spChatAppend(list, {name:'You', color:'#0d9e6f', text:t, ts:Date.now()}); }
   }));
   document.body.appendChild(spPostComposer({
     placeholder:'Share something with Design Space…',
     onPost: function(t, sched){ spChatAppend(list, {name:'You', color:'#0d9e6f', text:t + (sched ? ' (⏱ scheduled)' : ''), ts:Date.now()}); }
   }));
*/
})();
