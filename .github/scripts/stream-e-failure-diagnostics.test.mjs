import test from 'node:test';
import assert from 'node:assert/strict';
import {formatRuntimeFailure,redactDiagnostic,summarizeReceiverResponse} from './stream-e-failure-diagnostics.mjs';

test('redacts credentials and bounds diagnostic text',()=>{
  const value=redactDiagnostic('authorization: Bearer secret-token\nnext');
  assert.equal(value,'authorization=[REDACTED] next');
  assert.equal(redactDiagnostic('x'.repeat(600)).length,512);
});

test('summarizes receiver status, lineage, and fallback correlation',()=>{
  const value=summarizeReceiverResponse(500,{error:'SMART_NOTE_PIPELINE_FAILED',detail:'database detail',event_id:'event-1',receipt_id:'receipt-1',transaction_id:'transaction-1'},'smart-note-key');
  assert.deepEqual(value,{status:500,error:'SMART_NOTE_PIPELINE_FAILED',detail:'database detail',correlation_id:'smart-note-key',event_id:'event-1',receipt_id:'receipt-1',transaction_id:'transaction-1'});
});

test('formats a receiver failure without discarding detail',()=>{
  const message=formatRuntimeFailure(422,{error:'SMART_NOTE_PIPELINE_FAILED',detail:'validation failed',correlation_id:'corr-1'},'smart-note-key');
  assert.match(message,/^SMART_NOTE_PIPELINE_FAILED\|status=422\|code=SMART_NOTE_PIPELINE_FAILED\|correlation=corr-1\|event=UNAVAILABLE\|receipt=UNAVAILABLE\|transaction=UNAVAILABLE\|detail=validation failed$/);
});
