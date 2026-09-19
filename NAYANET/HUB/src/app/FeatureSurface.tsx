import { useEffect, useState } from 'react';
import { supabase, useIdentity } from '../identity/session';

type SurfaceKey='ledger'|'mail'|'spaces'|'lists'|'share'|'connections'|'reports'|'today';
type Row=Record<string,unknown>;
const cfg:Record<SurfaceKey,{title:string;subtitle:string;table:string;order:string;empty:string}>={
 ledger:{title:'Smart Ledger',subtitle:'Canonical record of meaningful intelligence and authorized action.',table:'nayanet_smart_ledger',order:'event_at',empty:'No Ledger events are visible for this identity yet.'},
 mail:{title:'Smart Mail',subtitle:'Authorized intelligence moving between people through the canonical Mail path.',table:'v7_mail_messages',order:'created_at',empty:'No Mail messages are visible for this identity yet.'},
 spaces:{title:'Smart Spaces',subtitle:'Permissioned places where intelligence can be shared and compounded.',table:'nayanet_spaces',order:'created_at',empty:'No Smart Spaces are visible for this identity yet.'},
 lists:{title:'Smart Lists',subtitle:'Actionable intelligence organized around real connections.',table:'nayanet_smart_lists',order:'created_at',empty:'No Smart Lists are visible for this identity yet.'},
 share:{title:'Smart Share',subtitle:'Consent-bound publication of intelligence from the canonical source.',table:'nayanet_intelligence_publications',order:'published_at',empty:'No shared intelligence is visible for this identity yet.'},
 connections:{title:'Your Connections',subtitle:'Canonical relationships available to the authenticated identity.',table:'nayanet_connections',order:'created_at',empty:'No Connections are visible for this identity yet.'},
 reports:{title:'Your Reports',subtitle:'Reports derived from canonical intelligence rather than a second source of truth.',table:'v7_intelligence_reports',order:'created_at',empty:'No Intelligence Reports are visible for this identity yet.'},
 today:{title:'Your Intelligence Today',subtitle:'A live summary of the canonical intelligence system available now.',table:'nayanet_intelligence_index',order:'event_time',empty:'No canonical intelligence is visible for this identity yet.'},
};

function label(v:unknown){return typeof v==='string'?v:String(v??'');}
function pretty(v:unknown){if(v==null)return '—'; if(typeof v==='object')return JSON.stringify(v); return String(v);}

export function FeatureSurface({kind}:{kind:SurfaceKey}){
 const id=useIdentity(); const c=cfg[kind]; const [rows,setRows]=useState<Row[]>([]); const [error,setError]=useState(''); const [busy,setBusy]=useState(true);
 useEffect(()=>{let alive=true;setBusy(true);setError('');
   if(!id.is_authenticated){setRows([]);setBusy(false);return;}
   (async()=>{const result=await supabase.from(c.table).select('*').order(c.order,{ascending:false}).limit(25);
     if(!alive)return; if(result.error){setError(result.error.message);setRows([]);}else setRows((result.data||[]) as Row[]);setBusy(false);
   })().catch(e=>{if(alive){setError(e instanceof Error?e.message:'SURFACE_LOAD_FAILED');setBusy(false);}});
   return()=>{alive=false};
 },[id.is_authenticated,c.table,c.order]);
 const fields=rows.length?Object.keys(rows[0]).filter(k=>!['metadata','verification','value','outcome','evidence_refs','learning_refs','report'].includes(k)).slice(0,8):[];
 return <section className="feature-surface">
   <div className="feature-hero"><div><div className="eyebrow">NAYANET · CANONICAL SYSTEM SURFACE</div><h1>{c.title}</h1><p>{c.subtitle}</p></div><div className="feature-state">{id.is_authenticated?'AUTHENTICATED':'AUTHENTICATION REQUIRED'} · {rows.length} RECORDS</div></div>
   {!id.is_authenticated ? <div className="feature-empty"><b>AUTHENTICATION REQUIRED</b><span>Sign in through the normal NayaNET identity surface to access this private system data. No browser session is fabricated.</span></div>
   : busy ? <div className="feature-empty"><b>LOADING CANONICAL STATE…</b></div>
   : error ? <div className="feature-empty"><b>SYSTEM READ FAILED</b><span>{error}</span></div>
   : !rows.length ? <div className="feature-empty"><b>{c.title.toUpperCase()} IS READY</b><span>{c.empty}</span></div>
   : <div className="feature-table" role="table"><div className="feature-table-head">{fields.map(f=><span key={f}>{f.replaceAll('_',' ').toUpperCase()}</span>)}</div>{rows.map((row,i)=><article className="feature-row" key={label(row.id||row.ledger_event_id||i)}>{fields.map(f=><span key={f}>{pretty(row[f])}</span>)}</article>)}</div>}
   <div className="feature-foot"><span>CANONICAL SOURCE</span><b>{c.table}</b><span>•</span><span>PRIVATE BY DEFAULT · SHARED BY CHOICE</span></div>
 </section>;
}
