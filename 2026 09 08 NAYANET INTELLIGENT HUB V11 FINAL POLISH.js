/* NAYANET V11 — SURGICAL LIVE HUB RECONCILIATION
   This layer is intentionally narrow. It does not replace the house.
   It removes only the retired right activation/operations rail, preserves the left navigation,
   makes the center feed full-width, mirrors Activity into Intelligent Blocks, and adds the
   shared social vocabulary to the existing premium blocks.
*/
(()=>{
  'use strict';

  const ROOT = '#nayanet-elite-feed';
  const clean = s => String(s || '').replace(/\s+/g,' ').trim();

  const enforceShell = () => {
    document.querySelectorAll('.activationRail').forEach(el => el.remove());
    const workspace = document.querySelector('.homeWorkspace');
    if (workspace) {
      workspace.style.setProperty('display','block','important');
      workspace.style.setProperty('grid-template-columns','1fr','important');
      workspace.style.setProperty('width','100%','important');
      workspace.style.setProperty('max-width','none','important');
      workspace.style.setProperty('gap','0','important');
    }
    document.querySelectorAll('.homeFeed,#nayanet-elite-feed').forEach(el => {
      el.style.setProperty('width','100%','important');
      el.style.setProperty('max-width','none','important');
      el.style.setProperty('min-width','0','important');
    });
  };

  const installStyle = () => {
    if (document.getElementById('nayanet-v11-live-style')) return;
    const style = document.createElement('style');
    style.id = 'nayanet-v11-live-style';
    style.textContent = `
      html,body{background:#000!important}
      .activationRail{display:none!important;width:0!important;height:0!important;min-width:0!important;max-width:0!important;overflow:hidden!important;visibility:hidden!important;pointer-events:none!important}
      .homeWorkspace{display:block!important;grid-template-columns:1fr!important;width:100%!important;max-width:none!important;gap:0!important}
      .homeFeed,#nayanet-elite-feed{width:100%!important;max-width:none!important;min-width:0!important}
      .nayanet-v11-actions{display:flex;gap:8px;flex-wrap:wrap;margin:0 18px 18px;padding-top:14px;border-top:1px solid #ffffff14}
      .nayanet-v11-actions button{min-height:40px;padding:0 13px;border:1px solid #8b63ff66;border-radius:11px;background:linear-gradient(145deg,#17111f,#08080c);color:#fff;font-size:8px;font-weight:1000;letter-spacing:.05em;box-shadow:inset 0 1px #fff4,0 8px 18px #0009}
      .nayanet-v11-actions button:hover,.nayanet-v11-actions button.active{border-color:#d86cff;box-shadow:0 0 22px #d86cff22}
      .nayanet-v11-actions .rank{color:#ffd98a}
      .nayanet-v11-actions .comment{border-color:#55b9ee66}
      @media(max-width:900px){.sidebar{display:none!important}.app{display:block!important;grid-template-columns:1fr!important}.main{width:100%!important;padding-left:12px!important;padding-right:12px!important}.nayanet-v11-actions button{flex:1 1 auto}}
    `;
    document.head.appendChild(style);
  };

  const addActions = () => {
    document.querySelectorAll(ROOT+' .n3-block').forEach(block => {
      if (block.querySelector('.nayanet-v11-actions')) return;
      const title = clean(block.querySelector('.n3-title')?.textContent || 'Intelligent Block');
      const bar = document.createElement('div');
      bar.className = 'nayanet-v11-actions';
      bar.innerHTML = '<button data-v11="share">＋ SHARE</button><button data-v11="like">👍 LIKE</button><button data-v11="love">♥ LOVE</button><button class="rank" data-v11="rank">★ RANK</button><button class="comment" data-v11="comment">💬 COMMENT</button><button data-v11="save">🔖 SAVE</button>';
      bar.querySelectorAll('button').forEach(btn => {
        btn.onclick = () => {
          const action = btn.dataset.v11;
          if (action === 'comment') {
            const text = window.prompt('Add a comment to this Intelligent Block:');
            if (text && text.trim()) btn.textContent = '💬 COMMENT ✓';
            return;
          }
          if (action === 'rank') {
            const rank = window.prompt('Rank this intelligence 1–5:', '');
            if (rank) btn.textContent = '★ RANK '+rank+'/5';
            return;
          }
          if (action === 'share') {
            const text = title+'\n\n'+clean(block.querySelector('.n3-nutshell p')?.textContent || '')+'\n\nNayaNET — Create. Connect. Grow with US.';
            if (navigator.share) navigator.share({title,text,url:location.href}).catch(()=>{});
            else if (navigator.clipboard) navigator.clipboard.writeText(text).then(()=>{btn.textContent='✓ COPIED';setTimeout(()=>btn.textContent='＋ SHARE',1200)}).catch(()=>{});
            return;
          }
          btn.classList.toggle('active');
        };
      });
      const footer = block.querySelector('.n3-footer');
      if (footer) footer.insertAdjacentElement('beforebegin',bar); else block.appendChild(bar);
    });
  };

  const mirrorActivity = () => {
    const feed = document.querySelector(ROOT);
    if (!feed || feed.dataset.v11ActivityBound) return;
    feed.dataset.v11ActivityBound = '1';
    feed.addEventListener('click', event => {
      const tab = event.target.closest('.n3-tab');
      if (!tab || tab.dataset.view !== 'activity') return;
      event.preventDefault();
      event.stopImmediatePropagation();
      feed.querySelectorAll('.n3-tab').forEach(x => {
        x.classList.toggle('active', x === tab);
        x.setAttribute('aria-selected', String(x === tab));
      });
      const body = feed.querySelector('.n3-body');
      if (!body) return;
      const source = [...body.querySelectorAll('.n3-block')];
      if (!source.length) return;
      body.innerHTML = source.map((block,i) => {
        const clone = block.cloneNode(true);
        clone.classList.add('nayanet-v11-activity-block');
        const eyebrow = clone.querySelector('.n3-eyebrow');
        if (eyebrow) eyebrow.innerHTML = '<span class="n3-led"></span><b>INTELLIGENT BLOCK</b> · ACTIVITY · EVENT '+String(i+1).padStart(2,'0');
        return clone.outerHTML;
      }).join('');
      addActions();
    }, true);
  };

  const boot = () => {
    installStyle();
    enforceShell();
    mirrorActivity();
    addActions();
    [100,350,800,1500,3000].forEach(ms => setTimeout(() => {
      enforceShell();
      mirrorActivity();
      addActions();
    }, ms));
    if (!document.documentElement.dataset.nayanetV11Observer) {
      document.documentElement.dataset.nayanetV11Observer = '1';
      new MutationObserver(() => {
        enforceShell();
        addActions();
      }).observe(document.body,{childList:true,subtree:true});
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',boot,{once:true});
  else boot();
})();
