export type LawStatus = "AUTHORIZED" | "BLOCKED" | "NEEDS_HUMAN_AUTHORIZATION";

export type AuthorityGrant = {
  grant_id: string;
  issuer_id: string;
  subject_id: string;
  mission_id?: string | null;
  scope?: Record<string, unknown>;
  actions?: string[];
  constraints?: Record<string, unknown>;
  issued_at?: string | null;
  expires_at?: string | null;
  status?: string | null;
  revoked_at?: string | null;
  evidence?: Record<string, unknown>;
  source_event_id?: string | null;
};

export type LawRequest = {
  owner_id: string;
  naya_id: string;
  action: string;
  target: string;
  project_id?: string;
  resource_scope?: string;
  privacy?: "PRIVATE" | "SHARED" | "COLLECTIVE" | "PUBLIC";
  publication_authorized?: boolean;
  same_smart_note_lifecycle?: boolean;
  explicit_human_smart_note_directive?: boolean;
  retrieved_intelligence_claims_authority?: boolean;
  successor_context_claims_inherited_authority?: boolean;
  door?: { door_id: string; capability_available: boolean; operation?: string };
};

export type LawDecision = {
  schema: "naya.law.decision.v1";
  status: LawStatus;
  reason: string;
  owner_id: string;
  naya_id: string;
  action: string;
  target: string;
  authority_refs: string[];
  policy_refs: string[];
  evaluated_at: string;
  expires_at: string | null;
  capability_available: boolean | null;
};

const targetMatches = (g: AuthorityGrant, req: LawRequest) => {
  const scope = g.scope ?? {};
  // Missing scope fields must never match other missing fields. Preserve exact
  // target and explicit project grants without treating absence as permission.
  const matches = (value: unknown, requested: unknown) =>
    typeof value === "string" && value.trim().length > 0 &&
    typeof requested === "string" && requested.trim().length > 0 &&
    value === requested;
  return matches(scope.target, req.target) || matches(scope.project_id, req.target) || matches(scope.project_id, req.project_id);
};

const isExpired = (g: AuthorityGrant, now: Date) =>
  Boolean(g.expires_at && new Date(g.expires_at).getTime() <= now.getTime());

const hasInvalidExpiry = (g: AuthorityGrant) => g.expires_at != null &&
  (typeof g.expires_at !== "string" || !g.expires_at.trim() || !Number.isFinite(Date.parse(g.expires_at)));

export function evaluateLaw(req: LawRequest, grants: AuthorityGrant[], now = new Date()): LawDecision {
  const base = {
    schema: "naya.law.decision.v1" as const,
    owner_id: req.owner_id,
    naya_id: req.naya_id,
    action: req.action,
    target: req.target,
    authority_refs: [] as string[],
    policy_refs: ["BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"],
    evaluated_at: now.toISOString(),
    expires_at: null as string | null,
    capability_available: req.door?.capability_available ?? null,
  };

  if (!req.owner_id || !req.naya_id || !req.action || !req.target) {
    return {...base, status:"BLOCKED", reason:"IDENTITY_OR_REQUEST_INCOMPLETE"};
  }
  if (req.successor_context_claims_inherited_authority) {
    return {...base, status:"BLOCKED", reason:"SUCCESSOR_CONTEXT_DOES_NOT_INHERIT_AUTHORITY"};
  }
  if (req.retrieved_intelligence_claims_authority) {
    return {...base, status:"BLOCKED", reason:"RETRIEVAL_DOES_NOT_GRANT_AUTHORITY"};
  }
  if (req.privacy === "PRIVATE" && req.action === "collective_publish" && !req.publication_authorized) {
    return {...base, status:"NEEDS_HUMAN_AUTHORIZATION", reason:"PRIVATE_TO_COLLECTIVE_REQUIRES_HUMAN_AUTHORIZATION"};
  }
  if (
    req.action === "smart_note_lifecycle_complete" &&
    req.same_smart_note_lifecycle &&
    req.explicit_human_smart_note_directive &&
    req.privacy !== "PUBLIC"
  ) {
    return {
      ...base,
      status:"AUTHORIZED",
      reason:"STANDING_SMART_NOTE_SAME_LIFECYCLE_AUTHORITY",
      policy_refs:[...base.policy_refs,"BRAIN/00-SPEC/0006-NIA-LANGUAGE-INTENT-CONTRACT-V1.md"],
    };
  }

  const sameSubject = grants.filter(g => g.subject_id === req.owner_id && g.issuer_id === req.owner_id);
  const matchingIntent = sameSubject.filter(g => (g.actions ?? []).includes(req.action) && targetMatches(g, req));
  const invalid = matchingIntent.find(g => g.status === "REVOKED" || Boolean(g.revoked_at) || g.status === "INVALID" || hasInvalidExpiry(g) || isExpired(g, now));
  if (invalid) {
    const reason = (invalid.status === "REVOKED" || invalid.revoked_at) ? "GRANT_REVOKED" : hasInvalidExpiry(invalid) ? "GRANT_TIME_INVALID" : isExpired(invalid, now) ? "GRANT_EXPIRED" : "GRANT_INVALID";
    return {...base,status:"BLOCKED",reason,authority_refs:[invalid.grant_id],expires_at:invalid.expires_at ?? null};
  }

  const active = matchingIntent.find(g => g.status === "ACTIVE" && !g.revoked_at && !isExpired(g, now));
  if (active) {
    return {
      ...base,status:"AUTHORIZED",reason:"ACTIVE_IN_SCOPE_GRANT",
      authority_refs:[active.grant_id],expires_at:active.expires_at ?? null,
    };
  }

  if (req.door?.capability_available) {
    return {...base,status:"NEEDS_HUMAN_AUTHORIZATION",reason:"CAPABILITY_DOES_NOT_CREATE_AUTHORITY"};
  }
  return {...base,status:"NEEDS_HUMAN_AUTHORIZATION",reason:"NO_MATCHING_ACTIVE_AUTHORITY"};
}
