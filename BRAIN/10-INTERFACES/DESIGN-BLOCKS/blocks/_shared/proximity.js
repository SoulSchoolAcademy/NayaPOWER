/* Optional page-level enhancement from Naya Building Blocks - The Ultimate Design System - Naya 2.html.
   Drives [data-aware] proximity lighting (cursor sheen) on hover-capable pointers.
   Components work without it; include for the full living-depth effect. */
(function(){
  var aware=Array.prototype.slice.call(document.querySelectorAll('[data-aware]'));
  var hoverable=window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  if(hoverable){
    document.addEventListener('pointermove',function(e){
      aware.forEach(function(el){
        var r=el.getBoundingClientRect();
        var cx=r.left+r.width/2,cy=r.top+r.height/2;
        var d=Math.hypot(e.clientX-cx,e.clientY-cy);
        var near=Math.max(0,1-d/170);
        el.style.setProperty('--px',((e.clientX-r.left)/r.width*100)+'%');
        el.style.setProperty('--py',((e.clientY-r.top)/r.height*100)+'%');
        el.style.setProperty('--near-scale',(1+near*.006).toFixed(3));
      });
    },{passive:true});
  }
  document.querySelectorAll('.segmented button').forEach(function(btn){btn.addEventListener('click',function(){var group=btn.parentElement;group.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-selected',b===btn?'true':'false')})})});
  var roomHeads={Today:'Your day, already understood.',Reports:'Evidence, made useful.','Smart Spaces':'Think together without losing the lesson.','Smart Mail':'Messages with meaning, not more noise.','Smart Ledger':'Truth has a visible trail.'};
  document.querySelectorAll('.app-nav button').forEach(function(btn){btn.addEventListener('click',function(){document.querySelectorAll('.app-nav button').forEach(function(b){b.setAttribute('aria-selected',b===btn?'true':'false')});document.getElementById('room-title').textContent=btn.dataset.room;document.getElementById('room-head').textContent=roomHeads[btn.dataset.room];document.getElementById('room-copy').textContent=btn.dataset.copy})});
  document.querySelectorAll('.smarttab').forEach(function(btn){btn.addEventListener('click',function(){document.querySelectorAll('.smarttab').forEach(function(b){b.setAttribute('aria-selected',b===btn?'true':'false')});document.getElementById('tab-title').textContent=btn.textContent.trim();document.getElementById('tab-copy').textContent=btn.dataset.tabCopy})});
  document.querySelector('[data-login-preview]').addEventListener('click',function(){showToast('Authentication presentation only · no sign-in sent')});
  var toast=document.getElementById('toast'),timer;
  function showToast(msg){toast.textContent=msg;toast.classList.add('show');clearTimeout(timer);timer=setTimeout(function(){toast.classList.remove('show')},1800)}
  document.querySelectorAll('[data-copy-target]').forEach(function(btn){btn.addEventListener('click',function(){var text=document.getElementById(btn.dataset.copyTarget).innerText;navigator.clipboard.writeText(text).then(function(){showToast('Button recipe copied')}).catch(function(){showToast('Select the recipe to copy')})})});
  document.querySelectorAll('.naya-toggle').forEach(function(toggle){toggle.addEventListener('click',function(){toggle.setAttribute('aria-checked',toggle.getAttribute('aria-checked')==='true'?'false':'true')})});
})();
