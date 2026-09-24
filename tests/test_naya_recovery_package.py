from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("naya_recovery_package", ROOT / "scripts/naya_recovery_package.py")
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repository, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_package_round_trip_is_deterministic_and_tamper_evident() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        repository = root / "repository"
        repository.mkdir()
        (repository / "README.md").write_text("fixture source\n", encoding="utf-8")
        (repository / "hub.html").write_text("<html>fixture</html>\n", encoding="utf-8")
        (repository / "schema.json").write_text('{"type":"object"}\n', encoding="utf-8")
        (repository / "runtime.py").write_text("VALUE = 'restored'\n", encoding="utf-8")
        git(repository, "init")
        git(repository, "remote", "add", "origin", "https://example.invalid/NayaPOWER.git")
        git(repository, "add", ".")
        git(repository, "-c", "user.name=CODA 3", "-c", "user.email=coda3@example.invalid", "commit", "-m", "fixture")
        hub_sha = git(repository, "rev-parse", "HEAD:hub.html")
        write_json(repository / "state.json", {"hub_sha": hub_sha})
        git(repository, "add", "state.json")
        git(repository, "-c", "user.name=CODA 3", "-c", "user.email=coda3@example.invalid", "commit", "--amend", "--no-edit")
        inventory = {
            "schema": module.INVENTORY_SCHEMA,
            "required_components": [
                {"id": "source", "paths": ["README.md"]},
                {"id": "control", "paths": ["state.json"]},
                {"id": "hub", "paths": ["hub.html"]},
                {"id": "schema", "paths": ["schema.json"]},
                {"id": "runtime", "paths": ["runtime.py"]},
            ],
            "required_json": ["state.json", "schema.json"],
            "required_python": ["runtime.py"],
            "control_plane_identity": {
                "hub_path": "hub.html",
                "sha_pointers": {"state.json": ["hub_sha"]},
            },
            "external_exports": [
                {"id": "schema_export", "filename": "schema.sql", "required": True},
                {"id": "data_export", "filename": "data.dump", "required": True},
            ],
            "external_policy": {
                "secret_values_forbidden": True,
                "forbidden_filename_tokens": ["secret", "token", "password", ".env"],
            },
        }
        inventory_path = root / "inventory.json"
        write_json(inventory_path, inventory)
        schema_export = root / "schema.sql"
        data_export = root / "data.dump"
        schema_export.write_text("create table fixture(id int);\n", encoding="utf-8")
        data_export.write_text("fixture data\n", encoding="utf-8")
        package = root / "recovery.zip"
        duplicate_package = root / "recovery-duplicate.zip"
        for output in (package, duplicate_package):
            with contextlib.redirect_stdout(io.StringIO()):
                module.create_package(repository, output, inventory_path, [schema_export, data_export])
        assert module.sha256_file(package) == module.sha256_file(duplicate_package)
        verification = module.verify_package(package)
        assert verification["status"] == "VERIFIED", verification
        destination = root / "restored"
        with contextlib.redirect_stdout(io.StringIO()):
            report = module.restore_package(package, destination)
        assert report["status"] == "VERIFIED", report
        assert report["disaster_recovery_ready"] is True
        assert (destination / "source/hub.html").is_file()
        assert (destination / "external/schema.sql").is_file()
        tampered = root / "tampered.zip"
        with zipfile.ZipFile(package, "r") as source, zipfile.ZipFile(tampered, "w") as target:
            for info in source.infolist():
                data = source.read(info.filename)
                if info.filename == "source.zip":
                    data = data + b"tampered"
                target.writestr(info, data)
        tampered_verification = module.verify_package(tampered)
        assert tampered_verification["status"] == "FAILED"
        assert tampered_verification["failure_code"] == "PACKAGE_CHECKSUM_MISMATCH"


def test_secret_named_external_export_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        repository = root / "repository"
        repository.mkdir()
        (repository / "README.md").write_text("fixture\n", encoding="utf-8")
        git(repository, "init")
        git(repository, "remote", "add", "origin", "https://example.invalid/NayaPOWER.git")
        git(repository, "add", ".")
        git(repository, "-c", "user.name=CODA 3", "-c", "user.email=coda3@example.invalid", "commit", "-m", "fixture")
        inventory = {
            "schema": module.INVENTORY_SCHEMA,
            "required_components": [{"id": "source", "paths": ["README.md"]}],
            "required_json": [],
            "required_python": [],
            "control_plane_identity": {"hub_path": "README.md", "sha_pointers": {"README.md": ["missing"]}},
            "external_exports": [{"id": "required", "filename": "secret.json", "required": True}],
            "external_policy": {
                "secret_values_forbidden": True,
                "forbidden_filename_tokens": ["secret"],
            },
        }
        inventory_path = root / "inventory.json"
        write_json(inventory_path, inventory)
        secret = root / "secret.json"
        write_json(secret, {"forbidden": True})
        try:
            module.create_package(repository, root / "blocked.zip", inventory_path, [secret])
        except module.RecoveryError as error:
            assert str(error) == "EXTERNAL_SECRET_FILENAME_FORBIDDEN:secret.json"
        else:
            raise AssertionError("secret-named external export was accepted")


if __name__ == "__main__":
    test_package_round_trip_is_deterministic_and_tamper_evident()
    test_secret_named_external_export_is_rejected()
    print("RECOVERY_PACKAGE_FIXTURE_ROUND_TRIP=PASS")
    print("RECOVERY_PACKAGE_DETERMINISM=PASS")
    print("RECOVERY_PACKAGE_TAMPER_DETECTION=PASS")
    print("RECOVERY_PACKAGE_SECRET_FILENAME_REJECTION=PASS")
