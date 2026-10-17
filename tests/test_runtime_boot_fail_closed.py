"""Fail-closed boot assertions for kernel/runtime_boot.py.

Scope: this module's fail-closed claim is exactly two checks —
(1) no BRAIN/03-KERNEL/MANIFEST.json anywhere up the tree -> RuntimeError,
     never a fallback node configuration;
(2) the manifest's nine nodes must be the canonical names in canonical order
     with ids NAYA-KERNEL-<name>, otherwise RuntimeError.

Every refusal path in the code gets at least one negative control below.
The two boundaries documented in PR #2298 (non-dict node entries escaping as
AttributeError; unknown top-level fields ignored) are CLOSED by this change:
they now assert RuntimeError. Anything the code still does NOT check (SHA
pinning, receipts, tip freshness) remains documented, not asserted.

Conventions: manifests are written into tmp_path fixtures, so these tests
never depend on the checked-out repo state.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from kernel import runtime_boot

CANONICAL_NAMES = (
    "SELF",
    "LAW",
    "ACT",
    "KNOW",
    "PROVE",
    "CONNECT",
    "VERIFY",
    "LEARN",
    "EVOLVE",
)


def make_manifest(names=CANONICAL_NAMES, id_template="NAYA-KERNEL-{name}"):
    return {
        "kernel_id": "NAYAPOWER-MASTER-KERNEL-V1",
        "schema": "naya.kernel.manifest.v1",
        "nodes": [
            {
                "id": id_template.format(name=name),
                "name": name,
                "responsibility": f"{name} duty",
            }
            for name in names
        ],
    }


def write_repo(tmp_path: Path, manifest) -> Path:
    """Create tmp_path/BRAIN/03-KERNEL/MANIFEST.json from a dict or raw string."""
    manifest_path = tmp_path / "BRAIN" / "03-KERNEL" / "MANIFEST.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(manifest, str):
        manifest_path.write_text(manifest, encoding="utf-8")
    else:
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# find_repository_root
# ---------------------------------------------------------------------------


def test_find_root_missing_manifest_fails_closed_no_fallback(tmp_path):
    """No manifest anywhere up the tree -> RuntimeError, never an invented config."""
    probe = tmp_path / "deep" / "nested"
    probe.mkdir(parents=True)
    with pytest.raises(RuntimeError, match="fails closed"):
        runtime_boot.find_repository_root(probe)


def test_find_root_locates_manifest_from_nested_start(tmp_path):
    root = write_repo(tmp_path, make_manifest())
    probe = tmp_path / "some" / "deep" / "dir"
    probe.mkdir(parents=True)
    assert runtime_boot.find_repository_root(probe) == root


def test_find_root_accepts_a_file_path_as_start(tmp_path):
    root = write_repo(tmp_path, make_manifest())
    start_file = tmp_path / "kernel" / "runtime_boot.py"
    start_file.parent.mkdir(parents=True)
    start_file.touch()
    assert runtime_boot.find_repository_root(start_file) == root


# ---------------------------------------------------------------------------
# load_runtime_manifest — happy path
# ---------------------------------------------------------------------------


def test_load_valid_canonical_manifest_returns_it(tmp_path):
    root = write_repo(tmp_path, make_manifest())
    manifest = runtime_boot.load_runtime_manifest(root)
    assert manifest["nodes"][0] == {
        "id": "NAYA-KERNEL-SELF",
        "name": "SELF",
        "responsibility": "SELF duty",
    }
    assert len(manifest["nodes"]) == 9


# ---------------------------------------------------------------------------
# load_runtime_manifest — fail-closed refusals
# ---------------------------------------------------------------------------


def test_load_missing_manifest_fails_closed(tmp_path):
    with pytest.raises(RuntimeError, match="BRAIN manifest not found"):
        runtime_boot.load_runtime_manifest(tmp_path)


def test_load_corrupt_json_fails_closed_and_names_the_path(tmp_path):
    root = write_repo(tmp_path, "{not valid json,,,")
    with pytest.raises(RuntimeError) as exc_info:
        runtime_boot.load_runtime_manifest(root)
    assert "invalid BRAIN manifest JSON" in str(exc_info.value)
    assert "BRAIN/03-KERNEL/MANIFEST.json" in str(exc_info.value)


def test_load_wrong_node_order_fails_closed(tmp_path):
    names = tuple(reversed(CANONICAL_NAMES))
    root = write_repo(tmp_path, make_manifest(names=names))
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


def test_load_wrong_node_name_fails_closed(tmp_path):
    names = list(CANONICAL_NAMES)
    names[2] = "WILL"  # canonical third node is ACT
    root = write_repo(tmp_path, make_manifest(names=tuple(names)))
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


def test_load_wrong_node_id_fails_closed(tmp_path):
    root = write_repo(tmp_path, make_manifest(id_template="WRONG-{name}"))
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


def test_load_id_attached_to_wrong_name_fails_closed(tmp_path):
    """Ids are canonical but attached to the wrong names -> still refused."""
    manifest = make_manifest()
    manifest["nodes"][0]["id"] = "NAYA-KERNEL-ACT"  # ACT's id on SELF's row
    manifest["nodes"][2]["id"] = "NAYA-KERNEL-SELF"  # SELF's id on ACT's row
    root = write_repo(tmp_path, manifest)
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


def test_load_missing_nodes_key_fails_closed(tmp_path):
    root = write_repo(tmp_path, {"kernel_id": "x"})
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


def test_load_nodes_null_fails_closed(tmp_path):
    root = write_repo(tmp_path, {"nodes": None})
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


def test_load_extra_tenth_node_fails_closed(tmp_path):
    manifest = make_manifest()
    manifest["nodes"].append(
        {"id": "NAYA-KERNEL-EXTRA", "name": "EXTRA", "responsibility": "none"}
    )
    root = write_repo(tmp_path, manifest)
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


def test_load_fewer_than_nine_nodes_fails_closed(tmp_path):
    root = write_repo(tmp_path, make_manifest(names=CANONICAL_NAMES[:8]))
    with pytest.raises(RuntimeError, match="node identity/order"):
        runtime_boot.load_runtime_manifest(root)


# ---------------------------------------------------------------------------
# Boundary hardening: previously documented gaps are now closed
# ---------------------------------------------------------------------------


def test_non_dict_node_entry_fails_closed(tmp_path):
    """A non-dict node entry must not escape as AttributeError: the
    fail-closed contract covers malformed node shapes too."""
    manifest = make_manifest()
    manifest["nodes"][4] = "PROVE"  # not a dict; .get() does not exist
    root = write_repo(tmp_path, manifest)
    with pytest.raises(RuntimeError, match="non-object node entry"):
        runtime_boot.load_runtime_manifest(root)


def test_non_dict_node_entry_variants_fail_closed(tmp_path):
    """None, int, and list entries are all non-object node entries."""
    for bad in (None, 42, ["PROVE"]):
        manifest = make_manifest()
        manifest["nodes"][4] = bad
        root = write_repo(tmp_path, manifest)
        with pytest.raises(RuntimeError, match="non-object node entry"):
            runtime_boot.load_runtime_manifest(root)


def test_unknown_top_level_field_fails_closed(tmp_path):
    """The kernel stores and exposes the manifest dict verbatim, so an
    unknown extra field would ride along unverified inside "the verified
    manifest". Unknown fields are refused, not ignored."""
    manifest = make_manifest()
    manifest["admin_note"] = "spoofed by an unverified writer"
    root = write_repo(tmp_path, manifest)
    with pytest.raises(RuntimeError, match="unexpected top-level fields"):
        runtime_boot.load_runtime_manifest(root)


def test_real_manifest_top_level_shape_is_accepted(tmp_path):
    """The canonical manifest's own top-level fields (kernel_id, schema,
    nodes, node_identity_law, runtime_binding, status) must keep booting."""
    manifest = make_manifest()
    manifest["node_identity_law"] = "NAYA-LAW-9"
    manifest["runtime_binding"] = "boot"
    manifest["status"] = "CANONICAL"
    root = write_repo(tmp_path, manifest)
    loaded = runtime_boot.load_runtime_manifest(root)
    assert loaded["status"] == "CANONICAL"
    assert len(loaded["nodes"]) == 9
