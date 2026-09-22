import { createClient } from 'npm:@supabase/supabase-js@2'

const URL = Deno.env.get('SUPABASE_URL')!
const publishable = JSON.parse(Deno.env.get('SUPABASE_PUBLISHABLE_KEYS')!).default
const secret = JSON.parse(Deno.env.get('SUPABASE_SECRET_KEYS')!).default
const admin = createClient(URL, secret)
const cors = {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization,apikey,content-type,x-client-info,x-supabase-api-version','Access-Control-Allow-Methods':'POST,OPTIONS'}
const json=(body:any,status=200)=>new Response(JSON.stringify(body),{status,headers:{...cors,'Content-Type':'application/json'}})

Deno.serve(async(req)=>{
  if(req.method==='OPTIONS') return new Response('ok',{headers:cors})
  const authorization=req.headers.get('Authorization')
  if(!authorization?.startsWith('Bearer ')) return json({ok:false,error:'AUTH_REQUIRED'},401)
  const userSupabase=createClient(URL,publishable,{global:{headers:{Authorization:authorization}}})
  const {data:{user},error:authError}=await userSupabase.auth.getUser()
  if(authError||!user) return json({ok:false,error:'AUTH_REQUIRED'},401)

  let body:any={}
  try{body=await req.json()}catch{}
  const stream=String(body.stream||'personal')
  const limit=Math.min(Math.max(Number(body.limit||20),1),50)
  const before=body.before?String(body.before):null
  const action=body.action?String(body.action):'read'

  if(action==='publish'){
    const sourceId=String(body.source_id||'')
    const authorityGrantId=String(body.authority_grant_id||'')
    if(!sourceId) return json({ok:false,error:'SOURCE_ID_REQUIRED'},400)
    if(!authorityGrantId) return json({ok:false,error:'AUTHORITY_GRANT_REQUIRED'},403)
    const owned=await userSupabase.from('nayanet_cognition_events').select('id').eq('id',sourceId).eq('user_id',user.id).maybeSingle()
    if(owned.error||!owned.data) return json({ok:false,error:'SOURCE_NOT_OWNED'},403)
    const validation=await userSupabase.rpc('nayanet_validate_authority_grant',{p_grant_id:authorityGrantId,p_action:'smart_feed_publish',p_target:sourceId})
    if(validation.error) return json({ok:false,error:'AUTHORITY_VALIDATION_FAILED',detail:validation.error.message},403)
    if(validation.data?.status!=='AUTHORIZED') return json({ok:false,error:'AUTHORITY_NOT_AUTHORIZED',detail:validation.data?.reason||'BLOCKED'},403)
    const result=await userSupabase.from('nayanet_intelligence_publications').upsert({intelligence_event_id:sourceId,owner_id:user.id,status:'published',consent_state:'explicit',published_at:new Date().toISOString()},{onConflict:'intelligence_event_id'}).select('*').single()
    if(result.error) return json({ok:false,error:result.error.message},400)
    return json({ok:true,action:'publish',publication:result.data,authority:{grant_id:authorityGrantId,status:validation.data.status,validated_at:new Date().toISOString()}})
  }

  if(action==='revoke'){
    const publicationId=String(body.publication_id||'')
    if(!publicationId) return json({ok:false,error:'PUBLICATION_ID_REQUIRED'},400)
    const result=await userSupabase.from('nayanet_intelligence_publications').update({status:'revoked',updated_at:new Date().toISOString()}).eq('id',publicationId).eq('owner_id',user.id).select('*').single()
    if(result.error||!result.data) return json({ok:false,error:result.error?.message||'NOT_FOUND'},403)
    return json({ok:true,action:'revoke',publication:result.data})
  }

  if(action==='interact'){
    const sourceId=String(body.source_id||'')
    const interaction=String(body.interaction||'')
    if(!sourceId||!['save','favorite','like','love'].includes(interaction)) return json({ok:false,error:'INVALID_INTERACTION'},400)
    const own=await userSupabase.from('nayanet_cognition_events').select('id').eq('id',sourceId).eq('user_id',user.id).maybeSingle()
    let allowed=!!own.data
    if(!allowed){
      const pub=await admin.from('nayanet_intelligence_publications').select('id').eq('intelligence_event_id',sourceId).eq('status','published').eq('consent_state','explicit').maybeSingle()
      allowed=!!pub.data
    }
    if(!allowed) return json({ok:false,error:'SOURCE_NOT_AUTHORIZED'},403)
    const eventId='feed-interaction-'+interaction+'-'+sourceId+'-'+user.id
    const payload={event_id:eventId,project:'NayaNET',source:'nayanet-smart-feed',actor:'human',created_at:new Date().toISOString(),schema_version:'2.0.0',title:'Smart Feed '+interaction,content:'Authorized Smart Feed interaction',type:'interaction',classification:'observation',status:'active',tags:['smart-feed','interaction',interaction],metadata:{source_id:sourceId,interaction,actor_user_id:user.id}}
    const rpc=await userSupabase.rpc('nayanet_record_cognition_event',{p_project_id:'NayaNET',p_event:payload,p_action:'smart_feed_interaction',p_expected_result:'interaction persisted idempotently',p_observed_result:'interaction persisted',p_learning:[{status:'captured',at:new Date().toISOString()}]})
    if(rpc.error) return json({ok:false,error:rpc.error.message},400)
    return json({ok:true,action:'interact',interaction,source_id:sourceId,receipt:rpc.data})
  }

  const fields='id,user_id,event_id,project_id,type,classification,title,content,source,status,confidence,tags,parent_event_id,created_at,updated_at,metadata'
  const attachLedger=async(items:any[],ownerId:string,collective=false)=>{
    const ids=[...new Set(items.flatMap((e:any)=>[e.id,e.event_id].map((v:any)=>String(v||'')).filter(Boolean)))]
    if(!ids.length) return items
    let ledgerQuery=admin.from('nayanet_smart_ledger')
      .select('ledger_event_id,source_id,event_hash,status,privacy_classification,verification,evidence_refs,value,outcome,learning_refs')
      .eq('source_table','nayanet_cognition_events').in('source_id',ids)
    if(ownerId) ledgerQuery=ledgerQuery.eq('owner_id',ownerId)
    const ledgerResult=await ledgerQuery
    if(ledgerResult.error) throw new Error('LEDGER_LOOKUP_FAILED:'+ledgerResult.error.message)
    const bySource=new Map((ledgerResult.data||[]).map((l:any)=>[String(l.source_id),l]))
    return items.map((e:any)=>{
      const l=bySource.get(String(e.id))
      const verification=l?.verification||{}
      const base={
        ...e,
        verification_state:verification.status||l?.status||'LEDGER_MISSING',
        verification_confidence:verification.confidence??null,
        ledger_event_id:l?.ledger_event_id??null,
        ledger_status:l?.status??null,
        ledger_event_hash:l?.event_hash??null,
        ledger_evidence_available:Array.isArray(l?.evidence_refs)?l.evidence_refs.length>0:false
      }
      if(collective){
        return base
      }
      return {...base,ledger_verification:verification,ledger_evidence_refs:l?.evidence_refs??[],ledger_value:l?.value??{},ledger_outcome:l?.outcome??{},ledger_learning_refs:l?.learning_refs??{}}
    })
  }
  const attachBlocks=async(items:any[],collective=false)=>{
    const ids=items.map((e:any)=>String(e.id)).filter(Boolean)
    if(!ids.length) return items
    const owners=[...new Set(items.map((e:any)=>String(e.user_id||'')).filter(Boolean))]
    let blockQuery=admin.from('nayanet_intelligent_blocks')
      .select('block_id,owner_id,subject_id,title,block_type,version,status,understanding_state,owner_scope,source_event_ids,evidence_refs,provenance,value_context,applicable_scope,content,supersedes_block_id,superseded_by_block_id,created_at,updated_at,schema_version')
      .overlaps('source_event_ids',ids)
    if(collective){
      if(owners.length) blockQuery=blockQuery.in('owner_id',owners)
    }else if(owners[0]){
      blockQuery=blockQuery.eq('owner_id',owners[0])
    }
    const blockResult=await blockQuery
    if(blockResult.error) throw new Error('INTELLIGENT_BLOCK_LOOKUP_FAILED:'+blockResult.error.message)
    const byEvent=new Map<string,any>()
    for(const block of blockResult.data||[]){
      for(const eventId of block.source_event_ids||[]) byEvent.set(String(eventId),block)
    }
    return items.map((e:any)=>{
      const block=byEvent.get(String(e.id))
      if(!block) return e
      if(!collective) return {...e,intelligent_block:block}
      return {...e,intelligent_block:{
        block_id:block.block_id,title:block.title,block_type:block.block_type,version:block.version,
        status:block.status,understanding_state:block.understanding_state,owner_scope:block.owner_scope,
        applicable_scope:block.applicable_scope,created_at:block.created_at,updated_at:block.updated_at,
        schema_version:block.schema_version,source_event_ids:[String(e.id)]
      }}
    })
  }
  if(stream==='personal'||stream==='activity'){
    let q=userSupabase.from('nayanet_cognition_events').select(fields).eq('project_id','NayaNET').eq('user_id',user.id).order('created_at',{ascending:false}).limit(limit+1)
    if(before) q=q.lt('created_at',before)
    const result=await q
    if(result.error) return json({ok:false,error:result.error.message},400)
    const rows=result.data||[]
    let items=rows.slice(0,limit).map((e:any)=>({...e,stream,source_id:e.id,visibility:'private',available_actions:stream==='personal'?['save','favorite','publish']:['save','favorite']}))
    try{items=await attachLedger(items,user.id,false);items=await attachBlocks(items,false)}catch(error){return json({ok:false,error:String(error?.message||error)},500)}
    return json({ok:true,stream,items,next_before:rows.length>limit?rows[limit-1].created_at:null})
  }

  if(stream==='collective'){
    let q=admin.from('nayanet_intelligence_publications').select('id,intelligence_event_id,published_at,created_at').eq('status','published').eq('consent_state','explicit').order('published_at',{ascending:false}).limit(limit+1)
    if(before) q=q.lt('published_at',before)
    const pubResult=await q
    if(pubResult.error) return json({ok:false,error:pubResult.error.message},400)
    const pubs=pubResult.data||[]
    const ids=pubs.slice(0,limit).map((p:any)=>p.intelligence_event_id)
    let events:any[]=[]
    if(ids.length){
      const eventResult=await admin.from('nayanet_cognition_events').select(fields).in('id',ids)
      if(eventResult.error) return json({ok:false,error:eventResult.error.message},400)
      events=eventResult.data||[]
    }
    const byId=new Map(events.map((e:any)=>[e.id,e]))
    let items=pubs.slice(0,limit).map((p:any)=>{const e=byId.get(p.intelligence_event_id);if(!e)return null;return {...e,stream:'collective',source_id:e.id,publication_id:p.id,published_at:p.published_at,visibility:'collective',publisher_identity:'private-by-default',available_actions:['save','favorite','like','love']}}).filter(Boolean)
    try{items=await attachLedger(items,null,true);items=await attachBlocks(items,true)}catch(error){return json({ok:false,error:String(error?.message||error)},500)}
    return json({ok:true,stream,items,next_before:pubs.length>limit?pubs[limit-1].published_at:null})
  }
  return json({ok:false,error:'INVALID_STREAM'},400)
})