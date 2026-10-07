import { selectableConnections, parsedTime } from "../_shared/connect_selector.ts";

export type KnowRequest = {
  owner_id: string;
  naya_id: string;
  task_id: string;
  task_class: string;
  required_capability: string;
};

export type IntelligentBlock = {
  intelligent_block_id?: string | null;
  owner_id?: string | null;
  status?: string | null;
  understanding_state?: string | null;
  owner_scope?: string | null;
  applicable_scope?: any;
  value_context?: any;
  content?: any;
  provenance?: any;
  evidence_refs?: any[];
  superseded_by_block_id?: string | null;
  updated_at?: string | null;
  // Outbound graph edges, written by the block writer at write time and read
  // from the same row/snapshot as the block itself. Retrieval consumes these
  // edges: the graph is load-bearing, not decorative.
  //
  // Graph V2 projection fields (contract 0003-GRAPH-RELATIONSHIP-CONTRACT-V2,
  // RATIFIED_CONTRACT. The V2
  // columns live on nayanet_brain_relationships; the retrieval path consumes
  // their write-time projection on the block row. Every V2 field is optional:
  // legacy two-field projections ({target_block_id, relationship_type})
  // predate V2 and are evaluated with conservative defaults — never silently
  // dropped, never silently promoted. Retrieval never creates authority from
  // these fields.
  connections?: Array<{
    target_block_id?: string | null;
    relationship_type?: string | null;
    relationship_id?: string | null;
    supersedes_relationship_id?: string | null;
    status?: string | null;          // ACTIVE | REVOKED | SUPERSEDED | INVALIDATED
    epistemic_state?: string | null; // UNKNOWN | CANDIDATE | SUPPORTED | CONTRADICTED | SUPERSEDED | INVALIDATED | LEARNED | VERIFIED
    valid_from?: string | null;
    valid_until?: string | null;     // null = open-ended
    visibility?: string | null;      // PRIVATE | DERIVED_SHARED | PUBLIC_DERIVED
    consent_ref?: string | null;
    applicability?: { state?: string | null; task_classes?: unknown; limitations?: unknown } | null;
  }> | null;
};

export type RelatedContextEntry = {
  block_id: string;
  relationship_type: string;
  epistemic_state: string | null;
  why_admitted: string;
};

export type KnowLawReceipt = {
  id?: string;
  user_id?: string;
  action?: string;
  status?: string;
  evidence?: any;
};

export type KnowGrant = {
  grant_id: string;
  issuer_id: string;
  subject_id: string;
  scope?: any;
  actions?: string[];
  status?: string | null;
  revoked_at?: string | null;
  expires_at?: string | null;
};

export type KnowAuthorityResult =
  | {ok:true; reason:"LAW_AND_LIVE_AUTHORITY_MATCH"; law_receipt_id:string; authority_grant_id:string; authorized_action:string}
  | {ok:false; reason:string};

export type KnowResult = {
  schema: "naya.know.context-result.v1";
  status: "HIT" | "MISS";
  task_id: string;
  required_capability: string;
  selected_block_id: string | null;
  selected_epistemic_state: string | null;
  selected_provenance: any | null;
  selected_evidence_refs: any[];
  applicable: boolean;
  reason: string;
  retrieval_creates_authority: false;
  handoff_to: "NAYA-KERNEL-PROVE";
  // Edge-derived context: relationships that changed or annotated this result.
  // Empty when the selected block carries no usable edges — flat behavior then
  // applies unchanged.
  related_context: RelatedContextEntry[];
  conflict_detected: boolean;
};

const SERVABLE_STATES=new Set(["VERIFIED","DISTILLED","APPLIED","LEARNED"]);
const SERVABLE_STATUS=new Set(["ACTIVE","DURABLE","RELEASED"]);

// Edge types that may attach supporting context to a retrieval result.
const CONTEXT_EDGE_ALLOWLIST=new Set([
  "SUPPORTS","REFINES","CONTEXTUALIZES","VERIFIED_BY","DERIVED_FROM",
  "APPLIES_TO","CORRECTS","LEARNED_FROM","ENABLES","PRODUCES"
]);

// Edge types that surface disagreement. They are admitted to the result so the
// conflict is visible, but they are never merged into the selected context.
const CONFLICT_EDGE_TYPES=new Set(["CONTRADICTS","INVALIDATES"]);

const SUPERSESSION_EDGE="SUPERSEDES";
const MAX_RELATED=5;
const MAX_SUPERSESSION_HOPS=3;

// Follow SUPERSEDES edges from the primary selection toward the current truth.
// Adversarial guards: the walk reads the same input snapshot as selection
// (no TOCTOU re-fetch); an edge can never promote an ineligible block
// (demotion-bypass guard); hops are bounded and cycle-safe.
function chaseSupersession(
  req:KnowRequest,
  selected:IntelligentBlock,
  byId:Map<string,IntelligentBlock>,
  nowMs:number
):{block:IntelligentBlock;followed:string[]}{
  let current=selected;
  const followed:string[]=[];
  const visited=new Set<string>([String(current.intelligent_block_id)]);
  for(let hop=0;hop<MAX_SUPERSESSION_HOPS;hop++){
    // The SUPERSEDES edge itself must pass the V2 gates: an expired,
    // revoked, superseded, or consentless edge can never redirect selection.
    const edge=selectableConnections(current,nowMs).find((c)=>c.relationship_type===SUPERSESSION_EDGE);
    if(!edge) break;
    if(visited.has(edge.target_block_id)) break;
    const target=byId.get(edge.target_block_id);
    if(!target) break;
    if(!isEligibleBlock(req,target)) break;
    if(!deriveCapabilities(target).includes(req.required_capability)) break;
    visited.add(edge.target_block_id);
    followed.push(edge.target_block_id);
    current=target;
  }
  return {block:current,followed};
}

// One-hop related context from the selected block's outbound edges.
// Every admitted target passes isEligibleBlock AND serves the requested
// capability: stale, forged, irrelevant, private, or revoked edges cannot
// influence the result. Order is deterministic (conflicts first, then
// recency, then id) and capped so edge volume cannot game the result.
function relatedContext(
  req:KnowRequest,
  selected:IntelligentBlock,
  byId:Map<string,IntelligentBlock>,
  nowMs:number
):{entries:RelatedContextEntry[];conflict:boolean}{
  const selectedId=String(selected.intelligent_block_id);
  const seen=new Set<string>();
  const scored:Array<{entry:RelatedContextEntry;rank:number;updated:number;id:string}>=[];
  for(const conn of selectableConnections(selected,nowMs)){
    const tid=conn.target_block_id;
    if(tid===selectedId||seen.has(tid)) continue;
    seen.add(tid);
    const target=byId.get(tid);
    if(!target) continue;
    if(!isEligibleBlock(req,target)) continue;
    // Irrelevant edges must not annotate the result: a related block that
    // does not serve the requested capability is excluded, even when it is
    // otherwise eligible. (NEG N3 guard.)
    if(!deriveCapabilities(target).includes(req.required_capability)) continue;
    const isConflict=CONFLICT_EDGE_TYPES.has(conn.relationship_type);
    if(!isConflict&&!CONTEXT_EDGE_ALLOWLIST.has(conn.relationship_type)) continue;
    scored.push({
      entry:{
        block_id:tid,
        relationship_type:conn.relationship_type,
        epistemic_state:String(target.understanding_state??"UNKNOWN"),
        why_admitted:isConflict
          ? `${conn.relationship_type} edge from ${selectedId} — surfaced as conflict, not merged`
          : `${conn.relationship_type} edge from ${selectedId} — eligible owner-scoped intelligence`,
      },
      rank:isConflict?0:1,
      updated:Date.parse(String(target.updated_at??""))||0,
      id:tid,
    });
  }
  scored.sort((a,b)=>a.rank-b.rank||b.updated-a.updated||(a.id<b.id?-1:a.id>b.id?1:0));
  const entries=scored.slice(0,MAX_RELATED).map((s)=>s.entry);
  return {entries,conflict:entries.some((e)=>CONFLICT_EDGE_TYPES.has(e.relationship_type))};
}

export function validateKnowAuthority(
  req:KnowRequest,
  receipt:KnowLawReceipt|null,
  grant:KnowGrant|null,
  now=new Date(),
  maxLawAgeSeconds=900
):KnowAuthorityResult{
  if(!receipt) return {ok:false,reason:"LAW_RECEIPT_REQUIRED"};
  if(receipt.user_id!==req.owner_id) return {ok:false,reason:"LAW_RECEIPT_OWNER_MISMATCH"};
  if(receipt.action!=="law_authority_decision"||receipt.status!=="SUCCESS") return {ok:false,reason:"LAW_RECEIPT_INVALID"};
  const ev=receipt.evidence??{},dec=ev.law_decision??{},lawReq=ev.law_request??{};
  if(ev.node_id!=="NAYA-KERNEL-LAW"||dec.status!=="AUTHORIZED") return {ok:false,reason:"LAW_NOT_AUTHORIZED"};
  if(dec.owner_id!==req.owner_id||dec.naya_id!==req.naya_id) return {ok:false,reason:"LAW_IDENTITY_MISMATCH"};
  if(lawReq.action!=="naya_node_apply"||dec.action!=="naya_node_apply") return {ok:false,reason:"LAW_ACTION_MISMATCH"};
  if(lawReq.target!==req.naya_id||dec.target!==req.naya_id) return {ok:false,reason:"LAW_TARGET_MISMATCH"};
  const evaluatedAt=parsedTime(dec.evaluated_at);
  if(evaluatedAt===null||Number.isNaN(evaluatedAt)||evaluatedAt>now.getTime()) return {ok:false,reason:"LAW_EVALUATED_AT_INVALID"};
  if((now.getTime()-evaluatedAt)/1000>maxLawAgeSeconds) return {ok:false,reason:"LAW_RECEIPT_STALE"};
  const decisionExpiry=parsedTime(dec.expires_at);
  if(Number.isNaN(decisionExpiry)) return {ok:false,reason:"LAW_EXPIRY_INVALID"};
  if(decisionExpiry!==null&&decisionExpiry<=now.getTime()) return {ok:false,reason:"LAW_AUTHORITY_EXPIRED"};
  const refs=Array.isArray(dec.authority_refs)?dec.authority_refs:[];
  if(refs.length!==1) return {ok:false,reason:"LAW_AUTHORITY_REFERENCE_INVALID"};
  const grantId=String(refs[0]);
  if(!grant||grant.grant_id!==grantId) return {ok:false,reason:"LIVE_AUTHORITY_NOT_FOUND"};
  if(grant.issuer_id!==req.owner_id||grant.subject_id!==req.owner_id) return {ok:false,reason:"LIVE_AUTHORITY_OWNER_MISMATCH"};
  if(grant.status!=="ACTIVE"||grant.revoked_at) return {ok:false,reason:"LIVE_AUTHORITY_NOT_ACTIVE"};
  const grantExpiry=parsedTime(grant.expires_at);
  if(Number.isNaN(grantExpiry)) return {ok:false,reason:"LIVE_AUTHORITY_EXPIRY_INVALID"};
  if(grantExpiry!==null&&grantExpiry<=now.getTime()) return {ok:false,reason:"LIVE_AUTHORITY_EXPIRED"};
  const authorizedAction=String(dec.action??lawReq.action??"");
  if(!authorizedAction||!Array.isArray(grant.actions)||!grant.actions.includes(authorizedAction)) return {ok:false,reason:"LIVE_AUTHORITY_ACTION_MISMATCH"};
  if(grant.scope?.target!==req.naya_id) return {ok:false,reason:"LIVE_AUTHORITY_TARGET_MISMATCH"};
  return {ok:true,reason:"LAW_AND_LIVE_AUTHORITY_MATCH",law_receipt_id:String(receipt.id??""),authority_grant_id:grantId,authorized_action:authorizedAction};
}

function structuredCapabilities(block:IntelligentBlock):string[]{
  const scope=block.applicable_scope;
  const direct=Array.isArray(scope?.capabilities)?scope.capabilities.map(String):[];
  const contentCaps=Array.isArray(block.content?.capabilities)?block.content.capabilities.map(String):[];
  return Array.from(new Set([...direct,...contentCaps]));
}

function boundedLegacyCapabilities(block:IntelligentBlock):string[]{
  const lesson=String(block.content?.lesson??"");
  const caps:string[]=[];
  if(/preserve provenance|provenance before applying retained intelligence/i.test(lesson)) caps.push("provenance_preservation");
  return caps;
}

export function deriveCapabilities(block:IntelligentBlock):string[]{
  const structured=structuredCapabilities(block);
  return structured.length?structured:boundedLegacyCapabilities(block);
}

export function isEligibleBlock(req:KnowRequest,block:IntelligentBlock):boolean{
  if(!block.intelligent_block_id) return false;
  if(block.owner_id!==req.owner_id) return false;
  if(!SERVABLE_STATUS.has(String(block.status??""))) return false;
  if(!SERVABLE_STATES.has(String(block.understanding_state??""))) return false;
  if(block.superseded_by_block_id) return false;
  if(!block.provenance || Object.keys(block.provenance).length===0) return false;
  if(!Array.isArray(block.evidence_refs) || block.evidence_refs.length===0) return false;
  const scopeTarget=String(block.applicable_scope?.target??"");
  if(scopeTarget && scopeTarget!==req.naya_id) return false;
  return true;
}

export function selectKnowContext(req:KnowRequest,blocks:IntelligentBlock[],now:Date=new Date()):KnowResult{
  const miss=(reason:string):KnowResult=>({
    schema:"naya.know.context-result.v1",status:"MISS",task_id:req.task_id,required_capability:req.required_capability,
    selected_block_id:null,selected_epistemic_state:null,selected_provenance:null,selected_evidence_refs:[],
    applicable:false,reason,retrieval_creates_authority:false,handoff_to:"NAYA-KERNEL-PROVE",
    related_context:[],conflict_detected:false
  });

  const eligible=blocks
    .filter((b)=>isEligibleBlock(req,b))
    .map((b)=>({block:b,capabilities:deriveCapabilities(b)}))
    .filter((x)=>x.capabilities.includes(req.required_capability))
    .sort((a,b)=>{
      const at=Date.parse(String(a.block.updated_at??""))||0;
      const bt=Date.parse(String(b.block.updated_at??""))||0;
      if(bt!==at) return bt-at;
      return String(a.block.intelligent_block_id).localeCompare(String(b.block.intelligent_block_id));
    });

  if(eligible.length===0) return miss("NO_ELIGIBLE_APPLICABLE_INTELLIGENCE");

  // Edge inputs resolve from the same snapshot as selection: no re-fetch,
  // no TOCTOU window between choosing the block and reading its edges.
  const byId=new Map<string,IntelligentBlock>();
  for(const b of blocks){
    const id=String(b.intelligent_block_id??"");
    if(id&&!byId.has(id)) byId.set(id,b);
  }

  const primary=eligible[0].block;
  // now is injected (default: wall clock) so temporal gates stay
  // recomputable: delayed-inspect replays the same now and must agree.
  const nowMs=now.getTime();
  const chased=chaseSupersession(req,primary,byId,nowMs);
  const selected=chased.block;
  const related=relatedContext(req,selected,byId,nowMs);
  const reason=chased.followed.length>0
    ? `SUPERSEDES_EDGE_FOLLOWED:${chased.followed.join(">")}`
    : "OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY";

  return {
    schema:"naya.know.context-result.v1",status:"HIT",task_id:req.task_id,required_capability:req.required_capability,
    selected_block_id:String(selected.intelligent_block_id),selected_epistemic_state:String(selected.understanding_state??"UNKNOWN"),
    selected_provenance:selected.provenance??null,selected_evidence_refs:Array.isArray(selected.evidence_refs)?selected.evidence_refs:[],
    applicable:true,reason,retrieval_creates_authority:false,handoff_to:"NAYA-KERNEL-PROVE",
    related_context:related.entries,conflict_detected:related.conflict
  };
}
