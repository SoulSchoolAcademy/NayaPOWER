"""Round-2 hardening tests for law-encoding BATCH 2 (2026-10-09).

The independent re-validator scored the round-1 hardened branch 8.9 and
named 2 residual gaps (report #1354, comment 6086628793). Each gap gets:
tests proving the RESIDUAL fails post-fix, tests proving the HONORING
side still passes, and tests PINNING the newly honest documented bounds
(a bound in a test name that says DOCUMENTED is an admitted limit, not a
feature).

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_batch2_r2_20261009.py
Also pytest-compatible (plain assert functions).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import two_layer  # noqa: E402

TECHNICAL = (
    "The GitHub Actions artifact zip endpoint 401s when the authd-surrogate "
    "Bearer is sent through the redirect: the API 302-redirects to a "
    "pre-signed blob URL and the surrogate is rejected at the blob host."
)
PLAIN_GOOD = (
    "Literally what I'm saying: imagine ordering a package, and the "
    "delivery driver is allowed into the building but the door of your "
    "apartment rejects his badge. The first door works, the second "
    "door doesn't."
)

# The re-validator's exact Gap-3 counter-examples (comment 6086628793).
CHOPPY_JARGON = (
    "In other words: the CSI driver choked. PVs stuck. Kubelet flapped. "
    "Restarts looped. Nodes drained."
)
GENUINE_PLAIN = (
    "In other words, imagine the authentication handshake between the "
    "deployment pipeline and the image registry failed. Think of it like "
    "a key card that stopped working."
)

# Real two-layer literal layers from #1354, verbatim (provenance: the
# comment id in each name). Written by seats BEFORE the check existed, so
# they are measured on the Flesch axis only — the honest claim is "real
# reports clear the wall with margin", not "every real report passes the
# full check".
CORPUS_6086636048 = (
    """We found the actual reason learning still cannot finish: saving the note and writing its visible Smart Note link are two separate steps. Saving can succeed while GitHub refuses to publish the link. We improved the system so the next refusal will tell us why, and the automated test suite passed all 11 checks. But those tests use a simulated refusal; nobody has yet run the changed code against the real production receiver, and the changed code is not deployed. So I am not calling learning activated yet."""
)
CORPUS_6086661723 = (
    """I turned the two-part update rule into a written law and added it to the instructions every repository agent is required to read at startup. It now says: show the technical proof first, then explain it in everyday words. That change is waiting for review and merge, so I won't pretend every running agent has already loaded it.

The learning blocker is no longer score-contract confusion: Naya 1 has ratified one score ladder. The first live break is that the note can be saved while GitHub refuses to publish its Smart Note page. We have tested the diagnostic fix in CI, but the production system has not yet run that new code."""
)
CORPUS_6086599220 = (
    """You wrote house rules: every wall black, no white paint, ever. Then you hired a guard to check every room. He walked into your own showroom \u2014 the one you designed, approved, and love \u2014 and wrote up violations on nearly every shelf: the glint on your jewel buttons, the shine on the toggle knob, the prism mark on the special button, the shimmer sweep, the colored bars. By the letter of the rules, he's right. But the showroom was beautiful before the rules were written, and you approved every sparkle. So this isn't a fight between a right side and a wrong side \u2014 both sides are yours. The only question is which one you want to bend. I'm not bending anything until you pick."""
)


def _report(plain):
    return {
        "report_type": "deliverable_report",
        "title": "t",
        "technical": TECHNICAL,
        "plain_human": plain,
    }


# ---------------- Gap 2, round 2: aggregate content accounting
def test_r2_split_across_fields_voids():
    # The re-validator's exact residual: 200+200 chars stays a ping.
    rec = {"report_type": "status_ping", "title": "x" * 200,
           "message": "x" * 200}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")
    assert "400 chars" in r["details"]["exemption_voided"]


def test_r2_split_across_unlisted_field_names_voids():
    # Field names never enumerated anywhere: the aggregate does not care.
    rec = {"report_type": "ack", "alpha": "x" * 150, "beta": "x" * 150}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_r2_non_str_list_payload_voids():
    # The re-validator's exact residual: a 600-word list payload.
    rec = {"report_type": "status_ping", "title": "ping",
           "payload": ["word"] * 600}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_r2_nested_dict_payload_voids():
    rec = {"report_type": "status_ping", "title": "ping",
           "nested": {"level": {"deep": "x" * 400}}}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_r2_blocker_x_on_ping_voids():
    # The re-validator's exact residual: 5000-char blocker_x on a ping.
    rec = {"report_type": "status_ping", "title": "ping",
           "blocker_x": "x" * 5000}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")
    assert "blocker_x" in r["details"]["exemption_voided"]


def test_r2_short_blocker_x_on_ping_voids_too():
    # Report-shaped fields void on PRESENCE: a ping never carries one,
    # consistent with the round-1 short-technical rule.
    rec = {"report_type": "status_ping", "title": "ping",
           "blocker_x": "ci is red"}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_r2_unblock_action_on_ping_voids():
    rec = {"report_type": "status_ping", "title": "ping",
           "unblock_action": "restart the runner"}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_r2_aggregate_boundary_total_299_still_ping():
    # The boundary is TOTAL content now: 290 + 9 (title) = 299 -> ping.
    rec = {"report_type": "status_ping", "title": "123456789",
           "message": "x" * 290}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert "exemption_voided" not in r["details"]


def test_r2_aggregate_boundary_total_300_voids():
    # 291 + 9 (title) = 300 -> voided.
    rec = {"report_type": "status_ping", "title": "123456789",
           "message": "x" * 291}
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_r2_legit_ping_with_metadata_still_passes():
    # Honoring side: a real ping with seat metadata and a small list.
    rec = {"report_type": "status_ping", "title": "still working",
           "seat": "naya-5", "checked_at": "2026-10-09T18:05:00Z",
           "tags": ["ci", "green"]}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]


def test_r2_numbers_and_bools_are_not_content():
    # Non-text scalars carry no prose: big numbers do not void a ping.
    rec = {"report_type": "ack", "title": "ok",
           "attempt": 5000, "retry": True, "ratio": 99.99}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]


def test_r2_voided_split_but_honored_still_passes():
    # Content decides the PATH, not the verdict: split content that IS
    # two-layered passes via the consequential path.
    rec = {"report_type": "status_ping", "title": "x" * 200,
           "technical": TECHNICAL, "plain_human": PLAIN_GOOD}
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert r["details"].get("exemption_voided")


# ---------------- Gap 3, round 2: honest bounds, pinned
def test_r2_choppy_jargon_passes_documented_bound():
    # ADMITTED BOUND (not a feature): Flesch rewards shortness, not
    # plainness. The re-validator's live counterexample scores 62.8 and
    # passes. If this test ever FAILS, the docs are wrong, not the code.
    r = two_layer.check(_report(CHOPPY_JARGON))
    ease = two_layer._flesch_reading_ease(CHOPPY_JARGON)
    assert ease >= 50.0, ease
    assert r["pass"] is True, r["reasons"]


def test_r2_genuine_plain_false_negative_documented():
    # ADMITTED FALSE NEGATIVE: a genuine flowing explanation that must
    # name technical things scores below 50 and fails. The docs admit
    # this; the test pins the admission so it cannot silently regress
    # into a pretended wall.
    r = two_layer.check(_report(GENUINE_PLAIN))
    ease = two_layer._flesch_reading_ease(GENUINE_PLAIN)
    assert ease < 50.0, ease
    assert r["pass"] is False, r["reasons"]
    assert "Flesch" in r["reasons"][0]


def test_r2_sprinkle_and_paraphrase_attacks_still_die():
    # The wall's REAL job, kept: lazy jargon attacks die here.
    sprinkle = (
        "The authentication surrogate token propagation mechanism "
        "experienced a 401 authorization rejection at the pre-signed "
        "blob storage endpoint after the API redirect; in other words, "
        "the credential relay subsystem failed validation."
    )
    paraphrase = (
        "In other words: the compressed artifact retrieval endpoint "
        "returns an unauthorized status when the credential delegation "
        "token traverses the redirection to the signed storage URL, "
        "because the delegation credential is refused at the storage host."
    )
    for attack in (sprinkle, paraphrase):
        r = two_layer.check(_report(attack))
        assert r["pass"] is False, r["reasons"]
        assert "Flesch" in r["reasons"][0]


def test_r2_real_corpus_flesch_clears_wall_with_margin():
    # The honest calibration claim: real two-layer reports from #1354
    # (n=3 sampled 2026-10-09) clear 50 with margin. Measured on the
    # Flesch axis only — these predate the signal requirement.
    for name, sample in (
        ("6086636048", CORPUS_6086636048),
        ("6086661723", CORPUS_6086661723),
        ("6086599220", CORPUS_6086599220),
    ):
        ease = two_layer._flesch_reading_ease(sample)
        assert ease >= 50.0, (name, ease)


def test_r2_honoring_fixture_still_passes():
    r = two_layer.check(_report(PLAIN_GOOD))
    assert r["pass"] is True, r["reasons"]
    assert r["details"]["plain_flesch"] >= 50.0


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
