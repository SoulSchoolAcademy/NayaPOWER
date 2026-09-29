export type KnowRequest = {
  owner_id: string;
  naya_id: string;
  target: string;
  task_context: string;
  law_receipt_id?: string;
  intelligent_block_id?: string;
  block_id?: string;
  lesson?: string;
  answer?: string;
  intelligence?: unknown;
  intelligence_content?: unknown;
};

export type KnowCandidate = {
  block_id?: string;
  intelligent_block_id: string;
  owner_id: string;
  subject_id?: string;
  title?: string;
  status?: string;
  understanding_state?: string;
  owner_scope?: string;
  evidence_refs?: unknown[];
  provenance?: Record<string, unknown>;
  applicable_scope?: Record<string, unknown>;
  content?: Record<string, unknown>;
  superseded_by_block_id?: string | null;
};

export type KnowDecision =
  | {status:"SELECTED"; reason:"CONTEXTUAL_APPLICABILITY_MATCH"; selected:KnowCandidate; score:number; matched_terms:string[]}
  | {status:"MISS"; reason:"NO_APPLICABLE_CANONICAL_INTELLIGENCE"; selected:null; score:0; matched_terms:string[]}
  | {status:"BLOCKED"; reason:string; selected:null; score:0; matched_terms:string[]};

const STOP=new Set([
  "a","an","and","are","as","at","be","before","by","for","from","in","into","is","it","of","on","or","the","this","to","with",
  "apply","applying","action","task","retained","intelligence"
]);

export type KnowLawReceipt = {id?:string; user_id?:string; action?:string; status?:string; evidence?:any};
export type KnowGrant = {grant_id:string; issuer_id:string; subject_id:string; scope?:Record<string,unknown>; actions?:string[]; status?:string|null; revoked_at?:string|null; expires_at?:string|null};

export function validateKnowAuthorization(req:KnowRequest, law:KnowLawReceipt|null, grant:KnowGrant|null, now=new Date()){
  if(!law) return {status:"BLOCKED",reason:"LAW_RECEIPT_REQUIRED"};
  const decision=law.evidence?.law_decision??{};
  const lawReq=law.evidence?.law_request??{};
  if(law.user_id!==req.owner_id) return {status:"BLOCKED",reason:"LAW_RECEIPT_OWNER_MISMATCH"};
  if(law.action!=="law_authority_decision"||law.status!=="SUCCESS"||law.evidence?.node_id!=="NAYA-KERNEL-LAW") return {status:"BLOCKED",reason:"LAW_RECEIPT_INVALID"};
  if(decision.status!=="AUTHORIZED") return {status:"BLOCKED",reason:"LAW_NOT_AUTHORIZED"};
  if(decision.owner_id!==req.owner_id||decision.naya_id!==req.naya_id) return {status:"BLOCKED",reason:"LAW_IDENTITY_MISMATCH"};
  if(lawReq.target!==req.target||decision.target!==req.target) return {status:"BLOCKED",reason:"AUTHORIZED_TARGET_MISMATCH"};
  const refs=Array.isArray(decision.authority_refs)?decision.authority_refs:[];
  if(refs.length!==1) return {status:"BLOCKED",reason:"LAW_AUTHORITY_REFERENCE_INVALID"};
  const grantId=String(refs[0]);
  if(!grant||grant.grant_id!==grantId) return {status:"BLOCKED",reason:"LIVE_AUTHORITY_NOT_FOUND"};
  if(grant.issuer_id!==req.owner_id||grant.subject_id!==req.owner_id) return {status:"BLOCKED",reason:"LIVE_AUTHORITY_OWNER_MISMATCH"};
  if(grant.status!=="ACTIVE"||grant.revoked_at) return {status:"BLOCKED",reason:"LIVE_AUTHORITY_NOT_ACTIVE"};
  if(grant.expires_at&&new Date(grant.expires_at).getTime()<=now.getTime()) return {status:"BLOCKED",reason:"LIVE_AUTHORITY_EXPIRED"};
  const action=String(decision.action??lawReq.action??"");
  if(!action||!Array.isArray(grant.actions)||!grant.actions.includes(action)) return {status:"BLOCKED",reason:"LIVE_AUTHORITY_ACTION_MISMATCH"};
  if((grant.scope as any)?.target!==req.target) return {status:"BLOCKED",reason:"LIVE_AUTHORITY_TARGET_MISMATCH"};
  return {status:"READY",reason:"LAW_AND_LIVE_AUTHORITY_MATCH",law_receipt_id:String(law.id??req.law_receipt_id??""),authority_grant_id:grantId,authorized_action:action};
}

function tokens(value:unknown):string[]{
  const text=typeof value==="string"?value:JSON.stringify(value??"");
  return [...new Set((text.toLowerCase().match(/[a-z0-9_]+/g)??[]).filter(x=>x.length>2&&!STOP.has(x)))];
}

function hasProvenance(candidate:KnowCandidate){
  return Boolean(candidate.provenance && Object.keys(candidate.provenance).length>0 && Array.isArray(candidate.evidence_refs) && candidate.evidence_refs.length>0);
}

function isEligible(req:KnowRequest,c:KnowCandidate){
  if(c.owner_id!==req.owner_id) return false;
  if(!["ACTIVE","DURABLE"].includes(String(c.status??""))) return false;
  if(!["VERIFIED","DISTILLED","APPLIED","LEARNED"].includes(String(c.understanding_state??""))) return false;
  if(c.superseded_by_block_id) return false;
  if(!hasProvenance(c)) return false;
  const scope=c.applicable_scope??{};
  const scopeTarget=String((scope as any).target??"");
  if(scopeTarget && scopeTarget!==req.target && scopeTarget!==req.naya_id) return false;
  return true;
}

export function selectKnow(req:KnowRequest,candidates:KnowCandidate[]):KnowDecision{
  if(!req.owner_id||!req.naya_id||!req.target||!req.task_context?.trim()){
    return {status:"BLOCKED",reason:"KNOW_CONTEXT_REQUIRED",selected:null,score:0,matched_terms:[]};
  }
  if(req.intelligent_block_id||req.block_id||req.lesson||req.answer||req.intelligence!==undefined||req.intelligence_content!==undefined){
    return {status:"BLOCKED",reason:"CALLER_SUPPLIED_INTELLIGENCE_FORBIDDEN",selected:null,score:0,matched_terms:[]};
  }

  const q=tokens(req.task_context);
  const ranked=candidates
    .filter(c=>isEligible(req,c))
    .map(c=>{
      const hay=tokens([
        c.title??"",
        c.subject_id??"",
        JSON.stringify(c.content??{}),
        JSON.stringify(c.applicable_scope??{})
      ].join(" "));
      const matches=q.filter(t=>hay.includes(t));
      const score=matches.length;
      return {c,score,matches};
    })
    .filter(x=>x.score>=2)
    .sort((a,b)=>b.score-a.score || a.c.intelligent_block_id.localeCompare(b.c.intelligent_block_id));

  if(!ranked.length) return {status:"MISS",reason:"NO_APPLICABLE_CANONICAL_INTELLIGENCE",selected:null,score:0,matched_terms:[]};
  if(ranked.length>1 && ranked[0].score===ranked[1].score){
    return {status:"BLOCKED",reason:"AMBIGUOUS_CONTEXTUAL_INTELLIGENCE",selected:null,score:0,matched_terms:[]};
  }
  return {status:"SELECTED",reason:"CONTEXTUAL_APPLICABILITY_MATCH",selected:ranked[0].c,score:ranked[0].score,matched_terms:ranked[0].matches};
}
