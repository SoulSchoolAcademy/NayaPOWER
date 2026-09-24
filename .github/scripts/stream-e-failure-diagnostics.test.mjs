import test from 'node:test';
import assert from 'node:assert/strict';
import {classifySenderFailure,formatRuntimeFailure,redactDiagnostic,summarizeReceiverResponse} from './stream-e-failure-diagnostics.mjs';

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

test('classifies a later production receiver failure as partial state',()=>{
  const value=classifySenderFailure(new Error('PRODUCTION_RECEIVER_FAILED'),{event_id:'event-1',receipt_id:'receipt-1',transaction_id:'transaction-1'});
  assert.deepEqual(value,{first_failure_boundary:'PRODUCTION_RECEIVER',partial_state:'PARTIAL_STATE_OBSERVED',downstream_reachability:'REACHED_PRODUCTION_RECEIVER_FAILED'});
});

test('does not claim partial state without lineage identifiers',()=>{
  const value=classifySenderFailure(new Error('PRODUCTION_RECEIVER_FAILED'),{event_id:'UNAVAILABLE',receipt_id:'UNAVAILABLE',transaction_id:'UNAVAILABLE'});
  assert.equal(value.partial_state,'UNDETERMINED');
});
