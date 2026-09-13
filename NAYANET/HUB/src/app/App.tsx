import { useEffect, useMemo, useState } from 'react';
import type { IntelligentEvent, Lens, Perspective } from '../intelligence/types';
import { loadPrimaryIntelligence, sortPrimaryIntelligence } from '../data/pis';

type LayerKey='nutshell'|'human'|'child'|'grandma'|'naya'|'machine'|'learning'|'meaning'|'value';
type ActionKey='favorite'|'save'|'love'|'like'|'rate'|'share';
const tones=['silver','magenta','indigo','sapphire','emerald','lime','yellow','gold','orange','red'];
const ecosystem=['HOME','NAYA POWER','5 DAY CHALLENGE','ENTER FREE','POWERCASTS','WHITE PAPER','ABOUT US','HMC LOGIN'];
const nav=['YOUR INTELLIGENCE TODAY','YOUR REPORT','INTELLIGENCE LIBRARY','SMART LISTS','SMART SHARE','SMART SPACES','CONNECTIONS','SMART MAIL','SETTINGS'];
const lensLabels:Record<Lens,string>={collective:'SMART SHARE',activity:'ACTIVITY',personal:'PERSONAL'};
const lensQuestions:Record<Lens,string>={collective:'WHAT VALUABLE INTELLIGENCE EXISTS FOR US?',activity:'WHAT HAPPENED?',personal:'WHAT MATTERS TO YOU?'};
const clean=(v?:string,fallback='')=>v?.replace(/\s+/g,' ').trim()||fallback;
const first=(e:IntelligentEvent,t:Perspective['tone'])=>e.perspectives.find(p=>p.tone===t)?.body||'';
const storage=(k:string)=>{try{return JSON.parse(localStorage.getItem(k)||'[]') as string[]}catch{return[]}};
const toggle=(key:string,id:string)=>{const current=storage(key);const next=current.includes(id)?current.filter(x=>x!==id):[...current,id];localStorage.setItem(key,JSON.stringify(next));return next.includes(id)};
const meaningLine=(e:IntelligentEvent)=>clean(e.meaning.significance||e.meaning.text,'This intelligence is connected to a larger decision, action or learning path.');
const isActivity=(e:IntelligentEvent)=>Boolean(e.action.status||e.machine_evidence.items?.length||/system|event|adapter/i.test(clean(e.source.type)));

function layers(e:IntelligentEvent):Record<LayerKey,{label:string;body:string;tone:string}>{return{
 nutshell:{label:'IN A NUTSHELL',body:clean(e.naya_interpretation.observation,e.weaver_synthesis.summary||e.source.label),tone:'silver'},
 human:{label:'HUMAN NOTE',body:clean(e.human_input.raw,'No human note recorded.'),tone:'magenta'},
 child:{label:'CHILD VIEW',body:clean(first(e,'child'),'A simpler view is not yet available.'),tone:'indigo'},
 grandma:{label:'GRABBER VIEW',body:clean(first(e,'grandma'),'A plain-language view is not yet available.'),tone:'sapphire'},
 naya:{label:'NAYA NOTE',body:clean(e.naya_interpretation.interpretation||first(e,'naya'),'Naya interpretation is still being resolved.'),tone:'emerald'},
 machine:{label:'MACHINE NOTE',body:clean(first(e,'machine'),'Structured machine context is preserved upstream.'),tone:'blue'},
 learning:{label:'ADAPTER LEARNING',body:clean(e.lesson.text,'Learning has not yet been recorded.'),tone:'lime'},
 meaning:{label:'WHAT IT MEANS',body:clean(e.meaning.text||e.meaning.significance,'Meaning is still being resolved.'),tone:'yellow'},
 value:{label:"WHAT'S IN IT FOR YOU",body:clean(e.whats_in_it_for_you,'Translate this intelligence into useful human value.'),tone:'gold'}
}};
function truth(e:IntelligentEvent){return clean(e.machine_evidence.verification_state,e.status).toUpperCase()}
function truthClass(e:IntelligentEvent){return truth(e).toLowerCase().replace(/[^a-z]+/g,'-')}

function Consequence({text}:{text:string}){return <div className="feed-consequence" role="status"><span>✓</span><div><b>INTELLIGENCE STATE CHANGED</b><p>{text}</p></div></div>}

function FeedCard({event,index,onOpen,lens}:{event:IntelligentEvent;index:number;onOpen:()=>void;lens:Lens}){
 const data=layers(event); const [open,setOpen]=useState<LayerKey>('nutshell');
 const [saved,setSaved]=useState(()=>storage('nayanet:saved-intelligence').includes(event.event_id));
 const [favorite,setFavorite]=useState(()=>storage('nayanet:favorites').includes(event.event_id));
 const [liked,setLiked]=useState(()=>storage('nayanet:likes').includes(event.event_id));
 const [loved,setLoved]=useState(()=>storage('nayanet:loves').includes(event.event_id));
 const [rated,setRated]=useState(()=>storage('nayanet:rated').includes(event.event_id));
 const [consequence,setConsequence]=useState('');
 const tone=tones[index%tones.length];
 const act=(key:ActionKey)=>{const map:Record<ActionKey,[string,(v:boolean)=>void]>= {
  favorite:['nayanet:favorites',setFavorite],save:['nayanet:saved-intelligence',setSaved],like:['nayanet:likes',setLiked],love:['nayanet:loves',setLoved],rate:['nayanet:rated',setRated],share:['',()=>{}]};
  if(key==='share'){const text=`${event.source.label}\n\n${data.nutshell.body}`;if(navigator.share)navigator.share({title:event.source.label,text}).catch(()=>{});else navigator.clipboard?.writeText(text);setConsequence('Intelligence prepared for sharing.');return}
  const [store,setter]=map[key];const active=toggle(store,event.event_id);setter(active);setConsequence(active?`${key.toUpperCase()} recorded on this intelligence.`:`${key.toUpperCase()} removed from this intelligence.`)
 };
 const visibleActions=lens==='collective'?['favorite','save','rate','share','love','like']:['favorite','save','share'];
 return <article className={`feed-card tone-${tone} ${consequence?'has-consequence':''}`}>
  <div className="feed-card-top"><div className="feed-source"><span>✦</span><b>{clean(event.source.type,'NAYA').toUpperCase()}</b><i>·</i><span>{clean(event.context.topic,'INTELLIGENCE')}</span></div><div className={`feed-truth truth-${truthClass(event)}`}><span/>{truth(event)}</div></div>
  <button className="feed-main" onClick={onOpen} aria-label={`Explore ${event.source.label}`}><span className="feed-label">{data.nutshell.label}</span><h2>{clean(event.weaver_synthesis.summary,event.source.label)}</h2><p>{data.nutshell.body}</p></button>
  <div className="feed-answer-rail"><span>WHY IT MATTERS</span><p>{meaningLine(event)}</p></div>
  <div className="feed-tabs" role="tablist" aria-label="Intelligence lenses">{(Object.keys(data) as LayerKey[]).map(k=><button key={k} role="tab" aria-selected={open===k} className={open===k?'active':''} onClick={()=>setOpen(k)}>{data[k].label}</button>)}</div>
  <div className={`feed-layer layer-${data[open].tone}`}><div className="layer-title">{data[open].label}</div><p>{data[open].body}</p></div>
  <div className="feed-next"><div><span>NEXT ACTION</span><b>{clean(event.action.text,'Understand this intelligence and decide what to do next.')}</b></div><div><span>PROVENANCE</span><b>{clean(event.source.type,'NAYA')} · {new Date(event.created_at).toLocaleDateString()}</b></div></div>
  <footer className="feed-meta"><div><span>{(event.context.tags||[]).slice(0,3).join(' · ')}</span><small>{event.event_id}</small></div><div className="feed-actions"><button onClick={onOpen}>EXPLORE</button>{visibleActions.map(k=><button key={k} className={((k==='save'&&saved)||(k==='favorite'&&favorite)||(k==='like'&&liked)||(k==='love'&&loved)||(k==='rate'&&rated))?'chosen':''} onClick={()=>act(k as ActionKey)}>{k==='favorite'?(favorite?'★ FAVORITED':'☆ FAVORITE'):k==='save'?(saved?'SAVED':'SAVE'):k.toUpperCase()}</button>)}</div></footer>
  {consequence&&<Consequence text={consequence}/>} 
 </article>
}

function LeftRail({lens,setLens,counts}:{lens:Lens;setLens:(l:Lens)=>void;counts:Record<Lens,number>}){return <aside className="feed-left-rail"><div className="rail-title">INTELLIGENCE PROJECTIONS <span>LIVE</span></div><div className="rail-orb"><b>{counts[lens]}</b><i/><i/><i/></div>{(['collective','activity','personal'] as Lens[]).map(k=><button key={k} className={`rail-lens ${lens===k?'active':''}`} onClick={()=>setLens(k)}><span>{k==='activity'?'◷':k==='personal'?'◇':'◈'}</span><div><b>{lensLabels[k]}</b><small>{k==='activity'?'What happened':k==='personal'?'What matters to you':'What valuable intelligence exists for us'}</small></div><em>{counts[k]}</em></button>)}<div className="rail-rule"/><button className="rail-link">⌕ <b>SEARCH INTELLIGENCE</b></button><button className="rail-link">◌ <b>SMART SPACES</b></button><button className="rail-link">▦ <b>INTELLIGENCE LIBRARY</b></button><div className="rail-presence"><span/><div><b>NAYA IS PRESENT</b><small>Finding, connecting, verifying and surfacing what matters.</small></div></div></aside>}

function RightRail({event}:{event?:IntelligentEvent}){const t=event?truth(event):'WAITING';return <aside className="feed-right-rail"><div className="naya-card"><div className="naya-card-top"><span className="naya-mark">N</span><div><span>NAYA</span><b>TRUSTED THINKING PARTNER</b></div><i>● PRESENT</i></div><p>{event?'I found something worth understanding. Go deeper through the intelligence lenses, then act if it earns action.':'I am following the intelligence loop and watching for what matters next.'}</p><div className="naya-state"><span>●</span>{event?'UNDERSTANDING':'WATCHING'}</div><button>ASK NAYA</button></div><div className="right-card"><span>TRUTH STATE</span><b>{t}</b><p>{event?'Fact, observation and Naya interpretation remain visibly distinct.':'Select intelligence to inspect its truth state.'}</p></div><div className="right-card"><span>INTELLIGENCE SPINE</span><b>SOURCE → UNDERSTAND → ACT</b><p>Then RESULT → VERIFY → LEARN → NEW INTELLIGENCE.</p></div>{event&&<div className="right-card"><span>PROVENANCE</span><b>{clean(event.source.type,'NAYA').toUpperCase()}</b><p>Created {new Date(event.created_at).toLocaleString()} · {clean(event.privacy.visibility,'UNKNOWN')}</p></div>}</aside>}

function SmartFeed(){const [events,setEvents]=useState<IntelligentEvent[]>([]);const[lens,setLens]=useState<Lens>('collective');const[query,setQuery]=useState('');const[loading,setLoading]=useState(true);const[selected,setSelected]=useState<IntelligentEvent>();
 useEffect(()=>{let live=true;loadPrimaryIntelligence().then(p=>{if(live)setEvents(sortPrimaryIntelligence(p.events))}).catch(()=>{}).finally(()=>{if(live)setLoading(false)});return()=>{live=false}},[]);
 const counts=useMemo(()=>({collective:events.filter(e=>e.privacy.visibility!=='PRIVATE').length,personal:events.filter(e=>e.privacy.visibility==='PRIVATE').length,activity:events.filter(isActivity).length}),[events]);
 const visible=useMemo(()=>{let list=events;if(lens==='personal')list=list.filter(e=>e.privacy.visibility==='PRIVATE');if(lens==='activity')list=list.filter(isActivity);if(lens==='collective')list=list.filter(e=>e.privacy.visibility!=='PRIVATE');const q=query.trim().toLowerCase();if(!q)return list;return list.filter(e=>[e.source.label,e.human_input.raw,e.naya_interpretation.observation||'',e.naya_interpretation.interpretation||'',e.meaning.text||'',e.whats_in_it_for_you||'',e.action.text||'',...(e.context.tags||[])].join(' ').toLowerCase().includes(q))},[events,lens,query]);
 if(selected)return <div className="feed-detail"><button className="back-button" onClick={()=>setSelected(undefined)}>← BACK TO INTELLIGENCE</button><div className="feed-detail-grid"><div><FeedCard event={selected} index={0} lens={lens} onOpen={()=>{}}/></div><RightRail event={selected}/></div></div>;
 return <div className="hub509-live"><section className="feed-hero"><div><span>LIVING INTELLIGENCE · ONE OBJECT, MANY PROJECTIONS</span><h1>Intelligence,<br/><em>made useful.</em></h1><p>The Smart Feed turns real intelligence into something you can understand, explore, act on, verify and learn from. This is not a stream of posts. It is the human presentation layer of the intelligence system.</p><div className="feed-hero-proof"><span>WHAT → WHY → MEANING → VALUE → ACTION</span><b>ONE INTELLIGENCE · MANY LENSES</b></div></div><div className="feed-hero-mark"><b>∞</b><span>NAYA LOOP</span></div></section>
 <div className="feed-search"><span>⌕</span><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search the intelligence…"/><kbd>⌘ K</kbd><small>{loading?'RESTORING…':'CANONICAL SOURCE CONNECTED'}</small></div>
 <div className="feed-layout"><LeftRail lens={lens} setLens={setLens} counts={counts}/><main className="smart-feed-stage"><div className="stage-line"><div><span>{lensLabels[lens]}</span><b>{query?`${visible.length} MATCHES`:`${visible.length} INTELLIGENT OBJECTS`}</b></div><p>{lensQuestions[lens]}</p></div>{loading?<div className="feed-loading"><span className="loading-orbit"/><b>Restoring canonical intelligence…</b><p>Naya is reconnecting the human presentation layer to the intelligence source.</p></div>:visible.length?visible.map((event,i)=><FeedCard key={event.event_id} event={event} index={i} lens={lens} onOpen={()=>setSelected(event)}/>):<div className="feed-loading"><b>NO INTELLIGENCE IN THIS PROJECTION</b><p>No dead end: change the projection or search for another relationship.</p></div>}</main><RightRail event={undefined}/></div></div>}

export default function App(){const[active,setActive]=useState('YOUR INTELLIGENCE TODAY');const[ecosystemActive,setEcosystemActive]=useState('HOME');return <div className="hub509"><aside className="side509"><button className="brand509" onClick={()=>setActive('YOUR INTELLIGENCE TODAY')}><span className="n-mark">N</span><span><b>NayaNET</b><small>INTELLIGENT HUB</small></span></button><div className="nav-caption">YOUR INTELLIGENCE</div><nav>{nav.map((item,i)=><button key={item} className={active===item?'active':''} onClick={()=>setActive(item)}><span>{['◷','▤','▦','◎','◈','◌','↔','✉','⚙'][i]}</span>{item}{item==='YOUR INTELLIGENCE TODAY'&&<em>LIVE</em>}</button>)}</nav><div className="side-bottom"><b>PRIVATE BY DEFAULT</b><span>Shared by choice · Collective by consent</span></div></aside><main className="stage509"><header className="top509"><div className="ecosystem-nav">{ecosystem.map(item=><button key={item} className={ecosystemActive===item?'active':''} onClick={()=>setEcosystemActive(item)}>{item}</button>)}</div><div className="top-search"><span>⌕</span><span>Search or talk to Naya…</span><kbd>⌘ K</kbd><button>ASK NAYA</button></div><div className="top-state"><span className="live-dot"/>NAYA ONLINE</div></header><SmartFeed/></main></div>}
