"""Directive Register — machine authority loader.

The single importable authority for master-directive metadata. Every gate,
scanner, or worker that needs directive facts (id, title, owner, status,
source) reads them here — never from a hardcoded copy.

FAIL-CLOSED CONTRACT (the whole point of this module):
  - register file missing        -> DirectiveRegisterError (never "empty OK")
  - register file invalid JSON    -> DirectiveRegisterError
  - register wrong shape          -> DirectiveRegisterError
  - duplicate directive ids      -> DirectiveRegisterError
  - entry missing required keys  -> DirectiveRegisterError
  - unknown directive id lookup  -> UnknownDirectiveError (never synthesized)

A caller that cannot load the register must refuse to certify, not proceed
on defaults. There are no defaults here by design.

Schema (BRAIN/01-GOVERNANCE/directive-register.json):
  [ {"id": "D8", "title": ..., "source_issue": 1354, "source_comment": "...",
      "owner": "naya5", "status": "NOT_STARTED" | "BUILDING" | "BUILT_AS_CODE" | "ENFORCED",
      "evidence_pr": 2184 | null, "wave": 6}, ... ]
"""

import json
from pathlib import Path

REGISTER_REL_PATH = Path("BRAIN") / "01-GOVERNANCE" / "directive-register.json"

REQUIRED_KEYS = frozenset(
    {"id", "title", "source_issue", "source_comment", "owner", "status", "evidence_pr", "wave"}
)

VALID_STATUSES = frozenset({"NOT_STARTED", "BUILDING", "BUILT_AS_CODE", "ENFORCED"})


class DirectiveRegisterError(Exception):
    """The register cannot be trusted. Callers must fail closed."""


class UnknownDirectiveError(DirectiveRegisterError):
    """A directive id was requested that the register does not know."""


def repo_root(start: Path | None = None) -> Path:
    """Walk up from `start` (or this file) to the repo root (the dir holding BRAIN/)."""
    here = Path(start) if start is not None else Path(__file__).resolve()
    if here.is_file():
        here = here.parent
    for candidate in (here, *here.parents):
        if (candidate / "BRAIN").is_dir():
            return candidate
    raise DirectiveRegisterError(
        f"Could not locate repo root (no BRAIN/ dir above {here})"
    )


def default_register_path() -> Path:
    return repo_root() / REGISTER_REL_PATH


def load_register(path: Path | None = None) -> list[dict]:
    """Load and validate the directive register. Raises DirectiveRegisterError
    on anything untrustworthy. Returns the list of directive entries."""
    reg_path = Path(path) if path is not None else default_register_path()
    if not reg_path.is_file():
        raise DirectiveRegisterError(f"Directive register not found: {reg_path}")
    try:
        raw = reg_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DirectiveRegisterError(f"Cannot read directive register {reg_path}: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise DirectiveRegisterError(
            f"Directive register is not valid JSON ({reg_path}): {exc}"
        ) from exc
    if not isinstance(data, list):
        raise DirectiveRegisterError(
            f"Directive register must be a JSON array, got {type(data).__name__}"
        )
    seen: set[str] = set()
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise DirectiveRegisterError(f"Register entry #{i} is not an object")
        missing = REQUIRED_KEYS - set(entry.keys())
        if missing:
            raise DirectiveRegisterError(
                f"Register entry #{i} ({entry.get('id', '?')}) missing keys: {sorted(missing)}"
            )
        did = entry["id"]
        if not isinstance(did, str) or not did.startswith("D"):
            raise DirectiveRegisterError(f"Register entry #{i} has bad id: {did!r}")
        if did in seen:
            raise DirectiveRegisterError(f"Duplicate directive id in register: {did}")
        seen.add(did)
        if entry["status"] not in VALID_STATUSES:
            raise DirectiveRegisterError(
                f"Register entry {did} has unknown status: {entry['status']!r}"
            )
    return data


def known_ids(directives: list[dict]) -> set[str]:
    return {d["id"] for d in directives}


def get_directive(directives: list[dict], directive_id: str) -> dict:
    """Return the register entry for `directive_id`.

    Raises UnknownDirectiveError if the register does not know it.
    Never invents, guesses, or defaults metadata.
    """
    for entry in directives:
        if entry["id"] == directive_id:
            return entry
    raise UnknownDirectiveError(
        f"Unknown directive {directive_id!r}: not in the machine register. "
        "Withhold certification until it is registered."
    )


def directive_number(directive_id: str) -> int:
    """D32 -> 32. Raises DirectiveRegisterError on malformed ids."""
    if not directive_id.startswith("D") or not directive_id[1:].isdigit():
        raise DirectiveRegisterError(f"Malformed directive id: {directive_id!r}")
    return int(directive_id[1:])
