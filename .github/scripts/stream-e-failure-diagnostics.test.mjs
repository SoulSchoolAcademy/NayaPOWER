import test from 'node:test';
import assert from 'node:assert/strict';
import {buildNoMutationProof,classifySenderFailure,formatRuntimeFailure,redactDiagnostic,resolveProofMode,summarizeReceiverBridgeResponse,summarizeReceiverResponse} from './stream-e-failure-diagnostics.mjs';

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

test('summarizes an authorization response without exposing the body',()=>{
  const value=summarizeReceiverBridgeResponse(403,{status:'REJECTED',code:'REF_NOT_AUTHORIZED',detail:'private detail',packet:{secret:'hidden'}});
  assert.deepEqual(value,{status:403,code:'REF_NOT_AUTHORIZED',detail:'private detail'});
});

test('classifies a receiver authorization refusal separately',()=>{
  const value=classifySenderFailure(new Error('PRODUCTION_RECEIVER_AUTHORIZATION_FAILED'),{event_id:'event-1',receipt_id:'receipt-1',transaction_id:'transaction-1'},{status:403,code:'REF_NOT_AUTHORIZED'});
  assert.deepEqual(value,{first_failure_boundary:'PRODUCTION_RECEIVER_AUTHORIZATION',partial_state:'PARTIAL_STATE_OBSERVED',downstream_reachability:'REACHED_RECEIVER_AUTHORIZATION_FAILED',receiver_code:'REF_NOT_AUTHORIZED'});
});

test('allows only an exact non-PR main ref into the main proof path',()=>{
  assert.equal(resolveProofMode('refs/heads/main','push',''),'MAIN_REF_PROOF');
  assert.equal(resolveProofMode('refs/heads/main','pull_request','feature'),'NON_MAIN_NO_MUTATION');
  assert.equal(resolveProofMode('refs/heads/feature','push',''),'NON_MAIN_NO_MUTATION');
  assert.equal(resolveProofMode('','local',''),'NON_MAIN_NO_MUTATION');
});

test('builds a deterministic non-main proof with zero production mutation claims',()=>{
  const value=buildNoMutationProof({ref:'refs/heads/feature',eventName:'push',headRef:'',headSha:'abc123',runId:'42'});
  assert.equal(value.status,'VERIFIED');
  assert.equal(value.proof_mode,'NON_MAIN_NO_MUTATION');
  assert.equal(value.ref,'refs/heads/feature');
  assert.equal(value.production_mutation,'NONE');
  assert.equal(value.browser_launch,'NOT_STARTED');
  assert.equal(value.network_activity,'NONE');
  assert.equal(value.smart_note_capture,'NOT_RUN');
  assert.equal(value.production_transaction,'NOT_CREATED');
  assert.equal(value.production_receipt,'NOT_CREATED');
  assert.equal(value.production_intelligence,'NOT_CREATED');
  assert.equal(value.capture_request_count,0);
  assert.equal(value.receiver_request_count,0);
  assert.deepEqual(value.trace,[]);
});

test('classifies a later production receiver failure as partial state',()=>{
  const value=classifySenderFailure(new Error('PRODUCTION_RECEIVER_FAILED'),{event_id:'event-1',receipt_id:'receipt-1',transaction_id:'transaction-1'});
  assert.deepEqual(value,{first_failure_boundary:'PRODUCTION_RECEIVER',partial_state:'PARTIAL_STATE_OBSERVED',downstream_reachability:'REACHED_PRODUCTION_RECEIVER_FAILED'});
});

test('does not claim partial state without lineage identifiers',()=>{
  const value=classifySenderFailure(new Error('PRODUCTION_RECEIVER_FAILED'),{event_id:'UNAVAILABLE',receipt_id:'UNAVAILABLE',transaction_id:'UNAVAILABLE'});
  assert.equal(value.partial_state,'UNDETERMINED');
});
