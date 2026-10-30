/* Specimen toggling is local. A live build re-renders counts from the server
   after each toggle lands — it never invents a number mid-flight. */
(function(){
  const wrap=document.querySelector('.rx-wrap'),add=wrap.querySelector('.rx-add'),pop=wrap.querySelector('.rx-pop');
  add.addEventListener('click',()=>{
    const open=add.getAttribute('aria-expanded')==='true';
    add.setAttribute('aria-expanded',String(!open));pop.hidden=open;
    if(!open)pop.querySelector('.rx').focus();
  });
  document.addEventListener('click',e=>{
    if(!pop.hidden&&!e.target.closest('.rx-wrap')){pop.hidden=true;add.setAttribute('aria-expanded','false');}
  });
  const order=['love','celebrate','thoughtful','agree','laugh'];
  pop.querySelectorAll('.rx').forEach(choice=>{
    choice.addEventListener('click',()=>{
      const key=choice.getAttribute('data-rx');
      const row=wrap.querySelector('.cmt-rx');
      let existing=row.querySelector(':scope > .rx[data-rx="'+key+'"]');
      if(existing){
        if(existing.getAttribute('aria-pressed')!=='true')existing.click();
      }else{
        const pill=choice.cloneNode(true);
        pill.removeAttribute('role');
        pill.classList.add('is-mine');
        pill.setAttribute('aria-pressed','true');
        const label=choice.getAttribute('title');
        pill.setAttribute('title',label+' — you reacted');
        const count=document.createElement('b');count.textContent='1';pill.appendChild(count);
        const sr=document.createElement('span');sr.hidden=true;sr.textContent=label;pill.appendChild(sr);
        const addBtn=row.querySelector('.rx-add');
        const later=[...row.querySelectorAll(':scope > .rx[data-rx]')]
          .find(p=>order.indexOf(p.getAttribute('data-rx'))>order.indexOf(key));
        row.insertBefore(pill,later||addBtn);
      }
      pop.hidden=true;add.setAttribute('aria-expanded','false');add.focus();
    });
  });
  wrap.querySelectorAll('.cmt-rx > .rx').forEach(pill=>{
    pill.addEventListener('click',()=>{
      const on=pill.classList.toggle('is-mine');
      pill.setAttribute('aria-pressed',String(on));
      const b=pill.querySelector('b'),n=parseInt(b.textContent,10);
      b.textContent=String(Math.max(0,n+(on?1:-1)));
    });
  });
})();
