(() => {
  const links = [
    ['HOME','https://hmclibrary.groovemember.net/home'],
    ['NAYA POWER','https://academy.nayanet.app/'],
    ['5 DAY CHALLENGE','https://academy.nayanet.app/'],
    ['ENTER FREE','https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab'],
    ['POWERCASTS','https://nayanet.groovepages.com/powerplayer'],
    ['WHITE PAPER','https://nayanet.groovepages.com/whitepaper'],
    ['ABOUT US','https://nayanet.groovepages.com/aboutus'],
    ['HMC LOGIN','https://hmclibrary.groovemember.net/login']
  ];
  const reports = [
    ['SMART NOTES','https://drive.google.com/file/d/19sRtp22aAn35wNoqqpNiZHkaFGmUOxoP/view?usp=sharing'],
    ['NO DEAD ENDS','https://drive.google.com/file/d/1LgRmYAQ85AB6mmu6Qp2ovghyd1lP-FNh/view?usp=sharing'],
    ['CONTEXT','https://drive.google.com/file/d/1N-XzV3_RCTHuLdp4leZNlOo7ITFwrICR/view?usp=sharing'],
    ['10 STAR SERVICE','https://drive.google.com/file/d/1F9M66i5Av_oJcIa5dve-U0mMeAgYKczT/view?usp=sharing'],
    ['ADAPTIVE LEARNING','https://drive.google.com/file/d/1dcViGUqV7GKnNBCYybbAEEKuOoZw3-XC/view?usp=sharing']
  ];
  const css = document.createElement('style');
  css.textContent = `
    .naya-ecosystem{position:relative;z-index:22;margin:0 28px 0;padding:12px 12px 11px;border:1px solid rgba(216,108,255,.22);border-radius:18px;background:linear-gradient(135deg,rgba(19,14,28,.96),rgba(7,7,11,.96));box-shadow:inset 0 1px rgba(255,255,255,.08),0 16px 36px rgba(0,0,0,.42),0 0 32px rgba(157,117,255,.06);backdrop-filter:blur(24px)}
    .naya-ecosystem__inner,.naya-reports__inner{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
    .naya-ecosystem__label,.naya-reports__label{margin:0 4px 0 2px;color:#817889;font-size:7px;font-weight:1000;letter-spacing:.18em;white-space:nowrap}
    .naya-link,.naya-report{position:relative;display:inline-flex;align-items:center;justify-content:center;min-height:35px;padding:0 11px;border:1px solid rgba(255,255,255,.12);border-radius:10px;background:linear-gradient(145deg,#17121f,#09090d);color:#e9e3ee;text-decoration:none;font-size:7px;font-weight:1000;letter-spacing:.055em;white-space:nowrap;overflow:hidden;transition:transform .2s cubic-bezier(.16,.84,.22,1),border-color .2s,box-shadow .2s,background .2s,color .2s}
    .naya-link:before,.naya-report:before{content:"";position:absolute;inset:0;background:linear-gradient(120deg,transparent 18%,rgba(255,255,255,.11) 48%,transparent 72%);transform:translateX(-130%);transition:transform .6s ease}
    .naya-link:hover,.naya-report:hover{transform:translateY(-2px);border-color:rgba(216,108,255,.72);color:#fff;background:linear-gradient(145deg,#251532,#0d0a12);box-shadow:inset 0 1px rgba(255,255,255,.12),0 10px 25px rgba(0,0,0,.5),0 0 24px rgba(216,108,255,.13)}
    .naya-link:hover:before,.naya-report:hover:before{transform:translateX(130%)}
    .naya-link:focus-visible,.naya-report:focus-visible{outline:2px solid #d86cff;outline-offset:2px}
    .naya-link--primary{border-color:rgba(216,108,255,.42);background:linear-gradient(145deg,#22122d,#0c0a10);box-shadow:inset 0 1px rgba(255,255,255,.09),0 7px 20px rgba(0,0,0,.35)}
    .naya-tagline{position:relative;z-index:17;margin:30px 28px 0;padding:22px 24px;text-align:center;border:1px solid rgba(216,108,255,.18);border-radius:20px;background:radial-gradient(700px 120px at 50% 0,rgba(216,108,255,.12),transparent 72%),linear-gradient(145deg,rgba(18,13,24,.92),rgba(7,7,10,.96));box-shadow:inset 0 1px rgba(255,255,255,.07),0 18px 42px rgba(0,0,0,.35)}
    .naya-tagline__main{display:block;color:#f8f4fb;font-size:clamp(15px,1.7vw,21px);font-weight:900;letter-spacing:-.025em;line-height:1.3}.naya-tagline__main em{font-style:normal;color:#dca1ff}.naya-tagline__sub{display:block;margin-top:6px;color:#98919f;font-size:8px;font-weight:850;letter-spacing:.12em;text-transform:uppercase}
    .naya-bottom{position:relative;z-index:60;margin:12px 28px 0;padding:11px;border:1px solid rgba(216,108,255,.28);border-radius:18px;background:rgba(7,7,10,.92);backdrop-filter:blur(28px);box-shadow:inset 0 1px rgba(255,255,255,.08),0 22px 55px rgba(0,0,0,.62),0 0 36px rgba(216,108,255,.07)}
    .naya-bottom .naya-reports__inner{justify-content:center}.naya-bottom .naya-report{flex:1 1 150px}
    @media(max-width:820px){.naya-ecosystem,.naya-tagline{margin-left:14px;margin-right:14px}.naya-ecosystem{padding:10px}.naya-ecosystem__inner{overflow:auto;flex-wrap:nowrap;scrollbar-width:none}.naya-ecosystem__inner::-webkit-scrollbar{display:none}.naya-ecosystem__label{display:none}.naya-link{flex:0 0 auto}.naya-tagline{padding:18px 16px;margin-top:22px}.naya-bottom{margin-left:8px;margin-right:8px;margin-bottom:8px}.naya-bottom .naya-reports__inner{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.naya-bottom .naya-report{min-width:0;width:100%}.naya-bottom .naya-report:last-child{grid-column:1/-1}.naya-bottom .naya-reports__label{grid-column:1/-1;text-align:center;width:100%;margin:0 0 2px}}
  `;
  document.head.appendChild(css);
  const makeLinks=(items,cls,primary=false)=>items.map(([label,url],i)=>`<a class="${cls}${primary&&i<4?' naya-link--primary':''}" href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`).join('');
  const top=document.createElement('div');
  top.className='naya-ecosystem';
  top.innerHTML=`<div class="naya-ecosystem__inner"><span class="naya-ecosystem__label">NAYANET ECOSYSTEM</span>${makeLinks(links,'naya-link',true)}</div>`;
  const main=document.querySelector('.main');
  const search=document.getElementById('searchSection');
  if(main&&search) main.insertBefore(top,search);
  const tagline=document.createElement('section');
  tagline.className='naya-tagline';
  tagline.innerHTML='<span class="naya-tagline__main">Your life creates your intelligence every day. <em>Naya</em> helps you capture it, understand it, remember it, compound it, and use it.</span><span class="naya-tagline__sub">Living intelligence · made useful</span>';
  const feed=document.querySelector('.feed');
  if(feed) feed.insertBefore(tagline,feed.querySelector('.feedHead'));
  const bottom=document.createElement('nav');
  bottom.className='naya-bottom';
  bottom.innerHTML=`<div class="naya-reports__inner"><span class="naya-reports__label">FEATURE REPORTS</span>${makeLinks(reports,'naya-report')}</div>`;
  if(main) main.appendChild(bottom);
})();
