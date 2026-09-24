/**
 * NayaNET compound-intelligence v36 NON-PRODUCTION candidate.
 *
 * Source parity:
 * - deployed v35: nayanet-compound-intelligence
 * - deployed version: 35
 * - deployed source SHA-256: 77940b934c2f1f0b8249c97b73f63ed782631407e62e81194813be6960d489cd
 *
 * This is an execution-seam candidate, not a deployable production function.
 * It preserves the v35 order: ordinary authorization -> intelligence capture
 * event construction -> governed receipt path. v36 adds the portable artifact
 * verification immediately before that receipt path and passes the exact
 * artifact/hash into receipt evidence.
 *
 * NO network, Supabase, production mutation, or live transaction occurs here.
 */

export const V35_SOURCE_VERSION = 35;
export const V35_SOURCE_SHA256 =
  "77940b934c2f1f0b8249c97b73f63ed782631407e62e81194813be6960d489cd";

export const PROJECT = "NayaNET";
export const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
export const ACTION_TYPE = "INTELLIGENCE_COMMIT";
export const PERMISSION = "intelligence_commit";
export const TARGET = "NayaNET";
export const PORTABLE_SCHEMA = "naya/portable_authorization/v1";

export type JsonObject = Record<string, unknown>;

export interface ExecutionAuthorization {
  authority_id: string;
  decision_id: string;
  action_id: string;
  action_type: string;
  target: string;
  actor_id: string;
  scope: string;
  permission: string;
  governance_state: string;
  binding_hash: string;
  [key: string]: unknown;
}

export interface AuthorityRecord {
  authority_id: string;
  principal_id: string;
  purpose: string;
  scope: string;
  granted_actions: string[];
  expires_at: string;
  revoked: boolean;
}

export interface AuthorityRegistry {
  authorities: Record<string, AuthorityRecord>;
}

export interface PortableArtifact {
  schema: string;
  authorization: JsonObject;
  signature: string;
}

export interface ReceiptEvidence {
  portable_authorization: PortableArtifact;
  portable_authorization_artifact_hash: string;
  [key: string]: unknown;
}

export interface V36Request {
  execution_authorization: ExecutionAuthorization;
  portable_authorization: PortableArtifact;
  portable_authorization_artifact_hash: string;
  idempotency_key: string;
  content: string;
  title?: string;
  category?: string;
  topic?: string;
  tags?: string[];
}

export interface BoundaryResult {
  allowed: boolean;
  code: string;
  artifact_hash?: string;
  evidence?: ReceiptEvidence;
}

function canonicalJson(value: unknown): string {
  return JSON.stringify(value, Object.keys(value as object).sort());
}

function canonicalJsonDeep(value: unknown): string {
  if (Array.isArray(value)) return "[" + value.map(canonicalJsonDeep).join(",") + "]";
  if (value !== null && typeof value === "object") {
    return (
      "{" +
      Object.entries(value as JsonObject)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, v]) => JSON.stringify(k) + ":" + canonicalJsonDeep(v))
        .join(",") +
      "}"
    );
  }
  return JSON.stringify(value);
}

function hexToBytes(hex: string): Uint8Array {
  if (!/^[0-9a-fA-F]*$/.test(hex) || hex.length % 2 !== 0) {
    throw new Error("INVALID_HEX");
  }
  return Uint8Array.from(hex.match(/../g) ?? [], (pair) => parseInt(pair, 16));
}

async function sha256Hex(value: string): Promise<string> {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
}

export function executionBindingHash(auth: ExecutionAuthorization): Promise<string> {
  return sha256Hex([
    auth.authority_id,
    auth.decision_id,
    auth.action_id,
    auth.action_type,
    auth.target,
    auth.actor_id,
    auth.scope,
    auth.permission,
  ].join("|"));
}

function parseTime(value: unknown): number | null {
  const t = Date.parse(String(value ?? ""));
  return Number.isFinite(t) ? t : null;
}

function registryRevision(registry: AuthorityRegistry): Promise<string> {
  const grants = Object.values(registry.authorities)
    .sort((a, b) => a.authority_id.localeCompare(b.authority_id))
    .map((a) => [
      a.authority_id,
      a.principal_id,
      a.purpose,
      a.scope,
      [...a.granted_actions].sort(),
      a.expires_at,
      Boolean(a.revoked),
    ]);
  return sha256Hex(canonicalJsonDeep(grants));
}

async function grantFingerprint(authority: AuthorityRecord): Promise<string> {
  return sha256Hex(canonicalJsonDeep({
    authority_id: authority.authority_id,
    principal_id: authority.principal_id,
    purpose: authority.purpose,
    scope: authority.scope,
    granted_actions: [...authority.granted_actions].sort(),
    expires_at: authority.expires_at,
    revoked: Boolean(authority.revoked),
  }));
}

/**
 * Independent verifier used by the execution-facing v36 seam.
 * It does not possess an issuer private key and cannot mint authority.
 */
export async function verifyPortableAuthorization(
  artifact: PortableArtifact,
  publicKeyHex: string,
  registry: AuthorityRegistry,
  nowIso: string,
): Promise<BoundaryResult> {
  if (!artifact || typeof artifact !== "object") return { allowed: false, code: "PORTABLE_AUTHORIZATION_REQUIRED" };
  if (artifact.schema !== PORTABLE_SCHEMA) return { allowed: false, code: "PORTABLE_SCHEMA_INVALID" };
  if (!artifact.authorization || typeof artifact.authorization !== "object") {
    return { allowed: false, code: "PORTABLE_AUTHORIZATION_MALFORMED" };
  }
  if (!artifact.signature) return { allowed: false, code: "PORTABLE_SIGNATURE_REQUIRED" };

  const auth = artifact.authorization;
  const authorityId = String(auth.authority_id ?? "");
  const authority = registry.authorities[authorityId];
  if (!authority) return { allowed: false, code: "AUTHORITY_NOT_IN_REGISTRY" };

  try {
    const publicKey = await crypto.subtle.importKey(
      "raw",
      hexToBytes(publicKeyHex),
      { name: "Ed25519" },
      false,
      ["verify"],
    );
    const signatureOk = await crypto.subtle.verify(
      { name: "Ed25519" },
      publicKey,
      hexToBytes(String(artifact.signature)),
      new TextEncoder().encode(canonicalJsonDeep(auth)),
    );
    if (!signatureOk) return { allowed: false, code: "PORTABLE_SIGNATURE_INVALID" };
  } catch {
    return { allowed: false, code: "PORTABLE_SIGNATURE_INVALID" };
  }

  const required = [
    "authority_id", "decision_id", "action_id", "action_type", "target",
    "actor_id", "scope", "permission", "governance_state", "binding_hash",
  ];
  if (required.some((key) => !String(auth[key] ?? "").trim())) {
    return { allowed: false, code: "PORTABLE_AUTHORIZATION_INCOMPLETE" };
  }
  if (auth.action_type !== ACTION_TYPE) return { allowed: false, code: "ACTION_TYPE_MISMATCH" };
  if (auth.permission !== PERMISSION) return { allowed: false, code: "PERMISSION_MISMATCH" };
  if (auth.target !== TARGET) return { allowed: false, code: "TARGET_MISMATCH" };
  if (auth.governance_state !== "AUTHORIZED") return { allowed: false, code: "GOVERNANCE_STATE_INVALID" };

  if (authority.principal_id !== auth.actor_id) return { allowed: false, code: "REGISTRY_ACTOR_MISMATCH" };
  if (authority.revoked) return { allowed: false, code: "AUTHORITY_REVOKED" };
  const now = parseTime(nowIso);
  const issued = parseTime(auth.issued_at);
  const expires = parseTime(auth.expires_at);
  if (now === null || issued === null || expires === null) return { allowed: false, code: "TIMELINE_INVALID" };
  if (now < issued || now >= expires) return { allowed: false, code: "PORTABLE_AUTHORIZATION_EXPIRED_OR_NOT_YET_VALID" };

  if (String(auth.repository ?? "") !== REPOSITORY) return { allowed: false, code: "REPOSITORY_MISMATCH" };
  if (!String(auth.commit_sha ?? "")) return { allowed: false, code: "SOURCE_COMMIT_MISSING" };

  if (String(auth.authority_fingerprint ?? "") !== await grantFingerprint(authority)) {
    return { allowed: false, code: "AUTHORITY_FINGERPRINT_MISMATCH" };
  }
  if (String(auth.registry_revision ?? "") !== await registryRevision(registry)) {
    return { allowed: false, code: "REGISTRY_REVISION_MISMATCH" };
  }
  if (String(auth.binding_hash) !== await executionBindingHash(auth as ExecutionAuthorization)) {
    return { allowed: false, code: "BINDING_HASH_MISMATCH" };
  }

  return { allowed: true, code: "PORTABLE_AUTHORIZATION_VERIFIED" };
}

export async function portableArtifactHash(artifact: PortableArtifact): Promise<string> {
  return sha256Hex(canonicalJsonDeep(artifact));
}

export async function validateExecutionEnvelope(
  request: V36Request,
  publicKeyHex: string,
  registry: AuthorityRegistry,
  expectedActorId: string,
  expectedCommitSha: string,
  nowIso: string,
): Promise<BoundaryResult> {
  if (!request.portable_authorization) return { allowed: false, code: "PORTABLE_AUTHORIZATION_REQUIRED" };
  if (!request.portable_authorization_artifact_hash) return { allowed: false, code: "PORTABLE_ARTIFACT_HASH_REQUIRED" };
  if (!request.execution_authorization) return { allowed: false, code: "EXECUTION_AUTHORIZATION_REQUIRED" };

  const computedHash = await portableArtifactHash(request.portable_authorization);
  if (computedHash !== request.portable_authorization_artifact_hash) {
    return { allowed: false, code: "PORTABLE_ARTIFACT_HASH_MISMATCH" };
  }

  const portable = await verifyPortableAuthorization(
    request.portable_authorization,
    publicKeyHex,
    registry,
    nowIso,
  );
  if (!portable.allowed) return portable;

  const signed = request.portable_authorization.authorization;
  const ordinary = request.execution_authorization;

  const fields = [
    "authority_id", "decision_id", "action_id", "action_type", "target",
    "actor_id", "scope", "permission", "governance_state", "binding_hash",
  ];
  for (const field of fields) {
    if (ordinary[field] !== signed[field]) {
      return { allowed: false, code: "AUTHORIZATION_ARTIFACT_MISMATCH" };
    }
  }

  if (ordinary.actor_id !== expectedActorId) return { allowed: false, code: "ACTOR_MISMATCH" };
  if (signed.actor_id !== expectedActorId) return { allowed: false, code: "ACTOR_MISMATCH" };
  if (String(signed.commit_sha ?? "") !== expectedCommitSha) {
    return { allowed: false, code: "SOURCE_COMMIT_MISMATCH" };
  }

  return {
    allowed: true,
    code: "PORTABLE_AUTHORIZATION_BOUND",
    artifact_hash: computedHash,
    evidence: {
      portable_authorization: structuredClone(request.portable_authorization),
      portable_authorization_artifact_hash: computedHash,
    },
  };
}

/**
 * v35-compatible record seam. In production this is the existing
 * nayanet_record_cognition_event RPC. The candidate injects it so the
 * harness can prove call-count behavior without any mutation.
 */
export type RecordFn = (event: JsonObject, action: string, executionAuthorization: ExecutionAuthorization, evidence: ReceiptEvidence) => Promise<unknown>;

export async function commitIntelligenceV36Candidate(
  request: V36Request,
  publicKeyHex: string,
  registry: AuthorityRegistry,
  expectedCommitSha: string,
  nowIso: string,
  recordFn: RecordFn,
): Promise<{ ok: true; receipt: unknown } | { ok: false; error: string }> {
  // v35 ordinary authorization is represented by the already-bound request
  // credential. The real v36 function keeps its existing
  // requireGovernedIntelligenceAuthorization(...) call before this seam.
  const executionAuthorization = request.execution_authorization;

  if (!request.idempotency_key.trim()) return { ok: false, error: "INTELLIGENCE_IDEMPOTENCY_KEY_REQUIRED" };
  if (!request.content.trim()) return { ok: false, error: "INTELLIGENCE_CONTENT_REQUIRED" };

  const event: JsonObject = {
    event_id: "intelligence:" + request.idempotency_key,
    type: "intelligent_block_capture",
    classification: "intelligent_block",
    title: request.title ?? "Intelligent Block",
    content: request.content,
    source: "nayanet-compound-intelligence",
    status: "active",
    actor: "naya",
    schema_version: "INTELLIGENT_BLOCK_V1",
    metadata: { idempotency_key: request.idempotency_key },
  };

  // === V36 PORTABLE BOUNDARY: IMMEDIATELY BEFORE THE EXISTING RECORD PATH ===
  const portable = await validateExecutionEnvelope(
    request,
    publicKeyHex,
    registry,
    executionAuthorization.actor_id,
    expectedCommitSha,
    nowIso,
  );
  if (!portable.allowed) return { ok: false, error: portable.code };

  // Existing v35 record() path, now unreachable unless the portable
  // artifact + signature + hash + ordinary authorization are all bound.
  const receipt = await recordFn(
    event,
    "intelligence.capture",
    executionAuthorization,
    portable.evidence!,
  );
  return { ok: true, receipt };
}

export async function buildTestArtifact(
  auth: ExecutionAuthorization,
  registry: AuthorityRegistry,
  privateKey: CryptoKey,
  commitSha: string,
  issuedAt: string,
  expiresAt: string,
): Promise<PortableArtifact> {
  const authorization: JsonObject = {
    ...auth,
    repository: REPOSITORY,
    commit_sha: commitSha,
    change_set: [],
    environment: "",
    deployment_surface: "",
    worker_name: "",
    project_id: "",
    issued_at: issuedAt,
    expires_at: expiresAt,
    authority_fingerprint: await grantFingerprint(registry.authorities[auth.authority_id]),
    registry_revision: await registryRevision(registry),
  };
  const signature = new Uint8Array(await crypto.subtle.sign(
    { name: "Ed25519" },
    privateKey,
    new TextEncoder().encode(canonicalJsonDeep(authorization)),
  ));
  return {
    schema: PORTABLE_SCHEMA,
    authorization,
    signature: Array.from(signature, (b) => b.toString(16).padStart(2, "0")).join(""),
  };
}

export async function buildTestKeypair(): Promise<{ privateKey: CryptoKey; publicKeyHex: string }> {
  const pair = await crypto.subtle.generateKey(
    { name: "Ed25519" },
    true,
    ["sign", "verify"],
  ) as CryptoKeyPair;
  const raw = new Uint8Array(await crypto.subtle.exportKey("raw", pair.publicKey));
  return {
    privateKey: pair.privateKey,
    publicKeyHex: Array.from(raw, (b) => b.toString(16).padStart(2, "0")).join(""),
  };
}
