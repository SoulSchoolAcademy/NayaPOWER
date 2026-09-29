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
};

const SERVABLE_STATES=new Set(["VERIFIED","DISTILLED","APPLIED","LEARNED"]);
const SERVABLE_STATUS=new Set(["ACTIVE","DURABLE","RELEASED"]);

function parsedTime(value:unknown):number|null{
  if(value===null||value===undefined||value==="") return null;
  const t=Date.parse(String(value));
  return Number.isFinite(t)?t:NaN;
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
  if(decisionExpiry===NaN||Number.isNaN(decisionExpiry)) return {ok:false,reason:"LAW_EXPIRY_INVALID"};
  if(decisionExpiry!==null&&decisionExpiry<=now.getTime()) return {ok:false,reason:"LAW_AUTHORITY_EXPIRED"};
  const refs=Array.isArray(dec.authority_refs)?dec.authority_refs:[];
  if(refs.length!==1) return {ok:false,reason:"LAW_AUTHORITY_REFERENCE_INVALID"};
  const grantId=String(refs[0]);
  if(!grant||grant.grant_id!==grantId) return {ok:false,reason:"LIVE_AUTHORITY_NOT_FOUND"};
  if(grant.issuer_id!==req.owner_id||grant.subject_id!==req.owner_id) return {ok:false,reason:"LIVE_AUTHORITY_OWNER_MISMATCH"};
  if(grant.status!=="ACTIVE"||grant.revoked_at) return {ok:false,reason:"LIVE_AUTHORITY_NOT_ACTIVE"};
  const grantExpiry=parsedTime(grant.expires_at);
  if(grantExpiry===NaN||Number.isNaN(grantExpiry)) return {ok:false,reason:"LIVE_AUTHORITY_EXPIRY_INVALID"};
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

export function selectKnowContext(req:KnowRequest,blocks:IntelligentBlock[]):KnowResult{
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

  if(eligible.length===0) return {
    schema:"naya.know.context-result.v1",status:"MISS",task_id:req.task_id,required_capability:req.required_capability,
    selected_block_id:null,selected_epistemic_state:null,selected_provenance:null,selected_evidence_refs:[],
    applicable:false,reason:"NO_ELIGIBLE_APPLICABLE_INTELLIGENCE",retrieval_creates_authority:false,handoff_to:"NAYA-KERNEL-PROVE"
  };

  const selected=eligible[0].block;
  return {
    schema:"naya.know.context-result.v1",status:"HIT",task_id:req.task_id,required_capability:req.required_capability,
    selected_block_id:String(selected.intelligent_block_id),selected_epistemic_state:String(selected.understanding_state??"UNKNOWN"),
    selected_provenance:selected.provenance??null,selected_evidence_refs:Array.isArray(selected.evidence_refs)?selected.evidence_refs:[],
    applicable:true,reason:"OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY",retrieval_creates_authority:false,handoff_to:"NAYA-KERNEL-PROVE"
  };
}
