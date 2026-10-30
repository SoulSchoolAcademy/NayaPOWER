/* The typing contract. Your transport owns the truth; this module owns the
   honesty. show() requires a signal id; the 30s watchdog is non-negotiable. */
(function(){
  const WATCHDOG_MS=30000, KEEPALIVE_MS=20000;
  const live=new Map(); /* signalId -> {el, timer} */
  function dismiss(id,silent){
    const s=live.get(id);if(!s)return;
    clearTimeout(s.timer);live.delete(id);
    s.el.hidden=true;
    if(!silent)s.el.dispatchEvent(new CustomEvent('chat:typing-expired',{bubbles:true,detail:{id}}));
  }
  window.chatTyping={
    /* show(el, signalId): render the dots. The signal id is the transport's
       live typing event; there is no show() without one. */
    show(el,signalId){
      if(!signalId)throw new Error('chatTyping.show requires a live signal id — no fake typing');
      el.hidden=false;
      if(live.has(signalId))clearTimeout(live.get(signalId).timer);
      /* watchdog: 30s with no keep-alive and no message => honest dismissal */
      const timer=setTimeout(()=>dismiss(signalId),WATCHDOG_MS);
      live.set(signalId,{el,timer});
    },
    /* keepalive(signalId): the transport re-asserts while the user still types */
    keepalive(signalId){
      const s=live.get(signalId);if(!s)return;
      clearTimeout(s.timer);
      s.timer=setTimeout(()=>dismiss(signalId),WATCHDOG_MS);
    },
    /* arrived(signalId): the message landed — the dots are replaced by truth */
    arrived(signalId){dismiss(signalId,true);}
  };
  /* The transport calls keepalive at most every 20s; a signal older than that
     without re-assertion is stale and the next keepalive is ignored. */
})();
