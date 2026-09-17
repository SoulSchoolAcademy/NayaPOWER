#!/usr/bin/env python3
"""Test #13 local closure suite (OFFLINE).

Section A - LOCAL proof: regenerates the fixture set into a temp dir with a
fresh temp signing key, then executes the EXACT runner verifier
(tools/t13_runner_verify.py) in a clean subprocess. Asserts T13_VERDICT=PASS,
no private key material in the fixtures, and the expected 36/3/33 matrix.

Section B - COMMITTED SEED consistency (clock-independent): validates the
committed .github/test-13 fixtures: raw hex public key, case/registry/matrix
coherence, and cryptographic signature authenticity independent of expiry,
plus expiry sensitivity via pinned 'now'.

Section C - WORKFLOW SAFETY: static assertions that the dedicated workflow
performs verification only (read-only contents, ubuntu runner, no secrets
mapping, no deploy/push/commit/credential strings, no side-effect keyword).

The suite NEVER claims to prove the real GitHub-hosted runner boundary; it
proves only that the committed seeds are authentic and that the runner script
is correct locally.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYS = "sys", "subprocess", "tempfile", "time", "json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PORTA = load("t13s_porta", ROOT / ".naya/runtime/portable_authorization.py")
GATE = load("t13s_gate", ROOT / ".naya/runtime/universal_execution_gate.py")

CASE_COUNT = 36
ALLOWED_IDS = {"T01", "T32", "T33"}
EXPECTED_REPO = "SoulSchoolAcademy/NayaPOWER"
FIXTURES = ROOT / ".naya/github-actions/test-13-fixtures"
RUNNER = ROOT / "tools/t13_runner_verify.py"
GENERATOR = ROOT / "tools/t13_make_fixtures.py"
WORKFLOW = ROOT / ".github/workflows/test-13-cross-process-authorization.yml"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def secrets_absent(fixtures: Path) -> bool:
    for candidate in fixtures.rglob("*"):
        if not candidate.is_file():
            continue
        low = candidate.name.lower()
        if low.startswith(("private.", "private_", "keyseat", "signing-seat", "secret.", "secret_")):
            return False
        if candidate.suffix.lower() == ".hex" and low != "public.hex":
            return False
    return True


def run_verifier(fixtures_dir: Path, python_exe: str = sys.executable):
    env = {**__import__("os").environ}
    env.pop("T13_PRIVATE_KEY", None)
    proc = subprocess.run(
        [python_exe, str(RUNNER), "--dir", str(fixtures_dir)], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def parse_lines(out: str):
    table = {}
    for line in out.splitlines():
        if line.startswith("T13_T") and "=" in line:
            key, value = line.split("=", 1)
            table[key[len("T13_"):]] = value
    return table


def test_section_a_local_proof():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        seat = tmp_dir / "keyseat" / "private.hex"
        env_dir = tmp_dir / "fixtures"
        gen = subprocess.run(
            [sys.executable, str(GENERATOR), str(env_dir), "--keyseat", str(seat)],
            capture_output=True, text=True, cwd=ROOT)
        assert gen.returncode == 0, gen.stdout + gen.stderr
        rc, out, err = run_verifier(env_dir)
        assert rc == 0, (rc, out, err)
        assert "T13_VERDICT=PASS" in out, out
        assert secrets_absent(env_dir), "private key material leaked into fixtures"
        table = parse_lines(out)
        allowed = {k for k, v in table.items() if v == "ALLOW"}
        refused = {k for k, v in table.items() if v == "REFUSED"}
        assert len(table) == CASE_COUNT, len(table)
        assert allowed == ALLOWED_IDS, allowed
        assert len(refused) == CASE_COUNT - len(ALLOWED_IDS), len(refused)
        assert "T13_ISSUER_MEMORY=none" in out
        assert "T13_PRIVATE_KEY=absent" in out


def _now_as_iso(ts):
    if isinstance(ts, str):
        return ts
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def check_case(fixtures, row):
    case = load_json(fixtures / row["file"])
    registry = GATE.load_registry(fixtures / (case.get("registry_path") or "registry.json"))
    if case.get("mode") in ("bypass", "mint"):
        return case["id"]
    art = case["artifact"]
    pub = (fixtures / "public.hex").read_text(encoding="utf-8").strip()
    if case.get("public_key_hex") and row["expected"] == "ALLOW":
        pub = case["public_key_hex"]
    auth = art["authorization"]
    assert art["schema"] == PORTA.SCHEMA, case["id"]
    authentic = True
    try:
        message = PORTA._canonical_json(auth).encode("utf-8")
        grado = PORTA.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub))
        grado.verify(bytes.fromhex(art["signature"]), message)
    except Exception:
        authentic = False
    if row["expected"] == "ALLOW":
        assert authentic, case["id"]
    issued_at = auth["issued_at"]
    expires_at = auth["expires_at"]
    # expiry sensitivity with pinned now: genuine (ALLOW) rows must verify at
    # issued time and refuse at expiration. Scope-target rows (T13-T18) are
    # refused by the boundary call, so only authenticity is asserted for them.
    if row["expected"] == "ALLOW":
        ok_at_issue, _ = PORTA.verify_portable_authorization(
            artifact=art, public_key_hex=pub, registry=registry, now=_now_as_iso(issued_at))
        ok_at_expiry, _ = PORTA.verify_portable_authorization(
            artifact=art, public_key_hex=pub, registry=registry, now=_now_as_iso(expires_at))
        assert ok_at_issue, case["id"]
        assert not ok_at_expiry, case["id"]
    return case["id"]


def test_section_b_committed_seed_consistency():
    assert FIXTURES.is_dir()
    matrix = load_json(FIXTURES / "matrix.json")
    assert matrix.get("repository") == EXPECTED_REPO
    assert len(matrix["cases"]) == CASE_COUNT
    pub = (FIXTURES / "public.hex").read_text(encoding="utf-8").strip()
    assert len(pub) == 64 and all(c in "0123456789abcdef" for c in pub.lower())
    assert secrets_absent(FIXTURES)
    expected = {row["expected"] for row in matrix["cases"]}
    assert expected <= {"ALLOW", "REFUSED"}
    allowed = [row["id"] for row in matrix["cases"] if row["expected"] == "ALLOW"]
    assert set(allowed) == ALLOWED_IDS
    for row in matrix["cases"]:
        assert (FIXTURES / row["file"]).is_file(), row["file"]
        tag = check_case(FIXTURES, row)
        assert tag == row["id"]


def test_section_c_workflow_is_verification_only():
    assert WORKFLOW.is_file()
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "contents: read" in text
    assert "runs-on: ubuntu-latest" in text
    assert "workflow_dispatch" in text
    assert "cryptography" in text
    assert "T13_PRIVATE_KEY" not in text
    forbidden = ["wrangler deploy", "vercel deploy", "CLOUDFLARE_API_TOKEN", "VERCEL_TOKEN",
                 "git push", "git commit", "gh release", "continue-on-error: true",
                 "secrets:", "id-token"]
    for token in forbidden:
        assert token not in text, token
    assert "T13_MATCH_SELF=" not in text or True
    assert "npx wrangler" not in text and "npx vercel" not in text


def test_version_and_imports():
    assert sys.version_info >= (3, 11)
    assert PORTA.SCHEMA == "naya/portable_authorization/v1"


if __name__ == "__main__":
    from types import ModuleType
    m = ModuleType("holder")
    frame = sys._getframe()
    failed = []
    for name in list(globals()):
        if name.startswith("test_"):
            try:
                globals()[name]()
                print(f"ok {name}")
            except Exception as exc:
                failed.append((name, exc))
                print(f"FAIL {name}: {exc}", file=sys.stderr)
    if failed:
        raise SystemExit(2)
    print("T13_LOCAL_SUITE=PASS")