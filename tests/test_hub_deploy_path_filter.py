"""Hub deployment must only react to deployable runtime inputs."""
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-hub-cloudflare.yml"


def test_hub_deploy_scope_excludes_content_only_feed_landings():
    text = WORKFLOW.read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^on:\n\s+push:\n\s+branches: \[main\]\n\s+paths:\n(?P<paths>(?:\s+- [^\n]+\n)+)",
        text,
    )
    assert match, "Hub deploy must have an explicit push-path contract"
    paths = [re.sub(r"^\s+-\s+|[\"']", "", line).strip()
             for line in match.group("paths").splitlines()]
    assert "HUB/**" not in paths, "broad HUB/** retriggers deployment for feed/content-only writes"
    assert "HUB/app/**" in paths
    assert "HUB/hub-worker.js" in paths
    assert "HUB/wrangler.toml" in paths
    assert not any(path.startswith("HUB/FEEDS") for path in paths)
