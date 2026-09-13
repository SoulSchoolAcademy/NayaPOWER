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

type LensDef={key:Lens;label:string;sub:string;glyph:string};
const LENSES:LensDef[]=[
 {key:'collective',label:'COLLECTIVE',sub:'Shared intelligence',glyph:'◈'},
 {key:'activity',label:'ACTIVITY',sub:'What is happening',glyph:'◷'},
 {key:'personal',label:'PERSONAL',sub:'Your intelligence',glyph:'◇'}
];
const routeLens=(path:string):Lens=>path===routes.today?'activity':path===routes.notes?'personal':path===routes.collective?'collective':'collective';
const text=(v:string|undefined,fallback:string)=>v?.trim()||fallback;
const upper=(v:string|undefined,fallback:string)=>text(v,fallback).toUpperCase();

function SignalBar({event,lens,count}:{event?:IntelligentEvent;lens:Lens;count:number}){
 const state=upper(event?.machine_evidence.verification_state||event?.status,'READY');
 const topic=text(event?.context.topic,'NayaNET intelligence');
 return <section className="signal-bar">
  <div className="signal-main"><span className="signal-kicker">{lens.toUpperCase()} · LIVING FIELD</span><strong>{event?text(event.weaver_synthesis.summary,event.source.label):'The intelligence field is ready.'}</strong><span>{event?text(event.naya_interpretation.observation,'Canonical intelligence is available to explore.'): 'Canonical intelligence will appear here as it is captured.'}</span></div>
  <div className="signal-stats"><div><b>{count}</b><small>OBJECTS</small></div><div><b>{state}</b><small>TRUTH STATE</small></div><div><b>{topic}</b><small>ACTIVE SIGNAL</small></div></div>
 </section>
}

function LensRail({lens,setLens,events}:{lens:Lens;setLens:(l:Lens)=>void;events:IntelligentEvent[]}){
 const count=(l:Lens)=>l==='personal'?events.filter(e=>e.privacy.visibility==='PRIVATE').length:l==='collective'?events.filter(e=>e.privacy.visibility!=='PRIVATE').length:events.length;
 return <nav className="lens-rail" aria-label="Intelligence lenses">
  <div className="lens-rail-head"><span>INTELLIGENCE</span><i>LIVE</i></div>
  <div className="lens-rail-orbit" aria-hidden="true"><span/><span/><span/></div>
  {LENSES.map(item=><button key={item.key} className={`lens-tab ${lens===item.key?'active':''}`} onClick={()=>setLens(item.key)} aria-current={lens===item.key?'page':undefined}><span className="lens-glyph">{item.glyph}</span><span className="lens-copy"><b>{item.label}</b><small>{item.sub}</small></span><em>{count(item.key)}</em></button>)}
  <div className="lens-divider"/>
  <button className="rail-tool" onClick={()=>dispatchEvent(new CustomEvent('nayanet:search',{detail:{query:''}}))}><span>⌕</span><b>DISCOVER</b></button>
  <button className="rail-tool" onClick={()=>dispatchEvent(new CustomEvent('nayanet:navigate',{detail:{path:routes.space}}))}><span>◌</span><b>SMART SPACES</b></button>
  <button className="rail-tool" onClick={()=>dispatchEvent(new CustomEvent('nayanet:navigate',{detail:{path:routes.library}}))}><span>▦</span><b>LIBRARY</b></button>
  <div className="rail-bottom"><span className="pulse-dot"/><div><b>NAYA IS PRESENT</b><small>Watching the intelligence loop</small></div></div>
 </nav>
}

function IntelligenceBlock({event,index,onOpen}:{event:IntelligentEvent;index:number;onOpen:()=>void}){
 const accent=['silver','magenta','purple','indigo','sapphire','blue','emerald','lime','yellow','gold','orange','red'][index%12];
 const state=upper(event.machine_evidence.verification_state||event.status,'UNKNOWN');
 const title=text(event.weaver_synthesis.summary,event.source.label);
 const nutshell=text(event.naya_interpretation.observation,event.human_input.raw);
 const meaning=text(event.meaning.text||event.meaning.significance,'Meaning has not yet been recorded.');
 const value=text(event.whats_in_it_for_you,'Human value has not yet been recorded.');
 const next=text(event.action.text,'Open this intelligence to inspect the next action.');
 const learning=text(event.lesson.text,'Learning has not yet been recorded.');
 return <article className={`intelligence-block edge-${accent}`}>
  <div className="block-glow" aria-hidden="true"/>
  <div className="block-head">
   <div className="block-origin"><span className="origin-mark">✦</span><span>{upper(event.source.type,'NAYA')} · {upper(event.source.label,'INTELLIGENCE')}</span></div>
   <div className="block-truth"><i/>{state}</div>
  </div>
  <button className="block-open" onClick={onOpen} aria-label={`Open ${title}`}>
   <div className="block-featured"><span className="section-label">IN A NUTSHELL</span><h2>{title}</h2><p>{nutshell}</p></div>
   <div className="block-ribbon"><span>{text(event.context.topic,'NAYANET')}</span>{(event.context.tags||[]).slice(0,3).map(t=><span key={t}>{t}</span>)}<span>{new Date(event.created_at).toLocaleDateString()}</span></div>
   <div className="block-depth">
    <div className="depth-panel human"><span>HUMAN NOTE</span><p>{text(event.human_input.raw,'No human note recorded.')}</p></div>
    <div className="depth-panel naya"><span>NAYA NOTE</span><p>{text(event.naya_interpretation.interpretation||event.naya_interpretation.recommendation,'Naya has not added an interpretation.')}</p></div>
    <div className="depth-panel learning"><span>ADAPTER LEARNING</span><p>{learning}</p></div>
    <div className="depth-panel meaning"><span>WHAT IT MEANS</span><p>{meaning}</p></div>
    <div className="depth-panel value"><span>WHAT'S IN IT FOR YOU</span><p>{value}</p></div>
    <div className="depth-panel action"><span>NEXT ACTION</span><p>{next}</p></div>
   </div>
  </button>
  <div className="block-footer">
   <div className="provenance"><span>PROVENANCE</span><b>{event.event_id.slice(0,12)}…</b><i>·</i><b>{upper(event.privacy.visibility,'UNKNOWN')}</b></div>
   <div className="block-actions"><button onClick={onOpen}>EXPLORE <span>↗</span></button><button onClick={onOpen}>SAVE</button><button onClick={onOpen}>SHARE</button></div>
  </div>
 </article>
}

function NayaPulse({event}:{event?:IntelligentEvent}){
 if(!event)return <aside className="naya-panel empty"><div className="naya-orb"><span>✦</span></div><div className="naya-eyebrow">NAYA · READY</div><h2>The field is waiting.</h2><p>No intelligence is fabricated. When the canonical source speaks, Naya will surface what matters.</p><div className="naya-next"><span>→</span><b>Next: capture intelligence</b></div></aside>;
 return <aside className="naya-panel">
  <div className="naya-panel-top"><div className="naya-orb"><span>✦</span></div><div><div className="naya-eyebrow">NAYA · NOW</div><b>INTELLIGENCE SIGNAL</b></div><i className="naya-live">LIVE</i></div>
  <h2>{text(event.source.label,'Something is moving.')}</h2>
  <p className="naya-observation">{text(event.naya_interpretation.observation,event.human_input.raw)}</p>
  <div className="naya-sections"><div><span>WHY IT MATTERS</span><p>{text(event.meaning.text||event.meaning.significance,'The significance is still being resolved.')}</p></div><div><span>NAYA RECOMMENDS</span><p>{text(event.naya_interpretation.recommendation||event.action.text,'Open the intelligence and inspect the next move.')}</p></div></div>
  <div className="naya-proof"><div><span>TRUTH</span><b>{upper(event.machine_evidence.verification_state||event.status,'UNKNOWN')}</b></div><div><span>TRUST</span><b>{upper(event.trust.level,'UNKNOWN')}</b></div><div><span>EVIDENCE</span><b>{event.machine_evidence.items.length}</b></div></div>
  <button className="naya-open" onClick={()=>dispatchEvent(new CustomEvent('nayanet:open-intelligence',{detail:{eventId:event.event_id}}))}>OPEN NAYA'S VIEW <span>→</span></button>
 </aside>
}

function LoopRail({event}:{event?:IntelligentEvent}){
 const steps=['CAPTURE','DISTILL','ORGANIZE','REMEMBER','FIND','CONNECT','ACT','VERIFY','LEARN','COMPOUND'];
 return <section className="loop-panel"><div className="panel-eyebrow">INTELLIGENCE LOOP</div><div className="loop-title">Always becoming more useful.</div><div className="loop-track">{steps.map((s,i)=><span className={event&&i<7?'lit':''} key={s}>{s}</span>)}</div><div className="loop-foot"><span>NOW</span><b>{event?text(event.action.text,'Inspect the next action.'):'Waiting for the first canonical event.'}</b></div></section>
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
 useEffect(()=>{const search=(e:Event)=>{const q=(e as CustomEvent<{query?:string}>).detail?.query||'';setQuery(q);setSelected(undefined)};const open=(e:Event)=>{const id=(e as CustomEvent<{eventId?:string}>).detail?.eventId;const found=events.find(x=>x.event_id===id);if(found)setSelected(found)};addEventListener('nayanet:search',search);addEventListener('nayanet:open-intelligence',open);return()=>{removeEventListener('nayanet:search',search);removeEventListener('nayanet:open-intelligence',open)}},[events]);
 const visible=useMemo(()=>{const q=query.trim().toLowerCase();let base=events;if(lens==='personal')base=base.filter(e=>e.privacy.visibility==='PRIVATE');if(lens==='collective')base=base.filter(e=>e.privacy.visibility!=='PRIVATE');if(!q)return base;return base.filter(e=>[e.source.label,e.human_input.raw,e.context.topic,...(e.context.tags||[]),e.naya_interpretation.observation||'',e.naya_interpretation.interpretation||'',e.meaning.text||'',e.lesson.text||'',e.action.text||'',e.whats_in_it_for_you||''].join(' ').toLowerCase().includes(q))},[events,lens,query]);
 if(selected)return <div className="hub-experience"><button className="return-field" onClick={()=>setSelected(undefined)}>← RETURN TO {lens.toUpperCase()} INTELLIGENCE</button><div className="detail-shell"><SmartFeedBoard event={selected}/></div></div>;
 const newest=events[0];
 return <div className="hub-experience">
  <div className="hub-commandline"><div><span className="command-kicker">NAYANET / INTELLIGENT HUB</span><h1>{lens==='collective'?'The intelligence field':lens==='activity'?'What is happening now':'Your intelligence'}</h1></div><div className="field-status"><span className="field-led"/>SOURCE {feed?.source==='supabase:nayanet_intelligence_index'?'CONNECTED':'BUILD'}<i>·</i>{events.length} OBJECTS</div></div>
  <div className="hub-core"><LensRail lens={lens} setLens={setLens} events={events}/><main className="intelligence-stage"><SignalBar event={newest} lens={lens} count={visible.length}/><LoopRail event={newest}/><div className="stage-head"><div><span>INTELLIGENT BLOCKS</span><h2>{query?`Found ${visible.length} matching intelligence`:'Living intelligence'}</h2></div><p>{query?'Search is filtering the same intelligence objects.':'One object. Many views. Follow the signal into the depth.'}</p></div>{error?<div className="state-panel"><b>INTELLIGENCE SOURCE UNAVAILABLE</b><span>{error}</span></div>:visible.length?<div className="intelligence-stream">{visible.map((event,i)=><IntelligenceBlock key={event.event_id} event={event} index={i} onOpen={()=>setSelected(event)}/>)}</div>:<div className="state-panel"><div className="state-orb">✦</div><b>{query?'NO MATCHING INTELLIGENCE':'THE FIELD IS QUIET'}</b><span>{query?'Try another concept, topic, person, status, or meaning.':'The Hub will not invent intelligence while the canonical source is empty.'}</span></div>}</main><aside className="intelligence-aside"><NayaPulse event={newest}/><section className="aside-panel"><div className="panel-eyebrow">CONTINUITY</div><h3>What Naya knows now</h3><div className="continuity"><div><b>{events.filter(e=>e.machine_evidence.verification_state==='VERIFIED').length}</b><span>verified</span></div><div><b>{events.filter(e=>e.status==='BLOCKED').length}</b><span>blocked</span></div><div><b>{events.reduce((n,e)=>n+e.relationships.event_ids.length,0)}</b><span>connections</span></div></div><p>The Hub exposes state and relationships without pretending that activity itself is proof.</p></section><section className="aside-panel next-panel"><div className="panel-eyebrow">HUMAN VALUE</div><h3>{newest?text(newest.whats_in_it_for_you,'Value is being resolved.'):'Make intelligence useful.'}</h3><button onClick={()=>newest&&setSelected(newest)}>SEE THE VALUE <span>→</span></button></section></aside></div>
 </div>
}

function Workspace({path}:{path:string}):ReactNode{if(path===routes.settings)return <AuthPanel/>;return <CommandCenter initialLens={routeLens(path)}/>}
export default function App(){useEffect(()=>{initializeCognition().catch(()=>{})},[]);return <IdentityProvider><AppShellV3>{path=><Workspace path={path}/>}</AppShellV3></IdentityProvider>}
