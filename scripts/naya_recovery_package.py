from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

PACKAGE_SCHEMA = "naya-recovery-package/v1"
INVENTORY_SCHEMA = "naya-recovery-package-inventory/v1"
MANIFEST_SCHEMA = "naya-recovery-package-manifest/v1"
VERIFY_SCHEMA = "naya-recovery-package-verification/v1"
RESTORE_SCHEMA = "naya-recovery-package-restore/v1"


class RecoveryError(RuntimeError):
    pass


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RecoveryError(result.stderr.strip() or "GIT_COMMAND_FAILED")
    return result.stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def safe_relative_path(value: str) -> str:
    if not value or value.startswith("/") or "\\" in value:
        raise RecoveryError("UNSAFE_RECOVERY_PATH:" + value)
    path = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise RecoveryError("UNSAFE_RECOVERY_PATH:" + value)
    return path.as_posix()


def validate_inventory(inventory: dict[str, Any]) -> dict[str, Any]:
    if inventory.get("schema") != INVENTORY_SCHEMA:
        raise RecoveryError("RECOVERY_INVENTORY_SCHEMA_INVALID")
    components = inventory.get("required_components")
    if not isinstance(components, list) or not components:
        raise RecoveryError("RECOVERY_INVENTORY_COMPONENTS_INVALID")
    component_ids: set[str] = set()
    for component in components:
        if not isinstance(component, dict) or not component.get("id") or not isinstance(component.get("paths"), list):
            raise RecoveryError("RECOVERY_INVENTORY_COMPONENT_INVALID")
        if component["id"] in component_ids:
            raise RecoveryError("RECOVERY_INVENTORY_COMPONENT_DUPLICATE:" + str(component["id"]))
        component_ids.add(str(component["id"]))
        for path in component["paths"]:
            safe_relative_path(str(path))
    for field in ("required_json", "required_python"):
        values = inventory.get(field)
        if not isinstance(values, list):
            raise RecoveryError("RECOVERY_INVENTORY_FIELD_INVALID:" + field)
        for path in values:
            safe_relative_path(str(path))
    identity = inventory.get("control_plane_identity")
    if not isinstance(identity, dict):
        raise RecoveryError("RECOVERY_INVENTORY_IDENTITY_INVALID")
    safe_relative_path(str(identity.get("hub_path") or ""))
    pointers = identity.get("sha_pointers")
    if not isinstance(pointers, dict) or not pointers:
        raise RecoveryError("RECOVERY_INVENTORY_IDENTITY_POINTERS_INVALID")
    for path in pointers:
        safe_relative_path(str(path))
        if not isinstance(pointers[path], list) or not pointers[path]:
            raise RecoveryError("RECOVERY_INVENTORY_IDENTITY_POINTER_INVALID:" + str(path))
    exports = inventory.get("external_exports")
    if not isinstance(exports, list) or not exports:
        raise RecoveryError("RECOVERY_INVENTORY_EXPORTS_INVALID")
    filenames: set[str] = set()
    for export in exports:
        if not isinstance(export, dict) or not export.get("id") or not export.get("filename"):
            raise RecoveryError("RECOVERY_INVENTORY_EXPORT_INVALID")
        filename = safe_relative_path(str(export["filename"]))
        if filename in filenames:
            raise RecoveryError("RECOVERY_INVENTORY_EXPORT_DUPLICATE:" + filename)
        filenames.add(filename)
    policy = inventory.get("external_policy") or {}
    if policy.get("secret_values_forbidden") is not True or not isinstance(policy.get("forbidden_filename_tokens"), list):
        raise RecoveryError("RECOVERY_INVENTORY_EXTERNAL_POLICY_INVALID")
    return inventory


def deterministic_zip_timestamp(value: datetime) -> tuple[int, int, int, int, int, int]:
    return value.year, value.month, value.day, value.hour, value.minute, value.second - value.second % 2


def write_deterministic_zip(output: Path, members: dict[str, Path], timestamp: datetime) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    zip_time = deterministic_zip_timestamp(timestamp)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, zip_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            archive.writestr(info, members[name].read_bytes())


def external_filename_allowed(filename: str, inventory: dict[str, Any]) -> bool:
    lowered = filename.casefold()
    tokens = [str(token).casefold() for token in inventory["external_policy"]["forbidden_filename_tokens"]]
    return not any(token in lowered for token in tokens)


def stage_external_files(paths: list[Path], stage: Path, inventory: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    allowed = {safe_relative_path(str(item["filename"])) for item in inventory["external_exports"]}
    required: set[str] = set()
    for item in inventory["external_exports"]:
        if item.get("required") is True:
            required.add(safe_relative_path(str(item["filename"])))
    external_dir = stage / "external"
    external_dir.mkdir(parents=True, exist_ok=True)
    checksums: dict[str, str] = {}
    seen: set[str] = set()
    for source in paths:
        resolved = source.resolve()
        if not resolved.is_file():
            raise RecoveryError("EXTERNAL_EXPORT_NOT_FOUND:" + str(source))
        filename = safe_relative_path(resolved.name)
        if filename not in allowed:
            raise RecoveryError("EXTERNAL_EXPORT_UNDECLARED:" + filename)
        if not external_filename_allowed(filename, inventory):
            raise RecoveryError("EXTERNAL_SECRET_FILENAME_FORBIDDEN:" + filename)
        if filename in seen:
            raise RecoveryError("EXTERNAL_EXPORT_DUPLICATE:" + filename)
        seen.add(filename)
        target = external_dir / filename
        shutil.copyfile(resolved, target)
        checksums["external/" + filename] = sha256_file(target)
    missing = sorted(filename for filename in required if "external/" + filename not in checksums)
    return checksums, missing


def create_package(
    repository: Path,
    output: Path,
    inventory_path: Path,
    external_paths: list[Path],
    source_ref: str = "HEAD",
) -> dict[str, Any]:
    repository = repository.resolve()
    inventory_bytes = inventory_path.read_bytes()
    inventory = validate_inventory(json.loads(inventory_bytes.decode("utf-8")))
    if run_git(["status", "--porcelain"], repository):
        raise RecoveryError("RECOVERY_SOURCE_WORKTREE_DIRTY")
    commit = run_git(["rev-parse", f"{source_ref}^{{commit}}"], repository)
    branch = run_git(["branch", "--show-current"], repository)
    remote = run_git(["remote", "get-url", "origin"], repository)
    created = parse_timestamp(run_git(["show", "-s", "--format=%cI", commit], repository)).astimezone(timezone.utc)
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        source_archive = stage / "source.zip"
        run_git(["archive", "--format=zip", f"--output={source_archive}", commit], repository)
        inventory_copy = stage / "inventory.json"
        inventory_copy.write_bytes(inventory_bytes)
        external_checksums, missing_external = stage_external_files(external_paths, stage, inventory)
        manifest = {
            "schema": MANIFEST_SCHEMA,
            "status": "CREATED",
            "created_at": created.isoformat(),
            "repository": remote,
            "source_branch": branch,
            "source_commit": commit,
            "source_worktree_dirty": False,
            "inventory": {
                "path": "inventory.json",
                "sha256": sha256_bytes(inventory_bytes),
            },
            "source_archive": {
                "path": "source.zip",
                "sha256": sha256_file(source_archive),
            },
            "external_members": dict(sorted(external_checksums.items())),
            "external_state": "COMPLETE" if not missing_external else "BLOCKED",
            "missing_external_exports": missing_external,
        }
        manifest_path = stage / "manifest.json"
        manifest_path.write_bytes(canonical_json(manifest))
        members = {
            "inventory.json": inventory_copy,
            "manifest.json": manifest_path,
            "source.zip": source_archive,
        }
        for name in sorted(external_checksums):
            members[name] = stage / name
        write_deterministic_zip(output.resolve(), members, created)
    result = {
        "schema": PACKAGE_SCHEMA,
        "status": "CREATED",
        "package": str(output.resolve()),
        "package_sha256": sha256_file(output.resolve()),
        "source_commit": commit,
        "external_state": manifest["external_state"],
        "missing_external_exports": missing_external,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def read_zip_members(package: Path) -> tuple[zipfile.ZipFile, dict[str, bytes], list[str]]:
    archive = zipfile.ZipFile(package, "r")
    infos = archive.infolist()
    names = [info.filename for info in infos]
    failures: list[str] = []
    if len(names) != len(set(names)):
        failures.append("DUPLICATE_PACKAGE_MEMBER")
    for name in names:
        try:
            safe_relative_path(name)
        except RecoveryError:
            failures.append("UNSAFE_PACKAGE_MEMBER")
    if failures:
        archive.close()
        raise RecoveryError(",".join(sorted(set(failures))))
    return archive, {name: archive.read(name) for name in names}, names


def verify_package(package: Path) -> dict[str, Any]:
    package = package.resolve()
    failures: list[dict[str, Any]] = []
    try:
        archive, members, names = read_zip_members(package)
    except (zipfile.BadZipFile, RecoveryError) as error:
        return {
            "schema": VERIFY_SCHEMA,
            "status": "FAILED",
            "failure_code": "PACKAGE_UNREADABLE",
            "failures": [{"code": "PACKAGE_UNREADABLE", "detail": str(error)}],
        }
    finally:
        if "archive" in locals():
            archive.close()
    required_members = {"manifest.json", "inventory.json", "source.zip"}
    missing_members = sorted(required_members - set(names))
    for member in missing_members:
        failures.append({"code": "PACKAGE_MEMBER_MISSING", "member": member})
    manifest: dict[str, Any] = {}
    inventory: dict[str, Any] = {}
    if "manifest.json" in members:
        try:
            manifest = json.loads(members["manifest.json"].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            failures.append({"code": "MANIFEST_INVALID", "member": "manifest.json"})
    if "inventory.json" in members:
        try:
            inventory = validate_inventory(json.loads(members["inventory.json"].decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError, RecoveryError):
            failures.append({"code": "INVENTORY_INVALID", "member": "inventory.json"})
    if manifest.get("schema") != MANIFEST_SCHEMA:
        failures.append({"code": "MANIFEST_SCHEMA_INVALID"})
    for key in ("inventory", "source_archive"):
        descriptor = manifest.get(key)
        member = descriptor.get("path") if isinstance(descriptor, dict) else None
        expected = descriptor.get("sha256") if isinstance(descriptor, dict) else None
        if member not in members or not expected:
            failures.append({"code": "PACKAGE_DESCRIPTOR_INVALID", "descriptor": key})
        elif sha256_bytes(members[member]) != expected:
            failures.append({"code": "PACKAGE_CHECKSUM_MISMATCH", "member": member})
    expected_external = manifest.get("external_members") if isinstance(manifest.get("external_members"), dict) else {}
    actual_external = {name: sha256_bytes(data) for name, data in members.items() if name.startswith("external/")}
    if actual_external != expected_external:
        failures.append({"code": "EXTERNAL_CHECKSUM_SET_MISMATCH"})
    status = "VERIFIED" if not failures else "FAILED"
    return {
        "schema": VERIFY_SCHEMA,
        "status": status,
        "failure_code": failures[0]["code"] if failures else None,
        "package_sha256": sha256_file(package),
        "source_commit": manifest.get("source_commit"),
        "external_state": manifest.get("external_state"),
        "missing_external_exports": manifest.get("missing_external_exports", []),
        "failures": failures,
    }


def get_json_pointer(value: Any, pointer: str) -> Any:
    current = value
    for segment in pointer.split("."):
        if not isinstance(current, dict) or segment not in current:
            return None
        current = current[segment]
    return current


def extract_source_archive(source_archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(source_archive, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise RecoveryError("DUPLICATE_SOURCE_ARCHIVE_MEMBER")
        for name in names:
            safe_relative_path(name)
        root = destination.resolve()
        for info in infos:
            target = (destination / info.filename).resolve()
            if target != root and root not in target.parents:
                raise RecoveryError("UNSAFE_SOURCE_ARCHIVE_MEMBER:" + info.filename)
        archive.extractall(destination)


def inspect_restored_source(source_root: Path, inventory: dict[str, Any], external_root: Path) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    checked_paths: list[str] = []
    for component in inventory["required_components"]:
        for relative in component["paths"]:
            path = safe_relative_path(str(relative))
            checked_paths.append(path)
            if not (source_root / path).exists():
                failures.append({"code": "CRITICAL_PATH_MISSING", "component": component["id"], "path": path})
    for relative in inventory["required_json"]:
        path = safe_relative_path(str(relative))
        target = source_root / path
        if not target.is_file():
            failures.append({"code": "REQUIRED_JSON_MISSING", "path": path})
            continue
        try:
            json.loads(target.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append({"code": "REQUIRED_JSON_INVALID", "path": path, "detail": str(error)})
    for relative in inventory["required_python"]:
        path = safe_relative_path(str(relative))
        target = source_root / path
        if not target.is_file():
            failures.append({"code": "REQUIRED_PYTHON_MISSING", "path": path})
            continue
        try:
            compile(target.read_text(encoding="utf-8"), str(target), "exec")
        except (UnicodeDecodeError, SyntaxError) as error:
            failures.append({"code": "REQUIRED_PYTHON_INVALID", "path": path, "detail": str(error)})
    identity = inventory["control_plane_identity"]
    hub_path = source_root / safe_relative_path(str(identity["hub_path"]))
    if not hub_path.is_file():
        failures.append({"code": "CONTROL_PLANE_HUB_MISSING", "path": identity["hub_path"]})
    else:
        actual_blob = git_blob_sha(hub_path)
        declared: list[dict[str, str | None]] = []
        for relative, pointers in identity["sha_pointers"].items():
            target = source_root / safe_relative_path(str(relative))
            if not target.is_file():
                failures.append({"code": "CONTROL_PLANE_DECLARATION_MISSING", "path": str(relative)})
                continue
            try:
                document = json.loads(target.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                failures.append({"code": "CONTROL_PLANE_DECLARATION_INVALID", "path": str(relative), "detail": str(error)})
                continue
            for pointer in pointers:
                value = get_json_pointer(document, str(pointer))
                declared.append({"path": str(relative), "pointer": str(pointer), "value": None if value is None else str(value)})
        if declared and any(item["value"] != actual_blob for item in declared):
            failures.append(
                {
                    "code": "CONTROL_PLANE_SOURCE_DIVERGENCE",
                    "actual_hub_blob": actual_blob,
                    "declared": declared,
                }
            )
    for export in inventory["external_exports"]:
        if export.get("required") is not True:
            continue
        filename = safe_relative_path(str(export["filename"]))
        if not (external_root / filename).is_file():
            failures.append({"code": "EXTERNAL_STATE_MISSING", "export_id": export["id"], "filename": filename})
    status = "VERIFIED" if not failures else "BLOCKED"
    return {
        "schema": RESTORE_SCHEMA,
        "status": status,
        "disaster_recovery_ready": not failures,
        "failure_code": failures[0]["code"] if failures else None,
        "checked_paths": sorted(set(checked_paths)),
        "failures": failures,
    }


def restore_package(package: Path, destination: Path, require_ready: bool = False) -> dict[str, Any]:
    package = package.resolve()
    verification = verify_package(package)
    if verification["status"] != "VERIFIED":
        report = {
            "schema": RESTORE_SCHEMA,
            "status": "BLOCKED",
            "disaster_recovery_ready": False,
            "failure_code": verification["failure_code"],
            "package_verification": verification,
            "failures": verification["failures"],
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        return report
    destination = destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise RecoveryError("RESTORE_DESTINATION_NOT_EMPTY")
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        with zipfile.ZipFile(package, "r") as archive:
            archive.extractall(stage)
        extract_source_archive(stage / "source.zip", stage / "source")
        source_root = destination / "source"
        external_root = destination / "external"
        shutil.copytree(stage / "source", source_root)
        if (stage / "external").exists():
            shutil.copytree(stage / "external", external_root)
        else:
            external_root.mkdir(parents=True, exist_ok=True)
        inventory = json.loads((stage / "inventory.json").read_text(encoding="utf-8"))
        inspection = inspect_restored_source(source_root, validate_inventory(inventory), external_root)
    report = {
        **inspection,
        "package": str(package),
        "package_sha256": verification["package_sha256"],
        "source_commit": verification["source_commit"],
        "restored_source": str(source_root),
        "package_verification": verification,
    }
    destination.joinpath("restore-report.json").write_bytes(canonical_json(report))
    print(json.dumps(report, indent=2, sort_keys=True))
    if require_ready and not report["disaster_recovery_ready"]:
        raise RecoveryExit(2)
    return report


class RecoveryExit(RuntimeError):
    def __init__(self, code: int):
        super().__init__(f"RECOVERY_EXIT:{code}")
        self.code = code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create")
    create.add_argument("--repository", default=str(Path(__file__).resolve().parents[1]))
    create.add_argument("--inventory", default=str(Path(__file__).resolve().with_name("naya_recovery_package_inventory.json")))
    create.add_argument("--output", required=True)
    create.add_argument("--source-ref", default="HEAD")
    create.add_argument("--external", action="append", default=[])
    verify = subparsers.add_parser("verify")
    verify.add_argument("--package", required=True)
    restore = subparsers.add_parser("restore")
    restore.add_argument("--package", required=True)
    restore.add_argument("--destination", required=True)
    restore.add_argument("--require-ready", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "create":
            create_package(Path(args.repository), Path(args.output), Path(args.inventory), [Path(value) for value in args.external], args.source_ref)
            return 0
        if args.command == "verify":
            report = verify_package(Path(args.package))
            print(json.dumps(report, indent=2, sort_keys=True))
            return 0 if report["status"] == "VERIFIED" else 1
        if args.command == "restore":
            restore_package(Path(args.package), Path(args.destination), args.require_ready)
            return 0
        raise RecoveryError("UNKNOWN_RECOVERY_COMMAND")
    except RecoveryExit as error:
        return error.code
    except RecoveryError as error:
        print(json.dumps({"schema": PACKAGE_SCHEMA, "status": "FAILED", "error": str(error)}, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
