from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import zipfile
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import naya_recovery_package as recovery

REBUILD_SCHEMA = "naya-clean-rebuild/v1"
DERIVED_OUTPUTS = (
    ".naya/memory/events/INDEX.json",
    ".naya/memory/VALIDATION-REPORT.json",
    ".naya/control-plane/RELATIONSHIP-INDEX.json",
    "SUPERBRAIN/NAYA-ACTIVITY/RELATIONSHIP-INDEX.md",
    "NAYANET/HUB/public/intelligence/pis-feed.json",
)
DETERMINISTIC_OUTPUTS = (
    ".naya/memory/events/INDEX.json",
    ".naya/memory/VALIDATION-REPORT.json",
    ".naya/control-plane/RELATIONSHIP-INDEX.json",
    "SUPERBRAIN/NAYA-ACTIVITY/RELATIONSHIP-INDEX.md",
)
HUB_PROJECTION_INPUTS = (
    "NAYANET/HUB/index.html",
    "NAYANET/HUB/public/assistant-runtime.js",
    "smart-feed.js",
    "hub-completeness.js",
    "NAYANET/HUB/intelligence-surfaces-runtime.js",
)
PIS_OUTPUT = "NAYANET/HUB/public/intelligence/pis-feed.json"
PIS_BUILDERS = (
    "scripts/build-primary-intelligence-feed.py",
    "scripts/build-smart-feed-projection.py",
)


class RebuildError(RuntimeError):
    pass


class RebuildExit(RuntimeError):
    def __init__(self, code: int):
        super().__init__(f"REBUILD_EXIT:{code}")
        self.code = code


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return recovery.sha256_file(path)


def run_checked(command: list[str], cwd: Path, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, env=env)
    if check and result.returncode:
        raise RebuildError("COMMAND_FAILED:" + " ".join(command) + "\n" + result.stdout + "\n" + result.stderr)
    return result


def package_created_at(package: Path) -> datetime:
    with zipfile.ZipFile(package, "r") as archive:
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
    return datetime.fromisoformat(str(manifest["created_at"]).replace("Z", "+00:00"))


def remove_derived_outputs(source: Path) -> list[str]:
    removed = []
    for relative in DERIVED_OUTPUTS:
        target = source / relative
        if target.exists():
            target.unlink()
            removed.append(relative)
    return removed


def rebuild_deterministic(source: Path, output: Path, source_date_epoch: int) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    run_checked([sys.executable, ".naya/memory/smart_notes_v3.py", "index"], source)
    validation = run_checked([sys.executable, ".naya/memory/smart_notes_v3.py", "validate"], source, check=False)
    current_truth = output / "current-truth.json"
    run_checked(
        [sys.executable, ".naya/runtime/project_intelligence_reconstruction.py", "--project", "NayaNET", "--out", str(current_truth)],
        source,
    )
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = str(source_date_epoch)
    run_checked([sys.executable, "scripts/build_repository_relationship_index.py"], source, env)
    files = {relative: sha256_file(source / relative) for relative in DETERMINISTIC_OUTPUTS}
    files["current-truth.json"] = sha256_file(current_truth)
    return {
        "files": files,
        "current_truth": json.loads(current_truth.read_text(encoding="utf-8")),
        "smart_notes_validation_exit_code": validation.returncode,
    }


def normalize_pis(data: bytes) -> bytes:
    payload = json.loads(data.decode("utf-8"))
    payload.pop("generated_at", None)
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def run_pis_builder(source: Path, script: str, destination: Path) -> list[dict[str, Any]]:
    output = source / PIS_OUTPUT
    records = []
    for index in range(2):
        if output.exists():
            output.unlink()
        run_checked([sys.executable, script], source)
        if not output.is_file():
            raise RebuildError("PIS_OUTPUT_MISSING:" + script)
        data = output.read_bytes()
        target = destination / f"{Path(script).stem}-{index + 1}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append(
            {
                "run": index + 1,
                "sha256": sha256_bytes(data),
                "normalized_sha256": sha256_bytes(normalize_pis(data)),
                "generated_at": json.loads(data.decode("utf-8")).get("generated_at"),
                "artifact": str(target),
            }
        )
        if index == 0:
            time.sleep(1.1)
    return records


def discover_pis_producers(source: Path) -> list[str]:
    producers = []
    for path in sorted((source / "scripts").glob("*.py")):
        if path.name == "naya_clean_rebuild.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        assigns_output = re.search(r"(?m)^(?:OUT|OUTPUT)\s*=.*pis-feed\.json", text)
        writes_output = re.search(r"\b(?:OUT|OUTPUT|output)\.write_(?:text|bytes)\s*\(", text)
        if assigns_output and writes_output:
            producers.append(path.relative_to(source).as_posix())
    return producers


def compare_deterministic(left: dict[str, Any], right: dict[str, Any]) -> tuple[bool, list[dict[str, str]]]:
    differences = []
    for name in sorted(set(left["files"]) | set(right["files"])):
        left_hash = left["files"].get(name)
        right_hash = right["files"].get(name)
        if left_hash != right_hash:
            differences.append({"output": name, "left": left_hash or "MISSING", "right": right_hash or "MISSING"})
    return not differences, differences


def verify_clean_rebuild(package: Path, workdir: Path) -> dict[str, Any]:
    package = package.resolve()
    workdir = workdir.resolve()
    if workdir.exists() and any(workdir.iterdir()):
        raise RebuildError("REBUILD_WORKDIR_NOT_EMPTY")
    workdir.mkdir(parents=True, exist_ok=True)
    verification = recovery.verify_package(package)
    if verification["status"] != "VERIFIED":
        raise RebuildError("RECOVERY_PACKAGE_INTEGRITY_FAILED")
    created = package_created_at(package)
    source_date_epoch = int(created.timestamp())
    restored = {}
    for label in ("A", "B"):
        destination = workdir / f"restore-{label}"
        with redirect_stdout(StringIO()):
            report = recovery.restore_package(package, destination)
        restored[label] = report
        source = destination / "source"
        removed = remove_derived_outputs(source)
        if label == "A":
            first_removed = removed
        else:
            second_removed = removed
    source_a = workdir / "restore-A/source"
    source_b = workdir / "restore-B/source"
    rebuilt_a = rebuild_deterministic(source_a, workdir / "rebuild-A", source_date_epoch)
    rebuilt_b = rebuild_deterministic(source_b, workdir / "rebuild-B", source_date_epoch)
    deterministic, differences = compare_deterministic(rebuilt_a, rebuilt_b)
    producers = discover_pis_producers(source_a)
    pis_primary = run_pis_builder(source_a, PIS_BUILDERS[0], workdir / "pis-primary")
    pis_smart_feed = run_pis_builder(source_b, PIS_BUILDERS[1], workdir / "pis-smart-feed")
    primary_raw_drift = pis_primary[0]["sha256"] != pis_primary[1]["sha256"]
    smart_feed_raw_drift = pis_smart_feed[0]["sha256"] != pis_smart_feed[1]["sha256"]
    primary_normalized_stable = pis_primary[0]["normalized_sha256"] == pis_primary[1]["normalized_sha256"]
    smart_feed_normalized_stable = pis_smart_feed[0]["normalized_sha256"] == pis_smart_feed[1]["normalized_sha256"]
    producer_content_match = pis_primary[0]["normalized_sha256"] == pis_smart_feed[0]["normalized_sha256"]
    hub_inputs = {relative: (source_a / relative).is_file() for relative in HUB_PROJECTION_INPUTS}
    current_truth = rebuilt_a["current_truth"]
    validation_failures = [
        exit_code
        for exit_code in (
            rebuilt_a["smart_notes_validation_exit_code"],
            rebuilt_b["smart_notes_validation_exit_code"],
        )
        if exit_code != 0
    ]
    findings = []
    if validation_failures:
        findings.append({"code": "SMART_NOTES_VALIDATION_FAILED", "exit_codes": validation_failures})
    if not deterministic:
        findings.append({"code": "DETERMINISTIC_OUTPUT_MISMATCH", "differences": differences})
    if len(producers) != 1:
        findings.append({"code": "DUPLICATE_PIS_PRODUCERS", "producers": producers})
    if primary_raw_drift or smart_feed_raw_drift:
        findings.append({"code": "PIS_TIMESTAMP_DRIFT", "primary": primary_raw_drift, "smart_feed": smart_feed_raw_drift})
    if not primary_normalized_stable or not smart_feed_normalized_stable:
        findings.append({
            "code": "PIS_SELF_CONTENT_DRIFT",
            "primary_normalized_stable": primary_normalized_stable,
            "smart_feed_normalized_stable": smart_feed_normalized_stable,
            "primary_normalized_sha256": [pis_primary[0]["normalized_sha256"], pis_primary[1]["normalized_sha256"]],
            "smart_feed_normalized_sha256": [pis_smart_feed[0]["normalized_sha256"], pis_smart_feed[1]["normalized_sha256"]],
        })
    if not producer_content_match:
        findings.append({"code": "PIS_PRODUCER_CONTENT_CONFLICT", "primary_normalized_sha256": pis_primary[0]["normalized_sha256"], "smart_feed_normalized_sha256": pis_smart_feed[0]["normalized_sha256"]})
    if int(current_truth.get("counts", {}).get("current") or 0) == 0:
        findings.append({"code": "CURRENT_TRUTH_EMPTY", "counts": current_truth.get("counts", {})})
    if any(report.get("external_status") != "VERIFIED" for report in restored.values()):
        findings.append({"code": "EXTERNAL_DATABASE_RESTORE_UNAVAILABLE"})
    if not all(hub_inputs.values()):
        findings.append({"code": "HUB_PROJECTION_INPUT_MISSING", "inputs": hub_inputs})
    report = {
        "schema": REBUILD_SCHEMA,
        "status": "VERIFIED" if deterministic and not findings else "BLOCKED",
        "local_deterministic_rebuild": "VERIFIED" if deterministic else "FAILED",
        "deterministic_clean_rebuild_ready": not findings,
        "source_commit": verification["source_commit"],
        "package_sha256": verification["package_sha256"],
        "source_date_epoch": source_date_epoch,
        "removed_derived_outputs": {"A": first_removed, "B": second_removed},
        "deterministic_outputs": {"A": rebuilt_a["files"], "B": rebuilt_b["files"]},
        "current_truth_counts": current_truth.get("counts", {}),
        "smart_notes_validation_exit_codes": {
            "A": rebuilt_a["smart_notes_validation_exit_code"],
            "B": rebuilt_b["smart_notes_validation_exit_code"],
        },
        "pis_producers": producers,
        "pis_runs": {"primary": pis_primary, "smart_feed": pis_smart_feed},
        "pis_normalized_content_match": producer_content_match,
        "pis_normalized_self_stable": {
            "primary": primary_normalized_stable,
            "smart_feed": smart_feed_normalized_stable,
        },
        "hub_projection_inputs": hub_inputs,
        "external_database_restore": "BLOCKED",
        "findings": findings,
        "truth_boundary": "Local deterministic rebuild is proven when deterministic=true. Full System 52 remains blocked by unresolved canonical projection producers, empty current truth, and unavailable external database state.",
    }
    (workdir / "clean-rebuild-report.json").write_bytes(recovery.canonical_json(report))
    print(json.dumps(report, indent=2, sort_keys=True))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True)
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    try:
        report = verify_clean_rebuild(Path(args.package), Path(args.workdir))
        if args.require_ready and not report["deterministic_clean_rebuild_ready"]:
            raise RebuildExit(2)
        return 0
    except RebuildExit as error:
        return error.code
    except (RebuildError, recovery.RecoveryError) as error:
        print(json.dumps({"schema": REBUILD_SCHEMA, "status": "FAILED", "error": str(error)}, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
