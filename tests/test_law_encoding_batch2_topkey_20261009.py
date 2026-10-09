"""Top-level-key narrow fix tests (2026-10-09).

The round-2 independent re-validator found ONE genuine new hole in the
hardened class (probes A4/D9 in /tmp/r2_probes.py, log /tmp/r2_probe_log.txt):
`_aggregate_content` counted nested dict keys but never the record's own
top-level field names — so {"report_type": "status_ping", "<400 chars of
English prose as the key>": ""} passed as an exempt ping with 0 chars
counted, contradicting the documented guarantee "dict keys count too" /
"total text chars across ALL fields (any name...)".

The fix: `_aggregate_content` now counts top-level field names exactly as
nested dict keys are counted (`_content_chars(key) + _content_chars(val)`).
This file proves the residual fails post-fix, proves the honoring side
still passes, and pins the 299/300 boundary exact on total content
INCLUDING field names.

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_batch2_topkey_20261009.py
Also pytest-compatible (plain assert functions).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import two_layer  # noqa: E402

# The re-validator's exact honoring fixtures (/tmp/r2_probes.py, verbatim).
TECH_FRESH = (
    "The nightly PDF job died at import: reportlab was missing from the "
    "job's Python, so the hourly report never rendered and the feed slot "
    "stayed empty until morning."
)
PLAIN_FRESH = (
    "Literally what I'm saying: think of a bakery whose ovens never got "
    "delivered. The bakers showed up, the recipe was ready, but with no "
    "heat there was no bread. We ordered the ovens, and now the bread "
    "bakes on time."
)


def _prose_key(n: int) -> str:
    """Exactly n chars of English prose as a field name — the task's own
    example shape: '<400 chars of English prose as the key>'."""
    prose = (
        "this field name is actually a whole paragraph of plain english prose "
        "smuggled into the key position where no content check that only "
        "reads values will ever see it, so the quick ping exemption stays "
        "wide open and the report slips through without anyone noticing "
        "what is really going on here, which is exactly the trick this "
        "narrow fix closes for good and all, no exceptions, period. "
    )
    key = (prose * ((n // len(prose)) + 1))[:n]
    assert len(key) == n, len(key)
    return key


# ---------------- the residual, post-fix
def test_topkey_400_char_key_voids():
    # The re-validator's exact failing probes A4/D9: a 400-char top-level
    # key with an empty value is 400 chars of content, not an empty field.
    rec = {"report_type": "status_ping", "k" * 400: ""}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")
    assert "400 chars" in r["details"]["exemption_voided"]


def test_topkey_english_prose_key_voids():
    # The task's exact example: English prose as the key, empty value.
    rec = {"report_type": "status_ping", _prose_key(400): ""}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_topkey_300_char_key_voids_at_boundary():
    # ">=300-char top-level field name voids": exactly 300 counts.
    rec = {"report_type": "ack", "k" * 300: ""}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_topkey_299_char_key_alone_still_ping():
    # Boundary exactness from below: 299 chars of key alone is still a ping.
    rec = {"report_type": "status_ping", "k" * 299: ""}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert "exemption_voided" not in r["details"]


def test_topkey_nested_key_behavior_unchanged():
    # The re-validator's other half: nested 400-char keys already voided
    # pre-fix, and still void post-fix. The fix only closes the top-level
    # residual; nested behavior is untouched.
    rec = {"report_type": "ack", "outer": {"k" * 400: ""}}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_topkey_299_300_boundary_exact_with_names():
    # The 300 boundary is exact on TOTAL content including field names:
    # title (5+9) + message key (7) + 278 = 299 -> ping; 279 -> 300 -> void.
    rec = {"report_type": "status_ping", "title": "123456789",
           "message": "x" * 278}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert "exemption_voided" not in r["details"]

    rec = {"report_type": "status_ping", "title": "123456789",
           "message": "x" * 279}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


# ---------------- honoring side: honest records still pass
def test_topkey_bare_ping_passes():
    # Re-validator probe B1, verbatim.
    r = two_layer.check({"report_type": "status_ping", "title": "still here"})
    assert r["pass"] is True, r["reasons"]
    assert "exemption_voided" not in r["details"]


def test_topkey_ping_with_metadata_passes():
    # Re-validator probe B2, verbatim: fresh metadata under 300 stays cheap.
    rec = {"report_type": "ack", "seat": "naya-5", "run": "hv-20261009-xyz",
           "tags": ["alpha", "beta"], "attempt": 3, "ok": True}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert "exemption_voided" not in r["details"]


def test_topkey_voided_but_two_layered_passes():
    # Re-validator probe B3, verbatim: content voids the exemption, but
    # the record IS two-layered, so it passes via the consequential path.
    rec = {"report_type": "status_ping", "frag1": "x" * 150,
           "frag2": "y" * 150, "technical": TECH_FRESH,
           "plain_human": PLAIN_FRESH}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert r["details"].get("exemption_voided")


# ---------------- battery replay: the claim, now replayable from the repo
def test_topkey_battery_fixture_all_die_at_wall():
    # The Gap-3 battery fixture (tests/fixtures/gap3_battery_attacks.json):
    # every attack dies at the abstraction-density wall, and the measured
    # densities match the pinned independent measurements (the function is
    # deterministic). Re-pinned on the density axis 2026-10-09 when the
    # clarity rewrite replaced the Flesch wall (see fixture _doc).
    fixture = json.loads(
        (ROOT / "tests" / "fixtures" / "gap3_battery_attacks.json").read_text()
    )
    technical = fixture["technical"]
    assert len(fixture["attacks"]) == 6, "fixture must carry all 6 attacks"
    for attack in fixture["attacks"]:
        density, hits = two_layer._abstraction_density(attack["plain_human"])
        assert density >= 0.10, (attack["id"], density, hits)
        assert abs(density - attack["measured_abstraction"]) < 0.005, (
            attack["id"], density, attack["measured_abstraction"])
        r = two_layer.check({
            "report_type": "deliverable_report",
            "title": attack["id"],
            "technical": technical,
            "plain_human": attack["plain_human"],
        })
        assert r["pass"] is False, (attack["id"], r["reasons"])
        assert "abstraction" in r["reasons"][0], (attack["id"], r["reasons"])


# ---------------------------------------------------------------- runner
def main() -> int:
    fns = sorted((n, f) for n, f in globals().items()
                 if n.startswith("test_") and callable(f))
    failures = []
    for name, fn in fns:
        try:
            fn()
            print(f"  ok {name}")
        except AssertionError as e:
            failures.append(name)
            print(f"  FAIL {name}: {e}")
        except Exception as e:  # noqa: BLE001
            failures.append(name)
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - len(failures)}/{len(fns)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
