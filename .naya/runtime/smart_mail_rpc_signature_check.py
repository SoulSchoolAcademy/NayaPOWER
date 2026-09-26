"""Static caller/callee conformance check for NayaNET Smart Mail RPCs.

Causal finding this guards against:
Supabase/PostgREST resolves rpc() by argument NAME against the schema cache. If
the Edge Function passes a parameter that the deployed SQL function does not
declare, the call fails with "Could not find the function ... in the schema
cache" instead of a useful error. That exact mismatch blocked the Collective
Intelligence Chain proof at INDEPENDENT_OUTCOME_ACTION_FAILED.

This check compares the argument names the Edge Function actually sends against
the parameter list of the NEWEST migration that defines each SQL function, so
the class of defect is caught deterministically without touching production.

Run: python -B .naya/runtime/smart_mail_rpc_signature_check.py
Exit 0 = every sent argument exists in the newest SQL definition.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MIGRATIONS = REPO / "supabase" / "migrations"
EDGE_FN = REPO / "supabase" / "functions" / "nayanet-smart-mail" / "index.ts"


def resolve_edge_function() -> Path:
    """Allow checking an alternate copy (used for negative-control proof)."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return EDGE_FN

# Edge Function rpc() call site -> the SQL function each branch targets.
CALL_SITES = {
    "nayanet_send_smart_mail_policy_authorized": "policy branch (experiment/policy evidence present)",
    "nayanet_send_smart_mail_authorized": "default branch",
}

DEF_RE = re.compile(
    r"create\s+or\s+replace\s+function\s+public\.([a-z0-9_]+)\s*\(([^)]*)\)",
    re.IGNORECASE | re.DOTALL,
)
PARAM_RE = re.compile(r"^\s*(p_[a-z0-9_]+)\s+", re.IGNORECASE)


def newest_definitions() -> dict[str, tuple[str, list[str]]]:
    """Return {function: (migration_filename, [param names])} using the last definition."""
    found: dict[str, tuple[str, list[str]]] = {}
    for path in sorted(MIGRATIONS.glob("*.sql")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in DEF_RE.finditer(text):
            name = match.group(1).lower()
            params = [
                p.group(1).lower()
                for p in (PARAM_RE.match(line) for line in match.group(2).splitlines())
                if p
            ]
            found[name] = (path.name, params)
    return found


def rpc_arg_branches(source: str) -> list[list[str]]:
    """Extract the ordered [policy, default] argument-name lists from rpcArgs."""
    start = source.find("const rpcArgs=")
    if start == -1:
        return []
    end = source.find("const {data:result", start)
    if end == -1:
        end = source.find("\n", start)
    region = source[start:end]
    branches: list[list[str]] = []
    for literal in re.findall(r"\{[^{}]*\}", region):
        keys: list[str] = []
        for key in re.findall(r"\b(p_[a-z0-9_]+)\s*:", literal):
            if key not in keys:
                keys.append(key)
        branches.append(keys)
    return branches


def main() -> int:
    edge_fn = resolve_edge_function()
    if not edge_fn.is_file():
        print(f"FAIL EDGE_FUNCTION_MISSING: {edge_fn}")
        return 1
    source = edge_fn.read_text(encoding="utf-8", errors="replace")
    definitions = newest_definitions()
    branches = rpc_arg_branches(source)
    if len(branches) != 2:
        print(f"FAIL RPC_ARGS_BRANCHES_UNRESOLVED: expected 2 object literals, found {len(branches)}")
        return 1
    ordered = list(CALL_SITES.items())
    failures: list[str] = []
    checked = 0

    for (function, label), sent in zip(ordered, branches):
        definition = definitions.get(function)
        if definition is None:
            failures.append(f"{function}: no SQL definition found in supabase/migrations")
            continue
        migration, params = definition
        if not sent:
            failures.append(f"{function}: no p_* arguments found in Edge Function source")
            continue
        unknown = [name for name in sent if name not in params]
        checked += len(sent)
        if unknown:
            failures.append(
                f"{function}: Edge Function sends undeclared parameter(s) {unknown}; "
                f"newest definition {migration} declares {params}"
            )
        else:
            print(f"PASS {function} ({label})")
            print(f"     newest definition: {migration}")
            print(f"     declared params   : {len(params)} -> {params}")
            print(f"     sent params       : {len(sent)} -> {sent}")
            required_unsent = [p for p in params if p not in sent and not _has_default(function, p)]
            if required_unsent:
                failures.append(
                    f"{function}: required parameter(s) never sent and without default: {required_unsent}"
                )

    print(f"\nchecked {checked} argument name(s) across {len(CALL_SITES)} RPC call site(s)")
    if failures:
        print("\nSMART_MAIL_RPC_SIGNATURE_MISMATCH")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("SMART_MAIL_RPC_SIGNATURE_ALIGNED")
    return 0


def _has_default(function: str, param: str) -> bool:
    """True if the newest definition of `param` on `function` declares a DEFAULT."""
    for path in sorted(MIGRATIONS.glob("*.sql"), reverse=True):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in DEF_RE.finditer(text):
            if match.group(1).lower() != function.lower():
                continue
            for line in match.group(2).splitlines():
                if re.match(rf"^\s*{re.escape(param)}\s+", line, re.IGNORECASE):
                    return "default" in line.lower()
    return False


if __name__ == "__main__":
    sys.exit(main())
