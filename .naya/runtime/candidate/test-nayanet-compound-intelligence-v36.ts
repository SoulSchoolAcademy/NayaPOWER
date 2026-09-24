/**
 * RED-first Deno harness for the actual TypeScript v36 execution seam.
 * No Supabase client, no network, no production mutation.
 */
import {
  ACTION_TYPE, PERMISSION, TARGET, REPOSITORY,
  buildTestArtifact, buildTestKeypair, commitIntelligenceV36Candidate,
  executionBindingHash, portableArtifactHash,
  type AuthorityRegistry, type ExecutionAuthorization, type V36Request,
} from "./nayanet-compound-intelligence-v36.ts";

const NOW = "2026-01-01T00:00:00.000Z";
const EXPIRES = "2026-01-01T00:01:00.000Z";
const SHA = "d253610f8ff8f27a838294a04c8893bf71bf7d4e";
const ACTOR = "execution-facing-actor";
const AUTHORITY = "execution-facing-authority";

const registry: AuthorityRegistry = {
  authorities: {
    [AUTHORITY]: {
      authority_id: AUTHORITY,
      principal_id: ACTOR,
      purpose: "execution-facing portable intelligence boundary",
      scope: "NayaNET",
      granted_actions: [PERMISSION],
      expires_at: "2030-01-01T00:00:00.000Z",
      revoked: false,
    },
  },
};

const unsignedAuth: ExecutionAuthorization = {
  authority_id: AUTHORITY,
  decision_id: "execution-facing-decision",
  action_id: "execution-facing-action",
  action_type: ACTION_TYPE,
  target: TARGET,
  actor_id: ACTOR,
  scope: "NayaNET",
  permission: PERMISSION,
  governance_state: "AUTHORIZED",
  binding_hash: "",
};

unsignedAuth.binding_hash = await executionBindingHash(unsignedAuth);

const keys = await buildTestKeypair();
const wrongKeys = await buildTestKeypair();
const artifact = await buildTestArtifact(unsignedAuth, registry, keys.privateKey, SHA, NOW, EXPIRES);

function request(a: any = artifact, ordinary: any = unsignedAuth): V36Request {
  return {
    execution_authorization: structuredClone(ordinary),
    portable_authorization: structuredClone(a),
    portable_authorization_artifact_hash: "",
    idempotency_key: "ts-v36-red-first",
    content: "candidate intelligence",
    title: "v36 candidate",
  };
}

const base = request();
base.portable_authorization_artifact_hash = await portableArtifactHash(base.portable_authorization);

let recordCalls = 0;
const recordFn = async () => {
  recordCalls += 1;
  return { receipt_id: "SIMULATED-RECEIPT" };
};

const attacks: Array<[string, () => Promise<V36Request>]> = [
  ["missing artifact", async () => { const x = request(); x.portable_authorization = undefined as any; return x; }],
  ["missing artifact hash", async () => { const x = structuredClone(base); x.portable_authorization_artifact_hash = ""; return x; }],
  ["malformed artifact", async () => { const x = structuredClone(base); x.portable_authorization = { schema: "broken" } as any; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["tampered field", async () => { const x = structuredClone(base); x.portable_authorization.authorization.target = "evil"; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["tampered signature", async () => { const x = structuredClone(base); x.portable_authorization.signature = "00".repeat(64); x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["wrong issuer key", async () => structuredClone(base)],
  ["unsigned", async () => { const x = structuredClone(base); delete x.portable_authorization.signature; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["wrong authority", async () => { const x = structuredClone(base); x.portable_authorization.authorization.authority_id = "wrong"; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["wrong actor", async () => { const x = structuredClone(base); x.portable_authorization.authorization.actor_id = "wrong"; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["wrong decision", async () => { const x = structuredClone(base); x.portable_authorization.authorization.decision_id = "wrong"; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["wrong action", async () => { const x = structuredClone(base); x.portable_authorization.authorization.action_id = "wrong"; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["wrong target", async () => { const x = structuredClone(base); x.portable_authorization.authorization.target = "evil"; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["wrong permission", async () => { const x = structuredClone(base); x.portable_authorization.authorization.permission = "repo_write"; x.portable_authorization_artifact_hash = await portableArtifactHash(x.portable_authorization); return x; }],
  ["expired", async () => structuredClone(base)],
  ["revoked", async () => structuredClone(base)],
  ["artifact hash mismatch", async () => { const x = structuredClone(base); x.portable_authorization.authorization.target = "evil"; return x; }],
  ["ordinary authorization mismatch", async () => { const x = structuredClone(base); x.execution_authorization = structuredClone(unsignedAuth); x.execution_authorization.actor_id = "different-actor"; return x; }],
];

for (const [label, make] of attacks) {
  const before = recordCalls;
  const x = await make();
  let now = NOW;
  let reg = registry;
  let pub = keys.publicKeyHex;
  if (label === "wrong issuer key") pub = wrongKeys.publicKeyHex;
  if (label === "expired") now = "2026-01-01T00:02:00.000Z";
  if (label === "revoked") reg = { authorities: { ...registry.authorities, [AUTHORITY]: { ...registry.authorities[AUTHORITY], revoked: true } } };
  const result = await commitIntelligenceV36Candidate(x, pub, reg, SHA, now, recordFn);
  if (result.ok) throw new Error(label + ": unexpectedly allowed");
  if (recordCalls !== before) throw new Error(label + ": record path was reached");
}

const legitimate = await commitIntelligenceV36Candidate(base, keys.publicKeyHex, registry, SHA, NOW, recordFn);
if (!legitimate.ok) throw new Error("legitimate credential rejected: " + legitimate.error);
if (recordCalls !== 1) throw new Error("legitimate credential did not call record exactly once: " + recordCalls);

console.log("V36_DENO_EXECUTION_SEAM_RED_FIRST=PASS");
console.log("17 attacks: FAIL-CLOSED + record_calls=0");
console.log("legitimate credential: PASS + record_calls=1");
console.log("portable signature verification: PASS");
console.log("artifact hash binding: PASS");
console.log("ordinary authorization binding: PASS");
console.log("production deployment: NOT RUN");
console.log("production mutation: NOT RUN");
console.log("live intelligence_commit: NOT RUN");
