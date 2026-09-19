import { supabase } from '../identity/session';
import { SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from '../config/supabase';
import type { IntelligentEvent, Lens, Perspective } from './types';

type FeedItem=Record<string,any>;
function map(item:FeedItem):IntelligentEvent{
 const perspectives:Perspective[]=[
  {label:'HUMAN',body:String(item.content||item.title||''),tone:'human'},
  {label:'NAYA',body:String(item.content||'No Naya interpretation recorded.'),tone:'naya'},
  {label:'MACHINE',body:String(item.type||'event')+' · '+String(item.source||'canonical cognition'),tone:'machine'}
 ];
 return {
  event_id:String(item.event_id||item.id),user_id:String(item.user_id||''),
  created_at:String(item.created_at),updated_at:String(item.updated_at||item.created_at),
  source:{type:String(item.type||'intelligence'),label:String(item.title||'NayaNET Intelligence')},
  human_input:{raw:String(item.content||''),captured_at:String(item.created_at)},
  context:{topic:String(item.title||''),tags:Array.isArray(item.tags)?item.tags:[],canonical_path:'naya-smart-feed'},
  naya_interpretation:{observation:String(item.content||''),interpretation:String(item.content||''),recommendation:'Inspect the canonical source and evidence before acting.',uncertainty:item.verification_state==='VERIFIED'?'None recorded.':'Runtime verification state is '+String(item.verification_state||'NOT_PROVEN')},
  machine_evidence:{items:['SOURCE:'+String(item.source||'nayanet_cognition_events'),'EVENT:'+String(item.id||item.event_id),'LEDGER:'+String(item.ledger_event_id||'NOT_ATTACHED'),'EVIDENCE:'+(item.ledger_evidence_available?'AVAILABLE':'NOT_RECORDED')],verification_state:String(item.verification_state||item.ledger_status||'RECORDED')},
  weaver_synthesis:{summary:String(item.title||'NayaNET Intelligence'),relationships:[]},
  lesson:{text:String(item.content||''),retained:true},
  meaning:{text:String(item.content||''),significance:String(item.title||'')},
  action:{text:'Inspect the source, evidence and verification state before authorized use.',status:'SOURCE + EVIDENCE FIRST'},
  whats_in_it_for_you:'Use only the value that is actually supported by the recorded intelligence.',
  relationships:{event_ids:[],connection_ids:[],space_ids:[]},
  privacy:{visibility:String(item.visibility||'private'),consent_state:item.stream==='collective'?'explicit':'private'},
  trust:{level:item.verification_state==='VERIFIED'?'verified':'recorded',evidence_ids:item.ledger_event_id?[String(item.ledger_event_id)]:[]},
  status:String(item.status||'active'),perspectives
 };
}
export async function loadSmartFeed(stream:Lens,limit=30):Promise<{events:IntelligentEvent[];next_before:string|null}>{
 const {data:{session}}=await supabase.auth.getSession();
 if(!session)return {events:[],next_before:null};
 const r=await fetch(SUPABASE_URL+'/functions/v1/naya-smart-feed',{method:'POST',headers:{Authorization:'Bearer '+session.access_token,apikey:SUPABASE_PUBLISHABLE_KEY,'Content-Type':'application/json'},body:JSON.stringify({stream,limit})});
 const data=await r.json().catch(()=>({}));
 if(!r.ok||!data.ok)throw new Error(data.error||'SMART_FEED_FAILED');
 return {events:(data.items||[]).map(map),next_before:data.next_before||null};
}
export async function smartFeedAction(sourceId:string,action:'save'|'favorite'|'like'|'love'){
 const {data:{session}}=await supabase.auth.getSession();if(!session)throw new Error('AUTHENTICATION_REQUIRED');
 const r=await fetch(SUPABASE_URL+'/functions/v1/naya-smart-feed',{method:'POST',headers:{Authorization:'Bearer '+session.access_token,apikey:SUPABASE_PUBLISHABLE_KEY,'Content-Type':'application/json'},body:JSON.stringify({action:'interact',stream:'personal',source_id:sourceId,interaction:action})});
 const data=await r.json().catch(()=>({}));if(!r.ok||!data.ok)throw new Error(data.error||'SMART_FEED_ACTION_FAILED');return data;
}
export async function publishSmartFeed(sourceId:string){
 const {data:{session}}=await supabase.auth.getSession();if(!session)throw new Error('AUTHENTICATION_REQUIRED');
 const r=await fetch(SUPABASE_URL+'/functions/v1/naya-smart-feed',{method:'POST',headers:{Authorization:'Bearer '+session.access_token,apikey:SUPABASE_PUBLISHABLE_KEY,'Content-Type':'application/json'},body:JSON.stringify({action:'publish',source_id:sourceId})});
 const data=await r.json().catch(()=>({}));if(!r.ok||!data.ok)throw new Error(data.error||'SMART_FEED_PUBLISH_FAILED');return data;
}

export async function revokeSmartFeed(publicationId:string){
 const {data:{session}}=await supabase.auth.getSession();if(!session)throw new Error('AUTHENTICATION_REQUIRED');
 const r=await fetch(SUPABASE_URL+'/functions/v1/naya-smart-feed',{method:'POST',headers:{Authorization:'Bearer '+session.access_token,apikey:SUPABASE_PUBLISHABLE_KEY,'Content-Type':'application/json'},body:JSON.stringify({action:'revoke',publication_id:publicationId})});
 const data=await r.json().catch(()=>({}));if(!r.ok||!data.ok)throw new Error(data.error||'SMART_FEED_REVOKE_FAILED');return data;
}
