document.querySelectorAll('.cal-month .cal-day').forEach(d=>{
  d.addEventListener('click',()=>{
    document.querySelectorAll('.cal-month .is-selected').forEach(x=>x.classList.remove('is-selected'));
    d.classList.add('is-selected');
  });
  d.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){e.preventDefault();d.click();} });
});
