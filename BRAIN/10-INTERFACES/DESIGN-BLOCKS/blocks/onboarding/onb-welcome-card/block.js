(function(){
  const card=document.getElementById('onbWelcome');
  const name=(card.dataset.name||'').trim();
  if(name){card.querySelector('[data-onb-name]').textContent=', '+name;}
})();
