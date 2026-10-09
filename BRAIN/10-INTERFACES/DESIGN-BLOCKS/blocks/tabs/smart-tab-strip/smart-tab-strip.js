/* smart-tab-strip.js — auto-initializes every .smart-tab-strip on the page.
   - positions the sliding indicator under the selected tab (transform translateX/scaleX)
   - roving tabindex; ArrowLeft/ArrowRight/Home/End move focus, Enter/Space activate
   - recomputes the indicator on resize (ResizeObserver + window resize + fonts.ready)
   Markup contract:
     <div class="smart-tab-strip">
       <div class="smart-tab-scroll">
         <div class="smart-tab-list" role="tablist" aria-label="...">
           <button class="smart-tab" role="tab" aria-selected="true|false">…</button>
           <span class="smart-tab-indicator" aria-hidden="true"></span>
         </div>
       </div>
       <button class="smart-tab-add" type="button" aria-label="Add tab">+</button>
     </div> */
(function () {
  'use strict';

  var INDICATOR_BASE = 32; // must match .smart-tab-indicator width in CSS
  var reduceMotion = false;
  try {
    reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (err) { /* matchMedia unavailable — keep smooth default */ }

  function tabsOf(list) {
    return Array.prototype.slice.call(list.querySelectorAll('.smart-tab'));
  }

  function stripOf(list) {
    return list.closest ? list.closest('.smart-tab-strip') : null;
  }

  function moveIndicator(list) {
    var strip = stripOf(list);
    if (!strip) return;
    var indicator = list.querySelector('.smart-tab-indicator');
    if (!indicator) return;
    var tabs = tabsOf(list);
    if (!tabs.length) return;
    var active = list.querySelector('.smart-tab[aria-selected="true"]') || tabs[0];
    var x = active.offsetLeft;
    var w = active.offsetWidth;
    if (reduceMotion) {
      var prev = indicator.style.transition;
      indicator.style.transition = 'none';
      indicator.style.transform = 'translateX(' + x + 'px) scaleX(' + (w / INDICATOR_BASE) + ')';
      void indicator.offsetWidth; /* force reflow so the snap is committed */
      indicator.style.transition = prev;
    } else {
      indicator.style.transform = 'translateX(' + x + 'px) scaleX(' + (w / INDICATOR_BASE) + ')';
    }
  }

  function selectTab(list, tab, moveFocus) {
    tabsOf(list).forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
    });
    moveIndicator(list);
    tab.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: reduceMotion ? 'auto' : 'smooth' });
    if (moveFocus) tab.focus();
  }

  function focusTab(list, index) {
    var tabs = tabsOf(list);
    if (!tabs.length) return;
    var i = ((index % tabs.length) + tabs.length) % tabs.length; /* wrap */
    tabs[i].focus();
  }

  function initStrip(strip) {
    var list = strip.querySelector('.smart-tab-list');
    if (!list) return;

    /* create the indicator if the author omitted it */
    if (!list.querySelector('.smart-tab-indicator')) {
      var ind = document.createElement('span');
      ind.className = 'smart-tab-indicator';
      ind.setAttribute('aria-hidden', 'true');
      list.appendChild(ind);
    }

    /* roving tabindex: exactly one tab in the tab order */
    var tabs = tabsOf(list);
    var selected = list.querySelector('.smart-tab[aria-selected="true"]');
    if (!selected && tabs.length) {
      selected = tabs[0];
      selected.setAttribute('aria-selected', 'true');
    }
    tabs.forEach(function (t) {
      t.tabIndex = (t === selected) ? 0 : -1;
    });

    /* activation */
    list.addEventListener('click', function (e) {
      var tab = e.target && e.target.closest ? e.target.closest('.smart-tab') : null;
      if (!tab || !list.contains(tab)) return;
      selectTab(list, tab, false);
    });

    /* keyboard: arrows/Home/End move focus; Enter/Space activate natively */
    list.addEventListener('keydown', function (e) {
      var tab = e.target && e.target.closest ? e.target.closest('.smart-tab') : null;
      if (!tab || !list.contains(tab)) return;
      var tabs = tabsOf(list);
      var i = tabs.indexOf(tab);
      switch (e.key) {
        case 'ArrowRight':
          e.preventDefault();
          focusTab(list, i + 1);
          break;
        case 'ArrowLeft':
          e.preventDefault();
          focusTab(list, i - 1);
          break;
        case 'Home':
          e.preventDefault();
          focusTab(list, 0);
          break;
        case 'End':
          e.preventDefault();
          focusTab(list, tabs.length - 1);
          break;
        default:
          break;
      }
    });

    /* keep the indicator honest as geometry changes */
    if ('ResizeObserver' in window) {
      var ro = new ResizeObserver(function () { moveIndicator(list); });
      ro.observe(list);
    }
    window.addEventListener('resize', function () { moveIndicator(list); });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () { moveIndicator(list); });
    }

    /* initial position after layout settles */
    window.requestAnimationFrame(function () { moveIndicator(list); });
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('.smart-tab-strip'), initStrip);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
