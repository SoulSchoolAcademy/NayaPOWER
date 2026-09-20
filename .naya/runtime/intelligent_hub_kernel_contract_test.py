#!/usr/bin/env python3
"""Executable happy-path and adversarial proof for the Intelligent Hub kernel."""
from intelligent_hub_kernel import AuthenticatedContext, GateStatus, IntelligentHubKernel, ReferenceAuthenticator, validate_collective_event

def fixture():
    auth=ReferenceAuthenticator(b"test-secret")
    hub=IntelligentHubKernel(auth)
    c=hub.connect(owner_subject="subject:anonymous-test-01",provider="github",installation_id="gh-install-01",resource_id="repo-superbrain-01",capabilities={"submit_wisdom_candidate","receive_collective_updates","event_acknowledgement"})
    ctx=AuthenticatedContext("subject:anonymous-test-01","github","gh-install-01","repo-superbrain-01")
    return hub,c,ctx,auth.issue(ctx.subject,ctx.installation_id,ctx.resource_id)

def wisdom():
    return {"subject":"Smallest safe integration boundary","wisdom":"Preserve working behavior and establish the smallest verified boundary before expanding scope.","why_it_matters":"This reduces architectural drift and makes failures easier to localize.","applicability":["software architecture"],"evidence":[{"kind":"test","state":"observed"}],"confidence":0.92}

def test_connection_and_consent_boundary():
    h,c,x,t=fixture(); r=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t,contribution=wisdom(),human_approved=True); assert r.status==GateStatus.REJECTED and "contribution_consent_not_granted" in r.reasons

def test_authenticated_contribution_publishes_anonymous_event():
    h,c,x,t=fixture(); h.grant_consent(c.connection_id,{"wisdom_contribution"}); r=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t,contribution=wisdom(),human_approved=True); assert r.status==GateStatus.ACCEPTED; assert validate_collective_event(r.event)==[]; assert r.event["privacy"]["identity_included"] is False; assert "owner_subject" not in r.event; assert h.retrieve_event(r.event["event_id"])["event_id"]==r.event["event_id"]

def test_human_approval_required():
    h,c,x,t=fixture(); h.grant_consent(c.connection_id,{"wisdom_contribution"}); r=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t,contribution=wisdom(),human_approved=False); assert r.status==GateStatus.REJECTED and "human_review_required_before_publication" in r.reasons

def test_bad_authentication_rejected():
    h,c,x,t=fixture(); h.grant_consent(c.connection_id,{"wisdom_contribution"}); r=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t+"tampered",contribution=wisdom(),human_approved=True); assert r.status==GateStatus.REJECTED and "authentication_or_binding_failed" in r.reasons

def test_private_identity_repository_and_secret_inputs_quarantined():
    h,c,x,t=fixture(); h.grant_consent(c.connection_id,{"wisdom_contribution"})
    for extra in ({"raw_source":"private conversation"},{"wisdom":"Contact jane@example.com"},{"wisdom":"See https://github.com/example/private-superbrain"},{"wisdom":"Use ghp_abcdefghijklmnopqrstuvwxyz1234567890"}):
        candidate=wisdom(); candidate.update(extra); r=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t,contribution=candidate,human_approved=True); assert r.status==GateStatus.QUARANTINED
    assert h.intelligence_feed()==[]

def test_duplicate_and_acknowledgement():
    h,c,x,t=fixture(); h.grant_consent(c.connection_id,{"wisdom_contribution"}); a=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t,contribution=wisdom(),human_approved=True); b=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t,contribution=wisdom(),human_approved=True); assert a.status==GateStatus.ACCEPTED and b.status==GateStatus.DUPLICATE; assert h.acknowledge(c.connection_id,a.event["event_id"])

def test_revoked_connection_cannot_contribute():
    h,c,x,t=fixture(); h.grant_consent(c.connection_id,{"wisdom_contribution"}); h.revoke(c.connection_id); r=h.submit_wisdom(connection_id=c.connection_id,context=x,token=t,contribution=wisdom(),human_approved=True); assert r.status==GateStatus.REJECTED

if __name__=="__main__":
    tests=[v for k,v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests: test()
    print(f"PASS: {len(tests)} Intelligent Hub contract/adversarial tests")
