#!/usr/bin/env python3
"""Production-grade Cloudflare Worker adapter for governed execution.

Authority remains outside this adapter. The adapter is only the concrete side-
effect implementation consumed by model_tool_gateway.execute_authorized() and
the independent portable runner after its own portable-boundary verification.

Preview means a real Cloudflare version upload with no traffic promotion.
Production means the canonical Wrangler deploy command.
"""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from universal_execution_gate import _execution_binding_hash
from release_execution_boundary import deploy_target

WORKER = "sparkling-shape-7ae5"
ACCOUNT_ID = "b5e2a51b3e883f7722287c5f51b1196b"
REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
HUB_RELATIVE = Path("NAYANET") / "HUB"
WRANGLER_CONFIG = "wrangler.jsonc"
WRANGLER_VERSION = "4"

_VERSION_RE = re.compile(
    r"(?:Version ID|version_id|versionId)\s*[:=]\s*([0-9a-fA-F-]{20,})"
)


@dataclass(frozen=True)
class CloudflareExecutionResult:
    execution_state: str
    execution_id: str
    action: str
    observed_output: str
    result: str
    commit_sha: str
    action_ref: str
    outcome_ref: str
    environment: str
    source: str
    external_version_id: str
    external_worker: str
    external_account_id: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "execution_state": self.execution_state,
            "execution_id": self.execution_id,
            "action": self.action,
            "observed_output": self.observed_output,
            "result": self.result,
            "commit_sha": self.commit_sha,
            "action_ref": self.action_ref,
            "outcome_ref": self.outcome_ref,
            "environment": self.environment,
            "source": self.source,
            "external_version_id": self.external_version_id,
            "external_worker": self.external_worker,
            "external_account_id": self.external_account_id,
        }


class CloudflareWorkerProductionAdapter:
    """Concrete Cloudflare Workers side-effect adapter."""

    def __init__(self, source_dir: str | Path | None = None) -> None:
        self.source_dir = Path(source_dir or Path(__file__).resolve().parents[2]).resolve()

    @property
    def hub_dir(self) -> Path:
        return self.source_dir / HUB_RELATIVE

    def _current_commit(self) -> str:
        proc = subprocess.run(
            ["git", "-C", str(self.source_dir), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()

    def _check_target(self, action: Mapping[str, Any]) -> tuple[str, str]:
        env = str(action.get("environment") or "")
        worker = str(action.get("worker_name") or WORKER)
        repository = str(action.get("repository") or REPOSITORY)
        commit_sha = str(action.get("commit_sha") or action.get("protected_baseline") or "")
        expected = deploy_target(
            deployment_surface="cloudflare",
            environment=env,
            repository=repository,
            commit_sha=commit_sha,
            worker_name=worker,
        )
        if str(action.get("target")) != expected:
            raise AssertionError("Cloudflare adapter target does not match the canonical deploy target")
        if worker != WORKER:
            raise AssertionError("Cloudflare adapter is bound to the canonical worker only")
        if repository != REPOSITORY:
            raise AssertionError("Cloudflare adapter is bound to the canonical repository only")
        return env, commit_sha

    def _check_config(self) -> None:
        config_path = self.hub_dir / WRANGLER_CONFIG
        if not config_path.is_file():
            raise AssertionError("canonical Cloudflare wrangler.jsonc is missing")
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if config.get("name") != WORKER:
            raise AssertionError("wrangler worker name does not match the governed target")
        if config.get("account_id") != ACCOUNT_ID:
            raise AssertionError("wrangler account id does not match the governed target")
        if not (self.hub_dir / "dist").is_dir():
            raise AssertionError("canonical Hub dist artifact is missing; build must complete before execution")

    def execute(self, action: dict[str, Any]) -> Mapping[str, Any]:
        env, commit_sha = self._check_target(action)
        actual_commit = self._current_commit()
        if actual_commit != commit_sha:
            raise AssertionError(
                f"source checkout {actual_commit!r} does not match authorization commit {commit_sha!r}"
            )
        self._check_config()

        action_id = str(action["action_id"])
        tag = re.sub(r"[^A-Za-z0-9._-]", "-", action_id)[:80]
        message = f"NayaPOWER governed Cloudflare external execution {action_id}"

        if env == "preview":
            command = [
                "npx", "--yes", f"wrangler@{WRANGLER_VERSION}",
                "versions", "upload",
                "--config", WRANGLER_CONFIG,
                "--name", WORKER,
                "--tag", tag,
                "--message", message,
            ]
        elif env == "production":
            command = [
                "npx", "--yes", f"wrangler@{WRANGLER_VERSION}",
                "deploy",
                "--config", WRANGLER_CONFIG,
            ]
        else:
            raise AssertionError("Cloudflare adapter environment must be preview or production")

        proc = subprocess.run(
            command,
            cwd=str(self.hub_dir),
            capture_output=True,
            text=True,
        )
        output = ((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")).strip()
        if proc.returncode != 0:
            raise RuntimeError(f"Cloudflare Wrangler execution failed ({proc.returncode}): {output[-12000:]}")

        version_id = ""
        match = _VERSION_RE.search(output)
        if match:
            version_id = match.group(1)

        return CloudflareExecutionResult(
            execution_state="COMPLETED",
            execution_id=action_id,
            action=str(action.get("action_type") or "deploy_public_runtime"),
            observed_output=output[-12000:] or "Wrangler completed without textual output",
            result="PASS",
            commit_sha=commit_sha,
            action_ref=f"cloudflare:{WORKER}:{env}:{action_id}",
            outcome_ref=f"cloudflare-outcome:{action_id}",
            environment=env,
            source="cloudflare_production_adapter",
            external_version_id=version_id,
            external_worker=WORKER,
            external_account_id=ACCOUNT_ID,
        ).as_dict()


def execute_cloudflare_authorized(
    action: dict[str, Any],
    *,
    execution_authorization: Any,
    identity_envelope: Mapping[str, Any],
    gate: Any = None,
    preflight: Any = None,
    now: str | None = None,
    source_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Bind the concrete Cloudflare adapter to the governed execute_authorized seam."""
    from model_tool_gateway import execute_authorized

    adapter = CloudflareWorkerProductionAdapter(source_dir=source_dir)
    return execute_authorized(
        action,
        execution_authorization=execution_authorization,
        identity_envelope=identity_envelope,
        executor=adapter.execute,
        gate=gate,
        preflight=preflight,
        now=now,
    )


__all__ = [
    "WORKER",
    "ACCOUNT_ID",
    "REPOSITORY",
    "CloudflareExecutionResult",
    "CloudflareWorkerProductionAdapter",
    "execute_cloudflare_authorized",
]
