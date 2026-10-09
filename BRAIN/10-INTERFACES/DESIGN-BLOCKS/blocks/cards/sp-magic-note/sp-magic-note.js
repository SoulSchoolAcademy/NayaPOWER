/* sp-magic-note — accept / edit / save / cancel behaviors. Vanilla, no dependencies. */
(function(){
  document.querySelectorAll('.sp-mnote').forEach(function(card){
    var text = card.querySelector('.sp-mnote-text');
    var edit = card.querySelector('.sp-mnote-edit');
    var acceptBtn = card.querySelector('[data-mnote="accept"]');
    var editBtn = card.querySelector('[data-mnote="edit"]');
    var saveBtn = card.querySelector('[data-mnote="save"]');
    var cancelBtn = card.querySelector('[data-mnote="cancel"]');

    function announce(detail){
      card.dispatchEvent(new CustomEvent('sp-mnote', { bubbles: true, detail: detail }));
    }
    function showEditing(editing){
      card.classList.toggle('is-editing', editing);
      if(editing){
        edit.value = text.textContent.replace(/^["“]|["”]$/g, '').trim();
        edit.focus();
      }
      editBtn.style.display = editing ? 'none' : '';
      acceptBtn.style.display = editing ? 'none' : '';
      saveBtn.style.display = editing ? '' : 'none';
      cancelBtn.style.display = editing ? '' : 'none';
    }
    acceptBtn.addEventListener('click', function(){
      card.classList.add('is-done');
      announce({ action: 'accept', text: text.textContent.trim() });
    });
    editBtn.addEventListener('click', function(){ showEditing(true); });
    cancelBtn.addEventListener('click', function(){ showEditing(false); });
    saveBtn.addEventListener('click', function(){
      var v = edit.value.trim();
      if(v) text.textContent = '\u201C' + v + '\u201D';
      showEditing(false);
      announce({ action: 'save', text: text.textContent.trim() });
    });
  });
})();
