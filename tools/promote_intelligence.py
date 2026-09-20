#!/usr/bin/env python3
"""Deterministic NayaPOWER Intelligence Event promotion engine."""
from __future__ import annotations
import hashlib,json,re
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]; EVENT_DIR=ROOT/"MASTER-NOTES/INTELLIGENCE-EVENTS"; RECEIPT_DIR=ROOT/"MASTER-NOTES/INTELLIGENCE-PROMOTIONS"; NAYA_DIR=ROOT/"MASTER-NOTES/NAYA-NOTES"; SHAWN_DIR=ROOT/"MASTER-NOTES/SHAWN-NOTES"; FEED_DIR=ROOT/"MASTER-NOTES/INTELLIGENCE-FEED"; HUB_PATH=ROOT/"MASTER-NOTES/PRIMARY-INTELLIGENCE-HUB.md"
REQUIRED={"event_id","timestamp","project","lesson","source","evidence_state","promotion_status"}; EVIDENCE_STATES={"UNKNOWN","IMPLEMENTED","TESTED","VERIFIED","RUNTIME-PROVEN","PRODUCTION-PROVEN"}; PROMOTION_STATES={"NOT_REQUIRED","PROPOSED","WRITTEN","TESTED","VERIFIED","CANONICAL","BLOCKED","FAILED","UNKNOWN"}; HOMES={"LAW","GUARDRAIL","MACHINE_CONTRACT","TEST","PROCEDURE","MISSION_STATE","ARCHITECTURE","SPECIFICATION","NAYA_NOTE","HUMAN_SMART_NOTE"}; AUTO_HOMES={"NAYA_NOTE","HUMAN_SMART_NOTE","PROCEDURE","ARCHITECTURE","SPECIFICATION"}; AUTHORITY_HOMES={"LAW","GUARDRAIL","MACHINE_CONTRACT","TEST","MISSION_STATE"}; STOPWORDS={"the","and","that","this","with","from","into","must","should","when","then","than","for","are","was","were","not","only","every","next","naya","system"}
def normalize(text:str)->str:return " ".join(t for t in re.findall(r"[a-z0-9]+",text.lower()) if t not in STOPWORDS and len(t)>2)
def fingerprint(e:dict[str,Any])->str:return hashlib.sha256("|".join(normalize(str(e.get(k,""))) for k in ("project","lesson","root_cause","recommendation")).encode()).hexdigest()[:16]
def similarity(a:str,b:str)->float:
 sa,sb=set(a.split()),set(b.split());return len(sa&sb)/len(sa|sb) if sa and sb else 0.0
def display_path(p:Path)->str:
 try:return str(p.relative_to(ROOT))
 except ValueError:return str(p)
def load_events():
 out=[]
 for p in sorted(EVENT_DIR.glob("*.json")):
  try:out.append((p,json.loads(p.read_text(encoding="utf-8"))))
  except json.JSONDecodeError as exc:raise ValueError(f"{p}: invalid JSON: {exc}") from exc
 return out
def validate_event(e:dict[str,Any],p:Path):
 err=[];missing=sorted(REQUIRED-set(e))
 if missing:return [f"{p}: missing required fields: {', '.join(missing)}"]
 if len(str(e["event_id"]))<8:err.append(f"{p}: event_id must be at least 8 characters")
 if not str(e["project"]).strip() or not str(e["lesson"]).strip():err.append(f"{p}: project and lesson must be non-empty")
 if not isinstance(e["source"],list):err.append(f"{p}: source must be an array")
 if e["evidence_state"] not in EVIDENCE_STATES:err.append(f"{p}: invalid evidence_state={e['evidence_state']}")
 if e["promotion_status"] not in PROMOTION_STATES:err.append(f"{p}: invalid promotion_status={e['promotion_status']}")
 for h in e.get("candidate_homes",[]):
  if h not in HOMES:err.append(f"{p}: invalid candidate home={h}")
 try:datetime.fromisoformat(str(e["timestamp"]).replace("Z","+00:00"))
 except ValueError:err.append(f"{p}: timestamp is not ISO-8601 date-time")
 return err
def classify(e):
 homes=[x for x in e.get("candidate_homes",[]) if x in HOMES]
 if homes:homes=list(dict.fromkeys(homes))
 else:
  text=" ".join(str(e.get(k,"")) for k in ("lesson","what_happened","root_cause","recommendation")).lower();homes=[]
  if any(x in text for x in ("law","constitutional","governance","universal")):homes.append("LAW")
  if any(x in text for x in ("repeat","regression","prevent","guardrail")):homes.append("GUARDRAIL")
  if any(x in text for x in ("test","assert","machine contract","automate")):homes.append("TEST")
  if not homes:homes=["NAYA_NOTE"]
 return homes,"PROMOTION_PROPOSAL_REQUIRES_AUTHORITY" if any(h in AUTHORITY_HOMES for h in homes) else "AUTO_PROMOTE_APPROVED_DESTINATIONS"
def write_note(e,target,heading):
 target.mkdir(parents=True,exist_ok=True);p=target/f"{e['event_id']}.md";text=f"# 🔱 {heading}\n\n**Event:** {e['event_id']}\n**Timestamp:** {e['timestamp']}\n**Project:** {e['project']}\n**Promotion fingerprint:** `{fingerprint(e)}`\n\n## WHAT HAPPENED\n{e.get('what_happened','')}\n\n## WHAT WE LEARNED\n{e['lesson']}\n\n## VALUE\n{e.get('value','')}\n\n## WHAT CHANGED\n{e.get('actual_outcome','')}\n\n## EVIDENCE STATE\n`{e['evidence_state']}`\n\n## EVIDENCE\n"+"\n".join(f"- `{x}`" for x in e.get("evidence",[]))+f"\n\n## NEXT ACTION\n{e.get('next_action','')}\n\n## SUCCESSOR / HUMAN GUIDANCE\n{e.get('successor_instruction','')}\n\n## PROVENANCE\nSource event: `{e['event_id']}`\nSource: {', '.join(e.get('source',[]))}\n"
 if not p.exists() or p.read_text(encoding="utf-8")!=text:p.write_text(text,encoding="utf-8")
 return display_path(p)
def load_prior_event_index(events):return {"by_id":{e["event_id"]:e for _,e in events},"normalized":{e["event_id"]:normalize(str(e.get("lesson",""))) for _,e in events}}
def find_duplicate(e,index):
 fp=fingerprint(e)
 for eid,p in index["by_id"].items():
  if eid!=e["event_id"] and fingerprint(p)==fp:return eid,1.0
 cur=normalize(str(e.get("lesson","")));best=None;score=0.0
 for eid,lesson in index["normalized"].items():
  if eid==e["event_id"]:continue
  s=similarity(cur,lesson)
  if s>score:best,score=eid,s
 return (best,score) if score>=0.82 else (None,score)
def write_feed(e,homes,decision,duplicate,status):
 FEED_DIR.mkdir(parents=True,exist_ok=True);p=FEED_DIR/f"{e['event_id']}.md";dup=f"`{duplicate}`" if duplicate else "None";text=f"# 🔱 Intelligence Feed — {e.get('title',e['event_id'])}\n\n**Event:** `{e['event_id']}`  \n**Timestamp:** {e['timestamp']}  \n**Project:** {e['project']}  \n**Promotion:** `{status}`  \n**Decision:** `{decision}`  \n**Durable homes:** {', '.join(f'`{h}`' for h in homes)}  \n**Duplicate / related prior event:** {dup}\n\n## LESSON\n{e['lesson']}\n\n## VALUE / IMPACT\n{e.get('value','')}\n\n## SOURCE\n"+"\n".join(f"- `{x}`" for x in e.get("source",[]))+f"\n\n## EVIDENCE STATE\n`{e['evidence_state']}`\n\n## SUCCESSOR INSTRUCTION\n{e.get('successor_instruction','')}\n\n## PROMOTION\nThis entry is append-oriented intelligence. It does not override canonical governance or verified project truth.\n"
 if not p.exists() or p.read_text(encoding="utf-8")!=text:p.write_text(text,encoding="utf-8")
 return display_path(p)
def update_hub(summary):
 if not HUB_PATH.exists():return
 a,b="<!-- PROMOTION-ENGINE-V1:START -->","<!-- PROMOTION-ENGINE-V1:END -->";existing=HUB_PATH.read_text(encoding="utf-8");block=[a,"","## 🔱 PROMOTION ENGINE V1 — CURRENT OPERATIONAL STATE","","Generated from canonical Intelligence Events; this section does not replace canonical synthesis.",""]
 for item in summary[-10:]:block.append(f"- `{item['event_id']}` — **{item['promotion_status']}** — homes: {', '.join(item['candidate_homes'])}; duplicate: {item['duplicate_of'] or 'none'}; evidence: `{item['evidence_state']}`")
 block += ["","**Current invariant:** `EVENT → DEDUP → CLASSIFY → PROMOTE → VERIFY → HUB → SUCCESSOR`","",b];new="\n".join(block);updated=existing.split(a,1)[0]+new+existing.split(b,1)[1] if a in existing and b in existing else existing.rstrip()+"\n\n"+new+"\n"
 if updated!=existing:HUB_PATH.write_text(updated,encoding="utf-8")
def main():
 events=load_events();errors=[]
 for p,e in events:errors+=validate_event(e,p)
 if errors:print("\n".join(errors));return 1
 index=load_prior_event_index(events);receipts=[]
 for p,e in events:
  homes,decision=classify(e);duplicate,sim=find_duplicate(e,index);promoted=list(e.get("promoted_artifacts",[]));auto=[h for h in homes if h in AUTO_HOMES];restricted=[h for h in homes if h in AUTHORITY_HOMES]
  if "NAYA_NOTE" in auto:promoted.append(write_note(e,NAYA_DIR,"NAYA NOTE / AI INTELLIGENCE"))
  if "HUMAN_SMART_NOTE" in auto:promoted.append(write_note(e,SHAWN_DIR,"SHAWN NOTE / HUMAN RECEIPT"))
  status="DUPLICATE_REVIEW" if duplicate else "PROMOTION_PROPOSAL_REQUIRES_AUTHORITY" if restricted else "PROMOTED_WRITTEN" if auto else "CLASSIFIED_ONLY";promoted.append(write_feed(e,homes,decision,duplicate,status));receipts.append({"event_id":e["event_id"],"source_event":display_path(p),"fingerprint":fingerprint(e),"candidate_homes":homes,"auto_promotable_homes":auto,"authority_gated_homes":restricted,"decision":decision,"duplicate_of":duplicate,"duplicate_similarity":round(sim,4),"evidence_state":e["evidence_state"],"source_promotion_status":e["promotion_status"],"promotion_status":status,"promoted_artifacts":list(dict.fromkeys(promoted)),"verification_required":bool(auto or restricted),"verified":False,"rule":"NO_FILE_WRITE_ALONE_COUNTS_AS_VERIFICATION"})
 RECEIPT_DIR.mkdir(parents=True,exist_ok=True);receipt={"engine":"Promotion Engine v1","generated_at":datetime.now(timezone.utc).isoformat(),"event_count":len(receipts),"receipts":receipts,"verification_summary":{"implemented":True,"tested":False,"verified":False,"runtime_proven":False,"production_proven":False,"note":"CI verification must close these states."}};(RECEIPT_DIR/"LATEST-PROMOTION-RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8");update_hub(receipts);print(f"Promotion Engine v1 processed {len(receipts)} event(s); receipt and feed/hub state written.");return 0
if __name__=="__main__":raise SystemExit(main())
