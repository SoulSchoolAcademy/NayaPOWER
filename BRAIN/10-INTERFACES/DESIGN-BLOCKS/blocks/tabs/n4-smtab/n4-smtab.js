/* Smart Block: n4-smtab — source behavior, byte-true */
(function(){
  var row = document.getElementById('demo-smtabs');
  var status = document.getElementById('smtabs-status');
  if (!row || !status) return;
  var palette = ['#ed42c4','#8a5cff','#3ca8ff','#35e39b','#ffd45a'];
  var extra = 0;

  function activate(tab){
    var tabs = row.querySelectorAll('.smtab:not(.add)');
    for (var i = 0; i < tabs.length; i++) tabs[i].classList.remove('active');
    tab.classList.add('active');
  }

  row.addEventListener('click', function(e){
    var t = e.target;
    if (!t.closest) return;
    var tab = t.closest('.smtab');
    if (!tab || !row.contains(tab)) return;

    if (tab.classList.contains('add')){
      if (extra >= 4){
        status.textContent = 'Ribbon is full in this demo — ⋯ on a tab cycles its state: 💜 priority → ⭐ favorite → plain.';
        return;
      }
      extra++;
      var nt = document.createElement('button');
      nt.type = 'button';
      nt.className = 'smtab';
      nt.setAttribute('data-label', 'Favorite ' + extra);
      nt.style.setProperty('--tc', palette[(extra + 3) % palette.length]);
      nt.innerHTML = 'Favorite ' + extra + ' <span class="dots" aria-hidden="true">⋯</span>';
      row.insertBefore(nt, tab);
      activate(nt);
      status.textContent = 'Added "Favorite ' + extra + '" — in the real ribbon it saves and follows you to every page.';
      return;
    }

    var label = tab.getAttribute('data-label') || 'Tab';
    if (t.closest('.dots')){
      if (tab.classList.contains('heart')){
        tab.classList.remove('heart'); tab.classList.add('star');
        status.textContent = label + ' is now a ⭐ favorite.';
      } else if (tab.classList.contains('star')){
        tab.classList.remove('star');
        status.textContent = label + ' state cleared — plain tab again.';
      } else {
        tab.classList.add('heart');
        status.textContent = label + ' is now a 💜 priority.';
      }
      return;
    }

    activate(tab);
    status.textContent = 'Now showing: ' + label + ' — click navigates, ⋯ edits.';
  });
})();
