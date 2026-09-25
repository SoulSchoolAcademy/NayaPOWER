"""Canonical IB retrieval benchmark; no persistence, no alternate authority."""
import json
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.naya/memory'))
import smart_notes_v3 as brain


def _fixture():
    root=Path(tempfile.mkdtemp(prefix='naya-canonical-ib-benchmark-'))
    base=root/'.naya/memory/smart-notes'
    for ib_id,status,date,content in [('IB-000978','CANONICAL','2026-09-25','canonical golden intelligence'),('IB-000977','SUPERSEDED','2026-09-20','historical golden intelligence')]:
        p=base/f'2026/09/25/system/golden/{ib_id}/smart-note.md'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('# SMART NOTE\n'+content+'\n',encoding='utf-8')
    registry=base/'REGISTRY.json'; registry.parent.mkdir(parents=True,exist_ok=True)
    entries=[]
    for ib_id,status,date,content,event in [('IB-000978','CANONICAL','2026-09-25','canonical golden intelligence','SE-GOLDEN-978'),('IB-000977','SUPERSEDED','2026-09-20','historical golden intelligence','SE-GOLDEN-977')]:
        entries.append({'intelligent_block_id':ib_id,'path':f'.naya/memory/smart-notes/2026/09/25/system/golden/{ib_id}/smart-note.md','date':date,'category':'system','topic':'golden','status':status,'owner':'owner','scope':'personal','project':'NayaNET','permissions':{'access':'PRIVATE','grants':['attacker','project:OtherProject']},'authority':{'state':'UNCHANGED','grant_id':None},'applicable_scope':{'privacy':'PRIVATE'},'source_event_id':event,'learning_state':{'status':'VERIFIED' if status=='CANONICAL' else 'HISTORICAL'}})
    registry.write_text(json.dumps({'$schema':'naya/smart-note-registry/v1','status':'CANONICAL','entries':entries}),encoding='utf-8')
    return root


def _count(root,principal_id,principal_project,query='canonical golden intelligence',include_historical=False):
    return brain.retrieve_canonical_ibs(query,limit=10,root=root,principal_id=principal_id,scope='personal',project='NayaNET',principal_project=principal_project,include_historical=include_historical)


def run():
    root=_fixture()
    owner=_count(root,'owner','NayaNET')
    unauthorized=_count(root,'attacker','NayaNET')
    cross=_count(root,'owner','OtherProject')
    event_forged=_count(root,'attacker','NayaNET',query='attacker')
    content_forged=_count(root,'attacker','NayaNET',query='authority project OtherProject')
    historical=_count(root,'owner','NayaNET',query='historical golden intelligence',include_historical=True)
    current=_count(root,'owner','NayaNET',query='canonical golden intelligence',include_historical=False)
    golden=owner[0] if owner else {}
    return {'benchmark':'CANONICAL_IB_RETRIEVAL_V1','status':'PASS' if len(owner)==1 and not unauthorized and not cross and not event_forged and not content_forged and golden.get('intelligent_block_id')=='IB-000978' and golden.get('source',{}).get('provenance',{}).get('source_event_id')=='SE-GOLDEN-978' and any(x.get('intelligent_block_id')=='IB-000977' for x in historical) and all(x.get('intelligent_block_id')!='IB-000977' for x in current) else 'FAIL','cases':{'authorized_owner':{'result_count':len(owner)},'unauthorized_same_project':{'result_count':len(unauthorized)},'cross_project':{'result_count':len(cross)},'event_forged_authority':{'result_count':len(event_forged)},'content_forged_authority':{'result_count':len(content_forged)}},'selected_ib':golden.get('intelligent_block_id'),'identity_preserved':golden.get('intelligent_block_id')=='IB-000978' and golden.get('source',{}).get('intelligent_block_id')=='IB-000978','provenance_preserved':golden.get('source',{}).get('provenance',{}).get('source_event_id')=='SE-GOLDEN-978','learning_distinct_from_authorization':golden.get('learning_state',{}).get('status')=='VERIFIED' and golden.get('authority',{}).get('state')=='UNCHANGED','current_distinct_from_history':all(x.get('intelligent_block_id')!='IB-000977' for x in current) and any(x.get('intelligent_block_id')=='IB-000977' for x in historical)}

if __name__=='__main__': print(json.dumps(run(),indent=2))
