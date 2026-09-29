export type ActStatus = "READY" | "BLOCKED";

export type LawReceipt = {
  id?: string;
  user_id?: string;
  action?: string;
  status?: string;
  evidence?: any;
  created_at?: string;
};

export type Grant = {
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
};

export type DoorOperation = {
  door_id: string;
  operation: string;
  authority_action: string;
  target: string;
  consequential: boolean;
  max_law_age_seconds?: number | null;
};

export type ActRequest = {
  owner_id: string;
  naya_id: string;
  law_receipt_id?: string;
  action: string;
  target: string;
  door_id: string;
  operation: string;
  retrieved_intelligence_claims_authority?: boolean;
  successor_context_claims_inherited_authority?: boolean;
};

export type ActDecision = {
  schema: "naya.act.guard.v1";
  status: ActStatus;
  reason: string;
  law_receipt_id: string | null;
  authority_grant_id: string | null;
  door_id: string;
  operation: string;
  action: string;
  target: string;
};

const blocked = (req: ActRequest, reason: string, lawId: string | null = null, grantId: string | null = null): ActDecision => ({
  schema:"naya.act.guard.v1",status:"BLOCKED",reason,law_receipt_id:lawId,authority_grant_id:grantId,
  door_id:req.door_id,operation:req.operation,action:req.action,target:req.target
});

export function validateAct(
  req: ActRequest,
  lawReceipt: LawReceipt | null,
  liveGrant: Grant | null,
  door: DoorOperation | null,
  now = new Date()
): ActDecision {
  if (!lawReceipt) return blocked(req,"LAW_RECEIPT_REQUIRED");
  const lawId=String(lawReceipt.id ?? req.law_receipt_id ?? "");
  if (lawReceipt.user_id !== req.owner_id) return blocked(req,"LAW_RECEIPT_OWNER_MISMATCH",lawId);
  if (lawReceipt.action !== "law_authority_decision") return blocked(req,"LAW_RECEIPT_TYPE_INVALID",lawId);
  if (lawReceipt.status !== "SUCCESS") return blocked(req,"LAW_NOT_AUTHORIZED",lawId);

  const ev=lawReceipt.evidence ?? {};
  const decision=ev.law_decision ?? {};
  const lawReq=ev.law_request ?? {};
  if (ev.node_id !== "NAYA-KERNEL-LAW") return blocked(req,"LAW_RECEIPT_NODE_INVALID",lawId);
  if (decision.status !== "AUTHORIZED") return blocked(req,"LAW_NOT_AUTHORIZED",lawId);
  if (decision.owner_id !== req.owner_id || decision.naya_id !== req.naya_id) return blocked(req,"LAW_IDENTITY_MISMATCH",lawId);
  if (lawReq.action !== req.action || decision.action !== req.action) return blocked(req,"AUTHORIZED_ACTION_MISMATCH",lawId);
  if (lawReq.target !== req.target || decision.target !== req.target) return blocked(req,"AUTHORIZED_TARGET_MISMATCH",lawId);

  if (req.retrieved_intelligence_claims_authority) return blocked(req,"RETRIEVAL_DOES_NOT_GRANT_AUTHORITY",lawId);
  if (req.successor_context_claims_inherited_authority) return blocked(req,"SUCCESSOR_CONTEXT_DOES_NOT_INHERIT_AUTHORITY",lawId);

  if (!door) return blocked(req,"SMART_DOOR_OPERATION_NOT_REGISTERED",lawId);
  if (door.door_id !== req.door_id || door.operation !== req.operation) return blocked(req,"SMART_DOOR_OPERATION_MISMATCH",lawId);
  if (door.authority_action !== req.action) return blocked(req,"DOOR_AUTHORITY_BROADER_THAN_LAW",lawId);
  if (door.target !== req.target) return blocked(req,"DOOR_TARGET_MISMATCH",lawId);

  const nowMs = now.getTime();
  const evaluatedMs = typeof decision.evaluated_at === "string" && decision.evaluated_at.trim()
    ? Date.parse(decision.evaluated_at) : NaN;
  if (!Number.isFinite(nowMs) || !Number.isFinite(evaluatedMs) || evaluatedMs > nowMs) {
    return blocked(req,"LAW_RECEIPT_TIME_INVALID",lawId);
  }
  if (door.max_law_age_seconds) {
    const age=(nowMs-evaluatedMs)/1000;
    if (age > door.max_law_age_seconds) return blocked(req,"LAW_RECEIPT_STALE",lawId);
  }
  if (decision.expires_at != null) {
    const expiryMs = typeof decision.expires_at === "string" && decision.expires_at.trim()
      ? Date.parse(decision.expires_at) : NaN;
    if (!Number.isFinite(expiryMs)) return blocked(req,"LAW_AUTHORITY_TIME_INVALID",lawId);
    if (expiryMs <= nowMs) return blocked(req,"LAW_AUTHORITY_EXPIRED",lawId);
  }

  const refs=Array.isArray(decision.authority_refs)?decision.authority_refs:[];
  if (refs.length !== 1) return blocked(req,"LAW_AUTHORITY_REFERENCE_INVALID",lawId);
  const grantId=String(refs[0]);
  if (!liveGrant || liveGrant.grant_id !== grantId) return blocked(req,"LIVE_AUTHORITY_NOT_FOUND",lawId,grantId);
  if (liveGrant.issuer_id !== req.owner_id || liveGrant.subject_id !== req.owner_id) return blocked(req,"LIVE_AUTHORITY_OWNER_MISMATCH",lawId,grantId);
  if (liveGrant.status !== "ACTIVE" || liveGrant.revoked_at) return blocked(req,"LIVE_AUTHORITY_NOT_ACTIVE",lawId,grantId);
  if (liveGrant.expires_at != null) {
    const expiryMs = typeof liveGrant.expires_at === "string" && liveGrant.expires_at.trim()
      ? Date.parse(liveGrant.expires_at) : NaN;
    if (!Number.isFinite(expiryMs)) return blocked(req,"LIVE_AUTHORITY_TIME_INVALID",lawId,grantId);
    if (expiryMs <= nowMs) return blocked(req,"LIVE_AUTHORITY_EXPIRED",lawId,grantId);
  }
  if (!Array.isArray(liveGrant.actions) || !liveGrant.actions.includes(req.action)) return blocked(req,"LIVE_AUTHORITY_ACTION_MISMATCH",lawId,grantId);
  if ((liveGrant.scope as any)?.target !== req.target) return blocked(req,"LIVE_AUTHORITY_TARGET_MISMATCH",lawId,grantId);

  return {
    schema:"naya.act.guard.v1",status:"READY",reason:"LAW_AND_LIVE_AUTHORITY_MATCH",
    law_receipt_id:lawId,authority_grant_id:grantId,
    door_id:req.door_id,operation:req.operation,action:req.action,target:req.target
  };
}
