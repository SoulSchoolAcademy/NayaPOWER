/* NayaNET V7 — surgical Play Naya polish + canonical feed finish.
   Keeps the existing feed intact while making playback state note-specific,
   resilient to feed re-renders, and preserving one identical premium block
   architecture across Activity, Personal Intelligence, and Collective Intelligence.
*/
(()=>{
  'use strict';
  if(window.__NAYA_PLAY_NAYA_POLISH__) return;
  window.__NAYA_PLAY_NAYA_POLISH__=true;

  let activeId=null;
  let paused=false;
  let queue=[];
  let index=0;
  let observer=null;

  const buttons=()=>Array.from(document.querySelectorAll('.naya-play[data-play]'));
  const activeButton=()=>buttons().find(b=>b.dataset.play===activeId);

  function setButton(b,mode){
    if(!b) return;
    const isActive=activeId && b.dataset.play===activeId;
    b.textContent=isActive ? (mode==='paused'?'▶ RESUME NAYA':'Ⅱ PAUSE NAYA') : '▶ PLAY NAYA';
    b.classList.toggle('is-playing',!!isActive);
    b.setAttribute('aria-pressed',isActive?'true':'false');
    b.setAttribute('aria-label',isActive ? (mode==='paused'?'Resume Naya playback':'Pause Naya playback') : 'Play Naya for this intelligence event');
  }

  function syncButtons(){
    buttons().forEach(b=>setButton(b,paused?'paused':'playing'));
  }

  function stop(){
    if('speechSynthesis' in window) window.speechSynthesis.cancel();
    activeId=null; paused=false; queue=[]; index=0; syncButtons();
  }

  function finish(){
    activeId=null; paused=false; queue=[]; index=0; syncButtons();
  }

  function speakNext(){
    if(!activeId || !queue[index]){ finish(); return; }
    const u=new SpeechSynthesisUtterance(queue[index].label+'. '+queue[index].text);
    u.rate=.94;
    u.pitch=1.02;
    u.onend=()=>{
      if(!activeId) return;
      index++;
      speakNext();
    };
    u.onerror=()=>finish();
    window.speechSynthesis.speak(u);
  }

  function readDisplayedNote(button){
    if(!('speechSynthesis' in window)){
      alert('Naya audio is not available in this browser yet.');
      return;
    }
    const card=button.closest('.ib') || button.closest('.n3-block');
    if(!card) return;
    const id=card.dataset.id || card.querySelector('.n3-title')?.textContent?.trim();

    if(activeId===id){
      if(paused){ window.speechSynthesis.resume(); paused=false; syncButtons(); }
      else { window.speechSynthesis.pause(); paused=true; syncButtons(); }
      return;
    }

    if(activeId) window.speechSynthesis.cancel();
    activeId=id; paused=false; index=0;
    const selectors=[
      ['IN A NUTSHELL','.nutshell p,.n3-nutshell p'],
      ['HUMAN NOTE','.persp.human p,.n3-perspective:nth-child(1) .n3-pbody'],
      ['CHILD NOTE','.persp.child p,.n3-perspective:nth-child(2) .n3-pbody'],
      ['GRANDMA NOTE','.persp.grandma p,.n3-perspective:nth-child(3) .n3-pbody'],
      ['NAYA NOTE','.persp.naya p,.n3-perspective:nth-child(4) .n3-pbody'],
      ['MACHINE NOTE','.persp.machine p,.n3-perspective:nth-child(5) .n3-pbody'],
      ['WHAT WE LEARNED','.meaning p:nth-of-type(1),.n3-perspective:nth-child(6) .n3-pbody'],
      ['WHAT IT MEANS','.meaning p:nth-of-type(2)']
    ];
    queue=selectors.map(([label,selector])=>({label,text:card.querySelector(selector)?.textContent?.trim()||''})).filter(x=>x.text);
    syncButtons();
    speakNext();
  }

  function bind(){
    buttons().forEach(b=>{
      if(b.dataset.nayaPolishBound==='1') return;
      b.dataset.nayaPolishBound='1';
      b.onclick=(event)=>{
        event.preventDefault();
        event.stopPropagation();
        readDisplayedNote(b);
      };
      setButton(b,paused?'paused':'playing');
    });
  }

  function finishFeedPresentation(){
    if(document.getElementById('nayanet-v7-feed-finish-style')) return;
    const style=document.createElement('style');
    style.id='nayanet-v7-feed-finish-style';
    style.textContent=`
      /* CANONICAL FEED PARITY: all three views are projections of one block. */
      #nayanet-elite-feed{max-width:none!important;width:100%!important;padding-left:0!important;padding-right:0!important}
      #nayanet-elite-feed .n3-body{gap:24px!important}
      #nayanet-elite-feed .n3-block{border-color:#ffffff28!important;border-radius:28px!important;background:linear-gradient(145deg,#030304 0%,#000 62%,#020203 100%)!important;box-shadow:inset 0 1px #fff7,0 30px 76px #000e,0 0 42px color-mix(in srgb,var(--accent) 10%,transparent)!important}
      #nayanet-elite-feed .n3-block:before{width:4px!important;box-shadow:0 0 30px var(--accent),0 0 70px color-mix(in srgb,var(--accent) 34%,transparent)!important}
      #nayanet-elite-feed .n3-block:after{opacity:.07!important;filter:blur(2px)!important}
      #nayanet-elite-feed .n3-head{padding:25px 26px 19px!important;background:linear-gradient(180deg,#ffffff03,transparent)!important}
      #nayanet-elite-feed .n3-title{color:#fff!important;font-weight:900!important;text-wrap:balance}
      #nayanet-elite-feed .n3-nutshell{margin:18px 20px 13px!important;padding:22px 24px 24px!important;border-color:#ffffff52!important;background:linear-gradient(145deg,#0d0d11,#030305)!important;box-shadow:inset 0 1px #fff9,0 20px 44px #000b,0 0 38px #fff06!important}
      #nayanet-elite-feed .n3-nutshell p{color:#fff!important;font-weight:560!important}
      #nayanet-elite-feed .n3-perspectives{gap:10px!important;padding:7px 20px 5px!important}
      #nayanet-elite-feed .n3-perspective{min-height:86px!important;border-width:1px!important;background:linear-gradient(145deg,#09090c,#020203)!important;box-shadow:inset 0 1px #fff4,0 12px 28px #000a,0 0 28px color-mix(in srgb,var(--p) 10%,transparent)!important;transition:transform .22s cubic-bezier(.16,.84,.22,1),box-shadow .22s ease,border-color .22s ease!important}
      #nayanet-elite-feed .n3-perspective:hover{transform:translateY(-2px)!important;box-shadow:inset 0 1px #fff6,0 17px 34px #000c,0 0 32px color-mix(in srgb,var(--p) 15%,transparent)!important}
      #nayanet-elite-feed .n3-phead{padding:13px 15px 9px!important}
      #nayanet-elite-feed .n3-picon{width:30px!important;height:30px!important;border-radius:10px!important}
      #nayanet-elite-feed .n3-phead b,#nayanet-elite-feed .n3-label,#nayanet-elite-feed .n3-eyebrow{color:#fff!important}
      #nayanet-elite-feed .n3-pbody{padding:12px 15px 16px!important;color:#f4f1f6!important;font-size:11.5px!important;line-height:1.66!important}
      #nayanet-elite-feed .n3-footer{padding:15px 20px 20px!important}
      #nayanet-elite-feed .n3-btn{min-height:38px!important;border-radius:11px!important;color:#fff!important;background:#07070a!important}
      #nayanet-elite-feed .n3-btn.naya-play,.n3-btn.naya-play{border-color:#d86cff66!important;box-shadow:inset 0 1px #fff4,0 0 22px #d86cff0c!important}
      #nayanet-elite-feed .n3-btn.naya-play.is-playing{border-color:#fff!important;box-shadow:inset 0 1px #fff8,0 0 25px #d86cff22!important}
      #nayanet-elite-feed .n3-bottom{margin-top:40px!important;padding-top:28px!important}
      #nayanet-elite-feed .n3-bottom strong,#nayanet-elite-feed .n3-bottom span{color:#fff!important}
      /* The view changes meaning, never geometry. */
      #nayanet-elite-feed[data-view="activity"] .n3-block,#nayanet-elite-feed[data-view="personal"] .n3-block,#nayanet-elite-feed[data-view="collective"] .n3-block{border-radius:28px!important}
      @media(max-width:820px){
        #nayanet-elite-feed .n3-block{border-radius:23px!important}
        #nayanet-elite-feed .n3-head{padding:19px 15px 15px!important}
        #nayanet-elite-feed .n3-nutshell{margin:14px 12px 10px!important;padding:18px!important}
        #nayanet-elite-feed .n3-perspectives{padding:6px 12px 3px!important}
      }
    `;
    document.head.appendChild(style);
  }

  function init(){
    finishFeedPresentation();
    bind();
    if(observer) observer.disconnect();
    observer=new MutationObserver(()=>{finishFeedPresentation();bind();});
    const root=document.getElementById('nayanet-ten-star-feed') || document.getElementById('nayanet-elite-feed');
    if(root) observer.observe(root,{subtree:true,childList:true});
    window.addEventListener('pagehide',stop,{once:true});
    window.addEventListener('beforeunload',stop,{once:true});
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
