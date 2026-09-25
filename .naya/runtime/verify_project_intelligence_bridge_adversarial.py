#!/usr/bin/env python3
import json, os, urllib.request, urllib.error
URL=os.environ['NAYANET_BRIDGE_URL']; TOKEN=os.environ['NAYANET_BRIDGE_TOKEN']; OWNER_BINDING=os.environ['NAYANET_OWNER_BINDING_TOKEN']
packet=json.load(open('project-intelligence-bridge-packet.json',encoding='utf-8'))
def post(p, token):
    req=urllib.request.Request(URL,data=json.dumps(p).encode(),method='POST',headers={'Authorization':'Bearer '+token,'X-Naya-Owner-Binding':OWNER_BINDING,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=30) as r: return r.status,json.loads(r.read().decode())
    except urllib.error.HTTPError as e: return e.code,json.loads(e.read().decode())
s1,a1=post(packet,TOKEN)
assert s1==200 and a1.get('status') in ('COMPLETED','ACCEPTED') and a1.get('packet_id')==packet['packet_id']
s2,a2=post(packet,TOKEN)
assert s2==200 and a2.get('replay') is True and a2.get('receipt_id')==a1.get('receipt_id') and a2.get('receiver_transaction_id')==a1.get('receiver_transaction_id')
bad=dict(packet); bad['receiver']=dict(packet['receiver']); bad['receiver']['canonical_source']='WRONG-HUB'
s3,a3=post(bad,TOKEN)
assert s3==403 and a3.get('code')=='RECEIVER_MISMATCH'
s4,a4=post(packet,'invalid-oidc-token')
assert s4==401 and a4.get('code')=='OIDC_INVALID'
print(json.dumps({'status':'PASS','first_status':s1,'replay_status':s2,'replay_same_receipt':a2.get('receipt_id')==a1.get('receipt_id'),'wrong_receiver_status':s3,'wrong_receiver_rejected':a3.get('code'),'invalid_token_status':s4,'invalid_token_rejected':a4.get('code'),'receipt_id':a1.get('receipt_id')},indent=2))