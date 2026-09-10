import {useEffect,useState} from 'react';
import {useIdentity} from '../identity/session';
import type {ReactNode} from 'react';
import {routes} from './routes';

type ShellProps={children:(path:string)=>ReactNode};
const nav:[string,string,string][]=[
 ['Home',routes.home,'⌂'],['Smart Feed',routes.feed,'✦'],['Smart Notes',routes.notes,'◈'],['Intelligence Today',routes.today,'◷'],['Reports',routes.reports,'▤'],['Intelligent Library',routes.library,'▦'],['Collective',routes.collective,'◎'],['Evidence',routes.evidence,'◉'],['Connections',routes.connections,'↔'],['Smart Mail',routes.mail,'✉'],['Smart Space',routes.space,'◌'],['Settings',routes.settings,'⚙']
];
function normalize(path:string){if(path.length>1&&path.endsWith('/'))return path.slice(0,-1);return path||'/'}
export function AppShell({children}:ShellProps){
 const id=useIdentity();
 const [path,setPath]=useState(()=>normalize(window.location.pathname));
 useEffect(()=>{const onPop=()=>setPath(normalize(window.location.pathname));window.addEventListener('popstate',onPop);return()=>window.removeEventListener('popstate',onPop)},[]);
 const go=(next:string)=>{if(next===path)return;window.history.pushState({},'',next);setPath(next)};
 const current=nav.find(([,p])=>p===path);
 const label=current?.[0]||'NayaNET';
 return <div className="app" data-shell-owner="AppShell" data-route={path} data-runtime-marker="NAYANET-HUB-REACT-CANONICAL"><aside className="sidebar"><div className="brand"><div className="logo">N</div><div><b>NayaNET</b><small>INTELLIGENT HUB</small></div></div><div className="navlabel">NETWORK</div><nav className="nav" aria-label="NayaNET navigation">{nav.map(([name,route,icon])=><button key={route} className={path===route?'active':''} onClick={()=>go(route)} aria-current={path===route?'page':undefined}><span className="ico">{icon}</span>{name}</button>)}</nav><div className="sidefoot"><b>PRIVATE BY DEFAULT</b>Shared by choice · Collective by consent · Public by decision</div></aside>
  <main className="main"><header className="topbar"><div className="crumb"><strong>{label}</strong><span> / NayaNET Intelligence</span></div><div className="topright"><div className="identity"><b>{id.smart_name}</b><span>@{id.smart_alias}</span></div></div></header><section className="home">{children(path)}</section></main>
 </div>
}
