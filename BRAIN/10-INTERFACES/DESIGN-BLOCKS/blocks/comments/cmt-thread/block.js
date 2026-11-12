/* Specimen behavior is local. A live build posts through your API and renders
   the server's receipt (real id, real timestamp) — it never claims a local
   append reached anyone. */
(function(){
  const box=document.getElementById('cmtBox'),post=document.getElementById('cmtPost');
  box.addEventListener('input',()=>{post.disabled=!box.value.trim();});
  document.querySelectorAll('.cmt-chev').forEach(chev=>{
    chev.addEventListener('click',()=>{
      const main=chev.closest('.cmt-main');
      const kids=main?main.querySelector(':scope > .cmt-kids'):null;
      const open=chev.getAttribute('aria-expanded')==='true';
      chev.setAttribute('aria-expanded',String(!open));
      if(kids)kids.hidden=open;
      const base=chev.getAttribute('aria-label').replace(/^(Expand|Collapse) /,'');
      chev.setAttribute('aria-label',(open?'Expand ':'Collapse ')+base);
    });
  });
  document.querySelectorAll('.cmt-more').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const deep=btn.nextElementSibling,open=btn.getAttribute('aria-expanded')==='true';
      btn.setAttribute('aria-expanded',String(!open));deep.hidden=open;
    });
  });
  document.querySelectorAll('.cmt-act.cmt-love').forEach(love=>{
    love.addEventListener('click',()=>{
      const on=love.classList.toggle('is-on');
      love.setAttribute('aria-pressed',String(on));
    });
  });
})();
