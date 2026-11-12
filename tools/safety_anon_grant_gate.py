#!/usr/bin/env python3
"""Safety anon-grant gate (fail-closed CI check for Supabase migrations).

Every migration that GRANTs privileges to the `anon` role or to `PUBLIC`
must carry a matching entry in tools/safety_grant_allowlist.json. Anything
else fails the build.

Why: the 2026-10-06 Security Advisor 27-warning classification found live
anon-reachable DEFINER functions and tables whose repo sources had already
revoked the grants -- the grants landed without a review checkpoint. This
gate is that checkpoint: widening anonymous access is a conscious,
documented, allowlisted decision, never an accident.

Fail-closed rules:
  - GRANT ... TO anon / PUBLIC without an allowlist entry  -> FAIL
  - GRANT whose privileges exceed the allowlist entry        -> FAIL
  - GRANT ON ALL TABLES / ALL FUNCTIONS / ALL SEQUENCES     -> FAIL
    (too broad to be allowlisted; split into explicit grants)
  - a GRANT-like statement the parser cannot understand      -> FAIL
  - missing migrations dir / missing or invalid allowlist   -> FAIL (error)
  - REVOKE statements are always fine (removing access is the safe direction)
  - grants to authenticated / service_role / postgres are not in scope
    (signed-in or infrastructure roles; governed elsewhere)

Exit codes: 0 = pass, 1 = violation, 2 = gate error (fail closed).
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MIGRATIONS = REPO_ROOT / "supabase" / "migrations"
DEFAULT_ALLOWLIST = Path(__file__).resolve().parent / "safety_grant_allowlist.json"

# Roles whose widening is governed by this gate.
WATCHED_ROLES = {"anon", "public"}

# Grants to these roles are out of scope (not anonymous surface).
TRUSTED_ROLES = {"authenticated", "service_role", "postgres"}

_GRANT_RE = re.compile(
    r"""grant\s+(?P<privs>.*?)\s+on\s+(?P<rest>[^;]+?)\s+to\s+(?P<grantees>[^;]+)""",
    re.IGNORECASE | re.DOTALL,
)

_OBJTYPE_RE = re.compile(
    r"^(?P<objtype>table|function|sequence|schema|database|"
    r"all\s+tables|all\s+functions|all\s+sequences)\s+(?P<objects>.*)$",
    re.IGNORECASE | re.DOTALL,
)

_COLLIST_RE = re.compile(r"\([^()]*\)")  # column lists / function signatures


def _split_top_level(text: str) -> list[str]:
    """Split on commas that are not inside parentheses."""
    parts, depth, cur = [], 0, []
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p for p in (x.strip() for x in parts) if p]


@dataclass
class Grant:
    privileges: tuple
    objtype: str
    object: str
    grantees: tuple
    source: str  # "file:line"


def _strip_comments(sql: str) -> str:
    out = []
    for line in sql.splitlines():
        s = line.strip()
        if s.startswith("--"):
            continue
        # cut trailing -- comments (naive: good enough for migrations)
        idx = line.find("--")
        if idx != -1:
            line = line[:idx]
        out.append(line)
    return "\n".join(out)


def _normalize_object(objtype: str, obj: str) -> str:
    obj = re.sub(r"\s+", " ", obj.strip().rstrip(";").strip()).lower()
    # collapse "in schema public" tails
    obj = re.sub(r"\s+in\s+schema\s+\S+$", "", obj).strip()
    return f"{objtype}:{obj}"


def parse_grants(sql_text: str, source: str) -> tuple[list[Grant], list[str]]:
    """Return (grants, parse_problems). Problems fail the gate closed."""
    grants: list[Grant] = []
    problems: list[str] = []
    cleaned = _strip_comments(sql_text)
    for stmt in cleaned.split(";"):
        stmt = stmt.strip()
        if not stmt:
            continue
        if not re.match(r"(?i)^\s*grant\b", stmt):
            continue
        m = _GRANT_RE.match(stmt + ";")
        if not m:
            problems.append(f"{source}: unparseable GRANT statement: {stmt[:120]!r}")
            continue
        rest = m.group("rest").strip()
        om = _OBJTYPE_RE.match(rest)
        if om:
            objtype = re.sub(r"\s+", " ", om.group("objtype").strip().lower())
            objects = _split_top_level(om.group("objects"))
        else:
            # bare "ON <name>" without TABLE/FUNCTION keyword: infer from shape
            objtype = None
            objects = _split_top_level(re.sub(r"\s+in\s+schema\s+\S+$", "", rest, flags=re.IGNORECASE))
        # privileges may carry a column list: "select (id, name)" -> "select"
        raw_privs = _COLLIST_RE.sub("", m.group("privs"))
        privs = tuple(p.strip().lower() for p in raw_privs.split(",") if p.strip())
        grantees = tuple(g.strip().lower().strip('"') for g in m.group("grantees").split(",") if g.strip())
        if not privs or not grantees or not objects:
            problems.append(f"{source}: GRANT with empty privileges/grantees/objects: {stmt[:120]!r}")
            continue
        if any(not re.fullmatch(r"[a-z_]+", p) for p in privs):
            problems.append(f"{source}: GRANT with non-privilege tokens: {stmt[:120]!r}")
            continue
        for obj in objects:
            otype = objtype or ("function" if "(" in obj else "table")
            grants.append(Grant(privileges=privs, objtype=otype,
                                object=_normalize_object(otype, obj),
                                grantees=grantees, source=source))
    return grants, problems


def load_allowlist(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        raise GateError(f"allowlist not found: {path}")
    except json.JSONDecodeError as e:
        raise GateError(f"allowlist is not valid JSON: {e}")
    entries = data.get("grants", [])
    if not isinstance(entries, list):
        raise GateError("allowlist 'grants' must be a list")
    normalized = []
    for i, e in enumerate(entries):
        for key in ("object", "privileges", "grantees", "justification"):
            if key not in e:
                raise GateError(f"allowlist entry {i} missing key: {key}")
        normalized.append({
            "object": e["object"].strip().lower(),
            "privileges": {p.strip().lower() for p in e["privileges"]},
            "grantees": {g.strip().lower() for g in e["grantees"]},
            "justification": e["justification"],
        })
    return {"entries": normalized}


class GateError(Exception):
    pass


def check(migrations_dir: Path, allowlist_path: Path) -> tuple[list[str], list[str]]:
    """Return (violations, errors). Either non-empty fails the gate."""
    violations: list[str] = []
    errors: list[str] = []
    if not migrations_dir.is_dir():
        return [], [f"migrations dir not found: {migrations_dir}"]
    try:
        allowlist = load_allowlist(allowlist_path)
    except GateError as e:
        return [], [str(e)]

    files = sorted(migrations_dir.glob("*.sql"))
    if not files:
        return [], [f"no migration files in {migrations_dir}"]

    for path in files:
        try:
            text = path.read_text()
        except OSError as e:
            errors.append(f"cannot read {path.name}: {e}")
            continue
        grants, problems = parse_grants(text, path.name)
        errors.extend(problems)
        for g in grants:
            watched = [r for r in g.grantees if r in WATCHED_ROLES]
            if not watched:
                continue  # only anonymous-surface grants are in scope
            if g.objtype.startswith("all "):
                violations.append(
                    f"{g.source}: broad grant '{' '.join(g.privileges)}' ON {g.objtype.upper()} "
                    f"to {','.join(watched)} -- split into explicit per-object grants with allowlist entries"
                )
                continue
            covered = False
            for entry in allowlist["entries"]:
                if entry["object"] != g.object:
                    continue
                if not set(watched) <= entry["grantees"]:
                    continue
                if not set(g.privileges) <= entry["privileges"]:
                    violations.append(
                        f"{g.source}: grant {g.object} privileges {sorted(g.privileges)} exceed "
                        f"allowlist {sorted(entry['privileges'])}"
                    )
                    covered = True  # reported; don't also report as missing
                    break
                covered = True
                break
            if not covered:
                violations.append(
                    f"{g.source}: GRANT {', '.join(g.privileges)} ON {g.object} "
                    f"TO {', '.join(watched)} has no allowlist entry "
                    f"(tools/safety_grant_allowlist.json)"
                )
    return violations, errors


def main(argv: list[str]) -> int:
    migrations = Path(argv[1]) if len(argv) > 1 else DEFAULT_MIGRATIONS
    allowlist = Path(argv[2]) if len(argv) > 2 else DEFAULT_ALLOWLIST
    violations, errors = check(migrations, allowlist)
    if errors:
        print("SAFETY-GRANT-GATE: ERROR (fail closed)")
        for e in errors:
            print(f"  ! {e}")
        return 2
    if violations:
        print("SAFETY-GRANT-GATE: FAIL")
        for v in violations:
            print(f"  x {v}")
        print(f"\n{len(violations)} unallowlisted anonymous-surface grant(s). "
              "Document the intent in tools/safety_grant_allowlist.json or remove the grant.")
        return 1
    print("SAFETY-GRANT-GATE: PASS (no unallowlisted anon/PUBLIC grants)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
