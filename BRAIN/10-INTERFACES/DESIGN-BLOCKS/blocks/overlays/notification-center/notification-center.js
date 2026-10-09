/* Smart Block: notification-center — open/close + read-state wiring */

(function () {
  document.querySelectorAll('.nc').forEach(function (panel) {
    var backdrop = document.querySelector('.nc-backdrop');
    var openers = document.querySelectorAll('[data-nc-open]');
    var closers = panel.querySelectorAll('[data-nc-close]');

    function open() {
      panel.classList.add('is-on');
      if (backdrop) backdrop.classList.add('is-on');
      document.body.style.overflow = 'hidden';
    }
    function close() {
      panel.classList.remove('is-on');
      if (backdrop) backdrop.classList.remove('is-on');
      document.body.style.overflow = '';
      panel.dispatchEvent(new CustomEvent('nc:closed', { bubbles: true }));
    }

    openers.forEach(function (b) { b.addEventListener('click', open); });
    closers.forEach(function (b) { b.addEventListener('click', close); });
    if (backdrop) backdrop.addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('is-on')) close();
    });

    // Mark read on click
    panel.querySelectorAll('.nc-item.is-unread').forEach(function (item) {
      item.addEventListener('click', function () {
        item.classList.remove('is-unread');
        updateCount();
        panel.dispatchEvent(new CustomEvent('nc:read', { bubbles: true, detail: { id: item.dataset.id } }));
      }, { once: true });
    });

    function updateCount() {
      var n = panel.querySelectorAll('.nc-item.is-unread').length;
      panel.querySelectorAll('.nc-count').forEach(function (c) {
        c.textContent = n;
        c.style.display = n ? '' : 'none';
      });
    }
    updateCount();
  });
})();
