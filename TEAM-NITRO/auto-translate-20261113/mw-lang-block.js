/* ---------- language (fix 18, grown AUTO-TRANSLATE 2026-11-13) ---------- */
/* The dictionary grows from 17 distinct keys to the whole home chrome (the
   inventory the maker counted at round start: 165 keys (158 chrome + 'In a
   nutshell' + 'open' + 6 creator/chat keys found while grounding tgSetMode and
   fcOpenChat). Harvested verbatim in shape — same MW_I18N + mwApplyLang machine,
   never a framework. Proper names never translate (Naya, NayaNET, a citizen's
   alias, page names). Icons never translate (R20). The dict was drafted
   through the round's own Workers AI translation worker and reviewed string
   by string by the maker — see RECORD §4 for the review fixes. */
var MW_I18N=/*__MW_I18N_JSON__*/;
function mwBrowserLang(){
  try{
    var l=(navigator.language||navigator.userLanguage||'en').toLowerCase().slice(0,2);
    return (l==='es'||l==='fr'||l==='de')?l:'en';
  }catch(e){ return 'en'; }
}
function mwLangCode(){
  var s=null; try{ s=mwGet('lang',null); }catch(e){}
  if(s) return s;
  return mwBrowserLang();
}
function mwTr(en){
  var code=mwLangCode();
  if(code==='en') return en;
  var d=MW_I18N[code]||{};
  return d[en]||en;
}
window.mwTr=mwTr; window.mwLangCode=mwLangCode; window.mwBrowserLang=mwBrowserLang;
function mwApplyLang(){
  var code=mwLangCode();
  try{ document.documentElement.lang=code; }catch(e){}
  var dict=MW_I18N[code]||{};
  var byId={msgbtn:'Message',aboutbtn:'About',myworldbtn:'My World',statsbtn:'Stats',intelbtn:"Today's Intel",skillsbtn:'Skills',connbtn:'Connections',growthbtn:'Invite',sharebtn:'Share',joinbtn:'Join NayaNET',settingsbtn:'Settings',memberbtn:'Become a Member',saBackBtn:'Back to my world',cvrbtn:'Change cover','tg-back':'Back to my words','tg-post-smart':'Post smart note',fcChatSend:'Send'}; /* AUTO-TRANSLATE: the row's missing three (Stats, Today's Intel, Skills — the first two are dead ids today, covered for when they return) + the hidden-until-open buttons + the chat Send. The creator's two buttons are NOT here: os-post-btn's label is per-mode (tgSetMode owns it, re-run below) and os-sched-btn's label is dynamic (a scheduled date) — the byId pass would clobber both. */
  Object.keys(byId).forEach(function(id){
    var el=$(id); if(!el) return;
    if(el.classList && el.classList.contains('pc-gear')) return; /* PERSONAL-COMPLETE: the gear is an icon, not a label. */
    var en=byId[id];
    var txt=(code==='en')?en:(dict[en]||en);
    var icon=(el.textContent||'').match(/^([^\p{L}\p{N}'’]+\s)/u); /* ROUND 6 FIX-1 (this round, self-check 4): only a leading non-word token is an icon — a label that starts with a word ("Today's Intel") is the label, not an icon to re-attach. \p{L} not \w: JS \w is ASCII-only, so a French 'À propos' or German 'Über'/'Ändern' had its first letter eaten into the 'icon' on the NEXT switch ('ⓘ À Über'). Unicode letters are word characters. */
    el.textContent=(icon?icon[1]:'')+txt;
    if(id==='myworldbtn' && code==='en') el.textContent='🌍 My World';
  });
  /* AUTO-TRANSLATE: the Schedule button only when nothing is scheduled — a
     scheduled date label is data, never chrome, and must never be clobbered. */
  var sb=$('os-sched-btn'); if(sb && !sb.classList.contains('set')) sb.textContent='\uD83D\uDD50 '+((code==='en')?'Schedule':(dict['Schedule']||'Schedule'));
  /* AUTO-TRANSLATE: the creator's mode labels (title, hint, post button) live
     in tgSetMode — re-run the current mode so they follow the switch. */
  if(window.tgSetMode && window.osNoteMode){ try{ window.tgSetMode(window.osNoteMode); }catch(e){} }
  var sbtn=$('pcSearchBtn'); if(sbtn) sbtn.setAttribute('aria-label',(code==='en')?'Search the public feed':(dict['Search the public feed']||'Search the public feed'));
  if(window.mwSyncMsgBtn) window.mwSyncMsgBtn(); /* ROUND 6: the Message/Connect label survives a language switch. */
  document.querySelectorAll('[data-mw-tr]').forEach(function(el){
    var key=el.getAttribute('data-mw-tr');
    var en=el.dataset.mwEn||el.textContent;
    if(!el.dataset.mwEn) el.dataset.mwEn=en;
    el.textContent=(code==='en')?en:(dict[en]||en);
  });
  /* AUTO-TRANSLATE: placeholders translate the same way (the mechanism never
     reached them — a placeholder is not textContent). */
  document.querySelectorAll('[data-mw-ph]').forEach(function(el){
    var en=el.dataset.mwEn||el.getAttribute('placeholder')||'';
    if(!el.dataset.mwEn) el.dataset.mwEn=en;
    el.setAttribute('placeholder',(code==='en')?en:(dict[en]||en));
  });
  /* CARD-LABELS-FIX: aria-labels on card buttons ride the same shape as
     placeholders — the English key rides in data-mw-aria, re-synced in
     place on every switch. (The [data-mw-tr] pass cannot do it: it writes
     textContent, and an aria-label is not textContent.) */
  document.querySelectorAll('[data-mw-aria]').forEach(function(el){
    var en=el.getAttribute('data-mw-aria')||'';
    if(!en) return;
    el.setAttribute('aria-label',(code==='en')?en:(dict[en]||en));
  });
  /* AUTO-TRANSLATE: the switch caps (On/Off) are set by mwSyncSwitch at
     setup — before mwTr exists, so they stay English after a switch unless
     re-synced here from each switch's own on/off state. */
  document.querySelectorAll('.os-switch-wrap').forEach(function(w){
    var sw=w.querySelector('.os-switch'), cap=w.querySelector('.os-switch-cap');
    if(sw && cap) cap.textContent=sw.classList.contains('on')?((code==='en')?'On':(dict['On']||'On')):((code==='en')?'Off':(dict['Off']||'Off'));
  });
  /* SETTINGS-FIX: the install-state line is written by page JS
     (renderInstallState, global), not by markup — re-run it so it follows
     the switch. The auth button likewise is written by the auth IIFE
     (updateAuthUI, not global) — re-sync it here only while signed out;
     signed in it shows the citizen's own email, which is data, never
     translated. */
  if(window.renderInstallState){ try{ window.renderInstallState(); }catch(e){} }
  var ab=$('naya-auth-btn');
  if(ab && !(window.NayaAuth && window.NayaAuth.user)) ab.textContent=(code==='en')?'Sign in':(dict['Sign in']||'Sign in');
  /* SETTINGS-FIX: the auth card's info button (round 2d decorator) carries
     its explanation as an aria-label — re-sync it like the bottom bar's. */
  var aib=document.querySelector('#settings .os-info-btn');
  if(aib) aib.setAttribute('aria-label',(code==='en')?'What does signing in do?':(dict['What does signing in do?']||'What does signing in do?'));
  /* SETTINGS-FIX: the cover-slot placeholders are visible labels in the
     panel; sync them (and their aria-labels) in place on every switch —
     never re-render the slots here, or text the citizen is typing into a
     slot would be wiped. */
  document.querySelectorAll('#mw-cover-slots input[data-mw-slot-label]').forEach(function(inp){
    var n=inp.getAttribute('data-mw-slot-label');
    inp.setAttribute('placeholder',(code==='en')?'Button name — e.g. Naya Academy':(dict['Button name — e.g. Naya Academy']||'Button name — e.g. Naya Academy'));
    inp.setAttribute('aria-label',((code==='en')?'Cover button':(dict['Cover button']||'Cover button'))+' '+(+n+1)+' '+((code==='en')?'Name':(dict['Name']||'Name')));
  });
  document.querySelectorAll('#mw-cover-slots input[data-mw-slot-url]').forEach(function(inp){
    var n=inp.getAttribute('data-mw-slot-url');
    inp.setAttribute('placeholder',(code==='en')?'URL — enter it and the button wakes up':(dict['URL — enter it and the button wakes up']||'URL — enter it and the button wakes up'));
    inp.setAttribute('aria-label',((code==='en')?'Cover button':(dict['Cover button']||'Cover button'))+' '+(+n+1)+' URL');
  });
  /* AUTO-TRANSLATE: the bottom bar is icon-only — its only words are the
     accessible names. They translate in place; the icons never change. */
  var segNames={plus:'ADD',mail:'MAIL',activity:'ACTIVITY',spaces:'SPACES',eco:'ECOSYSTEM'};
  document.querySelectorAll('#naya-notif-bar [data-notif]').forEach(function(b){
    var en=segNames[b.getAttribute('data-notif')]; if(!en) return;
    var t=(code==='en')?en:(dict[en]||en);
    b.setAttribute('aria-label', t+' — '+(code==='en'?'open':(dict['open']||'open')));
    b.setAttribute('title', t);
  });
  /* AUTO-TRANSLATE: the login bottombar shows a course description when a
     membership is active (its text is content then, not chrome) — translate
     it only while it still holds the chrome tagline in any of the four. */
  var bb=$('saLoginBottombar');
  if(bb){ var cur=bb.textContent.trim(), en0='Create. Connect. Grow with us.';
    var tr0=(code==='en')?en0:(dict[en0]||en0);
    var isChrome=(cur===en0)||(cur===(MW_I18N.es[en0]||''))||(cur===(MW_I18N.fr[en0]||''))||(cur===(MW_I18N.de[en0]||''));
    if(isChrome) bb.textContent=tr0; }
  /* AUTO-TRANSLATE: the side rail is rendered by JS — re-render it so its
     buttons, section labels and counts follow the picked language. */
  if(window.pcRenderRail){ try{ window.pcRenderRail(); }catch(e){} }
  /* AUTO-TRANSLATE: the Translate taps re-label with the chrome. */
  try{ document.dispatchEvent(new CustomEvent('mw-lang-changed')); }catch(e){}
}
