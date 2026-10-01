from kernel.activation_context import ActivationContext, ActivationMode


def context(**overrides):
    base = dict(
        human_owner_id="owner-a",
        naya_id="NAYA-A",
        owner_repo="Alice/NayaPOWER",
        upstream_repo="SoulSchoolAcademy/NayaPOWER",
        tenant_project_id="tenant-a",
        authority_context={"state": "RESOLVE_AT_ACTION"},
        persistence_context={"provider": "NAYANET_SHARED", "owner_scoped": True},
        network_scope="PRIVATE",
        mode=ActivationMode.FORK_FIRST,
    )
    base.update(overrides)
    return ActivationContext(**base)


def test_fork_first_context_targets_the_owner_repo_not_upstream():
    ctx = context().validate()
    assert ctx.repository_target == "Alice/NayaPOWER"
    assert ctx.repository_target != ctx.upstream_repo


def test_independent_bootstrap_converges_into_same_context_shape():
    ctx = context(
        mode=ActivationMode.INDEPENDENT_BOOTSTRAP,
        owner_repo="Bob/NayaPOWER",
        human_owner_id="owner-b",
        naya_id="NAYA-B",
        tenant_project_id="tenant-b",
    ).validate()
    assert ctx.repository_target == "Bob/NayaPOWER"
    assert ctx.upstream_repo == "SoulSchoolAcademy/NayaPOWER"


def test_missing_owner_identity_fails_closed():
    try:
        context(human_owner_id="").validate()
    except ValueError as exc:
        assert "human_owner_id" in str(exc)
    else:
        raise AssertionError("missing owner identity must fail closed")


def test_owner_repo_cannot_be_the_upstream_repo():
    try:
        context(owner_repo="SoulSchoolAcademy/NayaPOWER").validate()
    except ValueError as exc:
        assert str(exc) == "OWNER_REPO_MUST_BE_DISTINCT_FROM_UPSTREAM"
    else:
        raise AssertionError("owner repo must be distinct from upstream")


def test_two_owners_resolve_to_distinct_projection_targets():
    a = context().validate()
    b = context(
        human_owner_id="owner-b",
        naya_id="NAYA-B",
        owner_repo="Bob/NayaPOWER",
        tenant_project_id="tenant-b",
    ).validate()
    assert a.human_owner_id != b.human_owner_id
    assert a.repository_target != b.repository_target
