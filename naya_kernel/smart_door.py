"""Smart Door integration layer (CANDIDATE — NOT RATIFIED, NOT MERGED).

This module is the binding between the canonical Smart Door registry and
the kernel's ACT node. It is a PROJECTION, not a parallel registry:

- Capability declarations (what the tool is, its bounds, its authority
  action) live ONLY in
  ``BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json``.
- This module reads that file and projects one door operation into the
  ``tool_registry`` entry shape ACT's admission (§4.3) expects.
- ACT-side treatment (authority_class, idempotency, retry policy,
  evidence_capture, required_authority basis kind) is ACT's own
  configuration — declared here next to the projection, never presented
  as a capability declaration.

Per the Smart Door contract
(``BRAIN/10-INTERFACES/0001-SMART-DOOR-CONTRACT-V1.md``): doors expose
what Naya can do; LAW decides what Naya may do; ACT does it; VERIFY
checks what happened. Nothing here grants authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, Tuple

from naya_kernel.nodes import act_node

# ---------------------------------------------------------------------------
# Registry loading / operation resolution
# ---------------------------------------------------------------------------

_DEFAULT_REGISTRY = (
    Path(__file__).resolve().parents[1]
    / "BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json"
)

REGISTRY_SOURCE_OF_TRUTH = (
    "BRAIN/10-INTERFACES/0001-SMART-DOOR-CONTRACT-V1.json"
)


def load_registry(path: str | Path | None = None) -> Dict[str, Any]:
    """Parse the canonical Smart Door registry. Raises on any problem."""
    p = Path(path) if path else _DEFAULT_REGISTRY
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("source_of_truth") != REGISTRY_SOURCE_OF_TRUTH:
        raise ValueError(
            "smart-door registry source_of_truth mismatch: %r"
            % data.get("source_of_truth")
        )
    return data


def find_operation(
    registry: Dict[str, Any], door_id: str, operation: str
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Resolve exactly one (door, operation). Raises if not exactly one."""
    doors = [d for d in registry.get("doors", []) if d.get("door_id") == door_id]
    if len(doors) != 1:
        raise KeyError("door %r: found %d matches" % (door_id, len(doors)))
    ops = [
        o
        for o in doors[0].get("operations", [])
        if o.get("operation") == operation
    ]
    if len(ops) != 1:
        raise KeyError(
            "operation %r on door %r: found %d matches"
            % (operation, door_id, len(ops))
        )
    return doors[0], ops[0]


# ---------------------------------------------------------------------------
# Projection: registry declaration -> ACT tool_registry entry
# ---------------------------------------------------------------------------

# ACT-side treatment for the Demo-1 staging write. These describe how ACT
# admits and invokes the tool — they are ACT configuration, not capability
# declarations (those live in the registry JSON).
_STAGING_ACT_PROFILE: Dict[str, Any] = {
    "authority_class": act_node.TOOL_CLASS_WRITE_SCOPED,
    "idempotent": True,
    "max_timeout_ms": 5000,
    "retry_policy": {"attempts": 0, "backoff": "none"},
    # The registry's "LAW decision per operation" is satisfied, for the
    # director-run demo, by a LAW-shaped receipt carrying a director_order
    # basis — the kernel's LAW gate authorizes the demo decision.
    "required_authority": "director_order",
    "compensating_tool": None,
    "evidence_capture": "return_value",
}


def project_act_tool_entry(
    door: Dict[str, Any],
    operation: Dict[str, Any],
    registry_version: str = "1.0",
    act_profile: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Project one registry operation into ACT's tool_registry entry shape.

    Every capability-describing field is read from the registry arguments;
    nothing about the capability is invented here. Raises KeyError if the
    operation declaration lacks a required bound.
    """
    profile = dict(act_profile) if act_profile else dict(_STAGING_ACT_PROFILE)
    params = operation.get("params") or {}
    for field in ("max_bytes", "overwrite"):
        if field not in params:
            raise KeyError(
                "operation %r declares no params.%s bound"
                % (operation.get("operation"), field)
            )
    entry = {
        "tool_id": operation["operation"],
        "version": registry_version,
        # --- from the canonical registry declaration ---
        "authority_action": operation["authority_action"],
        "target": operation.get("target"),
        "max_bytes": params["max_bytes"],
        "overwrite": params["overwrite"],
        "verification_required": bool(operation.get("verification_required")),
        "door_id": door["door_id"],
        "registry_status": door.get("status"),
    }
    entry.update(profile)
    return entry


def staging_tool_registry(
    registry_path: str | Path | None = None,
    door_id: str = "DOOR-LOCAL-STAGING",
    operation: str = "staging.write_file",
) -> Dict[str, Dict[str, Any]]:
    """Build ACT's tool_registry for the staging write from the canonical
    registry. The registry file remains the single source of truth."""
    reg = load_registry(registry_path)
    door, op = find_operation(reg, door_id, operation)
    entry = project_act_tool_entry(door, op, registry_version=reg.get("version", "1.0"))
    return {entry["tool_id"]: entry}


# ---------------------------------------------------------------------------
# The real bounded executor: staging.write_file
# ---------------------------------------------------------------------------

_TOOL_ID = "staging.write_file"
_FILENAME_RE = re.compile(r"^sn-candidate-[A-Za-z0-9][A-Za-z0-9_-]*\.md$")
_STAGING_DIR = "demo-staging"


def _err(detail: str) -> Dict[str, Any]:
    return {
        "status": "error",
        "effects": "",
        "error_class": act_node.ERROR_PERMANENT,
        "error_detail": detail,
    }


def make_staging_executor(base_dir: str | Path) -> Callable[[str, Dict[str, Any]], Dict[str, Any]]:
    """Build the bounded staging.write_file executor for one sandbox root.

    Bounds (mirroring the canonical registry declaration):
    - writes only inside ``<base_dir>/demo-staging/``;
    - filename must match ``sn-candidate-*.md`` (no separators, no ``..``);
    - content at most 64 KiB;
    - never overwrites: identical content is an idempotent no-op,
      conflicting content is refused;
    - every parameter is validated BEFORE any filesystem mutation.

    Returns an ``executor(tool_id, params)`` callable matching ACT's seam.
    Cleanup/rollback: the operation is a single file write; rollback is
    deleting the file. No compensating tool is registered (declared None).
    """

    def executor(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_id != _TOOL_ID:
            return _err("executor serves only %r, got %r" % (_TOOL_ID, tool_id))
        if not isinstance(params, dict):
            return _err("params must be an object")
        filename = params.get("filename")
        content = params.get("content")
        if not isinstance(filename, str) or not _FILENAME_RE.match(filename):
            return _err(
                "filename must match sn-candidate-*.md with no path separators; "
                "got %r" % (filename,)
            )
        if not isinstance(content, str):
            return _err("content must be a string")
        data = content.encode("utf-8")
        if len(data) > 65536:
            return _err(
                "content exceeds 65536 bytes (%d)" % len(data)
            )

        root = Path(base_dir) / _STAGING_DIR
        try:
            root.mkdir(parents=True, exist_ok=True)
            target = root / filename
            # Defense in depth: the regex already forbids separators, but
            # never trust a path you did not fully construct.
            if target.resolve().parent != root.resolve():
                return _err("resolved path escapes the staging root")
            digest = hashlib.sha256(data).hexdigest()
            if target.exists():
                existing = target.read_bytes()
                if hashlib.sha256(existing).hexdigest() == digest:
                    return {
                        "status": "ok",
                        "effects": "already_present demo-staging/%s "
                        "(%d bytes, sha256:%s) — no second write"
                        % (filename, len(data), digest),
                        "error_class": None,
                    }
                return _err(
                    "refuses to overwrite demo-staging/%s "
                    "(existing content differs)" % filename
                )
            target.write_bytes(data)
        except OSError as exc:
            return _err("filesystem error: %s" % exc)

        return {
            "status": "ok",
            "effects": "wrote demo-staging/%s (%d bytes, sha256:%s)"
            % (filename, len(data), digest),
            "error_class": None,
        }

    return executor
