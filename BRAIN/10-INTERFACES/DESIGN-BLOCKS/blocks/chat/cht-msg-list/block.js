/* The scroll contract. appendBubble() is the ONLY writer of new rows.
   Rule: stick to bottom only if already there (within 64px). Otherwise the
   pill counts honestly and the reader is never yanked. */
(function(){
  const sc=document.getElementById('chatScroll'),pill=document.getElementById('chatNew'),
        n=document.getElementById('chatNewN');
  const EDGE=64;let unread=0;
  function atBottom(){return sc.scrollHeight-sc.scrollTop-sc.clientHeight<=EDGE;}
  function render(){pill.hidden=unread===0;n.textContent=unread;}
  sc.addEventListener('scroll',()=>{if(atBottom()&&unread>0){unread=0;render();}},{passive:true});
  pill.addEventListener('click',()=>{sc.scrollTop=sc.scrollHeight;unread=0;render();pill.blur();});
  window.chatAppend=function(rowEl){
    const wasDown=atBottom();
    sc.insertBefore(rowEl,pill);
    if(wasDown){sc.scrollTop=sc.scrollHeight;}
    else{unread++;render();}
  };
  /* Presence line contract: "N here now" renders only from a live presence
     feed. No feed, no line — the head shows the name alone. Never a guess. */
})();
