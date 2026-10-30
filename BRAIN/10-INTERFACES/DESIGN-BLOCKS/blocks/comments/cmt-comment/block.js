(function(){
  const btn=document.querySelector('.cmt-morebtn'),body=document.getElementById('cmtBody1');
  btn.addEventListener('click',()=>{
    const open=btn.getAttribute('aria-expanded')==='true';
    btn.setAttribute('aria-expanded',String(!open));
    body.classList.toggle('is-clamped',open);
    btn.textContent=open?'Show more':'Show less';
  });
})();
