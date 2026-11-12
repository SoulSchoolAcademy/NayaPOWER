import { selectKnowContext, type IntelligentBlock, type KnowRequest } from "../nayanet-know-runtime/know.ts";
import type { DecisionContext } from "./decision-context.ts";

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

export type SelectedBlock = IntelligentBlock;

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
  selection_replay_verified: boolean;
  selection_replay_reason: string;
  selection_now: string | null;
  effect_executed: false;
  // WO4 seam: the verified-learning decision context consulted for this plan.
  // Pinned on every result (even BLOCKED) so the receipt records what learning
  // was available. The context itself never claims influence — see
  // measureLearningInfluence for the controlled-intervention measurement.
  decision_context: DecisionContext | null;
  learning_context_applied: boolean;
  learning_prescription: string | null;
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
// Retained intelligence may propose a change to LAW-governed scope, but that
// proposal can never authorize itself: any changed field below forces
// LAW_RERESOLUTION_REQUIRED before effect. Non-scope behavior is NOT accepted as
// an arbitrary patch; bounded behavior steering stays capability-specific below.
const PLAN_PATCH_FIELDS = new Set(["action", "target", "door_id", "operation"]);

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
    selection_replay_verified:false,
    selection_replay_reason:reason,
    selection_now:null,
    effect_executed:false,
    decision_context:null,
    learning_context_applied:false,
    learning_prescription:null,
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

function replayKnowSelection(
  req: ActRequest,
  receipt: KnowReceipt,
  universe: SelectedBlock[] | null,
): {ok:true;selection_now:string;recomputed:any} | {ok:false;reason:string} {
  if (!Array.isArray(universe)) return {ok:false,reason:"KNOW_SELECTION_UNIVERSE_REQUIRED"};
  const ev=receipt.evidence ?? {};
  const recorded=ev.result ?? {};
  const task=taskIdentityFromKnow(receipt);
  if (!task) return {ok:false,reason:"KNOW_TASK_IDENTITY_MISSING"};
  const rawSelectionNow=ev.selection_now;
  const selectionMs=typeof rawSelectionNow==="string" ? Date.parse(rawSelectionNow) : NaN;
  if (!Number.isFinite(selectionMs)) return {ok:false,reason:"KNOW_SELECTION_TIME_INVALID"};

  const replayRequest:KnowRequest={
    owner_id:req.owner_id,
    naya_id:req.naya_id,
    task_id:task.task_id,
    task_class:task.task_class,
    required_capability:task.required_capability,
  };
  const recomputed=selectKnowContext(replayRequest,universe,new Date(selectionMs));
  if (!canonicalEqual(recorded,recomputed)) return {ok:false,reason:"KNOW_SELECTION_REPLAY_MISMATCH"};
  return {ok:true,selection_now:new Date(selectionMs).toISOString(),recomputed};
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

// WO4 — verified-lesson → decision seam.
//
// A verified lesson steers the plan only when it PRESCRIBES a behavior change
// for the plan's task. Prescriptions are explicit, mechanical, capability-bound
// rules — the same convention as applyBlockToPlan above — never free-text
// interpretation of the claim. A lesson that is present but prescribes nothing
// for this task changes nothing: availability without a prescription is not
// influence (PR #1733).
const LESSON_PRESCRIPTIONS: ReadonlyArray<{
  capability: string;
  claimPattern: RegExp;
  behavior: string;
  prescription: string;
}> = [
  {
    capability: "provenance_preservation",
    claimPattern: /preserve provenance before applying retained intelligence/i,
    behavior: ACT_PROVENANCE_BEHAVIOR,
    prescription: "PRESERVE_PROVENANCE_BEFORE_APPLY",
  },
];

export function applyDecisionContextToPlan(
  pre: ActPlan,
  task: { required_capability?: string } | null,
  decisionContext: DecisionContext | null,
): { plan: ActPlan; applied: boolean; prescription: string | null } {
  const post = { ...pre };
  if (!decisionContext?.learning_context_available) return { plan: post, applied: false, prescription: null };
  const claim = String(decisionContext.context?.claim ?? "");
  const capability = String(task?.required_capability ?? "");
  for (const rule of LESSON_PRESCRIPTIONS) {
    if (capability === rule.capability && rule.claimPattern.test(claim)) {
      post.behavior = rule.behavior;
      return { plan: post, applied: true, prescription: rule.prescription };
    }
  }
  return { plan: post, applied: false, prescription: null };
}

export type LearningInfluence = {
  influenced: boolean;
  control_behavior: string | null;
  treatment_behavior: string | null;
  // NO_VERIFIED_LEARNING_CONTEXT: no ACTIVE lesson existed — the control arm.
  // OBSERVED_BEHAVIORAL_DELTA: the treatment plan differs from the control plan;
  //   the lesson caused the delta (arms differ ONLY in the lesson input).
  // LESSON_PRESENT_NO_PLAN_DELTA: a lesson was available but prescribed nothing
  //   for this task — present, not influential. This is the PR #1733 boundary.
  // PLANS_NOT_COMPARABLE: an arm was not READY (blocked/rerouted); no honest
  //   delta can be read, so influence stays false.
  basis: "NO_VERIFIED_LEARNING_CONTEXT" | "OBSERVED_BEHAVIORAL_DELTA" | "LESSON_PRESENT_NO_PLAN_DELTA" | "PLANS_NOT_COMPARABLE";
};

// The controlled intervention: controlPlan is built with decisionContext=null,
// treatmentPlan with the lesson. influenced is true ONLY when the two arms
// differ observably — never on mere lesson presence.
export function measureLearningInfluence(
  decisionContext: DecisionContext | null,
  controlPlan: ActPlanResult,
  treatmentPlan: ActPlanResult,
): LearningInfluence {
  const controlBehavior = controlPlan?.post_retrieval_plan?.behavior ?? null;
  const treatmentBehavior = treatmentPlan?.post_retrieval_plan?.behavior ?? null;
  if (!decisionContext?.learning_context_available) {
    return { influenced: false, control_behavior: controlBehavior, treatment_behavior: treatmentBehavior, basis: "NO_VERIFIED_LEARNING_CONTEXT" };
  }
  if (controlPlan?.status !== "READY" || treatmentPlan?.status !== "READY") {
    return { influenced: false, control_behavior: controlBehavior, treatment_behavior: treatmentBehavior, basis: "PLANS_NOT_COMPARABLE" };
  }
  const delta = !canonicalEqual(controlPlan.post_retrieval_plan, treatmentPlan.post_retrieval_plan);
  return {
    influenced: delta,
    control_behavior: controlBehavior,
    treatment_behavior: treatmentBehavior,
    basis: delta ? "OBSERVED_BEHAVIORAL_DELTA" : "LESSON_PRESENT_NO_PLAN_DELTA",
  };
}

export function buildActPlan(
  req: ActRequest,
  lawReceipt: LawReceipt | null,
  liveGrant: Grant | null,
  door: DoorOperation | null,
  knowReceipt: KnowReceipt | null,
  selectedBlock: SelectedBlock | null,
  selectionUniverse: SelectedBlock[] | null,
  now = new Date(),
  decisionContext: DecisionContext | null = null,
): ActPlanResult {
  const guard=validateAct(req,lawReceipt,liveGrant,door,now);
  const dc: DecisionContext | null = decisionContext ?? null;
  // Every result pins the consulted decision context so the receipt records
  // what verified learning was available even when the plan is blocked.
  // Causal influence is NOT decided here — the caller builds a control arm
  // (dc=null) and measures the delta with measureLearningInfluence.
  const emit=(
    status: ActPlanResult["status"],
    reason: string,
    extra: Partial<ActPlanResult> = {},
  ): ActPlanResult => planResult(req,guard,status,reason,{
    decision_context:dc,
    learning_context_applied:false,
    learning_prescription:null,
    ...extra,
  });
  if (guard.status!=="READY") return emit("BLOCKED",guard.reason);

  if (!knowReceipt) return emit("BLOCKED","KNOW_RECEIPT_REQUIRED");
  const retrievalId=String(knowReceipt.id ?? "");
  if (knowReceipt.user_id!==req.owner_id) return emit("BLOCKED","KNOW_RECEIPT_OWNER_MISMATCH",{retrieval_receipt_id:retrievalId});
  if (knowReceipt.action!=="know_context_retrieval" || knowReceipt.status!=="SUCCESS") {
    return emit("BLOCKED","KNOW_RECEIPT_INVALID",{retrieval_receipt_id:retrievalId});
  }

  const ev=knowReceipt.evidence ?? {};
  const knowRequest=ev.request ?? {};
  const result=ev.result ?? {};
  const task=taskIdentityFromKnow(knowReceipt);
  if (ev.schema!=="naya.know.receipt.v1" || ev.node_id!=="NAYA-KERNEL-KNOW") {
    return emit("BLOCKED","KNOW_RECEIPT_SCHEMA_INVALID",{retrieval_receipt_id:retrievalId});
  }
  if (ev.law_receipt_id!==guard.law_receipt_id) {
    return emit("BLOCKED","KNOW_LAW_BINDING_MISMATCH",{retrieval_receipt_id:retrievalId});
  }
  const authorityRefs=Array.isArray(ev.authority_refs)?ev.authority_refs.map(String):[];
  if (authorityRefs.length!==1 || authorityRefs[0]!==guard.authority_grant_id) {
    return emit("BLOCKED","KNOW_AUTHORITY_BINDING_MISMATCH",{retrieval_receipt_id:retrievalId});
  }
  if (ev.caller_selected_block!==false || ev.retrieval_creates_authority!==false) {
    return emit("BLOCKED","KNOW_BOUNDARY_INVALID",{retrieval_receipt_id:retrievalId});
  }
  if (!task) return emit("BLOCKED","KNOW_TASK_IDENTITY_MISSING",{retrieval_receipt_id:retrievalId});
  if (
    String(result.schema ?? "")!=="naya.know.context-result.v1" ||
    String(result.task_id ?? "")!==task.task_id ||
    String(result.required_capability ?? "")!==task.required_capability ||
    result.retrieval_creates_authority!==false
  ) {
    return emit("BLOCKED","KNOW_RESULT_BINDING_INVALID",{retrieval_receipt_id:retrievalId,task_identity:task});
  }
  if (
    String(knowRequest.task_id ?? "")!==task.task_id ||
    String(knowRequest.task_class ?? "")!==task.task_class ||
    String(knowRequest.required_capability ?? "")!==task.required_capability
  ) {
    return emit("BLOCKED","KNOW_REQUEST_BINDING_INVALID",{retrieval_receipt_id:retrievalId,task_identity:task});
  }

  // Do not trust a persisted KNOW result merely because its selected block,
  // provenance and evidence are self-consistent. Replay the canonical KNOW
  // selector over the owner-scoped current universe at the receipt's pinned
  // selection time. This catches a coherently forged selected ID that points
  // at a real but non-canonical block.
  const replay=replayKnowSelection(req,knowReceipt,selectionUniverse);
  if ("reason" in replay) {
    return emit("BLOCKED",replay.reason,{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
      selection_replay_reason:replay.reason,
    });
  }

  const pre=basePlan(req);
  if (result.status==="MISS") {
    // WO4: the verified lesson steers the post plan even when KNOW missed —
    // the lesson is an independent intelligence input, not a KNOW byproduct.
    const lesson=applyDecisionContextToPlan(pre,task,dc);
    return emit("READY","NO_APPLICABLE_RETAINED_INTELLIGENCE",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
      pre_learning_plan:pre,
      post_retrieval_plan:lesson.plan,
      learning_context_applied:lesson.applied,
      learning_prescription:lesson.prescription,
      selection_replay_verified:true,
      selection_replay_reason:"KNOW_SELECTION_REPLAY_VERIFIED",
      selection_now:replay.selection_now,
      application_reason:String(result.reason ?? "NO_APPLICABLE_RETAINED_INTELLIGENCE"),
    });
  }
  if (result.status!=="HIT" || result.applicable!==true || !result.selected_block_id) {
    return emit("BLOCKED","KNOW_RESULT_NOT_APPLICABLE",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
    });
  }
  if (result.conflict_detected===true) {
    // WO4: conflicted KNOW intelligence does not steer, but an applicable
    // verified lesson still may — the lesson is evaluated independently.
    const lesson=applyDecisionContextToPlan(pre,task,dc);
    return emit("READY","CONFLICTED_INTELLIGENCE_NON_STEERING",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
      pre_learning_plan:pre,
      post_retrieval_plan:lesson.plan,
      learning_context_applied:lesson.applied,
      learning_prescription:lesson.prescription,
      selection_replay_verified:true,
      selection_replay_reason:"KNOW_SELECTION_REPLAY_VERIFIED",
      selection_now:replay.selection_now,
      application_reason:"CONFLICT_SURFACED_BY_CONNECT_NO_STEERING",
    });
  }

  const snapshot=selectedBlockMatchesReceipt(req,result,selectedBlock);
  if ("reason" in snapshot) {
    return emit("BLOCKED",snapshot.reason,{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
    });
  }

  const post=applyBlockToPlan(pre,task,selectedBlock as SelectedBlock);
  // WO4: the verified lesson applies on top of the KNOW-steered plan. The
  // lesson can only steer non-scope behavior; scope is guarded below.
  const lesson=applyDecisionContextToPlan(post,task,dc);
  const lessonedPost=lesson.plan;
  const planChanged=!canonicalEqual(pre,lessonedPost);
  const scopeChanged=!canonicalEqual(authorityScope(pre),authorityScope(lessonedPost));
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
    return emit("LAW_RERESOLUTION_REQUIRED","LAW_RERESOLUTION_REQUIRED",{
      retrieval_receipt_id:retrievalId,
      task_identity:task,
      pre_learning_plan:pre,
      post_retrieval_plan:lessonedPost,
      plan_changed:planChanged,
      authority_scope_changed:true,
      law_reresolution_required:true,
      intelligence_applied_to_plan:false,
      learning_context_applied:lesson.applied,
      learning_prescription:lesson.prescription,
      selection_replay_verified:true,
      selection_replay_reason:"KNOW_SELECTION_REPLAY_VERIFIED",
      selection_now:replay.selection_now,
      application_reason:"RETRIEVED_INTELLIGENCE_CHANGED_CONSEQUENTIAL_SCOPE",
      selected_intelligence:selected,
    });
  }

  return emit("READY",planChanged?"APPLICABLE_INTELLIGENCE_STEERED_PLAN":"APPLICABLE_INTELLIGENCE_NO_PLAN_DELTA",{
    retrieval_receipt_id:retrievalId,
    task_identity:task,
    pre_learning_plan:pre,
    post_retrieval_plan:lessonedPost,
    plan_changed:planChanged,
    intelligence_applied_to_plan:planChanged,
    learning_context_applied:lesson.applied,
    learning_prescription:lesson.prescription,
    selection_replay_verified:true,
    selection_replay_reason:"KNOW_SELECTION_REPLAY_VERIFIED",
    selection_now:replay.selection_now,
    application_reason:planChanged
      ? "NORMAL_KNOW_CONNECT_SELECTION_CHANGED_ACT_PLAN"
      : "SELECTED_INTELLIGENCE_HAS_NO_ACT_PLAN_EFFECT",
    selected_intelligence:selected,
  });
}
