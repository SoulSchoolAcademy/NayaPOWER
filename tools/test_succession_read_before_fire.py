#!/usr/bin/env python3
"""Self-tests for tools/succession_read_before_fire.py.

Zero API: the venue read (read_venue_issue) is monkeypatched — only the pure
extractors and the CLI's fail-closed paths run. Exit 0 = all pass.
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("srb", HERE / "succession_read_before_fire.py")
srb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srb)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f" — {detail}"))


def run_main(pkg_text, venue_body=None, venue_err=None):
    """Run main() with a fake package file and a monkeypatched venue read.
    Returns (exit_code, venue_call_count)."""
    calls = {"n": 0}

    def fake_read(number):
        calls["n"] += 1
        assert str(number) == "1599", f"venue issue must be 1599, got {number}"
        return (venue_body, None) if venue_err is None else (None, venue_err)

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(pkg_text)
        pkg = f.name
    real = srb.read_venue_issue
    srb.read_venue_issue = fake_read
    old = sys.argv
    sys.argv = ["succession_read_before_fire.py", "--venue-issue", "1599", "--package", pkg]
    try:
        rc = srb.main()
    finally:
        sys.argv = old
        srb.read_venue_issue = real
        os.unlink(pkg)
    return rc, calls["n"]


VENUE_LIVE = "[#2721 — Team coordination feed — live board](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721)"

# T1: consumed board vs live board -> exit 2 fail-closed, venue read exactly once
rc, n = run_main("[TEAM NAYA] feed (successor to #2641)", venue_body=VENUE_LIVE)
check("T1 stale-package refused", rc == 2 and n == 1, f"rc={rc} calls={n}")

# T2: package names the live board -> exit 0 FIRE ALLOWED
rc, n = run_main("[TEAM NAYA] feed (successor to #2721)", venue_body=VENUE_LIVE)
check("T2 live-package allowed", rc == 0 and n == 1, f"rc={rc} calls={n}")

# T3: unparseable package (no successor line) -> exit 2, venue never read
rc, n = run_main("a draft with no board reference at all", venue_body=VENUE_LIVE)
check("T3 unparseable fail-closed, no venue read", rc == 2 and n == 0, f"rc={rc} calls={n}")

# T4: venue body has no live-board line -> exit 2
rc, n = run_main("[TEAM NAYA] feed (successor to #2721)", venue_body="no live board line here")
check("T4 venue-without-live-line fail-closed", rc == 2 and n == 1, f"rc={rc} calls={n}")

# T5: extractor unit checks
check("T5 extract_package_source paren form", srb.extract_package_source("x (successor to #2641) y") == "2641")
check("T5 extract_package_source arrow form", srb.extract_package_source("#2641 -> successor") == "2641")
check("T5 extract_package_source no match", srb.extract_package_source("nothing here") is None)
check("T5 extract_live_board", srb.extract_live_board(VENUE_LIVE) == "2721")
check("T5 extract_live_board no match", srb.extract_live_board("plain text") is None)

# T6: NAYA_GH_API env overrides the default gh-api path
os.environ["NAYA_GH_API"] = "/tmp/fake-gh-api"
try:
    spec2 = importlib.util.spec_from_file_location("srb2", HERE / "succession_read_before_fire.py")
    m2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(m2)
    check("T6 env override honored", m2.GH_API == "/tmp/fake-gh-api", f"got {m2.GH_API}")
finally:
    del os.environ["NAYA_GH_API"]
check("T6 default path intact", srb.GH_API == "/home/hatch/workspace/naya/bin/gh-api", f"got {srb.GH_API}")

print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
sys.exit(0 if not FAIL else 1)
