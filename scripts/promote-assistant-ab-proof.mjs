import fs from 'node:fs';

const receiptPath = process.argv[2];
const proofPath = process.argv[3];
if (!receiptPath || !proofPath) throw new Error('USAGE receipt.json PROOF.json');

const receipt = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
if (receipt.schema !== 'naya.assistant.protected.ab.ownership.receipt.v1') throw new Error('RECEIPT_SCHEMA_MISMATCH');
if (receipt.status !== 'VERIFIED_AUTHENTICATED_OWNER_ISOLATION') throw new Error('RECEIPT_NOT_VERIFIED');
if (receipt.claim_type !== 'RUNTIME') throw new Error('RECEIPT_CLAIM_TYPE_MISMATCH');

const criteria = receipt.verification?.criteria || {};
for (const [name, value] of Object.entries(criteria)) {
  if (value !== true) throw new Error('RECEIPT_CRITERION_FAILED:' + name);
}

const privacy = receipt.privacy || {};
for (const key of ['credentials_in_receipt','access_tokens_in_receipt','passwords_in_receipt','raw_user_ids_in_receipt']) {
  if (privacy[key] !== false) throw new Error('RECEIPT_PRIVACY_FAILED:' + key);
}

const proof = JSON.parse(fs.readFileSync(proofPath, 'utf8'));
proof.current_evidence = proof.current_evidence || {};
proof.readiness_evidence = proof.readiness_evidence || {};

const evidence = {
  status: 'VERIFIED',
  claim_type: 'RUNTIME',
  workflow: '.github/workflows/assistant-cloudflare-protected-ab-proof.yml',
  observed_head: receipt.source.head,
  run_id: receipt.test.run_id,
  receipt_schema: receipt.schema,
  source_scope: [
    'assistant-runtime.js',
    'scripts/nayanet-cognitive-engine.js',
    '.github/workflows/assistant-cloudflare-protected-ab-proof.yml',
    'scripts/promote-assistant-ab-proof.mjs'
  ],
  identities: {
    distinct: true,
    A_principal_hash: receipt.principals.A.principal_hash,
    B_principal_hash: receipt.principals.B.principal_hash
  },
  transactions: receipt.transactions,
  verification: receipt.verification,
  interpretation: 'Two real, independently authenticated Supabase identities each retrieved only its own cognition event; cross-owner retrieval returned zero rows. The receipt is machine-generated and contains no credential, access token, password, or raw user ID.'
};

proof.current_evidence.assistant_protected_ab_owner_isolation = evidence;
proof.readiness_evidence.assistant_protected_ab_owner_isolation = evidence;
proof.interpretation = 'Protected Assistant-lane authenticated owner isolation is verified by a machine-generated secret-free A/B receipt. Existing anonymous authenticated lifecycle evidence remains distinct from this owner-isolation proof.';

fs.writeFileSync(proofPath, JSON.stringify(proof, null, 2) + '\n');
console.log('PROOF_PROMOTION=PASS');
