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

export type KnowReceipt = {
  id?: string;
  user_id?: string;
  action?: string;
  status?: string;
  evidence?: any;
};

export type SelectedBlock = {
  intelligent_block_id?: string | null;
  owner_id?: string | null;
  status?: string | null;
  understanding_state?: string | null;
  applicable_scope?: any;
  content?: any;
  provenance?: any;
  evidence_refs?: any[];
  superseded_by_block_id?: string | null;
  updated_at?: string | null;
};

export type ActPlan = {
  action: string;
  target: string;
  door_id: string;
  operation: string;
  behavior: string;
};

export type ActPlanResult = {
  schema: "naya.act.plan.v1";
  status: "READY" | "BLOCKED" | "LAW_RERESOLUTION_REQUIRED";
  reason: string;
  guard: ActDecision;
  task_identity: {
    task_id: string;
    task_class: string;
    required_capability: string;
  } | null;
  selector: {
    owner: "KNOW+CONNECT";
    id: "selectKnowContext+selectableConnections";
    version: "naya.know.context-result.v1/connect-selector-v2";
  };
  pre_learning_plan: ActPlan;
  post_retrieval_plan: ActPlan;
  plan_changed: boolean;
  authority_scope_changed: boolean;
  law_reresolution_required: boolean;
  intelligence_applied_to_plan: boolean;
  application_reason: string;
  selected_intelligence: null | {
    intelligent_block_id: string;
    provenance: any;
    evidence_refs: any[];
    lifecycle_state: string;
    truth_state: string;
    applicability: boolean;
    retrieval_reason: string;
  };
  retrieval_receipt_id: string | null;
  effect_executed: false;
};

export const ACT_RETRIEVAL_SELECTOR = {
  owner: "KNOW+CONNECT" as const,
  id: "selectKnowContext+selectableConnections" as const,
  version: "naya.know.context-result.v1/connect-selector-v2" as const,
};

export const ACT_BASELINE_BEHAVIOR = "APPLY_BASELINE_WITHOUT_RETAINED_STEERING";
export const ACT_PROVENANCE_BEHAVIOR = "PRESERVE_PROVENANCE_BEFORE_APPLY";

const SERVABLE_STATUS = new Set(["ACTIVE", "DURABLE", "RELEASED"]);
const SERVABLE_STATES = new Set(["VERIFIED", "DISTILLED", "APPLIED", "LEARNED"]);
const PLAN_PATCH_FIELDS = new Set(["action", "target", "door_id", "operation", "behavior"]);

function canonicalize(value: any): any {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    const out: Record<string, unknown> = {};
    for (const key of Object.keys(value).sort()) out[key] = canonicalize(value[key]);
    return out;
  }
  return value;
}

export function canonicalEqual(a: any, b: any): boolean {
  return JSON.stringify(canonicalize(a)) === JSON.stringify(canonicalize(b));
}

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

function basePlan(req: ActRequest): ActPlan {
  return {
    action: req.action,
    target: req.target,
    door_id: req.door_id,
    operation: req.operation,
    behavior: ACT_BASELINE_BEHAVIOR,
  };
}

function planResult(
  req: ActRequest,
  guard: ActDecision,
  status: ActPlanResult["status"],
  reason: string,
  extra: Partial<ActPlanResult> = {},
): ActPlanResult {
  const baseline=basePlan(req);
  return {
    schema:"naya.act.plan.v1",
    status,
    reason,
    guard,
    task_identity:null,
    selector:ACT_RETRIEVAL_SELECTOR,
    pre_learning_plan:baseline,
    post_retrieval_plan:baseline,
    plan_changed:false,
    authority_scope_changed:false,
    law_reresolution_required:false,
    intelligence_applied_to_plan:false,
    application_reason:reason,
    selected_intelligence:null,
    retrieval_receipt_id:null,
    effect_executed:false,
    ...extra,
  };
}

function authorityScope(plan: ActPlan) {
  return {
    action:plan.action,
    target:plan.target,
    door_id:plan.door_id,
    operation:plan.operation,
  };
}

function taskIdentityFromKnow(receipt: KnowReceipt) {
  const request=receipt?.evidence?.request ?? {};
  const task_id=String(request.task_id ?? "").trim();
  const task_class=String(request.task_class ?? "").trim();
  const required_capability=String(request.required_capability ?? "").trim();
  if (!task_id || !task_class || !required_capability) return null;
  return {task_id,task_class,required_capability};
}

function selectedBlockMatchesReceipt(
  req: ActRequest,
  result: any,
  block: SelectedBlock | null,
): {ok:true} | {ok:false;reason:string} {
  if (!block) return {ok:false,reason:"SELECTED_INTELLIGENCE_NOT_FOUND"};
  if (String(block.intelligent_block_id ?? "") !== String(result.selected_block_id ?? "")) {
    return {ok:false,reason:"SELECTED_INTELLIGENCE_ID_MISMATCH"};
  }
  if (block.owner_id !== req.owner_id) return {ok:false,reason:"SELECTED_INTELLIGENCE_OWNER_MISMATCH"};
  if (!SERVABLE_STATUS.has(String(block.status ?? ""))) return {ok:false,reason:"SELECTED_INTELLIGENCE_LIFECYCLE_NOT_SERVABLE"};
  if (!SERVABLE_STATES.has(String(block.understanding_state ?? ""))) return {ok:false,reason:"SELECTED_INTELLIGENCE_TRUTH_NOT_SERVABLE"};
  if (block.superseded_by_block_id) return {ok:false,reason:"SELECTED_INTELLIGENCE_SUPERSEDED"};
  if (String(block.understanding_state ?? "") !== String(result.selected_epistemic_state ?? "")) {
    return {ok:false,reason:"SELECTED_INTELLIGENCE_TRUTH_MISMATCH"};
  }
  if (!block.provenance || Object.keys(block.provenance).length===0) {
    return {ok:false,reason:"SELECTED_INTELLIGENCE_PROVENANCE_MISSING"};
  }
  if (!Array.isArray(block.evidence_refs) || block.evidence_refs.length===0) {
    return {ok:false,reason:"SELECTED_INTELLIGENCE_EVIDENCE_MISSING"};
  }
  if (!canonicalEqual(block.provenance,result.selected_provenance)) {
    return {ok:false,reason:"SELECTED_INTELLIGENCE_PROVENANCE_MISMATCH"};
  }
  if (!canonicalEqual(block.evidence_refs,result.selected_evidence_refs)) {
    return {ok:false,reason:"SELECTED_INTELLIGENCE_EVIDENCE_MISMATCH"};
  }
  const target=String(block.applicable_scope?.target ?? "");
  if (target && target!==req.naya_id) return {ok:false,reason:"SELECTED_INTELLIGENCE_APPLICABILITY_MISMATCH"};
  return {ok:true};
}

function applyBlockToPlan(pre: ActPlan, task: NonNullable<ActPlanResult["task_identity"]>, block: SelectedBlock) {
  const post={...pre};
  const content=(block.content && typeof block.content==="object") ? block.content : {};
  const patch=(content as any).act_plan_patch;
  if (patch && typeof patch==="object" && !Array.isArray(patch)) {
    for (const [key,value] of Object.entries(patch)) {
      if (PLAN_PATCH_FIELDS.has(key) && value!==undefined) (post as any)[key]=String(value);
    }
  }
  const lesson=String((content as any).lesson ?? "");
  if (
    task.required_capability==="provenance_preservation" &&
    /preserve provenance before applying retained intelligence/i.test(lesson)
  ) {
    post.behavior=ACT_PROVENANCE_BEHAVIOR;
  }
  return post;
}

export function buildActPlan(
  req: ActRequest,
  lawReceipt: LawReceipt | null,
  liveGrant: Grant | null,
  door: DoorOperation | null,
  knowReceipt: KnowReceipt | null,
  selectedBlock: SelectedBlock | null,
  now = new Date(),
): ActPlanResult {
  const guard=validateAct(req,lawReceipt,liveGrant,door,now);
  if (guard.status!=="READY") return planResult(req,guard,"BLOCKED",guard.reason);

  if (!knowReceipt) return planResult(req,guard,"BLOCKED","KNOW_RECEIPT_REQUIRED");
  const retrievalId=String(knowReceipt.id ?? "");
  if (knowReceipt.user_id!==req.owner_id) return planResult(req,guard,"BLOCKED","KNOW_RECEIPT_OWNER_MISMATCH",{retrieval_receipt_id:retrievalId});
  if (knowReceipt.action!=="know_context_retrieval" || knowReceipt.status!=="SUCCESS") {
    return planResult(req,guard,"BLOCKED","KNOW_RECEIPT_INVALID",{retrieval_receipt_id:retrievalId});
  }

  const ev=knowReceipt.evidence ?? {};
  const knowRequest=ev.request ?? {};
  const result=ev.result ?? {};
  const task=taskIdentityFromKnow(knowReceipt);
  if (ev.schema!=="naya.know.receipt.v1" || ev.node_id!=="NAYA-KERNEL-KNOW") {
    return planResult(req,guard,"BLOCKED","KNOW_RECEIPT_SCHEMA_INVALID",{retrieval_receipt_id:retrievalId});
  }
  if (ev.law_receipt_id!==guard.law_receipt_id) {
    return planResult(req,guard,"BLOCKED","KNOW_LAW_BINDING_MISMATCH",{retrieval_receipt_id:retrievalId});
  }
  const authorityRefs=Array.isArray(ev.authority_refs)?ev.authority_refs.map(String):[];
  if (authorityRefs.length!==1 || authorityRefs[0]!==guard.authority_grant_id) {
    return planResult(req,guard,"BLOCKED","KNOW_AUTHORITY_BINDING_MISMATCH",{retrieval_receipt_id:retrievalId});
  }
  if (ev.caller_selected_block!==false || ev.retrieval_creates_authority!==false) {
    return planResult(req,guard,"BLOCKED","KNOW_BOUNDARY_INVALID",{retrieval_receipt_id:retrievalId});
  }
  if (!task) return planResult(req,guard,"BLOCKED","KNOW_TASK_IDENTITY_MISSING",{retrieval_receipt_id:retrievalId});
  if (
    String(result.schema ?? "")!=="naya.know.context-result.v1" ||
    String(result.task_id ?? "")!==task.task_id ||
    String(result.required_capability ?? "")!==task.required_capability ||
    result.retrieval_creates_authority!==false
  ) {
    return planResult(req,guard,"BLOCKED","KNOW_RESULT_BINDING_INVALID",{retrieval_receipt_id:retrievalId,task_identity:task});
  }
  if (
    String(knowRequest.task_id ?? "")!==task.task_id ||
    String(knowRequest.task_class ?? "")!==task.task_class ||
    String(knowRequest.required_capability ?? "")!==task.required_capability
  ) {
    return planResult(req,guard,"BLOCKED","KNOW_REQUEST_BINDING_INVALID",{retrieval_receipt_id:retrievalId,task_identity:task});
  }

  const pre=basePlan(req);
  if (result.status==="MISS") {
    return planResult(req,guard,"READY","NO_APPLICABLE_RETAINED_INTELLIGENCE",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
      pre_learning_plan:pre,
      post_retrieval_plan:{...pre},
      application_reason:String(result.reason ?? "NO_APPLICABLE_RETAINED_INTELLIGENCE"),
    });
  }
  if (result.status!=="HIT" || result.applicable!==true || !result.selected_block_id) {
    return planResult(req,guard,"BLOCKED","KNOW_RESULT_NOT_APPLICABLE",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
    });
  }
  if (result.conflict_detected===true) {
    return planResult(req,guard,"READY","CONFLICTED_INTELLIGENCE_NON_STEERING",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
      pre_learning_plan:pre,
      post_retrieval_plan:{...pre},
      application_reason:"CONFLICT_SURFACED_BY_CONNECT_NO_STEERING",
    });
  }

  const snapshot=selectedBlockMatchesReceipt(req,result,selectedBlock);
  if ("reason" in snapshot) {
    return planResult(req,guard,"BLOCKED",snapshot.reason,{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
    });
  }

  const post=applyBlockToPlan(pre,task,selectedBlock as SelectedBlock);
  const planChanged=!canonicalEqual(pre,post);
  const scopeChanged=!canonicalEqual(authorityScope(pre),authorityScope(post));
  const selected={
    intelligent_block_id:String(selectedBlock?.intelligent_block_id ?? ""),
    provenance:selectedBlock?.provenance ?? null,
    evidence_refs:Array.isArray(selectedBlock?.evidence_refs)?selectedBlock?.evidence_refs:[],
    lifecycle_state:String(selectedBlock?.status ?? ""),
    truth_state:String(selectedBlock?.understanding_state ?? ""),
    applicability:true,
    retrieval_reason:String(result.reason ?? ""),
  };
  if (scopeChanged) {
    return planResult(req,guard,"LAW_RERESOLUTION_REQUIRED","LAW_RERESOLUTION_REQUIRED",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
      pre_learning_plan:pre,
      post_retrieval_plan:post,
      plan_changed:planChanged,
      authority_scope_changed:true,
      law_reresolution_required:true,
      intelligence_applied_to_plan:false,
      application_reason:"RETRIEVED_INTELLIGENCE_CHANGED_CONSEQUENTIAL_SCOPE",
      selected_intelligence:selected,
    });
  }

  return planResult(req,guard,"READY",planChanged?"APPLICABLE_INTELLIGENCE_STEERED_PLAN":"APPLICABLE_INTELLIGENCE_NO_PLAN_DELTA",{
    retrieval_receipt_id:retrievalId,
    task_identity:task,
    pre_learning_plan:pre,
    post_retrieval_plan:post,
    plan_changed:planChanged,
    intelligence_applied_to_plan:planChanged,
    application_reason:planChanged
      ? "NORMAL_KNOW_CONNECT_SELECTION_CHANGED_ACT_PLAN"
      : "SELECTED_INTELLIGENCE_HAS_NO_ACT_PLAN_EFFECT",
    selected_intelligence:selected,
  });
}
