const LIMIT=512;
const redact=value=>String(value??'').replace(/(bearer|token|apikey|secret|password|authorization)\s*[:=]\s*(?:bearer\s+)?[^\s,;|]+/gi,'$1=[REDACTED]').replace(/\bbearer\s+[^\s,;|]+/gi,'bearer=[REDACTED]').replace(/\s+/g,' ').trim().slice(0,LIMIT)||'UNAVAILABLE';
const pick=(...values)=>{for(const value of values){if(value!==undefined&&value!==null&&String(value).trim())return redact(value)}return 'UNAVAILABLE'};
export function redactDiagnostic(value){return redact(value)}
export function resolveProofMode(ref,eventName='',headRef=''){
  const pullRequest=eventName==='pull_request'||eventName==='pull_request_target'||Boolean(headRef);
  return String(ref||'UNPINNED_LOCAL')==='refs/heads/main'&&!pullRequest?'MAIN_REF_PROOF':'NON_MAIN_NO_MUTATION';
}
export function buildNoMutationProof({ref='UNPINNED_LOCAL',eventName='',headRef='',headSha='',runId='' }={}){
  return {
    schema:'NAYANET_UNIVERSAL_ENVELOPE_HUB_RUNTIME_SENDER_PROOF_V1',
    status:'VERIFIED',
    proof_mode:'NON_MAIN_NO_MUTATION',
    ref:redact(ref),
    event_name:redact(eventName),
    head_ref:redact(headRef),
    head_sha:redact(headSha),
    run_id:redact(runId),
    production_mutation:'NONE',
    browser_launch:'NOT_STARTED',
    network_activity:'NONE',
    smart_note_capture:'NOT_RUN',
    production_transaction:'NOT_CREATED',
    production_receipt:'NOT_CREATED',
    production_intelligence:'NOT_CREATED',
    capture_request_count:0,
    receiver_request_count:0,
    main_only_receiver_policy:'PRESERVED',
    trace:[],
    truth_boundary:'Non-main execution exits before browser launch, network activity, Smart Note capture, or production receiver calls.'
  };
}
export function buildColdReconstruction(proof,{repository='',mainRef='',hubBlob=''}={}){
  const checks={
    positive_proof:proof?.proof_mode==='MAIN_REF_PROOF'&&proof?.status==='VERIFIED',
    persistence:proof?.checks?.independent_persistence==='VERIFIED',
    projection_index:proof?.checks?.projection_index==='VERIFIED',
    retrieval:proof?.checks?.independent_retrieval==='VERIFIED',
    causal_lineage:proof?.checks?.causal_lineage==='VERIFIED',
    replay:proof?.checks?.exact_replay==='VERIFIED'
  };
  return {schema:'NAYANET_STREAM_E_COLD_RECONSTRUCTION_V1',status:Object.values(checks).every(Boolean)?'VERIFIED':'NOT_VERIFIED',repository,main_ref:mainRef,hub_blob:hubBlob,source_proof_status:proof?.status||'UNAVAILABLE',source_proof_mode:proof?.proof_mode||'UNAVAILABLE',checks,missing:Object.entries(checks).filter(([,value])=>!value).map(([key])=>key)};
}
export function summarizeReceiverResponse(status,body,idempotencyKey=''){
  const value=body&&typeof body==='object'?body:{};
  return {
    status:Number.isFinite(Number(status))?Number(status):null,
    ok:value.ok===true,
    pipeline:pick(value.pipeline),
    error:pick(value.error,'SMART_NOTE_PIPELINE_FAILED'),
    detail:pick(value.detail),
    correlation_id:pick(value.correlation_id,value.request_id,value.trace_id,idempotencyKey),
    event_id:pick(value.event_id,value.transaction?.evidence?.event_id),
    receipt_id:pick(value.receipt_id,value.transaction?.evidence?.receipt_id),
    transaction_id:pick(value.transaction_id,value.transaction?.id),
    learning_status:pick(value.transaction?.learning_evidence?.status),
    checkpoint_status:pick(value.transaction?.intelligence_checkpoint?.status)
  };
}
export function summarizeReceiverBridgeResponse(status,body){
  const value=body&&typeof body==='object'?body:{};
  return {
    status:Number.isFinite(Number(status))?Number(status):null,
    code:pick(value.code),
    detail:pick(value.detail)
  };
}
export function formatRuntimeFailure(status,body,idempotencyKey=''){
  const value=summarizeReceiverResponse(status,body,idempotencyKey);
  return `SMART_NOTE_PIPELINE_FAILED|status=${value.status??'UNKNOWN'}|pipeline=${value.pipeline}|code=${value.error}|correlation=${value.correlation_id}|event=${value.event_id}|receipt=${value.receipt_id}|transaction=${value.transaction_id}|detail=${value.detail}`;
}
export function classifySenderFailure(error,responseTrace,receiverResponseTrace){
  const code=String(error?.message||error||'').split('\n')[0].trim();
  const hasLineage=Boolean(responseTrace&&responseTrace.event_id&&responseTrace.event_id!=='UNAVAILABLE');
  if(code==='SMART_NOTE_RECEIVER_PIPELINE_FAILED')return {first_failure_boundary:'SMART_NOTE_RECEIVER_PIPELINE',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'NOT_REACHED_BY_SENDER'};
  if(code==='PRODUCTION_RECEIVER_AUTHORIZATION_FAILED'||receiverResponseTrace?.code==='REF_NOT_AUTHORIZED')return {first_failure_boundary:'PRODUCTION_RECEIVER_AUTHORIZATION',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'REACHED_RECEIVER_AUTHORIZATION_FAILED',receiver_code:'REF_NOT_AUTHORIZED'};
  if(code==='PRODUCTION_RECEIVER_FAILED')return {first_failure_boundary:'PRODUCTION_RECEIVER',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'REACHED_PRODUCTION_RECEIVER_FAILED'};
  if(code==='INDEPENDENT_RETRIEVAL_FAILED')return {first_failure_boundary:'INDEPENDENT_RETRIEVAL',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'REACHED_RECEIVER_FAILED'};
  if(code==='INDEX_RECONSTRUCTION_FAILED')return {first_failure_boundary:'INDEX_RECONSTRUCTION',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'REACHED_RECEIVER_FAILED'};
  if(code==='EXACT_REPLAY_FAILED')return {first_failure_boundary:'EXACT_REPLAY',partial_state:'PARTIAL_STATE_OBSERVED',downstream_reachability:'REACHED_REPLAY_CHECK'};
  if(code==='HUB_RUNTIME_CAPTURE_LINEAGE_MISSING')return {first_failure_boundary:'HUB_RUNTIME_CAPTURE_LINEAGE',partial_state:'UNDETERMINED',downstream_reachability:'NOT_REACHED_BY_SENDER'};
  if(responseTrace)return {first_failure_boundary:'HUB_RUNTIME_RESPONSE_MAPPING',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'NOT_REACHED_BY_SENDER'};
  return {first_failure_boundary:'UNKNOWN',partial_state:'UNDETERMINED',downstream_reachability:'NOT_REACHED_BY_SENDER'};
}
const same=(actual,expected)=>actual!==undefined&&actual!==null&&String(actual)===String(expected);
const parseContent=value=>{try{return value&&typeof value==='string'?JSON.parse(value):value||{}}catch{return {}}};
const contract=(checks)=>({status:Object.values(checks).every(Boolean)?'VERIFIED':'NOT_VERIFIED',checks});
export function verifyCausalLineage({correlationId,envelope,smartNote,bridge,retrievedEvent}={}){
  const content=parseContent(retrievedEvent?.content);
  const universal=(content.intelligence||[]).find(item=>item?.object_id==='envelope:'+envelope?.envelope_id);
  const checks={
    correlation_id_present:Boolean(correlationId),
    envelope_correlation_matches:same(envelope?.context?.correlation_id,correlationId)&&same(envelope?.provenance?.correlation_id,correlationId),
    smart_note_correlation_matches:same(smartNote?.correlation_id,correlationId),
    smart_note_event_present:Boolean(smartNote?.event_id),
    smart_note_transaction_present:Boolean(smartNote?.transaction_id),
    smart_note_receipt_present:Boolean(smartNote?.receipt_id),
    bridge_receiver_event_present:Boolean(bridge?.receiver_event_id),
    bridge_receiver_transaction_present:Boolean(bridge?.receiver_transaction_id),
    bridge_receipt_present:Boolean(bridge?.receipt_id),
    retrieved_event_matches:same(retrievedEvent?.event_id,bridge?.receiver_event_id),
    retrieved_receipt_matches:same(retrievedEvent?.receipt_id,bridge?.receipt_id),
    retrieved_correlation_preserved:same(universal?.content?.context?.correlation_id,correlationId)
  };
  return contract(checks);
}
export function verifyPersistenceRecord(bridge,record){
  const row=Array.isArray(record)?record[0]:record;
  return contract({record_present:Boolean(row),packet_id:same(row?.packet_id,bridge?.packet_id),receiver_transaction_id:same(row?.receiver_transaction_id,bridge?.receiver_transaction_id),receiver_event_id:same(row?.receiver_event_id,bridge?.receiver_event_id),receipt_id:same(row?.receipt_id,bridge?.receipt_id),persisted:row?.persisted===true,indexed:row?.indexed===true,projected:row?.projected===true});
}
export function verifyProjectionIndex(bridge,rows,ownerId){
  const row=Array.isArray(rows)?rows.find(item=>same(item?.id,bridge?.projection?.index_id)):rows;
  return contract({index_present:Boolean(row),index_id:same(row?.id,bridge?.projection?.index_id),owner_id:same(row?.owner_id,ownerId)});
}
export function verifyRetrievedEvent(bridge,event,envelopeId){
  const content=parseContent(event?.content);
  const lineage=content.bridge||{};
  const universal=(content.intelligence||[]).find(item=>item?.object_id==='envelope:'+envelopeId);
  return contract({event_id:same(event?.event_id,bridge?.receiver_event_id),receipt_id:same(event?.receipt_id,bridge?.receipt_id),receiver_transaction_id:same(lineage.receiver_transaction_id,bridge?.receiver_transaction_id),receiver_event_id:same(lineage.receiver_event_id,bridge?.receiver_event_id),lineage_receipt_id:same(lineage.receipt_id,bridge?.receipt_id),universal_envelope:same(universal?.content?.envelope_id,envelopeId)});
}
export function verifyExactReplay(bridge,replay){
  return contract({status:replay?.status==='ACCEPTED',replay:replay?.replay===true,receiver_event_id:same(replay?.receiver_event_id,bridge?.receiver_event_id),receipt_id:same(replay?.receipt_id,bridge?.receipt_id),receiver_transaction_id:same(replay?.receiver_transaction_id,bridge?.receiver_transaction_id)});
}
