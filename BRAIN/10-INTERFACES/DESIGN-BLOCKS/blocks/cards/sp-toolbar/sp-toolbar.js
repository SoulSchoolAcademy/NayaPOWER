/* sp-toolbar — view switcher radio behavior. Vanilla, no dependencies. */
(function(){
  document.querySelectorAll('.sp-tb-views').forEach(function(group){
    var views = Array.prototype.slice.call(group.querySelectorAll('.sp-tb-view'));
    views.forEach(function(view, i){
      view.setAttribute('role', 'tab');
      view.setAttribute('aria-selected', view.classList.contains('on') ? 'true' : 'false');
      view.addEventListener('click', function(){
        views.forEach(function(v){
          v.classList.remove('on');
          v.setAttribute('aria-selected', 'false');
        });
        view.classList.add('on');
        view.setAttribute('aria-selected', 'true');
        group.dispatchEvent(new CustomEvent('sp-view-change', {
          bubbles: true,
          detail: { view: view.dataset.view || view.textContent.trim().toLowerCase() }
        }));
      });
      view.addEventListener('keydown', function(e){
        var j = i;
        if(e.key === 'ArrowRight') j = (i + 1) % views.length;
        else if(e.key === 'ArrowLeft') j = (i - 1 + views.length) % views.length;
        else return;
        e.preventDefault();
        views[j].focus();
        views[j].click();
      });
    });
  });
})();
