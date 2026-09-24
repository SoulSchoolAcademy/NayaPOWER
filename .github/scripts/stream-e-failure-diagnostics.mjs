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
