"""Factory standard-feature contracts — checker, certification baseline,
and the R1b direct-build door cure.

The contracts live in templates-registry.json (the file the engine reads)
under `standard_feature_contracts`; the checker is
engine/check_standard_features.py; the direct-build door is
engine/build-api.py.

The Personal baseline below is the 2026-10-22 certification measurement
(first measurement entry on the Smart Factory board, #2883): the flagship
base passes 5 of 13 standard features. When a future cure improves the
base, update EXPECTED_PERSONAL in the same PR — the baseline moving is
the proof the cure worked.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "BRAIN" / "10-INTERFACES" / "SMART-FACTORY-CANON" / "engine"
REGISTRY_PATH = ENGINE / "templates-registry.json"

sys.path.insert(0, str(ENGINE))

import check_standard_features as checker  # noqa: E402


def _load_build_api():
    spec = importlib.util.spec_from_file_location(
        "build_api", ENGINE / "build-api.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def personal_report(registry):
    body, metadata = checker.load_target(
        None, REGISTRY_PATH, registry, "personal"
    )
    return checker.evaluate(body, metadata, registry)


# --- contracts themselves -------------------------------------------------

def test_contracts_are_valid_and_complete(registry):
    assert checker.validate_contracts(registry) == []
    features = registry["standard_feature_contracts"]["features"]
    assert [f["code"] for f in features] == [f"S{n}" for n in range(1, 14)]
    for feature in features:
        assert feature["promise"]
        assert feature["pass_standard"]
        assert feature["checks"], feature["id"]


# --- certification baseline: the Personal flagship base -------------------

EXPECTED_PERSONAL = {
    "S1": "PASS",   # Settings
    "S2": "FAIL",   # Install as App inside Settings — no manifest/SW/control
    "S3": "FAIL",   # Working communication — Message button has no handler
    "S4": "PASS",   # Changeable main picture
    "S5": "PASS",   # + button home
    "S6": "PASS",   # About
    "S7": "FAIL",   # Cross-page sync — labels/routes only, no sync channel
    "S8": "FAIL",   # Today's Intel — static seed, no data source
    "S9": "FAIL",   # Smart Growth email invites — no surface at all
    "S10": "FAIL",  # Reports — no in-app surface
    "S11": "FAIL",  # Intelligent Library / Q&A shell — no in-app surface
    "S12": "FAIL",  # Hub apps — Lists/Mail surfaces present but inert
    "S13": "PASS",  # Scrolling Smart Tabs
}


def test_personal_flagship_certification_baseline(personal_report):
    observed = {f["code"]: f["status"] for f in personal_report["features"]}
    assert observed == EXPECTED_PERSONAL
    assert personal_report["score"] == {"passed": 5, "total": 13}
    assert personal_report["target"]["registry_md5_matches"] is True


# --- negative control: a template missing a feature must FAIL it ----------

def test_negative_control_missing_smart_tabs_fails_s13(registry):
    body, metadata = checker.load_target(
        None, REGISTRY_PATH, registry, "personal"
    )
    html = body.decode("utf-8")
    stripped = html.replace('id="smarttabs"', 'id="smarttabs-removed"')
    stripped = stripped.replace(
        'data-fn="smart-tabs"', 'data-fn="smart-tabs-removed"'
    )
    assert stripped != html
    report = checker.evaluate(
        stripped.encode("utf-8"), metadata, registry
    )
    by_code = {f["code"]: f for f in report["features"]}
    assert by_code["S13"]["status"] == "FAIL"
    assert "smart-tabs-mount" in by_code["S13"]["failed_required_checks"]


def test_negative_control_missing_settings_fails_s1_and_s2(registry):
    body, metadata = checker.load_target(
        None, REGISTRY_PATH, registry, "personal"
    )
    html = body.decode("utf-8")
    stripped = html.replace('id="settings"', 'id="settings-removed"')
    assert stripped != html
    report = checker.evaluate(stripped.encode("utf-8"), metadata, registry)
    by_code = {f["code"]: f["status"] for f in report["features"]}
    assert by_code["S1"] == "FAIL"
    assert by_code["S2"] == "FAIL"


# --- positive control: a real install path passes S2 ----------------------

def test_positive_control_install_path_passes_s2(registry):
    body, metadata = checker.load_target(
        None, REGISTRY_PATH, registry, "personal"
    )
    html = body.decode("utf-8")
    cured = html.replace(
        "</head>",
        '<link rel="manifest" href="/manifest.json"></head>',
        1,
    )
    cured = cured.replace(
        '<div class="ph-sec" id="settings">',
        '<div class="ph-sec" id="settings">'
        '<button id="installapp">Install app</button>',
        1,
    )
    cured = cured.replace(
        "</body>",
        "<script>"
        "window.addEventListener('beforeinstallprompt',function(e){"
        "e.preventDefault();window.__dip=e;});"
        "document.getElementById('installapp').addEventListener('click',"
        "function(){if(window.__dip){window.__dip.prompt();}});"
        "if('serviceWorker' in navigator){"
        "navigator.serviceWorker.register('/sw.js');}"
        "</script></body>",
        1,
    )
    assert cured != html
    report = checker.evaluate(cured.encode("utf-8"), metadata, registry)
    by_code = {f["code"]: f["status"] for f in report["features"]}
    assert by_code["S2"] == "PASS"


# --- checker CLI ----------------------------------------------------------

def test_checker_cli_registry_only(capsys):
    assert checker.main(["--registry-only"]) == 0
    assert "13 features" in capsys.readouterr().out


def test_checker_cli_template_personal_exit_1_while_features_missing(capsys):
    assert checker.main(["--template", "personal", "--format", "json"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["score"] == {"passed": 5, "total": 13}


def test_checker_missing_template_key_is_an_honest_error(registry):
    with pytest.raises(ValueError, match="not buildable"):
        checker.load_target(None, REGISTRY_PATH, registry, "today")


# --- R1b: the direct-build door (build-api.py) ----------------------------

def test_build_api_uses_registry_and_returns_ledger():
    build_api = _load_build_api()
    calls = []

    def fake_deploy(path, worker):
        calls.append((path, worker))
        return "https://naya-app-testbistro.example.workers.dev"

    receipt = build_api.build_app(
        {
            "template": "personal",
            "name": "Test Bistro",
            "handle": "testbistro",
            "about": "A tiny test bistro for the direct-build door.",
        },
        deploy_fn=fake_deploy,
        enable_subdomain_fn=lambda worker: True,
    )
    assert receipt["status"] == "deployed"
    assert receipt["url"].endswith("example.workers.dev")
    assert receipt["worker"] == "naya-app-testbistro"
    assert receipt["template_file"] == "templates/personal.html"
    assert receipt["template_md5"] == "1b44636b7758dba0b95356211f8b042b"
    ledger = {row["field"]: row["status"] for row in receipt["ledger"]}
    assert ledger["name"] == "APPLIED"
    assert ledger["about"] == "APPLIED"
    assert calls and calls[0][1] == "naya-app-testbistro"


def test_build_api_missing_template_fails_without_deploying():
    build_api = _load_build_api()
    calls = []
    result = build_api.build_app(
        {"template": "today", "name": "Today App"},
        deploy_fn=lambda path, worker: calls.append(worker),
        enable_subdomain_fn=lambda worker: True,
    )
    assert "error" in result and "no base yet" in result["error"]
    assert calls == []


def test_build_api_unknown_template_fails_without_deploying():
    build_api = _load_build_api()
    result = build_api.build_app(
        {"template": "no-such-template", "name": "Nope"},
        deploy_fn=lambda path, worker: "https://should-not-happen.example",
        enable_subdomain_fn=lambda worker: True,
    )
    assert "error" in result and "unknown template" in result["error"]


def test_build_api_requires_name_and_template():
    build_api = _load_build_api()
    assert "error" in build_api.build_app({"name": "x"})
    assert "error" in build_api.build_app({"template": "personal"})
