export type KnowRequest = {
  owner_id: string;
  naya_id: string;
  target: string;
  task_context: string;
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
      const hay=tokens([c.title,c.subject_id,c.content,c.applicable_scope].filter(Boolean).join(" "));
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
