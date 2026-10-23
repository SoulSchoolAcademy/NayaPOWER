"""Regression: legacy Hub concepts cannot become an alternate published app.

The single production source contract is tools.hub_deploy.HUB_SOURCE_DIR
(HUB/app). Historical root pages and concept generations remain readable
in Git history but must never be included in the deployment source package.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import hub_deploy as hd


def _git(repo, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "hub-guard",
           "GIT_AUTHOR_EMAIL": "hub-guard@example.invalid",
           "GIT_COMMITTER_NAME": "hub-guard",
           "GIT_COMMITTER_EMAIL": "hub-guard@example.invalid"}
    return subprocess.run(["git", *args], cwd=repo, env=env,
                          check=True, capture_output=True, text=True).stdout.strip()


def test_hub_deployment_uses_single_canonical_source():
    assert hd.HUB_SOURCE_DIR == ROOT / "HUB" / "app"
    assert (hd.HUB_SOURCE_DIR / "index.html").is_file()


def test_legacy_root_and_concepts_cannot_enter_published_bundle(tmp_path):
    repo = tmp_path / "repo"
    current = repo / "HUB" / "app"
    current.mkdir(parents=True)
    (current / "index.html").write_text("CURRENT_HUB", encoding="utf-8")
    (repo / "HUB" / "NAYANET INTERFACE CONCEPT.html").write_text(
        "OLD_CONCEPT", encoding="utf-8")
    (repo / "index.html").write_text("OLD_ROOT_APP", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "fixture")
    head = _git(repo, "rev-parse", "HEAD")

    extracted = hd.extract_hub_source_at_ref(head, tmp_path / "extracted", repo=repo)
    assert extracted == tmp_path / "extracted" / "HUB" / "app"
    assert sorted(p.relative_to(extracted).as_posix()
                  for p in hd.collect_hub_files(extracted)) == ["index.html"]

    deployed = tmp_path / "published"
    hd.CopyAdapter(deployed).publish(extracted, head)
    assert (deployed / "index.html").read_text(encoding="utf-8") == "CURRENT_HUB"
    assert sorted(p.relative_to(deployed).as_posix()
                  for p in deployed.rglob("*") if p.is_file()) == ["index.html"]
