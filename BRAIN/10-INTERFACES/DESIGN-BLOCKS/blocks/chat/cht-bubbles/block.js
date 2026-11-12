/* The receipt contract. Your transport owns the truth; this is how the block
   displays it. setReceipt(el, state) is the ONLY writer of data-state. */
(function(){
  const ORDER=['sending','sent','delivered','read'];
  window.chatReceipt=function(el,state){
    if(!ORDER.includes(state))return;
    el.setAttribute('data-state',state);
    const sr=el.querySelector('.sr');if(sr)sr.textContent=state[0].toUpperCase()+state.slice(1);
    el.setAttribute('aria-label',state[0].toUpperCase()+state.slice(1));
  };
  /* Grouping rule, enforced by the renderer: same sender AND <5 min apart
     gets .grp; the first of the run gets .grp-first. A renderer that can't
     decide groups renders every row ungrouped — never a wrong group. */
})();
