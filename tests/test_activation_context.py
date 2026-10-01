import pytest

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


@pytest.mark.parametrize("field", ["human_owner_id", "naya_id", "owner_repo", "upstream_repo", "tenant_project_id", "network_scope"])
@pytest.mark.parametrize("value", [None, "", "   ", 17])
def test_required_identifiers_reject_null_blank_and_non_string_values(field, value):
    with pytest.raises(ValueError, match="ACTIVATION_CONTEXT_REQUIRED"):
        context(**{field: value}).validate()


def test_missing_owner_identity_fails_closed():
    with pytest.raises(ValueError, match="human_owner_id"):
        context(human_owner_id="").validate()


@pytest.mark.parametrize("owner_repo", [
    "SoulSchoolAcademy/NayaPOWER",
    "soulschoolacademy/nayapower",
    "SOULSCHOOLACADEMY/NAYAPOWER",
])
def test_owner_repo_cannot_be_the_upstream_repo_case_insensitively(owner_repo):
    with pytest.raises(ValueError, match="OWNER_REPO_MUST_BE_DISTINCT_FROM_UPSTREAM"):
        context(owner_repo=owner_repo).validate()


@pytest.mark.parametrize("mode", [None, "", "UNSUPPORTED", 17])
def test_missing_or_unsupported_activation_mode_fails_closed(mode):
    with pytest.raises(ValueError, match="ACTIVATION_MODE_INVALID"):
        context(mode=mode).validate()


@pytest.mark.parametrize("mode", ["FORK_FIRST", "INDEPENDENT_BOOTSTRAP"])
def test_supported_string_mode_is_normalized_to_enum(mode):
    validated = context(mode=mode).validate()
    assert validated.mode is ActivationMode(mode)


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
