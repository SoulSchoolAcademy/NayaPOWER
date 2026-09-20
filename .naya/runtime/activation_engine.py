#!/usr/bin/env python3
"""Deterministic zero-setup document activation.

Documents may originate from PDF extraction, copy/paste, or a future hosted
uploader. This layer establishes immutable identity, chunks content
deterministically, detects duplicates/conflicts, and promotes verified
activation documents through the existing canonical event writer.

Canonical Note Events remain authoritative. Chunks and indexes are derived.
Vectors are optional and never required for baseline activation.
"""
from __future__ import annotations
import hashlib,json,re
from dataclasses import dataclass,asdict
from datetime import datetime
from pathlib import Path
from typing import Any
from activation_contract import validate_manifest
from canonical_event_store import create_or_replay
ROOT=Path(__file__).resolve().parents[2]; MEMORY=ROOT/".naya"/"memory"; EVENTS=MEMORY/"events"; INDEX=EVENTS/"INDEX.json"; ACTIVATION_ROOT=MEMORY/"activations"; STATE_FILE=ACTIVATION_ROOT/"ACTIVATION-STATE.json"; RECEIPT_FILE=ACTIVATION_ROOT/"ACTIVATION-RECEIPT.json"; NEXT_EXECUTION=".naya/handoffs/NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md"
def sha256_text(text:str)->str:return hashlib.sha256(text.replace("\r\n","\n").encode("utf-8")).hexdigest()
def stable_document_identity(package_id:str,document_id:str,version:str,content:str)->str:return hashlib.sha256(f"{package_id}\n{document_id}\n{version}\n{sha256_text(content)}".encode()).hexdigest()
def chunk_text(text:str,max_chars:int=2400,overlap:int=240)->list[str]:
    if max_chars<=0 or overlap<0 or overlap>=max_chars:raise ValueError("chunk bounds are invalid")
    normalized=re.sub(r"\r\n?","\n",text).strip()
    if not normalized:return []
    paragraphs=[p.strip() for p in re.split(r"\n\s*\n",normalized) if p.strip()]; chunks=[]; current=""
    for paragraph in paragraphs:
        candidate=paragraph if not current else current+"\n\n"+paragraph
        if len(candidate)<=max_chars:current=candidate; continue
        if current:chunks.append(current)
        if len(paragraph)<=max_chars:current=paragraph; continue
        start=0
        while start<len(paragraph):
            end=min(start+max_chars,len(paragraph)); piece=paragraph[start:end].strip()
            if piece:chunks.append(piece)
            if end>=len(paragraph):break
            start=max(0,end-overlap)
        current=""
    if current:chunks.append(current)
    return chunks
@dataclass(frozen=True)
class ActivatedDocument:
    document_id:str; version:str; package_id:str; order:int; purpose:str; content_sha256:str; identity:str; chunk_count:int; status:str="READY"
def prepare_document(document:dict[str,Any],chunk_size:int=2400)->tuple[ActivatedDocument,list[str]]:
    required=("document_id","version","package_id","order","purpose","content"); missing=[key for key in required if document.get(key) in (None,"")]
    if missing:raise ValueError("document missing: "+", ".join(missing))
    content=str(document["content"]); chunks=chunk_text(content,max_chars=chunk_size)
    if not chunks:raise ValueError(f"document {document['document_id']} has no usable content")
    identity=stable_document_identity(str(document["package_id"]),str(document["document_id"]),str(document["version"]),content)
    return ActivatedDocument(document_id=str(document["document_id"]),version=str(document["version"]),package_id=str(document["package_id"]),order=int(document["order"]),purpose=str(document["purpose"]),content_sha256=sha256_text(content),identity=identity,chunk_count=len(chunks)),chunks
def inspect_package(manifest:dict[str,Any],chunk_size:int=2400)->dict[str,Any]:
    errors=validate_manifest(manifest)
    if errors:return {"status":"FAILED","errors":errors,"documents":[]}
    prepared=[]; identities=set()
    for document in sorted(manifest["documents"],key=lambda x:x["order"]):
        try:item,_=prepare_document(document,chunk_size=chunk_size)
        except ValueError as exc:return {"status":"FAILED","errors":[str(exc)],"documents":[]}
        if item.identity in identities:return {"status":"CONFLICT","errors":[f"duplicate content identity: {item.document_id}"],"documents":[]}
        identities.add(item.identity); prepared.append(item)
    expected=list(range(1,len(prepared)+1)); actual=[item.order for item in prepared]
    if actual!=expected:return {"status":"PARTIAL","errors":[f"missing or out-of-order documents: expected {expected}, got {actual}"],"documents":[asdict(x) for x in prepared]}
    return {"status":"READY","errors":[],"package_id":manifest["package_id"],"package_version":manifest["package_version"],"document_count":len(prepared),"chunk_count":sum(x.chunk_count for x in prepared),"documents":[asdict(x) for x in prepared]}
def _project_context()->tuple[dict[str,Any],str]:
    project_path=MEMORY/"projects"/"CURRENT-DAILY-PROJECT.json"; project=json.loads(project_path.read_text(encoding="utf-8")); return project,str(project.get("current_objective",""))
def _event_id(document_id:str,effective_at:str)->str:
    dt=datetime.fromisoformat(effective_at.replace("Z","+00:00")); slug=re.sub(r"[^a-z0-9-]+","-",document_id.lower()).strip("-") or "document"; return f"SE-{dt:%Y%m%d-%H%M%S}-activation-{slug}"
def promote_document(document:dict[str,Any],effective_at:str,chunk_size:int=2400)->dict[str,Any]:
    prepared,chunks=prepare_document(document,chunk_size=chunk_size); project,current_objective=_project_context(); event_id=_event_id(prepared.document_id,effective_at)
    event={"event_id":event_id,"created_at":effective_at,"effective_at":effective_at,"status":"CANONICAL","event_type":"system-change","type":"system-change","title":f"NayaPOWER activation: {prepared.document_id}","subject":prepared.purpose,"summary":f"Activated {prepared.document_id} from package {prepared.package_id}.","project":project["project_name"],"project_context":{"project_id":project["project_id"],"current_daily_project":project["project_name"],"project_name":project["project_name"],"current_objective":current_objective},"source":{"type":"activation-document","id":prepared.document_id,"package_id":prepared.package_id,"content_sha256":prepared.content_sha256},"tags":["activation","implementation","knowledge","canonical-memory"],"concepts":["document","chunk","canonical memory","retrieval"],"representations":{"naya":{"id":f"SN-{effective_at[:10].replace('-','')}-{effective_at[11:19].replace(':','')}-{prepared.document_id.lower()}-naya","canonical_event_id":event_id,"title":f"Naya activation — {prepared.document_id}","summary":f"Machine activation of {prepared.document_id} into canonical memory.","content":"\n\n".join(chunks),"lessons":["Activation documents become canonical memory only through the canonical event boundary."]},"shawn":{"id":f"SN-{effective_at[:10].replace('-','')}-{effective_at[11:19].replace(':','')}-{prepared.document_id.lower()}-shawn","canonical_event_id":event_id,"title":f"Shawn activation — {prepared.document_id}","summary":f"Human-facing record of {prepared.document_id} activation.","content":f"Activated document {prepared.document_id} ({prepared.purpose}).","lessons":["Document activation is deterministic and repeat-safe."]}},"learning":{"status":"CAPTURED","lessons":["Document identity and content hash make activation repeat-safe."]},"next_execution":{"path":NEXT_EXECUTION,"next_action":"Continue activation verification and retrieval validation."},"continuity":{"learning_status":"CAPTURED","next_execution_path":NEXT_EXECUTION},"verification":{"status":"VERIFIED","canonical_url":f"local://activation/{prepared.identity}","checks":["document_identity","chunking","project_binding","paired_representations","learning_capture"]},"delivery":{"status":"DELIVERED","target":"canonical-memory"},"receipt":{"status":"EMITTED","activation_identity":prepared.identity}}
    result=create_or_replay(event,EVENTS,INDEX); result["document_identity"]=prepared.identity; result["chunk_count"]=len(chunks); return result
def persist_activation_state(result:dict[str,Any],manifest:dict[str,Any])->None:
    ACTIVATION_ROOT.mkdir(parents=True,exist_ok=True); state={"schema_version":1,"package_id":manifest.get("package_id"),"package_version":manifest.get("package_version"),"status":result.get("status"),"document_count":result.get("document_count",0),"chunk_count":result.get("chunk_count",0),"documents":result.get("documents",[]),"authoritative_source":"canonical Note Events","derived_indexes":["events/INDEX.json","retrieval baseline"],"vectors":"OPTIONAL_DERIVED","errors":result.get("errors",[])}; STATE_FILE.write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def make_receipt(result:dict[str,Any])->dict[str,Any]:
    status=result.get("status"); return {"schema_version":1,"receipt_type":"NAYAPOWER_ACTIVATION","status":"VERIFIED" if status in {"READY","CREATED","REPLAY"} else status,"verified":status in {"READY","CREATED","REPLAY"},"package_id":result.get("package_id"),"package_version":result.get("package_version"),"document_count":result.get("document_count",0),"chunk_count":result.get("chunk_count",0),"canonical_source":"Note Events","derived_representations":["chunks","lexical index","retrieval"],"vector_requirement":"NONE","next_execution":NEXT_EXECUTION,"errors":result.get("errors",[])}
def persist_receipt(result:dict[str,Any])->dict[str,Any]:
    ACTIVATION_ROOT.mkdir(parents=True,exist_ok=True); receipt=make_receipt(result); RECEIPT_FILE.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); return receipt
def activate(manifest:dict[str,Any],chunk_size:int=2400,effective_at:str|None=None,promote:bool=False)->dict[str,Any]:
    result=inspect_package(manifest,chunk_size=chunk_size)
    if result.get("status")!="READY":persist_activation_state(result,manifest); persist_receipt(result); return result
    if promote:
        if not effective_at:effective_at=datetime.now().astimezone().isoformat(timespec="seconds")
        outcomes=[promote_document(document,effective_at,chunk_size=chunk_size) for document in sorted(manifest["documents"],key=lambda x:x["order"])]
        result["promotion"]=outcomes
        if any(item.get("status")=="CONFLICT" for item in outcomes):result["status"]="CONFLICT"; result["errors"]=["canonical promotion conflict detected"]
    persist_activation_state(result,manifest); persist_receipt(result); return result
