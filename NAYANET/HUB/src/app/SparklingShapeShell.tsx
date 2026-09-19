import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useIdentity } from '../identity/session';
import { routes } from './routes';
import { SmartTabsBar } from './SmartTabsBar';
type Props={children:(path:string)=>ReactNode};
type Item={name:string;route:string;icon:string};
const items:Item[]=[
 {name:'Your Intelligence Today',route:routes.home,icon:'◉'},{name:'Your Report',route:routes.reports,icon:'▤'},
 {name:'Intelligence',route:routes.feed,icon:'✦'},{name:'Smart Notes',route:routes.notes,icon:'◇'},
 {name:'Smart Lists',route:routes.lists,icon:'☷'},{name:'Smart Share',route:routes.share,icon:'↗'},
 {name:'Evidence',route:routes.evidence,icon:'◈'},{name:'Your Connections',route:routes.connections,icon:'↔'},
 {name:'Smart Spaces',route:routes.spaces,icon:'▱'},{name:'Smart Mail',route:routes.mail,icon:'✉'},
];
const top=[['HOME',routes.home],['NAYA POWER',routes.feed],['5-DAY CHALLENGE',routes.today],['ENTER FREE',routes.share],['POWERCAST',routes.mail],['WHITE PAPER',routes.reports],['ABOUT US',routes.connections],['LOGIN',routes.settings]] as const;
const bottom=[['✦ CAPTURE','CAPTURE'],['ASK NAYA','ASK'],['TODAY',routes.home],['REPORTS',routes.reports],['INTELLIGENCE',routes.feed],['LEDGER',routes.ledger],['MAIL',routes.mail],['SPACES',routes.spaces],['LISTS',routes.lists],['SHARE',routes.share]] as const;
const norm=(p:string)=>p.length>1&&p.endsWith('/')?p.slice(0,-1):p||'/';
export function SparklingShapeShell({children}:Props){
 const id=useIdentity();const[path,setPath]=useState(()=>norm(location.pathname));const[q,setQ]=useState('');
 const go=(p:string)=>{const n=norm(p);if(n===path)return;history.pushState({},'',n);setPath(n)};
 useEffect(()=>{const pop=()=>setPath(norm(location.pathname));const nav=(e:Event)=>{const p=(e as CustomEvent<{path?:string}>).detail?.path;if(p)go(p)};const key=(e:KeyboardEvent)=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();document.querySelector<HTMLInputElement>('.sparkling-search')?.focus()}};addEventListener('popstate',pop);addEventListener('nayanet:navigate',nav);addEventListener('keydown',key);return()=>{removeEventListener('popstate',pop);removeEventListener('nayanet:navigate',nav);removeEventListener('keydown',key)}},[path]);
 const ask=()=>{if(!q.trim())return;go(routes.feed);dispatchEvent(new CustomEvent('nayanet:search',{detail:{query:q.trim()}}))};
 return <div className="shell sparkling-shape-shell" data-shell-owner="SparklingShapeReactiveHub" data-route={path} data-runtime-marker="NAYANET-HUB-REACT-CANONICAL">
  <aside className="rail"><button className="brand" onClick={()=>go(routes.home)} aria-label="NayaNET home"><span className="sparkling-logo">✦</span><span><b>NayaNET</b><small>INTELLIGENT HUB</small></span></button><div className="sparkling-presence"><i/><span><b>NAYA IS READY</b><small>Private intelligence workspace</small></span><strong>LIVE</strong></div><div className="label">YOUR INTELLIGENCE</div><nav className="nav">{items.map(x=><button key={x.name} className={path===x.route?'active':''} onClick={()=>go(x.route)}><span className="ico">{x.icon}</span><span>{x.name}</span>{path===x.route&&<i className="sparkling-active"/>}</button>)}</nav><div className="private"><b>PRIVATE BY DEFAULT</b>Shared by choice · Collective by consent · Public by decision.</div></aside>
  <main className="main"><header className="top sparkling-top"><div className="sparkling-primary-nav">{top.map(([name,route])=><button key={name} onClick={()=>go(route)}>{name}</button>)}</div><button className="sparkling-corner" onClick={()=>go(routes.settings)}><span className="sparkling-avatar">{(id.smart_name||'N').slice(0,1).toUpperCase()}</span><span><b>{id.smart_name||'NAYA'}</b><small>@{id.smart_alias||'READY'}</small></span><i/></button></header><div className="sparkling-search-row"><span>⌕</span><input className="sparkling-search" value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>{if(e.key==='Enter')ask()}} placeholder="Search or talk to Naya…" aria-label="Search or talk to Naya"/><kbd>⌘ K</kbd><button onClick={ask}>✦ TALK TO NAYA</button></div><SmartTabsBar/><section className="home">{children(path)}</section></main>
  <aside className="right sparkling-right"><div className="nayaCard"><div className="sparkling-naya-orb">N</div><h2>NAYA</h2><div className="sub">TRUSTED THINKING PARTNER</div><div className="nayaInsight"><b>NAYA · NOW</b><p>Understanding what matters, connecting intelligence, verifying what earns trust, and helping turn it into useful action.</p></div><div className="why"><b>INTELLIGENCE LOOP</b><p>CAPTURE → COMPOUND → USE → VERIFY → LEARN</p></div><button className="action" onClick={()=>go(routes.feed)}>✦ EXPLORE INTELLIGENCE</button></div></aside>
  <div className="mission"><b>CREATE. CONNECT. GROW WITH US.</b> · Intelligence made visible, useful, and reusable.</div><nav className="features"><span className="featureLabel">NAYA POWER</span>{bottom.map(([name,route])=><button key={name} className="featureBtn" onClick={()=>route==='CAPTURE'?go(routes.notes):route==='ASK'?ask():go(route)}>{name}</button>)}</nav>
 </div>;
}
