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
import os
import re
import secrets
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


def find_operation_any_door(
    registry: Dict[str, Any], operation: str
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Resolve an operation name across ALL doors. Raises KeyError unless
    exactly one door declares it. Used by verifiers that must bind the
    receipt's actual tool instead of assuming a hardcoded door."""
    matches = []
    for door in registry.get("doors", []):
        for op in door.get("operations", []):
            if op.get("operation") == operation:
                matches.append((door, op))
    if len(matches) != 1:
        raise KeyError(
            "operation %r: found %d declarations across all doors"
            % (operation, len(matches))
        )
    return matches[0]


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
    # The registry's "LAW decision per operation" is satisfied by a real
    # LawNode.gate() evaluation: scripts/demo1/law_authorize.py builds the
    # proposal from the demo intent + the director-transcribed grant
    # (demo_grant.json) and only an ADMISSIBLE envelope reaches ACT.
    # ActNode._admit re-validates the grant and envelope at invocation time.
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
_DOOR_ID = "DOOR-LOCAL-STAGING"


def _compile_filename_pattern(pattern: Any) -> "re.Pattern[str]":
    """Translate the registry's filename glob into an admission regex.

    The declaration's ``*`` becomes a no-separator token. Any pattern
    that could admit a path separator or parent traversal is rejected:
    the executor fails closed when the declaration is incompatible with
    safe enforcement instead of silently widening it.
    """
    if not isinstance(pattern, str) or "*" not in pattern:
        raise ValueError(
            "executor refuses: declaration filename pattern %r is not a "
            "bounded glob" % (pattern,))
    if "/" in pattern or "\\" in pattern or ".." in pattern:
        raise ValueError(
            "executor refuses: declaration filename pattern %r admits "
            "path traversal" % (pattern,))
    rx = "^" + re.escape(pattern).replace(r"\*", r"[A-Za-z0-9][A-Za-z0-9_-]*") + "$"
    return re.compile(rx)


def _resolve_bounds(operation: Dict[str, Any]) -> Dict[str, Any]:
    """Read the executor's enforcement bounds from the canonical
    declaration. Raises ValueError when the declaration is missing a
    bound or is incompatible with safe enforcement — a profile may not
    override a canonical restriction, and a loosened declaration fails
    closed instead of widening the runtime."""
    params = operation.get("params") or {}
    max_bytes = params.get("max_bytes")
    if not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ValueError(
            "executor refuses: declaration of %r lacks a usable "
            "params.max_bytes bound" % (operation.get("operation"),))
    target = operation.get("target") or ""
    dirname = target.strip().rstrip("/")
    if (not dirname or "/" in dirname or "\\" in dirname or dirname in
            (".", "..") or dirname.startswith(".")):
        raise ValueError(
            "executor refuses: declaration target %r is not a single "
            "contained directory name" % (target,))
    if params.get("overwrite") is not False:
        raise ValueError(
            "executor refuses: declaration overwrite=%r is incompatible "
            "with the no-clobber safety invariant" % (params.get("overwrite"),))
    return {
        "max_bytes": max_bytes,
        "staging_dirname": dirname,
        "filename_re": _compile_filename_pattern(params.get("filename")),
        "filename_pattern": params.get("filename"),
    }


def _err(detail: str) -> Dict[str, Any]:
    return {
        "status": "error",
        "effects": "",
        "error_class": act_node.ERROR_PERMANENT,
        "error_detail": detail,
    }


def _needs_nofollow() -> None:
    # The containment and no-clobber guarantees below rest on O_NOFOLLOW
    # (refuse symlinked staging dir / target) and O_EXCL-via-link (atomic
    # no-clobber). POSIX-only; fail loudly instead of silently weakening.
    if not hasattr(os, "O_NOFOLLOW"):
        raise OSError(
            "staging executor requires os.O_NOFOLLOW, unavailable on this "
            "platform — containment cannot be enforced here")


def make_staging_executor(
    base_dir: str | Path,
    *,
    operation: Dict[str, Any] | None = None,
    registry_path: str | Path | None = None,
) -> Callable[[str, Dict[str, Any]], Dict[str, Any]]:
    """Build the bounded staging.write_file executor for one sandbox root.

    Bounds are read from the CANONICAL registry declaration (not
    hardcoded here): max content bytes, the contained staging directory
    name, the filename glob, and no-overwrite. Tightening the
    declaration tightens runtime behavior; an incompatible declaration
    fails closed at construction.

    Containment (POSIX):
    - the base is resolved once into the trusted root; every write must
      land inside it;
    - the staging directory is opened with O_DIRECTORY|O_NOFOLLOW, so a
      symlinked ``<base>/demo-staging`` is refused (ELOOP) instead of
      followed;
    - all file operations go through that directory fd, so path
      substitution between checking and opening cannot redirect the
      write;
    - the file is written to a unique temp name, fsynced, then hard-
      linked to the final name: link(2) is the atomic no-clobber
      linearization point. A crash can only leave an unlinked temp file,
      never a partial target.

    Idempotency: identical content is a no-op (no second effect);
    conflicting content is refused, never overwritten.

    Every parameter is validated BEFORE any filesystem mutation.
    Cleanup/rollback: the operation is a single file write; rollback is
    deleting the file. No compensating tool is registered (declared None).
    """

    if operation is None:
        reg = load_registry(registry_path)
        _, operation = find_operation(reg, _DOOR_ID, _TOOL_ID)
    bounds = _resolve_bounds(operation)
    _needs_nofollow()
    max_bytes = bounds["max_bytes"]
    dirname = bounds["staging_dirname"]
    filename_re = bounds["filename_re"]

    base_resolved = Path(base_dir).resolve()
    if not base_resolved.is_dir():
        raise ValueError(
            "staging executor refuses: base %r is not an existing "
            "directory" % (str(base_dir),))

    def executor(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_id != _TOOL_ID:
            return _err("executor serves only %r, got %r" % (_TOOL_ID, tool_id))
        if not isinstance(params, dict):
            return _err("params must be an object")
        filename = params.get("filename")
        content = params.get("content")
        if not isinstance(filename, str) or not filename_re.match(filename):
            return _err(
                "filename must match the declared pattern %r; got %r"
                % (bounds["filename_pattern"], filename))
        if not isinstance(content, str):
            return _err("content must be a string")
        data = content.encode("utf-8")
        if len(data) > max_bytes:
            return _err(
                "content exceeds the declared %d bytes (%d)"
                % (max_bytes, len(data)))

        digest = hashlib.sha256(data).hexdigest()
        staging = base_resolved / dirname
        try:
            staging.mkdir(exist_ok=True)
        except OSError as exc:
            return _err("cannot prepare staging root: %s" % exc)
        try:
            dir_fd = os.open(
                staging, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except OSError as exc:
            # ELOOP here means <base>/demo-staging is a symlink (or a
            # parent was swapped): refuse, never follow.
            return _err("staging root refused (unsafe link arrangement): %s"
                        % exc)
        try:
            return _atomic_publish(dir_fd, dirname, filename, data, digest)
        finally:
            os.close(dir_fd)

    return executor


def _atomic_publish(dir_fd: int, dirname: str, filename: str,
                    data: bytes, digest: str) -> Dict[str, Any]:
    """Write data under dir_fd and atomically publish it at filename.

    Temp-write + fsync + hard link: link(2) fails with EEXIST when the
    name is taken, which is the race-safe no-clobber decision point.
    """
    tmp_name = ".tmp-%d-%s" % (os.getpid(), secrets.token_hex(8))
    open_flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW)
    try:
        tmp_fd = os.open(tmp_name, open_flags, 0o644, dir_fd=dir_fd)
    except OSError as exc:
        return _err("filesystem error creating temp file: %s" % exc)
    try:
        with os.fdopen(tmp_fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(tmp_fd)
    except OSError as exc:
        try:
            os.unlink(tmp_name, dir_fd=dir_fd)
        except OSError:
            pass
        return _err("filesystem error writing temp file: %s" % exc)
    link_error: OSError | None = None
    try:
        os.link(tmp_name, filename, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
        won = True
    except FileExistsError:
        won = False
    except OSError as exc:
        won = False
        link_error = exc
    try:
        os.unlink(tmp_name, dir_fd=dir_fd)
    except OSError:
        pass
    if link_error is not None:
        return _err("filesystem error publishing artifact: %s" % link_error)
    if won:
        return {
            "status": "ok",
            "effects": "wrote %s/%s (%d bytes, sha256:%s)"
            % (dirname, filename, len(data), digest),
            "error_class": None,
        }
    # The name was already taken (pre-existing file or a lost race):
    # read the winner through dir_fd and compare. Never overwrite.
    try:
        rfd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
    except OSError as exc:
        return _err("existing artifact refused (unsafe link arrangement): %s"
                    % exc)
    with os.fdopen(rfd, "rb") as fh:
        existing = fh.read()
    if hashlib.sha256(existing).hexdigest() == digest:
        return {
            "status": "ok",
            "effects": "already_present %s/%s (%d bytes, sha256:%s) — "
            "no second write" % (dirname, filename, len(data), digest),
            "error_class": None,
        }
    return _err(
        "refuses to overwrite %s/%s (existing content differs)"
        % (dirname, filename))
