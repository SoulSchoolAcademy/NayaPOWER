"""Smart Note collision guard: claim before author, or the number is not yours.

Origin: 2026-10-26. The registry's allocator
(tools/smart_note_v2.py:_allocate_from_registry — locked, occupancy-aware)
had zero production callers; notes were numbered by hand from the
registry's next_sequence counter after it had gone stale and pointed at
an occupied number, producing the SN-1863 twin filing. The guard built
from the 2026-10-26 build brief:

  - tools/sn_claims.py gives the allocator its first production caller:
    a filing claims its number BEFORE the note is written, and the claim
    is anchored as a JSON file on the dedicated sn-claims branch — the
    push is a compare-and-swap (git rejects non-fast-forward), so two
    lanes racing in the same minute get a mechanical winner and the
    loser is renumbered by the allocator, with the receipt naming both
    claims;
  - the registry counter is repaired once and demoted to advisory,
    permanently — the allocator is the only numbering authority;
  - tools/check_door_obligation.py raises WARN-level (P1) filing
    warnings: COUNTER_STALE (the advisory counter drifted onto an
    occupied number) and UNCLAIMED_NUMBER (a filing in a checked range
    carries a number nobody claimed). Warnings never change the door's
    exit code.

Run:  python -m pytest tests/test_sn_collision_guard.py -q
"""

import importlib.util
import json
import shutil
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sn_claims = _load("sn_claims", "tools/sn_claims.py")
door = _load("check_door_obligation", "tools/check_door_obligation.py")


def make_registry(pairs, next_sequence):
    return {
        "schema": "naya.smart-note-projection-index.v1",
        "entries": [{"smart_note_id": sn, "intelligent_block_id": ib}
                    for sn, ib in pairs],
        "sequence_policy": {"human_id_format": "SN-###",
                            "next_sequence": next_sequence},
    }


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True)
    assert r.returncode == 0, f"git {args} failed: {r.stderr}"
    return r.stdout.strip()


def bare_remote(tmp_path: Path) -> Path:
    remote = tmp_path / "remote.git"
    remote.mkdir()
    git(remote, "init", "--bare", "-q", ".")
    return remote


# --------------------------------------------------------------------------
# The race: two lanes, same minute, one winner — mechanically

def test_race_two_claims_exactly_one_winner(tmp_path):
    remote = bare_remote(tmp_path)
    registry = make_registry([("SN-0001", "IB-A"), ("SN-0002", "IB-B")],
                             next_sequence=3)
    barrier = threading.Barrier(2)

    def hook(attempt, number):
        # Both lanes compute their candidate from the same branch tip
        # before either pushes — the contention is forced, not hoped for.
        if attempt == 1:
            barrier.wait(timeout=60)

    results, errors = {}, {}

    def run(key, ib):
        try:
            results[key] = sn_claims.claim_number(
                str(remote), ib=ib, seat=f"Seat {key}", registry=registry,
                _pre_push_hook=hook)
        except Exception as exc:  # surfaced by the assertion below
            errors[key] = exc

    threads = [threading.Thread(target=run, args=("a", "IB-RACE-A")),
               threading.Thread(target=run, args=("b", "IB-RACE-B"))]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=120)

    assert not errors, f"a racing claim failed closed instead of renumbering: {errors}"
    numbers = {results["a"]["claim"]["number"], results["b"]["claim"]["number"]}
    assert numbers == {3, 4}, f"expected exactly one winner on 3 and a renumber to 4, got {numbers}"

    loser = results["a"] if results["a"]["claim"]["number"] == 4 else results["b"]
    assert loser["attempts"] == 2
    assert loser["renumbered_from"] == 3
    assert loser["winning_claim"]["number"] == 3  # the receipt names both claims

    claims = sn_claims.read_claims(remote)
    assert sorted(claims) == [3, 4]
    assert {claims[n]["intelligent_block_id"] for n in (3, 4)} == {"IB-RACE-A", "IB-RACE-B"}


# --------------------------------------------------------------------------
# The stale counter: WARN fires; the allocator never uses it

def test_stale_counter_warn_fires_and_allocator_stays_authoritative(tmp_path):
    registry = make_registry(
        [("SN-0001", "IB-A"), ("SN-0002", "IB-B"), ("SN-0003", "IB-C")],
        next_sequence=2)  # the counter points AT occupied SN-0002
    assert sn_claims.counter_is_stale(registry)

    remote = bare_remote(tmp_path)
    receipt = sn_claims.claim_number(str(remote), ib="IB-NEW", seat="Seat X",
                                     registry=registry)
    assert receipt["claim"]["number"] == 4  # a free number — never the stale 2

    warnings = door.filing_warnings(ROOT, registry, [], None)
    assert [w["kind"] for w in warnings] == ["COUNTER_STALE"]


def test_counter_repair_sets_high_water_and_demotes_to_advisory():
    registry = make_registry(
        [("SN-0001", "IB-A"), ("SN-0003", "IB-C")], next_sequence=2)
    repaired = sn_claims.repair_counter(registry)
    assert repaired == 4
    assert registry["sequence_policy"]["next_sequence"] == 4
    assert registry["sequence_policy"]["counter_role"] == "advisory"
    assert not sn_claims.counter_is_stale(registry)
    # Idempotent: repairing a healthy counter changes nothing.
    assert sn_claims.repair_counter(registry) == 4


# --------------------------------------------------------------------------
# The unclaimed filing: WARN in range mode; silent once claimed

def _mini_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "tools").mkdir(parents=True)
    shutil.copy(ROOT / "tools" / "sn_claims.py", root / "tools" / "sn_claims.py")
    git(root, "init", "-q", ".")
    git(root, "config", "user.name", "Guard Test")
    git(root, "config", "user.email", "guard-test@nayanet.local")
    git(root, "commit", "-q", "--allow-empty", "-m", "seed")
    return root


def test_unclaimed_number_in_filing_range_warns(tmp_path):
    root = _mini_root(tmp_path)
    registry = make_registry([("SN-2001", "IB-OLD")], next_sequence=2002)
    page = {"sn": "SN-2002", "ib": "IB-NEW", "path": "BRAIN/05-MEMORY/SMART-NOTES/x.md"}

    warnings = door.filing_warnings(root, registry, [page], "HEAD~1..HEAD")
    assert [w["kind"] for w in warnings] == ["UNCLAIMED_NUMBER"]
    assert warnings[0]["sn"] == "SN-2002"

    # Anchor the claim in this very repo; the warning must clear.
    receipt = sn_claims.claim_number(str(root), ib="IB-NEW", seat="Seat X",
                                     registry=registry)
    assert receipt["claim"]["number"] == 2002
    assert door.filing_warnings(root, registry, [page], "HEAD~1..HEAD") == []

    # Full-tree mode never re-litigates the pre-guard corpus.
    assert door.filing_warnings(root, registry, [page], None) == []


# --------------------------------------------------------------------------
# The normal filing, end to end + fail-closed

def test_single_filing_claims_next_free_and_is_idempotent(tmp_path):
    remote = bare_remote(tmp_path)
    registry = make_registry([("SN-0007", "IB-A")], next_sequence=8)

    first = sn_claims.claim_number(str(remote), ib="IB-X", seat="Seat X",
                                   registry=registry)
    assert first["claim"]["sn"] == "SN-008"  # the allocator's canonical form
    assert first["attempts"] == 1 and first["renumbered_from"] is None

    claims = sn_claims.read_claims(remote)
    assert claims[8]["intelligent_block_id"] == "IB-X"
    assert claims[8]["seat"] == "Seat X"

    again = sn_claims.claim_number(str(remote), ib="IB-X", seat="Seat X",
                                   registry=registry)
    assert again["claim"]["number"] == 8  # same block, same number — no burn
    assert sorted(sn_claims.read_claims(remote)) == [8]

    other = sn_claims.claim_number(str(remote), ib="IB-Y", seat="Seat Y",
                                   registry=registry)
    assert other["claim"]["number"] == 9


def test_claim_cli_refuses_without_a_registry(tmp_path):
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "sn_claims.py"), "claim",
         "--ib", "IB-X", "--seat", "Seat X",
         "--registry", str(tmp_path / "no-such-registry.json"),
         "--repo", str(tmp_path)],
        capture_output=True, text=True)
    assert r.returncode == 1
    assert "CLAIM REFUSED" in r.stderr  # fail closed — never a guessed number
