from pathlib import Path

from kernel.brain_registry import load_and_validate_brain


def test_brain_population_has_exactly_nine_canonical_kernel_objects():
    root = Path(__file__).resolve().parents[1]

    report = load_and_validate_brain(root)

    assert report["ok"] is True, report
    assert report["node_count"] == 9
    assert report["source_count"] == 15
    assert report["graph_edge_count"] >= 9
    assert report["errors"] == []


def test_brain_population_rejects_missing_node_object(tmp_path):
    root = Path(__file__).resolve().parents[1]
    report = load_and_validate_brain(root, root_override=tmp_path)

    assert report["ok"] is False
    assert report["errors"]


def test_brain_population_rejects_node_relationship_drift(tmp_path):
    root = Path(__file__).resolve().parents[1]

    # Copy the canonical BRAIN tree into an isolated fixture so the test can
    # mutate one object without touching the repository source. The fixture
    # must be a real git checkout: the fail-closed reader (B-51) refuses to
    # read an unverifiable index, so the drifted object would never be
    # reached. Committing the copy lets the guard verify FRESH and the
    # relationship-drift assertion still gets exercised.
    import shutil
    import subprocess

    shutil.copytree(root / "BRAIN", tmp_path / "BRAIN")
    subprocess.run(["git", "-C", str(tmp_path), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-qm", "fixture"],
        check=True,
    )
    object_path = tmp_path / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-SELF.json"
    data = object_path.read_text(encoding="utf-8")
    data = data.replace('"REL-KERNEL-SELF-LAW"', '"REL-KERNEL-SELF-LAW-BROKEN"', 1)
    object_path.write_text(data, encoding="utf-8")
    # Re-point the fixture's manifest at the drifted bytes: the guard compares
    # against the manifest, so the fixture manifest must describe the fixture
    # corpus for the verdict to be FRESH and the relationship-drift check to
    # be the thing that refuses.
    import json

    manifest_path = tmp_path / "BRAIN/REAL-TREE.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    new_blob = subprocess.run(
        ["git", "-C", str(tmp_path), "hash-object", "--", str(object_path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    for entry in manifest["files"]:
        if entry["path"] == "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-SELF.json":
            entry["blob_sha"] = new_blob
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-qm", "drift"],
        check=True,
    )

    report = load_and_validate_brain(root, root_override=tmp_path)

    assert report["ok"] is False
    assert any("relationship" in error for error in report["errors"])
