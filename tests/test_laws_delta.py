"""Tests for tools/generate_laws_delta.py and the 0033/0034 law sets.

Covers: the new machine tongues are valid JSON; the generated delta
carries tonight's two laws complete (statement + falsifier + owner);
the generator is idempotent (second run = zero diff); a planted
malformed machine tongue is caught by --check with a cure line;
a stale delta is caught by --check with a cure line.

Scratch trees are built under tests/.laws-delta-scratch/ (repo disk,
never /tmp — the VM sweeps /tmp within seconds) and removed after.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOV = ROOT / "BRAIN" / "01-GOVERNANCE"
TOOL = ROOT / "tools" / "generate_laws_delta.py"
SCRATCH = ROOT / "tests" / ".laws-delta-scratch"


def run_gen(gov_dir, *extra):
    return subprocess.run(
        [sys.executable, str(TOOL), "--gov", str(gov_dir), *extra],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def scratch_gov():
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    dst = SCRATCH / "gov"
    shutil.copytree(GOV, dst)
    return dst


def teardown_function(_):
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)


def test_new_machine_tongues_are_valid_json():
    for name in ("0033-the-balanced-machine-v1.machine.json",
                 "0034-the-house-fire-law-v1.machine.json",
                 "LAWS-DELTA.machine.json"):
        d = json.loads((GOV / name).read_text())
        assert isinstance(d, dict), name


def test_delta_carries_tonights_laws_complete():
    delta = json.loads((GOV / "LAWS-DELTA.machine.json").read_text())
    by_id = {l["id"]: l for l in delta["laws"]}
    for gid in ("GOV-0033", "GOV-0034"):
        assert gid in by_id, f"{gid} missing from delta"
        law = by_id[gid]
        assert law["statement"], f"{gid} statement empty"
        assert law["falsifier"], f"{gid} falsifier empty"
        assert law["owner"], f"{gid} owner empty"
        assert law["tongues"]["human"] and law["tongues"]["ai"], gid
    assert delta["generated_from"]["source_fingerprint_sha256"]
    assert delta["generated_from"]["machine_tongue_blob_shas"]


def test_committed_delta_is_fresh():
    r = run_gen(GOV, "--check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_generator_is_idempotent():
    gov = scratch_gov()
    out = gov / "LAWS-DELTA.machine.json"
    if out.exists():
        out.unlink()
    r1 = run_gen(gov)
    assert r1.returncode == 0, r1.stdout + r1.stderr
    first = out.read_bytes()
    r2 = run_gen(gov)
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert out.read_bytes() == first, "second generation differs — not idempotent"


def test_malformed_machine_file_caught_with_cure_line():
    gov = scratch_gov()
    (gov / "0099-broken-v1.machine.json").write_text('{"title": "BROKEN", ')
    r = run_gen(gov, "--check")
    assert r.returncode == 1, r.stdout
    assert "MISSING:" in r.stdout and "CURE:" in r.stdout, r.stdout
    assert "0099-broken-v1.machine.json" in r.stdout, r.stdout


def test_stale_delta_caught_with_cure_line():
    gov = scratch_gov()
    out = gov / "LAWS-DELTA.machine.json"
    r1 = run_gen(gov)
    assert r1.returncode == 0, r1.stdout + r1.stderr
    # mutate a source after generation: the delta must now read stale
    p = gov / "0034-the-house-fire-law-v1.machine.json"
    d = json.loads(p.read_text())
    d["version"] = "1.0-test-mutation"
    p.write_text(json.dumps(d, indent=1, sort_keys=True) + "\n")
    r2 = run_gen(gov, "--check")
    assert r2.returncode == 1, r2.stdout
    assert "CURE:" in r2.stdout, r2.stdout


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
        finally:
            teardown_function(None)
    sys.exit(1 if failed else 0)
