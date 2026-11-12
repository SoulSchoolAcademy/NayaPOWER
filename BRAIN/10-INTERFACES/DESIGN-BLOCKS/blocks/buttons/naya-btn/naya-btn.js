/* Smart Block JS: naya-btn
 * Source: Naya_4_Design_Element_Set.html
 */

(function(){
  // Foundation specimens are canonical .naya-btn toggles: selection only.
  // Sheen, Aware proximity, Ignited hover and press all come from the
  // shared .naya-btn library behaviour below — one system, no forks.
  var status = document.getElementById('foundation-status');
  var btns = document.querySelectorAll('.trinity .naya-btn');
  if (!btns.length) return;
  btns.forEach(function(btn){
    btn.addEventListener('click', function(){
      btns.forEach(function(b){ b.setAttribute('aria-pressed','false'); });
      btn.setAttribute('aria-pressed','true');
      if (status) status.textContent = btn.getAttribute('data-message') || '';
    });
  });
})();

/* ---- */

(function(){
  // Naya Button Library — proximity awareness (Aware state)
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var btns = Array.prototype.slice.call(document.querySelectorAll('.naya-btn'));
  if (!btns.length) return;
  var raf = null, lastX = 0, lastY = 0;
  function update(){
    raf = null;
    for (var i = 0; i < btns.length; i++){
      var b = btns[i];
      if (b.disabled) continue;
      var r = b.getBoundingClientRect();
      if (r.bottom < -160 || r.top > window.innerHeight + 160) { b.classList.remove('is-aware'); continue; }
      var dx = Math.max(r.left - lastX, 0, lastX - r.right);
      var dy = Math.max(r.top - lastY, 0, lastY - r.bottom);
      var dist = Math.sqrt(dx*dx + dy*dy);
      var aware = dist < 140;
      if (aware !== b.classList.contains('is-aware')) b.classList.toggle('is-aware', aware);
      if (aware || b.matches(':hover')){
        var mx = ((lastX - r.left) / Math.max(r.width,1) * 100);
        var my = ((lastY - r.top) / Math.max(r.height,1) * 100);
        b.style.setProperty('--mx', mx + '%');
        b.style.setProperty('--my', my + '%');
      }
    }
  }
  document.addEventListener('pointermove', function(e){
    lastX = e.clientX; lastY = e.clientY;
    if (!raf) raf = requestAnimationFrame(update);
  }, { passive: true });
  document.addEventListener('pointerleave', function(){
    btns.forEach(function(b){ b.classList.remove('is-aware'); });
  });
  // Touch: brief aware flash on touchstart for tactile feedback
  btns.forEach(function(b){
    b.addEventListener('touchstart', function(){ b.classList.add('is-aware'); }, { passive: true });
  });
})();