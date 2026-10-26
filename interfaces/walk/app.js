// THE OFFICIAL WELCOME — LIVE walk script.
// The 10 new question slides + end slide v2, with LIVE wiring:
// complete() POSTs /api/welcome/complete; boot verifies /api/welcome/me
// and shows the certificate door unless verified; end doors navigate to
// real URLs. Play audio slots stay EMPTY (glow only, never faked) until
// the audio round. Topics: [] — no picker (live-step decision; the
// payload keeps the topics key). State key naya_welcome_right_v1,
// shape {alias, answers, topics, reveal}.
(function(){
var PHOTOS = [
__PHOTOS__
];
var KEYS = [__KEYS__];
var SKEY = 'naya_welcome_right_v1';
function lsGet(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }
function lsSet(k, v){ try { localStorage.setItem(k, v); } catch(e){} }
/* ingest — the Hub's own mechanism, reused: ?name=&alias= into the Hub's keys */
(function ingest(){
  try {
    var qp = new URLSearchParams(location.search);
    var qn = (qp.get('name') || '').trim();
    var qa = (qp.get('alias') || '').trim().toLowerCase().replace(/[^a-z0-9-]/g, '');
    if (qa) lsSet('nayanet_smart_alias', qa);
    if (qn) lsSet('nayanet_smart_name', qn);
    if (qn || qa) { try { history.replaceState(null, '', location.pathname + location.hash); } catch(e){} }
  } catch(e){}
})();
var ID = {
  name: (lsGet('nayanet_smart_name') || '').trim(),
  alias: (lsGet('nayanet_smart_alias') || '').trim().toLowerCase(),
  device_key: lsGet('nayanet_vault_key') || ''
};
var S = { answers: {}, topics: [], reveal: null };
try {
  var saved = JSON.parse(lsGet(SKEY) || 'null');
  if (saved && saved.alias === ID.alias && ID.alias) { S.answers = saved.answers || {}; S.topics = saved.topics || []; S.reveal = saved.reveal || null; }
} catch(e){}
function save(){ try { lsSet(SKEY, JSON.stringify({ alias: ID.alias, answers: S.answers, topics: S.topics, reveal: S.reveal })); } catch(e){} }
function cred(extra){ var b = { alias: ID.alias, device_key: ID.device_key, name: ID.name }; for (var k in extra) b[k] = extra[k]; return b; }
async function api(path, body){ var r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }); var d = {}; try { d = await r.json(); } catch(e){} return { ok: r.ok, d: d }; }
window.__walkState = S;

var STEPS = [];
for (var i = 1; i <= 10; i++) STEPS.push(document.getElementById('step-' + i));
var ENDSEC = document.getElementById('step-end');
var DOORSEC = document.getElementById('step-door');
var cur = 0; /* 0..9 question steps, 10 = end */
function showStep(n){
  cur = n;
  STEPS.forEach(function(s, i){ s.hidden = (i !== n); });
  ENDSEC.hidden = (n !== 10);
  DOORSEC.hidden = true;
  window.__walkStep = n;
  window.scrollTo(0, 0);
  var vis = n < 10 ? STEPS[n] : ENDSEC;
  var ta = vis.querySelector('textarea.visionin');
  if (ta) { try { ta.focus({ preventScroll: true }); } catch(e){} }
}
function showDoor(){
  STEPS.forEach(function(s){ s.hidden = true; });
  ENDSEC.hidden = true; DOORSEC.hidden = false;
  window.__walkStep = -1;
}

function showStatus(el, text){ if (el._t) clearTimeout(el._t); el.textContent = text; el.hidden = false; el._t = setTimeout(function(){ el.hidden = true; el._t = null; }, 5000); }
function hideStatus(el){ if (el._t){ clearTimeout(el._t); el._t = null; } el.hidden = true; }

/* --- per-step wiring: the preview script, scoped to one step --- */
var playFromEye = false;
function wireStep(sec, idx){
  var n = idx + 1, key = KEYS[idx];
  var answer = sec.querySelector('#answer-' + n);
  var speakBtn = sec.querySelector('#speakBtn-' + n);
  var speakNote = sec.querySelector('#speakNote-' + n);
  var enterBtn = sec.querySelector('#enterBtn-' + n);
  var enterNote = sec.querySelector('#enterNote-' + n);
  var hintRow = sec.querySelector('#hintRow-' + n);
  var playBtn = sec.querySelector('#playBtn-' + n);
  if (S.answers[key]) answer.value = S.answers[key];

  hintRow.addEventListener('click', function(e){
    var b = e.target.closest('.p3-hint'); if (!b) return;
    hideStatus(speakNote); hideStatus(enterNote);
    var was = b.classList.contains('show');
    hintRow.querySelectorAll('.p3-hint.show').forEach(function(x){ x.classList.remove('show'); });
    playBtn.classList.remove('show');
    if (!was) b.classList.add('show');
    var act = b.getAttribute('data-act');
    if (act === 'play'){ playFromEye = true; playBtn.click(); playFromEye = false; }
    else if (act === 'dictate'){ startDictation(); }
    else if (act === 'focus'){ answer.focus(); }
    else if (act === 'paste'){ pasteIntoBox(); }
    else if (act === 'submit'){ submitAnswer(); }
  });
  hintRow.querySelectorAll('.p3-hint').forEach(function(h){
    function dismissOthers(){ hintRow.querySelectorAll('.p3-hint.show').forEach(function(x){ if (x !== h) x.classList.remove('show'); }); playBtn.classList.remove('show'); }
    h.addEventListener('mouseenter', dismissOthers);
    h.addEventListener('focusin', dismissOthers);
  });

  /* play: audio slots are empty until the audio round — glow only, never faked */
  function playGlow(){ playBtn.classList.add('pending-glow'); setTimeout(function(){ playBtn.classList.remove('pending-glow'); }, 900); }
  playBtn.addEventListener('mouseenter', function(){ hintRow.querySelectorAll('.p3-hint.show').forEach(function(x){ x.classList.remove('show'); }); });
  playBtn.addEventListener('focusin', function(){ hintRow.querySelectorAll('.p3-hint.show').forEach(function(x){ x.classList.remove('show'); }); });
  playBtn.addEventListener('click', function(){
    if (!playFromEye){
      hintRow.querySelectorAll('.p3-hint.show').forEach(function(x){ x.classList.remove('show'); });
      playBtn.classList.toggle('show');
    }
    playGlow();
  });

  function startDictation(){
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR){ showStatus(speakNote, "Speaking isn't available in this browser — type it in instead."); hideStatus(enterNote); return; }
    var rec = new SR(); rec.lang = 'en-US'; rec.interimResults = false; rec.maxAlternatives = 1;
    speakBtn.classList.add('live'); hideStatus(speakNote); hideStatus(enterNote);
    speakNote.textContent = 'Listening…'; speakNote.hidden = false;
    rec.onresult = function(e){
      var t = e.results[0][0].transcript || '';
      answer.value = answer.value ? (answer.value.replace(/\s+$/, '') + ' ' + t) : t;
      S.answers[key] = answer.value; save();
      answer.focus();
    };
    rec.onerror = function(){ showStatus(speakNote, "Couldn't hear that — try again, or type it in."); };
    rec.onend = function(){ speakBtn.classList.remove('live'); if (speakNote.textContent === 'Listening…') speakNote.hidden = true; };
    try { rec.start(); } catch(err){ speakBtn.classList.remove('live'); showStatus(speakNote, "Speaking couldn't start here — type it in instead."); }
  }
  speakBtn.addEventListener('click', startDictation);
  answer.addEventListener('input', function(){ S.answers[key] = answer.value; save(); hideStatus(speakNote); hideStatus(enterNote); });
  answer.addEventListener('focus', function(){ hideStatus(speakNote); hideStatus(enterNote); });

  function submitAnswer(){
    if (!answer.value.trim()){ showStatus(enterNote, 'Say it first — speak, type, or paste your answer, then Enter.'); }
    else {
      S.answers[key] = answer.value; save();
      hideStatus(speakNote);
      if (idx < 9) showStep(idx + 1);
      else completeWalk(enterNote);
    }
  }
  enterBtn.addEventListener('click', submitAnswer);

  function pasteIntoBox(){
    if (navigator.clipboard && navigator.clipboard.readText){
      navigator.clipboard.readText().then(function(t){
        if (t){ answer.value = answer.value ? (answer.value.trimEnd() + ' ' + t) : t; S.answers[key] = answer.value; save(); }
        answer.focus();
      }).catch(function(){ answer.focus(); });
    } else { answer.focus(); }
  }
}

/* --- completion: LIVE — POSTs the real endpoint, renders the real receipt --- */
async function completeWalk(enterNote){
  var r = await api('/api/welcome/complete', cred({ answers: S.answers, topics: S.topics }));
  if (!r.ok) { showStatus(enterNote, (r.d && r.d.error) || 'Something went wrong building your world — your answers are saved here; try once more.'); return; }
  S.reveal = r.d; save(); renderEnd(); showStep(10);
}
function renderEnd(){
  var alias = ID.alias || 'yourname';
  var linkFace = document.getElementById('linkFace');
  var real = (S.reveal && S.reveal.ambassador_link) || ('https://nayanet.live/joinus?ref=' + alias);
  linkFace.setAttribute('data-branded', 'nayanet.live/' + alias);
  linkFace.setAttribute('data-real', real);
  linkFace.textContent = 'nayanet.live/' + alias;
  linkFace.setAttribute('aria-label', 'Show your real affiliate link');
}

/* --- end slide wiring: end v2's handlers, LIVE — doors navigate for real --- */
(function wireEnd(){
  var playBtn = document.getElementById('playBtn-end');
  function playGlow(){ playBtn.classList.add('pending-glow'); setTimeout(function(){ playBtn.classList.remove('pending-glow'); }, 900); }
  playBtn.addEventListener('click', function(){ playBtn.classList.toggle('show'); playGlow(); });
  var doorNote = document.getElementById('doorNote');
  function showEndStatus(text){ if (doorNote._t) clearTimeout(doorNote._t); doorNote.textContent = text; doorNote.hidden = false; doorNote._t = setTimeout(function(){ doorNote.hidden = true; doorNote._t = null; }, 5000); }
  document.getElementById('doorRow').addEventListener('click', function(e){
    var b = e.target.closest('.p3-door'); if (!b) return;
    var d = b.getAttribute('data-door');
    var alias = ID.alias || 'yourname';
    var P = (S.reveal && S.reveal.pages) || {};
    var personal = P.personal || ('/world/' + alias);
    var business = P.business || ('/world/' + alias + '/business');
    var space = P.space || ('/world/' + alias + '/space');
    var urls = { Dashboard: personal + '#dashboard', Personal: personal, Business: business, Space: space, Hub: 'https://nayanet.live/' };
    if (urls[d]) window.location.href = urls[d];
  });
  var linkFace = document.getElementById('linkFace');
  linkFace.addEventListener('click', function(){
    var showingReal = linkFace.textContent === linkFace.getAttribute('data-real');
    linkFace.textContent = showingReal ? linkFace.getAttribute('data-branded') : linkFace.getAttribute('data-real');
    linkFace.setAttribute('aria-label', showingReal ? 'Show your real affiliate link' : 'Show your branded Smart Link');
  });
  var copyBtn = document.getElementById('copyBtn');
  copyBtn.addEventListener('click', function(){
    var real = linkFace.getAttribute('data-real');
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(real).then(function(){
        var old = copyBtn.textContent; copyBtn.textContent = 'Copied ✓';
        setTimeout(function(){ copyBtn.textContent = old; }, 2000);
      }).catch(function(){ showEndStatus('Copy did not work automatically — long-press the link to copy it.'); });
    } else { showEndStatus('Copy did not work automatically — long-press the link to copy it.'); }
  });
  var deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', function(e){ e.preventDefault(); deferredPrompt = e; });
  document.getElementById('installBtn').addEventListener('click', function(){
    if (deferredPrompt){ deferredPrompt.prompt(); deferredPrompt = null; return; }
    showEndStatus('To install on iPhone: Share, then Add to Home Screen. On Android: open in Chrome and use the install prompt when it appears.');
  });
})();

/* --- boot: LIVE — verify the certificate, then resume; otherwise the door --- */
(function boot(){
  document.querySelectorAll('.p3-flank-photo').forEach(function(img){
    var pi = parseInt(img.getAttribute('data-photo'), 10);
    img.src = PHOTOS[pi];
  });
  STEPS.forEach(function(sec, i){ wireStep(sec, i); });
  if (!ID.alias) { showDoor(); return; }
  api('/api/welcome/me', cred({})).then(function(r){
    if (r.ok && r.d && r.d.alias) {
      ID.name = r.d.name || ID.name;
      if (S.reveal) { renderEnd(); showStep(10); return; }
      /* resume at the first unanswered step, else step 1 */
      var first = 0;
      for (var i = 0; i < 10; i++){ if (!S.answers[KEYS[i]]){ first = i; break; } if (i === 9) first = 9; }
      showStep(first);
    } else { showDoor(); }
  }).catch(function(){ showDoor(); });
})();
})();
