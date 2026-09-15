import {useEffect,useMemo,useState} from 'react';
import type {ReactNode} from 'react';
import {IdentityProvider,useIdentity} from '../identity/session';
import {AuthPanel} from '../identity/AuthPanel';
import type {IntelligentEvent,Lens} from '../intelligence/types';
import {SmartFeedBoard} from '../intelligence/SmartFeedBoard';
import {initializeCognition} from '../intelligence/cognition';
import {loadPrimaryIntelligence,sortPrimaryIntelligence,type PISFeed} from '../data/pis';
import {AppShellV3} from './AppShellV3';
import {routes} from './routes';

type LensTab={key:Lens;label:string;detail:string;icon:string};
const lensTabs:LensTab[]=[
 {key:'collective',label:'COLLECTIVE',detail:'Shared intelligence worth discovering',icon:'◎'},
 {key:'activity',label:'ACTIVITY',detail:'What Naya and the system are doing',icon:'◷'},
 {key:'personal',label:'PERSONAL',detail:'Your private intelligence and saves',icon:'◉'}
];
const routeLens=(path:string):Lens=>path===routes.today?'activity':path===routes.collective?'collective':path===routes.notes?'personal':'collective';
const compact=(value:string|undefined,fallback:string)=>value?.trim()||fallback;

function IntelligenceCard({event,onOpen}:{event:IntelligentEvent;onOpen:()=>void}){
 const summary=compact(event.weaver_synthesis.summary,event.source.label);
 const nutshell=compact(event.naya_interpretation.observation,event.human_input.raw);
 const meaning=compact(event.meaning.text||event.meaning.significance,'Meaning is not yet recorded.');
 const value=compact(event.whats_in_it_for_you,'Human value is not yet recorded.');
 const evidence=event.machine_evidence.verification_state||event.status;
 return <button className="intel-card" onClick={onOpen} aria-label={`Open ${event.source.label}`}>
  <div className="intel-card-top"><span className="intel-source">{event.source.type.replaceAll('_',' ').toUpperCase()} · INTELLIGENCE</span><span className="intel-state">{evidence.toUpperCase()}</span></div>
  <h3>{summary}</h3><p className="intel-nutshell">{nutshell}</p>
  <div className="intel-meta"><span className="intel-chip">{event.context.topic||'NayaNET'}</span>{(event.context.tags||[]).slice(0,3).map(tag=><span className="intel-chip" key={tag}>{tag}</span>)}<span className="intel-chip">{new Date(event.created_at).toLocaleDateString()}</span></div>
  <div className="intel-footer"><div className="intel-mini"><span>WHY IT MATTERS</span><p>{meaning}</p></div><div className="intel-mini"><span>WHAT'S IN IT FOR YOU</span><p>{value}</p></div><div className="intel-mini"><span>NAYA / NEXT</span><p>{compact(event.action.text,'Open the intelligence to inspect the next action.')}</p></div></div>
 </button>
}

function CommandCenter({initialLens='collective'}:{initialLens?:Lens}){
 const identity=useIdentity();
 const [events,setEvents]=useState<IntelligentEvent[]>([]);
 const [feed,setFeed]=useState<PISFeed>();
 const [error,setError]=useState('');
 const [lens,setLens]=useState<Lens>(initialLens);
 const [query,setQuery]=useState('');
 const [selected,setSelected]=useState<IntelligentEvent>();
 useEffect(()=>setLens(initialLens),[initialLens]);
 useEffect(()=>{let alive=true;setError('');loadPrimaryIntelligence().then(value=>{if(!alive)return;setFeed(value);setEvents(sortPrimaryIntelligence(value.events));}).catch(reason=>{if(alive)setError(reason instanceof Error?reason.message:'PIS_FEED_UNAVAILABLE')});return()=>{alive=false}},[identity.is_authenticated]);
 useEffect(()=>{const handler=(event:Event)=>{const q=(event as CustomEvent<{query?:string}>).detail?.query||'';setQuery(q);setSelected(undefined)};addEventListener('nayanet:search',handler);return()=>removeEventListener('nayanet:search',handler)},[]);
 const filtered=useMemo(()=>{const q=query.trim().toLowerCase();if(!q)return events;return events.filter(event=>[event.source.label,event.human_input.raw,event.context.topic,...(event.context.tags||[]),event.naya_interpretation.observation||'',event.naya_interpretation.interpretation||'',event.meaning.text||'',event.action.text||'',event.whats_in_it_for_you||''].join(' ').toLowerCase().includes(q))},[events,query]);
 const counts={collective:events.length,activity:events.length,personal:events.length};
 const activeTab=lensTabs.find(tab=>tab.key===lens)!;
 if(selected)return <div className="hub-command"><button className="hub-back" onClick={()=>setSelected(undefined)}>← BACK TO {activeTab.label}</button><div className="hub-detail"><SmartFeedBoard event={selected}/></div></div>;
 return <div className="hub-command">
  <header className="hub-command-head"><div className="hub-command-title"><div className="eyebrow">NAYANET · LIVING INTELLIGENCE NETWORK</div><h1>{activeTab.label.charAt(0)+activeTab.label.slice(1).toLowerCase()} Intelligence</h1><p>{activeTab.detail}. One intelligence object, many views — discover the signal first, then open the depth.</p></div><div className="hub-live"><i/>LIVE PIS · {feed?.source==='supabase:nayanet_intelligence_index'?'PERSISTENT':'BUILD'} · {events.length} OBJECTS</div></header>
  <div className="hub-lensbar" role="tablist" aria-label="Smart feeds">{lensTabs.map(tab=><button key={tab.key} role="tab" aria-selected={lens===tab.key} className={`hub-lens ${lens===tab.key?'active':''}`} onClick={()=>setLens(tab.key)}><b>{tab.icon} {tab.label} FEED</b><span>{tab.detail} · {counts[tab.key]}</span></button>)}</div>
  <div className="hub-search"><span>⌕</span><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search intelligence, people, topics, meaning, evidence…" aria-label="Search NayaNET intelligence"/><kbd>⌘ K</kbd></div>
  <div className="hub-workspace"><section className="hub-stream"><div className="hub-stream-head"><h2>{query?`Search results for “${query}”`:'Living intelligence'}</h2><span>{filtered.length} {filtered.length===1?'object':'objects'} · click any block to open full intelligence</span></div>{error?<div className="hub-empty"><b>INTELLIGENCE FEED UNAVAILABLE</b>{error}</div>:filtered.length?<div className="hub-results">{filtered.map(event=><IntelligenceCard key={event.event_id} event={event} onOpen={()=>setSelected(event)}/>)}</div>:<div className="hub-empty"><b>{query?'NO INTELLIGENCE MATCHES':'NO INTELLIGENCE YET'}</b><span>{query?'Try a different word or topic.':'The Hub is waiting for a canonical intelligence event.'}</span></div>}</section>
  <aside className="hub-rail"><section className="hub-rail-card"><div className="hub-rail-label">NAYA · NOW</div><h3>{events[0]?compact(events[0].source.label,'Intelligence is flowing.'):'Waiting for intelligence.'}</h3><p>{events[0]?compact(events[0].naya_interpretation.observation,'A canonical event is available to explore.'):'The Hub will not fabricate a feed when the upstream intelligence source is empty.'}</p><div className="hub-next"><i>✦</i><span>{events[0]?compact(events[0].action.text,'Open the newest block and inspect what happens next.'):'Next: capture a canonical intelligence event.'}</span></div></section><section className="hub-rail-card"><div className="hub-rail-label">INTELLIGENCE LOOP</div><div className="hub-rail-value">CAPTURE → COMPOUND</div><p>Discover → understand → connect → act → verify → learn. The feed is the living projection of that loop.</p></section><section className="hub-rail-card"><div className="hub-rail-label">TRUST SURFACE</div><h3>{events.filter(e=>e.machine_evidence.verification_state==='VERIFIED').length} verified</h3><p>Verification is a truth state, not a colour. Open any block for source, evidence, uncertainty and provenance.</p></section></aside></div>
 </div>
}

function Workspace({path}:{path:string}):ReactNode{if(path===routes.settings)return <AuthPanel/>;return <CommandCenter initialLens={routeLens(path)}/>}
export default function App(){useEffect(()=>{initializeCognition().catch(()=>{})},[]);return <IdentityProvider><AppShellV3>{path=><Workspace path={path}/>}</AppShellV3></IdentityProvider>}
