(function(){
  const trig=document.getElementById('dpTrig'),drop=document.getElementById('dpDrop'),
        grid=document.getElementById('dpGrid'),label=document.getElementById('dpLabel');
  const YEAR=2026,MONTH=9,TODAY=16; /* October 2026; live build derives from the clock */
  const firstDow=(new Date(YEAR,MONTH,1).getDay()+6)%7; /* Monday-first */
  for(let i=0;i<firstDow;i++){const s=document.createElement('span');grid.appendChild(s);}
  let focusIdx=-1;const btns=[];
  for(let d=1;d<=31;d++){
    const b=document.createElement('button');
    b.textContent=d;b.setAttribute('role','gridcell');
    const iso=`${YEAR}-${String(MONTH+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    b.dataset.iso=iso;
    if(d===TODAY){b.classList.add('is-todayd');b.setAttribute('aria-label',`October ${d}, today`);}
    if(d<TODAY){b.disabled=true;b.setAttribute('aria-disabled','true');b.tabIndex=-1;
      b.setAttribute('aria-label',`October ${d}, in the past`);}
    b.addEventListener('click',()=>choose(b));
    grid.appendChild(b);btns.push(b);
  }
  function choose(b){
    btns.forEach(x=>x.classList.remove('is-chosen'));b.classList.add('is-chosen');
    const d=+b.textContent;
    label.textContent=`${['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][MONTH]} ${d}, ${YEAR}`;
    label.classList.remove('ph');trig.dataset.value=b.dataset.iso;close();
    trig.focus();
  }
  function open(){drop.hidden=false;trig.setAttribute('aria-expanded','true');
    const t=btns.find(b=>b.classList.contains('is-chosen'))||btns.find(b=>!b.disabled);if(t)t.focus();}
  function close(){drop.hidden=true;trig.setAttribute('aria-expanded','false');}
  trig.addEventListener('click',()=>drop.hidden?open():close());
  document.addEventListener('click',e=>{if(!drop.hidden&&!e.target.closest('.cal-pick'))close();});
  document.addEventListener('keydown',e=>{
    if(drop.hidden)return;
    const live=btns.filter(b=>!b.disabled);
    const cur=live.indexOf(document.activeElement);
    if(e.key==='Escape'){close();trig.focus();}
    else if(e.key==='ArrowRight'){e.preventDefault();(live[cur+1]||live[0]).focus();}
    else if(e.key==='ArrowLeft'){e.preventDefault();(live[cur-1]||live[live.length-1]).focus();}
    else if(e.key==='ArrowDown'){e.preventDefault();(live[cur+7]||live[live.length-1]).focus();}
    else if(e.key==='ArrowUp'){e.preventDefault();(live[cur-7]||live[0]).focus();}
    else if(e.key==='Enter'&&document.activeElement.dataset.iso){choose(document.activeElement);}
  });
})();
