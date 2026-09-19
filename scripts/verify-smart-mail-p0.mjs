import crypto from 'node:crypto';
import fs from 'node:fs';

const base = process.env.SUPABASE_URL;
const key = process.env.SUPABASE_PUBLISHABLE_KEY;
const functionUrl = base + '/functions/v1/nayanet-smart-mail';

async function request(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let body = null;
  try { body = JSON.parse(text); } catch { body = { raw: text }; }
  if (!res.ok) throw new Error(url + ' HTTP ' + res.status + ' ' + JSON.stringify(body));
  return body;
}

async function anonymous() {
  return request(base + '/auth/v1/signup', {
    method: 'POST',
    headers: { apikey: key, 'content-type': 'application/json' },
    body: '{}'
  });
}

async function rawRequest(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let body = null;
  try { body = JSON.parse(text); } catch { body = { raw: text }; }
  return { status: res.status, body };
}
const authHeaders = token => ({ apikey: key, authorization: 'Bearer ' + token, 'content-type': 'application/json' });
async function rpc(token, fn, payload) {
  return request(base + '/rest/v1/rpc/' + fn, { method:'POST', headers:authHeaders(token), body:JSON.stringify(payload) });
}

const sender = await anonymous();
const receiver = await anonymous();
if (!sender?.user?.id || !sender?.access_token) throw new Error('SENDER_ANON_AUTH_FAILED');
if (!receiver?.user?.id || !receiver?.access_token) throw new Error('RECEIVER_ANON_AUTH_FAILED');

const senderId = sender.user.id;
const receiverId = receiver.user.id;

// Establish the existing governed Space -> mutual Connection prerequisite for these fresh proof identities.
const spaceRows = await request(base + '/rest/v1/nayanet_spaces', {
  method:'POST',
  headers:authHeaders(sender.access_token),
  body:JSON.stringify({
    owner_member_id: senderId,
    name: 'P0 Smart Mail Proof Space',
    purpose: 'P0 Smart Mail relationship prerequisite',
    visibility: 'shared'
  })
});
if (!Array.isArray(spaceRows) || spaceRows.length !== 1 || !spaceRows[0]?.id) throw new Error('PROOF_SPACE_NOT_CREATED');
const proofSpaceId = spaceRows[0].id;
const senderJoin = await rpc(sender.access_token, 'nayanet_join_space', { p_space_id: proofSpaceId });
if (!['JOINED','ALREADY_MEMBER'].includes(senderJoin?.status)) throw new Error('SENDER_SPACE_MEMBERSHIP_FAILED ' + JSON.stringify(senderJoin));
const receiverJoin = await rpc(receiver.access_token, 'nayanet_join_space', { p_space_id: proofSpaceId });
if (!['JOINED','ALREADY_MEMBER'].includes(receiverJoin?.status)) throw new Error('RECEIVER_SPACE_MEMBERSHIP_FAILED ' + JSON.stringify(receiverJoin));
const senderConnection = await rpc(sender.access_token, 'nayanet_save_connection', { p_target_member_id: receiverId, p_space_id: proofSpaceId });
if (!['CONNECTED','ALREADY_CONNECTED'].includes(senderConnection?.status)) throw new Error('SENDER_CONNECTION_FAILED ' + JSON.stringify(senderConnection));
const receiverConnection = await rpc(receiver.access_token, 'nayanet_save_connection', { p_target_member_id: senderId, p_space_id: proofSpaceId });
if (!['CONNECTED','ALREADY_CONNECTED'].includes(receiverConnection?.status)) throw new Error('RECEIVER_CONNECTION_FAILED ' + JSON.stringify(receiverConnection));

const idempotencyKey = 'p0-mail-proof-' + crypto.randomBytes(12).toString('hex');
const requestId = 'p0-request-' + crypto.randomUUID();
const body = 'P0 Smart Mail vertical proof: authenticated external sender -> Naya cognition -> governed mail -> receiver.';
const sendPayload = { recipient_user_id: receiverId, body, subject: 'NayaNET P0 Sender Receiver Proof', kind: 'direct', idempotency_key: idempotencyKey, project_id: 'NayaNET' };
const sourceEventId = 'human:smart-mail-send:' + idempotencyKey;
const grant = await rpc(sender.access_token, 'nayanet_issue_authority_grant', {
  p_subject_id: senderId,
  p_source_event_id: sourceEventId,
  p_mission_id: 'NayaNET-SMART-MAIL',
  p_scope: { target: receiverId, project_id: 'NayaNET' },
  p_actions: ['smart_mail_send'],
  p_constraints: { kind: 'direct', no_model_authority: true },
  p_expires_at: null,
  p_evidence: { human_action: 'explicit authenticated proof authorization', idempotency_key: idempotencyKey, request_id: requestId },
  p_parent_authority: null
});
if (!grant?.grant_id) throw new Error('AUTHORITY_GRANT_NOT_ISSUED');
sendPayload.authority_grant_id = grant.grant_id;
const preValidation = await rpc(sender.access_token, 'nayanet_validate_authority_grant', {
  p_grant_id: grant.grant_id, p_action: 'smart_mail_send', p_target: receiverId
});
if (preValidation.status !== 'AUTHORIZED') throw new Error('AUTHORITY_PREVALIDATION_FAILED ' + JSON.stringify(preValidation));
const first = await request(functionUrl, { method: 'POST', headers: { ...authHeaders(sender.access_token), 'x-request-id': requestId }, body: JSON.stringify(sendPayload) });
if (first.status !== 'CREATED') throw new Error('SEND_NOT_CREATED ' + JSON.stringify(first));
if (!first.correlation_id || !first.thread_id || !first.message_id || !first.cognition_event_id || !first.execution_receipt_id) throw new Error('SEND_LINEAGE_INCOMPLETE');
if (first.authority_changed !== false) throw new Error('AUTHORITY_CHANGED');

const receiverRows = await request(
  base + '/rest/v1/v7_mail_messages?select=id,thread_id,sender_id,body,metadata,created_at&thread_id=eq.' + first.thread_id,
  { headers: { apikey: key, authorization: 'Bearer ' + receiver.access_token } }
);
if (!Array.isArray(receiverRows) || receiverRows.length !== 1) throw new Error('RECEIVER_MESSAGE_COUNT');
const received = receiverRows[0];
if (received.id !== first.message_id || received.sender_id !== senderId || received.body !== body) throw new Error('RECEIVER_MESSAGE_MISMATCH');
if (received.metadata?.correlation_id !== first.correlation_id || received.metadata?.receiver_id !== receiverId) throw new Error('CORRELATION_OR_RECEIVER_MISMATCH');
const receiverVerification = await request(functionUrl, {
  method: 'POST',
  headers: authHeaders(receiver.access_token),
  body: JSON.stringify({ operation: 'verify', message_id: first.message_id })
});
if (receiverVerification.status !== 'VERIFIED' || receiverVerification.receiver_id !== receiverId || receiverVerification.authority_changed !== false) {
  throw new Error('RECEIVER_VERIFICATION_FAILED');
}

const cognition = await request(
  base + '/rest/v1/nayanet_cognition_events?select=id,user_id,event_id,type,source,receipt_id,metadata&user_id=eq.' + senderId + '&id=eq.' + encodeURIComponent(first.cognition_event_id),
  { headers: { apikey: key, authorization: 'Bearer ' + sender.access_token } }
);
if (!Array.isArray(cognition) || cognition.length !== 1) throw new Error('COGNITION_NOT_RETRIEVABLE');
if (cognition[0].receipt_id !== first.execution_receipt_id) throw new Error('COGNITION_RECEIPT_LINEAGE_MISMATCH');

const receipt = await request(
  base + '/rest/v1/nayanet_execution_receipts?select=id,user_id,action,status,evidence,learning,request_id,authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints,authority_status_at_execution,authority_source_event_id,authority_validated_at&user_id=' + senderId + '&id=' + first.execution_receipt_id,
  { headers: { apikey: key, authorization: 'Bearer ' + sender.access_token } }
);
if (!Array.isArray(receipt) || receipt.length !== 1 || receipt[0].status !== 'SUCCESS' || receipt[0].action !== 'smart_mail_send') throw new Error('EXECUTION_RECEIPT_INVALID');
if (receipt[0].request_id !== requestId) throw new Error('REQUEST_ID_LINEAGE_MISMATCH');
if (!receipt[0].authority_grant_id || receipt[0].authority_grant_id !== grant.grant_id || receipt[0].authority_issuer_id !== senderId || receipt[0].authority_status_at_execution !== 'ACTIVE' || receipt[0].authority_source_event_id !== sourceEventId || !receipt[0].authority_validated_at) throw new Error('AUTHORITY_PROVENANCE_INVALID');

const replay = await request(functionUrl, { method: 'POST', headers: authHeaders(sender.access_token), body: JSON.stringify(sendPayload) });
if (replay.status !== 'REPLAY' || replay.message_id !== first.message_id || replay.thread_id !== first.thread_id) throw new Error('IDEMPOTENCY_REPLAY_FAILED');

const revoked = await rpc(sender.access_token, 'nayanet_revoke_authority_grant', {
  p_grant_id: grant.grant_id,
  p_evidence: { proof: 'revocation-at-use production proof', idempotency_key: idempotencyKey }
});
if (!revoked?.grant_id || revoked.status !== 'REVOKED') throw new Error('AUTHORITY_REVOKE_FAILED ' + JSON.stringify(revoked));

const blockedAttempt = await rawRequest(functionUrl, { method:'POST', headers:authHeaders(sender.access_token), body:JSON.stringify({...sendPayload, idempotency_key:idempotencyKey + '-after-revoke'}) });
if (blockedAttempt.status < 400 || (blockedAttempt.body?.detail?.reason ?? blockedAttempt.body?.error) !== 'GRANT_REVOKED') {
  throw new Error('REVOKED_EXECUTION_NOT_BLOCKED ' + JSON.stringify(blockedAttempt));
}
const receiptAfterRevoke = await request(
  base + '/rest/v1/nayanet_execution_receipts?select=id&user_id=' + senderId + '&id=' + first.execution_receipt_id,
  { headers: { apikey:key, authorization:'Bearer '+sender.access_token } }
);
if (!Array.isArray(receiptAfterRevoke) || receiptAfterRevoke.length !== 1) throw new Error('ORIGINAL_RECEIPT_MISSING_AFTER_REVOKE');

const proof = {
  schema: 'naya.nayanet.smart_mail.p0.production.proof.v1',
  status: 'VERIFIED',
  user: { sender_id: senderId, receiver_id: receiverId },
  transaction: { correlation_id: first.correlation_id, thread_id: first.thread_id, message_id: first.message_id, cognition_event_id: first.cognition_event_id, execution_receipt_id: first.execution_receipt_id, idempotency_key: idempotencyKey, request_id: requestId },
  chain: { external_sender_authenticated: true, canonical_naya_identity: true, cognition_persisted: true, governed_processing_receipt: true, receiver_authenticated: true, receiver_retrieved_message: true, receiver_verified_receipt: true, correlation_preserved: true, authority_unchanged: true, idempotent_replay: true, authority_issued: true, authority_prevalidated: true, authority_revoked: true, revoked_execution_blocked: true, receipt_lineage_preserved_after_revoke: true },
  observed_at: new Date().toISOString()
};
const requiredProof=Object.values(proof.chain).every(v=>v===true); if(!requiredProof) throw new Error('SMART_MAIL_PROOF_POINT_FAILED '+JSON.stringify(proof.chain));
fs.writeFileSync(process.env.PROOF_PATH, JSON.stringify(proof, null, 2));
for (const [k,v] of Object.entries(proof.chain)) console.log('SMART_MAIL_' + k.toUpperCase() + '=' + (v ? 'PASS' : 'FAIL'));
console.log('SMART_MAIL_PROOF_STATUS=VERIFIED');
console.log('SMART_MAIL_CORRELATION_ID=' + first.correlation_id);
console.log('SMART_MAIL_THREAD_ID=' + first.thread_id);
console.log('SMART_MAIL_MESSAGE_ID=' + first.message_id);
console.log('SMART_MAIL_COGNITION_EVENT_ID=' + first.cognition_event_id);
console.log('SMART_MAIL_EXECUTION_RECEIPT_ID=' + first.execution_receipt_id);
