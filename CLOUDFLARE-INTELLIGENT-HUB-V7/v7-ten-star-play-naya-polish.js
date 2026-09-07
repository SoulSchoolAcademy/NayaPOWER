/* NayaNET V7 — surgical Play Naya polish layer.
   Keeps the existing feed intact while making playback state note-specific,
   resilient to feed re-renders, and easier to evolve toward the Naya Voice API.
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
    const card=button.closest('.ib');
    if(!card) return;
    const id=card.dataset.id;

    if(activeId===id){
      if(paused){ window.speechSynthesis.resume(); paused=false; syncButtons(); }
      else { window.speechSynthesis.pause(); paused=true; syncButtons(); }
      return;
    }

    if(activeId) window.speechSynthesis.cancel();
    activeId=id; paused=false; index=0;
    const selectors=[
      ['IN A NUTSHELL','.nutshell p'],
      ['HUMAN NOTE','.persp.human p'],
      ['CHILD NOTE','.persp.child p'],
      ['GRANDMA NOTE','.persp.grandma p'],
      ['NAYA NOTE','.persp.naya p'],
      ['MACHINE NOTE','.persp.machine p'],
      ['WHAT WE LEARNED','.meaning p:nth-of-type(1)'],
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

  function init(){
    bind();
    if(observer) observer.disconnect();
    observer=new MutationObserver(()=>bind());
    const root=document.getElementById('nayanet-ten-star-feed');
    if(root) observer.observe(root,{subtree:true,childList:true});
    window.addEventListener('pagehide',stop,{once:true});
    window.addEventListener('beforeunload',stop,{once:true});
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
