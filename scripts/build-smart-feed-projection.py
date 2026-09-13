#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'SMART FEED CONTENT'
OUT=ROOT/'NAYANET/HUB/public/intelligence/pis-feed.json'
NOTE_RE=re.compile(r'(?:^|\n)🧠\s*NAYA POWER\s*[—-]\s*SMART NOTE\s+(\d+)\s*\n')
SEC_RE=re.compile(r'(?:^|\n)\s*(?:#+\s*)?(\d+)\.\s+([^\n]+)\s*\n',re.M)
SUB_RE=re.compile(r'(?:\*\*\s*)?Subject ID:\s*([^\n]+)',re.I)
def clean(s):
 s=re.sub(r'\*\*([^*]+)\*\*',r'\1',s);s=re.sub(r'`([^`]+)`',r'\1',s);return re.sub(r'\n{3,}','\n\n',s).strip()
def para(s):
 for p in re.split(r'\n\s*\n',clean(s)):
  p=p.strip()
  if p and not re.match(r'^(?:\d+\.|#+)',p): return p[:1800]
 return clean(s)[:1800]
def sections(s):
 m=list(SEC_RE.finditer(s));return {int(x.group(1)):clean(s[x.end():m[i+1].start() if i+1<len(m) else len(s)]) for i,x in enumerate(m)}
def when():
 try:
  x=subprocess.check_output(['git','log','-1','--format=%cI','--','SMART FEED CONTENT'],cwd=ROOT,text=True).strip()
  if x:return x
 except Exception:pass
 return datetime.now(timezone.utc).isoformat()
def main():
 text=SRC.read_text(encoding='utf-8'); matches=list(NOTE_RE.finditer(text)); ts=when(); events=[]
 for i,m in enumerate(matches):
  body=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip(); sec=sections(body); sub=SUB_RE.search(body); eid=sub.group(1).strip() if sub else f'NAYA-POWER-{int(m.group(1)):02d}'
  title=body.splitlines()[0].strip(); title=re.sub(r'^What (?:Is|Are)\s+','',title)
  nutshell=para(sec.get(1,'')) or title; human=para(sec.get(2,'')); child=para(sec.get(3,'')); grandma=para(sec.get(4,'')); naya=para(sec.get(5,'')); machine=para(sec.get(6,'')); lesson=para(sec.get(7,'')); meaning=para(sec.get(8,'')); links=para(sec.get(9,'')); action=para(sec.get(10,'')); value=para(sec.get(11,''))
  events.append({'event_id':eid,'user_id':'canonical','created_at':ts,'updated_at':ts,'source':{'type':'smart_note','label':title},'human_input':{'raw':human or nutshell,'captured_at':ts},'context':{'topic':title,'tags':['Smart Note','Naya Power','Intelligent Feed'],'canonical_path':f'SMART FEED CONTENT#NAYA-POWER-{int(m.group(1)):02d}'},'naya_interpretation':{'observation':nutshell,'interpretation':naya,'recommendation':action,'uncertainty':'Source uncertainty is preserved; projection does not invent certainty.'},'machine_evidence':{'items':['Canonical source: SMART FEED CONTENT','PIS projection generated from canonical Smart Feed content.'],'verification_state':'source-projection-generated'},'weaver_synthesis':{'summary':nutshell,'relationships':[]},'lesson':{'text':lesson,'retained':True},'meaning':{'text':meaning,'significance':'Canonical Smart Note meaning'},'action':{'text':action,'status':'from-source'},'whats_in_it_for_you':value,'relationships':{'event_ids':[],'connection_ids':[],'space_ids':[]},'privacy':{'visibility':'source-defined','consent_state':'source-defined'},'trust':{'level':'source-projection','evidence_ids':[]},'status':'active','perspectives':[{'label':'HUMAN','body':human or nutshell,'tone':'human'},{'label':'CHILD','body':child,'tone':'child'},{'label':'GRANDMA','body':grandma,'tone':'grandma'},{'label':'NAYA','body':naya,'tone':'naya'},{'label':'MACHINE','body':machine,'tone':'machine'},{'label':'WEAVER','body':links,'tone':'weaver'}],'pis':{'source_ref':f'SMART FEED CONTENT#NAYA-POWER-{int(m.group(1)):02d}','projection_version':'2.0','timestamp_precision':'source-commit'}})
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({'schema_version':'PIS-2.0','generated_at':datetime.now(timezone.utc).isoformat(),'source':'SMART FEED CONTENT','event_count':len(events),'events':events},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'PIS_FEED_BUILT events={len(events)} source=SMART FEED CONTENT')
if __name__=='__main__':main()
