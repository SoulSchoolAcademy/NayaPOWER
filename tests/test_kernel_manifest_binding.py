"""The runtime must learn its node order from the canonical manifest, or fail closed.

These tests exist because `kernel/nayapower_kernel.py` previously carried its own
hardcoded nine-tuple while `kernel/brain_registry.py` validated the manifest.
That arrangement let the runtime and the canonical store drift with every gate
green, which the execution directive names as an explicit AAA blocker
("runtime/manifest drift").

Derivation is proven BEHAVIOURALLY: reordering or mutating the manifest changes
what the runtime reports. It is not proven by reading the source, because reading
the source is how the previous drift shipped.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kernel.brain_registry import (
    BrainIntegrityError,
    CANONICAL_MANIFEST_PATH,
    load_canonical_kernel,
    load_canonical_node_ids,
    load_canonical_node_names,
    repo_root,
)
from kernel.nayapower_kernel import (
    Authority,
    DecisionContext,
    Kernel,
    KernelIntegrityError,
    Node,
    TruthState,
)

ROOT = repo_root()
MANIFEST = ROOT / CANONICAL_MANIFEST_PATH


@pytest.fixture
def temp_brain(tmp_path: Path):
    """Build a throwaway tree containing a copy of the real manifest."""
    target = tmp_path / CANONICAL_MANIFEST_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(MANIFEST.read_text(encoding="utf-8"), encoding="utf-8")
    Kernel.clear_cache()
    yield tmp_path
    Kernel.clear_cache()


def mutate(temp_root: Path, fn) -> Path:
    path = temp_root / CANONICAL_MANIFEST_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    fn(data)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    Kernel.clear_cache()
    return temp_root


# ---------------------------------------------------------------- the happy path

def test_manifest_declares_exactly_nine_nodes():
    kernel = load_canonical_kernel(ROOT)
    assert kernel["node_count"] == 9
    assert len(load_canonical_node_names(ROOT)) == 9
    assert len(set(load_canonical_node_ids(ROOT))) == 9


def test_runtime_node_order_is_the_manifest_order():
    """LOADS: the runtime reports the nine nodes the manifest declares."""
    order = Kernel.node_order()
    assert len(order) == 9
    assert tuple(n.value for n in order) == load_canonical_node_names(ROOT)


def test_runtime_order_matches_the_registry_pin():
    """The manifest, the registry, and the code-level enum must all agree."""
    from kernel.brain_registry import NODE_NAMES

    assert tuple(n.value for n in Kernel.node_order()) == NODE_NAMES
    assert load_canonical_node_names(ROOT) == NODE_NAMES


def test_every_runtime_node_is_a_real_enum_member():
    for node in Kernel.node_order():
        assert isinstance(node, Node)


# ------------------------------------------- derivation proven by perturbation

def test_reordering_the_manifest_changes_the_runtime_order(temp_brain):
    """If the runtime were hardcoded, this test would not notice the change."""
    before = Kernel.node_order(temp_brain)

    def rotate(data):
        data["nodes"] = data["nodes"][1:] + data["nodes"][:1]

    after = Kernel.node_order(mutate(temp_brain, rotate))

    assert before != after
    assert after == before[1:] + before[:1]
    assert sorted(n.value for n in after) == sorted(n.value for n in before)


def test_renaming_a_node_in_the_manifest_breaks_the_runtime_loudly(temp_brain):
    """A manifest naming a node the runtime cannot represent is a hard failure.

    Silently dropping the unknown node would leave a kernel that reports nine
    nodes while running eight.
    """
    root = mutate(temp_brain, lambda d: d["nodes"][0].__setitem__("name", "REFLECT"))
    with pytest.raises(KernelIntegrityError) as exc:
        Kernel.node_order(root)
    assert "REFLECT" in str(exc.value)


def test_runtime_source_no_longer_hardcodes_the_node_order():
    """Guard against the hardcoded tuple being reintroduced."""
    source = (ROOT / "kernel/nayapower_kernel.py").read_text(encoding="utf-8")
    assert "_NODE_ORDER" not in source, (
        "kernel/nayapower_kernel.py reintroduced a hardcoded node order; the "
        "manifest is the single source of truth"
    )


# --------------------------------------------------------------- fail-closed

def _assert_refused(result) -> None:
    assert result.allowed is False
    assert result.executed is False
    assert result.truth_state is TruthState.BLOCKED
    assert result.blocked_by is Node.KNOW
    assert result.evidence and "kernel_integrity" in result.evidence[0]


AUTHORIZED = DecisionContext(
    action="publish_change",
    consequential=True,
    authority=Authority(scope="publish_change"),
)


def test_missing_manifest_refuses_even_a_correctly_scoped_action(tmp_path):
    """The most important case: valid authority must not rescue a broken kernel."""
    empty = tmp_path / "no-brain"
    empty.mkdir()
    result = Kernel().decide(AUTHORIZED, root=empty)
    _assert_refused(result)


def test_short_manifest_refuses(temp_brain):
    root = mutate(temp_brain, lambda d: d.__setitem__("nodes", d["nodes"][:8]))
    _assert_refused(Kernel().decide(AUTHORIZED, root=root))


def test_empty_node_list_refuses(temp_brain):
    root = mutate(temp_brain, lambda d: d.__setitem__("nodes", []))
    _assert_refused(Kernel().decide(AUTHORIZED, root=root))


def test_duplicate_node_name_refuses(temp_brain):
    root = mutate(
        temp_brain,
        lambda d: d["nodes"][1].__setitem__("name", d["nodes"][0]["name"]),
    )
    _assert_refused(Kernel().decide(AUTHORIZED, root=root))


def test_duplicate_node_id_refuses(temp_brain):
    root = mutate(
        temp_brain,
        lambda d: d["nodes"][1].__setitem__("id", d["nodes"][0]["id"]),
    )
    _assert_refused(Kernel().decide(AUTHORIZED, root=root))


def test_missing_node_name_refuses(temp_brain):
    root = mutate(temp_brain, lambda d: d["nodes"][2].pop("name"))
    _assert_refused(Kernel().decide(AUTHORIZED, root=root))


def test_missing_node_id_refuses(temp_brain):
    root = mutate(temp_brain, lambda d: d["nodes"][2].pop("id"))
    _assert_refused(Kernel().decide(AUTHORIZED, root=root))


def test_unparseable_manifest_refuses(temp_brain):
    (temp_brain / CANONICAL_MANIFEST_PATH).write_text("{not json", encoding="utf-8")
    Kernel.clear_cache()
    _assert_refused(Kernel().decide(AUTHORIZED, root=temp_brain))


def test_unparseable_manifest_is_reported_as_unparseable(temp_brain):
    """Refusing is not enough; the reason must survive, or diagnosis degrades.

    A corrupt manifest and an empty one are different faults. If both report
    'manifest_declares_no_nodes' the operator is sent to the wrong place.
    """
    (temp_brain / CANONICAL_MANIFEST_PATH).write_text("{not json", encoding="utf-8")
    Kernel.clear_cache()
    result = Kernel().decide(AUTHORIZED, root=temp_brain)
    _assert_refused(result)
    assert "unparseable_manifest" in result.evidence[0], result.evidence


def test_a_malformed_node_is_reported_not_silently_skipped(temp_brain):
    """A non-object node must be named, not dropped and blamed on the count.

    Silently skipping it would still fail closed via the count check, which
    makes the mutant look safe while destroying the diagnosis.
    """
    root = mutate(temp_brain, lambda d: d["nodes"].__setitem__(3, "SELF"))
    result = Kernel().decide(AUTHORIZED, root=root)
    _assert_refused(result)
    assert "is_not_an_object" in result.evidence[0], result.evidence


def test_a_truncated_manifest_is_reported_as_a_count_mismatch(temp_brain):
    root = mutate(temp_brain, lambda d: d.__setitem__("nodes", d["nodes"][:8]))
    result = Kernel().decide(AUTHORIZED, root=root)
    _assert_refused(result)
    assert "node_count_mismatch" in result.evidence[0], result.evidence


def test_node_that_is_not_an_object_refuses(temp_brain):
    root = mutate(temp_brain, lambda d: d["nodes"].__setitem__(3, "SELF"))
    _assert_refused(Kernel().decide(AUTHORIZED, root=root))


def test_blocked_by_integrity_never_reports_an_outcome(temp_brain):
    """An unverified kernel must not emit an outcome or a next state."""
    root = mutate(temp_brain, lambda d: d.__setitem__("nodes", d["nodes"][:3]))
    result = Kernel().decide(AUTHORIZED, root=root)
    assert result.outcome is None
    assert result.next_state == {}
    assert result.learning_candidate is None


def test_loader_reports_every_problem_not_just_the_first(temp_brain):
    root = mutate(
        temp_brain,
        lambda d: (
            d["nodes"][0].pop("id"),
            d["nodes"][1].pop("name"),
            d["nodes"][2].__setitem__("id", d["nodes"][3]["id"]),
        ),
    )
    with pytest.raises(BrainIntegrityError) as exc:
        load_canonical_kernel(root)
    detail = str(exc.value)
    assert "node_1_missing_id" in detail
    assert "node_2_missing_name" in detail
    assert "duplicate_node_id" in detail


# ------------------------------------------------- authority still outranks all

def test_intact_kernel_still_blocks_unscoped_authority():
    """The manifest binding must not weaken the LAW gate."""
    result = Kernel().decide(
        DecisionContext(action="publish_change", consequential=True, authority=None)
    )
    assert result.allowed is False
    assert result.blocked_by is Node.LAW


def test_intact_kernel_still_blocks_wrong_scope():
    result = Kernel().decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=Authority(scope="something_else"),
        )
    )
    assert result.allowed is False
    assert result.blocked_by is Node.LAW


def test_intact_kernel_still_does_not_claim_verification():
    """Execution is an observation. Binding to the manifest changes nothing here."""
    result = Kernel().decide(AUTHORIZED)
    assert result.allowed is True
    assert result.truth_state is TruthState.UNKNOWN
    assert result.trace == Kernel.node_order()
