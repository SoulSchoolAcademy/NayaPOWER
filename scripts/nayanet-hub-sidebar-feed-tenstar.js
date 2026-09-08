/* NayaNET Intelligent Hub — surgical presentation evolution
   Mission: remove persistent left sidebar while preserving navigation access;
   elevate Personal Intelligence, Smart Feed/Activity, and Collective Feed boards.
*/
(function(){
  'use strict';
  const STYLE_ID='nayanet-hub-sidebar-feed-tenstar-style';
  const DRAWER_ID='nayanet-hub-nav-drawer';
  if(document.getElementById(STYLE_ID)) return;

  const style=document.createElement('style');
  style.id=STYLE_ID;
  style.textContent=`
    /* FULL-WIDTH HUB: no persistent left rail */
    .app{grid-template-columns:minmax(0,1fr)!important}
    .sidebar{display:none!important}
    .main{width:100%;min-width:0;padding-left:clamp(18px,4vw,48px);padding-right:clamp(18px,4vw,48px)}

    /* Temporary navigation: accessible without restoring a persistent sidebar */
    .nh10-menu{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:40px;padding:0 13px;border:1px solid #ffffff24;border-radius:12px;background:#09090d;color:#fff;font-size:8px;font-weight:1000;letter-spacing:.1em;box-shadow:inset 0 1px #fff3,0 10px 25px #0008;cursor:pointer}
    .nh10-menu:hover,.nh10-menu:focus-visible{border-color:#d86cff70;box-shadow:inset 0 1px #fff5,0 14px 30px #000a,0 0 24px #d86cff14;outline:none;transform:translateY(-1px)}
    .nh10-overlay{position:fixed;inset:0;background:#0009;backdrop-filter:blur(8px);z-index:100;display:none}
    .nh10-overlay.open{display:block}
    .nh10-drawer{position:absolute;left:0;top:0;bottom:0;width:min(330px,88vw);padding:18px;background:#050507;border-right:1px solid #ffffff1d;box-shadow:25px 0 70px #000d;overflow:auto}
    .nh10-drawer-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;padding-bottom:14px;border-bottom:1px solid #ffffff14}
    .nh10-drawer-head strong{font-size:12px;letter-spacing:.08em}
    .nh10-close{width:38px;height:38px;border:1px solid #ffffff20;border-radius:11px;background:#0b0b10;color:#fff;cursor:pointer}
    .nh10-nav{display:grid;gap:7px}
    .nh10-nav button{min-height:48px;border:1px solid #ffffff17;border-radius:13px;background:#0a0a0e;color:#eeeaf2;text-align:left;padding:0 13px;font-size:9px;font-weight:900;cursor:pointer}
    .nh10-nav button:hover,.nh10-nav button:focus-visible{border-color:#d86cff60;background:#12101a;outline:none}

    /* 10/10 intelligence feed boards */
    #nhxLibraryGroups{display:grid;gap:18px}
    .nhx-library-group{position:relative;border:1px solid #ffffff1b;border-radius:26px;background:#050507;overflow:hidden;padding:26px;box-shadow:inset 0 1px #fff4,0 24px 55px #000b;isolation:isolate}
    .nhx-library-group:before{content:"";position:absolute;inset:0 0 auto 0;height:2px;background:linear-gradient(90deg,var(--nh10-tone,#55b9ee),transparent 72%);box-shadow:0 0 28px var(--nh10-tone,#55b9ee)}
    .nhx-library-group:after{content:"";position:absolute;inset:0;background:radial-gradient(500px 180px at 10% 0%,color-mix(in srgb,var(--nh10-tone,#55b9ee) 9%,transparent),transparent 72%);pointer-events:none;z-index:-1}
    .nhx-library-group[data-libgroup="personal"]{--nh10-tone:#d86cff}
    .nhx-library-group[data-libgroup="smart"]{--nh10-tone:#55b9ee}
    .nhx-library-group[data-libgroup="collective"]{--nh10-tone:#e8c766}
    .nhx-library-group>.eyebrow{color:#fff!important;letter-spacing:.18em;font-weight:1000}
    .nhx-library-group>h2{font-size:clamp(25px,3vw,38px);line-height:1;letter-spacing:-.045em;margin:9px 0 8px;color:#fff}
    .nhx-library-group>.nhx-group-sub{max-width:760px;color:#c9c4ce;font-size:12px;line-height:1.6;margin:0 0 20px}
    .nhx-library-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
    .nhx-library-grid:empty:after{content:"No verified intelligence is available in this feed yet.";grid-column:1/-1;padding:24px;border:1px dashed #ffffff22;border-radius:16px;color:#8f8996;font-size:10px;text-align:center}
    .nhx-library-group .nhx-library-card,.nhx-library-group article{border:1px solid #ffffff18!important;border-radius:18px!important;background:#08080c!important;box-shadow:inset 0 1px #fff3,0 15px 32px #0008!important;transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease!important}
    .nhx-library-group .nhx-library-card:hover,.nhx-library-group article:hover{transform:translateY(-3px);border-color:#ffffff35!important;box-shadow:inset 0 1px #fff5,0 22px 42px #000b,0 0 26px color-mix(in srgb,var(--nh10-tone) 9%,transparent)!important}
    .nhx-library-group .nhx-library-card h3,.nhx-library-group article h3{color:#fff!important;letter-spacing:-.025em}
    .nhx-library-group .nhx-library-card p,.nhx-library-group article p{color:#d0cbd4!important;line-height:1.6}
    .nh10-active-label{display:inline-flex;align-items:center;gap:7px;margin:0 0 13px;padding:7px 10px;border:1px solid #ffffff18;border-radius:999px;background:#08080c;color:#fff;font-size:7px;font-weight:1000;letter-spacing:.1em}
    .nh10-active-label i{width:6px;height:6px;border-radius:50%;background:var(--nh10-tone,#55b9ee);box-shadow:0 0 12px var(--nh10-tone,#55b9ee)}

    @media(max-width:800px){
      .main{padding-left:14px;padding-right:14px}
      .nhx-library-grid{grid-template-columns:1fr}
      .nhx-library-group{padding:19px;border-radius:21px}
      .nh10-menu{min-height:38px;padding:0 11px}
    }
  `;
  document.head.appendChild(style);

  function navItems(){
    const source=document.querySelector('.sidebar .nav');
    if(!source)return [];
    return [...source.querySelectorAll('[data-page]')].map(b=>({page:b.dataset.page,label:b.textContent.trim()}));
  }
  function openNav(){const o=document.getElementById(DRAWER_ID);if(o)o.classList.add('open')}
  function closeNav(){const o=document.getElementById(DRAWER_ID);if(o)o.classList.remove('open')}
  function installNav(){
    const top=document.querySelector('.topbar');
    if(!top||document.getElementById('nh10Menu'))return;
    const right=top.querySelector('.topright')||top;
    const menu=document.createElement('button');menu.id='nh10Menu';menu.className='nh10-menu';menu.type='button';menu.innerHTML='☰ MENU';menu.setAttribute('aria-label','Open NayaNET navigation');menu.onclick=openNav;right.insertBefore(menu,right.firstChild);
    const overlay=document.createElement('div');overlay.id=DRAWER_ID;overlay.className='nh10-overlay';overlay.innerHTML='<aside class="nh10-drawer" role="dialog" aria-label="NayaNET navigation"><div class="nh10-drawer-head"><strong>NayaNET</strong><button class="nh10-close" type="button" aria-label="Close navigation">×</button></div><nav class="nh10-nav"></nav></aside>';
    document.body.appendChild(overlay);
    const nav=overlay.querySelector('.nh10-nav');navItems().forEach(x=>{const b=document.createElement('button');b.type='button';b.textContent=x.label;b.dataset.page=x.page;b.onclick=()=>{if(typeof window.showPage==='function')window.showPage(x.page);else document.querySelector('[data-page="'+x.page+'"]')?.click();closeNav()};nav.appendChild(b)});
    overlay.querySelector('.nh10-close').onclick=closeNav;overlay.addEventListener('click',e=>{if(e.target===overlay)closeNav()});document.addEventListener('keydown',e=>{if(e.key==='Escape')closeNav()});
  }
  function labelBoards(){
    document.querySelectorAll('.nhx-library-group').forEach(g=>{if(g.querySelector('.nh10-active-label'))return;const label=document.createElement('div');label.className='nh10-active-label';label.innerHTML='<i></i><span>INTELLIGENCE FEED</span>';g.insertBefore(label,g.firstChild)});
  }
  function run(){installNav();labelBoards()}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  const observer=new MutationObserver(()=>{installNav();labelBoards()});observer.observe(document.body,{childList:true,subtree:true});
})();
