/* NayaNET — Component Physics Runtime
   One interaction language for every surface.
   DEPTH -> LIGHT -> STATE -> RESPONSE -> CONSEQUENCE */
(()=>{'use strict';
  const root=document.documentElement, body=document.body;
  const q=(s,c=document)=>c.querySelector(s), qa=(s,c=document)=>[...c.querySelectorAll(s)];
  const buttonSelector='button,[role="button"]';
  const inputSelector='input,textarea,select';
  const iconSelector='.brand-symbol,.ask-orb,.world-glyph,.core-eye,.player-live,.center-status i,.field-callout span';
  const classify=()=>{
    qa(buttonSelector).forEach(el=>{
      if(el.closest('#frontDoor')) return;
      el.classList.add('np-power-object');
      if(el.matches('.world,.world-card,.cast')) el.classList.add('np-intelligence-surface');
      if(el.matches('.naya-core,.ask-naya,.play-button')) el.dataset.npTone='intelligence';
      else if(el.matches('.world,.world-card')) el.dataset.npTone='knowledge';
      else if(el.matches('.world-secondary,.return-button')) el.dataset.npTone='connection';
      else if(el.matches('[data-action="goal"],[data-action="note"]')) el.dataset.npTone='growth';
      else if(el.matches('[data-action="copyid"],[data-action="copylink"]')) el.dataset.npTone='significance';
    });
    qa(inputSelector).forEach(el=>{
      if(el.closest('#frontDoor')) return;
      el.classList.add('np-identity-portal');
      if(el.value.trim()) el.classList.add('np-valid');
    });
    qa(iconSelector).forEach(el=>el.classList.add('np-intelligence-icon'));
    const seek=q('#seek'); if(seek) seek.classList.add('np-energy-path');
    const waveform=q('#waveform'); if(waveform) waveform.classList.add('np-energy-path');
  };
  const sunState=(name)=>{
    body.classList.remove('np-state-idle','np-state-approach','np-state-touch','np-state-intelligence','np-state-speaking','np-state-playing','np-state-return');
    body.classList.add(`np-state-${name}`);
  };
  sunState('idle');

  document.addEventListener('pointerover',e=>{
    const el=e.target.closest(buttonSelector); if(!el) return;
    if(el.matches('.naya-core,.ask-naya')) sunState('approach');
  },{passive:true});
  document.addEventListener('pointerout',e=>{
    const el=e.target.closest(buttonSelector); if(!el) return;
    if(el.matches('.naya-core,.ask-naya')) sunState(body.classList.contains('audio-live')?'playing':'idle');
  },{passive:true});
  document.addEventListener('pointerdown',e=>{
    const el=e.target.closest(buttonSelector); if(!el||el.disabled) return;
    el.classList.add('np-pressed');
    if(el.matches('.naya-core,.ask-naya,.world,.world-card')) sunState('touch');
  },{passive:true});
  ['pointerup','pointercancel'].forEach(type=>document.addEventListener(type,e=>{
    const el=e.target.closest(buttonSelector); if(!el) return;
    window.setTimeout(()=>el.classList.remove('np-pressed'),90);
    if(el.matches('.naya-core,.ask-naya')) window.setTimeout(()=>sunState(body.classList.contains('audio-live')?'playing':'intelligence'),120);
  },{passive:true}));

  document.addEventListener('input',e=>{
    const el=e.target.closest(inputSelector); if(!el) return;
    el.classList.toggle('np-valid',!!el.value.trim());
    el.classList.toggle('np-invalid',false);
  });
  document.addEventListener('change',e=>{
    const el=e.target.closest(inputSelector); if(el) el.classList.toggle('np-valid',!!String(el.value||'').trim());
  });
  document.addEventListener('focusin',e=>{
    const el=e.target.closest(inputSelector); if(el) el.dataset.npState='active';
    if(e.target.closest('#nameInput')) sunState('touch');
  });
  document.addEventListener('focusout',e=>{
    const el=e.target.closest(inputSelector); if(el) el.dataset.npState=el.value.trim()?'ready':'idle';
  });

  document.addEventListener('click',e=>{
    const el=e.target.closest(buttonSelector); if(!el) return;
    if(el.matches('.world,.world-card')){
      qa('.world,.world-card').forEach(x=>x.classList.remove('np-selected'));
      el.classList.add('np-selected');
      sunState('intelligence');
    }
  });

  window.addEventListener('naya:audio-state',e=>{
    const playing=!!e.detail?.playing;
    body.classList.toggle('audio-live',playing);
    sunState(playing?'playing':'idle');
    const seek=q('#seek'); if(seek) seek.classList.toggle('np-active',playing);
    const waveform=q('#waveform'); if(waveform) waveform.classList.toggle('np-active',playing);
  });
  const audio=q('#audio');
  if(audio){
    audio.addEventListener('play',()=>{body.classList.add('audio-live');sunState('playing');});
    audio.addEventListener('pause',()=>{body.classList.remove('audio-live');sunState('idle');});
    audio.addEventListener('ended',()=>{body.classList.remove('audio-live');sunState('return');window.setTimeout(()=>sunState('idle'),700);});
  }

  /* E02 ecosystem menu + reminders rail. Scoped to the Hub so the entrance is untouched. */
  const installHubNavigation=()=>{
    const hub=q('#hub'); if(!hub || q('#e02EcosystemNav')) return;
    const css=document.createElement('style');
    css.id='e02HubNavigationStyles';
    css.textContent=`
      #e02EcosystemNav{position:relative;z-index:40;display:flex;align-items:center;justify-content:flex-end;gap:7px;flex-wrap:wrap;margin:0 0 18px;padding:9px 10px;border:1px solid rgba(255,255,255,.1);border-radius:20px;background:rgba(7,6,12,.72);backdrop-filter:blur(22px);box-shadow:0 18px 50px rgba(0,0,0,.28)}
      #e02EcosystemNav a{display:inline-flex;align-items:center;min-height:34px;padding:0 11px;border:1px solid rgba(255,255,255,.09);border-radius:12px;background:rgba(255,255,255,.035);color:#eeeaf4;text-decoration:none;font-size:8px;font-weight:750;letter-spacing:.09em;white-space:nowrap;transition:.2s ease}
      #e02EcosystemNav a:hover{transform:translateY(-2px);border-color:rgba(141,99,255,.5);background:rgba(141,99,255,.1);box-shadow:0 8px 22px rgba(0,0,0,.28)}
      #e02EcosystemNav a[data-accent="gold"]{border-color:rgba(216,183,106,.22)}
      #e02RemindersRail{position:fixed;left:14px;top:50%;transform:translateY(-50%);z-index:45;width:126px;padding:10px;border:1px solid rgba(255,255,255,.1);border-radius:19px;background:rgba(7,6,12,.8);backdrop-filter:blur(24px);box-shadow:0 22px 60px rgba(0,0,0,.4);}
      #e02RemindersRail .e02-rail-label{display:block;padding:4px 5px 8px;color:#aaa5b5;font-size:7px;font-weight:900;letter-spacing:.18em}
      #e02RemindersRail button{width:100%;min-height:38px;border:1px solid rgba(216,183,106,.2);border-radius:12px;background:rgba(216,183,106,.045);color:#f3eef5;font-size:8px;font-weight:850;letter-spacing:.09em;text-align:left;padding:0 10px;transition:.2s ease}
      #e02RemindersRail button:hover{transform:translateX(2px);border-color:rgba(216,183,106,.55);background:rgba(216,183,106,.1)}
      #e02RemindersRail .e02-reminder-dot{display:inline-block;width:6px;height:6px;margin-right:7px;border-radius:50%;background:var(--gold,#d8b76a);box-shadow:0 0 10px var(--gold,#d8b76a)}
      @media(max-width:1100px){#e02EcosystemNav{justify-content:flex-start}#e02RemindersRail{position:relative;left:auto;top:auto;transform:none;width:auto;max-width:1180px;margin:0 auto 20px;padding:9px 12px;display:flex;align-items:center;gap:8px}#e02RemindersRail .e02-rail-label{padding:4px 2px;white-space:nowrap}#e02RemindersRail button{width:auto;padding:0 12px}}
      @media(max-width:620px){#e02EcosystemNav{gap:5px;padding:8px}#e02EcosystemNav a{font-size:7px;padding:0 8px;min-height:31px}#e02RemindersRail{overflow-x:auto}#e02RemindersRail button{flex:none}}
    `;
    document.head.appendChild(css);

    const nav=document.createElement('nav');
    nav.id='e02EcosystemNav';
    nav.setAttribute('aria-label','NayaNET ecosystem');
    const links=[
      ['Home','https://hmclibrary.groovemember.net/home'],
      ['Naya Power','https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab'],
      ['NayaNET Academy','https://academy.nayanet.app/'],
      ['Naya Power Player','https://nayanet.groovepages.com/powerplayer'],
      ['About Us','https://nayanet.groovepages.com/aboutus'],
      ['White Paper','https://nayanet.groovepages.com/aboutus'],
      ['FREE TRAIL','https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab'],
      ['Academy Login','https://hmclibrary.groovemember.net/login']
    ];
    links.forEach(([label,url])=>{
      const a=document.createElement('a'); a.href=url; a.textContent=label; a.target='_blank'; a.rel='noopener noreferrer';
      if(label==='FREE TRAIL') a.dataset.accent='gold';
      nav.appendChild(a);
    });

    const rail=document.createElement('aside');
    rail.id='e02RemindersRail';
    rail.setAttribute('aria-label','Reminders');
    rail.innerHTML='<span class="e02-rail-label">INTELLIGENCE</span><button type="button" id="e02RemindersButton"><span class="e02-reminder-dot"></span>REMINDERS</button>';
    hub.insertBefore(nav,hub.firstChild);
    hub.parentElement.insertBefore(rail,hub);
    q('#e02RemindersButton')?.addEventListener('click',()=>{
      const target=q('#reminders,[data-world="reminders"],#deepIntelligence,.deep-intelligence');
      if(target) target.scrollIntoView({behavior:'smooth',block:'center'});
      else window.dispatchEvent(new CustomEvent('naya:reminders-open'));
    });
  };

  window.addEventListener('naya:data-ready',()=>{classify();installHubNavigation();});
  const observer=new MutationObserver(()=>{classify();installHubNavigation();});
  observer.observe(document.body,{childList:true,subtree:true});
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>{classify();installHubNavigation();},{once:true}); else {classify();installHubNavigation();}
  window.NayaNETPhysics={version:'1.1',state:sunState,refresh:classify};
})();
