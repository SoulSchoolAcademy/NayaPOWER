(function(){
  const rail=document.getElementById('onbRail');
  if(!rail||rail.classList.contains('is-empty'))return;
  const steps=[...rail.querySelectorAll('.onb-step')];
  const fill=rail.querySelector('.onb-fill');
  const check='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function state(i,cur){return i<cur?'done':(i===cur?'current':'locked');}
  function render(){
    const cur=steps.findIndex(s=>s.classList.contains('is-current'));
    fill.style.width=(cur/(steps.length-1)*100)+'%';
    steps.forEach((s,i)=>{
      const st=state(i,cur),b=s.querySelector('.onb-node'),title=s.querySelector('.t').textContent;
      s.classList.toggle('is-done',st==='done');
      s.classList.toggle('is-current',st==='current');
      s.classList.toggle('is-locked',st==='locked');
      b.disabled=(st==='locked');
      if(st==='locked')b.setAttribute('aria-disabled','true');else b.removeAttribute('aria-disabled');
      b.querySelector('.in').innerHTML=(st==='done')?check:String(i+1);
      b.setAttribute('aria-label','Step '+(i+1)+' '+st+': '+title);
      s.querySelector('.s').textContent=st==='done'?'Done':(st==='current'?'You are here':'Locked');
      if(st==='current')s.setAttribute('aria-current','step');else s.removeAttribute('aria-current');
    });
  }
  steps.forEach((s,i)=>{
    s.querySelector('.onb-node').addEventListener('click',()=>{
      const cur=steps.findIndex(x=>x.classList.contains('is-current'));
      if(i<=cur){steps[cur].classList.remove('is-current');steps[i].classList.add('is-current');render();}
    });
  });
  render();
})();
