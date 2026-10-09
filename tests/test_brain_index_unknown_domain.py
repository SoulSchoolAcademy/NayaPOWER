"""Guards for the brain-index generator's domain classification tables.

Regression context (2026-10-09): BRAIN/00-ACTIVATION/ landed (Naya Activation
Package v1, PR #1971) without being registered in the generator's domain
tables, and `regenerate_brain_index.py --check` died with a bare
`KeyError: '00-ACTIVATION'` instead of a governed diagnosis. These tests pin
the repair: deliberate registration of the new domain, loud governed failure
for any future unregistered domain, and a mechanical guard that enumerates
the real git tree so no new domain can slip through unnoticed again.
"""

import subprocess
from pathlib import Path

import pytest

from tools import regenerate_brain_index as brain_index

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_activation_domain_is_registered():
    assert brain_index.domain_title("00-ACTIVATION") == "00-ACTIVATION — Activation"
    assert brain_index.BASELINE_DOMAIN_FLOORS["00-ACTIVATION"] == 2


def test_unknown_domain_fails_loud_with_governed_diagnosis():
    with pytest.raises(RuntimeError) as excinfo:
        brain_index.domain_title("88-NEWTHING")
    message = str(excinfo.value)
    assert "88-NEWTHING" in message
    assert "BASELINE_DOMAIN_FLOORS" in message
    assert "DOMAIN_TITLES" in message


def test_unknown_domains_detects_unclassified():
    counts = {"00-SPEC": 15, "88-NEWTHING": 3}
    assert brain_index.unknown_domains(counts) == ["88-NEWTHING"]


def test_all_classified_domains_are_quiet():
    counts = {d: 1 for d in brain_index.registered_domains()}
    assert brain_index.unknown_domains(counts) == []


def _brain_domains_in_git_tree() -> list[str]:
    out = subprocess.run(
        ["git", "ls-tree", "--name-only", "HEAD", "--", "BRAIN/"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if out.returncode != 0:
        pytest.skip("not running inside the NayaPOWER git tree")
    domains = set()
    for line in out.stdout.splitlines():
        parts = line.split("/")
        if len(parts) > 2 and parts[1] not in ("REAL-TREE.json", "REAL-TREE.md"):
            domains.add(parts[1])
    return sorted(domains)


def test_every_domain_in_git_tree_is_registered():
    """The mechanical guard: the tables must cover every BRAIN domain on disk."""
    unregistered = [
        d for d in _brain_domains_in_git_tree() if d not in brain_index.registered_domains()
    ]
    assert unregistered == [], (
        f"unregistered BRAIN domain(s) {unregistered}: add deliberate entries to "
        "BASELINE_DOMAIN_FLOORS and DOMAIN_TITLES with a comment naming the "
        "landing PR and the reason"
    )


def test_ratchet_still_catches_deletion_in_activation_domain():
    files = [{"path": "BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md"}]
    floors = brain_index.floor_domain_counts(files)
    actual = brain_index.domain_counts(files)
    violations = brain_index.floor_violations(actual, floors)
    assert any(v.startswith("00-ACTIVATION:") for v in violations)
