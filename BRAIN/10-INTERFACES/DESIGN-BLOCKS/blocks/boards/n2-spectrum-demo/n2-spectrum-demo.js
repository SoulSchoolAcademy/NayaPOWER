/* Smart Block: n2-spectrum-demo — source behavior, byte-true */
document.getElementById('swatches').addEventListener('click',function(e){
  var b=e.target.closest('.sw');if(!b)return;
  document.getElementById('demoBoard').style.setProperty('--c',b.dataset.c);
  document.getElementById('demoName').textContent=b.dataset.name;
});
