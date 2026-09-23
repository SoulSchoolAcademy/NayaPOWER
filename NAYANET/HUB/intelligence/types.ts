export type Lens='personal'|'collective'|'activity';
export type Perspective={label:string;body:string;tone:'human'|'child'|'grandma'|'naya'|'machine'|'wisdom'|'weaver'};

export type IntelligentBlockProjection={
  identity?:{object_id?:string;event_id?:string;version?:number;namespace?:string;schema_version?:string};
  type?:{object_type?:string;event_type?:string;classification?:string};
  meaning?:Record<string,unknown>;
  actors?:Record<string,unknown>;
  context?:Record<string,unknown>;
  time?:Record<string,unknown>;
  intent?:Record<string,unknown>;
  provenance?:Record<string,unknown>;
  evidence?:Record<string,unknown>;
  truth?:{state?:string;confidence?:number;conflicts?:string[]};
  authority?:{state?:string;authority_ref?:string;policy_ref?:string;consent_ref?:string;constraints?:string[]};
  relationships?:Record<string,unknown>[];
  value?:{state?:string;benefit?:number;harm?:number;cost?:number;risk?:number;effort?:number;relevance?:number;responsible_value?:number};
  action?:Record<string,unknown>;
  outcome?:Record<string,unknown>;
  learning?:Record<string,unknown>;
  successor?:Record<string,unknown>;
  lifecycle?:{stage?:string;captured_at?:string;verified_at?:string;updated_at?:string};
  integrity?:{algorithm?:string;content_hash?:string};
  projections?:Record<string,unknown>;
  metadata?:Record<string,unknown>;
  [key:string]:unknown;
};

export type IntelligentEvent={
  event_id:string;user_id:string;created_at:string;updated_at:string;
  source:{type:string;label:string};
  human_input:{raw:string;captured_at:string};
  context:{topic?:string;tags?:string[];canonical_path?:string;scope?:string;environment?:string};
  naya_interpretation:{observation?:string;interpretation?:string;recommendation?:string;uncertainty?:string};
  machine_evidence:{items:string[];verification_state:string};
  weaver_synthesis:{summary?:string;relationships?:string[]};
  lesson:{text?:string;retained?:boolean};
  meaning:{text?:string;significance?:string};
  action:{text?:string;status?:string};
  whats_in_it_for_you?:string;
  relationships:{event_ids:string[];connection_ids:string[];space_ids:string[]};
  privacy:{visibility:string;consent_state:string};
  trust:{level:string;evidence_ids:string[]};
  intelligent_block?:IntelligentBlockProjection;
  status:string;
  perspectives:Perspective[]
};
