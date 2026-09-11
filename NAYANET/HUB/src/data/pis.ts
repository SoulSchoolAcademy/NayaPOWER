import {createClient,type SupabaseClient} from '@supabase/supabase-js';
import type {IntelligentEvent} from '../intelligence/types';

export type PISFeed={schema_version:string;generated_at:string;source:string;event_count:number;events:IntelligentEvent[]};

type IndexRow={id:string;owner_id:string;source_table:string;source_id:string;object_type:string;title:string;event_time:string;created_at:string;updated_at:string;status:string|null;project_id:string|null;revision:number|null;metadata:Record<string,unknown>|null};

const PIS_URL='/intelligence/pis-feed.json';
const SUPABASE_URL=import.meta.env.VITE_SUPABASE_URL||'https://dahisasgpfvziswqvmvm.supabase.co';
const SUPABASE_KEY=import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY||'sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue';
const supabase:SupabaseClient=createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});

function indexRowToEvent(row:IndexRow):IntelligentEvent{
  const metadata=row.metadata||{};
  const sourceContext=(metadata.source_context&&typeof metadata.source_context==='object'?metadata.source_context:{}) as Record<string,unknown>;
  const privacy=typeof metadata.privacy_state==='string'?metadata.privacy_state:'PRIVATE BY DEFAULT';
  const status=row.status||'RECORDED';
  const topic=typeof sourceContext.topic==='string'?sourceContext.topic:row.title;
  const canonicalPath=typeof sourceContext.canonical_path==='string'?sourceContext.canonical_path:undefined;
  return {
    event_id:row.source_id,
    user_id:row.owner_id,
    created_at:row.created_at,
    updated_at:row.updated_at,
    source:{type:row.source_table==='smart_note_events'?'smart_note':row.source_table,label:row.title},
    human_input:{raw:row.title,captured_at:row.event_time},
    context:{topic,canonical_path:canonicalPath,tags:typeof sourceContext.tags==='string'?[sourceContext.tags]:Array.isArray(sourceContext.tags)?sourceContext.tags.filter((tag):tag is string=>typeof tag==='string'):[]},
    naya_interpretation:{observation:typeof metadata.event_type==='string'?metadata.event_type:undefined,uncertainty:'Runtime PIS projection exposes indexed metadata only; deeper interpretation remains attached to the canonical Smart Note.'},
    machine_evidence:{items:[`PERSISTENT_INDEX:${row.id}`,`SOURCE:${row.source_table}:${row.source_id}`,`STATUS:${status}`],verification_state:typeof metadata.verified_at==='string'?'VERIFIED':'RECORDED'},
    weaver_synthesis:{summary:row.title,relationships:[]},
    lesson:{text:typeof metadata.lesson==='string'?metadata.lesson:undefined,retained:false},
    meaning:{text:typeof metadata.meaning==='string'?metadata.meaning:undefined},
    action:{text:typeof metadata.action==='string'?metadata.action:undefined,status},
    relationships:{event_ids:[],connection_ids:[],space_ids:[]},
    privacy:{visibility:privacy,consent_state:privacy},
    trust:{level:typeof metadata.verified_at==='string'?'verified':'recorded',evidence_ids:[row.id]},
    status,
    perspectives:[{label:'NAYA',body:row.title,tone:'naya'},{label:'MACHINE',body:`Indexed ${row.source_table} event ${row.source_id}.`,tone:'machine'}]
  };
}

async function loadPersistentPIS():Promise<PISFeed|null>{
  const {data:{session}}=await supabase.auth.getSession();
  if(!session?.user?.id)return null;
  const {data,error}=await supabase.from('nayanet_intelligence_index').select('id,owner_id,source_table,source_id,object_type,title,event_time,created_at,updated_at,status,project_id,revision,metadata').eq('owner_id',session.user.id).order('event_time',{ascending:false}).limit(100);
  if(error)throw new Error(`PIS_DB_${error.code||'QUERY_FAILED'}`);
  const rows=(data||[]) as IndexRow[];
  const events=rows.filter(row=>row.source_table==='smart_note_events').map(indexRowToEvent);
  return {schema_version:'PIS-1.0',generated_at:new Date().toISOString(),source:'supabase:nayanet_intelligence_index',event_count:events.length,events};
}

async function loadBuildPIS():Promise<PISFeed>{
  const response=await fetch(PIS_URL,{cache:'no-store'});
  if(!response.ok)throw new Error(`PIS_FEED_HTTP_${response.status}`);
  const payload=(await response.json()) as PISFeed;
  if(!payload||!Array.isArray(payload.events))throw new Error('PIS_FEED_INVALID');
  return payload;
}

export async function loadPrimaryIntelligence():Promise<PISFeed>{
  try{
    const persistent=await loadPersistentPIS();
    if(persistent)return persistent;
  }catch(error){
    console.warn('PIS persistent transport unavailable; using verified build projection.',error);
  }
  return loadBuildPIS();
}

export function sortPrimaryIntelligence(events:IntelligentEvent[]):IntelligentEvent[]{
  return [...events].sort((a,b)=>Date.parse(b.created_at)-Date.parse(a.created_at));
}
