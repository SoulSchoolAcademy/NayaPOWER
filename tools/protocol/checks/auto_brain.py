#!/usr/bin/env python3
"""SN-AUTO-BRAIN — The Automatic Super Brain (mechanical layer).

Law: "The system must be structured so the correct action is the natural
action — computed by architecture, not discovered by effort."

The mechanical layer verifies that the architecture which computes the
right action is intact: every law registered in protocol_manifest.json
binds to a REAL, EXECUTABLE check; boot-gate modules reference manifests
that exist; and the boot gate itself runs green.

DRIFT → FAIL: any broken binding fails, naming the law, the missing file,
and the exact fix command.

What it proves:
  1. Binding integrity: every law has at least one executable binding —
     `check` -> existing file or `machine_check` -> existing file. A law
     whose binding points at a missing file FAILS (dead reference), naming
     the law id and the file.
  2. Honest nulls: a law with `check: null` is allowed ONLY with an explicit
     non-mechanical enforcement label (e.g. "human_attestation"). The label
     must not look like a file path — a phantom module reference fails.
     (SN-0500 "Think Before You Act" is honestly human; this gate does not
     fake-mechanize it.)
  3. Real gates: every `check:` binding is importable Python, defines
     `check()` and `main()`, and its CLI exits nonzero on a malformed
     record (fail-closed proof by execution, in a scratch subprocess).
  4. Boot-gate hygiene: every `*_gate.py` under tools/protocol/ and
     kernel/protocol/ that declares a MANIFEST_PATH must point at a file
     that exists (the dead-duplicate class: a gate that crashes on its own
     manifest — the class this PR removed as tools/protocol/cold_start_gate.py,
     a dead duplicate that crashed on a nonexistent manifest path).
  5. Boot gate health: kernel/protocol/protocol_integrity_gate.py runs
     green end-to-end for a probe agent. Step 5 needs network
     (git ls-remote); an outage fails the gate closed — correct, but a
     GitHub outage will red-line PRs until it clears.

What it does NOT prove (D32, said out loud): that agents actually consult
the architecture at decision time; that a check's semantics match its law's
intent; that every check is invoked by CI. Those are review concerns, not
this gate's. A law can pass here and still be weakly enforced in practice —
see the enforcement-coverage scorecard for the CI-wiring column.

Fail-closed: a malformed record, an unreadable manifest, or any subprocess
error fails the check — never silently checks the wrong tree.

Input record:
    {
      "repo_root": "<absolute path to the NayaPOWER checkout>"  # optional;
          # default = the repo root derived from this file's location
    }

The check verifies compliance; it never grants authority.

Usage:
    python3 tools/protocol/checks/auto_brain.py --record '{}' [--json]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))  # tools/protocol/checks/ -> helpers

from checks import emit, fail, load_record, result  # noqa: E402

LAW_ID = "SN-AUTO-BRAIN"
MANIFEST_REL = Path("kernel/protocol/protocol_manifest.json")
BOOT_GATE_REL = Path("kernel/protocol/protocol_integrity_gate.py")
FIX_COMMAND = "python3 tools/protocol/checks/auto_brain.py --record '{}'"
GARBAGE_RECORD = "###not-json###"
PROBE_TIMEOUT = 60
BOOT_GATE_TIMEOUT = 120


def _repo_root(record: dict) -> Path:
    """Resolve the checkout to check. Fail closed on anything that is not one."""
    raw = record.get("repo_root")
    if raw is None:
        root = TOOLS_DIR.parent.parent  # tools/protocol/checks/x.py -> repo root
    elif isinstance(raw, str) and raw.strip():
        root = Path(raw.strip())
    else:
        raise ValueError("repo_root must be a non-empty string or omitted")
    manifest = root / MANIFEST_REL
    if not manifest.is_file():
        raise ValueError(
            f"not a NayaPOWER checkout: {MANIFEST_REL} not found under {root}"
        )
    return root


def _load_manifest(root: Path) -> dict:
    path = root / MANIFEST_REL
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        raise ValueError(f"manifest unreadable at {path}: {e}")
    if not isinstance(data, dict) or not isinstance(data.get("laws"), list):
        raise ValueError(f"manifest at {path} is not a law manifest")
    return data


def _law_label(law: dict) -> str:
    return law.get("name") or law.get("title") or law.get("id", "?")


def _looks_like_path(value: str) -> bool:
    return "/" in value or "\\" in value or value.endswith(".py")


def _check_bindings(root: Path, laws: list) -> tuple[list, dict]:
    """Step 1+2: every law binds to something real; nulls are honestly labeled."""
    reasons: list[str] = []
    details: dict = {"laws_checked": len(laws), "bindings": {}}
    for law in laws:
        if not isinstance(law, dict):
            reasons.append(
                f"DRIFT: manifest contains a law entry that is not an object: "
                f"{str(law)[:120]}. Fix: repair the entry in "
                f"kernel/protocol/protocol_manifest.json, then re-run "
                f"`{FIX_COMMAND}`."
            )
            continue
        lid = law.get("id", "?")
        check_path = law.get("check")
        machine_path = law.get("machine_check")
        binding = check_path or machine_path
        if binding is None:
            label = law.get("enforcement")
            if isinstance(label, str) and label.strip() and not _looks_like_path(label):
                details["bindings"][lid] = f"human: {label}"
                continue
            reasons.append(
                f"DRIFT: law {lid} ({_law_label(law)}) has no executable binding "
                f"(check: null, machine_check missing) and no explicit "
                f"non-mechanical enforcement label. Fix: add a real check file "
                f"and register it as 'check', or declare an honest label like "
                f"'human_attestation' in kernel/protocol/protocol_manifest.json; "
                f"then re-run `{FIX_COMMAND}`."
            )
            details["bindings"][lid] = "MISSING"
            continue
        if not isinstance(binding, str) or not binding.strip():
            reasons.append(
                f"DRIFT: law {lid} ({_law_label(law)}) has a malformed binding "
                f"(not a file path): {str(binding)[:120]}. Fix: set 'check' or "
                f"'machine_check' to a real path in "
                f"kernel/protocol/protocol_manifest.json, then re-run "
                f"`{FIX_COMMAND}`."
            )
            details["bindings"][lid] = "MALFORMED"
            continue
        target = root / binding
        if not target.is_file():
            reasons.append(
                f"DRIFT: law {lid} ({_law_label(law)}) binds to a missing file: "
                f"{binding}. Fix: restore the file at {binding}, or update the "
                f"binding in kernel/protocol/protocol_manifest.json; then re-run "
                f"`{FIX_COMMAND}`."
            )
            details["bindings"][lid] = f"DEAD: {binding}"
            continue
        details["bindings"][lid] = binding
    return reasons, details


def _import_module(root: Path, path: Path):
    """Import a module from a path, package-aware.

    If the file lives inside a package (every parent directory up to the
    repo root has an __init__.py), import it by dotted name so relative
    imports work. Otherwise load it standalone under a probe name.
    Raises on failure.
    """
    rel = path.relative_to(root)
    parts = rel.with_suffix("").parts
    chain_ok = all(
        (root.joinpath(*parts[:i], "__init__.py")).is_file()
        for i in range(1, len(parts))
    )
    if chain_ok:
        dotted = ".".join(parts)
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        try:
            return importlib.import_module(dotted)
        except BaseException:
            pass  # fall through to the standalone attempt for a better error
    name = f"auto_brain_probe_{path.stem}_{abs(hash(str(path))) % 10**8}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def _probe_fail_closed(path: Path) -> tuple[bool, str]:
    """Run the check's CLI on a malformed record; it must exit nonzero."""
    try:
        proc = subprocess.run(
            [sys.executable, str(path), "--record", GARBAGE_RECORD],
            capture_output=True, text=True, timeout=PROBE_TIMEOUT,
        )
    except Exception as e:
        return False, f"probe error: {e}"
    if proc.returncode == 0:
        return False, "exited 0 on a malformed record (fail-open)"
    return True, f"exit {proc.returncode} on malformed record (fail-closed)"


def _check_gates_executable(root: Path, laws: list) -> tuple[list, dict]:
    """Step 3: every `check:` binding is a real, fail-closed gate."""
    reasons: list[str] = []
    details: dict = {"gates_probed": 0}
    for law in laws:
        binding = law.get("check")
        if not binding:
            continue
        lid = law.get("id", "?")
        path = root / binding
        if not path.is_file():
            continue  # already reported as DRIFT by _check_bindings
        try:
            module = _import_module(root, path)
        except BaseException as e:
            reasons.append(
                f"DRIFT: law {lid}'s check is not importable: {binding} "
                f"({type(e).__name__}: {e}). Fix: repair the module so it "
                f"imports cleanly, then re-run `{FIX_COMMAND}`."
            )
            continue
        missing = [n for n in ("check", "main") if not callable(getattr(module, n, None))]
        if missing:
            reasons.append(
                f"DRIFT: law {lid}'s check does not follow the gate pattern: "
                f"{binding} is missing {', '.join(missing)}(). Every protocol "
                f"check must define check(record) and main() (see "
                f"tools/protocol/checks/__init__.py). Fix the module, then "
                f"re-run `{FIX_COMMAND}`."
            )
            continue
        ok, note = _probe_fail_closed(path)
        details["gates_probed"] += 1
        if not ok:
            reasons.append(
                f"DRIFT: law {lid}'s check is fail-open: {binding} — {note}. "
                f"Fix: make main() exit nonzero on malformed input, then "
                f"re-run `{FIX_COMMAND}`."
            )
        else:
            details[binding] = note
    return reasons, details


def _check_machine_checks(root: Path, laws: list) -> tuple[list, dict]:
    """Step 4 (part 1): every `machine_check:` binding is importable and
    exposes at least one validation entry point."""
    reasons: list[str] = []
    details: dict = {}
    for law in laws:
        binding = law.get("machine_check")
        if not binding:
            continue
        lid = law.get("id", "?")
        path = root / binding
        if not path.is_file():
            continue  # already reported as DRIFT by _check_bindings
        try:
            module = _import_module(root, path)
        except BaseException as e:
            reasons.append(
                f"DRIFT: law {lid}'s machine_check is not importable: {binding} "
                f"({type(e).__name__}: {e}). Fix: repair the module so it "
                f"imports cleanly, then re-run `{FIX_COMMAND}`."
            )
            continue
        entry_points = [
            n for n in dir(module)
            if callable(getattr(module, n))
            and (n.startswith("check") or n in ("run_gate", "main"))
            and not n.startswith("_")
        ]
        if not entry_points:
            reasons.append(
                f"DRIFT: law {lid}'s machine_check exposes no validation entry "
                f"point: {binding} has no callable check*/run_gate/main. Fix: "
                f"expose one, then re-run `{FIX_COMMAND}`."
            )
        else:
            details[binding] = entry_points
    return reasons, details


def _check_boot_gate_manifests(root: Path, laws: list) -> tuple[list, dict]:
    """Step 4 (part 2): boot-gate modules must reference manifests that exist."""
    reasons: list[str] = []
    details: dict = {"gates_scanned": 0}
    gate_files = sorted((root / "tools" / "protocol").glob("*_gate.py"))
    gate_files += sorted((root / "kernel" / "protocol").glob("*_gate.py"))
    for path in gate_files:
        rel = path.relative_to(root)
        try:
            module = _import_module(root, path)
        except BaseException as e:
            reasons.append(
                f"DRIFT: boot-gate module is not importable: {rel} "
                f"({type(e).__name__}: {e}). Fix: repair the module, then "
                f"re-run `{FIX_COMMAND}`."
            )
            continue
        details["gates_scanned"] += 1
        manifest_path = getattr(module, "MANIFEST_PATH", None)
        if manifest_path is None:
            details[str(rel)] = "no MANIFEST_PATH declared (skipped)"
            continue
        manifest_path = Path(manifest_path)
        if not manifest_path.is_absolute():
            manifest_path = path.parent / manifest_path
        if not manifest_path.is_file():
            reasons.append(
                f"DRIFT: boot-gate module {rel} references a missing manifest: "
                f"{manifest_path}. A gate that cannot load its own manifest "
                f"crashes instead of governing. Fix: point MANIFEST_PATH at "
                f"the real manifest ({MANIFEST_REL}), then re-run "
                f"`{FIX_COMMAND}`."
            )
        else:
            details[str(rel)] = f"manifest OK: {manifest_path.relative_to(root)}"
    return reasons, details


def _check_boot_gate_green(root: Path) -> tuple[list, dict]:
    """Step 5: the canonical boot gate runs green end-to-end."""
    reasons: list[str] = []
    details: dict = {}
    gate = root / BOOT_GATE_REL
    if not gate.is_file():
        return [f"DRIFT: canonical boot gate missing: {BOOT_GATE_REL}."], details
    try:
        proc = subprocess.run(
            [sys.executable, str(gate), "--agent-id", "auto-brain-probe", "--json"],
            capture_output=True, text=True, timeout=BOOT_GATE_TIMEOUT, cwd=root,
        )
    except Exception as e:
        return [f"DRIFT: boot gate {BOOT_GATE_REL} could not run: {e}."], details
    if proc.returncode != 0:
        reasons.append(
            f"DRIFT: boot gate {BOOT_GATE_REL} exits {proc.returncode} for a "
            f"probe agent — the architecture cannot verify a cold start. "
            f"Output: {(proc.stdout + proc.stderr).strip()[:600]}. Fix the "
            f"gate, then re-run `{FIX_COMMAND}`."
        )
        return reasons, details
    try:
        data = json.loads(proc.stdout)
    except Exception as e:
        return [f"DRIFT: boot gate {BOOT_GATE_REL} emitted unparseable JSON: {e}."], details
    if not data.get("pass"):
        failed = [c.get("name") for c in data.get("failures", [])]
        reasons.append(
            f"DRIFT: boot gate {BOOT_GATE_REL} reports FAIL for a probe agent "
            f"(failed: {', '.join(failed) or 'unknown'}). Fix the gate or the "
            f"tree it checks, then re-run `{FIX_COMMAND}`."
        )
    else:
        details["boot_gate"] = f"green ({len(data.get('checks', []))} checks)"
    return reasons, details


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": LAW_ID}
    try:
        root = _repo_root(record)
    except Exception as e:
        return fail(f"unusable repo_root: {e}", {"law": LAW_ID})
    try:
        manifest = _load_manifest(root)
    except Exception as e:
        return fail(f"manifest unreadable: {e}", {"law": LAW_ID})
    laws = manifest["laws"]

    for step_fn in (_check_bindings, _check_gates_executable,
                    _check_machine_checks, _check_boot_gate_manifests):
        step_reasons, step_details = step_fn(root, laws)
        reasons.extend(step_reasons)
        details[step_fn.__name__] = step_details
    step_reasons, step_details = _check_boot_gate_green(root)
    reasons.extend(step_reasons)
    details["_check_boot_gate_green"] = step_details

    details["laws_total"] = len(laws)
    if reasons:
        return fail(
            f"DRIFT: the auto-brain surface is broken — {len(reasons)} problem(s). "
            + " ".join(reasons),
            details,
        )
    return result(True, ["auto-brain surface intact: every law binds to a real, "
                         "executable check; boot-gate manifests resolve; the "
                         "boot gate runs green."], details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-AUTO-BRAIN boot-surface gate")
    parser.add_argument("--record", required=True,
                        help="JSON record (or @file); {} checks this checkout")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": LAW_ID}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
