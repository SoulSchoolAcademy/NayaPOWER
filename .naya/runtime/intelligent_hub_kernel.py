#!/usr/bin/env python3
"""Contract-first Intelligent Hub connection kernel.

Provider-neutral kernel for sovereign Superbrain connection, explicit consent,
minimum-necessary wisdom contribution, privacy/quality gating, canonical
Collective Intelligence Event publication, and Intelligence Feed retrieval.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib, hmac, json, re, secrets

PROTOCOL_VERSION = "1.0"
CIE_SCHEMA_VERSION = "1.0"
_EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
_REPO = re.compile(r"https?://(?:www\.)?github\.com/[^/\s]+/[^/\s?#]+", re.I)
_SECRET = re.compile(r"(?:sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|Bearer\s+[A-Za-z0-9._-]{20,})")

class ConnectionStatus(str, Enum):
    PENDING="PENDING"; CONNECTED="CONNECTED"; DEGRADED="DEGRADED"; REVOKED="REVOKED"; UNKNOWN="UNKNOWN"
class GateStatus(str, Enum):
    ACCEPTED="accepted"; REJECTED="rejected"; NEEDS_REVIEW="needs_review"; QUARANTINED="quarantined"; DUPLICATE="duplicate"
@dataclass(frozen=True)
class AuthenticatedContext:
    subject: str; provider: str; installation_id: str; resource_id: str; authenticated: bool=True
@dataclass
class Connection:
    connection_id: str; owner_subject: str; provider: str; installation_id: str; resource_id: str
    capabilities: set[str]=field(default_factory=set); consent_scope: set[str]=field(default_factory=set)
    status: ConnectionStatus=ConnectionStatus.PENDING; created_at: str=""; updated_at: str=""; revoked_at: str|None=None
@dataclass(frozen=True)
class ContributionResult:
    status: GateStatus; contribution_id: str; event: dict|None; reasons: tuple[str,...]
class ReferenceAuthenticator:
    """HMAC fixture authenticator; production providers supply a provider adapter."""
    def __init__(self, secret: bytes|None=None): self._secret=secret or secrets.token_bytes(32)
    def issue(self, subject, installation_id, resource_id):
        p=f"{subject}|{installation_id}|{resource_id}".encode(); s=hmac.new(self._secret,p,hashlib.sha256).hexdigest(); return f"{subject}|{installation_id}|{resource_id}|{s}"
    def verify(self, token, expected):
        p=token.split("|")
        if len(p)!=4 or not expected.authenticated: return False
        payload=f"{p[0]}|{p[1]}|{p[2]}".encode(); s=hmac.new(self._secret,payload,hashlib.sha256).hexdigest()
        return hmac.compare_digest(p[3],s) and p[:3]==[expected.subject,expected.installation_id,expected.resource_id]
def _now(): return datetime.now(timezone.utc).isoformat()
def _id(prefix,value):
    raw=json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode(); return f"{prefix}_{hashlib.sha256(raw).hexdigest()[:24]}"
def privacy_findings(value):
    text=json.dumps(value,ensure_ascii=False,sort_keys=True); out=[]
    if _SECRET.search(text): out.append("secret_or_credential_detected")
    if _EMAIL.search(text): out.append("direct_identifier_detected")
    if _REPO.search(text): out.append("repository_identity_detected")
    return out
def validate_collective_event(event):
    required={"event_id","schema_version","event_type","created_at","effective_at","subject","wisdom","why_it_matters","applicability","evidence","confidence","provenance","privacy","relationships","supersedes","status","verification_receipt"}; errors=sorted(required-set(event))
    if event.get("schema_version")!=CIE_SCHEMA_VERSION: errors.append("schema_version_mismatch")
    try: datetime.fromisoformat(event["created_at"].replace("Z","+00:00")); datetime.fromisoformat(event["effective_at"].replace("Z","+00:00"))
    except (KeyError,ValueError,AttributeError): errors.append("invalid_timestamps")
    if not isinstance(event.get("confidence"),(int,float)) or not 0<=float(event.get("confidence",-1))<=1: errors.append("confidence_must_be_0_to_1")
    privacy=event.get("privacy") or {}
    if privacy.get("identity_included") is not False: errors.append("collective_identity_must_be_excluded")
    if privacy.get("raw_source_included") is not False: errors.append("collective_raw_source_must_be_excluded")
    if not isinstance(event.get("wisdom"),str) or not event["wisdom"].strip(): errors.append("wisdom_required")
    errors += privacy_findings({k:event.get(k) for k in ("subject","wisdom","why_it_matters","applicability")})
    return sorted(set(errors))
class IntelligentHubKernel:
    ALLOWED_CAPABILITIES={"read_superbrain_metadata","read_authorized_wisdom_scope","submit_wisdom_candidate","receive_collective_updates","event_acknowledgement"}
    RAW_FIELDS={"raw_source","conversation","transcript","private_memory","repository_contents","notes"}
    def __init__(self,authenticator=None): self.authenticator=authenticator or ReferenceAuthenticator(); self.connections={}; self.contributions={}; self.events={}; self.acknowledgements=set()
    def connect(self,*,owner_subject,provider,installation_id,resource_id,capabilities):
        if not all((owner_subject,provider,installation_id,resource_id)): raise ValueError("connection identity/resource fields are required")
        caps=set(capabilities); unknown=caps-self.ALLOWED_CAPABILITIES
        if unknown: raise ValueError(f"unsupported capabilities: {sorted(unknown)}")
        cid=_id("conn",[provider,installation_id,resource_id,owner_subject]); now=_now(); c=Connection(cid,owner_subject,provider,installation_id,resource_id,caps,status=ConnectionStatus.CONNECTED,created_at=now,updated_at=now); self.connections[cid]=c; return c
    def _connection(self,cid):
        if cid not in self.connections: raise KeyError(f"unknown connection: {cid}")
        return self.connections[cid]
    def authorize(self,cid,context,token):
        c=self.connections.get(cid); return bool(c and c.status!=ConnectionStatus.REVOKED and self.authenticator.verify(token,context) and (context.subject,context.provider,context.installation_id,context.resource_id)==(c.owner_subject,c.provider,c.installation_id,c.resource_id))
    def grant_consent(self,cid,scope):
        c=self._connection(cid)
        if "wisdom_contribution" in set(scope): c.consent_scope.add("wisdom_contribution")
        c.updated_at=_now(); return c
    def revoke(self,cid,contribution_only=False):
        c=self._connection(cid)
        if contribution_only: c.consent_scope.discard("wisdom_contribution")
        else: c.status=ConnectionStatus.REVOKED; c.revoked_at=_now()
        c.updated_at=_now(); return c
    def submit_wisdom(self,*,connection_id,context,token,contribution,human_approved):
        c=self._connection(connection_id)
        if "submit_wisdom_candidate" not in c.capabilities: return self._reject(contribution,"capability_not_granted")
        if "wisdom_contribution" not in c.consent_scope: return self._reject(contribution,"contribution_consent_not_granted")
        if not self.authorize(connection_id,context,token): return self._reject(contribution,"authentication_or_binding_failed")
        if not human_approved: return self._reject(contribution,"human_review_required_before_publication")
        if self.RAW_FIELDS.intersection(contribution): return self._quarantine(contribution,"raw_private_source_fields_rejected")
        try:
            candidate={"subject":str(contribution.get("subject","")).strip(),"wisdom":str(contribution.get("wisdom","")).strip(),"why_it_matters":str(contribution.get("why_it_matters","")).strip(),"applicability":list(contribution.get("applicability",[])),"evidence":list(contribution.get("evidence",[])),"confidence":float(contribution.get("confidence",0))}
        except (TypeError,ValueError): return self._quarantine(contribution,"malformed_contribution")
        findings=privacy_findings(candidate)
        if findings: return self._quarantine(candidate,*findings)
        if not 0<=candidate["confidence"]<=1: return self._reject(candidate,"confidence_out_of_range")
        if not candidate["subject"] or not candidate["wisdom"]: return self._reject(candidate,"subject_and_wisdom_required")
        fp=_id("fp",[candidate["subject"],candidate["wisdom"],candidate["why_it_matters"]])
        for old in self.contributions.values():
            if old["fingerprint"]==fp: return ContributionResult(GateStatus.DUPLICATE,old["contribution_id"],None,("duplicate_wisdom",))
        cid=_id("contrib",[connection_id,fp]); event=self._build_event(candidate,cid); errors=validate_collective_event(event)
        if errors: return self._quarantine(candidate,*errors)
        self.contributions[cid]={"contribution_id":cid,"connection_id":connection_id,"owner_subject":c.owner_subject,"fingerprint":fp,"status":"accepted"}; self.events[event["event_id"]]=event
        return ContributionResult(GateStatus.ACCEPTED,cid,event,())
    @staticmethod
    def _build_event(c,cid):
        now=_now(); return {"event_id":_id("cie",[c["subject"],c["wisdom"],c["why_it_matters"]]),"schema_version":CIE_SCHEMA_VERSION,"event_type":"insight","created_at":now,"effective_at":now,"subject":c["subject"],"wisdom":c["wisdom"],"why_it_matters":c["why_it_matters"],"applicability":c["applicability"],"evidence":c["evidence"],"confidence":c["confidence"],"provenance":{"source_kind":"authorized_wisdom_contribution","source_event_count":0,"validation_state":"validated","contribution_reference":cid},"privacy":{"identity_included":False,"raw_source_included":False,"privacy_review":"passed"},"relationships":[],"supersedes":[],"status":"published","verification_receipt":{"verified":True,"verified_at":now,"checks":["authenticated_connection","explicit_contribution_consent","human_review","privacy_gate","quality_gate","schema_validation","identity_excluded_from_collective_object","raw_source_excluded_from_collective_object"]}}
    @staticmethod
    def _reject(x,reason): return ContributionResult(GateStatus.REJECTED,_id("contrib",x),None,(reason,))
    @staticmethod
    def _quarantine(x,*reasons): return ContributionResult(GateStatus.QUARANTINED,_id("contrib",x),None,tuple(sorted(set(reasons))))
    def intelligence_feed(self,*,limit=50,event_type=None):
        rows=[e for e in self.events.values() if e["status"] in {"published","validated"}]
        if event_type: rows=[e for e in rows if e["event_type"]==event_type]
        return sorted(rows,key=lambda e:e["effective_at"],reverse=True)[:limit]
    def retrieve_event(self,event_id):
        e=self.events.get(event_id); return json.loads(json.dumps(e)) if e and e["status"] in {"published","validated"} else None
    def acknowledge(self,cid,event_id):
        c=self._connection(cid)
        if "event_acknowledgement" not in c.capabilities or c.status==ConnectionStatus.REVOKED or event_id not in self.events: return False
        self.acknowledgements.add((cid,event_id)); return True

__all__=["AuthenticatedContext","Connection","ConnectionStatus","ContributionResult","GateStatus","IntelligentHubKernel","ReferenceAuthenticator","validate_collective_event"]
