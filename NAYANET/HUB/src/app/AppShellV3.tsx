import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useIdentity } from '../identity/session';
import { routes } from './routes';

type ShellProps={children:(path:string)=>ReactNode};
type NavItem={name:string;route:string;icon:string};
const items:NavItem[]=[
 {name:'Your Intelligence Today',route:routes.home,icon:'◉'},
 {name:'Your Report',route:routes.reports,icon:'▤'},
 {name:'Intelligence',route:routes.feed,icon:'✦'},
 {name:'Smart Notes',route:routes.notes,icon:'◇'},
 {name:'Smart Lists',route:routes.lists,icon:'☷'},
 {name:'Smart Share',route:routes.share,icon:'↗'},
 {name:'Evidence',route:routes.evidence,icon:'◈'},
 {name:'Your Connections',route:routes.connections,icon:'↔'},
 {name:'Smart Spaces',route:routes.spaces,icon:'▱'},
 {name:'Smart Mail',route:routes.mail,icon:'✉'},
 {name:'Settings',route:routes.settings,icon:'⚙'}
];
const normalize=(p:string)=>p.length>1&&p.endsWith('/')?p.slice(0,-1):p||'/';
export function AppShellV3({children}:ShellProps){
 const id=useIdentity();const[path,setPath]=useState(()=>normalize(window.location.pathname));const[query,setQuery]=useState('');
 useEffect(()=>{const f=()=>setPath(normalize(window.location.pathname));const nav=(e:Event)=>{const p=(e as CustomEvent<{path?:string}>).detail?.path;if(p)go(p)};const key=(e:KeyboardEvent)=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();document.querySelector<HTMLInputElement>('.universal-search input')?.focus()}};addEventListener('popstate',f);addEventListener('nayanet:navigate',nav);addEventListener('keydown',key);return()=>{removeEventListener('popstate',f);removeEventListener('nayanet:navigate',nav);removeEventListener('keydown',key)}},[path]);
 const go=(p:string)=>{const next=normalize(p);if(next===path)return;history.pushState({},'',next);setPath(next)};const submit=()=>{const q=query.trim();if(!q)return;go(routes.feed);dispatchEvent(new CustomEvent('nayanet:search',{detail:{query:q}}))};const current=items.find(x=>x.route===path);const label=current?.name||'Your Intelligence Today';
 return <div className="app" data-shell-owner="AppShellV3" data-route={path} data-runtime-marker="NAYANET-HUB-REACT-CANONICAL"><aside className="sidebar"><button className="brand" onClick={()=>go(routes.home)} aria-label="NayaNET home"><span className="logo"><span>✦</span></span><span className="brand-copy"><b>NayaNET</b><small>INTELLIGENT HUB</small></span></button><div className="side-context"><span className="online-dot"/><span><b>NAYA IS READY</b><small>Private intelligence workspace</small></span><strong>LIVE</strong></div><div className="nav-section"><span>YOUR INTELLIGENCE</span>{items.map(item=><button key={item.name} className={`nav-item ${path===item.route?'active':''}`} onClick={()=>go(item.route)} aria-current={path===item.route?'page':undefined}><span className="nav-icon">{item.icon}</span><span className="nav-name">{item.name}</span>{path===item.route&&<i className="nav-active-dot"/>}</button>)}</div><div className="sidebar-spacer"/><div className="side-trust"><span className="trust-led"/><div><b>INTELLIGENCE MODE</b><small>Evidence-aware · stateful · bounded</small></div></div></aside><main className="main"><header className="topbar"><div className="top-context"><div className="connectionPill"><span className="led good"/><span>NAYANET ONLINE</span></div><div className="route-context"><span>NAYANET</span><i/> <strong>{label}</strong></div></div><div className="universal-search"><span className="search-icon">⌕</span><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>{if(e.key==='Enter')submit()}} placeholder="Search or talk to Naya…" aria-label="Search or talk to Naya"/><span className="search-hint">⌘ K</span><button className="talk-button" onClick={submit}>✦ TALK TO NAYA</button></div><div className="top-actions"><button className="top-action" onClick={()=>go(routes.feed)}>＋ <span>Explore Intelligence</span></button><button className="identity-chip" onClick={()=>go(routes.settings)} aria-label="Open settings"><span className="identity-avatar">{(id.smart_name||'N').slice(0,1).toUpperCase()}</span><span className="identity-copy"><b>{id.smart_name}</b><small>@{id.smart_alias}</small></span></button></div></header><section className="home">{children(path)}</section></main><aside className="hub-right-rail"><div className="naya-rail-card"><div className="naya-orb">N</div><div className="naya-rail-title">NAYA</div><div className="naya-rail-sub">TRUSTED THINKING PARTNER</div><div className="naya-rail-state"><span/> PRESENT</div><p>Understanding what matters, connecting intelligence, verifying what earns trust, and helping turn it into useful action.</p><button onClick={()=>go(routes.feed)}>✦ EXPLORE INTELLIGENCE</button></div><div className="rail-insight"><span>INTELLIGENCE LOOP</span><b>CAPTURE → COMPOUND</b><p>Discover → understand → connect → act → verify → learn → new intelligence.</p></div><div className="rail-insight"><span>PRIVACY</span><b>PRIVATE BY DEFAULT</b><p>Shared by choice · Collective by consent · Public by decision.</p></div></aside></div>;
}