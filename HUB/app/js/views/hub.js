/* ═══════════════════════════════════════════════════════════════════
   HUB SHELL — TWO CORNER CONTROLS, TWO DRAWERS, ONE MAIN SHOW.
   The Feed is home/the Main Show, never a room entry in the drawer.
   Navigation recedes until requested. Every visible control has a real
   destination or consequence.
   ═══════════════════════════════════════════════════════════════════ */

function HubView(params) {
  const { el, Icons } = window.NayaUI;
  const R = window.NayaRuntime;
  const activeRoom = params.room || 'feed';
  const room = R.ROOMS.find(r => r.id === activeRoom) || R.ROOMS[0];
  const isMainShow = room.id === 'feed';

  const shell = el('div', 'shell');

  const top = el('header', 'topbar');

  const leftBtn = el('button', 'corner-btn corner-left', Icons.icon('menu'));
  leftBtn.type = 'button';
  leftBtn.setAttribute('aria-label', 'Open room navigation');
  leftBtn.setAttribute('aria-expanded', 'false');
  leftBtn.setAttribute('aria-controls', 'hub-room-drawer');

  const brand = el(
    'button',
    'brand-mark',
    '<img class="brand-img" src="assets/nayanet-logo.png" alt=""><span><b>NAYANET</b><small>INTELLIGENT HUB</small></span>'
  );
  brand.type = 'button';
  brand.setAttribute('aria-label', 'NayaNET — return to the Main Show');
  brand.addEventListener('click', () => {
    closeDrawers();
    window.NayaRouter.navigate('/hub/feed');
  });

  const rightBtn = el('button', 'corner-btn corner-right', Icons.icon('grid'));
  rightBtn.type = 'button';
  rightBtn.setAttribute('aria-label', 'Open product navigation');
  rightBtn.setAttribute('aria-expanded', 'false');
  rightBtn.setAttribute('aria-controls', 'hub-product-drawer');

  top.append(leftBtn, brand, rightBtn);

  const leftDrawer = el('nav', 'drawer drawer-left');
  leftDrawer.id = 'hub-room-drawer';
  leftDrawer.setAttribute('aria-label', 'Hub rooms');
  leftDrawer.setAttribute('aria-hidden', 'true');
  leftDrawer.appendChild(el('p', 'drawer-kicker', 'ROOMS'));

  R.ROOMS.filter(r => r.id !== 'feed').forEach(r => {
    const b = el('button', 'drawer-btn' + (r.id === room.id ? ' active' : ''));
    b.type = 'button';
    b.style.setProperty('--nav', r.accent);
    b.innerHTML = '<span class="ico">' + Icons.icon(r.icon) + '</span><span>' + r.name + '</span>';
    if (r.id === room.id) b.setAttribute('aria-current', 'page');
    b.addEventListener('click', () => {
      closeDrawers();
      window.NayaRouter.navigate('/hub/' + r.id);
    });
    leftDrawer.appendChild(b);
  });

  const privacy = el(
    'div',
    'drawer-privacy',
    'PRIVATE BY DEFAULT.<br>SHARED BY CHOICE.<br>COLLECTIVE BY CONSENT.'
  );
  leftDrawer.appendChild(privacy);

  const PRODUCT_LINKS = [
    { name: 'HOME', href: 'https://hmclibrary.groovemember.net/home' },
    { name: 'NAYA POWER', href: 'https://academy.nayanet.app/' },
    { name: '5-DAY CHALLENGE', href: 'https://academy.nayanet.app/' },
    { name: 'ENTER FREE', href: 'https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab' },
    { name: 'POWERCAST', href: '../powercast-player.html' },
    { name: 'WHITE PAPER', href: 'https://nayanet.groovepages.com/whitepaper' },
    { name: 'ABOUT US', href: 'https://nayanet.groovepages.com/aboutus' },
    { name: 'LOGIN', href: 'https://hmclibrary.groovemember.net/login' }
  ];

  const rightDrawer = el('nav', 'drawer drawer-right');
  rightDrawer.id = 'hub-product-drawer';
  rightDrawer.setAttribute('aria-label', 'Product navigation');
  rightDrawer.setAttribute('aria-hidden', 'true');
  rightDrawer.appendChild(el('p', 'drawer-kicker', 'NAYANET'));

  PRODUCT_LINKS.forEach(item => {
    const a = el('a', 'drawer-btn product-btn', '<span>' + item.name + '</span>');
    a.href = item.href;
    a.addEventListener('click', closeDrawers);
    rightDrawer.appendChild(a);
  });

  const backdrop = el('div', 'drawer-backdrop');
  backdrop.setAttribute('aria-hidden', 'true');
  backdrop.addEventListener('click', closeDrawers);

  let lastFocus = null;

  function activeDrawer() {
    if (shell.dataset.drawer === 'left') return leftDrawer;
    if (shell.dataset.drawer === 'right') return rightDrawer;
    return null;
  }

  function openDrawer(which) {
    lastFocus = document.activeElement;
    shell.dataset.drawer = which;
    document.body.classList.add('drawer-open');
    leftBtn.setAttribute('aria-expanded', which === 'left' ? 'true' : 'false');
    rightBtn.setAttribute('aria-expanded', which === 'right' ? 'true' : 'false');
    leftDrawer.setAttribute('aria-hidden', which === 'left' ? 'false' : 'true');
    rightDrawer.setAttribute('aria-hidden', which === 'right' ? 'false' : 'true');
    backdrop.setAttribute('aria-hidden', 'false');
    const drawer = activeDrawer();
    const first = drawer && drawer.querySelector('.drawer-btn');
    if (first) first.focus();
  }

  function closeDrawers() {
    if (!shell.dataset.drawer) return;
    delete shell.dataset.drawer;
    document.body.classList.remove('drawer-open');
    leftBtn.setAttribute('aria-expanded', 'false');
    rightBtn.setAttribute('aria-expanded', 'false');
    leftDrawer.setAttribute('aria-hidden', 'true');
    rightDrawer.setAttribute('aria-hidden', 'true');
    backdrop.setAttribute('aria-hidden', 'true');
    if (lastFocus && lastFocus.focus) {
      try { lastFocus.focus(); } catch (_) {}
    }
    lastFocus = null;
  }

  function toggleDrawer(which) {
    if (shell.dataset.drawer === which) closeDrawers();
    else openDrawer(which);
  }

  function trapFocus(event) {
    const drawer = activeDrawer();
    if (!drawer || event.key !== 'Tab') return;
    const focusables = [...drawer.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')]
      .filter(node => node.getClientRects().length);
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  leftBtn.addEventListener('click', () => toggleDrawer('left'));
  rightBtn.addEventListener('click', () => toggleDrawer('right'));
  shell.addEventListener('keydown', event => {
    if (event.key === 'Escape' && shell.dataset.drawer) {
      event.preventDefault();
      closeDrawers();
      return;
    }
    trapFocus(event);
  });

  function modeZone() {
    const zone=el('div','mode-zone');
    zone.setAttribute('role','tablist');
    zone.setAttribute('aria-label','Intelligence mode');

    const label=el('span','mode-zone-label','SHOWING');
    zone.appendChild(label);

    R.MODES.forEach(mode=>{
      const active=R.mode===mode.id;
      const button=el('button','mode-btn'+(active?' active':''));
      button.type='button';
      button.dataset.mode=mode.id;
      button.style.setProperty('--mode-accent',mode.accent);
      button.setAttribute('role','tab');
      button.setAttribute('aria-selected',active?'true':'false');
      button.setAttribute('tabindex',active?'0':'-1');
      button.innerHTML='<span class="mode-name">'+mode.name+'</span><span class="mode-hint">'+mode.hint+'</span>';
      button.setAttribute('aria-label',mode.name+' mode — '+mode.desc);

      const activate=()=>{
        if(R.mode===mode.id) return;
        R.setMode(mode.id);
        window.NayaRouter.render();
        requestAnimationFrame(()=>{
          const current=document.querySelector('.mode-btn.active');
          if(current) current.focus({preventScroll:true});
        });
      };

      button.addEventListener('click',activate);
      button.addEventListener('keydown',event=>{
        if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
        event.preventDefault();
        const buttons=[...zone.querySelectorAll('.mode-btn')];
        const index=buttons.indexOf(button);
        let next=index;
        if(event.key==='ArrowLeft') next=(index-1+buttons.length)%buttons.length;
        if(event.key==='ArrowRight') next=(index+1)%buttons.length;
        if(event.key==='Home') next=0;
        if(event.key==='End') next=buttons.length-1;
        buttons[next].focus();
        buttons[next].click();
      });
      zone.appendChild(button);
    });
    return zone;
  }

  const main = el('main', 'main'+(isMainShow?' main-show':''));

  if (!isMainShow) {
    const head = el('div', 'room-head');
    head.style.setProperty('--room-accent', room.accent);
    head.innerHTML =
      '<div class="kicker">' + room.kicker + '</div>' +
      '<h2 class="room-title">' + room.name + '</h2>' +
      '<p class="room-desc">' + roomDesc(room.id) + '</p>';
    main.appendChild(head);
  }

  if (isMainShow) main.appendChild(modeZone());

  const body = el('div', 'room-body' + (isMainShow ? ' mainshow-body' : ''));
  body.style.setProperty('--room-accent', room.accent);
  const renderer = window.NayaRooms && window.NayaRooms[room.id];
  if (renderer) body.appendChild(renderer());
  else body.appendChild(notVerifiedPanel(room));
  main.appendChild(body);

  shell.append(backdrop, top, leftDrawer, rightDrawer, main);
  return shell;

  function roomDesc(id) {
    return {
      today: 'Your day, answered by the intelligence. What matters, what changed, and what deserves your attention.',
      reports: 'Proof, not promises. Every report carries its evidence and receipts.',
      library: 'Everything retained, organized by what it means — not where it happened to land.',
      connect: 'One brain. Many doors. Choose how humans, agents, apps, and systems connect to the same intelligence.',
      ledger: 'Consequential contributions and actions, inspectable through evidence.',
      connections: 'Humans, AIs, and machines you share intelligence with — each on your terms.',
      lists: 'Living lists that stay current because the intelligence behind them does.',
      mail: 'Messages understood and triaged by meaning, not only recency.',
      spaces: 'Contextual worlds for projects, people, and ideas that belong together.',
      settings: 'Your Hub, your rules: identity, privacy, doors, preferences, and system health.'
    }[id] || '';
  }

  function notVerifiedPanel(room) {
    const { StatePanel } = window.NayaUI;
    const c = R.NOT_VERIFIED_COPY;
    return StatePanel({
      accent: room.accent,
      icon: 'lock',
      title: c.title,
      body: c.body,
      actions: [{
        label: 'Open system health',
        icon: 'core',
        onClick: () => window.NayaRouter.navigate('/hub/settings')
      }]
    });
  }
}

window.HubView = HubView;
