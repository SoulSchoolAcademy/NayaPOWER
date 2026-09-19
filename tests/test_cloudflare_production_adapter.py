#!/usr/bin/env python3
"""Closure tests for the concrete Cloudflare production adapter."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ADAPTER = load("cloudflare_adapter_test", ROOT / ".naya/runtime/cloudflare_production_adapter.py")


def test_preview_adapter_binds_exact_target_and_commit():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        hub = root / "NAYANET" / "HUB"
        hub.mkdir(parents=True)
        (hub / "dist").mkdir()
        (hub / "wrangler.jsonc").write_text(json.dumps({
            "name": ADAPTER.WORKER,
            "account_id": ADAPTER.ACCOUNT_ID,
            "assets": {"directory": "./dist"},
            "main": "worker.js",
        }), encoding="utf-8")
        proc = subprocess.run(["git", "-C", str(root), "init"], capture_output=True, text=True)
        assert proc.returncode == 0
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "test"], check=True)
        (root / "sentinel").write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True)
        sha = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        target = ADAPTER.deploy_target(
            deployment_surface="cloudflare",
            environment="preview",
            repository=ADAPTER.REPOSITORY,
            commit_sha=sha,
            worker_name=ADAPTER.WORKER,
        )
        action = {
            "action_id": "CF-TEST-001",
            "action_type": "deploy_public_runtime",
            "target": target,
            "environment": "preview",
            "worker_name": ADAPTER.WORKER,
            "repository": ADAPTER.REPOSITORY,
            "commit_sha": sha,
        }
        completed = subprocess.CompletedProcess(["npx"], 0, "Version ID: abcdef-123456\n", "")
        with patch.object(ADAPTER.subprocess, "run", side_effect=[
            subprocess.CompletedProcess(["git"], 0, sha + "\n", ""),
            completed,
        ]) as mocked:
            result = ADAPTER.CloudflareWorkerProductionAdapter(root).execute(action)
        assert result["execution_state"] == "COMPLETED"
        assert result["result"] == "PASS"
        assert result["external_version_id"] == "abcdef-123456"
        assert mocked.call_count == 2


def test_target_mismatch_refuses_before_external_process():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        hub = root / "NAYANET" / "HUB"
        hub.mkdir(parents=True)
        (hub / "dist").mkdir()
        (hub / "wrangler.jsonc").write_text(json.dumps({"name": ADAPTER.WORKER, "account_id": ADAPTER.ACCOUNT_ID}), encoding="utf-8")
        action = {
            "action_id": "CF-TEST-002",
            "target": "cloudflare-runtime:attacker:environment:preview:repository:SoulSchoolAcademy/NayaPOWER:commit:bad",
            "environment": "preview",
            "worker_name": ADAPTER.WORKER,
            "repository": ADAPTER.REPOSITORY,
            "commit_sha": "bad",
        }
        with patch.object(ADAPTER.subprocess, "run") as mocked:
            try:
                ADAPTER.CloudflareWorkerProductionAdapter(root).execute(action)
            except Exception:
                pass
            else:
                raise AssertionError("expected target mismatch refusal")
        mocked.assert_not_called()


if __name__ == "__main__":
    test_preview_adapter_binds_exact_target_and_commit()
    test_target_mismatch_refuses_before_external_process()
    print("CLOUDFLARE_ADAPTER_TESTS=PASS")
