/* sp-topic-picker — chip multi-select toggle. Vanilla, no dependencies. */
(function(){
  document.querySelectorAll('.sp-topic').forEach(function(group){
    var chips = Array.prototype.slice.call(group.querySelectorAll('.sp-topic-chip'));
    function selected(){
      return chips.filter(function(c){ return c.classList.contains('on'); })
                  .map(function(c){ return c.dataset.topic || c.textContent.trim(); });
    }
    chips.forEach(function(chip){
      chip.setAttribute('aria-pressed', chip.classList.contains('on') ? 'true' : 'false');
      chip.addEventListener('click', function(){
        chip.classList.toggle('on');
        chip.setAttribute('aria-pressed', chip.classList.contains('on') ? 'true' : 'false');
        group.dispatchEvent(new CustomEvent('sp-topics-change', {
          bubbles: true,
          detail: { topics: selected() }
        }));
      });
    });
    group.spTopicPicker = { selected: selected };
  });
})();
