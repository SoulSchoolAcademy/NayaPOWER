export type ProveKnowReceipt = {
  id?: string;
  user_id?: string;
  project_id?: string;
  action?: string;
  status?: string;
  observed_result?: string | null;
  created_at?: string | null;
  evidence?: any;
};

export type ProveBlock = {
  intelligent_block_id?: string | null;
  owner_id?: string | null;
  status?: string | null;
  understanding_state?: string | null;
  applicable_scope?: any;
  content?: any;
  provenance?: any;
  evidence_refs?: any[];
  superseded_by_block_id?: string | null;
};

export type ProveGrant = {
  grant_id?: string | null;
  issuer_id?: string | null;
  subject_id?: string | null;
  scope?: any;
  actions?: any[];
  status?: string | null;
  revoked_at?: string | null;
  expires_at?: string | null;
};

export type ProveRelationship = {
  relationship_id?: string | null;
  source_id?: string | null;
  target_id?: string | null;
  relationship_type?: string | null;
  epistemic_state?: string | null;
  provenance?: any;
};

export type ProveAssessment = {
  schema: "naya.prove.assessment.v1";
  node_id: "NAYA-KERNEL-PROVE";
  state: "ASSESSED" | "CONFLICTED" | "FAILED";
  claim: string;
  epistemic_state: "SUPPORTED" | "UNVERIFIED" | "CONTRADICTED";
  claim_strength: "WEAK" | "MODERATE";
  evidence_strength: "WEAK" | "STRONG";
  evidence: Array<{evidence_id:string; source:string; strength:"STRONG"}>;
  provenance_chain: Array<{source:string; value:any}>;
  verification_method: string;
  limitations: string[];
  conflicts: Array<{
    relationship_id:string;
    relationship_type:string;
    epistemic_state:string;
    provenance:any;
  }>;
  selected_block_id: string | null;
  know_receipt_id: string | null;
  proof_creates_authority: false;
  handoff_to: "NAYA-KERNEL-CONNECT" | null;
  failure_reason: string | null;
};

const CURRENT_BLOCK_STATES=new Set(["VERIFIED","DISTILLED","APPLIED","LEARNED"]);
const CURRENT_BLOCK_STATUS=new Set(["ACTIVE","DURABLE","RELEASED"]);
const CONFLICT_TYPES=new Set(["CONTRADICTS","INVALIDATES"]);

const parsedTime=(value:unknown):number|null=>{
  if(value===null||value===undefined||value==="") return null;
  const t=Date.parse(String(value));
  return Number.isFinite(t)?t:NaN;
};

const nonEmptyObject=(value:any)=>Boolean(value && typeof value==="object" && !Array.isArray(value) && Object.keys(value).length>0);

const structuredCapabilities=(block:ProveBlock):string[]=>{
  const scope=block.applicable_scope;
  const direct=Array.isArray(scope?.capabilities)?scope.capabilities.map(String):[];
  const contentCaps=Array.isArray(block.content?.capabilities)?block.content.capabilities.map(String):[];
  return Array.from(new Set([...direct,...contentCaps]));
};

const boundedLegacyCapabilities=(block:ProveBlock):string[]=>{
  const lesson=String(block.content?.lesson??"");
  const caps:string[]=[];
  if(/preserve provenance|provenance before applying retained intelligence/i.test(lesson)) caps.push("provenance_preservation");
  return caps;
};

const deriveCapabilities=(block:ProveBlock):string[]=>{
  const structured=structuredCapabilities(block);
  return structured.length?structured:boundedLegacyCapabilities(block);
};

const stableJson=(value:any):string=>{
  if(Array.isArray(value)) return "["+value.map(stableJson).join(",")+"]";
  if(value && typeof value==="object"){
    return "{"+Object.keys(value).sort().map(k=>JSON.stringify(k)+":"+stableJson(value[k])).join(",")+"}";
  }
  return JSON.stringify(value);
};

function blocked(
  receipt:ProveKnowReceipt|null,
  reason:string,
  blockId:string|null=null,
  conflicts:ProveAssessment["conflicts"]=[]
):ProveAssessment{
  return {
    schema:"naya.prove.assessment.v1",
    node_id:"NAYA-KERNEL-PROVE",
    state:conflicts.length?"CONFLICTED":"FAILED",
    claim:blockId ? "Evidence-backed applicability of "+blockId : "No evidence-backed claim may be promoted",
    epistemic_state:"UNVERIFIED",
    claim_strength:"WEAK",
    evidence_strength:"WEAK",
    evidence:[],
    provenance_chain:[],
    verification_method:"PERSISTED_KNOW_RECEIPT_PLUS_CANONICAL_BLOCK_REREAD",
    limitations:[
      "This assessment does not prove behavioral outcome or causality; VERIFY remains a separate Node responsibility.",
      "Production proof requires exact deployed/source evidence and independent outcome verification."
    ],
    conflicts,
    selected_block_id:blockId,
    know_receipt_id:receipt?.id?String(receipt.id):null,
    proof_creates_authority:false,
    handoff_to:null,
    failure_reason:reason
  };
}

export function assessKnowProof(
  ownerId:string,
  nayaId:string,
  receipt:ProveKnowReceipt|null,
  block:ProveBlock|null,
  grant:ProveGrant|null,
  relationships:ProveRelationship[],
  now=new Date(),
  maxKnowAgeSeconds=900
):ProveAssessment{
  if(!receipt) return blocked(null,"KNOW_RECEIPT_REQUIRED");
  if(receipt.user_id!==ownerId || receipt.project_id!=="NayaNET") return blocked(receipt,"KNOW_RECEIPT_SCOPE_MISMATCH");
  if(receipt.action!=="know_context_retrieval" || receipt.status!=="SUCCESS") return blocked(receipt,"KNOW_RECEIPT_INVALID");

  const receiptTime=parsedTime(receipt.created_at);
  if(receiptTime===null || Number.isNaN(receiptTime) || receiptTime>now.getTime()) return blocked(receipt,"KNOW_RECEIPT_TIME_INVALID");
  if((now.getTime()-receiptTime)/1000>maxKnowAgeSeconds) return blocked(receipt,"KNOW_RECEIPT_STALE");

  const ev=receipt.evidence??{};
  const request=ev.request??{};
  const result=ev.result??{};
  if(ev.schema!=="naya.know.receipt.v1" || ev.node_id!=="NAYA-KERNEL-KNOW") return blocked(receipt,"KNOW_EVIDENCE_ENVELOPE_INVALID");
  if(request.owner_id!==ownerId || request.naya_id!==nayaId) return blocked(receipt,"KNOW_REQUEST_IDENTITY_MISMATCH");
  if(ev.handoff_to!=="NAYA-KERNEL-PROVE") return blocked(receipt,"KNOW_HANDOFF_MISMATCH");
  if(ev.retrieval_creates_authority!==false || result.retrieval_creates_authority!==false) return blocked(receipt,"RETRIEVAL_AUTHORITY_CLAIM_FORBIDDEN");

  const refs=Array.isArray(ev.authority_refs)?ev.authority_refs.map(String):[];
  if(refs.length!==1 || !grant || String(grant.grant_id??"")!==refs[0]) return blocked(receipt,"LIVE_AUTHORITY_NOT_FOUND");

  const grantExpiry=parsedTime(grant.expires_at);
  if(grant.issuer_id!==ownerId || grant.subject_id!==ownerId) return blocked(receipt,"LIVE_AUTHORITY_OWNER_MISMATCH");
  if(grant.status!=="ACTIVE" || Boolean(grant.revoked_at)) return blocked(receipt,"LIVE_AUTHORITY_NOT_ACTIVE");
  if(Number.isNaN(grantExpiry)) return blocked(receipt,"LIVE_AUTHORITY_EXPIRY_INVALID");
  if(grantExpiry!==null && grantExpiry<=now.getTime()) return blocked(receipt,"LIVE_AUTHORITY_EXPIRED");
  if(!Array.isArray(grant.actions) || !grant.actions.includes("naya_node_apply")) return blocked(receipt,"LIVE_AUTHORITY_ACTION_MISMATCH");
  if(grant.scope?.target!==nayaId) return blocked(receipt,"LIVE_AUTHORITY_TARGET_MISMATCH");

  if(result.status!=="HIT" || result.applicable!==true) return blocked(receipt,"KNOW_HIT_REQUIRED");
  const selectedBlockId=String(result.selected_block_id??"").trim();
  if(!selectedBlockId) return blocked(receipt,"KNOW_SELECTED_BLOCK_REQUIRED");

  if(!block || block.intelligent_block_id!==selectedBlockId) return blocked(receipt,"CANONICAL_BLOCK_NOT_FOUND",selectedBlockId);
  if(block.owner_id!==ownerId) return blocked(receipt,"CANONICAL_BLOCK_OWNER_MISMATCH",selectedBlockId);
  if(!CURRENT_BLOCK_STATUS.has(String(block.status??"")) || !CURRENT_BLOCK_STATES.has(String(block.understanding_state??"")) || block.superseded_by_block_id){
    return blocked(receipt,"CANONICAL_BLOCK_NOT_CURRENT",selectedBlockId);
  }
  const scopeTarget=String(block.applicable_scope?.target??"");
  if(scopeTarget && scopeTarget!==nayaId) return blocked(receipt,"CANONICAL_BLOCK_SCOPE_MISMATCH",selectedBlockId);
  const requiredCapability=String(request.required_capability??"").trim();
  if(!requiredCapability || !deriveCapabilities(block).includes(requiredCapability)) return blocked(receipt,"CANONICAL_BLOCK_CAPABILITY_MISMATCH",selectedBlockId);
  if(!nonEmptyObject(block.provenance)) return blocked(receipt,"PROVENANCE_REQUIRED",selectedBlockId);
  if(!Array.isArray(block.evidence_refs) || block.evidence_refs.length===0) return blocked(receipt,"EVIDENCE_REQUIRED",selectedBlockId);

  if(String(result.selected_epistemic_state??"")!==String(block.understanding_state??"")) return blocked(receipt,"EPISTEMIC_STATE_MISMATCH",selectedBlockId);
  if(stableJson(result.selected_provenance??null)!==stableJson(block.provenance??null)) return blocked(receipt,"PROVENANCE_MISMATCH",selectedBlockId);
  if(stableJson(result.selected_evidence_refs??[])!==stableJson(block.evidence_refs??[])) return blocked(receipt,"EVIDENCE_REFERENCE_MISMATCH",selectedBlockId);

  const conflicts=(relationships??[])
    .filter(r=>CONFLICT_TYPES.has(String(r.relationship_type??"")) &&
      (r.source_id===selectedBlockId || r.target_id===selectedBlockId) &&
      ["SUPPORTED","VERIFIED"].includes(String(r.epistemic_state??"")) &&
      nonEmptyObject(r.provenance))
    .map(r=>({
      relationship_id:String(r.relationship_id??""),
      relationship_type:String(r.relationship_type??""),
      epistemic_state:String(r.epistemic_state??""),
      provenance:r.provenance
    }));

  const verifiedConflict=conflicts.some(c=>c.epistemic_state==="VERIFIED");
  const unresolvedConflict=conflicts.length>0;
  const taskId=String(request.task_id??"").trim();
  const capability=String(request.required_capability??"").trim();
  const claim="Canonical Intelligent Block "+selectedBlockId+" is evidence-backed and applicable to task "+taskId+" for capability "+capability+".";

  const evidence=(block.evidence_refs??[]).map((ref:any,index:number)=>({
    evidence_id:String(ref?.id??ref?.evidence_id??ref?.receipt??(typeof ref==="string"?ref:("evidence-"+String(index+1)))),
    source:String(ref?.source??ref?.type??"canonical_intelligent_block"),
    strength:"STRONG" as const
  }));
  const provenance_chain=[
    {source:"know_receipt",value:String(receipt.id??"")},
    {source:"intelligent_block",value:selectedBlockId},
    {source:"block_provenance",value:block.provenance}
  ];

  if(verifiedConflict){
    return {
      schema:"naya.prove.assessment.v1",node_id:"NAYA-KERNEL-PROVE",state:"CONFLICTED",
      claim,epistemic_state:"CONTRADICTED",claim_strength:"MODERATE",evidence_strength:"STRONG",
      evidence,provenance_chain,verification_method:"PERSISTED_KNOW_RECEIPT_PLUS_CANONICAL_BLOCK_REREAD",
      limitations:["A verified contradiction exists; the claim must not be promoted or silently resolved.","This does not prove behavioral outcome or causality."],
      conflicts,selected_block_id:selectedBlockId,know_receipt_id:String(receipt.id??""),
      proof_creates_authority:false,handoff_to:null,failure_reason:"VERIFIED_CONTRADICTION_PRESENT"
    };
  }

  if(unresolvedConflict){
    return {
      schema:"naya.prove.assessment.v1",node_id:"NAYA-KERNEL-PROVE",state:"CONFLICTED",
      claim,epistemic_state:"UNVERIFIED",claim_strength:"MODERATE",evidence_strength:"STRONG",
      evidence,provenance_chain,verification_method:"PERSISTED_KNOW_RECEIPT_PLUS_CANONICAL_BLOCK_REREAD",
      limitations:["A supported contradiction/conflict remains unresolved; claim strength cannot be promoted.","This does not prove behavioral outcome or causality."],
      conflicts,selected_block_id:selectedBlockId,know_receipt_id:String(receipt.id??""),
      proof_creates_authority:false,handoff_to:null,failure_reason:"UNRESOLVED_CONFLICT_PRESENT"
    };
  }

  return {
    schema:"naya.prove.assessment.v1",node_id:"NAYA-KERNEL-PROVE",state:"ASSESSED",
    claim,epistemic_state:"SUPPORTED",claim_strength:"MODERATE",evidence_strength:"STRONG",
    evidence,provenance_chain,
    verification_method:"PERSISTED_KNOW_RECEIPT_PLUS_CANONICAL_BLOCK_REREAD",
    limitations:[
      "SUPPORTED is context-bound to the recorded KNOW task/capability and canonical block state.",
      "This assessment does not prove behavioral outcome or causality; VERIFY remains a separate Node responsibility.",
      "Production-proven status requires exact deployed/source evidence and independent outcome verification."
    ],
    conflicts:[],selected_block_id:selectedBlockId,know_receipt_id:String(receipt.id??""),
    proof_creates_authority:false,handoff_to:"NAYA-KERNEL-CONNECT",failure_reason:null
  };
}
