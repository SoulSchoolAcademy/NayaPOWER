const LIMIT=512;
const redact=value=>String(value??'').replace(/(bearer|token|apikey|secret|password|authorization)\s*[:=]\s*(?:bearer\s+)?[^\s,;|]+/gi,'$1=[REDACTED]').replace(/\bbearer\s+[^\s,;|]+/gi,'bearer=[REDACTED]').replace(/\s+/g,' ').trim().slice(0,LIMIT)||'UNAVAILABLE';
const pick=(...values)=>{for(const value of values){if(value!==undefined&&value!==null&&String(value).trim())return redact(value)}return 'UNAVAILABLE'};
export function redactDiagnostic(value){return redact(value)}
export function summarizeReceiverResponse(status,body,idempotencyKey=''){
  const value=body&&typeof body==='object'?body:{};
  return {
    status:Number.isFinite(Number(status))?Number(status):null,
    error:pick(value.error,'SMART_NOTE_PIPELINE_FAILED'),
    detail:pick(value.detail),
    correlation_id:pick(value.correlation_id,value.request_id,value.trace_id,idempotencyKey),
    event_id:pick(value.event_id,value.transaction?.evidence?.event_id),
    receipt_id:pick(value.receipt_id,value.transaction?.evidence?.receipt_id),
    transaction_id:pick(value.transaction_id,value.transaction?.id)
  };
}
export function formatRuntimeFailure(status,body,idempotencyKey=''){
  const value=summarizeReceiverResponse(status,body,idempotencyKey);
  return `SMART_NOTE_PIPELINE_FAILED|status=${value.status??'UNKNOWN'}|code=${value.error}|correlation=${value.correlation_id}|event=${value.event_id}|receipt=${value.receipt_id}|transaction=${value.transaction_id}|detail=${value.detail}`;
}
export function classifySenderFailure(error,responseTrace){
  const code=String(error?.message||error||'').split('\n')[0].trim();
  const hasLineage=Boolean(responseTrace&&responseTrace.event_id&&responseTrace.event_id!=='UNAVAILABLE');
  if(code==='PRODUCTION_RECEIVER_FAILED')return {first_failure_boundary:'PRODUCTION_RECEIVER',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'REACHED_PRODUCTION_RECEIVER_FAILED'};
  if(code==='INDEPENDENT_RETRIEVAL_FAILED')return {first_failure_boundary:'INDEPENDENT_RETRIEVAL',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'REACHED_RECEIVER_FAILED'};
  if(code==='INDEX_RECONSTRUCTION_FAILED')return {first_failure_boundary:'INDEX_RECONSTRUCTION',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'REACHED_RECEIVER_FAILED'};
  if(code==='EXACT_REPLAY_FAILED')return {first_failure_boundary:'EXACT_REPLAY',partial_state:'PARTIAL_STATE_OBSERVED',downstream_reachability:'REACHED_REPLAY_CHECK'};
  if(code==='HUB_RUNTIME_CAPTURE_LINEAGE_MISSING')return {first_failure_boundary:'HUB_RUNTIME_CAPTURE_LINEAGE',partial_state:'UNDETERMINED',downstream_reachability:'NOT_REACHED_BY_SENDER'};
  if(responseTrace)return {first_failure_boundary:'HUB_RUNTIME_RESPONSE_MAPPING',partial_state:hasLineage?'PARTIAL_STATE_OBSERVED':'UNDETERMINED',downstream_reachability:'NOT_REACHED_BY_SENDER'};
  return {first_failure_boundary:'UNKNOWN',partial_state:'UNDETERMINED',downstream_reachability:'NOT_REACHED_BY_SENDER'};
}
