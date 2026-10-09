/* sp-modal-type — single-select type options, close behaviors, focus handling. Vanilla. */
(function(){
  document.querySelectorAll('.sp-mback').forEach(function(back){
    var modal = back.querySelector('.sp-mtype');
    var options = Array.prototype.slice.call(back.querySelectorAll('.sp-mtype-opt'));
    var lastFocus = null;

    function selected(){
      return options.find(function(o){ return o.classList.contains('on'); });
    }
    options.forEach(function(opt, i){
      opt.setAttribute('role', 'radio');
      opt.setAttribute('tabindex', '0');
      opt.setAttribute('aria-checked', opt.classList.contains('on') ? 'true' : 'false');
      function choose(){
        options.forEach(function(o){
          o.classList.remove('on');
          o.setAttribute('aria-checked', 'false');
        });
        opt.classList.add('on');
        opt.setAttribute('aria-checked', 'true');
        modal.dispatchEvent(new CustomEvent('sp-type-change', {
          bubbles: true,
          detail: { type: opt.dataset.type || opt.querySelector('.sp-mtype-name').textContent.trim().toLowerCase() }
        }));
      }
      opt.addEventListener('click', choose);
      opt.addEventListener('keydown', function(e){
        if(e.key === ' ' || e.key === 'Enter'){ e.preventDefault(); choose(); }
        if(e.key === 'ArrowDown' || e.key === 'ArrowRight'){
          e.preventDefault();
          var n = options[(i + 1) % options.length]; n.focus(); n.click();
        }
        if(e.key === 'ArrowUp' || e.key === 'ArrowLeft'){
          e.preventDefault();
          var p = options[(i - 1 + options.length) % options.length]; p.focus(); p.click();
        }
      });
    });

    function open(){
      lastFocus = document.activeElement;
      back.classList.add('open');
      document.body.style.overflow = 'hidden';
      var first = selected() || options[0];
      if(first) first.focus();
    }
    function close(){
      back.classList.remove('open');
      document.body.style.overflow = '';
      if(lastFocus && lastFocus.focus) lastFocus.focus();
    }
    back.querySelectorAll('[data-sp-close]').forEach(function(el){
      el.addEventListener('click', close);
    });
    back.addEventListener('mousedown', function(e){
      if(e.target === back) close();
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && back.classList.contains('open')) close();
    });
    back.spModalType = { open: open, close: close, selected: selected };
  });
})();
