import { useEffect, useRef, useState } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import source from './hub-baseline.html?raw';
import { SmartMailSurface } from '../app/SmartMailSurface';
import '../styles/naya-mail-baseline.css';

export function HubBaselineApp() {
  const host = useRef<HTMLDivElement>(null);
  const mailRoot = useRef<Root | null>(null);
  const [mailOpen, setMailOpen] = useState(() => new URLSearchParams(location.search).get('surface') === 'mail');
  useEffect(() => {
    const root = host.current;
    if (!root || root.dataset.mounted === '1') return;
    root.dataset.mounted = '1';
    const doc = new DOMParser().parseFromString(source, 'text/html');
    doc.head.querySelectorAll('style').forEach(style => { const node=document.createElement('style'); node.dataset.nayanetBaseline='true'; node.textContent=style.textContent||''; document.head.appendChild(node); });
    root.innerHTML = doc.body.innerHTML;
    
    const mail = root.querySelector<HTMLButtonElement>('.nav button[data-page="mail"]');
    if (!mail) return;
    const intercept=(event:Event)=>{event.preventDefault();event.stopImmediatePropagation();setMailOpen(true);const title=root.querySelector('#topTitle');if(title)title.textContent='Smart Mail';};
    mail.addEventListener('click',intercept,true);
    return ()=>mail.removeEventListener('click',intercept,true);
  },[]);
  useEffect(()=>{
    const root=host.current;if(!root)return;
    const main=root.querySelector('main');if(!main)return;
    if(mailOpen){
      ['#searchSection','.hero','.feedNav','.feedHead','#blocks'].forEach(selector=>root.querySelectorAll<HTMLElement>(selector).forEach(node=>{node.dataset.baselineHiddenForMail='true';node.style.display='none';}));
      let mount=main.querySelector<HTMLDivElement>('#naya-mail-react-root');
      if(!mount){mount=document.createElement('div');mount.id='naya-mail-react-root';main.appendChild(mount);}
      if(!mailRoot.current)mailRoot.current=createRoot(mount);
      mailRoot.current.render(<SmartMailSurface/>);
    }else if(mailRoot.current){mailRoot.current.unmount();mailRoot.current=null;const mount=main.querySelector('#naya-mail-react-root');mount?.remove();root.querySelectorAll<HTMLElement>('[data-baseline-hidden-for-mail]').forEach(node=>{node.style.display='';delete node.dataset.baselineHiddenForMail;});}
  },[mailOpen]);
  return <div ref={host} data-nayanet-baseline-app="true" data-mail-open={mailOpen?'true':'false'} />;
}



