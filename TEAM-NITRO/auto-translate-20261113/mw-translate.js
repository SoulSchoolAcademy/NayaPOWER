/* ═══ AUTO-TRANSLATE 2026-11-13 — the Translate tap (Part 2) ═══
   Lives beside MW_I18N in the page's own language block — no new file, no new
   framework, no new vendor. One endpoint, the staging worker
   naya-auto-translate-staging (Workers AI m2m100, AI binding proven Step 0).
   The citizen's words are NEVER replaced and NEVER stored as the translation:
   the original stays in the card, untouched; the translation is a labelled
   view beside it, one tap away. On tap only — never a blanket auto-translate.
   Source language is NEVER assumed: the viewer picks it from a short list on
   the tap (the feed carries no language field). Multi-sentence notes are
   segmented before sending (the model's known sentence-drop quirk) and the
   translated segments come back in order — a dropped segment fails honestly. */
(function(){
"use strict";
var EP = 'https://naya-auto-translate-staging.nayapower.workers.dev/translate';
var LANGS = [['en','English'],['es','Español'],['fr','Français'],['de','Deutsch']];
function esc(s){ var d=document.createElement('div'); d.textContent=String(s==null?'':s); return d.innerHTML; }
function tr(en){ try{ if(window.mwTr) return window.mwTr(en); }catch(e){} return en; }
function pickLang(){ try{ var v=localStorage.getItem('mw.set.lang'); if(v) return JSON.parse(v); }catch(e){} return mwBrowserLang(); }
function mwBrowserLang(){
  try{
    var l=(navigator.language||navigator.userLanguage||'en').toLowerCase().slice(0,2);
    return (l==='es'||l==='fr'||l==='de')?l:'en';
  }catch(e){ return 'en'; }
}
function langName(code){
  for(var i=0;i<LANGS.length;i++) if(LANGS[i][0]===code) return LANGS[i][1];
  return code;
}
/* sentencesOf: the card renderer's own splitter, verbatim in shape — a note
   translated whole means every sentence counted in and every sentence out. */
/* REPAINT RESILIENCE (fresh maker, 2026-11-13): the page's own wall painter
   (mwPaintWallPosts) rebuilds the wall with list.innerHTML whenever the feed
   repaints — on load when the live rows land, on tab switches, on filters.
   A rebuild destroys the card node, and with it any open source-picker or
   finished translation view. Proven first-hand: picker opened at +100ms after
   the tap, wall repaint at +700ms swapped the card for a fresh node, picker
   gone, tap dead. The module therefore keeps its state by CARD KEY, not by
   node: an open picker (pendingPick) and a finished translation (doneViews)
   are re-mounted onto the fresh node when scan() sees it. The citizen's tap
   is never silently lost to a repaint. Keys are the stub id where the card
   has one, else a hash of its own words — same words, same translation. */
var pendingPick={}, doneViews={}, inFlight={};
function keyHash(s){ var h=0; for(var i=0;i<s.length;i++){ h=((h<<5)-h+s.charCodeAt(i))|0; } return (h>>>0).toString(36); }
function msgWords(m){ var txt=(m.childNodes[0] && m.childNodes[0].nodeType===3) ? m.childNodes[0].textContent : (m.textContent||''); return {body: String(txt||'').trim()}; }
function wordsFor(kind){ return kind==='wall'?cardWords:(kind==='msg'?msgWords:nayaCardWords); }
function cardKey(card, kind){
  if(!card) return '';
  var id=card.getAttribute && card.getAttribute('data-fc-stub');
  if(id) return 'stub:'+id;
  try{
    var w = wordsFor(kind)(card);
    var t = kind==='wall' ? (w.nutshell||'') : ((w.title||'')+'|'+(w.body||''));
    return kind+':h'+keyHash(String(t).replace(/\s+/g,' ').trim().slice(0,120));
  }catch(e){ return kind+':?'; }
}
function findCard(key, kind){
  if(!key) return null;
  var el=document.querySelector('[data-mw-tr-key="'+key+'"]');
  if(el) return el;
  /* the fresh node has not been through attachRow yet — match by content. */
  var sel = kind==='wall' ? '#os-wall-list article.intel-board' : (kind==='msg' ? '#fcChat .fc-chat-msg' : '#mwFeedNaya .ph-card');
  var nodes=document.querySelectorAll(sel);
  for(var i=0;i<nodes.length;i++){ if(cardKey(nodes[i],kind)===key) return nodes[i]; }
  return null;
}
function mountView(card, kind, data, src, tgt, doScroll){
  if(!card) return;
  var old=card.querySelector('.mw-tr-view');
  if(old) old.remove();
  var view=document.createElement('div');
  var vk = kind==='msg' ? 'naya' : kind;
  var renderView=function(){
    view.className='mw-tr-view';
    view.innerHTML=buildView(vk, data, src, tgt);
    view.querySelector('.mw-tr-orig').addEventListener('click', function(){
      /* original one tap away: the view collapses to a single pill; the
         original card content was never touched and is right there. */
      view.className='mw-tr-view mw-tr-collapsed';
      view.innerHTML='';
      var back=document.createElement('button');
      back.type='button'; back.className='mw-tr-orig';
      back.textContent=tr('Show translation');
      back.addEventListener('click', renderView);
      view.appendChild(back);
    });
  };
  renderView();
  card.appendChild(view);
  var row=card.querySelector('.mw-tr-row'); if(row) row.classList.remove('mw-tr-busy');
  /* a restore onto a repainted node never yanks the scroll — only a fresh
     tap the citizen just made scrolls the view into sight. */
  if(doScroll!==false){ try{ view.scrollIntoView({behavior:'smooth', block:'nearest'}); }catch(e){} }
}
function sentencesOf(txt){
  return (String(txt||'').replace(/\s+/g,' ').match(/[^.!?]+[.!?]+["']?|[^.!?]+$/g)||[])
    .map(function(s){ return s.trim(); }).filter(Boolean);
}
function shortHook(txt){
  var s=String(txt||'').replace(/\s+/g,' ').replace(/[*`]/g,'').trim();
  if(s.length<=60) return s;
  var cut=s.slice(0,59), sp=cut.lastIndexOf(' ');
  var head=(sp>30?cut.slice(0,sp):cut).replace(/[,;:\u2014\u2013-]+$/,'').trim();
  return head+'\u2026';
}
function translateSegments(segments, src, tgt){
  return fetch(EP, {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({segments:segments, source_lang:src, target_lang:tgt})})
    .then(function(r){ return r.json().then(function(d){ if(!r.ok||!d.ok) throw new Error((d&&d.error)||('HTTP '+r.status)); return d; }); })
    .then(function(d){
      if(!d.segments || d.segments.length!==segments.length) throw new Error('segment count mismatch');
      return d.segments;
    });
}
/* Read a wall card's own words from the rendered card (never the data store —
   this works for live rows, the collective, and local stubs alike). The
   headline/subtitle are derived from the nutshell, exactly as the card's own
   renderer derives them — so the translation carries title + subtitle +
   nutshell (L3), re-derived the same way. */
function cardWords(card){
  var nutEl=card.querySelector('.ib-nutshell');
  var nut='';
  if(nutEl){
    nut=(nutEl.textContent||'').replace(/^\s*IN A NUTSHELL\s*/i,'').trim();
  }
  var human='';
  var layers=card.querySelectorAll('.ib-layer');
  for(var i=0;i<layers.length;i++){
    var hb=layers[i].querySelector('.ib-layer-head b');
    var bd=layers[i].querySelector('.ib-layer-body');
    if(hb && /HUMAN NOTE/i.test(hb.textContent||'') && bd) human=(bd.textContent||'').trim();
  }
  return {nutshell:nut, human:human};
}
function nayaCardWords(card){
  /* the Naya card is: h3 title, p meta (category · date), p body — the body
     is the last <p>. */
  var h=card.querySelector('h3');
  var ps=card.querySelectorAll('p');
  var body=ps.length?(ps[ps.length-1].textContent||'').trim():'';
  return {title:h?(h.textContent||'').trim():'', body:body};
}
function buildView(kind, data, src, tgt){
  /* kind 'wall': data {title, subtitle, nutshell, human?}; kind 'naya': {title, body} */
  var srcName = src==='es'?'Spanish':(src==='fr'?'French':(src==='de'?'German':'English'));
  /* full-sentence keys — no grammar assembly across languages. */
  var label=tr('Translated from '+srcName);
  var h='<div class="mw-tr-view"><div class="mw-tr-label"><span class="mw-tr-globe">\u{1F310}</span> '+esc(label)+'</div>';
  if(kind==='wall'){
    h+='<h2 class="mw-tr-title">'+esc(data.title)+'</h2>';
    if(data.subtitle) h+='<div class="mw-tr-sub">'+esc(data.subtitle)+'</div>';
    h+='<div class="mw-tr-nut"><b>'+esc(tr('In a nutshell'))+'</b>'+esc(data.nutshell)+'</div>';
    if(data.human) h+='<div class="mw-tr-human">'+esc(data.human)+'</div>';
  }else{
    if(data.title) h+='<h2 class="mw-tr-title">'+esc(data.title)+'</h2>';
    h+='<div class="mw-tr-nut">'+esc(data.body)+'</div>';
  }
  h+='<button type="button" class="mw-tr-orig">'+esc(tr('Show original'))+'</button></div>';
  return h;
}
function showFailure(card){
  var old=card.querySelector('.mw-tr-view');
  if(old) old.remove();
  var d=document.createElement('div');
  d.className='mw-tr-view mw-tr-fail';
  d.textContent=tr('Translation unavailable \u2014 the original is here');
  card.appendChild(d);
  setTimeout(function(){ if(d.parentNode) d.parentNode.removeChild(d); }, 6000);
}
function startTranslate(card, kind, getWords){
  var tgt=pickLang();
  var key=cardKey(card, kind);
  var row=card.querySelector('.mw-tr-row');
  if(row) row.classList.add('mw-tr-busy');
  /* the picker is state by key: a repaint re-opens it on the fresh node. */
  pendingPick[key]={kind:kind, tgt:tgt};
  /* the source picker: four native-name buttons, never an assumed English. */
  var pick=document.createElement('div');
  pick.className='mw-tr-pick';
  pick.innerHTML='<span class="mw-tr-pick-q">'+esc(tr('What language is this note in?'))+'</span>';
  LANGS.forEach(function(L){
    var b=document.createElement('button');
    b.type='button'; b.className='mw-tr-lang'; b.textContent=L[1]; b.setAttribute('data-lang',L[0]);
    b.addEventListener('click', function(){ delete pendingPick[key]; run(card, kind, getWords, L[0], tgt, pick); });
    pick.appendChild(b);
  });
  card.appendChild(pick);
  var cancel=document.createElement('button');
  cancel.type='button'; cancel.className='mw-tr-cancel'; cancel.textContent='\u2715';
  cancel.setAttribute('aria-label','Close');
  cancel.addEventListener('click', function(){ delete pendingPick[key]; if(pick.parentNode) pick.parentNode.removeChild(pick); if(row) row.classList.remove('mw-tr-busy'); });
  pick.appendChild(cancel);
}
function run(card, kind, getWords, src, tgt, pick){
  if(pick.parentNode) pick.parentNode.removeChild(pick);
  var key=cardKey(card, kind);
  delete pendingPick[key];
  inFlight[key]=true;
  if(src===tgt){
    inFlight[key]=false;
    var d=document.createElement('div');
    d.className='mw-tr-view';
    d.textContent=tr('Already in your language');
    card.appendChild(d);
    setTimeout(function(){ if(d.parentNode) d.parentNode.removeChild(d); }, 4000);
    var row0=card.querySelector('.mw-tr-row'); if(row0) row0.classList.remove('mw-tr-busy');
    return;
  }
  var words=getWords(card);
  var fields=[], map=[];
  if(kind==='wall'){
    if(words.nutshell){ fields.push({k:'nut', text:words.nutshell}); }
    if(words.human){ fields.push({k:'human', text:words.human}); }
  }else{
    if(words.title){ fields.push({k:'title', text:words.title}); }
    if(words.body){ fields.push({k:'body', text:words.body}); }
  }
  var segments=[], owners=[];
  fields.forEach(function(f){
    var ss=sentencesOf(f.text);
    ss.forEach(function(s){ segments.push(s); owners.push(f.k); });
  });
  if(!segments.length){ inFlight[key]=false; showFailure(card); return; }
  translateSegments(segments, src, tgt).then(function(out){
    var byField={};
    out.forEach(function(t,i){ (byField[owners[i]]=byField[owners[i]]||[]).push(t); });
    var join=function(k){ return (byField[k]||[]).join(' '); };
    var data;
    if(kind==='wall'){
      var nutT=join('nut'), nutS=sentencesOf(nutT);
      data={title:nutS[0]||nutT, subtitle:shortHook(nutS[1]||''), nutshell:nutT, human:join('human')};
    }else{
      data={title:join('title'), body:join('body')};
    }
    /* store by key FIRST, then mount on the live node: if a repaint swapped
       the card mid-fetch, the fresh node gets the view from attachRow. */
    doneViews[key]={kind:kind, data:data, src:src, tgt:tgt};
    inFlight[key]=false;
    var live=findCard(key, kind);
    if(live) mountView(live, kind, data, src, tgt);
    /* the original stays: the translated view sits below it in the card and
       the card's own content is never removed, never rewritten. The toggle
       hides the view; the original was always there. */
  }).catch(function(){
    inFlight[key]=false;
    var live=findCard(key, kind);
    if(live){ var row=live.querySelector('.mw-tr-row'); if(row) row.classList.remove('mw-tr-busy'); showFailure(live); }
  });
}
function attachRow(card, kind){
  if(!card || card.querySelector('.mw-tr-row')) return;
  var key=cardKey(card, kind);
  try{ card.setAttribute('data-mw-tr-key', key); }catch(e){}
  var row=document.createElement('div');
  row.className='mw-tr-row';
  var btn=document.createElement('button');
  btn.type='button'; btn.className='mw-tr-btn';
  btn.innerHTML='<span class="mw-tr-ico">\u{1F310}</span> <span>'+esc(tr('Translate'))+'</span>';
  btn.addEventListener('click', function(){
    if(card.querySelector('.mw-tr-pick')) return;
    startTranslate(card, kind, wordsFor(kind));
  });
  row.appendChild(btn);
  card.appendChild(row);
  /* repaint resilience: a picker open, or a translation done, on the card
     this node replaced comes back on the fresh node. */
  if(pendingPick[key]){
    startTranslate(card, kind, wordsFor(kind));
  }else if(doneViews[key]){
    var dv=doneViews[key];
    mountView(card, dv.kind, dv.data, dv.src, dv.tgt, false);
  }
}
function scan(root){
  if(!root || !root.querySelectorAll) return;
  /* re-label Translate taps when the chrome language changes. The compare
     is the fix: an unconditional assignment is itself a mutation, and the
     observer below would re-fire scan forever on it (the tab hung after the
     first stub card appeared — 2026-11-13, caught in verification). */
  root.querySelectorAll('.mw-tr-btn').forEach(function(b){
    var spans=b.querySelectorAll('span');
    if(spans.length>1){ var t=tr('Translate'); if(spans[1].textContent!==t) spans[1].textContent=t; }
  });
  root.querySelectorAll('#os-wall-list article.intel-board').forEach(function(c){ attachRow(c,'wall'); });
  root.querySelectorAll('#mwFeedNaya .ph-card').forEach(function(c){ attachRow(c,'naya'); });
  /* chat messages: each message carries its own tap; the message text is the
     div's own text, translated the same way, shown under it, original kept. */
  root.querySelectorAll('#fcChat .fc-chat-msg').forEach(function(m){
    if(m.querySelector('.mw-tr-btn')) return;
    var b=document.createElement('button');
    b.type='button'; b.className='mw-tr-btn mw-tr-msg-btn';
    b.innerHTML='<span class="mw-tr-ico">\u{1F310}</span> <span>'+esc(tr('Translate'))+'</span>';
    b.addEventListener('click', function(){
      startTranslate(m, 'msg', msgWords);
    });
    m.appendChild(b);
  });
}
function boot(){
  scan(document);
  if(!window.MutationObserver) return;
  var obsPending=false;
  var obs=new MutationObserver(function(){
    /* coalesce a burst of mutations into one scan per microtask — a scan that
       itself mutates (attaching a row) must not re-enter the queue endlessly. */
    if(obsPending) return; obsPending=true;
    setTimeout(function(){ obsPending=false; scan(document); }, 0);
  });
  ['os-wall-list','mwFeedNaya','fcChat'].forEach(function(id){
    var el=document.getElementById(id);
    if(el) obs.observe(el, {childList:true, subtree:true});
  });
  /* re-label Translate buttons when the chrome language changes. */
  document.addEventListener('mw-lang-changed', function(){ scan(document); });
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
/* msg cards: the generic run() renders a 'naya' view; a chat message renders
   its translated text in the same view shape (title empty, body translated). */
window.__mwTranslate={translateSegments:translateSegments, sentencesOf:sentencesOf, scan:scan, cardKey:cardKey, findCard:findCard};
})();
