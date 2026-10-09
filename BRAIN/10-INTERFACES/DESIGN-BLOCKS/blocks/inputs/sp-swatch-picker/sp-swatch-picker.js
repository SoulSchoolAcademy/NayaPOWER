/* sp-swatch-picker — single-select swatch radiogroup. Vanilla, no dependencies. */
(function(){
  document.querySelectorAll('.sp-swatch').forEach(function(group){
    var swatches = Array.prototype.slice.call(group.querySelectorAll('.sp-swatch-s'));
    function selected(){
      var on = swatches.find(function(s){ return s.classList.contains('on'); });
      return on ? (on.dataset.swatch || getComputedStyle(on).getPropertyValue('--sw').trim()) : null;
    }
    swatches.forEach(function(sw, i){
      sw.setAttribute('role', 'radio');
      sw.setAttribute('tabindex', sw.classList.contains('on') ? '0' : '-1');
      sw.setAttribute('aria-checked', sw.classList.contains('on') ? 'true' : 'false');
      function choose(){
        swatches.forEach(function(s){
          s.classList.remove('on');
          s.setAttribute('aria-checked', 'false');
          s.setAttribute('tabindex', '-1');
        });
        sw.classList.add('on');
        sw.setAttribute('aria-checked', 'true');
        sw.setAttribute('tabindex', '0');
        group.dispatchEvent(new CustomEvent('sp-swatch-change', {
          bubbles: true,
          detail: { swatch: sw.dataset.swatch || getComputedStyle(sw).getPropertyValue('--sw').trim() }
        }));
      }
      sw.addEventListener('click', choose);
      sw.addEventListener('keydown', function(e){
        var j = null;
        if(e.key === 'ArrowRight' || e.key === 'ArrowDown') j = (i + 1) % swatches.length;
        else if(e.key === 'ArrowLeft' || e.key === 'ArrowUp') j = (i - 1 + swatches.length) % swatches.length;
        else if(e.key === ' ' || e.key === 'Enter'){ e.preventDefault(); choose(); return; }
        else return;
        e.preventDefault();
        swatches[j].focus();
        swatches[j].click();
      });
    });
    group.spSwatchPicker = { selected: selected };
  });
})();
