from kernel.naya_identity_binding import (
    BindingContext,
    canonical_identity_is_stable_across_session_rotation,
    resolve_runtime_authorization,
)

CANONICAL_NAYA_ID = "NAYA-NODE-0001"
CANONICAL_OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f"

def test_runtime_identity_is_not_the_canonical_naya_identity():
    context = BindingContext(naya_id=CANONICAL_NAYA_ID, owner_id=CANONICAL_OWNER_ID, runtime_subject_id="runtime-session-subject", session_id="session-a")
    assert context.naya_id == CANONICAL_NAYA_ID
    assert context.owner_id == CANONICAL_OWNER_ID
    assert context.runtime_subject_id != context.naya_id

def test_token_rotation_does_not_change_canonical_naya_identity():
    before = BindingContext(naya_id=CANONICAL_NAYA_ID, owner_id=CANONICAL_OWNER_ID, runtime_subject_id=CANONICAL_OWNER_ID, session_id="session-a")
    after = BindingContext(naya_id=CANONICAL_NAYA_ID, owner_id=CANONICAL_OWNER_ID, runtime_subject_id=CANONICAL_OWNER_ID, session_id="session-b")
    assert canonical_identity_is_stable_across_session_rotation(before, after)

def test_runtime_authorization_requires_explicit_owner_binding():
    authorized = resolve_runtime_authorization(naya_id=CANONICAL_NAYA_ID, owner_id=CANONICAL_OWNER_ID, runtime_subject_id=CANONICAL_OWNER_ID, binding_owner_id=CANONICAL_OWNER_ID, session_id="session-a")
    assert authorized.authorized is True
    rejected = resolve_runtime_authorization(naya_id=CANONICAL_NAYA_ID, owner_id=CANONICAL_OWNER_ID, runtime_subject_id="orphan-runtime-subject", binding_owner_id=None, session_id="session-a")
    assert rejected.authorized is False
    assert rejected.reason == "OWNER_BINDING_REQUIRED"
